---
tech_spec_id: "TS-CMF-093"
title: "CMF Animation Studio Migration and Operator Rig Editor"
story_id: "7.21"
story_title: "Animation Studio Migration and Operator Rig Editor"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "2D Animation Studio audit repair"
pipeline_stage: "4 / 10 / 11 / 13"
entry_object: "LockedBrandContext, RigManifest, AnimationPlan, CompositionBeatMap, CompleteEditingSession"
exit_object: "AnimationStudioSession, AnimationManifestPatch, OperatorRigEditReceipt"
validation_contract: "CMF-native studio session, rig edit safety, doctrine gates, preview parity, exportable patch receipts"
required_receipt: "OperatorRigEditReceipt"
runtime_target: "Python / Pydantic v2 / FastAPI / Next.js / PixiJS / DragonBones-compatible manifests"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-093: CMF Animation Studio Migration and Operator Rig Editor

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/audits/CMF_2D_ANIMATION_STUDIO_AND_SPEC_PROTOCOL_AUDIT_2026-06-24.md` | Establishes the operational gap: backend contracts exist, but the CMF-native operator Animation Studio does not. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines the required CMF/ERA3 spec structure and audit lenses. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Provides FR-CMF-04.03, FR-CMF-07.05, FR-CMF-08.02, NFR-28, and NFR-31 obligations. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Requires Brand Genesis, 64-state assets, paper-cut rigging, and micro-semiotic binding before production rendering. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Confirms Python-first orchestration with TypeScript allowed only for UI and deterministic render leaves. |
| `THE CMF STUDIO/src/ccp_studio/contracts/rig_manifest.py` | Current CMF rig contract that the studio must load, validate, patch, and re-lock. |
| `THE CMF STUDIO/src/ccp_studio/services/rig_validation_service.py` | Existing validation service that must remain the backend authority for rig readiness. |
| `THE CMF STUDIO/src/ccp_studio/contracts/creative_libraries.py` | Source of Acting Library, paper-cut props, and creative library bindings exposed to the editor. |
| `THE CMF STUDIO/registries/evals/doctrine/cmf_papercut_rig_doctrine_eval.v1.json` | Defines doctrine evidence routes, threshold, hard failures, and rig-lock obligations. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Requires at least three validated primitives across meaning, delivery shape, and material/format roles. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\page.tsx` | Legacy reference for the six-panel operator shell: Clip Library, Beat Timeline, Bone Inspector, Layer Manager, Audio Panel, Transport. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\types.ts` | Legacy reference for character packages, manifest patches, BPM, lip-sync keyframes, and frame export jobs. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\scene-presets.ts` | Legacy reference for SC-01 through SC-08 scene presets that must be adapted into CMF template families. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\two-character.ts` | Legacy reference for two-character guest/interviewer composition layouts. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\gate-o.ts` | Legacy reference for pre-session validation, to be replaced by CMF doctrine and primitive gates. |

## 2. Overview

The CMF Studio needs a real operator Animation Studio, not only backend contracts. This spec migrates the valuable legacy editor concepts into `THE CMF STUDIO` as a CMF-native operator surface for paper-cut avatars, 2D animated explainers, and Conscious Living Reaction layouts.

The studio is a controlled editor for approved production objects. It must not become a separate source of product truth. Operators can inspect, preview, adjust, and approve rig and animation decisions, but every edit is converted into a typed `AnimationManifestPatch`, validated by CMF backend services, and written with an `OperatorRigEditReceipt`.

The first production focus is the four canonical video formats:

| Format | Studio Responsibility |
|---|---|
| Cinematic Story Commentary | Preview character cutouts, memory-object layers, emotional subtitle timing, and restrained motion. |
| Educational / Explainer | Build paper-cut or animated avatar explainer scenes from transcript beats, doctrine cues, and primitive triads. |
| Challenger / Frame Breaker | Validate debate, ranking, poll, and proof-card motion without collapsing into generic outrage templates. |
| Reaction / Recognition Clip | Edit upper reaction UI and lower guest/interviewer cutouts with transcript-accurate timing. |

