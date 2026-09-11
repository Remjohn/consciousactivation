# M0083 — Transformation Intent and Recipe System

## Status

`IMPLEMENTED — FOCUSED TESTS PASS — OPERATOR REVIEW REQUIRED`

M0083 extends the existing M0079 storyboard transformation objects with a
bounded deterministic projection layer. It does not create a second storyboard,
VAE, retrieval, semantic-program, Design System, or runtime authority.

## Authority basis

The dated CAE Visual Production Authority Pack was inspected at:

- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
- `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`

Authority source commit:
`de202244eb5b8e436685bf4e9ed02f93b6f5faa4`

The build plan establishes `TransformationIntent → TransformationRecipe →
primitive operations → MotionPlan/keyframes`, a compact editorial grammar, and
source-quality-aware transformation. The Visual Asset Studio requirements make
`intent`, `source`, `semantic_target`, `mode`, `emphasis`, `motion`, and
`constraints` the minimum TransformationIntent fields and require unknown
transformations to fail closed. Motion standards require deterministic control
of motion/keyframes and source-quality-aware reduction.

No external repository implementation was adopted for M0083, so there is no
external source license or upstream code mapping to record.

## Brownfield compatibility

The canonical brownfield object remains:

`Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`

Existing `StoryboardElement.transformation_intent` and
`StoryboardElement.transformation_recipe` fields remain the storage boundary.
M0079 payloads that encoded the editorial intent token in `mode` are normalized
at model validation time into explicit `intent` plus `mode=AUTO`.

The implementation uses `source_element_id` as the existing canonical storage
field and exposes `source` as its M0083 contract alias. This avoids introducing
a second source identity field or changing existing storyboard state shape.

## TransformationIntent contract

`TransformationIntent` now contains:

| Field | Purpose | Bound by M0083 |
|---|---|---|
| `intent_id` | Stable identity of the requested transformation | Required |
| `source_element_id` / `source` | Existing storyboard source-element identity | Required, non-empty |
| `intent` | Why the source should change | One of the 10 grammar intents |
| `semantic_target` | What meaning the transformation must make perceptible | Required, non-empty |
| `mode` | How the intent is expressed | Registered mode vocabulary |
| `emphasis` | Editorial emphasis level supplied upstream | Non-empty; not converted into an effects catalog |
| `motion` | Requested motion expression | Registered motion vocabulary |
| `constraints` | Source-quality and bounded execution limits | Strict key/value validation in compiler |

### Intent vocabulary

The compact grammar is:

`WITHHOLD, REVEAL, FOCUS, CONTRAST, PROVE, EXPLAIN, CONNECT, ESCALATE, INTERRUPT, RESOLVE`

These are editorial relationships, not visual effects.

### Mode vocabulary

`AUTO, EXTRACT_REGION, REFRAME, COMPARE, ANNOTATE, INSET, PROTECT, HOLD, RETURN, CUT`

### Motion vocabulary

`STATIC, SUBTLE_ZOOM, SUBTLE_PAN, RETURN`

`SUBTLE_PAN` is accepted as a bounded request but M0083 deliberately does not
invent geometry for it; exact positional solving remains downstream.

### Constraint vocabulary

The compiler accepts only:

- `source_quality`: `HIGH | MEDIUM | LOW | DEGRADED | UNKNOWN`
- `source_role`: `A_ROLL | B_ROLL | E_ROLL | DOCUMENT | PATTERN_INTERRUPT`
- `allow_motion`: boolean
- `max_scale_change_bps`: integer `0..2000`
- `max_motion_amplitude_bps`: integer `0..2000`

Unknown constraint keys fail closed.

## TransformationRecipe contract

`TransformationRecipe` remains the existing primitive/keyframe payload, with M0083
provenance fields added for governed compilation:

- `recipe_id`: deterministic digest-derived recipe identity
- `intent_id`: source TransformationIntent identity
- `primitives`: registered primitive operation payloads
- `keyframes`: deterministic keyframe payloads
- `constraints`: normalized and effective constraints
- `template_id`: registry recipe template identity
- `registry_version`: recipe registry version
- `motion_template`: compiled keyframe template
- `governed`: `true` only for registry-compiled recipes
- `recipe_sha256`: canonical recipe digest

A legacy recipe may still load through M0079-compatible storage, but M0083 does
not treat such a recipe as governed merely because its shape is valid.

## Recipe registry

Registry version: `M0083-1`

There are eight compact recipe templates covering all ten intents:

