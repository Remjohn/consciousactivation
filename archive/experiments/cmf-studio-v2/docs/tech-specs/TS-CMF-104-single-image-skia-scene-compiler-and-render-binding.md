---
tech_spec_id: "TS-CMF-104"
title: "Single Image Skia Scene Compiler and Render Binding"
story_id: "7.27E"
story_title: "Single Image Deterministic Render Runtime"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "11 / 12"
entry_object: "SingleImageRouterDecision, SingleImageLayerMaterializationReceipt, ProductionTextPlan, BrandContextVersion"
exit_object: "SingleImageSceneSpecV2, GeometricsLayoutPlan, SkiaRenderReceipt"
validation_contract: "normalized zones, text budgets, editable final text, PRETEXT measurements, Skia component catalog, masks, annotation cues, output hashes"
required_receipt: "SkiaRenderReceipt"
runtime_target: "Python / PRETEXT / Geometrics / Skia CanvasKit / Rough Annotation Manifest"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-104: Single Image Skia Scene Compiler and Render Binding

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream deterministic still render runtime. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | SceneSpec and render receipt requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md` | Provider output dependency. |
| `THE CMF STUDIO/registries/composition/single_image_skia_component_catalog.v2.json` | Allowed component catalog. |
| `THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json` | Zones and text budgets. |

## 2. Overview

This spec compiles a selected single-image composition into deterministic renderer truth. Generative plates and assets are inputs. Final text, typography, geometry, component selection, borders, panels, poll UI, scorecards, annotations, and export hashes are owned by the Skia scene compiler.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-104-001 | `SingleImageLayerMaterializationReceipt` | Supplies approved assets, masks, layers, and hashes. |
| DEP-CMF-104-002 | `ProductionTextPlan` | Supplies final editable text. |
| DEP-CMF-104-003 | `single_image_skia_component_catalog.v2.json` | Allows only registered Skia components. |
| DEP-CMF-104-004 | `SingleImageSceneSpecV2` | Canonical JSON/timeline-less still scene spec. |
| DEP-CMF-104-005 | `SkiaRenderReceipt` | Final render proof. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/services/single_image_compiler_service.py` | Builds scene spec and Geometrics handoff. |
| `src/ccp_studio/services/geometrics_layout_service.py` | Resolves exact positions, text measurement, collisions, and safe zones. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Executes Skia still render. |
| `src/ccp_studio/services/review_state_service.py` | Exposes final preview and render evidence. |

### ADR-05 Primitives

The compiler must carry primitive refs into every scene spec and annotation cue. Rough annotation is allowed only when it performs one of the approved semantic jobs and references a primitive.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase1-M05 Deterministic Override | Skia owns final layout and text. |
| Phase4-M02 Cinematic Meaning | Scene spec preserves selected meaning operation and visual feel. |
| Phase4-M04 Frictionless Block | Text overflow, missing mask, unknown component, or invalid zone blocks before final render. |
| Phase5-M01 Verifiable Artifact | Render receipt stores scene hash, font hash, asset hashes, and output SHA. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| SceneSpec is JSON truth. | Generated preview images are artifacts, not source of truth. |
| PRETEXT precedes Skia render. | Text must be measured before final composition. |
| Skia component catalog is closed. | Prevents arbitrary UI drift and unreproducible layouts. |

## 4. Implementation Plan

1. Add scene compiler from router decision and provider receipt.
2. Validate selected composition zones and text budgets.
3. Load final `ProductionTextPlan`.
4. Validate Skia component catalog refs.
5. Run PRETEXT measurement and collision checks.
6. Create `GeometricsLayoutPlan`.
7. Compile sealed Skia render packet.
8. Render final image.
9. Emit `SkiaRenderReceipt`.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageSceneCompileReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_scene_compile_receipt.v1"]
    receipt_id: UUID
    scene_spec_id: UUID
    geometrics_layout_plan_id: UUID
    skia_render_job_id: UUID
    scene_spec_hash: str
    approved_for_render: bool
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Final text absent | Block with `SINGLE_IMAGE_FINAL_TEXT_REQUIRED`. |
| Unknown Skia component | Block with `SINGLE_IMAGE_SKIA_COMPONENT_UNKNOWN`. |
| PRETEXT overflow unresolved | Block with `SINGLE_IMAGE_TEXT_BUDGET_EXCEEDED`. |
| Skia worker unavailable | Block with `SKIA_RENDER_RECEIPT_REQUIRED`; no browser screenshot fallback. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T104-01 | Add scene compiler service. |
| T104-02 | Add component catalog validator. |
| T104-03 | Add PRETEXT and Geometrics handoff. |
| T104-04 | Add sealed Skia render packet generation. |
| T104-05 | Add render receipt validation. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC104-01 | Final text is editable and Skia-owned. | Baked Ideogram text is final. | Phase1-M05 |
| AC104-02 | Every scene spec uses registered components. | Renderer calls arbitrary custom panel component. | Phase5-M01 |
| AC104-03 | PRETEXT blocks overflow before render. | Tiny text is exported unreadably. | Phase4-M04 |
| AC104-04 | Render receipt includes all reconstruction hashes. | PNG exists but scene cannot be reproduced. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Geometrics still runtime | `TS-CMF-095` |
| Provider materialization | `TS-CMF-103` |
| Renderer prop compiler | `TS-CMF-090` |
| Approval workbench | `TS-CMF-092` |

## 10. Testing Strategy

- Unit tests for component catalog validation.
- PRETEXT overflow fixture.
- Missing mask fixture.
- Skia render receipt hash fixture.
- Negative browser screenshot fallback fixture.
