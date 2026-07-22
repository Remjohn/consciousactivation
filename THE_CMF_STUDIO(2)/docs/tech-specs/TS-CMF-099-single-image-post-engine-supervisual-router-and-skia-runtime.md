---
tech_spec_id: "TS-CMF-099"
title: "Single Image Post Engine, SuperVisual Router, and Skia Runtime"
story_id: "7.27"
story_title: "Single Image and SuperVisual Composition Engine"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "CCP Single Image Post Engine V2 bundle integration"
pipeline_stage: "8 / 9 / 10 / 11 / 12 / 13"
entry_object: "SingleImageEngineInput, BrandContextVersion, ExpressionMoment, AssetPackageItem, TargetPlatformSpec, VoiceVisualDNA"
exit_object: "SingleImageSceneSpecV2, CompositionRouterDecision, ProviderJobSpec, SkiaRenderReceipt, SingleImageEvaluationReceiptV2, SingleImageProductionRecord"
validation_contract: "archetype to derivative to single-image composition routing, SuperVisual format support, text budget, normalized zones, provider role boundaries, primitive triad, source fidelity, Skia deterministic render, eval receipt, operator approval"
required_receipt: "SingleImageProductionRecord"
runtime_target: "Python / Pydantic v2 / DSPy Composition Router / Ideogram 4 / GPT Image 2 / Flux Edit / Qwen-Image-Layered / SAM3 / PRETEXT / Skia CanvasKit / Rough Annotation Manifest / PWA and Telegram review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-099: Single Image Post Engine, SuperVisual Router, and Skia Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section ERA3 protocol, existing-backend mapping, ADR-05 primitive requirements, CBAR mandates, acceptance criteria, and testing discipline. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/CCP_SINGLE_IMAGE_POST_ENGINE_V2.md` | Human-readable Single Image Post Engine V2 doctrine: structured input, archetype routing, 28 contracts, Skia rendering, eval, approval, and reproducibility. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_composition_models_v2.py` | Source Pydantic model sketch for engine input, composition contracts, router decisions, scene specs, provider jobs, render receipts, eval receipts, and production records. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_render_contracts_v2.ts` | Generated TypeScript consumer contract sketch proving TS must consume Python/Pydantic semantic authority. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_composition_registry_v2.json` | Source registry with 28 canonical single-image composition contracts across eight families. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_archetype_composition_matrix_v2.csv` | Archetype, derivative, content shape, format, provider mode, and eval profile mapping. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_router_policy_v2.json` | Router hard constraints, scoring weights, penalties, selection policy, and fallbacks. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_skia_component_catalog_v2.json` | Skia component catalog for deterministic final still rendering. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_ideogram_prompt_contracts_v2.json` | Ideogram 4 prompt contracts and negative rules per composition family. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_provider_responsibilities_v2.json` | Provider ownership policy for Ideogram, GPT Image 2, Flux Edit, Qwen layered, SAM3, Skia, Rough Notation, and ImageCritic/visual eval. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_eval_rubrics_v2.json` | Global and family-specific evaluation rubrics, thresholds, hard failures, and repair dimensions. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_examples_v2.json` | Golden routing examples for myth debunk, identity poll, interview quote, framework, and social reaction. |
| `THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json` | Canonical migrated runtime registry path for the 28 composition contracts. |
| `THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json` | Canonical migrated runtime router policy path. |
| `THE CMF STUDIO/registries/composition/single_image_skia_component_catalog.v2.json` | Canonical migrated runtime Skia component catalog path. |
| `THE CMF STUDIO/registries/composition/single_image_ideogram_prompt_contracts.v2.json` | Canonical migrated Ideogram prompt contract path. |
| `THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json` | Canonical migrated provider responsibility policy path. |
| `THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json` | Canonical migrated eval rubric path. |
| `THE CMF STUDIO/registries/composition/evidence/single_image_archetype_composition_matrix.v2.csv` | Canonical migrated evidence fixture for archetype-to-composition compatibility. |
| `THE CMF STUDIO/registries/composition/evidence/single_image_examples.v2.json` | Canonical migrated evidence fixture for router examples. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines `SPV-CON`, `SPV-SYM`, `SPV-PRM`, `VPL-*`, `TWQ-*`, `MEM-*`, and `RCT-SEED` as non-video content format codes. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream deterministic still visual runtime for Geometrics, PRETEXT, SAM3, Qwen, Rough Annotation, and Skia. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Meaning-level carousel slide atom layer; this spec must not collapse SuperVisuals into carousel slide logic. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` | Full carousel compiler workflow; this spec is a sibling single-image compiler, not a child of carousel. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` | Visual grammar atlas for carousel slides; useful pattern for registry and router integration. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Mandatory primitive triad registry for composition-bearing assets. |
| `THE CMF STUDIO/src/ccp_studio/contracts/asset_package.py` | AssetPackageItem owner that must represent still visual subtype refs and package counts. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Current composition contracts that must link into single-image scene specs and Geometrics plans. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Composition service owner that should call the single-image router and provider planner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Provider capability registry and provider job receipt owner. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_evaluation_service.py` | Doctrine and primitive eval owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Approval blocker and policy report owner. |

## 2. Overview

The Single Image Post Engine V2 makes SuperVisuals, visual polls, tweet-like quotes, memes, documentary social cards, promo cards, and reaction stills first-class CMF outputs. It is not a carousel slide builder and it is not a prompt-to-image shortcut.

The engine consumes structured CMF context:

```text
Complete Expression Session
-> Expression Moment
-> Core Content Archetype
-> Asset Derivative
-> optional Meme / Reaction mechanism
-> Single Image Composition Router
-> SingleImageSceneSpecV2
-> Provider Jobs
-> Geometrics / PRETEXT / SAM3 / Qwen handoff
-> Skia Render
-> Evaluation Receipt
-> Operator Approval
-> Publishing Intent
```

This spec integrates `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE` into the current CMF architecture. The bundle's key correction is that archetypes are not carousel-specific. The same source archetype can produce:

- a video format such as `SV-FRB`;
- a carousel such as `CAR-JUX`;
- a visual poll such as `VPL-WYR`;
- a tweet-like quote such as `TWQ-IMG`;
- a meme such as `MEM-REL`;
- a SuperVisual such as `SPV-CON`, `SPV-SYM`, or `SPV-PRM`.

The router must therefore choose the output family from archetype, derivative, content shape, source evidence, asset availability, target platform, Visual DNA, primitive fit, and operator intent. It must not assume that an archetype is only a carousel route.

### Scope

This spec covers:

- the 28 canonical single-image composition contracts;
- single-image archetype/derivative/content-shape routing;
- SuperVisual format support;
- registry loading and query;
- provider role planning;
- deterministic Skia scene assembly;
- family-specific eval rubrics;
- operator override and approval;
- audit receipts and reproducibility.

This spec does not cover:

- multi-slide carousel sequence planning, which belongs to TS-CMF-096 through TS-CMF-098;
- video timeline rendering, which belongs to the future VideoEditProgram spec;
- 2D character animation rigging, which belongs to TS-CMF-086, TS-CMF-093, TS-CMF-094, and future character animation specs;
- newsletters or unsupported content outputs.

### Decomposition Boundary

This spec is the umbrella contract for the Single Image Post Engine. It is not sufficient by itself as an implementation plan. Production work must follow the decomposed child specs below:

| Child Spec | Ownership |
|---|---|
| `TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md` | Pydantic contracts, canonical registry bundle loading, hash validation, and generated TypeScript parity. |
| `TS-CMF-101-single-image-router-format-family-and-archetype-selection.md` | Output-family-aware routing, format subtype validation, candidate scoring, fatigue, and override receipts. |
| `TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | `SPV-CON`, `SPV-SYM`, and `SPV-PRM` semantic separation, visual feel contracts, and primitive triad gates. |
| `TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md` | Provider responsibility planning for Ideogram 4, GPT Image 2, Flux Edit, Qwen layered, and SAM3. |
| `TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | SceneSpec compilation, PRETEXT, Geometrics, Skia component binding, and render receipts. |
| `TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md` | Eval rubrics, hard failures, operator review read model, approval blockers, and golden fixtures. |

Implementation cannot mark the Single Image or SuperVisual engine complete until all six child specs have passing acceptance criteria and fixtures.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-099-001 | `SingleImageEngineInput` | Validates organization, brand, Brand Context Version, source Expression Moment, archetype, derivative, target platform, aspect ratio, content shape, primitives, doctrines, text payload, assets, and micro-semiotic anchors before routing. |
| DEP-CMF-099-002 | `single_image_composition_registry.v2.json` | Canonical registry of 28 composition contracts. Runtime loads this path, not loose files from the source bundle. |
| DEP-CMF-099-003 | `single_image_router_policy.v2.json` | Hard constraints, scoring weights, penalties, candidate selection, fallback policy, and operator override behavior. |
| DEP-CMF-099-004 | `single_image_archetype_composition_matrix.v2.csv` | Evidence fixture for archetype, derivative, content shape, format, provider mode, and eval profile compatibility. |
| DEP-CMF-099-005 | `single_image_skia_component_catalog.v2.json` | Defines allowed deterministic Skia components. Renderer props cannot call arbitrary UI components. |
| DEP-CMF-099-006 | `single_image_ideogram_prompt_contracts.v2.json` | Governs Ideogram output mode, textless/placeholder rules, reserved text zones, and family-specific prompt fields. |
| DEP-CMF-099-007 | `single_image_provider_responsibilities.v2.json` | Defines provider ownership boundaries and prohibited responsibilities. |
| DEP-CMF-099-008 | `single_image_eval_rubrics.v2.json` | Global and family-specific scoring dimensions, thresholds, and hard fail codes. |
| DEP-CMF-099-009 | `SingleImageSceneSpecV2` | Deterministic scene spec containing zones, text elements, visual asset placements, annotation specs, anchor placements, provider jobs, and eval profile. |
| DEP-CMF-099-010 | `GeometricsLayoutPlan` | Downstream exact coordinate, safe-zone, text measurement, mask, collision, and Skia readiness object from TS-CMF-095. |
| DEP-CMF-099-011 | `SkiaRenderReceipt` | Proves renderer version, font manifest hash, asset hashes, scene spec hash, output URI, SHA-256, and duration. |
| DEP-CMF-099-012 | `SingleImageEvaluationReceiptV2` | Stores rubric scores, hard failures, repairs, operator status, and notes. |
| DEP-CMF-099-013 | `SingleImageProductionRecord` | Final audit object combining input, router decision, scene spec, render receipt, eval receipt, and status. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/single_image.py` | New Pydantic contracts adapted from the source bundle: enums, bounds, zones, composition contract, engine input, score, router decision, text elements, visual placements, annotations, provider jobs, scene spec, render receipt, eval receipt, and production record. |
| `src/ccp_studio/services/single_image_registry_service.py` | New registry loader and validator for composition registry, router policy, Skia component catalog, provider responsibilities, Ideogram prompt contracts, and eval rubrics. |
| `src/ccp_studio/services/single_image_router_service.py` | New router service applying hard constraints, weighted scoring, penalties, diversity policy, and operator override recording. |
| `src/ccp_studio/services/single_image_compiler_service.py` | New compiler that turns `SingleImageEngineInput` and router decision into `SingleImageSceneSpecV2`, provider job specs, Geometrics handoff, Skia render job, eval receipt, and production record. |
| `src/ccp_studio/contracts/asset_package.py` | Add still visual item subtype refs for `VPL-*`, `TWQ-*`, `MEM-*`, `SPV-*`, `RCT-SEED`, and source compatibility. |
| `src/ccp_studio/services/asset_package_service.py` | Route still visual package items through Single Image Engine when the item is not a carousel and not a video. |
| `src/ccp_studio/contracts/composition.py` | Link existing Ideogram `CompositionJob` / `CompositionPlate` to `SingleImageSceneSpecV2.provider_jobs` and downstream Geometrics. |
| `src/ccp_studio/services/composition_service.py` | Call Single Image Router and Provider Job Planner for still outputs instead of stopping at generated plates. |
| `src/ccp_studio/services/provider_operations_service.py` | Ensure capability entries exist for Ideogram 4, GPT Image 2, Flux Edit, Qwen-Image-Layered, SAM3, Skia still render, Rough Annotation, and visual eval workers. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Validate primitive triads and single-image eval rubric coverage before approval. |
| `src/ccp_studio/services/approval_gate_service.py` | Block approval for source fidelity failure, registry mismatch, unsafe identity, missing render hash, or operator approval gap. |
| `src/ccp_studio/services/review_state_service.py` | Add single-image review read model with source, composition, candidates, provider jobs, preview, eval, repairs, and approval state. |
| `src/ccp_studio/generated/typescript/` | Generate TypeScript consumer contracts from Python/Pydantic; do not hand-maintain semantic TS authority. |

