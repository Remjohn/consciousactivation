# Test plan

Run every command with `PYTHONPATH=src`. Use deterministic clocks, UUIDv7 providers, repository-local fixtures, and the in-memory development/test adapter. No network or external runtime is permitted.

The new Story suite must contain at least 20 independently named tests across the following seams:

1. Acceptance: exact Source Lock and declared input accepted; human approval compiles and freezes; deterministic model/receipt hashes; all required model fields and status metadata; `HG-003=PASS` only on valid approval.
2. Decision paths: approve, revise, and reject each preserve their distinct outcome; incomplete rationale, evidence, rejected alternatives, risks, or identity is rejected.
3. Authority: human grant succeeds; agent, code, evaluator, external, unknown, expired, wrong-action, and wrong-resource actors fail without mutation.
4. Failure boundaries: input hash drift; source-lock mismatch; critical contradiction; silent broadening/merge/split; same-version rewrite; unratified downstream field consumption; stale version; command payload mismatch; injected atomic commit failure.
5. Reopen and rollback: authorized reopen emits invalidation for boundary/model/receipt dependents and requires a new version; unauthorized reopen fails; rollback needs no migration or external cleanup.
6. Replay and observability: identical command returns identical receipt without duplicate events; event replay reconstructs the same state/model refs; success and rejection observations carry every required field.
7. Architecture: exact source set, standard-library-only imports, no external product/runtime imports, no schemas/dependencies, no task execution, no later Story behavior.

Required commands:

- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_02_05`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01_synthetic_proof`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_02`
- `$env:PYTHONPATH='src'; python -m pytest -q`

Passing thresholds: all mandatory tests pass, no skips, prior baseline `57/57` passes, Story suite has at least 20 tests, architecture subset passes, deterministic fresh-context rerun passes twice, and receipt/capsule/hash validation passes.
