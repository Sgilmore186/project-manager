#!/usr/bin/env python3
"""pm.py: deterministic CRUD for the project-manager repo.

No network, no AI. Reads and writes ideas.json and projects.json,
appends one line to log.md per change, and can git-commit the result.

Usage (run from anywhere; paths resolve to the repo root):
  pm.py list [ideas|projects|parts|all]
  pm.py get ID
  pm.py add idea    --id ID --name NAME [--goal G] [--notes N]
  pm.py add project --id ID --name NAME --goal G [--status S] [--focus F] [--stage S] [--next-step N]
  pm.py add part    --id ID --name NAME --part-of A,B [--stage S]
  pm.py update ID --set field=value [--set field=value ...] [--reason R]
  pm.py move ID --to idea|project [--goal G] [--reason R]
  pm.py delete ID --reason R
  pm.py check
  pm.py commit [--push]

Every write takes --date YYYY-MM-DD (default: today) and --dry-run.
"""
import argparse, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDEAS, PROJECTS, LOG = (os.path.join(ROOT, f) for f in ("ideas.json", "projects.json", "log.md"))
STATUSES = ["active", "paused", "archived", "done", "dropped"]
FOCUS = ["primary", "secondary", "none"]
LIST_FIELDS = {"open_items", "part_of", "aliases"}
KINDS = {"idea": ("ideas", "ideas"), "project": ("projects", "projects"), "part": ("projects", "parts")}

class PMError(Exception):
    pass

def load():
    with open(IDEAS) as f: ideas = json.load(f)
    with open(PROJECTS) as f: projects = json.load(f)
    projects.setdefault("parts", [])
    return {"ideas": ideas, "projects": projects}

def save(db, date):
    db["ideas"]["updated"] = date
    db["projects"]["updated"] = date
    for path, key in ((IDEAS, "ideas"), (PROJECTS, "projects")):
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(db[key], f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)

def log(date, text):
    with open(LOG, "a") as f:
        f.write(f"- {date}: {text}\n")

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
    rules = db["projects"].get("rules", {})
    counts = {"primary": 0, "secondary": 0}
    for p in db["projects"]["projects"]:
        if not p.get("goal"):
            errors.append(f"project '{p['id']}' has no goal")
        if p.get("status") not in STATUSES:
            errors.append(f"project '{p['id']}' has invalid status '{p.get('status')}'")
        if p.get("focus") not in FOCUS:
            errors.append(f"project '{p['id']}' has invalid focus '{p.get('focus')}'")
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

def commit_changes(db, date, message, dry):
    errors = validate(db)
    if errors:
        raise PMError("refusing to save:\n  " + "\n  ".join(errors))
    if dry:
        print(f"[dry run] would save and log: {message}")
        return
    save(db, date)
    log(date, message)
    print(message)

def cmd_list(db, a):
    which = a.what
    show = {"ideas": ["idea"], "projects": ["project"], "parts": ["part"], "all": ["project", "part", "idea"]}[which]
    cols = collections(db)
    for kind in show:
        print(f"## {kind}s ({len(cols[kind])})")
        for x in cols[kind]:
            extra = ""
            if kind == "project":
                extra = f" [{x.get('status')}{', ' + x['focus'] if x.get('focus') not in (None, 'none') else ''}]"
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
        item = {"id": a.id, "name": a.name, "goal": a.goal or "", "added": a.date, "notes": a.notes or ""}
    elif a.kind == "project":
        if not a.goal:
            raise PMError("a project needs --goal")
        item = {"id": a.id, "name": a.name, "goal": a.goal, "status": a.status, "focus": a.focus,
                "stage": a.stage or "", "next_step": a.next_step or "", "open_items": [],
                "started": a.date, "updated": a.date}
    else:
        parents = parse_value("part_of", a.part_of or "")
        item = {"id": a.id, "name": a.name, "part_of": parents, "stage": a.stage or "", "updated": a.date}
    collections(db)[a.kind].append(item)
    commit_changes(db, a.date, f"Added {a.kind} '{a.name}'." + (f" {a.reason}" if a.reason else ""), a.dry_run)

