#!/usr/bin/env python3
"""pm.py: deterministic CRUD for the project-manager repo.

No AI. Reads and writes ideas.json and projects.json and appends one line
to log.md per change, all in one all-or-nothing save. Inside a git repo each
change is committed on its own. Only 'sync' and 'commit --push' use the network.
Works on Python 3.9+ with the standard library only.

Usage (run from anywhere; paths resolve to the repo root):
  pm.py list [ideas|projects|parts|all]
  pm.py get ID
  pm.py add idea    --id ID --name NAME --description D [--goal G] [--notes N]
  pm.py add project --id ID --name NAME --goal G --skip-idea --reason R [--description D] [--status S] [--focus F] [--stage S] [--next-step N]
  pm.py add part    --id ID --name NAME --part-of A,B [--stage S]
  pm.py update ID [--set field=value] [--add list_field=item] [--remove list_field=item] [--reason R]
  pm.py move ID --to idea|project [--goal G] [--reason R]
  pm.py done ID [--step S] [--item OPEN_ITEM] [--next N] [--reason R]
  pm.py delete ID --reason R
  pm.py check
  pm.py sync
  pm.py commit [--push]

Every write takes --date YYYY-MM-DD (default: today in US Central time), --dry-run and --no-commit.
"""
import argparse, datetime, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDEAS, PROJECTS, LOG = (os.path.join(ROOT, f) for f in ("ideas.json", "projects.json", "log.md"))
TIMEZONE = "America/Chicago"  # Seph's time zone; default dates follow his calendar day
STATUSES = ["active", "paused", "archived", "done", "dropped"]
STEP_AWAY = {"paused", "archived", "dropped"}  # leaving a project for these needs a reason
FOCUS = ["primary", "secondary", "none"]
LIST_FIELDS = {"open_items", "part_of", "aliases"}
MANAGED_FIELDS = {"progress", "project_history", "idea_history"}  # changed only by dedicated commands, never by --set
# Fields kept aside when an item moves, so moving back restores them.
PROJECT_ONLY = ["status", "focus", "stage", "next_step", "open_items", "progress", "started", "updated"]
IDEA_ONLY = ["added", "notes"]
FIELDS = {
    "idea": ["id", "name", "description", "goal", "added", "notes", "aliases", "project_history"],
    "project": ["id", "name", "description", "goal", "status", "focus", "stage", "next_step",
                "open_items", "progress", "started", "updated", "notes", "aliases", "idea_history"],
    "part": ["id", "name", "part_of", "stage", "updated", "aliases"],
}

class PMError(Exception):
    pass

# ---------- helpers ----------

def today():
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
        return datetime.datetime.now(ZoneInfo(TIMEZONE)).date().isoformat()
    except Exception:  # no zoneinfo or no tz database (some Windows installs): fixed UTC-6
        return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-6))).date().isoformat()

def valid_date(text):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text or ""):
        raise argparse.ArgumentTypeError(f"date must be YYYY-MM-DD, got '{text}'")
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a real date")
    return text

def clean(text):
    """Text for a log line: no trailing period, so sentences end with exactly one."""
    return str(text).strip().rstrip(".").strip()

def with_reason(msg, reason):
    return msg + (f" Reason: {clean(reason)}." if reason else "")

def norm(text):
    """Loose match key: case, spacing and punctuation ignored."""
    return " ".join(re.sub(r"[^\w\s]", " ", text).split()).casefold()

def whats_left(item):
    left = []
    if item.get("next_step"):
        left.append(f"next step: {item['next_step']}")
    if item.get("open_items"):
        left.append(f"open items: {', '.join(item['open_items'])}")
    return "; ".join(left) or "nothing recorded"

# ---------- data ----------

def load():
    with open(IDEAS) as f: ideas = json.load(f)
    with open(PROJECTS) as f: projects = json.load(f)
    projects.setdefault("parts", [])
    ideas["ideas"] = [with_description(x) for x in ideas.get("ideas", [])]
    for p in projects.get("projects", []):
        p.setdefault("progress", [])
    return {"ideas": ideas, "projects": projects}

