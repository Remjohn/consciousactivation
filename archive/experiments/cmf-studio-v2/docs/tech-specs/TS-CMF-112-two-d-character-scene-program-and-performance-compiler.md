---
tech_spec_id: "TS-CMF-112"
title: "2D Character Scene Program and Performance Compiler"
story_id: "7.28"
story_title: "2D Character Performance Compiler"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP 2D Character Animation Engine V1 bundle performance compiler integration"
pipeline_stage: "7 / 8 / 9 / 10 / 11"
entry_object: "BrandContextVersion, InterviewBrief, InterviewAssetContract, TranscriptBeatMap, ExpressionMoment, CharacterRigVersion, PerformanceLibraryVersion, SceneTemplate, FormatTarget"
exit_object: "TwoDCharacterProgram, CharacterPerformanceCompilerReceipt"
validation_contract: "interview source alignment, integer timebase, beat-to-state mapping, gesture/gaze/face/viseme planning, primitive compliance, doctrine compatibility, operator-ready preview"
required_receipt: "CharacterPerformanceCompilerReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / Pi Command Bus / generated TypeScript contracts / Motion Canvas / Remotion"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-112: 2D Character Scene Program and Performance Compiler

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec format. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/01_MASTER_SPEC.md` | Defines Performance Compilation and `TwoDCharacterProgram`. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/04_PERFORMANCE_COMPILER.md` | Defines DSPy modules, candidate retrieval, beat-to-state mapping, gesture, gaze, face, viseme, prop, transition, and evaluation stages. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/models/two_d_character_models.py` | Defines canonical program model: timebase, context refs, character refs, rig manifest, performance library, transcript alignment, performance tracks, choreography, Remotion composition, finishing, evals, approval, receipt. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/examples/example_two_d_character_program.json` | Example scene program fixture. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Source doctrine for interview-first expression extraction and scene source binding. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Source doctrine for expression capture, routing, and approved moment boundaries. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-027-interview-asset-contract-and-quality-gate.md` | Interview Asset Contract dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-031-anchor-hit-and-expression-moment-candidate-detection.md` | Expression Moment candidate dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-032-expression-moment-review-and-boundary-control.md` | Approved Expression Moment boundary dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Canonical four video format routing. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md` | Transcript-to-frame and beat map dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-085-64-state-acting-and-avatar-performance-selector.md` | Acting/avatar state selection dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md` | Character object model dependency. |

## 2. Overview

`TwoDCharacterProgram` is the canonical scene program for 2D avatar and PaperCut performances. It is not a render preset and not a prompt. It is an immutable, transcript-timed, character-aware program compiled from structured interview context and approved character infrastructure.

The compiler path is:

```text
Brand Context
+ Interview Brief
+ Interview Asset Contract
+ Transcript Beat Map
+ Expression Moments
+ Voice/Visual DNA
+ primitive and doctrine bundles
+ CharacterRigVersion
+ PerformanceLibraryVersion
+ SceneTemplate
+ FormatTarget
-> BeatMeaningAnalyzer
-> EmotionCurveCompiler
-> PrimitivePerformanceMapper
-> ActingStateRetriever
-> GesturePlanner
-> GazePlanner
-> FacialPosePlanner
-> VisemePlanner
-> PropAndAnchorPlanner
-> TransitionPlanner
-> PerformanceEvaluator
-> TwoDCharacterProgramAssembler
-> TwoDCharacterProgram
```

The Educational / Explainer format uses this program as a primary scene engine. Other formats may consume it as a supporting scene element:

| Video Format | Character Scene Program Role |
|---|---|
| Cinematic Story Commentary | Optional memory-object or symbolic PaperCut insert; restrained and source-bound. |
| Educational / Explainer | Primary PaperCut / 2D Avatar scene program. |
| Challenger / Frame Breaker | Optional debate-card, ranking, quiz, or character emphasis layer; must not override reaction edit grammar. |
| Reaction / Recognition Clip | Optional animated emphasis, prop, or upper-body avatar moment when live footage is unavailable or intentionally stylized. |

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-108-001 | `ContextRefs` | Pins brand, interview brief, interview asset contract, expression session, transcript beat map, expression moments, DNA, primitive bundle, doctrine bundle, asset package, scene template, and format target. |
| DEP-CMF-108-002 | `CharacterRefs` | Pins identity pack, art version, layered asset version, rig version, performance library, acting library, costume skin, and micro-semiotic anchor skins. |
| DEP-CMF-108-003 | `Timebase` | Uses integer ticks, FPS rational, audio sample rate, and duration ticks. Floating seconds are not production truth. |
| DEP-CMF-108-004 | `TranscriptAlignment` | Stores word, phoneme, viseme, alignment confidence, and manual repairs. |
| DEP-CMF-108-005 | `PerformanceTrack` | Stores cue tracks for acting states, body, face, gaze, hands, props, visemes, camera, and scene objects. |
| DEP-CMF-108-006 | `MotionCanvasChoreography` | Stores scene-level camera, object paths, character placement, and deterministic seed. |
| DEP-CMF-108-007 | `RemotionComposition` | Stores final composition dimensions, FPS, duration, character render mode, subtitles, background, safe zones, audio refs, and seed. |
| DEP-CMF-108-008 | `EvaluationSpec` | Declares gates and thresholds before render. |
| DEP-CMF-108-009 | `CharacterPerformanceCompilerReceipt` | Records compiler stages, selected states, rejected candidates, evals, hashes, and blockers. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/two_d_character.py` | Add `TwoDCharacterProgram` and related submodels, or generate them from the CMF schema source. |
| `src/ccp_studio/services/two_d_performance_compiler_service.py` | New service that runs DSPy stages and assembles the program. |
| `src/ccp_studio/dspy/two_d_character_compiler.py` | New DSPy module set for beat meaning, emotion curve, primitive performance mapping, state retrieval, gesture, gaze, face, viseme, prop, transition, and evaluation. |
| `src/ccp_studio/services/transcript_beat_map_service.py` | Supplies transcript beat map and frame/tick mapping from `TS-CMF-084`. |
| `src/ccp_studio/services/expression_moment_service.py` | Supplies approved expression moments and source boundaries. |
| `src/ccp_studio/services/acting_state_selection_service.py` | Supplies candidate acting states and transition constraints. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Runs primitive and doctrine gates before program assembly. |
| `src/ccp_studio/contracts/deterministic_rendering.py` | Receives `TwoDCharacterProgram` refs for downstream renderer prop compilation. |

### ADR-05 Primitives

Every program must express at least three primitives:

| Role | Program Obligation |
|---|---|
| Meaning transform | The selected acting and scene cues must express the approved source idea, not a generic performance. |
| Delivery shape | Gesture, gaze, pause, face, subtitle, object, and camera cues must support comprehension. |
| Format material | PaperCut/avatar materiality and movement must suit the selected format route. |

The compiler must store primitive refs at cue or beat level where possible. A program-level primitive list alone is insufficient for production approval.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Compiler cannot run without all pinned context refs and approved character refs. |
| Phase4-M02 Cinematic Meaning | Each beat-to-state decision must declare the meaning job and source beat. |
| Phase4-M04 Frictionless Block | Missing alignment, missing state, illegal transition, or primitive gaps block before rendering. |
| Phase4-M05 Actionable Rejection | Rejections name beat ID, state ID, cue ID, failed rule, and repair command. |
| Phase5-M01 Verifiable Artifact | Program hash, input refs, candidate scoring, rejected states, seeds, and evals are captured in the receipt. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Use integer ticks as canonical time. | Avoid frame drift, subtitle drift, and audio alignment errors. |
| Compile from approved interview context only. | Keeps the platform interview-first and prevents generic avatar scripts. |
| Separate candidate retrieval from final cue assembly. | Allows evaluation, rejected-candidate memory, and repair without rerunning all stages. |
| Store cue-level primitive refs. | Program quality depends on where the principle appears, not only that it is named. |
| Treat Motion Canvas and Remotion as consumers. | They cannot select acting states or reinterpret transcript meaning. |

### Gate Thresholds and Verdicts

Performance compiler gates inherit the source bundle `per_program` thresholds from `registries/eval_gates.json`.

| Gate ID | Threshold | Hard Fail | Downstream Consequence |
|---|---:|---|---|
| `source_alignment` | 0.95 | Yes | Blocks program assembly. |
| `lip_sync` | 0.86 | No | Below threshold creates `PROVISIONAL_LIP_SYNC_REVIEW`; visible-mouth final render requires repair or operator approval. |
| `beat_performance_match` | 0.82 | Yes | Blocks `TwoDCharacterProgram` assembly. |
| `primitive_compliance` | 0.90 | Yes | Blocks program assembly and render handoff. |
| `doctrine_alignment` | 0.95 | Yes | Blocks program assembly and operator approval. |
| `motion_restraint` | 0.82 | No | Below threshold creates `PROVISIONAL_MOTION_RESTRAINT_REVIEW`; operator must approve or reduce motion before final render. |
| `technical_render` | 1.00 | Yes | Blocks render package creation. |

Verdict semantics are deterministic: hard-fail gates return `PASS` when `score >= threshold` and `FAIL` otherwise. Non-hard-fail gates return `PASS` when `score >= threshold`, `PROVISIONAL` when `threshold - 0.08 <= score < threshold`, and `FAIL` when below that provisional floor.

## 4. Implementation Plan

1. Add `TwoDCharacterProgram` contracts with timebase, context refs, character refs, transcript alignment, performance tracks, choreography, composition, finishing, evals, approval, and receipt refs.
2. Add `two_d_performance_compiler_service.py` with an orchestration method `compile_program(request)`.
3. Add DSPy modules listed in Section 2 with strict Pydantic outputs.
4. Add acting-state retrieval scoring by communicative intent, emotion, body language, gesture family, energy, content format, primitive affinity, doctrine compatibility, transition legality, and recent-use diversity.
5. Add beat-to-state mappings for memory, confession, meaning reveal, teaching, challenge, invitation, humor, and warning beats.
6. Add gesture planner with prepare, stroke, hold, recover, amplitude, hand pose, gaze target, and primitive refs.
7. Add gaze, facial pose, viseme, prop/MSA, and transition planners.
8. Add `TwoDCharacterProgramAssembler` that assembles only passing plans.
9. Add export of generated TypeScript contracts for Motion Canvas and Remotion consumers.
10. Add fixture programs for Educational/PaperCut, avatar explainer, and a restrained cinematic PaperCut insert.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class CharacterPerformanceCompilerRequest(BaseModel):
    schema_version: Literal["cmf.character_performance_compiler_request.v1"]
    workspace_id: UUID
    brand_context_version_id: UUID
    interview_brief_id: UUID
    interview_asset_contract_id: UUID
    transcript_beat_map_id: UUID
    expression_moment_ids: list[UUID]
    voice_dna_version_id: UUID
    visual_dna_version_id: UUID
    primitive_eval_bundle_id: UUID
    doctrine_bundle_id: UUID
    asset_package_spec_id: UUID
    scene_template_id: UUID
    format_target: Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
    character_rig_version_id: UUID
    performance_library_version_id: UUID


class CharacterPerformanceCue(BaseModel):
    cue_id: UUID
    track_id: str
    beat_id: UUID
    start_tick: int = Field(ge=0)
    end_tick: int | None = Field(default=None, ge=0)
    action: Literal[
        "set_state",
        "set_clip",
        "set_gaze",
        "set_face_pose",
        "set_hand_pose",
        "set_mouth_shape",
        "attach_prop",
        "detach_prop",
        "set_camera",
        "show_scene_object",
    ]
    target_id: str | None = None
    value: dict | str | float | int | bool | None = None
    mix_in_ticks: int = Field(default=0, ge=0)
    mix_out_ticks: int = Field(default=0, ge=0)
    semantic_target: str
    primitive_refs: list[str] = Field(min_length=1)


class TwoDCharacterProgram(BaseModel):
    schema_version: Literal["cmf.two_d_character_program.v1"]
    program_id: UUID
    status: Literal["draft", "compiled", "eval_failed", "blocking_preview_ready", "approved_for_render"]
    context_refs: dict[str, str]
    character_refs: dict[str, str]
    timebase: dict
    transcript_alignment_ref: str
    performance_tracks: list[dict]
    motion_canvas_choreography: dict
    remotion_composition: dict
    ffmpeg_finishing: dict
    evaluation_spec: dict
    operator_approval: dict
    program_hash: str


class CharacterPerformanceCompilerReceipt(BaseModel):
    schema_version: Literal["cmf.character_performance_compiler_receipt.v1"]
    receipt_id: UUID
    program_id: UUID
    compiler_stage_receipts: list[str]
    selected_acting_state_refs: list[str]
    rejected_candidate_refs: list[str]
    eval_receipt_refs: list[str]
    input_hashes: dict[str, str]
    program_hash: str
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Transcript alignment confidence too low | Block with `TRANSCRIPT_ALIGNMENT_CONFIDENCE_LOW`; allow manual repair. |
| Acting state missing | Request PerformanceLibrary repair or block with `ACTING_STATE_NOT_FOUND`. |
| Illegal transition | Select bridge clip if available; otherwise block with `ACTING_TRANSITION_ILLEGAL`. |
| Viseme alignment unavailable | Allow blocking preview; block final render with `VISEME_ALIGNMENT_REQUIRED` when mouth animation is visible. |
| Primitive refs absent from cues | Block with `CUE_PRIMITIVE_REF_MISSING`. |
| Remotion duration does not match timebase | Block with `REMOTION_DURATION_TIMEBASE_MISMATCH`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T108-01 | Add `TwoDCharacterProgram` contracts and schema generation. |
| T108-02 | Add DSPy performance compiler modules with typed outputs. |
| T108-03 | Add acting-state retrieval scoring and rejected candidate receipts. |
| T108-04 | Add gesture, gaze, face, viseme, prop, and transition planners. |
| T108-05 | Add integer tick timebase validation and frame conversion. |
| T108-06 | Add cue-level primitive and source beat binding. |
| T108-07 | Add TypeScript contract generation for render consumers. |
| T108-08 | Add program fixtures and golden schema tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate |
|---|---|---|---|
| AC108-01 | Compiler requires all pinned context and character refs. | Program compiles from a loose prompt and character name only. | Phase4-M01 |
| AC108-02 | Timebase uses integer ticks and validates Remotion frame duration. | Program stores cue timing as floating seconds and final frames drift. | Phase5-M01 |
| AC108-03 | Every performance cue binds to a source beat and primitive ref. | A hand gesture exists because it looks good but has no source meaning. | Phase4-M02 |
| AC108-04 | Illegal acting transitions are blocked or repaired before assembly. | Reflective grief jumps into aggressive direct-camera challenge without bridge. | Phase4-M04 |
| AC108-05 | `TwoDCharacterProgram` assembles only after evaluation passes. | A program with missing gaze logic proceeds to render. | Phase4-M05 |
| AC108-06 | Generated TS contracts are consumers only. | Motion Canvas code changes acting-state selection. | Phase5-M01 |

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `TS-CMF-027` | Internal | Interview Asset Contract. |
| `TS-CMF-031` | Internal | Expression Moment candidates. |
| `TS-CMF-032` | Internal | Approved Expression Moment boundaries. |
| `TS-CMF-078` | Internal | Four video format doctrine crosswalk. |
| `TS-CMF-084` | Internal | Transcript beat map and timing compiler. |
| `TS-CMF-085` | Internal | Acting/avatar performance selector. |
| `TS-CMF-110` | Internal | Character Genesis object model. |
| `TS-CMF-113` | Internal | Render, eval, approval, and repair runtime. |
| DSPy | Runtime | Structured compiler stages. |
| Motion Canvas | Consumer | Scene choreography consumer. |
| Remotion | Consumer | Final platform composition consumer. |

## 10. Testing Strategy

- Unit test timebase conversion, frame duration parity, and invalid cue bounds.
- Unit test DSPy module output schemas with valid and invalid fixtures.
- Test acting-state retrieval ranking and hard doctrine failure removal.
- Test beat-to-state mapping for memory, confession, meaning reveal, teaching, challenge, invitation, humor, and warning.
- Test gesture planner prepare/stroke/hold/recover tick ordering.
- Test gaze target legality for camera, interviewer, teaching object, quote card, poll A/B, and memory directions.
- Test viseme alignment with low confidence, missing phonemes, and manual repairs.
- Test program assembly rejects missing primitive refs, illegal transitions, and missing source beat refs.
- Golden test `example_two_d_character_program.json` against generated schema and expected hashes.