### Registry Migration Boundary

The source bundle is an included source artifact. Runtime should load canonical registry paths:

```text
THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json
THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json
THE CMF STUDIO/registries/composition/single_image_skia_component_catalog.v2.json
THE CMF STUDIO/registries/composition/single_image_ideogram_prompt_contracts.v2.json
THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json
THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json
THE CMF STUDIO/registries/composition/evidence/single_image_archetype_composition_matrix.v2.csv
THE CMF STUDIO/registries/composition/evidence/single_image_examples.v2.json
```

The source files remain useful for audit, but production services should not read directly from `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE` unless running migration/evidence verification.

### Composition Families

The registry contains 28 canonical composition contracts across eight families:

| Family | Count | Purpose |
|---|---:|---|
| `assertion_commentary` | 4 | Forceful claims, quote commentary, difficult conversation cards, premium assertion formats. |
| `documentary_social_card` | 2 | Tweet/social-source cards and screenshot-reaction proof cards. |
| `comparison_poll` | 7 | Would-you-rather, versus, scorecard, debate, binary choice, and identity ladder visuals. |
| `cartoon_moral` | 3 | Single moral scene, character thesis, and object metaphor. |
| `cartoon_framework` | 4 | Diptych, triptych, quad, and progression framework visuals. |
| `conceptual_metaphor` | 4 | Emotional scenes, urgency scenes, powerful demonstrations, and two-scenario visuals. |
| `sports_collage` | 2 | Verified stat/photo/quote collage formats. |
| `promo_live` | 2 | Episode, live show, expert flyer, or event promo cards. |

