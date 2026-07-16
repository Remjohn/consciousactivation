# Governing technical specifications

## Primary: TS-07

`docs/tech-specs/specs/TS-07-OWNERSHIP-PHASE-CONTEXT-CONTRACT-REFERENCE-REPAIR-GRAPHS.md`

ST-04.02 implements only TS-07's responsibility-centered `Module` slice: responsibility, owned capabilities, public contracts, invariants, exclusions, dependencies, failure owner, boundary rationale, and test seams. Compilation is deterministic and content-addressed; missing ownership, duplicate coverage, hidden side effects, mixed authority, or incompatible dependency topology blocks the commit.

## Boundary references

- `TS-12-HARNESS-CONTROL-TOWER.md`: events must remain projectable, but this Story implements no Control Tower query, command, API, UI, or projection.
- `TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md`: implementation and completion receipts remain exact and hash-bound; this Story does not implement capsule compilation.
- `TS-14-BUILDER-WORKFLOW-RUNTIME.md`: Harness module contracts remain product outputs and must not absorb Workflow IR, routing, scheduling, execution, retry, or sandbox behavior.

No TS-07 Phase Graph, Context Graph, Reference Graph, Loading Graph, Repair Graph, external handoff, or generated workflow behavior is in scope.
