---
title: TS-DLG-02 Authority Policy and Principal Identity
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-02 Authority Policy and Principal Identity

## 1. Identity and requirement coverage

- Primary features: F02 and the identity/authorization portion of F14
- Owned FRs: FR-009 through FR-016, FR-105, FR-106, FR-110, FR-111
- Owned NFRs: NFR-AUTH-001 through NFR-AUTH-005, NFR-SEC-001, NFR-SEC-004, NFR-GOV-002
- Decisions: D002, D014
- Resolves: ADR-DLG-003 signature preimage, ADR-DLG-004, ADR-DLG-017
- Journeys: UJ-01, UJ-04, UJ-05, UJ-06, UJ-07, UJ-08, UJ-12, UJ-13
- Supporting specs: TS-DLG-01 registry, TS-DLG-03 replay/lifecycle, TS-DLG-05 commands, TS-DLG-06 result authorities

## 2. Sources read

Normative inputs are `prd/05-features/F02-demand-ownership.md`, `prd/05-features/F14-trust-integrity.md`, `governance/AUTHORITY_MATRIX.yaml`, `governance/PRINCIPAL_AUTHORITY_REGISTRY.yaml`, `governance/PROTOCOL_CONSTITUTION.yaml`, the architecture preservation contract, all authority cases, the envelope/demand/result schemas, the Stage 1 ownership register and XRI-003 through XRI-005, XRI-008, XRI-010 and XRI-015.

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

Domain-level authority is documented, but public schemas contain open fields and two concrete ownership contradictions. The solution is a deterministic policy model that validates an authenticated principal, registered action and field-level authority before any lifecycle or persistence effect.

Authority validation answers whether a named principal may assert the exact fields and action in this message. It does not decide whether the creative intent is good, whether a production plan is effective or whether a visual candidate passes quality evaluation.

## 4. Principal and trust architecture

Every state-changing sender is a registered workload principal with:

- immutable `principal_id` URI: `cmf-principal://<tenant>/<principal-type>/<instance-id>`;
- `principal_type`: `content_harness`, `visual_asset_editor`, `composition_runtime`, `delegation_boundary_service`, `operator_policy` or `authorized_migration_service`;
- owning product and release identity;
- active public verification keys and historical key records;
- allowed message actions, authority scopes, environment and tenant;
- issuance, activation, expiry, revocation and compromise status.

Human operators act through an `operator_policy` workload principal carrying a short-lived authorization grant; personal identity remains in the audit evidence and is not copied into every domain payload. Transport identities authenticate channels but cannot substitute for the signed workload principal.

The required Release 1 signature suite is Ed25519 over SHA-512 as defined by Ed25519. `key_id` is a stable URI resolving to a versioned public key record. Algorithm agility is registry-controlled; an unnegotiated algorithm is rejected. Private keys remain in product-controlled KMS/HSM boundaries and are never held by the Delegation Protocol.

## 5. Signature and identity rules

The signature preimage is RFC 8785 canonical JSON of the complete envelope with `integrity.signature` omitted and with `payload_hash` present. The payload itself is not duplicated in the preimage; its verified hash binds it. The integrity object shall contain `signature_algorithm`, `key_id`, `signer_principal`, `signature`, `issued_at`, optional `expires_at` and `nonce`.

Validation requires:

1. signer principal equals `sender.principal_id`;
2. key belongs to that principal and was active at `issued_at`;
3. message time is within the negotiated clock-skew window, default plus or minus 120 seconds;
4. expiry has not passed;
5. signature verifies over canonical bytes;
6. principal and key are not revoked for the applicable time/policy;
7. historical verification can resolve the exact key version after rotation.

Revocation effective times are explicit. A compromise revocation may invalidate earlier messages only through a governed security impact notice; it never silently rewrites historical audit facts.

## 6. Field-level authority model

The canonical policy input is `(principal, action, message_type, message_version, field_paths, referenced_owner_facts, current_state, negotiated_profile)`. Output is `ALLOW` or `DENY` plus stable reason, matched policy version and field decisions. There is no model or heuristic fallback.

| Authority | May author | May not author |
|---|---|---|
| Content Harness | Demand identity/meaning, semantic and Activative intent, sequence/asset role, composition intent, identity/continuity, wrong-reading locks, delivery, budget authorization, cancellation, supersession, amendment response, acknowledgement, owned dependency invalidation | Production acceptance, VAE plans/workflows/evaluations/receipts |
| Visual Asset Editor | Admission fact, progress facts, feasibility/conflict evidence, amendment proposal, budget request, production failure, accepted assets, production acceptance/receipts, selective-invalidation evidence, cancellation disposition, production revocation | Demand mutation, downstream consumption acknowledgement, sequence-role changes |
| Composition runtime | Result acknowledgement and consumption record only when delegated by the owning harness and scoped to the exact composition/demand | Demand creation, production acceptance, budget or cancellation policy |
| Delegation boundary service | Validation results, negotiated profile, lifecycle projection, audit receipt, deterministic routing and derived consumption block | Demand meaning, production facts, creative choices or visual ranking |
| Operator policy | Explicit budget/degradation/cancellation/human-exception decisions within a versioned grant | Constitutional bypass or unscoped creative/production mutation |
| Migration service | Representational target artifact and transformation evidence under an approved migration | Semantic or authority changes |

