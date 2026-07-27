# Test Plan

Story tests must cover:

- complete synthetic coverage and exact `PASS`/`PROCEED` result;
- every FR-018 outcome, including guarded human-only limitations;
- missing role, sparse evidence, unreadable/quarantined evidence, contradictory
  sources, contradictory authority and unresolved provenance classifications;
- `HG-002`, unsupported `NOT_APPLICABLE`, stale/altered/invalidated lineage and
  unauthorized actor rejection;
- deterministic identities, canonical ordering and fresh-context byte equality;
- payload-safe idempotency, conflict rejection and post-commit outbox retry;
- injected atomic failure with no evaluation, receipt, event or command record;
- replay, resume, upstream invalidation and historical reproduction;
- required observations and exact-source architecture boundaries.

Run the Story suite twice, directly affected architecture and correction suites,
then the complete repository suite with `PYTHONPATH=src;.`. No mandatory skip is
permitted. Compile every Python file in memory. Rollback demonstration must remove
only the Story-created active descendant state in an isolated repository while
leaving predecessor artifacts unchanged.
