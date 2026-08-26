# CAE Phase 19 (CA-TOPO-07) Canonical Route Execution Proof

**Phase ID:** `CA-TOPO-07`  
**Operation Tested:** `register_verified_interview_source` (Canonical Bridge Adapter Route)  
**Contract ID:** `STC-BRIDGE-000` / `CAE-BRIDGE-001.verified-interview-source-registration`  
**Target Environment:** `disposable_topo07_pg` (`DISPOSABLE_POSTGRESQL_ONLY`)  
**Date:** 2026-08-26  

---

## 1. Canonical Route Execution Trace

The canonical bridge operation `register_verified_interview_source` was executed against synthetic Interview Expression inputs in `disposable_topo07_pg`:

```text
[INPUT PAYLOAD]
  workspace_id: "syn_ws_alpha"
  project_id: "syn_proj_alpha"
  bridge_actor_id: "syn_actor_01"
  source_package_id: "cae:source:syn_01"
  upstream_source_ref: {
    object_id: "obj_01",
    revision: "1",
    sha256: "de31216f21c32cd99a8384dc3851b32264d0c3ddb24f50455e2da4380bb7c011"
  }
  media_asset_id: "cae:media:syn_01"
  storage_bucket: "cae-media"
  storage_object_key: "interviews/syn_ws_alpha/syn_proj_alpha/clip.mp4"
  content_sha256: "de31216f21c32cd99a8384dc3851b32264d0c3ddb24f50455e2da4380bb7c011"
  byte_size: 23
  media_type: "video/mp4"
  idempotency_key: "idemp_topo07_01"

[EXECUTION SEQUENCE]
  1. Deterministic UUID Mapping:
     - workspace_uuid:   6b603c9c-91a4-5249-9471-45b7ebcf8e6a
     - engagement_uuid:  d1810052-a567-5ba7-b769-cf4d8c823028
     - media_uuid:       5199a077-23a4-5f8b-a896-e9948edbc646
     - receipt_uuid:     21fa3a4a-d28d-52ab-84ec-115a906d664e
  2. Tenancy Context:
     - SET LOCAL cae.current_workspace_id = '6b603c9c-91a4-5249-9471-45b7ebcf8e6a';
  3. Parent Verification:
     - SELECT 1 FROM cae.engagement WHERE engagement_id = 'd1810052-a567-5ba7-b769-cf4d8c823028' AND workspace_id = '6b603c9c-91a4-5249-9471-45b7ebcf8e6a' -> FOUND
  4. Media Insertion:
     - INSERT INTO cae.media_asset (media_id, workspace_id, file_name, content_type, byte_size, sha256_hash) -> COMMITTED (1 row)
  5. Immutable Receipt:
     - INSERT INTO cae.receipt (receipt_id, workspace_id, operation_id, payload) -> COMMITTED (1 row)
  6. Lineage Evidence Link (F-01 Constraint fk_workspace_receipt):
     - INSERT INTO cae.receipt_evidence_link (link_id, workspace_id, receipt_id, media_id) -> COMMITTED (1 row)
```

---

## 2. Idempotent Replay Verification

A re-execution of `register_verified_interview_source` with the exact same inputs and `idempotency_key = "idemp_topo07_01"` was executed:
- **Result:** `outcome = IDEMPOTENT_REPLAY`, `idempotent_replay = True`.
- **Receipt ID:** Matched original receipt `21fa3a4a-d28d-52ab-84ec-115a906d664e`.
- **Row Count:** 0 additional rows created in `cae.media_asset`, `cae.receipt`, or `cae.receipt_evidence_link`.

---

## 3. Schema Inspection Verification

Inspection of `information_schema.tables` confirmed clean isolation of relation families:

| Table Name | Key Schema Type | Namespace / Role | Status |
| :--- | :--- | :--- | :--- |
| `cae.workspace` | UUID (`workspace_id`) | Canonical Multi-Tenancy Root | **ACTIVE** |
| `cae.engagement` | UUID (`engagement_id`) | Canonical Project / Engagement Aggregate | **ACTIVE** |
| `cae.media_asset` | UUID (`media_id`) | Canonical Media Aggregate | **ACTIVE** |
| `cae.receipt` | UUID (`receipt_id`) | Immutable Execution Receipt Ledger | **ACTIVE** |
| `cae.receipt_evidence_link` | UUID (`link_id`) | Composite FK Evidence Linkage | **ACTIVE** |
| `legacy_wp03_workspace` | Text (`workspace_id`) | Quarantined Legacy WP-03 Table | **QUARANTINED** |
| `legacy_wp03_media_asset` | Text (`asset_id`) | Quarantined Legacy WP-03 Table | **QUARANTINED** |
| `legacy_wp03_execution_receipt` | Text (`receipt_id`) | Quarantined Legacy WP-03 Table | **QUARANTINED** |
