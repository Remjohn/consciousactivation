# CAE-BMAD Routing Model

The router should inspect:

1. current project state
2. artifact statuses
3. research completion
4. unresolved decisions
5. current user request
6. BMAD base capabilities
7. CAE workflow gates

It should recommend the minimum next valid step.

When multiple paths are possible, prefer the one that closes the earliest dependency.

Never recommend Architecture merely because the user asked about architecture if Product Brief/PRD/FR prerequisites are unresolved.

Never recommend a full research pass when the specific claim can be resolved by a targeted repository inspection.

Never treat "file exists" as "workflow complete".
