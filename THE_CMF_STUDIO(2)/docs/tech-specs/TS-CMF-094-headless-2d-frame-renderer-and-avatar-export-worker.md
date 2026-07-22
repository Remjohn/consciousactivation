---
tech_spec_id: "TS-CMF-094"
title: "Headless 2D Frame Renderer and Avatar Export Worker"
story_id: "7.22"
story_title: "Headless 2D Renderer Worker"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "2D Animation Studio audit repair"
pipeline_stage: "11 / 12"
entry_object: "PaperCutRuntimeManifest, AnimationStudioSession, AnimationManifestPatch, CompositionBeatMap"
exit_object: "FrameRenderJob, FrameSequenceManifest, AvatarPoseExportManifest, RenderReceipt"
validation_contract: "headless deterministic frame rendering, alpha export, timing parity, rough annotation cues, receipt hashing"
required_receipt: "Headless2DFrameRenderReceipt"
runtime_target: "Python / Pydantic v2 / Node.js worker / PixiJS or Motion Canvas / Skia CanvasKit / rough-notation-compatible cues / FFmpeg / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-094: Headless 2D Frame Renderer and Avatar Export Worker

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Identifies the missing renderer worker as the major gap between contracts and operational animation output. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines required spec structure and acceptance criteria discipline. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Requires deterministic render contracts, reconstruction, scene reproducibility, and replaceable renderer adapters. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Existing render job and deterministic rendering authority. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Existing service to extend for frame job planning and receipt generation. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Current render workflow that the frame worker must plug into, not bypass. |
| `THE CMF STUDIO/generated/typescript/deterministic_renderer_props.ts` | Current generated TypeScript contract pattern for render props. |
| `THE CMF STUDIO/src/ccp_studio/contracts/rig_manifest.py` | Rig/layer/bone contract consumed by avatar frame rendering. |
| `THE CMF STUDIO/registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json` | Requires rig, paper-cut style, animation readiness, composition JSON, and lock receipts. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\frame_export_service.py` | Legacy reference for frame export concept; not complete enough to use as production runtime. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\bpm_service.py` | Legacy reference for beat grid calculations that can inform but not own CMF timing. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\lip_sync_service.py` | Legacy reference for mouth cue generation that must become CMF typed cue data. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\api\main.py` | Legacy API reference for worker endpoint shape. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Legacy CVE reference for Skia rendering, Rough.js aesthetics, and Geometrics visual constraints. |
| `THE CMF STUDIO/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Audit requiring rough annotation cues and Skia/SAM3/PRETEXT continuity. |
| `https://github.com/rough-stuff/rough-notation` | Reference for supported hand-drawn annotation cue types and ordered animation groups. |

## 2. Overview

The CMF Animation Studio can approve animation edits only if the system can render those edits into reproducible frames and video-ready assets. This spec defines the headless 2D worker that renders paper-cut avatar rigs, 2D explainer layers, reaction UI overlays, and upper-body guest/interviewer cutouts into deterministic frame sequences.

The worker is not the product brain. It is an execution leaf. Python creates the render job, validates source lineage, resolves assets, enforces doctrine and primitive gates, and records receipts. The Node/renderer worker receives a sealed job packet and returns frame manifests, hashes, and logs.

The worker must support:

- transparent alpha frame export for avatar overlays;
- full-frame paper-cut explainer scene rendering;
- rough-notation-compatible text annotation cues for cinematic and explainer beats;
- upper reaction UI plus lower human proof composition frames;
- pose sheet export for the 64-state acting library;
- preview keyframes for operator approval;
- final frame sequence generation for Remotion or FFmpeg assembly.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-094-001 | `PaperCutRuntimeManifest` | Provides layer order, material rules, motion recipe, SFX refs, and micro-semiotic anchors. |
| DEP-CMF-094-002 | `AnimationManifestPatch` | Applies approved operator edits before rendering. |
| DEP-CMF-094-003 | `CompositionBeatMap` | Provides exact frame windows for motion, captions, reaction UI, and cuts. |
| DEP-CMF-094-004 | `RigManifest` | Provides rig hierarchy, avatar states, hidden regions, and layer assets. |
| DEP-CMF-094-005 | `FrameRenderJob` | Sealed job packet sent to the headless renderer. |
| DEP-CMF-094-006 | `FrameSequenceManifest` | Lists exported frames, hashes, dimensions, alpha mode, and frame count. |
| DEP-CMF-094-007 | `AvatarPoseExportManifest` | Exports approved poses and expression states for reuse. |
| DEP-CMF-094-008 | `Headless2DFrameRenderReceipt` | Records worker version, inputs, outputs, validation, and failures. |
| DEP-CMF-094-009 | `TextAnnotationCueManifest` | Provides frame-timed underline, highlight, circle, box, strike-through, crossed-off, and bracket annotations. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `deterministic_rendering.py` | Add frame-worker job types and frame sequence outputs. |
| `deterministic_rendering_service.py` | Create sealed job packets, compute hashes, and validate returned manifests. |
| `render_workflow.py` | Enqueue frame worker jobs before final video assembly. |
| `rig_validation_service.py` | Reject jobs with invalid or unlocked rigs. |
| `doctrine_evaluation_service.py` | Reject jobs with doctrine hard failures. |
| `generated/typescript/deterministic_renderer_props.ts` | Generate matching TypeScript worker input types. |
| `TS-CMF-090` | Supplies annotation cue refs and renderer target compatibility for rough-notation-compatible effects. |

