---
tech_spec_id: "TS-CMF-084"
title: "Transcript Beat Map and Timeline Cue Compiler"
story_id: "7.14"
story_title: "Transcript Beat Map Compiler"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and protocol repair"
pipeline_stage: "9 / 10 / 11"
entry_object: "AlignedTranscriptSegment, ExpressionMoment, InterviewAssetContract, CompleteEditingSession"
exit_object: "CompositionBeatMap, TimelineCueManifest, BeatMapCompilationReceipt"
validation_contract: "timestamp alignment, frame conversion, source evidence, speaker binding, cue coverage"
required_receipt: "BeatMapCompilationReceipt"
runtime_target: "Python / Pydantic v2 / FFmpeg metadata / Remotion props / Motion Canvas props"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-084: Transcript Beat Map and Timeline Cue Compiler

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines mandatory CMF/ERA3 spec sections and acceptance criteria requirements. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Identifies timing, transcript, lip-sync, and render-worker gaps that this spec must close. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Requires scene reproducibility, source timestamp traceability, transcript segment binding, and render contract generation. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Establishes interview-first expression capture as the source of downstream content, not generic script generation. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Requires expression moment boundaries, routing updates, and transcript-grounded extraction. |
| `THE CMF STUDIO/src/ccp_studio/contracts/scene_spec.py` | Existing scene contract that receives beat map references. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Existing composition contract that must bind to timed cue manifests. |
| `THE CMF STUDIO/src/ccp_studio/contracts/assembly.py` | Existing assembly contract for captions, audio, and timeline outputs. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Existing render contract that consumes exact duration, fps, and renderer props. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Requires primitive-triad evidence on composition targets including `SceneSpec`, `CompositionJob`, and renderer templates. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\bpm_service.py` | Legacy reference for beat-grid and tempo calculations. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\services\lip_sync_service.py` | Legacy reference for mouth-shape timing, to be adapted into CMF typed cue data. |

## 2. Overview

The Transcript Beat Map compiler is the bridge between the real interview and the exact visual/audio timeline. CMF is interview-first: a scene exists because a guest said, paused, reacted, contradicted, remembered, taught, or revealed something in a source artifact. This compiler turns that source evidence into frame-accurate beats that downstream composition, paper-cut animation, reaction UI, subtitles, SFX, and renderers can obey.

This spec prevents the video system from behaving like generic short-form automation. Every cue must answer:

- Which transcript segment or word timing caused this cue?
- Which speaker owns the cue?
- Which expression moment or interviewer question created the scene?
- Which route and format does the cue serve?
- Which primitive or doctrine obligation does the cue support?
- Which renderer can execute it without changing product truth?

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-084-001 | `InterviewAssetContract` | Provides source recording, transcript, speaker labels, consent, and source lineage. |
| DEP-CMF-084-002 | `AlignedTranscriptSegment` | Provides word, sentence, pause, and speaker timestamps. |
| DEP-CMF-084-003 | `ExpressionMoment` | Defines approved source boundaries and extraction meaning. |
| DEP-CMF-084-004 | `CompleteEditingSession` | Scopes beat map to guest, workspace, route, format, and selected output. |
| DEP-CMF-084-005 | `CompositionTemplateFamily` | Defines expected cue families for cinematic, explainer, challenger, and reaction outputs. |
| DEP-CMF-084-006 | `SceneSpec` | Receives beat map refs for reproducible scene construction. |
| DEP-CMF-084-007 | `AnimationPlan` | Receives motion, mouth, gesture, camera, and SFX cue windows. |
| DEP-CMF-084-008 | `RendererPropsManifest` | Receives exact duration, fps, captions, layer cues, and frame windows. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `contracts/scene_spec.py` | Add `beat_map_id`, `timeline_cue_manifest_id`, `source_timestamp_range_ms`, and `source_alignment_confidence`. |
| `contracts/composition.py` | Bind `CompositionJob` and `CompositionRuntimeBinding` to cue manifests. |
| `contracts/assembly.py` | Consume caption groups, audio cue refs, and cut instructions. |
| `contracts/deterministic_rendering.py` | Consume duration frames, fps, safe zones, cue manifests, and props references. |
| `services/doctrine_evaluation_service.py` | Evaluate route/cue integrity before renderer handoff. |
| `workflows/render_workflow.py` | Enforce beat map existence before render jobs are created. |

### ADR-05 Primitives

Beat maps are not just timing data. They must preserve the reason a scene exists. The compiler MUST carry primitive obligations from the approved source route into cue targets.

