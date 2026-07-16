# Failure and rollback plan

All command failures are typed and fail closed. Required rejection classes cover input/hash drift, missing or mismatched Source Lock, invalid synthetic classification, unresolved critical contradiction, incomplete human decision package, authority denial, unratified promotion, immutable-version violation, silent boundary mutation, downstream field-authority violation, stale concurrency version, idempotency payload mismatch, and injected atomic commit failure.

The persistence operation must atomically commit the human decision, ratification when applicable, Draft Harness Model, lifecycle/invalidation events, command record, and receipt. The injected failure seam must prove zero partial events, models, decisions, command records, receipts, and lifecycle transitions.

Rollback is non-destructive because this Story adds only source, tests, and in-memory development/test state. It introduces no database, schema, migration, persistent store, network side effect, or external compensation. Demonstrate rollback by removing the three new source modules and the Story tests, reverting the allowlisted additive edits, and rerunning the prior `57` tests. Do not execute a destructive workspace rollback; record hash-based reproducibility and injected-failure evidence.

Reopening a boundary is not a rollback. It is a governed human action that emits invalidation, preserves history, blocks the old model, and requires a new immutable version.
