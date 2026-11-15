#!/usr/bin/env python3
"""dashboard_data.py: pack ideas.json and projects.json into one GitHub issue body.

The Project Manager dashboard can't read repo files through the GitHub connector
(it only gets a "downloaded" note), but it can read an issue. The
dashboard-data workflow runs this on every push to main and writes the output
into the issue labeled 'dashboard-data'. Never edit that issue by hand.

Usage: python3 scripts/dashboard_data.py [--commit SHA] [--out FILE]
Standard library only.
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABEL = "dashboard-data"
TITLE = "Dashboard data (auto-updated, do not edit)"
MAX_BODY = 65536  # GitHub's limit for an issue body, in characters
HEADER = ("This issue is written by the dashboard-data workflow on every push to main. "
          "The Project Manager dashboard reads it. Don't edit it by hand: change the data with scripts/pm.py.")

def build(root=ROOT, commit=""):
    data = {}
    for name in ("ideas", "projects"):
        with open(os.path.join(root, f"{name}.json")) as f:
            data[name] = json.load(f)
    payload = {"commit": commit, "ideas": data["ideas"], "projects": data["projects"]}
    body = f"{HEADER}\n\n```json\n{json.dumps(payload, ensure_ascii=False, separators=(',', ':'))}\n```\n"
    if len(body) > MAX_BODY:
        raise ValueError(f"issue body would be {len(body)} characters, over GitHub's {MAX_BODY} limit")
    return body

def parse(body):
    """Read the payload back out of an issue body (what the dashboard does)."""
    start, end = body.index("{"), body.rindex("}")
    return json.loads(body[start:end + 1])

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--commit", default="")
    p.add_argument("--out")
    a = p.parse_args(argv)
    try:
        body = build(commit=a.commit)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w") as f:
            f.write(body)
    else:
        sys.stdout.write(body)
    return 0

if __name__ == "__main__":
    sys.exit(main())
