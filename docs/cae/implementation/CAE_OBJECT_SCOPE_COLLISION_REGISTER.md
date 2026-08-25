# CAE Object & Scope Collision Register — CA-MAP-01

**Status:** `ACTIVE_COLLISION_REGISTER`  
**Phase ID:** `CA-MAP-01`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/02_CA_MAP_01_SCOPE_AUTHORITY_MAPPING_MANDATE.md`  
**Authority Reference:** Multi-Tenant Authority and Canonicalization Plan §3.3; Phase 0 Meta-Object Constitution  

---

## 1. Purpose & Register Rules

This register records every ambiguous object classification, architectural split, authority mismatch, and competing interpretation discovered in the CAE first slice.

Non-negotiable register laws:
1. **No Silent Database Resolutions:** Ambiguous classifications are recorded here with competing interpretations; they are never resolved as a convenient database schema decision.
2. **Status Constraints:** Status MUST be exactly one of:
   - `RATIFIED`: Only for pre-existing, evidence-backed operator decisions approved in prior gates.
   - `SPLIT`: Architecturally separated into distinct objects with bounded roles.
   - `DEFERRED`: Deliberately postponed to a downstream phase with an explicit dependency.
   - `BLOCKED`: Work on this object is halted pending an external decision or repair.
3. **Evidence Classification:** Every statement must cite concrete repository evidence labeled as `[EXECUTABLE]`, `[SCHEMA]`, `[MIGRATION]`, `[REGISTRY_SOURCE]`, `[DOCUMENT]`, `[TEST]`, `[HYPOTHESIS]`, or `[OPERATOR_DECISION_REQUIRED]`.

---

## 2. Collision & Split Register

### COL-MAP-001: `OperatorAccessPolicy` vs `OperatorAccessGrant`

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-001` |
| **Object / Proposed Split** | Split single concept of "Operator Access" into `OperatorAccessPolicy` (Global Policy) and `OperatorAccessGrant` (Operational Grant) |
| **Candidate Plane / Class / Scope** | `OperatorAccessPolicy`: `CANONICAL_PLANE` / `Policy / Contract` / `OPERATOR_AUDIT`<br>`OperatorAccessGrant`: `OPERATIONAL_PLANE` / `Relation` / `OPERATOR_AUDIT` |
| **Competing Interpretations** | **Interpretation A (Unified Access Role):** Operator access is a static global role granted to administrators that bypasses all workspace RLS without time bounds or per-session justification.<br>**Interpretation B (Separated Policy & Time-Bounded Grant):** `OperatorAccessPolicy` defines global rules, eligible reasons, and maximum durations, while `OperatorAccessGrant` is an ephemeral, workspace-targeted, reason-bearing grant with an immutable audit receipt. |
| **Direct Evidence** | `[DOCUMENT]` `CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:68, 189-196`; `[SCHEMA]` Absence of operator tables in `sql/0001_cae_foundation_draft.sql`; `[SCHEMA]` `cae.has_workspace_access` in `sql/0002_cae_workspace_rls.sql:13-26` |
| **Consequence of Interpretations** | **Interpretation A:** Breaks multi-tenant client confidentiality, enables unmonitored cross-workspace data leakage, and violates zero-trust audit principles.<br>**Interpretation B:** Enforces cryptographically auditable access boundaries, requires explicit operator justification, and produces append-only receipts. |
| **Recommended Disposition** | **SPLIT:** Formally separate into `OperatorAccessPolicy` (constituted in CA-CAN-01A) and `OperatorAccessGrant` (constituted in CA-CAN-01A). Prohibit standing global bypass. |
| **Required Decision Owner** | CAE Platform Security & Governance Committee |
| **Status** | `SPLIT` |

---

