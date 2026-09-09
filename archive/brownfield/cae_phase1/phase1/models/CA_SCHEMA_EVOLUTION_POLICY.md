# Conscious Activation Engine — Schema Evolution Policy

## Purpose

This policy governs how discovered concepts become canonical data structures without turning experimental inference into accidental ontology.

## Canonical Evolution Path

```text
Evidence / Observation
        ↓
Hypothesis
        ↓
JSONB / experimental object
        ↓
Repeated observation + contrastive verification
        ↓
Candidate concept
        ↓
Object Constitution
        ↓
Canonical taxonomy / ontology placement
        ↓
Typed schema
        ↓
SQL relation / column / function
        ↓
Runtime use
        ↓
Outcome evidence
        ↓
Versioned refinement
```

## Laws

1. A novel field does not become ontology merely because an agent generated it.
2. A concept becomes canonical only after role, boundary, provenance, and validation are explicit.
3. Immutable evidence is never rewritten to fit the new schema.
4. Dynamic state is stored as observation history; current state is a projection, not a replacement for history.
5. JSONB may carry structured prose, examples, hypotheses, and evolving attributes when they have a defined role and schema boundary.
6. JSONB must not become an ungoverned document dump.
7. Vectors are retrieval infrastructure, not the authority for ontology.
8. SQL functions/views are allowed to expose narrow semantic operations to agents and thereby function as governance boundaries.
9. Any promoted concept must receive a versioned Object Constitution before production-critical use.
10. Reclassification requires lineage and migration notes.

## Promotion Tests

A candidate is eligible for promotion when:

- its role is stable;
- its nearest neighbors are understood;
- its provenance is adequate;
- its state/lifecycle behavior is known;
- its relationships are explicit;
- its operational questions are identifiable;
- validators exist;
- a hard-negative or contrastive boundary is available where ambiguity is material.
