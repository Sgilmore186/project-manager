# AGENTS.md

Instructions for any AI working on this repo. Read this first, every session.
This file is the single source of truth for how the repo works. README.md is a short overview that points here. CLAUDE.md imports this file for Claude Code, and GEMINI.md imports it for Gemini CLI.

## What this repo is
Seph's single source of truth for ideas and projects. Plain JSON so it moves across tools and AIs.
The goal: hold Seph accountable and challenge him to finish what he starts.

## Files
- `ideas.json`: outcomes Seph wants but hasn't committed to.
- `projects.json`: outcomes Seph has committed to, with current status.
- `log.md`: dated, human-readable history of every change (written by the script). `.gitattributes` merges it line by line, so two AIs adding lines never conflict.
- `scripts/pm.py`: the only way to change the data. Python 3.9+, standard library only.
- `tests/test_pm.py`: behavior tests for the script.
- `.github/workflows/tests.yml`: runs the tests on every PR and push to main (on Ubuntu 24.04, the last runner image with Python 3.9).
- `scripts/dashboard_data.py` and `.github/workflows/dashboard-data.yml`: on every push to main, copy `ideas.json` and `projects.json` into the GitHub issue labeled `dashboard-data`. Seph's dashboard reads that issue, so it stays live. Never edit or close that issue by hand; if it's missing, run the `dashboard-data` workflow.
- `README.md`: short overview for humans.
- `CLAUDE.md`: two lines that import this file for Claude Code. Never put rules there.
- `GEMINI.md`: the same two lines, for Gemini CLI. Never put rules there.
- `docs/REPO_STANDARD.md`: the organization standard every Seph repo follows.

## Approved development workflow

- [Agent workflow](docs/AGENT_WORKFLOW.md) defines the shared Dream Board and central Development Board system.
- Unattended agents start with [agent-execution](skills/agent-execution/SKILL.md). Select the explicitly assigned active project or the active primary. Never infer authorization from a Dream Board or legacy open items.
- Duet uses [duet-planning](skills/duet-planning/SKILL.md) to refine ideas and promote only approved scope.
- `development/<project-id>/BOARD.md` holds the executable queue for an enrolled project. Existing project boards remain authoritative until explicitly migrated.
- Canonical skills live in `skills/`; native Codex and Claude Code entry points in `.agents/skills/` and `.claude/skills/` load the same definitions. Follow [the shared skill standard](docs/REPO_STANDARD.md#shared-skills).
- `templates/` holds the standard board and task formats. [Nightly run](docs/NIGHTLY_RUN.md) is the portable scheduler prompt.
- The operational board-only push exception in the workflow does not apply to code, skills, templates or registry data. Existing registry writes still go exclusively through pm.py. All other existing repo rules remain in force.

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
Example: Crosswalk is part of Project Manager and the orchestrator (the multi-model workflow idea).

## Statuses
- `active`: committed and being worked on.
- `paused`: committed, deliberately on hold.
- `archived`: set aside by Seph; kept for the record. Shown under **Archived** with `dropped`. Not worked on, not counted toward focus, not nagged about. Only Seph archives or un-archives.
- `done`: goal reached. Shown under **Completed** in `list` and on the dashboard, kept apart from archived.
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
Every change to the existing project registry goes through `scripts/pm.py`. Never hand-edit the JSON or `log.md`. The separate enrolled Development Boards follow the approved development workflow above.
The script is deterministic: no AI, Python standard library only. It checks the rules, then saves both JSON files and the `log.md` line together (all or nothing). Inside a git repo, each change is then committed on its own, with the log line as the message. Only `sync` and `commit --push` touch the network.
The step-by-step version is skills/pm-update/SKILL.md.

### Steps
0. At the start of a session, run `python3 scripts/pm.py sync` to pull changes other AIs made.
1. Seph talks. Decide what changed: new idea, new project, status, focus, progress, next step.
2. If unsure whether something is an idea, project or part, ask Seph. Don't guess.
3. Run the matching command below. Pass Seph's reason with `--reason` whenever he gives one.
4. If the script prints `error:`, nothing was saved. Fix the input or ask Seph; never force it.
5. Run `python3 scripts/pm.py commit --push`. It commits anything left over, pulls other AIs' changes, then pushes. If it prints `error:`, nothing was pushed; read the message. If it says the pull was undone, tell Seph which change clashed. Never force-push or reset without his OK.

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
python3 scripts/pm.py update ID [--set field=value] [--add list_field=item] [--remove list_field=item] [--reason R]
python3 scripts/pm.py move ID --to idea|project [--goal G] [--reason R]
python3 scripts/pm.py done ID [--step S] [--item OPEN_ITEM] [--next N] [--reason R]
python3 scripts/pm.py delete ID --reason R
python3 scripts/pm.py sync
python3 scripts/pm.py commit [--push]
```
Every write also takes `--date YYYY-MM-DD` (default: today in US Central time, Seph's day) `--dry-run`, and `--no-commit` (save without the automatic commit).

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
- **One list item:** `update ID --add open_items="..."` or `--remove open_items="..."`. Use these for open items, parts and aliases; one item can contain commas. Matching on `--remove` ignores case, spacing and punctuation.
- **Whole list:** `--set open_items=A,B,C` replaces the list and splits on commas.
- **Moving between ideas and projects keeps everything.** Project-only fields go into `project_history` on the idea, and idea-only fields into `idea_history` on the project. Moving back restores them (focus always comes back as `none`).

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
- `progress` is a list of `{date, step}` entries, can't be set with `--set`, and only projects have it. The same goes for `project_history` and `idea_history`.
- Every save is all or nothing across `ideas.json`, `projects.json` and `log.md`.
- `done` writes progress, open items and next step together in one save, or not at all.
- Deleting a parent unlinks its parts; a part is removed only when no parents remain.
- `commit` refuses if the data changed without a new log line (a hand edit), and reports a failed git commit or push as an error.

## How to challenge Seph
- When he brings a new idea, ask how it ranks against his current focus before logging it.
- When he wants to move off a project, ask for the reason and name what's unfinished.
- When a project's goal is vague, ask him to sharpen it.
- Be direct and brief. Push back once, clearly, then respect his decision.

## Repo standard
This repo is the model for every Seph repo. The full standard is [docs/REPO_STANDARD.md](docs/REPO_STANDARD.md).
Short version: AGENTS.md holds the rules, CLAUDE.md and GEMINI.md only import it, README stays short, docs have one index, code changes go through a branch and PR (data changes here go through `pm.py`), and nothing private is committed.

## Writing style
Short, scannable, plain words. No em dashes. No long paragraphs.

## Current status
Don't copy status into this file. It goes stale. For the live picture run `python3 scripts/pm.py list`, or read `projects.json`.
