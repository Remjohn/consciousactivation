# Governing ADRs

- `ADR-001`: preserve the modular-monolith command boundary and one canonical model.
- `ADR-003`: atomic commands, optimistic concurrency, command receipts, outbox,
  immutable artifact references and transaction-manager semantics. This correction
  implements only the current in-memory adapter seam, not PostgreSQL or S3.
- `ADR-004`: deterministic compilation, content identity, atomic artifacts and
  explicit drift rejection.
- `ADR-005`: actor/action/resource/expected-version authority is deny-by-default.
- `ADR-007`: exact source-byte identity, immutable descriptors, read-only archive
  inspection and fail-closed archive threats.
- `ADR-012`: least-privilege read-only evidence access; no external runtime or network.
- `ADR-013`: target compiler semantic authority and external-boundary separation.
- `ADR-016`: logs, metrics, traces, events and receipts are distinct; telemetry
  interruption must have a typed non-ambiguous outcome.

All accepted ADR decisions remain unchanged.

