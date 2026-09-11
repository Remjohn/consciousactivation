# CAE Migration 03 F-01 and F-02 Repair Boundary Specification

**Phase ID:** `CA-MIG-03`  
**Document ID:** `CAE_MIG_03_F01_F02_REPAIR_BOUNDARY`  
**Status:** `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/15_CA_MIG_03_FORWARD_ONLY_MIGRATION_SAFETY_MANDATE.md`  

---

## 1. Technical Finding F-01: Lineage Link Single-Column Foreign Key

### 1.1 Finding Description and Risk
- **Current State:** Table `cae.receipt_evidence_link` binds to `cae.receipt` via single-column foreign key `receipt_id REFERENCES cae.receipt(receipt_id) ON DELETE CASCADE`.
- **Architectural Risk:** Although Python runtime discipline (`TenantContextManager`) enforces workspace isolation at the application layer, raw SQL execution or malformed queries could theoretically insert cross-workspace evidence links without triggering a database schema rejection.
- **Governing Requirement:** Multi-tenant composite foreign key pattern `(workspace_id, receipt_id)` referencing `cae.receipt(workspace_id, receipt_id)`.

### 1.2 Target Repair Migration (`MIG-0007`) Specification
- **Migration ID:** `MIG-0007` (`0007_cae_f01_composite_receipt_fk.sql`)
- **Action Type:** Forward-only constraint replacement.
- **Preflight Integrity Sweep (Dry-Run Only):**
  ```sql
  -- Preflight: Detect any orphaned or cross-workspace mismatched evidence links
  SELECT l.link_id, l.workspace_id AS link_ws, r.workspace_id AS rcpt_ws
  FROM cae.receipt_evidence_link l
  JOIN cae.receipt r ON l.receipt_id = r.receipt_id
  WHERE l.workspace_id <> r.workspace_id;
  ```
  *Precondition Rule:* If preflight returns $> 0$ rows, migration halts and requires quarantined data repair before adding constraint.
- **Ordered DDL Delta:**
  ```sql
  -- Drop single-column foreign key constraint
  ALTER TABLE cae.receipt_evidence_link 
      DROP CONSTRAINT IF EXISTS receipt_evidence_link_receipt_id_fkey;

  -- Add composite foreign key constraint enforcing strict workspace tenancy matching
  ALTER TABLE cae.receipt_evidence_link 
      ADD CONSTRAINT fk_receipt_evidence_link_composite_receipt
      FOREIGN KEY (workspace_id, receipt_id) 
      REFERENCES cae.receipt(workspace_id, receipt_id) 
      ON DELETE CASCADE;
  ```
- **Postcondition Verification:** Query `pg_constraint` to confirm composite column binding on `fk_receipt_evidence_link_composite_receipt`.
- **Status in CA-MIG-03:** `STILL_OPEN — DESIGNED_NOT_APPLIED`.

---

## 2. Technical Finding F-02: Staging Schema Table Name Shadowing

### 2.1 Finding Description and Risk
- **Current State:** Staging database contains two concurrent schema table families:
  1. **WP-03 Brownfield Tables:** Text-keyed tables (`cae.workspace`, `cae.media_asset`, `cae.execution_receipt`) used by historical FastAPI and early SQLite adapters.
  2. **CA-IMPL-01B UUID-keyed Tables:** TS-CAE-TEN-001 conforming multi-tenant tables.
- **Architectural Risk:** Dual-schema topology creates ambiguous query routing if un-aliased raw SQL queries execute against the staging database without explicit fully qualified types.

### 2.2 Target Repair Migration (`MIG-0008`) Specification
- **Migration ID:** `MIG-0008` (`0008_cae_f02_topology_shadow_reconciliation.sql`)
- **Action Type:** Non-destructive schema deprecation / table renaming.
- **Topology Options for Operator Authorization:**
  - *Option A (Deprecate & Rename):* Rename legacy WP-03 tables to `cae.legacy_wp03_*` to eliminate namespace collisions while preserving historical data.
  - *Option B (View Aliasing):* Create compatibility views pointing to new UUID tables for legacy read paths during migration transition.
- **Preflight Integrity Sweep:**
  ```sql
  SELECT table_name, column_name, data_type 
  FROM information_schema.columns 
  WHERE table_schema = 'cae' AND table_name IN ('workspace', 'media_asset', 'receipt');
  ```
- **Ordered DDL Delta (Option A Candidate):**
  ```sql
  -- Rename legacy tables non-destructively
  ALTER TABLE IF EXISTS cae.workspace RENAME TO legacy_wp03_workspace;
  ALTER TABLE IF EXISTS cae.media_asset RENAME TO legacy_wp03_media_asset;
  ALTER TABLE IF EXISTS cae.execution_receipt RENAME TO legacy_wp03_execution_receipt;
  ```
- **Status in CA-MIG-03:** `STILL_OPEN — DESIGNED_NOT_APPLIED`.

---

## 3. Strict Non-Claims and Guardrails

1. **No Application in Phase 15:** Neither `F-01` nor `F-02` repair DDL is applied to any live, staging, or local database in `CA-MIG-03`.
2. **Preservation of Open Status:** Both findings remain `STILL_OPEN` in the Implementation Control State and Ratification Register.
3. **No Premature Closure:** Ratification or closure of `F-01` or `F-02` requires a subsequent authorized execution phase (`CA-MIG-04` or `CA-TOPO-06/07`) following disposable-environment proof.
