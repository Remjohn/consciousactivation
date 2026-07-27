---
tech_spec_id: "TS-CMF-113"
title: "2D Character Render Runtime, Evals, Approval, and Repair"
story_id: "7.29"
story_title: "2D Character Runtime, Evals, and Repair"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP 2D Character Animation Engine V1 bundle rendering and eval integration"
pipeline_stage: "10 / 11 / 12 / 13"
entry_object: "TwoDCharacterProgram, RenderPackage, EvaluationSpec, OperatorReviewCommand"
exit_object: "RigDebugPreview, PerformanceBlockingPreview, FinalCompositionPreview, CharacterRenderReceipt, CharacterRepairReceipt, ApprovedTwoDCharacterSceneProgram"
validation_contract: "render reproducibility, preview hierarchy, primitive/doctrine gates, source alignment, performance quality, technical quality, typed repairs, operator approval"
required_receipt: "CharacterRenderReceipt"
runtime_target: "Python / Pydantic v2 / Motion Canvas / Remotion / FFmpeg / object storage / PWA review / Telegram quick review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-113: 2D Character Render Runtime, Evals, Approval, and Repair

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 format. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/05_RENDERING_AND_REPRODUCIBILITY.md` | Defines embedded runtime, precomposed RGBA plate, Motion Canvas, Remotion, FFmpeg, reproducibility receipt, golden tests, and network isolation. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/06_EVALS_APPROVAL_AND_REPAIR.md` | Defines Character Genesis gates, per-program gates, preview hierarchy, typed repair commands, approval lifecycle, and receipt chain. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/eval_gates.json` | Machine-readable eval gate registry. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/repair_commands.json` | Machine-readable repair command registry. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Existing deterministic render dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-047-audio-caption-timeline-and-mix-assembly.md` | Audio, captions, timeline, and mix dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md` | Evaluation receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-053-approval-blockers.md` | Approval blocker dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | PWA/Telegram review surface dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval and approval workbench dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | Headless 2D frame renderer dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md` | Upstream `TwoDCharacterProgram` dependency. |

## 2. Overview

This spec makes the 2D character scene program executable, inspectable, repairable, and approvable. It owns render package creation, preview hierarchy, eval gates, typed repair commands, operator approval lifecycle, and reproducibility receipts for `TwoDCharacterProgram`.

The runtime supports two render modes:

| Mode | Use |
|---|---|
| `embedded_runtime` | Character runtime is evaluated inside Remotion for simpler scenes and exact subtitle/audio synchronization. |
| `precomposed_rgba_plate` | Motion Canvas or character runtime renders transparent frames/ProRes 4444 before final Remotion/FFmpeg composition. Useful for complex choreography and isolated debugging. |

