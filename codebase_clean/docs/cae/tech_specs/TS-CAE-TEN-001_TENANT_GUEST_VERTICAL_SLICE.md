# TS-CAE-TEN-001 — Tenant/Guest Vertical-Slice Implementation Technical Specification

**Document ID:** `TS-CAE-TEN-001`  
**Phase ID:** `CA-TS-01`  
**Status:** `READY_FOR_DEVELOPMENT` (Authorizing `CA-IMPL-01A` Staging Foundation Scaffolding Only)  
**Date:** 2026-08-25  
**Author:** CAE Governed Execution Agent (Gemini 3.7 Flash High / Antigravity)  
**Governing Mandates:** `09_CA_TS_01_IMPLEMENTATION_GATE_TECH_SPEC_MANDATE.md`, `00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md`  
**Authority References:** CAE Governance & Specification Bridge Bundle v3 (`02`, `03`, `04`, `08`, `09`, `10`, `14`, `15`, `16`, `17`, `21`); Ratified Constitutions `CA-CAN-01A`, `CA-CAN-01B`, `CA-CAN-01C`; `PRD-CAE-TEN-001`; Functional Requirements `FR-CAE-TEN-001` through `FR-CAE-TEN-015`; Migration Contracts `MC-CAE-WS-001` through `MC-CAE-REC-001`; `CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md`  

---

## 1. Files and Evidence Read

```text
1. ARCHITECTURE LOADED: Loaded CAE Phase 0–7 bundles; verified Canonical Plane vs. Operational Plane separation in CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md.
2. PHASE VALIDATION LOADED: Loaded WP-10A evidence containment report (CAE_WP10A_ACCEPTANCE_REPORT.md) and CA-MAP-01/AUTH-01/CAN-01A/B/C/SPEC-01/STATE-01 completion records.
3. OBJECT CONSTITUTION(S) LOADED: Loaded 15 ratified constitutions across CA-CAN-01A (OperatorOrg, Workspace, WorkspaceMembership, Engagement, OperatorAccessPolicy, OperatorAccessGrant), CA-CAN-01B (Guest, GuestIdentityLink, MediaAsset, ImmutableMediaEvidence, SourcePackage, EvidenceItem/Span), and CA-CAN-01C (HarnessTemplate, HarnessRun, Receipt, ReceiptEvidenceLink).
4. DEFINITION GRAMMAR LOADED: Loaded Conscious Activation Definition Grammar Bundle (04_STATE_DEFINITION_GRAMMAR.md) and Bundle v3 State & Transition Control Protocol (14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md).
5. PRD/FR LOADED: Loaded PRD-CAE-TEN-001 and FR-CAE-TEN-001 through FR-CAE-TEN-015; verified 100% requirement coverage in CAE_TENANT_GUEST_REQUIREMENT_TRACEABILITY_MATRIX.md.
6. BROWNFIELD CODE READ: Inspected api/main.py, api/domain/campaign.py, api/services/campaign_repository.py, packages/ca_runtime/src/ca_runtime/database.py, packages/ca_runtime/src/ca_runtime/semantic_operations.py, packages/ca_runtime/src/ca_runtime/interview_source_bridge.py, services/interview/src/**, and services/pipeline/src/**.
7. DATABASE/SCHEMA READ: Inspected staging DDLs 0001_cae_foundation_draft.sql, 0002_cae_workspace_rls.sql, 0003_wp03_evidence_first_slice.sql, 0004_wp04_registry_authority.sql, 0007_wp07_execution_receipt_lineage.sql, and 0009_wp09_interview_source_bridge.sql.
8. REGISTRIES READ: Loaded SDA registry (13 YAML definitions), SFL registry (28 definitions; 5 quarantined), and Primitive inventory (243 records; 1 duplicate quarantined) from WP-04 snapshot.
9. TEST PATTERN READ: Inspected test_*.py test files across services, verify_wp02a_foundation_structure.py, verify_wp03_first_slice.py, verify_wp08_reality_contact.py, and verify_ca_state_01.py.
10. REASONING/VALIDATION PROTOCOLS READ: Loaded Bundle v3 Protocols 08 (Implementation Gate), 09 (Reality Contact), 10 (Test Governance & Reward Hacking), 16 (Semantic Operations), and 21 (State Control Test/Proof).
```

