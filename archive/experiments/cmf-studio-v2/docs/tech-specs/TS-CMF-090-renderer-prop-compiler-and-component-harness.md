---
tech_spec_id: "TS-CMF-090"
title: "Renderer Prop Compiler and Component Harness"
story_id: "7.20"
story_title: "Renderer Prop Compiler"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and protocol repair"
pipeline_stage: "11 / 12"
entry_object: "CompositionRuntimeBinding, CompositionBeatMap, PaperCutRuntimeManifest, FrameSequenceManifest"
exit_object: "RendererPropsManifest, RendererComponentCompatibilityReport, RenderJob"
validation_contract: "typed props, component registry, deterministic render inputs, Geometrics/Skia compatibility, annotation cues, preview/final parity, hash stability"
required_receipt: "RendererPropsCompilationReceipt"
runtime_target: "Python / Pydantic v2 / TypeScript generated types / Remotion / Motion Canvas / Manim / FFmpeg / Skia CanvasKit / rough-notation-compatible annotation cues"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-090: Renderer Prop Compiler and Component Harness

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines the spec protocol, CBAR enforcement, and acceptance criteria format. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Identifies gaps around renderer worker, preview/final parity, and thin existing specs. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Requires deterministic render contracts, provider replaceability, SceneSpec reconstruction, and output traceability. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Existing render contract and deterministic output model to extend. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Current service owner for render job creation and validation. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Current render workflow that must remain the orchestration boundary. |
| `THE CMF STUDIO/generated/typescript/deterministic_renderer_props.ts` | Existing generated TypeScript prop pattern for renderer leaves. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Source of composition runtime binding and visual plan references. |
| `THE CMF STUDIO/src/ccp_studio/contracts/scene_spec.py` | Source of scene-level reproducibility data. |
| `THE CMF STUDIO/src/ccp_studio/contracts/assembly.py` | Source of audio, captions, and final assembly metadata. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Defines primitive triad obligations for renderer templates and motion templates. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\types.ts` | Legacy reference for Remotion manifest and frame export shape. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Legacy CVE/Geometrics source for SAM3, PRETEXT, 2D bin packing, Skia rendering, and Rough.js annotation aesthetics. |
| `THE CMF STUDIO/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Audit that repairs the missing Skia/SAM3/PRETEXT visual template spine. |
| `https://github.com/rough-stuff/rough-notation` | Reference for hand-drawn animated annotation cue types and sequencing. |

## 2. Overview

The Renderer Prop Compiler converts CMF product truth into deterministic renderer inputs. Remotion, Motion Canvas, Manim, FFmpeg, and headless 2D workers are execution targets; they do not decide the story, route, primitives, guest identity, timing, or approvals.

This spec defines:

- the renderer component registry;
- typed prop compilation from CMF contracts;
- compatibility checks before rendering;
- preview/final parity rules;
- generated TypeScript prop types;
- render job creation for Remotion, Motion Canvas, Manim, Skia/CanvasKit still visual rendering, and frame sequence assembly;
- rough-notation-compatible annotation cue propagation for cinematic and explainer text emphasis;
- blocker and receipt behavior.

This is also where open-source-inspired components become safe. A component can be imported or adapted only if it consumes typed CMF props, cannot read unscoped data, and passes deterministic preview/final tests.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-090-001 | `SceneSpec` | Supplies scene identity, route, platform, safe zones, and reconstruction refs. |
| DEP-CMF-090-002 | `CompositionRuntimeBinding` | Supplies selected template, visual plan, assets, brand substrate, and eval refs. |
| DEP-CMF-090-003 | `CompositionBeatMap` | Supplies exact duration, frame windows, captions, and cue tracks. |
| DEP-CMF-090-004 | `PaperCutRuntimeManifest` | Supplies paper-cut layer/motion/SFX cues when applicable. |
| DEP-CMF-090-005 | `FrameSequenceManifest` | Supplies pre-rendered 2D avatar or paper-cut frame assets from `TS-CMF-094`. |
| DEP-CMF-090-006 | `RendererComponentRegistry` | Defines allowed components, prop schemas, route compatibility, and renderer target. |
| DEP-CMF-090-007 | `RendererPropsManifest` | Canonical output consumed by TypeScript renderer code. |
| DEP-CMF-090-008 | `RenderJob` | Final deterministic render job passed to render workflow. |
| DEP-CMF-090-009 | `GeometricsLayoutPlan` | Supplies PRETEXT-measured text boxes, SAM3 safe zones, collision results, and absolute coordinates for Skia-capable visual templates. |
| DEP-CMF-090-010 | `TextAnnotationCueManifest` | Supplies transcript-timed underline, highlight, circle, box, strike-through, crossed-off, and bracket cues. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `deterministic_rendering.py` | Add component registry, props manifest, compatibility report, and render job refs. |
| `deterministic_rendering_service.py` | Compile props, validate compatibility, hash props, and create render jobs. |
| `render_workflow.py` | Refuse render job creation when props or compatibility checks fail. |
| `generated/typescript/deterministic_renderer_props.ts` | Regenerate renderer prop types from Pydantic contracts. |
| `composition.py` | Supplies runtime binding and template family information. |
| `assembly.py` | Supplies captions, audio, and final assembly references. |
| `doctrine_evaluation_service.py` | Validates primitive, doctrine, and route feel obligations before render. |

