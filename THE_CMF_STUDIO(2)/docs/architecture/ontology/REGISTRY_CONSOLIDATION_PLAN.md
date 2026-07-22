# Registry Consolidation Plan V1

## Goal

Create a canonical registry architecture that eliminates scattered, duplicate, and untyped entries across primitives, composition, evals, skills, providers, styles, and content systems.

## Proposed registry namespaces

```text
registry.primitive.meaning
registry.primitive.experience
registry.methodology
registry.content.archetype
registry.content.asset_derivative
registry.content.meme_mechanism
registry.content.reaction_archetype
registry.sequence.pattern
registry.composition.template
registry.composition.frame_profile
registry.visual.style_route
registry.visual.motion_skill
registry.asset.class
registry.asset.role
registry.provider.capability
registry.eval.rubric
registry.agent.role
registry.skill.binding
registry.ui.action
```

## Required registry entry fields

```json
{
  "registry_id": "registry.visual.style_route",
  "entry_id": "style.gmg.expert_04.paper_architect.v1",
  "version": "1.0.0",
  "status": "active",
  "display_name": "GMG Expert 04 — Paper Architect",
  "description": "...",
  "required_inputs": [],
  "forbidden_inputs": [],
  "compatible_frame_profiles": [],
  "compatible_content_archetypes": [],
  "primitive_affinities": [],
  "eval_rubric_refs": [],
  "provider_capability_refs": [],
  "source_docs": [],
  "owner_component": "Visual Style Router"
}
```

## Consolidation workflow

```text
1. Inventory all existing registry files.
2. Inventory all bundle registries.
3. Inventory all skill folders.
4. Assign every entry to one namespace.
5. Detect duplicates and aliases.
6. Create canonical IDs.
7. Create migration crosswalk.
8. Validate all entries against schemas.
9. Generate TypeScript consumers.
10. Add registry service query API.
```

## Non-negotiable registry laws

1. No prompt skill without a registry entry.
2. No style route without required-input declarations.
3. No composition template without frame profile compatibility.
4. No eval rubric without target object type.
5. No provider capability without input/output and receipt schema.
6. No primitive use without primitive ID and role.