This spec covers the UI/editor and backend patch contract. The headless frame renderer is specified separately in `TS-CMF-094`.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-093-001 | `RigManifest` | Load approved rig layers, bones, hidden regions, facial states, hand states, and validation status. |
| DEP-CMF-093-002 | `AnimationPlan` | Expose beat-level motion plans, lip-sync cues, camera moves, SFX markers, and caption timing. |
| DEP-CMF-093-003 | `CompositionBeatMap` | Bind every visible edit to transcript timestamps and frame ranges. |
| DEP-CMF-093-004 | `CreativeLibraryBinding` | Provide approved acting states, paper props, style rules, and motion constitution assets. |
| DEP-CMF-093-005 | `AnimationManifestPatch` | Persist operator edits as deterministic patch operations, never as untracked canvas state. |
| DEP-CMF-093-006 | `OperatorRigEditReceipt` | Record user, workspace, source object, before/after hashes, validation results, blockers, and approval decision. |
| DEP-CMF-093-007 | `CompleteEditingSession` | Scope editor access to one guest, one workspace, one source moment, and one render route. |
| DEP-CMF-093-008 | `EvaluationReceipt` | Surface doctrine and primitive blockers before export. |

### Existing Backend Integration

The studio MUST call existing CMF backend services instead of inventing its own state model:

| Backend Owner | Integration |
|---|---|
| `src/ccp_studio/contracts/rig_manifest.py` | Type source for rig IDs, layer IDs, bone IDs, hidden-region repair, and lock status. |
| `src/ccp_studio/services/rig_validation_service.py` | Validates rig readiness after every patch. |
| `src/ccp_studio/contracts/creative_libraries.py` | Provides Acting Library states, paper props, SFX libraries, and style constitution bindings. |
| `src/ccp_studio/services/creative_library_service.py` | Resolves approved creative libraries by guest workspace and locked Brand Context. |
| `src/ccp_studio/contracts/deterministic_rendering.py` | Provides render-route and preview determinism contracts. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Runs doctrine evals before an edit can be approved or exported. |
| `src/ccp_studio/workflows/render_workflow.py` | Receives only validated renderer-ready outputs after preview approval. |

The frontend MUST be a leaf runtime. It can use Next.js, React, PixiJS, and DragonBones-compatible manifest playback, but it cannot query production data directly. It receives typed view models from CMF APIs and sends typed patch commands back.

### ADR-05 Primitives

Every studio session MUST display the active primitive triad for the selected composition. At least three primitives must be valid before approval:

| Role | Required Primitive Examples |
|---|---|
| Meaning transform | `PRM-HUM-025`, `PRM-PRS-015`, `PRM-PRS-009`, `PRM-PRS-002` |
| Delivery shape | `PRM-PRS-032`, `PRM-PRS-025`, `PRM-VOC-007`, `PRM-VOC-009` |
| Format material | `PRM-VSG-020`, `PRM-VSG-008`, `PRM-VSG-021`, `PRM-VSG-024` |

The studio MUST fail approval with `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET` if fewer than three primitives are validated, and with `COMPOSITION_PRIMITIVE_ROLE_COVERAGE_MISSING` if one required role is absent.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | The editor opens in blocked state until source lineage, locked Brand Context, and eval target are present. |
| Phase4-M02 Cinematic Meaning | Motion controls must show the narrative or teaching job of each motion cue. |
| Phase4-M04 Frictionless Block | Blockers must disable export while still allowing inspection and repair. |
| Phase4-M05 Actionable Rejection | Every blocker must provide the failed object ID, rule ID, and recommended repair path. |
| Phase5-M01 Verifiable Artifact | Every approved patch must produce a receipt with hashes and evidence refs. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Migrate concepts, not legacy code wholesale. | The legacy app is useful, but it is not CMF-native and lacks full backend authority. |
| Keep Python as source of truth. | CMF contracts, receipts, evals, and orchestration remain Python/Pydantic. |
| Use TypeScript for the editor only. | The editor is a human-facing runtime and can use React/PixiJS as a controlled leaf. |
| Store patches, not opaque editor state. | Reproducibility requires replayable changes over locked CMF objects. |
| Gate export through doctrine and primitive evals. | The studio must enforce CMF quality standards rather than become a freeform design tool. |

