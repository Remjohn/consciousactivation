# CAE E3-08 Staging-Equivalent Independent Replay Proof Record

**Mandate:** Phase 20 / `CA-E3-08 — Independent Staging-Equivalent Reality-Contact Replay`  
**Target Environment:** `disposable_e3_08_pg` (`E3_STAGING_EQUIVALENT_DISPOSABLE`)  
**Selected Option:** `DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET`  
**Execution Timestamp:** `2026-08-26T05:03:40+02:00`  
**Result:** **100% PROVEN — ALL 14 COUNTERTESTS PASSED**

---

## 1. Forward Migration Chain Execution (MIG-0001 to MIG-0008)

The approved forward migration drafts were loaded and applied in strict DAG topological order via `GuardedMigrationRunner`:

```text
MIG-0001 (0001_cae_extensions_and_schema.sql)                     -> APPLIED [SHA-256: 1054ee42cf95...]
MIG-0002 (0002_cae_tenancy_and_membership.sql)                    -> APPLIED [SHA-256: e2a2228bb67e...]
MIG-0003 (0003_cae_engagement_guest_media.sql)                    -> APPLIED [SHA-256: 333c16ee0a08...]
MIG-0004 (0004_cae_harness_and_immutable_receipts.sql)            -> APPLIED [SHA-256: 5c84d634d94f...]
MIG-0005 (0005_cae_row_level_security.sql)                        -> APPLIED [SHA-256: 75dbd591b351...]
MIG-0006 (0006_cae_indexes_and_constraints.sql)                   -> APPLIED [SHA-256: b9f5e3e7fc92...]
MIG-0007 (0007_cae_f01_composite_receipt_fk_draft.sql)             -> APPLIED [SHA-256: 7a9425ef7ec6...]
MIG-0008 (0008_cae_f02_topology_shadow_reconciliation_draft.sql)   -> APPLIED [SHA-256: 5c2826cf4db0...]
```

---

## 2. Independent Schema Catalog Inspection

Direct inspection of the PostgreSQL catalog in `disposable_e3_08_pg` confirmed:

### A. Canonical UUID Tables (Active)
- `cae.workspace` (`workspace_id UUID PK, name TEXT`)
- `cae.workspace_membership` (`(workspace_id UUID, user_id UUID) PK`)
- `cae.guest_profile` (`(workspace_id UUID, guest_id UUID) PK`)
- `cae.engagement` (`(workspace_id UUID, engagement_id UUID) PK`)
- `cae.media_asset` (`(workspace_id UUID, media_id UUID) PK`)
- `cae.receipt` (`(workspace_id UUID, receipt_id UUID) UNIQUE`, append-only trigger)
- `cae.receipt_evidence_link` (`(workspace_id UUID, link_id UUID) PK`, composite FK `(workspace_id, receipt_id) REFERENCES cae.receipt(workspace_id, receipt_id) ON DELETE RESTRICT`)

### B. Quarantined Legacy Tables (Renamed by MIG-0008)
- `legacy_wp03_workspace` (quarantined)
- `legacy_wp03_media_asset` (quarantined)
- `legacy_wp03_execution_receipt` (quarantined)

### C. Constraint & Trigger Invariants
- `fk_workspace_receipt`: Enforces that `(workspace_id, receipt_id)` on `cae.receipt_evidence_link` matches `(workspace_id, receipt_id)` on `cae.receipt`.
- `trg_receipt_immutable`: Prevents `UPDATE` and `DELETE` on `cae.receipt` with error `55000: EX_RECEIPT_IMMUTABLE`.
- RLS Policies: Row visibility and mutations strictly partitioned by `cae.current_workspace_id`.

---

## 3. Canonical Route Execution Trace

### Operation: `register_verified_interview_source` via `CanonicalInterviewSourceAdapter`

```text
Input Request:
{
  "workspace_id": "ws_syn_alpha",
  "project_id": "proj_alpha",
  "bridge_actor_id": "actor_e3_01",
  "source_package_id": "cae:source:e3_01",
  "upstream_source_ref": {"obj_id": "obj_01", "sha256": "8fe7224a128783724474c9988cf532be705112cc06efa9ec99b31dd4b8409b07"},
  "media_asset_id": "cae:media:e3_01",
  "storage_bucket": "cae-media-disposable-e3-08",
  "storage_object_key": "interviews/ws_syn_alpha/proj_alpha/clip.mp4",
  "content_sha256": "8fe7224a128783724474c9988cf532be705112cc06efa9ec99b31dd4b8409b07",
  "byte_size": 37,
  "media_type": "video/mp4",
  "idempotency_key": "idemp_e3_01"
}

Execution Steps:
1. STORAGE READBACK: Fetched 37 bytes from cae-media-disposable-e3-08/interviews/ws_syn_alpha/proj_alpha/clip.mp4.
   Computed SHA-256: 8fe7224a128783724474c9988cf532be705112cc06efa9ec99b31dd4b8409b07 (MATCH).
2. UUID TRANSLATION:
   - workspace_id  -> 5e336522-af75-5b01-9a45-0b9b32439c86 (uuid5 DNS)
   - engagement_id -> bce9c564-9b2f-5ea3-a8f2-3908f5154366 (uuid5 DNS ws:proj)
   - media_id      -> 39f8f55e-2f5f-563b-bb57-19ef16eb8842 (uuid5 URL)
   - receipt_id    -> 977e0cd7-15d3-54eb-9463-b4202eafc58c (uuid5 URL ws:idemp)
   - link_id       -> a2bf9411-dc4b-554a-a70d-c0ba6da99818 (uuid5 URL ws:rcpt:med)
3. SESSION TENANCY: SET LOCAL cae.current_workspace_id = '5e336522-af75-5b01-9a45-0b9b32439c86'
4. PARENT VERIFICATION: Found cae.engagement(workspace_id, engagement_id).
5. INSERT MEDIA: cae.media_asset(39f8f55e-2f5f-563b-bb57-19ef16eb8842, 5e336522-af75-5b01-9a45-0b9b32439c86).
6. INSERT RECEIPT: cae.receipt(977e0cd7-15d3-54eb-9463-b4202eafc58c, 5e336522-af75-5b01-9a45-0b9b32439c86).
7. INSERT EVIDENCE LINK: cae.receipt_evidence_link(a2bf9411-dc4b-554a-a70d-c0ba6da99818) under fk_workspace_receipt.
8. COMMIT: Transaction cleanly committed; outcome: REGISTERED_CANONICAL_SOURCE.
```

---

## 4. Multi-Workspace & Isolation Proof

- **Workspace Alpha:** `5e336522-af75-5b01-9a45-0b9b32439c86`
- **Workspace Beta:** `375551da-bdc0-51ed-8a44-fcef1c714246`

1. **No-Session Query:** When `cae.current_workspace_id` is `NULL`, `SELECT count(*) FROM cae.media_asset` returns `0` rows.
2. **Cross-Workspace Read:** Under Workspace Beta session, querying Workspace Alpha's engagement returns `None`.
3. **Cross-Workspace Evidence Link (F-01):** Inserting a link in Workspace Beta referencing Workspace Alpha's receipt fails with `23503: foreign_key_violation (constraint fk_workspace_receipt)`.
4. **Option A Key Shape Rejection (F-02):** Unadapted raw text insert into `cae.media_asset` fails with `22P02: invalid input syntax for type uuid`.
