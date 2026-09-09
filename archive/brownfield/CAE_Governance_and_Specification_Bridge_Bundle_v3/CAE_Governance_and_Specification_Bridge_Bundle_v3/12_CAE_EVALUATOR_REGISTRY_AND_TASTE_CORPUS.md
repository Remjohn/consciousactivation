# CAE Evaluator Registry & Taste Corpus Protocol v2.0

## Purpose

CAE evaluators themselves are governed assets. A system can reward-hack not only application logic but the evaluators that judge it.

Therefore evaluators, fixtures, hard negatives, mutation suites, and taste examples require lineage, versioning, and ownership.

## Evaluator registry record

Each material evaluator SHOULD be represented as a typed registry record containing:

```yaml
evaluator_id:
name:
version:
claim_scope:
artifact_classes: []
ontological_planes: []
input_contract:
output_contract:
primary_metric:
proxy_definition:
intended_property:
known_gaming_modes: []
required_environment_fidelity:
taste_dimensions: []
anti_centroid_dimensions: []
hard_negative_suite_id:
mutation_suite_id:
owner:
source_lineage: []
last_calibrated_at:
status:
```

## Taste corpus taxonomy

The corpus SHOULD distinguish:

- `POSITIVE_REFERENCE`
- `GENERIC_NEAR_NEGATIVE`
- `SEMANTICALLY_VALID_PERCEPTUALLY_DEAD`
- `OVEREXPLAINED`
- `FALSE_DEPTH`
- `SYNTHETIC_AUTHORITY`
- `DEAD_POLISH`
- `EMPTY_MOTIVATIONAL_SMOOTHNESS`
- `CENTROIDED_REPAIR`
- `EDGE_PRESERVING_REPAIR`

The inherited SFL corpus SHOULD be mapped into this taxonomy without changing original source identities.

## Anti-centroid calibration

A taste corpus must include not only bad outputs but **false positives** that the evaluator is tempted to approve.

Example:

```text
A polished, grammatically perfect, balanced paragraph
that contains no concrete lived detail and no tension.
```

This should be structurally valid but taste-negative.

Similarly, a deliberately sharp output that violates no semantic invariant but uses uncommon phrasing SHOULD NOT be rejected merely for being unusual.

## Evaluator independence

Where practical, the same implementation agent SHOULD NOT:

1. implement the evaluator;
2. implement the feature being evaluated;
3. calibrate the reward metric;
4. decide the final promotion result.

At minimum, the system should use distinct roles or separate evaluation stages.

## Calibration rule

Whenever a validator is changed:

- rerun its existing test suite;
- rerun reward-hack cases;
- rerun taste corpus;
- compare score distribution before/after;
- inspect newly passing hard negatives;
- record the calibration event.

## No scalar-only law

No evaluator that protects a high-value CAE quality property may rely on one scalar score without contrastive evidence.

A score is a measurement.

It is not the property itself.
