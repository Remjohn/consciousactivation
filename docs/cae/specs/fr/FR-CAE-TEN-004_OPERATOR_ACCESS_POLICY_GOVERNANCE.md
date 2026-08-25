# Functional Requirement — FR-CAE-TEN-004: Operator Access Policy Governance

**Requirement ID:** `FR-CAE-TEN-004`  
**Title:** Cross-Workspace Operator Access Governance Policy  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `OperatorAccessPolicy` (`CA-POL-001`, `Policy / Contract`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml`
- **Canonical Edge:** Operational Governance Policy in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-001` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects client operational privacy and security from untracked internal operator access. Prevents standing global "super-admin" backdoors by defining the strict constitutional rules, allowed diagnostic scopes, mandatory justification requirements, and maximum grant durations under which operator grants may be issued.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL maintain a global `OperatorAccessPolicy` governing all temporary operator diagnostic access to client workspaces.
2. The policy SHALL enforce that no operator can access a workspace without an active, explicit `OperatorAccessGrant` conforming to the policy rules.
3. The policy SHALL enforce mandatory justification logging (`reason_code`, `ticket_reference`, `requesting_operator_id`).
4. The policy SHALL enforce a hard maximum duration limit (e.g. 4 hours) after which any granted access automatically expires.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `policy_name` (string, required): Policy identifier.
  - `max_duration_seconds` (integer, required): Maximum allowed grant window (<= 14400s).
  - `allowed_roles` (array of enum, required): Operator roles permitted to request access (`DIAGNOSTIC_OPERATOR`, `SECURITY_AUDITOR`).
  - `requires_client_approval` (boolean, required): Whether explicit workspace admin consent is required.
- **Semantic Outputs:**
  - `policy_id` (UUID, immutable): Unique policy identifier.
  - `version` (string, semver): Version of the governance policy.
  - `is_active` (boolean): Active governance flag.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Policy / Contract`
- **Scope Classification:** `OPERATOR_AUDIT` (Platform Governance Scope)
- **Direct Relations:**
  - `OperatorOrganization` $\longrightarrow$ `OperatorAccessPolicy` (1:N)
  - `OperatorAccessPolicy` $\longrightarrow$ `OperatorAccessGrant` (1:N)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml`.
  - *Target Runtime Representation:* Relational policy registry table evaluated by access control validators.
  - *Promotion Authority:* CAE Security Governance Committee.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `DRAFT` $\longrightarrow$ `ACTIVE` $\longrightarrow$ `SUPERSEDED` $\longrightarrow$ `REVOKED`.
- **State Transition Contracts:**
  - `STC-POL-001`: `RATIFY -> ACTIVE`
  - `STC-POL-002`: `ACTIVE -> SUPERSEDED`
  - `STC-POL-003`: `ACTIVE -> REVOKED`

---

### 7. Authorized Operation Family
- `cae.operator-policy.publish@1.0.0`
- `cae.operator-policy.revoke@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Policy changes SHALL emit an immutable `Receipt` (`CA-REC-001`) with cryptographic digest of policy rules and sign-off signatures.

---

### 9. Validation and Typed Failure Classes
- `ERR_POL_INVALID_DURATION`: Proposed grant duration exceeds policy maximum.
- `ERR_POL_DISALLOWED_ROLE`: Operator role not authorized to request workspace access.
- `ERR_POL_INACTIVE`: Attempt to issue grants against an inactive/superseded policy.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An operator access grant cannot exceed the policy's configured `max_duration_seconds`.
2. **Proposition 2:** Unregistered operator roles are rejected by the policy validator.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-POL-001` (Operator Access Policy Enforcement)
- **Minimum Fidelity:** `E2_REPOSITORY_FIXTURE` / `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-006`):** Verify that attempting to create an `OperatorAccessGrant` with a duration of 24 hours fails policy validation when the policy cap is 4 hours.

---

### 12. Brownfield Impact
- **Classification:** `NEW`
- **Impact Details:** Introduces policy-based governance contract for cross-tenant diagnostic access.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Security Policy Aggregate Contract.
- **Rollback Posture:** Non-breaking; revert to strict default-deny policy.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01A`.
- **Prohibited Interpretation:** MUST NOT treat policy definition as automatic access permission. Access requires an individual grant.
