# CA-M034 Agent Handoff

## Mandate

`CA-M034` — Two-Phase Atomic Program Lease Dispatch (`INV-DISP-001`).

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` | Replaced the old `initialize -> RUNNING` start path with CA-M034 Phase 1 version-0 registration plus Phase 2 atomic lease claim/workflow enqueue; preserved COMMANDER authorization and preflight gating. | `run_program()` cannot return RUNNING until the durable lease CAS path succeeds; failed claims never synthesize RUNNING. |
| `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | Added durable execution-lease and workflow-dispatch persistence, version-0 registration, atomic SQLite lease CAS (`LEASE_ENQUEUED` v0 -> `LEASE_ACQUIRED` v1), aggregate transition to RUNNING in the same transaction, thread-safe in-memory equivalent, and fail-closed lease conflict error. | RUNNING is paired with a held durable lease; SQLite `BEGIN IMMEDIATE` plus `UPDATE ... WHERE status='LEASE_ENQUEUED' AND lease_version=0` permits exactly one concurrent claimant. |
| `tests/cae/test_ca_m034_atomic_dispatch.py` | Added unit/integration evidence for two phases, stale/fail-closed claims, false-proof in-memory marker countercase, real SQLite concurrent claims, SQLite operator-boundary persistence, and COMMANDER authorization. | Positive execution, negative CAS conflict, environment-fidelity, and false-proof countercase are all executable at the canonical runtime/operator boundary. |

## Exact paste instructions

Replace the following repository paths with the same paths from this bundle:

1. `CA-M034_BUNDLE/packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` → `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
2. `CA-M034_BUNDLE/packages/ca_runtime/src/ca_runtime/program_state_runtime.py` → `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
3. `CA-M034_BUNDLE/tests/cae/test_ca_m034_atomic_dispatch.py` → `tests/cae/test_ca_m034_atomic_dispatch.py`

Do not copy any other repository paths from this bundle.

## Persistence / migration notes

No separate migration command is required for the repository's SQLite state store. `SqliteProgramStateStore._init_schema()` creates the additive tables idempotently:

- `cae_program_execution_leases`
- `cae_program_workflow_dispatch_queue`

Existing pre-CA-M034 aggregates are not backfilled or silently promoted. New operator starts use the CA-M034 dispatch path only. Because the schema addition is additive and created with `CREATE TABLE IF NOT EXISTS`, rollback of the code is possible without destructive data movement; the new tables may remain unused until a future controlled cleanup.

## Manual post-apply commands

Per the execution instruction, no test suite was run during this implementation.

Run the CA-M034 evidence suite after applying the files:

```bash
python -m pytest tests/cae/test_ca_m034_atomic_dispatch.py
```

A broader regression pass should subsequently include the existing CAE operator/API suites because `run_program()` now returns the CA-M034 execution version after lease acquisition.

## New automated tests included

- `test_ca_m034_positive_path_is_two_phase_and_workflow_triggered`
- `test_ca_m034_stale_claim_fails_closed_without_running_state`
- `test_ca_m034_false_proof_in_memory_lease_marker_does_not_claim_authority`
- `test_ca_m034_sqlite_concurrent_claim_has_exactly_one_winner`
- `test_ca_m034_sqlite_operator_boundary_persists_phase_one_and_phase_two`
- `test_ca_m034_operator_boundary_requires_commander_and_returns_running`

## Evidence locators

- Phase 1 construction: `UniversalProgramStateRuntime.register_program_dispatch()`
- Phase 2 orchestration: `UniversalProgramStateRuntime.acquire_execution_lease_and_trigger()`
- SQLite atomic claim: `SqliteProgramStateStore.acquire_execution_lease()`
- Operator entry point: `ProgramOperatorRuntimeService.run_program()`
- Durable workflow handoff: table `cae_program_workflow_dispatch_queue`, trigger operation `cae.program.dispatch@1.0.0`
- Durable lease state: table `cae_program_execution_leases`, `status='LEASE_ENQUEUED'`, `lease_version=0` → `status='LEASE_ACQUIRED'`, `lease_version=1`

## Scope and residual limitations

This bundle implements CA-M034 only. The workflow-dispatch queue is the durable post-lease handoff boundary; resolution of real workflow agents/compiled skills belongs to Q35 / CA-M035 and is intentionally not implemented here. Context projection/masking belongs to Q36 / CA-M036 and is intentionally not implemented here. Zombie-lease reconciliation belongs to later mandates and is intentionally not implemented here.

The legacy low-level `initialize_program_state()` API remains available for existing non-operator/runtime tests and callers; CA-M034 specifically replaces the authoritative `ProgramOperatorRuntimeService.run_program()` start path with the two-phase lease contract.

## Repository state / commit

The supplied archive is not a Git working tree and contains no `.git` metadata, so an authentic commit SHA cannot be captured here. No commit or tracker update was fabricated.

Static verification performed before packaging: Python byte-compilation of the two modified runtime modules and the new CA-M034 test module. Test execution was intentionally not performed.
