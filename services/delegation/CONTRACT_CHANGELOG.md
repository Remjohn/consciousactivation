# Contract Changelog

historical_evidence: true

This changelog covers the canonical shared delegation contracts under
`packages/`. The historical draft artifacts under `contracts/` remain source
evidence and are not the active Stage 3 release-candidate registry.

## 1.1.0-rc.4 - 2026-07-15

Status: portable derivative-lock inheritance correction candidate, unsigned
and not production-authorized.

### Added

- Added closed `derivative-lock-inheritance@1.0` with authoritative parent,
  parent contract version, immutable parent lock evidence/hash, derivative
  locks, derivation type, semantic classification, and upstream authorization.
- Added a transport-neutral release-only validator returning typed inheritance,
  evidence, removal, weakening, authorization, and classification outcomes.
- Added generated Python/TypeScript structures, deterministic fixtures,
  no-guess legacy migration declaration, adapter-preservation checks, and
  compatibility enforcement claims for derivative asset flows.
- Added release-only and reference-engine tests for exact inheritance, stricter
  locks, removal, weakening, missing evidence, ambiguous/semantic derivation,
  authorized successor-demand relaxation, and parse-without-enforcement.

### Preservation

RC3 remains immutable historical evidence. Visual Asset Demand and VAE boundary
bytes, envelope protocol `1.0`, compatibility profile `1.0`, source-kind,
interview provenance, Activative lineage, authority, lifecycle, acceptance,
acknowledgement, replay, idempotency, cancellation, amendment, supersession,
replacement, and Delegation Set behavior remain unchanged.

## 1.1.0-rc.3 - 2026-07-14

Status: convergence identity and packaging correction candidate, unsigned and
not production-authorized.

### Corrected

- Corrected the Node contract package and both Python package declarations to
  the current immutable candidate identity.
- Added generated Python and TypeScript package, envelope-protocol, Visual
  Asset Demand, and compatibility-profile version constants.
- Added an exhaustive release-relative stale-identity scanner. Active RC1/RC2
  package declarations fail validation; explicitly marked historical evidence
  remains permitted only in governed changelog or rejection-history files.
- Added exact identity-axis validation across package declarations, registry,
  compatibility profile, schemas, migrations, fixtures, manifest, and receipt.

### Preservation

Envelope protocol `1.0`, compatibility profile `1.0`, Visual Asset Demand
message `1.1`, schema IDs, migrations, semantic fields, authority, lifecycle,
idempotency, replay, cancellation, amendment, supersession, replacement, and
Delegation Set behavior remain unchanged.

## 1.1.0-rc.2 - 2026-07-14

Status: consumer-conformance correction candidate, unsigned and not
production-authorized. Replaces consumer-rejected `1.1.0-rc.1` without
overwriting it.

### Corrected

- Added mandatory typed `source_provenance.source_kind` with the governed
  source-kind enum.
- `interview_expression` now conditionally requires non-empty Reaction Receipt
  and Expression Moment reference collections. Other source kinds may omit
  those collections, but supplied collections remain non-empty and fully typed.
- Added deterministic pre-discriminator V1.1 migration behavior. Unproven source
  class returns `SOURCE_KIND_CLASSIFICATION_REQUIRED`; interview provenance is
  never inferred or manufactured.
- Added source-provenance preservation to behavioral compatibility and adapter
  losslessness checks. Parse-only support remains incompatible.
- Rebased registry, fixture, validator, and protocol lookups to the clean
  release root instead of a source-checkout `packages/...` tree.
- Split the source-only manifest from the canonical release manifest. The
  canonical release manifest is generated from actual staged release contents.
- Excluded and actively rejected pytest caches, Python bytecode, temporary
  files, editor swaps, and operating-system metadata.
- Added clean-room release-only execution of schemas, examples, generated
  types, fixtures, migrations, compatibility, validators, protocol tests,
  release manifest, and receipt.

### Preservation

Envelope protocol `1.0`, Visual Asset Demand message `1.1`, lifecycle,
authority, integrity, replay, idempotency, amendment, cancellation,
supersession, replacement, and Delegation Set semantics remain unchanged.

## 1.1.0-rc.1 - 2026-07-14

Status: constitutionally aligned local release candidate, unsigned and not
production-authorized.

### Added

- Constitution-complete Visual Asset Demand `1.1` with exact Activative
  Intelligence Pack, Coach/Guest Identity DNA, Context Premise, Resonance,
  Matrix of Edging, Activative Call, Reaction Receipt, and Expression Moment
  lineage references.
- Closed Activation Contract, Visual Semantic Pack, Visual Narrative Program,
  Feature Contracts, and somatic T/V route structures.
- Non-empty `wrong_reading_locks` and closed rejection of legacy aliases.
- Per-domain preservation, enforcement, evaluation, evaluator-profile, feature
  family, and evidence claims for compatibility negotiation.
- Explicit owner-evidenced, deterministic `visual-asset-demand@1.0` to `@1.1`
  migration with immutable source/target hashes and supersession identity.

### Compatibility

- The Delegation Envelope protocol remains `1.0`; only the Visual Asset Demand
  message advances to `1.1`.
- Parsing without enforcement is incompatible. Adapters that drop, weaken,
  synthesize, flatten, or reinterpret mandatory meaning are rejected.
- Existing lifecycle, idempotency, replay, cancellation, amendment,
  supersession, replacement, and Delegation Set decisions are unchanged.

### Publication Gate

This release candidate remains unsigned and unpublished. External owner
ratification, trust-root/key lifecycle, consumer integration, and publication
infrastructure blockers remain open; no production authorization is claimed.

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
