# Functional Requirement — FR-CAE-TEN-013: Harness Run Execution Lifecycle

**Requirement ID:** `FR-CAE-TEN-013`  
**Title:** Engagement-Scoped Harness Execution Lifecycle and State Machine  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `HarnessRun` (`CA-EXE-001`, `Execution Packet`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01C_HARNESS_RUN.yaml`
- **Canonical Edge:** `REL-OP-004`, `REL-CANON-001` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-002`, `COL-CAN-009` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the deterministic execution and state control of operational workflows. Enforces that operational runs (`HarnessRun`) are stateful, tenant-isolated instances bound to a parent `Workspace` and `Engagement`, referencing an immutable `HarnessTemplate`, and advancing through discrete, typed semantic operations emitting cryptographic receipts.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require every `HarnessRun` to be instantiated within a specific `workspace_id` and `engagement_id`, referencing a pinned `template_id` and `template_version`.
2. The run SHALL execute through an explicit state machine (`INITIALIZED` $\rightarrow$ `RUNNING` $\longleftrightarrow$ `PAUSED` $\rightarrow$ `COMPLETED` / `FAILED` / `ABORTED`).
3. The system SHALL enforce that each step transition executes via authorized typed semantic operations and emits an immutable `Receipt`.
4. The system SHALL prohibit a run from mutating its referenced template or writing data across workspace boundaries.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `engagement_id` (UUID, required): Parent engagement.
  - `template_id` (string, required): Canonical template ID.
  - `template_version` (string, required): Pinned semantic version.
  - `execution_context` (object, required): Initial input parameter bindings.
- **Semantic Outputs:**
  - `run_id` (UUID, immutable): Unique execution run identifier.
  - `run_state` (`INITIALIZED`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `ABORTED`): Current state.
  - `current_step` (string): Active procedural step identifier.
  - `receipt_id` (UUID): Step transition receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Execution Packet`
- **Scope Classification:** `ENGAGEMENT_SCOPED` (Workspace-Contained)
- **Direct Relations:**
  - `REL-OP-004` (`Engagement` $\longrightarrow$ `HarnessRun`, 1:N)
  - `REL-CANON-001` (`HarnessRun` $\longrightarrow$ `HarnessTemplate`, N:1 forward reference)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01C_HARNESS_RUN.yaml`.
  - *Target Runtime Representation:* Relational execution table `cae.harness_run` with composite FK `(workspace_id, engagement_id)`.
  - *Promotion Authority:* Workspace Runner Service / Transactional State Engine.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `INITIALIZED` $\longrightarrow$ `RUNNING` $\longleftrightarrow$ `PAUSED` $\longrightarrow$ `COMPLETED` / `FAILED` / `ABORTED`.
- **State Transition Contracts:**
  - `STC-RUN-001`: `INITIALIZE -> INITIALIZED`
  - `STC-RUN-002`: `INITIALIZED -> RUNNING`
  - `STC-RUN-003`: `RUNNING -> PAUSED` / `PAUSED -> RUNNING`
  - `STC-RUN-004`: `RUNNING -> COMPLETED` upon final step commit.
  - `STC-RUN-005`: `RUNNING -> FAILED` upon unrecoverable step error.
  - `STC-RUN-006`: `RUNNING/PAUSED -> ABORTED` upon operator cancel.

---

### 7. Authorized Operation Family
- `cae.run.initialize@1.0.0`
- `cae.run.step@1.0.0`
- `cae.run.pause@1.0.0`
- `cae.run.resume@1.0.0`
- `cae.run.abort@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every step execution and lifecycle state change SHALL emit an immutable `Receipt` (`CA-REC-001`) linking input digests, step outputs, and validator outcomes.

---

### 9. Validation and Typed Failure Classes
- `ERR_RUN_TEMPLATE_NOT_FOUND`: Referenced template ID / version does not exist.
- `ERR_RUN_INVALID_STEP_TRANSITION`: Proposed step violates template state machine.
- `ERR_RUN_CROSS_WORKSPACE`: Run parameters reference assets from another workspace.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** A run cannot be initialized without a valid `workspace_id`, `engagement_id`, and pinned `template_version`.
2. **Proposition 2:** A completed run preserves an immutable sequence of step execution receipts.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-RUN-001` (Harness Run Execution & State Transitions)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-009`, `HN-CAN-024`):** Verify that executing a HarnessRun does not mutate the `cae.harness_template` record or alter the template's publication checksum.

---

### 12. Brownfield Impact
- **Classification:** `ADAPT`
- **Impact Details:** Reconciles `services/pipeline` `WorkflowRunService` into the CAE typed harness execution model.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Workflow Run Aggregate Contract.
- **Rollback Posture:** Mark run as `ABORTED`; retain step receipts for post-mortem analysis.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01C`.
- **Prohibited Interpretation:** MUST NOT interpret a HarnessRun as direct database mutation access. Operations must execute via registered semantic contracts.
