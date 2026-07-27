---
tech_spec_id: "TS-CMF-096"
title: "Carousel Slide Composition Library and Sequence Builder"
story_id: "7.24"
story_title: "Carousel Slide Composition Library"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "Carousel slide composition library repair"
pipeline_stage: "8 / 10 / 11 / 12"
entry_object: "AssetPackageItem, ExpressionMoment, PrimitiveTriadEvalReceipt, BrandContextVersion"
exit_object: "CarouselSequencePlan, CarouselSlideCompositionPlan, CarouselCompositionLibraryReceipt"
validation_contract: "slide atom selection, composition meaning, primitive triad, sequence arc, grid continuity, shot variety, atlas routing readiness"
required_receipt: "CarouselCompositionLibraryReceipt"
runtime_target: "Python / Pydantic v2 / JSON registry loader / Geometrics / Skia CanvasKit"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-096: Carousel Slide Composition Library and Sequence Builder

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec protocol and build-readiness requirements. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines `CAR-LST` and `CAR-JUX`. |
| `THE CMF STUDIO/docs/composition-libraries/CMF_Carousel_Slide_Composition_Library.md` | Human-readable slide library doctrine. |
| `THE CMF STUDIO/registries/composition/carousel_slide_composition_library.v1.json` | Machine-readable slide atom registry. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-003.yaml` | Narrative Structural Backbone, required for sequence arc. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-012.yaml` | Grid as Cognitive Relief, required for carousel continuity. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-018.yaml` | Sequence Over Single Image, required for slide variety. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | Eye-path engineering, required per slide. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/persuasion/PRM-PRS-032.yaml` | Explanation Engine, required for teaching slides. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/persuasion/PRM-PRS-015.yaml` | What Is / What Could Be Contrast Engine, required for juxtaposition slides. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream Geometrics/Skia renderer path for still visuals. |

## 2. Overview

CMF already recognizes carousel format codes, but format codes are not enough. A carousel needs a queryable slide-level composition library where every slide atom has:

- a stable code;
- a composition meaning;
- allowed sequence positions;
- compatible carousel format codes;
- primitive triad defaults;
- visual grammar;
- geometry requirements;
- query tags.

This spec defines how agents select slide atoms and assemble them into a `CarouselSequencePlan` that the TS-CMF-098 atlas router can convert into concrete visual grammar before downstream Geometrics and Skia rendering.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-096-001 | `carousel_slide_composition_library.v1.json` | Queryable source of slide atoms and sequence blueprints. |
| DEP-CMF-096-002 | `AssetPackageItem` | Supplies carousel package item and format subtype. |
| DEP-CMF-096-003 | `ExpressionMoment` | Supplies source quote, edge product, audience recognition point, and route. |
| DEP-CMF-096-004 | `PrimitiveTriadEvalReceipt` | Supplies at least three validated primitive refs. |
| DEP-CMF-096-005 | `CarouselSlideCompositionPlan` | Per-slide plan with atom, source refs, text, geometry intent, and primitive evidence. |
| DEP-CMF-096-006 | `CarouselSequencePlan` | Ordered sequence of slide plans and arc validation. |
| DEP-CMF-096-007 | `CarouselAtlasRoutingInput` | Downstream TS-CMF-098 input proving each slide atom is ready for visual grammar routing before Geometrics. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `asset_package.py` | Carousel items must resolve to `CAR-LST` or `CAR-JUX`. |
| `composition_service.py` | Carousel sequence plan becomes input to TS-CMF-098 composition routing before any Geometrics runtime call. |
| `doctrine_evaluation_service.py` | Validates primitive triads and sequence blockers. |
| `deterministic_rendering_service.py` | Receives carousel render jobs only after TS-CMF-098 atlas routing and TS-CMF-095 Geometrics/Skia preparation. |

### ADR-05 Primitives

Each slide must have at least three primitive validations. The carousel sequence must also prove:

| Sequence Requirement | Primitive |
|---|---|
| Meaning arc | `PRM-BUS-003` Narrative Structural Backbone |
| Grid continuity | `PRM-BUS-012` The Grid as Cognitive Relief |
| Slide variety | `PRM-VSG-018` Sequence Over Single Image |
| Per-slide scan path | `PRM-VSG-001` Composition as Eye-Path Engineering |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Blocks sequence planning without source Expression Moment, format subtype, and primitive receipt. |
| Phase4-M02 Cinematic Meaning | Each slide must declare a composition meaning and source role. |
| Phase4-M04 Frictionless Block | Unknown slide atom, invalid position, flat arc, or missing grid continuity blocks before render. |
| Phase4-M05 Actionable Rejection | Blockers name slide index, atom code, failed primitive, and repair instruction. |
| Phase5-M01 Verifiable Artifact | Sequence plan, slide plans, registry version, and render outputs are hashable. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Slide atoms are registry records. | Agents can query and reuse them instead of inventing slide layouts every time. |
| Composition meaning is required. | Prevents decorative slides and generic template thinking. |
| Sequence blueprints are optional accelerators. | They help common cases but should not override source-specific primitive routing. |
| Atlas routing remains downstream of this spec. | Slide library decides meaning and sequence role; TS-CMF-098 decides concrete visual grammar; Geometrics decides exact coordinates. |

## 4. Implementation Plan

1. Add registry loader for `registries/composition/carousel_slide_composition_library.v1.json`.
2. Add `CarouselSlideAtom`, `CarouselSlideCompositionPlan`, `CarouselSequencePlan`, and receipt contracts.
3. Add query method by format, primitive, composition meaning, allowed position, and query tags.
4. Add sequence builder that can use a blueprint or assemble atoms dynamically.
5. Add validation for slide positions, primitive triads, grid continuity, shot variety, and arc progression.
6. Add bridge to TS-CMF-098 so each slide plan emits atlas-routing-ready input; Geometrics handoff occurs only after `CompositionRouterDecision`.
7. Add tests for `CAR-LST` and `CAR-JUX` blueprints and negative fixtures.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class CarouselSlideAtom(BaseModel):
    schema_version: Literal["cmf.carousel_slide_atom.v1"]
    slide_atom_code: str
    display_name: str
    composition_meaning: str
    allowed_positions: list[str]
    compatible_format_codes: list[str]
    default_primitive_triads: list[dict]
    visual_grammar: dict
    query_tags: list[str]


class CarouselSlideCompositionPlan(BaseModel):
    schema_version: Literal["cmf.carousel_slide_composition_plan.v1"]
    slide_plan_id: UUID
    slide_index: int
    slide_atom_code: str
    content_asset_code: str
    source_expression_moment_id: UUID
    format_code: Literal["CAR-LST", "CAR-JUX"]
    composition_meaning: str
    final_text_layer_refs: list[str]
    visual_asset_refs: list[str]
    primitive_refs: list[str] = Field(min_length=3)
    visual_grammar: dict
    composition_router_decision_id: UUID | None
    blocker_codes: list[str]


class CarouselSequencePlan(BaseModel):
    schema_version: Literal["cmf.carousel_sequence_plan.v1"]
    sequence_plan_id: UUID
    content_asset_code: str
    format_code: Literal["CAR-LST", "CAR-JUX"]
    blueprint_code: str | None
    registry_version: str
    slides: list[CarouselSlideCompositionPlan]
    sequence_arc: list[str]
    grid_continuity_passed: bool
    shot_variety_passed: bool
    primitive_coverage_passed: bool
    approved_for_atlas_routing: bool
    blocker_codes: list[str]


class CarouselCompositionLibraryReceipt(BaseModel):
    schema_version: Literal["cmf.carousel_composition_library_receipt.v1"]
    receipt_id: UUID
    sequence_plan_id: UUID
    registry_id: str
    registry_hash: str
    selected_atom_codes: list[str]
    primitive_eval_receipt_refs: list[str]
    approved_for_render: bool
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Existing carousel has no slide atom plan | Block render with `CAROUSEL_SLIDE_MEANING_MISSING`. |
| Existing carousel lacks subtype | Block with `FORMAT_SUBTYPE_REQUIRED`. |
| A slide uses unknown atom code | Block with `CAROUSEL_SLIDE_ATOM_UNKNOWN`. |
| Same slide grammar repeats without sequence reason | Block with `CAROUSEL_SHOT_VARIETY_MISSING`. |
| Sequence lacks arc | Block with `CAROUSEL_SEQUENCE_ARC_FLAT`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T096-01 | Add carousel registry loader. |
| T096-02 | Add contracts listed in Section 5. |
| T096-03 | Add atom query service. |
| T096-04 | Add sequence builder for blueprint and dynamic modes. |
| T096-05 | Add primitive triad, grid, and shot variety validators. |
| T096-06 | Add TS-CMF-098 atlas-router handoff per slide. |
| T096-07 | Add positive and negative fixtures. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC096-01 | Every carousel slide has a known slide atom code. | Slide 3 is just `layout_03`. | Phase5-M01 |
| AC096-02 | Every slide declares composition meaning. | Slide exists only because the carousel needed another page. | Phase4-M02 |
| AC096-03 | Every slide has at least three primitive refs. | A slide says "premium educational" without primitive IDs. | Phase4-M01 |
| AC096-04 | Sequence validates grid continuity and visual variety. | Ten slides reuse the same medium-shot layout. | Phase4-M04 |
| AC096-05 | `CAR-JUX` sequences include a contrast-bearing atom. | Juxtaposition carousel has no actual contrast slide. | Phase4-M02 |
| AC096-06 | Approved sequences produce atlas-router-ready slide plans. | Registry plan tries to render without a `CompositionRouterDecision`. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Content asset code registry | `docs/content-asset-code-and-format-registry.md` |
| Carousel slide registry | `registries/composition/carousel_slide_composition_library.v1.json` |
| Still visual Geometrics runtime | `TS-CMF-095` |
| Carousel composition atlas and router | `TS-CMF-098` |
| Composition eval workbench | `TS-CMF-092` |
| Primitive triad eval registry | `registries/evals/composition/cmf_composition_primitive_triads.v1.json` |

## 10. Testing Strategy

- Registry JSON schema validation.
- Query tests by format, primitive, composition meaning, and position.
- Blueprint tests for explanation, juxtaposition, and pattern-break sequences.
- Negative tests for unknown atom, invalid position, missing primitive triad, flat arc, missing grid continuity, and missing Geometrics plan.
- Golden fixture for one `CAR-LST` and one `CAR-JUX` sequence that can be consumed by TS-CMF-098 without direct Geometrics assumptions.
