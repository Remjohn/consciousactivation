---
tech_spec_id: "TS-CMF-098"
title: "Carousel Composition Atlas Registry and Router Integration"
story_id: "7.26"
story_title: "Carousel Composition Atlas Integration"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "CCP Carousel Composition Atlas V1 bundle integration"
pipeline_stage: "8 / 10 / 11 / 12"
entry_object: "CarouselSequencePlan, CarouselSpecSlideIntent, BrandContextVersion, TargetPlatformSpec, VoiceVisualDNA, AssetPackageSpec"
exit_object: "CarouselCompositionAtlasRecord, CompositionRouterDecision, CarouselSlideVisualGrammarPlan, CarouselAtlasIntegrationReceipt"
validation_contract: "atlas registry schema, slide atom to composition mapping, sequence grammar fit, tool routing policy, text budget, normalized zones, primitive triad preservation, corpus evidence, diversity constraints, Geometrics handoff"
required_receipt: "CarouselAtlasIntegrationReceipt"
runtime_target: "Python / Pydantic v2 / JSON registry loader / DSPy Composition Router / Skia / Qwen-Image-Layered / SAM3 / Ideogram 4 / Rough Annotation Manifest"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-098: Carousel Composition Atlas Registry and Router Integration

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory ERA3 10-section spec protocol, backend mapping, ADR-05 primitive, CBAR, acceptance, and testing requirements. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/CCP_CAROUSEL_COMPOSITION_ATLAS_V1.md` | Human-readable atlas defining the composition grammar registry, 44 composition specifications, 12 sequence grammars, router formula, evaluation gates, and tool doctrine. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/carousel_composition_registry_v1.json` | Machine-readable source registry containing 44 canonical compositions and 12 sequence grammars. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/carousel_composition_models.py` | Source Pydantic model sketch for composition families, layout zones, tool routing, annotation specs, render contracts, and sequence specs. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/carousel_corpus_mapping_v1.csv` | Evidence map from 118 inspected slides across 16 folders to canonical composition IDs; useful as eval fixture data, not as runtime truth. |
| `THE CMF STUDIO/registries/composition/carousel_composition_atlas.v1.json` | Canonical staged atlas registry path consumed by CMF after schema normalization and hash validation. |
| `THE CMF STUDIO/registries/composition/evidence/carousel_corpus_mapping.v1.csv` | Canonical staged evidence fixture path for corpus-derived atlas validation. |
| `THE CMF STUDIO/registries/composition/carousel_slide_composition_library.v1.json` | Existing CMF slide atom registry with 12 meaning-level atoms and 3 sequence blueprints. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Downstream Geometrics/Skia runtime that consumes zones, text budgets, masks, annotation cues, and provider artifacts. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Meaning-level slide atom and sequence plan layer that this atlas must extend, not replace. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` | Full carousel builder workflow that must call the composition atlas router before Geometrics handoff. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Composition primitive triad registry; atlas selection cannot dilute primitive obligations. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-003.yaml` | Narrative Structural Backbone; required for sequence grammar validation. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/design_business/PRM-BUS-012.yaml` | Grid as Cognitive Relief; required for visual continuity and layout consistency. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-018.yaml` | Sequence Over Single Image; required for diversity and rhythm across slides. |
| `THE CMF STUDIO/registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | Composition as Eye-Path Engineering; required for attention path and zone validation. |

## 2. Overview

The current carousel architecture has two strong layers:

- `TS-CMF-096`: slide atoms that define what each slide means;
- `TS-CMF-097`: the full carousel builder workflow from typed request to export.

The CCP Carousel Composition Atlas adds the missing third layer: concrete visual grammar. The atlas proves that a carousel should not be a folder of templates. It should be a composition grammar registry where each visual pattern has:

- a stable `composition_id`;
- a composition family;
- semantic roles;
- supported aspect ratios;
- recommended sequence positions;
- normalized layout zones;
- text budgets;
- attention path;
- micro-semiotic anchor slots;
- provider routing rules;
- rough annotation constraints;
- Skia responsibilities;
- avoid rules;
- corpus evidence.

This spec integrates the atlas as a canonical CMF registry and router. It does not replace the 12 slide atoms. Instead:

```text
CarouselSlideAtom = the slide's meaning job
CanonicalCarouselComposition = the slide's visual grammar
CompositionRouterDecision = why this composition fits this slide now
GeometricsLayoutPlan = exact coordinates, text measurements, masks, and render readiness
```

The atlas source bundle contains 44 canonical composition specs and 12 sequence grammars derived from 118 inspected slides across 16 folders. That is not redundant with the current CMF registry. The current registry is semantic; the atlas is visual-operational.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-098-001 | `carousel_composition_registry_v1.json` | Source artifact for migration into canonical CMF registry shape. |
| DEP-CMF-098-002 | `carousel_composition_models.py` | Source model sketch; adapt into CMF contracts with receipts, primitive refs, brand refs, and approval lineage. |
| DEP-CMF-098-003 | `carousel_corpus_mapping_v1.csv` | Evidence fixture proving where composition IDs came from; not used as runtime truth. |
| DEP-CMF-098-004 | `carousel_slide_composition_library.v1.json` | Meaning-level slide atoms remain authoritative for slide purpose and primitive obligations. |
| DEP-CMF-098-005 | `CarouselSequencePlan` | Input sequence plan from TS-CMF-096; each slide must receive one or more composition candidates. |
| DEP-CMF-098-006 | `CompositionRouterDecision` | Router output selecting one `composition_id`, alternatives, score breakdown, and blocker codes. |
| DEP-CMF-098-007 | `CarouselSlideVisualGrammarPlan` | Per-slide plan combining slide atom, composition spec, zones, text budgets, tool policy, and Geometrics hints. |
| DEP-CMF-098-008 | `TextAnnotationCueManifest` | Rough annotation output must follow atlas limits and semantic reasons. |
| DEP-CMF-098-009 | `GeometricsLayoutPlan` | Downstream handoff consumes atlas zones and transforms normalized intent into exact render coordinates. |
| DEP-CMF-098-010 | `CarouselAtlasIntegrationReceipt` | Immutable receipt proving atlas version, mapping, routing scores, evidence, and validation state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/carousel_composition_atlas.py` | New adapted Pydantic contracts for composition families, zones, budgets, routing policy, score breakdowns, decisions, visual grammar plans, and receipts. |
| `src/ccp_studio/services/carousel_composition_atlas_service.py` | New registry loader/query service for the canonical atlas JSON, schema validation, hash verification, and evidence lookups. |
| `src/ccp_studio/services/composition_router_service.py` | New service that retrieves 3-5 candidates and scores them against semantic role, copy budget, assets, sequence position, brand style, micro-semiotic anchors, aspect ratio, and diversity. |
| `src/ccp_studio/services/carousel_builder_service.py` | Must call the composition router after `CarouselSequencePlan` and before Geometrics materialization. |
| `src/ccp_studio/contracts/carousel_builder.py` | Extend `CarouselSpecSlideIntent` or downstream slide plan with `composition_id`, `composition_family`, `visual_mode`, `composition_score`, and `composition_router_decision_id`. |
| `src/ccp_studio/contracts/composition.py` | Add or import normalized composition zones and attention paths for Geometrics handoff. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Validate that selected compositions preserve primitive triads rather than only matching visual style. |
| `src/ccp_studio/services/review_workbench_service.py` | Expose chosen composition ID, alternatives, score breakdown, and avoid-rule checks to the operator. |
| `THE CMF STUDIO/registries/composition/carousel_composition_atlas.v1.json` | Canonical staged atlas registry; runtime must normalize and validate schema metadata before loading as production truth. |
| `THE CMF STUDIO/registries/composition/evidence/carousel_corpus_mapping.v1.csv` | Canonical migrated evidence fixture path for the corpus mapping. |