def with_description(item):
    """Return item with a 'description' key placed right after 'name'."""
    if "description" in item:
        return item
    out = {}
    for k, v in item.items():
        out[k] = v
        if k == "name":
            out["description"] = ""
    out.setdefault("description", "")
    return out

def save(db, date, message):
    """Write both JSON files and the log line together: all of it lands, or none of it does."""
    db["ideas"]["updated"] = date
    db["projects"]["updated"] = date
    paths = {"ideas": IDEAS, "projects": PROJECTS}
    originals = {}
    for path in (IDEAS, PROJECTS, LOG):
        with open(path, "rb") as f:
            originals[path] = f.read()
    tmps = []
    try:
        for key, path in paths.items():
            tmp = path + ".tmp"
            tmps.append(tmp)
            with open(tmp, "w") as f:
                json.dump(db[key], f, indent=2, ensure_ascii=False)
                f.write("\n")
        for key, path in paths.items():
            os.replace(path + ".tmp", path)
        with open(LOG, "a") as f:
            f.write(f"- {date}: {message}\n")
    except Exception as e:
        for path, data in originals.items():
            try:
                with open(path, "wb") as f:
                    f.write(data)
            except Exception:
                pass
        for tmp in tmps:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
        raise PMError(f"save failed, nothing was changed: {e}")

def collections(db):
    return {"idea": db["ideas"]["ideas"], "project": db["projects"]["projects"], "part": db["projects"]["parts"]}

def find(db, id_):
    for kind, items in collections(db).items():
        for i, item in enumerate(items):
            if item.get("id") == id_:
                return kind, items, i
    raise PMError(f"no item with id '{id_}'")

def all_ids(db):
    return {x["id"] for items in collections(db).values() for x in items}

def parse_value(field, raw):
    if raw == "" or raw.lower() == "null":
        return None if field not in LIST_FIELDS else []
    if field in LIST_FIELDS:
        return [v.strip() for v in raw.split(",") if v.strip()]
    return raw

def validate(db):
    errors = []
    seen = set()
    for kind, items in collections(db).items():
        for x in items:
            id_ = x.get("id")
            if not id_ or not x.get("name"):
                errors.append(f"{kind} missing id or name: {x}")
            if id_ in seen:
                errors.append(f"duplicate id '{id_}'")
            seen.add(id_)
            unknown = [k for k in x if k not in FIELDS[kind]]
            if unknown:
                errors.append(f"{kind} '{id_}' has unknown field(s): {', '.join(unknown)}")
    rules = db["projects"].get("rules", {})
    counts = {"primary": 0, "secondary": 0}
    for p in db["projects"]["projects"]:
        if not p.get("goal"):
            errors.append(f"project '{p['id']}' has no goal")
        if p.get("status") not in STATUSES:
            errors.append(f"project '{p['id']}' has invalid status '{p.get('status')}'")
        if p.get("focus") not in FOCUS:
            errors.append(f"project '{p['id']}' has invalid focus '{p.get('focus')}'")
        prog = p.get("progress", [])
        if not isinstance(prog, list) or any(
                not isinstance(e, dict) or not e.get("date") or not e.get("step") for e in prog):
            errors.append(f"project '{p['id']}' has malformed progress (needs a list of {{date, step}})")
        if p.get("focus") in counts:
            if p.get("status") != "active":
                errors.append(f"project '{p['id']}' has focus but is not active")
            counts[p["focus"]] += 1
    if counts["primary"] > rules.get("max_primary", 1):
        errors.append(f"too many primary projects ({counts['primary']})")
    if counts["secondary"] > rules.get("max_secondary", 2):
        errors.append(f"too many secondary projects ({counts['secondary']})")
    for part in db["projects"]["parts"]:
        if not part.get("part_of"):
            errors.append(f"part '{part['id']}' has no parents")
        for parent in part.get("part_of", []):
            if parent not in seen:
                errors.append(f"part '{part['id']}' points to unknown parent '{parent}'")
    return errors

