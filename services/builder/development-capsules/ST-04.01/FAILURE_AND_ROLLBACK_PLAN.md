# Failure and rollback plan

All failures are typed and fail closed. No failing decision set may attach an active graph or commit an event, command record, receipt, or partial graph. Injected persistence failure must prove zero partial state.

An authorized upstream reopen emits a linked capability-graph invalidation after the constitutional-validation invalidation, blocks active consumption, preserves immutable history, and requires a new graph version.

Source rollback is additive: remove the two new source modules and six Story test files, restore four existing source files and seven architecture tests to recorded pre-Story hashes, and rerun the 186 predecessor tests. No schema, database, dependency, network, external repository, or published artifact cleanup is authorized or required.
