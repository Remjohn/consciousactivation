# ADR-002: Separate Harness IR And Workflow IR

Status: `ACCEPTED`

Owners: Architecture. Trace: D006, D011, D013, D014, D025; F06, F18; TS-06, TS-14.

## Context

Harness IR describes the atomic harness being designed. Workflow IR describes how Builder performs that design. Combining them would leak Builder orchestration into generated products and make lifecycle changes mutate harness semantics.

## Decision

Maintain two versioned aggregates with separate schemas, identities, migrations, compilers, and authorization. Workflow IR may reference Harness IR paths and product graph hashes but cannot own or rewrite harness values. Harness IR cannot contain worker, queue, retry, sandbox, or deployment state.

## Alternatives

- One universal IR: rejected because it conflates product and factory authority.
- Workflow only in code or Markdown: rejected because routes, gates, retries, and promotion would be untraceable.
- Harness phases as Builder workflow nodes: rejected because downstream runtime phases are compiler outputs.

## Interfaces, Data, And Errors

`CompileWorkflow(product_graph_refs) -> WorkflowIR`; workflow nodes invoke typed application commands against a Harness IR revision. Cross-IR references include schema version and hash. Mismatch returns `ReferencedProductGraphChanged` and triggers recompile/invalidation.

## Authority, Security, And Determinism

Only deterministic compilers create Workflow IR. Agents can propose topology but cannot promote it. Separate access policies prevent workflow workers from acquiring product authority.

## Consequences

Positive: clear ownership, independent evolution, safer rollback, and faithful Control Tower views. Cost: cross-IR compatibility and invalidation machinery.

## Observability, Performance, Migration

Events carry both identities when workflow acts on product state. In-flight workflows remain bound to one compatible pair. Future schema migrations are independent and receipt-backed.

## Verification

Schema tests reject orchestration fields in Harness IR and product-semantic fields in Workflow IR. Replay tests bind every node result to exact product and workflow hashes.

