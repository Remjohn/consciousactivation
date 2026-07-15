# Failure and rollback plan

All failures are typed and fail closed. Required classes cover missing/mismatched/stale/invalidated upstream references; non-synthetic profile substitution; incomplete governed metadata; missing provenance; authority promotion; semantic invention; forbidden Workflow IR fields; unsupported schema version; missing migration; malformed deprecation; same-version rewrite; stale concurrency; idempotency payload mismatch; and injected atomic commit failure.

The persistence operation must atomically commit the immutable IR snapshot, run event/reference, lifecycle transition, command record, and compilation receipt. The injected-failure seam must prove zero partial snapshots, events, references, command records, or receipts.

An authorized upstream boundary reopen must preserve the original IR snapshot/history, emit an IR descendant invalidation, prevent downstream consumption, and require a new immutable IR revision after a new boundary version. Invalidation is not destructive rollback.

Source rollback is additive: remove the three new modules and Story tests, restore the nine allowlisted existing files to completion-manifest hashes, and rerun the prior `84` tests. No database, schema, migration, persistent store, network state, external compensation, or prior receipt rewrite is required. Do not execute a destructive workspace rollback; issue hash-based evidence.
