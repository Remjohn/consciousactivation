# Failure and rollback plan

All failures are typed and fail closed. Invalid phase input may not attach a graph or commit an event, command record, receipt, or partial artifact. Injected persistence failure must prove zero partial state.

An authorized upstream reopen emits a linked phase-graph invalidation after module-graph invalidation, blocks active consumption, preserves immutable history, and requires a new graph version.

Source rollback is additive: remove the two new source modules and six Story test files, restore four existing source files and nine architecture tests to recorded pre-Story hashes, and rerun the 256 predecessor tests. No schema, database, dependency, network, external repository, runtime, or published-artifact cleanup is authorized or required.
