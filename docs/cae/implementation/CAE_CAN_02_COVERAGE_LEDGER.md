# CAE Coverage Ledger — Phase 24 / CA-CAN-02

**Document ID:** `CAE_CAN_02_COVERAGE_LEDGER`  
**Phase ID:** `CA-CAN-02`  
**Title:** Definitive Object Coverage Ledger & Constitution Gap Analysis  
**Date:** `2026-08-26`  
**Status:** `AUTHORED — PENDING OPERATOR READING PAUSE`  
**Governing Mandate:** `docs/cae/gemini_execution/24_CA_CAN_02_CONSTITUTION_SET_COMPLETION_MANDATE.md`  
**Authoritative References:**  
- `docs/cae/implementation/CAE_SCOPE_AND_AUTHORITY_MATRIX.md` (CA-MAP-01)  
- `docs/cae/state/CAE_AGGREGATE_AUTHORITY_MATRIX.md` (CA-STATE-01)  
- `docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md` (CA-TS-01)  
- `docs/cae/specs/PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` (CA-SPEC-01)  
- `docs/cae/implementation/CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET.md` (CA-UPTL-01 / U1 Ratified Dispositions)  

---

## 1. Executive Framework & Classification Protocol

In accordance with Mandate §3 (C1) and Operator Ratification Conditions:
1. Every scoped object across the CAE architecture is accounted for. Silence is prohibited.
2. Every object on the authoring gap list (`REQUIRES_CONSTITUTION`) cites the exact matrix row, contract, or specification section establishing its boundary. No object is invented.
3. Every unconstituted object is classified into exactly one of three categories:
   - **`COVERED_BY_EXISTING`**: Object is governed by one of the 15 ratified constitutions authored in `CA-CAN-01A`, `CA-CAN-01B`, or `CA-CAN-01C`.
   - **`REQUIRES_CONSTITUTION`**: Scoped object in active architecture requiring an authoritative 26-dimension constitution under `CA-CAN-02`.
   - **`DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED`**: Architectural concept, storage projection, operational protocol, or Phase-6/7 intelligence artifact whose constitutional authoring is formally deferred to a downstream mandate.

---

## 2. Definitive Object Coverage Ledger

