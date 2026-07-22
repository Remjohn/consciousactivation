---
tech_spec_id: "TS-CMF-101"
title: "Single Image Router, Format Family, and Archetype Selection"
story_id: "7.27B"
story_title: "Single Image Routing Runtime"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "8 / 9 / 10"
entry_object: "SingleImageEngineInput, SingleImageRegistryBundle, AssetPackageItem, ExpressionMoment"
exit_object: "SingleImageRouterDecision, SingleImageRouteReceipt"
validation_contract: "format subtype, output-family separation, candidate pool, scoring policy, primitive role availability, source fidelity, operator override reason"
required_receipt: "SingleImageRouteReceipt"
runtime_target: "Python / Pydantic v2 / DSPy Router / Pi Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-101: Single Image Router, Format Family, and Archetype Selection

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Umbrella routing requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md` | Registry bundle dependency. |
| `THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json` | Hard constraints, weights, penalties, fallback rules. |
| `THE CMF STUDIO/registries/composition/evidence/single_image_archetype_composition_matrix.v2.csv` | Archetype, derivative, format, provider, and eval compatibility evidence. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Format subtype source of truth. |

## 2. Overview

This spec owns the route decision that separates carousels from SuperVisuals and other single-image outputs. It ensures archetypes do not force one output family. The same myth-break, story, framework, or social proof moment may become a carousel, video, SuperVisual, poll, quote card, meme, or reaction seed depending on asset derivative, operator intent, source shape, platform, and primitive fit.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-101-001 | `SingleImageEngineInput` | Supplies format code, archetype, derivative, content shape, source refs, platform, Visual DNA, and primitive evidence. |
| DEP-CMF-101-002 | `SingleImageRegistryBundle` | Supplies valid compositions and policy hashes. |
| DEP-CMF-101-003 | `single_image_router_policy.v2.json` | Defines hard constraints, weights, penalties, candidate count, and fallbacks. |
| DEP-CMF-101-004 | `SingleImageRouterDecision` | Selects one composition and stores alternatives, score breakdowns, policy hashes, blockers, and override state. |
| DEP-CMF-101-005 | `SingleImageRouteReceipt` | Immutable routing proof. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/services/single_image_router_service.py` | New router service applying hard constraints, weighted scoring, penalties, fatigue, and override rules. |
| `src/ccp_studio/services/asset_package_service.py` | Sends only non-carousel, non-video still items to this router. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Supplies primitive evidence and doctrine blockers. |
| `src/ccp_studio/services/review_state_service.py` | Receives candidate and score read-model fields. |

### ADR-05 Primitives

Routing must verify that at least three primitive roles can be satisfied by the selected composition family before provider or Skia work begins:

| Role | Router Check |
|---|---|
| `meaning_transform` | Candidate can express the source idea operation. |
| `delivery_shape` | Candidate can guide comprehension or reaction. |
| `format_material` | Candidate's material form is justified by the selected format. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Blocks missing subtype, source refs, brand context, primitive evidence, or asset derivative. |
| Phase4-M02 Cinematic Meaning | Candidate score includes semantic intent, not only aesthetics. |
| Phase4-M04 Frictionless Block | Candidate failures block before provider jobs. |
| Phase4-M05 Actionable Rejection | Blockers name failed constraint and repair path. |
| Phase5-M01 Verifiable Artifact | Route receipt stores hashes, scores, selected and rejected IDs. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Single-image router rejects carousel codes. | `CAR-LST` and `CAR-JUX` belong to the carousel builder. |
| Router returns alternatives. | Operator review requires visible choice, not black-box selection. |
| Override requires reason. | Brand operators can decide, but receipts must preserve why. |

## 4. Implementation Plan

1. Add `SingleImageRoutingRequest` from engine input and registry bundle.
2. Validate format code is one of `SPV-*`, `VPL-*`, `TWQ-*`, `MEM-*`, or `RCT-SEED`.
3. Apply router hard constraints.
4. Retrieve compatible candidates from composition registry and matrix evidence.
5. Score using policy weights and penalties.
6. Enforce minimum candidate policy.
7. Apply family diversity and fatigue penalty.
8. Emit `SingleImageRouterDecision` and `SingleImageRouteReceipt`.
9. Store override reason if operator changes the selected composition.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageRoutingRequest(BaseModel):
    schema_version: Literal["cmf.single_image_routing_request.v1"]
    request_id: UUID
    registry_bundle_id: UUID
    content_asset_code: str
    format_code: Literal["SPV-CON", "SPV-SYM", "SPV-PRM", "VPL-WYR", "VPL-VRS", "TWQ-STD", "TWQ-IMG", "MEM-INC", "MEM-REL", "RCT-SEED"]
    content_archetype_id: str
    asset_derivative_id: str
    content_shape: str
    target_aspect_ratio: str
    source_refs: list[str] = Field(min_length=1)
    primitive_refs_available: list[str] = Field(min_length=3)


class SingleImageRouteReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_route_receipt.v1"]
    receipt_id: UUID
    request_id: UUID
    selected_composition_id: str
    candidate_count: int
    policy_hash: str
    registry_hash: str
    route_score: float
    operator_override: bool = False
    override_reason: str | None = None
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| Broad still family only | Infer subtype; if confidence below threshold, block with `SINGLE_IMAGE_FORMAT_SUBTYPE_REQUIRED`. |
| Carousel code received | Block with `SINGLE_IMAGE_OUTPUT_FAMILY_MISMATCH`. |
| Candidate pool too small | Block unless one candidate exceeds emergency confidence threshold and operator confirms. |
| Override missing reason | Block with `SINGLE_IMAGE_OVERRIDE_REASON_REQUIRED`. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T101-01 | Add routing request and receipt contracts. |
| T101-02 | Add router hard-constraint validator. |
| T101-03 | Add candidate retrieval by archetype, derivative, format, content shape, aspect ratio, and primitive role. |
| T101-04 | Add scoring and fatigue penalties. |
| T101-05 | Add override reason persistence. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC101-01 | Single-image router rejects `CAR-*` formats. | `SPV-CON` and `CAR-JUX` are handled by the same route. | Phase4-M04 |
| AC101-02 | Router returns scored candidates and alternatives. | Selected composition has no score breakdown. | Phase3-M02 |
| AC101-03 | SuperVisual codes route only to compatible families. | `SPV-SYM` routes to a generic tweet card. | Phase4-M02 |
| AC101-04 | Override requires a stored reason. | Operator swaps candidate without receipt trace. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Registry loader | `TS-CMF-100` |
| Umbrella Single Image spec | `TS-CMF-099` |
| Content asset code registry | `docs/content-asset-code-and-format-registry.md` |
| Upstream archetype routing | `TS-CMF-033` |

## 10. Testing Strategy

- Positive routing tests for `SPV-CON`, `SPV-SYM`, `SPV-PRM`, `VPL-WYR`, `TWQ-IMG`, `MEM-REL`, and `RCT-SEED`.
- Negative test for `CAR-LST` and `CAR-JUX`.
- Candidate scoring snapshot tests.
- Override reason tests.
- Fatigue and family-diversity tests.