### Format Mapping

| Format Code | Single Image Engine Role |
|---|---|
| `SPV-CON` | Routes primarily to conceptual metaphor, comparison poll, powerful demonstration, and two-scenario compositions. |
| `SPV-SYM` | Routes to symbolic conceptual metaphor, object metaphor, cartoon moral, and main-character emotional scene compositions. |
| `SPV-PRM` | Routes to premium brand-forward assertion, quote closeup, expert flyer, and hero-scene compositions. |
| `VPL-WYR` | Routes to would-you-rather, identity ladder, comparison poll vertical, and this-or-that debate card. |
| `VPL-VRS` | Routes to versus scorecard, this-or-that debate card, conceptual contrast, and comparison poll vertical. |
| `TWQ-STD` | Routes to minimal black quote card, tweet-style commentary card, and deterministic social card. |
| `TWQ-IMG` | Routes to quote-on-closeup commentary, tweet-style commentary card, and image-backed quote layouts. |
| `MEM-INC` | Routes to cartoon moral, cartoon object metaphor, difficult conversation, and incongruity-safe compositions. |
| `MEM-REL` | Routes to relatable recognition, social screenshot reaction card, tweet-style commentary card, and mirror-prompt compositions. |
| `RCT-SEED` | Routes to social screenshot reaction card, quote-on-closeup commentary, tweet-style commentary card, and poll/reaction seed formats. |

### ADR-05 Primitives

Every single-image output must pass at least three primitive validations across:

| Role | Required Proof |
|---|---|
| `meaning_transform` | The image performs a real idea operation: contrast, myth break, proof, identity mirror, emotional scene, inversion, or teaching metaphor. |
| `delivery_shape` | The format guides comprehension through hierarchy, option parity, quote force, source proof, social recognition, visual moral, or progression. |
| `format_material` | The visual form is justified by eye path, negative space, paper/cartoon materiality, human proof, screenshot fidelity, symbolic object, or premium brand geometry. |

Useful primitive references include:

| Format/Family | Required Primitive Direction |
|---|---|
| Assertion and quote cards | `PRM-PRS-001` Strong Title as Idea Architecture, `PRM-VOC-006` Start Strong End Strong, `PRM-VSG-021` Punctum Air and Felt Truth. |
| Comparison and polls | `PRM-PRS-015` What Is / What Could Be Contrast Engine, `PRM-HUM-021` Irony Inversion, `PRM-VSG-012` Frame as Active Meaning Device. |
| SuperVisual conceptual metaphor | `PRM-PRS-015`, `PRM-VSG-016` Light and Color as Emotional Architecture, `PRM-VSG-024` Space as Psychological Relationship. |
| Framework visuals | `PRM-PRS-032` Explanation Engine, `PRM-PRS-025` Rule of Three Message Architecture, `PRM-BUS-012` Grid as Cognitive Relief. |
| Documentary social cards | source fidelity primitives plus human proof and context preservation primitives. |
| Cartoon moral | analogy, moral mechanism, single-reading clarity, materiality, and tone-fit primitives. |

Exact primitive IDs must be loaded from the active registry. Generic words like "premium", "viral", "clean", or "smart" cannot satisfy primitive proof.

### CBAR Mandate Enforcement

| Mandate | Governing Story | Enforcement |
|---|---|---|
| Phase1-M05: The Deterministic Override Rule | Story 2.2 | Final text, final typography, final geometry, panel borders, poll UI, scorecards, and export are Skia-owned. Generative models provide assets or plates only. |
| Phase3-M02: Per-Slide Feedback Rule | Story 1.2 | Operator review must expose composition candidates, score breakdowns, selected composition ID, eval failures, and repair actions per single-image asset. |
| Phase3-M05: Modular CMF Recovery Rule | Story 3.2 | Router decision, provider jobs, layer/mask artifacts, Geometrics plan, render receipt, eval receipt, and approval state persist independently for retry/resume. |
| Phase4-M01: Intelligence-Gated Intercept Rule | Story 1.1 | Routing blocks without source route, Brand Context Version, archetype, derivative, content shape, target aspect ratio, primitive evals, and source fidelity. |
| Phase4-M02: Cinematic Meaning Rule | Story 2.1 | Composition choice must prove semantic intent, not aesthetic preference. SuperVisuals must carry meaning operations, not decoration. |
| Phase4-M04: Frictionless Block Rule | Story 4.1 | Unsupported aspect ratio, text overflow, missing assets, source fidelity failure, identity risk, or unsafe micro-semiotic anchor block before provider/render cost. |
| Phase4-M05: Actionable Rejection Rule | Story 5.1 | Every blocker names failed composition, score dimension, text budget, asset, mask, source object, or eval profile with repair hints. |
| Phase5-M01: Verifiable Artifact Rule | Story 1.1 | Production record stores registry version, registry hash, provider versions/seeds, scene spec hash, asset hashes, Skia output hash, eval receipt, and operator approval. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Single Image Engine is a sibling of Carousel Builder, not a carousel subtype. | Carousels require sequence planning; SuperVisuals and single-image outputs require one-frame composition routing and Skia assembly. |
| The output family is selected after archetype and derivative, not from archetype alone. | The same archetype can become video, carousel, poll, quote, meme, reaction seed, or SuperVisual. |
| Canonical registry files live under `registries/composition`. | Runtime services should load normalized registry paths instead of source bundles. |
| Ideogram 4 can direct composition but cannot own final text or geometry. | Source fidelity, text accuracy, and brand consistency require deterministic downstream assembly. |
| Qwen layered is optional. | It is needed only when generated plates must become editable layers. Pure typography, social cards, quote cards, sports stats, and promo cards often skip it. |
| SAM3 is the mask authority for subjects and objects. | Text and layout must respect safe zones around faces, hands, products, symbols, and screenshots. |
| Skia is final renderer. | Still visuals require reproducible typography, geometry, masks, panels, borders, rough annotations, and output hashes. |
| The TypeScript contract is generated from Python. | UI and renderer consumers cannot become semantic source of truth. |

## 4. Implementation Plan

1. Add `src/ccp_studio/contracts/single_image.py` adapted from the V2 source model with CMF receipt fields, brand scope, content asset code, Command Bus refs, primitive refs, eval refs, and approval blockers.
2. Add `SingleImageRegistryService`:
   - load canonical registry files;
   - validate all 28 composition contracts;
   - validate normalized zones;
   - validate text budgets;
   - validate provider modes;
   - validate evaluation profiles;
   - compute registry hashes.
3. Add `SingleImageRouterService`:
   - apply hard constraints;
   - compute weighted score;
   - apply penalties;
   - return three candidate compositions with family diversity;
   - record operator override reason.
4. Add `SingleImageCompilerService`:
   - hydrate Brand Context, Expression Moment, AssetPackageItem, Voice/Visual DNA, primitives, doctrines, text payload, and asset refs;
   - compile `SingleImageSceneSpecV2`;
   - compile `ProviderJobSpec[]`;
   - call Geometrics/PRETEXT/SAM3/Qwen handoff when required;
   - call Skia render job when approved for render;
   - store render and eval receipts.
5. Add format-family routing from `AssetPackageItem`:
   - `SPV-*` routes to SuperVisual-capable composition families;
   - `VPL-*` routes to comparison/poll families;
   - `TWQ-*` routes to quote/social card families;
   - `MEM-*` routes to cartoon moral, recognition, and meme-safe families;
   - `RCT-SEED` routes to reaction seed compatible families.