### Migration Boundary

The bundle is inside `THE CMF STUDIO`, but it is still a source bundle. Integration must be a controlled migration:

```text
CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE
-> staged canonical registry copy
-> schema audit
-> canonical registry normalization
-> CMF contract adaptation
-> loader/query service
-> router scoring service
-> builder workflow binding
-> Geometrics handoff
-> eval fixtures and review evidence
```

Do not copy the source Pydantic file directly into production contracts. It lacks CMF-specific receipts, primitive eval refs, brand workspace refs, operator approval linkage, Command Bus metadata, and failure-blocker semantics. The staged JSON registry is allowed as a migration input, but the loader must reject it as production truth until `schema_version`, `registry_id`, `registry_hash`, required hard-failure codes, and CMF receipt linkage are validated.

### ADR-05 Primitives

The atlas cannot replace primitive validation. It provides visual grammar, but every selected composition must preserve slide and sequence primitive obligations.

| Requirement | Primitive |
|---|---|
| Slide must have one clear job and attention path | `PRM-VSG-001` Composition as Eye-Path Engineering |
| Sequence must vary deliberately rather than reuse a generic look | `PRM-VSG-018` Sequence Over Single Image |
| Grid and zones must reduce cognitive burden | `PRM-BUS-012` The Grid as Cognitive Relief |
| Sequence grammar must support the argument arc | `PRM-BUS-003` Narrative Structural Backbone |