---

## 2. Architectural Role and Boundaries

### 2.1 Artifact Classification & Ontological Plane
- **Artifact Class:** Implementation Technical Specification (`TS`).
- **Ontological Plane:** Bridges `CANONICAL_PLANE` (global templates, state transition contracts, error taxonomies) to `OPERATIONAL_PLANE` (tenant-isolated relational entities, private object storage, cryptographic execution receipts).
- **Architectural Role:** Authorizes and defines the exact engineering boundaries for `CA-IMPL-01A` (Staging Relational Containment, RLS, Storage Foundation, and Typed Model Scaffolding).

```text
+====================================================================================================+
|                                           CANONICAL PLANE                                          |
|                                (Global, Stateless, Versioned, Immutable)                           |
|                                                                                                    |
|   - HarnessTemplate (CA-STR-001): Runbook step sequences, contracts, parameter schemas            |
|   - StateTransitionContract (CA-POL-002): Allowed transitions (from_state -> to_state)             |
|   - ErrorTaxonomy & StateVocabulary: Global error taxonomy and immutable enum definitions          |
+====================================================================================================+
                                                  │
                                                  │ Parameterizes / Governs (Read-Only)
                                                  ▼
+====================================================================================================+
|                                          OPERATIONAL PLANE                                         |
|                             (Multi-Tenant Isolated, State Machine Instances)                       |
|                                                                                                    |
|   - Tenant Boundary: Workspace (CA-ENT-001) [workspace_id]                                         |
|   - Actor Boundary: WorkspaceMembership (CA-REL-001), OperatorAccessGrant (CA-REL-002)            |
|   - Project Envelope: Engagement (CA-ENT-004)                                                      |
|   - Participant Entity: Guest (CA-ENT-003) [Strictly Workspace-Local]                             |
|   - Evidence Assets: EvidenceSource (CA-REL-004), MediaAsset (CA-ENT-002), Storage (CA-EVI-001)   |
|   - Execution Instance: HarnessRun (CA-EXE-001)                                                    |
|   - Cryptographic Ledger: Receipt (CA-REC-001), ReceiptEvidenceLink (CA-REL-005)                  |
+====================================================================================================+
```

### 2.2 Nearest Neighbors & Semantic Boundaries
- **Upstream Governance:** Bounded by `CA-CAN-01A/B/C`, `PRD-CAE-TEN-001`, and `CA-STATE-01` migration contracts.
- **Downstream Implementation:** Authorizes `CA-IMPL-01A` (Staging Foundation) only. Does NOT authorize `CA-IMPL-01B` (Typed Runtime Operations) or `CA-IMPL-02` (Production Authority Cutover).
- **Hard Exclusions:**
  - Zero modification to legacy production SQLite databases.
  - Zero adoption of global/universal guest identity merges.
  - Zero unconsented cross-workspace data access.
  - Zero storage of raw audio/video byte payloads in relational PostgreSQL rows.
  - Zero unverified receipt self-attestation.

---

## 3. Brownfield Reality & Component Disposition

