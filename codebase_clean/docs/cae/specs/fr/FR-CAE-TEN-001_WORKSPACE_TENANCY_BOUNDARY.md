# Functional Requirement — FR-CAE-TEN-001: Workspace Client Tenancy Boundary

**Requirement ID:** `FR-CAE-TEN-001`  
**Title:** Workspace Client Tenancy Boundary and Root Containment  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `Workspace` (`CA-ENT-001`, `Entity`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01A_WORKSPACE.yaml`
- **Canonical Edge:** `REL-OP-001`, `REL-OP-002`, `REL-OP-003` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-007` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the fundamental multi-tenant security boundary of CAE. Prevents cross-client data leakage, unconstrained global queries, and shared state corruption by mandating that `Workspace` is the sole client isolation root. Prohibits global tenancy fallbacks or treating `guest_id` as a tenant root.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require every tenant-scoped operational record (engagements, guests, media assets, evidence spans, assessments, runs, and receipts) to belong to exactly one immutable `workspace_id`.
2. The system SHALL reject any operational query, write, or mutation that does not supply a valid, authenticated workspace context.
3. The system SHALL enforce that `workspace_id` is immutable once assigned to an operational record.
4. The system SHALL isolate all client data at query time such that no workspace can view, mutate, or detect the existence of records belonging to another workspace.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_name` (string, required): Human-readable organization/client workspace name.
  - `client_legal_entity` (string, required): Legal corporate entity identifier.
  - `initial_admin_actor_id` (string, required): Authenticated principal creating the workspace.
- **Semantic Outputs:**
  - `workspace_id` (UUID, immutable): Unique tenant root identifier.
  - `workspace_status` (`ACTIVE`, `SUSPENDED`, `ARCHIVED`): Lifecycle state.
  - `created_at` (timestamp, ISO 8601): Immutable creation timestamp.
  - `receipt_id` (UUID): Cryptographic receipt of workspace creation.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Entity`
- **Scope Classification:** `WORKSPACE_SCOPED` (Root Tenant Boundary)
- **Direct Relations:**
  - `REL-OP-001` (`Workspace` $\longrightarrow$ `WorkspaceMembership`, 1:N)
  - `REL-OP-002` (`Workspace` $\longrightarrow$ `Guest`, 1:N)
  - `REL-OP-003` (`Workspace` $\longrightarrow$ `Engagement`, 1:N)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01A_WORKSPACE.yaml`, Multi-Tenant Plan §3.
  - *Target Runtime Representation:* Relational projection with primary key `workspace_id` and RLS isolation.
  - *Promotion Authority:* CAE Operator Organization Administrator.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `PROVISIONED` $\longrightarrow$ `ACTIVE` $\longleftrightarrow$ `SUSPENDED` $\longrightarrow$ `ARCHIVED`.
- **State Transition Contracts:**
  - `STC-WS-001`: `PROVISIONED -> ACTIVE` upon admin assignment.
  - `STC-WS-002`: `ACTIVE -> SUSPENDED` upon operator isolation trigger.
  - `STC-WS-003`: `SUSPENDED -> ACTIVE` upon remediation verification.
  - `STC-WS-004`: `SUSPENDED -> ARCHIVED` upon retention expiration.

---

### 7. Authorized Operation Family
- `cae.workspace.provision@1.0.0`
- `cae.workspace.update-status@1.0.0`
- `cae.workspace.archive@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every state transition SHALL emit an immutable `Receipt` (`CA-REC-001`) recording `actor_id`, `operation_id`, `input_digest`, `output_digest`, and commit timestamp.
- Provenance is anchored to the initiating operator grant or administrator membership.

---

### 9. Validation and Typed Failure Classes
- `ERR_WS_NOT_FOUND`: Workspace ID does not exist.
- `ERR_WS_SUSPENDED`: Target workspace is in `SUSPENDED` state; non-admin operations denied.
- `ERR_WS_IMMUTABLE_ID`: Attempt to alter `workspace_id` on an existing entity rejected.
- `ERR_WS_CROSS_TENANT_ACCESS`: Access to workspace by unauthorized principal denied.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An operational entity cannot be instantiated without a valid `workspace_id`.
2. **Proposition 2:** Queries executed under Workspace A context return zero records and zero metadata belonging to Workspace B.
3. **Proposition 3:** Attempting to update `workspace_id` on an existing record raises a typed validation failure.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-TEN-001` (Multi-Tenant Isolation & Lifecycle)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL RLS with Supavisor pooler)
- **Reward-Hack Countertest (`HN-SPEC-008`):** Verify that executing cross-workspace SELECT/UPDATE queries under an authenticated session for Workspace A against Workspace B rows returns 0 rows / access denial, not merely passing tests in a mock single-workspace fixture.

---

### 12. Brownfield Impact
- **Classification:** `NEW` / `ADAPT`
- **Impact Details:** Introduces explicit workspace root context to API middleware and query filters, replacing implicit single-tenant SQLite assumptions.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Workspace Aggregate Authority Contract and `CA-IMPL-01A` relational foundation.
- **Rollback Posture:** Invalidation of active workspace sessions; fallback to read-only archival state.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01A`.
- **Prohibited Interpretation:** MUST NOT interpret `Workspace` as a cosmetic group or optional tag. It is the mandatory, impenetrable tenant boundary.
