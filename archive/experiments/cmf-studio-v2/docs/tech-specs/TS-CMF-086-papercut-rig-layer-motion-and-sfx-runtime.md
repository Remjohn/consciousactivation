---
tech_spec_id: "TS-CMF-086"
title: "Paper-Cut Rig, Layer, Motion, and SFX Runtime"
story_id: "7.16"
story_title: "Paper-Cut Runtime"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and protocol repair"
pipeline_stage: "4 / 10 / 11"
entry_object: "ResolvedBrandGenesisSubstrate, RigManifest, PerformanceStateSelectionManifest, CompositionBeatMap"
exit_object: "PaperCutRuntimeManifest, PaperCutRuntimeReceipt"
validation_contract: "rig integrity, layer depth, motion restraint, SFX binding, primitive triad, doctrine evidence"
required_receipt: "PaperCutRuntimeReceipt"
runtime_target: "Python / Pydantic v2 / PixiJS worker / Motion Canvas / Remotion / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-086: Paper-Cut Rig, Layer, Motion, and SFX Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines mandatory CMF/ERA3 spec structure and audit expectations. |
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Identifies the missing operational runtime for paper-cut and 2D avatar animation. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Requires paper-cut avatar rig generation, evaluation, repair, approval, and lock. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Defines Brand Genesis, 64-state assets, micro-semiotic anchors, and paper-cut rig obligations. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Provides creative pipeline stages for scene, asset, motion, and review flow. |
| `THE CMF STUDIO/src/ccp_studio/contracts/rig_manifest.py` | Current rig contract for avatar layer, hidden-region, bone, and state validation. |
| `THE CMF STUDIO/src/ccp_studio/services/rig_validation_service.py` | Current backend authority for rig validation and repair status. |
| `THE CMF STUDIO/src/ccp_studio/contracts/creative_libraries.py` | Source of acting library, pose states, paper props, and creative library refs. |
| `THE CMF STUDIO/registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json` | Defines required doctrine evidence routes and hard blockers for paper-cut rigs. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Requires minimum three primitives and role coverage for composition targets. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\scene-presets.ts` | Legacy reference for scene presets and paper-cut/animation route families. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\two-character.ts` | Legacy reference for guest/interviewer layouts and interaction scenes. |

## 2. Overview

The paper-cut runtime turns an approved rig, selected performance state, micro-semiotic anchors, and transcript beat map into an executable animation manifest. It exists to prevent paper-cut from becoming a decorative style label. A valid CMF paper-cut scene must have tactile layer evidence, riggable character states, purposeful motion, source-timed cues, and doctrine receipts.

This runtime supports:

- 2D Avatar / Animated Explainer scenes;
- paper-cut myth, truth, contrast, timeline, and framework teaching layouts;
- guest/interviewer upper-body scenes when paper-cut or avatar treatment is selected;
- 64-state acting library pose and expression reuse;
- SFX and tactile paper sounds aligned to transcript beats;
- handoff to the operator Animation Studio and headless frame renderer.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-086-001 | `ResolvedBrandGenesisSubstrate` | Provides locked visual identity, micro-semiotic anchors, and approved creative material. |
| DEP-CMF-086-002 | `RigManifest` | Provides layer hierarchy, bones, hidden regions, rig lock status, and avatar state refs. |
| DEP-CMF-086-003 | `PerformanceStateSelectionManifest` | Selects face, hands, body posture, emotion, and teaching stance from the 64-state library. |
| DEP-CMF-086-004 | `CompositionBeatMap` | Supplies exact frame windows and meaning beats for motion and SFX. |
| DEP-CMF-086-005 | `MicroSemioticAnchorManifest` | Supplies symbolic, object, wardrobe, texture, and environment cues. |
| DEP-CMF-086-006 | `PaperCutRuntimeManifest` | Canonical output consumed by Animation Studio and renderer workers. |
| DEP-CMF-086-007 | `PaperCutRuntimeReceipt` | Records validations, hashes, eval evidence, blockers, and export readiness. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `rig_manifest.py` | Runtime cannot compile unless rig layers, hidden regions, and required states are valid. |
| `rig_validation_service.py` | Must run before runtime manifest creation and after operator patching. |
| `creative_libraries.py` | Provides approved paper props, pose states, SFX families, and style constitution refs. |
| `doctrine_evaluation_service.py` | Runs `EVL-DOCTRINE-PPR-RIG-001` and composition primitive triad evals. |
| `composition.py` | Receives paper-cut runtime refs as part of composition runtime binding. |
| `deterministic_rendering.py` | Receives runtime manifest refs for renderer prop compilation and frame worker jobs. |

### ADR-05 Primitives

