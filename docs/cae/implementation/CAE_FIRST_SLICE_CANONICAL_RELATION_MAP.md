# CAE First-Slice Canonical Relation Map

**Status:** `FIRST_SLICE_RELATION_MAP_AUTHORED`  
**Phase ID:** `CA-CAN-01C`  
**Date:** 2026-08-25  
**Governing Mandates:** `docs/cae/gemini_execution/04_CA_CAN_01A_WORKSPACE_TENANCY_MANDATE.md`, `05_CA_CAN_01B_GUEST_EVIDENCE_MANDATE.md`, `06_CA_CAN_01C_HARNESS_RECEIPT_RELATION_INTEGRATION_MANDATE.md`  
**Authority Reference:** CAE Governance & Specification Bridge Bundle v3; Phase 0 Object Constitution Protocol; Multi-Tenant Authority and Canonicalization Plan §2–§4  

---

## 1. Executive Summary & Legal Containment Model

This document establishes the **Canonical Relation Map** for the Conscious Activation Engine (CAE) First Vertical Slice. 

> [!IMPORTANT]
> **This is a legal relationship, authority, and containment model, NOT an SQL entity-relationship diagram.**  
> It defines the precise topological, evidentiary, and jurisdictional constraints governing objects across both the **Canonical Plane** (global, versioned, tenantless doctrine) and the **Operational Plane** (tenant-isolated, append-only, state-controlled reality).

```text
+====================================================================================================+
|                                           CANONICAL PLANE                                          |
|                       (Global Vocabulary, Geometric Direction, Procedural Rules)                  |
|                                                                                                    |
|    +----------------------+     +----------------------+     +-------------------------------+     |
|    |     SDA Registry     |     |     SFL Registry     |     |      Primitive Registry       |     |
|    | (Direction/Geometry) |     | (Perceptual Delivery)|     | (Semantic Primitives: 241/243)|     |
|    +----------+-----------+     +----------+-----------+     +---------------+---------------+     |
|               |                            |                                 |                     |
|               +----------------------------+---------------------------------+                     |
|                                            |                                                       |
|                                            v                                                       |
|                         +-------------------------------------+                                    |
|                         |       HarnessTemplate (CA-STR-001)   |                                    |
|                         |  (Canonical Runbook State Machine)  |                                    |
|                         +------------------+------------------+                                    |
|                                            |                                                       |
|                                            v                                                       |
|                         +-------------------------------------+                                    |
|                         |    StateTransitionContract (CA-POL-002)                                  |
|                         +------------------+------------------+                                    |
+============================================|=======================================================+
                                             | (Read-Only Reference via Pinned Snapshot & Semver)
                                             v
+====================================================================================================+
|                                          OPERATIONAL PLANE                                         |
|                 (Tenant Isolation, Cryptographic Lineage, State Transitions, Audit Proof)           |
|                                                                                                    |
|   +--------------------------------------------------------------------------------------------+   |
|   |                               OPERATOR AUDIT & GOVERNANCE                                  |   |
|   |     OperatorOrganization (CA-ENT-000)                                                      |   |
|   |       ├── OperatorAccessPolicy (CA-POL-001) [Global Audit Policy]                          |   |
|   |       └── OperatorAccessGrant (CA-REL-002) [Time/Reason-Bounded Bridge to Workspace]       |   |
|   +---------------------------------------------+----------------------------------------------+   |
|                                                 | (Audited Diagnostic Access Only)                 |
|                                                 v                                                  |
|   +--------------------------------------------------------------------------------------------+   |
|   |                                 WORKSPACE (TENANT ROOT)                                    |   |
|   |                                     (CA-ENT-001)                                           |   |
|   |                                                                                            |   |
|   |   +--------------------------+                         +-------------------------------+   |   |
|   |   | WorkspaceMembership      |                         | Guest (CA-ENT-003)            |   |   |
|   |   | (CA-REL-001)             |                         | (Strictly Workspace-Local)    |   |   |
|   |   +------------+-------------+                         +---------------+---------------+   |   |
|   |                |                                                       |                   |   |
|   |                +---------------------------+---------------------------+                   |   |
|   |                                            |                                               |   |
|   |                                            v                                               |   |
|   |                         +--------------------------------------+                           |   |
|   |                         | Engagement (CA-ENT-004)              |                           |   |
|   |                         | (Project / Campaign Context)         |                           |   |
|   |                         +------------------+-------------------+                           |   |
|   |                                            |                                               |   |
|   |                 +--------------------------+--------------------------+                    |   |
|   |                 |                                                     |                    |   |
|   |                 v                                                     v                    |   |
|   |   +----------------------------+                        +------------------------------+   |   |
|   |   | EvidenceSource (CA-REL-004)|                        | HarnessRun (CA-EXE-001)      |   |   |
|   |   | └── MediaAsset (CA-ENT-002)|                        | └── Command (CA-EXE-002)     |   |   |
|   |   |     └── EvidenceBytes      |                        |     └── StateAggregate       |   |   |
|   |   |         (CA-EVI-001)       |                        |         └── StateTransition  |   |   |
|   |   +--------------+-------------+                        |             └── Event        |   |   |
|   |                  |                                      +--------------+---------------+   |   |
|   |                  v                                                     |                   |   |
|   |   +----------------------------+                                       |                   |   |
|   |   | EvidenceItem (CA-EVI-002)  |                                       |                   |   |
|   |   | ├── EvidenceSpan (CA-REL-003)                                      |                   |   |
|   |   | └── EvidenceAuthentication <---------------------------------------+                   |   |
|   |   |     (CA-REC-002)           |                                       |                   |   |
|   |   +--------------+-------------+                                       |                   |   |
|   |                  |                                                     |                   |   |
|   |                  +--------------------------+--------------------------+                   |   |
|   |                                             |                                              |   |
|   |                                             v                                              |   |
|   |                          +-------------------------------------+                           |   |
|   |                          | SemanticAssessment (CA-ART-001)     |                           |   |
|   |                          | └── AssessmentEvidenceLink          |                           |   |
|   |                          +------------------+------------------+                           |   |
|   |                                             |                                              |   |
|   |                                             v                                              |   |
|   |                          +-------------------------------------+                           |   |
|   |                          | Receipt (CA-REC-001)                |                           |   |
|   |                          | ├── ExecutionReceipt                |                           |   |
|   |                          | └── ReceiptEvidenceLink (CA-REL-005)|                           |   |
|   |                          +-------------------------------------+                           |   |
|   +--------------------------------------------------------------------------------------------+   |
+====================================================================================================+
```

