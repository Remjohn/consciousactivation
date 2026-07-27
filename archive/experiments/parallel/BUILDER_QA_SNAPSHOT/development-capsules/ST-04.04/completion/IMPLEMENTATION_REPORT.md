# ST-04.04 implementation report

Verdict: `PASS`

`ST-04.04 / BUILDER_INTERNAL_HANDOFF` now compiles the exact active ST-04.03 Phase Graph and its hash-pinned handoff declarations into immutable Phase Context and Phase Handoff graphs for the category-neutral synthetic Builder Core proof.

The compiled contract represents both governed phases exactly once and defines one direct internal handoff from `ratified_boundary_ready` / `atomic_boundary_module` to `governed_contract_ready` / `governed_contract_module`. It preserves exact input/output declarations, single primary field ownership, authority, compatibility, mutation prohibitions, invalidation scope, all predecessor lineage, and deterministic graph and receipt identities. Context declarations remain declarative: the implementation does not select, load, budget, truncate, or execute context.

The Builder can issue the governed handoff only from the completed active producer phase with the exact frozen-boundary and boundary-validation-receipt artifacts. Artifact identity, version, hash, provenance, and the complete lineage chain are validated before commit. The governed receiver must make one explicit immutable acceptance or typed rejection decision. Acceptance never mutates upstream artifacts; rejection produces no downstream artifact state.

Identical compile, issue, and decision commands return their original receipts without duplicate events or state. Conflicting command payloads, missing or altered artifacts, wrong sender or receiver, invalid receiver authority, weakened compatibility or mutation rules, stale lineage, invalidated parents, and second decisions fail closed. Injected failures at graph compilation, handoff issuance, and receiver decision leave zero partial state.

An authorized upstream boundary reopen now atomically adds a ninth linked descendant event, `PhaseHandoffsInvalidated`, invalidating the active handoff graph and its affected issued handoffs while retaining byte-reproducible historical graphs, handoffs, decisions, and receipts. No external transport, queue, API, database, workflow execution, VAE handoff, Delegation runtime, Format 02, GPU, conversational, Control Tower, publication, or certification behavior was added. BD-014 remains open outside this Builder-internal sub-scope.

Validation completed with the preimplementation `292/292` regression, `36/36` Story tests passing twice, and final full regression `328/328 PASS` with no skips. All changed files are within the capsule allowlist; no external dependency, shared schema, database, or external-repository change was introduced.
