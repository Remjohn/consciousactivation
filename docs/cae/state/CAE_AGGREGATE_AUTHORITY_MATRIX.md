# CAE Per-Aggregate Authority Matrix

**Document ID:** `CAE_AGGREGATE_AUTHORITY_MATRIX`  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Authority References:** `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md`, `CAE_TENANT_GUEST_BROWNFIELD_IMPACT_MAP.md`, `CAE_SCOPE_AND_AUTHORITY_MATRIX.md`  

---

## 1. Executive Authority Framework

This document establishes the authoritative operational and migration taxonomy for every stateful, relational, immutable, and canonical aggregate in the **Conscious Activation Engine (CAE)** first vertical operational slice.

### The Four Distinct Authority Axes
In strict conformance with Bundle v3 doctrine and Mandate `CA-STATE-01`, authority is decomposed across four independent, non-collapsible axes:

```text
+------------------------------------------------------------------------------------------------+
| 1. CANONICAL DEFINITION SOURCE                                                                 |
|    The reviewed artifact, version, schema, and constitutional lineage defining semantic meaning.|
+------------------------------------------------------------------------------------------------+
| 2. CURRENT OPERATIONAL AUTHORITY                                                               |
|    The specific store, service, or repository currently trusted for live runtime facts.        |
+------------------------------------------------------------------------------------------------+
| 3. TARGET POSTGRESQL RUNTIME REPRESENTATION                                                    |
|    The verified PostgreSQL relational projection, RLS policies, and content-addressed storage.  |
+------------------------------------------------------------------------------------------------+
| 4. CHANGE & PROMOTION AUTHORITY                                                                |
|    The named operator role, governance committee, or protocol authorized to approve transitions.|
+------------------------------------------------------------------------------------------------+
```

### The Five-Stage Aggregate State Machine
No aggregate may skip stages. Progression is strictly evidence-bearing:

```text
[ LEGACY_ONLY ]
       │
       ▼ (Passes staging DDL, schema validation, and shadow force-rollback comparison)
[ DUAL_VERIFY ]
       │
       ▼ (Operator gate approval + automated zero-drift parity proof)
[ POSTGRES_AUTHORITATIVE ]
       │
       ▼ (Legacy write paths disabled; legacy store frozen as verifiable archive)
[ LEGACY_READ_ONLY ]
       │
       ▼ (Retention period expired + post-cutover audit receipt confirmed)
[ RETIRED ]
```

---

## 2. Per-Aggregate Authority Matrix

