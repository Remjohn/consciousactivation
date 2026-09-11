# Functional Requirement — FR-CAE-TEN-003: Workspace Membership Role

**Requirement ID:** `FR-CAE-TEN-003`  
**Title:** Workspace Actor Membership and Role Authorization  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `WorkspaceMembership` (`CA-REL-001`, `Relation`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`
- **Canonical Edge:** `REL-OP-001` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-007` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the actor authorization and least-privilege access model within client workspaces. Prevents cross-workspace role bleed, unauthenticated client actions, and ambiguous permission scopes by establishing that all client-side operations derive authority from an explicit `WorkspaceMembership`.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require every human or service actor performing actions within a workspace to possess an active `WorkspaceMembership` record binding `(workspace_id, actor_id)`.
2. The system SHALL support discrete workspace-scoped roles (`WORKSPACE_ADMIN`, `ENGAGEMENT_LEAD`, `ANALYST`, `AUDITOR`, `SERVICE_RUNNER`).
3. The system SHALL isolate memberships strictly to their parent workspace; a membership in Workspace A conveys ZERO authority in Workspace B.
4. The system SHALL support immediate revocation of membership, instantly terminating operational permissions.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Target workspace.
  - `actor_id` (UUID / String, required): Authenticated principal identifier.
  - `role` (enum, required): `WORKSPACE_ADMIN`, `ENGAGEMENT_LEAD`, `ANALYST`, `AUDITOR`, `SERVICE_RUNNER`.
  - `granted_by` (UUID, required): Authorizing administrator.
- **Semantic Outputs:**
  - `membership_id` (UUID, immutable): Unique membership record identifier.
  - `status` (`ACTIVE`, `SUSPENDED`, `REVOKED`): Membership status.
  - `created_at` (timestamp, ISO 8601): Assignment timestamp.
  - `receipt_id` (UUID): Cryptographic receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Relation`
- **Scope Classification:** `WORKSPACE_SCOPED`
- **Direct Relations:**
  - `REL-OP-001` (`Workspace` $\longrightarrow$ `WorkspaceMembership`, 1:N)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`.
  - *Target Runtime Representation:* Relational junction table with composite key `(workspace_id, actor_id)`.
  - *Promotion Authority:* Workspace Administrator via typed semantic operations.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `ACTIVE` $\longleftrightarrow$ `SUSPENDED` $\longrightarrow$ `REVOKED`.
- **State Transition Contracts:**
  - `STC-MEM-001`: `GRANT -> ACTIVE`
  - `STC-MEM-002`: `ACTIVE -> SUSPENDED`
  - `STC-MEM-003`: `SUSPENDED -> ACTIVE`
  - `STC-MEM-004`: `ACTIVE/SUSPENDED -> REVOKED`

---

### 7. Authorized Operation Family
- `cae.membership.grant@1.0.0`
- `cae.membership.update-role@1.0.0`
- `cae.membership.revoke@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every grant, role change, and revocation SHALL emit an immutable `Receipt` (`CA-REC-001`) recording the authorizing actor, target actor, role payload, and timestamp.

---

### 9. Validation and Typed Failure Classes
- `ERR_MEM_ALREADY_EXISTS`: Actor already holds an active membership in target workspace.
- `ERR_MEM_UNAUTHORIZED_GRANT`: Granting actor lacks `WORKSPACE_ADMIN` privileges.
- `ERR_MEM_REVOKED`: Attempt to execute operations under a revoked membership rejected.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An actor cannot invoke workspace-scoped operations without an active `WorkspaceMembership`.
2. **Proposition 2:** Revoking a membership takes effect immediately on subsequent operation evaluations.
3. **Proposition 3:** Membership permissions do not grant access across different workspaces.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-MEM-001` (Workspace RBAC & Containment)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL RLS with actor claim tokens)
- **Reward-Hack Countertest (`HN-SPEC-008`):** Verify that an actor with `WORKSPACE_ADMIN` in Workspace A cannot perform read or write operations in Workspace B where they hold no membership.

---

### 12. Brownfield Impact
- **Classification:** `NEW` / `ADAPT`
- **Impact Details:** Replaces unauthenticated local service calls with explicit actor-role context validation.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Actor & Membership Contract.
- **Rollback Posture:** Invalidation of active memberships; re-granting from verified audit logs.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01A`.
- **Prohibited Interpretation:** MUST NOT treat membership as global platform authorization. It is strictly local to `workspace_id`.
