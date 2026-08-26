# CAE Staging Preflight & Deployment Record — Phase 21 / CA-STAGE-09

**Status:** `APPLIED_AND_VERIFIED`  
**Phase ID:** `CA-STAGE-09`  
**Execution Date:** `2026-08-26T05:15:00Z`  
**Target:** `evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres`  
**Governing Mandate:** `docs/cae/gemini_execution/21_CA_STAGE_09_CONTROLLED_SHARED_STAGING_DEPLOYMENT_MANDATE.md`

---

## 1. Read-Only Preflight Verification

1. **Table Family Preflight:**
   - Pre-existing active relation inventory checked.
   - Quarantined table rename compatibility verified: `workspace` $\to$ `legacy_wp03_workspace`, `media_asset` $\to$ `legacy_wp03_media_asset`, `execution_receipt` $\to$ `legacy_wp03_execution_receipt`.
   - Zero collision detected in `cae.*` schema.
2. **Data Rewrite Absence:**
   - Schema modifications preflighted as DDL metadata operations only.
   - Zero row-level data conversions or table rewrites required.
3. **Recovery Readiness Preflight:**
   - Verified PITR recovery snapshot `snapshot_pre_stage09_20260826T051500Z` is active and restorable.

---

## 2. Guarded Deployment Execution Trace

The deployment was executed strictly via [`GuardedMigrationRunner`](file:///d:/Work/consciousactivation/packages/ca_runtime/src/ca_runtime/migration_runner.py):

```text
[MIGRATION START] Target: evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres (E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE)
[PREFLIGHT CHECK] Checking approved draft checksums and predecessor sequence...
  [OK] MIG-0001: 0001_cae_extensions_and_schema.sql (1c81a54160a2...)
  [OK] MIG-0002: 0002_cae_tenancy_and_membership.sql (f5ba22765d70...)
  [OK] MIG-0003: 0003_cae_engagement_guest_media.sql (fe166a0dbe38...)
  [OK] MIG-0004: 0004_cae_harness_and_immutable_receipts.sql (75f102717013...)
  [OK] MIG-0005: 0005_cae_row_level_security.sql (166cf3283311...)
  [OK] MIG-0006: 0006_cae_indexes_and_constraints.sql (e99fca315570...)
  [OK] MIG-0007: 0007_cae_f01_composite_receipt_fk_draft.sql (5e8557ee6c13...)
  [OK] MIG-0008: 0008_cae_f02_topology_shadow_reconciliation_draft.sql (90fa8b61c8d7...)

[APPLY] Executing forward DDL transactions...
  [APPLIED] MIG-0001: Extensions & schema 'cae' initialized.
  [APPLIED] MIG-0002: Tenancy & workspace_membership created.
  [APPLIED] MIG-0003: Engagement, guest_profile, media_asset created (UUID PKs).
  [APPLIED] MIG-0004: Receipt & execution harness structures initialized.
  [APPLIED] MIG-0005: Row-Level Security policies active across all cae tables.
  [APPLIED] MIG-0006: Indexes and primary integrity constraints created.
  [APPLIED] MIG-0007: Composite FK constraint 'fk_workspace_receipt' applied on receipt_evidence_link.
  [APPLIED] MIG-0008: Quarantined legacy WP-03 tables to 'legacy_wp03_*'; established canonical UUID topology.

[MIGRATION COMPLETE] All 8 forward migrations applied cleanly. Zero errors.
```

---

## 3. Post-Deployment Schema Catalog Manifest

| Table / Relation | Schema / Namespace | Primary Key Type | Constraints & Policies | Status |
|---|---|---|---|---|
| `cae.workspace` | `cae` | `UUID` | Tenancy root | **ACTIVE_CANONICAL** |
| `cae.workspace_membership` | `cae` | `(UUID, UUID)` | FK `workspace_id`, RLS enabled | **ACTIVE_CANONICAL** |
| `cae.guest_profile` | `cae` | `(UUID, UUID)` | FK `workspace_id`, RLS enabled | **ACTIVE_CANONICAL** |
| `cae.engagement` | `cae` | `(UUID, UUID)` | FK `workspace_id`, RLS enabled | **ACTIVE_CANONICAL** |
| `cae.media_asset` | `cae` | `(UUID, UUID)` | FK `workspace_id`, RLS enabled | **ACTIVE_CANONICAL** |
| `cae.receipt` | `cae` | `(UUID, UUID)` | Immutability Trigger `EX_RECEIPT_IMMUTABLE`, RLS enabled | **ACTIVE_CANONICAL** |
| `cae.receipt_evidence_link` | `cae` | `(UUID, UUID)` | Composite FK `fk_workspace_receipt`, RLS enabled | **ACTIVE_CANONICAL** |
| `legacy_wp03_workspace` | `public` | `TEXT` | Quarantined legacy table | **QUARANTINED** |
| `legacy_wp03_media_asset` | `public` | `TEXT` | Quarantined legacy table | **QUARANTINED** |
| `legacy_wp03_execution_receipt` | `public` | `TEXT` | Quarantined legacy table | **QUARANTINED** |
