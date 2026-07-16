# Deterministic test plan

Run with `PYTHONPATH=src` and no mandatory skips.

1. Preimplementation: full repository regression must pass `292/292`.
2. Acceptance: compile the exact two-phase internal Context Graph and one versioned handoff; assert exact phase, context, handoff and field coverage.
3. Integrity: reject missing or duplicate phases, undeclared fields, dangling or reversed consumers, output/input mismatches, conflicting ownership and contract contradictions.
4. Mutation and compatibility: reject downstream upstream-value rewrites, field omission/substitution, incompatible reuse, altered governed input and in-place version mutation.
5. Authority and lineage: reject missing authority, invalid provenance, stale/superseded/invalidated Phase Graphs, receipt/hash drift and mismatched run lineage.
6. Determinism: fresh repositories and equivalent inputs yield byte-identical contexts, graph and receipt with canonical ordering and no timestamps, random IDs, machine paths or environment values.
7. Replay: identical repeats and resume are payload-safe and idempotent; conflicting commands fail without mutation.
8. Invalidation: invalidate only affected handoff descendants, block active consumption and preserve historical reproduction without rerunning unaffected state.
9. Atomicity: injected repository failure leaves zero partial context, handoff graph, receipt, event, observation or command state.
10. Observability and rollback: required success, replay, invalidation and failure evidence is attributable and rollback is non-destructive.
11. Architecture: exact source-set and import-boundary tests pass; no external runtime, schema, dependency, API, UI, database or later-Story behavior appears.
12. Regression: run the ST-04.04 suite twice, then the complete repository suite with no mandatory skips.

All assertions use exact values and hashes. There are no network, provider, GPU, VAE or Delegation runtime tests.
