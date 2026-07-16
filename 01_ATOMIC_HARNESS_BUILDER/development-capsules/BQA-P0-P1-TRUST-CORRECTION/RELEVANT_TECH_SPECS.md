# Governing Technical Specifications

- `TS-01 — Governed Lifecycle and Target Profiles`: command transaction boundary,
  expected stream version, one event and receipt per transition, idempotency,
  replay, concurrency conflicts, failure behavior and observability.
- `TS-02 — Configured Evidence Workspace`: exact source-byte SHA-256 identity,
  immutable Source Locks, read-only archive inspection, archive safety and
  hash-mismatch failure.
- `TS-06 — Evaluation, Repair, Authorization and Artifact Integrity`: evaluated
  identity must match the receipt; partial outputs remain quarantined; authority
  and evidence trace cannot be replaced by self-consistent hashes.
- `TS-11 — Category Constitutions and Target Compilers`: semantic non-mutation,
  deterministic target-package identity, compatibility separation, false
  certification rejection and target compiler authority.
- `TS-13 — Implementation Authorization and Development Capsule`: exact hashes,
  failure-rooted correction, supplemental receipts and atomic capsule evidence.

No specification is changed by this capsule.

