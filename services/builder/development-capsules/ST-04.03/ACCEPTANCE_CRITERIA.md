# Acceptance criteria

## AC-01 — Exact active parent

Given the PASS ST-04.02 graph and receipt, when phase compilation begins, then the active run, module graph, capability graph, Harness IR, constitutional lineage, receipt identities, and hashes match exactly and none is invalidated.

## AC-02 — Explicit phase coverage

Given the governed input, when phases compile, then every phase has one responsibility, explicit module references, entry conditions, exit evidence, failure ownership, dependencies, gates, and execution kind; no phase is implicit.

## AC-03 — Deterministic ordering

Given an acyclic graph, when compiled, then phase identity, canonical topological order, initially runnable phases, blocked phases, and prerequisite reasons are deterministic.

## AC-04 — Explicit safe parallelism

Given dependency-independent phases, when parallelism is declared, then it is explicit, symmetric, gate-compatible, and dependency-safe; absent declarations mean sequential or blocked, never default parallelism.

## AC-05 — Graph integrity

Given invalid topology, when a cycle, self-edge, unresolved phase, undeclared module, asymmetric parallel declaration, or dependency/parallel conflict appears, then compilation fails closed.

## AC-06 — Gate and authority preservation

Given module and authority boundaries, when phases compile, then no edge bypasses a required human or validation gate and topology grants no new authority.

## AC-07 — Scope separation

Given the synthetic Builder Core profile, when the graph compiles, then it remains declarative, synthetic, repository-owned, non-production, and non-certified and executes no work.

## AC-08 — Lineage and immutable identity

Given acceptance, when committed, then complete Source Lock through module-graph lineage is preserved, changed governed input produces a new identity, and existing history is never mutated.

## AC-09 — Atomicity and idempotency

Given a valid command, when committed or repeated, then graph, run event/reference, command record, and receipt commit atomically; identical repeats return the same receipt and changed or injected-failure commands leave no partial state.

## AC-10 — Invalidation and history

Given an active phase graph, when its module graph or authoritative boundary is invalidated, then active consumption fails closed, a new graph version is required, and historical bytes remain reproducible.

## AC-11 — Observability

Given success, replay, invalidation, or failure, when evidence is emitted, then run, Story, parent graphs, phase graph, topology counts, runnable/blocked state, gates, authority, provenance, command, correlation, outcome, and typed failure context are observable without payload logging.

## AC-12 — Bounded completion

Given completion, when the receipt is issued, then all tests, exact file scope, rollback, 256 predecessor regressions, three owned obligations, and prohibited-boundary assertions pass with no phase execution or later Story claim.