| Aggregate ID & Name | Primary Class & Plane | Scope / Parent Chain | Canonical Definition Source | Current Operational Authority | Target PostgreSQL Runtime Representation | Change & Promotion Authority | Single Recommended Disposition | Current Authority State | Contract ID |
|---|---|---|---|---|---|---|---|---|---|
| **`Workspace`** (`CA-ENT-001`) | Entity<br>`OPERATIONAL_PLANE` | Root Tenant Boundary (`workspace_id`) | `PRD-CAE-TEN-001` §3.1,<br>`CA-CAN-01A` | Design Docs / Staging Table `cae.workspace` in `0001_cae_foundation_draft.sql` | PostgreSQL `cae.workspace` (RLS tenant root) | Workspace Admin via typed operation / Platform Policy | **`MIGRATE`**<br>(New Multi-Tenant Root) | `DUAL_VERIFY` (Staging) | `MC-CAE-WS-001` |
| **`WorkspaceMembership`** (`CA-REL-001`) | Relation<br>`OPERATIONAL_PLANE` | `Workspace` (`workspace_id`, `actor_id`) | `PRD-CAE-TEN-001` §3.1,<br>`CA-CAN-01A` | Staging Table `cae.actor` / RLS function `0002_cae_workspace_rls.sql` | PostgreSQL `cae.actor` / `cae.workspace_membership` with unique `(workspace_id, actor_id)` | Workspace Admin / IdP Sync | **`MIGRATE`**<br>(New Multi-Tenant Root) | `DUAL_VERIFY` (Staging) | `MC-CAE-WS-001` |
| **`OperatorOrganization`** (`CA-ENT-000`) | Entity<br>`OPERATIONAL_PLANE` | Root Governance (`operator_org_id`) | `PRD-CAE-TEN-001` §3.2,<br>`CA-CAN-01A` | Design Docs only; absent in legacy SQLite DDL | PostgreSQL `cae.operator_organization` | CAE Platform Governance Committee | **`MIGRATE`**<br>(New Governance Root) | `LEGACY_ONLY` (Design) | `MC-CAE-OPR-001` |
| **`OperatorAccessPolicy`** (`CA-POL-001`) | Policy / Contract<br>`OPERATIONAL_PLANE` | `OperatorOrganization` | `PRD-CAE-TEN-001` §3.2,<br>`14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md` | Design Docs only; absent in legacy SQLite DDL | PostgreSQL `cae.operator_access_policy` | CAE Security / Compliance Officer | **`MIGRATE`**<br>(New Governance Policy) | `LEGACY_ONLY` (Design) | `MC-CAE-OPR-001` |
| **`OperatorAccessGrant`** (`CA-REL-002`) | Relation<br>`OPERATIONAL_PLANE` | `OperatorOrganization` x `Workspace` | `PRD-CAE-TEN-001` §3.2,<br>`CA-CAN-01A` | Design Docs only; absent in legacy SQLite DDL | PostgreSQL `cae.operator_access_grant` (Ephemeral time-bounded) | Designated Security Officer Approval | **`MIGRATE`**<br>(Audit-bounded Grant) | `LEGACY_ONLY` (Design) | `MC-CAE-OPR-001` |
| **`Engagement`** (`CA-ENT-004`) | Entity<br>`OPERATIONAL_PLANE` | `Workspace` (`workspace_id`, `project_id`) | `PRD-CAE-TEN-001` §3.3,<br>`CA-CAN-01A` | SQLite `campaign_orders`, `campaign_states` in `api/services/campaign_repository.py` | PostgreSQL `cae.project` / `cae.engagement` with composite constraint `(workspace_id, project_id)` | Workspace Principal / Engagement Lead | **`MIGRATE`**<br>(Structured Campaign Alignment) | `LEGACY_ONLY` (SQLite Live) | `MC-CAE-ENG-001` |
| **`Guest`** (`CA-ENT-003`) | Entity<br>`OPERATIONAL_PLANE` | `Workspace` (`workspace_id`, `guest_id`) | `PRD-CAE-TEN-001` §3.4,<br>`CA-CAN-01B` | Implicit in Interview SQLite `services/interview/` & Campaign Order | PostgreSQL `cae.guest` (or `cae.actor` of kind `GUEST` scoped by `workspace_id`) | Workspace Engagement Lead / Guest Consent | **`MIGRATE`**<br>(Workspace-local only) | `LEGACY_ONLY` (SQLite Live) | `MC-CAE-GST-001` |
| **`GuestIdentityLink`** (`CA-MAP-001`) | Crosswalk / Mapping<br>`OPERATIONAL_PLANE` | Dual Workspaces (`workspace_a`, `workspace_b`) | `PRD-CAE-TEN-001` §3.4,<br>`CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER.md` | Absent in brownfield | PostgreSQL `cae.guest_identity_link` (Dual consent hashes) | Compliance Officer + Explicit Bilateral Guest Consent | **`RETAIN_OUT_OF_SCOPE`**<br>(Runtime Execution Deferred) | `LEGACY_ONLY` (Deferred) | `MC-CAE-GST-001` |
| **`MediaAsset`** (`CA-ENT-002`) | Entity<br>`OPERATIONAL_PLANE` | `Workspace` [`-> Engagement`] (`workspace_id`, `asset_id`) | `PRD-CAE-TEN-001` §3.5,<br>`CA-CAN-01B` | `services/interview/` SQLite + Local Filesystem media files | PostgreSQL `cae.media_asset` + Supabase Storage `cae-media/{workspace_id}/{asset_id}` | Typed operation `verify_media_asset` (STC-MEDIA-001) | **`READ_THROUGH`** (Legacy) /<br>**`MIGRATE`** (New CAE Assets) | `DUAL_VERIFY` (Staging) | `MC-CAE-MED-001` |
| **`Immutable Media Evidence Bytes`** (`CA-EVI-001`) | Immutable Evidence<br>`OPERATIONAL_PLANE` | `Workspace` -> `MediaAsset` (`workspace_id`, `asset_id`) | `PRD-CAE-TEN-001` §3.5,<br>Builder ADR-003 | Local Filesystem media files (`interviews/{workspace}/{project}/...`) | Private Supabase Storage bucket `cae-media` (SHA-256 content-addressed) | Storage Ingestion Gateway (Provider HEAD + SHA-256 match) | **`READ_THROUGH`**<br>(Via WP-09 Source Bridge) | `DUAL_VERIFY` (Staging) | `MC-CAE-MED-001` |
| **`SourcePackage`** (`CA-REL-004`) | Relation<br>`OPERATIONAL_PLANE` | `Workspace` -> `MediaAsset` (`workspace_id`, `source_package_id`) | `PRD-CAE-TEN-001` §3.5,<br>`CA-CAN-01B` | `conscious_activations_interview_expression` SQLite | PostgreSQL `cae.source_package` with unique `(workspace_id, canonical_sha256)` | Typed bridge operation `register-interview-source` (STC-BRIDGE-000) | **`READ_THROUGH`**<br>(Via WP-09 Bridge) | `DUAL_VERIFY` (Staging) | `MC-CAE-MED-001` |
| **`EvidenceItem` & `EvidenceSpan`** (`CA-EVI-002`, `CA-REL-003`) | Immutable Evidence<br>`OPERATIONAL_PLANE` | `Workspace` -> `SourcePackage` (`workspace_id`, `evidence_id`) | `PRD-CAE-TEN-001` §3.5,<br>`CA-CAN-01B` | SQLite `ie_objects` / `ie_edges` in `services/interview/` | PostgreSQL `cae.evidence_item` + `cae.evidence_span` (Immutable trigger protected) | Typed operations `capture_evidence` (STC-EVID-000), `authenticate_evidence` (STC-EVID-001) | **`MIGRATE`**<br>(First-Slice Operational Lineage) | `DUAL_VERIFY` (Staging) | `MC-CAE-MED-001` |
| **`EvidenceAuthentication`** (`CA-REC-003`) | Receipt / Evaluation<br>`OPERATIONAL_PLANE` | `Workspace` -> `EvidenceItem` (`evidence_id`) | `PRD-CAE-TEN-001` §3.5,<br>`14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md` | Absent in SQLite (Implicit) | PostgreSQL `cae.evidence_authentication` (Distinct evaluator required) | Designated Evaluator Actor via `authenticate_evidence` | **`MIGRATE`**<br>(Independent Attestation) | `DUAL_VERIFY` (Staging) | `MC-CAE-MED-001` |
| **`HarnessTemplate`** (`CA-STR-001`) | Canonical Grammar<br>`CANONICAL_PLANE` | Root Global Canonical (`template_id`, `version`) | `PRD-CAE-TEN-001` §3.6,<br>`CA-CAN-01C` | Versioned YAML runbooks (`docs/cae/runbooks/`) | Repository Git Versioning + Pinned DB snapshot `cae.harness_template` | Architecture Governance Committee | **`RETAIN_OUT_OF_SCOPE`**<br>(Stateless Canonical Definition) | `CANONICAL_PINNED` | `MC-CAE-RUN-001` |
| **`HarnessRun`** (`CA-EXE-001`) | Execution Packet<br>`OPERATIONAL_PLANE` | `Workspace` -> `Engagement` (`workspace_id`, `project_id`, `run_id`) | `PRD-CAE-TEN-001` §3.6,<br>`CA-CAN-01C` | `cmf_pipeline` SQLite `pipeline_runs`, `pipeline_node_states` | PostgreSQL `cae.harness_run`, `cae.harness_run_step` (Future projection) | Workspace Pipeline Runner Service | **`RETAIN_OUT_OF_SCOPE`** (Legacy) /<br>**`MIGRATE`** (New CAE Runs) | `LEGACY_ONLY` (SQLite Live) | `MC-CAE-RUN-001` |
| **`Receipt` & `ExecutionReceipt`** (`CA-REC-001`, `CA-REC-002`) | Receipt / Evaluation<br>`OPERATIONAL_PLANE` | `Workspace` -> `Command` (`workspace_id`, `receipt_id`) | `PRD-CAE-TEN-001` §3.7,<br>`CA-CAN-01C` | SQLite `receipts` in `packages/ca_runtime/src/ca_runtime/database.py` | PostgreSQL `cae.receipt`, `cae.execution_receipt`, `cae.v_receipt_evidence_lineage` | Transactional Operation Adapter at commit time | **`MIGRATE`**<br>(Authoritative Immutable Ledger) | `DUAL_VERIFY` (Staging) | `MC-CAE-REC-001` |
| **`ReceiptEvidenceLink`** (`CA-REL-005`) | Relation<br>`OPERATIONAL_PLANE` | `Workspace` -> `Receipt` x `EvidenceItem` | `PRD-CAE-TEN-001` §3.7,<br>`CA-CAN-01C` | Absent in brownfield SQLite | PostgreSQL `cae.receipt_evidence_link` | Transactional Operation Adapter at commit time | **`MIGRATE`**<br>(Causal Lineage Anchor) | `DUAL_VERIFY` (Staging) | `MC-CAE-REC-001` |
| **`StateAggregate` & `StateTransition`** (`CA-STA-001`, `CA-STA-002`) | State / Event<br>`OPERATIONAL_PLANE` | `Workspace` -> `Aggregate` (`workspace_id`, `aggregate_id`) | `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`,<br>`15_CAE_POSTGRES_STATE_MODEL.md` | Local SQLite sequence / `product_metadata` | PostgreSQL `cae.state_aggregate`, `cae.state_transition` | Transactional Operation Adapter guarding `expected_version` | **`MIGRATE`**<br>(Optimistic Concurrency Control) | `DUAL_VERIFY` (Staging) | `MC-CAE-REC-001` |
| **`SDA Registry`** (`CA-REG-001`) | Canonical Ontology<br>`CANONICAL_PLANE` | Root Global Canonical (`sda.zip`) | `CA-CAN-01C`,<br>`CAE_WP04_REGISTRY_MIGRATION_PROOF.md` | `sda.zip` archive (13 YAML files) | Pinned PostgreSQL read-only snapshot via `RegistryResolver` | Canonical Ontology Lead | **`READ_THROUGH`**<br>(Pinned Hash-Verified Snapshot) | `CANONICAL_PINNED` | Out-of-Scope (Registry) |
| **`SFL Registry`** (`CA-REG-002`) | Perceptual Function<br>`CANONICAL_PLANE` | Root Global Canonical (`sfl.zip`) | `CA-CAN-01C`,<br>`CAE_WP04_REGISTRY_MIGRATION_PROOF.md` | `sfl.zip` archive (28 YAML files; 5 defects) | Pinned PostgreSQL read-only snapshot (5 quarantined missing families) | Sensory Experience Lead | **`QUARANTINE`** (5 Defect Assets) /<br>**`READ_THROUGH`** (23 Valid Assets) | `QUARANTINED_BLOCKED` | Out-of-Scope (Registry) |
| **`Primitive Registry`** (`CA-REG-003`) | Operator / Primitive<br>`CANONICAL_PLANE` | Root Global Canonical (`PRIMITIVE_INVENTORY.csv`) | `CA-CAN-01C`,<br>`CAE_WP04_REGISTRY_MIGRATION_PROOF.md` | AIR Primitive snapshot (243 items; 1 duplicate) | Pinned PostgreSQL read-only snapshot (`EXP-TRG-001` duplicate quarantined) | Primitive Registry Curator | **`QUARANTINE`** (1 Duplicate) /<br>**`READ_THROUGH`** (242 Primitives) | `QUARANTINED_BLOCKED` | Out-of-Scope (Registry) |

