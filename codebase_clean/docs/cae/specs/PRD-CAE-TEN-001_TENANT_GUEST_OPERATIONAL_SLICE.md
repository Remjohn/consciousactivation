# Product Requirements Document — PRD-CAE-TEN-001: Tenant & Guest Operational Slice

**Document ID:** `PRD-CAE-TEN-001`  
**Phase ID:** `CA-SPEC-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Author:** CAE Governed Execution Agent (Gemini 3.7 Flash High / Antigravity)  
**Governing Mandates:** `07_CA_SPEC_01_TENANT_GUEST_PRD_FR_MANDATE.md`, `00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md`  
**Authority References:** CAE Governance & Specification Bridge Bundle v3; Phase 0 Object Constitution Protocol; Ratified Constitutions `CA-CAN-01A`, `CA-CAN-01B`, `CA-CAN-01C`; `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`; `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`; `CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md`  

---

## 1. Executive Summary & Purpose

The Conscious Activation Engine (CAE) is an internal cognitive and qualitative activation system designed to process participant expressions into structured, grounded semantic insights, archetypal alignments, and actionable activations. 

### 1.1 Problem Statement
Prior to this specification, the brownfield codebase operated across siloed, service-local SQLite databases (`cmf_pipeline`, `conscious_activations_interview_expression`, `api/domain/campaign.py`, `services/air`), with implicit assumption of single-tenant execution, undefined cross-client isolation boundaries, unconstrained operator bypass risks, and ambiguous relationships between global procedural templates and local execution runs. 

Furthermore, development practices exhibited risks of:
1. Conflating execution logging with epistemological or qualitative truth (reward hacking via receipt self-attestation).
2. Treating external URLs as verified media evidence without cryptographic tamper verification.
3. Treating guest identifiers as universal global keys, risking cross-tenant data leaks and unconsented data blending.
4. Conflating canonical procedural definitions (templates) with operational state machines (runs).

### 1.2 Module Purpose
`PRD-CAE-TEN-001` formally establishes the product requirements, operational behavior, boundary rules, and legal invariants for the **First Vertical Operational Slice**:
```text
Workspace (Client Boundary) 
  ──> WorkspaceMembership / OperatorAccess (Authorized Actor Boundary)
    ──> Engagement (Campaign / Project Envelope)
      ──> Guest (Strictly Workspace-Local Participant)
        ──> EvidenceSource & MediaAsset (Verified Evidence Ingestion Boundary)
          ──> HarnessRun (Operational Runbook Execution referencing Canonical HarnessTemplate)
            ──> Receipt Lineage (Cryptographic State & Transition Proof with Reality Contact)
```

This PRD establishes what the operational engine must do and preserve at the semantic layer, without prescribing physical table DDL, API signatures, Python class code, or infrastructure topology.

---

## 2. Canonical Plane vs. Operational Plane Separation

The Conscious Activation Engine operates strictly across two distinct ontological planes:

```text
+====================================================================================================+
|                                           CANONICAL PLANE                                          |
|         (Global Vocabulary, Geometric Direction, Procedural Grammars, Immutable Registries)        |
|                                                                                                    |
|   - SDA Registry (Direction & Geometric Anchors)                                                   |
|   - SFL Registry (Perceptual Modulation & Failure Modes)                                           |
|   - Semantic Primitive Registry (Lexical & Perceptual Semantics: 241/243)                          |
|   - HarnessTemplate (Stateless Procedural Runbook Grammars: CA-STR-001)                           |
|   - StateTransitionContract (Formal State Machine Laws: CA-POL-002)                                |
+====================================================================================================+
                                                 |
                                                 | Read-Only Parameterization / Reference
                                                 v
