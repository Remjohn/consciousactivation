# ST-02.05 rollback evidence

Rollback is non-destructive and repository-local. ST-02.05 added no database, migration, schema, dependency, network side effect, external runtime state, provider state, publication state, or production artifact.

## Atomic failure demonstration

The development/test repository's injected commit failure raised typed `AtomicCommitFailed`. The authoritative stream remained at its five-event precommand baseline, with zero boundary, model, ratification/decision receipt, or command record committed. Retrying after removing the injected failure committed the command exactly once and advanced the stream to version 9. This proves that the human decision, boundary, model, lifecycle events, command record, and receipt share one atomic persistence boundary.

## Reopen is not rollback

An authorized reopen preserved the original decision and receipt, emitted a typed invalidation chain, marked the frozen boundary and model unusable, set `HG-003=FAIL`, and required a new immutable version. No history was rewritten. Unauthorized reopen left the frozen state unchanged.

## Hash-based source rollback plan

To reproduce the pre-ST-02.05 implementation state without altering earlier Story evidence:

1. Remove only the three new source modules and six new Story test files listed in `FILE_CHANGE_MANIFEST.yaml`.
2. Restore the eight allowlisted existing files to their recorded `previous_sha256` states.
3. Keep all three predecessor completion receipts unchanged.
4. Run the prior suites with `PYTHONPATH=src`; their isolated results are `20/20`, `18/18`, and `19/19`, totaling `57/57 PASS` in the current workspace.

No destructive rollback was executed. The plan is reproducible from exact hashes, and the required rollback behavior is demonstrated by the atomic-failure and invalidation tests.

Verdict: `PASS`.
