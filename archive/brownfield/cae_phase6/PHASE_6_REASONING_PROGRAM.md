# Phase 6 Reasoning Program

## Mission

Given authenticated evidence and current semantic context, determine the smallest admissible set of transformation operators that preserves the evidence's live tension and produces a routeable semantic force object.

## SQL-of-Thought-inspired procedure

```text
Intent
↓
Schema Linking
↓
Evidence Linking
↓
Relevant Invariants / Geometry
↓
Relevant Primitive Families
↓
Subproblem Decomposition
↓
Candidate Generation
↓
Eligibility Plan
↓
Candidate Survival
↓
Compatibility Plan
↓
Coalition Plan
↓
Routeability Check
↓
Edge Product Derivation
↓
Validation
↓
Typed Error / Repair
↓
Receipt
```

## Agent governance

Agents should not be given the entire primitive registry when a relevant subset can be resolved through controlled queries.

Preferred functions:

```text
get_relevant_invariants(evidence_id)
get_relevant_representation_geometries(context_id)
find_eligible_primitives(evidence_id, constraints)
find_primitive_compatibilities(primitive_ids)
generate_candidate_set(evidence_id, primitive_subset)
score_candidate_survival(candidate_ids)
find_coalition_templates(candidate_ids, route)
derive_edge_product(coalition_id)
validate_coalition(coalition_id)
```

## Reasoning rules

- explore widely before selecting;
- preserve source language;
- explain every candidate through evidence lineage;
- do not choose a coalition because it is familiar;
- do not increase primitive count to simulate richness;
- prefer sparse force concentration;
- treat antagonism as potentially useful only when explicit contrast is intended;
- classify failure instead of retrying blindly.

## Anti-centroid patrol

The Semantic Patrol Agent MUST specifically search for:
- abstraction replacing source specificity;
- polite averaging of contradictory positions;
- disappearance of costly or vulnerable evidence;
- generic motivational language;
- broad claims replacing exact claims;
- unnecessary “safe” reframing;
- flattening of edge into neutral educational language.

The patrol is not an approval authority for blandness. Its purpose is to detect drift from the authenticated field.

## Human escalation

Escalate when:
- evidence is genuinely ambiguous;
- two coalitions remain materially tied;
- a new primitive definition appears necessary;
- a candidate requires changing canonical ontology;
- the coalition is high-impact and routeability is contested.
