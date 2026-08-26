# CAE Phase 19 (CA-TOPO-07) Target Admission Record and Scope Lock

**Phase ID:** `CA-TOPO-07`  
**Execution Authority:** CAE Governance & Specification Bridge Bundle v3; CA-TOPO-07 Mandate; Operator Selection of Option A (`DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET`)  
**Target Environment Class:** `DISPOSABLE_POSTGRESQL_ONLY`  
**Target Label:** `disposable_topo07_pg`  
**Target URL:** `postgresql://runner:***@127.0.0.1:5432/disposable_topo07_pg`  
**Data Classification:** `EMPTY_OR_SYNTHETIC_ONLY`  
**Teardown Owner:** `CA-TOPO-07 Execution Harness`  
**Date:** 2026-08-26  

---

## 1. Target Admission Rules Verification

| Admission Rule ID | Rule Requirement | Verification Result | Evidence / Details |
| :--- | :--- | :--- | :--- |
| **ADM-TOPO-01** | `DISPOSABLE_POSTGRESQL_ONLY` environment class | **PASS** | Target declared disposable with isolated lifecycle |
| **ADM-TOPO-02** | `EMPTY_OR_SYNTHETIC_ONLY` data classification | **PASS** | Zero real client/production/interview data admitted |
| **ADM-TOPO-03** | Shared Staging Endpoint Exclusion | **PASS** | Rejected signature `evnxdssbxxrsesftdvgx` / `.pooler.supabase.com` |
| **ADM-TOPO-04** | Production Hostname Exclusion | **PASS** | Rejected keywords `prod`, `production`, `live` |
| **ADM-TOPO-05** | Migration Draft Checksum Lock | **PASS** | Verified 8/8 draft checksums (`MIG-0001` through `MIG-0008`) |
| **ADM-TOPO-06** | F-01 Repair Predecessor Baseline | **PASS** | `MIG-0007` composite FK constraint verified in migration DAG |

---

## 2. Selected Option A Scope Lock

The operator has selected **Option A** (`DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET`):
- **Canonical Schema:** `CA_IMPL_UUID_FAMILY` (`cae.workspace`, `cae.workspace_membership`, `cae.guest_profile`, `cae.engagement`, `cae.media_asset`, `cae.receipt`, `cae.receipt_evidence_link`).
- **Legacy Quarantine:** `MIG-0008` renames legacy WP-03 tables to `legacy_wp03_workspace`, `legacy_wp03_media_asset`, and `legacy_wp03_execution_receipt`.
- **Canonical Route:** `register_verified_interview_source` mapped via `CanonicalInterviewSourceAdapter` into the canonical UUID schema with deterministic ID hashing, RLS context injection, and immutable receipt emission.

### Scope Lock File & Artifact Inventory

| Category | Allowed Files / Identifiers | Status |
| :--- | :--- | :--- |
| **Migration Drafts** | `0001` to `0008` in `packages/ca_runtime/src/ca_runtime/migrations/drafts/` | **LOCKED** |
| **Runner & Adapter** | `packages/ca_runtime/src/ca_runtime/migration_runner.py`<br>`scripts/cae/implementation/run_topo07_selected_proof.py` | **LOCKED** |
| **Documentation** | `docs/cae/implementation/CAE_TOPO_07_*.md` (6 files) | **LOCKED** |
| **Validators & Tests** | `scripts/cae/audit/verify_ca_topo_07.py`<br>`tests/cae/test_ca_topo_07_structure.py` | **LOCKED** |
| **Control State** | `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` | **LOCKED** |

---

## 3. Approved Migration Draft Checksums

```text
MIG-0001: 900ae2ee83c44c5ff0c08287752e505bfdfd11018c1fa8f760dff57335626244  0001_cae_extensions_and_schema.sql
MIG-0002: a84c781fe3cfa2a8f815049cf3fc07897c8cf3e2849e7552552a4209bf0b76be  0002_cae_tenancy_and_membership.sql
MIG-0003: eb936831d1ea1736e65eb3fce58d886fdfb55776c5b0f5b4a838be813d94a974  0003_cae_engagement_guest_media.sql
MIG-0004: 67bb8e376ea0a0662d08a54fc8ba8e67845f9a65d07c08bca0d3dd3d21b06803  0004_cae_harness_and_immutable_receipts.sql
MIG-0005: 78eb29ba0e5bfbda8d0d463dbe927a7c73a0c644efb4ec37059103e3a9a1476b  0005_cae_row_level_security.sql
MIG-0006: cf27329971bc391a3cf86981cfda55cf1c15f91ae4e84b1d6fbb59bf04b3a650  0006_cae_indexes_and_constraints.sql
MIG-0007: 09d3b41d2fb707ceee79e0bf81fec35832ea51d939634df81ea5d8d387ae88e0  0007_cae_f01_composite_receipt_fk_draft.sql
MIG-0008: 72e903a4658e45373da94a7322ebbc0628e833446c6fc3538dcbc60baefd57e2  0008_cae_f02_topology_shadow_reconciliation_draft.sql
```

---

## 4. Operational Boundaries & Non-Claims

1. **Staging & Production Isolation:** Zero connections were made to shared staging (`evnxdssbxxrsesftdvgx`), production, Supabase Storage, or SQLite databases.
2. **Operational Authority Unchanged:** `MC-CAE-MED-001` remains `POSTGRES_AUTHORITATIVE_STAGING_ONLY`. All other 21 aggregates remain SQLite-authoritative.
3. **Disposable Scope:** All proofs and tests executed exclusively within `disposable_topo07_pg` with synthetic fixtures.
