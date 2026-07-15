# ST-03.04 rollback evidence

Verdict: `PASS`.

The injected atomic-commit failure was exercised after deterministic rendering and before persistence. The authoritative stream remained at version 11 and the repository retained zero generated artifacts, zero manifests, zero artifact receipts, and no command record. This demonstrates that a partial artifact set cannot become visible.

The governed invalidation path was also exercised. Reopening the authoritative atomic boundary produced linked HarnessIR and artifact-set invalidations, blocked active artifact consumption, preserved all 21 immutable historical projections and their manifest, and required a new upstream and artifact-set version.

Source rollback is non-destructive and hash-driven: remove the three new source modules and seven ST-03.04 test files, restore the four existing source files and five architecture tests to the `previous_sha256` values in `FILE_CHANGE_MANIFEST.yaml`, and rerun the prior 112-test suite. The implementation created no database, migration, schema, dependency, network state, external state, or published artifact directory requiring cleanup. No destructive rollback command was executed.
