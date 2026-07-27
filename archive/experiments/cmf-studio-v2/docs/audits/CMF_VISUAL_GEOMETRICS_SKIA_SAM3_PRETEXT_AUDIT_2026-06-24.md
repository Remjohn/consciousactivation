# CMF Visual Geometrics, Skia, SAM3, PRETEXT Audit

Date: 2026-06-24
Auditor: Codex / John PM support
Scope: Old `The Conscious Coaching Factory` visual rendering evidence, current CMF Studio specs, still-image visual template runtime, Skia/SAM3/PRETEXT/Qwen-layered pipeline, and rough-notation text animation requirement.

## 1. Executive Finding

Yes, the old `D:\Work\The Conscious Coaching Factory` documentation does contain the Skia/SAM3/PRETEXT visual rendering architecture Emilio remembered.

The current CMF Studio specs mention Ideogram 4, provider adapters, layer extraction, Remotion, Motion Canvas, and frame rendering, but they were still incomplete for the old CVE/Geometrics doctrine. The missing spine was:

```text
Ideogram 4 composition direction
-> Qwen-Image-Layered / layer extraction
-> SAM3 saliency, subject masks, text safe zones, and surface quadrilaterals
-> PRETEXT DOM-less typography measurement
-> 2D bin-packing and collision resolution
-> headless Skia rendering
-> vision scoring and operator approval
```

Without this repair, a developer could build attractive Remotion/Pixi templates while ignoring the original deterministic visual intelligence layer.

## 2. Sources Read

| Source | Evidence |
|---|---|
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Defines Capability Area 10: CVE/SVRE, Geometrics Pipeline, SAM 3 saliency, PRETEXT measurement, 2D bin packing, Skia rendering, Rough.js aesthetics, NIM variant scoring, VCB JSON, and Canvas Composition delivery. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_06_Conscious_Reactions.md` | Defines Conscious Reactions handoff to CMF/Skia and JSON mapping of spoken ranking decisions to deterministic visual render state. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\evolution_timeline.md` | Records the transition to mathematical coordinate-based layout via Skia CanvasKit, SAM 3, PRETEXT, and JSON-driven generative compositions. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\scene-presets.ts` | Legacy scene/format matrix for deterministic placement. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\frame_export_service.py` | Legacy frame and pose export job descriptors for transparent PNG output. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Current Ideogram bridge; missing explicit Geometrics handoff. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Current asset/layer extraction spec; missing first-class Qwen layered and SAM3 geometrics outputs. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Current renderer props spec; missing Skia as first-class renderer target and annotation cue payload. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | Current headless 2D worker spec; missing rough-notation/annotation cue support. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Enforces at least three primitive validations across meaning, delivery, and format/material roles. |
| `https://github.com/rough-stuff/rough-notation` | External library for animated hand-drawn annotations; useful for cinematic and explainer text emphasis when represented as deterministic renderer cues. |

## 3. Five-Lens Audit Flags

### FLAG 1

**[TS-CMF-088] | LENS 1 | SEVERITY: WARNING**

- **Finding:** The Ideogram bridge extracts layout plans but does not explicitly hand off to SAM3/PRETEXT/Geometrics/Skia.
- **Location:** Sections 2-4, Bridge Outputs and Boundary Rules.
- **Required Action:** Add a downstream Geometrics handoff rule that treats Ideogram as composition director, then requires structured decomposition before production rendering.

### FLAG 2

**[TS-CMF-089] | LENS 1/5 | SEVERITY: CRITICAL**

- **Finding:** The asset factory spec names generic segmentation but does not make Qwen-Image-Layered and SAM3 saliency outputs first-class objects consumed by layout resolution.
- **Location:** Sections 1-4, Purpose, Provider Roles, Primary Contracts, Rules.
- **Required Action:** Add Qwen-Image-Layered, SAM3, mask refs, safe zones, surface quadrilaterals, and extraction outputs required by the Geometrics runtime.

### FLAG 3

**[TS-CMF-090] | LENS 3/5 | SEVERITY: CRITICAL**

- **Finding:** Renderer props support Remotion/Motion Canvas/Manim/FFmpeg/headless 2D but omit Skia as a production renderer target for still visual templates and high-precision visual compositions.
- **Location:** Frontmatter, Section 2 Overview, Section 3 Technical Decisions, Section 5 Primary Output Schema.
- **Required Action:** Add Skia/CanvasKit as a registered renderer target, add `geometrics_layout_plan_ref`, and require renderer props to carry text annotation cue refs.

