# Operator Request → Exact Tool Program

## Programmed Model candidate

This is one of the highest-value Programmed Models in the product.

Canonical learned capability claim:

> Given a current run state, selected artifact or timeline region, Atomic Harness,
> category-native tool registry, retrieved precedent, and an operator correction,
> compile the smallest valid typed change program that produces the requested result.

## Input

```yaml
operator_revision_request:
  run_ref: required
  target_refs: []
  category_id: required
  natural_language_request: required
  direct_manipulation_delta_ref: optional
  current_state_ref: required
  evaluation_ref: optional
  jit_capsule_ref: required
  permitted_tool_registry_ref: required
```

## Output

```yaml
change_request_program:
  interpretation: structured
  target_layer_or_nodes: []
  exact_operations:
    - tool_id
      tool_version
      arguments
      preconditions
      expected_effect
  declared_invariants: []
  required_transformations: []
  creative_degrees_of_freedom: []
  invalidated_downstream_nodes: []
  validation_plan: []
  preview_required: boolean
  confidence: number
  escalation: optional
```

## Execution

```text
operator request
→ Revision Compiler
→ deterministic schema and authority validation
→ dry-run or preview
→ execute exact tools
→ evaluate
→ accept or request another correction
→ HumanResolutionEpisode
```

## Model organization

Use one shared request-understanding layer plus category-specific capability claims:

- Static Revision Compiler;
- Video Revision Compiler;
- VAE Asset Revision Compiler;
- Interview Session Revision Compiler;
- Campaign Orchestration Revision Compiler.

A universal unrestricted tool-calling model is not the production target.

## Training source

Every human correction captured by `HumanResolutionEpisode` becomes direct training and
evaluation material for these Programmed Models.
