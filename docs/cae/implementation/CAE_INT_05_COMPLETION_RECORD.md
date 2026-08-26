# CAE Completion Record — Phase 17 / CA-INT-05

**Work Package:** `CA-INT-05 — F-01 Workspace/Receipt Evidence-Lineage Integrity Repair and Proof`  
**Governing Mandate:** `docs/cae/gemini_execution/17_CA_INT_05_WORKSPACE_RECEIPT_LINEAGE_INTEGRITY_MANDATE.md`  
**Execution Date:** 2026-08-26  
**Agent ID:** `ox-alpha / ZCode (CAE Governed Execution Agent)`  
**Git Commit:** `Pending Stage & Commit`  
**Operational Authority Status:** `ZERO_AUTHORITY_CHANGED` (`MC-CAE-MED-001` remains `POSTGRES_AUTHORITATIVE_STAGING_ONLY`; all other 21 aggregates remain SQLite-authoritative)  

---

## A. What Changed in the Disposable Target and Why

In the isolated disposable environment `disposable_f01_repair_pg`, migration draft `MIG-0007` (`0007_cae_f01_composite_receipt_fk_draft.sql`) was applied on top of baseline migrations `MIG-0001` through `MIG-0006`. This replaced the single-column foreign key `fk_receipt` with a native composite foreign key `fk_workspace_receipt` on `cae.receipt_evidence_link(workspace_id, receipt_id)` referencing `cae.receipt(workspace_id, receipt_id)` with `ON DELETE RESTRICT`.

This provides native PostgreSQL constraint enforcement that structurally rejects any cross-Workspace evidence linkage before a row can be created, eliminating reliance on compensating typed-operation checks or post-hoc parity sweeps.

---

## B. Tests, Environment, and Evidence Captured

1. **Environment:** Admitted isolated target `disposable_f01_repair_pg` (`DISPOSABLE_POSTGRESQL_ONLY`, `EMPTY_OR_SYNTHETIC_ONLY`).
2. **Harness & Runner:** `GuardedMigrationRunner` with preflight check for parent composite key and pre-existing cross-workspace link detection.
3. **Countertest Matrix:** All 11 adversarial countertests (`F01-CT-01` through `F01-CT-11`) executed and passed via `scripts/cae/implementation/run_f01_repair_proof.py`.
4. **Direct Structural Proof:** Under a privileged proof role, direct cross-Workspace link insertion (`workspace_id=B`, `receipt_id=A`) was rejected by PostgreSQL with error code `23503` (`fk_workspace_receipt`), resulting in 0 rows inserted. Positive insertion (`workspace_id=A`, `receipt_id=A`) succeeded with 1 row inserted.
5. **Defense Retention:** Trigger `trg_receipt_append_only` and RLS policies `p_*` remained active and fully enforced.

---

## C. What Failed or Remained Unproven

1. **Shared Staging / Production Execution:** `MIG-0007` was NOT applied to shared staging (`evnxdssbxxrsesftdvgx`) or production.
2. **Table Family Shadowing (F-02):** The WP-03 text-keyed vs CA-IMPL uuid-keyed table duality remains untouched and open (`F02_OPEN`).

---

## D. Cleanup and Teardown Result

All synthetic fixtures created during testing were purged. Teardown attestation confirmed zero database residue in the disposable target and zero connection to shared staging, production, or SQLite databases.

---

## E. F-01 and F-02 Status

- **F-01 (Lineage Link Composite FK):** `REPAIRED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY`.
- **F-02 (Staging Schema Shadowing):** `STILL_OPEN` (owned by upcoming Phase 18 / `CA-TOPO-06`).
- **F-03 (API Router Bypass):** `STILL_OPEN` (owned by CA-API-01).
- **F-04 (Scaffolding DDL):** `STILL_OPEN` (owned by Migration Governance).
- **F-05 (Quarantined Registries):** `STILL_OPEN` (owned by Lineage Governance).

---

## F. Risks and Non-Claims

1. **Zero Authority Escalation:** This proof does not promote `MC-CAE-MED-001` or any other aggregate to production, nor does it grant PostgreSQL authority to remaining aggregates.
2. **Staging Boundary:** Applying `MIG-0007` to shared staging requires explicit operator authorization and preflight verification that zero existing inconsistent links exist.

---

## G. Exact Next Authorization Requested

The agent requests the exact Section 6 operator decision:

> **Accept CA-INT-05 as disposable-environment proof that F-01 is structurally rejected by the exact approved forward migration, preserve F-02 and all shared-staging/production limitations, and authorize CA-TOPO-06 only to reconcile and prove the WP-03 versus CA-IMPL table-family topology—without applying F-01 to shared staging or changing operational authority?**
