---
tech_spec_id: "TS-CMF-095"
title: "Geometrics Still Visual Composition Runtime: Skia, SAM3, PRETEXT, and Qwen Layered"
story_id: "7.23"
story_title: "Still Visual Geometrics Runtime"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "Visual Geometrics audit repair"
pipeline_stage: "10 / 11 / 12"
entry_object: "CompositionLayoutPlan, LayerExtractionResult, AssetPackageItem, ProductionTextPlan"
exit_object: "GeometricsLayoutPlan, SkiaRenderJob, StillVisualRenderManifest, VisualTemplateRenderReceipt"
validation_contract: "primitive triads, masks, text safe zones, PRETEXT measurement, collision resolution, Skia render determinism, operator approval"
required_receipt: "VisualTemplateRenderReceipt"
runtime_target: "Python / Pydantic v2 / Qwen-Image-Layered / SAM3 / PRETEXT / Skia CanvasKit / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-095: Geometrics Still Visual Composition Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Defines the mandatory 10-section spec protocol, existing-backend mapping, primitives, and CBAR enforcement. |
| `THE CMF STUDIO/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Direct audit that identified the missing Skia/SAM3/PRETEXT still-visual runtime. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Legacy CVE/Geometrics source for SAM3 saliency, PRETEXT text measurement, 2D bin packing, Skia rendering, Rough.js aesthetics, and visual scoring. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_06_Conscious_Reactions.md` | Legacy proof that reaction mechanics output JSON state consumed by deterministic Skia rendering. |
| `D:\Work\The Conscious Coaching Factory\apps\animation-studio\app\scene-presets.ts` | Legacy scene/format matrix showing deterministic placement rather than loose manual canvas movement. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines asset codes for carousels, visual polls, tweet-like quotes, memes, Super Visuals, and reaction seeds. |
| `THE CMF STUDIO/src/ccp_studio/contracts/asset_package.py` | Current Guest Asset Pack item typing and package counts. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Current Ideogram CompositionJob, CompositionPlate, analysis, final text plan, and receipt contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Current composition service owner that must hand off to Geometrics rather than stop at Ideogram lineage. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Upstream bridge from Ideogram plates to production layout plans. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Upstream layer extraction, Qwen layered, SAM3, and repair queue. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Downstream renderer prop compiler and component registry. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Downstream eval and operator approval obligations. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Machine-loadable route triad registry requiring at least three primitive validations. |
| `https://github.com/rough-stuff/rough-notation` | Reference for hand-drawn annotation cue types used when still previews and video scenes need animated emphasis parity. |

## 2. Overview

CMF Studio needs a deterministic still-visual composition runtime for non-video assets:

- `CAR-LST` and `CAR-JUX` carousels;
- `VPL-WYR` and `VPL-VRS` visual polls;
- `TWQ-STD` and `TWQ-IMG` tweet-like quotes;
- `MEM-INC` and `MEM-REL` memes;
- `SPV-CON`, `SPV-SYM`, and `SPV-PRM` Super Visuals;
- still frames generated from reaction seeds when the output is not a video.

The runtime must not become a generic Canva-style editor or an HTML screenshot tool. It must preserve the old CVE doctrine:

```text
Ideogram 4 composition direction
-> Qwen-Image-Layered and SAM3 decomposition
-> PRETEXT typography measurement
-> Geometrics collision resolution
-> Skia render
-> vision/eval receipt
-> operator approval
```

