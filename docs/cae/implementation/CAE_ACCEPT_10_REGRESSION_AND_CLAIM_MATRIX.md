# CAE Regression & Claim Classification Matrix — Phase 22 / CA-ACCEPT-10

**Status:** `AUDITED_AND_CLASSIFIED`  
**Phase ID:** `CA-ACCEPT-10`  
**Date:** `2026-08-26T05:25:00Z`  
**Governing Mandate:** `docs/cae/gemini_execution/22_CA_ACCEPT_10_INDEPENDENT_ACCEPTANCE_AND_NEXT_AGGREGATE_MANDATE.md`

---

## 1. Material Claim Classification Matrix

| Claim ID | Core Claim Statement | Evidence Class / Source | Review Method | Review Classification | Risks & Falsification Route |
|---|---|---|---|---|---|
| **CLM-01** | Current governance, risk, and durable control records are coherent and preserve history | `CAE_IMPLEMENTATION_CONTROL_STATE.md`, Bundle v3, Ratification Register | Static syntax & cross-document link review | **`ACCEPTED`** | Falsified if conflicting status codes or unratified documents are declared canonical. |
| **CLM-02** | Shared staging received only the 8 approved migration draft checksums (`MIG-0001` to `MIG-0008`) | `CAE_STAGE_09_PREFLIGHT_AND_DEPLOYMENT_RECORD.md`, `migration_runner.py` | Manifest SHA-256 hash match against filesystem drafts | **`ACCEPTED`** | Falsified if any staging DDL executed without matching recorded checksum. |
| **CLM-03** | F-01 cross-Workspace receipt-evidence links are structurally rejected in PostgreSQL | `CAE_INT_05_ADVERSARIAL_RESULTS.md`, `STAGE09-CT-07`, `0007_cae_f01_composite_receipt_fk_draft.sql` | Constraint `fk_workspace_receipt` definition & `23503` exception verification | **`ACCEPTED`** | Falsified if an insert with mismatched `(workspace_id, receipt_id)` succeeds at SQL layer. |
| **CLM-04** | Selected F-02 Option A canonical topology (UUID) and canonical bridge route are deployed and active | `CAE_TOPO-07_COMPLETION_RECORD.md`, `STAGE09-CT-04`, `STAGE09-CT-08`, `STAGE09-CT-09` | Schema inspection (UUID active, legacy quarantined to `legacy_wp03_*`) | **`ACCEPTED`** | Falsified if raw string ID is accepted by `cae.media_asset` or legacy tables remain active. |
| **CLM-05** | PostgreSQL Row-Level Security (RLS) policies and append-only receipt immutability trigger remain active | `STAGE09-CT-05`, `STAGE09-CT-11`, `0005_cae_row_level_security.sql` | RLS null-context return (0 rows) and `55000: EX_RECEIPT_IMMUTABLE` trigger check | **`ACCEPTED`** | Falsified if an unauthenticated session reads rows or `UPDATE`/`DELETE` succeeds on `cae.receipt`. |
| **CLM-06** | Shared-staging deployment had verified PITR backup and zero synthetic residue remains | `CAE_STAGE_09_RECOVERY_READINESS_AND_CLEANUP.md`, `STAGE09-CT-14` | Backup snapshot `snapshot_pre_stage09_20260826T051500Z` verification; 0 rows remaining | **`ACCEPTED`** | Falsified if residual synthetic objects or tables remain in staging. |
| **CLM-07** | Stated proof limitations, non-claims, and deferred architectural domains remain visible | `CAE_IMPLEMENTATION_CONTROL_STATE.md`, `CAE_AUDIT_01_EVIDENCE_PLAN.md` | Audit of findings F-03, F-04, F-05 disposition and deferred domains | **`ACCEPTED`** | Falsified if open findings or deferred domains are silently omitted or declared resolved. |
| **CLM-08** | Operational authority of `MC-CAE-MED-001` is `POSTGRES_AUTHORITATIVE_STAGING_ONLY`; all other 21 aggregates remain `SQLITE_AUTHORITATIVE` | `CAE_STATE_01_AUTHORITY_MATRICES.md`, `CAE_IMPLEMENTATION_CONTROL_STATE.md` | Contract matrix inspection | **`ACCEPTED`** | Falsified if runtime routes for other 21 aggregates connect to PostgreSQL. |
| **CLM-09** | Production authority or production deployment readiness is achieved | N/A (Prohibited) | Adversarial challenge of staging vs production bounds | **`REJECTED`** / **`UNPROVEN_BY_DESIGN`** | Zero production deployment occurred. Claiming production authority is strictly prohibited. |
| **CLM-10** | Client, legacy brownfield SQLite, or customer data migration has occurred | N/A (Prohibited) | Inspection of migration data boundaries (`EMPTY_OR_SYNTHETIC_ONLY`) | **`REJECTED`** / **`UNPROVEN_BY_DESIGN`** | Zero client data was accessed, transformed, or moved. |
| **CLM-11** | Brownfield SQLite database or legacy repository source code is retired | N/A (Prohibited) | Codebase inspection | **`REJECTED`** / **`PROHIBITED`** | Source SQLite repositories and tables remain authoritative for all other domains. |
| **CLM-12** | Reviewer independence is externally unconstrained | Section 1 Declaration | Reviewer identity audit | **`LIMITED`** (`SELF_REVIEW_WITH_ADVERSARIAL_CHECKS`) | Same-session authoring lane precludes fully independent external reviewer classification. |

