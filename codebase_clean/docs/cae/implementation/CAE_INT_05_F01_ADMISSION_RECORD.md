# CAE Phase 17 / CA-INT-05: Target Admission Record & Baseline

**Phase ID:** `CA-INT-05`  
**Target Identifier:** `disposable_f01_repair_pg`  
**Environment Class:** `DISPOSABLE_POSTGRESQL_ONLY`  
**Data Classification:** `EMPTY_OR_SYNTHETIC_ONLY`  
**Governing Mandate:** `docs/cae/gemini_execution/17_CA_INT_05_WORKSPACE_RECEIPT_LINEAGE_INTEGRITY_MANDATE.md`  
**Operational Authority:** `ZERO_CHANGE_DURING_CA_INT_05`  

---

## 1. Admission Guard Verification

| Guard ID | Admission Assertion | Verification Value | Status |
|---|---|---|---|
| `ADM-INT-01` | Non-Staging Endpoint Identity | Endpoint `postgresql://127.0.0.1:5432/disposable_f01_db` does not contain `evnxdssbxxrsesftdvgx` or `.pooler.supabase.com` | **PASS** |
| `ADM-INT-02` | Non-Production Environment | No `prod`, `production`, or `live` host/cluster headers | **PASS** |
| `ADM-INT-03` | Explicit Disposable Declaration | `is_disposable_declared = True` explicitly set | **PASS** |
| `ADM-INT-04` | Synthetic Data Only | Zero client, Guest, media, or operational records | **PASS** |
| `ADM-INT-05` | Foundation Baseline Verified | Baseline migrations `MIG-0001` through `MIG-0006` applied | **PASS** |
| `ADM-INT-06` | Controlled Teardown Bound | Teardown ownership assigned to `CA-INT-05 Execution Harness` | **PASS** |

---

## 2. Baseline Schema & Defect Precondition Audit

Prior to applying the F-01 structural repair, the baseline schema established by `MIG-0001` through `MIG-0006` was audited:

1. **Parent Table (`cae.receipt`):**
   - Candidate Key: `CONSTRAINT uq_workspace_receipt UNIQUE (workspace_id, receipt_id)` exists.
   - Primary Key: `receipt_id UUID PRIMARY KEY`.
   - Append-only Trigger: `trg_receipt_append_only` calling `cae.fn_prevent_receipt_mutation()` is active.

2. **Child Table (`cae.receipt_evidence_link`):**
   - Single-column FK: `CONSTRAINT fk_receipt FOREIGN KEY (receipt_id) REFERENCES cae.receipt(receipt_id) ON DELETE RESTRICT`.
   - Defect (`F-01`): A raw SQL insert specifying Workspace B with a receipt belonging to Workspace A is accepted by the database because `fk_receipt` only validates `receipt_id`.

---

## 3. Approved Repair Draft Manifest

| Field | Specification |
|---|---|
| **Migration ID** | `MIG-0007` |
| **Filename** | `0007_cae_f01_composite_receipt_fk_draft.sql` |
| **Predecessor** | `MIG-0006` |
| **Data Action Class** | `SCHEMA_CONSTRAINT_REPAIR_NO_DML` |
| **Status Header** | `-- STATUS: DRAFT_NOT_APPLIED` |
| **Target Constraint** | `CONSTRAINT fk_workspace_receipt FOREIGN KEY (workspace_id, receipt_id) REFERENCES cae.receipt(workspace_id, receipt_id) ON DELETE RESTRICT` |

---

## 4. Admission Conclusion

The disposable target `disposable_f01_repair_pg` is fully isolated, admitted under strict non-staging / non-production rules, and confirmed ready for `MIG-0007` execution.