---

## 2. Canonical Plane vs Operational Plane Cross-Boundary Relations

### REL-CANON-001: `HarnessRunUsesTemplate`
- **Source Object:** `HarnessRun` (`OPERATIONAL_PLANE`, Scope: `ENGAGEMENT_SCOPED`)
- **Target Object:** `HarnessTemplate` (`CANONICAL_PLANE`, Scope: `GLOBAL_CANONICAL`)
- **Direction:** Operational `HarnessRun` $\longrightarrow$ Canonical `HarnessTemplate` (Unidirectional forward reference)
- **Cardinality & Temporal Behavior:** `N : 1` (Many operational runs reference one pinned template version; immutable link post-run-initialization)
- **Scope Inheritance & Tenant Containment:** The operational run inherits the procedural graph and constraints of the template; the canonical template absorbs ZERO tenant data and retains no reference to the run.
- **Authority Axes:**
  - *Definition Source:* Multi-Tenant Authority Plan §3; Bundle v3 `17_CAE_HARNESS_RUNBOOK_INTEGRATION_PROTOCOL.md`
  - *Target Runtime Representation:* Foreign reference columns `cae.harness_run.template_id`, `cae.harness_run.template_version`
  - *Change / Promotion Authority:* Workspace Runner Service binds at initialization; Canonical Architecture Governance Committee governs template publication.
- **Evidentiary Meaning:** Proves that an operational execution followed the exact procedural graph, before-transfer checks, and transition contracts defined in the pinned canonical specification.
- **Allowed Operations:** `initialize_harness_run(template_id, template_version)`
- **Prohibited Inferences:** MUST NOT infer that the HarnessRun may mutate the template, nor that template existence proves a general orchestrator exists.
- **Evidence Reference:** `[DOCUMENT]` `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml`, `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:178-200`

---

## 3. Operational Plane Legal Containment Chains

