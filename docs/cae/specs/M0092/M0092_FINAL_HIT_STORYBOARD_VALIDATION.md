# M0092 — Final-Hit Storyboard Validation, Motion Plans and Keyframes

**Status:** `EXECUTION_COMPLETE_WITH_OPERATOR_BLOCKER`
**Authority lane:** CAE storyboard projection / deterministic validation
**Scope:** storyboard validation + MotionPlan/Keyframe compilation only

## Decision implemented

M0092 adds a deterministic final-hit projection layer over the existing CAE `StoryboardRevision`. It does not replace the canonical `EditorialStoryboard`, Semantic Program, Narrative Editing Grammar, Design System, Transformation, format-program, or runtime authorities.

The implementation validates, in one fail-closed pass:

- semantic purpose presence and deterministic purpose↔transformation-target alignment;
- source evidence lineage, approved asset state, rights status and source-quality lineage;
- explicit evidence-legibility observations for evidence-bearing visual elements in strict mode;
- canonical Design System reference shape and per-element reference consistency;
- format-program constraints through the existing storyboard-program authority;
- normalized geometry and harness safe-area containment;
- Narrative Editing Grammar registry sequence/harness binding;
- wrong-reading locks supplied by the caller, or resolved from the existing canonical `SemanticProgramRecord` by the store facade;
- MotionPlan timing continuity, keyframe span/order, harness keyframe count, motion intensity and attention budget;
- source-quality constraints before non-static motion.

The compiler derives typed fixed-point `Keyframe` objects from the existing governed `TransformationRecipe`. It computes a deterministic `MotionPlan` identity and compilation digest. The compile path is pure: it returns a projection artifact and does not mutate canonical storyboard state.

## Authority mapping

| Concern | Existing authority adopted | M0092 behavior | Class |
|---|---|---|---|
| Semantic storyboard | `packages/ca_runtime/src/ca_runtime/storyboard_session.py::StoryboardRevision` | Validate/project only | `EXECUTABLE` |
| Narrative grammar | `packages/ca_runtime/src/ca_runtime/narrative_editing_grammar.py::NarrativeEditingGrammarRegistry` | Reuse registry validation; no duplicate grammar | `REGISTRY_SOURCE` |
| Format constraints | `packages/ca_runtime/src/ca_runtime/storyboard_programs.py::get_storyboard_program` | Reuse native program validation | `EXECUTABLE` |
| Transformation | `packages/ca_runtime/src/ca_runtime/transformation_recipe.py::TransformationRecipeCompiler` | Reuse governed Intent→Recipe path | `EXECUTABLE` |
| Source quality | `packages/ca_runtime/src/ca_runtime/storyboard_session.py::validate_transformation_for_source_quality` | Reuse quality bounds; final-hit rejects out-of-bound recipes | `EXECUTABLE` |
| Semantic wrong-reading locks | `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py::SemanticProgramRecord.wrong_reading_locks` | Store facade resolves existing canonical locks when caller omits them | `REGISTRY_SOURCE` |
| Geometry | `packages/ca_runtime/src/ca_runtime/storyboard_programs.py` and existing CAE geometry conventions | Validate storyboard basis-point geometry and harness safe area | `EXECUTABLE` |
| Design System | No canonical DS registry was found in the inspected M65–M72/M0089/M0091 path | Require an explicit canonical `{object_id, version, sha256}` reference in strict final-hit calls; no competing DS authority created | `OPERATOR_DECISION_REQUIRED` |
| Attention cost | Existing doctrine treats salience cost as bounded decision math, not universal psychology | Deterministic benchmark: intensity + 250 bps per keyframe beyond two, capped at 10,000 | `HYPOTHESIS` |

## MotionPlan / Keyframe contract

`Keyframe` is a fixed-point model with millisecond timing and optional scale/position fields. `MotionPlan` now uses typed `Keyframe` entries and carries the originating recipe id and observed source-quality level when compiled.

Compilation rules are deterministic:

1. Use the existing governed `TransformationRecipe` when supplied; otherwise compile the existing `TransformationIntent` through M0083's registry.
2. Require source-quality evidence before non-static motion.
3. Convert recipe keyframe `at_bps` to milliseconds using integer fixed-point conversion.
4. Derive motion intensity from declared scale/motion amplitude.
5. Derive attention cost using the bounded benchmark rule above.
6. Require first keyframe at `0 ms` and final keyframe at shot duration with strictly increasing times.
7. Reject plans that exceed supplied harness limits.

The existing M0083 compiler now makes generated `REFRAME`, `ZOOM` and `SCALE` primitives numerically explicit so the existing M0084 source-quality validator can inspect the actual declared magnitude. This is a narrow compatibility correction at the existing Transformation Recipe seam, not a new authority.

## Harness contract

Strict final-hit validation requires:

- `max_motion_intensity_bps` in `[0, 2000]`;
- `max_attention_cost_bps` in `[0, 10000]`;
- a normalized `safe_area` `{x_bps, y_bps, width_bps, height_bps}`;
- a bound `StoryboardRevision.harness_id`;
- explicit Design System canonical reference;
- wrong-reading locks;
- Narrative Editing Grammar for every scene.

Optional harness fields are `max_keyframes`, `min_legibility_bps`, `require_design_system`, and `require_wrong_reading_locks`. Unknown harness keys fail closed.

## Evidence-first and wrong-reading rules

M0092 does not retrieve, generate, synthesize or replace visual evidence. It consumes already-linked CAE evidence and asset/source-quality records. It follows the existing evidence-first discipline by rejecting ungrounded assets and missing source-quality proof before allowing final-hit motion compilation.

A plausible-looking composition without source lineage is explicitly blocked by test coverage. Pixel-level legibility is not inferred from documentation or model output; strict mode requires an explicit observation field and records the absence as unproven.

Wrong-reading locks remain upstream semantic state. The store facade only reads them from the existing `SemanticProgramRecord`; it does not author or mutate them.

## External repository extraction

No external repository behavior was adopted for M0092. The implementation uses current CAE symbols only. Therefore no external URL, commit/tag or license was needed for behavioral extraction.

Excluded from M0092: external render/runtime reachability, new Design System registry creation, retrieval-system changes, VAE state changes, database migrations, operator feedback persistence changes, and perceptual/creative approval automation.

## Verification boundary

The automated tests establish deterministic contract behavior, rejection properties, source-quality bounds, geometry/safe-area checks, grammar/harness checks, semantic-target consistency, wrong-reading-lock requirements, and replay/idempotence.

They do **not** establish that a real rendered preview is semantically correct, that human attention cost has psychological validity, that a browser/native media runtime is reachable, or that the transformation is creatively acceptable. Those remain operator/runtime responsibilities.
