# CA-M057 — Live End-to-End Proof Harness

## Mandate ID & Title

**Mandate ID:** `CA-M057`  
**Title:** Live End-to-End Proof Harness  
**User-stated invariant:** `INV-PROOF-001`  
**Governing mandate invariant:** `INV-LIVE-001` (per `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/09_CA_MANDATE_057.md`)

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `tests/e2e/test_live_e2e_proof_harness.py` | Added a self-contained 17-stage live proof harness that starts from raw audience/subject genesis data, renders a release artifact, executes the real `ProgramOperatorRuntimeService` lease path, calls `AgentInvocationRuntime` through a live HTTP provider boundary with `ExecutionMode.PRODUCTION`, suspends at the canonical human gate, resumes only after explicit approval, builds a sealed release manifest, performs real HTTP distribution through `ExternalDistributionClient`, records outcome evidence, persists Merkle receipts and replay witnesses, reopens persisted state for replay, ratifies learning, and performs typed durable memory write-back. Includes two proof-artifact tests and a row-only false-proof countercase. | `INV-PROOF-001` / M057 `INV-LIVE-001`: the positive path proves all 17 stages are exercised, the provider run is non-synthetic, the lease is acquired, the human gate actually suspends/resumes, distribution reaches a remote HTTP sink, Merkle/replay verification returns `PASS`, and a populated aggregate row alone is rejected as `EVIDENCE_GAP`. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

**Added**

- `tests/e2e/test_live_e2e_proof_harness.py` — the requested mandate-specific E2E proof harness. The supplied archive did not contain this target path. No production runtime/API source file was modified.

**Modified**

- None.

The working tree was intentionally constrained to the single requested test path. The repository-wide pytest attempt exposed unrelated legacy/scratch collection failures, but no unrelated repository files were changed to bypass them.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. From the repository root, paste/copy `tests/e2e/test_live_e2e_proof_harness.py` to that exact destination path.
2. No migration is required. The harness creates only disposable SQLite tables/database state under the pytest temporary directory for replay snapshots, a M057-specific persisted replay witness ledger, Merkle receipts, and the proof artifacts.
3. The test file is self-contained with respect to the sandbox's missing optional `psycopg` package: when `psycopg` is unavailable, it installs an import-only stub so SQLite-backed runtime imports can load. This does not replace the exercised SQLite persistence path and does not mock the live provider or distribution HTTP boundaries.
4. The positive path uses a loopback HTTP provider and loopback HTTP distribution sink to exercise actual network transport, provider-router execution, and delivery adapters without requiring external credentials or network access. This proves live boundary contact and `is_synthetic=false`, but it does not certify behavior of an external hosted model/service.
5. The current runtime's gate-suspension transition does not persist a native `state_updates` payload. To preserve the mandate's no-in-memory-replay rule, the harness persists the observed transition state delta in `m057_replay_transition_updates` and reads it back during replay; the replay itself is read-only against durable SQLite state.
6. No production database migration or deployment change is bundled or required for this test artifact.

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH="$(find packages services -type d -name src | paste -sd: -):${PYTHONPATH:-}" pytest -q tests/e2e/test_live_e2e_proof_harness.py
```

Additional syntax check used during verification:

```bash
python -m py_compile tests/e2e/test_live_e2e_proof_harness.py
```

## Expected Test Results (number of automated tests, all passing)

**Mandate-specific automated tests:** 3  
**Expected:** `3 passed`

Verified in the sandbox on 2026-09-08:

```text
3 passed in 5.39s
```

The repository-wide `pytest -q` command was also attempted. It did not reach a valid whole-repository test run: collection stopped with **382 unrelated errors**, including historical/scratch test import-path failures and missing optional `psycopg`. Those failures are outside the M057 file boundary and were not modified.

## Evidence Classes

- **EXECUTABLE:** actual `ProgramOperatorRuntimeService`, `UniversalProgramStateRuntime`, `AgentInvocationRuntime`, `ReleaseManifestBuilder`, `ExternalDistributionClient`, `ReleaseShipOutcomeCoordinator`, `PersistedReplayVerifier`, and `MemoryWritebackStore` execution.
- **TEST:** 3 passing mandate-specific positive/negative tests.
- **SCHEMA:** durable SQLite aggregate/transition/lease/replay/Merkle records and the M057 replay witness table created by the test.
- **DOCUMENT:** governing M057 mandate path and the invariant mapping stated above.
- **OPERATOR_DECISION_REQUIRED:** mandate completion still requires the authorized Operator to choose `APPROVE`, `REJECT`, or `DEFER`; a green test result does not imply approval.

## Baseline / Commit Capture

The public repository's current `main` history at the time of verification identifies commit `3a92a8394fa6d73973a6ad5d0b5a3fe1f95ed76a` as the latest commit. The supplied ZIP archive contains no `.git` metadata, so no implementation commit could be created or proven inside the supplied repository snapshot. The bundle therefore records the exact upstream baseline SHA rather than inventing an implementation commit SHA.

Source repository: `https://github.com/Remjohn/consciousactivation`  
Target branch: `main`  
Baseline SHA: `3a92a8394fa6d73973a6ad5d0b5a3fe1f95ed76a`

## Completion / Decision Status

The artifact and mandate-specific positive/negative evidence are complete within scope. The executor does **not** infer operator approval. Final action remains an explicit Operator decision: `APPROVE`, `REJECT with findings`, or `DEFER with named remediation`.

## Artifact Integrity

Bundled test SHA-256:

`71a2a97073012c8d7de4991d446372c4d48e97968742f9569ae67e8870395924`
