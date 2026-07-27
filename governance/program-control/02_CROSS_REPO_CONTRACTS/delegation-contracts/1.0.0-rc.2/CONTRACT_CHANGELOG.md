# Contract Changelog

This changelog covers the canonical shared delegation contracts under
`packages/`. The historical draft artifacts under `contracts/` remain source
evidence and are not the active Stage 3 release-candidate registry.

## 1.0.0-rc.2 - 2026-07-14

Status: remediated release candidate, not published or signed.

### Corrected

- Replaced all 26 blanket authority wildcards with exact generated JSON
  Pointer templates for every field and governed collection item.
- Aligned amendment proposal/response, selective invalidation, revocation,
  replacement, and compatibility-manifest producers to the Stage 2 authority
  specifications.
- Replaced the local lifecycle vocabulary with the 19 locked external states
  and a 44-row normalized expansion of the TS-DLG-03 transition table.
- Added complete direct negotiation, contextual adapter, and owner-evidenced
  immutable migration fixtures with positive, repeat, lossy, and missing-owner
  vectors.
- Replaced the Format 02 portfolio with the normative SCN-01 through SCN-10
  scenarios, including exact identities, fixture hashes, authority,
  lifecycle, audit, outbox, effect counts, projections, prohibited effects,
  negative variants, and race schedules.
- Expanded the Delegation Set reference fixture to three independently
  identified members.

### Compatibility

- The wire protocol remains `1.0`; this release-candidate bump records package
  correction before publication.
- `contract-migration` now records multiple target artifacts, ordered
  transformations, authority-effect analysis, source/target validation,
  equivalence, and immutable output/evidence references.
- `AssetResultContract` now distinguishes complete and policy-valid partial
  results and names unresolved roles.

### Readiness

Local Stage 4 semantic gates are re-evaluated after generation and conformance
testing. Publication and Stage 5 authorization remain blocked until external
owners ratify boundaries and an immutable signed release can be created.

## 1.0.0-rc.1 - 2026-07-14

Status: release candidate, not published or signed.

### Added

- Twenty-six closed Draft 2020-12 JSON Schemas with canonical IDs at protocol
  version `1.0`.
- One registry for schema identity, hashes, producers, consumers, idempotency
  classes, and lifecycle effects.
- Producer authority and lifecycle transition registries.
- Generated Python `TypedDict` and TypeScript top-level bindings.
- Deterministic schema, canonicalization, authority, lifecycle, compatibility,
  and Format 02 fixture validators.
- Ten executable Format 02 reference scenarios.
- A release manifest that hashes all Stage 3 package files.

### Breaking Corrections From The Draft Package

- Replaced the conditionally-owned `submission-receipt` with the
  protocol-owned `submission-validation-receipt` and VAE-owned
  `admission-receipt`.
- Removed `authorization.downstream_consumption_authorized` from the VAE-owned
  `asset-result-contract`. Consumption authority exists only on the
  Content Harness-owned `result-acknowledgement`.
- Replaced bare demand strings with the exact `DemandIdentityRef` tuple:
  `request_id`, `version`, `payload_hash`, and `canonical_ref`.
- Closed every public object with `additionalProperties: false`.
- Replaced unconstrained editor state with typed public lifecycle events and a
  protocol-owned state transition registry.
- Prohibited floating-point values in the canonical profile. Ratios use basis
  points and currency uses integer minor units, preserving RFC 8785-compatible
  deterministic bytes without cross-runtime number ambiguity.

### Migration

- `demand_ref:string@0.1` may be adapted only when an exact pinned demand
  identity context is supplied and matches the legacy request ID.
- `submission-receipt@0.1` has no automatic adapter. Migration requires the
  original producer, protocol validation decision, and editor admission
  decision so the two owner-specific facts can be reconstructed honestly.

### Publication Gate

The release candidate is intentionally unsigned and untagged. Publication is
blocked by absent upstream product repositories and source artifacts, missing
owner ratification, missing trust-root/key-lifecycle infrastructure, and the
absence of a Git repository in this checkout. No product may freeze a public
adapter against this release candidate as though it were a published baseline.
