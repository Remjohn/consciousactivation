---
tech_spec_id: "TS-CMF-088"
title: "Ideogram 4 Composition Director to Production Template Bridge"
story_id: "7.18"
story_title: "Ideogram to Production Template Bridge"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and Geometrics audit repair"
pipeline_stage: "10"
entry_object: "SceneSpec, VisualFeelContract, Ideogram CompositionJob, CompositionPlate"
exit_object: "CompositionLayoutPlan, ProductionTextPlan, GeometricsHandoffPlan"
validation_contract: "layout extraction, final text boundary, identity boundary, anchor placement, Geometrics handoff readiness"
required_receipt: "IdeogramProductionBridgeReceipt"
runtime_target: "Python / Pydantic v2 / provider adapter / Qwen-Image-Layered request / SAM3/PRETEXT/Skia handoff / object storage / review UI"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-088: Ideogram 4 Composition Director to Production Template Bridge

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec protocol and build-readiness requirements. |
| `THE CMF STUDIO/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Audit that found the missing Ideogram-to-Geometrics handoff. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Ideogram role, Brand Genesis substrate, 64-state acting, Paper-Cut, micro-semiotic anchors, and renderer routing. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Defines Ideogram as composition-control provider, not final renderer or text authority. |
| `THE CMF STUDIO/CCP V9 - Interview-First Expression Engine.md` | Requires Expression Moment and Interview Asset Contract lineage to drive downstream render choices. |
| `THE CMF STUDIO/CCP V9.1 - Expression Capture & Archetype Routing Update.md` | Requires Complete Expression Session, route, asset derivative, and CMF handoff evidence. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Legacy CVE source for Geometrics, SAM3, PRETEXT, Skia, and final visual validation. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Existing CompositionJob, CompositionPlate, CompositionAnalysis, FinalTextPlan, and receipt contracts to extend. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Current CompositionService owner for Ideogram job compilation, submission, and boundary evaluation. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-038-ideogram-4-compositionjob-lineage.md` | Existing Ideogram CompositionJob lineage spec. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Downstream Qwen/SAM3/layer extraction dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream Geometrics still visual runtime dependency. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Primitive triad rules that must travel into production layout planning. |

## 2. Overview

Ideogram 4 is CMF Studio's composition director. It can propose visual hierarchy, subject placement, text area, paper-strip arrangement, prop density, metaphor, color balance, and micro-semiotic anchor placement.

It must not become:

- final identity renderer;
- final text renderer;
- final coordinate authority;
- final source of truth for Brand Context;
- a shortcut around Qwen/SAM3/PRETEXT/Geometrics/Skia validation.

This bridge converts a `CompositionPlate` and `CompositionAnalysis` into production-safe layout objects:

```text
CompositionJob
-> CompositionPlate
-> CompositionLayoutPlan
-> ProductionTextPlan
-> GeometricsHandoffPlan
```

The handoff plan declares what Qwen-Image-Layered should decompose, what SAM3 must validate, what PRETEXT must measure, and what Skia/CanvasKit may render.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-088-001 | `SceneSpec` | Supplies source editing session, route, platform, aspect ratio, asset selections, and render contract refs. |
| DEP-CMF-088-002 | `VisualFeelContract` | Supplies route-specific feel, primitive obligations, and anti-slop constraints. |
| DEP-CMF-088-003 | `CompositionJob` | Supplies Ideogram prompt hash, constraints, output requirements, selected brand layer refs, and lineage hash. |
| DEP-CMF-088-004 | `CompositionPlate` | Supplies plate URI/hash, usage state, provider receipt, and analysis ref. |
| DEP-CMF-088-005 | `CompositionAnalysis` | Supplies text-space, identity drift, baked text risk, layerability, style fit, and flow scoring. |
| DEP-CMF-088-006 | `CompositionLayoutPlan` | Extracted production layout plan for zones, placements, flow, and handoff requirements. |
| DEP-CMF-088-007 | `ProductionTextPlan` | Final editable text plan rendered downstream, not by Ideogram. |
| DEP-CMF-088-008 | `GeometricsHandoffPlan` | Handoff object for Qwen layered, SAM3, PRETEXT, and Skia readiness. |
| DEP-CMF-088-009 | `IdeogramProductionBridgeReceipt` | Receipt recording all boundary decisions and blockers. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `contracts/composition.py` | Add `CompositionLayoutPlan`, `ProductionTextPlan` extensions, `GeometricsHandoffPlan`, and bridge receipt fields. |
| `services/composition_service.py` | Add commands to extract layout plans, build production text plans, declare Geometrics handoff, and block unsafe plates. |
| `repositories/composition.py` | Persist layout plans, handoff plans, and bridge receipts. |
| `providers/ideogram.py` | Remains provider adapter only; it does not approve final text or identity. |
| `doctrine_evaluation_service.py` | Validates primitive triad and route feel before bridge approval. |