## 4. Implementation Plan

1. Create CMF frontend route `/studio/animation/:editingSessionId` inside the CMF web app.
2. Add backend read model endpoint `GET /api/v1/animation-studio/sessions/{id}` returning `AnimationStudioSession`.
3. Add backend command endpoint `POST /api/v1/animation-studio/sessions/{id}/patches` accepting `AnimationManifestPatch`.
4. Implement six operator panels adapted from legacy: Clip Library, Beat Timeline, Bone Inspector, Layer Manager, Audio Panel, and Transport.
5. Add Guest/Brand Workspace header with asset code, locked Brand Context version, source moment, route, and active primitive triad.
6. Add preview canvas using PixiJS playback for static rig/layer preview and simple motion scrub.
7. Implement patch validation through `rig_validation_service.py` and doctrine evals.
8. Add export button that creates an `OperatorRigEditReceipt` and hands off to `TS-CMF-094` for frame rendering or `TS-CMF-090` for renderer prop compilation.
9. Add fixture sessions for one paper-cut explainer, one two-character reaction layout, and one cinematic story commentary layout.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class AnimationStudioPanelState(BaseModel):
    panel_id: Literal[
        "clip_library",
        "beat_timeline",
        "bone_inspector",
        "layer_manager",
        "audio_panel",
        "transport",
        "evals",
    ]
    is_visible: bool = True
    selected_object_id: str | None = None


class AnimationManifestPatchOperation(BaseModel):
    op_id: UUID
    op_type: Literal[
        "set_layer_visibility",
        "set_layer_order",
        "set_bone_transform",
        "assign_pose",
        "assign_mouth_shape",
        "assign_hand_state",
        "assign_prop",
        "assign_sfx",
        "adjust_cue_timing",
        "replace_motion_recipe",
    ]
    target_ref: str
    start_frame: int | None = None
    end_frame: int | None = None
    payload: dict
    reason: str
    primitive_refs: list[str] = Field(min_length=1)


class AnimationManifestPatch(BaseModel):
    schema_version: Literal["cmf.animation_manifest_patch.v1"]
    patch_id: UUID
    workspace_id: UUID
    complete_editing_session_id: UUID
    rig_manifest_id: UUID
    animation_plan_id: UUID
    beat_map_id: UUID
    base_manifest_hash: str
    operations: list[AnimationManifestPatchOperation]
    operator_note: str | None = None


class AnimationStudioSession(BaseModel):
    schema_version: Literal["cmf.animation_studio_session.v1"]
    session_id: UUID
    workspace_id: UUID
    guest_id: UUID
    complete_editing_session_id: UUID
    locked_brand_context_version: str
    asset_code: str
    route_code: str
    format_code: str
    rig_manifest_id: UUID
    animation_plan_id: UUID
    beat_map_id: UUID
    active_primitive_refs: list[str]
    eval_receipt_refs: list[str]
    panel_states: list[AnimationStudioPanelState]
    blocker_codes: list[str]


class OperatorRigEditReceipt(BaseModel):
    schema_version: Literal["cmf.operator_rig_edit_receipt.v1"]
    receipt_id: UUID
    patch_id: UUID
    operator_id: UUID
    before_hash: str
    after_hash: str
    validation_receipt_refs: list[str]
    eval_receipt_refs: list[str]
    approved_for_export: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

Legacy `apps/animation-studio` files are reference material only. If the new editor is not ready for a route, CMF MUST fall back to backend-only preview generation using locked manifests and static review images. It MUST NOT write new data back into the legacy repository and MUST NOT rely on legacy untyped JSON as production truth.

Fallback behavior:

