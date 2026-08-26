# CAE Phase 17 / CA-INT-05: Adversarial Countertest Results

**Phase ID:** `CA-INT-05`  
**Target Environment:** `disposable_f01_repair_pg`  
**Countertest Suite:** `F01-CT-01` through `F01-CT-11`  
**Overall Result:** `11 / 11 PASSED`  

---

## 1. Adversarial Countertest Matrix

| Countertest ID | Description | Expected Behavior | Actual Behavior | Result |
|---|---|---|---|---|
| `F01-CT-01` | Direct cross-Workspace link insertion (B-to-A) | Database raises PostgreSQL exception `23503` on `fk_workspace_receipt` | **REJECTED**: `foreign_key_violation` (`fk_workspace_receipt`), 0 rows created | **PASS** |
| `F01-CT-02` | Valid Workspace-local link insertion (A-to-A) | Insert succeeds cleanly | **ACCEPTED**: 1 row created with matching composite keys | **PASS** |
| `F01-CT-03` | Parent candidate key catalog inspection | `uq_workspace_receipt` exists on `cae.receipt(workspace_id, receipt_id)` | **VERIFIED**: Composite unique key present and active | **PASS** |
| `F01-CT-04` | Child composite FK catalog inspection | `fk_workspace_receipt` binds `(workspace_id, receipt_id)` | **VERIFIED**: Composite FK present with `ON DELETE RESTRICT` | **PASS** |
| `F01-CT-05` | Preflight cross-workspace data detection | Preflight halts if mismatched link records exist | **VERIFIED**: `IncompatibleTopologyError` raised on bad data | **PASS** |
| `F01-CT-06` | Preflight missing parent key detection | Preflight halts if parent lacks composite candidate key | **VERIFIED**: `IncompatibleTopologyError` raised on single key | **PASS** |
| `F01-CT-07` | Append-only receipt trigger retention | `UPDATE`/`DELETE` on `cae.receipt` raises `EX_RECEIPT_IMMUTABLE` | **VERIFIED**: Trigger `trg_receipt_append_only` active | **PASS** |
| `F01-CT-08` | RLS isolation and unscoped query denial | Unscoped `SELECT` returns 0 rows; cross-workspace queries isolated | **VERIFIED**: RLS policies `p_*` fully retained | **PASS** |
| `F01-CT-09` | Altered repair draft & predecessor rejection | Runner rejects tampered checksums and missing predecessor `MIG-0006` | **VERIFIED**: `MigrationPredecessorError` raised | **PASS** |
| `F01-CT-10` | Atomic rollback and honest history ledger | Failed migration aborts transaction with zero ghost history rows | **VERIFIED**: Atomic transaction rollback verified | **PASS** |
| `F01-CT-11` | Scoped synthetic teardown verification | Fixtures purges completely with zero shared staging leakage | **VERIFIED**: Complete teardown attestation | **PASS** |

---

## 2. Deep Dive: Direct Structural Countertest (`F01-CT-01` & `F01-CT-02`)

To prove structural enforcement independent of application logic or RLS visibility:

1. **Setup:**
   - Synthetic Workspace A: `ws_alpha` (`00000000-0000-4000-a000-000000000001`)
   - Synthetic Workspace B: `ws_beta` (`00000000-0000-4000-b000-000000000002`)
   - Synthetic Receipt in A: `rcpt_alpha` (`10000000-0000-4000-a000-000000000001`)

2. **Adversarial Negative Insertion (`B -> A`):**
   ```sql
   -- Executed under privileged proof connection bypassing RLS
   INSERT INTO cae.receipt_evidence_link (
       link_id, workspace_id, receipt_id, media_id, evidence_type, verified_sha256
   ) VALUES (
       gen_random_uuid(),
       '00000000-0000-4000-b000-000000000002', -- Workspace B
       '10000000-0000-4000-a000-000000000001', -- Receipt in Workspace A
       gen_random_uuid(),
       'SOURCE_FILE',
       'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
   );
   ```
   **PostgreSQL Engine Output:**
   ```text
   ERROR: insert or update on table "receipt_evidence_link" violates foreign key constraint "fk_workspace_receipt"
   DETAIL: Key (workspace_id, receipt_id)=(00000000-0000-4000-b000-000000000002, 10000000-0000-4000-a000-000000000001) is not present in table "receipt".
   SQLSTATE: 23503
   ```
   **Verification:** `SELECT count(*) FROM cae.receipt_evidence_link WHERE workspace_id = '00000000-0000-4000-b000-000000000002'` returns **0**.

3. **Positive Insertion (`A -> A`):**
   ```sql
   INSERT INTO cae.receipt_evidence_link (
       link_id, workspace_id, receipt_id, media_id, evidence_type, verified_sha256
   ) VALUES (
       gen_random_uuid(),
       '00000000-0000-4000-a000-000000000001', -- Workspace A
       '10000000-0000-4000-a000-000000000001', -- Receipt in Workspace A
       gen_random_uuid(),
       'SOURCE_FILE',
       'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
   );
   ```
   **PostgreSQL Engine Output:**
   ```text
   INSERT 0 1
   ```
   **Verification:** `SELECT count(*) FROM cae.receipt_evidence_link WHERE workspace_id = '00000000-0000-4000-a000-000000000001'` returns **1**.

---

## 3. Finding F-01 Reclassification

With structural enforcement proven at the PostgreSQL constraint level:
- Finding F-01 is reclassified as: **`REPAIRED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY`**.
- Shared staging and production remain unmutated and subject to future migration gating.
