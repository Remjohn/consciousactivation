# CA-IMPL-02 Reconciliation Ledger — `MC-CAE-MED-001`

**Phase ID:** `CA-IMPL-02`
**Document ID:** `CAE_CA_IMPL_02_MC_CAE_MED_001_RECONCILIATION_LEDGER`
**Status:** `RECONCILED_ZERO_MISMATCH`
**Date:** 2026-08-25
**Contract:** `CA-STATE-01_MEDIA_ASSET_AUTHORITY_MIGRATION_CONTRACT.md` (SHA-256 `03200cea77c9625e…`)
**Hard negative honored:** `HN-TS-008` — count-only reconciliation is forbidden; every relation below is field-, scope-, and lineage-aware.

---

## 1. Reconciliation Method

The reconciler (`reconcile_media_records` in the phase verifier) compares **expected** (transform manifest + typed-op
results) against **observed** (independent RLS-scoped SQL reads of `cae.media_asset` + receipt/lineage existence), row by
row and field by field. It emits typed mismatches only:

| Mismatch check | Meaning |
|---|---|
| `SCOPE_SWAPPED` | two rows with exchanged workspace attribution (even when totals match) |
| `FIELD_MISMATCH:<field>` | per-field divergence: id, scope, hash, size, mime, path, lifecycle state |
| `MISSING_TARGET_ROW` | expected VERIFIED asset absent from target (downstream-effect loss) |
| `UNEXPECTED_TARGET_ROW` | target contains a row outside the admitted manifest |
| `LINEAGE_MISSING_RECEIPT` | registered asset without its verify receipt |

Hashes are re-derived by **fresh reads of object bytes from private storage**, never from the manifest claim.

## 2. Canonical Run Relations (2026-08-25)

| Relation | Expected | Observed | Verdict |
|---|---|---|---|
| Registered media assets (Alpha + Beta) | 2 | 2 | MATCH (field-by-field, not count-only) |
| Fresh-read SHA-256 parity vs stored `canonical_sha256` | equal for all | equal for all 2 | MATCH |
| Workspace attribution per asset | Alpha→Alpha, Beta→Beta | identical | MATCH, no swap |
| Lifecycle states | `VERIFIED`, `VERIFIED` | `VERIFIED`, `VERIFIED` | MATCH |
| Verify receipts per registered asset | exactly 1 each | exactly 1 each (`rcpt_cae_media_verify_8ce287fda38a3f15ed036f6b`, `rcpt_cae_media_verify_732d24e191e0c5ef650257f0`) | MATCH |
| Orphan VERIFIED assets (contract §5 parity SQL) | 0 | 0 | CLEAN |
| Broken / cross-scope lineage links (contract §5 parity SQL) | 0 | 0 | CLEAN |
| Cutover transition receipts | exactly 1 | exactly 1 (`rcpt_cae_receipt_commit_1610201dbaba990e71a6b1b2`) | MATCH |

## 3. Adversarial Reconciliation Controls

The reconciler was proven capable of detecting failure before being trusted to report success:

- **Swapped-scope control (CT-01):** exchanging the two records' `workspace_id` values with byte-identical totals yields
  exactly one `SCOPE_SWAPPED` mismatch — proving totals-blindness.
- **Ghost-row control (CT-09):** an expectation row absent from the target yields `MISSING_TARGET_ROW`.
- **Lineage control (CT-06):** a forged cross-workspace link inserted via raw SQL is flagged by the parity relation
  (broken-link count ≥ 1) and returns to zero after repair. See finding F-01 in the cutover proof for the honest schema
  fidelity limitation this exposed.
- **Divergence control (Stage 5):** tampering an expectation's hash flags `FIELD_MISMATCH:canonical_sha256`;
  the independent fresh-read then restores the safe observed truth.

## 4. Ledger Closure

Final reconciliation state at proof close: **all relations MATCH/CLEAN, zero open mismatches**, transient fixtures pruned,
operational tables returned to zero rows for the phase's scoped workspaces (verified by Stage 7 assertions). This ledger
records reconciliation of the **pending-transition** state only; it does not assert promoted authority.
