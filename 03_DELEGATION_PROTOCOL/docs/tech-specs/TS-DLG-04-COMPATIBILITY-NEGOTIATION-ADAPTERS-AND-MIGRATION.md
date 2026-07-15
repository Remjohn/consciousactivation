---
title: TS-DLG-04 Compatibility Negotiation Adapters and Migration
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-04 Compatibility Negotiation, Adapters and Migration

## 1. Identity and requirement coverage

- Primary feature: F11
- Owned FRs: FR-081 through FR-088
- Owned NFRs: NFR-COMPAT-001 through NFR-COMPAT-005, NFR-CONTRACT-005
- Decision: D011
- Resolves: ADR-DLG-010 and compatibility/publication portions of ADR-DLG-020
- Journeys: UJ-02, UJ-11, UJ-13, UJ-14

## 2. Sources read

Normative inputs are `prd/05-features/F11-compatibility-migration.md`, `governance/COMPATIBILITY_POLICY.yaml`, `contracts/PROTOCOL_VERSION_POLICY.md`, compatibility-manifest and contract-migration schemas/examples, compatibility cases, Format 02 manifests/profile, TS-DLG-01 through TS-DLG-03 and XRI-007, XRI-008, XRI-012 and XRI-013.

## 2A. Cross-cutting protocol obligations

| Concern | Normative obligation in this specification |
|---|---|
| Service and library boundaries | Only the modules and ports named here are owned; Content Harness meaning, VAE production and the existing Control Tower remain external owners. |
| Canonical schemas and field-level authority | Public payloads are closed, versioned and registry-owned; every value path has one owner and every state-changing principal/action is validated before effect. |
| Lifecycle, correlation and causation | TS-DLG-03 transition rules apply; every message keeps the exact correlation and names its direct accepted cause unless it is the initial command. |
| Idempotency versus replay | Legitimate identical command delivery returns the prior receipt; nonce/message/key reuse with different bytes, scope or invalid state is rejected as replay/conflict. |
| Compatibility, adapters and migrations | TS-DLG-04 negotiation is pinned before admission; adapters/migrations are deterministic, lossless for mandatory meaning and cannot transfer authority. |
| Event routing and audit chain | Accepted/rejected actions are receipted; accepted messages route only after atomic message/state/audit/outbox commit. |
| Cancellation and race precedence | TS-DLG-03/05 committed-sequence rules apply; accepted cancellation or supersession blocks later stale promotion for its scope. |
| Supersession and selective invalidation | Old facts remain immutable; owner-authored changed paths and VAE evidence determine conservative reuse and exact invalidation. |
| Result acknowledgement | VAE production acceptance remains separate from Content Harness/composition-runtime downstream acknowledgement under TS-DLG-06. |
| Invalidation, revocation and replacement | Post-completion authorization changes use new notices and impact analysis; no completed result or historical use is overwritten. |
| Failure, persistence and transactions | Failures use the canonical taxonomy; state-changing acceptance fails closed unless durable protocol records and audit commit atomically. |
| Observability and SLOs | TS-DLG-08 source-linked projections, bounded metrics, incident rules and SLO definitions apply to all behavior specified here. |
| Threat model and test architecture | The threat and test sections below include negative, adversarial, recovery and Given/When/Then evidence for this spec's owned behavior. |

## 3. Problem, solution and scope

The package defines compatibility verdicts and sample manifests but has no signed release binding, deterministic negotiation algorithm, adapter registry or executable semantic-equivalence proof. This specification defines those artifacts without permitting best-effort parsing or authority transfer.

Compatibility means preservation of required semantics, field authority, lifecycle effects, failure behavior, profile capabilities, quality gates and receipts. JSON parseability alone is irrelevant.

## 4. Service and library boundaries

Required modules are `manifest-validator`, `profile-negotiator`, `adapter-registry`, `adapter-runner`, `migration-runner`, `equivalence-verifier` and `deprecation-policy`. Core functions are pure over signed manifests and registry snapshots; artifact fetching and publication use ports.

