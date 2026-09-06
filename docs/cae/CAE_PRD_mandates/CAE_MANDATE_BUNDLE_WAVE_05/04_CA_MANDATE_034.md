# CAE Mandate 034 — Real Program Execution Dispatch (Two-Phase Atomic Lease)

**Mandate ID:** `CA-M034`  
**Wave:** `05`  
**Canonical question:** `Q34`  
**Status:** `EXECUTION READY — bounded implementation mandate`

## 1. Identity and status

This mandate implements Canonical Question 34 (Spine Q01) of the ratified CAE 57-Question Decision & Convergence Canon. It is one member of Wave 05, covering Questions 32–39. The mandate is subordinate to the CAE Mandate Authoring Protocol and subordinate in semantic authority to the Master 57-Question Canon and the Product Brief/PRD/Functional Requirements layer (especially INV-DISP-001).

The purpose is to convert the ratified decision into executable repository behavior and evidence without changing the constitutional decision itself. The executor must work from the existing codebase and preserve existing compatible behavior. “Complete” means the requested property is physically represented, validated, tested, and evidenced; it does not mean that every adjacent CAE capability is complete.

### Governing authority distinction

- **Source of meaning:** the Master 57-Question Canon and the cited Product Brief/PRD materials.
- **Runtime authority:** the canonical CAE runtime and its authoritative state/command paths, particularly program operator and state runtime surfaces.
- **Change/promotion authority:** the human Operator/Commander and repository governance required by the project.

No YAML, database row, UI flag, model response, or generated artifact becomes authoritative merely because it exists.

## 2. Decision / objective being authorized

**Ratified decision (Canon Q34):** Two-phase atomic dispatch: Phase 1 registers the aggregate in SQLite at version 0 and enqueues lease (`LEASE_ENQUEUED`); Phase 2 acquires the lease via atomic CAS (0 → 1), refreshes context, and triggers the workflow. Program execution requires atomic two-phase lease acquisition (`INV-DISP-001`).

**Objective of this mandate:** Replace any non-atomic or synthetic program start path with a real two-phase atomic lease dispatch so that concurrent or crashed starts cannot leave the system in an inconsistent RUNNING state without a lease.

## 3. Governing doctrine and authority sources

- Master 57-Question Decision & Convergence Canon, Question 34.
- `FUNCTIONAL_REQUIREMENTS.md` entry for `INV-DISP-001`.
- Physical surfaces: `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`, `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`.
- Inherited authorization and production-authorization contracts from earlier waves.
- `Architecture.md` execution and state-machine sections.

## 4. Mandatory reading before action

Before any edit the executor MUST:

1. Read the Mandate Authoring Protocol.
2. Read Canon Q34 and the corresponding invariant entry in full.
3. Inspect the current `run_program()` / dispatch path in `program_operator_runtime.py` and the aggregate/lease handling in `program_state_runtime.py`.
4. Locate any path that initializes state without a two-phase atomic lease.
5. Confirm SQLite aggregate versioning and any existing CAS primitives.
6. Do not implement full workflow agent resolution (Q35) or context projection (Q36) under this mandate.

Document the current state before proposing changes.

## 5. Exact scope

**In scope**

- Two-phase atomic dispatch: (1) register aggregate at version 0 + enqueue lease; (2) atomic CAS lease acquisition then trigger workflow.
- Fail-closed behavior when CAS fails (stale version / concurrent claim).
- Positive and negative executable tests at the real operator/state boundary, including concurrent claim attempts where feasible.
- Minimal schema changes required for lease state if not already present.

**Out of scope**

- Production workflow dispatcher agent resolution (Q35).
- Lane-masked context projection (Q36).
- Live host runner loops (Q37).
- Provider routing or output parsing (Q38–Q39).
- Full zombie-lease reconciliation (later wave).

**Dependencies**

- Existing SQLite aggregate and version fields.
- Existing program operator entry points.

## 6. Allowed artifacts and file boundary

Allowed surfaces (illustrative; executor must confirm actual paths):

- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
- Related tests for dispatch and lease acquisition
- Minimal migration/schema for lease fields if required

Prohibited surfaces include synthetic adapters that bypass lease acquisition, unrelated API routers beyond the minimum dispatch surface, and later CAS-heavy transition logic beyond the lease CAS required here.

## 7. Prohibitions and collision procedure

- Do not leave a program in RUNNING without a successfully acquired lease.
- Do not implement a non-atomic read-modify-write for lease acquisition.
- Do not implement full workflow agent resolution or context projection under this mandate.
- Do not weaken existing authorization checks that gate who may start a program.
- If the current SQLite schema cannot support the two-phase pattern without a migration outside the smallest safe change, stop and report rather than inventing an in-memory lease.

