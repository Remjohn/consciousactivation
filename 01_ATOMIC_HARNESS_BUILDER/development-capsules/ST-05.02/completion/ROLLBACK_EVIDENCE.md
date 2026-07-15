# ST-05.02 Rollback Evidence

## Atomic failure

The Story test suite injects failure at the single authorized in-memory commit boundary. The failure leaves zero necessity decisions, receipts, run references, events, observations, command records, or invalidations. Removing the injected fault permits a clean retry with the same deterministic decision and receipt identities.

## Non-destructive invalidation

Reopening an upstream governed artifact creates a new `SkillNecessityInvalidation`; it does not mutate the historical necessity decision or receipt. The prior active decision becomes unusable for new active work, while its canonical bytes, hash, evidence, and governing lineage remain reproducible.

Replay and resume restore the same decision reference and run-state hash. Repeating an identical command returns the original receipt without duplicate state; changing the payload for the same command identifier fails closed.

## File rollback boundary

A source rollback removes only the ST-05.02 additions from these six allowed source files:

- `src/cmf_builder/domain/skill_registry.py`
- `src/cmf_builder/application/skill_commands.py`
- `src/cmf_builder/domain/run.py`
- `src/cmf_builder/application/atomicity_commands.py`
- `src/cmf_builder/application/ports.py`
- `src/cmf_builder/adapters/in_memory_run_repository.py`

It also removes the six Story-local test files and the six separate ST-05.02 completion artifacts. No ST-05.01 snapshot, registry fixture, policy, predecessor receipt, governance artifact, schema, shared contract, or historical evidence is mutated.

## Evidence

- injected atomic failure and zero partial state: PASS
- clean retry: PASS
- payload-safe idempotency: PASS
- conflicting-command rejection: PASS
- replay and checkpoint resume: PASS
- upstream descendant invalidation: PASS
- stale invalidated decision rejection: PASS
- historical reproduction after invalidation: PASS
- external state requiring cleanup: none

Rollback verdict: **PASS**.
