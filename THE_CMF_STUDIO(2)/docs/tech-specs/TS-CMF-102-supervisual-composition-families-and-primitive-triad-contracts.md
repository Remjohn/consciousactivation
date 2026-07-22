---
tech_spec_id: "TS-CMF-102"
title: "SuperVisual Composition Families and Primitive Triad Contracts"
story_id: "7.27C"
story_title: "SuperVisual Composition Semantics"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "9 / 10"
entry_object: "SingleImageRouterDecision, ExpressionMoment, BrandContextVersion, VoiceVisualDNA"
exit_object: "SuperVisualCompositionBrief, SuperVisualPrimitiveTriadReceipt, SuperVisualVisualFeelContract"
validation_contract: "SPV-CON, SPV-SYM, SPV-PRM semantic separation, primitive triad, visual feel, source meaning, brand substrate, micro-semiotic anchor safety"
required_receipt: "SuperVisualPrimitiveTriadReceipt"
runtime_target: "Python / Pydantic v2 / Doctrine Evaluation / Primitive Registry"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-102: SuperVisual Composition Families and Primitive Triad Contracts

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Umbrella SuperVisual requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-101-single-image-router-format-family-and-archetype-selection.md` | Upstream route decision. |
| `THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json` | Composition families available to SuperVisuals. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Required primitive role coverage. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines `SPV-CON`, `SPV-SYM`, and `SPV-PRM`. |

## 2. Overview

SuperVisuals are not prettier quote cards. They are standalone single-frame meaning operations. This spec separates the three SuperVisual modes:

- `SPV-CON`: conceptual contrast or binary tension;
- `SPV-SYM`: symbolic scene, object metaphor, or emotional image;
- `SPV-PRM`: premium brand-forward visual with source-backed claim, quote, or campaign signal.

Each SuperVisual must validate at least three primitives before provider work. The primitive triad is the quality floor, not a decorative tag.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-102-001 | `SingleImageRouterDecision` | Supplies selected composition and family. |
| DEP-CMF-102-002 | `ExpressionMoment` | Supplies source meaning operation and evidence. |
| DEP-CMF-102-003 | `BrandContextVersion` | Supplies visual constitution, banned motifs, claims, and identity rules. |
| DEP-CMF-102-004 | `SuperVisualCompositionBrief` | Declares the SuperVisual's semantic job before providers. |
| DEP-CMF-102-005 | `SuperVisualPrimitiveTriadReceipt` | Proves meaning, delivery, and format/material primitive coverage. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Validates primitive triad and doctrine fit. |
| `src/ccp_studio/services/micro_semiotic_anchor_service.py` | Validates anchor choices and risk. |
| `src/ccp_studio/services/single_image_compiler_service.py` | Consumes the SuperVisual brief before provider planning. |

### ADR-05 Primitives

| SuperVisual Code | Minimum Primitive Direction |
|---|---|
| `SPV-CON` | `PRM-PRS-015`, contrast/inversion, eye-path/frame primitive. |
| `SPV-SYM` | metaphor/symbol, emotional space/light, material form primitive. |
| `SPV-PRM` | strong title or quote architecture, brand geometry, source fidelity. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Blocks SuperVisuals without source, brand, primitive triad, and selected family. |
| Phase4-M02 Cinematic Meaning | Requires a declared meaning operation and visual feel contract. |
| Phase4-M04 Frictionless Block | Blocks unsafe anchors, weak primitive coverage, or generic premium style. |
| Phase4-M05 Actionable Rejection | Returns failed primitive role and repair instruction. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| SuperVisuals get their own brief. | A single image can be more complex than a carousel slide because it carries the whole argument alone. |
| Visual feel is route-specific. | Prevents every image from collapsing into the same high-contrast social aesthetic. |
| Primitive triad precedes provider calls. | Providers should execute meaning, not invent it. |

## 4. Implementation Plan

1. Add `SuperVisualCompositionBrief`.
2. Add format-specific semantic checks for `SPV-CON`, `SPV-SYM`, and `SPV-PRM`.
3. Validate primitive role coverage.
4. Validate visual feel contract against selected family.
5. Validate micro-semiotic anchors and brand substrate.
6. Emit `SuperVisualPrimitiveTriadReceipt`.
7. Block provider planning when receipt fails.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SuperVisualCompositionBrief(BaseModel):
    schema_version: Literal["cmf.supervisual_composition_brief.v1"]
    brief_id: UUID
    request_id: UUID
    format_code: Literal["SPV-CON", "SPV-SYM", "SPV-PRM"]
    selected_composition_id: str
    meaning_operation: str
    visual_feel_contract: str
    source_refs: list[str] = Field(min_length=1)
    required_primitive_refs: list[str] = Field(min_length=3)
    micro_semiotic_anchor_refs: list[str] = Field(default_factory=list)


class SuperVisualPrimitiveTriadReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_primitive_triad_receipt.v1"]
    receipt_id: UUID
    brief_id: UUID
    meaning_transform_ref: str
    delivery_shape_ref: str
    format_material_ref: str
    passed: bool
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| SuperVisual has no subtype | Block with `SUPERVISUAL_SUBTYPE_REQUIRED`. |
| Primitive role missing | Block with `SUPERVISUAL_PRIMITIVE_TRIAD_INCOMPLETE`. |
| Visual feel generic | Block with `SUPERVISUAL_VISUAL_FEEL_COLLAPSE`. |
| Anchor unsafe | Block with `SUPERVISUAL_MSA_UNSAFE`. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T102-01 | Add SuperVisual brief and receipt contracts. |
| T102-02 | Add triad validator for `SPV-CON`, `SPV-SYM`, `SPV-PRM`. |
| T102-03 | Add visual feel collapse detector. |
| T102-04 | Add MSA risk gate integration. |
| T102-05 | Add fixtures for all three SuperVisual codes. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC102-01 | Every SuperVisual declares one meaning operation. | Premium image has no semantic job. | Phase4-M02 |
| AC102-02 | Every SuperVisual passes three primitive roles. | `SPV-CON` has only a contrast label and no format primitive. | Phase4-M01 |
| AC102-03 | `SPV-CON`, `SPV-SYM`, and `SPV-PRM` produce distinct visual feel contracts. | All three use the same poster layout. | Phase4-M04 |
| AC102-04 | Unsafe anchors block before providers. | Symbolic image uses a stereotype cue. | Phase4-M04 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Single-image router | `TS-CMF-101` |
| MSA risk gate | `TS-CMF-087` |
| Brand substrate | `TS-CMF-082` |
| Primitive eval harness | `TS-CMF-077` |

## 10. Testing Strategy

- Golden `SPV-CON`, `SPV-SYM`, and `SPV-PRM` briefs.
- Negative fixture for generic premium collapse.
- Negative fixture for missing primitive role.
- Negative fixture for unsafe MSA.
- Review fixture proving the primitive triad is visible to the operator.
