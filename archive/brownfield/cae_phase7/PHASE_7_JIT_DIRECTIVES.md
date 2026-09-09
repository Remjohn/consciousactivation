# Phase 7 — Human Director Notes → JIT Directive Compilation

## Purpose

Human expertise enters the system as prose, but runtime execution requires typed instructions.

## Pipeline

```text
Director Note
   ↓
Semantic Interpretation
   ↓
Directive Candidate
   ↓
Role / Target Resolution
   ↓
Priority + Scope Binding
   ↓
Validation
   ↓
JITDirective
   ↓
JITDirectiveSet
```

## Directive types

- `semantic_preservation`
- `structural_preference`
- `perceptual_intent`
- `rhythm_instruction`
- `emphasis_instruction`
- `forbidden_effect`
- `variation_instruction`
- `human_texture_instruction`
- `asset_strategy_hint` (advisory only until Phase 8)

## Example

Human prose:

> “I want this to feel like recognition, not motivation. Let the reveal land without explaining it.”

Typed form:

```yaml
intent_type: perceptual_intent
 target: semantic_program
 desired_effect: recognition
 forbidden_effect: motivational_framing
 explanation_policy: preserve_implication
 source: director_note
 priority: high
```

## Constitutional rule

A Director Note may sharpen or constrain a program, but it does not mutate canonical ontology, primitive definitions, archetype definitions, or SFL definitions in place.

Canonical change requires an architecture-governed update path.
