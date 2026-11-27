---
name: agent-execution
description: Run approved project tasks autonomously, defaulting to the active primary project in Project Manager. Verify, test, push authorized changes and record evidence before continuing.
---

# Agent execution

Entry point: Sgilmore186/project-manager. Read its AGENTS.md and docs/AGENT_WORKFLOW.md. Follow the project's own AGENTS.md and permissions as well. This skill is for unattended and manual development runs, not for brainstorming.

## 1. Route and check access

- Sync Project Manager using scripts/pm.py sync in a git checkout. If unavailable, fetch current main and verify the revision. Do not work from stale copies.
- Read projects.json (or pm.py list/get). Use the explicitly assigned project ID if active; otherwise select the sole active primary project. If no active primary exists, stop with a short report. Do not choose a secondary on your own.
- Read development/<project-id>/BOARD.md. If no enrolled board exists, stop and report that enrollment is needed. Do not create one from guesses or treat legacy open_items as automatic authorization.
- Read the board's target repository, branch and push policy. Fetch it and read AGENTS.md plus the relevant spec. If permissions, scope, access or rules conflict, stop the affected work and report it. Never silently override them.
- Confirm available tools, runtime and actual usage/time budget when exposed. Do not assume reset times, buy credits or work around usage limits.

## 2. Pick and claim

- First inspect reproducible urgent defects (security, data integrity, broken tests, broken functionality), then necessary scoped code-quality/performance fixes, then unfinished tasks in the current approved phase in board order.
- A bug or necessary repair within approved scope can be added by an agent: record reproduction, scope, acceptance and evidence. No new feature, unrelated cleanup, permission expansion or major rewrite without Seph's approval.
- Check dependencies, approval evidence, existing commits, tests, current claims and relevant project-local legacy claims. Do not start a later phase while an earlier required task or phase gate is open. Skip active claims, unrelated blocked tasks and proposals. Work on another independent eligible task in the same phase if possible.
- Use a unique run ID and UTC time. Fetch main, acquire the board's single-writer run claim with a normal non-force push, then fetch and confirm ownership before modifying the target. If a competing claim wins, do not continue. Connector-only agents without a reliable way to claim must stop. Never automatically steal a stale claim without checking target state and whether the old agent is still active; if uncertain report the blocker.
- Update the task to in-progress with owner, run ID, timestamp and starting commit. If another agent has a conflicting local claim, leave that task alone.

## 3. Execute efficiently

- Verify whether the acceptance criteria already hold before implementing. If yes, record actual evidence and skip the rewrite. If partly built, complete only the gap.
- Read only this task's instructions, referenced specifications and relevant toolbox skills. Choose the least costly suitable tools. Use existing scripts and deterministic tests before extra AI analysis.
- Keep changes coherent and reversible. Record a starting commit. Avoid unrelated formatting or architecture churn; preserve user changes and backward compatibility.
- Test relevant behaviors, regressions and project-required checks. Run builds and simulations when required. Never fake test results or mark unrun checks as passing. Fix verified defects before declaring success.

## 4. Push, verify and record

- Follow target branch policy. Where direct pushes are explicitly permitted, fetch/reconcile, push without force and verify the remote contains the intended commit. Otherwise create/update a PR and leave merge pending unless separately authorized. Never bypass branch protection or deploy private data.
- Check required CI when available. A pending/unavailable check is not a pass. If required checks fail, investigate or mark blocked/needs-fix; preserve a working baseline and do not publish a broken build.
- Record commit/PR, test commands and results, acceptance evidence, remaining checks, publication/playtest status and next step in the central board. A task is done only when its stated gates pass; validated code awaiting an external gate remains validated or blocked. Do not repeat verified implementation just because a later gate remains open.
- Use scripts/pm.py for any change to existing ideas.json, projects.json or log.md; keep coarse project progress aligned only when a real milestone changes. Do not manually edit those files. Verify board and target writes remotely.
- Re-read the board and project status before the next task. Renew the run claim on progress and release it in the final report. If interrupted, leave enough evidence to resume safely.

## 5. Finish

Continue while eligible useful work and usage remain. Reserve time/usage for checks, pushes and a concise report. Stop if no task is eligible, the project is paused, verification cannot proceed safely, or limits are near. Never consume tokens merely to exhaust a quota.

Report: project, run ID, tasks done/skipped/blocked, target commits or PRs, actual checks and CI status, discovered defects, remaining steps, any decisions/limitations. No private data in Git. Independent morning review is intentionally out of scope for v1.
