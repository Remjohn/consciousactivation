# CAE Phase 18 / CA-TOPO-06: F-02 Table-Family Topology Inventory

**Phase ID:** `CA-TOPO-06`  
**Finding Reference:** `F-02 (Staging Table-Family Shadowing & Duality)`  
**Classification:** `SOURCE_DEFINED` & `TOPOLOGY_EVIDENCED_DECISION_REQUIRED`  
**Governing Mandate:** `docs/cae/gemini_execution/18_CA_TOPO_06_TABLE_FAMILY_TOPOLOGY_RECONCILIATION_MANDATE.md`  
**Operational Authority:** `ZERO_CHANGE_DURING_CA_TOPO_06`  

---

## 1. Table Family Identification & Provenance

The CAE codebase and staging history contain two distinct relational table families:

1. **Family 1: WP-03 Legacy Text-Keyed Family (`WP03_TEXT_FAMILY`)**
   - **Origin:** Early brownfield prototypes and WP-03 first-slice bridge implementation (`packages/ca_runtime/src/ca_runtime/semantic_operations.py`, `interview_source_bridge.py`).
   - **Key Architecture:** Text/String primary keys (`id TEXT`, `workspace_id TEXT`, `project_id TEXT`, `asset_id TEXT`).
   - **Entity Hierarchy:** `cae.workspace` -> `cae.project` -> `cae.media_asset` -> `cae.execution_receipt`.
   - **Tenancy Model:** String workspace matching without composite foreign keys or tenant session context variables.

2. **Family 2: CA-IMPL UUID-Keyed Family (`CA_IMPL_UUID_FAMILY`)**
   - **Origin:** `TS-CAE-TEN-001`, `CA-IMPL-01A`, `CA-IMPL-01B`, and `CA-IMPL-02` (`packages/ca_runtime/src/ca_runtime/tenant_operations.py`, `models/tenant_slice.py`).
   - **Key Architecture:** Native PostgreSQL `UUID` primary and composite foreign keys (`workspace_id UUID`, `media_id UUID`, `receipt_id UUID`).
   - **Entity Hierarchy:** `cae.workspace` -> `cae.workspace_membership` / `cae.guest_profile` -> `cae.engagement` -> `cae.media_asset` -> `cae.receipt` -> `cae.receipt_evidence_link`.
   - **Tenancy Model:** Strict Row-Level Security (`current_setting('cae.current_workspace_id')`), composite candidate keys, append-only immutability triggers.

---

## 2. Evidence-Classified Relational Inventory

