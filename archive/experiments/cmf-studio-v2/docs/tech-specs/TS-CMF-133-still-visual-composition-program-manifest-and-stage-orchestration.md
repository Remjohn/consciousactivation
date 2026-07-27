---
tech_spec_id: "TS-CMF-133"
title: "Still Visual Composition Program, Manifest, and Stage Orchestration"
story_id: "14.1"
story_title: "Still Visual Composition Program Manifest"
epic_id: 14
epic_title: "Still Visual Composition Architecture"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-14.01"
  - "FR-CMF-14.02"
  - "FR-CMF-14.03"
pipeline_stage: "still visual composition orchestration"
entry_object: "StillVisualCompositionRequest"
exit_object: "StillVisualCompositionProgramReceipt"
validation_contract: "format family route, guest workspace, brand context, source evidence, primitive triad, stage manifest, provider materialization, deterministic Skia export"
required_receipt: "StillVisualCompositionProgramReceipt"
runtime_target: "Python / Pydantic v2 / stage workflow / provider jobs / Geometrics / Skia / evaluation receipts / approval gate"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-133: Still Visual Composition Program, Manifest, and Stage Orchestration

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec format, existing backend mapping, ADR-05, CBAR, failure examples, and testing strategy. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | CBAR mandates for cinematic meaning, routing SLA, frictionless blocking, and actionable rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact rule and approval evidence requirements. |
| `THE CMF STUDIO/docs/audits/CMF_STILL_VISUAL_COMPOSITION_ARCHITECTURE_AUDIT_2026-06-25.md` | Audit finding that still visual content needs the same stage manifest discipline as video composition. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Existing Geometrics, SAM3, PRETEXT, and Skia rendering spine for still visuals. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Carousel slide atom and sequence meaning dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` | Carousel compiler workflow dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` | Carousel Composition Atlas dependency for slide composition grammar. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Single image and SuperVisual router dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md` | Registry/schema parity owner for single-image contracts. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-101-single-image-router-format-family-and-archetype-selection.md` | Format family router dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | SuperVisual primitive triad and visual feel dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md` | Provider materialization owner for Ideogram 4, GPT Image 2, Flux 2, Qwen layered, SAM3, and Skia. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | Deterministic Skia scene compiler dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md` | Still image eval, review, and golden fixture dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-120-openmontage-reference-adapter-governance.md` | External architecture reference governance. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-121-production-pipeline-manifest-registry.md` | Production manifest pattern to reuse for still visual stage orchestration. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-124-scored-provider-selector-and-capability-router.md` | Provider capability scoring pattern. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-128-render-runtime-selection-and-locking.md` | Render runtime lock pattern for deterministic rendering. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` | Canonical artifact and approval protocol to apply to still visual stages. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_03_CMF_Media_Factory.md` | Product module defining monthly content package and media factory behavior. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_05_Brand_Context_and_Brand_Genesis.md` | Brand Context, prop library, micro-semiotic anchor, composition preference, and guest workspace requirements. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | Composition state, provider job, render contract, eval receipt, and approval requirements. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_08_Evals_and_Primitives.md` | Primitive-driven quality gate and eval receipt mandate. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis and micro-semiotic source of truth for brand-owned visual systems. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Scene program and composition handoff constraints. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE` | Legacy carousel visual grammar bundle to integrate, not bypass. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE` | Legacy single-image and SuperVisual composition bundle to integrate, not bypass. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Mandatory minimum of three primitive validations across meaning, delivery, and format/material roles. |
| `THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json` | Existing routing and candidate scoring policy for single image outputs. |
| `THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json` | Provider boundary policy for Ideogram 4, GPT Image 2, Flux, Qwen layered, SAM3, Skia, RoughNotation, and visual eval. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Existing composition contract owner to extend or reference. |
| `THE CMF STUDIO/src/ccp_studio/contracts/provider_jobs.py` | Existing provider job contract owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Existing deterministic render contract owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/evaluation_receipts.py` | Existing evaluation receipt contract owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/approval_gate.py` | Existing approval gate contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Existing composition service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Existing provider operation owner. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Existing deterministic render service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Existing receipt writer. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Existing render workflow owner to integrate with still visual programs. |
| `THE CMF STUDIO/src/ccp_studio/workflows/review_workflow.py` | Existing review workflow owner. |