### COL-MAP-002: Canonical `HarnessTemplate` vs Operational `HarnessRun`

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-002` |
| **Object / Proposed Split** | Split "Harness" into `HarnessTemplate` (Canonical Procedural Doctrine) and `HarnessRun` (Workspace-Scoped Operational Execution) |
| **Candidate Plane / Class / Scope** | `HarnessTemplate`: `CANONICAL_PLANE` / `Canonical Structural Grammar` / `GLOBAL_CANONICAL`<br>`HarnessRun`: `OPERATIONAL_PLANE` / `Execution Packet` / `ENGAGEMENT_SCOPED` |
| **Competing Interpretations** | **Interpretation A (Unified Executable):** Harness is a single monolithic runtime service that owns both the workflow graph definition and the mutable state of executing steps.<br>**Interpretation B (Plane Separation):** `HarnessTemplate` is an immutable, versioned canonical specification (YAML/Skill), while `HarnessRun` is an operational aggregate executing inside a specific `Workspace` and `Engagement` context. |
| **Direct Evidence** | `[DOCUMENT]` `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml`; `[EXECUTABLE]` `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py`; `[SCHEMA]` `services/pipeline/src/cmf_pipeline/migrations/0001_pipeline_core.sql` |
| **Consequence of Interpretations** | **Interpretation A:** Conflates procedural doctrine with tenant runtime state, risking tenant data leaking into reusable templates or runtime mutating canonical definitions.<br>**Interpretation B:** Enables deterministic reproducibility of runs against pinned template versions with full tenant isolation. |
| **Recommended Disposition** | **SPLIT:** Constitute `HarnessTemplate` under CA-CAN-01C as canonical doctrine, and `HarnessRun` under CA-CAN-01C as operational state. |
| **Required Decision Owner** | CAE Platform Architecture Lead |
| **Status** | `SPLIT` |

---

### COL-MAP-003: `MediaAsset` Relational Metadata vs Immutable Media Evidence Bytes

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-003` |
| **Object / Proposed Split** | Split "Media Asset" into `MediaAsset` (Relational Identity & Lifecycle Metadata) and `Immutable Media Evidence Bytes` (Object Storage Payload) |
| **Candidate Plane / Class / Scope** | `MediaAsset`: `OPERATIONAL_PLANE` / `Entity` / `WORKSPACE_SCOPED`<br>`Immutable Media Evidence Bytes`: `OPERATIONAL_PLANE` / `Immutable Evidence` / `WORKSPACE_SCOPED` |
| **Competing Interpretations** | **Interpretation A (Database BLOB):** Media bytes and metadata are stored together in PostgreSQL rows or accessed via mutable external file paths.<br>**Interpretation B (Content-Addressed Storage Boundary):** PostgreSQL stores verified identity, SHA-256 hash, byte size, lineage, and lifecycle state (`cae.media_asset`), while raw bytes reside in private object storage (`storage://cae-media/{workspace_id}/{path}`) with strict immutability. |
| **Direct Evidence** | `[DOCUMENT]` Builder ADR-003; `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:38-57`; `[TEST]` `scripts/cae/verify_private_storage.py`; `[DOCUMENT]` `CAE_POSTGRES_STATE_MODEL_RECONCILIATION.md:25-29` |
| **Consequence of Interpretations** | **Interpretation A:** Causes PostgreSQL database bloat, performance degradation, and risks silent in-place byte mutation.<br>**Interpretation B:** Guarantees cryptographic immutability, supports efficient streaming and transcoding, and enables strict RLS and storage bucket policies. |
| **Recommended Disposition** | **SPLIT:** Adopt ADR-003 storage boundary. Constitute `MediaAsset` metadata and `Immutable Media Evidence Bytes` in CA-CAN-01B. Never store raw bytes in Postgres rows. |
| **Required Decision Owner** | Platform Infrastructure Lead |
| **Status** | `RATIFIED` *(Adopted in WP-02/WP-02a and proven in WP-08)* |

---

