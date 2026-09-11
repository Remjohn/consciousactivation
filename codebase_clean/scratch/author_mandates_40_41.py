import os
import re
import json


# -----------------------------------------------------------------------------
# MANDATE 40: CA-M040
# Real Human Gate Milestones & Fail-Closed Execution Suspension
# -----------------------------------------------------------------------------

m040_content = """# CA-M040 — Real Human Gate Milestones & Fail-Closed Execution Suspension

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
"""

# -----------------------------------------------------------------------------
# MANDATE 41: CA-M041
# Reactive Gate Resumption, Commander Receipts & Rejection Routing
# -----------------------------------------------------------------------------

m041_content = """# CA-M041 — Reactive Gate Resumption, Commander Approval Receipts & Rejection Disposition Routing

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
"""

# -----------------------------------------------------------------------------
# WRITE FILES AND VALIDATE WORD COUNTS
# -----------------------------------------------------------------------------

def count_words(text):
    return len(text.split())

def extract_section_13(text):
    m = re.search(r'## 13\. Activation prompt\s*\n+(.*)', text, re.DOTALL)
    return m.group(1).strip() if m else ''

m040_path = 'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md'
m041_path = 'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md'

with open(m040_path, 'w', encoding='utf-8') as f:
    f.write(m040_content)

with open(m041_path, 'w', encoding='utf-8') as f:
    f.write(m041_content)

total_words_040 = count_words(m040_content)
prompt_words_040 = count_words(extract_section_13(m040_content))

total_words_041 = count_words(m041_content)
prompt_words_041 = count_words(extract_section_13(m041_content))

print(f"Mandate 040: Total Words = {total_words_040} (Target > 700), Activation Prompt Words = {prompt_words_040} (Target 200-300)")
print(f"Mandate 041: Total Words = {total_words_041} (Target > 700), Activation Prompt Words = {prompt_words_041} (Target 200-300)")

assert total_words_040 > 700, f"Mandate 040 total words ({total_words_040}) < 700"
assert 200 <= prompt_words_040 <= 300, f"Mandate 040 prompt words ({prompt_words_040}) not in [200, 300]"
assert total_words_041 > 700, f"Mandate 041 total words ({total_words_041}) < 700"
assert 200 <= prompt_words_041 <= 300, f"Mandate 041 prompt words ({prompt_words_041}) not in [200, 300]"


# -----------------------------------------------------------------------------
# UPDATE WAVE 05 INDEX & MANIFEST
# -----------------------------------------------------------------------------

wave5_index_path = 'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/00_CA_MANDATE_BUNDLE_WAVE_05_INDEX.md'
with open(wave5_index_path, 'r', encoding='utf-8') as f:
    w5_idx = f.read()

# Update Scope and table
if '10_CA_MANDATE_040.md' not in w5_idx:
    w5_idx = w5_idx.replace('Scope:** Canonical Questions Q32–Q39', 'Scope:** Canonical Questions Q32–Q40 (including Gate Suspension & Resumption)')
    w5_idx = w5_idx.replace(
        "| `09_CA_MANDATE_039.md` | Q39 | `INV-OUT-001` |",
        "| `09_CA_MANDATE_039.md` | Q39 | `INV-OUT-001` |\n| `10_CA_MANDATE_040.md` | Q40 | `INV-GATE-001` |\n| `11_CA_MANDATE_041.md` | Q40 | `INV-GATE-002` / `INV-AUTH-001` |"
    )
    with open(wave5_index_path, 'w', encoding='utf-8') as f:
        f.write(w5_idx)
    print("Updated Wave 05 Index with Mandates 040 and 041")

wave5_manifest_path = 'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/BUNDLE_MANIFEST.json'
with open(wave5_manifest_path, 'r', encoding='utf-8') as f:
    w5_mani = json.load(f)

w5_mani['scope'] = "Q32-Q40"
w5_mani['files']['10_CA_MANDATE_040.md'] = {
    "words": total_words_040,
    "activation_prompt_words": prompt_words_040
}
w5_mani['files']['11_CA_MANDATE_041.md'] = {
    "words": total_words_041,
    "activation_prompt_words": prompt_words_041
}

with open(wave5_manifest_path, 'w', encoding='utf-8') as f:
    json.dump(w5_mani, f, indent=2)
print("Updated Wave 05 BUNDLE_MANIFEST.json")

# -----------------------------------------------------------------------------
# ALSO ADD BRIDGE TO WAVE 06 SO BOTH WAVES ARE COHERENT
# -----------------------------------------------------------------------------

# Also write to Wave 06 as 01_CA_MANDATE_040_041_BRIDGE.md or copy so it can be discovered from Wave 06
wave6_bridge_path = 'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/01_CA_MANDATES_040_041_BRIDGE.md'
bridge_content = f"""# Wave 05 / 06 Gate Governance Bridge: Mandates CA-M040 and CA-M041

This bridge document references the completed, execution-ready gate governance mandates covering Canon Question 40:

1. **`CA-M040` (Real Human Gate Milestones & Fail-Closed Execution Suspension):**
   - File: [`../CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md`](file:///d:/Work/consciousactivation/docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md)
   - Canonical Question: `Q40`
   - Primary Invariant: `INV-GATE-001` (`FR-040`)
   - Scope: Eliminates mock auto-approvals, halts execution at declared gates fail-closed, releases worker leases, transitions lifecycle to `AWAITING_APPROVAL`.

2. **`CA-M041` (Reactive Gate Resumption, Commander Approval Receipts & Rejection Routing):**
   - File: [`../CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md`](file:///d:/Work/consciousactivation/docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md)
   - Canonical Question: `Q40` / Bridge to `Q41`
   - Primary Invariant: `INV-GATE-002` / `INV-AUTH-001` (`FR-040`, `FR-025`)
   - Scope: Implements `approve_program` with `AuthorityLane.COMMANDER` validation, signed `AuthorizationDecisionReceipt` generation, and reactive `RESUME` signals; implements `reject_program` with typed `RejectionDispositionRoute` rewinds without evidence destruction.

These two mandates complete the prerequisite dependency chain (`Q34–Q40`) required by Wave 06 Mandate `CA-M042` (Atomic CAS State Transitions in SQLite).
"""

with open(wave6_bridge_path, 'w', encoding='utf-8') as f:
    f.write(bridge_content)
print("Created Wave 06 Bridge Document: 01_CA_MANDATES_040_041_BRIDGE.md")

print("All tasks completed successfully!")
