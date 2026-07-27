# Observability plan

Emit `implementation_plan_compilation_started`, one
`implementation_plan_increment_compiled` observation per increment,
`implementation_plan_compilation_committed`, replay and rejection observations.
Each carries run, Story, plan identity, authority, parent capsule provenance,
outcome, command, correlation, causation and failure context.

