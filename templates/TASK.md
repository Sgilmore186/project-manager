# Task template

Copy the section below into an approved phase or Priority repairs on the central Development Board. Replace all placeholders. An agent must not execute a placeholder task.

### <permanent task ID> - <short title>

- **Objective:** <what Seph wants accomplished>
- **Approval:** <date and source of explicit approval, or repair within approved scope with reproduction/evidence>
- **Dependencies:** <task IDs and external gates, or none>
- **Status:** pending
- **Claim:** none
- **Instructions:** <specific prompt; constraints, relevant paths/specs and intended behavior>
- **Toolbox:** <shared skill paths, project-local skill paths, installed skill names, test commands, tools or references; only relevant items>
- **Acceptance criteria:**
  - <observable requirement and how to verify it>
  - <required tests or regression checks>
  - <required publication, merge or user approval, if applicable>
- **Evidence:** none yet
- **Handoff:** none yet

## Status meanings

- pending: approved, not yet started.
- in-progress: claimed, with run ID, owner, time and starting commit.
- blocked: reason and next step recorded; no implementation until the blocker is resolved.
- implemented: code exists; some required checks remain.
- validated: required implementation checks pass; a required external gate remains.
- needs-fix: a known failure or regression prevents completion.
- done: all stated acceptance and delivery gates passed; remote evidence recorded.

Do not mark a task done only because code exists. If the task is already satisfied, verify it and record evidence without rebuilding. Record publication and physical playtest separately where relevant. A validated task awaiting a gate should not be reimplemented. Use an explicit gate when Seph's approval is needed before moving on.
