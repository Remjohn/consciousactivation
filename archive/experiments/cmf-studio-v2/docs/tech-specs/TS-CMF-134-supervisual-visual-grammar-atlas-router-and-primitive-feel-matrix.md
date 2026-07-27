---
tech_spec_id: "TS-CMF-134"
title: "SuperVisual Visual Grammar Atlas, Router, and Primitive Feel Matrix"
story_id: "14.2"
story_title: "SuperVisual Grammar Router and Primitive Feel Matrix"
epic_id: 14
epic_title: "Still Visual Composition Architecture"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-14.04"
  - "FR-CMF-14.05"
  - "FR-CMF-14.06"
pipeline_stage: "supervisual composition routing and visual grammar"
entry_object: "SuperVisualGrammarRouteRequest"
exit_object: "SuperVisualGrammarRouterDecision"
validation_contract: "SuperVisual subtype, grammar atlas, primitive triad, feel matrix, micro-semiotic anchors, provider boundaries, deterministic Skia scene obligations"
required_receipt: "SuperVisualGrammarRouterDecision"
runtime_target: "Python / Pydantic v2 / registry loader / composition router / primitive evals / Geometrics / Skia"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-134: SuperVisual Visual Grammar Atlas, Router, and Primitive Feel Matrix

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory tech spec protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | CBAR rules for meaning, route, blockers, and rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact and earned escalation requirements. |
| `THE CMF STUDIO/docs/audits/CMF_STILL_VISUAL_COMPOSITION_ARCHITECTURE_AUDIT_2026-06-25.md` | Audit finding that SuperVisuals need distinct visual grammar and cannot be treated as generic single-image posts. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Parent single-image runtime and SuperVisual router spec. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md` | Registry loader and schema parity dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-101-single-image-router-format-family-and-archetype-selection.md` | Router dependency for output family and archetype selection. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | Existing SuperVisual primitive triad contract. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md` | Provider materialization dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | Deterministic Skia scene compiler dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md` | Eval, review, and golden fixture dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md` | Parent still visual stage manifest. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_05_Brand_Context_and_Brand_Genesis.md` | Brand substrate, prop library, micro-semiotic anchor, and composition preference requirements. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_08_Evals_and_Primitives.md` | Primitive quality standard and eval registry requirement. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis and micro-semiotic requirements for visual meaning. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE` | Legacy single-image post and SuperVisual composition contracts. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Mandatory primitive role coverage and failure codes. |
| `THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json` | Existing router policy and scoring weights. |
| `THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json` | Provider responsibility boundaries. |
| `THE CMF STUDIO/src/ccp_studio/services/registry_service.py` | Registry loader service to extend. |
| `THE CMF STUDIO/src/ccp_studio/services/composition_service.py` | Router and composition service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/doctrine_evaluation_service.py` | Doctrine evaluation owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Evaluation receipt owner. |

## 2. Overview

SuperVisuals are not merely higher-effort single images. They are compressed visual arguments: a premise, contradiction, symbolic object, authority frame, or recognition moment made inspectable in one image. A conceptual contrast SuperVisual must make the conflict visible. A symbolic SuperVisual must make an abstract idea feel embodied. A premise/authority SuperVisual must make the claim feel earned by the guest's identity, domain, and evidence. These three families cannot share the same generic "black background, big text, cutout person" pattern without violating CMF's doctrines and primitive standards.

This spec creates a SuperVisual visual grammar atlas and primitive feel matrix. The atlas describes eligible composition grammars, layer stacks, object roles, text budgets, negative-space rules, micro-semiotic anchor rules, provider responsibilities, and Skia scene obligations. The feel matrix ensures that each SuperVisual subtype carries its own emotional and rhetorical texture. The router scores candidates from the atlas using source evidence, Brand Context, archetype route, primitives, platform target, and operator intent. The selected grammar becomes a binding contract inside `StillVisualCompositionProgram`.

The key correction is simple: SuperVisuals must be routable by meaning, not style mood. If the guest's source material is a contradiction, route toward `SPV-CON`. If it is an embodied metaphor or transformation symbol, route toward `SPV-SYM`. If it is a strong teaching premise, framework, or authority statement, route toward `SPV-PRM`. Each route then carries primitive obligations and visual grammar obligations that can be evaluated before the image is approved.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-134-001 | `supervisual_visual_grammar_atlas.v1.json` | Registry of SuperVisual composition grammars, layer obligations, meaning roles, and Skia component requirements. |
| DEP-CMF-134-002 | `supervisual_feel_matrix.v1.json` | Registry mapping each subtype to emotional texture, visual density, color posture, negative space, typography posture, and primitive emphasis. |
| DEP-CMF-134-003 | `SuperVisualGrammarRouteRequest` | Request from TS-CMF-133 or single-image router containing source evidence, Brand Context, archetype, platform, and target subtype hints. |
| DEP-CMF-134-004 | `SuperVisualGrammarRouterDecision` | Scored decision selecting one grammar, rejecting unsafe candidates, and recording primitive role coverage. |
| DEP-CMF-134-005 | `SuperVisualPrimitiveRoleCoverageReceipt` | Receipt proving meaning, delivery, and format/material primitive roles are covered. |
| DEP-CMF-134-006 | `SuperVisualVisualGrammarRecord` | Canonical grammar record used to compile Geometrics/Skia layout plans. |
| DEP-CMF-134-007 | `SuperVisualFailureCode` | Typed blocker codes for generic flattening, missing contrast, missing symbol, missing authority evidence, missing Brand Context, unsafe micro-semiotics, and non-deterministic final layout. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/supervisual_grammar.py` | New contract owner for grammar records, feel matrix, route request, router decision, and coverage receipts. |
| `src/ccp_studio/services/registry_service.py` | Load, validate, and version SuperVisual atlas and feel matrix registries. |
| `src/ccp_studio/services/composition_service.py` | Add `route_supervisual_grammar` and bind selected grammar to still visual program. |
| `src/ccp_studio/services/doctrine_evaluation_service.py` | Evaluate doctrine compatibility for symbolic, authority, contradiction, and source-truth claims. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Emit grammar route receipts and primitive coverage receipts. |
| `src/ccp_studio/services/approval_gate_service.py` | Block approval when selected SuperVisual grammar fails primitive or visual-feel obligations. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Enforce that selected grammar compiles into deterministic Skia scene obligations. |