Ideogram 4 creates a composition plate and layout intent. It is not final text, final identity, final geometry, or final output. The Geometrics runtime converts that intent into renderable coordinates, masks, safe zones, text measurements, material layers, annotation cues, and deterministic Skia outputs.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-095-001 | `AssetPackageItem` | Supplies package item, format family, source route, and production readiness. |
| DEP-CMF-095-002 | `CompositionLayoutPlan` | Supplies Ideogram-derived zones, subject placement, text-space map, prop placement, and usage state. |
| DEP-CMF-095-003 | `ProductionTextPlan` | Supplies final editable text layers; baked Ideogram text is not accepted. |
| DEP-CMF-095-004 | `LayerExtractionResult` | Supplies Qwen/SAM3 layer refs, masks, safe zones, quadrilaterals, bboxes, anchors, z-index, and quality scores. |
| DEP-CMF-095-005 | `PrimitiveTriadEvalReceipt` | Proves at least three exact primitive validations across meaning, delivery, and format/material roles. |
| DEP-CMF-095-006 | `GeometricsLayoutPlan` | Stores resolved coordinates, collision outcomes, typography measurements, masks, and variants. |
| DEP-CMF-095-007 | `TextAnnotationCueManifest` | Stores rough-notation-compatible underline, highlight, box, circle, strike-through, crossed-off, and bracket cues. |
| DEP-CMF-095-008 | `SkiaRenderJob` | Sealed job packet for headless Skia/CanvasKit still rendering. |
| DEP-CMF-095-009 | `StillVisualRenderManifest` | Stores output image refs, per-slide refs, hashes, dimensions, and preview/final parity. |
| DEP-CMF-095-010 | `VisualTemplateRenderReceipt` | Immutable receipt for source, geometry, render, eval, and approval evidence. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `contracts/asset_package.py` | Add explicit still visual subtype refs so `carousel`, `meme_visual`, and `poll_visual` can resolve to registry codes such as `CAR-LST`, `TWQ-STD`, or `SPV-CON`. |
| `contracts/composition.py` | Add downstream Geometrics linkage from `CompositionPlate` / `CompositionAnalysis` to `CompositionLayoutPlan` and `GeometricsLayoutPlan`. |
| `services/composition_service.py` | Add command path for `BuildGeometricsLayoutPlanCommand` after Ideogram bridge approval. |
| `TS-CMF-089` service owner | Supply Qwen/SAM3 layer and mask artifacts required by this runtime. |
| `TS-CMF-090` service owner | Compile Skia renderer props and annotation cue refs from the Geometrics plan. |
| `TS-CMF-092` workbench owner | Display geometry blockers, primitive blockers, and preview/final parity evidence to the operator. |

### ADR-05 Primitives

Every still visual template must load `registries/evals/composition/cmf_composition_primitive_triads.v1.json` and pass at least three primitive validations before preview render.

Required role coverage:

| Role | Meaning |
|---|---|
| `meaning_transform` | The composition changes meaning through story, contrast, analogy, inversion, proof, or stakes. |
| `delivery_shape` | The composition guides the viewer through the meaning using explanation, tension, recognition, rule of three, or social proof. |
| `format_material` | The composition's physical/formal style is justified: paper layer, cinematic light, eye path, visual density, human proof, or frame behavior. |

Examples by still format:

| Format | Useful Triad |
|---|---|
| `CAR-LST` | `PRM-PRS-032` Explanation Engine, `PRM-PRS-025` Rule of Three Message Architecture, `PRM-VSG-001` Composition as Eye-Path Engineering. |
| `VPL-WYR` / `VPL-VRS` | `PRM-PRS-015` What Is / What Could Be Contrast Engine, `PRM-HUM-021` Irony Inversion, `PRM-VSG-012` Frame as Active Meaning Device. |
| `TWQ-STD` / `TWQ-IMG` | `PRM-PRS-001` Strong Title as Idea Architecture, `PRM-VOC-006` Start Strong, End Strong, `PRM-VSG-021` Punctum, Air, and Felt Truth. |
| `MEM-INC` / `MEM-REL` | `PRM-HUM-021` Irony Inversion, `PRM-HUM-025` Analogy Bridge, `PRM-VSG-015` Composition as Attention Routing. |
| `SPV-CON` / `SPV-SYM` / `SPV-PRM` | `PRM-PRS-015` What Is / What Could Be Contrast Engine, `PRM-VSG-016` Light and Color as Emotional Architecture, `PRM-VSG-024` Space as Psychological Relationship. |

