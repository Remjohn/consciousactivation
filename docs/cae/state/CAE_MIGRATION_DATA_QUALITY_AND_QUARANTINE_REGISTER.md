# CAE Migration Data Quality and Quarantine Register

**Document ID:** `CAE_MIGRATION_DATA_QUALITY_AND_QUARANTINE_REGISTER`  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Authority References:** `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER.md`, `CAE_WP04_REGISTRY_MIGRATION_PROOF.md`  

---

## 1. Governance and Quarantine Policy

In accordance with Bundle v3 doctrine and Mandate `CA-STATE-01`:
1. **No Silent Swallowing of Defects:** Any brownfield defect, integrity anomaly, missing lineage, unconsented identity match, or schema conflict MUST be explicitly recorded in this register and routed to a quarantined state.
2. **Quarantine is a Governed Outcome:** Classifying an entity as `QUARANTINE` is a valid, evidence-bearing outcome that protects production integrity.
3. **Strict Resolution Custody:** Moving an item out of quarantine requires an explicit remediation receipt signed by the designated operator authority.

---

## 2. Active Quarantine and Data Quality Register

| Quarantine ID | Defect Title & Severity | Affected Aggregate & Contract | Trigger Condition & Detection Logic | Defect Description & Risk Impact | Quarantine Route & Containment Behavior | Resolution Custody & Required Authority | Status |
|---|---|---|---|---|---|---|---|
| **`QUAR-SFL-001`** | SFL Missing Family Metadata<br>`HIGH` | `CA-REG-002` (SFL Registry)<br>`Out-of-Scope (Registry)` | Ingestion of `sfl.zip` detects 5 YAML files without declared `family` attributes (`005, 006, 007, 009, 012`). | Missing family metadata breaks perceptual modulation taxonomy and pipeline DAG dispatch. | The 5 defective assets are quarantined in `cae.quarantine_registry_item`; remaining 23 valid assets admitted. | Sensory Experience Lead & Canonical Ontology Committee | **`ACTIVE_QUARANTINE`** |
| **`QUAR-PRIM-001`** | Primitive Registry Duplicate Key<br>`HIGH` | `CA-REG-003` (Primitive Registry)<br>`Out-of-Scope (Registry)` | Ingestion of `PRIMITIVE_INVENTORY.csv` detects duplicate key `EXP-TRG-001`. | Duplicate primary key causes database collision and nondeterministic primitive resolution during AIR assessment. | Duplicate entry quarantined; first occurrence loaded with uniqueness lock; second flagged for manual review. | Primitive Registry Curator & Architecture Governance | **`ACTIVE_QUARANTINE`** |
| **`QUAR-GST-001`** | Cross-Workspace Guest Identity Collision<br>`CRITICAL` | `CA-ENT-003` (`Guest`), `CA-MAP-001`<br>`MC-CAE-GST-001` | Same participant email, name, or phone number encountered across distinct `workspace_id`s. | Automatic merging across workspaces violates tenant isolation and GDPR/privacy boundaries (`HN-STATE-003`). | Profiles are retained strictly workspace-local; cross-workspace link creation is quarantined and blocked. | Platform Compliance Officer + Bilateral Guest Cryptographic Consent | **`ACTIVE_QUARANTINE`** |
| **`QUAR-MED-001`** | Legacy Media Checksum / Byte Count Mismatch<br>`CRITICAL` | `CA-ENT-002` (`MediaAsset`), `CA-EVI-001`<br>`MC-CAE-MED-001` | Raw disk bytes SHA-256 or byte length differs from legacy source manifest payload (`HN-STATE-007`). | Indicates corrupted media file or mismatched source package; ingesting bad bytes invalidates evidence lineage. | Bridge immediately aborts upload; asset recorded in `cae.quarantine_media_asset`; transaction rolled back. | Media Ingestion Lead & Originating Interview Operator | **`ACTIVE_QUARANTINE`** |
| **`QUAR-ENG-001`** | Format 02 Deferred Campaign Order<br>`MEDIUM` | `CA-ENT-004` (`Engagement`)<br>`MC-CAE-ENG-001` | Campaign order specifies `category_id = "2d_character_animation"` or `format_profile_id` starting with `format02_`. | Format 02 is deferred pending a current validated Atomic Harness per `TS-APP-API-004` and `PRD-CAE-TEN-001`. | Order rejected with `FORMAT02_DEFERRED` exception; quarantined in `cae.legacy_import_record`. | Creative Production Lead & Architecture Governance | **`ACTIVE_QUARANTINE`** |
| **`QUAR-RLS-001`** | Orphan Operational Record Without Workspace Scope<br>`CRITICAL` | All Operational Aggregates<br>`All Contracts` | Ingestion encounter record with `workspace_id IS NULL`, empty string, or non-existent workspace reference. | Orphaned records violate RLS multi-tenant boundary and cause security leakage (`HN-STATE-002`). | Ingestion rejected immediately; record routed to `cae.quarantine_unscoped_record` with source trace. | Platform Security Officer & Workspace Admin | **`ACTIVE_QUARANTINE`** |

---

## 3. Quarantine Ingestion and Recovery Procedures

### 3.1 Automated Ingestion Containment
When an operational service or ingestion bridge encounters an anomaly matching any trigger condition above:
1. The active transaction MUST execute an immediate `ROLLBACK`.
2. A structured incident record is inserted into `cae.quarantine_record` capturing:
   - `quarantine_id`: Matching the registered defect identifier.
   - `source_identifier`: Exact brownfield locator / primary key.
   - `defect_payload`: Raw problematic JSON or byte hash.
   - `detected_at_utc`: Immutable timestamp.
   - `containment_state`: Set to `CONTAINED_UNRESOLVED`.
3. An audit event is emitted to `cae.event` at severity `WARNING` or `ERROR`.

### 3.2 Governed Operator Resolution Procedure
An item may be released from quarantine ONLY under the following protocol:
1. The designated authority inspects the defect and authors a formal remediation patch (e.g. corrected YAML, re-recorded audio file, or explicit bilateral consent receipt).
2. The patch is tested against the static verifier and staging test suite.
3. The operator issues an explicit remediation command with a cryptographic receipt reference.
4. The quarantine state is updated to `RESOLVED_WITH_RECEIPT`.

---

## 4. Verification and Non-Claims

1. **Zero-Movement Guarantee:** Authoring this register executes no live data purging or quarantine table creation in production.
2. **Static Verifier Coverage:** All 6 registered defects are tested and verified by `scripts/cae/state/verify_ca_state_01.py`.