def warnings(db):
    out = [f"idea '{x['id']}' has no description" for x in db["ideas"]["ideas"]
           if not (x.get("description") or "").strip()]
    out += [f"project '{p['id']}' is active but has no focus (give it focus, or pause it with a reason)"
            for p in db["projects"]["projects"] if p.get("status") == "active" and p.get("focus") == "none"]
    return out

def commit_changes(db, date, message, dry, no_commit=False):
    errors = validate(db)
    if errors:
        raise PMError("refusing to save:\n  " + "\n  ".join(errors))
    if dry:
        print(f"[dry run] would save and log: {message}")
        return
    save(db, date, message)
    print(message)
    if not no_commit and in_git():
        git("add", "ideas.json", "projects.json", "log.md")
        r = git("commit", "-q", "-m", f"{date}: {message}", "--", "ideas.json", "projects.json", "log.md")
        if r.returncode != 0:
            print(f"warning: saved but not committed ({(r.stderr or r.stdout).strip()}). "
                  "Run 'pm.py commit' once that's fixed.", file=sys.stderr)

# ---------- commands ----------

def cmd_list(db, a):
    which = a.what
    show = {"ideas": ["idea"], "projects": ["project"], "parts": ["part"], "all": ["project", "part", "idea"]}[which]
    cols = collections(db)
    for kind in show:
        print(f"## {kind}s ({len(cols[kind])})")
        for x in cols[kind]:
            extra = ""
            if kind == "project":
                tags = [x.get("status")]
                if x.get("focus") not in (None, "none"):
                    tags.append(x["focus"])
                elif x.get("status") == "active":
                    tags.append("NO FOCUS")
                extra = f" [{', '.join(tags)}]"
            elif kind == "part":
                extra = f" (part of: {', '.join(x.get('part_of', []))})"
            print(f"- {x['id']}: {x['name']}{extra}")

def cmd_get(db, a):
    kind, items, i = find(db, a.id)
    print(json.dumps({"kind": kind, **items[i]}, indent=2, ensure_ascii=False))

def cmd_add(db, a):
    if a.id in all_ids(db):
        raise PMError(f"id '{a.id}' already exists")
    if a.kind == "idea":
        if not (a.description or "").strip():
            raise PMError("an idea needs --description (what the idea is)")
        item = {"id": a.id, "name": a.name, "description": a.description.strip(), "goal": a.goal or "",
                "added": a.date, "notes": a.notes or ""}
    elif a.kind == "project":
        if not a.skip_idea:
            raise PMError("new work goes to ideas first: 'add idea', then 'move ID --to project --goal ...'. "
                          "To skip that on purpose, pass --skip-idea with --reason")
        if not a.reason:
            raise PMError("--skip-idea needs --reason (why this skips the ideas list)")
        if not a.goal:
            raise PMError("a project needs --goal")
        item = {"id": a.id, "name": a.name, "description": a.description or "", "goal": a.goal,
                "status": a.status, "focus": a.focus, "stage": a.stage or "", "next_step": a.next_step or "",
                "open_items": [], "progress": [], "started": a.date, "updated": a.date}
    else:
        parents = parse_value("part_of", a.part_of or "")
        item = {"id": a.id, "name": a.name, "part_of": parents, "stage": a.stage or "", "updated": a.date}
    collections(db)[a.kind].append(item)
    commit_changes(db, a.date, with_reason(f"Added {a.kind} '{a.name}'.", a.reason), a.dry_run, a.no_commit)