| Subsystem / Brownfield Path | Inspected Structure & Behavior | Disposition | Exact Integration & Adaptation Boundary |
|---|---|---|---|
| `api/main.py` | FastAPI application instantiating routers across services with SQLite initialization. | `ADAPT` | Introduce workspace resolution middleware (`WorkspaceContextMiddleware`) that extracts and cryptographically validates tenant context (`workspace_id`, `actor_id`) from trusted JWT/session tokens; rejects unauthenticated scope parameters. Legacy routes retained. |
| `api/domain/campaign.py` | Python domain model for campaign orders and lifecycles (`DRAFT` $\rightarrow$ `LAUNCHED` $\rightarrow$ `RUNNING` $\rightarrow$ `SHIPPED`). | `ADAPT` | Reconcile campaign fields with `Engagement` (`CA-ENT-004`) entity; enforce mandatory `workspace_id` containment foreign key. |
| `packages/ca_runtime` | Shared SQLite persistence (`ProductDatabase`), command/event/receipt recording, and initial PostgreSQL staging operations (`FirstSliceSemanticOperations`). | `EXTEND` | Add tenant-scoped composite primary keys, RLS session configuration (`set_config('app.current_workspace_id', ...)`), typed Pydantic v2 domain schemas, and atomic receipt-evidence linking. |
| `services/pipeline` | Local SQLite workflow execution service (`cmf_pipeline`) with `WorkflowRunService`. | `RETAIN` | Retained as legacy development engine; NO premature cutover. Runs in parallel during staging validation. |
| `services/interview` | SQLite-backed interview capture (`ie_objects`, `ie_edges`, `ie_events`). | `ADAPT` | Wrap interview export packages in `EvidenceSource` (`CA-REL-004`) bridge via WP-09 read-only protocol. |
| `services/air` | Qualitative analysis and evidence span parser. | `ADAPT` | Interface with staging `cae.evidence_item` tables via typed operations; remove direct database write mutations. |
| `services/studio` | Frontend workspace interface (`dist/rpc.js`). | `DEFER` | Client UI portal remains out-of-scope for the first vertical backend slice. |
| `storage/` | Local filesystem directories (`storage/harness-library`). | `NEW` | Provision private tenant-isolated Supabase/S3 Storage buckets (`cae-media/{workspace_id}/{asset_id}/...`) with SHA-256 content addressing. |

---

## 4. Functional Requirement Traceability

| FR ID | Requirement Title | Target Component / Schema | Authorized Operation / Contract | Verification Method |
|---|---|---|---|---|
| **`FR-CAE-TEN-001`** | Workspace Tenancy Boundary | `cae.workspace` | `workspace.provision@1.0.0` | RLS isolation test & composite key constraint verification |
| **`FR-CAE-TEN-002`** | Operator Governance Boundary | `cae.operator_organization` | `operator.org.register@1.0.0` | Governance boundary audit & tenant data exclusion test |
| **`FR-CAE-TEN-003`** | Workspace Membership Role | `cae.workspace_membership` | `workspace.membership.grant@1.0.0` | RBAC role transition test & revocation assertion |
| **`FR-CAE-TEN-004`** | Operator Access Policy Governance | `cae.operator_access_policy` | `operator.policy.define@1.0.0` | Policy scope validation & justification syntax enforcement |
| **`FR-CAE-TEN-005`** | Operator Access Grant Lifecycle | `cae.operator_access_grant` | `operator.grant.issue@1.0.0` | Time-to-live expiration & audit receipt logging verification |
| **`FR-CAE-TEN-006`** | Engagement Project Containment | `cae.engagement` | `engagement.initialize@1.0.0` | Workspace containment FK check & lifecycle progression test |
| **`FR-CAE-TEN-007`** | Guest Locality and Lifecycle | `cae.guest` | `guest.register@1.0.0` | Anti-cross-tenant query test & workspace locality assertion |
| **`FR-CAE-TEN-008`** | Guest Identity Link Anti-Merge | `cae.guest_identity_link` | `guest.link.propose@1.0.0` (DEFERRED) | Bilateral consent verification & auto-merge rejection test |
| **`FR-CAE-TEN-009`** | Evidence Source Provenance | `cae.evidence_source` | `evidence.source.register@1.0.0` | External package SHA-256 digest validation |
| **`FR-CAE-TEN-010`** | Media Asset Verification Lifecycle | `cae.media_asset` | `media.verify@1.0.0` | State machine `STAGED -> VERIFIED` and hash mismatch test |
| **`FR-CAE-TEN-011`** | Immutable Media Byte Isolation | Storage Bucket `cae-media` | `media.upload@1.0.0` | Private bucket path structure & SHA-256 byte readback check |
| **`FR-CAE-TEN-012`** | Harness Template Canonical Versioning | `cae.harness_template` | `template.publish@1.0.0` | Immutability check & zero tenant data constraint assertion |
| **`FR-CAE-TEN-013`** | Harness Run Execution Lifecycle | `cae.harness_run` | `harness.run.step@1.0.0` | State machine `INITIALIZED -> RUNNING -> COMPLETED` test |
| **`FR-CAE-TEN-014`** | Operation Receipt Immutable Ledger | `cae.receipt` | `receipt.commit@1.0.0` | Append-only trigger test & SHA-256 payload tampering check |
| **`FR-CAE-TEN-015`** | Receipt Evidence Lineage Traceability | `cae.receipt_evidence_link` | `receipt.link_evidence@1.0.0` | Causal lineage graph query & reality-contact verification |

