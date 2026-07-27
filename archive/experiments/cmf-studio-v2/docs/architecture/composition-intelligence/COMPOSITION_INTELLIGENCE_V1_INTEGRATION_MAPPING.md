# Composition Intelligence V1 Integration Mapping

## Position In The Pipeline

Composition Intelligence sits after Format Intelligence and before preproduction, asset selection, style routing, provider planning, avatar performance, and video editing.

```text
Narrative Story Doctor / Extraction Intelligence
-> Format Intelligence
-> Composition Intelligence
-> Visual Preproduction
-> Asset Intelligence / Visual Research
-> Provider Composition Plate Contract
-> Reference Edit Contract
-> Avatar Performance Layer
-> Video Editing Engine
```

Composition Intelligence owns spatial meaning before editing begins. It decides layout, cognitive load, attention path, safe zones, text placement, avatar placement, audience proxy placement, real-life cutout role, layer plan, and provider edit boundaries. Video Editing later owns timing, motion, sound, final render, and timeline execution.

## Input Mapping

```text
Format02AvatarPaperCutExplainerProgram
-> Format02CompositionService.compile_scene_program(...)
```

Mapped inputs:

- `brand_id`
- `brand_context_version_id`
- `source_span_refs`
- `format_program_id`
- `teachable_mechanism_ref`
- `concept_node_refs`
- `diagram_sequence_ref`
- `avatar_clip_requirements`
- `sub_format_id`
- `frame_profile`

Composition defaults:

- Frame profile: `9:16_PAPERCUT_EXPLAINER`
- Scene concept: one teachable mechanism or one concept node.
- Headline: seven words or fewer where possible.
- Visible words: fourteen words or fewer by default.
- Avatar action: one action that serves the concept.
- Audience proxy: one proxy with an SFL function.
- Hero real-life object: one source-backed object.
- Negative space: at least 30%.

## Output Mapping

```text
Format02SceneProgram
-> Visual Preproduction
-> Asset Intelligence / Visual Research
-> ProviderCompositionPlateContract
-> ReferenceEditContract
-> Avatar Performance Layer later
-> Video Editing Engine later
```

`Format02SceneProgram` contains:

- `CompositionSceneProgram`
- `Format02ConceptUnit`
- `Format02VisualAction`
- `Format02ConceptMotionBudget`
- `Format02AvatarActionRequirement`
- optional audience proxy requirement
- optional real-life cutout requirement
- paper-card layout
- cognitive-load receipt

## Provider Contract Mapping

### Ideogram

Role: `composition_plate_generator`

Ideogram creates an approved paper-cut composition plate from a locked composition. It may create a paper-cut scene plate, rough typography preview, and placeholder object slots. It must preserve locked text, layout, avatar placement, source refs, and concept meaning.

Forbidden:

- rewrite locked text
- change locked layout
- invent claims
- add extra objects

### Flux

Role: `reference_based_object_editor`

Flux integrates real-life cutout references into the approved composition plate. It may replace placeholder objects, paperize the reference, harmonize lighting, and add contact shadow. It must not own composition meaning.

Forbidden:

- rewrite text
- move avatar
- change layout
- invent claims
- add extra objects

## Non-Goals

- No real provider calls.
- No Ideogram API calls.
- No Flux API calls.
- No image generation.
- No rendering.
- No timeline.
- No UI/API endpoints.
- No Avatar Performance runtime yet.
- No Video Editing Engine yet.
