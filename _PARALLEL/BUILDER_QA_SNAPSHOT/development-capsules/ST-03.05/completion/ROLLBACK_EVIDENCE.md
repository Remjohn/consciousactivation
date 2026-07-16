# ST-03.05 rollback evidence

Verdict: `PASS`.

The injected atomic-commit failure was exercised after policy, Harness IR, manifest, all 21 stored artifacts, and re-rendered projections validated, but before persistence. The run remained at stream version 12 and retained zero constitutional reports, zero constitutional receipts, no constitutional run reference, no command record, and no partial event.

The governed upstream-reopen path was also exercised. One authorized reopen emitted five linked events and stored boundary, Harness IR, artifact-set, and constitutional-validation invalidations atomically. Active constitutional consumption then failed closed, while the immutable report and receipt remained historically reproducible against their pinned policy, Constitution, and Builder PRD amendment hashes.

Source rollback is non-destructive and hash-driven: remove the three new source modules and seven ST-03.05 test files; restore the four existing source files and six architecture tests to their `previous_sha256` values in `FILE_CHANGE_MANIFEST.yaml`; restore the explicitly reconciled authority and capsule identities only if a later human authority supersedes the current confirmed Program Control amendment hash; then rerun the exact predecessor suite. The current predecessor result is 147/147 PASS.

No database, schema, migration, package dependency, network state, external repository state, published artifact directory, or external runtime requires cleanup. No destructive rollback command was executed.
