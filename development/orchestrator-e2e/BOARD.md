# Development Board: Orchestrator smoke test

Test board for [orchestration](../../docs/ORCHESTRATION.md). Not a registry project. Normal runs never select it; only an explicit orchestrator test run with `--allow-test` does. Every job here is throwaway: draft PRs only, never merged, closed after the test.

## Project routing

- Project ID: orchestrator-e2e (test board, not in projects.json)
- Target repository: Sgilmore186/research-paper-workflow
- Target branch: main
- Push policy: draft PR only, never merged. No direct pushes to main.
- Project rules: https://github.com/Sgilmore186/research-paper-workflow/blob/main/CLAUDE.md
- Dream Board: none (test board)
- Enrollment approval/source: Seph asked on 2026-11-28 to test live delegation to Codex and Claude Code without touching Gridline.
- Activation: test

## Run claim

- Owner: Claude Code (cloud, Duet thread)
- Run ID: cc-e2e-20261128-a
- Claimed/renewed UTC: 2026-11-28T17:11:04Z
- Starting target commit: aa18f43

Only one active implementation run per project. Follow agent-execution skill before claiming or recovering a claim.

## Priority repairs

None.

## Ordered phases

### E2E - Orchestrator smoke test

- Objective: prove dispatch, claim, duplicate refusal, overlap detection, STOP and validation work end to end in the cloud.
- Approval: 2026-11-28, Seph's request to test live delegation (see Enrollment).
- Dependencies: none
- Phase gate: each job's evidence recorded; no PR merged.

#### E2E-CC-1 - Claude Code cloud job

- **Objective:** a cloud Claude Code session picks up this job from the board and completes it.
- **Approval:** 2026-11-28, smoke test.
- **Dependencies:** none
- **Assignee:** claude-code
- **Touches:** e2e/claude_ping.py, e2e/test_claude_ping.py
- **Status:** pending
- **Claim:** none
- **Instructions:** Add `e2e/claude_ping.py` with `ping()` returning `"claude-code-cloud-ok"`, and `e2e/test_claude_ping.py` (unittest) asserting it. Change nothing else. Open a draft PR titled `[JOB orchestrator-e2e/E2E-CC-1] ...`.
- **Toolbox:** `python3 -m unittest discover -s e2e -v`; `python3 scripts/control.py`.
- **Acceptance criteria:**
  - The test passes when run by the validator (Duet), not just the executor.
  - The diff stays inside Touches.
  - Claim taken and released on this board with a run ID.
- **Evidence:** none yet
- **Handoff:** none yet

#### E2E-CODEX-1 - Codex cloud job

- **Objective:** a GitHub `@codex` mention starts a Codex cloud task that opens a PR, not only a review.
- **Approval:** 2026-11-28, smoke test.
- **Dependencies:** a Codex cloud environment for the target repo (Seph's ChatGPT Codex settings).
- **Assignee:** codex
- **Touches:** e2e/codex_ping.py, e2e/test_codex_ping.py
- **Status:** blocked
- **Claim:** none
- **Instructions:** Add `e2e/codex_ping.py` with `ping()` returning `"codex-cloud-ok"`, and `e2e/test_codex_ping.py` (unittest) asserting it. Change nothing else. Open a PR against main.
- **Toolbox:** `python3 -m unittest discover -s e2e -v`.
- **Acceptance criteria:**
  - Codex opens a PR from a dispatch issue mention.
  - Duet validates the test and the Touches boundary.
- **Evidence:** 2026-11-28 probe: `@codex` on Sgilmore186/claude-codex-bridge issue #2 got a reply from the Codex GitHub app within 6 seconds asking for a Codex cloud environment for that repo. No task started. Blocked until Seph creates environments.
- **Handoff:** none yet

#### E2E-OVERLAP-1 - Overlap probe (never executed)

- **Objective:** `control.py overlap` must report a clash with any active e2e job.
- **Approval:** 2026-11-28, smoke test.
- **Dependencies:** none
- **Assignee:** any
- **Touches:** e2e/
- **Status:** pending
- **Claim:** none
- **Instructions:** Do not execute. Probe only.
- **Toolbox:** `python3 scripts/control.py overlap orchestrator-e2e E2E-OVERLAP-1`.
- **Acceptance criteria:**
  - Exit 4 while E2E-CC-1 or E2E-CODEX-1 is active; exit 0 otherwise.
- **Evidence:** none yet
- **Handoff:** none yet

## Run handoffs

None yet.