Each product publishes its own capabilities. The protocol validates and intersects them. It does not advertise unsupported product capabilities, reinterpret requirements or choose a creative degradation.

## 5. Canonical compatibility manifest

Each released Content Harness, VAE and protocol package publishes a signed closed manifest containing:

- product type, product/release ID, build digest and principal ID;
- accepted/emitted protocol and message versions with schema IDs/hashes;
- authority-model and lifecycle-machine versions;
- required/optional feature tokens;
- supported asset families, category/format/geometry profiles and Budget Programs;
- required evaluation and receipt capabilities;
- certified profile/version tuples and evidence references;
- adapter IDs/versions that the release can invoke;
- unsupported required capabilities and known limitations;
- active/discouraged/deprecated/read-only/retired states and dates;
- signature metadata and immutable canonical reference.

The manifest is itself signed under TS-DLG-02. A product cannot claim another product's capabilities. The protocol release manifest identifies the canonical contract package and conformance-suite digest.

## 6. Deterministic negotiation algorithm

Inputs are the exact Content Harness, VAE and protocol manifests plus requested demand profile. Negotiation uses this order:

1. Validate manifest schemas, hashes, signatures, release identities and non-expiry.
2. Intersect protocol major/minor versions and select the highest protocol-preferred mutually accepted version.
3. For every message required by the requested journeys, select a directly compatible producer-emitted/consumer-accepted version or an approved adapter path.
4. Require exact authority-model, lifecycle semantics and failure-taxonomy compatibility.
5. Verify every required feature token, asset family, category/format/geometry profile, Budget Program, evaluation receipt and post-completion behavior.
6. Reject any path that drops or weakens semantic, Activative, continuity, composition, wrong-reading, quality or authority fields.
7. Select at most one deterministic adapter path per message direction; cycles and ambiguous equal-precedence paths are invalid.
8. Produce and sign an immutable `NegotiatedDelegationProfile` pinned to the correlation.

Selection is deterministic using protocol preference order, then highest compatible minor, then lowest adapter count, then lexicographic adapter ID as a final stable tie-breaker. Product cost or convenience cannot override required behavior.

## 7. Verdicts and degradation

The output is exactly one of:

- `COMPATIBLE`: direct support for every mandatory behavior;
- `COMPATIBLE_WITH_ADAPTER`: approved lossless deterministic representation change;
- `COMPATIBLE_WITH_DECLARED_DEGRADATION`: only optional behavior is omitted and its owner signs the omission;
- `MIGRATION_REQUIRED`: a new immutable representation must be created before admission;
- `INCOMPATIBLE`: at least one mandatory semantic/authority/lifecycle/profile/evaluation/failure behavior cannot be preserved.

Each verdict lists dimensions, selected versions, adapters/migrations, evidence and stable reasons. Declared degradation cannot affect mandatory demand fields, constitutional gates, required roles, security, audit, production acceptance or downstream acknowledgement.

## 8. Adapter model

An adapter registry entry declares source/target schema IDs and hashes, adapter package digest, owner, deterministic transformation ID, field mapping, preserved required features, prohibited losses, fixtures and conformance evidence.

Adapters are pure functions of source payload and pinned configuration. They have no network, clock, random, model or mutable-state dependency. Output is canonicalized and hashed. The runner emits an `AdapterReceipt` linking source, output, adapter version and field-level preservation result.

Adapters may rename, wrap, split or combine representational fields only where semantic equivalence is proven. They cannot invent missing owner facts, choose amendment options, downgrade quality gates, alter lifecycle intent, change principal authority or silently default mandatory values.

## 9. Immutable migration

Migration is used when direct/adapter representation is insufficient but an approved semantic-preserving transformation exists. It produces a new immutable target artifact and `contract-migration` receipt containing exact source/target identities, ordered transformations, authority-effect analysis, source/target validation, equivalence result and output reference/hash.

The migration service authors only the transformation artifact. Original field owners retain semantic authority. Any transformation that needs an owner decision stops with `MIGRATION_REQUIRED` plus an amendment/owner action; it cannot make the decision itself.