The paper-cut runtime MUST validate at least three primitives from the active route triad. For educational paper-cut explainers, preferred primitive coverage is:

| Role | Primitive Examples |
|---|---|
| Meaning transform | `PRM-HUM-025` Analogy Bridge, `PRM-PRS-015` What Is / What Could Be Contrast Engine |
| Delivery shape | `PRM-PRS-032` Explanation Engine, `PRM-PRS-025` Rule of Three Message Architecture |
| Format material | `PRM-VSG-020` Perspective and Layering as Meaning, `PRM-VSG-008` Character Coherence Beats Beauty |

For cinematic paper-cut memory scenes, use source-appropriate primitives such as `PRM-PRS-009`, `PRM-PRS-002`, `PRM-VOC-009`, `PRM-VOC-007`, and `PRM-VSG-021`.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Runtime cannot compile without locked Brand Context, approved rig, beat map, and eval target. |
| Phase4-M02 Cinematic Meaning | Motion cue must declare one of four jobs: attention, meaning reveal, tactile realism, emotional beat. |
| Phase4-M04 Frictionless Block | Invalid rig, missing paper materiality, or missing primitives block export without destroying draft data. |
| Phase4-M05 Actionable Rejection | Blockers name failed layer, state, cue, primitive, or doctrine evidence route. |
| Phase5-M01 Verifiable Artifact | Runtime manifest and receipts must be reconstructable from locked inputs. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Treat paper-cut as a runtime, not an image style. | CMF needs editable, riggable, timed scenes. |
| Compile motion from transcript beats. | Animation must serve the interview moment, not generic explainer motion. |
| Use restraint-first motion constitution. | Paper-cut should feel intentional, tactile, and legible. |
| Separate material rules from renderer implementation. | The same manifest can feed PixiJS, Motion Canvas, or Remotion. |
| Require SFX to be cue-bound. | Paper sounds and accents must reinforce timing rather than clutter scenes. |

## 4. Implementation Plan

1. Add contracts for `PaperCutRuntimeManifest`, `PaperCutMotionCue`, `PaperCutLayerCue`, `PaperCutSfxCue`, and `PaperCutRuntimeReceipt`.
2. Implement `paper_cut_runtime_service.py` to compile approved inputs into runtime manifests.
3. Integrate `rig_validation_service.py` before manifest creation.
4. Integrate doctrine eval `EVL-DOCTRINE-PPR-RIG-001` and composition primitive triad eval.
5. Compile beat-to-layer, beat-to-motion, beat-to-SFX, and beat-to-caption bindings from `CompositionBeatMap`.
6. Add materiality rules: torn paper edges, visible layer depth, shadow offset, cutout outline, tactile prop evidence, limited parallax.
7. Add motion constitution validator: every motion cue must serve attention, meaning, tactile realism, or emotional beat.
8. Emit read models for `TS-CMF-093` and render job inputs for `TS-CMF-094`.
9. Add route fixtures for paper-cut myth-busting, paper-cut framework teaching, paper-cut identity metaphor, and two-character explainer.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class PaperCutMaterialityRule(BaseModel):
    rule_id: str
    rule_type: Literal["edge", "shadow", "texture", "layer_depth", "cutout_outline", "paper_prop"]
    renderer_payload: dict
    required: bool = True


class PaperCutMotionCue(BaseModel):
    cue_id: UUID
    beat_id: UUID
    target_ref: str
    motion_type: Literal[
        "slide",
        "nudge",
        "reveal",
        "parallax",
        "blink",
        "mouth_shape",
        "hand_gesture",
        "prop_pop",
        "paper_wiggle",
    ]
    motion_job: Literal["attention", "meaning_reveal", "tactile_realism", "emotional_beat"]
    start_frame: int
    end_frame: int
    easing: str
    amplitude: float
    primitive_refs: list[str] = Field(min_length=1)


class PaperCutSfxCue(BaseModel):
    cue_id: UUID
    beat_id: UUID
    sfx_ref: str
    start_frame: int
    end_frame: int | None = None
    gain_db: float
    reason: str


class PaperCutRuntimeManifest(BaseModel):
    schema_version: Literal["cmf.papercut_runtime_manifest.v1"]
    manifest_id: UUID
    workspace_id: UUID
    composition_runtime_binding_id: UUID
    rig_manifest_id: UUID
    layer_manifest_id: UUID
    beat_map_id: UUID
    performance_state_selection_id: UUID
    route_code: str
    format_code: str
    materiality_rules: list[PaperCutMaterialityRule]
    motion_cues: list[PaperCutMotionCue]
    sfx_cues: list[PaperCutSfxCue]
    prop_layer_refs: list[str]
    micro_semiotic_anchor_refs: list[UUID]
    eval_receipt_refs: list[str]
    blocker_codes: list[str]