---

## 5. Canonical Object & Schema Contract (Design Only — No SQL Executed)

### 5.1 Relational Entity Definitions & Constraints

```text
                                  +-----------------------+
                                  | OperatorOrganization  |
                                  | (operator_org_id PK)  |
                                  +-----------+-----------+
                                              |
                                              | 1:N
                                              v
                                  +-----------------------+
                                  |  OperatorAccessGrant  |
                                  |   (grant_id, org_id,  |
                                  |     workspace_id)     |
                                  +-----------+-----------+
                                              |
                                              | Ephemeral Diagnostic Access
                                              v
+===========================================================================================+
| WORKSPACE TENANCY ROOT (workspace_id UUID PK)                                             |
|                                                                                           |
|   +-----------------------+       +-----------------------+       +-------------------+   |
|   |  WorkspaceMembership  |       |       Engagement      |       |       Guest       |   |
|   | (workspace_id, actor) |       | (workspace_id, eng_id)|       | (workspace_id,    |   |
|   +-----------------------+       +-----------+-----------+       |     guest_id)     |   |
|                                               |                   +-------------------+   |
|                                               | 1:N                                       |
|                                               v                                           |
|                                   +-----------------------+                               |
|                                   |       MediaAsset      |                               |
|                                   |  (workspace_id,       |                               |
|                                   |    asset_id, sha256)  |                               |
|                                   +-----------+-----------+                               |
|                                               |                                           |
|                                               | 1:N                                       |
|                                               v                                           |
|   +-----------------------+       +-----------------------+       +-------------------+   |
|   |    HarnessTemplate    | ----> |       HarnessRun      |       |    EvidenceItem   |   |
|   | (template_id, version)| 1:N   | (workspace_id, run_id)|       |  (workspace_id,   |   |
|   | [CANONICAL PLANE]     |       +-----------+-----------+       |     item_id)      |   |
|   +-----------------------+                   |                   +---------+---------+   |
|                                               | 1:N                         |             |
|                                               v                             |             |
|                                   +-----------------------+                 |             |
|                                   |        Receipt        |                 |             |
|                                   |  (workspace_id,       |                 |             |
|                                   |     receipt_id)       |                 |             |
|                                   +-----------+-----------+                 |             |
|                                               |                             |             |
|                                               +--------------+--------------+             |
|                                                              |                            |
|                                                              v 1:N                        |
|                                                   +--------------------+                  |
|                                                   | ReceiptEvidenceLink|                  |
|                                                   | (receipt, evidence)|                  |
|                                                   +--------------------+                  |
+===========================================================================================+
```

### 5.2 Target Relational Table Schemas

#### 1. `cae.workspace` (Tenant Isolation Root)
- `workspace_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `slug` (`VARCHAR(64)`, Unique, Non-Null)
- `display_name` (`VARCHAR(255)`, Non-Null)
- `status` (`VARCHAR(32)`, Non-Null: `ACTIVE`, `SUSPENDED`, `ARCHIVED`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- `updated_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Row-Level Security:* Enabled; policy: `workspace_id = current_setting('app.current_workspace_id', true)::uuid`.

#### 2. `cae.workspace_membership` (Actor Binding)
- `membership_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)` ON DELETE CASCADE)
- `actor_id` (`VARCHAR(128)`, Non-Null)
- `role` (`VARCHAR(32)`, Non-Null: `ADMIN`, `MEMBER`, `OBSERVER`, `SYSTEM_AGENT`)
- `status` (`VARCHAR(32)`, Non-Null: `ACTIVE`, `REVOKED`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Unique Constraint:* `UNIQUE (workspace_id, actor_id)`

#### 3. `cae.operator_organization` (Governance Root — Platform Scope)
- `operator_org_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `org_name` (`VARCHAR(255)`, Non-Null)
- `status` (`VARCHAR(32)`, Non-Null: `ACTIVE`, `SUSPENDED`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)

#### 4. `cae.operator_access_grant` (Ephemeral Support Grant)
- `grant_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `operator_org_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.operator_organization(operator_org_id)`)
- `operator_actor_id` (`VARCHAR(128)`, Non-Null)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `justification` (`TEXT`, Non-Null)
- `expires_at` (`TIMESTAMPTZ`, Non-Null)
- `revoked_at` (`TIMESTAMPTZ`, Nullable)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)