6. Update provider operations with capability checks for:
   - `ideogram_4.composition_plate.v1`;
   - `gpt_image_2.asset_generation.v1`;
   - `flux_edit.identity_preserving_repair.v1`;
   - `qwen_image_layered.rgba_layers.v1`;
   - `sam3.subject_object_masks.v1`;
   - `skia_canvaskit.still_render.v1`;
   - `rough_annotation.semantic_cues.v1`;
   - `single_image.visual_eval.v1`.
7. Update review surfaces:
   - candidate comparison view;
   - selected composition ID and family;
   - scene spec editor;
   - text budget/overflow status;
   - layer and cutout review;
   - final mobile preview;
   - eval and repair panel;
   - approve/revise/reject actions.
8. Add operator approval blockers:
   - no source fidelity proof;
   - unsafe micro-semiotic anchor;
   - text overflow;
   - identity mismatch;
   - provider responsibility violation;
   - primitive triad missing;
   - missing Skia hash;
   - eval below threshold;
   - operator approval missing.
9. Generate TypeScript consumer contracts from Python/Pydantic and replace any hand-maintained semantic TS definitions.
10. Add golden fixtures for the five source examples and at least one output per single-image family.

## 5. Primary Output Schema

```python
from __future__ import annotations

from enum import Enum
from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageFormatCode(str, Enum):
    vpl_wyr = "VPL-WYR"
    vpl_vrs = "VPL-VRS"
    twq_std = "TWQ-STD"
    twq_img = "TWQ-IMG"
    mem_inc = "MEM-INC"
    mem_rel = "MEM-REL"
    spv_con = "SPV-CON"
    spv_sym = "SPV-SYM"
    spv_prm = "SPV-PRM"
    rct_seed = "RCT-SEED"


class SingleImageAspectRatio(str, Enum):
    square = "1:1"
    portrait = "4:5"
    story = "9:16"
    landscape = "16:9"


class SingleImageReviewStatus(str, Enum):
    draft = "draft"
    routed = "routed"
    assets_pending = "assets_pending"
    rendering = "rendering"
    auto_evaluated = "auto_evaluated"
    awaiting_operator_review = "awaiting_operator_review"
    approved = "approved"
    needs_revision = "needs_revision"
    rejected = "rejected"
    published = "published"


class SingleImageBounds(BaseModel):
    schema_version: Literal["cmf.single_image_bounds.v1"]
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    w: float = Field(gt=0, le=1)
    h: float = Field(gt=0, le=1)


class SingleImageCompositionZone(BaseModel):
    schema_version: Literal["cmf.single_image_composition_zone.v1"]
    zone_id: str
    role: str
    bounds: SingleImageBounds
    z_index: int
    required: bool = True
    content_type: str
    alignment: str = "center"


class SingleImageTextBudget(BaseModel):
    schema_version: Literal["cmf.single_image_text_budget.v1"]
    headline_words_max: int | None = None
    support_words_max: int | None = None
    body_words_max: int | None = None
    option_words_max: int | None = None
    caption_words_per_panel: int | None = None
    bullet_lines_per_side: int | None = None
    stat_chips_max: int | None = None
    metadata_lines_max: int | None = None


class SingleImageCompositionContract(BaseModel):
    schema_version: Literal["cmf.single_image_composition_contract.v2"]
    composition_id: str
    source_schema_id: str
    registry_bundle_version: str
    family: str
    semantic_intent: str
    layout_template_id: str
    compatible_archetypes: list[str]
    compatible_derivatives: list[str]
    compatible_meme_mechanisms: list[str] = Field(default_factory=list)
    compatible_reaction_archetypes: list[str] = Field(default_factory=list)
    content_shapes: list[str]
    format_support: list[SingleImageAspectRatio]
    text_budget: SingleImageTextBudget
    provider_mode: str
    rough_notation_contract: dict[str, Any]
    micro_semiotic_anchor_slots: list[dict[str, Any]] = Field(default_factory=list)
    evaluation_profile_id: str
    visual_energy: str
    visual_density: str
    zones: list[SingleImageCompositionZone]
    primitive_defaults: list[str] = Field(default_factory=list)
    source_registry_ref: str


class SingleImageEngineInput(BaseModel):
    schema_version: Literal["cmf.single_image_engine_input.v1"]
    request_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    brand_context_version_id: UUID
    content_asset_code: str
    format_code: SingleImageFormatCode
    registry_bundle_version: str
    source_expression_session_id: UUID | None = None
    source_expression_moment_id: UUID | None = None
    interview_asset_contract_id: UUID | None = None
    content_archetype_id: str
    asset_derivative_id: str
    meme_mechanism_id: str | None = None
    reaction_archetype_id: str | None = None
    expression_state: str | None = None
    primitive_evaluations: dict[str, float] = Field(default_factory=dict)
    doctrine_refs: list[str] = Field(default_factory=list)
    target_platform: str
    target_aspect_ratio: SingleImageAspectRatio
    content_shape: str
    headline: str
    support_text: str | None = None
    body_text: str | None = None
    option_a: str | None = None
    option_b: str | None = None
    panel_captions: list[str] = Field(default_factory=list)
    verified_quote_refs: list[str] = Field(default_factory=list)
    verified_stat_refs: list[str] = Field(default_factory=list)
    approved_asset_ids: list[UUID] = Field(default_factory=list)
    micro_semiotic_anchor_candidates: list[str] = Field(default_factory=list)


class SingleImageRouterCandidateScore(BaseModel):
    schema_version: Literal["cmf.single_image_router_candidate_score.v1"]
    composition_id: str
    total_score: float = Field(ge=0, le=1)
    component_scores: dict[str, float]
    penalties: dict[str, float] = Field(default_factory=dict)
    hard_constraint_failures: list[str] = Field(default_factory=list)
    explanation: str


class SingleImageRouterDecision(BaseModel):
    schema_version: Literal["cmf.single_image_router_decision.v1"]
    decision_id: UUID
    request_id: UUID
    selected_composition_id: str
    selected_family: str
    candidates: list[SingleImageRouterCandidateScore]
    operator_override: bool = False
    override_reason: str | None = None
    router_policy_hash: str
    registry_hash: str


class SingleImageTextElement(BaseModel):
    schema_version: Literal["cmf.single_image_text_element.v1"]
    text_element_id: UUID
    zone_id: str
    role: str
    text: str
    font_token: str
    color_token: str
    max_lines: int
    alignment: str
    emphasis_spans: list[dict[str, Any]] = Field(default_factory=list)
    source_ref: str | None = None


class SingleImageVisualAssetPlacement(BaseModel):
    schema_version: Literal["cmf.single_image_visual_asset_placement.v1"]
    placement_id: UUID
    zone_id: str
    asset_id: UUID
    asset_role: str
    fit: str = "cover"
    focal_point: dict[str, float] | None = None
    mask_asset_id: UUID | None = None
    layer_manifest_id: UUID | None = None


class SingleImageAnnotationSpec(BaseModel):
    schema_version: Literal["cmf.single_image_annotation_spec.v1"]
    annotation_id: UUID
    target_element_id: UUID
    annotation_type: str
    color_token: str
    roughness: float = Field(default=1.0, ge=0, le=3)
    seed: int
    semantic_job: Literal[
        "direct_attention",
        "mark_contrast",
        "reject_claim",
        "group_information",
        "prove_relationship",
        "point_to_action",
    ]
    primitive_ref: str


class SingleImageProviderJobSpec(BaseModel):
    schema_version: Literal["cmf.single_image_provider_job_spec.v1"]
    provider: str
    task_type: str
    input_contract: dict[str, Any]
    model_version: str
    seed: int | None = None
    output_asset_roles: list[str]
    approval_required: bool = True
    provider_responsibility_policy_ref: str


class SingleImageSceneSpecV2(BaseModel):
    schema_version: Literal["cmf.single_image_scene_spec.v2"]
    scene_spec_id: UUID
    request_id: UUID
    input_context_hash: str
    brand_context_version_id: UUID
    content_asset_code: str
    format_code: SingleImageFormatCode
    registry_bundle_version: str
    composition_id: str
    aspect_ratio: SingleImageAspectRatio
    canvas_width: int
    canvas_height: int
    background_token: str
    text_elements: list[SingleImageTextElement]
    visual_assets: list[SingleImageVisualAssetPlacement]
    annotations: list[SingleImageAnnotationSpec] = Field(default_factory=list)
    micro_semiotic_anchors: list[dict[str, Any]] = Field(default_factory=list)
    provider_jobs: list[SingleImageProviderJobSpec] = Field(default_factory=list)
    evaluation_profile_id: str
    primitive_refs: list[str] = Field(min_length=3)
    blocker_codes: list[str] = Field(default_factory=list)


class SingleImageSkiaRenderReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_skia_render_receipt.v1"]
    render_id: UUID
    scene_spec_id: UUID
    renderer_version: str
    font_manifest_hash: str
    asset_hashes: dict[str, str]
    scene_spec_hash: str
    output_uri: str
    output_sha256: str
    duration_ms: int


class SingleImageEvaluationReceiptV2(BaseModel):
    schema_version: Literal["cmf.single_image_evaluation_receipt.v2"]
    receipt_id: UUID
    render_id: UUID
    composition_id: str
    evaluation_profile_id: str
    dimension_scores: dict[str, float]
    hard_failures: list[str] = Field(default_factory=list)
    overall_score: float = Field(ge=0, le=1)
    suggested_repairs: list[dict[str, Any]] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]
    operator_notes: str | None = None


class SingleImageProductionRecord(BaseModel):
    schema_version: Literal["cmf.single_image_production_record.v1"]
    production_record_id: UUID
    input: SingleImageEngineInput
    router_decision: SingleImageRouterDecision
    scene_spec: SingleImageSceneSpecV2
    render_receipt: SingleImageSkiaRenderReceipt | None = None
    evaluation_receipt: SingleImageEvaluationReceiptV2 | None = None
    status: SingleImageReviewStatus = SingleImageReviewStatus.draft
    approval_policy_report_id: UUID | None = None
```

