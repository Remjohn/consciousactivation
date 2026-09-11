# CAE Phase 17 / CA-INT-05: F-01 Schema Repair Proof

**Phase ID:** `CA-INT-05`  
**Migration ID:** `MIG-0007`  
**Title:** Technical Finding F-01 Composite Foreign Key Lineage Repair  
**Target Environment:** `disposable_f01_repair_pg` (`DISPOSABLE_POSTGRESQL_ONLY`)  
**Data Action Class:** `SCHEMA_CONSTRAINT_REPAIR_NO_DML`  

---

## 1. Migration Application Log

The guarded migration runner applied `MIG-0007` following successful execution of baseline `MIG-0001` through `MIG-0006`:

```text
[GUARDED-RUNNER] Admitting target 'disposable_f01_repair_pg'... ADMISSION_OK
[GUARDED-RUNNER] Predecessor check: MIG-0006 applied... OK
[GUARDED-RUNNER] Static linting: Prohibited DDL/DML absent... OK
[GUARDED-RUNNER] Preflight: Parent candidate key cae.receipt(workspace_id, receipt_id) verified... OK
[GUARDED-RUNNER] Preflight: Existing cross-workspace evidence links check (0 found)... OK
[GUARDED-RUNNER] Executing MIG-0007 (0007_cae_f01_composite_receipt_fk_draft.sql)...
  -> ALTER TABLE cae.receipt_evidence_link DROP CONSTRAINT IF EXISTS fk_receipt;
  -> ALTER TABLE cae.receipt_evidence_link DROP CONSTRAINT IF EXISTS receipt_evidence_link_receipt_id_fkey;
  -> ALTER TABLE cae.receipt_evidence_link ADD CONSTRAINT fk_workspace_receipt 
       FOREIGN KEY (workspace_id, receipt_id) REFERENCES cae.receipt(workspace_id, receipt_id) ON DELETE RESTRICT;
[GUARDED-RUNNER] Migration MIG-0007 applied successfully in 14.2ms.
```

---

## 2. Post-Repair Independent Schema Inspection

An independent PostgreSQL catalog inspection was performed on `cae.receipt_evidence_link`:

| Attribute | Prior State (`MIG-0006`) | Repaired State (`MIG-0007`) |
|---|---|---|
| **Foreign Key Constraint** | `fk_receipt` | `fk_workspace_receipt` |
| **Child Constrained Columns** | `(receipt_id)` | `(workspace_id, receipt_id)` |
| **Parent Reference Table** | `cae.receipt` | `cae.receipt` |
| **Parent Reference Columns** | `(receipt_id)` | `(workspace_id, receipt_id)` |
| **Delete Action** | `RESTRICT` | `RESTRICT` |
| **Row Level Security** | `ENABLED` (`p_receipt_evidence_link_isolation`) | `ENABLED` (`p_receipt_evidence_link_isolation`) |
| **Receipt Trigger Protection** | `trg_receipt_append_only` (`fn_prevent_receipt_mutation`) | `trg_receipt_append_only` (`fn_prevent_receipt_mutation`) |

---

## 3. Structural Enforcement Attestation

1. **True Structural Constraint:** The relationship is now enforced by a native PostgreSQL composite foreign key (`fk_workspace_receipt`), completely independent of application code, typed runtime models, triggers, or RLS visibility rules.
2. **Column Order Parity:** Child column pair `(workspace_id, receipt_id)` aligns identically with parent candidate key `uq_workspace_receipt` on `cae.receipt(workspace_id, receipt_id)`.
3. **No Substitute Controls:** The structural repair does not rely on post-hoc parity sweeps or trigger compensation; invalid inserts are rejected at parse/execution time before any row is written.
