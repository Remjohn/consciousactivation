---
tech_spec_id: "TS-CMF-097"
title: "Carousel Builder Engine, Compiler Workflow, and Skia Export Runtime"
story_id: "7.25"
story_title: "Carousel Builder Engine"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "Carousel builder engine MCDA synthesis and deep research integration"
pipeline_stage: "8 / 9 / 10 / 11 / 12 / 13"
entry_object: "CreateCarouselRequest, BrandContextVersion, ExpressionMoment, AssetPackageSpec, TargetPlatformSpec, VoiceVisualDNA"
exit_object: "CarouselSpec, CarouselSequencePlan, GeometricsLayoutPlan, SkiaStillRenderOutput, CarouselExportManifest, CarouselBuilderReceipt"
validation_contract: "source lineage, brand lock, slide atom meaning, primitive triads, provider role boundaries, layer/mask readiness, rough annotation parity, Skia render determinism, export manifest, review approval"
required_receipt: "CarouselBuilderReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / Pi Command Bus / Durable workflow / Ideogram 4 / Qwen-Image-Layered / SAM3 / PRETEXT / rough annotation manifest / Skia CanvasKit / PWA and Telegram review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-097: Carousel Builder Engine, Compiler Workflow, and Skia Export Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section ERA3 protocol, backend mapping, ADR-05 primitive, CBAR, acceptance, and testing requirements. |
| `THE CMF STUDIO/deep-research-report.md` | Target architecture for the Carousel Builder Engine using typed context, DSPy, Ideogram 4, Qwen-Image-Layered, SAM3, rough annotation, Skia, PWA, and Telegram review. |
| `THE CMF STUDIO/docs/audits/CMF_CAROUSEL_BUILDER_ENGINE_MCDA_2026-06-24.md` | MCDA comparison proving the current specs are aligned but fragmented and runtime implementation is incomplete. |
| `THE CMF STUDIO/docs/architecture.md` | Canonical Python-first Command Bus, durable workflow, provider boundary, PWA, Telegram, receipt, and object-store architecture. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines content asset codes, including `CAR-LST` and `CAR-JUX`. |
| `THE CMF STUDIO/docs/composition-libraries/CMF_Carousel_Slide_Composition_Library.md` | Human-readable carousel slide atom doctrine. |
| `THE CMF STUDIO/registries/composition/carousel_slide_composition_library.v1.json` | Machine-readable slide atom registry that the builder must query. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Composition primitive triad obligations for meaning, delivery, and format/material coverage. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-003.yaml` | Narrative Structural Backbone; required for carousel sequence arc. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-012.yaml` | Grid as Cognitive Relief; required for carousel continuity. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-018.yaml` | Sequence Over Single Image; required for slide-to-slide variety. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | Composition as Eye-Path Engineering; required per slide. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Provider capability registry and job receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Existing deterministic rendering contract that must be extended, not misused, for still carousel output. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-044-generative-provider-adapters.md` | Generative adapter boundary and provider receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | PWA, Telegram, command, receipt, review, and generated-contract UI architecture. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Ideogram composition director bridge. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Qwen/SAM3/layer extraction and repair dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Renderer prop compiler, component harness, and annotation cue dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Eval, visual fixture, and operator approval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Still visual Geometrics, Skia, SAM3, PRETEXT, and rough annotation runtime dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Upstream slide atom and sequence builder dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` | Visual grammar atlas and composition router dependency between sequence planning and Geometrics. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Current runtime renderer enum only covers Remotion and Motion Canvas; Skia still rendering must be added. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Current runtime renders video-style outputs; carousel still exports require new output modes. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Current provider registry lacks a `skia_canvaskit.still_render.v1` capability. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Current composition contracts stop before the full carousel compiler contract. |
| `THE CMF STUDIO/src/ccp_studio/contracts/assembly.py` | Existing generic `LayerManifest` pattern to extend for carousel-specific layered still composition. |

## 2. Overview

The Carousel Builder Engine is the integrated compiler that turns locked CMF context into export-ready carousel assets. It is not a prompt-to-image shortcut and it is not a generic template picker. It must bind:

- interview-first and expression-backed source context;
- locked guest or brand workspace context;
- content asset code and carousel subtype;
- slide atom composition meaning;
- primitive triad evaluation;
- provider-specific generative and decomposition roles;
- deterministic Skia still rendering;
- operator review and approval receipts.

The MCDA result showed the correct shape:

```text
CreateCarouselRequest
-> context hydration
-> CarouselSpec
-> CarouselSequencePlan
-> CompositionRouterDecision and CarouselSlideVisualGrammarPlan
-> Ideogram composition direction when required
-> Qwen layered decomposition when required
-> SAM3 mask and safe-zone cleanup when required
-> PRETEXT text measurement
-> rough annotation cue manifest
-> GeometricsLayoutPlan
-> Skia still render job
-> CarouselExportManifest
-> Eval and Review Workbench
-> CarouselBuilderReceipt
```

This spec binds the fragmented existing specs into one executable workflow. `TS-CMF-096` owns slide atoms and sequence planning. `TS-CMF-095` owns deterministic still visual geometry and Skia rendering. `TS-CMF-097` owns the full carousel builder command lifecycle from request validation through export approval.

This spec explicitly does not:

- bypass the interview-first source pipeline when an interview or transcript exists;
- accept loose prompts as production input;
- use Ideogram 4 as final text, final identity, final geometry, or final render truth;
- use Remotion or Motion Canvas as final still carousel renderers;
- rely on browser screenshots as production still exports;
- treat ImageCritic or any third-party model as the primary aesthetic authority;
- introduce newsletters or unsupported content formats.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-097-001 | Command Bus | Every carousel mutation is issued as a command and produces a receipt. No background carousel mutation bypasses the command spine. |
| DEP-CMF-097-002 | `BrandContextVersion` | Locks guest or brand workspace identity, visual DNA, typography, colors, claims, banned claims, motifs, rights, and source registry refs. |
| DEP-CMF-097-003 | `ExpressionMoment` | Supplies the approved source moment, quote, meaning operation, archetype route, audience recognition point, and timestamp lineage. |
| DEP-CMF-097-004 | `AssetPackageSpec` and `AssetPackageItem` | Supplies `CAR-LST` or `CAR-JUX` asset intent, approved images, logos, subject cutouts, screenshots, references, and rights state. |
| DEP-CMF-097-005 | `TargetPlatformSpec` | Defines target dimensions, safe margins, export formats, platform caps, and delivery constraints. |
| DEP-CMF-097-006 | `VoiceVisualDNA` | Carries style constraints for visual composition, typography, annotation, density, tone, hook style, and banned visual moves. |
| DEP-CMF-097-007 | `carousel_slide_composition_library.v1.json` | Supplies known slide atoms, sequence roles, primitive defaults, visual grammar, and query tags. |
| DEP-CMF-097-008 | `CarouselSequencePlan` | Upstream plan from TS-CMF-096; no carousel can materialize without it. |
| DEP-CMF-097-008A | `CompositionRouterDecision` and `CarouselSlideVisualGrammarPlan` | Atlas-router output from TS-CMF-098; binds each slide atom to a concrete visual grammar before Geometrics. |
| DEP-CMF-097-009 | `CompositionLayoutPlan` | Ideogram-derived composition plan from TS-CMF-088; used only when generative composition direction is required. |
| DEP-CMF-097-010 | `LayerManifest` and `LayerExtractionResult` | Qwen/SAM3 normalized layers, masks, z-order, subject safe zones, and editable asset refs. |
| DEP-CMF-097-011 | `TextAnnotationCueManifest` | Rough-notation-compatible underline, highlight, box, circle, strike, crossed-off, and bracket cue data. |
| DEP-CMF-097-012 | `GeometricsLayoutPlan` | Resolved coordinates, collision outcomes, typography measurements, masks, and Skia readiness. |
| DEP-CMF-097-013 | `SkiaStillRenderOutput` | Deterministic PNG/JPEG/PDF/PPTX-ready still outputs with hashes and preview/final parity. |
| DEP-CMF-097-014 | `CarouselExportManifest` | Export target manifest for Instagram, LinkedIn document, Telegram preview, web embed, or custom delivery. |
| DEP-CMF-097-015 | `CarouselBuilderReceipt` | Immutable proof that source, brand, primitives, providers, render, export, review, and approval are valid. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/carousel_builder.py` | New Pydantic contracts for request, spec, workflow state, routing, export, and receipt objects in Section 5. |
| `src/ccp_studio/services/carousel_builder_service.py` | New service that validates requests, hydrates context, builds specs, coordinates providers, and emits receipts. |
| `src/ccp_studio/services/composition_router_service.py` | Required atlas-router service from TS-CMF-098 that selects concrete visual grammar after sequence planning. |
| `src/ccp_studio/workflows/carousel_builder.py` | New durable workflow owner for long-running carousel jobs, provider retries, human approval pauses, and resumability. |
| `src/ccp_studio/contracts/deterministic_rendering.py` | Add `skia_still` as a deterministic renderer target for still visual outputs. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Add still-render output modes so final carousel artifacts are PNG/JPEG/PDF/PPTX manifest outputs, not `.mp4` video-style URIs. |
| `src/ccp_studio/services/provider_operations_service.py` | Add provider capability record `skia_canvaskit.still_render.v1` and provider job receipts for still renders. |
| `src/ccp_studio/contracts/composition.py` | Add or import `CompositionLayoutPlan` and `GeometricsHandoffPlan` bindings required by TS-CMF-088 and TS-CMF-095. |
| `src/ccp_studio/contracts/assembly.py` | Extend `LayerManifest` for carousel slide layer roles, safe zones, masks, z-index, and export refs. |
| `src/ccp_studio/services/composition_service.py` | Route approved Ideogram composition plates into carousel materialization rather than stopping at image lineage. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Validate slide and sequence primitive triads from `cmf_composition_primitive_triads.v1.json`. |
| `src/ccp_studio/services/review_workbench_service.py` | Expose carousel evidence read model to PWA and Telegram quick review. |
| `src/ccp_studio/api/main.py` | Register API routes only through existing API patterns if command submission or review endpoints are needed. |
| Object storage | Persist Ideogram source images immediately, generated layers, masks, Skia outputs, PDF exports, hashes, and review thumbnails. |

