# Conscious Activation Engine — Authorized Semantic Functions

Phase 1 establishes the doctrine that agents should reason through controlled semantic functions rather than arbitrary database access.

## Function families

### Retrieval

- `get_audience_world(audience_id)`
- `get_active_audience_state(audience_id)`
- `get_guest_world(guest_id)`
- `get_current_guest_state(guest_id)`
- `get_context_premise(audience_id, theme)`
- `get_active_tensions(audience_id)`
- `get_relevant_invariants(context)`
- `get_cultural_memory(context)`
- `get_research_field(context)`

### Relational

- `find_guest_audience_resonances(guest_id, audience_id)`
- `find_trigger_matches(guest_id, audience_id, tension_set)`
- `find_schema_crossings(subject_schema, object_schema)`

### Transformation

- `find_eligible_primitives(semantic_field, constraints)`
- `generate_primitive_candidates(evidence_set, allowed_families)`
- `evaluate_candidate_survival(candidates, constraints)`
- `generate_coalition_candidates(candidates, constraints)`
- `select_coalition(candidates, constraints)`
- `derive_edge_product(coalition, evidence, context)`

### Planning

- `build_interview_plan(context, guest, audience)`
- `build_semantic_composition_plan(edge, archetype_set)`
- `build_scene_composition_plan(semantic_program, format)`

### Validation

- `validate_object_constitution(object_spec)`
- `validate_relationship(subject, relation, object)`
- `validate_state_transition(entity, previous_state, next_state)`
- `validate_semantic_integrity(program)`
- `validate_anti_centroid(output)`
- `classify_error(failure)`
- `build_repair_plan(failure, taxonomy)`

Functions are conceptual authorization boundaries in Phase 1. Concrete SQL signatures and implementation contracts belong in later technical specifications.
