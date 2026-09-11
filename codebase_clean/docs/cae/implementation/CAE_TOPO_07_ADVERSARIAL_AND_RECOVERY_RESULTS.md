# CAE Phase 19 (CA-TOPO-07) Adversarial Countertests and Recovery Results

**Phase ID:** `CA-TOPO-07`  
**Execution Environment:** `disposable_topo07_pg` (`DISPOSABLE_POSTGRESQL_ONLY`)  
**Test Suite:** 12 Adversarial Countertests (`TOPO07-CT-01` to `TOPO07-CT-12`)  
**Status:** **12/12 PASSED (100% SUCCESS)**  
**Date:** 2026-08-26  

---

## 1. Adversarial Countertest Matrix & Results

| Test ID | Test Title | Objective | Result | Verification Details |
| :--- | :--- | :--- | :--- | :--- |
| **TOPO07-CT-01** | Migration Checksum Mismatch | Ensure runner rejects modified/corrupted migration drafts | **PASS** | Verified 8/8 checksums across `MIG-0001` through `MIG-0008` |
| **TOPO07-CT-02** | Prohibited Staging Identity | Ensure runner blocks connections to shared staging or prod | **PASS** | Rejected signature `evnxdssbxxrsesftdvgx.pooler.supabase.com` |
| **TOPO07-CT-03** | Canonical Schema Resolution | Verify Option A designates UUID family as sole canonical schema | **PASS** | Verified canonical tables active and legacy tables quarantined |
| **TOPO07-CT-04** | Legacy Route Fallthrough | Verify unadapted legacy raw text queries fail deterministically | **PASS** | Rejected invalid UUID input syntax (`22P02`) |
| **TOPO07-CT-05** | Adapter Parameter Validation | Verify adapter rejects malformed/missing required fields | **PASS** | Rejected empty `workspace_id` and non-SHA256 digests |
| **TOPO07-CT-06** | Canonical Operation Proof | Verify `register_verified_interview_source` writes UUID rows | **PASS** | Committed media row, receipt, and evidence link cleanly |
| **TOPO07-CT-07** | F-01 Composite FK Protection | Verify cross-workspace evidence link is structurally rejected | **PASS** | Rejected cross-workspace link with PostgreSQL `23503` |
| **TOPO07-CT-08** | RLS & Receipt Immutability | Verify no-context queries return 0 rows & mutation fails | **PASS** | 0 rows returned under NULL context; `EX_RECEIPT_IMMUTABLE` raised |
| **TOPO07-CT-09** | Idempotent Replay | Verify identical replay returns existing receipt with 0 new rows | **PASS** | Returned original receipt ID; 0 extra rows created |
| **TOPO07-CT-10** | Atomic Failure Rollback | Verify mid-flight failure rolls back all partial inserts | **PASS** | Missing engagement induced rollback; 0 ghost rows left |
| **TOPO07-CT-11** | Repeat Migration Idempotency | Verify repeat runner execution causes no schema drift | **PASS** | Manifest re-evaluation passed cleanly without drift |
| **TOPO07-CT-12** | Scoped Teardown | Verify complete purge of synthetic fixtures | **PASS** | 100% synthetic fixtures purged; zero residual state |

---

## 2. Failure Recovery & Atomic Rollback Proof

Countertest `TOPO07-CT-10` simulated a mid-flight database error during bridge execution by referencing a non-existent `engagement_id`.
- **Pre-condition:** `cae.workspace` seeded; `cae.engagement` intentionally absent.
- **Trigger:** Adapter attempted insertion and failed parent validation.
- **Recovery:** PostgreSQL `ROLLBACK` invoked by transaction context manager.
- **Post-condition:**
  - `SELECT count(*) FROM cae.media_asset` $\to$ `0`
  - `SELECT count(*) FROM cae.receipt` $\to$ `0`
  - `SELECT count(*) FROM cae.receipt_evidence_link` $\to$ `0`
- **Conclusion:** Mid-flight failures in the canonical bridge adapter leave zero unreferenced or partially committed ghost records.
