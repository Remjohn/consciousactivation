# CAE WP-10A Regression and Verification Ledger

**Status:** `AUDITED_AND_VERIFIED`  
**Work Package:** `WP-10A — Vertical-Slice Evidence Containment and Acceptance`  
**Execution Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/01_WP10A_EVIDENCE_CONTAINMENT_MANDATE.md`  
**Executing Agent:** Antigravity / Gemini 3.7 Flash (High)

---

## 1. Executed Verification Ledger

| Command | Purpose | Exit Status | Environment Class | Mutation / Rollback Behavior | Cleanup Outcome | Observed Limitations |
|---|---|:---:|---|---|---|---|
| `python scripts/cae/verify_wp05_specs.py` | Verify Phase 5–7 requirement classification, first-slice Tech Spec `TS-CAE-EVID-001` section coverage, and trace matrix integrity. | `0` (PASS) | `STATIC_WORKSPACE` | Read-only static AST / Markdown parser. No database or filesystem mutations. | N/A (Read-only) | Validates document structure and traceability only; does not validate runtime implementation or database application. |
| `python scripts/cae/verify_wp06_runbook.py` | Verify runbook YAML and Skill Markdown identity, states, recovery rules, and contract bindings against staging database. | `0` (PASS) | `STATIC_WORKSPACE` + `E3_STAGING_SESSION_POOLER` | Read-only SQL queries on `cae.semantic_operation` and `cae.state_transition_contract`. No mutations. | N/A (Read-only) | Validates procedural doctrine and registered schema contract alignment; does not execute an agent orchestrator or JIT compiler. |
| `python scripts/cae/verify_foundation_structure.py` | Verify presence of 22 required CAE foundation tables, private bucket access settings, and foreign-key enforcement on `cae.evidence_span`. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | `connection.transaction(force_rollback=True)` around orphan FK insert test. | Zero test rows persisted; tables verified. | Structural verification only; does not verify live application write paths or dynamic multi-tenant auth policies. |
| `python scripts/cae/verify_private_storage.py` | Verify private bucket upload, authorized SHA-256 readback, and unauthenticated read denial on `cae-media`. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | Uploads temporary object `proof/wp02a/{uuid}.txt`. Deletes in `finally` block. | `DELETE` request verified; 0 orphaned objects in `cae-media` bucket. | Validates storage provider privacy and server-key authorization; does not test signed URL generation or client browser upload. |
| `python scripts/cae/verify_wp03_first_slice.py` | Verify 5 first-slice semantic operations, transition contracts, immutability triggers, optimistic concurrency, and tamper rejections. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | Uploads temporary source object to `cae-media`. Wraps all DB fixtures and operations in `connection.transaction(force_rollback=True)`. Deletes storage object in `finally`. | 0 rows retained in `cae` transient tables; temporary storage object deleted. | Exercises isolated adapter; no write cutover from legacy SQLite services; validation is lifecycle governance without SDA/SFL scoring. |
| `python scripts/cae/verify_wp04_registry_migration.py` | Verify SDA (13), SFL (28), and Primitive (243) archive counts, archive hashes, active graph (67), quarantined references (6), resolver behavior, and immutability. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | Read-only queries and resolver checks; mutation rejection tested in `connection.transaction(force_rollback=True)`. | Zero fixture mutations; quarantine status preserved. | Staging registry tables only; no brownfield service runtime uses `RegistryResolver`; missing SFL families remain unresolved. |
| `python scripts/cae/verify_wp07_receipt_lineage.py` | Verify execution receipt generation, evidence linkage, immutability triggers, false reference rejection, and `v_receipt_evidence_lineage` view. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | Wraps all execution in `connection.transaction(force_rollback=True)` and deletes temporary storage object in `finally`. | Zero fixture rows retained; temporary storage object deleted. | Proves database-level evidence lineage; explicit non-claims maintained (`reward_hack_result: UNVERIFIED`, `taste_integrity: NOT_APPLICABLE`). |
| `python scripts/cae/verify_wp08_reality_contact.py` | Verify governed E3 test suite against live private storage byte readback, unverified asset rejection, idempotency conflicts, unauthenticated assessment rejection, and empty operator decision rejection. | `0` (PASS) | `E3_PRODUCTION_SHAPED_DISPOSABLE_STAGING` | Uploads temporary object, reads back and hashes remote bytes, executes 5-step path and 6 negative paths in forced-rollback transaction, deletes object in `finally`. | 0 domain side-effects persisted; temporary storage object deleted. | Governed E3 operational/structural proof only; does not evaluate human truth, semantic direction quality, or E4 audience outcomes. |
| `python scripts/cae/verify_wp09_interview_source_bridge.py` | Verify read-only bridge from real Interview Expression SQLite repository fixture to CAE staging storage, typed source registration, tamper rejections, and capture compatibility. | `0` (PASS) | `E2_REPOSITORY_INTEGRATED` + `E3_PRODUCTION_SHAPED` | Constructs temporary directory with SQLite database and local media files; verifies and copies bytes to private Storage; executes registration in forced-rollback transaction; deletes storage object in `finally`. | Temporary directory auto-cleaned; temporary storage object deleted; legacy SQLite source unchanged. | Tests isolated repository fixture; no API route calls bridge; legacy SQLite authority not retired; transcript component reconciliation out of scope. |

---

## 2. SQL Migration Checksum Verification

| File | Recorded Checksum (SHA-256) | Computed File Checksum (SHA-256) | Database Ledger Status (`cae.schema_migrations`) | Result |
|---|---|---|---|:---:|
| `0001_cae_foundation_draft.sql` | `b9ac25e8bd81abab2f01af828d3ab209b4d2e7308a2f698272f720e944430b91` | `b9ac25e8bd81abab2f01af828d3ab209b4d2e7308a2f698272f720e944430b91` | `APPLIED` (2026-08-24 01:03:58 UTC) | MATCH |
| `0002_cae_workspace_rls.sql` | `6067550621e78a3aa4f645e84e9be34b907df4441cd0d1851a1b8c8bc28d095d` | `6067550621e78a3aa4f645e84e9be34b907df4441cd0d1851a1b8c8bc28d095d` | `APPLIED` (2026-08-24 01:21:02 UTC) | MATCH |
| `0003_cae_immutable_evidence_payloads.sql` | `3d331989fd74af1ccfec71d6087b481f4369debe5045d4e7d4dbaed1c1373124` | `3d331989fd74af1ccfec71d6087b481f4369debe5045d4e7d4dbaed1c1373124` | `APPLIED` (2026-08-24 01:39:15 UTC) | MATCH |
| `0004_cae_first_slice_semantic_operations.sql` | `ad6ccc6f08d3e46cfdff42fc9a2be52b9998eea4c62a21fa9c044c5a4c69df8d` | `ad6ccc6f08d3e46cfdff42fc9a2be52b9998eea4c62a21fa9c044c5a4c69df8d` | `APPLIED` (2026-08-24 01:43:28 UTC) | MATCH |
| `0005_cae_registry_authority.sql` | `9a7724013676b08cc4f0cb454bfb7aef0d075a90cbd58808cb59fd718a8d1793` | `9a7724013676b08cc4f0cb454bfb7aef0d075a90cbd58808cb59fd718a8d1793` | `APPLIED` (2026-08-24 02:42:53 UTC) | MATCH |
| `0006_cae_registry_reference_classifier_correction.sql` | `20c6f9605ff3f9f372a763a6dc327cc15ba3651ce03a6d6a86a5eb4425670a7f` | `20c6f9605ff3f9f372a763a6dc327cc15ba3651ce03a6d6a86a5eb4425670a7f` | `APPLIED` (2026-08-24 02:47:05 UTC) | MATCH |
| `0007_cae_registry_reference_classifier_v2.sql` | `94352d602539bfe44071a204b665facafa53b453d334c3c597245bd7ee301447` | `94352d602539bfe44071a204b665facafa53b453d334c3c597245bd7ee301447` | `APPLIED` (2026-08-24 02:48:09 UTC) | MATCH |
| `0008_cae_execution_receipt_lineage.sql` | `8902468b434dd8dc081446d138d3305ff5c55f9f419d89dce8f81956ac0083cc` | `8902468b434dd8dc081446d138d3305ff5c55f9f419d89dce8f81956ac0083cc` | `APPLIED` (2026-08-24 03:15:29 UTC) | MATCH |
| `0009_cae_interview_source_bridge_operation.sql` | `26a3b4c08e90d4845612ae6263c1850ac5cfa5d23e7664547c01f1697a24e9a0` | `26a3b4c08e90d4845612ae6263c1850ac5cfa5d23e7664547c01f1697a24e9a0` | `APPLIED` (2026-08-24 04:00:11 UTC) | MATCH |

---

## 3. Post-Execution Database and Storage Cleanup Audit

Direct SQL and REST queries against the Supabase staging project after all verification runs confirmed:

- **Transient database rows:** `0` rows in `cae.workspace`, `cae.actor`, `cae.media_asset`, `cae.source_package`, `cae.command`, `cae.event`, `cae.receipt`, `cae.execution_receipt`, `cae.receipt_evidence_link`, `cae.evidence_item`, and `cae.semantic_assessment`.
- **Durable registry records:** `3` snapshots, `284` total imported items (with 7 quarantined), `553` references (`67` active, `6` quarantined unresolved, `486` dispositioned artifacts), `35` integrity issues, `6` semantic operations registered, `6` active transition contracts.
- **Storage bucket residue:** `0` objects in `cae-media`; `0` objects in `cae-artifacts`.

---

## 4. Inspections Deliberately Not Run and Rationale

1. **Brownfield Test Suite Execution (`pytest` across 70 existing test files):**
   - *Rationale:* Governed brownfield tests belong to separate SQLite-backed service lifecycles (Pipeline, VAE, AIR, Campaign, Builder). Mandate Section 1 and Section 5 forbid executing wide unit suites that could mutate local SQLite databases or create false impressions of global test coverage.
2. **Migration Scripts Execution (`apply_*.py`):**
   - *Rationale:* All 9 migrations are already in `APPLIED` state with verified checksums. Running migration apply scripts without schema changes is unnecessary and risks attempting duplicate migrations or mutating ledger timestamps.
3. **Registry Import Execution (`import_wp04_registries.py`):**
   - *Rationale:* Staging registry tables already hold the immutable snapshots from WP-04. Re-importing would attempt duplicate snapshot insertions against immutable tables.
4. **Live API Integration / HTTP Endpoint Calls:**
   - *Rationale:* No API route is authorized to call the CAE bridge or semantic operations. Calling API routes would test brownfield SQLite paths rather than the isolated CAE vertical slice.
5. **E4 Human / Semantic Quality Evaluations:**
   - *Rationale:* E4 evaluations require live human subjects, external audience feedback, and ratified semantic evaluators. Neither evaluators nor human subjects exist in this phase.
