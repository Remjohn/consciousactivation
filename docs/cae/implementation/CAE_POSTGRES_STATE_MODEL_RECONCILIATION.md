# CAE PostgreSQL/Supabase State Model Reconciliation

**Work package:** WP-02 — PostgreSQL State Model Reconciliation  
**Status:** `MODEL_DRAFT_PENDING_OPERATOR_REVIEW`  
**Date:** 2026-08-23  
**Decision:** PostgreSQL/Supabase is the target authoritative durable operational-state store for CAE. This document does not claim that cutover, provisioning, or data migration has occurred.

## Objective and scope

Engineer the canonical relational model, state-transition contracts, storage boundary, and phased migration plan before changing service authority. This package reconciles existing SQLite implementations with the target design; it does not copy their tables into PostgreSQL.

| Field | Definition |
|---|---|
| Allowed changes | Governance records and the reviewed PostgreSQL foundation DDL draft under `docs/cae/implementation/sql/`. |
| Prohibited changes | Service runtime behavior, local SQLite data, registry contents, deployed Supabase configuration, secrets, and production cutover. |
| Dependencies | WP-00 and WP-01, existing local migrations, Builder ADR-003, Phase 0–7 target contracts. |
| State transition | `OPERATOR_REVIEW -> MODEL` for this design; no `MODEL -> IMPLEMENT` promotion is implied. |
| Next bounded packages | WP-02a provisioning foundation; WP-02b first vertical-slice migration; WP-03 typed semantic operations. |
| Rollback | No database is changed. Revert the draft documents only. |

## Authority and storage boundary

PostgreSQL/Supabase is authoritative for operational facts, relationships, transitions, registries, commands, events, receipts, projections, permissions, and artifact metadata.

Raw media remains in an object store: Supabase Storage or a compatible S3 implementation. Its authoritative relational record is a `media_asset` row that carries the provider, bucket, immutable object key, SHA-256, byte size, media type, lineage, lifecycle state, and access policy.

Do **not** persist expiring signed URLs as identity. The stable automation-facing URL is application-owned (for example, `/media/{asset_id}`); it resolves to a time-bounded signed storage URL when access is allowed. The durable storage identity is `storage://{provider}/{bucket}/{object_key}` plus the content hash. This keeps URLs useful for automations without treating a secret-bearing or expiring URL as the source of truth.

Large bytes, derivative files, and immutable artifacts are not duplicated in Postgres rows. PostgreSQL stores their verified identity and lineage. This follows Builder ADR-003 while supporting Supabase Storage as the first object-store adapter.

## Canonical relational model

The model deliberately uses a shared relational spine **and** typed domain tables. `jsonb` is allowed for versioned contract payloads and auxiliary evidence, but it must not replace identity, joins, state, permissions, versioning, lineage, or query-critical fields.

| Domain | Canonical tables | Principal relationships and integrity rules |
|---|---|---|
| Tenancy and authorization | `workspace`, `project`, `actor` | Every operational record belongs to a workspace; project membership and RLS are enforced before normal reads/writes. |
| Media / artifacts | `media_asset`, later `artifact_derivative` | An asset points to one immutable storage object/key and SHA-256. A verified asset cannot be rewritten in place; a new asset/derivative must be created. |
| Interview source | `interview_session`, `interview_turn`, `source_package` | Sessions own ordered turns; source packages identify the verified media/transcript inputs that produced evidence. |
| Evidence | `evidence_item`, `evidence_span`, `evidence_authentication` | Each span anchors to an immutable source/package; authentication is an independently attributable decision, not a Boolean set by the writer. |
| AIR semantic assessment | `semantic_assessment`, `assessment_evidence_link` | An assessment has a typed kind, lifecycle/epistemic state, validator version, evidence links, and receipt. It does not silently make the source evidence canonical. |
| Registries | `registry_snapshot`, `registry_item`, `registry_crosswalk` | Original ID, version, source hash, source URI, rationale, and mapping lineage are preserved. SDA directs semantic geometry; SFL only modulates delivery and cannot replace Primitive Registry authority. |
| State control | `state_aggregate`, `state_transition_contract`, `state_transition` | A state projection has an optimistic version. Only a registered contract may change it, and every accepted transition creates an event and receipt. |
| Commands and proof | `semantic_operation`, `command`, `event`, `receipt`, `outbox` | Idempotency is scoped to semantic operation/workspace/key. Events and receipts are append-only. A receipt references its command and evidence, and cannot be sole proof of itself. |