The Stage 1 field register is the seed. Stage 3 schemas must carry machine-readable `x-cmf-value-owner` metadata for every closed field. A wildcard or unregistered field fails the ownership gate.

Free-form demand notes are `non_authoritative_enrichment`. They are preserved with provenance, excluded from hash-independent interpretation and cannot override a typed field. If a note conflicts with a typed field, the typed field wins and a warning receipt may be emitted without changing meaning.

## 7. Resolution of provisional ownership contradictions

### Submission admission

The current conditional `submission-receipt` is replaced in the next major contract family by two single-purpose facts:

- `submission-validation-receipt`, authored by the Delegation Protocol, records contract, identity, integrity, authority, compatibility and idempotency validation and causes `DRAFT -> SUBMITTED` or `DRAFT/SUBMITTED -> REJECTED`.
- `admission-receipt`, authored by the VAE, records VAE admission with `execution_id`, accepted exact demand identity and accepted/rejected reason; accepted causes `SUBMITTED -> ACCEPTED`. A VAE admission rejection uses a typed capability/admission failure and does not let the protocol impersonate VAE authority.

The existing `submission-receipt` becomes read-only compatibility input and must be migrated or adapted losslessly. This resolves XRI-003 and ADR-DLG-004 without blending principals.

### Result consumption authorization

`asset-result-contract.authorization.downstream_consumption_authorized` is removed in the next major result schema. The VAE may assert only production acceptance. Downstream authorization is established solely by an accepted `result-acknowledgement` from the owning Content Harness or delegated composition runtime. This resolves XRI-004; detailed behavior belongs to TS-DLG-06.

### Demand evaluation policy

The Content Harness may specify certified evaluation profile references, mandatory owner gates and a maximum repair budget. It may not specify evaluator models, VLM prompts, candidate ranking, workflow nodes or repair strategy. Those remain VAE production fields. An unsupported required profile yields compatibility failure or amendment proposal, not reinterpretation.

## 8. Lifecycle, messages and event routing

Authority is checked before lifecycle transition validation. A valid identity with an unauthorized action is rejected as `authority_failure`; it is never treated as an illegal lifecycle transition. Every denial emits an audit receipt with principal, action, denied paths and policy version while minimizing sensitive claims.

Correlation and causation follow TS-DLG-01. Delegated composition-runtime acknowledgement includes the owner grant reference as a signed immutable resource. Admission, cancellation, supersession, amendment, result and post-completion facts route only after authority acceptance and through the transactional outbox.

An authority policy update applies to new messages, not retroactively to already accepted facts, unless a separate invalidation/revocation process is authorized. Running correlations pin the policy major/minor version used at admission; critical principal revocation is evaluated at every message.

## 9. Cross-cutting protocol behavior

- Idempotency: the same authorized principal, action, payload hash and idempotency key may return the original receipt; a different principal or payload is a conflict.
- Replay: a valid old signature or nonce outside policy is rejected before authority effects under TS-DLG-03.
- Compatibility: principal types, authority model and required scopes are negotiated dimensions; adapters may rename representational fields but cannot change owners.
- Cancellation/races: only an authorized harness/operator command enters precedence ordering; unauthorized commands have no ordering effect.
- Supersession: only the demand owner may change demand fields; changed JSON Pointers are checked individually.
- Result acknowledgement: only the owner or an exact delegated composition runtime may authorize consumption.
- Invalidation/revocation/replacement: the sender must own the triggering dependency, production defect or integrity authority specified by the notice reason.

## 10. Persistence and transaction boundaries

Principal/key records and policy bundles are versioned immutable resources. Acceptance stores their exact IDs/hashes in the audit receipt. Key status lookup may be external, but the verification decision and evidence are persisted atomically with message acceptance/rejection.

No lifecycle mutation, outbox event or idempotency success record may commit unless identity, signature and authority results are durable. Policy caches fail closed on unknown or stale critical revocation state. Read-only historical verification may use archived public keys but never re-enable a revoked active principal.

## 11. Failure, retry and recovery

Stable failures include `IDENTITY_UNVERIFIED`, `SIGNATURE_INVALID`, `MESSAGE_EXPIRED`, `UNAUTHORIZED_DEMAND_MUTATION`, `INVALID_AMENDMENT_AUTHOR`, `UNAUTHORIZED_CANCELLATION`, `UNAUTHORIZED_BUDGET_PROGRAM` and `UNAUTHORIZED_DEGRADED_ACCEPTANCE`. They do not consume VAE quality rounds.

Identity/signature failures are not ordinary retryable. A new credential or corrected authorization creates a new message. Temporary key-registry unavailability is an infrastructure failure; the original message may be redelivered unchanged after recovery and resolved idempotently.