### FLAG 4

**[TS-CMF-094] | LENS 1/4 | SEVERITY: WARNING**

- **Finding:** The headless 2D worker covers paper-cut/avatar frame export but does not make rough hand-drawn annotation cues available to cinematic or explainer scenes.
- **Location:** Section 2 Overview, Section 4 Implementation Plan, Section 5 Schema.
- **Required Action:** Add `TextAnnotationCueManifest` references and renderer adapter support for rough-notation-compatible underline, highlight, circle, box, strike-through, crossed-off, and bracket cues.

### FLAG 5

**[MISSING SPEC] | LENS 1/5 | SEVERITY: CRITICAL**

- **Finding:** Still-image content formats have registry coverage but no full build-grade runtime spec for carousels, visual polls, tweet-like quotes, memes, and Super Visuals using the old Geometrics/Skia architecture.
- **Location:** Tech spec index after TS-CMF-094.
- **Required Action:** Add `TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md`.

## 4. Decision Log

### Decision 1 - Skia Remains The Deterministic Visual Renderer

Skia/CanvasKit should be retained for still visual templates and high-precision visual composition because the old CVE doctrine explicitly rejected DOM-bound visual rendering for production geometry. Remotion and Motion Canvas remain valid for video assembly, procedural animation, and preview/final video export, but still-image visual assets need the Skia path where exact text geometry, masks, collision, and coordinate receipts matter.

### Decision 2 - Ideogram 4 Is Composition Director, Not Final Renderer

Ideogram 4 should design composition, hierarchy, subject placement, prop density, and visual feel. Qwen-Image-Layered, SAM3, PRETEXT, Geometrics, and Skia convert that direction into editable, reproducible production artifacts. Ideogram output cannot become final baked text, final identity, or the only layout source.

### Decision 3 - Rough-Notation Is A Registered Annotation Cue, Not A Free DOM Effect

`rough-notation` is useful for cinematic and explainer text emphasis because it supports animated hand-drawn annotation styles. It must be represented as typed `TextAnnotationCue` JSON, bound to transcript frame ranges, primitive evidence, and renderer targets. Browser previews may use `rough-notation`; Skia/Motion Canvas/Remotion final renders must reproduce the same visual cue deterministically.

## 5. Required Revisions Executed

| Artifact | Revision |
|---|---|
| `TS-CMF-088` | Add downstream Geometrics handoff, Qwen layered, SAM3, PRETEXT, and Skia readiness rules. |
| `TS-CMF-089` | Add Qwen-Image-Layered, SAM3 saliency, segmentation mask refs, text safe zones, surface quadrilaterals, and Geometrics handoff blockers. |
| `TS-CMF-090` | Add Skia/CanvasKit renderer target, `geometrics_layout_plan_ref`, `annotation_cue_refs`, and rough-notation-compatible cue requirements. |
| `TS-CMF-094` | Add rough-notation-compatible text annotation cue support for paper-cut, explainer, and cinematic frame render jobs. |
| `TS-CMF-095` | Add full canonical Geometrics still visual composition runtime spec. |
| `README.md` | Register TS-CMF-095 in the dependency order and notes. |

## 6. Build Consequences If Not Repaired

- Still visual assets would remain "composition inspired" instead of mathematically reproducible.
- Carousels, polls, quote cards, memes, and Super Visuals could be rendered as generic templates instead of CMF visual intelligence outputs.
- Ideogram plates could be misused as final assets rather than layout direction.
- Qwen-layered and SAM3 would not produce the exact masks and safe zones needed by the solver.
- Text could collide with faces or critical objects because PRETEXT and bin-packing were not enforced.
- Rough annotation animations could be implemented as ad hoc frontend effects with no transcript timing or receipt trail.
- Primitive validation would remain separate from visual geometry instead of blocking weak compositions before render.

## 7. Audit Conclusion

The old Skia/SAM3/PRETEXT architecture was real and should be preserved in CMF Studio.

The corrected production path is:

```text
source expression
-> primitive triad
-> Ideogram 4 composition direction
-> Qwen/SAM3 layer and saliency extraction
-> PRETEXT typography measurement
-> Geometrics collision solver
-> Skia render
-> vision/eval receipt
-> operator approval
```

This audit blocks the previous specs from being treated as complete until the listed repairs are present.