def cmd_update(db, a):
    kind, items, i = find(db, a.id)
    item = items[i]
    changes = []
    for pair in a.set or []:
        if "=" not in pair:
            raise PMError(f"--set needs field=value, got '{pair}'")
        field, raw = pair.split("=", 1)
        field = field.strip().replace("-", "_")
        if field == "id":
            raise PMError("ids can't be changed; delete and re-add instead")
        item[field] = parse_value(field, raw)
        changes.append(f"{field}={raw}")
    if not changes:
        raise PMError("nothing to update; pass --set field=value")
    if "updated" in item or kind != "idea":
        item["updated"] = a.date
    msg = f"Updated {kind} '{item['name']}': {'; '.join(changes)}."
    commit_changes(db, a.date, msg + (f" Reason: {a.reason}" if a.reason else ""), a.dry_run)

def cmd_move(db, a):
    kind, items, i = find(db, a.id)
    if kind == a.to:
        raise PMError(f"'{a.id}' is already a {kind}")
    if kind == "part":
        raise PMError("parts can't be moved; delete and re-add instead")
    old = items.pop(i)
    if a.to == "project":
        goal = a.goal or old.get("goal")
        if not goal:
            raise PMError("moving to a project needs a goal (--goal)")
        new = {"id": old["id"], "name": old["name"], "goal": goal, "status": "active", "focus": "none",
               "stage": old.get("notes", ""), "next_step": "", "open_items": [], "started": a.date, "updated": a.date}
    else:
        notes = old.get("stage", "")
        new = {"id": old["id"], "name": old["name"], "goal": old.get("goal", ""), "added": a.date,
               "notes": notes}
        for part in db["projects"]["parts"]:
            if old["id"] in part.get("part_of", []):
                print(f"note: part '{part['id']}' still lists '{old['id']}' as a parent")
    collections(db)[a.to].append(new)
    msg = f"Moved '{old['name']}' from {kind}s to {a.to}s."
    commit_changes(db, a.date, msg + (f" Reason: {a.reason}" if a.reason else ""), a.dry_run)

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
    msg = f"Removed {kind} '{old['name']}'. Reason: {a.reason.rstrip(".")}."
    if removed_parts:
        msg += f" Also removed parts with no parents left: {', '.join(removed_parts)}."
    commit_changes(db, a.date, msg, a.dry_run)

def cmd_check(db, a):
    errors = validate(db)
    if errors:
        print("problems:\n  " + "\n  ".join(errors))
        sys.exit(1)
    print("ok")

def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)

def cmd_commit(db, a):
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        raise PMError("not a git repo yet; run 'git init' and add the remote first")
    git("add", "ideas.json", "projects.json", "log.md")
    if git("diff", "--cached", "--quiet").returncode == 0:
        print("nothing to commit")
        return
    with open(LOG) as f:
        last = [l for l in f.read().splitlines() if l.startswith("- ")][-1][2:]
    r = git("commit", "-m", last)
    print(r.stdout or r.stderr)
    if a.push:
        r = git("push")
        print(r.stdout or r.stderr)
        if r.returncode != 0:
            sys.exit(r.returncode)

def main(argv=None):
    p = argparse.ArgumentParser(prog="pm.py", description="CRUD for ideas, projects and parts.")
    sub = p.add_subparsers(dest="cmd", required=True)
    def writer(sp):
        sp.add_argument("--date", default=datetime.date.today().isoformat())
        sp.add_argument("--dry-run", action="store_true")
        sp.add_argument("--reason")
    s = sub.add_parser("list"); s.add_argument("what", nargs="?", default="all", choices=["ideas", "projects", "parts", "all"])
    s = sub.add_parser("get"); s.add_argument("id")
    s = sub.add_parser("add"); writer(s)
    s.add_argument("kind", choices=["idea", "project", "part"])
    s.add_argument("--id", required=True); s.add_argument("--name", required=True)
    s.add_argument("--goal"); s.add_argument("--notes"); s.add_argument("--stage"); s.add_argument("--next-step")
    s.add_argument("--status", default="active", choices=STATUSES); s.add_argument("--focus", default="none", choices=FOCUS)
    s.add_argument("--part-of")
    s = sub.add_parser("update"); writer(s); s.add_argument("id"); s.add_argument("--set", action="append")
    s = sub.add_parser("move"); writer(s); s.add_argument("id"); s.add_argument("--to", required=True, choices=["idea", "project"]); s.add_argument("--goal")
    s = sub.add_parser("delete"); writer(s); s.add_argument("id")
    sub.add_parser("check")
    s = sub.add_parser("commit"); s.add_argument("--push", action="store_true")
    a = p.parse_args(argv)
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