The worker may use PixiJS, Motion Canvas, or a small purpose-built canvas renderer. The selection must be hidden behind `FrameRendererAdapter`, because NFR-28 requires replaceable providers/renderers.

### ADR-05 Primitives

The worker MUST receive primitive validation state, not infer it. Required checks:

| Check | Rule |
|---|---|
| Minimum primitive count | At least three validated primitive refs must be present. |
| Role coverage | Meaning transform, delivery shape, and format material roles must be covered. |
| Route feel | `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC` must not share one generic style envelope. |
| Paper-cut materiality | Paper-cut scenes must include tactile paper/layer evidence, not flat poster output. |

Useful primitives include `PRM-VSG-020`, `PRM-VSG-008`, `PRM-PRS-032`, `PRM-PRS-025`, `PRM-VOC-007`, and `PRM-VSG-021`.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Worker refuses jobs without source lineage, locked Brand Context, validated primitives, and eval target. |
| Phase4-M02 Cinematic Meaning | Motion and frame export must preserve the declared narrative or teaching role of each beat. |
| Phase4-M04 Frictionless Block | Job can fail fast with actionable receipts instead of producing low-quality output. |
| Phase4-M05 Actionable Rejection | Every failed render returns blocker code, failed object ref, and repair hint. |
| Phase5-M01 Verifiable Artifact | Every frame sequence must be hashable and reconstructable from the sealed job packet. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Use sealed job packets. | Prevents renderer workers from reading unscoped data. |
| Render transparent alpha and full-frame outputs. | Needed for avatar overlays and complete paper-cut scenes. |
| Keep preview and final render on same adapter path. | Prevents approval drift between what Emilio sees and what the renderer exports. |
| Store frames in object storage with manifests. | Enables reconstruction and downstream Remotion/FFmpeg assembly. |
| Add worker version and renderer adapter hash to receipts. | Enables reproducibility audits and rollback. |
| Represent rough text emphasis as cue data. | Prevents text animation from becoming a non-reproducible browser effect disconnected from transcript timing. |

## 4. Implementation Plan

1. Extend deterministic rendering contracts with `FrameRenderJob`, `FrameRendererAdapter`, `FrameSequenceManifest`, `AvatarPoseExportManifest`, and `Headless2DFrameRenderReceipt`.
2. Add a Python service `headless_2d_frame_render_service.py` that validates objects and creates sealed worker packets.
3. Add generated TypeScript input types for the Node worker.
4. Implement an adapter interface with at least one concrete local adapter using PixiJS or Motion Canvas.
5. Implement frame export modes: `preview_keyframes`, `alpha_sequence`, `full_scene_sequence`, and `pose_sheet`.
6. Add FFmpeg handoff metadata: fps, duration, alpha mode, audio refs, caption refs, and assembly refs.
7. Add receipt hashing: sealed packet hash, frame list hash, output object URI hash, and worker log hash.
8. Add tests for determinism, alpha output, nonblank output, frame count, and failure receipts.
9. Add `TextAnnotationCueManifest` ingestion and deterministic rendering for underline, highlight, circle, box, strike-through, crossed-off, and bracket cues.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class FrameRendererAdapterRef(BaseModel):
    adapter_id: str
    adapter_version: str
    adapter_hash: str
    runtime: Literal["pixijs_node", "motion_canvas_node", "custom_canvas_node"]


class FrameRenderJob(BaseModel):
    schema_version: Literal["cmf.frame_render_job.v1"]
    job_id: UUID
    workspace_id: UUID
    complete_editing_session_id: UUID
    composition_runtime_binding_id: UUID
    paper_cut_runtime_manifest_id: UUID | None = None
    rig_manifest_id: UUID | None = None
    animation_manifest_patch_id: UUID | None = None
    beat_map_id: UUID
    renderer_adapter: FrameRendererAdapterRef
    mode: Literal["preview_keyframes", "alpha_sequence", "full_scene_sequence", "pose_sheet"]
    fps: int
    width: int
    height: int
    start_frame: int
    end_frame: int
    alpha: bool
    annotation_cue_refs: list[str] = []
    sealed_packet_uri: str
    sealed_packet_hash: str
    required_eval_receipt_refs: list[str] = Field(min_length=1)


class FrameSequenceManifest(BaseModel):
    schema_version: Literal["cmf.frame_sequence_manifest.v1"]
    manifest_id: UUID
    job_id: UUID
    frame_count: int
    fps: int
    width: int
    height: int
    alpha: bool
    frame_uri_pattern: str
    first_frame_hash: str
    last_frame_hash: str
    sequence_hash: str
    nonblank_pixel_ratio: float
    blocker_codes: list[str]