### ADR-05 Primitives

The bridge does not create primitive obligations, but it must carry them forward and reject layout plans that lose them.

Required primitive evidence:

| Requirement | Enforcement |
|---|---|
| Minimum count | At least three primitive refs from `cmf_composition_primitive_triads.v1.json`. |
| Role coverage | Meaning transform, delivery shape, and format/material roles must all survive bridge extraction. |
| Element binding | Each major layout element must map to a primitive role or source evidence. |
| Route feel | Bridge output must preserve route-specific feel from TS-CMF-079. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Blocks bridge approval without source lineage, route feel, primitive triad, and valid plate usage state. |
| Phase4-M02 Cinematic Meaning | Layout extraction must preserve meaning-bearing elements, not only visual balance. |
| Phase4-M04 Frictionless Block | Baked text, identity drift, missing handoff, or screenshot fallback risk block before downstream rendering. |
| Phase4-M05 Actionable Rejection | Blockers include failed object, failed score, repair target, and downstream consequence. |
| Phase5-M01 Verifiable Artifact | Bridge receipt records prompt hash, plate hash, analysis ref, layout hash, text plan hash, and handoff hash. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Ideogram remains upstream direction. | It is valuable for composition intuition but unsafe as final production truth. |
| Final text is downstream and editable. | Prevents baked text typos, localization failure, and inaccessible text layers. |
| Identity boundaries are strict. | Guest, interviewer, and brand likeness must come from approved source/asset refs. |
| Geometrics handoff is required for production visuals. | Qwen/SAM3/PRETEXT/Skia need explicit instructions, not inferred screenshots. |
| Browser screenshot production fallback is blocked. | It violates the old CVE doctrine and weakens reproducibility. |

## 4. Implementation Plan

1. Extend composition contracts with `CompositionLayoutPlan`, `GeometricsHandoffPlan`, and `IdeogramProductionBridgeReceipt`.
2. Add `ExtractIdeogramLayoutPlanCommand`.
3. Add layout extraction from `CompositionPlate` and `CompositionAnalysis`.
4. Add `ValidateIdeogramBoundaryCommand` for baked text, identity drift, missing text space, and unsupported usage states.
5. Add `BuildProductionTextPlanCommand` that creates editable text layers and rejects baked text as final.
6. Add `BuildGeometricsHandoffCommand` that specifies Qwen layered candidates, SAM3 safe-zone requirements, PRETEXT measurement requirements, and Skia candidate state.
7. Add bridge blockers and repair instructions.
8. Add receipt generation with all input and output hashes.
9. Add tests for accepted layout, background-only layout, repair-required layout, rejected layout, and screenshot fallback attempts.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class CompositionLayoutPlan(BaseModel):
    schema_version: Literal["cmf.composition_layout_plan.v1"]
    layout_plan_id: UUID
    composition_job_id: UUID
    composition_plate_id: UUID
    template_family_code: str
    zones: list[dict]
    text_space_map: dict
    subject_placement: dict
    prop_placement: list[dict]
    micro_semiotic_anchor_placement: list[dict]
    visual_flow_notes: list[str]
    layer_extraction_candidates: list[str]
    qwen_layered_decomposition_required: bool = True
    sam3_safe_zone_required: bool = True
    pretext_measurement_required: bool = True
    geometrics_handoff_required: bool = True
    skia_render_candidate: bool = True
    primitive_refs: list[str] = Field(min_length=3)
    usage_state: Literal["approved_layout", "background_only", "repair_required", "rejected"]
    blocker_codes: list[str]


