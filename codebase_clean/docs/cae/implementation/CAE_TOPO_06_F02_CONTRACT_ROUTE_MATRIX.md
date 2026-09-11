# CAE Phase 18 / CA-TOPO-06: Contract-Route Matrix & Executability Analysis

**Phase ID:** `CA-TOPO-06`  
**Finding Reference:** `F-02 (Staging Table-Family Shadowing & Duality)`  
**Scope:** Contract Routes, Semantic Operations, Key Compatibility, and Consumer Impact  
**Governing Mandate:** `docs/cae/gemini_execution/18_CA_TOPO_06_TABLE_FAMILY_TOPOLOGY_RECONCILIATION_MANDATE.md`  

---

## 1. Contract-to-Route Traceability Matrix

| Contract / Operation ID | Handler Class | Input Key Shape | Target Relation Family | Target DDL Table & Columns | RLS / Session Mechanism | Receipt & Lineage Behavior | Consumers / Callers | Current Executability | Route Classification |
|---|---|---|---|---|---|---|---|---|---|
| `CAE-BRIDGE-001.verified-interview-source-registration` (`cae.bridge.register-interview-source`) | `FirstSliceSemanticOperations.register_verified_interview_source` | String / Text (`workspace_id`, `project_id`, `asset_id`) | `WP03_TEXT_FAMILY` | `cae.project`, `cae.media_asset(asset_id, project_id, ...)` | None (unscoped connection) | Emits text receipt payload to `cae.execution_receipt` | `interview_source_bridge.py`, Evaluation Suite | **NON-EXECUTABLE** against CA-IMPL UUID schema | `BLOCKED_SCHEMA_MISMATCH` |
| `CAE-MEDIA-001.media-verification` (`cae.media.verify@1.0.0`) | `TenantScopedSemanticOperations.verify_media_asset` | `UUID` (`workspace_id`, `media_asset_id`, optional `engagement_id`) | `CA_IMPL_UUID_FAMILY` | `cae.media_asset(workspace_id, media_id, ...)`, `cae.receipt` | Thread-safe `SET LOCAL cae.current_workspace_id` | Emits immutable `cae.receipt` + `cae.receipt_evidence_link` | `tenant_operations.py`, `CA-IMPL-02` Cutover Suite | **FULLY EXECUTABLE** in CA-IMPL schema | `BOUNDED_TYPED_ROUTE_ACTIVE` |
| `CAE-EVID-001.capture-traceability` | `FirstSliceSemanticOperations` (Legacy) | String / Text | `WP03_TEXT_FAMILY` | Legacy text tables | None | Legacy text receipt | Legacy prototype scripts | **NON-EXECUTABLE** against CA-IMPL UUID schema | `LEGACY_UNRECONCILED` |
| `CAE-TENANT-001.workspace-creation` | `TenantScopedSemanticOperations.create_workspace` | `UUID` (`workspace_id`) | `CA_IMPL_UUID_FAMILY` | `cae.workspace(workspace_id, name)` | RLS Enabled | Emits `cae.receipt` | `tenant_operations.py`, Test Suites | **FULLY EXECUTABLE** | `CANONICAL_TARGET_ROUTE` |

---

## 2. Root Cause Analysis: Why `register_verified_interview_source` Cannot Execute

The bridge operation `register_verified_interview_source` in `packages/ca_runtime/src/ca_runtime/semantic_operations.py` is structurally and syntactically incompatible with the target `CA_IMPL_UUID_FAMILY`:

1. **Missing Table Dependency (`cae.project`):**
   - In line 507, the bridge executes: `SELECT 1 FROM cae.project WHERE workspace_id = %s AND project_id = %s`.
   - The CA-IMPL schema (`0001` through `0007`) does NOT define a `cae.project` table; projects were superseded by the `cae.engagement` aggregate.
   - **Result:** PostgreSQL raises `undefined_table` (`42P01`).

2. **Column Divergence in `cae.media_asset`:**
   - In line 524, the bridge attempts an `INSERT INTO cae.media_asset (asset_id, workspace_id, project_id, storage_provider, storage_bucket, storage_object_key, canonical_uri, content_sha256, byte_size, media_type, lifecycle_state, created_by_actor_id, verified_at)`.
   - In CA-IMPL `cae.media_asset`, the actual columns are:
     - `media_id UUID` (not `asset_id TEXT`)
     - `workspace_id UUID` (not `workspace_id TEXT`)
     - `file_name TEXT`, `content_type TEXT`, `byte_size BIGINT`, `sha256_hash TEXT`, `storage_bucket TEXT`, `storage_path TEXT`, `created_at TIMESTAMPTZ`, `created_by_user_id UUID`.
     - Columns `project_id`, `storage_provider`, `canonical_uri`, `lifecycle_state`, `created_by_actor_id`, and `verified_at` do NOT exist.
   - **Result:** PostgreSQL raises `undefined_column` (`42703`).

3. **Key Type Incompatibility (String vs UUID):**
   - The bridge generates prefixed text IDs such as `cae:media:ie:7f8a9b...`.
   - The CA-IMPL primary key is `UUID NOT NULL`.
   - **Result:** PostgreSQL raises `invalid_text_representation` (`22P02`).

4. **Tenancy Session Absence:**
   - The bridge connects using a raw database connection without invoking `apply_tenant_session(cur, ctx)`.
   - Under CA-IMPL Row-Level Security, queries without `cae.current_workspace_id` set return 0 rows or trigger RLS rejection.

---

## 3. Bounded Cutover Workaround vs Canonical Authority

During Phase 12 (`CA-IMPL-02`), operator authorization permitted verifying the `MC-CAE-MED-001` cutover via the typed `verify_media_asset` route in `tenant_operations.py`:

- **Why it was permitted:** `verify_media_asset` strictly conformed to `TS-CAE-TEN-001`, enforced RLS, performed live storage byte readbacks, and recorded immutable receipts on the CA-IMPL schema.
- **Why it did NOT resolve F-02:** The typed route bypassed `interview_source_bridge.py` and `FirstSliceSemanticOperations`. It did not reconcile the table naming collision or establish canonical status for either family. The underlying bridge contract `register_verified_interview_source` remains broken and unexecutable.
- **Conclusion:** Workarounds do not establish canonical architecture. Reconciling F-02 requires an explicit operator decision among defined topology options.
