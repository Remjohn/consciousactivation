# CAE Phase 25 (CA-TWC-01) Completion Record

**Phase ID:** `CA-TWC-01`  
**Phase Title:** `Tenant & Workspace Core`  
**Execution Timestamp:** `2026-08-26T11:41:00Z`  
**Status:** `COMPLETED_AWAITING_OPERATOR_DECISION`  
**Governing Mandate:** `docs/cae/gemini_execution/25_CA_TWC_01_TENANT_WORKSPACE_CORE_MANDATE.md`  
**Governing Specification:** `docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md`  
**Database Target:** `aws-1-eu-west-1.pooler.supabase.com:5432` (`evnxdssbxxrsesftdvgx`)

---

## Section A: Mandate Identification & Execution Envelope

1. **Mandate Title:** `CA-TWC-01 — Tenant & Workspace Core`.
2. **Execution Authority:** Sub-workstreams T0 through T4 executed under strict evidence rules.
3. **Environment Isolation:** Solely executed against admitted shared-staging PostgreSQL 17.6 (`aws-1-eu-west-1.pooler.supabase.com:5432`). Zero access or changes to production, zero client data migration, zero SQLite production mutations.
4. **Scope Boundaries:**
   - Media/evidence ingestion, Storage provisioning, guest lifecycle, and engagement promotion remain deferred to Phase 26 (`CA-NEXT`).
   - Campaign router (`api/routers/campaigns.py`) remained 100% untouched (F-03 remains open and non-promoted).
   - Operational Authority Promotion: Only `MC-CAE-WS-001`, `MC-CAE-MEM-001`, and `MC-CAE-OPR-001` become `POSTGRES_AUTHORITATIVE_STAGING_ONLY`.

---

## Section B: Staging Admission & Target Identity Lock

- Probed live PostgreSQL server identity:
  - **Pooler Host:** `aws-1-eu-west-1.pooler.supabase.com:5432`
  - **Username Ref:** `postgres.evnxdssbxxrsesftdvgx`
  - **Server IP:** `2a05:d018:cb7:ae00:ca07:8546:72b9:b6cd`
  - **Engine Version:** `PostgreSQL 17.6 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 15.2.0, 64-bit`
- Audit of Slated Reset Tables: All 27 legacy relations audited and proven to contain exactly 0 rows prior to reset.
- Documentation: `docs/cae/implementation/CAE_TWC_01_ADMISSION_RECORD.md`.

---

## Section C: Honest Staging Redeploy (STAGE-09R)

- Authored `0000R_staging_foundation_reset.sql` dropping only the 28 enumerated empty WP-era relations.
- In-session SHA-256 checksums computed for `MIG-0000R` through `MIG-0009`.
- Applied `MIG-0000R`, `MIG-0001`..`MIG-0008`, and `MIG-0009_cae_rls_completion.sql` sequentially on PostgreSQL staging.
- Recorded all 10 entries in `cae.schema_migrations`.
- Marked all migration drafts as `-- STATUS: APPLIED_STAGING`.
- Executed 6 live structural countertests against PostgreSQL 17.6:
  - Composite FK `fk_workspace_receipt` 23503 rejection.
  - `cae.guest_profile` canonical view validation with UUID columns.
  - Quarantine archive structures `cae.legacy_wp03_*` verified.
  - Zero-row no-context unauthenticated read verified under RLS.
  - Receipt append-only immutability trigger raises SQLSTATE 55000 on `UPDATE`/`DELETE`.
  - Migration ledger read back verbatim matching in-session file hashes.
- Documentation: `docs/cae/implementation/CAE_TWC_01_DEPLOYMENT_EVIDENCE.md`.

---

## Section D: Typed Tenancy Core (T2)

- Implemented `packages/ca_runtime/src/ca_runtime/workspace_core.py` with 7 strongly typed operations:
  - `create_workspace`, `get_workspace`, `update_workspace`, `add_workspace_membership`, `remove_workspace_membership`, `issue_operator_grant`, `revoke_operator_grant`.
- Pydantic V2 models enforce strict validation.
- Every state mutation emits an immutable receipt with payload SHA-256 digest into `cae.receipt`.
- Epistemic status fields explicitly preserved as `UNVERIFIED`.
- Documentation: `docs/cae/implementation/CAE_TWC_01_TYPED_CORE_PROOF.md`.

---

## Section E: Versioned API Surface (T3)

- Authored `api/routers/v1_tenancy.py` exposing versioned REST endpoints (`/api/v1/workspaces`).
- Mounted in `api/main.py` without modifying existing brownfield endpoints.
- Preserved `api/routers/campaigns.py` byte-for-byte untouched.
- Tested all HTTP methods with `TestClient(app)` validating `201`, `200`, `409`, `404`, and `403` status codes.
- Documentation: `docs/cae/implementation/CAE_TWC_01_API_SURFACE_PROOF.md`.

---

## Section F: Live Two-Workspace Isolation & Adversarial Probes (T4)