class ProductionTextPlan(BaseModel):
    schema_version: Literal["cmf.production_text_plan.v1"]
    text_plan_id: UUID
    layout_plan_id: UUID
    final_text_layers: list[dict]
    localization_ready: bool
    platform_caption_variants: list[dict]
    baked_text_risk: float
    renderer_route: Literal["skia_canvaskit", "remotion", "motion_canvas", "manim"]
    approved_for_downstream_render: bool


class GeometricsHandoffPlan(BaseModel):
    schema_version: Literal["cmf.geometrics_handoff_plan.v1"]
    handoff_plan_id: UUID
    layout_plan_id: UUID
    qwen_layered_targets: list[dict]
    sam3_required_outputs: list[Literal["subject_masks", "text_safe_zones", "surface_quadrilaterals", "saliency_map"]]
    pretext_text_layer_ids: list[UUID]
    skia_candidate: bool
    still_visual_runtime_required: bool
    video_runtime_required: bool
    handoff_hash: str
    blocker_codes: list[str]


class IdeogramProductionBridgeReceipt(BaseModel):
    schema_version: Literal["cmf.ideogram_production_bridge_receipt.v1"]
    receipt_id: UUID
    composition_job_id: UUID
    composition_plate_id: UUID
    layout_plan_id: UUID | None
    production_text_plan_id: UUID | None
    geometrics_handoff_plan_id: UUID | None
    input_hashes: dict[str, str]
    output_hashes: dict[str, str]
    approved_for_geometrics: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Plate has strong composition but identity drift | Mark `background_only` or `repair_required`; do not use likeness. |
| Plate has strong layout but baked final text | Extract layout only and rebuild all text downstream. |
| Layout extraction confidence is weak | Block with `IDEOGRAM_LAYOUT_PLAN_MISSING`; request another plate or operator repair. |
| Geometrics handoff is incomplete | Block with `GEOMETRICS_HANDOFF_MISSING`; no downstream render job. |
| Still visual renderer tries browser screenshot | Block with `BROWSER_SCREENSHOT_RENDER_RISK`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T088-01 | Add bridge contracts and repository methods. |
| T088-02 | Implement layout extraction command. |
| T088-03 | Implement identity and baked-text boundary validation. |
| T088-04 | Implement editable production text plan creation. |
| T088-05 | Implement Geometrics handoff plan creation. |
| T088-06 | Add primitive triad propagation checks. |
| T088-07 | Add blocker and repair instruction generation. |
| T088-08 | Add bridge receipt generation. |
| T088-09 | Add tests for accepted, background-only, repair, and rejected paths. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC088-01 | Every Ideogram plate has layout plan, usage state, and receipt before downstream use. | Only an image URL is stored. | Phase5-M01 |
| AC088-02 | Final text plan is editable and renderer-owned. | AI text baked into final output. | Phase4-M01 |
| AC088-03 | Identity drift restricts or rejects plate use. | Generated face becomes final guest likeness. | Phase4-M04 |
| AC088-04 | Micro-semiotic anchors are mapped or explicitly blocked. | Anchor disappears after rebuild. | Phase4-M02 |
| AC088-05 | Every production layout declares Qwen/SAM3/PRETEXT/Skia handoff. | Plate is approved with no Geometrics readiness. | Phase5-M01 |
| AC088-06 | Browser screenshot production path is blocked. | Layout is rendered through headless DOM capture. | Phase4-M04 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Ideogram CompositionJob lineage | `TS-CMF-038` |
| Composition template runtime spine | `TS-CMF-080` |
| Generative layer extraction | `TS-CMF-089` |
| Renderer prop compiler | `TS-CMF-090` |
| Still visual Geometrics runtime | `TS-CMF-095` |
| Composition eval workbench | `TS-CMF-092` |

## 10. Testing Strategy

- Unit tests for boundary validation and usage-state transitions.
- Schema tests for `CompositionLayoutPlan`, `ProductionTextPlan`, and `GeometricsHandoffPlan`.
- Negative fixtures for baked text, identity drift, missing anchor placement, missing text space, missing handoff, and browser screenshot fallback.
- Integration test from `CompositionPlate` to `GeometricsHandoffPlan`.
- Receipt hash tests proving bridge outputs can be reconstructed from source inputs.