### ADR-05 Primitives

Renderer props must carry primitive evidence into render leaves. The renderer does not score primitives, but it must receive enough metadata for review and overlay debugging.

Required propagation:

| Prop Field | Purpose |
|---|---|
| `primitive_refs` | Shows which primitives justify the composition. |
| `primitive_role_map` | Proves meaning, delivery, and material roles are covered. |
| `eval_receipt_refs` | Links renderer output to doctrine and primitive checks. |
| `route_feel_contract_ref` | Prevents visual feel collapse across formats. |
| `source_evidence_refs` | Lets operators inspect transcript/source lineage from preview. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Props cannot compile without approved runtime binding, beat map, and eval receipts. |
| Phase4-M02 Cinematic Meaning | Props must include meaning-bearing cue metadata, not only layers and text. |
| Phase4-M04 Frictionless Block | Invalid components block with compatibility report before expensive rendering. |
| Phase4-M05 Actionable Rejection | Compatibility blockers include component ID, missing prop, schema path, and repair instruction. |
| Phase5-M01 Verifiable Artifact | Props, component version, assets, and output hashes must reconstruct preview and final output. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Renderer components are registered, not ad hoc imported. | Prevents drift, unsafe assets, and unreviewed open-source code paths. |
| Props are generated from Python contracts. | Keeps Python product truth authoritative while allowing TypeScript execution. |
| Preview and final render share the same props hash. | Operator approval must match final output. |
| Component compatibility is explicit. | Components must declare supported routes, formats, dimensions, fps, asset modes, and prop schema. |
| Pre-rendered frame sequences are first-class assets. | Paper-cut and avatar worker outputs must compose cleanly in Remotion/FFmpeg. |
| Skia/CanvasKit is a first-class renderer target. | Still visual content and precision typography layouts need deterministic geometry, masks, and text measurement rather than DOM screenshot rendering. |
| Annotation cues are typed data. | Rough hand-drawn emphasis must be transcript-timed and reproducible, not a loose frontend animation effect. |

## 4. Implementation Plan

1. Add `RendererComponentRegistration`, `RendererPropsManifest`, `RendererComponentCompatibilityReport`, and `RendererPropsCompilationReceipt`.
2. Add `renderer_component_registry_service.py` with route, format, platform, prop schema, and asset scope validation.
3. Extend `deterministic_rendering_service.py` with a `compile_renderer_props()` command.
4. Generate TypeScript prop types from Pydantic contracts.
5. Add component harness packages for Remotion, Motion Canvas, Manim, Skia/CanvasKit, and FFmpeg assembly.
6. Add open-source adapter gate: imported components must be wrapped by registered CMF components.
7. Add preview render command using same props hash as final render.
8. Add compatibility fixtures for all four video formats and negative fixtures for invalid prop, unsafe fetch, mismatched duration, and unregistered component.
9. Add `TextAnnotationCueManifest` support for rough-notation-compatible cues.
10. Add Skia compatibility checks for `GeometricsLayoutPlan` presence on still visual formats.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class RendererComponentRegistration(BaseModel):
    schema_version: Literal["cmf.renderer_component_registration.v1"]
    component_id: str
    renderer_target: Literal["remotion", "motion_canvas", "manim", "ffmpeg", "headless_2d", "skia_canvaskit"]
    component_version: str
    supported_route_codes: list[str]
    supported_format_codes: list[str]
    supported_dimensions: list[str]
    prop_schema_ref: str
    asset_scope_policy: Literal["sealed_packet_only", "object_storage_refs_only"]
    deterministic: bool


class RendererPropsManifest(BaseModel):
    schema_version: Literal["cmf.renderer_props_manifest.v1"]
    manifest_id: UUID
    workspace_id: UUID
    complete_editing_session_id: UUID
    composition_runtime_binding_id: UUID
    beat_map_id: UUID
    component_id: str
    renderer_target: str
    props_uri: str
    props_hash: str
    duration_frames: int
    fps: int
    width: int
    height: int
    asset_refs: list[str]
    frame_sequence_refs: list[str]
    geometrics_layout_plan_ref: str | None = None
    annotation_cue_refs: list[str] = []
    primitive_refs: list[str] = Field(min_length=3)
    primitive_role_map: dict[str, list[str]]
    eval_receipt_refs: list[str]
    blocker_codes: list[str]


