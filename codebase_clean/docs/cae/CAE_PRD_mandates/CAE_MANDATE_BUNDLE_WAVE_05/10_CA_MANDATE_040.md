# CA-M040 — Real Human Gate Milestones & Fail-Closed Execution Suspension

## 1. Identity and status

- **Mandate ID:** `CA-M040`
- **Canonical question:** `Q40` (Phase 1: Gate Milestone Suspension Contract)
- **Wave:** `05`
- **Status:** `EXECUTION READY — bounded implementation mandate`
- **Primary requirement/invariant:** `INV-GATE-001` (`FR-040`)
- **Collision primitive:** `PREDICTION VIOLATION`
- **Dependency set:** Q34–Q39 execution spine (`INV-DISP-001` through `INV-OUT-001`); existing `ProgramStateLifecycle` and aggregate transition mechanics
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; api/routers/programs.py; focused gate-suspension tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement and authoritatively prove the real human gate milestone suspension contract for CAE program executions. Under historical development test harnesses, gates were frequently bypassed or simulated via mock auto-approvals, creating a dangerous prediction violation where operators assume an executing pipeline safely halts for review when in reality compute proceeds unchecked.

The objective of this mandate is to eliminate all mock auto-approvals and enforce genuine fail-closed execution suspension at every declared milestone gate boundary (such as `hypothesis_approval_gate`, `editorial_approval_gate`, and `script_approval_gate`). When the workflow dispatcher or state machine driver encounters a node boundary marked as requiring human authorization, execution must immediately halt. The runtime must transition the program aggregate's lifecycle state atomically to `AWAITING_APPROVAL`, freeze an immutable context snapshot of the current state, release or suspend the active worker execution lease, and emit a structured `GateSuspensionEvent` to the audit log. The system must physically refuse to execute subsequent agent turns or downstream mutations until an authentic Commander receipt is supplied.

This mandate authorizes only the gate suspension and fail-closed halting mechanism. It does not author gate resumption or disposition routing (which is governed by `CA-M041`).

## 3. Governing doctrine and authority sources

Semantic authority derives from the Master 57-Question Decision & Convergence Canon (specifically Question 40 / Spine Q07) and `docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md` (`FR-040`). Runtime authority is the canonical CAE program operator runtime (`ProgramOperatorRuntimeService`) and universal program state runtime (`UniversalProgramStateRuntime`). Change and promotion authority remains with the human Operator acting under `COMMANDER` lane authority.

Primary references:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative 13-section grammar, authority separation, and stop conditions.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution rules and reality-contact evidence standards.
3. `docs/cae/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q40 decision and invariant specification (`INV-GATE-001`).
4. `docs/cae/cae-bmad/03_product/modules/PRD-005.md` — runtime execution and gate governance specification.
5. Physical code surfaces: `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`, `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`, and `api/routers/programs.py`.

## 4. Mandatory reading before action

Before executing any code modifications, the executor MUST read the complete contents of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` (specifically Question 40)
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (inspecting `ProgramStateLifecycle.AWAITING_APPROVAL` and gate evaluation paths)
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` (inspecting execution loop and gate checks)
- `api/routers/programs.py` (inspecting execution state serialization)

The executor must inspect physical repository reality first. If gate evaluation currently relies on boolean mock flags or auto-advancing stubs, that defect must be documented explicitly in the pre-execution evidence record.

## 5. Exact scope

**In scope:**
- Identification of declared human gate milestones from program manifests and state machine definitions.
- Implementation of fail-closed gate halting logic in the workflow dispatcher and operator runtime.
- Atomic lifecycle transition from `RUNNING` to `AWAITING_APPROVAL` upon reaching a declared human gate.
- Creation of an immutable gate snapshot payload capturing the exact state version, state hash, gate identifier, required authority lane (`COMMANDER`), and candidate outputs awaiting review.
- Suspension of active worker leases to prevent background workers from advancing the state while awaiting human authorization.
- Positive and negative executable tests proving that execution halts at gate boundaries and refuses unauthorized turn execution.

**Out of scope:**
- Operator approval receipt verification and reactive workflow resumption (authorized under `CA-M041`).
- Rejection disposition routing and rewind mechanics (authorized under `CA-M041`).
- Database-level atomic CAS transitions inside SQLite (authorized under `CA-M042`).
- Modifications to upstream research or downstream video composition packages.

## 6. Allowed artifacts and file boundary

Allowed code modifications are strictly confined to:
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
- `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (host runner gate check hook)
- `api/routers/programs.py` (execution status presentation)
- Direct automated test files under `packages/ca_runtime/tests/` or `tests/` dedicated to gate suspension.

New files are permitted only if they represent focused unit/integration tests proving gate halting behavior. Modifying schema migrations or unrelated routers is strictly prohibited.

## 7. Prohibitions and collision procedure

