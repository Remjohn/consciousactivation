# Validation Report — CAE Mandate M08: Archetype / Format Compatibility

- **Mandate ID**: `M08`
- **Functional Requirement**: `FR-IP-004` (Downstream composition, format, and narrative compatibility)
- **Status**: `VERIFIED & PASSING`
- **Date**: 2026-08-30
- **Scope**: `services/interview-intelligence/src/cae_interview_intelligence/composition_compatibility.py`, `question_resolver.py`, `__init__.py`, and `tests/interview_intelligence/test_composition_compatibility.py`

---

## 1. Executive Summary

Mandate `M08` establishes the downstream format, archetype, and narrative role compatibility contract (`FR-IP-004`) within the CAE Interview Intelligence Service.

It exposes downstream format and archetype intent as explicit constraints that shape question resolution and candidate evaluation without allowing format or archetype containers to manufacture evidence or override absent lived testimony.

---

## 2. Implemented Components & Registries

### 2.1 Authoritative Downstream Registries
Reuses existing CMF and AIR identifiers:
- **Known Content Archetypes (`KNOWN_ARCHETYPES`)**:
  - `ARCH-CRUCIBLE` (`archetype:crucible_testimony`): High-friction reckoning and sacrifice. Preferred: `EPISODIC` / `STORY`. Expected shape: `["chronological_event", "internal_friction", "cost_paid"]`.
  - `ARCH-WITNESS` (`archetype:witness`): First-hand empirical observation. Preferred: `EPISODIC` / `STORY`. Expected shape: `["observed_scene", "sensory_detail", "verifiable_action"]`.
  - `ARCH-ACHIEVEMENT` (`archetype:achievement_story`): Transformation over systemic barrier. Preferred: `EPISODIC` / `STORY`. Expected shape: `["starting_barrier", "inflection_decision", "transformation_outcome"]`.
  - `ARCH-INVESTIGATIVE` (`archetype:investigative_breakdown`): Causal breakdown of systemic debt. Preferred: `MECHANISTIC` / `FACT`. Expected shape: `["causal_mechanism", "structural_anomaly", "empirical_metric"]`.
  - `ARCH-DEBUNK` (`archetype:myth_debunk`): Exposing consensus illusion. Preferred: `MECHANISTIC` / `COUNTERFACTUAL`. Expected shape: `["stated_orthodoxy", "contradictory_evidence", "underlying_reality"]`.
  - `ARCH-OBSERVATIONAL` (`archetype:observational_humor`): Systemic critique with sharp wit. Preferred: `SPECIFIC` / `INTERPRETATION`. Expected shape: `["absurd_norm", "unspoken_incentive", "cultural_contradiction"]`.
- **Known Delivery Formats (`KNOWN_FORMATS`)**:
  - `FMT-01-STORY` (`format:01_story`): Cinematic multi-roll story harness (`A_ROLL_NARRATIVE`, `B_ROLL_CONTEXT`, `C_ROLL_EVIDENCE`, `E_ROLL_SONIC`).
  - `FMT-02-REACTION` (`format:02_reaction`): Reaction/commentary harness.
  - `FMT-03-BREAKDOWN` (`format:03_breakdown`): Deep analytical breakdown harness (`ANOMALY_HOOK`, `CAUSAL_TRACE`, `EMPIRICAL_PROOF`, `SYSTEM_CONCLUSION`).
  - `FMT-04-CAROUSEL` (`format:04_carousel`): Structured sequential multi-slide narrative harness.
- **Known Narrative Roles (`KNOWN_NARRATIVE_ROLES`)**:
  - `ROLE-PROTAGONIST-CRUCIBLE`, `ROLE-OBSERVER-WITNESS`, `ROLE-TECHNICAL-ANALYST`, `ROLE-CONTRARIAN-DEBUNKER`, `ROLE-SYSTEMIC-CRITIC`.

### 2.2 Composition Compatibility Model & Evaluator
- **`CompositionCompatibility`**: Derived model exposing `archetype_refs`, `format_refs`, `narrative_role_refs`, `expected_response_structure`, `compatibility_score`, `compatible_reasons`, and `incompatible_reasons`.
- **`CompositionCompatibilityEvaluator`**: Multi-dimensional evaluator matching target resolution and evidence mode against archetype requirements, rejecting invalid syntax (e.g. promotional soundbite broadcast), and evaluating roll pacing constraints.
- **Anti-Evidence Manufacturing Invariant (`assert_archetype_does_not_manufacture_evidence`)**: Ensures generic/slop responses cannot be converted into authenticated story evidence merely by attaching an archetype label.

---

## 3. Test Suite Verification

All 6 acceptance criteria for Mandate M08 pass unconditionally:

```text
tests/interview_intelligence/test_composition_compatibility.py::test_story_oriented_hypothesis_prefers_episodic_evidence PASSED [ 16%]
tests/interview_intelligence/test_composition_compatibility.py::test_mechanism_oriented_hypothesis_prefers_mechanistic_evidence PASSED [ 33%]
tests/interview_intelligence/test_composition_compatibility.py::test_semantically_strong_question_rejected_when_composition_incompatible PASSED [ 50%]
tests/interview_intelligence/test_composition_compatibility.py::test_archetype_labels_cannot_turn_generic_responses_into_story_evidence PASSED [ 66%]
tests/interview_intelligence/test_composition_compatibility.py::test_compatibility_view_exposes_derived_reasons_and_expected_response_structure PASSED [ 83%]
tests/interview_intelligence/test_composition_compatibility.py::test_format_harness_constrains_multi_roll_narrative_roles PASSED [100%]
```

Full repository regression verification: **71 / 71 tests passing**.