### COL-MAP-004: `Receipt` vs Evaluation Record (`SemanticAssessment` / `EvidenceAuthentication`)

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-004` |
| **Object / Proposed Split** | Distinguish mechanical execution receipts (`cae.receipt`, `cae.execution_receipt`) from qualitative/epistemic evaluation records (`cae.evidence_authentication`, `cae.semantic_assessment`) |
| **Candidate Plane / Class / Scope** | `Receipt`: `OPERATIONAL_PLANE` / `Receipt / Evaluation Record` / `WORKSPACE_SCOPED`<br>`SemanticAssessment`: `OPERATIONAL_PLANE` / `Derived Semantic Artifact` / `WORKSPACE_SCOPED`<br>`EvidenceAuthentication`: `OPERATIONAL_PLANE` / `Receipt / Evaluation Record` / `WORKSPACE_SCOPED` |
| **Competing Interpretations** | **Interpretation A (Receipt as Evaluation):** A successful execution receipt generated by an automated service proves that the semantic output is valid, tasteful, and true.<br>**Interpretation B (Anti-Self-Attestation):** A mechanical receipt only proves that an operation executed with specific inputs/outputs; semantic evaluation requires independent, attributable evidence links and cannot self-attest validity. |
| **Direct Evidence** | `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:120-144, 233-240`; `[SCHEMA]` `sql/0008_cae_execution_receipt_lineage.sql:5-33`; `[DOCUMENT]` Bundle v3 `08_CAE_IMPLEMENTATION_GATE.md:58-69` |
| **Consequence of Interpretations** | **Interpretation A:** Enables reward hacking and false verification where automated services declare themselves valid without independent reality contact.<br>**Interpretation B:** Enforces Gate H/I anti-centroid and anti-reward-hacking doctrine, requiring independent evaluation links. |
| **Recommended Disposition** | **SPLIT & CONTRACT_RULE:** Maintain `cae.receipt` as mechanical execution proof and require `cae.evidence_authentication` / `cae.semantic_assessment` to supply independent evaluator identities and evidence spans. Constitute in CA-CAN-01C. |
| **Required Decision Owner** | CAE Evaluation Governance Committee |
| **Status** | `SPLIT` |

---

### COL-MAP-005: `GuestIdentityLink` vs Prohibited Automatic `Guest` Merge

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-005` |
| **Object / Proposed Split** | Separate workspace-local `Guest` entities from explicit, auditable `GuestIdentityLink` records. Prohibit automatic cross-workspace guest merges. |
| **Candidate Plane / Class / Scope** | `Guest`: `OPERATIONAL_PLANE` / `Entity` / `GUEST_SCOPED` (Workspace-local)<br>`GuestIdentityLink`: `OPERATIONAL_PLANE` / `Crosswalk / Mapping Object` / `OPERATOR_AUDIT` |
| **Competing Interpretations** | **Interpretation A (Global Guest Master Record):** If two workspaces register a guest with the same email, name, or phone, CAE automatically merges their profiles, evidence, and interview history.<br>**Interpretation B (Strict Workspace Isolation with Explicit Governed Link):** `Guest` is strictly local to a `Workspace`. Cross-workspace record merging is prohibited. Exceptional longitudinal links require an explicit, dual-consented, audit-receipted `GuestIdentityLink`. |
| **Direct Evidence** | `[DOCUMENT]` `CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md:70-71, 407`; `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:74`; `[DOCUMENT]` Mandate Section 3 & 4 |
| **Consequence of Interpretations** | **Interpretation A:** Catastrophic multi-tenant privacy breach; one client gains access to guest interview data from another client without legal basis.<br>**Interpretation B:** Total tenant isolation guaranteed by default; compliant with GDPR/CCPA; preserves legal parent chains. |
| **Recommended Disposition** | **RATIFIED_POLICY & DEFERRED_OBJECT:** Ratify strict workspace-local `Guest` isolation (CA-CAN-01B). Defer `GuestIdentityLink` implementation until multi-workspace enterprise research is explicitly scheduled. |
| **Required Decision Owner** | CAE Legal & Data Protection Officer |
| **Status** | `RATIFIED` *(Workspace-local Guest is non-negotiable; automatic merge strictly prohibited)* |

