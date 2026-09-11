# Workflow Primitive Semantics Matrix & State Transfer Specification

**Mandate:** CAE-M57 (Phase 07 — Workflow Engineering)  
**Authority:** `docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml` & `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`  
**Status:** RATIFIED CANONICAL SPECIFICATION  
**Version:** 1.0.0  

---

## 1. Executive Summary & Core Doctrine

In the Conscious Activation Engine, **code owns deterministic control flow**, **Agents own bounded reasoning within steps**, **Skills remain passive**, and **State transitions follow checked transfer semantics**.

This specification defines the exact semantics, execution laws, failure/termination rules, state retention policies, and legal/illegal transition examples for the 14 ratified workflow primitives and 2 work-unit kinds.

---

## 2. Ratified Vocabulary

### 2.1 Control-Flow Primitives
1. `SEQUENCE`: Linear deterministic progression of steps.
2. `CONDITION`: Deterministic binary branch based on host-evaluated boolean predicates.
3. `SWITCH`: Deterministic multi-way pattern matching on host expressions with required default fallback.
4. `LOOP`: Host-bounded iteration with mandatory finite `max_iterations` bound and termination law.
5. `RETRY`: Same-step retry policy with bounded budget, backoff strategy, and error classification.
6. `PARALLEL`: Deterministic fan-out of concurrent branches with strict side-effect conflict isolation.
7. `JOIN`: Deterministic fan-in barrier for parallel branches (`ALL`, `ANY`, `QUORUM`) with error aggregation.
8. `TIMEOUT`: Host-enforced execution deadline duration preserving partial trace on expiration.
9. `WAIT`: Deterministic time delay, event wait, or barrier condition.
10. `HUMAN_GATE`: Explicit operator pause and approval/rejection boundary in COMMANDER lane.
11. `FAIL`: Explicit terminal failure with structured error code and source state preservation.
12. `REPAIR`: Governed repair step retaining source state, failed obligation, and prior receipts.
13. `CANCEL`: Controlled cancellation transitioning state aggregate to CANCELLED state.
14. `RESUME`: Controlled resumption from checkpointed/paused state validating idempotency.

### 2.2 Work-Unit Kinds
1. `AGENT_CALL`: Invocation of a canonical Agent object via compiled context capsule and gate engine.
2. `CODE_FUNCTION`: Deterministic host code execution (pure computation, database query, validation, linter, hash calculation) avoiding model token waste.

---

## 3. Workflow Primitive Semantics Matrix