+====================================================================================================+
|                                          OPERATIONAL PLANE                                         |
|                 (Tenant Isolation, Cryptographic Lineage, Dynamic State, Audit Proof)              |
|                                                                                                    |
|   - OperatorOrganization (Platform Governance & Audit Root: CA-ENT-000)                           |
|     └── OperatorAccessPolicy (Global Governance Policy: CA-POL-001)                                |
|     └── OperatorAccessGrant (Time/Reason-Bounded Diagnostic Grant: CA-REL-002)                     |
|                                                                                                    |
|   - Workspace (Client / Tenant Isolation Root: CA-ENT-001)                                         |
|     ├── WorkspaceMembership (Actor Permission Binding: CA-REL-001)                                 |
|     ├── Guest (Strictly Workspace-Local Participant: CA-ENT-003)                                   |
|     ├── GuestIdentityLink (Exceptional Audited Crosswalk: CA-MAP-001 [DEFERRED RUNTIME])            |
|     └── Engagement (Campaign / Project Envelope: CA-ENT-004)                                      |
|           ├── EvidenceSource (Ingestion Provenance Package: CA-REL-004)                            |
|           ├── MediaAsset (Relational Verification Metadata: CA-ENT-002)                            |
|           ├── ImmutableMediaEvidence (Content-Addressed Payload: CA-EVI-001)                       |
|           ├── HarnessRun (Operational State Machine Instance: CA-EXE-001)                          |
|           ├── Receipt (Atomic Operation Audit Ledger: CA-REC-001)                                  |
|           └── ReceiptEvidenceLink (Traceable Reality Contact Linkage: CA-REL-005)                  |
+====================================================================================================+
```

### 2.1 Separation Invariants
1. **No Tenant Facts on the Canonical Plane:** Canonical objects (`HarnessTemplate`, `SDA`, `SFL`, `Primitive`) MUST contain ZERO tenant identifiers (`workspace_id`), ZERO guest facts, ZERO private storage paths, and ZERO runtime state counters.
2. **Read-Only Pinned Reference:** Operational runs reference canonical templates via immutable identifier and pinned semantic version (`template_id`, `template_version`).
3. **No Operational Contamination:** Operational executions cannot alter, fork, or patch canonical templates in-flight.

---

## 3. Core Operational Objects & Role Definitions

The first-slice operational module is composed of the following ratified canonical objects:

### 3.1 Tenancy & Actor Governance
- **`OperatorOrganization` (`CA-ENT-000`, `Entity`):** Represents the administrative authority governing the CAE platform. It manages platform operators and audit policies. It does NOT own client operational facts.
- **`Workspace` (`CA-ENT-001`, `Entity`):** The primary client/tenant isolation root. Every client-specific datum in the operational plane MUST trace its provenance to exactly one `workspace_id`.
- **`WorkspaceMembership` (`CA-REL-001`, `Relation`):** Binds an authenticated human or service actor to a specific role within a Workspace. Cross-workspace memberships are distinct, independently revocable records.
- **`OperatorAccessPolicy` (`CA-POL-001`, `Policy / Contract`):** Global governance contract defining the rules, allowed scopes, mandatory justification, and maximum durations under which internal CAE operators may access client workspaces for support or diagnostics.
- **`OperatorAccessGrant` (`CA-REL-002`, `Relation`):** An ephemeral, time-bounded, audited authorization record granting a specific operator diagnostic access to a specific workspace. Standing global bypasses are strictly prohibited.

### 3.2 Engagement & Guest Domain
- **`Engagement` (`CA-ENT-004`, `Entity`):** A bounded project, campaign, or research study envelope within a Workspace. Groups execution runs and participant interactions under a unified operational lifecycle (`PLANNED` $\rightarrow$ `ACTIVE` $\rightarrow$ `PAUSED` $\rightarrow$ `COMPLETED` $\rightarrow$ `ARCHIVED`).
- **`Guest` (`CA-ENT-003`, `Entity`):** A participant whose expressions and evidence are captured within a specific Workspace. Guest identity is strictly local to its parent Workspace.
- **`GuestIdentityLink` (`CA-MAP-001`, `Crosswalk / Mapping Object`):** An exceptional, dual-consented, audit-receipted crosswalk linking guest profiles across distinct workspaces for enterprise research. Automatic cross-workspace identity merging is strictly prohibited. Runtime execution is formally `DEFERRED`.

### 3.3 Evidence & Media Ingestion Domain
- **`EvidenceSource` (`CA-REL-004`, `Relation`):** External provenance envelope linking raw external interview exports or package digests to internal CAE assets.
- **`MediaAsset` (`CA-ENT-002`, `Entity`):** The relational entity representing an audio/visual recording. Holds lifecycle state (`REGISTERED`, `STAGED`, `VERIFIED`, `QUARANTINED`, `REVOKED`), SHA-256 digest, mime type, and byte count. Raw media bytes MUST NOT be stored in relational database rows.
- **`ImmutableMediaEvidence` (`CA-EVI-001`, `Immutable Evidence`):** The physical, content-addressed byte payload stored in private object storage, partitioned strictly under tenant prefixes (`storage://cae-media/{workspace_id}/{asset_id}/...`).