| Template | Intents | Modes | Primitives | Default motion |
|---|---|---|---|---|
| `REVEAL_TARGET_V1` | `REVEAL`, `PROVE` | `AUTO`, `EXTRACT_REGION` | `EXTRACT_REGION`, `HIGHLIGHT` | `SUBTLE_ZOOM` |
| `FOCUS_TARGET_V1` | `FOCUS`, `ESCALATE` | `AUTO`, `REFRAME` | `REFRAME`, `HIGHLIGHT` | `SUBTLE_ZOOM` |
| `CONTRAST_SOURCES_V1` | `CONTRAST` | `AUTO`, `COMPARE` | `SIDE_BY_SIDE`, `HIGHLIGHT` | `STATIC` |
| `EXPLAIN_TARGET_V1` | `EXPLAIN` | `AUTO`, `ANNOTATE` | `EXTRACT_REGION`, `ANNOTATE` | `STATIC` |
| `CONNECT_CONTEXT_V1` | `CONNECT` | `AUTO`, `INSET` | `INSET`, `CONNECTOR` | `STATIC` |
| `WITHHOLD_REGION_V1` | `WITHHOLD` | `AUTO`, `PROTECT` | `MASK_REGION` | `STATIC` |
| `INTERRUPT_CUT_V1` | `INTERRUPT` | `AUTO`, `CUT` | `CUT`, `HOLD` | `STATIC` |
| `RESOLVE_RETURN_V1` | `RESOLVE` | `AUTO`, `RETURN` | `RETURN`, `HOLD` | `RETURN` |

Approved primitive vocabulary is limited to:

`EXTRACT_REGION, REFRAME, HIGHLIGHT, SIDE_BY_SIDE, ANNOTATE, INSET, CONNECTOR, MASK_REGION, CUT, RETURN, HOLD`

The registry validates that every declared intent is represented and every
template uses only approved modes, motions, and primitives.

## Compilation rules

The compiler performs these bounded steps:

1. Reject a stale expected registry version.
2. Resolve the declared editorial intent to exactly one registered template.
3. Reject an intent/mode combination not explicitly approved by that template.
4. If an authorization allow-list is supplied, reject recipes outside it.
5. Validate constraint keys and bounded values.
6. Resolve requested motion from the intent, falling back to the template default
   only when the intent specifies `STATIC`.
7. Suppress motion when `allow_motion=false`.
8. Require explicit source quality before non-static motion.
9. Reduce `LOW` or `DEGRADED` sources to static presentation for zoom-capable
   templates; `HIGH` and `MEDIUM` sources receive bounded scale deltas.
10. Clamp scale by `max_scale_change_bps` where supplied.
11. Emit only registered primitive operations and deterministic keyframe templates.
12. Hash the canonical identity payload and derive a deterministic `recipe_id`.

No model output, arbitrary effect dictionary, free-form operation name, or
unregistered mode can bypass these checks.

## Determinism and replay

For identical intent, registry version, authorized recipe set, and normalized
constraints, compilation produces byte-for-byte-equivalent model data and the
same recipe digest/id. The test suite explicitly compiles the same intent twice
and compares the resulting model payloads.

## Contrastive safety case

A `FOCUS` intent with `COMPARE` mode is a plausible, polished-looking visual
because side-by-side comparison is a legitimate recipe elsewhere in the
registry. It is nevertheless semantically wrong for the declared intent. M0083
rejects this combination rather than inferring a different editorial meaning.

This is the intended distinction between “looks useful” and “is authorized for
the declared transformation intent.”

## Source-quality behavior

M0083 uses the compact source-quality classes required by the authority pack.
For zoom-capable recipes:

- `HIGH`: use the template's high-quality bounded scale delta.
- `MEDIUM`: use the smaller medium-quality bounded scale delta.
- `LOW` / `DEGRADED`: suppress zoom to static presentation.
- missing / `UNKNOWN`: fail closed before non-static motion.

The compiler does not claim perceptual validation. Geometry, safe-area, source
crop history, final composition, renderer fidelity, and operator visual quality
remain downstream validation concerns.

## Non-goals and explicit limits

M0083 does not:

- retrieve or select source media;
- determine semantic meaning upstream of `TransformationIntent`;
- solve final crop/BBOX geometry;
- create a visual asset editor UI;
- execute OpenChatCut, presentation, or other external runtimes;
- replace `MotionPlan` or `CompositionIR` authority;
- implement operator promotion or feedback persistence;
- prove perceptual correctness from unit tests;
- treat mocks or preview output as runtime evidence.

The resulting recipe is a governed projection object, not production approval.

## Evidence map

- **EXECUTABLE** — `packages/ca_runtime/src/ca_runtime/storyboard_session.py`
  and `packages/ca_runtime/src/ca_runtime/transformation_recipe.py` implement
  and bound the M0083 projection.
- **TEST** — `tests/cae/test_m0083_transformation_intent_recipe.py` covers all
  declared intents, deterministic replay, legacy normalization, mode mismatch,
  authorization, stale registry, source-quality gating, quality reduction,
  clamping, and malformed constraints.
- **DOCUMENT** — this specification records the implementation contract and
  limitations.
- **REGISTRY_SOURCE** — the dated Visual Production Authority Pack and M0078
  storyboard reference establish the editorial chain and compact grammar.
- **OPERATOR_DECISION_REQUIRED** — implementation is not a promotion or final
  visual/perceptual acceptance decision.


