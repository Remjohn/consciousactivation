# Failure and Rollback Plan

All target, identity, hash, version, active-state, lineage, authority, provenance, semantic completeness, compatibility, and synthetic-scope validation precedes commit.

Reject missing, altered, stale, superseded, invalidated, category-bound, external-target, falsely certified, semantically flattened, or unauthorized inputs with typed errors. Reject any definition that omits an explicit required or `NOT_APPLICABLE` field.

The in-memory development/test repository supports injected failure at the single authorized write boundary. Failure commits zero definition, receipt, event, command record, run reference, observation, or invalidation. Removing the injected fault permits a clean retry with the same deterministic identity.

Rollback is non-destructive: revert only the six allowed source paths, four exact-source architecture updates, ST-07.02 tests, and completion evidence. Predecessor artifacts and receipts remain immutable. Upstream invalidation emits a new descendant record and retains historical definition bytes.

