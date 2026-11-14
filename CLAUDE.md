# CLAUDE.md

Instructions for any AI working on this repo. Read this first, every session.

## What this repo is
Seph's single source of truth for ideas and projects. Plain JSON so it moves across tools and AIs.
The goal: hold Seph accountable and challenge him to finish what he starts.

## Files
- `ideas.json`: outcomes Seph wants but hasn't committed to.
- `projects.json`: outcomes Seph has committed to, with current status.
- `log.md`: dated, human-readable history of every change (written by the script).
- `scripts/pm.py`: the only way to change the data.
- `README.md`: short overview for humans.

## Definitions

### Idea
An outcome Seph wants that he hasn't committed to finishing. Old or abandoned prototypes count as ideas.

### Project
An outcome Seph has committed to finishing.
- **Goal (required):** one sentence saying what done looks like (`goal`).
- **Next step (nice to have):** one concrete action that keeps his work organized (`next_step`). Ask for one when it helps, but a project without it is still a project.
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
- A good reason is his call, but it should be stated. Log it in `log.md`.
- Name what's left on the project before he moves on.

## Focus limits
- Up to 1 `primary` project and up to 2 `secondary` projects at a time.
- These are limits, not requirements. Zero primaries is allowed.
- Everything else has `focus: none`.
- A new idea never jumps straight into work. It goes to `ideas.json` first.

## How to update
Every change goes through `scripts/pm.py`. Never hand-edit the JSON or `log.md`.
The script is deterministic: no AI, no network, Python standard library only. It checks the rules before saving, writes the JSON, and appends a dated line to `log.md`.

### Steps
1. Seph talks. Decide what changed: new idea, new project, status, focus, progress, next step.
2. If unsure whether something is an idea, project or part, ask Seph. Don't guess.
3. Run the matching command below. Pass Seph's reason with `--reason` whenever he gives one.
4. If the script prints `error:`, nothing was saved. Fix the input or ask Seph; never force it.
5. Run `python3 scripts/pm.py commit --push`. The commit message is the last log line.

### Commands
Run from the repo root.
```
python3 scripts/pm.py list [ideas|projects|parts|all]
python3 scripts/pm.py get ID
python3 scripts/pm.py check
python3 scripts/pm.py add idea    --id ID --name NAME [--goal G] [--notes N]
python3 scripts/pm.py add project --id ID --name NAME --goal G [--status S] [--focus F] [--stage S] [--next-step N]
python3 scripts/pm.py add part    --id ID --name NAME --part-of PARENT1,PARENT2 [--stage S]
python3 scripts/pm.py update ID --set field=value [--set field=value] [--reason R]
python3 scripts/pm.py move ID --to idea|project [--goal G] [--reason R]
python3 scripts/pm.py done ID [--step S] [--next N] [--reason R]
python3 scripts/pm.py delete ID --reason R
python3 scripts/pm.py commit [--push]
```
Every write also takes `--date YYYY-MM-DD` (default today) and `--dry-run`.

### Common cases
- **New idea:** `add idea`. Ask how it ranks against current focus first.
- **Seph commits to an idea:** `move ID --to project --goal "..."`.
- **Seph sets focus:** `update ID --set focus=primary` (or `secondary`, `none`).
- **Seph steps away from a project:** ask for his reason, then `update ID --set status=paused` (or `archived`, `dropped`) with `--reason`.
- **Goal reached:** `update ID --set status=done --set focus=none`.
- **Next step finished:** `done ID --next "..."`. Moves the current `next_step` into `progress` and sets the new one. Without `--next`, `next_step` is cleared; ask Seph what's next.
- **Something else got finished** (not the `next_step`): `done ID --step "what was done"`. Leaves `next_step` alone.
- **Stage changed:** `update ID --set stage="..."`.
- **List fields** (`open_items`, `part_of`, `aliases`) take comma-separated values.

### What the script enforces
- Unique ids; every item has an id and name.
- Every project has a goal, a valid status and a valid focus.
- At most 1 primary and 2 secondary projects, and only active projects can hold focus.
- Every part has at least one parent, and every parent exists.
- `progress` is a list of `{date, step}` entries, can't be set with `--set`, and only projects have it.
- Deleting a parent unlinks its parts; a part is removed only when no parents remain.

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