| Topology Item ID | Relation / Entity | Family Label | Evidence Class | Key Shape & Types | Constraints & RLS | Contract & Operation Bindings | Consumers & Callers | Executability | Authority / Scope | Collision Role | Risk | Proposed Disposition | Decision Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `TOPO-01` | `cae.workspace` (Legacy) | `WP03_TEXT_FAMILY` | `SOURCE_DEFINED` | `workspace_id TEXT PRIMARY KEY` | No RLS, single PK | `FirstSliceSemanticOperations` | `interview_source_bridge.py` | Executable in WP-03 DB | Brownfield Prototype | Collides with CA-IMPL `cae.workspace` on relation name | Namespace collision; type mismatch | Quarantined / Rename to `legacy_wp03_workspace` | **Decision Required (Option A/B/C)** |
| `TOPO-02` | `cae.project` (Legacy) | `WP03_TEXT_FAMILY` | `SOURCE_DEFINED` | `project_id TEXT PRIMARY KEY, workspace_id TEXT` | `fk_workspace` (TEXT) | `FirstSliceSemanticOperations.register_verified_interview_source` | `interview_source_bridge.py` | Non-executable (Table absent in CA-IMPL) | Brownfield Prototype | Absent in CA-IMPL | Bridge fails on `SELECT FROM cae.project` | Drain or recreate in legacy namespace | **Decision Required (Option A/B/C)** |
| `TOPO-03` | `cae.media_asset` (Legacy) | `WP03_TEXT_FAMILY` | `SOURCE_DEFINED` | `asset_id TEXT PRIMARY KEY, workspace_id TEXT, project_id TEXT` | No RLS | `register_verified_interview_source` | `FirstSliceSemanticOperations` | Non-executable against UUID schema | Brownfield Prototype | Shadowed by CA-IMPL `cae.media_asset` | Schema column mismatch (`asset_id` vs `media_id`) | Quarantined / Rename to `legacy_wp03_media_asset` | **Decision Required (Option A/B/C)** |
| `TOPO-04` | `cae.execution_receipt` (Legacy) | `WP03_TEXT_FAMILY` | `SOURCE_DEFINED` | `receipt_id TEXT PRIMARY KEY, workspace_id TEXT` | No triggers, single PK | `FirstSliceSemanticOperations._execution_receipt_context` | `FirstSliceSemanticOperations` | Non-executable against `cae.receipt` | Brownfield Prototype | Shadowed by CA-IMPL `cae.receipt` | Receipt structure divergence | Quarantined / Rename to `legacy_wp03_execution_receipt` | **Decision Required (Option A/B/C)** |
| `TOPO-05` | `cae.workspace` (Modern) | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `workspace_id UUID PRIMARY KEY, name TEXT` | RLS Enabled (`p_workspace_isolation`) | `TenantScopedSemanticOperations.create_workspace` | `tenant_operations.py`, `test_ca_impl_02_cutover.py` | Fully Executable | Target Foundation | Collides with WP-03 `cae.workspace` | Rejection of text IDs | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-06` | `cae.workspace_membership` | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `(workspace_id UUID, user_id UUID) PRIMARY KEY` | RLS Enabled, Composite FK | `TenantScopedSemanticOperations.add_member` | `tenant_operations.py` | Fully Executable | Target Foundation | No legacy counterpart | None | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-07` | `cae.guest_profile` | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `(workspace_id UUID, guest_id UUID) PRIMARY KEY` | RLS Enabled, Composite FK | `TenantScopedSemanticOperations.create_guest_profile` | `tenant_operations.py` | Fully Executable | Target Foundation | No legacy counterpart | None | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-08` | `cae.engagement` | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `(workspace_id UUID, engagement_id UUID) PRIMARY KEY` | RLS Enabled, Composite FK | `TenantScopedSemanticOperations.create_engagement` | `tenant_operations.py` | Fully Executable | Target Foundation | Replaces `cae.project` concept | Semantic divergence | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-09` | `cae.media_asset` (Modern) | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `(workspace_id UUID, media_id UUID) PRIMARY KEY` | RLS Enabled, Composite FK | `TenantScopedSemanticOperations.verify_media_asset` | `tenant_operations.py`, CA-IMPL-02 Cutover | Fully Executable | `POSTGRES_AUTHORITATIVE_STAGING_ONLY` (`MC-CAE-MED-001`) | Shadows legacy `cae.media_asset` | Legacy bridge incompatible | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-10` | `cae.receipt` (Modern) | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `receipt_id UUID PRIMARY KEY, (workspace_id UUID, receipt_id UUID) UNIQUE` | RLS Enabled, `trg_receipt_append_only` | `TenantScopedSemanticOperations` receipts | `tenant_operations.py` | Fully Executable | Target Foundation | Replaces `execution_receipt` | Incompatible receipt schema | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |
| `TOPO-11` | `cae.receipt_evidence_link` | `CA_IMPL_UUID_FAMILY` | `SOURCE_DEFINED` | `(workspace_id UUID, link_id UUID) PRIMARY KEY, FK (workspace_id, receipt_id)` | RLS Enabled, Composite FK (F-01 Repaired) | `TenantScopedSemanticOperations` lineage | `tenant_operations.py`, CA-INT-05 Proof | Fully Executable | Target Foundation | No legacy counterpart | None | Canonical Target (Option A) | **Decision Required (Option A/B/C)** |

---

## 3. Inventory Summary & Status

- **Total Analyzed Entities:** 11 relations / components.
- **WP-03 Legacy Family:** 4 relations (`workspace`, `project`, `media_asset`, `execution_receipt`).
- **CA-IMPL Modern Family:** 7 relations (`workspace`, `workspace_membership`, `guest_profile`, `engagement`, `media_asset`, `receipt`, `receipt_evidence_link`).
- **Direct Namespace Collisions:** 3 relations (`cae.workspace`, `cae.media_asset`, `cae.execution_receipt` vs `cae.receipt`).
- **Current Topology Status:** `TOPOLOGY_EVIDENCED_DECISION_REQUIRED`.
