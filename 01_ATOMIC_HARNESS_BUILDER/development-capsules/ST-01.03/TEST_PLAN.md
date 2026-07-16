# Test plan

Create a Story fixture that starts the existing synthetic run and completes
`ST-01.02` to obtain its authoritative `SourceLock`.

- Acceptance: complete descriptor-to-specimen coverage, typed observation/status/
  knowledge/provenance separation and query behavior.
- Identity: canonical ordering, stable specimen identity, exact Source Lock lineage,
  changed-input identity and fresh-context byte equality.
- Failure and authority: missing/unaccounted descriptors, collisions, altered lock,
  missing provenance, unsupported knowledge status, stale version, invalidated lock,
  unauthorized actor and conflicting command payload.
- Atomicity and rollback: inject repository failure before commit; prove zero index,
  receipt, event and command record. Inject observation failure after commit; prove a
  committed receipt and retryable outbox.
- Scale: compile 100,000 deterministic descriptors through the pure domain compiler
  and assert exact count, ordering, identity and bounded one-pass output behavior.
- Replay/invalidation: duplicate-command idempotency, repository replay, active
  descendant invalidation and historical reproduction.
- Architecture: add only the two authorized source paths to every predecessor exact
  source set; imports remain standard-library and layered.

Run the Story suite twice, affected predecessor suites, correction suite and the full
repository suite before issuing a receipt. Every test is mandatory.