| Object Identifier & Name | Candidate Primary Class | Ontological Plane | Source Matrix / Contract Traceability Citation | Governing / Target Constitution | Classification | Rationale & Scope Boundary |
|---|---|---|---|---|---|---|
| **`OperatorOrganization`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:30`, `CA-STATE-01:62`, `MC-CAE-OPR-001` | `CA-CAN-01A_OPERATOR_ORGANIZATION.yaml` | `COVERED_BY_EXISTING` | Root platform administration entity. |
| **`Workspace`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:31`, `CA-STATE-01:60`, `MC-CAE-WS-001` | `CA-CAN-01A_WORKSPACE.yaml` | `COVERED_BY_EXISTING` | Sole customer tenant boundary. |
| **`WorkspaceMembership`** | Relation | `OPERATIONAL_PLANE` | `CA-MAP-01:32`, `CA-STATE-01:61`, `MC-CAE-WS-001` | `CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml` | `COVERED_BY_EXISTING` | Multi-tenant user binding relation. |
| **`OperatorAccessPolicy`** | Policy / Contract | `OPERATIONAL_PLANE` | `CA-MAP-01:33`, `CA-STATE-01:63`, `MC-CAE-OPR-001` | `CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml` | `COVERED_BY_EXISTING` | Global operator governance policies. |
| **`OperatorAccessGrant`** | Relation | `OPERATIONAL_PLANE` | `CA-MAP-01:34`, `CA-STATE-01:64`, `MC-CAE-OPR-001` | `CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml` | `COVERED_BY_EXISTING` | Ephemeral, reason-bounded operator access grant. |
| **`Engagement`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:35`, `CA-STATE-01:65`, `MC-CAE-ENG-001` | `CA-CAN-01A_ENGAGEMENT.yaml` | `COVERED_BY_EXISTING` | Workspace campaign/project container. |
| **`Guest`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:36`, `CA-STATE-01:66`, `MC-CAE-GST-001` | `CA-CAN-01B_GUEST.yaml` | `COVERED_BY_EXISTING` | Workspace-local participant entity. |
| **`GuestIdentityLink`** | Crosswalk / Mapping | `OPERATIONAL_PLANE` | `CA-MAP-01:37`, `CA-STATE-01:67`, `MC-CAE-GST-001` | `CA-CAN-01B_GUEST_IDENTITY_LINK.yaml` | `COVERED_BY_EXISTING` | Dual-consented cross-workspace mapping. |
| **`MediaAsset`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:38`, `CA-STATE-01:68`, `MC-CAE-MED-001` | `CA-CAN-01B_MEDIA_ASSET.yaml` | `COVERED_BY_EXISTING` | Media lifecycle and metadata entity. |
| **`Immutable Media Evidence Bytes`** | Immutable Evidence | `OPERATIONAL_PLANE` | `CA-MAP-01:39`, `CA-STATE-01:69`, `MC-CAE-MED-001` | `CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml` | `COVERED_BY_EXISTING` | Content-addressed storage payload. |
| **`EvidenceSource` / `SourcePackage`** | Relation / Ingestion Envelope | `OPERATIONAL_PLANE` | `CA-MAP-01:47`, `CA-STATE-01:70`, `MC-CAE-MED-001` | `CA-CAN-01B_EVIDENCE_SOURCE.yaml` | `COVERED_BY_EXISTING` | Bridges raw media assets to evidence ingestion. |
| **`HarnessTemplate`** | Canonical Structural Grammar | `CANONICAL_PLANE` | `CA-MAP-01:40`, `CA-STATE-01:73`, `MC-CAE-RUN-001` | `CA-CAN-01C_HARNESS_TEMPLATE.yaml` | `COVERED_BY_EXISTING` | Versioned pipeline execution runbook specification. |
| **`HarnessRun`** | Execution Packet | `OPERATIONAL_PLANE` | `CA-MAP-01:41`, `CA-STATE-01:74`, `MC-CAE-RUN-001` | `CA-CAN-01C_HARNESS_RUN.yaml` | `COVERED_BY_EXISTING` | Workspace-scoped pipeline execution state. |
| **`Receipt`** | Receipt / Evaluation Record | `OPERATIONAL_PLANE` | `CA-MAP-01:42`, `CA-STATE-01:75`, `MC-CAE-REC-001` | `CA-CAN-01C_RECEIPT.yaml` | `COVERED_BY_EXISTING` | Atomic operational execution receipt ledger. |
| **`ReceiptEvidenceLink`** | Relation | `OPERATIONAL_PLANE` | `CA-MAP-01:43`, `CA-STATE-01:76`, `MC-CAE-REC-001` | `CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml` | `COVERED_BY_EXISTING` | Causal lineage anchor from receipt to evidence. |
| **`ExecutionReceipt`** | Receipt / Evaluation Record | `OPERATIONAL_PLANE` | `CA-MAP-01:43`, `CA-STATE-01:75`, `sql/0008` | `CA-CAN-01C_RECEIPT.yaml` + `CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml` | `COVERED_BY_EXISTING` | Evaluated specialization of `Receipt` carrying taste/reward-hack flags. |
| **`InterviewSession`** | Entity | `OPERATIONAL_PLANE` | `CA-MAP-01:48`, `TS-CAE-TEN-001` §3.4 | `CA-CAN-02_INTERVIEW_SESSION.yaml` | `REQUIRES_CONSTITUTION` | Stateful interview lifecycle aggregate. |
| **`InterviewTurn`** | Conversational Turn Record / Event | `OPERATIONAL_PLANE` | `CA-MAP-01:49`, `TS-CAE-TEN-001` §3.4 | `CA-CAN-02_INTERVIEW_TURN.yaml` | `REQUIRES_CONSTITUTION` | Append-only sequential conversational turn. |
| **`EvidenceItem`** | Immutable Evidence | `OPERATIONAL_PLANE` | `CA-MAP-01:50`, `CA-STATE-01:71`, `TS-CAE-TEN-001` §3.5 | `CA-CAN-02_EVIDENCE_ITEM.yaml` | `REQUIRES_CONSTITUTION` | Discrete extracted evidentiary atom. |
| **`EvidenceSpan`** | Relation | `OPERATIONAL_PLANE` | `CA-MAP-01:51`, `CA-STATE-01:71`, `TS-CAE-TEN-001` §3.5 | `CA-CAN-02_EVIDENCE_SPAN.yaml` | `REQUIRES_CONSTITUTION` | Spatial/temporal/character offset anchor to media. |
| **`EvidenceAuthentication`** | Receipt / Evaluation Record | `OPERATIONAL_PLANE` | `CA-MAP-01:52`, `CA-STATE-01:72`, `TS-CAE-TEN-001` §3.5 | `CA-CAN-02_EVIDENCE_AUTHENTICATION.yaml` | `REQUIRES_CONSTITUTION` | Attributable, independent evaluator attestation. |
| **`SemanticAssessment`** | Derived Semantic Artifact | `OPERATIONAL_PLANE` | `CA-MAP-01:53`, `TS-CAE-TEN-001` §3.5 | `CA-CAN-02_SEMANTIC_ASSESSMENT.yaml` | `REQUIRES_CONSTITUTION` | Versioned qualitative assessment derived from evidence. |
| **`AssessmentEvidenceLink`** | Relation | `OPERATIONAL_PLANE` | `CA-MAP-01:54`, `TS-CAE-TEN-001` §3.5 | `CA-CAN-02_ASSESSMENT_EVIDENCE_LINK.yaml` | `REQUIRES_CONSTITUTION` | Relational binding linking assessment to supporting spans. |
| **`StateAggregate`** | State | `OPERATIONAL_PLANE` | `CA-MAP-01:55`, `CA-STATE-01:77`, `14_CAE_STATE...` | `CA-CAN-02_STATE_AGGREGATE.yaml` | `REQUIRES_CONSTITUTION` | Optimistic concurrency control root for runtime aggregates. |
| **`StateTransitionContract`** | Policy / Contract | `CANONICAL_PLANE` | `CA-MAP-01:56`, `TS-CAE-TEN-001` §3.7 | `CA-CAN-02_STATE_TRANSITION_CONTRACT.yaml` | `REQUIRES_CONSTITUTION` | Canonical declaration of legal state transitions. |
| **`StateTransition`** | Event | `OPERATIONAL_PLANE` | `CA-MAP-01:57`, `CA-STATE-01:77`, `15_CAE_POSTGRES...` | `CA-CAN-02_STATE_TRANSITION.yaml` | `REQUIRES_CONSTITUTION` | Immutable atomic transition event record. |
| **`Command`** | Execution Packet | `OPERATIONAL_PLANE` | `CA-MAP-01:58`, `CA-STATE-01:75`, `16_CAE_SEMANTIC...` | `CA-CAN-02_COMMAND.yaml` | `REQUIRES_CONSTITUTION` | Idempotent client/agent intent packet. |
| **`Event`** | Event | `OPERATIONAL_PLANE` | `CA-MAP-01:59`, `CA-STATE-01:77`, `15_CAE_POSTGRES...` | `CA-CAN-02_EVENT.yaml` | `REQUIRES_CONSTITUTION` | Runtime domain event-sourcing occurrence (`cae.event`). |
| **`SDARegistry`** | Canonical Ontology | `CANONICAL_PLANE` | `CA-MAP-01:44`, `CA-STATE-01:78`, `CA-UPTL-01/U1` | `CA-CAN-02_SDA_REGISTRY.yaml` | `REQUIRES_CONSTITUTION` | Pinned SDA snapshot with manifest inheritance. |
| **`SFLRegistry`** | Experience / Perceptual Function | `CANONICAL_PLANE` | `CA-MAP-01:45`, `CA-STATE-01:79`, `CA-UPTL-01/U1` | `CA-CAN-02_SFL_REGISTRY.yaml` | `REQUIRES_CONSTITUTION` | Pinned SFL snapshot with Route B quarantine invariants. |
| **`PrimitiveRegistry`** | Operator / Primitive | `CANONICAL_PLANE` | `CA-MAP-01:46`, `CA-STATE-01:80`, `CA-UPTL-01/U1` | `CA-CAN-02_PRIMITIVE_REGISTRY.yaml` | `REQUIRES_CONSTITUTION` | Pinned Primitive snapshot with `EXP-TRG-010` disambiguation. |

---

## 3. Explicit Classifications of Objects Not on the Authoring List

In strict conformance with Operator Condition 2, the following architectural concepts and infrastructure objects are accounted for:

| Architectural Concept / Object | Category / Domain | Current Governance Location | Target Status | Classification | Detailed Rationale & Deferment Boundary |
|---|---|---|---|---|---|
| **`semantic_operation`** | Operational API Protocol | `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md`, `CAE_SCOPE_AND_AUTHORITY_MATRIX.md` | Protocol Specification | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | An abstract protocol template rather than an individual domain entity. Each concrete semantic operation (`verify_media_asset`, `capture_evidence`, `authenticate_evidence`, `validate_semantic_assessment`) is constituted under its respective aggregate. Global protocol constitution deferred. |
| **`registry_snapshot`** | Infrastructure Storage Projection | `0005_cae_registry_authority.sql`, `packages/ca_runtime/src/ca_runtime/registry.py` | Storage Table | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Relational projection table (`cae.registry_snapshot`) that stores pinned archive metadata for SDA, SFL, and Primitives. Governed by the canonical registry constitutions (`CA-CAN-02_SDA/SFL/PRIMITIVE_REGISTRY.yaml`). Dedicated infrastructure constitution deferred. |
| **`registry_item`** | Infrastructure Leaf Node | `packages/ca_runtime/src/ca_runtime/registry.py` | Model Record | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Generic container class for individual registry YAML leaf elements. Governed by specific registry constitutions (`CA-CAN-02_SDA/SFL/PRIMITIVE_REGISTRY.yaml`). Standalone leaf constitution deferred. |
| **`registry_reference`** | Relational Cross-Pointer | `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md` | Lineage Relation | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Cross-registry foreign-key link (e.g., SFL to SDA, Primitive to Archetype). Governed by the canonical relation map and registry schemas. Standalone constitution deferred. |
| **`registry_disposition`** | Custodian Governance Record | `CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET.md` | Custodian Ledger | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Audit artifact recording operator rulings on defect routes (Route A/B). Governed by Phase 23 U1 packet. Standalone runtime constitution deferred. |
| **`Candidate` (Archetype Candidate)** | Upstream AIR Hypothesis | `services/air/src/cmf_activative_intelligence/services/archetype_service.py` | Intelligence Generator | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Phase 6 AIR candidate generation artifact (`generate_archetype_candidates`). Requires Phase 6 AIR Production mandate authorization before constitution. |
| **`Coalition` (Primitive Coalition)** | Upstream AIR Synthesis | `services/air/src/cmf_activative_intelligence/services/coalition_service.py` | Intelligence Generator | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Phase 6 AIR coalition formation artifact (`generate_coalition`). Governed by Phase 6 AIR Production mandate. |
| **`Edge` (Edging Candidate / Tension Resolution)** | Upstream AIR Perceptual Engine | `services/air/src/cmf_activative_intelligence/services/edging_service.py` | Intelligence Generator | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Phase 6 AIR psychological edging candidate (`generate_edging_candidate`). Governed by Phase 6 AIR Production mandate. |
| **`SemanticProgram` (Compiled Activation Program)** | Compiled Activation Program | `services/air/src/cmf_activative_intelligence/services/archetype_service.py:generate_program` | Compilation Output | `DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` | Phase 7 end-to-end compiled activation program object. Authoring constitution deferred to Phase 7 Activation Program mandate. |

---

## 4. Summary & Gap Reconciliation

- **Total Objects Accounted For:** 40 objects and architectural concepts.
- **`COVERED_BY_EXISTING`:** 16 objects (15 ratified YAML files in `docs/cae/constitutions/`).
- **`REQUIRES_CONSTITUTION`:** 15 objects (to be authored in `docs/cae/constitutions/CA-CAN-02_*.yaml`).
- **`DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED`:** 9 concepts (cleanly classified and deferred with rationale).
- **Invented Objects:** **0** (All 15 target constitutions derive directly from verified matrix/contract rows).
- **Contradictions Identified:** **0** unresolved gaps in the matrix crosswalk.