### Legacy Migration Context

Legacy CMF and CVE work proved three important design constraints:

- still visual content was intended to be deterministic and composition-driven, not prompt-only;
- Skia, SAM3, PRETEXT, and Geometrics were used to convert visual intent into coordinates and renderable artifacts;
- carousel, visual poll, tweet-like quote, meme, Super Visual, and reaction still formats need format-specific composition meaning.

This spec migrates those principles into the CMF STUDIO project folder as contracts, registries, services, workflows, and tests. It must not import production runtime directly from `D:\Work\The Conscious Coaching Factory`; that location remains reference-only unless a later migration spec explicitly copies a reviewed asset, fixture, or registry into `THE CMF STUDIO`.

### ADR-05 Primitives

Every carousel slide must pass at least three primitive validations across:

| Role | Required Proof |
|---|---|
| `meaning_transform` | The slide performs a real idea operation such as contrast, explanation, inversion, proof, myth-break, analogy, or stakes. |
| `delivery_shape` | The slide guides comprehension through structure, rhythm, hierarchy, evidence, recognition, or sequence. |
| `format_material` | The slide's physical composition is justified by eye path, grid, texture, paper layer, human proof, negative space, or frame behavior. |

The carousel sequence must also prove:

| Sequence Requirement | Primitive |
|---|---|
| Narrative arc | `PRM-BUS-003` Narrative Structural Backbone |
| Grid continuity | `PRM-BUS-012` The Grid as Cognitive Relief |
| Slide-to-slide variety | `PRM-VSG-018` Sequence Over Single Image |
| Per-slide scan path | `PRM-VSG-001` Composition as Eye-Path Engineering |

