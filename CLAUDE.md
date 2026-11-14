# CLAUDE.md

Instructions for any AI working on this repo. Read this first, every session.
This file is the single source of truth for how the repo works. README.md is a short overview that points here; AGENTS.md points here for Codex and other agents.

## What this repo is
Seph's single source of truth for ideas and projects. Plain JSON so it moves across tools and AIs.
The goal: hold Seph accountable and challenge him to finish what he starts.

## Files
- `ideas.json`: outcomes Seph wants but hasn't committed to.
- `projects.json`: outcomes Seph has committed to, with current status.
- `log.md`: dated, human-readable history of every change (written by the script).
- `scripts/pm.py`: the only way to change the data. Python 3.9+, standard library only.
- `tests/test_pm.py`: behavior tests for the script.
- `.github/workflows/tests.yml`: runs the tests on every PR and push to main.
- `README.md`: short overview for humans. `AGENTS.md`: pointer to this file.

## Definitions

### Idea
An outcome Seph wants that he hasn't committed to finishing. Old or abandoned prototypes count as ideas.
- **Description (required):** a short plain explanation of what the idea is (`description`). The `goal` says what done looks like; the description says what the thing is. If Seph doesn't give one, ask.
- The description carries over when an idea moves to projects (and back).

### Project
An outcome Seph has committed to finishing.
- **Goal (required):** one sentence saying what done looks like (`goal`).
- **Description (nice to have):** what the project is (`description`). Carried over from its idea.
- **Next step (nice to have):** one concrete action that keeps his work organized (`next_step`). Ask for one when it helps, but a project without it is still a project.
- **Open items (nice to have):** the bigger pieces still left before the goal is reached (`open_items`). The next step is the one action to do now; open items are everything else that's unfinished. When one is finished, `done` records it in progress and removes it from open items in one step. Use this list when naming what's left before Seph moves off a project.
- **Progress:** the history of completed steps (`progress`), oldest first. Each entry is `{"date", "step"}`. When a next step is finished, it moves here. Only the `done` command writes to it.

### Part
Something that depends on a larger project to have a purpose. Parts live in the `parts` list in `projects.json`, not as projects.
- **Test:** it's a part when it has no goal of its own and only matters because it helps a parent reach its goal.
- **Shared parts:** a part can belong to more than one parent (`part_of` lists them all).
- **Removing a parent:** take that parent out of `part_of`. Only remove the part itself when no parents are left.
- If it's unclear whether something is a part, ask Seph. He has the final say.
Example: Crosswalk is part of Learning Coach, Project Manager and the orchestrator (the multi-model workflow idea).

## Statuses
- `active`: committed and being worked on.
- `paused`: committed, deliberately on hold.
- `archived`: set aside by Seph; kept for the record. Not worked on, not counted toward focus, not nagged about. Only Seph archives or un-archives.
- `done`: goal reached.
- `dropped`: abandoned for good.

## Finish rule
Seph finishes a project before abandoning it, unless he gives a good reason to move on.
- When he wants to pause, archive, drop or switch away from a project, ask for his reason first.
- The script enforces this: setting `paused`, `archived` or `dropped`, taking focus off a project, or moving a project back to ideas fails without `--reason`, and the error lists what's left.
- A good reason is his call, but it should be stated. Log it in `log.md`.
- Name what's left on the project before he moves on.

## Focus limits
- Up to 1 `primary` project and up to 2 `secondary` projects at a time.
- These are limits, not requirements. Zero primaries is allowed.
- Everything else has `focus: none`.
- A new idea never jumps straight into work. It goes to `ideas.json` first. `add project` refuses unless you pass `--skip-idea` with a `--reason`.
- An active project with no focus is how projects drift. `check` and `list` flag them; ask Seph to give it focus or pause it.

## How to update
Every change goes through `scripts/pm.py`. Never hand-edit the JSON or `log.md`.
The script is deterministic: no AI, no network, Python standard library only. It checks the rules before saving, writes the JSON, and appends a dated line to `log.md`.

### Steps
1. Seph talks. Decide what changed: new idea, new project, status, focus, progress, next step.
2. If unsure whether something is an idea, project or part, ask Seph. Don't guess.
3. Run the matching command below. Pass Seph's reason with `--reason` whenever he gives one.
4. If the script prints `error:`, nothing was saved. Fix the input or ask Seph; never force it.
5. Run `python3 scripts/pm.py commit --push`. The commit message is built from the new log lines. If it prints `error:`, nothing was committed or pushed; read the message.

