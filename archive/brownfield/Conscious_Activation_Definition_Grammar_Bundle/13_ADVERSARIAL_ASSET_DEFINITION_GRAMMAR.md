# Adversarial Evaluation Asset Definition Grammar Protocol

## Artifact class

`ADVERSARIAL_ASSET`

## Purpose

Defines contrastive evaluation material designed to expose deceptively close failures.

## Definition grammar

Use:

**Positive Anchor + Deceptive Near-Neighbor + Divergence Axes + Expected Failure + Mutation Suite + Validator Expectation**

## Examples

`HardNegative`, `MutationStressSuite`, `FalseDepthContrastCase`, `DeadPolishCase`, `SemanticDriftCase`.

## Required property

An adversarial asset must test a meaningful distinction, not merely provide an obviously bad example.

## Hard negative structure

```yaml
positive_anchor:
negative_variant:
divergence_axes:
adjacency_class:
mutation_tests:
expected_validator_outcomes:
```

## Hard negatives for the protocol itself

- negative example that is obviously bad
- negative example differing on irrelevant dimensions
- benchmark case without expected verdict
- failure asset accidentally used as production ontology