---

### COL-MAP-006: Canonical Registry Source Archives vs PostgreSQL Runtime Projections

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-006` |
| **Object / Proposed Split** | Distinguish Canonical Registry Definition Source (YAML/ZIP/CSV archives) from Canonical Runtime Representation (`cae.registry_item` / `RegistryResolver`) |
| **Candidate Plane / Class / Scope** | Source Archives: `CANONICAL_PLANE` / `Canonical Ontology` / `GLOBAL_CANONICAL`<br>PostgreSQL Projections: `CANONICAL_PLANE` / `Canonical Ontology` / `GLOBAL_CANONICAL` (Read-only projection) |
| **Competing Interpretations** | **Interpretation A (PostgreSQL as Definition Source):** Because SDA/SFL/Primitive data was migrated into PostgreSQL staging tables in WP-04, PostgreSQL is now the definition source and the original YAML/ZIP archives can be discarded or edited.<br>**Interpretation B (Three Authority Axes):** The definition source remains the immutable, hash-verified archive files (`sda.zip`, `sfl.zip`, `PRIMITIVE_INVENTORY.csv`). PostgreSQL stores an immutable relational projection for runtime lookup. Promotion authority belongs exclusively to the Canonical Governance Committee. |
| **Direct Evidence** | `[REGISTRY_SOURCE]` `sda.zip`, `sfl.zip`, `PRIMITIVE_INVENTORY.csv`; `[SCHEMA]` `sql/0005_cae_registry_authority.sql:13-54`; `[DOCUMENT]` `CAE_WP04_REGISTRY_MIGRATION_PROOF.md`; `[TEST]` `scripts/cae/verify_wp04_registry_migration.py` |
| **Consequence of Interpretations** | **Interpretation A:** Destroys source lineage, obscures inherited defects, and confuses runtime query performance with semantic truth.<br>**Interpretation B:** Preserves 100% cryptographic provenance, keeps defects quarantined, and allows deterministic reconstitution of the registry from source. |
| **Recommended Disposition** | **RATIFIED_PRINCIPLE:** Retain source archives as Definition Source; use PostgreSQL `cae.registry_*` as Runtime Representation. Prohibit in-place database edits. |
| **Required Decision Owner** | Canonical Architecture Lead |
| **Status** | `RATIFIED` *(Enforced by WP-04 and verified by `verify_wp04_registry_migration.py`)* |

---

### COL-MAP-007: Tenancy Boundary: `Workspace` vs `Guest` vs `Engagement` vs `OperatorOrganization`

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-007` |
| **Object / Proposed Split** | Establish `Workspace` as the sole client tenant boundary, subordinate to `OperatorOrganization`, with `Engagement` and `Guest` as workspace-contained children. |
| **Candidate Plane / Class / Scope** | `Workspace`: `OPERATIONAL_PLANE` / `Entity` / `WORKSPACE_SCOPED` (Tenant boundary)<br>`OperatorOrganization`: `OPERATIONAL_PLANE` / `Entity` / `OPERATOR_AUDIT` (Administrative envelope)<br>`Engagement`: `OPERATIONAL_PLANE` / `Entity` / `ENGAGEMENT_SCOPED`<br>`Guest`: `OPERATIONAL_PLANE` / `Entity` / `GUEST_SCOPED` |
| **Competing Interpretations** | **Interpretation A (Guest as Tenancy Key):** Tenancy is anchored to the individual guest, and engagements attach to the guest across multiple organizations.<br>**Interpretation B (Engagement as Tenancy Key):** Tenancy is ephemeral, created per campaign/engagement, with no persistent workspace.<br>**Interpretation C (Workspace as Tenancy Key):** `Workspace` is the durable tenant boundary. An enterprise client holds a workspace. All projects/engagements, guest profiles, media assets, and evidence items belong strictly to that workspace. |
| **Direct Evidence** | `[DOCUMENT]` Multi-Tenant Plan §1, §3; `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:14-36`; `[SCHEMA]` `sql/0002_cae_workspace_rls.sql:62-100`; `[EXECUTABLE]` `api/domain/campaign.py:79-80` |
| **Consequence of Interpretations** | **Interpretation A & B:** Creates orphaned data, prevents enterprise access management, complicates RLS security policies, and risks cross-tenant exposure.<br>**Interpretation C:** Provides clean RLS enforcement (`has_workspace_access`), aligns with standard SaaS multi-tenancy, and preserves legal parent containment. |
| **Recommended Disposition** | **CANDIDATE_RATIFICATION:** Nominate `Workspace` as the candidate tenant boundary for CA-MAP-01 approval, with `Engagement` and `Guest` strictly contained within `Workspace`. |
| **Required Decision Owner** | Operator Gate (CA-MAP-01 Approval Decision) |
| **Status** | `RATIFIED` *(Candidate tenant boundary nominated; awaiting Section 7 operator gate)* |