### REL-OP-001: `WorkspaceContainsMembership`
- **Source Object:** `Workspace` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `WorkspaceMembership` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `Workspace` $\longrightarrow$ `WorkspaceMembership` (1:N Parent-to-Child)
- **Cardinality & Temporal Behavior:** `1 : N` (A workspace has multiple actor memberships; memberships are versioned and revocable)
- **Scope Inheritance & Tenant Containment:** Every membership is strictly contained within its parent `workspace_id`. Cross-workspace memberships are distinct rows.
- **Authority Axes:**
  - *Definition Source:* Multi-Tenant Plan §3; CA-CAN-01A Constitution
  - *Target Runtime Representation:* `cae.actor` / `cae.workspace_membership` with composite key `(workspace_id, actor_id)`
  - *Change / Promotion Authority:* Workspace Administrator via typed operation `grant_workspace_membership`
- **Evidentiary Meaning:** Authorizes an external subject to execute scoped semantic operations within the tenant boundary.
- **Allowed Operations:** `grant_workspace_membership`, `revoke_workspace_membership`, `update_workspace_role`
- **Prohibited Inferences:** MUST NOT infer global cross-workspace administrative authority from a single workspace membership.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:28-36`, `sql/0002_cae_workspace_rls.sql:13-26`

---

### REL-OP-002: `WorkspaceContainsGuest`
- **Source Object:** `Workspace` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `Guest` (`OPERATIONAL_PLANE`, Scope: `GUEST_SCOPED`)
- **Direction:** `Workspace` $\longrightarrow$ `Guest` (1:N Parent-to-Child)
- **Cardinality & Temporal Behavior:** `1 : N` (A workspace contains multiple guest profiles; strictly local to that workspace)
- **Scope Inheritance & Tenant Containment:** Guest identity is strictly local to `workspace_id`. Global guest pooling and automatic matching are prohibited.
- **Authority Axes:**
  - *Definition Source:* Multi-Tenant Plan §3; CA-CAN-01B Constitution
  - *Target Runtime Representation:* `cae.actor` (kind='GUEST') / `cae.guest` with composite key `(workspace_id, guest_id)`
  - *Change / Promotion Authority:* Workspace Engagement Lead / Guest Consent Action
- **Evidentiary Meaning:** Represents the participant whose interview expressions and evidence are captured within this workspace.
- **Allowed Operations:** `register_guest`, `update_guest_profile`, `archive_guest`
- **Prohibited Inferences:** MUST NOT infer that two guest rows in different workspaces representing the same human can be merged automatically.
- **Evidence Reference:** `[DOCUMENT]` `CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:70`, `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:74`

---

### REL-OP-003: `WorkspaceContainsEngagement`
- **Source Object:** `Workspace` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `Engagement` (`OPERATIONAL_PLANE`, Scope: `ENGAGEMENT_SCOPED`)
- **Direction:** `Workspace` $\longrightarrow$ `Engagement` (1:N Parent-to-Child)
- **Cardinality & Temporal Behavior:** `1 : N` (A workspace contains multiple engagements; lifecycle is stateful from PLANNED to ARCHIVED)
- **Scope Inheritance & Tenant Containment:** Engagement is strictly contained within `workspace_id`. All sub-resources (sessions, runs) inherit this scope.
- **Authority Axes:**
  - *Definition Source:* Multi-Tenant Plan §3; CA-CAN-01A Constitution
  - *Target Runtime Representation:* `cae.project` / `cae.engagement` with composite key `(workspace_id, project_id)`
  - *Change / Promotion Authority:* Workspace Engagement Lead via typed semantic operations
- **Evidentiary Meaning:** Defines the operational campaign or client study envelope.
- **Allowed Operations:** `create_engagement`, `transition_engagement_state`, `archive_engagement`
- **Prohibited Inferences:** MUST NOT infer that an engagement can span across multiple workspaces.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:20-26`, `[EXECUTABLE]` `api/domain/campaign.py:18-27`

---