### 3.4 Procedural Execution & Cryptographic Receipt Domain
- **`HarnessTemplate` (`CA-STR-001`, `Canonical Structural Grammar`):** A stateless, globally versioned procedural definition specifying step sequences, state transitions, required inputs, validation rules, before-transfer checks, and typed failure routes.
- **`HarnessRun` (`CA-EXE-001`, `Execution Packet`):** An operational state machine instance scoped to a specific Workspace and Engagement. Advances through discrete steps by executing authorized typed semantic operations.
- **`Receipt` (`CA-REC-001`, `Receipt / Evaluation Record`):** An immutable, append-only cryptographic ledger entry recording the successful execution of an authorized semantic operation and its atomic state transition.
- **`ReceiptEvidenceLink` (`CA-REL-005`, `Relation`):** An immutable relational bridge linking execution receipts to the specific evidence items observed, extracted, or produced during execution, establishing verifiable reality contact.

---

## 4. The Three Independent Authority Axes

To eliminate ambiguity across specifications and implementation, every operational and canonical object maintains three distinct authority axes:

```text
1. Canonical Definition Source:
   The authoritative reviewed source artifact, repository file, or versioned snapshot governing the object's definition and legal rules.

2. Canonical Runtime Representation:
   The verified runtime projection (e.g. PostgreSQL schema, private object store bucket) utilized by typed semantic operations.

3. Change / Promotion Authority:
   The designated governance body, operator role, or automated state engine authorized to modify definitions or promote operational state.
```

Collapsing or conflating these axes (e.g. treating an in-place database edit as a definition change) is strictly prohibited.

---

## 5. End-to-End First-Slice Operational Lifecycle

The standard operational workflow proceeds through nine legal phases:

```text
+----------------------------------------------------------------------------------------------------+
| 1. Workspace Provisioning: Operator creates Workspace (CA-ENT-001) under client legal entity.       |
|    - Emits: WorkspaceCreatedEvent, OperationReceipt.                                               |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 2. Actor Authorization: Admin issues WorkspaceMembership (CA-REL-001) to Operators/Clients.        |
|    - Optional: Ephemeral OperatorAccessGrant (CA-REL-002) issued for diagnostic support.          |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 3. Engagement Initialization: Client creates Engagement (CA-ENT-004) in PLANNED state.            |
|    - Transitions: PLANNED -> ACTIVE via authorized semantic operation.                            |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 4. Guest Registration: Participant profile registered as workspace-local Guest (CA-ENT-003).        |
|    - Anti-Merge Invariant: No automatic link to guest records in other workspaces.                 |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 5. Media Ingestion & Verification: Source package admitted via EvidenceSource (CA-REL-004).        |
|    - Raw bytes written to private storage (CA-EVI-001); MediaAsset (CA-ENT-002) verifies SHA-256.  |
|    - Transition: STAGED -> VERIFIED. (Fails to QUARANTINED if hash mismatches).                    |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 6. Harness Run Initialization: WorkspaceRunner instantiates HarnessRun (CA-EXE-001) referencing    |
|    pinned canonical HarnessTemplate (CA-STR-001). Initial state: INITIALIZED.                     |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 7. Step Execution & Evidence Capture: HarnessRun executes step operations (e.g. capture evidence).  |
|    - Typed semantic operation captures spans from verified media asset.                            |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 8. Atomic Transition & Receipt Commit: State engine commits state change, generates Receipt         |
|    (CA-REC-001), and binds ReceiptEvidenceLink (CA-REL-005) in a single atomic transaction.        |
+----------------------------------------------------------------------------------------------------+
                                                 |
                                                 v
+----------------------------------------------------------------------------------------------------+
| 9. Run Finalization & Engagement Closure: HarnessRun transitions to COMPLETED. Output artifacts    |
|    anchored to evidence lineage. Engagement moves to COMPLETED / ARCHIVED.                         |
+----------------------------------------------------------------------------------------------------+
```