Each `CompositionRouterDecision` must carry:

- selected `composition_id`;
- source `slide_atom_code`;
- exact primitive refs preserved;
- attention path;
- score breakdown;
- avoid rules checked;
- blocker codes when the composition cannot safely express the slide atom.

### CBAR Mandate Enforcement

| Mandate | Governing Story | Enforcement |
|---|---|---|
| Phase1-M05: The Deterministic Override Rule | Story 2.2 | Atlas zones and text budgets are deterministic inputs to Geometrics/Skia; generative providers can propose assets but cannot own final geometry. |
| Phase3-M02: Per-Slide Feedback Rule | Story 1.2 | Review UI must show per-slide selected composition, alternatives, routing scores, failed avoid rules, and repair actions. |
| Phase3-M05: Modular CMF Recovery Rule | Story 3.2 | Router decisions are persisted independently so provider/render failures do not force sequence replanning. |
| Phase4-M01: The Intelligence-Gated Intercept Rule | Story 1.1 | Router blocks without slide atom, source refs, brand context, target aspect ratio, text budget, and primitive triad evidence. |
| Phase4-M02: The Cinematic Meaning Rule | Story 2.1 | Composition choice must prove semantic role fit, not aesthetic preference alone. |
| Phase4-M04: The Frictionless Block Rule | Story 4.1 | Unknown composition ID, invalid zone, copy overflow, unsupported aspect ratio, and repeated adjacent composition stop before provider calls. |
| Phase4-M05: The Actionable Rejection Rule | Story 5.1 | Blockers include slide index, slide atom, composition candidates, failed score dimension, and repair hint. |
| Phase5-M01: The Verifiable Artifact Rule | Story 1.1 | Atlas registry version, registry hash, selected IDs, score breakdowns, and evidence fixture refs are stored in receipts. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Create a dedicated atlas registry instead of merging it into slide atoms. | Slide atoms express meaning; atlas specs express visual grammar. Merging them would flatten the architecture. |
| Canonical destination is `registries/composition/carousel_composition_atlas.v1.json`. | The source bundle remains readable, while runtime consumes a normalized registry path. |
| The router retrieves multiple candidates before choosing. | The atlas requires 3-5 candidates and score comparison, preventing prompt intuition from choosing layout. |
| Composition selection happens after sequence planning and before Geometrics. | The system must know slide role first, then choose visual grammar, then solve exact coordinates. |
| Atlas text budgets are hard preflight constraints. | Copy overflow should be blocked before expensive generation or render. |
| Corpus mapping is eval evidence, not truth. | It proves source lineage for the grammar, but runtime should route from current source context and brand needs. |
| Tool routing policy is advisory but enforceable. | It tells the builder when to call Ideogram, Qwen, SAM3, rough annotation, and Skia, while provider availability still comes from the provider registry. |

