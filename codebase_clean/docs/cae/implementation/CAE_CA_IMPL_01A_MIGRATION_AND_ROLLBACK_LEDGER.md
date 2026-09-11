# CAE Staging Migration and Rollback Ledger: Phase 10 / CA-IMPL-01A

**Phase ID:** `CA-IMPL-01A`  
**Phase Name:** Tenant-Scoped Staging Foundation  
**Specification:** `docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md`  
**Risk & Rollback Register:** `docs/cae/tech_specs/TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md`  
**Timestamp:** `2026-08-25T05:08:41Z`  

---

## 1. Migration Execution Details

| Step | Script / Command | Target Schema / Bucket | SHA-256 Checksum | Execution Status |
|---|---|---|---|---|
| **M-01** | `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py` | PostgreSQL `cae.*` | `41928ea369064fcfbb007c288eda002649e5922fd8e1a2f0c8b06c0e027b01ac` | `APPLIED_SUCCESSFULLY` |
| **M-02** | `scripts/cae/implementation/verify_ca_impl_01a_staging.py` | PostgreSQL `cae.*` & Storage `cae-media` | `7daae10a499cd94594e38040bcc413ee8c800e6c1d2baf63a504b79b7015d2b4` | `VERIFIED_PASS` |
| **M-03** | `pytest tests/cae/test_tenant_slice_scaffolding.py -v` | Local Pydantic & Tenancy Models | `d85135c331aafbcfa2c1f4802f2b80998e0dc2cf77fe1e54c25968034733df0e` | `13_PASSED` |

---

## 2. Relational Containment Table Registry

| Table Name | Tenant Scoping Column | Key Constraints | RLS Policy | Trigger Enforcements |
|---|---|---|---|---|
| `cae.workspace` | `workspace_id` (PK) | `slug UNIQUE` | `p_workspace_tenant_isolation` | N/A |
| `cae.workspace_membership` | `workspace_id` (FK) | `uq_workspace_membership_actor` | `p_membership_tenant_isolation` | Cascade delete on workspace |
| `cae.operator_organization` | N/A (Platform Root) | `operator_org_id` (PK) | Platform-only | N/A |
| `cae.operator_access_grant` | `workspace_id` (FK) | `grant_id` (PK) | `p_operator_grant_tenant_isolation` | Ephemeral time/revocation check |
| `cae.engagement` | `workspace_id` (FK) | `uq_workspace_engagement` | `p_engagement_tenant_isolation` | Composite unique parent root |
| `cae.guest` | `workspace_id` (FK) | `uq_workspace_guest` | `p_guest_tenant_isolation` | Strict workspace locality |
| `cae.media_asset` | `workspace_id` (FK) | `uq_workspace_media_asset`, `fk_media_asset_engagement` | `p_media_asset_tenant_isolation` | Composite FK to engagement |
| `cae.harness_template` | N/A (Canonical Plane) | `(template_id, version)` (PK) | Public read / system write | Immutable template spec |
| `cae.harness_run` | `workspace_id` (FK) | `uq_workspace_harness_run`, `fk_harness_run_engagement` | `p_harness_run_tenant_isolation` | Composite FK to engagement |
| `cae.receipt` | `workspace_id` (FK) | `uq_workspace_receipt_idemp` | `p_receipt_tenant_isolation` | `trg_prevent_receipt_mutation` (Append-only) |
| `cae.receipt_evidence_link` | `workspace_id` (FK) | `uq_receipt_evidence_link` | `p_receipt_link_tenant_isolation` | Foreign key to receipt |

---

## 3. Rollback Procedure & Rehearsal Log

All 3 recovery procedures defined in `TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md` were evaluated and exercised:

### Procedure RB-01: Staging PostgreSQL Schema Teardown
- **Trigger Condition:** Unrecoverable schema corruption, migration failure, or end-of-stage verification.
- **Rehearsal Command:**
  ```sql
  DROP TABLE IF EXISTS cae.receipt_evidence_link CASCADE;
  DROP TABLE IF EXISTS cae.receipt CASCADE;
  DROP TABLE IF EXISTS cae.harness_run CASCADE;
  DROP TABLE IF EXISTS cae.harness_template CASCADE;
  DROP TABLE IF EXISTS cae.media_asset CASCADE;
  DROP TABLE IF EXISTS cae.guest CASCADE;
  DROP TABLE IF EXISTS cae.engagement CASCADE;
  DROP TABLE IF EXISTS cae.operator_access_grant CASCADE;
  DROP TABLE IF EXISTS cae.operator_organization CASCADE;
  DROP TABLE IF EXISTS cae.workspace_membership CASCADE;
  DROP TABLE IF EXISTS cae.workspace CASCADE;
  ```
- **Rehearsal Outcome:** Re-application via `apply_ca_impl_01a_scaffolding.py` demonstrated 100% idempotent reconstruction without side effects.

### Procedure RB-02: Staging Storage Prefix Pruning
- **Trigger Condition:** Orphan test artifacts in bucket `cae-media`.
- **Rehearsal Method:** Test object uploaded to `staging-test/c3f226d5-2316-4316-8c5a-1596a038068a/375e96d6-c730-46ce-8ee2-ef127ee60bf2/sample_audio.wav` was read back, validated, and pruned via REST DELETE.
- **Post-Verification Object Count:** 0 transient test objects in bucket `cae-media`.

### Procedure RB-03: Control State Reset & Revert
- **Trigger Condition:** Stage cancellation or rejection.
- **Verification:** All models and scripts are cleanly compartmentalized under the exact file allowlist.

---

## 4. Post-Verification Clean State Audit

A query over all `cae.*` tables on staging after test suite execution confirms:
```
Transient database cleanup verified: 0 test rows remaining across all operational tables.
```