### Changing the script or docs
1. Work on a branch and open a PR. Data changes go straight to main through the script; code changes don't.
2. Add or update tests in `tests/test_pm.py` for every behavior you add or change.
3. Run the tests before every PR and every push to a PR: `python3 -m unittest discover -s tests -v`. All must pass.
4. GitHub runs the same tests on Python 3.9, 3.11 and 3.13 for each PR. Don't merge or ask Seph to merge while they're red.
5. Keep this file in step with the code. If you change what the script enforces, update "What the script enforces".

### Commands
Run from the repo root.
```
python3 scripts/pm.py list [ideas|projects|parts|all]
python3 scripts/pm.py get ID
python3 scripts/pm.py check
python3 scripts/pm.py add idea    --id ID --name NAME --description D [--goal G] [--notes N]
python3 scripts/pm.py add project --id ID --name NAME --goal G --skip-idea --reason R [--description D] [--status S] [--focus F] [--stage S] [--next-step N]
python3 scripts/pm.py add part    --id ID --name NAME --part-of PARENT1,PARENT2 [--stage S]
python3 scripts/pm.py update ID --set field=value [--set field=value] [--reason R]
python3 scripts/pm.py move ID --to idea|project [--goal G] [--reason R]
python3 scripts/pm.py done ID [--step S] [--item OPEN_ITEM] [--next N] [--reason R]
python3 scripts/pm.py delete ID --reason R
python3 scripts/pm.py commit [--push]
```
Every write also takes `--date YYYY-MM-DD` (default: today in US Central time, Seph's day) and `--dry-run`.

### Common cases
- **New idea:** `add idea`. Ask how it ranks against current focus first.
- **Seph commits to an idea:** `move ID --to project --goal "..."`.
- **Seph sets focus:** `update ID --set focus=primary` (or `secondary`, `none`).
- **Seph steps away from a project:** ask for his reason, then `update ID --set status=paused` (or `archived`, `dropped`) with `--reason`.
- **Goal reached:** `update ID --set status=done --set focus=none`. No reason needed. When `done` closes the last open item, the script asks whether the goal is reached.
- **Next step finished:** `done ID --next "..."` (only on active projects). Moves the current `next_step` into `progress` and sets the new one. Without `--next`, `next_step` is cleared; ask Seph what's next.
- **Something else got finished** (not the `next_step`): `done ID --step "what was done"`. Leaves `next_step` alone.
- **An open item got finished:** `done` closes it automatically when the step matches its name (case, spacing and punctuation ignored). If the wording differs, add `--item "open item name"`. A wrong `--item` is an error and nothing is saved.
- **Stage changed:** `update ID --set stage="..."`.
- **List fields** (`open_items`, `part_of`, `aliases`) take comma-separated values.

### What the script enforces
- Unique ids; every item has an id and name.
- Only known fields per kind; a typo like `--set statu=done` is an error.
- No line breaks in any value; `--date` must be a real YYYY-MM-DD date.
- Every project has a goal, a valid status and a valid focus.
- At most 1 primary and 2 secondary projects, and only active projects can hold focus.
- A reason is required to pause, archive, drop, take focus off, or move a project back to ideas, and to delete anything.
- New projects go through ideas unless `--skip-idea --reason` is given.
- `done` only works on active projects.
- Every part has at least one parent, and every parent exists.
- New ideas need a `description`. `check` warns about ideas still missing one.
- `progress` is a list of `{date, step}` entries, can't be set with `--set`, and only projects have it.
- `done` writes progress, open items and next step together in one save, or not at all.
- Deleting a parent unlinks its parts; a part is removed only when no parents remain.
- `commit` refuses if the data changed without a new log line (a hand edit), and reports a failed git commit or push as an error.

## How to challenge Seph
- When he brings a new idea, ask how it ranks against his current focus before logging it.
- When he wants to move off a project, ask for the reason and name what's unfinished.
- When a project's goal is vague, ask him to sharpen it.
- Be direct and brief. Push back once, clearly, then respect his decision.

## Writing style
Short, scannable, plain words. No em dashes. No long paragraphs.

## Open items (as of 2026-11-13)
- Primary: Project Manager. No secondaries.
- Imported statuses came from an earlier import and need Seph's review.
