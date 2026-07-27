# Failure and Rollback Plan

All semantic, authority, concurrency, lifecycle-storage and archive failures are
fail-closed with zero partial state. Observation delivery is the sole post-commit
degraded case: the command remains successful, its receipt is returned and pending
observations remain retryable through the governed outbox.

Rollback is non-destructive:

1. Preserve all original Story receipts and historical artifacts.
2. Revert only the seven allowlisted production diffs and remove new correction tests.
3. No migration, database, schema, external dependency or stored production data exists.
4. Demonstrate pre/post repository snapshots for every injected failure.
5. Demonstrate a clean retry after failure and historical replay after invalidation.
6. If any correction changes valid canonical artifact bytes unexpectedly, fail the
   correction gate and restore the pre-correction implementation before issuing receipts.

