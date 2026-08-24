# Phase 6 Data Model

## Canonical
- primitive_definitions
- primitive_families
- primitive_geometry_definitions
- primitive_compatibility_rules
- coalition_policies
- edge_type_definitions

## Derived runtime objects
- invariant_field_packets
- representation_geometry_packets
- archetypal_geometry_packets
- primitive_candidates
- candidate_assessments
- coalition_candidates
- coalition_signatures
- edge_products

## Dynamic state
- candidate_states
- coalition_states
- edge_states
- primitive_activations

## Events
- semantic_field_events
- candidate_events
- coalition_events
- edge_events

## Receipts
- candidate_receipts
- coalition_receipts
- semantic_compilation_receipts

## Suggested relational structure

```text
primitive_definitions
primitive_families
primitive_geometry_definitions
primitive_compatibility_rules

primitive_candidates
candidate_assessments

coalition_candidates
coalition_members
coalition_signatures

edge_type_definitions
edge_products

semantic_compilation_runs
semantic_compilation_events
semantic_compilation_receipts
```

## JSONB

Good candidates:
- evidence_snapshot
- candidate_reasoning_metadata
- evaluator_payloads
- interaction_notes
- routeability_details
- crosswalk_snapshot
- model-specific diagnostic payloads

Do not use JSONB as the only representation of:
- primitive identity
- coalition membership
- edge identity
- lineage
- state
- validator verdict.

## Vector retrieval

Use vectors for:
- semantic neighborhood of authenticated evidence
- similar prior candidates
- prior coalition patterns
- similar Edge Products
- hard-negative retrieval
- prior successful route patterns

Vector similarity is evidence for retrieval, never authorization for execution.

## Graph / relational structure

Explicit relations are required for:
- Primitive ↔ Primitive synergy
- Primitive ↔ Primitive antagonism
- Primitive ↔ Invariant sensitivity
- Candidate → Evidence
- Coalition → Candidate
- Edge → Coalition
- Edge → Invariant
- Edge → Audience/Gues relational context

## Immutability

Canonical registry definitions are versioned.
Authenticated evidence is immutable.
Candidate and coalition artifacts are append-only in execution history.
Corrections create new versions/events rather than rewriting history.
