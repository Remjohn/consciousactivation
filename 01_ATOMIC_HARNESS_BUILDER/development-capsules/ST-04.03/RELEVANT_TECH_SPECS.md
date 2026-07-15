# Governing technical specifications

## Primary: TS-07

`docs/tech-specs/specs/TS-07-OWNERSHIP-PHASE-CONTEXT-CONTRACT-REFERENCE-REPAIR-GRAPHS.md`

ST-04.03 implements only TS-07's Phase Graph slice: explicit phase nodes, declared prerequisites, deterministic topological order, explicit safe parallelism, gate preservation, failure ownership, and content-addressed identity. Cycles, undeclared references, inferred parallelism, or gate bypass block commit.

## Boundary references

- `TS-12-HARNESS-CONTROL-TOWER.md`: events remain projectable; no Control Tower behavior is implemented.
- `TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md`: implementation and completion evidence remains exact and hash-bound; no capsule compiler is implemented.
- `TS-14-BUILDER-WORKFLOW-RUNTIME.md`: Phase Graph is a Harness product contract, not Workflow IR and not runtime execution.

No Context, Contract, Reference, Loading, Repair, handoff, workflow, scheduler, retry, sandbox, provider, or external runtime behavior is in scope.
