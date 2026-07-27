# Failure and rollback plan

All failures are typed and fail closed. No invalid module input may attach a graph or commit an event, command record, receipt, or partial module artifact. Injected persistence failure must prove zero partial state.

An authorized upstream reopen emits a linked module-graph invalidation after capability-ownership invalidation, blocks active consumption, preserves immutable history, and requires a new graph version. A direct future capability-graph replacement must likewise require a new module graph identity; in-place mutation is prohibited.

Source rollback is additive: remove the two new source modules and six Story test files, restore four existing source files and eight architecture tests to recorded pre-Story hashes, and rerun the 221 predecessor tests. No schema, database, dependency, network, external repository, or published artifact cleanup is authorized or required.