#### 5. `cae.engagement` (Project Envelope)
- `engagement_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `title` (`VARCHAR(255)`, Non-Null)
- `lifecycle_state` (`VARCHAR(32)`, Non-Null: `PLANNED`, `ACTIVE`, `PAUSED`, `COMPLETED`, `ARCHIVED`)
- `version` (`BIGINT`, Default: `1`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- `updated_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Composite Key / Unique:* `UNIQUE (workspace_id, engagement_id)`

#### 6. `cae.guest` (Strictly Workspace-Local Participant)
- `guest_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `external_reference_id` (`VARCHAR(128)`, Nullable)
- `pseudonym` (`VARCHAR(128)`, Non-Null)
- `consent_status` (`VARCHAR(32)`, Non-Null: `PENDING`, `GRANTED`, `REVOKED`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Composite Unique:* `UNIQUE (workspace_id, guest_id)`
- *Constraint:* Cross-workspace searches and foreign keys on `guest_id` alone are prohibited.

#### 7. `cae.media_asset` (Relational Verification Metadata)
- `media_asset_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `engagement_id` (`UUID`, Nullable, FK $\rightarrow$ `cae.engagement(engagement_id)`)
- `storage_path` (`TEXT`, Non-Null)
- `canonical_sha256` (`VARCHAR(64)`, Non-Null)
- `byte_size` (`BIGINT`, Non-Null)
- `mime_type` (`VARCHAR(128)`, Non-Null)
- `lifecycle_state` (`VARCHAR(32)`, Non-Null: `REGISTERED`, `STAGED`, `VERIFIED`, `QUARANTINED`, `REVOKED`)
- `version` (`BIGINT`, Default: `1`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)

#### 8. `cae.harness_template` (Canonical Structural Grammar — Canonical Plane)
- `template_id` (`VARCHAR(64)`, Non-Null)
- `version` (`VARCHAR(32)`, Non-Null)
- `definition_yaml` (`TEXT`, Non-Null)
- `definition_sha256` (`VARCHAR(64)`, Non-Null)
- `is_active` (`BOOLEAN`, Default: `true`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Primary Key:* `PRIMARY KEY (template_id, version)`
- *Constraint:* Contains ZERO tenant identifiers, ZERO guest data, and ZERO storage URLs.

#### 9. `cae.harness_run` (Operational Run State Machine)
- `run_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `engagement_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.engagement(engagement_id)`)
- `template_id` (`VARCHAR(64)`, Non-Null)
- `template_version` (`VARCHAR(32)`, Non-Null)
- `current_step` (`VARCHAR(64)`, Non-Null)
- `lifecycle_state` (`VARCHAR(32)`, Non-Null: `INITIALIZED`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `CANCELLED`)
- `version` (`BIGINT`, Default: `1`)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- `updated_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)

#### 10. `cae.receipt` (Immutable Execution & Audit Ledger)
- `receipt_id` (`VARCHAR(128)`, Primary Key)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `operation_id` (`VARCHAR(128)`, Non-Null)
- `idempotency_key` (`VARCHAR(128)`, Non-Null)
- `actor_id` (`VARCHAR(128)`, Non-Null)
- `canonical_payload` (`TEXT`, Non-Null)
- `payload_jsonb` (`JSONB`, Non-Null)
- `payload_sha256` (`VARCHAR(64)`, Non-Null)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Unique Constraint:* `UNIQUE (workspace_id, operation_id, idempotency_key)`
- *Immutability Rule:* Update/Delete strictly prohibited via trigger.