---

## 3. Single Recommended Dispositions & First Cutover Candidate

### Recommended First Cutover Candidate
In strict accordance with Mandate Section 3:
> **The recommended first cutover candidate is newly created CAE-owned media asset metadata and immutable evidence lineage (`MC-CAE-MED-001`), together with execution receipt lineage (`MC-CAE-REC-001`).**

**Rationale:**
1. **Zero Data Corruption Risk to Legacy DBs:** New media assets and receipts are authored directly into the PostgreSQL/Supabase schema through typed semantic operations (`verify_media_asset`, `capture_evidence`, `authenticate_evidence`).
2. **Cryptographic Reality Contact:** Media bytes are content-addressed (SHA-256) in private Supabase Storage, and execution receipts enforce immutable evaluation links without relying on legacy SQLite state.
3. **Isolation Protection:** Multi-tenant RLS boundaries (`workspace_id`) are proven on newly instantiated records without needing to backfill messy single-tenant historical databases.

### Deferred & Out-of-Scope Dispositions
1. **Bulk SQLite Historical Backfill:** Wholesale database copying of `cmf_pipeline.db` and `campaign.db` is **`RETAIN_OUT_OF_SCOPE`**. Legacy pipelines continue executing under their current SQLite authority.
2. **Cross-Workspace Guest Linking (`GuestIdentityLink`):** Marked **`RETAIN_OUT_OF_SCOPE`** / **`QUARANTINE`**; runtime link resolution is deferred to prevent unconsented data linkage.
3. **Quarantined Registry Defects:** SFL missing families (`005, 006, 007, 009, 012`) and Primitive duplicate (`EXP-TRG-001`) remain strictly **`QUARANTINE`** and will not be loaded into active execution resolvers.

---

## 4. Non-Claims & Guardrails

1. **Zero Data Movement:** Authoring this matrix moves ZERO rows of data, applies ZERO SQL DDL migrations, and activates ZERO dual-write paths.
2. **No Automatic Cutover:** Declaring an aggregate in `DUAL_VERIFY` or `POSTGRES_AUTHORITATIVE` in this design document does NOT make PostgreSQL authoritative in production. Production cutover requires an explicit operator decision at the Section 7 Gate.
3. **Documentation Integrity:** This matrix is an authoritative state specification governed by `CA-STATE-01`.
