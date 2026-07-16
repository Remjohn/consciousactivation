# Implementation scope

Implement one additive category-neutral module compiler over the exact active ST-04.01 capability ownership graph.

The compiler must load the hash-pinned module input, prove exact 3/3 capability coverage across two cohesive modules, validate owner-kind authority, public contracts, invariants, exclusions, dependencies, failure ownership, failure modes, boundary rationales, and complete public test seams, then atomically attach an immutable module graph and receipt to the existing run.

Required source work is limited to two new modules plus additive run, port, in-memory persistence, and upstream invalidation support. Required tests cover successful compilation, graph and receipt identity, malformed boundaries, horizontal-layer rejection, authority, determinism, replay, idempotency, invalidation, atomic failure, observations, and architecture boundaries.

No Phase Graph, Context Graph, Contract/Reference/Loading/Repair Graph, Workflow IR, Control Tower, task execution, external handoff, production database, API, UI, or production profile is implemented.
