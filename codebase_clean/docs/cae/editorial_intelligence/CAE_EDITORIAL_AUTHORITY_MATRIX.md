# CAE Editorial Intelligence Authority Matrix

**Document ID:** `CAE-AUT-ED-001`  
**Governing Mandate:** `CAE-M00`  
**Status:** `CANONICAL SPECIFICATION`  
**Version:** `1.0.0`  
**Prepared:** 2026-08-28  

---

## 1. The Three Axes of Authority

In accordance with the CAE Object Constitution and Mandate Authoring Protocol, authority over editorial intelligence is separated across three orthogonal axes:

1. **Definition Authority:** The artifact, document, or repository commit that establishes what an object or relation means ontologically.
2. **Runtime Authority:** The active, verified software component and database schema responsible for state validation, transactions, and execution.
3. **Change / Promotion Authority:** The explicit role, governance process, or operator gate authorized to alter definitions or advance lifecycle state.

---

## 2. Comprehensive Authority Matrix

| Object Name | Definition Authority | Runtime Authority | Change / Promotion Authority |
| :--- | :--- | :--- | :--- |
| `ResearchSignal` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_discovery` / Ingestion Engine | Ingestion Ingestion Pipeline / TTL Expiry |
| `AudienceState` | `docs/cae/constitutions/CA-CAN-02_STATE_AGGREGATE.yaml` | `ca_relational` / PostgreSQL `cae_audience_state` | Lead Strategist / Operator Update |
| `GuestState` | `docs/cae/constitutions/CA-CAN-01B_GUEST.yaml` | `ca_relational` / PostgreSQL `cae_guest_state` | Operator / Verified Onboarding Dossier |
| `CollisionHypothesis` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_collision` / PostgreSQL `cae_collision_hypotheses` | Collision Engine Evaluator Gating |
| `InterviewBrief` | `docs/cae/specs/current/SPEC-BRF-001.md` | `services/interview-composer` / PostgreSQL `cae_briefs` | Lead Interviewer / Operator Seal |
| `InterviewResponse` | `docs/cae/constitutions/CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml` | Media Storage API / S3 Object Store + PostgreSQL | WORM Ingestion (Immutable once hashed) |
| `EvidenceSegment` | `docs/cae/constitutions/CA-CAN-02_EVIDENCE_SPAN.yaml` | `ca_evidence_engine` / PostgreSQL `cae_evidence_segments` | Segmentation Service (Immutable once created) |
| `SemanticAnnotation` | `docs/cae/constitutions/CA-CAN-02_SEMANTIC_ASSESSMENT.yaml` | `ca_assessment_engine` / PostgreSQL `cae_annotations` | Model Evaluator / Operator Re-annotation |
| `ContentCandidate` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_editorial_engine` / PostgreSQL `cae_candidates` | Candidate Formation Engine |
| `CandidateCluster` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_editorial_engine` / PostgreSQL `cae_clusters` | Clustering Service Evaluator |
| `EditorialStoryboard` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_editorial_console` / PostgreSQL `cae_storyboards` | **Operator Signature Sole Authority (`CAE-M09`)** |
| `MediaAsset` | `docs/cae/constitutions/CA-CAN-01B_MEDIA_ASSET.yaml` | `services/pipeline` / S3 Blob Storage + PostgreSQL | Storage Service Ingestion |
| `AssetAnnotation` | `docs/cae/editorial_intelligence/CAE_EDITORIAL_OBJECT_REGISTER.md` | `ca_asset_registry` / PostgreSQL `cae_asset_annotations` | Operator / Selected Asset Annotator |
| `InsertRole` | `docs/cae/constitutions/CA-CAN-02_PRIMITIVE_REGISTRY.yaml` | Core Platform Enums (`InsertRoleEnum`) | CAE Governance RFC / Protocol Amendment |
| `SemanticProgram` | `docs/cae/specs/current/SPEC-CMP-002.md` | `services/pipeline` / PostgreSQL `cae_semantic_programs` | Approved Storyboard Compiler |
| `CompositionIR` | `services/pipeline/src/cmf_pipeline/composition/` | `cmf_pipeline.composition` / Memory & Artifact Storage | Composition Generator Engine |
| `VideoEditProgram` | `services/pipeline/src/cmf_pipeline/media/` | `cmf_pipeline.render` / Temporary Execution Workspace | Render Engine Dispatcher |
| `Outcome` | `docs/cae/constitutions/CA-CAN-01C_RECEIPT.yaml` | `ca_analytics` / PostgreSQL `cae_outcomes` | Platform API Ingestion / Verified Webhook |

---

## 3. Constitutional Safeguards on Authority

1. **No Inferred Authority:** No component may assume definition or change authority over an object merely because it performs read or transform operations upon it.
2. **Operator Exclusivity over `EditorialStoryboard`:** The promotion of a `ContentCandidate` to an `EditorialStoryboard` cannot be delegated to an autonomous LLM agent. It requires an authenticated `CA-CAN-01A_OPERATOR_ACCESS_GRANT` signature.
3. **Immutability of Evidence:** `InterviewResponse` and `MediaAsset` byte records reside under WORM policy; neither operator nor autonomous agent may alter their stored bytes.
