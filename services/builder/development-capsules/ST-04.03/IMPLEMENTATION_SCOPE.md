# Implementation scope

Implement one additive category-neutral phase-graph compiler over the exact active ST-04.02 responsibility-module graph.

The compiler loads the hash-pinned synthetic phase input; verifies every module reference, entry condition, exit evidence, gate, failure owner, dependency, and parallelism declaration; rejects cycles and inferred parallelism; computes deterministic topological and runnable-state views; and atomically attaches one immutable graph and receipt to the existing run.

Required work is limited to two new source modules plus additive run, port, in-memory persistence, and upstream invalidation support. No phase executes. No Context Graph, handoff behavior, Workflow IR, Control Tower, external runtime, database, API, UI, category adapter, or production profile is implemented.
