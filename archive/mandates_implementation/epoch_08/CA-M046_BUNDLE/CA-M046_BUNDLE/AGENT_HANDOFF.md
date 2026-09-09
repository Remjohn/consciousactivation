# Mandate ID & Title

**CA-M046 — Real Operator Control & Preemption**

Implemented invariant: **INV-PREEMPT-001**.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/operator_preemption.py` | Added a thread-safe execution cancellation token/registry, synchronous resource-notification hooks, cancellation observation, and cryptographically self-consistent preemption receipt model. | The runtime has one canonical in-memory preemption signal per execution and can synchronously notify bound worker/model/tool resources. |
| `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` | Added the authoritative `abort_program()` control path with operator-role validation, actor binding, workspace isolation, terminal/gate fail-closed checks, CAS-backed `RUNNING/active -> CANCELLED` mutation, and durable preemption receipt material in aggregate state. | Authorized aborts commit exactly one CAS lifecycle mutation to `CANCELLED`; stale, unauthorized, cross-workspace, terminal, and gate-blocked requests do not preempt. |
| `packages/ca_runtime/src/ca_runtime/agent_host_runner.py` | Added optional cancellation-token propagation to model/tool isolated calls and process-loop checks; cancellation terminates a real child process instead of only flipping a status flag. | A real interruptible execution boundary stops when the operator token is set; the false-proof case of `CANCELLED` while the isolated worker continues is rejected by test. |
| `api/routers/programs.py` | Added `POST /executions/{aggregate_id}/abort`, reusing canonical tenancy parsing through a lazy dependency wrapper and existing CAS headers. | The operator control signal has an API entry point tied to authenticated operator context, workspace scope, and canonical runtime state. |
| `tests/cae/test_ca_m046_operator_preemption.py` | Added 11 focused tests covering positive control, negative authorization/scope/CAS/state cases, receipt integrity, callback propagation, state preservation, and a real isolated-worker interruption path. | End-to-end mandate proof passes 11/11 automated tests in the sandbox. |

## Files Added and Files Modified

### Files Added

- `packages/ca_runtime/src/ca_runtime/operator_preemption.py` — smallest direct implementation of the missing execution-control primitive; no lifecycle authority is duplicated here.
- `tests/cae/test_ca_m046_operator_preemption.py` — mandate-specific proof artifact.

### Files Modified

- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` — wires operator authorization and canonical CAS state mutation to the new preemption registry.
- `packages/ca_runtime/src/ca_runtime/agent_host_runner.py` — propagates the cancellation signal into the existing isolated model/tool worker boundary.
- `api/routers/programs.py` — exposes the authorized operator abort command at the ratified API surface.

No other repository files were intentionally modified.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Apply the five files at the exact repository destinations listed above, preserving package/module names and existing import layout.

No database migration is required. The preemption receipt is persisted inside the existing `ProgramStateAggregate.state_data`, and the canonical aggregate version/hash/receipt fields continue to be managed by the existing `UniversalProgramStateRuntime.set_lifecycle()` CAS path.

Ensure the normal repository runtime dependencies are installed before running the API or full suite. The validation environment used for this handoff did not include the repository's optional database/provider dependencies, so its focused test command used a temporary non-repository `psycopg` shim plus existing local source packages. In a normal checkout with the declared dependencies installed, the shim is not required.

Post-apply syntax check:

```bash
python -m compileall -q \
  packages/ca_runtime/src/ca_runtime/operator_preemption.py \
  packages/ca_runtime/src/ca_runtime/program_operator_runtime.py \
  packages/ca_runtime/src/ca_runtime/agent_host_runner.py \
  api/routers/programs.py \
  tests/cae/test_ca_m046_operator_preemption.py
```

Focused mandate verification in a fully provisioned checkout:

```bash
python -m pytest -q tests/cae/test_ca_m046_operator_preemption.py
```

The API command is:

```text
POST /api/programs/executions/{aggregate_id}/abort
```

The endpoint accepts the existing CAS request/header fields plus `actor_id` and an optional abort reason, and derives operator/workspace authorization from the existing `X-Actor-Id`, `X-Workspace-Id`, `X-Role`, `X-Is-Operator`, and `X-Operator-Grant-Id` tenancy context.

## Test Command (exact pytest/test command to verify)

```bash
python -m pytest -q tests/cae/test_ca_m046_operator_preemption.py
```

Sandbox command actually executed for this bundle, because the uploaded environment lacked `psycopg` and one additional local package dependency:

```bash
PYTHONPATH=/tmp/psycopg_stub:.:packages/ca_contracts/src:packages/ca_runtime/src:packages/ca_delegation_rc4/src:services/pipeline/src:$PYTHONPATH \
python -m pytest -q tests/cae/test_ca_m046_operator_preemption.py
```

## Expected Test Results (number of automated tests, all passing)

**11 automated tests — 11 passed, 0 failed.**

Coverage includes:

- authorized abort and `CANCELLED` CAS commit;
- execution-state preservation;
- stale-version rejection with no preemption side effect;
- cross-workspace rejection;
- non-operator rejection;
- actor-identity forgery rejection;
- terminal-state fail-closed behavior;
- gate-suspended fail-closed behavior;
- immediate cancellation callback propagation;
- real isolated child-process interruption;
- cryptographic receipt self-consistency;
- unchanged pause/resume semantics.

Sandbox note: an adjacent regression run exposed one pre-existing/platform-sensitive CA-M037 assertion because the host-runner test expects mutation of a parent-thread closure while the existing Linux runtime takes the fork-isolated process path. API import smoke coverage was also not executable in the provided environment because additional repository dependencies (`cmf_builder`, `cae_collision_intelligence`) are absent. These observations are recorded rather than masked; they are outside CA-M046's mandate-specific test suite.

Control-state impact: `source_state -> abort -> CANCELLED` is recorded in `state_data["preemption"]` alongside actor, workspace, reason, request timestamp, expected/committed version, receipt ID, and receipt SHA-256. Cancellation is signalled only after the authoritative CAS commit, preventing a stale request from preempting a newer state.

Residual limitation: the fallback thread execution mode cannot forcibly kill an arbitrary Python thread. In the provided Linux sandbox and the production-designated isolated worker path, model/tool calls are child processes and are terminated on cancellation. No universal sub-millisecond termination guarantee is claimed.

Commit SHA: not available because the uploaded codebase is a source ZIP without a Git working tree/history.

Requested Operator decision: **Approve or reject CA-M046 based on the mandate-specific evidence above.**