No composition may pass with fuzzy labels like "premium", "viral", or "clean". Exact primitive IDs or approved registry refs are required.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Render blocks without source route, locked brand context, primitive triad, layer extraction, and eval target. |
| Phase4-M02 Cinematic Meaning | Layout variants must preserve the source meaning operation, not only visual balance. |
| Phase4-M04 Frictionless Block | Geometry, layer, mask, and text failures stop before expensive Skia render. |
| Phase4-M05 Actionable Rejection | Every failure returns blocker code, object ref, coordinate/mask detail, and repair hint. |
| Phase5-M01 Verifiable Artifact | Every output is reconstructable from source refs, layout plan, renderer props, Skia job, and hashes. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Skia/CanvasKit is the production renderer for still visuals. | Still images need deterministic text geometry, masks, layers, and high-quality export. |
| PRETEXT owns text measurement before layout resolution. | DOM screenshots are too unstable for collision-free visual templates. |
| SAM3 safe zones outrank typography scale. | Faces, hands, symbolic objects, and critical product/scene surfaces must not be covered. |
| Ideogram is upstream direction only. | Final text, final identity, and final coordinates must be downstream and editable. |
| Qwen layered output is a candidate decomposition. | It must be validated against SAM3 masks and operator/eval gates before render. |
| Rough annotations are optional typed cues. | They may express emphasis but cannot replace primitive evidence or route fit. |

## 4. Implementation Plan

1. Add Pydantic contracts for `GeometricsLayoutPlan`, `GeometricsVariant`, `TextMeasurementBox`, `CollisionResolution`, `TextAnnotationCueManifest`, `SkiaRenderJob`, `StillVisualRenderManifest`, and `VisualTemplateRenderReceipt`.
2. Add content-format subtype resolution from `AssetPackageItem` to registry codes in `docs/content-asset-code-and-format-registry.md`.
3. Add `build_geometrics_layout_plan()` service method that consumes `CompositionLayoutPlan`, `ProductionTextPlan`, `LayerExtractionResult`, and primitive eval receipts.
4. Run SAM3 safe-zone checks and reject any layout without subject masks, text safe zones, and critical-object no-go zones.
5. Run PRETEXT text measurement for every editable text layer and produce line boxes, font metrics, overflow state, and minimum readable scale.
6. Run Geometrics solver with priority order:
   - subject masks and identity zones;
   - final text readability;
   - micro-semiotic anchors;
   - route-specific visual feel;
   - ornamental props;
   - annotation cues.
7. Generate 3-5 layout variants when there is more than one valid solution.
8. Score variants through primitive, readability, negative-space, attention-flow, route-fit, and brand-fit checks.
9. Create sealed `SkiaRenderJob` packets for single-frame, carousel slide set, stitched carousel preview, and platform export variants.
10. Emit `StillVisualRenderManifest` and `VisualTemplateRenderReceipt`.
11. Block operator approval unless preview/final hashes, primitive triad, geometry plan, and source lineage are present.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class TextMeasurementBox(BaseModel):
    schema_version: Literal["cmf.text_measurement_box.v1"]
    text_layer_id: UUID
    raw_text: str
    font_family: str
    font_size_px: float
    line_boxes: list[dict]
    measured_width_px: float
    measured_height_px: float
    min_readable_scale: float
    overflow: bool


class CollisionResolution(BaseModel):
    schema_version: Literal["cmf.collision_resolution.v1"]
    object_id: str
    object_type: Literal["text", "subject", "prop", "anchor", "annotation"]
    requested_bbox: dict
    resolved_bbox: dict
    blocked_by_refs: list[str]
    resolution_action: Literal["accepted", "moved", "scaled", "rewritten", "removed", "blocked"]
    reason: str


class TextAnnotationCue(BaseModel):
    schema_version: Literal["cmf.text_annotation_cue.v1"]
    cue_id: UUID
    text_layer_id: UUID
    annotation_type: Literal["underline", "highlight", "box", "circle", "strike-through", "crossed-off", "bracket"]
    start_frame: int
    end_frame: int
    color: str
    stroke_width_px: float
    roughness: float
    primitive_ref: str


class TextAnnotationCueManifest(BaseModel):
    schema_version: Literal["cmf.text_annotation_cue_manifest.v1"]
    manifest_id: UUID
    composition_layout_plan_id: UUID
    cues: list[TextAnnotationCue]
    preview_renderer: Literal["rough-notation", "motion_canvas", "remotion", "skia_canvaskit"]
    final_renderer: Literal["motion_canvas", "remotion", "skia_canvaskit"]
    cue_hash: str


class GeometricsVariant(BaseModel):
    schema_version: Literal["cmf.geometrics_variant.v1"]
    variant_id: UUID
    coordinates: dict
    text_measurements: list[TextMeasurementBox]
    collision_resolutions: list[CollisionResolution]
    primitive_scores: dict[str, float]
    readability_score: float
    attention_flow_score: float
    negative_space_score: float
    route_fit_score: float
    blocker_codes: list[str]


