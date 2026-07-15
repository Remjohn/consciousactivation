# Failure and Rollback Plan

All identity, authority, input, snapshot, context, capability, alternative, gap-evidence, and brief-disposition validation precedes commit.

Reject altered or inactive lineage, missing target-failure evidence, skipped alternatives, unnecessary skill proposals, implicit ownership, hidden workflow behavior, same-version mutation, unauthorized actors, and prohibited skill operations with typed errors.

The in-memory development repository supports injected failure at the single authorized write boundary. Failure commits zero decision, receipt, event, command record, run reference, observation, or invalidation. Removing the injected fault permits a clean retry with the same deterministic identity.

Rollback is non-destructive: revert only the six allowed source modifications, ST-05.02 tests, and completion evidence. The ST-05.01 snapshot/receipt and all governance and predecessor artifacts remain immutable. Upstream invalidation emits a new descendant invalidation and retains historical decision bytes.
