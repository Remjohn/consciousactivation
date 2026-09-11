# Functional Requirement — FR-CAE-TEN-005: Operator Access Grant Lifecycle

**Requirement ID:** `FR-CAE-TEN-005`  
**Title:** Ephemeral Operator Access Grant and Audit Lifecycle  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `OperatorAccessGrant` (`CA-REL-002`, `Relation`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml`
- **Canonical Edge:** Operational Diagnostic Bridge in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-001` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the auditability and containment of operator diagnostic sessions. Prevents unrecorded, persistent, or unexpired operator access to client workspaces by enforcing ephemeral, reason-bounded grants that emit full audit receipts.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require any internal CAE operator accessing a client workspace to execute under an active, non-expired `OperatorAccessGrant` record.
2. The grant SHALL bind `(operator_id, workspace_id, policy_id, valid_from, valid_until, reason_code, ticket_id)`.
3. The system SHALL automatically revoke/deny access immediately when `current_timestamp > valid_until`.
4. The system SHALL record all actions taken under an active grant with the specific `grant_id` in emitted receipts.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `operator_id` (UUID, required): Requesting operator principal.
  - `workspace_id` (UUID, required): Target client workspace.
  - `policy_id` (UUID, required): Reference to governing `OperatorAccessPolicy`.
  - `duration_seconds` (integer, required): Requested duration (within policy limit).
  - `reason_code` (enum, required): `INCIDENT_INVESTIGATION`, `DATA_REPAIR`, `MIGRATION_AUDIT`.
  - `ticket_reference` (string, required): External issue ticket ID.
- **Semantic Outputs:**
  - `grant_id` (UUID, immutable): Unique grant identifier.
  - `status` (`ACTIVE`, `EXPIRED`, `REVOKED`): Lifecycle status.
  - `valid_from` (timestamp, ISO 8601): Start time.
  - `valid_until` (timestamp, ISO 8601): Expiration time.
  - `receipt_id` (UUID): Cryptographic audit receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Relation`
- **Scope Classification:** `OPERATOR_AUDIT` (Platform Diagnostic Bridge Scope)
- **Direct Relations:**
  - `OperatorAccessPolicy` $\longrightarrow$ `OperatorAccessGrant` (1:N)
  - `OperatorAccessGrant` $\longrightarrow$ `Workspace` (N:1 ephemeral bridge)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml`.
  - *Target Runtime Representation:* Relational audit table with TTL/expiration checks.
  - *Promotion Authority:* CAE Operator Lead / Security Reviewer.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `REQUESTED` $\longrightarrow$ `ACTIVE` $\longrightarrow$ `EXPIRED` / `REVOKED`.
- **State Transition Contracts:**
  - `STC-GRNT-001`: `ISSUE -> ACTIVE`
  - `STC-GRNT-002`: `EXPIRE (TTL) -> EXPIRED`
  - `STC-GRNT-003`: `REVOKE -> REVOKED`

---

### 7. Authorized Operation Family
- `cae.operator-grant.issue@1.0.0`
- `cae.operator-grant.revoke@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every grant issuance, renewal, expiration, and revocation SHALL emit an immutable `Receipt` (`CA-REC-001`) with full operator and ticket provenance.

---

### 9. Validation and Typed Failure Classes
- `ERR_GRNT_POLICY_VIOLATION`: Requested duration or role violates policy.
- `ERR_GRNT_EXPIRED`: Attempt to use an expired grant for workspace operations.
- `ERR_GRNT_REVOKED`: Attempt to use a revoked grant rejected.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An operator cannot access workspace endpoints once `valid_until` timestamp has elapsed.
2. **Proposition 2:** Every operation executed during a diagnostic session records `grant_id` in its resulting receipt.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-GRNT-001` (Operator Grant Expiration & Audit)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-006`):** Verify that executing a workspace operation 1 millisecond after `valid_until` produces `ERR_GRNT_EXPIRED` and denies the operation.

---

### 12. Brownfield Impact
- **Classification:** `NEW`
- **Impact Details:** Implements ephemeral audited diagnostic access, replacing standing administrative access.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Access Grant Aggregate Contract.
- **Rollback Posture:** Immediate invalidation of all active grants.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01A`.
- **Prohibited Interpretation:** MUST NOT treat an operator access grant as a permanent membership or workspace ownership.
