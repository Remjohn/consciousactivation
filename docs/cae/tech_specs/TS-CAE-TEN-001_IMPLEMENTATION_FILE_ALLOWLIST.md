# TS-CAE-TEN-001 Implementation File Allowlist & Boundary Register

**Document ID:** `TS-CAE-TEN-001_IMPLEMENTATION_FILE_ALLOWLIST`  
**Phase ID:** `CA-TS-01`  
**Status:** `READY_FOR_DEVELOPMENT` (Governing `CA-IMPL-01A` Only)  
**Date:** 2026-08-25  
**Author:** CAE Governed Execution Agent (Gemini 3.7 Flash High / Antigravity)  
**Governing Mandates:** `09_CA_TS_01_IMPLEMENTATION_GATE_TECH_SPEC_MANDATE.md`, `10_CA_IMPL_01A_TENANT_FOUNDATION_MANDATE.md`  

---

## 1. Executive Implementation Boundary

This document defines the strict, exhaustive file allowlist for the upcoming **`CA-IMPL-01A` Tenant Foundation & Staging Containment** implementation phase.

### Governing Rules
1. **Zero-Creep Law:** The implementing agent in `CA-IMPL-01A` MAY create or modify ONLY the explicitly enumerated files in Section 2.
2. **Prohibition on Legacy Code Modification:** No legacy service runtime (`services/pipeline/`, `services/interview/`, `services/air/`, `services/vae/`), legacy database (`*.db`), or production infrastructure file may be altered.
3. **Staging Containment Only:** All SQL DDL, RLS policies, and Storage bucket configurations must target disposable staging environments only.

---

## 2. Explicit Allowed Files for `CA-IMPL-01A`

| Action | Relative File Path | Component Scope & Responsibility |
|---|---|---|
| **`NEW`** | `packages/ca_runtime/src/ca_runtime/models/tenant_slice.py` | Pydantic v2 typed data models for Workspace, Membership, OperatorOrg, Grant, Engagement, Guest, MediaAsset, HarnessRun, Receipt, and ReceiptEvidenceLink. |
| **`NEW`** | `packages/ca_runtime/src/ca_runtime/tenancy.py` | Tenant context manager, JWT claim extraction, and PostgreSQL RLS session variable helpers (`set_config('app.current_workspace_id', ...)`). |
| **`EXTEND`** | `packages/ca_runtime/src/ca_runtime/database.py` | Add helper methods for tenant-isolated PostgreSQL connection pooling and transaction lifecycle. (Zero breaking changes to SQLite methods). |
| **`NEW`** | `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py` | Standalone staging migration script applying schema `cae.*`, RLS policies, and triggers on disposable Supabase instances. |
| **`NEW`** | `scripts/cae/implementation/verify_ca_impl_01a_staging.py` | Automated staging verifier testing RLS isolation, foreign key constraints, byte readback, and hard negatives `HN-TS-001` through `HN-TS-011`. |
| **`NEW`** | `tests/cae/test_tenant_slice_scaffolding.py` | Unit and integration pytest suite executing against local models and staging test database. |
| **`NEW`** | `docs/cae/implementation/CAE_CA_IMPL_01A_COMPLETION_RECORD.md` | Formal phase completion and evidence handoff record. |
| **`MODIFY`** | `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` | Control state tracking update. |

---

## 3. Explicitly Prohibited Files and Directories

The following directories, files, and systems are STRICTLY PROHIBITED from modification during `CA-IMPL-01A`:

```text
[ STRICTLY PROHIBITED DIRECTORIES & FILES ]
├── api/main.py                              (API router changes deferred to later integration)
├── api/domain/**                            (Legacy campaign domain models retained untouched)
├── api/services/**                          (Legacy SQLite repositories retained untouched)
├── services/pipeline/**                     (cmf_pipeline service retained untouched)
├── services/interview/**                    (Interview service & SQLite DB retained untouched)
├── services/air/**                          (AIR qualitative engine retained untouched)
├── services/vae/**                          (VAE engine retained untouched)
├── services/studio/**                       (Studio frontend retained untouched)
├── inherited_registries/**                  (SDA, SFL, and Primitive registries are read-only)
├── storage/harness-library/**               (Runbook library changes deferred)
└── *.db, *.sqlite, *.sqlite3                (All legacy SQLite databases are write-prohibited)
```

---

## 4. What `CA-IMPL-01A` Proves vs. Non-Claims

### 4.1 What `CA-IMPL-01A` Proves
- **Staging Multi-Tenant Containment:** PostgreSQL RLS and composite foreign keys isolate data between distinct `workspace_id` contexts.
- **Private Storage Boundaries:** Content-addressed file uploads under `storage://cae-media/{workspace_id}/...` with SHA-256 integrity verification.
- **Typed Model Scaffolding:** Strongly typed Pydantic v2 schemas and context propagation.
- **Deterministic Hard-Negative Defense:** Proof that scope forgery, RLS bypass, and unverified paths are rejected.

### 4.2 Explicit Non-Claims for `CA-IMPL-01A`
- **Zero Production Parity:** Does NOT cut over production traffic or deprecate SQLite databases.
- **Zero Data Migration:** Does NOT migrate legacy single-tenant campaign or interview records.
- **Zero Semantic / Taste Evaluation:** Does NOT evaluate qualitative insight truth, SDA directions, SFL perceptual quality, or human world outcomes.
