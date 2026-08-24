# CAE Semantic Operation API Protocol v1.0

## 1. Purpose

Agents should not reason over or mutate an amorphous database surface.
They should operate through a typed semantic function layer that exposes the subset of the ontology, state model, relations, and transition contracts relevant to the current mission.

This is the CAE implementation of the broader pattern:

```text
Human / Agent Intent
→ Schema Linking
→ Relevant Entities + Relations
→ Subproblem Decomposition
→ Retrieval / Composition Plan
→ Structured Query
→ Execute
→ Validate
→ Typed Error
→ Repair
```

## 2. Operation families

### World / evidence

- `search_world_signals`
- `get_cultural_memory`
- `get_research_evidence`

### Audience

- `get_audience`
- `get_audience_schema`
- `get_audience_context_premise`
- `get_current_audience_state`
- `get_active_audience_tensions`
- `get_audience_maturity`

### Guest

- `get_guest`
- `get_guest_story_archive`
- `get_guest_voice_dna`
- `get_guest_state`
- `find_guest_audience_resonances`

### Semantic discernment

- `get_active_invariants`
- `get_representation_geometry`
- `get_archetypal_geometry`
- `get_species_composition_rules`

### Pressure / edging

- `get_pressure_field`
- `generate_broad_primary_signals`
- `evaluate_edge_candidates`

### Human evidence

- `issue_provocation`
- `record_interview_response`
- `authenticate_evidence`

### Primitive / coalition

- `find_eligible_primitives`
- `generate_primitive_candidates`
- `score_candidate_survival`
- `generate_coalition_candidates`
- `validate_coalition`
- `form_coalition`
- `form_edge_product`

### SFL

- `resolve_sfl_function_profile`
- `compile_sfl_stack`
- `validate_perceptual_alignment`

### Realization

- `resolve_archetype_container`
- `compile_semantic_program`
- `compile_scene_plan`
- `compile_composition_ir`

### State control

- `get_current_run_state`
- `get_legal_transitions`
- `evaluate_transition`
- `request_transition`
- `commit_transition`
- `record_transition_receipt`
- `get_unresolved_obligations`

## 3. Function contract requirements

Every exposed semantic operation should specify:

```yaml
operation_id:
purpose:
role_required:
input_schema:
output_schema:
reads:
writes:
preconditions:
postconditions:
validators:
errors:
receipt_type:
idempotency:
authority_scope:
```

## 4. Authorization by semantic role

Agent access must be bounded by role and mission.

Example:

```text
Interview Compiler
  READ: Audience, Guest, Context, SDA, Research
  WRITE: Provocation, InterviewResponse, EvidenceAuthenticationRequest
  CANNOT WRITE: Canonical primitive definitions
```

## 5. Typed errors

Preferred errors include:

- `SCHEMA_ERROR`
- `TAXONOMY_ERROR`
- `RELATION_ERROR`
- `STATE_ERROR`
- `EVIDENCE_ERROR`
- `PROVENANCE_ERROR`
- `TRANSITION_ERROR`
- `AUTHORITY_ERROR`
- `PRIMITIVE_ERROR`
- `COALITION_ERROR`
- `EDGE_ERROR`
- `SEMANTIC_DRIFT`
- `FORMAT_DRIFT`
- `COMPOSITION_ERROR`
- `VALIDATION_ERROR`
- `ENVIRONMENT_FIDELITY_ERROR`
- `REWARD_HACK_ERROR`
- `TASTE_REGRESSION`
- `ANTI_CENTROID_ERROR`
- `RUNTIME_ERROR`

## 6. SQL is downstream of semantic intent

The agent may receive a structured query plan or invoke an approved query function. It should not infer table topology by improvisation when an authoritative semantic function exists.

The semantic API therefore becomes the controlled operating language above SQL.
