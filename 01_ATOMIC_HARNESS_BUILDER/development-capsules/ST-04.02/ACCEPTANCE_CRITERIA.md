# Acceptance criteria

## AC-01 — Exact active parent

Given the PASS ST-04.01 graph and receipt, when module compilation begins, then the active run, capability graph, Harness IR, constitutional lineage, owner assignments, receipt identities, and hashes match exactly and none is invalidated.

## AC-02 — Exact capability partition

Given the three active capabilities, when modules compile, then every capability appears in exactly one module, no capability is missing or duplicated, and the module and capability order is canonical.

## AC-03 — Responsibility-centered boundaries

Given each module, when its boundary is validated, then it declares one cohesive outcome responsibility, a non-empty reason for the boundary, owned capabilities, and no identity based only on database, API, UI, router, agent, adapter, queue, worker, or infrastructure layers.

## AC-04 — Complete public contracts

Given each module, when accepted, then its public input/output contract, invariants, exclusions, dependency set, failure owner, and failure modes are explicit; hidden side effects and undeclared dependencies fail closed.

## AC-05 — Complete public test seams

Given each module, when accepted, then a public command seam, expected fixtures, contract tests, failure injections, and observable outputs are all non-empty and attributable.

## AC-06 — Authority preservation

Given capability owner assignments, when capabilities are grouped, then no module silently changes an owner kind or authority boundary; mixed owner-kind authority without an explicit governed boundary fails closed.

## AC-07 — Dependency integrity

Given module dependencies, when the graph is compiled, then references resolve, self-dependencies and cycles fail closed, dependency order is deterministic, and no Phase Graph or Workflow IR semantics are inferred.

## AC-08 — Scope separation

Given the synthetic Builder Core profile, when modules compile, then the result remains synthetic, repository-owned, non-production, and non-certified and adds no Format 02, VAE, Delegation runtime, GPU, conversational, Control Tower, workflow, or production behavior.

## AC-09 — Atomicity and idempotency

Given a valid command, when committed or repeated, then graph, run event/reference, command record, and receipt commit atomically; repeat payloads return the same receipt and stale, changed, or injected-failure commands leave no partial state.

## AC-10 — Invalidation and history

Given an active module graph, when its capability graph or authoritative boundary is invalidated, then the module graph becomes inactive, a new immutable version is required, and historical bytes remain reproducible.

## AC-11 — Observability

Given success, replay, invalidation, or failure, when evidence is emitted, then run, Story, capability graph, module graph, module/capability counts, test-seam coverage, authority, provenance, command, correlation, outcome, and typed failure context are observable without payload logging.

## AC-12 — Bounded completion

Given completion, when the Story receipt is issued, then all tests, exact file scope, rollback, 221 predecessor regressions, three owned obligations, and prohibited-boundary assertions pass with no later Story or production claim.