| Condition | Fallback |
|---|---|
| PixiJS preview unavailable | Show deterministic keyframe preview frames from `TS-CMF-094`. |
| Bone inspector unsupported for a rig | Disable bone editing and permit layer/pose review only. |
| Audio panel unavailable | Show transcript beat timeline and require backend lip-sync receipt before approval. |
| Legacy preset not migrated | Block with `ANIMATION_STUDIO_PRESET_UNMIGRATED`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T093-01 | Define Pydantic models for `AnimationStudioSession`, `AnimationManifestPatch`, and `OperatorRigEditReceipt`. |
| T093-02 | Add API read model and patch command endpoints with workspace and guest scoping. |
| T093-03 | Build the six-panel operator UI with stable layout, no nested cards, and route-specific visual density. |
| T093-04 | Implement PixiJS rig preview using CMF rig/layer manifests. |
| T093-05 | Bind Beat Timeline to transcript-derived frame ranges from `TS-CMF-084`. |
| T093-06 | Bind Bone Inspector and Layer Manager to patch operations only. |
| T093-07 | Add primitive triad and doctrine eval status to the editor header and eval panel. |
| T093-08 | Add export blocker handling and actionable repair instructions. |
| T093-09 | Add fixtures for paper-cut explainer, two-character reaction, and cinematic story commentary. |
| T093-10 | Add tests proving that no patch can export without source lineage, Brand Context, rig validation, and three primitive validations. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC093-01 | Operator can open an Animation Studio session scoped to one guest workspace and one Complete Editing Session. | UI mixes assets from two guests. | Phase4-M01 |
| AC093-02 | Every operator edit is persisted as an `AnimationManifestPatch` operation with before/after hashes. | Canvas state changes but no replayable patch exists. | Phase5-M01 |
| AC093-03 | Export is blocked when rig validation fails. | A broken mouth layer exports to renderer props. | Phase4-M04 |
| AC093-04 | Export is blocked when fewer than three primitive validations pass. | A paper-cut explainer passes with only a style primitive. | Phase4-M01 |
| AC093-05 | The Beat Timeline uses transcript frame ranges, not arbitrary manual timing. | Operator drags a caption outside the source segment without repair receipt. | Phase4-M02 |
| AC093-06 | Blockers include object ID, rule ID, and repair instruction. | UI says "invalid" without explaining which rig layer failed. | Phase4-M05 |
| AC093-07 | Legacy presets are transformed into CMF template family IDs before use. | `SC-04` appears in production without a CMF registry entry. | Phase5-M01 |
| AC093-08 | Preview and export handoff reference the same manifest hash. | Operator approves preview A, renderer receives props from preview B. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner Spec |
|---|---|
| Brand Genesis and acting library | `TS-CMF-018`, `TS-CMF-019`, `TS-CMF-020` |
| Complete Editing Session and SceneSpec | `TS-CMF-036`, `TS-CMF-037` |
| Beat map and timeline cues | `TS-CMF-084` |
| Paper-cut runtime manifest | `TS-CMF-086` |
| Renderer worker and props compiler | `TS-CMF-094`, `TS-CMF-090` |
| Eval and approval workbench | `TS-CMF-077`, `TS-CMF-092` |
| UI architecture | `TS-CMF-070`, `TS-CMF-075` |

## 10. Testing Strategy

| Test | Required Evidence |
|---|---|
| Contract tests | Pydantic validation for session, patch, operation, and receipt schemas. |
| API tests | Workspace scoping, patch validation, blocker creation, and receipt persistence. |
| UI tests | Session load, panel switching, timeline scrub, patch creation, export blocking, and repair display. |
| Fixture tests | Paper-cut explainer, two-character reaction, and cinematic story sessions load without cross-guest leakage. |
| Doctrine tests | `EVL-DOCTRINE-PPR-RIG-001` hard failures block approval. |
| Primitive tests | `CMF-COMP-PRIMITIVE-TRIADS-001` minimum and role coverage failures block export. |
| Regression tests | Existing rig validation and deterministic rendering tests continue passing. |
| Visual tests | Nonblank preview canvas, correct character framing, no text overlap, and stable safe-zone layout. |