---

## 6. Prohibitions, Deferrals, and Hard Boundaries

### 6.1 Strict Prohibitions
1. **No Universal Guest Keys:** `guest_id` SHALL NOT be used as a global partition or tenancy key across workspaces.
2. **No Unaudited Operator Bypass:** Internal operators SHALL NOT access workspace data without an active, unexpired, reason-bounded `OperatorAccessGrant`.
3. **No Database Raw Media Payloads:** Audio, video, and large binary blobs SHALL NOT be stored in relational database columns.
4. **No Receipt Self-Attestation:** The generation or existence of a `Receipt` SHALL NOT be interpreted as proof of semantic truth, human validity, or aesthetic quality without an independent evaluator verification record.
5. **No Cross-Workspace Linkage:** Receipts, evidence items, media assets, runs, and guest profiles SHALL NOT be linked across workspace boundaries.

### 6.2 Formal Deferments
1. **Cross-Workspace Guest Research Crosswalk:** `GuestIdentityLink` runtime operations are formally `DEFERRED` until enterprise cross-workspace research requirements are prioritized.
2. **Phase-5 Dynamic Replanning & Brief Compiler:** Dynamic replanning (`FR-P05-08`) and interview brief compilation (`FR-P05-01`) are `DEFERRED`.
3. **Phase-6 Candidate Generation & Coalition Formation:** Candidate synthesis (`FR-P06-03`) and coalition validation (`FR-P06-08`) are `DEFERRED`.
4. **Phase-7 SFL Stack & SemanticProgram Compiler:** Archetype selection (`FR-P07-03`) and SemanticProgram compilation (`FR-P07-09`) are `DEFERRED`.
5. **General Autonomous Agent Orchestrator:** Multi-agent runtime coordination is `DEFERRED` / `NOT_IN_SCOPE`.

### 6.3 Quarantined Defects
1. **SFL Registry Missing Families:** 5 failure assets citing missing families `005, 006, 007, 009, 012` remain `QUARANTINED` and blocked from runtime resolution.
2. **Primitive Duplicate Key:** Duplicate primitive ID `EXP-TRG-001` remains `QUARANTINED` and rejected by resolvers.

---

## 7. Brownfield Integration & Adaptation Posture

```text
+-----------------------+----------------------------------------------------------------------------+
| Component             | Brownfield Adaptation Posture                                              |
+-----------------------+----------------------------------------------------------------------------+
| api/main.py           | ADAPT: Add workspace context middleware; retain SQLite during phase.       |
| api/domain/campaign.py| ADAPT: Reconcile campaign state model with Engagement (CA-ENT-004).        |
| packages/ca_runtime   | EXTEND: Integrate workspace-scoped idempotency and immutable receipt logic.|
| services/pipeline     | RETAIN: Maintain legacy run service for development; defer cutover.        |
| services/interview    | ADAPT: Wrap read-only interview export in EvidenceSource bridge (WP-09).   |
| services/air          | ADAPT: Interface with staging evidence capture; no direct DB mutation.     |
| storage/              | NEW: Provision private S3/Supabase storage buckets for media evidence.     |
+-----------------------+----------------------------------------------------------------------------+
```

---

## 8. Downstream Dependencies and Next Gates

1. **Gate to CA-STATE-01:** Approval of `PRD-CAE-TEN-001` and its 15 Functional Requirements authorizes the authoring of per-aggregate state authority and migration contracts in `CA-STATE-01`.
2. **Gate to CA-TS-01:** Physical schemas, DDL scripts, RLS policies, endpoint signatures, and background worker topologies SHALL NOT be authored until `CA-STATE-01` contracts are ratified and `CA-TS-01` is formally authorized.
