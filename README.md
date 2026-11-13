# Project Manager

Seph's running record of ideas and projects. Plain JSON so any tool or AI can read it.

## Data model
- **Idea**: an outcome you want to accomplish that hasn't started yet. Lives in `ideas.json`.
- **Project**: an idea in motion, with the current status of fulfilling it. Lives in `projects.json`.

When an idea starts, it moves from `ideas.json` to `projects.json` and keeps its `id`.

## Rules
- Finish a project before abandoning it, unless there's a good reason.
- Up to 1 primary and 2 secondary projects (limits, not requirements).
- A new idea goes to the ideas list first, not straight into work.
- Every change is a dated commit. `log.md` keeps the human-readable history.

## Project fields
- `id`, `name`, `goal` (what done looks like), `status` (active, paused, archived, done, dropped)
- `focus` (primary, secondary, or none), `stage` (where it actually is)
- `next_step`, `open_items`, `started`, `updated`

## Updating
Use `scripts/pm.py`. Run `python3 scripts/pm.py --help`.