## 2. Overview

Still visual content currently has strong component specs, but it lacks a single operational program object that tells the factory exactly what is being produced, why it was routed, which visual grammar owns it, which provider jobs are allowed, which layers must exist, which primitives validate the composition, and when a human may approve it. This spec creates `StillVisualCompositionProgram` as the stage manifest for non-video visual outputs.

The program is not a new renderer and not a replacement for the carousel or SuperVisual specs. It is the orchestration contract above them. It accepts a source-backed request from the interview-first pipeline, resolves the guest workspace and Brand Context, chooses the still visual family, locks the route, expands the relevant composition atlas, plans provider materialization, records layer/mask/typography obligations, runs deterministic Skia rendering, evaluates primitive and doctrine compliance, and emits a receipt that the review workbench and package compiler can trust.

This matters because a carousel and a SuperVisual are not just "images." A carousel needs sequence grammar, slide atom meaning, continuity, and per-slide composition contracts. A SuperVisual needs a single-frame thesis, symbolic compression, brand authority, and a different visual feeling than a tweet-like quote or meme. The program manifest makes that difference explicit and testable. It also prevents the common failure where Ideogram or another generative model becomes the invisible source of truth. Generative providers may create plates, characters, object cutouts, repairs, and visual options; the final composition authority remains CMF-owned JSON, registry-backed layout, deterministic Skia render, primitive receipts, and operator approval.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-133-001 | `StillVisualCompositionRequest` | Source-backed request from Content Sequence Program, operator command, or package compiler. Must include guest workspace, Brand Context version, source evidence, target format, and package slot. |
| DEP-CMF-133-002 | `StillVisualCompositionProgram` | Canonical stage manifest containing route, family, atlas refs, provider plan, layer plan, render plan, eval plan, review policy, and immutable receipt links. |
| DEP-CMF-133-003 | `StillVisualFamilyRoute` | Declares whether the output is carousel, SuperVisual, visual poll, tweet-like quote, meme, reaction still, documentary social card, or promo card. |
| DEP-CMF-133-004 | `CompositionAtlasBinding` | Links the program to the carousel atlas, single image contract registry, SuperVisual grammar, slide atom library, or meme/quote/poll registry. |
| DEP-CMF-133-005 | `ProviderMaterializationPlan` | Separates generative asset creation from final deterministic composition. Must obey provider responsibility registry. |
| DEP-CMF-133-006 | `LayerMaskTypographyManifest` | Declares required layers, masks, cutouts, text zones, subtitle/quote zones, annotation zones, brand lockups, and export variants. |
| DEP-CMF-133-007 | `StillVisualStageState` | Tracks each stage from requested to routed, materialized, composed, rendered, evaluated, reviewed, approved, exported, or rejected. |
| DEP-CMF-133-008 | `StillVisualCompositionProgramReceipt` | Final receipt proving source lineage, route, provider jobs, render hash, primitive evals, review decision, and export manifest. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/composition.py` | Keep common composition contracts. Add imports or references from new still visual contracts instead of duplicating universal composition primitives. |
| `src/ccp_studio/contracts/still_visuals.py` | New Pydantic owner for still visual request, program, family route, manifests, stage state, and receipts. |
| `src/ccp_studio/services/composition_service.py` | Add `create_still_visual_program`, `lock_still_visual_route`, and `bind_still_visual_atlas` commands. |
| `src/ccp_studio/services/still_visual_program_service.py` | New service for state transitions, stage validation, receipt assembly, and package handoff. |
| `src/ccp_studio/services/provider_operations_service.py` | Execute provider materialization jobs only from the locked provider plan. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Render only from approved Skia/Geometrics scene specs and locked runtime selection. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Attach primitive, visual grammar, source truth, likeness, text fit, platform fit, and deterministic replay receipts. |
| `src/ccp_studio/services/approval_gate_service.py` | Block approval when route, primitive triad, Brand Context, provider boundary, or render hash is missing. |
| `src/ccp_studio/workflows/still_visual_program.py` | New workflow orchestrating route, materialize, compile, render, evaluate, review, approve, and export. |
| `src/ccp_studio/repositories/still_visuals.py` | New persistence owner for programs, stage states, provider plans, render refs, eval refs, and receipts. |
| `src/ccp_studio/api/v1/still_visuals.py` | New API surface specified in TS-CMF-135. |

### ADR-05 Primitive Implementation

ADR-05 applies because every still visual composition is a production artifact whose quality is governed by primitives, not aesthetic preference. `StillVisualCompositionProgram` must load `registries/evals/composition/cmf_composition_primitive_triads.v1.json` and prove at least three primitive validations before render approval:

1. One primitive with role `meaning_transform`.
2. One primitive with role `delivery_shape`.
3. One primitive with role `format_material`.

The program must carry primitive references at the composition-family level and at the concrete scene/slide level. A carousel may satisfy the program-level triad through its sequence thesis, but each slide atom still needs local primitive evidence for why that slide exists. A SuperVisual may satisfy the triad through single-frame compression, but its symbolic elements, guest cutout, text hierarchy, and micro-semiotic anchors must remain traceable.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Requirement |
|---|---|
| Intelligence-Gated Intercept Rule | Reject any program created without source evidence from interview, transcript, Brand Context, research, approved operator input, or package sequence. |
| Cinematic Meaning Rule | Still visuals must carry meaning, not decorative templates. Each composition route needs a declared story, teaching, recognition, provocation, or authority function. |
| Inline Routing SLA | Route decision must be available immediately after request validation and before provider jobs run. |
| Frictionless Block Rule | Operators must see blockers as actionable fixes, not generic "failed eval" messages. |
| Actionable Rejection Rule | Rejection must include failed primitive, layer, source, provider, or render contract refs and suggested repair command. |
| Verifiable Artifact Rule | The final image export is not enough. The program receipt must reconstruct source, route, provider jobs, render hash, evals, and approval. |

### Technical Decisions

1. `StillVisualCompositionProgram` is the parent manifest for carousels, SuperVisuals, polls, quotes, memes, and reaction stills.
2. Existing carousel and single-image specs remain the detailed builders. This spec adds orchestration, state, and receipt discipline.
3. Final composition authority is Skia/Geometrics JSON plus registry-bound layout, not provider raster output.
4. Provider-generated plates and layered assets must be treated as materialization inputs, not finished approved content.
5. Human approval is required before public export, package inclusion, or publishing handoff.
6. Each still visual must be guest-scoped. No operator should see or reuse another guest's assets by accident.
7. The program must be replayable from stored JSON, asset refs, provider job reports, render inputs, and locked registries.

## 4. Implementation Plan

### Step 1 - Add Contracts

Create `src/ccp_studio/contracts/still_visuals.py` with Pydantic v2 models listed in Section 5. Reuse shared IDs, timestamps, source refs, evaluation refs, and approval refs where existing project contracts already define them.

### Step 2 - Add Persistence

Create persistence tables or repository entities:

| Table | Purpose |
|---|---|
| `still_visual_programs` | Program identity, guest workspace, Brand Context version, format code, route, status, and hashes. |
| `still_visual_stage_states` | Stage transition history and blocker state. |
| `still_visual_provider_plans` | Provider materialization plan and job references. |
| `still_visual_layer_manifests` | Layer, mask, typography, annotation, and export obligations. |
| `still_visual_program_receipts` | Immutable final receipt for review, approval, export, and package compiler handoff. |

### Step 3 - Implement Service

Create `StillVisualProgramService` with these commands:

| Command | Behavior |
|---|---|
| `create_program(request)` | Validate guest scope, source evidence, Brand Context, format, target platform, and initial package slot. |
| `resolve_family_route(program_id)` | Call carousel or single-image routers and create `StillVisualFamilyRoute`. |
| `bind_composition_atlas(program_id)` | Attach carousel atlas, single-image contract, SuperVisual grammar, or other visual family registry. |
| `plan_materialization(program_id)` | Generate provider job plan with provider responsibility boundaries. |
| `attach_layer_manifest(program_id)` | Validate text zones, masks, cutouts, micro-semiotic anchors, annotations, and export variants. |
| `lock_render_plan(program_id)` | Lock deterministic Skia/Geometrics runtime and render settings. |
| `emit_program_receipt(program_id)` | Assemble final receipt after eval and approval. |

### Step 4 - Add Workflow

Create `src/ccp_studio/workflows/still_visual_program.py` to orchestrate state transitions:

```text
REQUESTED -> VALIDATED -> ROUTED -> ATLAS_BOUND -> MATERIALIZATION_PLANNED
-> MATERIALIZED -> SCENE_COMPILED -> RENDER_LOCKED -> RENDERED
-> EVALUATED -> REVIEW_READY -> APPROVED -> EXPORTED
```

Any failed stage enters `BLOCKED` with a typed blocker and repair command.

### Step 5 - Integrate Existing Builders

The program must call existing specialized builders rather than duplicating them:

| Format Family | Required Builder |
|---|---|
| Carousel | TS-CMF-096, TS-CMF-097, TS-CMF-098 |
| SuperVisual | TS-CMF-099, TS-CMF-100, TS-CMF-101, TS-CMF-102, TS-CMF-134 |
| Visual Poll | TS-CMF-099 plus poll contract registry |
| Tweet-like Quote | TS-CMF-099 plus quote card contract registry |
| Meme | TS-CMF-099 plus meme safety and source-truth evals |
| Reaction Still | TS-CMF-099 plus reaction source refs and optional video route refs |

### Step 6 - Add Package Handoff

The final receipt must be consumable by the monthly package compiler, review board, and UI asset browser. Package handoff must include asset code, content format, guest workspace, export variants, approved thumbnail, source refs, and production readiness state.

## 5. Primary Output Schema

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

StillVisualFormatCode = Literal[
    "CAR-LST",      # listicle carousel
    "CAR-JUX",      # juxtaposition carousel
    "CAR-STORY",    # story carousel
    "SPV-CON",      # conceptual contrast SuperVisual
    "SPV-SYM",      # symbolic SuperVisual
    "SPV-PRM",      # premise/authority SuperVisual
    "VPL-WYR",      # would-you-rather visual poll
    "VPL-VRS",      # versus visual poll
    "TWQ-STD",      # tweet-like quote
    "TWQ-IMG",      # quote over image
    "MEM-INC",      # incongruity meme
    "MEM-REL",      # relatable meme
    "RCT-SEED",     # reaction seed still
]

StillVisualStage = Literal[
    "REQUESTED",
    "VALIDATED",
    "ROUTED",
    "ATLAS_BOUND",
    "MATERIALIZATION_PLANNED",
    "MATERIALIZED",
    "SCENE_COMPILED",
    "RENDER_LOCKED",
    "RENDERED",
    "EVALUATED",
    "REVIEW_READY",
    "APPROVED",
    "EXPORTED",
    "BLOCKED",
    "REJECTED",
]

class StillVisualTargetPlatform(BaseModel):
    platform: Literal["instagram", "linkedin", "youtube_community", "x", "facebook", "threads"]
    aspect_ratio: Literal["1:1", "4:5", "9:16", "16:9"]
    width_px: int = Field(ge=320)
    height_px: int = Field(ge=320)
    safe_area_ref: str
    export_profile_ref: str

class StillVisualCompositionRequest(BaseModel):
    request_id: str
    guest_workspace_id: str
    brand_context_id: str
    brand_context_version: str
    content_asset_code: str
    requested_format: StillVisualFormatCode
    package_slot_ref: str | None = None
    source_evidence_refs: list[str] = Field(min_length=1)
    expression_moment_refs: list[str] = Field(default_factory=list)
    sequence_program_ref: str | None = None
    target_platforms: list[StillVisualTargetPlatform] = Field(min_length=1)
    operator_intent: str
    created_by: str
    created_at: datetime

class StillVisualFamilyRoute(BaseModel):
    route_id: str
    program_id: str
    requested_format: StillVisualFormatCode
    resolved_family: Literal[
        "carousel",
        "supervisual",
        "visual_poll",
        "tweet_quote",
        "meme",
        "reaction_still",
        "documentary_social_card",
        "promo_card",
    ]
    resolved_subtype: str
    router_policy_ref: str
    atlas_registry_refs: list[str] = Field(min_length=1)
    candidate_scores: list[dict]
    selected_candidate_id: str
    operator_override_reason: str | None = None
    route_blockers: list[str] = Field(default_factory=list)

class StillVisualStageState(BaseModel):
    state_id: str
    program_id: str
    stage: StillVisualStage
    status: Literal["pending", "running", "passed", "blocked", "failed"]
    started_at: datetime | None = None
    completed_at: datetime | None = None
    blocker_codes: list[str] = Field(default_factory=list)
    repair_command_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)

class StillVisualProviderMaterializationPlan(BaseModel):
    plan_id: str
    program_id: str
    provider_policy_ref: str
    allowed_providers: list[str]
    prohibited_provider_uses: list[str]
    ideogram_composition_job_refs: list[str] = Field(default_factory=list)
    qwen_layered_job_refs: list[str] = Field(default_factory=list)
    sam3_mask_job_refs: list[str] = Field(default_factory=list)
    gpt_image_2_asset_job_refs: list[str] = Field(default_factory=list)
    flux_2_repair_job_refs: list[str] = Field(default_factory=list)
    rough_annotation_job_refs: list[str] = Field(default_factory=list)
    provider_receipt_refs: list[str] = Field(default_factory=list)

class LayerMaskTypographyManifest(BaseModel):
    manifest_id: str
    program_id: str
    layer_refs: list[str] = Field(min_length=1)
    mask_refs: list[str] = Field(default_factory=list)
    text_zone_refs: list[str] = Field(min_length=1)
    typography_contract_ref: str
    rough_annotation_cue_refs: list[str] = Field(default_factory=list)
    micro_semiotic_anchor_refs: list[str] = Field(default_factory=list)
    brand_lockup_refs: list[str] = Field(default_factory=list)
    export_variant_refs: list[str] = Field(min_length=1)

class StillVisualExportManifest(BaseModel):
    export_manifest_id: str
    program_id: str
    render_runtime_ref: str
    skia_scene_ref: str
    geometrics_layout_ref: str
    output_asset_refs: list[str] = Field(min_length=1)
    preview_asset_ref: str
    render_hash: str
    deterministic_replay_command_ref: str

class StillVisualCompositionProgram(BaseModel):
    program_id: str
    request: StillVisualCompositionRequest
    current_stage: StillVisualStage
    route: StillVisualFamilyRoute | None = None
    provider_plan: StillVisualProviderMaterializationPlan | None = None
    layer_manifest: LayerMaskTypographyManifest | None = None
    export_manifest: StillVisualExportManifest | None = None
    primitive_eval_refs: list[str] = Field(default_factory=list)
    doctrine_eval_refs: list[str] = Field(default_factory=list)
    review_state_ref: str | None = None
    approval_receipt_ref: str | None = None
    stage_states: list[StillVisualStageState] = Field(default_factory=list)

class StillVisualCompositionProgramReceipt(BaseModel):
    receipt_id: str
    program_id: str
    content_asset_code: str
    guest_workspace_id: str
    brand_context_version: str
    requested_format: StillVisualFormatCode
    resolved_family: str
    resolved_subtype: str
    source_evidence_refs: list[str]
    atlas_registry_refs: list[str]
    provider_job_refs: list[str]
    skia_scene_ref: str
    render_hash: str
    primitive_eval_refs: list[str]
    doctrine_eval_refs: list[str]
    review_decision_ref: str
    approval_receipt_ref: str
    export_asset_refs: list[str]
    created_at: datetime
```