## 12. Threat model and data minimization

Threats include principal spoofing, confused deputy, stolen/rotated keys, forged delegation grants, policy downgrade, cross-tenant access, authority claims hidden in extensions and log leakage. Controls are signed workload identity, exact recipient/tenant binding, field-policy evaluation, pinned policy versions, revocation checks, extension closure, least-privilege grants and audit evidence.

Payloads include principal IDs and grant references, not bearer tokens, private keys or unnecessary human details. Diagnostics containing sensitive identity-provider data remain behind access-controlled references.

## 13. Observability and SLOs

Metrics include identity lookup/verification latency, signature failures, authority denials by stable code, denied field counts, key-rotation age, revocation propagation and policy-cache freshness. Alerts fire on any accepted unauthorized mutation, signature bypass, repeated cross-tenant attempts or revocation propagation above the critical-notice SLO.

Targets are zero unauthorized state mutations, 100% state-changing signature verification and 100% audit coverage. Cardinality is controlled by excluding raw principal IDs from metric labels while retaining them in secured audit records.

## 14. Compatibility, migration and rollback

Authority-model versions are required compatibility dimensions. An adapter cannot convert a VAE principal into a Content Harness principal or drop an owner field. Principal-type or action changes are major. Key rotation is compatible when historical verification remains available.

Migration of the old `submission-receipt` produces immutable protocol-validation and VAE-admission facts only when source evidence proves both authorities; otherwise the source remains read-only and cannot certify admission. Migration of the old result drops no production fact but moves downstream authorization to an explicit acknowledgement. Rollback retains new facts and routes new correlations to the prior policy bundle only if it still recognizes them safely.

## 15. Test architecture

- Policy-table unit tests cover every principal/action/field combination and every prohibited action.
- Signature vectors cover canonical bytes, key rotation, expiry, skew, revocation and historical verification.
- Authority conformance executes all existing cases plus every open field path and extension route.
- Cross-tenant, forged grant, algorithm downgrade and confused-deputy adversarial tests are mandatory.
- Admission split and result-authority migration fixtures prove no conditional owner remains.
- Product contract tests verify Content Harness and VAE adapters cannot emit each other's authority facts.

## 16. Given/When/Then acceptance criteria

1. Given a VAE principal that submits a changed demand field, when authority is checked, then `UNAUTHORIZED_DEMAND_MUTATION` is receipted and state is unchanged.
2. Given an authorized Content Harness and an immutable demand, when submitted, then every demand field maps to exactly one owner and the accepted policy version is audited.
3. Given a VAE production result, when validated, then production acceptance is allowed and downstream consumption authorization in that payload is rejected.
4. Given a delegated composition runtime with an exact unexpired owner grant, when it acknowledges the referenced result, then the action is allowed; an unscoped result is denied.
5. Given a rotated signing key, when an old accepted message is audited, then its historical signature remains verifiable without reactivating the old key.
6. Given an unsupported evaluation profile, when admission occurs, then the VAE emits incompatibility or amendment evidence and does not rewrite evaluation requirements.
7. Given an unknown authority-bearing extension, when parsed, then acceptance fails before lifecycle mutation.

## 17. Implementation tasks

1. Generate field authority metadata from closed schemas and ownership register.
2. Define principal, key record, policy bundle and delegation-grant schemas.
3. Define Ed25519 canonical signing vectors shared by all product languages.
4. Split submission validation and VAE admission contracts.
5. Revise result authority for the next major schema.
6. Implement a deterministic policy decision interface and exhaustive conformance vectors.
7. Integrate external identity/key providers through ports without selecting a vendor in the core library.
8. Obtain cross-repository principal and adapter evidence for XRI-002 and XRI-015.

## 18. Explicit non-goals

- Human identity-provider UI or credential provisioning product
- Storage of private signing keys in the protocol
- Creative, semantic or production-quality decisions
- Internal VAE worker authorization beyond the shared boundary
- Automatic constitutional amendments
- Production implementation during Stage 2

## 19. Readiness and blockers

Specification verdict: `CONCERNS`. The ownership contradictions have a normative resolution, but contract freeze requires upstream acceptance, closed schemas, real principal infrastructure and cross-product signature vectors. This spec does not authorize implementation.

## 20. V1.1 constitutional alignment amendment

Content Harness owns every value under `activative_semantic_lineage`,
`activation_contract`, `visual_semantic_pack`, `visual_narrative_program`,
`feature_contracts`, `somatic_route_request`, `activative_function`, and
`wrong_reading_locks`. Reaction Receipt and Expression Moment references are
nested under semantic lineage and retain source authority. The protocol may
validate, hash, negotiate support, and reject; it may not select or rewrite
meaning. VAE mutation of recognition intent, viewer role, stance, or narrative
program is `AUTHORITY_DENIED` with no state or production effect and a rejection
audit receipt. Traceability: `AUTH-CONSTITUTION-001`.
