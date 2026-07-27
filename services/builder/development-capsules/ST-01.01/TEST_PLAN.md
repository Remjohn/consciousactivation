# Deterministic Test Plan

## Test runtime

- Python 3.12-compatible standard library only.
- No network, database, process worker, clock service, provider, VAE, Delegation or workflow engine.
- Inject deterministic ID and UTC-clock providers in tests.
- Run from repository root with `python -B -c "import sys, unittest; sys.path.insert(0, 'src'); suite=unittest.defaultTestLoader.discover('tests/stories/st_01_01'); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(0 if result.wasSuccessful() else 1)"`.
- Two consecutive clean runs must produce identical domain event payloads and state hashes after excluding explicitly declared observation timestamps.

## Required Story tests

| Test ID | File | Assertions |
| --- | --- | --- |
| `ST-01.01-acceptance` | `test_acceptance.py` | Exactly one Format 02 target/profile creates a stable run; target, category, profile, compiler, operator, state and required work are bound before evidence work. |
| `ST-01.01-failure` | `test_failure.py` | Zero/multiple/unknown/unauthorized targets, illegal edges, stale versions, mismatched idempotency payloads and corrupt checkpoints fail without mutation. |
| `ST-01.01-authority` | `test_authority.py` | Deny-by-default actor matrix; only exact grants allow transition/waiver; agents and unauthorized actors cannot waive or authorize. |
| `ST-01.01-receipt` | `test_replay.py` | Every accepted command returns stable event/receipt IDs; replay reconstructs state; resume preserves human receipts and does not repeat decisions. |

## Additional bounded tests

### Target and profile invariants

- Registry adapter accepts only the three target IDs in the governed registry.
- Execution is allowed only for `atomic_content_harness` plus Format 02.
- Conversational, VAE and Delegation execution attempts fail with no external call and no state event.
- No target is silently defaulted.
- Profile/target binding is immutable after the source-lock boundary; any later change requires an explicit governed fork, which is not implemented in this Story and must fail closed.

### State machine and event ledger

- Legal edge appends one event and increments stream version once.
- Illegal edge, missing prerequisite and denial append zero authoritative events.
- Duplicate identical command returns original receipt; mismatched reuse rejects.
- Replay order is stable and discontinuous stream versions reject.

### Checkpoint and resume

- Latest valid checkpoint is selected by input/profile/policy hashes.
- Newer invalid checkpoint is skipped only when full event replay is valid and emits an incident observation; incompatible event history blocks.
- Human decision receipt IDs survive replay and resume without a new decision request.

### Architecture and security

- `test_architecture_boundary.py` parses imports and proves domain imports no application or adapter module.
- No file imports network clients, database drivers, web frameworks, workflow engines, VAE packages or Delegation packages.
- No modified path falls outside `ALLOWED_FILE_SCOPE.yaml`.
- No new dependency or schema is introduced.

## Evidence output

The implementation run writes a machine-readable `TEST_RESULTS.json` listing runtime version, command, test IDs, pass/fail, duration, deterministic rerun result and captured failure summaries. A failing test prevents `StoryCompletionReceipt` issuance.