def cmd_update(db, a):
    kind, items, i = find(db, a.id)
    item = items[i]
    before = dict(item)
    changes = []
    for flag, pairs in (("--add", a.add or []), ("--remove", a.remove or [])):
        for pair in pairs:
            if "=" not in pair:
                raise PMError(f"{flag} needs list_field=item, got '{pair}'")
            field, value = (t.strip() for t in pair.split("=", 1))
            field = field.replace("-", "_")
            if field not in LIST_FIELDS or field not in FIELDS[kind]:
                raise PMError(f"{flag} works on list fields of a {kind}: "
                              f"{', '.join(f for f in FIELDS[kind] if f in LIST_FIELDS)}")
            if not value:
                raise PMError(f"{flag} {field}= needs an item")
            current = list(item.get(field) or [])
            if flag == "--add":
                if any(norm(v) == norm(value) for v in current):
                    raise PMError(f"'{value}' is already in {field}")
                current.append(value)
                changes.append(f"added to {field}: {clean(value)}")
            else:
                match = next((v for v in current if norm(v) == norm(value)), None)
                if match is None:
                    raise PMError(f"'{value}' is not in {field}; current: {', '.join(current) or 'none'}")
                current = [v for v in current if v is not match]
                changes.append(f"removed from {field}: {clean(match)}")
            item[field] = current
    for pair in a.set or []:
        if "=" not in pair:
            raise PMError(f"--set needs field=value, got '{pair}'")
        field, raw = pair.split("=", 1)
        field = field.strip().replace("-", "_")
        if field == "id":
            raise PMError("ids can't be changed; delete and re-add instead")
        if field in MANAGED_FIELDS:
            raise PMError(f"'{field}' can't be set directly; use 'pm.py done ID' to record a completed step")
        if field not in FIELDS[kind]:
            raise PMError(f"'{field}' is not a {kind} field; allowed: {', '.join(f for f in FIELDS[kind] if f not in MANAGED_FIELDS and f != 'id')}")
        item[field] = parse_value(field, raw)
        changes.append(f"{field}={clean(raw)}")
    if not changes:
        raise PMError("nothing to update; pass --set, --add or --remove")
    if kind == "project" and not a.reason:
        new_status, old_status = item.get("status"), before.get("status")
        lost_focus = before.get("focus") in ("primary", "secondary") and item.get("focus") == "none"
        if new_status != old_status and new_status in STEP_AWAY:
            raise PMError(f"setting '{a.id}' to {new_status} needs --reason. What's left: {whats_left(before)}")
        if lost_focus and new_status != "done":
            raise PMError(f"taking focus off '{a.id}' needs --reason. What's left: {whats_left(before)}")
    if "updated" in item or kind != "idea":
        item["updated"] = a.date
    msg = f"Updated {kind} '{item['name']}': {'; '.join(changes)}."
    commit_changes(db, a.date, with_reason(msg, a.reason), a.dry_run, a.no_commit)

def cmd_move(db, a):
    kind, items, i = find(db, a.id)
    if kind == a.to:
        raise PMError(f"'{a.id}' is already a {kind}")
    if kind == "part":
        raise PMError("parts can't be moved; delete and re-add instead")
    if kind == "project" and not a.reason:
        raise PMError(f"moving project '{a.id}' back to ideas needs --reason. What's left: {whats_left(items[i])}")
    old = items.pop(i)
    shared = {k: old[k] for k in ("id", "name", "description", "aliases") if k in old}
    shared.setdefault("description", "")
    if a.to == "project":
        goal = a.goal or old.get("goal")
        if not goal:
            raise PMError("moving to a project needs a goal (--goal)")
        back = old.get("project_history") or {}
        new = {**shared, "goal": goal, "status": "active", "focus": "none",
               "stage": back.get("stage") or old.get("notes", ""), "next_step": back.get("next_step", ""),
               "open_items": back.get("open_items", []), "progress": back.get("progress", []),
               "started": back.get("started") or a.date, "updated": a.date}
        kept = {k: old[k] for k in IDEA_ONLY if old.get(k)}
        if kept:
            new["idea_history"] = kept
    else:
        back = old.get("idea_history") or {}
        new = {**shared, "goal": old.get("goal", ""), "added": back.get("added") or a.date,
               "notes": old.get("stage", "") or back.get("notes", "")}
        kept = {k: old[k] for k in PROJECT_ONLY if old.get(k) not in (None, "", [])}
        if kept:
            new["project_history"] = kept
        for part in db["projects"]["parts"]:
            if old["id"] in part.get("part_of", []):
                print(f"note: part '{part['id']}' still lists '{old['id']}' as a parent")
    collections(db)[a.to].append(new)
    msg = f"Moved '{old['name']}' from {kind}s to {a.to}s."
    commit_changes(db, a.date, with_reason(msg, a.reason), a.dry_run, a.no_commit)

