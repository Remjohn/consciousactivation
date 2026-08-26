# CAE Migration 03 Forward-Only Migration Plan

**Phase ID:** `CA-MIG-03`  
**Document ID:** `CAE_MIG_03_FORWARD_MIGRATION_PLAN`  
**Status:** `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/15_CA_MIG_03_FORWARD_ONLY_MIGRATION_SAFETY_MANDATE.md`  

---

## 1. Architectural Philosophy and Migration Principles

The CAE forward-only migration system eliminates the destructive patterns of `apply_ca_impl_01a_scaffolding.py` (`F-04`) and replaces them with an immutable, versioned delta sequence:

1. **Strict Forward-Only Progression:** No down migrations that execute `DROP TABLE`, `TRUNCATE`, or `DROP SCHEMA CASCADE`. Rollbacks are achieved via forward-repair patches or point-in-time recovery.
2. **Deterministic Preflight Verification:** Every migration requires a read-only preflight query that inspects schema metadata before attempting any DDL modification.
3. **Zero Data Mutation During Foundation Application:** Foundation migrations are classified as `SCHEMA_ONLY_NO_DML` and execute zero data transformation or backfilling.
4. **Decoupled Repair Boundaries:** Known debt items (`F-01` composite FK repair and `F-02` table shadow reconciliation) are modeled as distinct subsequent migrations, preserving clean auditability.

---

## 2. Forward-Only Migration Sequence

```text
[MIG-0001: Extensions & Schema]
            |
[MIG-0002: Tenancy & Membership Root]
            |
[MIG-0003: Engagement, Guest & Media Core]
            |
[MIG-0004: Harness & Immutable Receipts]
            |
[MIG-0005: Row-Level Security & Policies]
            |
[MIG-0006: Composite Foreign Keys & Indexes]
            |
[MIG-0007: (Future) F-01 Composite Lineage FK Patch]
            |
[MIG-0008: (Future) F-02 Staging Shadow Table Reconciliation]
```

---

## 3. Detailed Migration Specifications

### 3.1 `MIG-0001`: `0001_cae_extensions_and_schema.sql`
- **Migration ID:** `MIG-0001`
- **Purpose:** Initialize required PostgreSQL extensions and the isolated `cae` namespace.
- **Predecessor:** `NONE` (Genesis migration)
- **Data Action Class:** `SCHEMA_ONLY_NO_DML` (Data effect: `NONE`)
- **Preconditions:** PostgreSQL $\ge 15.0$; database user has `CREATE` privilege on current database.
- **Ordered DDL:**
  ```sql
  CREATE EXTENSION IF NOT EXISTS "pgcrypto";
  CREATE SCHEMA IF NOT EXISTS cae;
  ```
- **Postconditions:** Schema `cae` exists; function `gen_random_uuid()` is executable.
- **Failure & Forward Repair:** If extension fails to create, halt execution and grant database superuser privileges or request managed extension provisioning.
- **Verification Requirement:** `SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cae';` returns 1 row.

---

### 3.2 `MIG-0002`: `0002_cae_tenancy_and_membership.sql`
- **Migration ID:** `MIG-0002`
- **Purpose:** Establish tenant root envelopes (`workspace`, `operator_organization`) and access bindings (`workspace_membership`, `operator_access_grant`).
- **Predecessor:** `MIG-0001`
- **Data Action Class:** `SCHEMA_ONLY_NO_DML` (Data effect: `NONE`)
- **Preconditions:** `MIG-0001` applied; tables `cae.workspace` and `cae.operator_organization` do not exist or conform to target schema.
- **Ordered DDL:**
  1. `CREATE TABLE IF NOT EXISTS cae.workspace (...)`
  2. `CREATE TABLE IF NOT EXISTS cae.workspace_membership (...)`
  3. `CREATE TABLE IF NOT EXISTS cae.operator_organization (...)`
  4. `CREATE TABLE IF NOT EXISTS cae.operator_access_grant (...)`
- **Postconditions:** 4 core tenancy tables exist with expected columns, constraints, and defaults.
- **Failure & Forward Repair:** Halt transaction on key collision; inspect table metadata for conflicting types before applying repair patch.

---

