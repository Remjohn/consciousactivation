# Failure and rollback plan

All failures are typed and fail closed. Required classes cover missing/mismatched/altered/invalidated HarnessIR; unsupported input or manifest version; invalid reproducible timestamp/config; incomplete/extra artifact inventory; missing or undeclared source nodes; semantic invention; cross-artifact conflict; nondeterministic rerender; manual drift; secret or undeclared external reference; unauthorized writer; stale concurrency; idempotency payload mismatch; and injected atomic commit failure.

The persistence boundary atomically commits all 21 immutable artifacts, the manifest, run event/reference, command record, and compilation receipt. Injected failure must prove zero partial state.

An authorized upstream reopen preserves prior IR/artifact history, emits linked descendant invalidations, blocks active consumption, and requires new immutable upstream and artifact-set versions. Drift quarantine and invalidation are not destructive rollback.

Source rollback is additive: remove the three new modules and seven Story test files, restore the nine allowlisted existing files to their pre-ST-03.04 hashes, and rerun the prior 112 tests. No database, schema, migration, persistent filesystem artifact, network state, or external compensation exists. Never execute a destructive workspace rollback; issue hash-based evidence.