def cmd_done(db, a):
    kind, items, i = find(db, a.id)
    if kind != "project":
        raise PMError(f"'{a.id}' is a {kind}; progress is tracked on projects only")
    item = items[i]
    if item.get("status") != "active":
        raise PMError(f"'{a.id}' is {item.get('status')}, not active; set it back to active before logging work on it")
    step = (a.step or item.get("next_step") or "").strip()
    if not step:
        raise PMError("no next_step to complete; pass --step \"what was done\"")
    used_next_step = not a.step or step == (item.get("next_step") or "").strip()
    open_items = item.get("open_items") or []
    target = a.item if a.item is not None else step
    match = next((o for o in open_items if norm(o) == norm(target)), None)
    if a.item is not None and match is None:
        raise PMError(f"'{a.item}' is not an open item on '{a.id}'; open items: {', '.join(open_items) or 'none'}")
    item.setdefault("progress", []).append({"date": a.date, "step": step})
    if match is not None:
        item["open_items"] = [o for o in open_items if o is not match]
    if a.next is not None:
        item["next_step"] = a.next
    elif used_next_step:
        item["next_step"] = ""
    item["updated"] = a.date
    msg = f"Completed step on '{item['name']}': {clean(step)}."
    if match is not None:
        msg += f" Closed open item: {clean(match)}."
    if a.next is not None:
        msg += f" Next step: {clean(a.next)}." if a.next else " Next step cleared."
    elif used_next_step:
        msg += " No next step set."
    commit_changes(db, a.date, with_reason(msg, a.reason), a.dry_run, a.no_commit)
    if match is not None and not item["open_items"] and not a.dry_run:
        print(f"note: that was the last open item on '{a.id}'. Ask Seph: is the goal reached? "
              f"If yes: update {a.id} --set status=done --set focus=none")

def cmd_delete(db, a):
    kind, items, i = find(db, a.id)
    old = items.pop(i)
    removed_parts = []
    for part in list(db["projects"]["parts"]):
        if a.id in part.get("part_of", []):
            part["part_of"] = [p for p in part["part_of"] if p != a.id]
            if not part["part_of"]:
                db["projects"]["parts"].remove(part)
                removed_parts.append(part["name"])
    msg = with_reason(f"Removed {kind} '{old['name']}'.", a.reason)
    if removed_parts:
        msg += f" Also removed parts with no parents left: {', '.join(removed_parts)}."
    commit_changes(db, a.date, msg, a.dry_run, a.no_commit)

def cmd_check(db, a):
    errors = validate(db)
    if errors:
        print("problems:\n  " + "\n  ".join(errors))
        sys.exit(1)
    for w in warnings(db):
        print(f"warning: {w}")
    print("ok")

def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)

def in_git():
    return git("rev-parse", "--is-inside-work-tree").returncode == 0

def pull():
    """Bring in other AIs' changes. log.md merges by union (.gitattributes); JSON conflicts stop it."""
    if git("remote").stdout.strip() == "":
        return "no remote; nothing to pull"
    r = git("pull", "--rebase", "--autostash", "-q")
    if r.returncode != 0:
        git("rebase", "--abort")
        raise PMError("someone else changed the same lines, so the pull was undone and nothing was pushed. "
                      f"Your changes are still committed locally.\n{(r.stderr or r.stdout).strip()}\n"
                      "Tell Seph which change clashed. Don't force-push or reset without his OK.")
    return "up to date with the remote"

