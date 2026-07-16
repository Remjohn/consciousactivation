# ST-03.04 implementation report

Verdict: `PASS`.

ST-03.04 now compiles the exact active ST-03.03 HarnessIR into one immutable, atomic, deterministic artifact set. The set contains 8 human-readable Markdown projections, 3 governed OpenSpec JSON projections, and 10 machine JSON projections. Every projection is non-executable, subordinate to HarnessIR, bound to declared IR source nodes, and identified by reproducible SHA-256 content.

The new typed boundary covers reproducible build configuration, dependency selectors, generated artifacts, the artifact manifest, compilation receipt, drift report, and descendant invalidation. Compilation performs a double render, validates the closed inventory and cross-artifact bindings, and atomically commits 21 artifacts, one manifest, one run event/reference, one command record, and one receipt. The run remains in `GENESIS`.

Manual byte drift returns a typed quarantined report without modifying HarnessIR. Duplicate commands are payload-safe and return the original receipt. Changed payload reuse, stale stream state, invalid IR, missing authority, incomplete inventory, undeclared nodes, secret or external references, cross-artifact conflicts, and injected atomic failures fail closed. An authoritative boundary reopen now invalidates both HarnessIR and the artifact-set descendant while preserving immutable history.

No filesystem artifact publication, schema, database, package, network, provider, task execution, external-product behavior, Atomic Harness Definition, Development Capsule compiler, certification, or production claim was added.

## Deterministic evidence fixture

- HarnessIR: `harness-ir_80c1172a4438a01cdd14951ef6dc9bd8378ab15847aee5aec4c8e53c0e5f9bc2`
- Artifact set: `artifact-set_dff446489010347f7c6b9c60ed21564d6f64fc337504191c53494abc9959745a`
- Manifest: `artifact-manifest_dff446489010347f7c6b9c60ed21564d6f64fc337504191c53494abc9959745a`
- Manifest hash: `sha256:dff446489010347f7c6b9c60ed21564d6f64fc337504191c53494abc9959745a`
- Receipt: `artifact-receipt_a38c7f1e13a4b1ddc61c47008721c194978afaea27be3abf09417009cf6a734e`
- Receipt hash: `sha256:a38c7f1e13a4b1ddc61c47008721c194978afaea27be3abf09417009cf6a734e`
- Artifact count: 21
- Total artifact bytes: 146177
- Nondeterminism exceptions: none

The Story suite passes 35/35 and the complete repository suite passes 147/147 with no skips. The only emitted warning is the pre-existing pytest-asyncio loop-scope deprecation warning.