### New Registry Files

Create:

```text
THE CMF STUDIO/registries/composition/supervisual_visual_grammar_atlas.v1.json
THE CMF STUDIO/registries/composition/supervisual_feel_matrix.v1.json
```

These registries must be versioned and loaded through existing registry infrastructure. They must not live in the legacy reference folder once promoted.

### ADR-05 Primitive Implementation

The SuperVisual router must evaluate primitives at two levels:

1. **Subtype-level primitive obligations**: each subtype declares required primitive roles and preferred primitive candidates.
2. **Candidate-level primitive proof**: each candidate grammar must show evidence that the actual source material satisfies the declared primitive roles.

Required role coverage:

| Primitive Role | SuperVisual Meaning |
|---|---|
| `meaning_transform` | The image changes how the audience sees the premise, contradiction, or symbol. |
| `delivery_shape` | The visual hierarchy, caption, object arrangement, and guest pose make the idea legible quickly. |
| `format_material` | The material treatment fits the output family: premium single-frame, symbolic poster, contrast card, or authority visual. |

### CBAR Mandate Enforcement

| CBAR Mandate | SuperVisual Requirement |
|---|---|
| Intelligence-Gated Intercept Rule | No SuperVisual grammar route may run without source evidence and Brand Context. |
| Cinematic Meaning Rule | Each grammar must declare the transformation, contradiction, symbol, or authority function. |
| Inline Routing SLA | The router must return top candidates, blockers, and selected grammar before provider materialization. |
| Frictionless Block Rule | Rejection must name what is missing: contrast, symbol, authority evidence, primitive role, or deterministic layout. |
| Actionable Rejection Rule | Every blocker must include a repair command, such as request stronger quote, choose alternate grammar, reduce text, add symbol evidence, or reroute subtype. |
| Verifiable Artifact Rule | Final approval requires grammar route receipt, primitive coverage receipt, provider job receipts, render hash, and review decision. |