## 4. Implementation Plan

1. Validate staged canonical registry destination `THE CMF STUDIO/registries/composition/carousel_composition_atlas.v1.json`.
2. Normalize `carousel_composition_registry_v1.json` or the staged registry into CMF naming and schema:
   - `schema_version`;
   - `registry_id`;
   - `registry_hash`;
   - `canonical_compositions`;
   - `sequence_grammars`;
   - `global_rules`;
   - `source_corpus`;
   - `hard_failure_codes`.
3. Validate evidence path `THE CMF STUDIO/registries/composition/evidence/carousel_corpus_mapping.v1.csv`.
4. Add `contracts/carousel_composition_atlas.py` using Section 5 contracts and adapting, not blindly copying, the source model file.
5. Add `CarouselCompositionAtlasService`:
   - load registry;
   - validate normalized zone rectangles;
   - validate text budgets;
   - validate provider routing policy;
   - query by semantic role, family, position, aspect ratio, visual mode, text budget, micro-semiotic slot, and provider need;
   - emit registry hash.
6. Add `CompositionRouterService`:
   - accept `CompositionRoutingInput`;
   - retrieve 3-5 candidates;
   - compute score breakdown;
   - apply repetition and generation-cost penalties;
   - return `CompositionRouterDecision`.
7. Add `CarouselSlideVisualGrammarPlan` as the handoff object between `CarouselSequencePlan` and `GeometricsLayoutPlan`.
8. Update `CarouselBuilderService` so the builder flow becomes:

```text
CarouselSequencePlan
-> CompositionRouterDecision[]
-> CarouselSlideVisualGrammarPlan[]
-> GeometricsLayoutPlan[]
-> SkiaRenderJob[]
```

9. Update review read model to show:
   - selected `composition_id`;
   - composition family;
   - attention path;
   - zones;
   - score breakdown;
   - rejected alternatives;
   - avoid-rule checks;
   - operator repair actions.
10. Add tests and fixtures for registry validation, routing score, failure blockers, and Geometrics handoff.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class CarouselCompositionFamily(str, Enum):
    HOOK_COVER = "hook_cover"
    NARRATIVE_EMOTION = "narrative_emotion"
    FRAMEWORK_EDUCATION = "framework_education"
    COMPARISON_JUXTAPOSITION = "comparison_juxtaposition"
    IDENTITY_BRAND = "identity_brand"
    CTA_CLOSING = "cta_closing"


class NormalizedLayoutZone(BaseModel):
    schema_version: Literal["cmf.normalized_layout_zone.v1"]
    zone_id: str
    kind: str
    rect: tuple[float, float, float, float]
    required: bool = True
    align: str | None = None

    @field_validator("rect")
    @classmethod
    def rect_inside_canvas(cls, value: tuple[float, float, float, float]):
        x, y, width, height = value
        if min(value) < 0 or width <= 0 or height <= 0:
            raise ValueError("Rectangle values must be non-negative and dimensions positive")
        if x + width > 1.0001 or y + height > 1.0001:
            raise ValueError("Rectangle exceeds normalized canvas")
        return value


class TextBudgetRange(BaseModel):
    schema_version: Literal["cmf.text_budget_range.v1"]
    headline_words: tuple[int, int]
    headline_lines: tuple[int, int]
    body_words: tuple[int, int]
    bullets: tuple[int, int] | None = None


