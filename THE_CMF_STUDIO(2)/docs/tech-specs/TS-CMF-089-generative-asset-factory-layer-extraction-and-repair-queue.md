---
tech_spec_id: "TS-CMF-089"
title: "Generative Asset Factory, Layer Extraction, and Repair Queue"
story_id: "7.19"
story_title: "Generative Asset Factory and Layer Extraction"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
updated_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition and Geometrics audit repair"
pipeline_stage: "2 / 10 / 11"
entry_object: "AssetGenerationRequest, CompositionLayoutPlan, GeometricsHandoffPlan"
exit_object: "LayerExtractionResult, LayerManifest, RepairJobReceipt, approved creative asset"
validation_contract: "provider role boundary, layerability, alpha/edge quality, SAM3/PRETEXT/Geometrics handoff, identity repair, approval"
required_receipt: "GenerativeAssetFactoryReceipt"
runtime_target: "Python / Pydantic v2 / ComfyUI worker / GPT Image 2 adapter / Flux 2 / Qwen-Image-Layered / SAM3 / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-089: Generative Asset Factory, Layer Extraction, and Repair Queue

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec protocol and build-readiness requirements. |
| `THE CMF STUDIO/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Audit requiring Qwen layered, SAM3 masks, safe zones, quadrilaterals, and Geometrics handoff readiness. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Asset factory, 64-state acting refs, avatar sheets, prop packs, layer extraction, repair edits, and render evals. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Provider role boundaries, Ideogram non-finality, layer extraction, and deterministic rendering doctrine. |
| `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` | Legacy CVE source for Qwen/VLM scoring, SAM3, PRETEXT, Geometrics, and Skia. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Existing composition lineage contracts consumed upstream. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Provider capability and receipt registry. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-044-generative-provider-adapters.md` | GPT Image 2, Flux 2, Qwen-Image-Layered, SAM3, LavaSR, and MOSS-TTS adapter boundary. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-045-self-hosted-comfyui-docker-gpu-worker.md` | ComfyUI Docker GPU worker deployment boundary. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Upstream Geometrics handoff source. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream consumer of layers, masks, safe zones, and quadrilaterals. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Primitive triad obligations that generated assets must preserve. |

## 2. Overview

This spec defines how generated or extracted visual material becomes production-safe CMF assets.

Allowed providers and workers include:

- GPT Image 2 for acting refs, expression sheets, mouth shapes, prop packs, style exploration, and repair edits;
- Flux 2 / Flux Kontext / Klein 9b for identity refinement, local repair, paper texture harmonization, and cleanup;
- self-hosted ComfyUI Docker workers on 24GB/32GB VRAM GPU machines for batch execution;
- Qwen-Image-Layered for decomposition and editable object proposals;
- SAM3 for subject masks, saliency maps, text safe zones, no-go zones, alpha masks, and surface quadrilaterals;
- See-Through-like tools for supplementary segmentation and transparency extraction.

Provider outputs are never final truth by themselves. They are candidate materials that must pass role, identity, layer, geometry, primitive, and receipt checks before any renderer consumes them.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-089-001 | `AssetGenerationRequest` | Requests candidate assets with provider, role, source refs, constraints, and expected layer roles. |
| DEP-CMF-089-002 | `GeometricsHandoffPlan` | Declares Qwen/SAM3/PRETEXT/Skia downstream requirements from TS-CMF-088. |
| DEP-CMF-089-003 | `GenerativeAssetFactoryJob` | Tracks provider job, prompt hash, worker receipt, source refs, and requested asset role. |
| DEP-CMF-089-004 | `QwenLayeredDecompositionReceipt` | Records layered decomposition result and confidence. |
| DEP-CMF-089-005 | `SAM3SaliencyReceipt` | Records subject masks, saliency maps, safe zones, no-go zones, and quadrilaterals. |
| DEP-CMF-089-006 | `LayerExtractionResult` | Canonical output consumed by Geometrics and renderer specs. |
| DEP-CMF-089-007 | `LayerManifest` | Stores layer URIs, alpha, bbox, anchor, z-index, shadow behavior, and motion affordance. |
| DEP-CMF-089-008 | `RepairJobReceipt` | Records queued repair work, provider, reason, and result. |
| DEP-CMF-089-009 | `GenerativeAssetFactoryReceipt` | Immutable receipt for provider role, inputs, outputs, and approval/block state. |

### Existing Backend Integration

| Backend Owner | Integration |
|---|---|
| `provider_capability_registry` | Register GPT Image 2, Flux 2, Klein 9b, Qwen-Image-Layered, SAM3, and ComfyUI capabilities. |
| `generative_provider_adapters` | Normalize provider requests/responses into CMF receipts. |
| `composition_service` | Supplies `GeometricsHandoffPlan` and source layout requirements. |
| `deterministic_rendering_service` | Consumes only approved layer/manifests and geometry-ready extraction results. |
| `doctrine_evaluation_service` | Blocks generated assets that violate identity, primitive, or route feel constraints. |
| `object_storage` | Stores raw outputs, extracted layers, masks, repaired assets, and manifests by scoped refs. |

### ADR-05 Primitives

Generated assets must preserve the primitive obligations already selected upstream. They do not get to invent new meaning.

| Rule | Enforcement |
|---|---|
| Minimum primitive count | At least three primitive refs must remain attached to approved generated assets. |
| Format/material primitive | Layer extraction must prove the visual material supports the declared format, such as Paper-Cut texture or cinematic light. |
| Evidence refs | Every approved output must reference source prompt, source image/video, or CompositionLayoutPlan. |
| Anti-slop | Assets that are pretty but do not activate the declared primitive route are repair-required or rejected. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Provider jobs block without source refs, role, expected layers, and primitive/eval context. |
| Phase4-M02 Cinematic Meaning | Generated assets must preserve declared meaning and visual function, not only aesthetics. |
| Phase4-M04 Frictionless Block | Weak layer separation, missing masks, bad alpha, or identity drift block before rendering. |
| Phase4-M05 Actionable Rejection | Every repair includes provider, failed score, failed layer, and repair instruction. |
| Phase5-M01 Verifiable Artifact | Every raw output, extraction, repair, and approval produces hashable receipts. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Qwen layered is a decomposition proposal. | It helps recover editable elements but must be validated by geometry and eval checks. |
| SAM3 is the geometry authority for masks and safe zones. | Geometrics cannot protect faces, hands, or key surfaces without masks and no-go zones. |
| Layer extraction result is canonical. | Renderers consume `LayerExtractionResult` and `LayerManifest`, not raw provider output. |
| Identity repair is explicit. | No provider may silently alter guest, interviewer, or brand likeness. |
| GPU workers are batch execution leaves. | They run jobs and shut down; they do not own product state. |

## 4. Implementation Plan

1. Add contracts for `GenerativeAssetFactoryJob`, `QwenLayeredDecompositionReceipt`, `SAM3SaliencyReceipt`, `LayerExtractionResult`, `LayerManifest`, and `RepairJobReceipt`.
2. Add provider capability records for GPT Image 2, Flux 2, Klein 9b, Qwen-Image-Layered, SAM3, and ComfyUI GPU worker modes.
3. Add `CreateGenerativeAssetFactoryJobCommand`.
4. Add `RunLayerExtractionCommand` that can use Qwen layered, SAM3, and supplementary segmentation.
5. Add `ValidateLayerExtractionCommand` with alpha, edge, separation, bbox, anchor, and geometry readiness scores.
6. Add `QueueAssetRepairCommand` for weak alpha, weak separation, identity drift, missing mask, or missing surface quadrilateral.
7. Add `ApproveGeneratedAssetCommand` that requires provider receipt, primitive refs, source refs, layer manifest, and no hard blockers.
8. Add object storage layout for raw outputs, layers, masks, repair results, and manifests.
9. Add fixtures for still visuals, Paper-Cut rigs, 64-state acting refs, and reaction UI assets.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class GenerativeAssetFactoryJob(BaseModel):
    schema_version: Literal["cmf.generative_asset_factory_job.v1"]
    job_id: UUID
    brand_id: UUID
    brand_context_version_id: UUID | None
    provider: Literal["gpt_image_2", "flux_2", "klein_9b", "qwen_image_layered", "sam3", "comfyui_docker"]
    requested_asset_role: str
    source_refs: list[str] = Field(min_length=1)
    prompt_hash: str
    negative_constraints: list[str]
    expected_layer_roles: list[str]
    provider_receipt_ref: str | None
    output_receipt_id: UUID | None


class QwenLayeredDecompositionReceipt(BaseModel):
    schema_version: Literal["cmf.qwen_layered_decomposition_receipt.v1"]
    receipt_id: UUID
    source_asset_id: UUID
    proposed_layers: list[dict]
    decomposition_confidence: float
    editable_object_count: int
    blocker_codes: list[str]


class SAM3SaliencyReceipt(BaseModel):
    schema_version: Literal["cmf.sam3_saliency_receipt.v1"]
    receipt_id: UUID
    source_asset_id: UUID
    subject_mask_refs: list[str]
    saliency_map_ref: str | None
    text_safe_zones: list[dict]
    object_no_go_zones: list[dict]
    surface_quadrilaterals: list[dict]
    blocker_codes: list[str]


class LayerManifestEntry(BaseModel):
    schema_version: Literal["cmf.layer_manifest_entry.v1"]
    layer_id: UUID
    layer_role: str
    file_uri: str
    alpha_mask_uri: str | None
    bbox: dict
    anchor_point: dict
    z_index: int
    shadow_behavior: str
    motion_affordance: list[str]
    alpha_quality_score: float
    edge_quality_score: float


class LayerExtractionResult(BaseModel):
    schema_version: Literal["cmf.layer_extraction_result.v1"]
    result_id: UUID
    source_asset_id: UUID
    layers: list[LayerManifestEntry]
    qwen_layered_receipt_ref: str | None
    sam3_saliency_receipt_ref: str | None
    segmentation_mask_refs: list[str]
    subject_mask_refs: list[str]
    text_safe_zones: list[dict]
    surface_quadrilaterals: list[dict]
    alpha_quality_score: float
    edge_quality_score: float
    layer_separation_score: float
    geometrics_ready: bool
    primitive_refs: list[str] = Field(min_length=3)
    repair_required: bool
    blocker_codes: list[str]


class RepairJobReceipt(BaseModel):
    schema_version: Literal["cmf.repair_job_receipt.v1"]
    receipt_id: UUID
    source_result_id: UUID
    repair_provider: str
    repair_reason: str
    requested_actions: list[str]
    output_result_id: UUID | None
    status: Literal["queued", "succeeded", "blocked", "failed"]
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Existing asset has no provider receipt | Mark candidate-only and block render with `PROVIDER_RECEIPT_MISSING`. |
| Existing cutout has weak alpha | Queue repair with `ALPHA_EDGE_QUALITY_LOW`. |
| Source asset has no SAM3 safe zones | Block Geometrics handoff with `SAM3_GEOMETRY_MISSING`. |
| Qwen layered separation is weak | Queue repair or manual layer extraction with `QWEN_LAYERED_DECOMPOSITION_WEAK`. |
| Identity drift detected | Block approval with `IDENTITY_REPAIR_REQUIRED`. |
| GPU worker receipt missing | Block approval with `GPU_WORKER_RECEIPT_MISSING`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T089-01 | Add contracts listed in Section 5. |
| T089-02 | Register provider capabilities and worker modes. |
| T089-03 | Implement generative job creation with source and role validation. |
| T089-04 | Implement Qwen layered decomposition adapter path. |
| T089-05 | Implement SAM3 saliency and safe-zone adapter path. |
| T089-06 | Implement layer manifest generation and quality scoring. |
| T089-07 | Implement repair queue and repair receipts. |
| T089-08 | Implement approval command with primitive and provider receipt gates. |
| T089-09 | Add object storage layout and hash validation. |
| T089-10 | Add positive and negative fixtures. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC089-01 | Every generated asset has provider receipt, prompt hash, and source refs. | Asset exists with no generation lineage. | Phase5-M01 |
| AC089-02 | Layer extraction emits layer manifest entries with alpha, bbox, anchor, z-index, shadow, and motion affordance. | Renderer receives a flattened image. | Phase4-M04 |
| AC089-03 | SAM3 masks, text safe zones, and quadrilaterals are present before Geometrics handoff. | Skia receives a flat image with no safe-zone evidence. | Phase4-M04 |
| AC089-04 | Weak alpha, edge, or separation scores queue repair. | Bad cutout edge is approved. | Phase4-M05 |
| AC089-05 | Provider boundaries block final baked text or identity drift. | GPT Image output becomes final identity. | Phase4-M01 |
| AC089-06 | Approved extraction result carries at least three primitive refs. | Pretty prop pack has no primitive evidence. | Phase4-M02 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Provider capability registry | `TS-CMF-042` |
| Generative provider adapters | `TS-CMF-044` |
| ComfyUI Docker GPU worker | `TS-CMF-045` |
| Ideogram bridge | `TS-CMF-088` |
| Renderer prop compiler | `TS-CMF-090` |
| Still visual Geometrics runtime | `TS-CMF-095` |
| Composition eval workbench | `TS-CMF-092` |

## 10. Testing Strategy

- Unit tests for provider role boundary validation.
- Unit tests for layer manifest quality thresholds.
- Qwen layered positive and negative decomposition fixtures.
- SAM3 safe-zone and quadrilateral required-field fixtures.
- Repair queue tests for alpha, edge, identity, missing mask, and weak separation failures.
- Integration test from `GeometricsHandoffPlan` to `LayerExtractionResult`.
- Receipt reconstruction tests for provider job, extraction, repair, and approval.