## First vertical slice: object and transition contracts

The first slice is deliberately narrow: **source interview media/transcript -> evidence span -> authenticated evidence -> AIR semantic eligibility assessment -> receipt**. It proves relational identity, object storage linkage, evidence lineage, optimistic concurrency, independent authentication, and operator review without claiming the complete CAE runtime.

| Contract ID | Aggregate / transition | Required preconditions | Authoritative effects | Required independent evidence / receipt | Failure route |
|---|---|---|---|---|---|
| STC-MEDIA-001 | `media_asset: STAGED -> VERIFIED` | staged object exists; provider HEAD metadata matches declared key, byte size, content type, and SHA-256 | media asset becomes readable as a source candidate; verification event is appended | object-store verification result, hash, verifier identity, receipt | `QUARANTINED`; retain failure diagnostics and never overwrite bytes |
| STC-EVID-001 | `evidence_item: CAPTURED -> AUTHENTICATED` | one or more valid spans; parent media/source package is verified; provenance and capture actor supplied | evidence becomes eligible for semantic assessment | authentication decision by a designated evaluator, source-span refs, command/event/receipt | `REJECTED` or `NEEDS_REPAIR`, with reason and no semantic promotion |
| STC-AIR-001 | `semantic_assessment: PROPOSED -> VALIDATED` | assessment schema validates; evidence links are authenticated; validator/version and registry references are resolvable | semantic assessment may be presented for operator review | AIR validator result, linked evidence IDs, registry snapshot IDs, validation receipt | `REJECTED` / `SUPERSEDED`; a new assessment revision is required |
| STC-AIR-002 | `semantic_assessment: VALIDATED -> OPERATOR_CONFIRMED` | STC-AIR-001 succeeded; consequential operator decision is supplied | assessment can feed a later CAE semantic operation, within its policy | operator identity/decision, reviewed evidence set, transition receipt | `REJECTED` / `SUPERSEDED`; no automatic promotion |

The local AIR epistemic transition rules and Pipeline/Campaign transition implementations are evidence inputs for these contracts, not automatic adoption. Exact enum values and operation names will be frozen in WP-03 typed semantic-operation contracts.

## Transition-control invariants

1. One current projection per aggregate, guarded by `expected_version`; a stale writer receives a version-conflict result and creates no transition.
2. A normal application write enters through a typed semantic operation and a command with a scoped idempotency key. Direct domain-table writes are prohibited for application roles.
3. Every transition records source state, target state, contract version, actor, correlation/causation, command, evidence links, event, and receipt in one database transaction.
4. Events and receipts are immutable append-only records. A self-attested receipt is not independent evidence; its evidence links must identify a source or evaluator outside the action being asserted.
5. Typed tables own query-critical fields. Payload hashes and contract versions make revisioned payloads reproducible without using JSON as the relational model.
6. StateM concepts may inform contracts, recovery, and checks; no StateM source/runtime is adopted.
7. RLS must use workspace/project membership and service-role separation. Public object storage is prohibited for non-public media.

## Source-to-target reconciliation

| Existing source | Current evidence | Target disposition |
|---|---|---|
| `packages/ca_runtime` commands/events/receipts | local SQLite foundation with idempotency and aggregate sequencing | Preserve concepts; replace isolated stores with canonical Postgres command/event/receipt contracts after parity proof. |
| AIR `air_objects`, `air_object_edges`, primitive/archetype snapshots | revisioned semantic objects and local registries | Map eligible AIR semantic records to typed semantic assessments and registry tables; retain immutable legacy provenance; do not bulk-copy unreviewed JSON. |
| Interview `ie_objects`, `ie_events`, session snapshots | local source/evidence/session behavior | First-slice source. Extract verified media, source packages, sessions/turns, spans, and provenance into typed tables. |
| Pipeline runs/nodes/events/checkpoints | mature local execution state | Defer migration until the first evidence slice proves foundation semantics. Map later to state aggregates, transitions, workflow/run projections, and events. |
| Campaign state | local campaign state machine | Defer. Preserve current state behavior until a campaign-specific transition contract and Pipeline linkage are reconciled. |
| VAE objects/jobs/outbox | local artifacts and job-state system | Defer. Adopt object storage metadata/outbox concepts later; do not migrate job leases as canonical CAE state without a dedicated contract. |
| SDA/SFL ZIPs and AIR primitive snapshot | inherited registry inputs, including unresolved SFL family references | Do not migrate in WP-02. WP-04 imports only hash-validated, reference-valid records with original IDs/version/lineage and explicit crosswalks. |

