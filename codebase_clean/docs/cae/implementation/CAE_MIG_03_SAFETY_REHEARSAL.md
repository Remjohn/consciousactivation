# CAE Migration 03 Safety Rehearsal and No-Go Checklist

**Phase ID:** `CA-MIG-03`  
**Document ID:** `CAE_MIG_03_SAFETY_REHEARSAL`  
**Status:** `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/15_CA_MIG_03_FORWARD_ONLY_MIGRATION_SAFETY_MANDATE.md`  

---

## 1. Offline Rehearsal Framework

This rehearsal models the dry-run execution profile of the forward-only migration sequence (`MIG-0001` through `MIG-0006`) against an offline schema state machine. **Zero remote database connections or live SQL executions are conducted in this phase.**

---

## 2. Step-by-Step Offline Rehearsal Ledger

### Step 1: Extensions and Schema Genesis (`MIG-0001`)
- **Input Preconditions:** Target database engine is PostgreSQL $\ge 15.0$; database user possesses `CREATE` schema privilege.
- **Expected Schema Delta:** Schema `cae` registered; extension `pgcrypto` active.
- **Allowed Data Effect:** `NONE` (Zero rows inserted, modified, or deleted).
- **Lock & Concurrency Impact:** Brief catalog lock on `pg_namespace` and `pg_extension`; zero table-level lock contention.
- **Future Preflight Detection Query:**
  ```sql
  SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'cae') AS schema_exists;
  ```
- **Postcondition Assertion:** `schema_exists = TRUE` and `gen_random_uuid()` callable.
- **Compensating / Forward-Repair Route:** If creation is denied by privilege error, request database administrator elevation; do not drop existing schema.

---

### Step 2: Tenancy Roots & Access Bounding (`MIG-0002`)
- **Input Preconditions:** `MIG-0001` completed; no incompatible legacy tables named `cae.workspace` with non-UUID keys.
- **Expected Schema Delta:** Tables `cae.workspace`, `cae.workspace_membership`, `cae.operator_organization`, `cae.operator_access_grant` created.
- **Allowed Data Effect:** `NONE`.
- **Lock & Concurrency Impact:** `AccessExclusiveLock` during table creation; duration $< 50\text{ms}$.
- **Future Preflight Detection Query:**
  ```sql
  SELECT table_name, column_name, data_type 
  FROM information_schema.columns 
  WHERE table_schema = 'cae' AND table_name = 'workspace' AND column_name = 'workspace_id';
  ```
- **Postcondition Assertion:** Column `workspace_id` is of type `uuid` with `PRIMARY KEY`.
- **Compensating / Forward-Repair Route:** If a column type mismatch occurs, halt immediately; author forward-repair migration `MIG-0002_repair` to alter column type safely.

---

### Step 3: Domain Entities & Tenant Partitioning (`MIG-0003`)
- **Input Preconditions:** `MIG-0002` completed; `cae.workspace` parent table exists.
- **Expected Schema Delta:** Tables `cae.engagement`, `cae.guest`, `cae.media_asset` created with composite unique constraints `uq_workspace_engagement`, `uq_workspace_guest`, `uq_workspace_media`, and `uq_workspace_storage_path`.
- **Allowed Data Effect:** `NONE`.
- **Lock & Concurrency Impact:** `AccessExclusiveLock` on new table creation only.
- **Future Preflight Detection Query:**
  ```sql
  SELECT conname FROM pg_constraint WHERE conname IN ('uq_workspace_engagement', 'uq_workspace_guest', 'uq_workspace_media');
  ```
- **Postcondition Assertion:** All 3 composite constraints exist in `pg_constraint`.
- **Compensating / Forward-Repair Route:** If constraint creation fails, check for duplicate index names and emit patch script.

---

### Step 4: Pipeline Runs & Immutable Receipt Ledger (`MIG-0004`)
- **Input Preconditions:** `MIG-0003` completed.
- **Expected Schema Delta:** Tables `cae.harness_template`, `cae.harness_run`, `cae.receipt`, `cae.receipt_evidence_link`, function `cae.fn_prevent_receipt_mutation()`, and trigger `trg_receipt_append_only` created.
- **Allowed Data Effect:** `NONE`.
- **Lock & Concurrency Impact:** Minimal DDL creation lock.
- **Future Preflight Detection Query:**
  ```sql
  SELECT tgname FROM pg_trigger WHERE tgname = 'trg_receipt_append_only';
  ```