## 6. Backward Compatibility Fallback

If an existing asset package item is labeled only as `poll_visual`, `meme_visual`, `tweet_like_quote`, `super_visual`, or `reaction_seed` without a subtype:

1. attempt subtype inference from `content_shape`, `asset_derivative_id`, and `content_archetype_id`;
2. if confidence is below threshold, block render with `SINGLE_IMAGE_FORMAT_SUBTYPE_REQUIRED`;
3. provide three compatible subtype candidates to the operator;
4. record operator selection in `SingleImageProductionRecord`;
5. never render a still visual from only a broad family label.

If registry loading fails:

- do not fall back to freeform prompt generation;
- allow only deterministic minimal quote fallback for verified quote outputs;
- block all generated SuperVisuals until registry and provider policy are available.

If a composition cannot satisfy text budget:

- rewrite or compress copy within source-safe constraints;
- choose another candidate composition;
- ask operator for revision;
- never auto-shrink below readability threshold.

## 7. Tasks

| Task ID | Task |
|---|---|
| T099-01 | Add `contracts/single_image.py` with CMF-adapted Pydantic models. |
| T099-02 | Add registry loaders for composition registry, router policy, Skia component catalog, provider responsibility policy, Ideogram prompt contracts, and eval rubrics. |
| T099-03 | Validate the 28 composition contracts and all normalized zones. |
| T099-04 | Add archetype/derivative/content-shape query methods. |
| T099-05 | Add `SingleImageRouterService` with hard constraints, scoring, penalties, and candidate diversity. |
| T099-06 | Add `SingleImageCompilerService` to build scene specs, provider jobs, render receipts, eval receipts, and production records. |
| T099-07 | Extend `AssetPackageItem` with still visual subtype refs and SuperVisual routing support. |
| T099-08 | Add content format compatibility tests for `SPV-*`, `VPL-*`, `TWQ-*`, `MEM-*`, and `RCT-SEED`. |
| T099-09 | Add provider capability checks and responsibility validation. |
| T099-10 | Connect Single Image SceneSpec to TS-CMF-095 Geometrics/Skia runtime. |
| T099-11 | Add review read model for candidate comparison, scene spec edit, layer/cutout review, final preview, eval repairs, and approval. |
| T099-12 | Add approval blockers for source fidelity, text overflow, unsafe anchor, identity mismatch, primitive failure, eval failure, and missing Skia hash. |
| T099-13 | Generate TypeScript contracts from Python. |
| T099-14 | Add golden fixtures for all eight families and the five included examples. |
| T099-15 | Add regression fixtures proving archetypes can route to carousel, SuperVisual, visual poll, quote card, meme, reaction seed, or video depending on derivative and output intent. |