## 6. Backward Compatibility Fallback

Existing carousel and single-image services may continue to run in lab mode, but production export must pass through `StillVisualCompositionProgram` once this spec is implemented. The fallback must behave as follows:

| Existing Path | Allowed Temporarily | Required Migration |
|---|---|---|
| Direct carousel build from TS-CMF-097 | Lab preview only | Wrap output in `StillVisualCompositionProgram` before approval/export. |
| Direct single-image render from TS-CMF-104 | Lab preview only | Attach route, provider, layer, render, eval, and approval manifests. |
| Manual PNG export | Not production-approved | Import as external asset candidate and run eval/review before package inclusion. |
| Ideogram-only image output | Reference plate only | Must be decomposed or bound into deterministic Skia final render. |
| Browser screenshot export | Blocked | TS-CMF-095 already prohibits browser screenshots as production fallback. |

## 7. Tasks

1. Add `src/ccp_studio/contracts/still_visuals.py` with schemas from Section 5.
2. Add repository methods for still visual programs, stage states, provider plans, layer manifests, export manifests, and receipts.
3. Implement `StillVisualProgramService.create_program`.
4. Implement route resolution by calling existing carousel and single-image routers.
5. Implement atlas binding for carousel atlas, single-image contract registry, and SuperVisual grammar registry.
6. Implement provider materialization plan validation against `single_image_provider_responsibilities.v2.json`.
7. Implement layer/mask/typography manifest validation.
8. Implement render runtime lock handoff to deterministic rendering service.
9. Implement primitive and doctrine receipt attachment.
10. Implement package handoff and content asset code persistence.
11. Add stage blockers and actionable repair commands.
12. Add golden fixture tests for one carousel, one SuperVisual, one visual poll, one quote card, one meme, and one reaction still.