### REL-OP-004: `EngagementScopingHarnessRun`
- **Source Object:** `Engagement` (`OPERATIONAL_PLANE`, Scope: `ENGAGEMENT_SCOPED`)
- **Target Object:** `HarnessRun` (`OPERATIONAL_PLANE`, Scope: `ENGAGEMENT_SCOPED`)
- **Direction:** `Engagement` $\longrightarrow$ `HarnessRun` (1:N Parent-to-Child)
- **Cardinality & Temporal Behavior:** `1 : N` (An engagement coordinates multiple execution runs over time)
- **Scope Inheritance & Tenant Containment:** Every HarnessRun inherits `workspace_id` and `project_id` from its parent Engagement.
- **Authority Axes:**
  - *Definition Source:* Multi-Tenant Plan §3; CA-CAN-01C Constitution
  - *Target Runtime Representation:* Foreign keys `cae.harness_run.workspace_id`, `cae.harness_run.project_id`
  - *Change / Promotion Authority:* Workspace Runner Service via registered typed semantic operations
- **Evidentiary Meaning:** Binds procedural runbook execution to a specific client engagement.
- **Allowed Operations:** `initialize_harness_run`, `step_harness_run`, `abort_harness_run`
- **Prohibited Inferences:** MUST NOT infer that a run can execute outside of an engagement context.
- **Evidence Reference:** `[DOCUMENT]` `CAE_WP06_HARNESS_RUNBOOK_INTEGRATION.md`, `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:178-185`

---

### REL-OP-005: `EvidenceSourceContainsMediaAsset`
- **Source Object:** `EvidenceSource` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `MediaAsset` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `EvidenceSource` $\longrightarrow$ `MediaAsset` (1:1 Provenance Envelope to Internal Asset)
- **Cardinality & Temporal Behavior:** `1 : 1` (An external source package registers exactly one internal MediaAsset entity)
- **Scope Inheritance & Tenant Containment:** Both objects share identical `workspace_id`.
- **Authority Axes:**
  - *Definition Source:* WP-09 First Vertical Runtime Slice; CA-CAN-01B Constitution
  - *Target Runtime Representation:* Foreign key `cae.source_package.media_asset_id`
  - *Change / Promotion Authority:* Ingestion Bridge Adapter via typed operation `cae.bridge.register-interview-source` (STC-BRIDGE-000)
- **Evidentiary Meaning:** Establishes cryptographic provenance linking external package digests to internal content-addressed assets.
- **Allowed Operations:** `admit_source_package`, `verify_source_package`
- **Prohibited Inferences:** MUST NOT interpret upstream legacy source authority as CAE administrative privilege.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:59-68`, `[MIGRATION]` `sql/0009_cae_interview_source_bridge_operation.sql`

---

### REL-OP-006: `MediaAssetReferencesImmutableBytes`
- **Source Object:** `MediaAsset` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `ImmutableMediaEvidence` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `MediaAsset` $\longrightarrow$ `ImmutableMediaEvidence` (1:1 Metadata to Storage Payload)
- **Cardinality & Temporal Behavior:** `1 : 1` (Relational metadata points to immutable byte payload in private bucket)
- **Scope Inheritance & Tenant Containment:** Private bucket path is strictly prefixed: `storage://cae-media/{workspace_id}/{asset_id}/...`
- **Authority Axes:**
  - *Definition Source:* Builder ADR-003; CA-CAN-01B Constitution
  - *Target Runtime Representation:* `cae.media_asset.storage_path`, `cae.media_asset.canonical_sha256`
  - *Change / Promotion Authority:* Storage Ingestion Gateway via byte-level SHA-256 verification
- **Evidentiary Meaning:** Guarantees that relational metadata corresponds to tamper-evident physical recording bytes.
- **Allowed Operations:** `upload_media_bytes`, `verify_media_asset`
- **Prohibited Inferences:** MUST NOT store raw audio bytes in PostgreSQL relational rows.
- **Evidence Reference:** `[DOCUMENT]` Builder ADR-003, `[TEST]` `scripts/cae/verify_private_storage.py`

---

### REL-OP-007: `EvidenceItemAnchoredBySpan`
- **Source Object:** `EvidenceItem` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `EvidenceSpan` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `EvidenceItem` $\longrightarrow$ `EvidenceSpan` (1:N Primary Claim to Media Anchors)
- **Cardinality & Temporal Behavior:** `1 : N` (An evidence item is anchored by one or more contiguous/discontinuous spans in media or turns)
- **Scope Inheritance & Tenant Containment:** Strictly within the same `workspace_id`.
- **Authority Axes:**
  - *Definition Source:* State Reconciliation §40; CA-CAN-01B Constitution
  - *Target Runtime Representation:* `cae.evidence_span.evidence_id`
  - *Change / Promotion Authority:* Workspace Evidence Capture Agent via typed operation `capture_evidence` (STC-EVID-000)
