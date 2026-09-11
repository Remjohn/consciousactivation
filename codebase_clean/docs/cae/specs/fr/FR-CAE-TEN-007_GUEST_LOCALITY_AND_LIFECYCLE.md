# Functional Requirement — FR-CAE-TEN-007: Guest Locality and Lifecycle

**Requirement ID:** `FR-CAE-TEN-007`  
**Title:** Workspace-Local Guest Identity and Operational Lifecycle  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `Guest` (`CA-ENT-003`, `Entity`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01B_GUEST.yaml`
- **Canonical Edge:** `REL-OP-002` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-005`, `COL-MAP-007` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects participant privacy and prevents dangerous cross-tenant data blending. Enforces the non-negotiable law that `Guest` identity is strictly local to its parent `Workspace`. Prohibits global guest pools, universal `guest_id` partition keys, and automatic matching of participants across different client workspaces.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require every `Guest` entity to be created within exactly one parent `workspace_id`.
2. The system SHALL enforce that a guest profile exists solely within that workspace and has ZERO global presence by default.
3. The system SHALL prohibit automatic deduplication, matching, or merging of guest profiles across workspaces, even if names, emails, or biometric hashes appear identical.
4. The system SHALL isolate guest dynamic state, interview turns, and evidence items strictly within the parent workspace boundary.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `local_pseudonym` (string, required): Workspace-local participant identifier/pseudonym.
  - `consent_record` (object, required): Participant consent timestamp and scope.
- **Semantic Outputs:**
  - `guest_id` (UUID, immutable): Unique workspace-local guest identifier.
  - `lifecycle_status` (`REGISTERED`, `ACTIVE`, `ANONYMIZED`, `ARCHIVED`): Guest status.
  - `created_at` (timestamp, ISO 8601): Registration timestamp.
  - `receipt_id` (UUID): Cryptographic receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Entity`
- **Scope Classification:** `GUEST_SCOPED` (Workspace-Contained)
- **Direct Relations:**
  - `REL-OP-002` (`Workspace` $\longrightarrow` `Guest`, 1:N)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01B_GUEST.yaml`, Multi-Tenant Plan §3.
  - *Target Runtime Representation:* Relational projection with composite primary key `(workspace_id, guest_id)`.
  - *Promotion Authority:* Workspace Engagement Lead / Participant Consent Controller.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `REGISTERED` $\longleftrightarrow$ `ACTIVE` $\longrightarrow$ `ANONYMIZED` / `ARCHIVED`.
- **State Transition Contracts:**
  - `STC-GST-001`: `REGISTER -> REGISTERED`
  - `STC-GST-002`: `REGISTERED -> ACTIVE` upon interview initiation.
  - `STC-GST-003`: `ACTIVE -> ANONYMIZED` upon privacy erasure request.
  - `STC-GST-004`: `ACTIVE/ANONYMIZED -> ARCHIVED`.

---

### 7. Authorized Operation Family
- `cae.guest.register@1.0.0`
- `cae.guest.update-consent@1.0.0`
- `cae.guest.anonymize@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every guest registration, consent update, and anonymization SHALL emit an immutable `Receipt` (`CA-REC-001`) with cryptographic hash of the consent manifest.

---

### 9. Validation and Typed Failure Classes
- `ERR_GST_CROSS_WORKSPACE_MERGE`: Attempt to link or merge guest records across workspaces rejected.
- `ERR_GST_MISSING_CONSENT`: Operation attempted without active consent verification.
- `ERR_GST_NOT_FOUND`: Guest ID does not exist within target workspace.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** A guest record cannot exist without an explicit `workspace_id`.
2. **Proposition 2:** Two guests in different workspaces with identical metadata remain completely separate records with no shared history.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-GST-001` (Guest Locality & Anti-Merge)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-002`, `HN-SPEC-010`):** Create two guests with identical email/name in Workspace A and Workspace B; verify that queries in Workspace A return only the Workspace A record and cannot access Workspace B turns or evidence.

---

### 12. Brownfield Impact
- **Classification:** `NEW` / `ADAPT`
- **Impact Details:** Refactors brownfield participant references in `services/interview` to be strictly workspace-local.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Guest Aggregate Contract.
- **Rollback Posture:** Invalidation of active guest sessions; preserve local consent records.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01B`.
- **Prohibited Interpretation:** MUST NOT treat `guest_id` as a global Person identifier or a universal tenancy key.