#### 11. `cae.receipt_evidence_link` (Reality Contact Junction)
- `link_id` (`UUID`, Primary Key, Default: `gen_random_uuid()`)
- `workspace_id` (`UUID`, Non-Null, FK $\rightarrow$ `cae.workspace(workspace_id)`)
- `receipt_id` (`VARCHAR(128)`, Non-Null, FK $\rightarrow$ `cae.receipt(receipt_id)`)
- `evidence_item_id` (`UUID`, Non-Null)
- `created_at` (`TIMESTAMPTZ`, Default: `clock_timestamp()`)
- *Unique Constraint:* `UNIQUE (workspace_id, receipt_id, evidence_item_id)`

---

## 6. Relationships, State Machines, Events, and Temporal Semantics

### 6.1 State Machines & Legal Transitions

#### 1. `MediaAsset` Lifecycle
```text
[ REGISTERED ] ──(upload bytes)──> [ STAGED ] ──(verify sha256)──> [ VERIFIED ]
                                      │                                 │
                               (hash mismatch)                   (revoke asset)
                                      ▼                                 ▼
                               [ QUARANTINED ]                    [ REVOKED ]
```

#### 2. `Engagement` Lifecycle
```text
[ PLANNED ] ──(activate)──> [ ACTIVE ] ──(pause)──> [ PAUSED ]
                                │                       │
                            (complete)               (resume)
                                ▼                       ▼
                           [ COMPLETED ]           [ ACTIVE ]
                                │
                            (archive)
                                ▼
                           [ ARCHIVED ]
```

#### 3. `HarnessRun` Lifecycle
```text
[ INITIALIZED ] ──(start)──> [ RUNNING ] ──(step success)──> [ COMPLETED ]
                                 │
                            (step fail)
                                 ▼
                             [ FAILED ]
```

### 6.2 Optimistic Concurrency & Version Locking
Every update to a stateful operational aggregate (`Engagement`, `MediaAsset`, `HarnessRun`) MUST evaluate:
```sql
UPDATE cae.<table_name>
SET lifecycle_state = :new_state, version = version + 1, updated_at = clock_timestamp()
WHERE workspace_id = :workspace_id AND id = :id AND version = :expected_version;
```
If zero rows are updated, the operation raises `SemanticOperationConflict` (`STATE_ERROR: STALE_VERSION`).

---

## 7. Authorized Typed Semantic Operations & Agent Program Contract

### 7.1 Governing Principles
1. **Scope Derivation:** `workspace_id` is derived strictly from trusted authorization tokens (JWT / Session context). The caller-supplied `workspace_id` parameter is verified against the context and never trusted alone.
2. **No Direct SQL for Normal Agents:** Agents and services interact strictly through typed operations in `ca_runtime.semantic_operations`.
3. **Atomic State & Receipt Persistence:** State transitions, event emissions, receipt insertions, and evidence linkages commit in one atomic PostgreSQL transaction (`BEGIN ... COMMIT`).

### 7.2 Operation Catalog (Summary)

```text
+------------------------------------+---------------------------------------------------------------+
| Operation ID                       | Purpose & State Transition                                    |
+------------------------------------+---------------------------------------------------------------+
| cae.workspace.provision@1.0.0      | Provision new client Workspace root entity.                   |
| cae.workspace.membership.grant@1.0.0| Grant/bind actor role to Workspace.                           |
| cae.operator.grant.issue@1.0.0     | Issue time-bounded diagnostic access grant to platform operator.|
| cae.engagement.initialize@1.0.0   | Create new Engagement envelope in PLANNED state.              |
| cae.guest.register@1.0.0           | Register workspace-local Guest profile.                       |
| cae.media.verify@1.0.0             | Read back bytes from Storage, check SHA-256, STAGED->VERIFIED.|
| cae.evidence.capture@1.0.0         | Extract and anchor EvidenceSpan from verified MediaAsset.     |
| cae.harness.run.initialize@1.0.0   | Instantiate HarnessRun referencing canonical HarnessTemplate. |
| cae.harness.run.step@1.0.0         | Advance HarnessRun state machine through discrete step.       |
| cae.receipt.commit@1.0.0           | Record immutable operation receipt and reality contact link.  |
+------------------------------------+---------------------------------------------------------------+
```

---

## 8. Intermediate Representation (IR) & Runtime Contract

### 8.1 Pydantic Model Boundaries
- Core models reside in `packages/ca_runtime/src/ca_runtime/models/tenant_slice.py`.
- Enforce strict typing, immutability (`frozen=True`), and validation of UUID strings and SHA-256 hexadecimal digests.

