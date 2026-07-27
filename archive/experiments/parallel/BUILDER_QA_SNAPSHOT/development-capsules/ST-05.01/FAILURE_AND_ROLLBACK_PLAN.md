# Failure and Rollback Plan

All validation precedes commit. Invalid registry bytes or pins, nonempty skill data, duplicate/conflicting capabilities, unsupported dependency or cycle, unsupported maturity, stale evaluator identity, unauthorized actor, stale/invalidated context, altered lineage, conflicting idempotency payload, and prohibited operation return typed failures.

The in-memory development repository must support injected failures at every authorized write boundary. A failed transaction commits zero snapshots, receipts, events, observations, command records, run references, or invalidations. Removing the injected fault permits a clean retry with the same deterministic identity.

Rollback is non-destructive: revert only the six authorized source additions/changes, exact architecture-set updates, and ST-05.01 tests. Governance, predecessor artifacts, receipts, and historical events are never mutated. If an active upstream artifact is reopened or invalidated, emit a new descendant invalidation record and retain the prior snapshot and receipt for historical reproduction.
