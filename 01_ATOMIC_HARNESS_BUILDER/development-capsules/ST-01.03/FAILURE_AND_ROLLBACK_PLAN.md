# Failure and rollback plan

Fail closed before commit on missing or inactive Source Lock, incomplete descriptor
coverage, duplicate/colliding identity, invalid provenance or knowledge status,
authority denial, stale stream version, altered lineage or conflicting idempotency
payload.

The repository validates the event, index, receipt, Source Lock, authority and command
record before one synchronized commit. Injected failure leaves the run stream, index
store, receipt store, command store and outbox unchanged.

A committed index is immutable. Rollback is non-destructive: issue an immutable
`EvidenceIndexInvalidation`, detach the active run reference through a governed event,
and preserve the original index and receipt for historical replay. A replacement
requires a new command and new immutable index identity.

Observation delivery is retried from the durable in-memory development/test outbox;
delivery failure never rolls back committed authoritative state or reports a false
uncommitted result.