Migration is idempotent by `(source_hash, target_schema_hash, migration_id/version, configuration_hash)`. Repeated identical execution returns the same output hash. Different output is a conformance failure and security incident.

## 10. Lifecycle and event routing

Negotiation occurs before `submission-validation-receipt.accepted`. The signed profile is stored with the correlation and referenced by every receipt. Running delegations never silently upgrade. An emitted message is validated against the pinned profile even if a newer compatible release exists.

Adapter/migration outputs use new message IDs, retain the original correlation and set causation to the source message or approved migration request. Both source and transformed facts remain auditable. Routing sends only the selected target representation to the consumer while preserving source history.

Cancellation, supersession, amendment, result acknowledgement and post-completion messages are included in required-message negotiation when their feature is in scope. Missing support for a required failure or governance path is `INCOMPATIBLE`, not a runtime surprise.

## 11. Authority, idempotency and replay

Manifests are authored by their product principal. Profiles and compatibility verdicts are authored by the protocol. Adapters/migrations cannot change value owners. Owner-authorized degradations carry a separate signed causally linked decision.

Manifest/profile IDs and hashes are immutable. Duplicate negotiation with identical inputs returns the same profile. Replayed expired manifests or altered artifacts fail signature/replay validation before use.

## 12. Persistence and transactions

Manifest, adapter and migration registries are immutable signed snapshots. Admission atomically records selected snapshot hashes and profile. Adapter execution records source/output/receipt as one unit before routing. A partial migration output is never visible as accepted.

Registry unavailability fails new negotiation closed but does not stop already pinned correlations whose required artifacts are locally verified and available. Revoked adapter/package digests block new use and trigger impact analysis for active correlations.

## 13. Failure, recovery and rollback

Failures map to `UNSUPPORTED_CONTRACT_VERSION`, `UNSUPPORTED_DEMAND_PROFILE`, `INCOMPATIBLE_RESULT_VERSION`, `UNSUPPORTED_ASSET_FAMILY`, `INCOMPATIBLE_GEOMETRY_PROFILE`, `CATEGORY_PROFILE_NOT_CERTIFIED`, invalid signature/hash or migration-equivalence failures.

No blind retry occurs. Temporary registry/object-store failures may retry unchanged. Semantic incompatibility requires a different release, approved migration or owner-authored amendment. Rollback selects a prior signed registry/package for new correlations; active profiles remain pinned unless a security revocation requires cancellation or governed migration.

## 14. Threat model

Threats include forged capability claims, downgrade, adapter substitution, lossy mapping, ambiguous path selection, migration non-determinism, stale certification and malicious declared degradation. Controls are signed manifests, digest pinning, deterministic selection, no ambiguous paths, field-level equivalence fixtures, owner signatures and conformance evidence.

Manifest evidence references are access-controlled and hash-verified. Private product configuration and internal workflows are not exposed as compatibility dimensions.

## 15. Observability and SLOs

Metrics include verdict counts/reasons, negotiation latency, adapter usage, deprecated profile use, manifest age, migration determinism, equivalence failures and active correlations by pinned profile. Alert on forged/expired manifests, adapter digest mismatch, deterministic-output mismatch or active use of a revoked artifact.

Compatibility truthfulness target is 100% of declared paths passing fixtures. Adapter usage is a counter-metric, not a success target; direct compatibility is preferred.

## 16. Test architecture

- Manifest schema/signature tests for every product type and release state.
- Pairwise and three-way negotiation matrices over versions, features, profiles and receipts.
- Golden adapter fixtures with field-by-field preservation and deterministic repeat runs.
- Migration fixtures with source/target validation and negative semantic-change cases.
- Downgrade, forged manifest, ambiguous path and revoked adapter adversarial tests.
- In-flight pinning/rollback tests and Format 02 cross-product compatibility tests.

## 17. Given/When/Then acceptance criteria