| Route | Minimum Primitive Coverage |
|---|---|
| Cinematic Story Commentary | `PRM-PRS-009`, `PRM-PRS-002`, `PRM-VOC-009`, `PRM-VSG-021` |
| Educational / Explainer | `PRM-HUM-025`, `PRM-PRS-032`, `PRM-PRS-025`, `PRM-VSG-020` |
| Challenger / Frame Breaker | `PRM-PRS-015`, route-specific proof primitives, and safe confrontation checks. |
| Reaction / Recognition Clip | Human-proof, emotional-recognition, and timing authenticity primitives. |

Every beat map MUST expose at least three validated primitive refs across meaning, delivery, and material roles or downstream approval fails with `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Beat map cannot compile without approved source lineage and expression boundary. |
| Phase4-M02 Cinematic Meaning | Beat types must encode the meaning job, not only visual timing. |
| Phase4-M03 Inline Routing SLA | Route and format must be selected before cue family compilation. |
| Phase4-M04 Frictionless Block | Missing transcript, speaker, or timestamp evidence blocks renderer handoff. |
| Phase4-M05 Actionable Rejection | Each blocker must identify the missing segment, timestamp, cue type, or primitive role. |
| Phase5-M01 Verifiable Artifact | Beat maps must be hashable and reconstructable from source alignment data. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Use frame ranges as the canonical renderer boundary. | Remotion, Motion Canvas, and frame workers need exact frames, not vague seconds. |
| Preserve transcript milliseconds in every cue. | Operators must trace each visual event back to source evidence. |
| Separate semantic beat from renderer cue. | One meaning beat can generate captions, camera movement, paper-cut motion, SFX, and UI cues. |
| Include guest and interviewer tracks. | Reaction and recognition clips often depend on interaction, not just guest monologue. |
| Treat lip-sync as derived cue data. | Mouth cues are generated from source audio/transcript but must be editable through receipts. |

## 4. Implementation Plan

1. Add `CompositionBeat`, `TimelineCue`, `TimelineCueManifest`, and `BeatMapCompilationReceipt` contracts.
2. Add `transcript_beat_map_service.py` to compile source segments into semantic beats.
3. Add route-specific cue compilers for `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC`.
4. Add speaker-aware cue tracks: guest, interviewer, overlay UI, caption, SFX, camera, paper-cut layer, avatar mouth, avatar gesture.
5. Add frame conversion utility: `ms_to_frame`, `frame_to_ms`, `snap_to_word_boundary`, `snap_to_pause_boundary`.
6. Add source evidence refs for every cue.
7. Add blockers for missing timestamps, speaker ambiguity, invalid boundaries, and primitive role gaps.
8. Add read model for the operator timeline in `TS-CMF-093`.
9. Add tests with real-like transcript fixtures containing interruption, pause, emotional beat, teaching beat, and debate beat.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SourceTimestampRange(BaseModel):
    start_ms: int
    end_ms: int
    start_word_index: int | None = None
    end_word_index: int | None = None
    source_evidence_ref: str


class CompositionBeat(BaseModel):
    schema_version: Literal["cmf.composition_beat.v1"]
    beat_id: UUID
    beat_type: Literal[
        "hook",
        "question",
        "guest_reaction",
        "interviewer_reaction",
        "memory_image",
        "concept_reveal",
        "contrast",
        "proof_reveal",
        "challenge",
        "recognition",
        "cta",
    ]
    speaker: Literal["guest", "interviewer", "audience", "system"]
    source_range: SourceTimestampRange
    start_frame: int
    end_frame: int
    semantic_summary: str
    primitive_refs: list[str] = Field(min_length=1)


class TimelineCue(BaseModel):
    schema_version: Literal["cmf.timeline_cue.v1"]
    cue_id: UUID
    beat_id: UUID
    cue_type: Literal[
        "caption",
        "layer",
        "sfx",
        "music",
        "camera",
        "cut",
        "reaction_ui",
        "human_subject",
        "avatar_mouth",
        "avatar_gesture",
        "paper_prop",
    ]
    track_id: str
    start_frame: int
    end_frame: int
    source_range: SourceTimestampRange
    renderer_payload: dict
    eval_obligation_refs: list[str]


class CompositionBeatMap(BaseModel):
    schema_version: Literal["cmf.composition_beat_map.v1"]
    beat_map_id: UUID
    complete_editing_session_id: UUID
    expression_moment_id: UUID
    interview_asset_contract_id: UUID
    route_code: str
    format_code: str
    fps: int
    duration_frames: int
    beats: list[CompositionBeat]
    cues: list[TimelineCue]
    caption_manifest_ref: str | None = None
    source_alignment_confidence: float
    primitive_refs: list[str]
    blocker_codes: list[str]


class BeatMapCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.beat_map_compilation_receipt.v1"]
    receipt_id: UUID
    beat_map_id: UUID
    input_hashes: dict[str, str]
    output_hash: str
    alignment_warnings: list[str]
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

If legacy BPM or lip-sync services are used during migration, they may only produce draft cue suggestions. CMF Python contracts remain authoritative.

| Condition | Fallback |
|---|---|
| Word-level timestamps missing | Use segment timestamps and block mouth/lip-sync export with `WORD_TIMESTAMPS_REQUIRED_FOR_LIPSYNC`. |
| Speaker labels ambiguous | Compile draft beats but block approval with `SPEAKER_LABEL_AMBIGUOUS`. |
| Existing interview video has no interviewer track | Permit guest-only reaction route only if route contract allows it. |
| Beat alignment confidence below threshold | Require operator review in `TS-CMF-093`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T084-01 | Add Pydantic contracts for beat, cue, beat map, cue manifest, and receipt. |
| T084-02 | Implement source-aligned beat map compiler service. |
| T084-03 | Implement route-specific cue rules for four canonical video formats. |
| T084-04 | Implement speaker-aware track generation for guest and interviewer. |
| T084-05 | Implement lip-sync and mouth cue suggestion from transcript/audio evidence. |
| T084-06 | Implement caption grouping and safe-zone timing payloads. |
| T084-07 | Implement blocker generation and actionable repair metadata. |
| T084-08 | Add operator read model for beat timeline preview. |
| T084-09 | Add regression fixtures based on CCP V9/V9.1 interview-first flows. |
| T084-10 | Add integration tests with SceneSpec, AnimationPlan, and RendererPropsManifest compilation. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC084-01 | Every beat has transcript source timestamps and evidence ref. | A "hook" beat exists with no source segment. | Phase5-M01 |
| AC084-02 | Every cue has frame start/end and renderer payload. | A caption cue has milliseconds but no frame range. | Phase4-M02 |
| AC084-03 | Beat map blocks renderer handoff if speaker labels are ambiguous. | Guest and interviewer cues are swapped silently. | Phase4-M04 |
| AC084-04 | Route-specific cue families differ across the four formats. | Cinematic and poll reaction clips receive identical cue tracks. | Phase4-M03 |
| AC084-05 | Lip-sync cues are blocked when word-level timing is missing. | Mouth shapes are guessed from sentence text only. | Phase4-M01 |
| AC084-06 | At least three primitive refs are present across required roles. | Explainer beat map uses only a style primitive. | Phase4-M01 |
| AC084-07 | Operator repair instructions identify failed segment, cue, or primitive role. | Error says "timing invalid" with no timestamp. | Phase4-M05 |
| AC084-08 | Rerunning the compiler on identical inputs produces identical beat map hash. | Same transcript produces different cue IDs or frame ranges. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| Source ingestion and transcript alignment | `TS-CMF-030` |
| Expression moment boundaries | `TS-CMF-031`, `TS-CMF-032` |
| Route and asset derivative selection | `TS-CMF-033`, `TS-CMF-034` |
| Complete Editing Session | `TS-CMF-036` |
| SceneSpec and render contract | `TS-CMF-037` |
| Layer, animation, captions, and sonic plans | `TS-CMF-039` |
| Four video format runtime | `TS-CMF-078` |
| Animation Studio timeline | `TS-CMF-093` |
| Renderer prop compiler | `TS-CMF-090` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Valid and invalid beats, cues, beat maps, and receipts. |
| Source alignment tests | Frame ranges match transcript milliseconds at multiple fps values. |
| Speaker tests | Guest, interviewer, and interaction cues are routed correctly. |
| Route tests | Four video formats produce distinct cue families and blockers. |
| Lip-sync tests | Mouth cues require word-level timing and audio availability. |
| Primitive tests | Missing minimum count and missing role coverage create hard blockers. |
| Determinism tests | Same input hashes produce same beat map hash. |
| Integration tests | Beat map drives `TS-CMF-086`, `TS-CMF-090`, `TS-CMF-093`, and `TS-CMF-094` without timing drift. |

