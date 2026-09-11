# CA-M041 — Reactive Gate Resumption, Commander Approval Receipts & Rejection Disposition Routing

## 1. Identity and status

- **Mandate ID:** `CA-M041`
- **Canonical question:** `Q40` (Phase 2: Gate Resolution, Resumption & Rejection Routing)
- **Wave:** `05`
- **Status:** `EXECUTION READY — bounded implementation mandate`
- **Primary requirement/invariant:** `INV-GATE-002` / `INV-AUTH-001` (`FR-040`, `FR-025`)
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q34–Q39 execution spine; CA-M040 gate suspension contract (`INV-GATE-001`); existing `approve_program` and `reject_program` endpoints
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py; api/routers/programs.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; focused gate-resolution tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement and authoritatively prove the reactive gate resolution contract for CAE program executions. While `CA-M040` ensures that executions halt fail-closed in `AWAITING_APPROVAL`, a severe costly exposure arises if gate resolution relies on unvalidated operator inputs, unauthenticated role assumptions, or destructive error recovery that deletes upstream evidence.

The objective of this mandate is to establish a typed, cryptographically grounded resolution mechanism for suspended human gates across both approval and rejection paths:
1. **Positive Approval Path:** When an operator submits gate approval via `POST /executions/{aggregate_id}/approve` or `approve_program()`, the runtime must verify that the caller exercises `AuthorityLane.COMMANDER`. It must emit an immutable, signed `AuthorizationDecisionReceipt` binding the gate ID, actor identity, decision timestamp, and state digest. It must emit a reactive `RESUME` signal, re-acquire an exclusive worker lease via atomic CAS, and resume autonomous agent execution.
2. **Negative Rejection Path:** When an operator rejects a gate via `POST /executions/{aggregate_id}/reject` or `reject_program()`, the runtime must enforce a typed `RejectionDispositionRoute` (`RETURN_TO_HUNTER`, `RETURN_TO_ANALYST`, `RETURN_TO_COMPOSER`, or `ARCHIVE`). It must emit a signed `GateRejectionReceipt` containing feedback notes and rewind the state machine safely to the designated target node without mutating or deleting raw evidentiary artifacts.

This mandate bridges the suspension foundation of `CA-M040` to the atomic CAS mechanics of `CA-M042`.

## 3. Governing doctrine and authority sources

Semantic authority derives from the Master 57-Question Decision & Convergence Canon (specifically Question 40 and Question 25) and `docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md` (`FR-040`, `FR-025`). Runtime authority is the canonical CAE program operator runtime service (`ProgramOperatorRuntimeService`) and API router (`api/routers/programs.py`). Change and promotion authority remains with the human Operator acting under `COMMANDER` authority.

Primary references:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar and evidence standards.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — execution sequence, failure classes, and stop conditions.
3. `docs/cae/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q40 decision text (`INV-GATE-001`, `INV-AUTH-001`).
4. `docs/cae/cae-bmad/03_product/modules/PRD-005.md` — operator supervision and gate authorization specifications.
5. Physical code surfaces: `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py:L429-L570`, `api/routers/programs.py:L280-L360`, and `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`.

## 4. Mandatory reading before action

Before executing any code modifications, the executor MUST read the complete contents of:
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` (Question 40 and Question 25)
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` (specifically `approve_program`, `reject_program`, and `RejectionDispositionRoute`)
- `api/routers/programs.py` (endpoints `/executions/{aggregate_id}/approve` and `/executions/{aggregate_id}/reject`)
- `CA_M040_COMPLETION_RECORD.md` (verifying that gate suspension is operational)

The executor must inspect the current implementation of `approve_program` to verify whether it emits real cryptographic receipts or falls back to informal state repairs.

## 5. Exact scope

**In scope:**
- Strict `AuthorityLane.COMMANDER` validation on all approval and rejection requests, raising `ProgramAuthorityLaneViolationError` upon violation.
- Generation and persistence of signed `AuthorizationDecisionReceipt` records linking `aggregate_id`, `version`, `gate_id`, and `state_hash`.
- Emitting reactive resumption events that trigger worker lease acquisition and advance lifecycle state from `AWAITING_APPROVAL` back to `RUNNING`.
- Implementation of typed `RejectionDispositionRoute` execution (`RETURN_TO_HUNTER`, `RETURN_TO_ANALYST`, `RETURN_TO_COMPOSER`, `ARCHIVE`), transitioning state safely to the target node while preserving upstream evidence.
- Full positive and negative integration tests exercising API endpoints and operator runtime methods.

**Out of scope:**
- Halting and lifecycle suspension into `AWAITING_APPROVAL` (governed by `CA-M040`).
- Underlying SQLite atomic CAS transaction predicates (`UPDATE ... WHERE version = expected_version`, governed by `CA-M042`).
- Merkle parent-hash chaining across the transitions table (`CA-M043`).
- In-memory operator preemption and mid-flight abort sockets (`CA-M046`).

## 6. Allowed artifacts and file boundary

Allowed changes are strictly limited to:
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- `api/routers/programs.py`
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` (receipt persistence helpers)
- Direct automated test files under `packages/ca_runtime/tests/` or `tests/api/` validating gate approval and rejection.

New files are restricted to test suites and the mandate completion record. Modifying database schemas or external provider integrations is prohibited.

## 7. Prohibitions and collision procedure

1. **Prohibition on Non-Commander Authorization:** Non-Commander callers (e.g. `AuthorityLane.HUNTER` or unauthenticated API callers) must never be permitted to authorize gates or trigger resumption.
2. **Prohibition on Destructive Rejection:** Rejecting a gate must never purge, overwrite, or mutate raw interview evidence, research transcripts, or earlier committed aggregate versions.
3. **Prohibition on Transient Approvals:** Approvals must be backed by durable, cryptographically hashed receipts in SQLite; storing approvals exclusively in memory or transient cache is forbidden.
4. **Collision Procedure:** If an approval transition conflicts with an already-advanced aggregate version, the runtime must reject the request with a typed `ProgramStateVersionConflictError` (HTTP 409) and require operator reconciliation.

