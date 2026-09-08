# CA-M035 Agent Handoff

## Mandate

`CA-M035` — Workflow Dispatcher Runtime (`INV-DISP-002`).

---

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/workflow_dispatch.py` | **New file.** Implements `WorkflowDispatcherRuntime` orchestrating multi-stage program pipelines with: idempotency key registry (prevents duplicate step execution); pre-step aggregate state snapshot and rollback on exhausted retries; step retry limit enforcement via `StepDefinition.max_attempts`; distributed lease lifecycle tracking (`ACQUIRED → STEP_RUNNING → STEP_COMPLETE → RELEASED/FAILED`). Also provides `IdempotencyRegistry`, `LeaseManager`, `StepDefinition`, `StepExecutionRecord`, `PipelineRun`, `DistributedLeaseRecord`, and all supporting error types. | `INV-DISP-002` — no duplicate step execution (same idempotency key + same payload is a no-op; key collision on different payload is a hard `IdempotencyKeyConflictError`); state consistency guaranteed across failures (pre-step snapshot is taken before every executor call; on retry exhaustion the snapshot is restored and the lease transitions to `FAILED`). |
| `tests/cae/test_ca_m035_workflow_dispatch.py` | **New file.** Comprehensive evidence suite covering: positive end-to-end pipeline run; per-step lease lifecycle advancement; idempotent replay (`SKIPPED` status, executor NOT called again); idempotency key conflict; transient failure + retry within `max_attempts`; retry limit exhaustion + aggregate rollback; COMMANDER-lane authority enforcement for initialize/complete/execute; non-`RUNNING` aggregate rejection; duplicate `initialize_pipeline` rejection (lease already held); re-acquire after release; snapshot capture; rollback state_data restoration; heartbeat; regression (store unaffected); false-proof countercase; `LeaseManager` unit tests; `IdempotencyRegistry` unit tests; factory test. | All evidence classes required by the mandate (positive, negative, regression, false-proof countercase). |

---

## Exact Paste Instructions

Replace / add the following repository paths with the files from this bundle (same relative paths):

1. **New file** — copy `CA-M035_BUNDLE/packages/ca_runtime/src/ca_runtime/workflow_dispatch.py`  
   → `packages/ca_runtime/src/ca_runtime/workflow_dispatch.py`

2. **New file** — copy `CA-M035_BUNDLE/tests/cae/test_ca_m035_workflow_dispatch.py`  
   → `tests/cae/test_ca_m035_workflow_dispatch.py`

Do **not** copy any other files from this bundle. Both target paths are new (they do not exist in the current repository). No existing files are modified.

---

## Manual Post-Apply Commands

No migrations required. The dispatcher operates entirely against the existing `IProgramStateStore` / `InMemoryProgramStateStore` / `SqliteProgramStateStore` interface (no new database tables).

After applying the two files, run the evidence suite:

```bash
python -m pytest tests/cae/test_ca_m035_workflow_dispatch.py -v
```

A broader regression sweep that should remain green:

```bash
python -m pytest tests/cae/test_ca_m034_atomic_dispatch.py tests/cae/test_ca_m035_workflow_dispatch.py -v
```

---

## New Automated Tests Included

All tests are in `tests/cae/test_ca_m035_workflow_dispatch.py`.

### Positive path

| Test | Evidence class |
|---|---|
| `test_ca_m035_positive_end_to_end_pipeline_completes` | EXECUTABLE positive — three-step pipeline; lease RELEASED on complete |
| `test_ca_m035_positive_lease_lifecycle_tracks_per_step` | EXECUTABLE positive — ACQUIRED→STEP_RUNNING→STEP_COMPLETE→RELEASED |
| `test_ca_m035_positive_step_records_are_appended` | EXECUTABLE positive — record status, attempt, result |

### Idempotency

| Test | Evidence class |
|---|---|
| `test_ca_m035_idempotency_same_key_same_payload_is_skipped` | EXECUTABLE positive — executor NOT re-called; SKIPPED record |
| `test_ca_m035_idempotency_conflict_different_payload_raises` | EXECUTABLE negative — `IdempotencyKeyConflictError` |
| `test_ca_m035_idempotency_key_is_deterministic_from_pipeline_step_payload` | False-proof countercase — key stability |

### Retry & Rollback

| Test | Evidence class |
|---|---|
| `test_ca_m035_retry_transient_failure_then_success` | EXECUTABLE positive — 1 fail + 1 success within max_attempts=3 |
| `test_ca_m035_retry_limit_exceeded_raises_and_rolls_back` | EXECUTABLE negative — `StepRetryLimitExceededError`; aggregate restored |
| `test_ca_m035_retry_limit_exceeded_step_record_rolled_back` | EXECUTABLE negative — record status == ROLLED_BACK |

### Authority Lane

| Test | Evidence class |
|---|---|
| `test_ca_m035_non_commander_cannot_initialize_pipeline` | EXECUTABLE negative — `WorkflowAuthorityViolationError` |
| `test_ca_m035_non_commander_cannot_complete_pipeline` | EXECUTABLE negative — `WorkflowAuthorityViolationError` |
| `test_ca_m035_hunter_cannot_execute_commander_step` | EXECUTABLE negative — `WorkflowAuthorityViolationError` |

### Aggregate Preconditions

| Test | Evidence class |
|---|---|
| `test_ca_m035_non_running_aggregate_rejected` | EXECUTABLE negative — `WorkflowAggregatePreconditionError` |
| `test_ca_m035_missing_aggregate_rejected` | EXECUTABLE negative — `WorkflowDispatchError` AGGREGATE_NOT_FOUND |

### Distributed Lease

| Test | Evidence class |
|---|---|
| `test_ca_m035_double_initialize_rejected_lease_already_held` | EXECUTABLE negative — LEASE_ALREADY_HELD |
| `test_ca_m035_reinitialize_after_release_succeeds` | EXECUTABLE positive — new run after RELEASED |

### Step Definition Constraints

| Test | Evidence class |
|---|---|
| `test_ca_m035_step_definition_max_attempts_must_be_positive` | Fail-closed validation |
| `test_ca_m035_step_definition_empty_id_rejected` | Fail-closed validation |
| `test_ca_m035_unknown_step_id_raises_not_found` | `WorkflowStepNotFoundError` |

### Snapshot & Rollback

| Test | Evidence class |
|---|---|
| `test_ca_m035_snapshot_captured_before_step_execution` | Snapshot key present |
| `test_ca_m035_rollback_restores_pre_step_state_data` | Exact state_data restoration |

### Heartbeat & Regression

| Test | Evidence class |
|---|---|
| `test_ca_m035_heartbeat_updates_lease_status` | Lease HEARTBEAT status |
| `test_ca_m035_regression_get_aggregate_survives_pipeline_lifecycle` | Regression — store unaffected |

### False-proof Countercase

| Test | Evidence class |
|---|---|
| `test_ca_m035_false_proof_stub_that_skips_idempotency_registry_is_invalid` | Demonstrates that naive stub allows duplicate execution; real dispatcher prevents it |

### Unit Tests

| Test | Evidence class |
|---|---|
| `test_ca_m035_lease_manager_acquire_and_release` | LeaseManager unit |
| `test_ca_m035_lease_manager_double_acquire_rejected` | LeaseManager unit — LEASE_ALREADY_HELD |
| `test_ca_m035_lease_manager_step_running_and_complete` | LeaseManager unit — lifecycle |
| `test_ca_m035_lease_manager_fail_transitions_to_failed` | LeaseManager unit — FAILED |
| `test_ca_m035_idempotency_registry_same_payload_returns_already_done` | IdempotencyRegistry unit |
| `test_ca_m035_idempotency_registry_mark_completed` | IdempotencyRegistry unit |
| `test_ca_m035_factory_creates_dispatcher_with_default_store` | Factory correctness |

---

## Evidence Locators

| Property | Location |
|---|---|
| Idempotency key derivation | `workflow_dispatch.py` → `_make_step_idempotency_key()` |
| Idempotency registry (check + register) | `workflow_dispatch.py` → `IdempotencyRegistry.check_and_register()` |
| Pre-step snapshot capture | `workflow_dispatch.py` → `WorkflowDispatcherRuntime.execute_step()` snapshot block |
| Rollback on exhausted retries | `workflow_dispatch.py` → `WorkflowDispatcherRuntime._rollback_step()` |
| Step retry enforcement | `workflow_dispatch.py` → `execute_step()` attempt vs. `step_def.max_attempts` |
| Lease lifecycle tracking | `workflow_dispatch.py` → `LeaseManager.{acquire,mark_step_running,mark_step_complete,release,fail}()` |
| Authority lane enforcement | `workflow_dispatch.py` → `WorkflowDispatcherRuntime._require_lane()` |
| Aggregate RUNNING precondition | `workflow_dispatch.py` → `WorkflowDispatcherRuntime._load_running_aggregate()` |
| Duplicate lease guard | `workflow_dispatch.py` → `LeaseManager.acquire()` — LEASE_ALREADY_HELD check |

---

## Residual Limitations

1. **Persistence** — `WorkflowDispatcherRuntime` stores `PipelineRun` objects in
   an in-process dict (`self._runs`). This is intentional for this mandate scope
   (INV-DISP-002 does not prescribe durable pipeline run storage beyond the existing
   `IProgramStateStore` used for aggregate state). A future mandate may wire
   `PipelineRun` serialization into `SqliteProgramStateStore`.

2. **Cross-process lease durability** — `LeaseManager` is in-memory. For true
   distributed lease durability (multi-process/multi-host) a future mandate should
   persist lease records to `SqliteProgramStateStore` or an external lock service.
   The current implementation satisfies INV-DISP-002 within a single process.

3. **Rollback scope** — `_rollback_step()` restores `state_data` only; it does not
   undo external side effects produced by the executor (e.g. database writes, API
   calls). Side-effect compensation is out of scope for this mandate and must be
   addressed by the executor implementation or a future saga/compensation mandate.

4. **No multi-turn host runner** — per mandate scope exclusions (§5 out of scope),
   Q37 multi-turn loops and Q38 provider routing are not implemented here.

---

## Operator Decision Request

**Question for Operator approve/reject:**

Does the evidence above prove that `WorkflowDispatcherRuntime` (CA-M035):

- Prevents duplicate step execution via deterministic idempotency keys?
- Guarantees state consistency across failures via pre-step snapshots and rollback?
- Enforces step retry limits and fails closed on exhaustion?
- Tracks distributed lease lifecycle from ACQUIRED through RELEASED/FAILED?
- Rejects non-COMMANDER callers and non-RUNNING aggregates?

**Approve or reject `CA-M035`.**