class AvatarPoseExportManifest(BaseModel):
    schema_version: Literal["cmf.avatar_pose_export_manifest.v1"]
    manifest_id: UUID
    rig_manifest_id: UUID
    acting_library_version: str
    pose_exports: list[dict]
    sprite_sheet_uri: str | None = None
    transparent_png_uris: list[str]
    export_hash: str


class Headless2DFrameRenderReceipt(BaseModel):
    schema_version: Literal["cmf.headless_2d_frame_render_receipt.v1"]
    receipt_id: UUID
    job_id: UUID
    adapter_ref: FrameRendererAdapterRef
    input_hashes: dict[str, str]
    output_manifest_ref: str
    output_hashes: dict[str, str]
    eval_receipt_refs: list[str]
    render_started_at: str
    render_finished_at: str
    status: Literal["succeeded", "blocked", "failed"]
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

If the headless renderer is unavailable, CMF may generate static approval previews from existing Composition JSON and rig thumbnails, but final video export MUST remain blocked. The system must not silently replace 2D animation with flat generated images.

| Condition | Fallback |
|---|---|
| Worker unavailable | Block final export with `HEADLESS_2D_WORKER_UNAVAILABLE`; show static preview only. |
| Alpha export unsupported | Block avatar overlay routes with `ALPHA_EXPORT_UNSUPPORTED`. |
| Frame count mismatch | Discard output and create `FRAME_SEQUENCE_COUNT_MISMATCH` receipt. |
| Nonblank check fails | Discard output and create `FRAME_SEQUENCE_BLANK_OUTPUT`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T094-01 | Add frame worker Pydantic contracts and generated TypeScript types. |
| T094-02 | Implement sealed packet builder with workspace scoping and hash generation. |
| T094-03 | Implement worker adapter interface and one local Node adapter. |
| T094-04 | Implement alpha sequence export for avatar overlays. |
| T094-05 | Implement full-scene sequence export for paper-cut explainers. |
| T094-06 | Implement preview keyframe export for operator review. |
| T094-07 | Implement pose sheet export for acting library and 64-state assets. |
| T094-08 | Add object storage write/read manifests and hash validation. |
| T094-09 | Add receipt generation for success, block, and failure. |
| T094-10 | Add tests for determinism, alpha, timing parity, and nonblank output. |
| T094-11 | Add rough-notation-compatible text annotation cue rendering and timing tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC094-01 | Identical sealed packets produce identical sequence hashes. | Same job produces different frame hashes on rerun. | Phase5-M01 |
| AC094-02 | Avatar overlay routes export transparent alpha frames. | Guest avatar exports with black background baked in. | Phase4-M02 |
| AC094-03 | Full-scene paper-cut routes preserve paper materiality and layer depth. | Output is a flat poster with no layer parallax or tactile evidence. | Phase4-M02 |
| AC094-04 | Worker blocks jobs without required eval receipts. | Renderer produces frames before primitive triad validation. | Phase4-M01 |
| AC094-05 | Frame count equals beat map duration for the requested range. | 450-frame beat renders 442 frames. | Phase5-M01 |
| AC094-06 | Nonblank visual checks run for preview and final sequences. | Final output is blank but marked succeeded. | Phase4-M04 |
| AC094-07 | Receipts include adapter version, input hashes, output hashes, and blocker codes. | A failed render log cannot be traced to the input packet. | Phase5-M01 |
| AC094-08 | Worker cannot read unscoped assets or production DB state. | Node worker fetches arbitrary guest assets by URL. | Phase4-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| Rig and creative library contracts | `TS-CMF-019`, `TS-CMF-020` |
| Complete Editing Session and render contract | `TS-CMF-036`, `TS-CMF-037` |
| Layer manifest and animation plan | `TS-CMF-039` |
| Beat map and timeline cues | `TS-CMF-084` |
| Paper-cut runtime manifest | `TS-CMF-086` |
| Animation Studio editor | `TS-CMF-093` |
| Renderer props and component harness | `TS-CMF-090` |
| Doctrine eval harness | `TS-CMF-077`, `TS-CMF-092` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Valid and invalid frame jobs, manifests, adapter refs, and receipts. |
| Determinism tests | Same packet, same adapter, same asset hashes produce identical sequence hash. |
| Alpha tests | Transparent pixel samples prove overlay export is actually alpha-capable. |
| Timing tests | Frame ranges match `CompositionBeatMap` exactly. |
| Nonblank tests | Pixel checks reject blank or fully transparent output. |
| Fixture tests | One paper-cut explainer, one avatar overlay, one reaction composition, one pose sheet. |
| Failure tests | Missing eval receipts, invalid rig, missing asset, and adapter failure produce blocker receipts. |
| Integration tests | Frame output can be consumed by `TS-CMF-090` or final Remotion/FFmpeg assembly without timing drift. |