class RendererComponentCompatibilityReport(BaseModel):
    schema_version: Literal["cmf.renderer_component_compatibility_report.v1"]
    report_id: UUID
    component_id: str
    props_manifest_id: UUID
    compatible: bool
    checked_schema_ref: str
    failures: list[dict]
    blocker_codes: list[str]


class RendererPropsCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.renderer_props_compilation_receipt.v1"]
    receipt_id: UUID
    props_manifest_id: UUID
    component_id: str
    input_hashes: dict[str, str]
    props_hash: str
    compatibility_report_ref: str
    preview_render_ref: str | None = None
    approved_for_render_job: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

Existing renderer props and TypeScript components may continue only if they are wrapped by a `RendererComponentRegistration` and pass compatibility validation. No renderer code may fetch guest assets, transcripts, or brand data directly.

| Condition | Fallback |
|---|---|
| Component unregistered | Block with `RENDERER_COMPONENT_NOT_REGISTERED`. |
| Props schema mismatch | Block with `RENDERER_PROPS_SCHEMA_INVALID`. |
| Unsupported route/format | Route to another registered component or block with `RENDERER_ROUTE_UNSUPPORTED`. |
| Frame sequence unavailable | Block animated/avatar route with `FRAME_SEQUENCE_REQUIRED`. |
| Preview/final props hash mismatch | Block final render with `PREVIEW_FINAL_PROPS_HASH_MISMATCH`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T090-01 | Add renderer component and props contracts. |
| T090-02 | Add component registry service with route, format, dimension, and asset-scope checks. |
| T090-03 | Extend deterministic rendering service with props compilation. |
| T090-04 | Generate TypeScript prop types from Pydantic contracts. |
| T090-05 | Build component harness entrypoints for Remotion and Motion Canvas first. |
| T090-06 | Add frame sequence composition support for `TS-CMF-094` outputs. |
| T090-07 | Add preview/final parity validation by props hash. |
| T090-08 | Add Skia/CanvasKit renderer target registration and compatibility validation. |
| T090-09 | Add rough-notation-compatible annotation cue propagation for cinematic and explainer text emphasis. |
| T090-08 | Add open-source adapter wrapping checks for imported components. |
| T090-09 | Add renderer compatibility and blocker receipts. |
| T090-10 | Add positive and negative fixtures for all four video formats. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC090-01 | Props cannot compile for unregistered renderer components. | A copied React video component renders production assets without registry entry. | Phase4-M01 |
| AC090-02 | Props include source, beat map, primitive, eval, route, and asset refs. | Renderer receives only text and image URLs. | Phase5-M01 |
| AC090-03 | Component compatibility report is required before render job creation. | Render job starts despite unsupported `SV-RRC` route. | Phase4-M04 |
| AC090-04 | Preview and final render use the same props hash. | Operator approves preview but final render uses modified props. | Phase5-M01 |
| AC090-05 | Renderer code cannot fetch unscoped assets or production DB data. | Remotion component calls `/api/guest/all-assets`. | Phase4-M01 |
| AC090-06 | Frame sequence refs from `TS-CMF-094` are supported for avatar and paper-cut routes. | Alpha avatar frames cannot be composed into final video. | Phase4-M02 |
| AC090-07 | Compatibility blockers identify component, schema path, and repair. | Error says "bad props" without field path. | Phase4-M05 |
| AC090-08 | Identical inputs produce identical props hash. | Same CES compiles different props ordering or cue IDs. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| SceneSpec and render contract | `TS-CMF-037` |
| Layer, animation, caption, and sonic plans | `TS-CMF-039` |
| Provider and render job receipts | `TS-CMF-042`, `TS-CMF-043`, `TS-CMF-048` |
| Audio/caption/timeline assembly | `TS-CMF-047` |
| Four video format runtime | `TS-CMF-078` |
| Composition runtime binding | `TS-CMF-080` |
| Beat map and cue compiler | `TS-CMF-084` |
| Paper-cut runtime | `TS-CMF-086` |
| Headless frame renderer | `TS-CMF-094` |
| Eval and approval workbench | `TS-CMF-092` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Component registration, props manifest, compatibility report, and receipt validation. |
| Registry tests | Unsupported route, dimension, fps, component, and asset policy failures. |
| Type generation tests | Python contracts regenerate TypeScript props and compile cleanly. |
| Determinism tests | Same inputs produce identical props hash and render job packet. |
| Preview/final tests | Final render blocked when preview props hash differs. |
| Security tests | Renderer components cannot fetch unscoped assets or call production APIs. |
| Fixture tests | Four positive format fixtures and negative fixtures for each blocker. |
| Integration tests | Props consume `TS-CMF-084`, `TS-CMF-086`, and `TS-CMF-094` outputs without manual JSON conversion. |