1. **Prohibition on Mock Auto-Advance:** No test harness or execution runner may implement an automatic boolean bypass that skips `AWAITING_APPROVAL` status under live or simulated modes.
2. **Prohibition on Downstream State Mutation:** The runtime must not compute, emit, or persist downstream node states while the aggregate resides in `AWAITING_APPROVAL`.
3. **Prohibition on Lease Retention:** An execution worker must not hold an active exclusive write lease while waiting for human authorization; leases must be released or marked suspended.
4. **Collision Procedure:** If an existing program package contains conflicting gate definitions or bypass flags, the executor must halt, record the collision in the execution log, and defer to the Operator.

## 8. Required work / implementation behavior

1. **Gate Milestone Detection:** When `UniversalProgramStateRuntime` or `ProductionAgentWorkflowDispatcher` evaluates node completion, it must query the program manifest for `human_gate_milestone` declarations.
2. **Fail-Closed Halt:** If the next pending transition is gated by human authorization, the runtime must refrain from dispatching subsequent agent invocations.
3. **Atomic State Suspension:** Transition the aggregate lifecycle state to `ProgramStateLifecycle.AWAITING_APPROVAL`. Persist the suspension record containing `gate_id`, `required_lane: AuthorityLane.COMMANDER`, `suspended_at`, and `state_hash`.
4. **Lease De-escalation:** Release or suspend the active worker lease (`lease_worker_id = NULL`, `lease_expires_at = NULL`), transitioning the job out of active worker queues.
5. **State Grammar:**
   ```text
   RUNNING (active worker node execution)
     → evaluate_gate_milestone(node_id, gate_id)
     → AWAITING_APPROVAL (lease suspended, gate snapshot persisted)
   ```

## 9. Verification and evidence standard

The executor must produce executable proof demonstrating:
1. **Positive Gate Suspension Test:** A program execution (e.g. `collision_discovery_program`) advances through autonomous steps and halts immediately upon reaching `hypothesis_approval_gate`, asserting `aggregate.lifecycle == ProgramStateLifecycle.AWAITING_APPROVAL`.
2. **Negative Advancement Countertest:** An attempt to dispatch subsequent agent turns or execute transitions while the aggregate is in `AWAITING_APPROVAL` raises a typed `ProgramTransitionBlockedError` or HTTP 400 with error code `GATE_AWAITING_APPROVAL`.
3. **Worker Lease Release Test:** Verification that after halting, the worker lease is unassigned and worker polling ignores the suspended aggregate.
4. **Anti-Centroid Test:** Proving that the system rejects "optimistic execution" (where downstream compute runs speculatively before approval is granted).

## 10. Completion and stop condition

The mandate is complete ONLY when:
1. All declared physical code surfaces are updated and pass syntax/linting checks.
2. Positive and negative automated test suites execute and pass against the real runtime.
3. A formal completion record `CA_M040_COMPLETION_RECORD.md` is authored citing exact test outputs, file diffs, and commit hash.
4. The executor stops calling tools and presents the completion evidence to the Operator.

## 11. Rollback / recovery

If the gate suspension logic causes unexpected deadlocks or disrupts existing non-gated program executions:
1. Revert modifications in `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` via git checkout.
2. Non-gated programs continue standard autonomous execution.
3. Gate-requiring programs revert to explicit manual pause states without corrupting persisted aggregate versions.

## 12. Operator decision

The Operator is asked to review the test evidence demonstrating fail-closed gate halting and ratify:
- Does the execution engine reliably halt at declared human gate milestones without speculative execution?
- Is `ProgramStateLifecycle.AWAITING_APPROVAL` correctly reflected across API responses?
- Upon ratification, authorize progression to `CA-M041` (Reactive Gate Resumption and Disposition Routing).

## 13. Activation prompt

You are directed to execute mandate CA-M040 under the strict authority of docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md, the Master 57-Question Decision & Convergence Canon (specifically Question 40), and FUNCTIONAL_REQUIREMENTS.md (FR-040). Your single operational objective is to implement genuine, fail-closed human gate milestone suspension and completely eliminate mock auto-approvals across packages/ca_runtime/src/ca_runtime/program_operator_runtime.py, packages/ca_runtime/src/ca_runtime/program_state_runtime.py, and api/routers/programs.py.

Under historical development test fixtures, milestone gates were frequently simulated via boolean flags or auto-advancing bypasses, violating prediction safety. Under this mandate, whenever an autonomous pipeline execution reaches a declared human milestone gate boundary (such as hypothesis_approval_gate, editorial_approval_gate, or script_approval_gate), the runtime engine must immediately halt worker execution, transition the program aggregate lifecycle atomically to ProgramStateLifecycle.AWAITING_APPROVAL, freeze an immutable state snapshot with exact state hashes, release all active worker leases, and emit an audit event. Downstream mutations or speculative agent turns are strictly prohibited while suspended.

You are explicitly forbidden from authoring gate resumption mechanics, approval receipts, disposition rewinds, or SQLite CAS predicates, as those boundaries are reserved for CA-M041 and CA-M042. You must first inspect current physical code reality, document any mock bypass defects, author positive gate-halting tests and negative turn-dispatch blocking countertests, execute the test suite to produce concrete verification evidence with exit codes and execution logs, update control state, compile CA_M040_COMPLETION_RECORD.md, and immediately stop to present your findings for human Operator sign-off.
