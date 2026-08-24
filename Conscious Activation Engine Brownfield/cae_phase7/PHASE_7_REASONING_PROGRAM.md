# Phase 7 — Agent Reasoning Program

## Governing agent pattern

```text
Human / Event Intent
↓
Schema Linking
↓
Relevant Edge + State + Archetype + SFL Entities
↓
Subproblem Decomposition
↓
Archetype Plan
↓
SFL Plan
↓
Depth Plan
↓
Contract Assembly
↓
Validation
↓
Typed SemanticProgram
↓
Repair / Escalation if required
```

## SQL-of-Thought style decomposition

The agent MUST NOT receive the full knowledge universe by default. It should query authorized views/functions such as:

- `get_edge_product_context(edge_id)`
- `find_eligible_archetypes(edge_id, state)`
- `get_archetype_contract(archetype_id)`
- `find_sfl_functions(edge_id, archetype_id, state)`
- `get_sfl_alignment_policy(function_ids, brand_id)`
- `get_depth_profiles(archetype_id, state)`
- `get_previous_programs(archetype_id, edge_signature)`
- `get_hard_negatives(program_class)`

## Planning questions

1. What semantic force must survive?
2. What structural carriers are admissible?
3. Which carrier best preserves the edge without overfitting?
4. What perceptual functions increase uptake without changing meaning?
5. What depth profile matches the audience's capacity and the archetype's grammar?
6. What must not be introduced during realization?
7. What evidence and contracts must be preserved into Phase 8?

## Error-aware reasoning

A failed plan must be classified before repair. Never “try again” without identifying whether the failure is schema, relationship, state, evidence, taxonomy, structural, perceptual, contract, or anti-centroid related.