def cmd_sync(db, a):
    if not in_git():
        raise PMError("not a git repo")
    print(pull())

def cmd_commit(db, a):
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        raise PMError("not a git repo yet; run 'git init' and add the remote first")
    git("add", "ideas.json", "projects.json", "log.md")
    if git("diff", "--cached", "--quiet").returncode == 0:
        print("nothing to commit")
    else:
        diff = git("diff", "--cached", "-U0", "--", "log.md").stdout
        new_lines = [l[3:] for l in diff.splitlines() if l.startswith("+- ")]
        if not new_lines:
            git("reset", "-q", "ideas.json", "projects.json", "log.md")
            raise PMError("the data changed but log.md has no new line, so it was probably hand-edited. "
                          "Undo the edit and make the change with pm.py")
        if len(new_lines) == 1:
            r = git("commit", "-m", new_lines[0])
        else:
            subject = f"{new_lines[-1][:10]}: {len(new_lines)} changes"
            r = git("commit", "-m", subject, "-m", "\n".join(f"- {l}" for l in new_lines))
        if r.returncode != 0:
            raise PMError(f"git commit failed, nothing was committed:\n{(r.stderr or r.stdout).strip()}")
        print((r.stdout or "").strip())
    if a.push:
        print(pull())
        r = git("push")
        out = (r.stdout + r.stderr).strip()
        if r.returncode != 0:
            raise PMError(f"git push failed:\n{out}")
        print(out or "pushed")

def main(argv=None):
    p = argparse.ArgumentParser(prog="pm.py", description="CRUD for ideas, projects and parts.")
    sub = p.add_subparsers(dest="cmd", required=True)
    def writer(sp):
        sp.add_argument("--date", type=valid_date, default=today())
        sp.add_argument("--dry-run", action="store_true")
        sp.add_argument("--reason")
        sp.add_argument("--no-commit", action="store_true", help="save without the automatic git commit")
    s = sub.add_parser("list"); s.add_argument("what", nargs="?", default="all", choices=["ideas", "projects", "parts", "all"])
    s = sub.add_parser("get"); s.add_argument("id")
    s = sub.add_parser("add"); writer(s)
    s.add_argument("kind", choices=["idea", "project", "part"])
    s.add_argument("--id", required=True); s.add_argument("--name", required=True)
    s.add_argument("--goal"); s.add_argument("--description"); s.add_argument("--notes"); s.add_argument("--stage"); s.add_argument("--next-step")
    s.add_argument("--status", default="active", choices=STATUSES); s.add_argument("--focus", default="none", choices=FOCUS)
    s.add_argument("--part-of"); s.add_argument("--skip-idea", action="store_true")
    s = sub.add_parser("update"); writer(s); s.add_argument("id"); s.add_argument("--set", action="append")
    s.add_argument("--add", action="append"); s.add_argument("--remove", action="append")
    s = sub.add_parser("move"); writer(s); s.add_argument("id"); s.add_argument("--to", required=True, choices=["idea", "project"]); s.add_argument("--goal")
    s = sub.add_parser("done", help="move the current next_step (or --step) into progress")
    writer(s); s.add_argument("id"); s.add_argument("--step"); s.add_argument("--item"); s.add_argument("--next")
    s = sub.add_parser("delete"); writer(s); s.add_argument("id")
    sub.add_parser("check")
    sub.add_parser("sync")
    s = sub.add_parser("commit"); s.add_argument("--push", action="store_true")
    a = p.parse_args(argv)
    for name, value in vars(a).items():
        values = value if isinstance(value, list) else [value]
        if any(isinstance(v, str) and ("\n" in v or "\r" in v) for v in values):
            p.error(f"--{name.replace('_', '-')} can't contain line breaks")
    if a.cmd == "delete" and not a.reason:
        p.error("delete needs --reason")
    try:
        db = load()
        globals()["cmd_" + a.cmd](db, a)
    except PMError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