No plan may use vague labels such as `premium`, `viral`, `clean`, `social`, or `cinematic` as primitive proof. Exact primitive IDs or approved registry refs are required.

### CBAR Mandate Enforcement

| Mandate | Governing Story | Enforcement |
|---|---|---|
| Phase1-M05: The Deterministic Override Rule | Story 2.2 | Final still rendering must be deterministic through `skia_still`; generative outputs can direct or supply assets but cannot be final truth. |
| Phase3-M02: Per-Slide Feedback Rule | Story 1.2 | Operator review read model exposes per-slide blockers, primitive status, source lineage, render hashes, and repair actions. |
| Phase3-M05: Modular CMF Recovery Rule | Story 3.2 | Workflow can resume from context hydration, spec planning, provider materialization, Geometrics, render, export, or approval without restarting the whole job. |
| Phase4-M01: The Intelligence-Gated Intercept Rule | Story 1.1 | Blocks any request missing locked brand context, source refs, format subtype, target platform, and primitive eval path. |
| Phase4-M02: The Cinematic Meaning Rule | Story 2.1 | Every slide must declare composition meaning and source role; visual balance alone cannot pass. |
| Phase4-M04: The Frictionless Block Rule | Story 4.1 | Cheap blockers stop before expensive provider or render calls: unknown atom, missing primitive triad, missing masks, text overflow, or unsupported export target. |
| Phase4-M05: The Actionable Rejection Rule | Story 5.1 | Every rejection names slide index, object refs, provider refs, failed primitive, blocker code, and repair instruction. |
| Phase5-M01: The Verifiable Artifact Rule | Story 1.1 | Outputs are reconstructable from request, spec, registry version, provider receipts, layer manifests, Skia job, export manifest, and hashes. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| `CreateCarouselRequest` is the only production entry object. | Prevents loose prompt generation and keeps brand, source, asset, target, and DNA context together. |
| `CarouselSpec` becomes immutable after plan approval. | Later stages add manifests and receipts without changing approved intent. |
| TS-CMF-096 remains the slide atom authority. | Slide meaning and sequence grammar should be reusable registry data, not invented per generation. |
| Ideogram 4 is optional per slide. | Typography-only, quote, diagram, or pure Skia slides do not need a whole-image composition pass. |
| Qwen and SAM3 are required only when the plan needs editable generated layers or masks. | Pure type/grid slides can skip expensive decomposition while still passing primitive and layout gates. |
| Rough annotation is a typed cue manifest. | DOM-only rough notation cannot be the source of final output; Skia or motion renderers need replayable cue data. |
| Skia/CanvasKit owns final still outputs. | Carousel assets require deterministic text geometry, masks, layers, export hashes, and PDF/still parity. |
| Remotion and Motion Canvas are derivative renderers here. | They may create animated previews or video derivatives but not the final still carousel truth. |
| PWA is the full review surface; Telegram is quick review. | Telegram must share the same evidence read model but should not become the heavyweight authoring canvas. |