### 3.3 `MIG-0003`: `0003_cae_engagement_guest_media.sql`
- **Migration ID:** `MIG-0003`
- **Purpose:** Create domain entities (`engagement`, `guest`, `media_asset`) with composite unique constraints for tenant-partitioned foreign referencing.
- **Predecessor:** `MIG-0002`
- **Data Action Class:** `SCHEMA_ONLY_NO_DML` (Data effect: `NONE`)
- **Preconditions:** `MIG-0002` applied; `cae.workspace` present with `workspace_id` PK.
- **Ordered DDL:**
  1. `CREATE TABLE IF NOT EXISTS cae.engagement (...)` with `uq_workspace_engagement UNIQUE (workspace_id, engagement_id)`
  2. `CREATE TABLE IF NOT EXISTS cae.guest (...)` with `uq_workspace_guest UNIQUE (workspace_id, guest_id)`
  3. `CREATE TABLE IF NOT EXISTS cae.media_asset (...)` with `uq_workspace_media UNIQUE (workspace_id, media_id)` and `uq_workspace_storage_path UNIQUE (workspace_id, storage_path)`
- **Postconditions:** 3 domain tables created with composite unique constraints intact.
- **Failure & Forward Repair:** If column type conflict detected, emit non-destructive warning and stop before DDL modification.

---

### 3.4 `MIG-0004`: `0004_cae_harness_and_immutable_receipts.sql`
- **Migration ID:** `MIG-0004`
- **Purpose:** Create pipeline execution entities (`harness_template`, `harness_run`) and immutable receipt ledger (`receipt`, `receipt_evidence_link`, append-only trigger).
- **Predecessor:** `MIG-0003`
- **Data Action Class:** `SCHEMA_ONLY_NO_DML` (Data effect: `NONE`)
- **Preconditions:** `MIG-0003` applied.
- **Ordered DDL:**
  1. `CREATE TABLE IF NOT EXISTS cae.harness_template (...)`
  2. `CREATE TABLE IF NOT EXISTS cae.harness_run (...)`
  3. `CREATE TABLE IF NOT EXISTS cae.receipt (...)`
  4. `CREATE TABLE IF NOT EXISTS cae.receipt_evidence_link (...)`
  5. `CREATE OR REPLACE FUNCTION cae.fn_prevent_receipt_mutation() ...`
  6. `CREATE TRIGGER trg_receipt_append_only BEFORE UPDATE OR DELETE ON cae.receipt ...`
- **Postconditions:** Tables exist; attempt to `UPDATE` or `DELETE` on `cae.receipt` raises exception `EX_RECEIPT_IMMUTABLE`.
- **Failure & Forward Repair:** Recreate trigger function in `cae` schema if trigger creation encounters dependency error.

---

### 3.5 `MIG-0005`: `0005_cae_row_level_security.sql`
- **Migration ID:** `MIG-0005`
- **Purpose:** Enable Row-Level Security (RLS) across all 10 `cae` tables and install tenant isolation and operator grant policies.
- **Predecessor:** `MIG-0004`
- **Data Action Class:** `SECURITY_ONLY_NO_DML` (Data effect: `NONE`)
- **Preconditions:** Tables exist in `cae` schema; session user has permission to alter tables and create policies.
- **Ordered DDL:**
  - `ALTER TABLE cae.<table_name> ENABLE ROW LEVEL SECURITY;` for all 10 tables.
  - Create `p_workspace_isolation_*` and `p_operator_grant_*` policies.
- **Postconditions:** `rowsecurity = true` for all 10 tables in `pg_tables`; cross-tenant select returns 0 rows.
- **Failure & Forward Repair:** If policy creation fails, verify `current_setting('app.current_workspace_id', true)` configuration helper.

---

### 3.6 `MIG-0006`: `0006_cae_indexes_and_constraints.sql`
- **Migration ID:** `MIG-0006`
- **Purpose:** Create performance indexes on workspace lookup columns, storage path hashes, and timestamps.
- **Predecessor:** `MIG-0005`
- **Data Action Class:** `PERFORMANCE_INDEXES_NO_DML` (Data effect: `NONE`)
- **Ordered DDL:** `CREATE INDEX IF NOT EXISTS idx_...` on foreign keys and lookup paths.
- **Postconditions:** Indexes present in `pg_indexes`.

---

## 4. Operational Safety and Non-Claims

1. **Non-Executable Status:** This plan and all associated SQL drafts are marked `DRAFT_NOT_APPLIED`. They SHALL NOT be executed against any database in Phase 15.
2. **Zero Authority Mutation:** This design does not alter the current operational authority (`MC-CAE-MED-001` is `POSTGRES_AUTHORITATIVE_STAGING_ONLY`; all other aggregates remain SQLite).
3. **F-01 and F-02 Handling:** `F-01` (composite FK on receipts) and `F-02` (staging schema shadow table resolution) are planned as subsequent forward migrations (`MIG-0007` and `MIG-0008`) and remain explicitly open.
