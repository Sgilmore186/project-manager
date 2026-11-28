# Development Boards

One board per enrolled project: development/<project-id>/BOARD.md. Project ID must match an existing record in projects.json. No board here means the project is not enrolled in this workflow.

Exception: `orchestrator-e2e/` is a test board (Activation: test) for the orchestration smoke test. It is not a registry project and normal runs never select it.

Use [the workflow](../docs/AGENT_WORKFLOW.md) and [board template](../templates/DEVELOPMENT_BOARD.md) to enroll. Do not infer authorization from legacy project open items or Dream Boards. Existing project-specific work queues remain in force until explicitly migrated.