## 8. Acceptance Criteria

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC099-01 | All eight canonical single-image registry files load from `registries/` paths and hash successfully. | Runtime reads directly from `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE` in production. | Phase5-M01 |
| AC099-02 | All 28 composition contracts validate zones, text budgets, provider modes, aspect ratios, and eval profiles. | A composition has a zone extending outside canvas and still renders. | Phase4-M04 |
| AC099-03 | A SuperVisual package item routes through `SPV-CON`, `SPV-SYM`, or `SPV-PRM` and selects a compatible composition. | A SuperVisual is incorrectly converted into a carousel slide. | Phase4-M02 |
| AC099-04 | Archetype routing is output-family-aware. | `archetype.myth_debunk.v1` always becomes `CAR-JUX` even when asset derivative asks for `SPV-CON`. | Phase4-M01 |
| AC099-05 | Router returns three candidates when available, with score breakdown and family diversity. | Router returns only `BLUNT_IMPERATIVE_POSTER` with no alternatives or explanation. | Phase3-M02 |
| AC099-06 | Operator override requires and stores an override reason. | Operator changes composition but the receipt cannot explain why. | Phase5-M01 |
| AC099-07 | Ideogram never owns final text, quotes, statistics, handles, metadata, dates, logos, final borders, or final geometry. | Generated image ships with misspelled headline baked into pixels. | Phase1-M05 |
| AC099-08 | Qwen layered and SAM3 are called only when provider mode and asset needs justify them. | Pure typography quote card spends provider budget on unnecessary layer extraction. | Phase3-M05 |
| AC099-09 | Every scene spec includes at least three primitive refs across meaning, delivery, and format/material roles. | Scene spec uses `premium` as primitive proof. | Phase4-M01 |
| AC099-10 | Quote, stat, screenshot, sports, and promo outputs block when source objects are unverified. | Sports stat collage publishes an unverified statistic. | Phase4-M04 |
| AC099-11 | Skia render receipt includes renderer version, font manifest hash, asset hashes, scene spec hash, output URI, and SHA-256. | Final PNG exists with no reconstructable render receipt. | Phase5-M01 |
| AC099-12 | Evaluation profile threshold and hard failures block approval until repaired or rejected. | `quote_source_fidelity` hard failure passes because visual is attractive. | Phase4-M05 |
| AC099-13 | Review UI exposes composition ID, family, candidates, score breakdown, source, eval, provider jobs, and approval state. | Operator sees only a thumbnail and approve button. | Phase3-M02 |
| AC099-14 | Content asset code appears on review, receipt, export, and publishing intent. | File is named `final_post.png` with no guest/package scope. | Phase5-M01 |
| AC099-15 | Regression tests prove carousel and SuperVisual routes are separate. | Single-image router accepts `CAR-LST` or carousel builder accepts `SPV-CON` as a slide atom. | Phase4-M04 |

## 9. Dependencies

| Dependency | Purpose |
|---|---|
| `TS-CMF-033-archetype-and-asset-derivative-routing.md` | Upstream archetype and derivative selection. |
| `TS-CMF-034-guest-asset-pack-spec-generation.md` | Supplies still visual package item intent. |
| `TS-CMF-036-complete-editing-session-creation-from-approved-source.md` | Creates editing session from approved source. |
| `TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Provider capability and job receipts. |
| `TS-CMF-044-generative-provider-adapters.md` | Generative adapters. |
| `TS-CMF-048-provider-job-retry-resume-cancel-and-compensation.md` | Provider retry/resume/cancel behavior. |
| `TS-CMF-049-svre-aurore-and-asset-research-engine-routing.md` | Visual research and asset source candidates. |
| `TS-CMF-050-evaluation-receipt-generation.md` | Evaluation receipt generation. |
| `TS-CMF-053-approval-blockers.md` | Approval blockers. |
| `TS-CMF-070-ui-architecture-and-operator-experience.md` | Operator PWA and Telegram review architecture. |
| `TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Canonical composition JSON and preview approval rules. |
| `TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine-driven testing and primitive eval coverage. |
| `TS-CMF-081-composition-template-family-registry-and-content-asset-codes.md` | Template family and content asset code registry. |
| `TS-CMF-082-brand-genesis-substrate-resolver-for-composition-runtime.md` | Brand substrate, visual constitution, micro-semiotic anchor library. |
| `TS-CMF-087-micro-semiotic-anchor-selection-and-risk-gate.md` | Micro-semiotic anchor risk gate. |
| `TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Ideogram composition direction bridge. |
| `TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Qwen/SAM3/layer extraction and repair queue. |
| `TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Renderer prop compiler and component harness. |
| `TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval and operator workbench. |
| `TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Final Geometrics/PRETEXT/SAM3/Skia still render path. |
| `TS-CMF-096` through `TS-CMF-098` | Carousel-specific sibling path. Must remain separate. |
| `single_image_*` registries | Runtime registry/eval/provider/source evidence. |
| `TS-CMF-100` through `TS-CMF-105` | Buildable child specs that implement this umbrella. |