### Technical Decisions

1. SuperVisual visual grammar is registry-driven, not hard-coded inside prompts.
2. `SPV-CON`, `SPV-SYM`, and `SPV-PRM` are first-class subtypes with separate feel matrices.
3. Ideogram 4 may propose composition plates, but final layout authority belongs to the selected grammar and Skia scene.
4. The router must prefer source-truth and primitive fit over raw visual excitement.
5. Generic premium-social sameness is a hard failure, not a minor style note.
6. Micro-semiotic anchors are required when Brand Genesis declares them available for the guest.

## 4. Implementation Plan

### Step 1 - Build Grammar Atlas Registry

Create `supervisual_visual_grammar_atlas.v1.json` with at least these records:

| Grammar Code | Subtype | Composition Meaning |
|---|---|---|
| `SPV-CON-DUAL-FRAME-001` | `SPV-CON` | Two opposing visual states with visible tension and a decisive thesis line. |
| `SPV-CON-EVIDENCE-TILT-001` | `SPV-CON` | A public claim or social object tilted against guest reaction or counterframe. |
| `SPV-SYM-METAPHOR-OBJECT-001` | `SPV-SYM` | One central metaphor object carries the emotional argument. |
| `SPV-SYM-THRESHOLD-001` | `SPV-SYM` | Character or guest stands at a threshold, river, door, bridge, archive, or symbolic boundary. |
| `SPV-PRM-AUTHORITY-POSTER-001` | `SPV-PRM` | Guest claim, proof cue, and domain object create authority without visual clutter. |
| `SPV-PRM-FRAMEWORK-CARD-001` | `SPV-PRM` | Clear premise, mini framework, and guest anchor create a teachable single image. |

Each record must include:

```json
{
  "grammar_code": "SPV-CON-DUAL-FRAME-001",
  "subtype": "SPV-CON",
  "meaning_function": "make contradiction inspectable",
  "eligible_archetype_routes": [],
  "required_source_refs": ["quote_or_claim", "counterframe"],
  "layer_stack": [],
  "text_budget": {},
  "negative_space_rule": {},
  "micro_semiotic_anchor_policy": {},
  "provider_policy_refs": [],
  "skia_component_refs": [],
  "primitive_role_requirements": [],
  "hard_failure_codes": []
}
```

### Step 2 - Build Feel Matrix Registry

Create `supervisual_feel_matrix.v1.json` with subtype-specific targets:

| Subtype | Required Feel | Must Avoid |
|---|---|---|
| `SPV-CON` | Tension, contrast, decision pressure, visible stakes | Decorative symmetry, vague inspirational poster, identical sides |
| `SPV-SYM` | Embodiment, metaphor, memory, transformation, symbolic depth | Random surrealism, unexplained objects, generic mysticism |
| `SPV-PRM` | Authority, clarity, proof, premise discipline, calm force | Overloaded infographics, empty guru poster, unsupported certainty |

### Step 3 - Add Router

Implement `SuperVisualGrammarAtlasService.route(request)`:

1. Validate source evidence and Brand Context.
2. Determine or confirm subtype.
3. Load eligible grammar records.
4. Score candidates using source fit, primitive fit, Brand Context fit, platform fit, text fit, micro-semiotic fit, provider feasibility, and deterministic render readiness.
5. Reject candidates that trigger hard failures.
6. Return selected grammar and alternates.

### Step 4 - Bind To Still Visual Program

When TS-CMF-133 requests a SuperVisual route, attach:

1. Selected grammar record ref.
2. Feel matrix ref.
3. Primitive coverage receipt ref.
4. Provider materialization constraints.
5. Geometrics/Skia scene obligations.
6. Review blockers and repair commands.

### Step 5 - Add Evaluation

Create eval fixtures that deliberately fail:

1. Conceptual contrast where the two sides do not actually contrast.
2. Symbolic visual with beautiful but unsupported objects.
3. Authority visual with unsupported claim.
4. SuperVisual with fewer than three primitive roles.
5. SuperVisual whose final Skia scene does not match selected grammar.

## 5. Primary Output Schema

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

SuperVisualSubtype = Literal["SPV-CON", "SPV-SYM", "SPV-PRM"]

class SuperVisualGrammarRouteRequest(BaseModel):
    request_id: str
    program_id: str
    guest_workspace_id: str
    brand_context_id: str
    brand_context_version: str
    requested_subtype: SuperVisualSubtype | None = None
    source_evidence_refs: list[str] = Field(min_length=1)
    expression_moment_refs: list[str] = Field(default_factory=list)
    archetype_route_refs: list[str] = Field(default_factory=list)
    operator_intent: str
    target_platform_ref: str
    package_slot_ref: str | None = None

class SuperVisualFeelAxis(BaseModel):
    axis_id: str
    label: str
    min_value: int = Field(ge=0, le=100)
    max_value: int = Field(ge=0, le=100)
    target_value: int = Field(ge=0, le=100)
    evidence_requirement: str

class SuperVisualFeelMatrix(BaseModel):
    matrix_id: str
    version: str
    subtype: SuperVisualSubtype
    required_feel_summary: str
    forbidden_feel_summary: str
    visual_density_target: Literal["low", "medium", "high"]
    negative_space_posture: Literal["cinematic", "argumentative", "instructional", "poster"]
    typography_posture: Literal["thesis", "caption", "proof", "label_stack", "poll"]
    color_posture: Literal["brand-led", "contrast-led", "symbol-led", "minimal"]
    axes: list[SuperVisualFeelAxis]
    hard_failure_codes: list[str]

class SuperVisualVisualGrammarRecord(BaseModel):
    grammar_code: str
    version: str
    subtype: SuperVisualSubtype
    title: str
    meaning_function: str
    eligible_archetype_routes: list[str]
    required_source_roles: list[str]
    required_brand_assets: list[str]
    layer_stack_contract: list[dict]
    text_budget_contract: dict
    negative_space_contract: dict
    micro_semiotic_anchor_policy: dict
    provider_policy_refs: list[str]
    skia_component_refs: list[str]
    primitive_role_requirements: list[str]
    eval_rubric_refs: list[str]
    hard_failure_codes: list[str]

class SuperVisualPrimitiveRoleCoverageReceipt(BaseModel):
    receipt_id: str
    program_id: str
    grammar_code: str
    subtype: SuperVisualSubtype
    meaning_transform_primitive_ref: str
    delivery_shape_primitive_ref: str
    format_material_primitive_ref: str
    evidence_refs_by_primitive: dict[str, list[str]]
    failed_roles: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    created_at: datetime

class SuperVisualGrammarCandidateScore(BaseModel):
    candidate_id: str
    grammar_code: str
    subtype: SuperVisualSubtype
    source_fit_score: float = Field(ge=0, le=1)
    primitive_fit_score: float = Field(ge=0, le=1)
    brand_fit_score: float = Field(ge=0, le=1)
    platform_fit_score: float = Field(ge=0, le=1)
    text_fit_score: float = Field(ge=0, le=1)
    micro_semiotic_fit_score: float = Field(ge=0, le=1)
    provider_feasibility_score: float = Field(ge=0, le=1)
    deterministic_render_score: float = Field(ge=0, le=1)
    total_score: float = Field(ge=0, le=1)
    blocker_codes: list[str] = Field(default_factory=list)
    repair_suggestions: list[str] = Field(default_factory=list)