class GeometricsLayoutPlan(BaseModel):
    schema_version: Literal["cmf.geometrics_layout_plan.v1"]
    geometrics_layout_plan_id: UUID
    composition_layout_plan_id: UUID
    layer_extraction_result_id: UUID
    production_text_plan_id: UUID
    format_subtype_code: str
    width: int
    height: int
    aspect_ratio: str
    subject_mask_refs: list[str]
    text_safe_zones: list[dict]
    surface_quadrilaterals: list[dict]
    variants: list[GeometricsVariant]
    selected_variant_id: UUID | None
    annotation_cue_manifest_id: UUID | None
    primitive_refs: list[str] = Field(min_length=3)
    approved_for_skia_render: bool
    blocker_codes: list[str]


class SkiaRenderJob(BaseModel):
    schema_version: Literal["cmf.skia_render_job.v1"]
    skia_render_job_id: UUID
    geometrics_layout_plan_id: UUID
    selected_variant_id: UUID
    mode: Literal["single_image", "carousel_slide_set", "stitched_carousel_preview", "platform_export"]
    width: int
    height: int
    sealed_packet_uri: str
    sealed_packet_hash: str
    renderer_version: str
    expected_output_count: int


class StillVisualRenderManifest(BaseModel):
    schema_version: Literal["cmf.still_visual_render_manifest.v1"]
    manifest_id: UUID
    skia_render_job_id: UUID
    content_asset_code: str
    output_uris: list[str]
    output_hashes: list[str]
    width: int
    height: int
    format_subtype_code: str
    preview_hash: str
    final_hash: str
    nonblank_pixel_ratio: float
    status: Literal["rendered", "blocked", "failed"]
    blocker_codes: list[str]


class VisualTemplateRenderReceipt(BaseModel):
    schema_version: Literal["cmf.visual_template_render_receipt.v1"]
    receipt_id: UUID
    content_asset_id: UUID
    content_asset_code: str
    geometrics_layout_plan_id: UUID
    skia_render_job_id: UUID | None
    still_visual_render_manifest_id: UUID | None
    source_refs: list[str]
    primitive_eval_receipt_refs: list[str]
    provider_receipt_refs: list[str]
    input_hashes: dict[str, str]
    output_hashes: dict[str, str]
    approved_for_operator_review: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

Existing broad still-asset records may continue to exist, but they cannot be marked render-complete until they have a format subtype and Geometrics receipt.

