# Nightly run entrypoint

The actual scheduled task is configured in the chosen agent platform, not by this file. Use a runner with access to Project Manager and the target repository, a usable execution environment, and permission to test and push. With Project Manager in the runner's workspace, Codex can discover the entry point in `.agents/skills/agent-execution/` and Claude Code in `.claude/skills/agent-execution/`. Both load the canonical `skills/agent-execution/SKILL.md`. Explicitly load the canonical skill if native discovery is unavailable; a remote repository alone does not install a skill.

## Portable trigger prompt

```text
Open or fetch the latest main of Sgilmore186/project-manager.
Read AGENTS.md. Run python3 scripts/control.py status; if it prints STOPPED, report the reason and stop.
Then load and follow skills/agent-execution/SKILL.md.
Use the explicitly assigned project ID if provided; otherwise use the active primary project. If an assignee is given (claude-code or codex), take only tasks assigned to it or to any.
Process the approved central Development Board in order. Verify existing work before implementing, prioritize defects and code quality, load only relevant skills, test, push where authorized, verify remotely, update evidence and repeat while productive usage remains.
Leave a concise handoff and release the claim before stopping. Do not buy credits, bypass permissions or invent tasks beyond approved scope.
```

Optional arguments: project ID and assignee. Omitting it uses the current active primary. No enrolled board, no primary, unresolved claim or unavailable required tooling means stop safely and report.

## Enablement checklist

- Shared infrastructure merged and readable from main.
- Project enrolled and legacy work queue reconciled.
- Agent access, native skill discovery (or explicit loading) and toolchain checked; read-only routing trial succeeds.
- Target branch policy and central board write policy verified.
- Platform schedule set after the actual usage reset if applicable; confirm the schedule on that platform. Do not infer account reset time.
- First supervised or bounded run verifies claim, task selection, tests, remote push, evidence and release of claim.

Do not schedule concurrent implementations for the same project. No independent morning review or custom scheduler in the first version.
