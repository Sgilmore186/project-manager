# Development Board: <project name>

Copy to development/<existing-project-id>/BOARD.md after explicit enrollment approval. Remove instructional placeholders before use. The central board is the executable queue, not the brainstorm board.

## Project routing

- Project ID: <existing ID in projects.json>
- Target repository: <owner/name>
- Target branch: <branch>
- Push policy: <PR or explicitly authorized direct push, with source>
- Project rules: <AGENTS.md link>
- Dream Board: <target repository docs/DREAM_BOARD.md link>
- Enrollment approval/source: <date and non-private reference>
- Activation: pending | active (active only after local queue migration and verification)

## Run claim

- Owner: none
- Run ID: none
- Claimed/renewed UTC: none
- Starting target commit: none

Only one active implementation run per project. Follow agent-execution skill before claiming or recovering a claim.

## Priority repairs

Use the task template for reproducible urgent bugs, failed checks and necessary scoped quality repairs. Repairs may preempt feature work. Do not add unapproved features.

## Ordered phases

### <phase ID> - <phase name>

- Objective: <approved outcome>
- Approval: <date/source>
- Dependencies: <prior phase IDs or none>
- Phase gate: <required tests, release, user approval or other conditions>

Paste tasks using templates/TASK.md in intended execution order. Keep task IDs permanent. A phase is complete only when its required tasks and gate are satisfied. A blocked task may be bypassed only for independent eligible work, not to violate a phase gate.

## Run handoffs

Add short dated summaries with run ID, target commit/PR, completed/skipped/blocked IDs, actual test results, remaining work, and decisions. Keep detailed task evidence in the task itself; link rather than copy it. Preserve history and do not store private logs.