- **Evidentiary Meaning:** Binds subjective or objective evidence claims to verifiable physical temporal/character offsets.
- **Allowed Operations:** `capture_evidence`, `authenticate_evidence`
- **Prohibited Inferences:** MUST NOT create an unanchored evidence item without valid span links.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:94-118`, `[TEST]` `scripts/cae/verify_wp03_first_slice.py`

---

### REL-OP-008: `SemanticAssessmentLinksEvidence`
- **Source Object:** `SemanticAssessment` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `EvidenceItem` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `SemanticAssessment` $\longrightarrow$ `AssessmentEvidenceLink` $\longrightarrow$ `EvidenceItem` (N:M via Relation Table)
- **Cardinality & Temporal Behavior:** `N : M` (Assessments cite multiple evidence items with roles: SUPPORTS, CONTRADICTS, CONTEXTUALIZES)
- **Scope Inheritance & Tenant Containment:** Both assessment and evidence items must share identical `workspace_id`.
- **Authority Axes:**
  - *Definition Source:* State Reconciliation §41; CA-MAP-01 Matrix
  - *Target Runtime Representation:* `cae.assessment_evidence_link` with composite PK `(assessment_id, assessment_revision, evidence_id, relation_type)`
  - *Change / Promotion Authority:* Workspace AIR Analyst / Evaluator via `validate_semantic_assessment` (STC-AIR-001)
- **Evidentiary Meaning:** Establishes the factual grounding of derived semantic assessments against primary evidence.
- **Allowed Operations:** `propose_semantic_assessment`, `validate_semantic_assessment`, `confirm_semantic_assessment`
- **Prohibited Inferences:** MUST NOT treat an ungrounded assessment as valid without evidence links.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:130-153`

---

### REL-OP-009: `ReceiptRecordsOperationAndTransition`
- **Source Object:** `Receipt` / `ExecutionReceipt` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `Command` / `StateTransition` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `Receipt` $\longrightarrow$ `Command` + `StateTransition` (1:1 Atomic Transition Audit Link)
- **Cardinality & Temporal Behavior:** `1 : 1` (Every consequential state transition emits exactly one immutable execution receipt)
- **Scope Inheritance & Tenant Containment:** Strictly within the same `workspace_id`.
- **Authority Axes:**
  - *Definition Source:* Bundle v3 `11_CAE_PHASE_PROMOTION_AND_PROOF_PROTOCOL.md`, `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`
  - *Target Runtime Representation:* `cae.receipt.command_id`, `cae.receipt.transition_id`, `cae.execution_receipt.receipt_id`
  - *Change / Promotion Authority:* CAE Runtime State Engine / Transactional Operation Adapter at commit time
- **Evidentiary Meaning:** Cryptographic proof that an authorized command executed, satisfied its contract, and committed state.
- **Allowed Operations:** `commit_execution_receipt`, `verify_receipt_integrity`
- **Prohibited Inferences:** MUST NOT treat receipt presence as independent proof of semantic truth, human truth, or taste quality without separate evaluator evidence.
- **Evidence Reference:** `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:233-240`, `sql/0008_cae_execution_receipt_lineage.sql:5-33`

---

### REL-OP-010: `ReceiptLinksEvidenceLineage`
- **Source Object:** `Receipt` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Target Object:** `EvidenceItem` (`OPERATIONAL_PLANE`, Scope: `WORKSPACE_SCOPED`)
- **Direction:** `Receipt` $\longrightarrow$ `ReceiptEvidenceLink` $\longrightarrow$ `EvidenceItem` (N:M Lineage Bridge)
- **Cardinality & Temporal Behavior:** `N : M` (Execution receipts record the specific evidence items used or produced during operation commit)
- **Scope Inheritance & Tenant Containment:** Strictly within the same `workspace_id`. Cross-workspace evidence linking is rejected by triggers.
- **Authority Axes:**
  - *Definition Source:* WP-07 Execution Receipts & Evidence Lineage; CA-CAN-01C Constitution
  - *Target Runtime Representation:* `cae.receipt_evidence_link` + view `cae.v_receipt_evidence_lineage`
  - *Change / Promotion Authority:* CAE Runtime State Engine / Transactional Operation Adapter at commit time