---

### COL-MAP-008: Quarantined Registry Defects (SFL Missing Families & Primitive Duplicate ID)

| Field | Detail |
|---|---|
| **Collision ID** | `COL-MAP-008` |
| **Object / Proposed Split** | Quarantine inherited registry defects without silent repair or synthetic remapping. |
| **Candidate Plane / Class / Scope** | `SFL Registry`: Missing families `SFL-FAM-005, 006, 007, 009, 012` (5 assets quarantined)<br>`Primitive Registry`: Duplicate ID `EXP-TRG-001` (2 files quarantined) |
| **Competing Interpretations** | **Interpretation A (Silent Synthetic Repair):** The migration script or database should invent placeholder family definitions for SFL and assign a new ID (e.g., `EXP-TRG-001-B`) to the second primitive to achieve 100% import pass.<br>**Interpretation B (Strict Evidence Quarantine):** Inherited source defects are imported raw with preserved lineage, flagged with `integrity_issues`, and quarantined from runtime resolution until the accountable lineage owner provides authoritative corrections. |
| **Direct Evidence** | `[REGISTRY_SOURCE]` `sfl.zip`, `PRIMITIVE_INVENTORY.csv`; `[SCHEMA]` `sql/0005_cae_registry_authority.sql:70-82`; `[DOCUMENT]` `CAE_WP04_REGISTRY_MIGRATION_PROOF.md:39-55`; `[TEST]` `scripts/cae/verify_wp04_registry_migration.py` |
| **Consequence of Interpretations** | **Interpretation A:** Manufactures false canonical authority, risks semantic drift, and hides source corpus errors.<br>**Interpretation B:** Enforces complete evidentiary integrity; ensures runtime resolver rejects ambiguous or missing identities; highlights accountable debt. |
| **Recommended Disposition** | **RATIFIED_DISPOSITION:** Maintain quarantines in `cae.registry_integrity_issue` and `RegistryResolver`. Block affected assets from runtime resolution until upstream repair. |
| **Required Decision Owner** | Accountable Lineage Owners (Sensory Experience Lead & Primitive Ontology Lead) |
| **Status** | `BLOCKED` *(Quarantined assets blocked from runtime; awaiting accountable source lineage repair)* |

---

## 3. Register Summary

- **Total Registered Collisions/Splits:** 8 items.
- **Architectural Splits (`SPLIT`):** 3 (`OperatorAccessPolicy`/`Grant`, `HarnessTemplate`/`Run`, `Receipt`/`EvaluationRecord`).
- **Ratified Principles/Boundaries (`RATIFIED`):** 4 (`MediaAsset` ADR-003 Storage Boundary, Prohibited `Guest` Merge, Registry Source/Projection Axes, `Workspace` Candidate Tenant Boundary).
- **Quarantined Debt / Blocked (`BLOCKED`):** 1 (SFL missing families & Primitive duplicate `EXP-TRG-001`).
