# CA-M046 — Real Operator Control and Preemption

## 1. Identity and status

- **Mandate ID:** `CA-M046`
- **Canonical question:** `Q45`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-PREEMPT-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q34–Q44 execution, state, lease, and gate semantics
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py; api/routers/programs.py; cancellation token/worker execution path; abort tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement the ratified operator abort/preemption boundary so an authorized Operator can terminate an active execution through `POST /executions/{id}/abort`, cause an atomic aggregate transition to `CANCELLED`, and propagate cancellation to active model sockets, tools, and worker loops where the runtime supports cancellation. The objective is not a cosmetic “cancel” button. It is a real control path from API command to authoritative state transition to execution interruption, with evidence showing that long-running activity does not continue after cancellation acceptance. The system must remain fail-closed when authorization or state predicates do not permit the abort.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority comes from Q45 and the runtime supervision doctrine. Runtime authority is the canonical execution aggregate and cancellation token/worker control boundary. API/UI are projections and control entry points, not alternate state stores. Operator authority is explicit and must be validated by the existing authorization system; an agent or browser cannot self-grant it. The executor may wire the command only through existing typed operation/state helpers and must preserve Q41 CAS semantics and Q40 gate behavior. If the currently named route is absent or differs, the executor must reconcile with existing API conventions rather than create a parallel endpoint without authority.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q45`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q45`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q45` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py; api/routers/programs.py; cancellation token/worker execution path; abort tests`
- Q45 decision; `program_operator_runtime.py`; `api/routers/programs.py`; agent invocation loop; socket/tool cancellation implementation; authorization helpers; abort/cancel tests.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M046` / `Q45` as defined by the ratified canon and the physical surfaces named above.

Implement and prove the operator abort command for active execution: route or route completion where missing; authorization check; atomic state transition to `CANCELLED`; cancellation token propagation into active work; durable receipt/audit record through existing state mechanisms; and focused tests. Inputs are an execution identifier, authenticated/authorized operator context, current aggregate state/version, and active runtime handle when present. Outputs are a durable cancellation transition and termination request/observation. Operators allowed are authorized Operator plus runtime executor. Validators must test successful abort, unauthorized abort, abort of already-terminal execution, stale-state conflict, and interruption of a long-running tool/model path.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py; api/routers/programs.py; cancellation token/worker execution path; abort tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not use a UI-only flag, process kill, or database status flip as a substitute for the runtime cancellation path. Do not kill unrelated worker processes. Do not bypass authorization. Do not mark `CANCELLED` while leaving active sockets/tools running without recording that cancellation was requested but not yet observed; the state semantics must follow the existing runtime contract. Do not silently turn abort into pause or rewind. Do not add arbitrary new lifecycle states. Do not implement a new job scheduler or orchestration layer. If a third-party client cannot be interrupted safely, stop and record the environment limitation rather than claiming synchronous termination.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace the current operator-command path, aggregate state transition function, and active execution object. Implement or complete the abort route so it validates workspace, operator authority, execution existence, current state, and expected version. Perform the state transition through the canonical CAS/state-runtime path. Bind the aggregate to an in-memory cancellation token or repository-equivalent execution control primitive that active loops check at safe boundaries. Ensure model sockets and tools are interrupted using existing cancellation mechanisms where available. The command should be idempotent or explicitly reject repeat aborts according to existing state semantics, and it must create a receipt for the accepted transition. Test a long-running synthetic or controlled integration path only if it represents the real cancellation machinery; mocks that never enter the worker loop do not prove interruption. Also test that unauthorized users and cross-workspace identifiers are rejected. Capture observed timing as evidence only; do not claim a universal milliseconds guarantee unless a contract exists.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Proof must show the complete control chain from authorized operator request to authoritative `CANCELLED` state and interruption observation. Positive evidence: API call, state receipt, worker/runtime observation. Negative evidence: unauthorized request, stale version, already-terminal execution, and cross-workspace identifier. The verifier measures command authorization, CAS transition, and cancellation propagation; it does not prove cancellation of every possible third-party library under every network condition. False-proof countercase: POST endpoint returns 200 and a database row becomes `CANCELLED` while the model request continues in another thread/process; reject. Environment fidelity requires the actual execution control boundary and at least one real interruptible long-running path.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop if authorization or execution-control ownership is ambiguous, if cancellation cannot reach the active worker boundary, or if an abort could incorrectly cancel another workspace or execution. Stop after evidence and operator decision request; do not proceed to tenant/sandbox hardening.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Rollback the route/control code in isolation. Preserve cancellation receipts and historical terminal state. If an active execution becomes stuck because of a broken cancellation hook, use the project’s established operational recovery rather than editing its state blindly. Any ambiguity about force-killing a process is an Operator decision.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M046` based on end-to-end proof that an authorized operator can preempt an active execution, durably transition it to `CANCELLED`, and interrupt the real execution path without cross-scope side effects.

## 13. 200–300 word activation prompt

Execute `CA-M046` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q45 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, `program_operator_runtime.py`, `api/routers/programs.py`, and the current agent/tool cancellation path. Implement `INV-PREEMPT-001`: an authorized abort command must atomically transition an active execution to `CANCELLED` and propagate cancellation to active model/tool work through the real runtime control path. Scope is the abort API/control operation, authorization, CAS transition, cancellation token propagation, receipt/audit evidence, and focused tests. Do not use a UI flag, direct SQL status flip, unrelated process kill, pause/rewind substitution, or new lifecycle states. Prove positive end-to-end abort, unauthorized rejection, stale-state rejection, terminal-state behavior, and at least one real long-running interruptible path. A 200 response plus a database row change while the worker continues is a false proof. Record exact environment, timing limitations, evidence classes, and cross-workspace negative proof. Stop if cancellation cannot reach the authoritative worker boundary. Completion requires changed files, exact test evidence, control-state update, limitations, commit SHA, and the Operator decision request: approve or reject `CA-M046`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