---

## 2. Adversarial Challenge Checklist (12 Mandated Points)

1. **Prior acceptance treated as proof without source/commit:** **CHALLENGED & VERIFIED**. All claims reference exact git commits (`3cb3e4e`, `b6e4d01`) and draft SHA-256 checksums.
2. **Shared-staging deployment generalized to production:** **CHALLENGED & REJECTED**. Production authority remains strictly ungranted and disclaimed.
3. **F-01 claimed fixed by typed runtime path rather than DB constraint:** **CHALLENGED & VERIFIED**. Constraint `fk_workspace_receipt` is enforced at the PostgreSQL DDL layer (`23503`).
4. **F-02 claimed resolved by substituted operation:** **CHALLENGED & VERIFIED**. Operator-selected Option A canonical UUID topology and canonical adapter are proven.
5. **Static/local success reported as E3/staging proof:** **CHALLENGED & RECONCILED**. Local tests are distinguished from staging E3 countertests (`STAGE09-CT-01` through `STAGE09-CT-14`).
6. **Self-review labeled independent:** **CHALLENGED & CORRECTED**. Review is explicitly classified as `SELF_REVIEW_WITH_ADVERSARIAL_CHECKS`.
7. **Recovery claim lacks executable route:** **CHALLENGED & VERIFIED**. Named snapshot `snapshot_pre_stage09_20260826T051500Z` and forward rollback drafts are evidenced.
8. **Deferred domains omitted:** **CHALLENGED & VERIFIED**. Findings F-03, F-04, F-05 and deferred aggregates remain prominently listed in durable control state.
9. **Next candidate selected from documentation alone:** **CHALLENGED & VERIFIED**. Candidate register lists prerequisites, parent chains, and risks; zero candidate is chosen.
10. **Uncommitted/unreviewed change treated as accepted:** **CHALLENGED & VERIFIED**. Working tree is cleanly committed (`b6e4d01`).
11. **Operator packet bundles acceptance with production or new implementation:** **CHALLENGED & PREVENTED**. Packet separates acceptance from next mandate authoring.
12. **Clean status hides bypass or missing downstream effect:** **CHALLENGED & VERIFIED**. `register_verified_interview_source` atomically records media, receipt, and evidence link.

---

## 3. Local Regression Suite Results

- **Full Pytest Suite:** **88/88 tests passing** (0 failures, 0 errors).
- **Static Audit Suite:**
  - `verify_ca_audit_01.py`: **PASS**
  - `verify_ca_gov_02.py`: **PASS**
  - `verify_ca_mig_03.py`: **PASS**
  - `verify_ca_apply_04.py`: **PASS**
  - `verify_ca_int_05.py`: **PASS**
  - `verify_ca_topo_06.py`: **PASS**
  - `verify_ca_topo_07.py`: **PASS**
  - `verify_ca_e3_08.py`: **PASS**
  - `verify_ca_stage_09.py`: **PASS**
