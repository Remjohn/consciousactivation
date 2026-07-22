# Video Editing Engine V1 Integration Mapping

## Canonical Boundary

```text
Composition decides what the scene is.
Avatar Performance decides how the character acts.
Video Editing decides when everything happens.
```

Video Editing Engine V1 consumes already-extracted, already-formatted, already-composed, and already-authorized scene programs. It does not own extraction, format doctrine, composition decisions, visual research, provider calls, or real rendering.

## Narrative Story Doctor Inputs

Narrative Story Doctor and Content Extraction Intelligence provide:

- source spans
- expression moments
- format extraction packets
- A-roll spine for Format 01
- proof inputs
- reaction inputs
- debate tension inputs

Video Engine stores these as source refs and timing/meaning inputs. It must not reinterpret interview meaning or invent new source facts.

## Format Intelligence Inputs

Format Intelligence provides authorized format programs:

- `Format01CinematicStoryProgram`
- `Format02AvatarPaperCutExplainerProgram`
- `Format03LivingCommentaryReactionProgram`
- `Format04ConsciousReactionEditingProgram`

It also provides sound, motion, memetic, style-route, render, and eval policies. Video Engine converts these into realization plans, timing plans, tracks, captions, sound cues, render contracts, and eval receipts.

## Composition Intelligence Inputs

Composition Intelligence provides:

- `CompositionSceneProgram`
- `Format02SceneProgram`
- `TextPlacementPlan`
- `TextRevealPolicy`
- `RealLifeCutoutPlacementPlan`
- `LayerPlan`
- `CognitiveLoadBudget`

Video Engine requires locked composition scene refs for Format 02 and preserves the cognitive-load budget. It must not move locked layout, rewrite locked text, or change avatar/composition intent.

## Avatar Performance Inputs

Avatar Performance Layer provides:

- `AvatarPerformancePlan`
- `AudienceProxyPerformancePlan`
- `AvatarRenderPayload`

Video Engine converts these into avatar/proxy tracks and timing. It requires no-lip-sync avatar references and rejects lip-sync-enabled avatar plans.

## Asset Intelligence Inputs

Asset Intelligence provides:

- materialized asset refs
- asset hashes
- rights/provenance receipts
- usage/fatigue records

Video Engine requires source asset sets and asset hashes for render contracts. Asset Intelligence remains the owner of source quality, rights, provenance, reuse, and fatigue logic.

## Render Runtime Later

Video Editing Engine V1 prepares render-facing contracts only:

- `RemotionInputProps`
- `OTIOAuditTimeline`
- `FFmpegFinishPlan`

V1 does not call Remotion or FFmpeg. Proxy and final render receipts are deterministic fake receipts. Real render execution belongs in a later adapter bundle.

## Non-Goals

- No extraction decisions
- No format doctrine decisions
- No composition decisions
- No visual research
- No provider calls
- No real Remotion calls
- No real FFmpeg calls
- No real render in V1
- No UI/API endpoints