class AtlasToolRoutingPolicy(BaseModel):
    schema_version: Literal["cmf.atlas_tool_routing_policy.v1"]
    ideogram_4: dict
    qwen_image_layered: dict
    sam3: dict
    rough_notation: dict
    skia: list[str]


class CanonicalCarouselComposition(BaseModel):
    schema_version: Literal["cmf.canonical_carousel_composition.v1"]
    composition_id: str
    name: str
    family: CarouselCompositionFamily
    summary: str
    semantic_roles: list[str]
    recommended_slide_positions: list[int]
    supported_aspect_ratios: list[Literal["1:1", "4:5", "3:4"]]
    attention_path: str
    zones: list[NormalizedLayoutZone]
    text_budget: TextBudgetRange
    visual_mode: str
    tool_routing: AtlasToolRoutingPolicy
    micro_semiotic_anchor_slots: list[str]
    source_references: list[str]
    avoid: list[str]


class CarouselSequenceGrammar(BaseModel):
    schema_version: Literal["cmf.carousel_sequence_grammar.v1"]
    sequence_id: str
    name: str
    recommended_length: tuple[int, int]
    beats: list[str]
    source: str
    compatible_format_codes: list[Literal["CAR-LST", "CAR-JUX"]] = Field(default_factory=list)


class CarouselCompositionAtlasRegistry(BaseModel):
    schema_version: Literal["cmf.carousel_composition_atlas_registry.v1"]
    registry_id: str
    version: str
    registry_hash: str
    source_bundle_ref: str
    corpus: dict
    canonical_compositions: list[CanonicalCarouselComposition]
    sequence_grammars: list[CarouselSequenceGrammar]
    hard_failure_codes: list[str]


class CompositionRoutingInput(BaseModel):
    schema_version: Literal["cmf.composition_routing_input.v1"]
    request_id: UUID
    carousel_spec_id: UUID
    sequence_plan_id: UUID
    slide_index: int
    slide_atom_code: str
    semantic_role: str
    composition_meaning: str
    format_code: Literal["CAR-LST", "CAR-JUX"]
    target_aspect_ratio: Literal["1:1", "4:5", "3:4"]
    copy_word_count: int
    required_primitive_refs: list[str] = Field(min_length=3)
    brand_context_version_id: UUID
    asset_refs: list[str]
    voice_visual_dna_ref: str | None = None
    previous_composition_ids: list[str] = Field(default_factory=list)


class CompositionScoreBreakdown(BaseModel):
    schema_version: Literal["cmf.composition_score_breakdown.v1"]
    semantic_role_fit: float = Field(ge=0, le=1)
    copy_budget_fit: float = Field(ge=0, le=1)
    asset_availability_fit: float = Field(ge=0, le=1)
    sequence_position_fit: float = Field(ge=0, le=1)
    brand_style_fit: float = Field(ge=0, le=1)
    micro_semiotic_anchor_fit: float = Field(ge=0, le=1)
    aspect_ratio_fit: float = Field(ge=0, le=1)
    sequence_diversity_gain: float = Field(ge=0, le=1)
    repetition_penalty: float = Field(ge=0, le=1)
    generation_cost_penalty: float = Field(ge=0, le=1)
    weighted_score: float = Field(ge=0, le=1)


class CompositionRouterDecision(BaseModel):
    schema_version: Literal["cmf.composition_router_decision.v1"]
    decision_id: UUID
    routing_input_id: UUID
    selected_composition_id: str
    selected_family: CarouselCompositionFamily
    candidate_composition_ids: list[str] = Field(min_length=1)
    rejected_candidate_reasons: dict[str, list[str]]
    score_breakdown: CompositionScoreBreakdown
    required_tool_policy: AtlasToolRoutingPolicy
    primitive_refs_preserved: list[str] = Field(min_length=3)
    avoid_rules_checked: list[str]
    approved_for_geometrics: bool
    blocker_codes: list[str] = Field(default_factory=list)