### 8.2 Execution Receipt Envelope
```json
{
  "receipt_type": "cae_execution_receipt",
  "receipt_id": "rcpt_cae_01h9x7z8...",
  "workspace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "operation_id": "cae.media.verify@1.0.0",
  "idempotency_key": "idemp_med_verify_001",
  "actor_id": "usr_analyst_01",
  "input_snapshot_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "output_snapshot_sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
  "environment_fidelity": "E3_PRODUCTION_SHAPED",
  "environment_identity": {
    "state_authority": "postgresql_supabase",
    "runtime_component": "ca_runtime.semantic_operations",
    "deployment_boundary": "staging_only"
  },
  "evaluator_versions": {
    "media_verifier": "cae.media.verify@1.0.0"
  },
  "validator_results": {
    "transition_contract": "PASS",
    "storage_sha256_match": "PASS"
  },
  "reward_hack_result": "UNVERIFIED",
  "taste_integrity_result": "NOT_APPLICABLE",
  "anti_centroid_result": "NOT_APPLICABLE"
}
```

---

## 9. Validation and Error Taxonomy

| Error Code | Error Category | Description & Cause | Fatality Level | Recovery / Remediation |
|---|---|---|---|---|
| `TENANCY_VIOLATION` | `PROVENANCE_ERROR` | Cross-workspace foreign key, missing tenant context, or forged `workspace_id`. | FATAL | Terminate transaction immediately; log security incident. |
| `UNAUTHORIZED_OPERATOR_ACCESS` | `CONTRACT_ERROR` | Operator access attempted without active, valid `OperatorAccessGrant`. | FATAL | Deny access; require formal grant issuance. |
| `CROSS_WORKSPACE_LEAK` | `RELATION_ERROR` | Attempted relation linking objects from two different workspaces. | FATAL | Reject write; isolate entities. |
| `UNVERIFIED_MEDIA_DIGEST` | `EVIDENCE_ERROR` | Storage byte SHA-256 digest does not match claimed hash. | RECOVERABLE | Transition `MediaAsset` to `QUARANTINED`; request re-upload. |
| `RECEIPT_SELF_ATTESTATION_VIOLATION` | `VALIDATION_ERROR` | Claiming qualitative or semantic truth based solely on receipt existence. | FATAL | Invalidate claim; route to independent evaluator. |
| `STALE_VERSION_CONFLICT` | `STATE_ERROR` | Concurrency version mismatch during state transition. | RECOVERABLE | Reload current aggregate state and retry. |
| `IDEMPOTENCY_PAYLOAD_MISMATCH` | `CONTRACT_ERROR` | Re-submitting identical idempotency key with different payload. | FATAL | Reject command with conflict error. |

---

## 10. Implementation Plan

### 10.1 Staging Phasing Boundary (`CA-IMPL-01A`)
1. **Module Scaffolding:** Create `packages/ca_runtime/src/ca_runtime/models/tenant_slice.py` containing strongly typed Pydantic models.
2. **Context Manager:** Create `packages/ca_runtime/src/ca_runtime/tenancy.py` for RLS workspace session variable management.
3. **Database Migration Script (Staging Only):** Prepare `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py` applying PostgreSQL schema and RLS policies on disposable staging Supabase instances.
4. **Unit & Isolation Test Suite:** Author `tests/cae/test_tenant_slice_scaffolding.py` executing tenant containment and RLS verification.

---

## 11. Backward Compatibility, Migration & Rollback

### 11.1 Brownfield Compatibility Invariants
- Existing SQLite databases (`cmf_pipeline.db`, `campaign.db`, `interview.db`) remain untouched and operational for existing tests and services.
- No live service write paths are cut over in this phase.
- Staging PostgreSQL tables run in parallel under strict schema separation (`cae.*`).

### 11.2 Rollback Procedure
If staging verification detects structural defects:
1. Execute schema down-migration dropping `cae.*` staging tables and functions.
2. Delete transient objects under `storage://cae-media/staging-test/`.
3. Reset `CAE_IMPLEMENTATION_CONTROL_STATE.md` to `CA_STATE_01_ACCEPTED`.

---

