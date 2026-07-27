# ST-06.01 Rollback Evidence

The category-binding repository performs every registry, authority, semantic-lineage,
and immutable-conflict check before committing a binding, command payload, and receipt.
The injected pre-commit failure test proves `0` bindings and `0` receipts remain after
failure. A typed rejection observation is emitted outside the governed commit state.

Rollback is non-destructive: existing immutable category bindings are never mutated.
Removing the two additive modules and reverting the explicitly listed manifest/export
contract additions restores the prior product surface; no data migration, shared schema,
external service, or persistent category store was introduced.

Evidence:

- `test_injected_atomic_failure_leaves_zero_partial_state`: `PASS`.
- conflicting same-command payload rejection: `PASS`.
- same-version category replacement rejection: `PASS`.
- original receipt replay without duplicate state: `PASS`.