On collision: halt, record the exact conflicting surface and the governing authority that cannot be satisfied, and request Operator direction.

## 8. Required work / implementation behavior

1. Identify the authoritative program start / dispatch path.
2. Implement Phase 1: register aggregate at version 0 and enqueue lease (LEASE_ENQUEUED).
3. Implement Phase 2: atomic CAS lease acquisition (0 → 1), context refresh, workflow trigger.
4. Ensure concurrent or failed CAS leaves the system consistent (no orphan RUNNING without lease).
5. Prefer the smallest change that makes two-phase atomic dispatch enforceable.

State transition (conceptual):

```text
source state: program start may initialize aggregate without atomic lease
→ operation: Phase1 register+enqueue; Phase2 CAS lease acquire then trigger
→ target state: execution proceeds only after atomic lease acquisition; CAS failure fails closed
```

Actor is the program operator / state runtime path. Preconditions include valid program identity and caller authority. Validators enforce CAS success. Postcondition is that RUNNING implies a held lease. Error route is LEASE_CONFLICT or equivalent fail-closed. Recovery is retry with fresh expected version or Operator intervention, never silent double-start.

## 9. Verification and evidence standard

Evidence must demonstrate two-phase atomic lease acquisition, not merely that a lease field exists.

Required proof classes:

- `EXECUTABLE` positive path: a program start completes both phases and holds a lease.
- `EXECUTABLE` negative path: concurrent or stale CAS fails closed without leaving inconsistent RUNNING.
- Integration evidence at the real operator/state boundary.
- False-proof countercase: a test that sets lease=1 in memory and asserts success. That proves labeling, not atomic two-phase dispatch.
- Environment fidelity: tests must exercise the repository’s real SQLite (or declared persistence) boundary for the CAS claim.

Verification MUST include positive acceptance, negative/fail-closed path, regression for an adjacent behavior, exact evidence locators, and residual unproven claims.

## 10. Completion and stop condition

Stop once two-phase atomic lease dispatch is implemented and evidenced at the authoritative operator/state boundary. If a broader concurrency redesign is required outside scope, stop after documenting the exact dependency and do not weaken the invariant.

Completion requires the requested behavior, passing tests, fail-closed negatives, no prohibited changes, recorded limitations, commit SHA, tracker update if applicable, and explicit Operator decision request.

## 11. Rollback / recovery

Any schema or persistence change must have a safe recovery story. Dispatch logic that is purely evaluative can be reverted by code; durable lease state must not leave aggregates permanently stuck without a documented recovery path.

## 12. Operator decision

Approve or reject based on whether the evidence proves that program execution requires atomic two-phase lease acquisition at the canonical runtime boundary.

The Operator must receive a concise evidence package: changed files, tests, exact locators, residual limitations, commit SHA, and the explicit approve/reject question.

## 13. 200–300 word activation prompt

> You are executing CAE mandate `CA-M034` only. Read the Mandate Authoring Protocol, the Master 57-Question Canon Q34, `INV-DISP-001`, `UI.md`, `Architecture.md`, and the current dispatch paths in `program_operator_runtime.py` and `program_state_runtime.py` before editing. Implement real two-phase atomic program execution dispatch: Phase 1 registers the aggregate at version 0 and enqueues lease; Phase 2 acquires the lease via atomic CAS then triggers the workflow. Do not implement workflow agent resolution, context projection, host runner loops, or provider routing. Do not leave programs RUNNING without a held lease. Establish positive and negative executable evidence at the real operator/state boundary, including concurrent CAS failure. Preserve existing compatible behavior and use the canonical runtime/persistence boundary. If a collision or missing dependency cannot be resolved within this scope, stop and report it. Completion requires changed files, tests, exact evidence locators, limitations, and commit SHA. Stop after the mandate is evidenced and request the Operator decision: approve or reject `CA-M034`. Before making any edit, inspect the current implementation and identify the authoritative boundary you will change. Do not infer missing behavior from documentation alone. Preserve existing compatible behavior, keep the change minimal, and test the failure mode that would otherwise create a convincing but invalid result. Do not continue into the next mandate. If a required source of authority is absent or contradictory, stop and report the collision. The completion report must distinguish executable proof from documentation, list every changed file, include exact test commands and evidence locations, state residual limitations, capture the exact commit SHA, and explicitly ask the Operator whether to approve or reject this mandate.