## 8. Required work / implementation behavior

1. **Commander Lane Enforcement:** In `approve_program` and `reject_program`, enforce `if actor_lane != AuthorityLane.COMMANDER: raise ProgramAuthorityLaneViolationError(...)`.
2. **Signed Receipt Generation:** Construct an immutable receipt payload containing `receipt_id = f"rcpt_appr_{sha256(...)}"`, `gate_id`, `actor_id`, `decision: "APPROVE"`, timestamp, and snapshot hash. Persist receipt to aggregate metadata and transitions ledger.
3. **Reactive Resumption Flow:** When approval commits, transition aggregate lifecycle to `ProgramStateLifecycle.RUNNING`. Enqueue or trigger worker lease acquisition to resume execution at the node immediately following the gate.
4. **Disposition Routing Flow:** When rejection commits, inspect `disposition_route`. Map route to target state (`initial_state`, `REQUIREMENTS_EXTRACTED`, or `FAILED`). Rewind state machine cleanly, increment version, and record `GateRejectionReceipt`.
5. **State Grammar:**
   ```text
   Approval Path:
   AWAITING_APPROVAL → approve_program(gate_id, COMMANDER) → RUNNING (receipt persisted, lease enqueued)
   
   Rejection Path:
   AWAITING_APPROVAL → reject_program(gate_id, route) → REWOUND_STATE (rejection receipt persisted, feedback attached)
   ```

## 9. Verification and evidence standard

The executor must produce executable proof demonstrating:
1. **Positive Gate Approval Test:** An aggregate suspended in `AWAITING_APPROVAL` receives `approve_program()` with Commander credentials, asserting lifecycle transitions to `RUNNING`, a valid receipt is recorded, and workflow execution resumes.
2. **Negative Authority Lane Countertest:** An approval request submitted with `actor_lane = AuthorityLane.HUNTER` or `ANALYST` raises `ProgramAuthorityLaneViolationError` (HTTP 403) and leaves state unchanged.
3. **Rejection Disposition Route Test:** An aggregate rejected with `RETURN_TO_HUNTER` transitions state back to `initial_state`, attaches feedback notes, and preserves all earlier transition logs.
4. **Version Conflict Countertest:** An approval request presenting a stale `expected_version` raises `ProgramStateVersionConflictError` without advancing state.

## 10. Completion and stop condition

The mandate is complete ONLY when:
1. Physical code surfaces in `program_operator_runtime.py` and `programs.py` are updated and validated.
2. Automated test suites verify approval receipts, lane enforcement, and disposition rewinds against the real runtime.
3. A formal completion record `CA_M041_COMPLETION_RECORD.md` is generated with full test logs, commit SHA, and artifact diffs.
4. The executor stops execution and requests formal Operator sign-off.

## 11. Rollback / recovery

If gate resumption causes unexpected deadlocks or routing failures:
1. Revert modifications in `program_operator_runtime.py` and `programs.py` via git checkout.
2. Suspended aggregates remain safely in `AWAITING_APPROVAL` without data corruption.
3. Offline operator intervention can inspect aggregate state directly via `UniversalProgramStateRuntime.get_aggregate()`.

## 12. Operator decision

The Operator is asked to review the test evidence demonstrating reactive resumption and ratify:
- Does `approve_program` reliably verify Commander authority and generate durable, signed receipts?
- Does `reject_program` correctly execute typed disposition routing without destroying upstream evidence?
- Upon ratification, authorize progression to `CA-M042` (Atomic CAS State Transitions in SQLite).

## 13. Activation prompt

You are directed to execute mandate CA-M041 under the strict authority of docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md, the Master 57-Question Decision & Convergence Canon (specifically Question 40 and Question 25), and FUNCTIONAL_REQUIREMENTS.md (FR-040, FR-025). Your operational objective is to implement the reactive gate resolution contract, durable signed Commander authorization receipts, and typed rejection disposition routing across packages/ca_runtime/src/ca_runtime/program_operator_runtime.py, packages/ca_runtime/src/ca_runtime/program_state_runtime.py, and api/routers/programs.py.

While CA-M040 establishes fail-closed suspension into AWAITING_APPROVAL, CA-M041 governs the dual resolution paths. On approval submission via approve_program or POST /executions/{aggregate_id}/approve, you must strictly verify AuthorityLane.COMMANDER, generate a cryptographically signed AuthorizationDecisionReceipt containing gate identity, actor fingerprint, timestamp, and snapshot digest, emit a reactive RESUME event, and transition lifecycle state to RUNNING. On rejection via reject_program or POST /executions/{aggregate_id}/reject, you must enforce typed RejectionDispositionRoute routing (RETURN_TO_HUNTER, RETURN_TO_ANALYST, RETURN_TO_COMPOSER, ARCHIVE), attach structured feedback, and safely rewind the state machine without purging, overwriting, or corrupting upstream evidentiary artifacts.

You are strictly forbidden from authoring initial gate suspension logic (reserved for CA-M040) or underlying SQLite CAS transaction queries (reserved for CA-M042). You must inspect existing physical reality in program_operator_runtime.py, construct positive approval tests asserting signed receipts and resumption, author negative authority countertests asserting rejection of non-Commander callers, test disposition route rewinds, verify evidence persistence, record exhaustive execution logs with exact terminal outputs, generate CA_M041_COMPLETION_RECORD.md, update control state, and halt execution to request Operator review.