## 4. Implementation Plan

1. Add `contracts/carousel_builder.py` with the Section 5 Pydantic contracts.
2. Add a carousel registry loader that reads `registries/composition/carousel_slide_composition_library.v1.json`, validates schema, exposes query methods, and returns registry hashes.
3. Add DSPy signatures for `ContextHydrator`, `CarouselSpecPlanner`, `SlideAtomSelector`, `CompositionDirector`, `LayerDirector`, `PrimitiveGateEvaluator`, `QCManager`, and `RepairCoordinator`.
4. Add `services/carousel_builder_service.py` with methods for request validation, context hydration, spec planning, sequence planning, atlas composition routing, provider routing, materialization, render handoff, export, and receipt emission.
5. Add `workflows/carousel_builder.py` durable workflow with resumable states:
   - `accepted`;
   - `hydrated`;
   - `planned`;
   - `sequence_selected`;
   - `awaiting_plan_approval`;
   - `materializing`;
   - `geometrics_ready`;
   - `rendered`;
   - `exported`;
   - `awaiting_operator_approval`;
   - `approved`;
   - `failed`.
6. Extend `provider_operations_service.py` with `skia_canvaskit.still_render.v1` capability, cost metadata, artifact classes, and receipt expectations.
7. Extend `deterministic_rendering.py` with `skia_still` and add output modes for single slide, slide set, stitched preview, platform export, PDF document, and editable package.
8. Extend `deterministic_rendering_service.py` so still jobs produce `SkiaStillRenderOutput` and `CarouselExportManifest` instead of video-only final URIs.
9. Bind TS-CMF-088 by routing only slides with `needs_ideogram_composition=true` into the Ideogram composition director.
10. Bind TS-CMF-098 by converting each slide atom into `CompositionRouterDecision` and `CarouselSlideVisualGrammarPlan` before provider materialization.
11. Bind TS-CMF-089 by routing only slides with `needs_layered_decomposition=true` into Qwen/SAM3/repair workers and normalizing the layer manifests.
12. Bind TS-CMF-095 by converting approved visual grammar plans into `GeometricsLayoutPlan` and sealed `SkiaRenderJob` packets.
13. Add rough annotation cue compilation so underline, highlight, box, circle, strike-through, crossed-off, and bracket cues replay in Skia preview/final paths.
14. Add `CarouselExportManifest` generation for Instagram feed images, LinkedIn document PDF, Telegram preview, web embed, and custom target exports.
15. Add PWA and Telegram read model projection using the same canonical evidence object.
16. Add approval blockers using TS-CMF-050, TS-CMF-052, and TS-CMF-053 patterns where available.
17. Generate JSON Schema and TypeScript types from the Python contracts and commit generated artifacts only where the project already stores generated API types.
18. Add positive and negative fixtures for `CAR-LST` and `CAR-JUX`.
19. Add an operational readiness check that proves provider capabilities, object storage, Skia render worker, export paths, and review commands are configured.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class TargetPlatformSpec(BaseModel):
    schema_version: Literal["cmf.target_platform_spec.v1"]
    platform: Literal[
        "instagram_feed",
        "linkedin_document",
        "telegram_preview",
        "web_embed",
        "custom",
    ]
    aspect_ratio: str
    width_px: int
    height_px: int
    max_slides: int
    export_formats: list[Literal["png", "jpeg", "pdf", "pptx", "zip"]]
    safe_margin_px: int = 48
    platform_notes: dict = Field(default_factory=dict)


