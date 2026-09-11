---
name: interview_brief_composer
version: 1.0.0
description: "Passive, flat Canonical Skill for assembling canonical Activative Interview Brief payloads via ActivativeInterviewBriefCompiler and the Composer boundary."
authority_lane: COMPOSER
---

# Interview Brief Composer Skill

## 1. Purpose & Authority Lane
This skill operates strictly within the **COMPOSER** lane of `interview_semantic_program`.
Its mandate is assembling the authoritative `ActivativeInterviewBrief` payload bridging approved hypothesis candidates to the canonical Composer domain schema (`conscious_activations_interview_composer.domain.make_activative_interview_brief`).

## 2. Compilation Contracts
- Reuses existing `ActivativeInterviewBriefCompiler.compile_brief_payload` without schema duplication.
- Assembles:
  - `research_package_ref`: Validated object reference with SHA-256.
  - `tension_hypothesis`: Explicit collision thesis statement.
  - `matrix_of_edging_seed`: Evaluated 7-field Matrix of Edging seed.
  - `planned_questions`: Sequenced prompt array with activation directions and psychological roles.
  - `expression_targets`: Derived expression objectives.
  - `composer_authority`: Operator assertions (`operator_id`, `authority_scope`, `assertion_id`).

## 3. Invariant Constraints
- **Zero Rebuild**: Does not instantiate private brief models or duplicate storage schemas.
- **Lineage Integrity**: Preserves complete cryptographic provenance back to M32 Collision Hypotheses and upstream Guest DNA.