class CarouselSlideVisualGrammarPlan(BaseModel):
    schema_version: Literal["cmf.carousel_slide_visual_grammar_plan.v1"]
    visual_grammar_plan_id: UUID
    carousel_spec_id: UUID
    slide_index: int
    slide_atom_code: str
    composition_id: str
    composition_family: CarouselCompositionFamily
    visual_mode: str
    attention_path: str
    normalized_zones: list[NormalizedLayoutZone]
    text_budget: TextBudgetRange
    annotation_policy: dict
    provider_routing_policy: AtlasToolRoutingPolicy
    micro_semiotic_anchor_slots: list[str]
    geometrics_ready: bool
    blocker_codes: list[str] = Field(default_factory=list)


class CarouselAtlasIntegrationReceipt(BaseModel):
    schema_version: Literal["cmf.carousel_atlas_integration_receipt.v1"]
    receipt_id: UUID
    registry_id: str
    registry_version: str
    registry_hash: str
    carousel_spec_id: UUID
    sequence_plan_id: UUID
    router_decision_ids: list[UUID]
    selected_composition_ids: list[str]
    evidence_fixture_refs: list[str]
    approved_for_geometrics: bool
    blocker_codes: list[str] = Field(default_factory=list)
```

### Router Score Formula

The routing score must implement the atlas formula:

```text
composition_score =
  0.24 * semantic_role_fit
