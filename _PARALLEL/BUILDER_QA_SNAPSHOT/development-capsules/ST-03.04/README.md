# ST-03.04 Development Capsule

This capsule governs only confirmed Story `ST-03.04`, “Compile Human and Machine Artifacts Deterministically,” in bounded mode `DETERMINISTIC_ARTIFACT_SET`.

The outcome is one immutable, atomic artifact set compiled exclusively from the active `cmf-builder-harness-ir/v1@1.0.0` snapshot produced by completed ST-03.03. It contains deterministic human-readable shards, a governed OpenSpec view, machine-readable projections, a drift-verifiable manifest, and a receipt. Every artifact is bound to the exact IR hash, source node set, compiler identity/version, reproducible build configuration, and content hash.

The artifacts are generated views, not independent authority. The OpenSpec and dashboard-named artifacts are non-executable projections only. This capsule does not implement ST-03.05 constitutional cross-artifact enforcement, architecture graphs, Atomic Harness Definition compilation, Development Capsule generation, workflow/runtime execution, Control Tower, external products, Format 02, category adapters, or production behavior.

Implementation is not authorized until the exact phrase in `IMPLEMENTATION_AUTHORIZATION.yaml` is supplied by human product authority.
