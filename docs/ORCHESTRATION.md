# Orchestration

How Duet runs Codex and Claude Code from the central Development Boards, with Seph's MacBook off.
Adopted 2026-11-28 on Seph's direction: build on this board, no MacBook dependency, no Cloudflare or other external server, no paid API, no new subscription.

This adds a dispatch layer to the [agent workflow](AGENT_WORKFLOW.md). It does not replace it. Boards, claims, approvals, phase gates and evidence work exactly as written there.

## Roles

| Role | Who | Does |
| --- | --- | --- |
| Owner | Seph | Approves scope, merges PRs, clears STOP, changes account settings |
| Orchestrator | Duet (Claude Duet main chat and its cloud routines) | Files and assigns jobs, checks STOP and claims, dispatches, validates results, reports to Seph |
| Executor | Claude Code (cloud session) | Runs [agent-execution](../skills/agent-execution/SKILL.md) on a job assigned to it |
| Executor | Codex (cloud, chatgpt.com) | Runs a job Duet dispatches through a GitHub `@codex` mention |
| Optional executor | Codex on the Mac, or the claude-codex-bridge daemon | Same rules; only works while the Mac is on |

## Jobs

A job is a board task. Its ID is `<project-id>/<task-id>`, for example `football-game/B-025/r1`. Two task fields drive dispatch (see [the task template](../templates/TASK.md)):

- **Assignee:** `claude-code`, `codex` or `any`. Duet sets it when it promotes or dispatches a task. An executor only claims tasks assigned to it or to `any`.
- **Touches:** the files or folders the task may change in the target repo, comma separated. Globs are allowed. Duet uses it to stop two jobs editing the same code.

Statuses are the template's, plus `dispatched`: Duet handed the job to an executor that can't write the board itself (Codex cloud). It counts as active work.

## Lanes

| Lane | How Duet starts it | Mac off? | Who writes the board |
| --- | --- | --- | --- |
| Claude Code cloud | A Duet routine (scheduled cloud session) runs the [nightly prompt](NIGHTLY_RUN.md) with the project ID and `assignee claude-code` | Yes | The Claude Code run itself |
| Codex cloud | Duet opens a dispatch issue in the target repo and comments `@codex` with the task | Yes, once the repo has a Codex cloud environment | Duet, on Codex's behalf |
| Codex on Mac / bridge | Seph or a Mac schedule | No | The Codex run itself |

Codex cloud works in its own container with only the target repo, so it can't read this repo or push claims. Duet holds the claim for it and records the result.

## Dispatch (Duet)

Run in this order. Stop at the first failure and report it.

1. `python3 scripts/control.py status`: must print `RUN`.
2. `python3 scripts/control.py ready <project-id>`: board active, no run claim held.
3. `python3 scripts/control.py overlap <project-id> <task-id>`: no overlap with active work.
4. Duplicate check: search the target repo for open issues or PRs whose title starts with `[JOB <project-id>/<task-id>]`, and read the task's Status and Evidence. Anything open or already done means don't dispatch.
5. Claim (Codex only): fetch main, write the run claim (Owner `Codex cloud via Duet`, run ID, UTC time, starting target commit) and set the task to `dispatched` with Assignee `codex`. Normal push, then fetch and confirm the claim is yours. A Claude Code run claims for itself in agent-execution, so Duet doesn't pre-claim for it.
6. Dispatch:
   - Claude Code: start the routine for that project. It claims, works, records and releases on its own.
   - Codex: open issue `[JOB <project-id>/<task-id>] <title>` in the target repo with the task card (objective, instructions, Touches, acceptance, test commands). Then comment `@codex` asking it to implement the issue and open a PR against the target branch. Record both links in the task's Evidence.
7. Recheck STOP right before step 6. If it's set, release the claim and stop.

## Results (Duet)

When a job's PR or branch arrives:

1. Check STOP. If set, record what arrived and don't validate or report it as done.
2. Read the diff. Every changed path must be inside the task's Touches. Anything else means `needs-fix`.
3. Fetch the branch and run the task's test commands yourself. Check required CI. A pending check is not a pass.
4. Record commit or PR, commands and results in the task's Evidence. Set `implemented`, `validated` or `needs-fix`.
5. Release the run claim, with a short entry in Run handoffs.
6. Report to Seph: what was done, what passed, the PR link, and what's his.

Duet doesn't merge. Seph merges, unless he authorizes Duet to merge for a named project in writing on that board. A board's direct-push policy covers an executor's own pushes, not merging someone else's PR.

## Duplicates and conflicts

- One run claim per project (v1). It is the main guard: a second agent sees the claim and stands down.
- Claims use Git's compare-and-swap: a claim push that loses the race is rejected as non-fast-forward. Re-read, never force.
- Job IDs are permanent, and step 4 above finds an earlier dispatch of the same job.
- Touches plus `control.py overlap` catch two jobs on one repo touching the same paths, including across boards.
- A stale claim (`control.py claims` flags over 6 hours) is reported, never stolen, until the target repo and the owner show the old run has stopped.
- A Codex cloud task can't be cancelled from GitHub. If one finishes after its job was released or done elsewhere, Duet reports the PR as a duplicate for Seph to close.

## STOP (system-wide)

A file named `STOP` at the root of this repo's main branch halts all agent work on every project. Its first line is the reason.

**Set it:** anyone may, at any time, by a direct push to main. Seph can do it from the GitHub app: Add file, name it `STOP`, write one line, commit. Setting STOP only reduces activity, so it skips the PR rule.

**Clear it:** only Seph, or an agent on his explicit word, by deleting the file. The commit message says who cleared it.

**Who checks, and when:** `python3 scripts/control.py status` exits 3 while STOP is set.

- Every executor: at route, before claiming, before every push to a target repo, and before starting the next task.
- Duet: before dispatching, before every `@codex` mention, and before validating or reporting a result.
- Scheduled routines: first step of every run. A stopped run exits after one short report.

**What a running agent does when it sees STOP:** stop changing code, push nothing to the target's main, release its claim with a short handoff (board-only writes stay allowed so work can resume cleanly), and report.

**Limits:** a Codex cloud task that already started can't be stopped from here; its PR is simply not validated or merged. The claude-codex-bridge daemon has its own `.runtime/STOP`; run `python3 -m bridge stop` on the Mac too if it's running. After Seph clears STOP, nothing resumes by itself: the next scheduled run or dispatch starts fresh.

## With the Mac off

Works: this repo, the boards and claims (GitHub), Duet's routines and Claude Code cloud sessions, Codex cloud via `@codex`, CI.
Doesn't: Codex on the Mac, the bridge daemon, anything that needs Seph's local sign-ins or files.

## Known limits (v1)

- Each target repo needs a Codex cloud environment before `@codex` can run a task there. Only Seph can create it, in his ChatGPT Codex settings.
- Codex cloud and Claude Code usage come from Seph's existing plans. Runs stop at usage limits; nothing buys more.
- Duet's routines can't message Seph's other Claude Code sessions; a routine starts a fresh cloud session instead.
- Browser-only checks (Playwright sims) need a lane with a browser; say so on the task.
- The smoke test board is [development/orchestrator-e2e](../development/orchestrator-e2e/BOARD.md). It is a test board, never selected by normal runs.