| Primitive | Kind | Deterministic Execution Law | Failure / Termination Behavior | State Retention & Evidence Survival | Illegal Transition / Negative Example |
|---|---|---|---|---|---|
| **`SEQUENCE`** | Control | Executes child steps in strict ascending ordinal sequence `[0..N-1]`. Step `i+1` starts only after Step `i` succeeds. | If step `i` fails, sequence execution halts immediately; transitions to error handler or FAIL. | Progress through step `i-1` and step receipts are retained in run history. | Reordering steps dynamically at runtime or skipping step `i` without an explicit branch. |
| **`CONDITION`** | Control | Evaluates a deterministic host predicate against state/context. If `true`, routes to `then_step`; if `false`, routes to `else_step`. | If expression cannot be evaluated or raises exception, raises `ERR_UNEVALUABLE_CONDITION` and retains state. | Source state and condition evaluation outcome are appended to the audit trace. | Asking an LLM to hallucinate which branch to take instead of evaluating host predicate. |
| **`SWITCH`** | Control | Evaluates a deterministic host expression against discrete cases. Matches exact case or falls back to `default_step`. | If no case matches and `default_step` is missing, raises `ERR_UNEVALUABLE_CONDITION`. | Expression evaluation digest and matched case are preserved in run history. | Branching on non-deterministic or unindexed unstructured model text. |
| **`LOOP`** | Control | Iterates a body primitive while condition holds AND `iteration < max_iterations`. Host enforces loop bound. | If `iteration >= max_iterations` without condition satisfaction, terminates with `ERR_UNBOUNDED_LOOP` / `LOOP_EXHAUSTED`. | All intermediate iteration receipts, state diffs, and loop counter survive. | Agent mutating `max_iterations` at runtime or configuring `max_iterations <= 0`. |
| **`RETRY`** | Control | Retries a failed step up to `max_attempts` using specified backoff strategy (`CONSTANT`, `LINEAR`, `EXPONENTIAL`). | If budget exhausted or `NonRetryableError` occurs, raises `ERR_RETRY_BUDGET_EXHAUSTED`. | Retains source state, prior failed attempts, and error records in `BoundedRepairSession`. | Resetting retry budget infinitely or silently clearing previous attempt failures. |
| **`PARALLEL`** | Control | Dispatches independent branches concurrently. All branches must have side-effect class `NONE` or `READ_ONLY`. | If any branch encounters an error, child branch is aborted and join aggregates failure. | Branch outputs and partial execution traces are tagged by `branch_id`. | Spawning concurrent branches that both attempt `MUTATION_OPERATION` on the same aggregate. |
| **`JOIN`** | Control | Synchronization barrier waiting for parallel branches per policy: `ALL` (wait for all), `ANY` (first), `QUORUM` (N). | If required policy criteria cannot be met (e.g. quorum impossible due to failures), join fails. | Aggregates all branch receipts into a composite join receipt. | Continuing execution before required join policy is satisfied. |
| **`TIMEOUT`** | Control | Host-enforced deadline duration in seconds/ms. Cancels underlying task if duration exceeded. | Raises `ERR_EXECUTION_TIMEOUT`; records timeout duration and execution state at cutoff. | Partial output, trace nodes up to timeout, and timeout event survive in state ledger. | Silently extending timeout without operator grant or ignoring timeout signal. |
| **`WAIT`** | Control | Suspends execution until explicit timestamp, duration, or published external event arrival. | If wait condition times out or target event fails authentication, aborts wait. | Aggregate enters `PAUSED` / `WAITING` state; checkpoint is committed. | Polling in a tight CPU loop rather than registering a governed wait barrier. |
| **`HUMAN_GATE`** | Control | Suspends execution awaiting operator decision (`APPROVE` / `REJECT` / `REPAIR`) in COMMANDER lane. | Rejection routes to specified disposition; timeout aborts or pauses per policy. | Gate receipt with operator ID, rationale, and timestamp is immutably committed. | Agent generating a synthetic approval receipt to self-approve its own output. |
| **`FAIL`** | Control | Explicit terminal step marking aggregate as `FAILED`. Halts further execution. | Terminal state; no outgoing transitions permitted. | Retains failure code, reason, causal lineage, and all accumulated receipts. | Attempting an outbound transition from terminal `FAILED` state without new command. |
| **`REPAIR`** | Control | Enters bounded repair cycle preserving source state, re-invoking agent/operator with failure diagnosis. | If repair budget exhausted, escalates to `FAIL` or `HUMAN_GATE`. | Retains failed obligation, repair attempt record, and diagnostic feedback. | Overwriting original error context or advancing state before repair succeeds. |
| **`CANCEL`** | Control | Gracefully terminates active tasks and marks aggregate as `CANCELLED`. | Terminal state; active subagents/invocations receive cancel signal. | Final cancellation receipt and cancellation trigger provenance are recorded. | Leaving background worker tasks running orphaned after cancellation. |
| **`RESUME`** | Control | Resumes execution of a `PAUSED` aggregate after validating state hash and expected version. | If state version has drifted or aggregate is `TOMBSTONED`, raises version conflict. | Resumes from exact checkpoint, preserving full prior execution history. | Resuming an already active or completed execution (duplicate resume). |
| **`AGENT_CALL`** | Work Unit | Compiles context capsule, executes model invocation via bridge, validates output schema and gates. | If gate fails, returns typed failure result; triggers repair or failure handler. | Generates non-repudiable `AgentInvocationReceipt` with prompt/response hashes. | Executing uncompiled prompt or bypassing output contract schema validation. |
| **`CODE_FUNCTION`** | Work Unit | Executes pure host Python function (computation, transformation, validation, database read). | Unhandled exception captured, typed, and routed to error handler. | Execution receipt with function ref, duration, and output digest is committed. | Spending model tokens on deterministic calculations that belong in code. |

