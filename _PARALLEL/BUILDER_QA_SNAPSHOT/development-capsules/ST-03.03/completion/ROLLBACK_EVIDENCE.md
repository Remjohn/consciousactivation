# ST-03.03 rollback evidence

Verdict: `PASS`

Rollback is non-destructive and repository-local. ST-03.03 added no database, migration, schema file, dependency, network side effect, external runtime state, provider state, publication state, or production artifact.

## Atomic failure demonstration

The injected repository commit failure raised typed `AtomicCommitFailed`. The authoritative stream remained at its nine-event precommand baseline, with zero Harness IR snapshot, receipt, run reference, or command record committed. After removing the injected failure, the same command committed exactly once. This proves that the immutable snapshot, two run events, lifecycle transition, command record, and compilation receipt share one atomic persistence boundary.

## Invalidation is not destructive rollback

An authorized atomic-boundary reopen preserved the original canonical snapshot and prior event history, created one typed Harness IR descendant invalidation, advanced the event stream from 11 to 14, and caused active-IR reads to fail with `HarnessIRInvalidatedError`. A new upstream boundary and a new immutable IR revision are required. Unauthorized reopen preserves the active IR unchanged.

## Hash-based source rollback plan

To reproduce the pre-ST-03.03 implementation state without changing predecessor evidence:

1. Remove only the three new source modules and seven new Story test files listed in `FILE_CHANGE_MANIFEST.yaml`.
2. Restore the five allowlisted existing source files and four architecture tests to their recorded `previous_sha256` states.
3. Restore the authorization outputs to their pre-grant state; do not alter any immutable capsule input or predecessor completion receipt.
4. Run the predecessor suites with `PYTHONPATH=src`; their isolated results are 20/20, 18/18, 19/19, and 27/27, totaling the prior 84/84 PASS state.

No destructive workspace rollback was executed. Exact previous/current hashes and aggregate bundles make the plan independently checkable.