- **Postcondition Assertion:** Trigger exists and is enabled on `cae.receipt`.
- **Compensating / Forward-Repair Route:** If trigger binding fails, drop and recreate trigger specifically within `MIG-0004` scope; do not alter receipt table schema.

---

### Step 5: Row-Level Security & Access Policies (`MIG-0005`)
- **Input Preconditions:** `MIG-0004` completed; all 10 `cae` tables present.
- **Expected Schema Delta:** `rowsecurity = true` on all 10 tables; 10 workspace isolation policies and operator grant policies installed.
- **Allowed Data Effect:** `NONE`.
- **Lock & Concurrency Impact:** `AccessExclusiveLock` during `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`.
- **Future Preflight Detection Query:**
  ```sql
  SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'cae';
  ```
- **Postcondition Assertion:** All 10 tables return `rowsecurity = true`.
- **Compensating / Forward-Repair Route:** If policy syntax error occurs, issue `DROP POLICY ... ON cae.<table>` and recreate corrected policy statement in forward patch.

---

### Step 6: Indexes & Constraint Enforcement (`MIG-0006`)
- **Input Preconditions:** `MIG-0005` completed.
- **Expected Schema Delta:** Lookup indexes created on `workspace_id`, `created_at`, `status`, and `storage_path`.
- **Allowed Data Effect:** `NONE`.
- **Lock & Concurrency Impact:** Use `CREATE INDEX CONCURRENTLY` in live environments to prevent read/write locks.
- **Future Preflight Detection Query:**
  ```sql
  SELECT indexname FROM pg_indexes WHERE schemaname = 'cae';
  ```
- **Postcondition Assertion:** All target indexes present and valid (`indisvalid = true`).
- **Compensating / Forward-Repair Route:** If index build fails concurrently, execute `DROP INDEX CONCURRENTLY` and retry with specific index migration.

---

## 3. Mandatory No-Go Safety Checklist

A future application mandate SHALL NOT proceed if any of the following 10 conditions are violated:

| Check ID | No-Go Condition | Rejection Rule / Safety Barrier | Status in CA-MIG-03 |
|---|---|---|---|
| **NOGO-01** | Destructive DDL statement present (`DROP TABLE`, `TRUNCATE`, `DROP SCHEMA CASCADE`, unbounded `DELETE`) | Strictly prohibited; all proposed migrations are forward-only (`SCHEMA_ONLY_NO_DML`). | `DEFENDED` |
| **NOGO-02** | Concealed incompatible table, column type, or key via silent `IF NOT EXISTS` | Preflight detection query must verify exact column types before attempting creation. | `DEFENDED` |
| **NOGO-03** | RLS policy or receipt immutability trigger omitted, weakened, or bypassed | Preflight checks must verify `rowsecurity = true` and trigger presence across all 10 tables. | `DEFENDED` |
| **NOGO-04** | Checksum recorded in migration history before postconditions verified | Migration history insertion must be strictly ordered *after* postcondition assertions pass. | `DEFENDED` |
| **NOGO-05** | Child foreign keys or access policies applied before parent tables exist | Strict topological sort verified in dependency DAG (`MIG-0001` through `MIG-0006`). | `DEFENDED` |
| **NOGO-06** | F-01 composite FK claimed without structural enforcement | F-01 is explicitly modeled as a separate future migration (`MIG-0007`) requiring preflight integrity validation. | `DEFENDED` |
| **NOGO-07** | F-02 table shadowing silently resolved without approved topology | F-02 is explicitly isolated to `MIG-0008` pending operator topology approval. | `DEFENDED` |
| **NOGO-08** | Rollback mechanism relies on destructive drop or unverified backup | Rollback is defined strictly as forward-repair migrations or point-in-time recovery. | `DEFENDED` |
| **NOGO-09** | Static SQL analysis claimed as proof of live database compatibility | Explicit non-claim: Static parsing proves design integrity only (E1/E2), not E3 reality. | `DEFENDED` |
| **NOGO-10** | Migration drafts executable by automation without explicit guard | All SQL drafts carry mandatory `-- STATUS: DRAFT_NOT_APPLIED` header guard. | `DEFENDED` |
