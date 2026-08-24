# Phase 7 — Semantic Program and IR Contract

## SemanticProgram purpose

`SemanticProgram` is the intermediate representation between semantic compilation and physical media realization. It is the first downstream-facing object that contains a complete structural/perceptual authorization for Phase 8 without containing implementation-specific scene instructions.

## Required fields

```yaml
program_id:
version:
source_edge_product_id:
archetype_container_id:
sfl_stack_id:
composition_depth_profile_id:
audience_state_ref:
guest_state_ref:
sda_refs:
jit_directives:
sections:
semantic_invariants:
required_effects:
forbidden_effects:
route_targets:
validation_status:
provenance:
```

## SemanticProgramSection

Each section should identify:
- semantic purpose
- structural role
- evidence lineage
- required transition
- emphasis
- permitted variation
- SFL expectations
- validation hooks

## Not allowed in SemanticProgram

- concrete asset file IDs unless purely declarative and Phase 8-safe
- coordinates
- scene-edit commands
- frame-accurate timings
- codec settings
- renderer-specific code
- invented factual evidence

## Program properties

A valid SemanticProgram is:
- typed
- versioned
- reproducible from recorded upstream inputs
- inspectable by a human operator
- consumable by Phase 8
- rejected if critical lineage is missing

## Program stability

A SemanticProgram is derived, not canonical. It can be recomputed when upstream state or definitions change.
