# ST-07.02 Rollback Evidence

## Atomic failure

The Story suite injects failure at the single authorized in-memory definition commit boundary. The failure leaves zero definitions, receipts, run references, events, observations, command records, milestone state, or invalidations. Removing the injected fault permits a clean retry with the same deterministic definition and receipt identities.

## Non-destructive invalidation

An authorized upstream boundary reopen creates the complete descendant invalidation chain, ending in `AtomicHarnessDefinitionInvalidated`. The active definition becomes unusable for new work. Its historical canonical bytes, hash, receipt, and exact authority lineage remain reproducible from the pre-invalidation event stream. Replay, checkpoint resume, and identical-command retry do not duplicate state.

## Source rollback boundary

A source rollback removes only:

- `src/cmf_builder/domain/atomic_harness_definition.py`;
- `src/cmf_builder/application/definition_commands.py`;
- the bounded ST-07.02 additions from `run.py`, `atomicity_commands.py`, `ports.py`, and `in_memory_run_repository.py`;
- the two ST-07.02 source entries from the seven authorized predecessor architecture tests;
- the six ST-07.02 Story test files;
- the six ST-07.02 completion artifacts.

The human-authorized capsule-amendment records remain historical governance evidence and are not silently deleted. No predecessor receipt, authority source, governance artifact, contract/schema, planning baseline, external repository, or immutable historical Builder artifact is mutated by rollback.

## Evidence

- injected atomic failure and zero partial state: PASS;
- clean retry: PASS;
- payload-safe idempotency: PASS;
- conflicting-command rejection: PASS;
- replay and checkpoint resume: PASS;
- upstream descendant invalidation: PASS;
- stale or invalidated definition rejection: PASS;
- historical reproduction after invalidation: PASS;
- external state requiring cleanup: none.

Rollback verdict: **PASS**.
