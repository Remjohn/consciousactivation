# Functional Requirement — FR-CAE-TEN-011: Immutable Media Byte Isolation

**Requirement ID:** `FR-CAE-TEN-011`  
**Title:** Content-Addressed Immutable Media Byte Storage and Access Isolation  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `ImmutableMediaEvidence` (`CA-EVI-001`, `Immutable Evidence`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml`
- **Canonical Edge:** `REL-OP-006` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-003` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects physical media recording payloads from tampering, accidental deletion, and unauthorized cross-tenant exposure. Enforces that raw recording bytes reside strictly in private, tenant-prefixed object storage paths with content-addressed SHA-256 integrity checks, rather than unencrypted public buckets or database rows.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL store raw media recording bytes in private object storage buckets under strict workspace prefixes: `storage://cae-media/{workspace_id}/{media_asset_id}/{canonical_sha256}.ext`.
2. The system SHALL enforce byte-level immutability post-upload (Write Once, Read Many).
3. The system SHALL restrict byte retrieval exclusively via short-lived, authenticated signed URLs or secure backend proxy streams scoped to authorized workspace actors.
4. The system SHALL prohibit cross-workspace read access to storage buckets via Storage RLS / IAM bucket policies.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `media_asset_id` (UUID, required): Parent media asset.
  - `raw_byte_stream` (binary, required): Physical audio/video data stream.
  - `claimed_sha256` (string, required): Claimed SHA-256 digest.
- **Semantic Outputs:**
  - `storage_path` (string, immutable): Normalized storage object key.
  - `verified_sha256` (string, immutable): Calculated SHA-256 digest.
  - `byte_size` (integer): Verified byte length.
  - `receipt_id` (UUID): Storage commit receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Immutable Evidence`
- **Scope Classification:** `WORKSPACE_SCOPED` (Private Object Storage)
- **Direct Relations:**
  - `REL-OP-006` (`MediaAsset` $\longrightarrow$ `ImmutableMediaEvidence`, 1:1)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml`, Builder ADR-003.
  - *Target Runtime Representation:* Private S3/Supabase Storage bucket with workspace prefix policies.
  - *Promotion Authority:* Storage Gateway SHA-256 Verification Service.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `UPLOADING` $\longrightarrow$ `COMMITTED_IMMUTABLE` $\longrightarrow$ `ARCHIVED_COLD`.
- **State Transition Contracts:**
  - `STC-STO-001`: `UPLOAD -> COMMITTED_IMMUTABLE` upon verified write.
  - `STC-STO-002`: `COMMITTED -> ARCHIVED_COLD` upon lifecycle policy trigger.

---

### 7. Authorized Operation Family
- `cae.storage.upload-bytes@1.0.0`
- `cae.storage.generate-signed-read-url@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Byte storage commit SHALL emit an immutable `Receipt` (`CA-REC-001`) with byte size, calculated SHA-256, and storage path.

---

### 9. Validation and Typed Failure Classes
- `ERR_STO_INTEGRITY_MISMATCH`: Uploaded bytes do not match claimed SHA-256.
- `ERR_STO_CROSS_TENANT_ACCESS`: Attempt to read storage key outside caller's workspace prefix.
- `ERR_STO_MUTATION_DENIED`: Attempt to overwrite existing immutable storage key.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An uploaded media object cannot be overwritten or modified in-place.
2. **Proposition 2:** Requesting a signed URL for an object in Workspace B from an actor in Workspace A fails authorization.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-STO-001` (Private Storage Isolation & Hash Integrity)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE` (Supabase Storage bucket verification with cross-tenant read attempt)
- **Reward-Hack Countertest (`HN-SPEC-005`, `HN-SPEC-008`):** Verify that generating a signed download URL using credentials from Workspace A against a storage path prefixed with Workspace B returns HTTP 403 / Access Denied.

---

### 12. Brownfield Impact
- **Classification:** `NEW`
- **Impact Details:** Introduces private tenant-isolated object storage buckets, replacing local ephemeral file storage.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Storage Infrastructure Contract.
- **Rollback Posture:** Non-destructive; retain uploaded files in quarantine bucket if verification fails.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01B`.
- **Prohibited Interpretation:** MUST NOT store raw audio/video files in public buckets or unencrypted public endpoints.
