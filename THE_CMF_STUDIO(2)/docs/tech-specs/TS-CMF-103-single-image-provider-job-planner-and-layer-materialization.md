---
tech_spec_id: "TS-CMF-103"
title: "Single Image Provider Job Planner and Layer Materialization"
story_id: "7.27D"
story_title: "Single Image Provider Materialization"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "10 / 11"
entry_object: "SingleImageRouterDecision, SuperVisualCompositionBrief, SingleImageRegistryBundle"
exit_object: "SingleImageProviderJobPlan, SingleImageLayerMaterializationReceipt"
validation_contract: "provider responsibility policy, Ideogram textless plates, GPT Image 2 assets, Flux repairs, Qwen layered outputs, SAM3 masks, asset hashes, source fidelity"
required_receipt: "SingleImageLayerMaterializationReceipt"
runtime_target: "Python / Provider adapters / Ideogram 4 / GPT Image 2 / Flux 2 Klein / Qwen-Image-Layered / SAM3"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-103: Single Image Provider Job Planner and Layer Materialization

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Provider responsibility requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | SuperVisual meaning brief dependency. |
| `THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json` | Provider ownership and prohibited responsibilities. |
| `THE CMF STUDIO/registries/composition/single_image_ideogram_prompt_contracts.v2.json` | Ideogram textless/placeholder and family prompt policy. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Qwen/SAM3/layer extraction dependency. |

## 2. Overview

This spec owns provider job planning for single-image outputs. Providers are workers, not authors of final truth. Ideogram may create composition plates or option assets. GPT Image 2 may create character or object assets. Flux may repair or harmonize. Qwen may extract editable layers. SAM3 owns masks. Skia owns final layout later in TS-CMF-104.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-103-001 | `SingleImageRouterDecision` | Supplies selected composition and provider mode. |
| DEP-CMF-103-002 | `SuperVisualCompositionBrief` | Supplies meaning, primitive, brand, and anchor constraints. |
| DEP-CMF-103-003 | `single_image_provider_responsibilities.v2.json` | Defines allowed and prohibited provider ownership. |
| DEP-CMF-103-004 | `SingleImageProviderJobPlan` | Lists bounded provider jobs and expected outputs. |
| DEP-CMF-103-005 | `SingleImageLayerMaterializationReceipt` | Stores provider outputs, hashes, masks, and blockers. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/services/provider_operations_service.py` | Adds capability checks for all single-image providers. |
| `src/ccp_studio/services/generative_asset_factory_service.py` | Executes bounded generation and repair jobs. |
| `src/ccp_studio/services/single_image_compiler_service.py` | Consumes provider job plan and materialization receipts. |
| Object storage | Persists every provider output immediately with hash refs. |

### ADR-05 Primitives

Provider prompts must include the primitive roles from the approved brief. No provider job may invent a new message operation without returning to routing/brief review.

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase1-M05 Deterministic Override | Providers cannot own final text, final geometry, logos, stats, or source metadata. |
| Phase4-M01 Intelligence-Gated Intercept | Provider work blocks without route, brief, registry, source, and primitive receipt. |
| Phase4-M04 Frictionless Block | Unsupported provider mode blocks before spend. |
| Phase5-M01 Verifiable Artifact | Every provider output has asset hash and policy ref. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Provider jobs are planned before execution. | Enables cost control, review, retry, and determinism. |
| Ideogram outputs are textless when final text exists. | Prevents baked text corruption. |
| SAM3 masks are separate artifacts. | Final layout needs inspectable safe zones. |

## 4. Implementation Plan

1. Add `SingleImageProviderJobPlan`.
2. Load provider responsibility policy.
3. Validate provider mode from selected composition.
4. Produce provider jobs with explicit allowed outputs.
5. Persist all outputs to object storage.
6. Validate outputs against prohibited responsibility rules.
7. Emit materialization receipt.
8. Return only approved asset refs to TS-CMF-104.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageProviderJobPlan(BaseModel):
    schema_version: Literal["cmf.single_image_provider_job_plan.v1"]
    plan_id: UUID
    request_id: UUID
    composition_id: str
    jobs: list[dict]
    responsibility_policy_hash: str
    approval_required_before_execution: bool = False
    blocker_codes: list[str] = Field(default_factory=list)


class SingleImageLayerMaterializationReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_layer_materialization_receipt.v1"]
    receipt_id: UUID
    plan_id: UUID
    provider_job_receipt_refs: list[str]
    generated_asset_refs: list[str]
    mask_asset_refs: list[str] = Field(default_factory=list)
    layer_manifest_refs: list[str] = Field(default_factory=list)
    source_fidelity_passed: bool
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Ideogram returns baked text | Block or repair with `PROVIDER_BAKED_TEXT_VIOLATION`. |
| Qwen unavailable for layered route | Choose alternate candidate or block with `QWEN_LAYERED_REQUIRED`. |
| SAM3 mask fails | Block with `SAM3_MASK_REQUIRED`. |
| Provider output lacks hash | Block with `PROVIDER_ASSET_HASH_REQUIRED`. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T103-01 | Add provider job plan and materialization receipt contracts. |
| T103-02 | Add provider responsibility validator. |
| T103-03 | Add Ideogram prompt contract enforcement. |
| T103-04 | Add Qwen/SAM3 materialization checks. |
| T103-05 | Add hash/object-storage tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC103-01 | Provider plan declares allowed outputs per provider. | Ideogram owns final headline. | Phase1-M05 |
| AC103-02 | Provider outputs are persisted and hashed. | Expiring URL is used in render. | Phase5-M01 |
| AC103-03 | Layer-dependent routes require Qwen/SAM3 artifacts. | Subject cutout route renders without mask. | Phase4-M04 |
| AC103-04 | Source-fidelity outputs cannot fabricate quotes, stats, or handles. | Social card invents a quote. | Phase4-M04 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Router | `TS-CMF-101` |
| SuperVisual brief | `TS-CMF-102` |
| Provider registry | `TS-CMF-042`, `TS-CMF-044` |
| Layer extraction | `TS-CMF-089` |

## 10. Testing Strategy

- Unit tests for provider policy validation.
- Negative Ideogram baked-text fixture.
- Qwen/SAM3 required-route fixture.
- Source-fidelity provider output fixture.
- Object-storage hash persistence fixture.