## 12. Acceptance Criteria

```text
AC-01: Workspace Tenancy Containment
  GIVEN an authenticated actor in Workspace A
  WHEN the actor attempts to query or insert records belonging to Workspace B
  THEN PostgreSQL Row-Level Security and foreign key constraints reject the operation with TENANCY_VIOLATION.
  Failure Example: Query returns rows from another workspace.
  Governing Contract: MC-CAE-WS-001 / FR-CAE-TEN-001.

AC-02: Media Asset Hash Verification
  GIVEN a media asset uploaded to private Supabase Storage
  WHEN media.verify@1.0.0 is executed
  THEN the operation reads back raw bytes, verifies SHA-256 match, and atomically transitions state from STAGED to VERIFIED.
  Failure Example: Asset is marked VERIFIED despite hash mismatch.
  Governing Contract: MC-CAE-MED-001 / FR-CAE-TEN-010.

AC-03: Guest Locality Anti-Merge
  GIVEN two guests with identical names/emails in Workspace A and Workspace B
  WHEN querying guests within Workspace A
  THEN only Workspace A guest records are returned, with zero cross-tenant merging.
  Failure Example: Guest records automatically merge across workspaces.
  Governing Contract: MC-CAE-GST-001 / FR-CAE-TEN-007.

AC-04: Receipt Immutability & Lineage
  GIVEN an emitted operation receipt
  WHEN an update or delete is attempted on cae.receipt
  THEN PostgreSQL trigger aborts the transaction with FATALITY.
  Failure Example: Receipt row updated in place.
  Governing Contract: MC-CAE-REC-001 / FR-CAE-TEN-014.
```

---

## 13. Dependencies & External Concept Adaptations

### 13.1 Infrastructure & Storage Dependencies
- PostgreSQL 15+ / Supabase with `pgcrypto` extension.
- Private Supabase Storage / S3-compatible bucket `cae-media`.

### 13.2 StateM Reference Boundary
- **Reference Status:** `ADAPTED_CONCEPT` (State machine transition contracts and event logs adapted from StateM pattern).
- **Storage Boundary:** Local StateM storage is NOT used; CAE adopts PostgreSQL/Supabase as durable state authority.
- **Reference Citations:** StateM repository: `https://github.com/cased/statem`; Paper: `https://arxiv.org/abs/2403.00001`.

---

## 14. Testing and Reality-Contact Verification

### 14.1 Reality-Contact Evaluation Table

| Claim | Proxy | Intended Property | Minimum Fidelity | Gaming Strategy | Counter-Test | Taste/Reality Test | Receipt Verification |
|---|---|---|---|---|---|---|---|
| Multi-tenant containment | RLS session variable | Complete data isolation between client tenants | `E3_STAGING` | Service role key bypass or global query | Attempt cross-tenant SELECT with forged workspace header | Multi-tenant adversarial penetration test | Receipt asserts `tenancy_isolation: PASS` |
| Media byte integrity | SHA-256 digest check | Stored file bytes match recorded hash exactly | `E3_STAGING` | Register URL path without reading back file bytes | Corrupt 1 byte in Storage payload and execute verify | Raw byte readback comparison test | Receipt asserts `storage_sha256_match: PASS` |
| Guest locality | Workspace FK on Guest table | Guest facts never bleed across client engagements | `E3_STAGING` | Cross-workspace search on email/phone | Query guest across workspaces with identical email | Independent tenant search query | Receipt asserts `guest_merge: REJECTED` |
| Receipt immutability | DB trigger preventing UPDATE | Audit log is tamper-evident and append-only | `E3_STAGING` | In-place UPDATE on receipt table | Execute direct SQL UPDATE on committed receipt | DB raises exception; row unchanged | Receipt trigger log confirmed |

### 14.2 Explicit Statement of Non-Claims
1. **No Production Parity Claim:** Staging RLS and schema tests do not claim live multi-region production readiness.
2. **No Qualitative / Semantic Taste Claim:** Structural receipt generation does NOT prove SDA direction, SFL perceptual fidelity, Matrix of Edging resonance, or human value.
3. **No Legacy Data Migration Claim:** Authoring this spec migrates ZERO legacy rows and modifies ZERO production databases.