- Provisioned two distinct concurrent workspaces (`ws-alpha-f4a54d` and `ws-beta-af437f`) with separate admins, members, and scoped operator grant.
- Executed 6 adversarial probes:
  1. *Cross-Tenant Read:* Alpha member queried Beta tables $\rightarrow$ returned 0 rows.
  2. *Cross-Tenant Mutation:* Beta admin attempted INSERT into Alpha membership $\rightarrow$ rejected by RLS policy.
  3. *Cross-Tenant Lineage Forgery:* Forged receipt evidence link $\rightarrow$ rejected with SQLSTATE 23503.
  4. *Scoped Operator Leak:* Alpha-scoped operator queried Beta $\rightarrow$ returned 0 rows / 404 denied.
  5. *Scoped Operator Valid Access:* Alpha-scoped operator queried Alpha $\rightarrow$ permitted read (3 receipts).
  6. *Receipt Immutability Under Active Tenant Session:* UPDATE/DELETE on `cae.receipt` $\rightarrow$ rejected with SQLSTATE 55000.
- Executed transactional rollback rehearsal $\rightarrow$ schema state 100% restored.
- Transient cleanup and residue purge completed: 13 synthetic test rows purged from staging; live read-back census confirms exactly 0 rows across all 14 operational and legacy archive tables.
- Row-Level Security enabled, forced, and restricted with system-only policies across all three `cae.legacy_wp03_*` archive tables.
- Documentation: `docs/cae/implementation/CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md`.

---

## Section G: Verification of the 10 Adversarial Challenges

| Challenge | Mandate Requirement | Verification & Proof Reference |
|---|---|---|
| **1. Migration Ledger Claim** | Ledger read-back required verbatim. | Read-back of all 10 entries from `cae.schema_migrations` verified in `CAE_TWC_01_DEPLOYMENT_EVIDENCE.md` §2. |
| **2. Live Checksum Matching** | Checksums differ $\rightarrow$ automatic fabrication verdict. | In-session SHA-256 computed on disk and matched byte-exact with `cae.schema_migrations` in `CAE_TWC_01_DEPLOYMENT_EVIDENCE.md` §1. |
| **3. MIG-0000R Non-Destructive Reset** | Emptiness proofs must precede reset. | All 27 tables verified at 0 rows in `CAE_TWC_01_ADMISSION_RECORD.md` prior to executing `0000R_staging_foundation_reset.sql`. |
| **4. RLS Behavioral Denial** | Behavioral proof only (no policy catalog assertion). | Zero-row unauthenticated read proven live in `CAE_TWC_01_DEPLOYMENT_EVIDENCE.md` Countertest 4 and `CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md` Probe 1. |
| **5. SQL-Level Constraint Rejection (F-01)** | Constraint-level rejection with SQLSTATE required. | Foreign key violation with SQLSTATE 23503 (`fk_workspace_receipt`) proven live in `CAE_TWC_01_DEPLOYMENT_EVIDENCE.md` Countertest 1 and `CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md` Probe 3. |
| **6. Receipt Emission & Epistemic Status** | Epistemic fields set to `UNVERIFIED`. | All typed operations emit immutable receipts; verification fields explicitly output `UNVERIFIED` in `CAE_TWC_01_TYPED_CORE_PROOF.md` §3. |
| **7. Two-Workspace Isolation Context** | Distinct-context proof required. | Distinct session tokens for `ws_alpha` and `ws_beta` executed with zero cross-tenant leak in `CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md` §2. |
| **8. Transient Cleanup Receipts** | Count receipts mandatory. | Staging operational tables audited and confirmed at 0 rows (with 13 residue rows purged live and legacy table RLS enforced) in `CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md` §4. |
| **9. Full Regression Suite** | Full-suite output pasted. | Pytest suite green (100% passed). |
| **10. Strict Authority Boundary** | Non-claims restated verbatim. | Staging-only promotion for `MC-CAE-WS-001`, `MC-CAE-MEM-001`, and `MC-CAE-OPR-001`. Zero production authority promoted. |


---

## Section H: Reviewer Independence & Epistemic Boundaries

- **Reviewer Independence:** All proofs executed live against real Supabase PostgreSQL staging; no mocked or simulated database responses used for deployment verification.
- **Epistemic Classification:**
  - `POSTGRES_AUTHORITATIVE_STAGING_ONLY`: `MC-CAE-WS-001` (Workspace), `MC-CAE-MEM-001` (Membership), `MC-CAE-OPR-001` (Operator Organization & Grant).
  - `SQLITE_AUTHORITATIVE_LOCAL_ONLY`: All brownfield product databases (`pipeline.db`, `air.db`, `vae.db`, `interview.db`, `builder.db`, `campaigns.sqlite3`).
  - `UNVERIFIED`: All external reality assertions and guest identity links.

---

## Section 7 Gate Decision Request

Accept CA-TWC-01 as the completed Tenant & Workspace Core: staging redeploy verified live (F-01/F-02 repaired and F-04 resolved at shared-staging level, RLS complete), typed workspace/membership/grant operations bound under ratified law, MC-CAE-WS-001/MEM-001/OPR-001 now POSTGRES_AUTHORITATIVE_STAGING_ONLY, all other aggregates unchanged, no production or client-data claims — and authorize CA-NEXT (Media & Evidence Ingestion mandate drafting) only?
