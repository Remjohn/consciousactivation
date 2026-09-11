# CAE CA-MAP-01 Source Crosswalk

**Status:** `MODEL_MAPPED_PENDING_OPERATOR_REVIEW`  
**Phase ID:** `CA-MAP-01`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/02_CA_MAP_01_SCOPE_AUTHORITY_MAPPING_MANDATE.md`  
**Authority Reference:** Multi-Tenant Authority and Canonicalization Plan §3.2, §5; WP-10A Acceptance Report  

---

## 1. Purpose & Crosswalk Principles

This crosswalk establishes direct traceability between every mapped object in the CA-MAP-01 scope and actual brownfield repositories, schemas, migrations, runtime services, and documentation.

Each source relationship is classified according to the standard brownfield taxonomy:
- `NEW`: Object required by target multi-tenant architecture but currently absent in brownfield codebase.
- `EXTEND`: Existing brownfield service or schema to be expanded with multi-tenant workspace keys or contracts.
- `ADAPT`: Brownfield component wrapped via a typed bridge or adapter without direct SQLite schema mutation.
- `RETAIN`: Brownfield asset preserved in its original immutable form (e.g. source YAML/ZIP archives).
- `DEFER`: Mature brownfield service or complex aggregate postponed to a subsequent implementation phase.
- `QUARANTINE`: Defective or ambiguous inherited asset isolated from runtime resolution until upstream repair.
- `CONFLICTING`: Competing brownfield implementations requiring architectural split or operator arbitration.

---

## 2. Comprehensive Object-to-Source Crosswalk Matrix

| Object Name | Source Classification | Brownfield File / Service Path | Staging SQL / Schema Reference | Target Disposition & Traceability Notes |
|---|---|---|---|---|
| `OperatorOrganization` | `NEW` | `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:65` | Future schema `cae.operator_organization` | To be constituted in CA-CAN-01A. Provides administrative envelope for platform security. |
| `Workspace` | `EXTEND` | `api/domain/campaign.py:79-80` (`workspace_id` validation) | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:14-18` (`cae.workspace`) | Proven in WP-02a/WP-02b staging. Serves as root RLS isolation key across all operational tables. |
| `WorkspaceMembership` | `ADAPT` | `services/air/src/cmf_activative_intelligence/domain.py` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:28-36` (`cae.actor`), `0002_cae_workspace_rls.sql:13-26` | Adapts local actor concepts into workspace-scoped principal with external subject claim binding. |
| `OperatorAccessPolicy` | `NEW` | `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:68` | Future schema `cae.operator_access_policy` | To be constituted in CA-CAN-01A. Replaces ad-hoc administrative access with explicit policy rules. |
| `OperatorAccessGrant` | `NEW` | `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:189-196` | Future schema `cae.operator_access_grant` | To be constituted in CA-CAN-01A. Time/reason-bounded access grant with immutable audit receipt. |
| `Engagement` | `EXTEND` | `api/domain/campaign.py:18-27` (`CampaignState`), `api/services/campaign_repository.py` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:20-26` (`cae.project`) | Extends existing campaign state machine into workspace-scoped `cae.engagement` / `cae.project`. |
| `Guest` | `ADAPT` | `services/interview/src/conscious_activations_interview_expression/` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:74` (`guest_actor_id`) | Reconciled as workspace-local entity. Prohibits global identity merges across tenants. |
| `GuestIdentityLink` | `NEW` / `DEFER` | `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:71, 407` | Future schema `cae.guest_identity_link` | Defer implementation until multi-tenant longitudinal research is scheduled. Requires dual consent. |
| `MediaAsset` | `EXTEND` | Builder ADR-003; `services/builder/` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:38-57` (`cae.media_asset`) | Content-addressed metadata table tracking SHA-256, byte size, lifecycle state, and storage URI. |
| `Immutable Media Evidence Bytes` | `RETAIN` | Private Supabase Storage bucket `cae-media` | Verified in `scripts/cae/verify_private_storage.py` and `verify_wp08_reality_contact.py` | Raw media bytes stored in private object storage (`storage://cae-media/{workspace_id}/{path}`). |
| `HarnessTemplate` | `RETAIN` | `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml`; `docs/cae/skills/` | Future snapshot table `cae.harness_template` | Canonical procedural doctrine versioned in Git and imported as immutable snapshot. |
| `HarnessRun` | `ADAPT` | `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` | `services/pipeline/src/cmf_pipeline/migrations/0001_pipeline_core.sql` | Adapts Pipeline SQLite runs into workspace-scoped operational execution aggregates. |
| `Receipt` | `EXTEND` | `packages/ca_runtime/src/ca_runtime/database.py:44`; `packages/ca_runtime/src/ca_runtime/migrations/0001_foundation.sql:44-52` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:233-240` (`cae.receipt`) | Extends ca_runtime SQLite receipt pattern into canonical PostgreSQL immutable receipt ledger. |
| `ExecutionReceipt` | `EXTEND` | `docs/cae/implementation/CAE_WP07_EXECUTION_RECEIPTS_EVIDENCE_LINEAGE.md` | `docs/cae/implementation/sql/0008_cae_execution_receipt_lineage.sql:5-33` | Adds evaluation fidelity context, anti-centroid results, and evidence links (`cae.receipt_evidence_link`). |
| `SDA Registry` | `RETAIN` | Inherited archive `sda.zip` (13 YAML files) | `docs/cae/implementation/sql/0005_cae_registry_authority.sql:13-54` (`cae.registry_snapshot`) | 13 records imported cleanly in WP-04. Pinned read-only snapshot via `RegistryResolver`. |
| `SFL Registry` | `QUARANTINE` | Inherited archive `sfl.zip` (28 YAML files) | `docs/cae/implementation/sql/0005_cae_registry_authority.sql:70-82` (`cae.registry_integrity_issue`) | 23 valid records imported; 5 failure assets referencing missing families (`005, 006, 007, 009, 012`) quarantined. |
| `Primitive Registry` | `QUARANTINE` | `services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv` | `docs/cae/implementation/sql/0005_cae_registry_authority.sql:70-82` (`cae.registry_integrity_issue`) | 241 records imported cleanly; 2 duplicate files for `EXP-TRG-001` quarantined from runtime resolution. |
| `SourcePackage` | `ADAPT` | `services/interview/src/conscious_activations_interview_expression/` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:59-68`, `0009_cae_interview_source_bridge_operation.sql` | Adapts Interview Expression source media/transcripts via typed bridge operation STC-BRIDGE-000. |
| `InterviewSession` | `ADAPT` | `services/interview/src/conscious_activations_interview_expression/migrations/0001_interview_expression.sql:47-54` (`ie_session_snapshots`) | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:70-79` (`cae.interview_session`) | Bridges SQLite interview session snapshots into relational schema scoped to `workspace_id` and `guest_actor_id`. |
| `InterviewTurn` | `ADAPT` | `services/interview/src/conscious_activations_interview_expression/migrations/0001_interview_expression.sql:13-27` (`ie_objects`) | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:81-92` (`cae.interview_turn`) | Relational turns provide character/temporal offset anchors for `cae.evidence_span`. |
| `EvidenceItem` | `EXTEND` | `services/air/src/cmf_activative_intelligence/domain.py` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:94-105` (`cae.evidence_item`) | Governed by typed lifecycle `CAPTURED -> AUTHENTICATED -> REJECTED -> NEEDS_REPAIR -> SUPERSEDED`. |
| `EvidenceSpan` | `NEW` | `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md:40` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:107-118` (`cae.evidence_span`) | Explicit immutable relational span anchoring evidence to media asset byte range or interview turn text. |
| `EvidenceAuthentication` | `NEW` | `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md:40` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:120-128` (`cae.evidence_authentication`) | Independent evaluator attribution for STC-EVID-001; prohibits self-attestation. |
| `SemanticAssessment` | `EXTEND` | `services/air/src/cmf_activative_intelligence/domain.py` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:130-144` (`cae.semantic_assessment`) | Versioned semantic assessment aggregate with epistemic and lifecycle states validated in WP-03. |
| `AssessmentEvidenceLink` | `NEW` | `docs/cae/implementation/CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md:41` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:146-153` (`cae.assessment_evidence_link`) | Typed link (`SUPPORTS`, `CONTRADICTS`, `CONTEXTUALIZES`) connecting assessment revisions to authenticated evidence. |
| `StateAggregate` | `EXTEND` | `packages/ca_runtime/src/ca_runtime/database.py:23-33` (`ProductHealth`) | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:178-185` (`cae.state_aggregate`) | Optimistic concurrency projection guarding `expected_version` for all aggregate transitions. |
| `StateTransitionContract` | `NEW` | Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md:99-100` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:187-200` (`cae.state_transition_contract`) | Global contract registry defining valid `(from_state, to_state)` pairs and semantic operation bindings. |
| `StateTransition` | `EXTEND` | `packages/ca_runtime/src/ca_runtime/database.py` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:202-217` (`cae.state_transition`) | Append-only transition log recording command ID, contract version, actor ID, and resulting version. |
| `Command` | `EXTEND` | `packages/ca_runtime/src/ca_runtime/migrations/0001_foundation.sql:19-27` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:164-176` (`cae.command`) | Scoped idempotency key `(workspace_id, operation_id, idempotency_key)` preventing duplicate execution. |
| `Event` | `EXTEND` | `packages/ca_runtime/src/ca_runtime/migrations/0001_foundation.sql:29-42` | `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:219-231` (`cae.event`) | Append-only domain event log recording causation/correlation IDs and payload SHA-256. |