1. Given directly compatible signed manifests, when negotiated, then `COMPATIBLE` pins exact schema and policy hashes.
2. Given an approved lossless adapter, when direct versions differ, then `COMPATIBLE_WITH_ADAPTER` names one deterministic path and its evidence.
3. Given an adapter that drops a wrong-reading lock, when validated, then negotiation returns `INCOMPATIBLE`.
4. Given only an optional unsupported feature and an owner-signed omission, when negotiated, then declared degradation is allowed without changing mandatory behavior.
5. Given identical migration inputs, when executed repeatedly, then output hashes are identical.
6. Given a newer protocol release during an active delegation, when messages continue, then the pinned profile remains unchanged.
7. Given an expired or forged manifest, when negotiation starts, then no profile is created and a security receipt is emitted.

## 18. Implementation tasks

1. Close and sign compatibility-manifest and negotiated-profile schemas.
2. Define generated feature/profile/version vocabularies from the contract registry.
3. Implement the pure negotiation algorithm and complete decision vectors.
4. Define adapter registry/receipt and migration-equivalence schemas.
5. Produce at least one older/newer lossless adapter and migration fixture.
6. Add package digest, deprecation timeline and rollback metadata.
7. Obtain pinned product manifests and releases under XRI-012/XRI-013.

## 19. Explicit non-goals

- Semantic best-effort parsing or model-based translation
- Product release management beyond shared compatibility artifacts
- Silent in-flight upgrades
- Lossy authority or quality degradation
- Runtime implementation or Stage 3 publication during Stage 2

## 20. Readiness and blockers

Specification verdict: `CONCERNS`. The algorithm and evidence model are defined, but executable adapters/migrations and accessible signed product releases are required before compatibility can pass its readiness gate.

## 21. V1.1 constitutional alignment amendment

Compatibility requires explicit per-domain `PRESERVE` and `ENFORCE` support;
domains that affect activation/evaluation additionally require `EVALUATE` and
non-empty evaluator-profile evidence. Feature Contracts require supported
feature-family evidence. `PARSE` alone is incompatible. An adapter or migration
must reject `DROP`, `WEAKEN`, `SYNTHESIZE`, `FLATTEN`, or `REINTERPRET` effects
on mandatory meaning.

`visual-asset-demand@1.0` cannot be silently defaulted into `@1.1`. The approved
migration requires Content Harness-owned context for every new canonical
domain, losslessly renames only the three legacy aliases, creates a new
immutable demand version, pins the complete source identity in `supersedes`,
and emits source/target hashes plus authority-effect evidence. Traceability:
`COMPAT-CONSTITUTION-001`, `MIGRATION-CONSTITUTION-001`.

## 22. RC2 consumer-conformance correction

`source_provenance` is a required semantic domain with `PRESERVE` and `ENFORCE`
support. Parse-only support is incompatible. An adapter changing source kind or
Reaction Receipt/Expression Moment provenance is lossy. A pre-discriminator
V1.1 demand produces `SOURCE_KIND_CLASSIFICATION_REQUIRED` unless Content
Harness supplies an explicit governed classification. The migration never
defaults a source kind; interview classification without both provenance
collections produces `INTERVIEW_PROVENANCE_REQUIRED` and no target demand.

## 23. RC4 portable derivative-lock enforcement

A consumer claiming derivative asset flows must declare `PRESERVE` and
`ENFORCE` support with validator evidence. The portable
`derivative-lock-inheritance@1.0` relationship pins the authoritative parent,
parent contract version, parent lock evidence and hash, derivative lock set,
derivation type, semantic classification, and authoritative demand evidence.
`PARSE` alone is incompatible.

For deterministic non-semantic derivation, each parent lock ID, statement and
meaning hash must remain exact, each parent scope must remain a subset of the
derivative scope, and enforcement strength cannot decrease. A semantic or
transformative derivative requires an explicit authoritative applicable lock
set. Relaxation is valid only through a new immutable demand version that
supersedes the governing demand. Missing evidence and legacy classification are
typed failures; adapters and migrations cannot invent lock content.
