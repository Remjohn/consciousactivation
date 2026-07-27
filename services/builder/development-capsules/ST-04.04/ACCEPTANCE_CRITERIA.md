# Acceptance criteria

## AC-01 — Compile the internal contracts

Given the exact active ST-04.03 Phase Graph, its PASS receipt, and the hash-pinned synthetic handoff input, when the authorized Builder code compiles ST-04.04, then it emits immutable context contracts for every phase, an aggregate Context Graph, the declared typed handoff contract, and one attributable completion receipt.

## AC-02 — Preserve exact coverage and lineage

Given two active Phase Graph nodes and their module, responsibility, authority, input and output declarations, when compilation succeeds, then both phases are represented exactly once and every context and handoff preserves the exact Phase Graph identity plus the complete upstream lineage chain.

## AC-03 — Enforce one authoritative owner

Given every included context field and every authoritative handoff field, when ownership is validated, then each field has exactly one primary owner and authority; missing, duplicate or conflicting ownership fails closed with zero committed partial state.

## AC-04 — Protect upstream truth

Given an immutable upstream handoff value, when a downstream phase attempts to alter, substitute, omit or relabel that authoritative value, then the command fails closed and requires a new authoritative upstream artifact version rather than mutating existing truth.

## AC-05 — Validate phase and dependency integrity

Given a handoff producer and its consumers, when contracts are compiled, then every phase and field is declared by the active Phase Graph, every consumer is a valid descendant, all required fields exist in producer outputs and consumer inputs, and dangling or reversed dependencies are rejected.

## AC-06 — Govern context declarations without implementing completeness

Given the exact context declarations in the governed input, when the Context Graph is compiled, then inclusions, exclusions, conditional loads, unload behavior and downstream exposure are preserved deterministically; no context is inferred, selected, loaded, budgeted or silently truncated.

## AC-07 — Enforce version and compatibility semantics

Given a versioned handoff contract, when identical governed inputs are recompiled, then bytes and identities are identical; when a field, owner, authority, compatibility, mutation, exposure or invalidation rule changes, a new immutable identity is required and incompatible reuse fails closed.

## AC-08 — Limit invalidation impact

Given an invalidated parent Phase Graph or changed authoritative producer contract, when impact is evaluated, then active affected handoff descendants are invalidated while unrelated context and historical artifacts remain unchanged and reproducible.

## AC-09 — Preserve authority and provenance

Given code authority and valid upstream provenance, when compilation occurs, then the receipt records producer, consumer, owners, authority, provenance and lineage; missing or unverifiable authority, provenance or constitutional evidence fails closed.

## AC-10 — Preserve replay, idempotency and atomicity

Given an identical command identity and payload, when the command repeats or resumes, then it returns the same graph and receipt without duplicate state; a conflicting payload is rejected; injected failure commits no graph, receipt, event or command record.

## AC-11 — Keep external boundaries closed

Given the Builder-first internal-handoff mode, when ST-04.04 runs, then no Format 02, VAE, Delegation runtime, shared schema ownership, external provider, GPU, evaluator, conversational, Control Tower, production or publication behavior is invoked or claimed, and BD-014 remains open for external-product handoffs.

## AC-12 — Produce bounded completion evidence

Given all tests and regressions pass, when completion is evaluated, then observations, rollback evidence, exact changed-file hashes, scope validation and a separate canonical Story Completion Receipt are present; ST-04.05 remains unauthorized.