## Executable foundation artifact

[0001_cae_foundation_draft.sql](D:\Work\consciousactivation\docs\cae\implementation\sql\0001_cae_foundation_draft.sql) is the reviewed foundation DDL for a clean PostgreSQL/Supabase project. It creates the shared relational spine and typed first-slice tables. WP-02a applied it once to the disposable staging project through the guarded migration runner, then applied RLS scaffolding and verified private Storage behavior. Its checksum and proof are recorded in [the WP-02a foundation proof](D:\Work\consciousactivation\docs\cae\implementation\CAE_WP02A_FOUNDATION_PROOF.md). It is not a production deployment or a legacy-data migration.

The [phased migration execution plan](D:\Work\consciousactivation\docs\cae\implementation\CAE_POSTGRES_MIGRATION_EXECUTION_PLAN.md) defines the exact import and cutover boundaries, ledger requirements, reconciliation gates, rollback behavior, and future implementation artifacts. The staging proof used a real PostgreSQL client and environment; production and legacy-data proof remain deferred.

## Required proof before cutover

| Test class | Required proof | Anti-reward-hack countertest |
|---|---|---|
| Structural | constraints reject orphan spans, duplicate immutable keys, invalid state pairs, and duplicate scoped idempotency keys | Direct insert attempt that bypasses a required foreign key/constraint must fail. |
| Behavioral | each STC transition accepts only valid preconditions and increments exactly one aggregate version | stale expected version must fail without a new event or receipt. |
| Integration | one real object-store upload is hash-verified, indexed, then cited by an authenticated evidence item and AIR assessment | object key exists but bytes/hash differ; transition must quarantine/reject. |
| Environment fidelity | run against disposable Supabase/Postgres and real object-store adapter, not SQLite/mocks | a mock verification response alone must not satisfy STC-MEDIA-001. |
| Reality-contact | retrieve the stored object through the application URL under authorized and denied identities | a public URL or expired signed URL must not be treated as a durable identity or authorization proof. |
| Anti-reward-hack | cross-check receipt evidence against independently persisted source/evaluator rows | self-attested receipt with no independent evidence link must fail promotion. |

## Operator gate

### A. What changed

WP-02 now defines a Postgres/Supabase target authority, object-storage boundary, typed relational first slice, four transition contracts, source dispositions, and a reviewed DDL draft.

### B. Why it changed

The repository has several locally coherent SQLite models but no shared relation/state authority. A direct database copy would reproduce those seams rather than establish canonical CAE relationships.

### C. What was proven

The source migrations demonstrate repeated local implementations of revisions, idempotency, events, receipts, and transitions. Builder ADR-003 independently supports PostgreSQL plus content-addressed object storage.

### D. What was not proven

No legacy data is migrated, no existing service is redirected, no production environment is provisioned, and no end-to-end first semantic-operation slice is proven. The staging DDL, private buckets, RLS allow/deny behavior, and private-object upload/hash/denied-read behavior are proven separately in WP-02a.

### E–F. Remaining uncertainty and what could still be wrong

Legacy record quality, true production data volumes, authentication topology, retention rules, data residency, and the final Supabase-versus-external-S3 operating choice remain unknown. Some service-specific fields may require additions after a controlled data-profile inventory.

### G. Operator inspection

Inspect the media identity rule, typed first-slice entities, transition contracts, legacy-source dispositions, and the DDL draft before anything is provisioned.

### H. Exact decision required

**Promote WP-02 and authorize WP-02a to provision a disposable Supabase/Postgres plus private object-storage foundation, apply the reviewed draft migration, and run only structural/environment-fidelity proof—without importing legacy data or redirecting production writes?**