class VoiceVisualDNA(BaseModel):
    schema_version: Literal["cmf.voice_visual_dna.v1"]
    visual_style: dict
    typography_preferences: dict
    annotation_style: dict
    voice_style: dict | None = None
    banned_visual_moves: list[str] = Field(default_factory=list)
    required_brand_motifs: list[str] = Field(default_factory=list)


class CreateCarouselRequest(BaseModel):
    schema_version: Literal["cmf.create_carousel_request.v1"]
    request_id: UUID
    organization_id: UUID
    brand_workspace_id: UUID
    actor_id: UUID
    brand_context_version_id: UUID
    expression_moment_ids: list[UUID] = Field(min_length=1)
    asset_package_spec_id: UUID
    format_code: Literal["CAR-LST", "CAR-JUX"]
    target_platforms: list[TargetPlatformSpec] = Field(min_length=1)
    voice_visual_dna: VoiceVisualDNA
    requested_slide_count: int = Field(ge=2, le=20)
    source_refs: list[str] = Field(min_length=1)
    primitive_eval_receipt_refs: list[str] = Field(default_factory=list)
    operator_notes: str | None = None


class CarouselSpecSlideIntent(BaseModel):
    schema_version: Literal["cmf.carousel_spec_slide_intent.v1"]
    slide_index: int
    slide_atom_code: str
    source_expression_moment_id: UUID
    composition_meaning: str
    source_role: str
    headline: str
    body_text: str | None = None
    visual_intent: str
    callout_text: str | None = None
    needs_ideogram_composition: bool
    needs_layered_decomposition: bool
    needs_sam3_cleanup: bool
    needs_rough_annotation: bool
    primitive_refs: list[str] = Field(min_length=3)
    query_tags: list[str] = Field(default_factory=list)


class CarouselSpec(BaseModel):
    schema_version: Literal["cmf.carousel_spec.v1"]
    carousel_spec_id: UUID
    request_id: UUID
    brand_context_version_id: UUID
    registry_version: str
    registry_hash: str
    format_code: Literal["CAR-LST", "CAR-JUX"]
    narrative_arc: list[str] = Field(min_length=2)
    slides: list[CarouselSpecSlideIntent] = Field(min_length=2)
    approved_for_materialization: bool
    blocker_codes: list[str] = Field(default_factory=list)


class CarouselBuildCommandState(BaseModel):
    schema_version: Literal["cmf.carousel_build_command_state.v1"]
    workflow_id: UUID
    request_id: UUID
    state: Literal[
        "accepted",
        "hydrated",
        "planned",
        "sequence_selected",
        "awaiting_plan_approval",
        "materializing",
        "qc_failed",
        "geometrics_ready",
        "rendered",
        "exported",
        "awaiting_operator_approval",
        "approved",
        "failed",
    ]
    completed_steps: list[str] = Field(default_factory=list)
    resumable_from_step: str | None = None
    blocker_codes: list[str] = Field(default_factory=list)


class CarouselProviderRoutingDecision(BaseModel):
    schema_version: Literal["cmf.carousel_provider_routing_decision.v1"]
    slide_index: int
    slide_atom_code: str
    use_ideogram_4: bool
    use_qwen_image_layered: bool
    use_sam3: bool
    use_repair_provider: bool
    use_skia_still: bool
    reason: str
    provider_capability_refs: list[str]
    blocker_codes: list[str] = Field(default_factory=list)


class SkiaStillRenderOutput(BaseModel):
    schema_version: Literal["cmf.skia_still_render_output.v1"]
    output_id: UUID
    skia_render_job_id: UUID
    mode: Literal[
        "single_slide",
        "carousel_slide_set",
        "stitched_preview",
        "platform_export",
        "pdf_document",
        "editable_package",
    ]
    output_uris: list[str]
    output_hashes: list[str]
    width_px: int
    height_px: int
    export_format: Literal["png", "jpeg", "pdf", "pptx", "zip"]
    preview_final_parity_hash: str | None = None