## 8. Acceptance Criteria

### AC133-01: Program Creation Requires Guest Scope

Given a request without `guest_workspace_id`, when `create_program` runs, then the service must reject the request with `STILL_VISUAL_GUEST_SCOPE_MISSING`.

Failure example: an operator creates a SuperVisual from a transcript excerpt but does not bind Claude's workspace. The output cannot be routed because brand assets, likeness rules, and source lineage could leak across guests.

### AC133-02: Source Evidence Is Mandatory

Given a request with no `source_evidence_refs`, when validation runs, then the service must reject with `STILL_VISUAL_SOURCE_EVIDENCE_MISSING`.

Failure example: a meme is generated from a generic viral idea without transcript, interview brief, approved operator context, or research evidence.

### AC133-03: Route Must Precede Provider Jobs

Given a program in `VALIDATED`, when provider jobs are requested before `ROUTED`, then the service must block with `STILL_VISUAL_ROUTE_NOT_LOCKED`.

### AC133-04: Atlas Binding Is Required

Given a routed program, when no carousel atlas, single-image contract, SuperVisual grammar, or relevant format registry is attached, then the service must block with `STILL_VISUAL_ATLAS_BINDING_MISSING`.

### AC133-05: Provider Boundaries Are Enforced

Given an Ideogram 4 job marked as final typography authority, when the provider plan is validated, then the service must block with `PROVIDER_RESPONSIBILITY_VIOLATION`.

