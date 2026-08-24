# Phase 6 Candidate Generation & Survival Protocol

## Objective

Turn authenticated evidence into multiple plausible transformation candidates before selecting any coalition.

## Candidate generation

For each relevant primitive family:
1. retrieve canonical definitions;
2. retrieve source examples and admissible ranges;
3. inspect evidence for activation cues;
4. generate multiple contextual candidates;
5. attach direct evidence spans;
6. attach an explicit candidate rationale;
7. attach expected semantic effect.

## Candidate survival dimensions

Recommended score dimensions:
- evidence_fidelity
- semantic_specificity
- tension_preservation
- recognition_potential
- prediction_violation_potential
- costly_exposure_potential
- latent_pattern_articulation
- compositional_independence
- routeability
- contextual_fit

Scores are diagnostic. They do not replace eligibility rules.

## Survival states

```text
generated
→ eligible
→ evaluated
→ survived
→ selected
```

Alternative terminal states:

```text
rejected_evidence
rejected_range
rejected_compatibility
rejected_redundancy
rejected_route
rejected_genericity
superseded
```

## Candidate rejection law

A rejected candidate must record:
- rejection code;
- failed constraint;
- evidence references;
- evaluator;
- timestamp;
- whether the failure is reusable learning.

No silent deletion.