class CarouselExportManifest(BaseModel):
    schema_version: Literal["cmf.carousel_export_manifest.v1"]
    export_manifest_id: UUID
    request_id: UUID
    carousel_spec_id: UUID
    target_platforms: list[TargetPlatformSpec]
    render_output_refs: list[UUID]
    delivery_bundle_uris: list[str]
    export_hashes: list[str]
    approved_for_delivery: bool
    blocker_codes: list[str] = Field(default_factory=list)


class CarouselBuilderReceipt(BaseModel):
    schema_version: Literal["cmf.carousel_builder_receipt.v1"]
    receipt_id: UUID
    request_id: UUID
    workflow_id: UUID
    carousel_spec_id: UUID
    carousel_sequence_plan_id: UUID
    brand_context_version_id: UUID
    provider_job_receipt_refs: list[str]
    primitive_eval_receipt_refs: list[str] = Field(min_length=1)
    render_output_refs: list[UUID]
    export_manifest_id: UUID
    operator_approval_receipt_id: UUID | None = None
    approved_for_delivery: bool
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Required Fallback |
|---|---|
| Existing carousel request has only a prompt and no typed context | Block with `CAROUSEL_TYPED_CONTEXT_REQUIRED`. |
| Carousel item lacks `CAR-LST` or `CAR-JUX` subtype | Block with `FORMAT_SUBTYPE_REQUIRED`. |
| Slide does not resolve to a known slide atom | Block with `CAROUSEL_SLIDE_ATOM_UNKNOWN`. |
| Slide has fewer than three primitive refs | Block with `PRIMITIVE_TRIAD_REQUIRED`. |
| Ideogram output contains baked final text that conflicts with production text plan | Block or route to repair with `BAKED_TEXT_NOT_FINAL_TRUTH`. |
| Qwen or SAM3 is unavailable for a layer-dependent slide | Block with `LAYERED_DECOMPOSITION_UNAVAILABLE`; allow pure typography slides only if no layer dependency exists. |
| Rough annotation runtime is unavailable | Continue only if no primitive or slide meaning depends on the annotation; otherwise block with `ANNOTATION_CUE_UNAVAILABLE`. |
| `skia_still` provider capability is unavailable | Block final export with `SKIA_STILL_RENDERER_UNAVAILABLE`. |
| Remotion or Motion Canvas is requested as final still renderer | Block with `FINAL_STILL_RENDERER_MUST_BE_SKIA`. |
| ImageCritic or a non-commercial evaluator is unavailable | Do not block by default; use OCR, semantic, layout, mask, primitive, and brand checks unless explicitly configured as an R&D-only optional worker. |
| PPTX export is unsupported | Export PNG/PDF/ZIP where configured and mark `editable_package_unavailable`; do not mark PPTX as delivered. |
| Operator has not approved the export manifest | Block delivery with `OPERATOR_APPROVAL_REQUIRED`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T097-01 | Add `contracts/carousel_builder.py` with Section 5 contracts and JSON Schema generation tests. |
| T097-02 | Add carousel slide atom registry loader, hash verification, query API, and invalid-registry tests. |
| T097-03 | Add `CarouselBuilderService.validate_request()` with typed context, brand lock, format code, source refs, target platform, and primitive requirements. |
| T097-04 | Add `CarouselBuilderService.plan_carousel_spec()` using DSPy signatures and TS-CMF-096 slide atom selection. |
| T097-04A | Call TS-CMF-098 `CompositionRouterService` so every slide receives a concrete `composition_id` and `CarouselSlideVisualGrammarPlan` before Geometrics. |
| T097-05 | Add `CreateCarouselWorkflow` with resumable state transitions and command receipts. |
| T097-06 | Add provider routing decisions per slide, including when to skip Ideogram/Qwen/SAM3 for pure Skia typography slides. |
| T097-07 | Add `skia_canvaskit.still_render.v1` provider capability and provider receipt expectations. |
| T097-08 | Add `DeterministicRenderer.skia_still` and still output modes to deterministic rendering contracts and services. |
| T097-09 | Add Ideogram materialization bridge for slides requiring generated composition direction. |
| T097-10 | Add Qwen/SAM3 normalization path for layer and mask dependent slides. |
| T097-11 | Add rough annotation cue manifest generation and parity checks. |
| T097-12 | Add Geometrics handoff integration and sealed `SkiaRenderJob` generation. |
| T097-13 | Add `CarouselExportManifest` service for Instagram, LinkedIn PDF, Telegram preview, web embed, and custom exports. |
| T097-14 | Add PWA and Telegram carousel review read model projection with identical evidence source. |
| T097-15 | Add approval blocker integration and operator approval receipt references. |
| T097-16 | Add positive fixtures for `CAR-LST` explanation carousel and `CAR-JUX` juxtaposition carousel. |
| T097-17 | Add negative fixtures for missing brand context, unknown slide atom, missing primitives, missing masks, Skia unavailable, and unapproved export. |
| T097-18 | Update generated TypeScript contracts and tech-spec README dependency order. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC097-01 | A carousel build cannot start from a loose prompt alone. | `make a premium carousel about leadership` is accepted without brand, source, and target objects. | Phase4-M01 |
| AC097-02 | Every carousel request binds a locked `BrandContextVersion`, at least one `ExpressionMoment`, an `AssetPackageSpec`, and a `TargetPlatformSpec`. | Operator accidentally generates guest A's content inside guest B's workspace. | Phase4-M01 |
| AC097-03 | Every slide resolves to a known slide atom from `carousel_slide_composition_library.v1.json`. | Slide 4 uses freeform `template_blue_4`. | Phase4-M04 |
| AC097-04 | Every slide declares composition meaning and source role. | A slide exists only to fill the carousel count. | Phase4-M02 |
| AC097-05 | Every slide has at least three primitive refs and the sequence proves `PRM-BUS-003`, `PRM-BUS-012`, `PRM-VSG-018`, and `PRM-VSG-001`. | Carousel looks good but cannot prove why its structure, grid, or eye path serves the idea. | Phase4-M01 |
| AC097-06 | Ideogram-generated plates cannot be final text or final geometry. | Ideogram text is shipped directly with misspellings or wrong brand claim. | Phase1-M05 |
| AC097-07 | Layer-dependent slides require normalized Qwen/SAM3 layer and mask manifests before Geometrics. | Subject photo is covered by text because no mask/safe-zone existed. | Phase4-M04 |
| AC097-08 | Rough annotations are represented as typed cue manifests and can be replayed by final renderers. | Highlight exists only as a browser DOM animation and is missing from export. | Phase5-M01 |
| AC097-09 | Final still carousel output is rendered through `skia_still`. | Service emits MP4-style Remotion final URIs for a still PDF carousel. | Phase1-M05 |
| AC097-10 | `CarouselExportManifest` includes per-target outputs, hashes, dimensions, and delivery bundle refs. | LinkedIn PDF is delivered but has no manifest or hash evidence. | Phase5-M01 |
| AC097-11 | PWA and Telegram quick review consume the same evidence read model. | Telegram approval sees a different status than the PWA review workbench. | Phase3-M02 |
| AC097-12 | Workflow can resume from every long-running stage without duplicating provider costs. | Failed Qwen job forces the entire carousel, including Ideogram images, to rerun. | Phase3-M05 |
| AC097-13 | Every rejection includes slide index, object ref, provider ref when relevant, blocker code, and repair instruction. | Operator sees `failed quality check` with no actionable detail. | Phase4-M05 |
| AC097-14 | Export is blocked until operator approval receipt exists. | Carousel files are published after render but before review approval. | Phase5-M01 |
| AC097-15 | Generated TypeScript types match Python contracts for request, read model, export manifest, and receipt objects. | Frontend sends a field not accepted by the Python command handler. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Command Bus and receipt chain | `TS-CMF-001`, `TS-CMF-002`, `TS-CMF-050` |
| Provider capability registry and provider receipts | `TS-CMF-042`, `TS-CMF-044`, `src/ccp_studio/services/provider_operations_service.py` |
| Deterministic renderer contracts | `TS-CMF-043`, `src/ccp_studio/contracts/deterministic_rendering.py`, `src/ccp_studio/services/deterministic_rendering_service.py` |
| Operator UI and review state parity | `TS-CMF-007`, `TS-CMF-051`, `TS-CMF-055`, `TS-CMF-070` |
| Approval blockers and review commands | `TS-CMF-052`, `TS-CMF-053` |
| Ideogram composition bridge | `TS-CMF-088` |
| Qwen/SAM3 layer extraction and repair | `TS-CMF-089` |
| Renderer prop compiler and component harness | `TS-CMF-090` |
| Composition eval workbench | `TS-CMF-092` |
| Geometrics/Skia still runtime | `TS-CMF-095` |
| Carousel slide atom registry | `TS-CMF-096`, `registries/composition/carousel_slide_composition_library.v1.json` |
| Carousel composition atlas and router | `TS-CMF-098`, `registries/composition/carousel_composition_atlas.v1.json` |
| Composition primitive triad registry | `registries/evals/composition/cmf_composition_primitive_triads.v1.json` |
| Skia provider capability | New `skia_canvaskit.still_render.v1` provider capability |
| Object storage | Provider source assets, layer files, masks, render outputs, PDF exports, hashes, and delivery bundles |

