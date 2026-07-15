# Relevant Accepted ADRs

- **ADR-007 — Evidence Identity and Source Profiles** (owned obligation),
  `docs/architecture/adr/ADR-007-EVIDENCE-IDENTITY-AND-SOURCE-PROFILES.md`,
  SHA-256 `cbf2353989544486907827ef141ee2cb07f7a5d0aa61d3862db7b1fc8df97725`.
  It governs SHA-256 source identity, portable provenance, read-only sources,
  archive safety, and aggregate Source Lock semantics. BD-004 remains active
  only for the real-profile branch.

- **ADR-001 — Product Boundary and Modular Monolith** (supporting),
  SHA-256 `ac021e5b1567922e56ecf644e420d9ce2bc3f36d21ee46c8fbdb7b0a3ca27531`.
  Domain/application/adapter boundaries and external-runtime prohibitions are
  mandatory.

- **ADR-003 — Authoritative State and Artifact Storage** (supporting),
  SHA-256 `77911f5a7aa4b10047196bc0cca1fc3f89cadd01e85f688a07adcf8b374a7f16`.
  The Story defines an atomic repository port and a deterministic in-memory
  development/test adapter. PostgreSQL/CAS production adapters are not claimed
  or required for this bounded proof.

- **ADR-005 — Human-Agent-Code Authority** (supporting), SHA-256
  `783835d294590b52737f841adf59f588bce41bbae4fd3d2e0b7ddcc425aaf92e`.
  Source-lock commit is a deny-by-default deterministic command; agents and
  external actors cannot commit it.

- **ADR-012 — Sandbox and Least Privilege** (supporting), SHA-256
  `0c8c0d0e9dff8ce1ec9a61069946b1d3998bc870c1c9eefc84859c3c8f83b477`.
  Read-only source access, root confinement, no network, bounded resources,
  and cleanup are enforced.

No ADR is changed by this implementation capsule.
