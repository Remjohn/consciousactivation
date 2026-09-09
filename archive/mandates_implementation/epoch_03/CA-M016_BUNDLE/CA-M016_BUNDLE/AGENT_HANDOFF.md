# CA-M016 Agent Handoff

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/collision_matrix.py` | Added the CA-M016 grounded Collision Tension Matrix implementation: typed Audience Belief Structure, Subject Genesis Territory, World Signal, exact Verbatim Anchor coordinates, four bounded normalized score dimensions, complete rectangular matrix construction, deterministic aggregate scoring, explainability projection, stale-reference hooks, falsification requirements, and fail-closed Collision admission. | `FR-016 / FR-COLL-001`: a Collision is not admissible from a score alone; required semantic poles, admitted evidence, exact revisions/digests, verbatim anchors, supported relation semantics, falsification conditions, and bounded/explainable matrices are required. |
| `tests/phase4/test_ca_m016_collision_matrix.py` | Added mandate-specific unit coverage for normalization, multidimensional matrix shape, coordinate explainability, positive admission, score-only rejection, single-pole rejection, label-only rejection, stale pole/evidence revisions, forged verbatim quotes, missing anchors, incomplete matrices, and out-of-range scores. | The acceptance boundary is exercised against the principal positive path and required false-proof/fail-closed cases. |

## Exact paste instructions

Replace or create the following repository paths exactly:

1. `services/interview/src/conscious_activations_interview_expression/collision_matrix.py`
   ← replace/create from this bundle's file at the identical path.

2. `tests/phase4/test_ca_m016_collision_matrix.py`
   ← replace/create from this bundle's file at the identical path.

No other repository files are part of this CA-M016 bundle and no other file boundary is authorized by this implementation.

## Manual post-apply commands

No migration, dependency upgrade, or generated-file step is required.

A syntax-only validation was performed against both delivered Python files with `py_compile`. The test suite was intentionally **not run**, per the execution instruction.

The intended direct acceptance test file is:
`tests/phase4/test_ca_m016_collision_matrix.py`

## New automated tests included

- `test_normalize_score_accepts_only_bounded_finite_values`
- `test_collision_tension_score_is_mathematically_normalized`
- `test_matrix_is_rectangular_and_retains_separate_dimension_matrices`
- `test_every_score_cell_is_explainable_by_verbatim_coordinates`
- `test_positive_grounded_collision_admits_and_returns_digest`
- `test_score_only_admission_is_impossible_without_structural_poles`
- `test_beautiful_single_pole_statement_fails_closed`
- `test_three_labeled_poles_without_real_evidence_or_falsification_fails`
- `test_stale_pole_revision_is_rejected`
- `test_stale_evidence_revision_is_rejected`
- `test_forged_verbatim_quote_fails_before_matrix_admission`
- `test_missing_dimension_anchor_fails_cell_creation`
- `test_matrix_rejects_incomplete_rectangle`
- `test_matrix_rejects_out_of_range_scores_without_clamping`
- `test_anchor_coordinates_include_exact_upstream_revision_and_media_coordinates`

## Evidence and limitations

- The supplied repository archive did not contain the originally named M016 target files. The current repository did contain the Interview Expression package and the prior CA-M015 verbatim evidence implementation, so the mandated target paths were created as new, bounded M016 surfaces.
- The implementation reuses the repository's existing conceptual contracts: CA-M015's exact character-slice/verbatim evidence model, the three-pole Collision definition in `docs/cae/Architecture.md`, and `FR-COLL-001` in PRD-003.
- Every score is explicitly finite and constrained to `[0.0, 1.0]`. Out-of-range values are rejected rather than silently clamped.
- Each matrix coordinate retains separate dimension scores. The aggregate score is descriptive only and cannot authorize admission.
- Each score dimension must cite at least one exact verbatim anchor, and explanations expose source revision, media revision, temporal coordinates, character coordinates, quote text, quote digest, and admitted evidence identity.
- Repository-backed stale-reference verification is exposed through `current_pole_refs` and `current_evidence_refs`; when supplied, exact object/revision/digest equality is required.
- The archive supplied for this execution did not expose `.git` metadata, so an exact repository commit SHA could not be captured from the supplied artifact.
- CAE control-state updates and the operator-gate decision were not modified because they are outside the two explicitly authorized implementation/test file paths.
