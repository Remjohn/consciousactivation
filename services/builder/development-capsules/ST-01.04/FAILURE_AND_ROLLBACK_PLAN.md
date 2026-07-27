# Failure and Rollback Plan

Validation failures are typed and occur before any commit. A blocked saturation
result is a successful immutable evaluation, not a partial failure, and its
downstream consequence remains `BLOCK`. Injected repository failure must atomically
leave no evaluation, receipt, event, command record or outbox item.

Rollback is non-destructive: deactivate or invalidate only a newly committed active
evaluation and restore the prior run snapshot in an isolated test transaction.
Never mutate Source Locks, Evidence Indexes, prior receipts or event history.
Regeneration after a governed input change creates a new identity and preserves the
historical invalidated evaluation for reproduction.