- **Evidentiary Meaning:** Establishes auditable proof of reality contact for anti-reward-hacking verification.
- **Allowed Operations:** `link_receipt_evidence`
- **Prohibited Inferences:** MUST NOT link evidence from Workspace A into a receipt for Workspace B.
- **Evidence Reference:** `[SCHEMA]` `sql/0008_cae_execution_receipt_lineage.sql:5-33`, `[TEST]` `scripts/cae/verify_wp07_receipt_lineage.py`

---

## 4. Summary Relation Matrix

| Relation ID | Relation Name | Source Object | Target Object | Cardinality | Direction | Tenant Containment | Evidentiary Role |
|---|---|---|---|---|---|---|---|
| `REL-CANON-001` | `HarnessRunUsesTemplate` | `HarnessRun` (Op) | `HarnessTemplate` (Canon) | `N : 1` | `Op -> Canon` | Global Template / Scoped Run | Procedural Graph Conformance |
| `REL-OP-001` | `WorkspaceContainsMembership` | `Workspace` (Op) | `WorkspaceMembership` (Op) | `1 : N` | `Parent -> Child` | Strictly Scoped (`workspace_id`) | Actor Permission Boundary |
| `REL-OP-002` | `WorkspaceContainsGuest` | `Workspace` (Op) | `Guest` (Op) | `1 : N` | `Parent -> Child` | Strictly Scoped (`workspace_id`) | Local Participant Identity |
| `REL-OP-003` | `WorkspaceContainsEngagement` | `Workspace` (Op) | `Engagement` (Op) | `1 : N` | `Parent -> Child` | Strictly Scoped (`workspace_id`) | Campaign Study Context |
| `REL-OP-004` | `EngagementScopingHarnessRun` | `Engagement` (Op) | `HarnessRun` (Op) | `1 : N` | `Parent -> Child` | Strictly Scoped (`workspace_id`) | Workflow Execution Envelope |
| `REL-OP-005` | `EvidenceSourceContainsMediaAsset` | `EvidenceSource` (Op) | `MediaAsset` (Op) | `1 : 1` | `Source -> Asset` | Strictly Scoped (`workspace_id`) | Ingestion Package Provenance |
| `REL-OP-006` | `MediaAssetReferencesImmutableBytes`| `MediaAsset` (Op) | `ImmutableMediaEvidence` (Op)| `1 : 1` | `Meta -> Storage`| Strictly Scoped (`workspace_id`) | Physical Recording Tamper-Proof |
| `REL-OP-007` | `EvidenceItemAnchoredBySpan` | `EvidenceItem` (Op) | `EvidenceSpan` (Op) | `1 : N` | `Claim -> Span` | Strictly Scoped (`workspace_id`) | Temporal / Textual Grounding |
| `REL-OP-008` | `SemanticAssessmentLinksEvidence` | `SemanticAssessment` (Op) | `EvidenceItem` (Op) | `N : M` | `Derived -> Evidence`| Strictly Scoped (`workspace_id`) | Factual Assessment Grounding |
| `REL-OP-009` | `ReceiptRecordsOperationAndTransition`| `Receipt` (Op) | `StateTransition` (Op) | `1 : 1` | `Receipt -> Transition`| Strictly Scoped (`workspace_id`)| Atomic Execution Audit Proof |
| `REL-OP-010` | `ReceiptLinksEvidenceLineage` | `Receipt` (Op) | `EvidenceItem` (Op) | `N : M` | `Receipt -> Evidence`| Strictly Scoped (`workspace_id`)| Reality Contact & Anti-Hack |

---

## 5. Non-Claims & Boundary Declarations

1. **Not a PRD or Tech Spec:** This document defines canonical relations and containment laws. It does not authorize software engineering implementation or schema modifications.
2. **No Generic State Engine Claim:** The relations mapped above describe discrete, typed operational state transitions. They do not claim or imply the existence of an unconstrained generic state engine.
3. **No General Agent Orchestrator Claim:** Harness templates and runs represent bounded procedural execution graphs for ratified vertical slices (e.g. Evidence-to-AIR). They do not constitute a general autonomous multi-agent framework.
4. **Anti-Self-Attestation Enforced:** No receipt, assessment, or operational relation may self-attest its own semantic truth without independent evaluator verification and evidence links.
