# Functional Requirement — FR-CAE-TEN-008: Guest Identity Link Anti-Merge

**Requirement ID:** `FR-CAE-TEN-008`  
**Title:** Controlled Cross-Workspace Guest Identity Linkage and Anti-Merge Policy  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW (RUNTIME DEFERRED)`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `GuestIdentityLink` (`CA-MAP-001`, `Crosswalk / Mapping Object`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01B_GUEST_IDENTITY_LINK.yaml`
- **Canonical Edge:** Cross-Workspace Research Crosswalk in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-005` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects participant autonomy and client isolation during enterprise longitudinal research. Enforces that linking participant histories across workspaces is an extraordinary, auditable, dual-consented crosswalk rather than an automatic identity merge. Mandates that operational runtime execution remains formally deferred.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL define `GuestIdentityLink` as a separate crosswalk object linking two distinct workspace-local guest records `(workspace_a, guest_a) <---> (workspace_b, guest_b)`.
2. The crosswalk SHALL require explicit, dual-sided consent proofs from both workspace administrators and the participant.
3. The crosswalk SHALL NOT merge database rows, combine operational histories, or expose private media bytes across workspaces without explicit scoped authorization.
4. The system SHALL mark runtime execution of this crosswalk as `DEFERRED` during the first operational slice.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `source_workspace_id` (UUID, required): Origin workspace.
  - `source_guest_id` (UUID, required): Origin guest.
  - `target_workspace_id` (UUID, required): Target workspace.
  - `target_guest_id` (UUID, required): Target guest.
  - `consent_bundle_hash` (string, required): Cryptographic hash of bilateral consent manifests.
- **Semantic Outputs:**
  - `link_id` (UUID, immutable): Unique crosswalk record identifier.
  - `link_status` (`PENDING_APPROVAL`, `ESTABLISHED`, `REVOKED`): Crosswalk status.
  - `receipt_id` (UUID): Cryptographic audit receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Crosswalk / Mapping Object`
- **Scope Classification:** `OPERATOR_AUDIT` (Cross-Tenant Audit Boundary)
- **Direct Relations:**
  - `GuestIdentityLink` $\longrightarrow$ `Guest` (N:M bilateral crosswalk)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01B_GUEST_IDENTITY_LINK.yaml`.
  - *Target Runtime Representation:* Relational crosswalk table with strict RLS denial for normal tenant queries.
  - *Promotion Authority:* CAE Ethics & Compliance Officer.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `PROPOSED` $\longrightarrow$ `ACTIVE` $\longrightarrow$ `REVOKED`.
- **State Transition Contracts:**
  - `STC-LNK-001`: `PROPOSE -> ACTIVE` upon dual consent verification.
  - `STC-LNK-002`: `ACTIVE -> REVOKED` upon consent withdrawal.

---

### 7. Authorized Operation Family
- `cae.guest-link.propose@1.0.0`
- `cae.guest-link.revoke@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every link establishment and revocation SHALL emit an immutable `Receipt` (`CA-REC-001`) with cryptographic proof of consent.

---

### 9. Validation and Typed Failure Classes
- `ERR_LNK_AUTOMATIC_MERGE_PROHIBITED`: System attempted automatic matching without dual consent.
- `ERR_LNK_CONSENT_INVALID`: Missing or unverifiable consent digest.
- `ERR_LNK_RUNTIME_DEFERRED`: Operation blocked because runtime execution is deferred.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An automated heuristic cannot instantiate a `GuestIdentityLink`.
2. **Proposition 2:** A linked guest in Workspace A cannot read raw interview turns from Workspace B without an explicit cross-workspace research contract.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-LNK-001` (Crosswalk Deferment & Anti-Merge)
- **Minimum Fidelity:** `E1_STATIC` / `E2_REPOSITORY_FIXTURE`
- **Reward-Hack Countertest (`HN-SPEC-010`):** Verify that attempting to run automatic guest identity resolution fails static validation and is rejected as an unratified operation.

---

### 12. Brownfield Impact
- **Classification:** `DEFER`
- **Impact Details:** Formally defines specification boundary; blocks runtime implementation until prioritized.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on future Enterprise Research Specification; non-applicable to first slice.
- **Rollback Posture:** Invalidation of crosswalk records; zero impact on local guest histories.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** Runtime execution deferred to future phase. Ratified under `CA-CAN-01B`.
- **Prohibited Interpretation:** MUST NOT interpret `GuestIdentityLink` as permission for global data warehousing or unconsented participant tracking.