class SuperVisualGrammarRouterDecision(BaseModel):
    decision_id: str
    request_id: str
    program_id: str
    selected_subtype: SuperVisualSubtype
    selected_grammar_code: str
    selected_feel_matrix_ref: str
    candidate_scores: list[SuperVisualGrammarCandidateScore]
    primitive_coverage_receipt_ref: str
    atlas_registry_version: str
    router_policy_ref: str
    operator_override_reason: str | None = None
    decision_receipt_ref: str
    created_at: datetime
```

## 6. Backward Compatibility Fallback

Existing `SPV-CON`, `SPV-SYM`, and `SPV-PRM` references from TS-CMF-099 through TS-CMF-105 may continue to exist, but they must be promoted into the new grammar atlas before production use. During migration:

| Legacy Behavior | Temporary Status | Production Requirement |
|---|---|---|
| Hard-coded SuperVisual layout in prompt | Lab only | Must be represented as grammar atlas record. |
| Ideogram output selected by taste | Lab only | Must pass router score, primitive coverage, and Skia deterministic render. |
| Generic SuperVisual label without subtype | Blocked | Must resolve to `SPV-CON`, `SPV-SYM`, or `SPV-PRM`. |
| Existing single-image registry contract | Allowed | Must include SuperVisual grammar binding and feel matrix binding. |
| Manual operator override | Allowed with reason | Must store override reason, failed candidate scores, and approval receipt. |

## 7. Tasks

1. Create `src/ccp_studio/contracts/supervisual_grammar.py`.
2. Create `registries/composition/supervisual_visual_grammar_atlas.v1.json`.
3. Create `registries/composition/supervisual_feel_matrix.v1.json`.
4. Implement registry validation for grammar atlas records.
5. Implement registry validation for feel matrix records.
6. Implement `SuperVisualGrammarAtlasService`.
7. Implement grammar routing score calculation.
8. Implement primitive role coverage receipt generation.
9. Integrate selected grammar into `StillVisualCompositionProgram`.
10. Integrate selected grammar into Skia scene compiler obligations.
11. Add approval blockers for generic flattening, missing contrast, missing symbol, missing authority evidence, missing primitive role, and non-deterministic final scene.
12. Add golden fixtures for each SuperVisual subtype and negative fixtures for each failure mode.

## 8. Acceptance Criteria

### AC134-01: Subtype Must Resolve

Given a SuperVisual request without a clear subtype, when routing runs, then the router must either infer one from source evidence or block with `SUPERVISUAL_SUBTYPE_REQUIRED`.

### AC134-02: Grammar Atlas Must Bind

Given a selected SuperVisual candidate, when no grammar atlas record exists for its grammar code, then the router must block with `SUPERVISUAL_GRAMMAR_ATLAS_MISSING`.

### AC134-03: Conceptual Contrast Must Show Contrast

Given `SPV-CON`, when both sides express the same idea, share the same semantic role, or do not create a visible decision pressure, then evaluation must block with `SPV_CON_CONTRAST_NOT_VISIBLE`.

Failure example: a "before vs after" visual uses two similar confident portraits and generic motivational copy without a true contradiction.

### AC134-04: Symbolic SuperVisual Must Explain Its Symbol

Given `SPV-SYM`, when a metaphor object is present but has no source evidence, Brand Context anchor, or primitive proof, then evaluation must block with `SPV_SYM_SYMBOLIC_OPERATION_MISSING`.

Failure example: a river, mask, key, or flame appears because it looks dramatic, but the guest never spoke about it and Brand Genesis does not justify it.

### AC134-05: Authority Visual Must Be Earned

Given `SPV-PRM`, when the premise is not supported by quote, credential, framework, lived evidence, audience context, or Brand Context, then evaluation must block with `SPV_PRM_BRAND_AUTHORITY_MISSING`.

### AC134-06: Primitive Role Coverage Is Mandatory

Given any SuperVisual candidate, when the primitive coverage receipt lacks meaning, delivery, or format/material role, then approval must block with `PRIMITIVE_ROLE_COVERAGE_FAILED`.

### AC134-07: Generic Flattening Fails

Given any SuperVisual candidate, when the visual grammar collapses into a generic premium-social layout that could fit any guest, any claim, and any format, then evaluation must block with `SUPERVISUAL_GENERIC_POSTER_FLATTENING`.

### AC134-08: Micro-Semiotic Anchors Are Safe

Given a grammar that uses cultural, personal, religious, political, trauma, or identity symbols, when no micro-semiotic safety decision is attached, then approval must block with `SUPERVISUAL_MSA_UNSAFE`.

### AC134-09: Skia Scene Must Match Grammar

Given a selected grammar, when the compiled Skia scene omits required zones, layers, objects, text hierarchy, or negative-space obligations, then render approval must block with `SKIA_SCENE_NOT_DETERMINISTIC`.

## 9. Dependencies

| Dependency | Type | Status |
|---|---|---|
| TS-CMF-099 | Tech spec | Required |
| TS-CMF-100 | Tech spec | Required |
| TS-CMF-101 | Tech spec | Required |
| TS-CMF-102 | Tech spec | Required |
| TS-CMF-103 | Tech spec | Required |
| TS-CMF-104 | Tech spec | Required |
| TS-CMF-105 | Tech spec | Required |
| TS-CMF-133 | Tech spec | Required parent manifest |
| `cmf_composition_primitive_triads.v1.json` | Registry | Required |
| `single_image_router_policy.v2.json` | Registry | Required |
| `single_image_provider_responsibilities.v2.json` | Registry | Required |
| `supervisual_visual_grammar_atlas.v1.json` | New registry | Required |
| `supervisual_feel_matrix.v1.json` | New registry | Required |

## 10. Testing Strategy

### Unit Tests

1. Validate each grammar atlas record has subtype, meaning function, source role requirements, layer contract, text budget, provider policy, primitive requirements, and hard failure codes.
2. Validate each feel matrix record has forbidden feel summary and at least three measurable feel axes.
3. Validate router rejects missing source refs, missing Brand Context, missing platform target, and missing subtype resolution.
4. Validate primitive role coverage receipt rejects duplicate role masquerading as three separate validations.
5. Validate candidate scoring is deterministic for the same request and registry versions.

### Integration Tests

1. Route a valid `SPV-CON` request from a contradiction in interview source evidence and confirm selected grammar has contrast obligations.
2. Route a valid `SPV-SYM` request from a metaphor-rich expression moment and confirm symbolic object obligations.
3. Route a valid `SPV-PRM` request from an authority teaching claim and confirm proof/authority obligations.
4. Bind each route to a TS-CMF-133 program and confirm downstream provider plan and Skia scene obligations inherit the grammar.
5. Verify approval gate blocks when a grammar route receipt is missing.

### Negative Fixtures

Store under `THE CMF STUDIO/tests/fixtures/supervisuals/`:

| Fixture | Expected Failure |
|---|---|
| `spv_con_no_contrast.json` | `SPV_CON_CONTRAST_NOT_VISIBLE` |
| `spv_sym_random_symbol.json` | `SPV_SYM_SYMBOLIC_OPERATION_MISSING` |
| `spv_prm_unsupported_claim.json` | `SPV_PRM_BRAND_AUTHORITY_MISSING` |
| `spv_generic_poster.json` | `SUPERVISUAL_GENERIC_POSTER_FLATTENING` |
| `spv_missing_primitive_role.json` | `PRIMITIVE_ROLE_COVERAGE_FAILED` |

### Golden Tests

Golden fixtures must assert:

1. Route score is stable.
2. Selected grammar code is stable.
3. Primitive role receipt contains three distinct roles.
4. Skia scene contains required grammar zones.
5. Render hash is deterministic when replayed with locked assets.