| Condition | Fallback |
|---|---|
| Existing `carousel` item lacks subtype | Block with `FORMAT_SUBTYPE_REQUIRED`; operator chooses or route service resolves `CAR-LST` or `CAR-JUX`. |
| Ideogram plate has no usable layer plan | Use as reference only and block production render with `GEOMETRICS_LAYOUT_PLAN_MISSING`. |
| Qwen/SAM3 unavailable | Block final render; allow static reference preview only with `LAYER_GEOMETRY_UNAVAILABLE`. |
| PRETEXT measurement fails | Block with `TEXT_MEASUREMENT_FAILED`; no Skia render. |
| Skia worker unavailable | Block final output with `SKIA_RENDERER_UNAVAILABLE`; do not fallback to browser screenshot. |
| Rough annotation unsupported on final renderer | Drop annotation only if meaning and primitive eval still pass; otherwise block with `ANNOTATION_CUE_UNSUPPORTED`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T095-01 | Add contracts listed in Section 5. |
| T095-02 | Extend package item subtype resolution for all non-video formats. |
| T095-03 | Add Geometrics layout service and command handler. |
| T095-04 | Integrate Qwen/SAM3 artifacts from TS-CMF-089. |
| T095-05 | Add PRETEXT measurement adapter and overflow/rewrite blocker. |
| T095-06 | Add collision solver and constraint precedence rules. |
| T095-07 | Add Skia/CanvasKit sealed render job builder. |
| T095-08 | Add rough-notation-compatible annotation cue manifest support. |
| T095-09 | Add operator preview manifest and final export manifest. |
| T095-10 | Add eval receipt integration with primitive triads and doctrine gates. |
| T095-11 | Add golden fixtures for carousel, poll, tweet-like quote, meme, and Super Visual. |
| T095-12 | Add negative fixtures for face-covered text, missing masks, unreadable text, weak primitives, and browser-screenshot fallback. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC095-01 | Every still visual render has a registered format subtype code. | A `carousel` item renders without `CAR-LST` or `CAR-JUX`. | Phase5-M01 |
| AC095-02 | Every approved plan has at least three validated primitive refs with role coverage. | A poll passes with only a generic "engaging" label. | Phase4-M01 |
| AC095-03 | Every Skia render job has SAM3 masks, text safe zones, and surface quadrilaterals when source imagery is present. | Text overlays a guest face because no mask was available. | Phase4-M04 |
| AC095-04 | PRETEXT measurements exist for every final text layer. | Renderer guesses text size from character count. | Phase5-M01 |
| AC095-05 | Collision resolver records every move, scale, rewrite, removal, or block. | Text silently shrinks until unreadable. | Phase4-M05 |
| AC095-06 | Ideogram baked text cannot become final production text. | A generated plate with misspelled text is exported as final. | Phase4-M01 |
| AC095-07 | Preview and final output are generated from the same selected variant and sealed packet hash. | Operator approves one layout but final export uses another. | Phase5-M01 |
| AC095-08 | Rough annotation cues are frame-timed and deterministic when used. | Underline appears in preview but is missing in final. | Phase4-M02 |
| AC095-09 | Browser screenshot rendering is blocked as production fallback. | A headless browser screenshot is accepted when Skia is unavailable. | Phase4-M04 |
| AC095-10 | Output manifests include all hashes, output URIs, and reconstruction refs. | PNG exists with no render receipt. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Content asset code registry | `docs/content-asset-code-and-format-registry.md` |
| Ideogram CompositionJob lineage | `TS-CMF-038`, `TS-CMF-088` |
| Layer extraction and repair queue | `TS-CMF-089` |
| Renderer props and component registry | `TS-CMF-090` |
| Operator approval workbench | `TS-CMF-092` |
| Doctrine and primitive eval harness | `TS-CMF-077`, `TS-CMF-079` |
| Provider capability registry | `TS-CMF-042`, `TS-CMF-044` |
| Skia/CanvasKit worker | This spec plus implementation under deterministic rendering service boundary |

## 10. Testing Strategy

### Unit Tests

- Format subtype resolution for `CAR`, `VPL`, `TWQ`, `MEM`, `SPV`, and `RCT`.
- PRETEXT measurement overflow and readable-scale tests.
- SAM3 mask/safe-zone required-field tests.
- Collision resolution priority tests.
- Primitive triad loading and blocker tests.
- Rough annotation cue hash tests.

### Integration Tests

- Ideogram layout plan -> Qwen/SAM3 extraction -> Geometrics layout -> Skia job.
- Carousel slide set render with stitched preview.
- Visual poll two-option render with safe subject/text zones.
- Tweet-like quote render with editable text layers.
- Meme render with humor/primitive evidence and no identity drift.
- Super Visual render with micro-semiotic anchor and negative-space scoring.

### Golden Fixtures

| Fixture | Required Proof |
|---|---|
| `golden_car_lst_learning_sequence` | Text hierarchy, slide continuity, primitive triad, stitched preview. |
| `golden_vpl_wyr_split_choice` | Two-option contrast, eye path, no text collision. |
| `golden_twq_img_quote` | Editable quote text, identity-safe portrait placement, platform readability. |
| `golden_mem_rel_recognition` | Valid meme mechanism, recognition primitive, no unsafe distortion. |
| `golden_spv_con_symbolic_contrast` | Strong metaphor, safe negative space, anchor effectiveness. |

### Negative Fixtures

- Missing format subtype.
- Fewer than three primitive validations.
- Text over face or key object.
- PRETEXT overflow unresolved.
- Ideogram baked text used as final.
- Qwen layered result with weak separation.
- Skia worker unavailable and browser screenshot attempted.
- Annotation cue mismatch between preview and final.

### Spec Audit Receipt

Implementation cannot be marked complete until a `VisualTemplateRenderReceipt` proves:

- source expression lineage;
- format subtype;
- primitive triad receipt;
- Ideogram layout lineage;
- Qwen/SAM3/PRETEXT/Geometrics evidence;
- Skia render job hash;
- preview/final parity;
- operator approval state.
