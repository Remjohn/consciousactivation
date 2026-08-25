# CAE Aggregate Authority & Migration Contract: Media Asset & Evidence Lineage

**Contract ID:** `MC-CAE-MED-001`  
**Aggregate ID:** `CA-ENT-002` (`MediaAsset`), `CA-EVI-001` (`ImmutableMediaEvidence`), `CA-REL-004` (`SourcePackage`), `CA-EVI-002` (`EvidenceItem`), `CA-REL-003` (`EvidenceSpan`), `CA-REC-003` (`EvidenceAuthentication`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01B_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-009`, `FR-CAE-TEN-010`, `FR-CAE-TEN-011`  
**First Cutover Candidate:** `YES — RECOMMENDED FIRST CUTOVER CANDIDATE`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-MED-001"
  aggregate_name: "MediaAssetAndEvidence"
  single_aggregate_verified: true
  primary_class: "Entity / Immutable Evidence / Relation"
  plane: "OPERATIONAL_PLANE"
  recommended_disposition: "MIGRATE"
  current_authority_state: "DUAL_VERIFY"
  zero_data_movement_guaranteed: true
  execution_action_permitted: false
  recovery_procedure_defined: true
  contract_status: "CONTRACT_RATIFIED_SPEC_ONLY"
  is_first_cutover_candidate: true
```

---

## 1. Authority Axes Deconstruction

| Authority Axis | Specification & Provenance | Evidence Reference |
|---|---|---|
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.5; `CA-CAN-01B_CONSTITUTION.md` §3; Builder ADR-003; Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`. Defines media assets as immutable binary payloads paired with relational metadata and evidence spans. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | Legacy local filesystem (`interviews/{workspace}/{project}/...`) and SQLite `services/interview/` `ie_objects` / `ie_edges`. | `[EXECUTABLE]` `packages/ca_runtime/src/ca_runtime/interview_source_bridge.py:53-100` |
| **Target Runtime Representation** | PostgreSQL relational tables (`cae.media_asset`, `cae.source_package`, `cae.evidence_item`, `cae.evidence_span`, `cae.evidence_authentication`) and private Supabase Storage bucket `cae-media` with SHA-256 content addressing. | `[SCHEMA]` `sql/0003_cae_immutable_evidence_payloads.sql:1-45` |
| **Change & Promotion Authority** | Typed semantic operations: `register_verified_interview_source` (STC-BRIDGE-000), `capture_evidence` (STC-EVID-000), `authenticate_evidence` (STC-EVID-001). | `[EXECUTABLE]` `packages/ca_runtime/src/ca_runtime/semantic_operations.py:111-205` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** `Workspace` (`workspace_id`) -> `MediaAsset` (`asset_id`) -> `SourcePackage` (`source_package_id`) -> `EvidenceItem` (`evidence_id`) -> `EvidenceSpan` (`span_id`).
- **Subordinate Relational Chain:** `EvidenceItem` -> `EvidenceAuthentication` (`auth_id`, distinct evaluator actor required).

### Identity Mapping Rules
- **Media Asset Identity:** `cae:media:ie:{bridge_identity}` derived from deterministic hash `canonical_sha256({"upstream_source_ref": upstream_ref, "content_sha256": content_sha256})[:32]`.
- **Storage Object Key:** `cae/interview-expression/{bridge_identity}/{content_sha256}.bin`.
- **Evidence Item Identity:** `deterministic_id("evi", {workspace_id, source_package_id, byte_range, content_sha256})`.
- **Storage Verification Law (`HN-STATE-007`):** Copying a storage key or URL without reading back binary bytes and asserting `hashlib.sha256(bytes).hexdigest() == expected_sha256` is strictly PROHIBITED. The bridge enforces byte readback on existing keys before registering metadata.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY`
- **Entry Criteria:** Media files stored on local disk; metadata in local interview SQLite.
- **Read Path:** Direct file reads from local disk path.
- **Write Path:** Direct file writes to local filesystem directory.
- **Receipt Requirement:** Local file SHA-256 in SQLite `ie_objects`.
- **Exit Criteria:** Storage bucket `cae-media` provisioned; `InterviewExpressionSourceBridge` authored.

### Stage 2: `DUAL_VERIFY` (Current Staging State)
- **Entry Criteria:** `cae_runtime.interview_source_bridge` validated in staging with live Supabase Storage (`CAE_WP09_VERTICAL_SLICE_PROOF.md`).
- **Read Path:** Legacy services read local files; CAE services read Supabase Storage with SHA-256 verification.
- **Write Path:** Bridge copies legacy media bytes to Supabase Storage with atomic rollback on metadata failure.
- **Receipt Requirement:** Storage upload receipt + `cae.receipt` transaction receipt from `register_verified_interview_source`.
- **Exit Criteria:** 100% byte-exact parity across 50 staging test assets; operator cutover authorization.

### Stage 3: `POSTGRES_AUTHORITATIVE` (Target Production State)
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** All CAE services stream media directly from Supabase Storage using signed, time-limited URLs validated against `cae.media_asset`.
- **Write Path:** New media uploads write directly to Supabase Storage and register through `register_verified_interview_source`.
- **Receipt Requirement:** Cryptographic execution receipts in `cae.receipt` and `cae.execution_receipt`.
- **Exit Criteria:** Zero media byte integrity errors across 30 operational days.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy media directories set to read-only permissions (`chmod 444`).
- **Read Path:** Supabase Storage authoritative; local disk retained for backup.
- **Write Path:** Supabase Storage exclusive; local disk writes locked.
- **Receipt Requirement:** Full archive checksum manifest.
- **Exit Criteria:** Backup audit passed.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy local media directories purged after encrypted cold storage archival.
- **Read Path / Write Path:** Supabase Storage exclusive.
- **Receipt Requirement:** Final media migration ledger closure receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `logical_uri`: Parsed and validated against `workspace://<workspace_id>/<project_id>/<filename>`.
2. `content_sha256`: Recomputed from raw disk bytes; MUST match legacy manifest `sha256`.
3. `byte_size`: Integer byte count; MUST match raw disk length.
4. `media_type`: Explicit MIME type (e.g. `audio/wav`, `video/mp4`).

### Loss Policy
- Zero data loss. Binary bytes are copied bit-for-bit. Content hash mismatch immediately halts the bridge with `InterviewSourceBridgeError`.

### Idempotency & Concurrency
- Storage upload uses `x-upsert: false`. If key already exists (HTTP 400/409), the bridge downloads existing bytes and verifies SHA-256. If matching, operation proceeds idempotently; if conflicting, aborts.
- `register_verified_interview_source` uses `idempotency_key` locking `cae.command`.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify that every media asset has corresponding verified evidence items and valid storage keys
SELECT 'missing_source_package' AS check_name, count(*) AS failure_count
FROM cae.media_asset m
LEFT JOIN cae.source_package s ON m.source_package_id = s.source_package_id
WHERE s.source_package_id IS NULL
UNION ALL
SELECT 'missing_evidence_item', count(*)
FROM cae.source_package s
LEFT JOIN cae.evidence_item e ON s.source_package_id = e.source_package_id
WHERE e.evidence_id IS NULL;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `SHA256_MISMATCH` | Disk bytes hash does not match legacy manifest hash | Bridge halts; legacy asset marked `QUARANTINE_CORRUPT`. |
| `STORAGE_UPLOAD_FAILURE` | Network/auth error during Supabase Storage upload | Transaction aborted; orphaned object deleted via `delete_object()`. |
| `ORPHAN_MEDIA_ASSET` | Metadata registered without verified storage object | Database foreign key rejects; transaction rolled back. |

### Deterministic Emergency Rollback
If metadata registration fails after binary upload, `InterviewExpressionSourceBridge.bridge_source_package()` automatically deletes the newly created storage object via `self.delete_object(storage_object_key)`.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + Supabase Storage).
- **Hard Negative Countertest (`HN-STATE-007`):**
  - Attempt: Bridge passes string URL to `register_verified_interview_source` without byte hash readback.
  - Expected Verdict: System rejects registration with `InterviewSourceBridgeError("legacy media bytes do not match")`.
  - Verification: Enforced in `interview_source_bridge.py:64` and tested in `verify_ca_state_01.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-MED-001 as Recommended First Cutover Candidate"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
