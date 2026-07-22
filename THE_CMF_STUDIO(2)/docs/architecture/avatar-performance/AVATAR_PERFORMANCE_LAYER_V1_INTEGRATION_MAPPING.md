# Avatar Performance Layer V1 Integration Mapping

## Canonical Input

Avatar Performance Layer V1 consumes locked Format 02 composition scene programs:

```text
Format02SceneProgram
-> Format02AvatarPerformanceAdapterService.compile_from_format02_scene(...)
```

The adapter preserves:

- `brand_id`
- `brand_context_version_id`
- `source_span_refs`
- primitive function
- SFL function
- scene role
- avatar action requirements
- audience proxy requirements

The adapter must not infer new claims, add lip sync, add phoneme or viseme behavior, call providers, or render assets.

## Canonical Output

The adapter emits:

- `AvatarPerformancePlan`
- `AudienceProxyPerformancePlan`
- `AvatarRenderPayload`

`AvatarRenderPayload` is a planning payload only. It is not final render output and it must not execute providers or rendering.

## Downstream Later

```text
AvatarPerformancePlan
-> Video Editing Engine scene timeline
-> Remotion avatar layer
-> optional Spine / DragonBones runtime bridge
-> final render later
```

The downstream Video Editing Engine should receive a locked performance plan and timeline payload. It should not own avatar meaning, primitive function, SFL function, or no-lip-sync doctrine.

## Format Usage

- Format 02: primary use. Avatar acts as guide, explainer, and concept mover. Audience proxy mirrors viewer state without mockery.
- Format 01: avatar minimal or off. If used, it should appear only as a small symbolic insert.
- Format 03: real coach or guest cutout remains primary. Avatar may appear only as a sticker, mascot, or annotation helper if justified.
- Format 04: avatar may act as scorekeeper, referee, or sidekick, but should not be the default speaker.
- SuperVisual and Carousel: avatar or audience proxy can be a visual anchor, but should not dominate the composition.

## Non-Goals

- No lip sync
- No phonemes
- No visemes
- No talking avatar
- No face morphing
- No provider calls
- No render calls
- No full animation runtime
- No Video Editing Engine implementation

