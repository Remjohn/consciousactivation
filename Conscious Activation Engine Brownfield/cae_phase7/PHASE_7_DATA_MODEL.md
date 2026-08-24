# Phase 7 Data Model

## Storage law

```text
Strict relational columns → stable semantics
Relations → explicit tables / foreign keys
JSONB → evolving or sparse profile attributes
Vectors → fuzzy retrieval / semantic neighborhoods
Events → temporal history
Receipts → immutable execution lineage
```

## Canonical tables

- `archetype_definition`
- `archetype_contract`
- `sfl_function_family`
- `sfl_function_definition`
- `sfl_alignment_policy`
- `sfl_failure_asset`
- `depth_profile_definition`
- `crosswalk_archetype_sfl`
- `crosswalk_archetype_edge`

## Dynamic tables

- `archetype_eligibility_assessment`
- `archetype_selection`
- `sfl_stack`
- `sfl_stack_member`
- `perceptual_effect_profile`
- `influence_alignment_report`
- `jit_directive_set`
- `semantic_program`
- `semantic_program_section`
- `phase7_compilation_receipt`
- `phase7_failure`

## Immutable evidence

- Director Note source
- accepted Edge Product receipt
- canonical registry snapshots used at compile time
- original SFL references

## Derived objects

SemanticProgram, selection assessments, perceptual profiles, and receipts are derived from upstream state and should be reproducible.

## JSONB policy

JSONB MAY contain:
- evolving parameters
- sparse archetype-specific fields
- experimental perceptual dimensions
- example payloads
- local Director Note interpretation metadata

JSONB MUST NOT be used to hide stable relational concepts that need joins, indexes, validators, or lifecycle management.

## Vector policy

Vector search is appropriate for:
- similar Edge Products
- archetype example retrieval
- SFL example retrieval
- perceptual failure similarity
- reference program retrieval

Vector similarity never overrides typed eligibility rules.