---

## 4. Checked Transfer Semantics (StateM Alignment)

Under `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`, state transitions are **context-and-contract boundaries**. Every state transition must follow the strict 6-stage protocol:

```
[Source State]
      │
      ▼
1. Validate Transition Edge (Edge must exist in StateTransitionContract)
      │
      ▼
2. Blocking Pre-Transfer Checks (e.g. QA gates, schema validators, policy checks)
      │  └── If FAILED: ABORT transfer, RECORD failure, RETAIN source state.
      ▼
3. Execute Persistence & Out-Hooks (Flush checkpoint, run on_exit hooks)
      │
      ▼
4. Evaluate Edge Guards & Transition Hooks (Dynamic invariants, transfer locks)
      │
      ▼
5. Commit Target State & Update History (Increment aggregate_version by +1)
      │
      ▼
6. Run In-Hooks & Refresh Entry Context (Recompile JITContextCapsule for target state)
      │
      ▼
[Target State]
```

### Invariant: Source State Retention
If any check in Steps 1–4 fails:
1. The execution state aggregate **MUST remain in the source state**.
2. `aggregate_version` is **NOT incremented**.
3. A `FailedObligationRecord` is attached to the run record.
4. Execution may transition to `REPAIR` or `HUMAN_GATE` within the same source state context.

---

## 5. Parallel Concurrency & Side-Effect Law

When executing a `PARALLEL` primitive:
1. Every branch must declare its `side_effect_class`:
   - `NONE`: Pure computation; no external state read or write.
   - `READ_ONLY`: Reads state or storage; zero mutations.
   - `MUTATION_OPERATION`: Performs typed state mutations on an aggregate.
2. **Concurrency Rule:** Multiple branches may execute concurrently if and only if **ALL branches declare `NONE` or `READ_ONLY`**.
3. If two or more branches declare `MUTATION_OPERATION`, the workflow compiler/validator **MUST reject the workflow with `ERR_PARALLEL_SIDE_EFFECT_CONFLICT`**.

---

## 6. Contrastive Legal vs. Illegal Transition Examples

### 6.1 Loop Primitive
- **Legal:**
  ```python
  loop = WorkflowPrimitiveDefinition(
      primitive_id="PRIM-LOOP-001",
      primitive_kind=WorkflowPrimitiveKind.LOOP,
      loop_policy=LoopBoundPolicy(max_iterations=3, timeout_seconds=300, allow_agent_override=False),
  )
  ```
- **Illegal (Rejected with `ERR_UNBOUNDED_LOOP`):**
  ```python
  loop = WorkflowPrimitiveDefinition(
      primitive_id="PRIM-LOOP-BAD",
      primitive_kind=WorkflowPrimitiveKind.LOOP,
      loop_policy=LoopBoundPolicy(max_iterations=0),  # INVALID: must be > 0
  )
  ```

### 6.2 Checked Transfer Pre-Check Failure
- **Legal (Source State Preserved):**
  - Run in `ANALYSIS_IN_PROGRESS` state.
  - Pre-transfer check `EVAL_SCORE_GE_80` fails (score is 65).
  - State remains `ANALYSIS_IN_PROGRESS`.
  - Failure recorded in `RepairAttemptRecord`.
  - Next step is `REPAIR` within `ANALYSIS_IN_PROGRESS`.
- **Illegal (Rejected as `StateRetentionViolationError`):**
  - Pre-transfer check fails, but runtime advances `current_state` to `COMPOSITION_READY` and then sets an error flag.

### 6.3 Parallel Side-Effect Isolation
- **Legal:**
  - Branch A: `AnalyzeEvidence` (`side_effect_class="READ_ONLY"`).
  - Branch B: `SynthesizeKeywords` (`side_effect_class="READ_ONLY"`).
  - Both branches run concurrently.
- **Illegal (Rejected with `ParallelSideEffectConflictError`):**
  - Branch A: `UpdateWorkspaceGuest` (`side_effect_class="MUTATION_OPERATION"`).
  - Branch B: `UpdateWorkspaceGuest` (`side_effect_class="MUTATION_OPERATION"`).
  - Compiler rejects workflow before execution starts.