## 10. Testing Strategy

### Unit Tests

- Validate `CreateCarouselRequest` rejects loose prompt-only input.
- Validate `TargetPlatformSpec` dimensions, export formats, caps, and safe margins.
- Validate registry loader rejects unknown slide atoms, duplicate atom codes, invalid positions, and missing primitive defaults.
- Validate every slide has a TS-CMF-098 `CompositionRouterDecision` before Geometrics.
- Validate provider routing decisions for pure typography, Ideogram composition, Qwen layered, SAM3 cleanup, and repair-required slides.
- Validate `DeterministicRenderer.skia_still` is accepted and Remotion/Motion Canvas are rejected for final still output.
- Validate primitive triad coverage for each slide and sequence-level primitives.
- Validate rough annotation cue manifests are hashable and renderer-agnostic.
- Validate `CarouselExportManifest` hash and target-platform output requirements.

### Integration Tests

- Run `CreateCarouselWorkflow` for a `CAR-LST` explanation carousel from locked brand context through export manifest.
- Run `CreateCarouselWorkflow` for a `CAR-JUX` juxtaposition carousel using at least one layer-dependent slide.
- Run a pure typography carousel path that skips Ideogram, Qwen, and SAM3 while still passing primitive and Skia gates.
- Run a layer-dependent slide path that uses Ideogram direction, Qwen decomposition, SAM3 mask cleanup, Geometrics, and Skia export.
- Verify PWA and Telegram review read models return the same slide evidence and blocker state.
- Verify workflow resume from failed Ideogram, failed Qwen, failed Skia, and failed operator approval states.

