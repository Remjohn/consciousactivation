# Functional Requirement — FR-CAE-TEN-009: Evidence Source Provenance

**Requirement ID:** `FR-CAE-TEN-009`  
**Title:** External Evidence Source Provenance and Ingestion Boundary  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `EvidenceSource` (`CA-REL-004`, `Relation`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01B_EVIDENCE_SOURCE.yaml`
- **Canonical Edge:** `REL-OP-005` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-003` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects external package ingestion provenance. Establishes cryptographic lineage linking external interview packages, recording systems, and legacy exports to internal CAE `MediaAsset` entities. Prevents unverified ingestion payloads from entering downstream semantic analysis.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require any external media package entering CAE to be registered via an `EvidenceSource` record.
2. The record SHALL capture the external system identity, source path/digest, export timestamp, and source manifest hash.
3. The system SHALL bind `EvidenceSource` to exactly one internal `MediaAsset` entity within the same `workspace_id`.
4. The system SHALL enforce that upstream source system permissions do NOT grant administrative privileges within CAE.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Target workspace.
  - `source_system` (string, required): External system name (e.g. `INTERVIEW_EXPRESSION_EXPORT`).
  - `source_package_digest` (string, SHA-256, required): External package digest.
  - `metadata_manifest` (object, required): Ingestion metadata.
- **Semantic Outputs:**
  - `source_id` (UUID, immutable): Unique evidence source identifier.
  - `media_asset_id` (UUID, immutable): Internal media asset link.
  - `status` (`ADMITTED`, `VERIFIED`, `REJECTED`): Ingestion status.
  - `receipt_id` (UUID): Ingestion receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Relation`
- **Scope Classification:** `WORKSPACE_SCOPED`
- **Direct Relations:**
  - `REL-OP-005` (`EvidenceSource` $\longrightarrow$ `MediaAsset`, 1:1)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01B_EVIDENCE_SOURCE.yaml`, WP-09 First Vertical Runtime Slice.
  - *Target Runtime Representation:* Relational provenance record linked to `MediaAsset`.
  - *Promotion Authority:* Workspace Ingestion Bridge Adapter (`cae.bridge.register-interview-source`).

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `ADMITTED` $\longrightarrow$ `VERIFIED` / `REJECTED`.
- **State Transition Contracts:**
  - `STC-SRC-001`: `ADMIT -> ADMITTED`
  - `STC-SRC-002`: `ADMITTED -> VERIFIED` upon byte verification.
  - `STC-SRC-003`: `ADMITTED -> REJECTED` upon digest mismatch.

---

### 7. Authorized Operation Family
- `cae.source.register@1.0.0`
- `cae.source.verify@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every source admission and verification SHALL emit an immutable `Receipt` (`CA-REC-001`) recording external digests and ingestion timestamps.

---

### 9. Validation and Typed Failure Classes
- `ERR_SRC_DIGEST_MISMATCH`: External digest does not match ingested payload.
- `ERR_SRC_UNAUTHORIZED_SYSTEM`: Unregistered external source system.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** A media asset cannot be admitted from an external source without an `EvidenceSource` provenance record.
2. **Proposition 2:** A mismatch in external package digest triggers immediate rejection.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-SRC-001` (Source Ingestion Provenance)
- **Minimum Fidelity:** `E2_REPOSITORY_FIXTURE` / `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-005`):** Ingest a modified package with altered content; verify that ingestion fails digest verification and emits `ERR_SRC_DIGEST_MISMATCH`.

---

### 12. Brownfield Impact
- **Classification:** `ADAPT`
- **Impact Details:** Bridges `services/interview` export records into CAE canonical provenance model via WP-09 bridge.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Source Bridge Aggregate Contract.
- **Rollback Posture:** Invalidation of unverified source records; safe re-ingestion.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01B`.
- **Prohibited Interpretation:** MUST NOT interpret source package presence as verified internal media truth. Verification requires `MediaAsset` byte checking.
