# Functional Requirement — FR-CAE-TEN-010: Media Asset Verification Lifecycle

**Requirement ID:** `FR-CAE-TEN-010`  
**Title:** Relational Media Asset Metadata and Verification Lifecycle  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `MediaAsset` (`CA-ENT-002`, `Entity`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01B_MEDIA_ASSET.yaml`
- **Canonical Edge:** `REL-OP-005`, `REL-OP-006` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-003` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the evidentiary integrity of media assets within CAE. Prevents unverified, corrupt, or missing media files from being used in qualitative analysis by enforcing a rigorous verification lifecycle (`REGISTERED` $\rightarrow$ `STAGED` $\rightarrow$ `VERIFIED` $\rightarrow$ `QUARANTINED` $\rightarrow$ `REVOKED`) anchored to content-addressed SHA-256 hashes. Prohibits storing raw binary bytes in relational tables.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL maintain `MediaAsset` as the relational metadata entity representing audio/video recordings in PostgreSQL.
2. The entity SHALL store metadata only: `workspace_id`, `storage_path`, `canonical_sha256`, `byte_count`, `mime_type`, `duration_seconds`, and `lifecycle_state`.
3. The system SHALL prohibit downstream evidence extraction (`cae.evidence.capture`) from executing on any `MediaAsset` whose `lifecycle_state` is not `VERIFIED`.
4. The system SHALL automatically transition `MediaAsset` to `QUARANTINED` if physical byte verification or SHA-256 validation fails.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `storage_path` (string, required): URI in private object storage.
  - `expected_sha256` (string, required): 64-character hex hash.
  - `byte_count` (integer, required): File size in bytes.
  - `mime_type` (string, required): E.g. `audio/wav`, `audio/mpeg`.
- **Semantic Outputs:**
  - `media_asset_id` (UUID, immutable): Unique asset identifier.
  - `lifecycle_state` (`REGISTERED`, `STAGED`, `VERIFIED`, `QUARANTINED`, `REVOKED`): Verification state.
  - `verified_at` (timestamp, ISO 8601, optional): Timestamp of successful verification.
  - `receipt_id` (UUID): Lifecycle transition receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Entity`
- **Scope Classification:** `WORKSPACE_SCOPED`
- **Direct Relations:**
  - `REL-OP-005` (`EvidenceSource` $\longrightarrow$ `MediaAsset`, 1:1)
  - `REL-OP-006` (`MediaAsset` $\longrightarrow$ `ImmutableMediaEvidence`, 1:1)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01B_MEDIA_ASSET.yaml`, Builder ADR-003.
  - *Target Runtime Representation:* Relational metadata table `cae.media_asset` with SHA-256 uniqueness constraint per workspace.
  - *Promotion Authority:* Storage Ingestion Gateway / Verification Service.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `REGISTERED` $\longrightarrow$ `STAGED` $\longleftrightarrow$ `VERIFIED` $\longrightarrow$ `QUARANTINED` / `REVOKED`.
- **State Transition Contracts:**
  - `STC-MED-001`: `REGISTER -> REGISTERED`
  - `STC-MED-002`: `REGISTERED -> STAGED` upon upload start.
  - `STC-MED-003`: `STAGED -> VERIFIED` upon SHA-256 byte match.
  - `STC-MED-004`: `STAGED -> QUARANTINED` upon hash mismatch or corruption.
  - `STC-MED-005`: `VERIFIED -> REVOKED` upon asset invalidation.

---

### 7. Authorized Operation Family
- `cae.media.register@1.0.0`
- `cae.media.verify@1.0.0`
- `cae.media.quarantine@1.0.0`
- `cae.media.revoke@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Verification SHALL emit an immutable `Receipt` (`CA-REC-001`) recording the calculated SHA-256 digest, byte count, and storage URI.

---

### 9. Validation and Typed Failure Classes
- `ERR_MED_HASH_MISMATCH`: Calculated SHA-256 does not match expected hash.
- `ERR_MED_NOT_VERIFIED`: Attempt to capture evidence from an unverified media asset.
- `ERR_MED_RAW_BYTES_PROHIBITED`: Attempt to store raw media payload in relational row.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** Evidence capture operations fail if target `MediaAsset.lifecycle_state != 'VERIFIED'`.
2. **Proposition 2:** A media asset with mismatched byte hash is placed in `QUARANTINED` state.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-MED-001` (Media Verification & Lifecycle)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE` (Real private storage bucket upload and SHA-256 check)
- **Reward-Hack Countertest (`HN-SPEC-005`):** Verify that setting `lifecycle_state = 'VERIFIED'` via direct SQL or mock without verifying byte SHA-256 from object storage is detected and rejected by verification validators.

---

### 12. Brownfield Impact
- **Classification:** `ADAPT`
- **Impact Details:** Replaces unverified filesystem paths in brownfield services with content-addressed, verified media records.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Media Asset Aggregate Contract.
- **Rollback Posture:** Invalidation of unverified assets; revert to previous verified state.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01B`.
- **Prohibited Interpretation:** MUST NOT treat a public URL or unverified file reference as verified media evidence.