+ 0.18 * copy_budget_fit
+ 0.16 * asset_availability_fit
+ 0.12 * sequence_position_fit
+ 0.10 * brand_style_fit
+ 0.08 * micro_semiotic_anchor_fit
+ 0.07 * aspect_ratio_fit
+ 0.05 * sequence_diversity_gain
- repetition_penalty
- generation_cost_penalty
```

The router must block adjacent reuse of the same `composition_id` unless the sequence grammar explicitly allows a fixed shell, such as the recurring cinematic scene shell represented in the atlas.

Minimum selected score is `0.72`. If fewer than three candidates survive hard constraints, the router may proceed only when the selected candidate score is at least `0.84` and the receipt records `candidate_pool_below_preferred_size=true`; otherwise it blocks with `CAROUSEL_COMPOSITION_CANDIDATE_POOL_TOO_SMALL`.

## 6. Backward Compatibility Fallback

| Condition | Required Fallback |
|---|---|
| Existing carousel slide has a slide atom but no `composition_id` | Route through atlas before Geometrics; block with `CAROUSEL_COMPOSITION_ID_REQUIRED` if no candidate fits. |
| Existing carousel sequence uses only TS-CMF-096 blueprints | Keep blueprint, but resolve each atom into an atlas composition before render. |
| Atlas composition supports only aspect ratios not requested by target | Block with `CAROUSEL_COMPOSITION_ASPECT_RATIO_UNSUPPORTED`. |
| Copy exceeds selected composition text budget | Block with `CAROUSEL_COMPOSITION_COPY_OVERFLOW`; request copy compression before provider calls. |
| Selected composition repeats adjacent slide without sequence reason | Block with `CAROUSEL_COMPOSITION_REPETITION_BLOCKED`. |
| Composition requires SAM3 or Qwen but provider capability is unavailable | Return alternative candidate that does not require that tool, or block with provider-specific unavailable code. |
| Atlas source registry is malformed or hash mismatch occurs | Block with `CAROUSEL_ATLAS_REGISTRY_INVALID`. |
| Corpus evidence CSV is missing | Do not block runtime; mark evidence fixture unavailable in receipt and block only eval fixture runs that require it. |
| Existing Geometrics path receives normalized zones but no visual grammar plan | Block with `CAROUSEL_VISUAL_GRAMMAR_PLAN_MISSING`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T098-01 | Validate staged canonical registry file `registries/composition/carousel_composition_atlas.v1.json` and normalize it into the CMF production registry schema before runtime loading. |
| T098-02 | Validate evidence fixture `registries/composition/evidence/carousel_corpus_mapping.v1.csv`. |
| T098-03 | Add `contracts/carousel_composition_atlas.py` with Section 5 contracts. |
| T098-04 | Add registry loader validation for composition IDs, families, aspect ratios, zones, text budgets, routing policies, source refs, and avoid rules. |
| T098-05 | Add `CarouselCompositionAtlasService.query_candidates()` by semantic role, family, slide position, aspect ratio, copy budget, visual mode, and provider needs. |
| T098-06 | Add `CompositionRouterService.score_candidates()` implementing the atlas formula exactly. |
| T098-07 | Add repetition and generation-cost penalties, plus fixed-shell exception support. |
| T098-08 | Extend carousel builder contracts with `composition_id`, `composition_family`, `visual_mode`, and router decision refs. |
| T098-09 | Bind `CompositionRouterDecision` into `CarouselBuilderService` between sequence planning and Geometrics. |
| T098-10 | Add review read model fields for selected composition, alternatives, score breakdown, avoid rules, and repair actions. |
| T098-11 | Add Geometrics handoff tests proving normalized atlas zones become exact layout constraints. |
| T098-12 | Add eval fixtures from the 118-slide corpus mapping. |
| T098-13 | Add negative fixtures for unknown ID, invalid zone, copy overflow, unsupported aspect ratio, repeated composition, and missing visual grammar plan. |
| T098-14 | Update `TS-CMF-097` and tech-spec README to declare the atlas layer as a required carousel builder dependency. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR Reference |
|---|---|---|---|
| AC098-01 | The atlas is integrated as a dedicated visual grammar registry, not merged into slide atoms. | `CAR-SL-001-HOOK-PREMISE` directly contains all 44 visual layouts. | Phase4-M02 |
| AC098-02 | Every carousel slide that reaches Geometrics has both `slide_atom_code` and `composition_id`. | Slide has meaning but no visual grammar and still renders. | Phase4-M04 |
| AC098-03 | The router retrieves and scores 3-5 candidates before selecting a composition. | First matching layout is selected without score evidence. | Phase4-M01 |
| AC098-04 | The router implements the atlas weighted score dimensions and penalties. | Layout selection ignores copy budget or sequence diversity. | Phase5-M01 |
| AC098-04A | The router blocks candidates below score threshold or below minimum candidate-pool requirements. | A single weak candidate is accepted because no alternative was available. | Phase4-M04 |
| AC098-05 | Normalized zones are validated before Geometrics handoff. | A zone rect exceeds canvas bounds and creates broken coordinates. | Phase1-M05 |
| AC098-06 | Text budgets block overflow before Ideogram, Qwen, SAM3, or Skia work. | A 40-word headline enters a 3-9 word cover composition. | Phase4-M04 |
| AC098-07 | Provider routing policy from the selected composition is checked against provider capability registry. | A Qwen-dependent layout proceeds when Qwen is unavailable. | Phase4-M04 |
| AC098-08 | Composition selection preserves exact primitive refs from the slide atom and sequence plan. | A layout looks strong but drops primitive triad evidence. | Phase4-M01 |
| AC098-09 | Adjacent composition repetition is blocked unless the selected sequence grammar explicitly allows fixed-shell repetition. | Five unrelated slides all use the same composition ID. | Phase4-M02 |
| AC098-10 | Operator review shows selected composition, alternatives, score breakdown, avoid-rule checks, and repair actions. | Operator sees only a rendered preview with no routing evidence. | Phase3-M02 |
| AC098-11 | Corpus mapping is used as evidence/eval fixture data, not as production routing truth. | Runtime picks a layout because a historical file name used it. | Phase5-M01 |
| AC098-12 | `CarouselAtlasIntegrationReceipt` stores registry version, hash, selected IDs, decision refs, and blocker state. | A rendered carousel cannot prove which atlas version selected its layouts. | Phase5-M01 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Carousel builder workflow | `TS-CMF-097` |
| Carousel slide atom registry | `TS-CMF-096`, `registries/composition/carousel_slide_composition_library.v1.json` |
| Geometrics and Skia still runtime | `TS-CMF-095` |
| Provider registry and job receipts | `TS-CMF-042`, `TS-CMF-044` |
| Evaluation and operator approval workbench | `TS-CMF-092` |
| Primitive triad registry | `registries/evals/composition/cmf_composition_primitive_triads.v1.json` |
| Source atlas bundle | `CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE` |
| Canonical atlas registry | `registries/composition/carousel_composition_atlas.v1.json` |
| Composition router service | New `src/ccp_studio/services/composition_router_service.py` |
| Atlas loader service | New `src/ccp_studio/services/carousel_composition_atlas_service.py` |

## 10. Testing Strategy

### Unit Tests

- Validate every atlas composition has a unique `composition_id`.
- Validate every normalized zone is inside the canvas.
- Validate text budget ranges are ordered and non-negative.
- Validate every composition declares at least one semantic role and one supported aspect ratio.
- Validate every composition has provider routing policy for Ideogram 4, Qwen-Image-Layered, SAM3, rough annotation, and Skia.
- Validate sequence grammars have recommended length and beat chain.
- Validate registry hash is stable.
- Validate score formula output for a known candidate set.

### Integration Tests

- Route a `CAR-SL-001-HOOK-PREMISE` slide into 3-5 hook cover candidates and select a valid `H*` composition.
- Route a `CAR-SL-007-JUXTAPOSITION` slide into comparison candidates and reject non-comparison candidates when semantic fit is too low.
- Route a `CAR-SL-012-APPLICATION-CTA` slide into CTA candidates and enforce last-slide position.
- Pass a selected composition's normalized zones into Geometrics and verify exact layout constraints are produced.
- Verify carousel builder persists router decisions and can resume after provider/render failure without rerouting.
- Verify PWA/Telegram review read model exposes the same composition decision evidence.

### Golden Fixtures

| Fixture | Purpose |
|---|---|
| `golden_atlas_hook_cover_routing` | Selects from H01-H08 for a first-slide hook. |
| `golden_atlas_framework_routing` | Selects from F01-F10 for an educational mechanism slide. |
| `golden_atlas_juxtaposition_routing` | Selects from J01-J06 for contrast slides. |
| `golden_atlas_cta_routing` | Selects from C01-C06 for a final action slide. |
| `golden_atlas_fixed_shell_sequence` | Allows repeated N05 only when sequence grammar declares fixed-shell continuity. |

### Negative Fixtures

| Fixture | Expected Blocker |
|---|---|
| `negative_unknown_composition_id` | `CAROUSEL_COMPOSITION_ID_UNKNOWN` |
| `negative_invalid_zone_rect` | `CAROUSEL_COMPOSITION_ZONE_INVALID` |
| `negative_copy_budget_overflow` | `CAROUSEL_COMPOSITION_COPY_OVERFLOW` |
| `negative_aspect_ratio_unsupported` | `CAROUSEL_COMPOSITION_ASPECT_RATIO_UNSUPPORTED` |
| `negative_adjacent_repetition` | `CAROUSEL_COMPOSITION_REPETITION_BLOCKED` |
| `negative_missing_visual_grammar_plan` | `CAROUSEL_VISUAL_GRAMMAR_PLAN_MISSING` |
| `negative_provider_policy_unavailable` | Provider-specific unavailable blocker |

### Spec Audit Receipt

| Field | Value |
|---|---|
| Spec ID | `TS-CMF-098` |
| Protocol | ERA3 10-section spec format |
| Existing backend mapped | Yes |
| Legacy/source bundle referenced | Yes |
| Primitive obligations declared | Yes |
| CBAR mandates declared | Yes |
| Acceptance criteria include failure examples | Yes |
| Tests include unit, integration, golden, and negative fixtures | Yes |
