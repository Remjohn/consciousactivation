# Governing technical specifications

## Primary: TS-07

`docs/tech-specs/specs/TS-07-OWNERSHIP-PHASE-CONTEXT-CONTRACT-REFERENCE-REPAIR-GRAPHS.md`

ST-04.04 implements only the Builder-internal Context Graph and typed handoff slice: explicit phase context declarations; versioned producer/consumer contracts; field ownership, authority, provenance, validation, compatibility and mutability; silent-rewrite rejection; and affected-descendant impact analysis.

## Boundary references

- `TS-03-CANONICAL-HARNESS-IR-AND-CORE-SCHEMAS.md`: generated contracts remain subordinate, typed projections with immutable lineage.
- `TS-06-DETERMINISTIC-COMPILER-ARTIFACT-GRAPH-AND-VERSIONING.md`: canonical bytes, content identities, atomic commits and new-version semantics are mandatory.
- `TS-11-EVALUATION-VERIFICATION-PROMOTION-AND-REPAIR.md`: hard gates HG-004, HG-005 and HG-007 fail closed; no evaluator or repair implementation is in scope.
- `TS-12-HARNESS-CONTROL-TOWER.md`: observations remain projectable; no Control Tower behavior is implemented.
- `TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md`: evidence is exact and hash-bound; no capsule compiler is implemented.
- `TS-14-BUILDER-WORKFLOW-RUNTIME.md`: handoff contracts describe Harness product semantics, not Workflow IR or execution.

TS-01 and TS-05 remain authority and lineage references only. No minimum-complete-context selection, external target handoff or runtime behavior is authorized.