The output of this spec is not merely a video file. It is an approved, receipt-backed character scene program that can be consumed by the broader video editing engine.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-109-001 | `TwoDCharacterProgram` | Immutable program with context refs, character refs, timebase, tracks, choreography, composition, finishing, evals, approval, and receipt data. |
| DEP-CMF-109-002 | `RigDebugPreview` | Shows bones, pivots, meshes, masks, weights, draw order, and attachment IDs. |
| DEP-CMF-109-003 | `PerformanceBlockingPreview` | Shows neutral background, transcript, beat name, acting state, gesture markers, gaze target, primitive target, and viseme labels. |
| DEP-CMF-109-004 | `FinalCompositionPreview` | Shows full scene, subtitles, audio, SFX, platform framing, and safe zones. |
| DEP-CMF-109-005 | `EvaluationSpec` | Runs source alignment, performance, primitive/doctrine, and technical gates. |
| DEP-CMF-109-006 | `CharacterRepairCommand` | Typed command that creates a new revision or version; approved versions remain immutable. |
| DEP-CMF-109-007 | `CharacterRenderReceipt` | Pins program hash, assets, sidecars, runtime versions, fonts, provider hashes, seeds, color profile, codec settings, and final outputs. |
| DEP-CMF-109-008 | `ApprovedTwoDCharacterSceneProgram` | Approved scene-program handoff consumed by composition and video editing systems. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/two_d_character.py` | Add preview, repair, receipt, and approval models. |
| `src/ccp_studio/services/two_d_character_render_service.py` | New service that packages render inputs, invokes render workers, and emits receipts. |
| `src/ccp_studio/services/two_d_character_eval_service.py` | New service that runs source, performance, primitive/doctrine, and technical gates. |
| `src/ccp_studio/services/two_d_character_repair_service.py` | New service that applies typed repair commands and creates program revisions. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Invokes Motion Canvas, Remotion, and render-worker jobs through existing deterministic render patterns. |
| `src/ccp_studio/services/audio_caption_timeline_service.py` | Supplies captions, mix, SFX, and audio timing for final previews and render. |
| `src/ccp_studio/services/review_workbench_service.py` | Exposes preview hierarchy, blockers, repair commands, and approval state to PWA/Telegram. |
| `src/ccp_studio/workflows/two_d_character_render_workflow.py` | New durable workflow for preview, eval, repair, approval, render, final QC, and archive. |

### ADR-05 Primitives

Every final approval must prove:

| Role | Required Proof |
|---|---|
| Meaning transform | Character performance expresses the source idea and approved expression moment. |
| Delivery shape | Gesture, gaze, mouth, props, subtitles, and camera support understanding. |
| Format material | PaperCut/avatar materiality, motion restraint, and layer depth fit the selected format. |

The system must block approval if primitive evidence is only attached at project level and not visible in the program, preview, or cue evidence.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Render cannot start unless program status, eval spec, assets, and operator state are valid. |
| Phase4-M02 Cinematic Meaning | Preview and eval must show source beat, meaning job, and primitive target per key cue. |
| Phase4-M04 Frictionless Block | Failed gates pause render and expose repair commands without deleting draft work. |
| Phase4-M05 Actionable Rejection | Every blocker maps to a typed repair command or explicit non-repairable reason. |
| Phase5-M01 Verifiable Artifact | Final output is reconstructable from program JSON, render package, runtime versions, command lines, hashes, and approval receipt. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Preview hierarchy is mandatory. | Operators need to debug rig, performance, and final composition separately. |
| Repairs are typed commands. | Freeform edits break reproducibility and make approvals unverifiable. |
| Approved programs are immutable. | Repair creates a revision; it does not mutate approved history. |
| Renderers run with pinned inputs and no outbound network. | Production must be deterministic and auditable. |
| FFmpeg owns finishing only. | It does not decide semantic timing, gestures, scene structure, or subtitles. |

### Gate Thresholds and Verdicts

Runtime, eval, approval, and repair gates use the source bundle `per_program` thresholds and add render-package completeness gates.

| Gate ID | Threshold | Hard Fail | Downstream Consequence |
|---|---:|---|---|
| `source_alignment` | 0.95 | Yes | Blocks final preview and render. |
| `lip_sync` | 0.86 | No | Below threshold creates `PROVISIONAL_LIP_SYNC_REVIEW`; final render requires repair or explicit operator rationale. |
| `beat_performance_match` | 0.82 | Yes | Blocks render approval. |
| `primitive_compliance` | 0.90 | Yes | Blocks render approval. |
| `doctrine_alignment` | 0.95 | Yes | Blocks render approval. |
| `motion_restraint` | 0.82 | No | Below threshold creates `PROVISIONAL_MOTION_RESTRAINT_REVIEW`; final render requires repair or explicit operator rationale. |
| `technical_render` | 1.00 | Yes | Blocks publish approval. |
| `render_package_completeness` | 1.00 | Yes | Blocks renderer invocation. |
| `reproducibility_receipt_completeness` | 1.00 | Yes | Blocks archive and publishing handoff. |

Verdict semantics are deterministic: hard-fail gates return `PASS` when `score >= threshold` and `FAIL` otherwise. Non-hard-fail gates return `PASS` when `score >= threshold`, `PROVISIONAL` when `threshold - 0.08 <= score < threshold`, and `FAIL` when below that provisional floor.

### Repair Command Versioning Rules

Repair commands inherit versioning behavior from `registries/repair_commands.json`.

| Command Family | Target | Requires New Rig Version |
|---|---|---|
| `MOVE_PIVOT` | `rig` | Yes |
| `REPAIR_MASK` | `layered_asset` | Yes |
| `REORDER_LAYER` | `rig` | Yes |
| `REPLACE_HAND_POSE` | `program` | No |
| `CHANGE_ACTING_STATE` | `program` | No |
| `REDUCE_GESTURE_AMPLITUDE` | `program` | No |
| `SHIFT_GESTURE_STROKE` | `program` | No |
| `CHANGE_GAZE_TARGET` | `program` | No |
| `REMAP_VISEME` | `program` | No |
| `CHANGE_COSTUME_SKIN` | `program` | No |
| `ATTACH_PROP` | `program` | No |
| `DETACH_PROP` | `program` | No |
| `REMOVE_MICRO_SEMIOTIC_ANCHOR` | `program` | No |
| `REDUCE_PAPER_JITTER` | `program` | No |
| `CHANGE_MIX_DURATION` | `program` | No |

Commands requiring a new rig version cannot patch an approved `CharacterRigVersion` in place. They create a new rig revision and invalidate any `TwoDCharacterProgram` whose `character_refs.rig_version_id` points to the superseded rig until recompilation or explicit compatibility validation passes.

## 4. Implementation Plan

1. Add contracts for `RigDebugPreview`, `PerformanceBlockingPreview`, `FinalCompositionPreview`, `CharacterRepairCommand`, `CharacterRepairReceipt`, `CharacterRenderReceipt`, and `ApprovedTwoDCharacterSceneProgram`.
2. Add render package builder that collects program JSON, assets, sidecars, fonts, captions, audio, seeds, renderer config, and output targets.
3. Add render mode selection: `embedded_runtime` or `precomposed_rgba_plate`.
4. Add eval service with source alignment, performance, primitive/doctrine, and technical gates.
5. Add preview generators for rig debug, performance blocking, and final composition preview.
6. Add typed repair command execution for pivot, mask, layer order, attachment, hand pose, acting state, gesture amplitude, gaze, viseme, costume, prop, MSA, paper jitter, and mix duration.
7. Add operator approval lifecycle: `draft`, `compiled`, `automatic_eval_failed`, `blocking_preview_ready`, `revision_requested`, `final_preview_ready`, `approved_for_render`, `rendering`, `rendered`, `final_qc`, `approved_for_publish`, `archived`.
8. Add reproducibility receipt with program hash, asset hashes, sidecar hashes, runtime versions, container digests, fonts, seeds, FPS rational, sample rate, color profile, codec settings, and final command lines.
9. Add review workbench read model for PWA and Telegram quick review.
10. Add golden tests that render selected frames and compare perceptual hashes and structured state snapshots.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class CharacterPreviewArtifact(BaseModel):
    schema_version: Literal["cmf.character_preview_artifact.v1"]
    preview_id: UUID
    program_id: UUID
    preview_type: Literal["rig_debug", "performance_blocking", "final_composition"]
    artifact_refs: list[str]
    frame_refs: list[str]
    generated_at: str
    blocker_codes: list[str]


class CharacterRepairCommand(BaseModel):
    schema_version: Literal["cmf.character_repair_command.v1"]
    command_id: UUID
    program_id: UUID
    command_type: Literal[
        "MOVE_PIVOT",
        "REPAIR_MASK",
        "REORDER_LAYER",
        "REPLACE_ATTACHMENT",
        "REPLACE_HAND_POSE",
        "CHANGE_ACTING_STATE",
        "REDUCE_GESTURE_AMPLITUDE",
        "SHIFT_GESTURE_STROKE",
        "CHANGE_GAZE_TARGET",
        "REMAP_VISEME",
        "CHANGE_COSTUME_SKIN",
        "ATTACH_PROP",
        "DETACH_PROP",
        "REMOVE_MICRO_SEMIOTIC_ANCHOR",
        "REDUCE_PAPER_JITTER",
        "CHANGE_MIX_DURATION",
    ]
    target_ref: str
    payload: dict
    reason: str
    operator_id: UUID | None = None


class CharacterRenderReceipt(BaseModel):
    schema_version: Literal["cmf.character_render_receipt.v1"]
    receipt_id: UUID
    program_id: UUID
    render_mode: Literal["embedded_runtime", "precomposed_rgba_plate"]
    program_json_hash: str
    asset_hashes: dict[str, str]
    sidecar_hashes: dict[str, str]
    character_runtime_version: str
    motion_canvas_version: str | None = None
    remotion_version: str
    ffmpeg_version: str
    font_hashes: list[str]
    provider_output_hashes: list[str]
    renderer_container_digest: str
    random_seeds: dict[str, str]
    output_refs: list[str]
    output_hashes: dict[str, str]
    eval_receipt_refs: list[str]
    operator_approval_ref: str
    blocker_codes: list[str]


class ApprovedTwoDCharacterSceneProgram(BaseModel):
    schema_version: Literal["cmf.approved_two_d_character_scene_program.v1"]
    approved_scene_program_id: UUID
    program_id: UUID
    program_hash: str
    character_render_receipt_ref: str
    approved_for_format: Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
    handoff_ref: str
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Rig debug preview fails | Block final preview with `RIG_DEBUG_PREVIEW_FAILED`. |
| Performance blocking preview fails | Allow repair; block final render with `PERFORMANCE_BLOCKING_PREVIEW_FAILED`. |
| Final preview fails primitive/doctrine gates | Block approval with `CHARACTER_PROGRAM_EVAL_FAILED`. |
| Motion Canvas unavailable for complex choreography | Use embedded runtime only if the program declares no Motion Canvas dependency; otherwise block. |
| Remotion unavailable | Block final render with `REMOTION_RENDERER_REQUIRED`. |
| FFmpeg finishing fails | Keep rendered video-only master and block publish with `FFMPEG_FINISHING_FAILED`. |
| Network access required during render | Block with `RENDER_NETWORK_ISOLATION_VIOLATION`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T109-01 | Add preview, repair, receipt, and approval contracts. |
| T109-02 | Add render package builder and render mode selector. |
| T109-03 | Add rig debug, performance blocking, and final composition previews. |
| T109-04 | Add eval service for source alignment, performance, primitive/doctrine, and technical gates. |
| T109-05 | Add typed repair command executor and repair receipts. |
| T109-06 | Add operator approval lifecycle and immutable revision behavior. |
| T109-07 | Add reproducibility receipt and render network isolation checks. |
| T109-08 | Add review workbench read model and Telegram quick review payload. |
| T109-09 | Add golden render tests and perceptual hash comparisons. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate |
|---|---|---|---|
| AC109-01 | Render cannot start unless program is compiled, assets exist, eval spec is present, and render package is complete. | Remotion runs with missing textures and no eval state. | Phase4-M01 |
| AC109-02 | Preview hierarchy exposes rig, performance, and final composition separately. | Operator only sees final MP4 and cannot diagnose bad pivots. | Phase4-M05 |
| AC109-03 | Failed evals produce actionable typed repair commands. | "Looks off" is returned with no target object or command. | Phase4-M05 |
| AC109-04 | Approved programs are immutable and repairs create revisions. | Operator changes gaze after approval without a new receipt. | Phase5-M01 |
| AC109-05 | Final render receipt pins program, assets, sidecars, versions, fonts, seeds, container digest, and command lines. | Output hash exists but renderer versions are unknown. | Phase5-M01 |
| AC109-06 | Renderers cannot reinterpret acting states or transcript meaning. | Remotion code replaces gaze targets based on layout convenience. | Phase4-M02 |

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `TS-CMF-043` | Internal | Deterministic Remotion and Motion Canvas rendering. |
| `TS-CMF-047` | Internal | Audio, caption, timeline, and mix assembly. |
| `TS-CMF-050` | Internal | Evaluation receipt generation. |
| `TS-CMF-053` | Internal | Approval blockers. |
| `TS-CMF-070` | Internal | Operator PWA and Telegram experience. |
| `TS-CMF-092` | Internal | Composition eval fixtures and approval workbench. |
| `TS-CMF-094` | Internal | Headless 2D frame renderer and avatar export worker. |
| `TS-CMF-112` | Internal | `TwoDCharacterProgram` compiler. |
| Motion Canvas | Renderer | Scene choreography, transparent plate rendering, diagrams, camera/object motion. |
| Remotion | Renderer | Final platform composition, subtitles, safe zones, audio refs, overlays. |
| FFmpeg | Finishing | Mux, loudness, music ducking, codec, derivatives, metadata verification. |

## 10. Testing Strategy

- Unit test render package completeness and missing asset blockers.
- Test embedded runtime and precomposed RGBA plate selection.
- Test rig debug preview for bones, pivots, meshes, masks, weights, draw order, and attachment IDs.
- Test performance blocking preview with transcript, beat, acting state, gesture markers, gaze target, primitive target, and viseme labels.
- Test final composition preview with subtitles, audio, SFX, platform framing, and safe zones.
- Test eval gates for source alignment, performance, primitive/doctrine, and technical failures.
- Test every repair command family with valid target, invalid target, and immutable approved version cases.
- Test render network isolation by denying outbound access and requiring all files in render package.
- Golden render selected frames for neutral rig, extreme arm bends, eye clipping, mouth shapes, costume switch, prop attach/detach, warp deform, PaperCut material, acting-state transitions, and one end-to-end reference asset.
