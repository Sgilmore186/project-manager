---
name: duet-planning
description: Capture Seph's project ideas in a Dream Board, clarify one necessary decision at a time, and promote explicitly approved ideas into the central Development Board with executable tasks.
---

# Duet planning

Read Sgilmore186/project-manager AGENTS.md and docs/AGENT_WORKFLOW.md. Read the relevant project rules and current boards first.

## Brainstorm

- The project repository owns docs/DREAM_BOARD.md. Search for an existing idea before adding a new one. Record the actual request, source/date, open questions, assumptions and status. Do not write private conversation details to a public repository.
- Distinguish an idea, a design proposal and explicit approval. Brainstorming never authorizes implementation.
- Discuss one blocking design decision at a time; do not make Seph answer a long questionnaire. Use sensible defaults for minor details and disclose them. Do not ask again about settled decisions.
- Do not change overall project priorities or focus without Seph's direction. Use pm-update for changes to the existing project registry.

## Promote

- When Seph approves a feature, record a dated approval summary and source reference (no private transcript). Read the existing Development Board and relevant project specs; reconcile completed or active work and preserve old IDs.
- Create an ordered phase or add tasks to the appropriate existing phase. Break only the approved scope into small verifiable tasks using templates/TASK.md. Each task has objective, dependencies, instructions, toolbox, acceptance criteria, status/evidence and approval reference. Do not invent authorization for extra features.
- Keep future phases coarse until their design is ready. Mark unresolved requirements as blocked rather than granting implementation approval. If a claim is active, coordinate rather than editing under an agent's feet.
- Update the central board first and verify the remote change. Link the Dream Board idea to the approved phase/task IDs, without duplicating live status. If a cross-repo write fails, report the incomplete link and reconcile on the next run.
- Respect both repos' push and review rules. No forced pushes, fake approvals, private data or unsupported publication.

## Report

Say what changed, what was approved, what remains a dream and the next actual decision if one is needed. Do not start implementation unless assigned a separate development run.
