# CA-M040 Agent Handoff

## Mandate

- **Mandate ID:** CA-M040
- **Mandate Title:** Gate Milestone Suspension Contract
- **Primary Invariant:** INV-GATE-001 — milestone gates halt execution fail-closed in `AWAITING_APPROVAL` pending authentic Commander approval.

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | Added durable `GateSuspensionSnapshot` evidence, declared-manifest gate discovery, fail-closed `RUNNING -> AWAITING_APPROVAL` suspension, lease/dispatch suspension, structured `GateSuspensionEvent` alerts, snapshot integrity verification, and guards against downstream lifecycle/transition bypass while approval is pending. | **INV-GATE-001:** a declared human gate captures the committed state/version/hash and gate evidence, releases the worker lease, marks workflow dispatch suspended, and blocks downstream execution until an approval/rejection path is used by the governing runtime. |
| `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` | Updated execution-trace blocker projection to surface the concrete suspended gate and Commander approval requirement. | **INV-GATE-001:** operator-facing execution state explicitly reports the human gate as the blocking condition. |
| `packages/ca_runtime/src/ca_runtime/agent_invocation.py` | Added an optional authoritative execution guard immediately before model inference plus `GateSuspensionExecutionBlockedError`. | **INV-GATE-001:** a guarded agent turn is refused before inference when the bound program aggregate is gate-suspended. |
| `tests/cae/test_ca_m040_gate_suspension.py` | Added focused unit/integration coverage for positive suspension, downstream blocking, direct lifecycle bypass, pre-inference agent blocking, SQLite durability/lease release, and a non-gated control path. | **INV-GATE-001:** automated checks cover the required halt, durability, lease release, alert, and negative-path behaviors. |

## Exact paste instructions

Replace these repository paths with the corresponding complete files from this bundle:

1. `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
2. `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
3. `packages/ca_runtime/src/ca_runtime/agent_invocation.py`

Add this new automated test file:

4. `tests/cae/test_ca_m040_gate_suspension.py`

No other repository paths are part of this bundle.

### Important scope note

The mandate document's file-boundary prohibition permits production changes only in the named existing runtime files and permits new focused automated tests. The requested `packages/ca_runtime/src/ca_runtime/gate_suspension.py` production file does **not** exist in the supplied repository and is not an authorized new production file under CA-M040, so it was intentionally **not** created. The same applies to the originally named test target: this bundle adds the authorized `tests/cae/test_ca_m040_gate_suspension.py` path used by the repository's test layout.

The API router was not changed because the existing program/operator surfaces already serialize lifecycle/state data, while the execution-trace projection change makes the CA-M040 gate-specific blocker visible without expanding the patch boundary.

## Manual post-apply commands

No database migration is required by this implementation; the existing aggregate, lease, dispatch, and transition tables are reused.

Run the targeted CA-M040 tests after applying the bundle:

```text
pytest -q tests/cae/test_ca_m040_gate_suspension.py
```

This command was **not run by the execution agent**, per the explicit instruction: **DO NOT run TEST**.

## Automated tests included

- `test_ca_m040_halts_at_declared_gate_and_persists_immutable_snapshot`
- `test_ca_m040_blocks_downstream_transition_while_awaiting_approval`
- `test_ca_m040_prevents_direct_lifecycle_bypass`
- `test_ca_m040_agent_invocation_guard_blocks_before_inference`
- `test_ca_m040_sqlite_persists_suspension_and_released_lease`
- `test_ca_m040_non_gated_execution_remains_running`

## Verification status

The modified/new Python files were syntax-parsed successfully. No test suite or pytest invocation was executed. Therefore this handoff does not claim test-pass completion; it provides the complete implementation and the targeted automated tests for post-apply execution.
