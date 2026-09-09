# Mandate ID & Title

**CA-M044 — Persisted Replay Verification Engine**

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/replay_engine.py` | Added a read-only persisted replay verifier that reconstructs state from durable transition inputs, verifies cached model-completion fingerprints, validates the M043 Merkle receipt chain and transition/receipt bindings, checks every persisted replay snapshot and final aggregate fingerprint, reports first divergence/evidence gaps, and never invokes a model or writes to the authoritative store. | `INV-REPL-001`: a multi-step persisted run can be replayed and its canonical state fingerprints match bit-for-bit; receipt tamper, transition omission/reorder, snapshot corruption, and cached-completion tamper fail closed; insufficient durable history is reported as an explicit evidence gap. |
| `tests/cae/test_ca_m044_replay_engine.py` | Added 10 self-contained SQLite tests covering positive multi-step replay, single-field corruption, missing/reordered transitions, receipt-chain tampering, cached model-response tampering/missing data, current-schema evidence gaps, read-only behavior, and deterministic result serialization/reruns. | `INV-REPL-001` is executable as a regression-proof acceptance suite with all 10 tests passing in the supplied sandbox. |

## Files Added and Files Modified

### Files Added

- `packages/ca_runtime/src/ca_runtime/replay_engine.py` — required CA-M044 runtime implementation; this path did not exist in the supplied repository snapshot.
- `tests/cae/test_ca_m044_replay_engine.py` — required CA-M044 acceptance tests; this path did not exist in the supplied repository snapshot.

### Files Modified

- **None.** No pre-existing repository file was modified.

## Exact paste instructions and post-apply commands

From the repository root, extract the bundle and copy its two repository-relative files into place:

```bash
unzip CA-M044_BUNDLE.zip
cp CA-M044_BUNDLE/packages/ca_runtime/src/ca_runtime/replay_engine.py packages/ca_runtime/src/ca_runtime/replay_engine.py
cp CA-M044_BUNDLE/tests/cae/test_ca_m044_replay_engine.py tests/cae/test_ca_m044_replay_engine.py
```

No migration is included and the verifier deliberately performs no schema mutation or writes. The current CAE runtime persists only the latest aggregate state in `cae_program_state_aggregates`; without an independently persisted historical replay-snapshot/input ledger, the verifier returns `EVIDENCE_GAP` rather than claiming deterministic replay from insufficient evidence.

Post-apply validation:

```bash
pytest -q tests/cae/test_ca_m044_replay_engine.py
```

The supplied sandbox image lacks the repository's `psycopg` dependency, so the recorded sandbox execution used a temporary in-process dependency stub only; no repository file was changed for that workaround.

The uploaded repository snapshot contains no `.git` metadata, so an exact source commit SHA cannot be truthfully recorded. The bundle therefore records no fabricated SHA.

## Test Command

```bash
pytest -q tests/cae/test_ca_m044_replay_engine.py
```

## Expected Test Results

**10 automated tests, all passing.**

Recorded sandbox result:

```text
..........                                                               [100%]
10 passed in 0.25s
```