## 10. Testing Strategy

### Unit Tests

- Registry loader validates all 28 compositions.
- Router policy validates weights sum and required hard constraints exist.
- Bounds validator rejects zones outside normalized canvas.
- Text budget validator rejects overflow before provider calls.
- Provider responsibility validator rejects forbidden ownership, such as Ideogram final text.
- Eval rubric loader validates profile thresholds and hard failures.
- Content format resolver maps `SPV-*`, `VPL-*`, `TWQ-*`, `MEM-*`, and `RCT-SEED` correctly.

### Integration Tests

- Build `example_myth_debunk` from input to selected `BLUNT_IMPERATIVE_POSTER`.
- Build `example_identity_poll` to selected `WOULD_YOU_RATHER_IDENTITY_LADDER`.
- Build `example_interview_quote` to selected `QUOTE_ON_CLOSEUP_COMMENTARY`.
- Build `example_framework` to selected `CARTOON_QUAD_FRAMEWORK`.
- Build `example_social_reaction` to selected `SOCIAL_SCREENSHOT_REACTION_CARD`.
- Build one `SPV-CON`, one `SPV-SYM`, and one `SPV-PRM` through route, scene spec, provider planning, Skia receipt, eval receipt, and approval blocker.
- Verify pure typography path skips Ideogram, Qwen, and SAM3 while still passing primitives and Skia render.
- Verify generated metaphor path uses Ideogram, optional Qwen, SAM3 when masks are needed, Geometrics, and Skia.
- Verify documentary social card path blocks fabricated handles or unverified screenshot objects.

### Negative Fixtures

| Fixture | Expected Failure |
|---|---|
| `negative_supervisual_as_carousel_slide` | `SINGLE_IMAGE_OUTPUT_FAMILY_MISMATCH` |
| `negative_unknown_composition_id` | `SINGLE_IMAGE_COMPOSITION_NOT_REGISTERED` |
| `negative_text_overflow` | `SINGLE_IMAGE_TEXT_BUDGET_EXCEEDED` |
| `negative_missing_brand_context` | `BRAND_CONTEXT_VERSION_REQUIRED` |
| `negative_missing_primitive_triad` | `SINGLE_IMAGE_PRIMITIVE_TRIAD_MISSING` |
| `negative_ideogram_final_text` | `PROVIDER_RESPONSIBILITY_VIOLATION` |
| `negative_unverified_quote` | `SOURCE_FIDELITY_REQUIRED` |
| `negative_unsafe_msa` | `MICRO_SEMIOTIC_ANCHOR_UNSAFE` |
| `negative_identity_mismatch` | `IDENTITY_MISMATCH` |
| `negative_no_skia_hash` | `SKIA_RENDER_RECEIPT_REQUIRED` |

### Golden Fixtures

| Fixture | Proof |
|---|---|
| `golden_spv_con_conceptual_metaphor` | SuperVisual conceptual contrast route, source-backed metaphor, Skia render receipt. |
| `golden_spv_sym_symbolic_scene` | Symbolic image route with primitive-backed visual metaphor and safe anchors. |
| `golden_spv_prm_premium_brand_visual` | Premium single-frame brand-forward composition with deterministic typography. |
| `golden_vpl_wyr_identity_ladder` | Poll clarity, option parity, vote impulse, and source-safe framing. |
| `golden_twq_img_quote` | Quote source fidelity, speaker attribution, identity-safe crop, editable text. |
| `golden_mem_rel_recognition` | Recognition meme route with safe distortion and primitive proof. |
| `golden_social_reaction_card` | Verified screenshot/social proof object with deterministic shell and context. |
| `golden_cartoon_framework_quad` | Four-panel framework with density control and Skia geometry. |

### CI Gates

- Registry hash snapshot test.
- Generated TypeScript contract parity test.
- Provider responsibility policy test.
- Primitive triad coverage test.
- Eval threshold and hard-failure test.
- Skia output hash determinism test under same renderer environment.
- Review read model completeness test.
- Content asset code presence test across receipt, review, export, and publishing intent.

## Spec Audit Receipt

| Check | Status |
|---|---|
| Files read listed | Yes |
| Existing backend integration included | Yes |
| ADR-05 primitive obligations declared | Yes |
| CBAR mandates declared | Yes |
| Entry and exit objects explicit | Yes |
| Registry migration paths explicit | Yes |
| SuperVisuals separated from carousels | Yes |
| Child specs required before implementation complete | Yes |
| Provider responsibilities explicit | Yes |
| Skia deterministic render path explicit | Yes |
| Acceptance criteria include failure examples | Yes |
| Testing strategy includes positive, negative, and golden fixtures | Yes |