---

## 3. Subsystem Lineage & Integration Status

```text
+---------------------+-------------------+---------------------+-------------------------+
| Subsystem           | Storage Engine    | Migration State     | Target Disposition      |
+---------------------+-------------------+---------------------+-------------------------+
| ca_runtime          | SQLite            | Verified Brownfield | EXTEND into PostgreSQL  |
| AIR                 | SQLite / In-Memory| Verified Brownfield | ADAPT via WP-03 Bridge  |
| Interview Expression| SQLite            | Verified Brownfield | ADAPT via WP-09 Bridge  |
| Pipeline Core       | SQLite            | Verified Brownfield | DEFER to CA-STATE-01    |
| Studio / Campaign   | SQLite / In-Memory| Verified Brownfield | EXTEND via Workspace RLS|
| Builder Stage 1/2   | SQLite / JSON     | Verified Brownfield | RETAIN as Spec Inputs   |
| VAE                 | SQLite            | Verified Brownfield | DEFER to Post-Slice     |
| SDA/SFL/Primitive   | Staging PostgreSQL| Applied (WP-04)     | RETAIN Pinned Resolver  |
+---------------------+-------------------+---------------------+-------------------------+
```

---

## 4. Lineage Preservation Affirmation

The projection of SDA, SFL, Primitive, and Interview data into PostgreSQL staging tables does NOT erase original archive hashes, author timestamps, or source lineage. The raw YAML and JSON structures remain permanently queryable via `source_raw_text` and `payload` columns in `cae.registry_item` and `cae.source_package`.
