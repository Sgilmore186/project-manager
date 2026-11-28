#!/usr/bin/env python3
"""Orchestration safety checks for the central Development Boards.

Deterministic, read-only, Python standard library only (3.9+). It never edits
or pushes anything. Duet, Codex, Claude Code and scheduled routines run it
before they dispatch, claim, push or start the next task.

Commands (run from the repo root):
  python3 scripts/control.py status                 RUN (exit 0) or STOPPED (exit 3)
  python3 scripts/control.py claims [--stale-hours H]
  python3 scripts/control.py ready PROJECT [--allow-test]
  python3 scripts/control.py overlap PROJECT TASK_ID

Exit codes: 0 ok, 2 usage or missing board/task, 3 not safe to start
(STOP set, board not active, claim held), 4 path overlap with active work.
"""
import argparse, datetime as dt, fnmatch, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACTIVE_TASK = ("in-progress", "dispatched")
NO_OWNER = ("", "none", "-")


def root():
    return os.environ.get("PM_ROOT", ROOT)


def stop_state():
    """(stopped, reason). The STOP file at the repo root halts all agent work."""
    path = os.path.join(root(), "STOP")
    if not os.path.exists(path):
        return False, ""
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip() and not l.startswith("#")]
    return True, (lines[0] if lines else "no reason given")


def board_path(project):
    return os.path.join(root(), "development", project, "BOARD.md")


def boards():
    base = os.path.join(root(), "development")
    if not os.path.isdir(base):
        return []
    return sorted(p for p in os.listdir(base) if os.path.isfile(board_path(p)))


def field(text, name):
    m = re.search(r"^- (?:\*\*)?%s:(?:\*\*)? *(.*)$" % re.escape(name), text, re.M)
    return m.group(1).strip() if m else ""


def section(text, heading):
    m = re.search(r"^## %s\s*$(.*?)(?=^## |\Z)" % re.escape(heading), text, re.M | re.S)
    return m.group(1) if m else ""


def read_board(project):
    path = board_path(project)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    routing = section(text, "Project routing")
    claim = section(text, "Run claim")
    activation = field(routing, "Activation").split(" ")[0].strip().lower()
    return {
        "project": project,
        "repo": field(routing, "Target repository"),
        "activation": activation,
        "owner": field(claim, "Owner"),
        "run_id": field(claim, "Run ID"),
        "renewed": field(claim, "Claimed/renewed UTC"),
        "tasks": tasks(text),
    }


def tasks(text):
    out = []
    heads = list(re.finditer(r"^#{3,4} +([A-Za-z0-9][A-Za-z0-9_./-]*) +- +(.+)$", text, re.M))
    for i, h in enumerate(heads):
        body = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        status = field(body, "Status")
        if not status:
            continue  # a phase heading, not a task
        touches = [t.strip().strip("`") for t in field(body, "Touches").split(",")]
        out.append({
            "id": h.group(1),
            "title": h.group(2).strip(),
            "status": status.split(" ")[0].strip(".,;").lower(),
            "assignee": field(body, "Assignee").split(" ")[0].strip(".,;").lower(),
            "touches": [t for t in touches if t and t.lower() not in NO_OWNER],
        })
    return out


def parse_utc(value):
    m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z", value or "")
    if not m:
        return None
    return dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)


def held(board):
    return board["owner"].strip().lower() not in NO_OWNER


def overlaps(a, b):
    a, b = a.rstrip("/"), b.rstrip("/")
    if a == b or a.startswith(b + "/") or b.startswith(a + "/"):
        return True
    return fnmatch.fnmatch(a, b) or fnmatch.fnmatch(b, a)


def cmd_status(_):
    stopped, reason = stop_state()
    if stopped:
        print("STOPPED: " + reason)
        return 3
    print("RUN")
    return 0


def cmd_claims(args):
    now = dt.datetime.now(dt.timezone.utc)
    for name in boards():
        b = read_board(name)
        line = "%s [%s] owner=%s run=%s renewed=%s" % (name, b["activation"] or "?", b["owner"] or "none", b["run_id"] or "none", b["renewed"] or "none")
        when = parse_utc(b["renewed"])
        if held(b) and when:
            hours = (now - when).total_seconds() / 3600
            line += " age=%.1fh" % hours
            if hours > args.stale_hours:
                line += " STALE (check the target repo and the owner before any recovery)"
        print(line)
    return 0


def cmd_ready(args):
    stopped, reason = stop_state()
    if stopped:
        print("not ready: STOP is set (%s)" % reason)
        return 3
    b = read_board(args.project)
    if b is None:
        print("not ready: no board at development/%s/BOARD.md" % args.project)
        return 2
    allowed = ("active", "test") if args.allow_test else ("active",)
    if b["activation"] not in allowed:
        print("not ready: board activation is %r" % (b["activation"] or "missing"))
        return 3
    if held(b):
        print("not ready: run claim held by %s (%s)" % (b["owner"], b["run_id"] or "no run id"))
        return 3
    print("ready: %s" % args.project)
    return 0


def cmd_overlap(args):
    b = read_board(args.project)
    if b is None:
        print("no board at development/%s/BOARD.md" % args.project)
        return 2
    task = next((t for t in b["tasks"] if t["id"] == args.task_id), None)
    if task is None:
        print("no task %s on %s" % (args.task_id, args.project))
        return 2
    clashes = []
    for name in boards():
        other = read_board(name)
        if other["repo"].lower() != b["repo"].lower():
            continue
        for t in other["tasks"]:
            if (name, t["id"]) == (args.project, task["id"]) or t["status"] not in ACTIVE_TASK:
                continue
            hits = sorted({p for p in task["touches"] for q in t["touches"] if overlaps(p, q)})
            if hits:
                clashes.append("%s/%s (%s): %s" % (name, t["id"], t["status"], ", ".join(hits)))
    if clashes:
        print("overlap with active work:")
        for c in clashes:
            print("  " + c)
        return 4
    print("no overlap: %s/%s" % (args.project, args.task_id))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="control.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="command")
    sub.add_parser("status")
    c = sub.add_parser("claims"); c.add_argument("--stale-hours", type=float, default=6.0)
    r = sub.add_parser("ready"); r.add_argument("project"); r.add_argument("--allow-test", action="store_true")
    o = sub.add_parser("overlap"); o.add_argument("project"); o.add_argument("task_id")
    args = ap.parse_args(argv)
    if not args.command:
        ap.print_help()
        return 2
    return {"status": cmd_status, "claims": cmd_claims, "ready": cmd_ready, "overlap": cmd_overlap}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