### AC133-06: Primitive Triad Is Required

Given a rendered image with fewer than three primitive validations across meaning, delivery, and format/material roles, when approval is requested, then the approval gate must block with `COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET`.

### AC133-07: Deterministic Render Is Required

Given a program whose final asset has no Skia scene ref, Geometrics layout ref, render hash, or replay command, when approval is requested, then the approval gate must block with `STILL_VISUAL_DETERMINISTIC_RENDER_MISSING`.

### AC133-08: Stage Receipt Is Replayable

Given an approved export, when the program receipt is retrieved, then it must reconstruct the source evidence, Brand Context version, route, atlas refs, provider jobs, Skia scene, render hash, evals, review, approval, and export refs.

### AC133-09: Format Feel Cannot Collapse

Given two programs, one SuperVisual and one tweet-like quote, when the visual grammar and primitive roles are evaluated, then they must not resolve to identical composition obligations unless a justified operator override is stored.

Failure example: all formats become black background, cutout person, giant caption, and colored accent. This must fail because it erases the meaning of the format family.

### AC133-10: Package Compiler Can Consume Receipt

Given an approved program receipt, when the monthly package compiler requests still visual assets, then the compiler must retrieve asset code, format code, platform exports, source refs, approval refs, and preview asset without inspecting provider internals.