class PaperCutRuntimeReceipt(BaseModel):
    schema_version: Literal["cmf.papercut_runtime_receipt.v1"]
    receipt_id: UUID
    manifest_id: UUID
    input_hashes: dict[str, str]
    output_hash: str
    doctrine_eval_receipt_ref: str
    primitive_eval_receipt_ref: str
    approved_for_animation_studio: bool
    approved_for_render_worker: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

Legacy scene presets may inform initial templates, but they must be converted into CMF runtime manifests before use. If a route cannot satisfy runtime requirements, CMF may generate a still concept preview for operator discussion, but it must block final animation export.

| Condition | Fallback |
|---|---|
| Rig missing required layer | Block with `PAPERCUT_RIG_LAYER_MISSING`. |
| No validated primitive triad | Block with `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`. |
| Paper materiality absent | Block with `PAPERCUT_MATERIALITY_EVIDENCE_MISSING`. |
| Motion cue has no declared job | Block with `PAPERCUT_MOTION_JOB_MISSING`. |
| SFX library unavailable | Permit silent preview but block final sound assembly with `PAPERCUT_SFX_LIBRARY_MISSING` if SFX is required. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T086-01 | Add runtime manifest, motion cue, materiality rule, SFX cue, and receipt contracts. |
| T086-02 | Implement paper-cut runtime compiler service. |
| T086-03 | Integrate rig validation, doctrine eval, and primitive triad eval. |
| T086-04 | Compile motion cues from transcript beat map and performance states. |
| T086-05 | Compile SFX cues from beat roles and materiality rules. |
| T086-06 | Compile prop/layer bindings from Brand Genesis and micro-semiotic anchors. |
| T086-07 | Add read model for operator preview and patching. |
| T086-08 | Add handoff payload for headless frame renderer. |
| T086-09 | Add fixtures for myth-busting, teaching, contrast, and identity metaphor scenes. |
| T086-10 | Add failure fixtures for flat image, no rig, no primitives, no materiality, and generic route feel. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC086-01 | Runtime manifest cannot compile without valid and locked rig manifest. | Paper-cut route uses a single PNG portrait as avatar. | Phase4-M01 |
| AC086-02 | Every motion cue declares a motion job and source beat. | A prop wiggles without source timing or meaning. | Phase4-M02 |
| AC086-03 | Paper materiality rules are present and renderer-addressable. | Scene says paper-cut but renders as flat digital collage. | Phase4-M02 |
| AC086-04 | At least three primitives across required roles are validated. | Educational explainer uses only a visual style primitive. | Phase4-M01 |
| AC086-05 | Doctrine eval evidence routes include rig, motion, style, composition JSON, and lock receipt refs. | Runtime passes without `rig_lock_receipt`. | Phase5-M01 |
| AC086-06 | SFX cues are beat-bound and reasoned. | Random paper sound plays over a guest pause. | Phase4-M02 |
| AC086-07 | Operator Studio can inspect every layer, motion cue, and blocker. | Runtime creates hidden cues not visible to operator. | Phase4-M05 |
| AC086-08 | Runtime output can feed `TS-CMF-094` without manual conversion. | Frame worker requires untyped custom JSON. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| Acting library and paper-cut rig | `TS-CMF-019`, `TS-CMF-020` |
| Brand Context lock | `TS-CMF-021`, `TS-CMF-022` |
| Micro-semiotic anchors | `TS-CMF-087` |
| Complete Editing Session and SceneSpec | `TS-CMF-036`, `TS-CMF-037` |
| Layer manifest and animation plan | `TS-CMF-039` |
| Beat map and cues | `TS-CMF-084` |
| Performance state selector | `TS-CMF-085` |
| Animation Studio | `TS-CMF-093` |
| Headless frame renderer | `TS-CMF-094` |
| Eval workbench | `TS-CMF-077`, `TS-CMF-092` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Validate manifest, motion cue, materiality rule, SFX cue, and receipt schemas. |
| Rig tests | Invalid, unlocked, incomplete, and repaired rigs produce expected blockers. |
| Materiality tests | Missing edge, texture, shadow, or layer-depth evidence blocks paper-cut route. |
| Motion tests | Motion without job, source beat, or primitive ref fails. |
| Primitive tests | Minimum count, role coverage, and registered-ID checks use composition triad registry. |
| Doctrine tests | `EVL-DOCTRINE-PPR-RIG-001` hard failures block approval. |
| Fixture tests | Four positive paper-cut fixtures and five negative fixtures. |
| Integration tests | Manifest drives Animation Studio preview and headless frame render job creation. |