### Golden Fixtures

| Fixture | Purpose |
|---|---|
| `golden_car_lst_explanation` | Multi-slide educational/listicle carousel with primitive-backed sequence arc. |
| `golden_car_jux_contrast` | Juxtaposition carousel with contrast-bearing slide atoms and target platform exports. |
| `golden_car_lst_pattern_break` | Pattern-break carousel proving sequence variety and non-repetitive slide grammar. |

### Negative Fixtures

| Fixture | Expected Blocker |
|---|---|
| `negative_prompt_only_request` | `CAROUSEL_TYPED_CONTEXT_REQUIRED` |
| `negative_missing_brand_context` | `BRAND_CONTEXT_REQUIRED` |
| `negative_unknown_slide_atom` | `CAROUSEL_SLIDE_ATOM_UNKNOWN` |
| `negative_two_primitives_only` | `PRIMITIVE_TRIAD_REQUIRED` |
| `negative_baked_ideogram_text` | `BAKED_TEXT_NOT_FINAL_TRUTH` |
| `negative_missing_subject_mask` | `LAYER_MASK_REQUIRED` |
| `negative_skia_capability_missing` | `SKIA_STILL_RENDERER_UNAVAILABLE` |
| `negative_remotion_final_still` | `FINAL_STILL_RENDERER_MUST_BE_SKIA` |
| `negative_unapproved_export` | `OPERATOR_APPROVAL_REQUIRED` |

### Operational Tests

- Provider capability readiness check for Ideogram 4, Qwen-Image-Layered, SAM3, repair providers, and `skia_canvaskit.still_render.v1`.
- Object-store idempotency test proving expiring Ideogram URLs are persisted once and reused by hash.
- Cost and retry test proving provider jobs do not duplicate after workflow resume.
- Export parity test proving PNG slide set, stitched preview, and PDF document match the approved render manifest.
- Spec audit receipt test proving this spec references ERA3 protocol, existing backend owners, ADR-05 primitives, CBAR mandates, acceptance criteria, dependencies, and test fixtures.

### Spec Audit Receipt

| Field | Value |
|---|---|
| Spec ID | `TS-CMF-097` |
| Protocol | ERA3 10-section spec format |
| Existing backend mapped | Yes |
| Legacy inventory referenced | Yes, as read-only migration context |
| Primitive obligations declared | Yes |
| CBAR mandates declared | Yes |
| Acceptance criteria include failure examples | Yes |
| Tests include positive, negative, integration, and operational fixtures | Yes |