## 9. Dependencies

| Dependency | Type | Status |
|---|---|---|
| TS-CMF-095 | Tech spec | Required |
| TS-CMF-096 | Tech spec | Required for carousels |
| TS-CMF-097 | Tech spec | Required for carousel workflow |
| TS-CMF-098 | Tech spec | Required for carousel atlas |
| TS-CMF-099 | Tech spec | Required for single-image and SuperVisual runtime |
| TS-CMF-100 | Tech spec | Required for registry/schema parity |
| TS-CMF-101 | Tech spec | Required for format-family routing |
| TS-CMF-102 | Tech spec | Required for SuperVisual primitive contracts |
| TS-CMF-103 | Tech spec | Required for provider materialization |
| TS-CMF-104 | Tech spec | Required for Skia scene compilation |
| TS-CMF-105 | Tech spec | Required for eval/review fixtures |
| TS-CMF-121 | Tech spec | Required for manifest registry pattern |
| TS-CMF-128 | Tech spec | Required for runtime locking |
| TS-CMF-132 | Tech spec | Required for canonical stage review |
| `registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Registry | Required |
| `registries/composition/single_image_provider_responsibilities.v2.json` | Registry | Required |

## 10. Testing Strategy

### Unit Tests

1. Validate `StillVisualCompositionRequest` rejects missing guest workspace, Brand Context, source refs, target platform, and format code.
2. Validate `StillVisualFamilyRoute` cannot be created without router policy and atlas refs.
3. Validate provider plan rejects prohibited provider responsibility assignments.
4. Validate layer manifest rejects no text zones, no export variants, and missing typography contract.
5. Validate receipt assembly rejects missing render hash, eval refs, review decision, or approval receipt.

### Integration Tests

1. Create a carousel program and verify it calls carousel sequence, atlas, provider, Skia, eval, review, approval, and export stages.
2. Create a SuperVisual program and verify it routes through single-image router and SuperVisual grammar.
3. Create a visual poll and verify poll options, text budgets, and source evidence survive into the Skia scene.
4. Create a tweet-like quote and verify exact quote source refs are required.
5. Create a meme and verify source truth, safety, and primitive checks block generic unsupported claims.

### Golden Fixtures

Store fixtures under `THE CMF STUDIO/tests/fixtures/still_visuals/`:

| Fixture | Expected Result |
|---|---|
| `car_listicle_valid.json` | Approved after carousel atlas, primitive triad, and Skia render. |
| `supervisual_contrast_valid.json` | Approved after SuperVisual grammar and primitive triad. |
| `quote_no_source_invalid.json` | Blocks with `STILL_VISUAL_SOURCE_EVIDENCE_MISSING`. |
| `ideogram_final_text_invalid.json` | Blocks with `PROVIDER_RESPONSIBILITY_VIOLATION`. |
| `generic_premium_slop_invalid.json` | Blocks with `COMPOSITION_GENERIC_PREMIUM_SOCIAL_SLOP`. |

### Replay Tests

For each approved fixture, rerun deterministic render from stored scene refs and assert identical render hash. Provider jobs do not rerun during replay; only stored assets and locked registries may be used.

### Approval Gate Tests

1. Approval fails when primitive triad is incomplete.
2. Approval fails when review state is not `REVIEW_READY`.
3. Approval fails when human approval receipt is missing.
4. Approval succeeds only after all required receipts and export manifests exist.
