# Project Manager

Seph's running record of ideas and projects, in plain JSON so any tool or AI can read it.
The goal: hold Seph accountable and help him finish what he starts.

- **Idea** (`ideas.json`): an outcome Seph wants but hasn't committed to finishing.
- **Project** (`projects.json`): an outcome Seph has committed to finishing, with its goal, next step, open items and progress.
- **Part**: something that only matters because it helps a larger project.
- **Log** (`log.md`): a dated line for every change.

All changes go through `scripts/pm.py` (run `python3 scripts/pm.py --help`).
Tests: `python3 -m unittest discover -s tests -v`.

Full rules, fields and steps: [AGENTS.md](AGENTS.md). Repo organization standard: [docs/REPO_STANDARD.md](docs/REPO_STANDARD.md).
