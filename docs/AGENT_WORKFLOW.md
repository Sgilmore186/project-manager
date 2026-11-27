# Agent workflow

A small shared workflow, not a new orchestration platform. Seph chooses what to build. Duet plans. Development agents execute approved tasks. Project Manager stays the source of project focus and development work.

## Sources of truth

| Location | Owner / purpose |
| --- | --- |
| projects.json and ideas.json | Existing project registry and high-level priorities; scripts/pm.py remains the only writer. |
| development/<project-id>/BOARD.md | Central approved phases, tasks, prompts, toolbox, dependencies, claims and evidence. |
| Target repo docs/DREAM_BOARD.md | Ideas and open design questions. Not authorization to build. |
| Target repo AGENTS.md and specs | Local technical rules, requirements, permissions and tests. |
| skills/ | Shared portable skills; project-local and installed skills may be referenced by a task. |

No project is enrolled until its central board is explicitly created and verified. Existing local boards remain authoritative until their approved work, history and active claims are reconciled and the local rules are updated to point to the central board. Do not run both queues independently. This change does not enroll or migrate any project.

## Setup

1. Start with the existing active project ID from projects.json. Copy templates/DEVELOPMENT_BOARD.md to development/<project-id>/BOARD.md. Specify target repo, branch, permission policy and source of approval.
2. In that target repo, create docs/DREAM_BOARD.md from templates/DREAM_BOARD.md. Preserve existing idea history and specs.
3. Migrate approved items in order using templates/TASK.md, retaining IDs, sources and verified evidence. Keep unresolved ideas in the Dream Board. Coordinate with existing agents before switching.
4. Update the target AGENTS.md to point to the central board and retain target-specific instructions. Verify both repos and the first read-only routing pass before enabling unattended writes.

## Daily operation

- Duet loads skills/duet-planning/SKILL.md to brainstorm and promote approved scope.
- A scheduled agent loads skills/agent-execution/SKILL.md, selects an assigned project or active primary, claims, executes, tests, pushes, verifies, records and repeats.
- Agents may create and prioritize scoped bug/quality repairs, with evidence. New features and major changes require approval. Never expand a project's permissions.
- Use one active implementation run per project in v1. A claim is a coordination convention, not an external distributed lock. All agents must honor it. Re-fetch before claim and progress writes; if a normal push loses a race, re-read and reconcile, never force. Do not start while uncertain about another active run.
- The central board's phases and tasks are authoritative for execution. Project Manager's coarse open_items/next_step/stage remain summaries, maintained through pm.py. Do not mechanically equate every task with an open item.
- Keep approval, status and evidence in the board; Git preserves history. Do not delete finished tasks to make a board look clean.

## Push rules

Infrastructure, code, skills, templates and general docs in Project Manager follow its existing branch + PR policy. The existing registry data still changes only through pm.py.

Once this standard is merged, operational updates restricted to an already-enrolled development/<project-id>/BOARD.md (claims, approved promotions, progress and evidence) may use normal direct pushes to main, with fetch/reconciliation, explicit staging of that board, diff review and remote verification. This narrow operational exception does not authorize changing the registry manually, creating new enrollments on main, modifying infrastructure or bypassing CI. Initial enrollment uses a reviewed PR. Target code uses its own explicitly authorized push policy; otherwise use a PR. A task may be validated but not done while a required merge, release or review is pending.

## Run configuration

The scheduler belongs to the agent platform (Codex, Claude Code/Duet or another supported runner), not this repository. See [automation entrypoint](NIGHTLY_RUN.md). An agent must have access to both repos, the applicable tools and a usable environment. Scheduling and access must be verified on that platform. A ChatGPT reminder alone is not a Codex run.

No independent morning review in v1. Same-agent verification and existing CI are mandatory where applicable. Avoid recording private logs, secrets, account details or unapproved personal material in Git.
