---
title: "CMF Still Visual Composition Architecture Audit"
status: "audit"
created_at: "2026-06-25"
auditor: "Codex / John PM support"
question: "Can carousel and SuperVisual visual composition benefit from the same architectural composition pattern, or is that unnecessary?"
scope:
  - "Carousels"
  - "SuperVisuals"
  - "Single-image visual composition"
  - "Geometrics / Skia / SAM3 / PRETEXT / Qwen layered still rendering"
sources:
  - "THE CMF STUDIO/docs/content-asset-code-and-format-registry.md"
  - "THE CMF STUDIO/docs/composition-libraries/CMF_Carousel_Slide_Composition_Library.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-101-single-image-router-format-family-and-archetype-selection.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md"
  - "THE CMF STUDIO/docs/tech-specs/TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md"
  - "THE CMF STUDIO/registries/composition/carousel_slide_composition_library.v1.json"
  - "THE CMF STUDIO/registries/composition/carousel_composition_atlas.v1.json"
  - "THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json"
  - "THE CMF STUDIO/registries/composition/single_image_skia_component_catalog.v2.json"
  - "THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json"
---

# CMF Still Visual Composition Architecture Audit

## 1. Direct Answer

Yes. Carousel and SuperVisual visual composition should use the same architectural composition discipline as the rest of CMF, but adapted for still visuals.

The shared architecture should not copy the video timeline engine wholesale. Still visuals do not need transcript-clocked cuts, OTIO edit interchange, or frame-accurate audio sync. They do need the same production-grade pattern:

```text
structured source context
-> format and meaning route
-> composition grammar selection
-> primitive triad gate
-> provider materialization plan
-> layer, mask, and typography measurement
-> Geometrics layout plan
-> deterministic Skia render
-> eval receipt
-> operator approval
-> export manifest
```

This is not overengineering. It is the difference between "pretty generated posts" and CMF-grade visual assets that are source-faithful, brand-scoped, primitive-compliant, reproducible, reviewable, and safe to publish.

## 2. Evidence Snapshot

| Area | Evidence | Audit Reading |
|---|---|---|
| Content format registry | `CAR-LST`, `CAR-JUX`, `SPV-CON`, `SPV-SYM`, `SPV-PRM`, `VPL-*`, `TWQ-*`, `MEM-*`, `RCT-SEED` are defined in `content-asset-code-and-format-registry.md`. | CMF already distinguishes output families. Visual composition cannot be a single generic template path. |
| Carousel slide library | `carousel_slide_composition_library.v1.json` declares 12 slide atoms and requires at least 3 primitives. | Carousels have a meaning layer: slide atoms are not templates; they are sequence functions. |
| Carousel atlas | `carousel_composition_atlas.v1.json` contains 44 canonical compositions, 12 sequence grammars, 118 inspected slides, and 16 inspected folders. | Carousels have a visual grammar layer. This is the strongest current still-visual architecture. |
| Carousel workflow specs | `TS-CMF-096`, `TS-CMF-097`, and `TS-CMF-098` bind slide atoms, atlas router, visual grammar plan, Geometrics, Skia, eval, and approval. | The documented carousel architecture is close to the correct end state. |
| Single-image registry | `single_image_composition_registry.v2.json` contains 28 composition contracts across families such as comparison polls, assertion commentary, conceptual metaphor, cartoon framework, and documentary social cards. | SuperVisuals and other single-image outputs have registry substance, not just vague format labels. |
| SuperVisual specs | `TS-CMF-099` through `TS-CMF-105` decompose registry loading, routing, SuperVisual semantics, provider planning, Skia compile, eval, review, and fixtures. | The SuperVisual chain exists, but it is thinner and less integrated than the carousel chain. |
| Runtime code | Current `src/ccp_studio` scan finds only Ideogram composition lineage code/tests for this area. The specified carousel and single-image service files are not present. | Specs are not yet implementation. The still-visual production engine is documented but not built. |

## 3. What Carousel Composition Currently Does

The carousel system currently has the clearest visual composition architecture.

### 3.1 Format and Asset Identity

The content asset registry defines carousel codes:

| Code | Meaning |
|---|---|
| `CAR-LST` | Listicle carousel, numbered learning sequence, framework map, explanatory sequence. |
| `CAR-JUX` | Juxtaposition carousel, before/after, contrast, timeline, mistake/fix, two-world comparison. |

It also requires content assets to belong to a brand workspace, guest, session, package, format, sequence, and version. This is critical because carousel generation must not happen from a global loose prompt. It must happen inside a guest-scoped production context.

### 3.2 Slide Meaning Layer

The carousel slide library defines 12 slide atoms:

```text
HOOK_PREMISE
AUDIENCE_MIRROR
STAKES_COST
MYTH_BREAK
MECHANISM_REVEAL
THREE_PILLAR_MAP
JUXTAPOSITION
EVIDENCE_OBJECT
CONCRETE_SCENE
PATTERN_BREAK
REFRAME_IDENTITY
APPLICATION_CTA
```

This is strong architecture because each slide has a job in the audience's understanding. The carousel is treated as a sequence of meaning-bearing moves, not as a batch of designed cards.

### 3.3 Visual Grammar Layer

The carousel composition atlas adds the missing concrete visual grammar:

```text
CarouselSlideAtom = meaning job
CanonicalCarouselComposition = visual grammar
CompositionRouterDecision = why this composition fits now
CarouselSlideVisualGrammarPlan = selected grammar plus constraints
GeometricsLayoutPlan = exact coordinates, text, masks, and render readiness
```

The atlas has enough density to matter: 44 compositions and 12 sequence grammars. Its records include normalized zones, attention paths, text budgets, supported aspect ratios, tool routing rules, avoid rules, evidence notes, and render responsibilities.

### 3.4 Primitive and Eval Layer

Carousel rules require at least three primitive validations per slide and sequence-level coverage for structure, grid, variety, and eye-path. Key primitives named in the carousel library include:

| Primitive | Function |
|---|---|
| `PRM-BUS-003` | Narrative structural backbone. |
| `PRM-BUS-012` | Grid as cognitive relief. |
| `PRM-VSG-018` | Sequence over single image. |
| `PRM-VSG-001` | Composition as eye-path engineering. |
| `PRM-PRS-032` | Explanation engine. |
| `PRM-PRS-015` | What is / what could be contrast engine. |

This directly supports Emilio's rule that nothing should be built without at least three primitive validations.

### 3.5 Current Carousel Gap

The carousel architecture is well specified, but the current runtime is not built. The specs name owners such as:

```text
src/ccp_studio/contracts/carousel_builder.py
src/ccp_studio/contracts/carousel_composition_atlas.py
src/ccp_studio/services/carousel_builder_service.py
src/ccp_studio/services/carousel_composition_atlas_service.py
```

Current filesystem checks show these files do not exist yet. The current implementation only has Ideogram `CompositionJob` lineage concepts in `contracts/composition.py` and `services/composition_service.py`, plus one Ideogram lineage test. That is useful for composition-plate governance, but it is not the carousel builder engine.

## 4. What SuperVisual Composition Currently Does

The SuperVisual chain is present, but less mature than the carousel chain.

### 4.1 Format Separation

The registry separates three SuperVisual subtypes:

| Code | Meaning |
|---|---|
| `SPV-CON` | Conceptual contrast SuperVisual. High-impact visual metaphor or binary contrast. |
| `SPV-SYM` | Symbolic SuperVisual. Symbolic single-frame image tied to primitive or route. |
| `SPV-PRM` | Premium brand SuperVisual. Polished, brand-forward standalone visual. |

This distinction is correct because these three should not share the same feel. A conceptual contrast poster, a symbolic metaphor scene, and a premium brand asset are different visual machines.

### 4.2 Single-Image Registry

The single-image registry gives SuperVisuals and related still formats a composition base. It includes 28 composition contracts and covers families such as:

```text
assertion_commentary
comparison_poll
conceptual_metaphor
cartoon_moral
cartoon_framework
documentary_social_card
promo_live
```

The format registry maps SuperVisuals to canonical examples:

| Format | Candidate composition examples |
|---|---|
| `SPV-CON` | `POWERFUL_DEMONSTRATION_SINGLE`, `CONCEPTUAL_CONTRAST_POSTER_LIGHT`, `CONCEPTUAL_CONTRAST_POSTER_DARK`, `ONE_SCENE_TWO_SCENARIOS` |
| `SPV-SYM` | `MAIN_CHARACTER_EMOTIONAL_SCENE`, `CARTOON_OBJECT_METAPHOR`, `PROBLEM_AMPLIFICATION_URGENCY`, `CARTOON_MORAL_SCENE` |
| `SPV-PRM` | `QUOTE_ON_CLOSEUP_COMMENTARY`, `MINIMAL_BLACK_QUOTE_CARD`, `EXPERT_FLYER_MINIMAL`, `LIVE_SHOW_FLYER` |

This is a real start. It prevents SuperVisuals from collapsing into quote cards.

### 4.3 SuperVisual Semantic Layer

`TS-CMF-102` defines `SuperVisualCompositionBrief`, `SuperVisualPrimitiveTriadReceipt`, and `SuperVisualVisualFeelContract`. This is the right object family because a SuperVisual carries the whole argument in one frame.

However, `TS-CMF-102` is much thinner than the carousel atlas spec. It defines the three modes and the primitive triad rule, but it does not yet provide a SuperVisual-specific visual grammar atlas comparable to `TS-CMF-098`. It relies heavily on the general single-image registry.

### 4.4 Current SuperVisual Gap

The SuperVisual chain lacks a first-class equivalent to:

```text
SuperVisualVisualGrammarAtlas
SuperVisualCompositionRouterDecision
SuperVisualMeaningOperationScore
SuperVisualVisualFeelMatrix
SuperVisualPrimitiveRoleCoverageReceipt
```

The current specs say the right things, but they do not yet make the three SuperVisual types operationally distinct enough. The danger is "same-feel flattening": `SPV-CON`, `SPV-SYM`, and `SPV-PRM` could still route to the same poster-like treatment unless the runtime has stronger grammar, scoring, and eval gates.

As with carousels, the named runtime files do not exist yet:

```text
src/ccp_studio/contracts/single_image.py
src/ccp_studio/services/single_image_registry_service.py
src/ccp_studio/services/single_image_compiler_service.py
```

## 5. Architectural Fit Decision

The right move is to introduce a shared still-visual architecture kernel, then keep format-specific composition grammars.

### 5.1 Shared Kernel

Carousels and SuperVisuals should share:

```text
StillVisualRequestEnvelope
StillVisualCompositionProgram
CompositionGrammarRouterDecision
PrimitiveTriadGateReceipt
ProviderMaterializationPlan
LayerMaskTypographyManifest
GeometricsLayoutPlan
SkiaRenderJob
VisualEvaluationReceipt
OperatorApprovalReceipt
StillVisualExportManifest
```

This gives both systems the same production spine: structured context, deterministic contracts, provider boundaries, review receipts, and replayable output.

### 5.2 Format-Specific Grammar

They should not share the same grammar layer.

| Family | Needs |
|---|---|
| Carousel | Sequence grammar, slide atoms, slide-to-slide rhythm, continuity, pattern break logic, export set manifest. |
| SuperVisual | Single-frame semantic operation, visual feel contract, high-impact hierarchy, source-backed claim/symbol, stronger visual distinctness between `SPV-CON`, `SPV-SYM`, and `SPV-PRM`. |
| Visual Poll | Choice architecture, option symmetry, vote affordance, contrast legibility, engagement hook. |
| Tweet-like Quote | Voice fidelity, identity card, quotation accuracy, readable hierarchy, social-native restraint. |
| Meme | Meme mechanism, distortion boundary, humor safety, source-safe exaggeration. |

The shared architecture is the skeleton. The format grammar is the nervous system. Both are required.

## 6. Audit Findings

### Finding 1: Shared Architecture Is Needed

Severity: Critical

Still visuals benefit from the same CMF architectural composition pattern because they need reproducibility, source fidelity, brand separation, primitive validation, provider boundaries, eval receipts, and operator approval. Without the architecture, Ideogram/Qwen/Skia become disconnected tools instead of a governed production engine.

### Finding 2: Carousel Is Architecturally Strong But Not Implemented

Severity: Critical

The carousel specs and registries are strong. `TS-CMF-096`, `TS-CMF-097`, and `TS-CMF-098` describe the correct handoff from slide atom to visual grammar to Geometrics/Skia. The registry has meaningful depth. The problem is runtime absence: contracts, services, routes, workflow state, Skia still render target, and tests are not implemented.

### Finding 3: SuperVisuals Need A Stronger Atlas Equivalent

Severity: High

SuperVisuals have format codes, a single-image registry, a primitive triad spec, and downstream provider/render/eval specs. But they do not yet have a dedicated SuperVisual visual grammar atlas with the same specificity as the carousel atlas. That is the main reason SuperVisuals remain at risk of generic poster output.

### Finding 4: Primitive Triads Are Present But Need Role Coverage Enforcement

Severity: High

The specs and registries repeatedly require at least three primitives. The missing operational detail is role coverage. Three aesthetic primitives should not pass. A valid triad should cover:

```text
meaning operation
visual/form delivery
audience cognition or emotional effect
```

For SuperVisuals, this should be enforced before provider planning, not only at final eval.

### Finding 5: Current Runtime Is Still Ideogram-Centric

Severity: High

Current runtime code supports Ideogram composition job lineage, provider receipt concepts, composition plates, and downstream edit restrictions. It does not yet implement the still-visual architecture:

```text
no carousel builder service
no carousel atlas loader service
no single-image registry service
no SuperVisual compiler service
no still Skia render service for these outputs
no carousel/SuperVisual tests
```

This means the architecture exists as documentation and registry assets, not as a functioning production subsystem.

### Finding 6: Eval Registry Exists For Single Images But Needs Runtime Binding

Severity: Medium

`single_image_eval_rubrics.v2.json` contains thresholds and profile weights. `TS-CMF-105` defines eval and review. But without service implementation and read-model binding, the eval registry cannot block approvals in practice.

### Finding 7: The Previous Spec Repair Was Correct But Incomplete As A Build State

Severity: Medium

The prior audit correctly decomposed carousel and SuperVisual specs. It repaired documentation structure. It did not implement the contracts/services/tests. The present state should therefore be called:

```text
specified architecture: strong for carousel, partial for SuperVisual
implemented runtime: not yet built
```

## 7. Recommended Architecture Update

Create one shared still-visual orchestration spec and one SuperVisual-specific grammar spec before implementation continues.

### Required Spec 1: Still Visual Composition Program

Suggested ID: `TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md`

Purpose:

```text
Bind carousels, SuperVisuals, visual polls, quote posts, memes, and reaction seeds into one still-visual production command lifecycle.
```

Required objects:

```text
StillVisualCompositionProgram
StillVisualStageState
StillVisualCompositionProgramReceipt
StillVisualProviderMaterializationPlan
StillVisualReviewReadModel
StillVisualExportManifest
```

This spec should reuse `TS-CMF-120` through `TS-CMF-132` stage artifact discipline where appropriate, but remain still-image native.

### Required Spec 2: SuperVisual Visual Grammar Atlas

Suggested ID: `TS-CMF-134-supervisual-visual-grammar-atlas-router-and-primitive-feel-matrix.md`

Purpose:

```text
Give SPV-CON, SPV-SYM, and SPV-PRM the same operational visual grammar depth that carousels have through TS-CMF-098.
```

Required objects:

```text
SuperVisualVisualGrammarRecord
SuperVisualFeelMatrix
SuperVisualGrammarRouterDecision
SuperVisualPrimitiveRoleCoverageReceipt
SuperVisualHardFailureCode
```

Mandatory hard failures:

```text
SUPERVISUAL_SUBTYPE_REQUIRED
SUPERVISUAL_GENERIC_POSTER_FLATTENING
PRIMITIVE_ROLE_COVERAGE_FAILED
SOURCE_MEANING_NOT_VISIBLE
VISUAL_FEEL_CONTRACT_UNPROVEN
SKIA_SCENE_NOT_DETERMINISTIC
```

### Required Spec 3: Still Visual Runtime API And Review Model

Suggested ID: `TS-CMF-135-still-visual-runtime-api-review-read-model-and-approval-workbench.md`

Purpose:

```text
Expose the still-visual engine to PWA, Telegram quick review, and Pi/harness commands with one evidence model.
```

Required routes should be explicit, for example:

```text
POST /api/v1/still-visuals/programs
POST /api/v1/still-visuals/programs/{program_id}/route
POST /api/v1/still-visuals/programs/{program_id}/materialize
POST /api/v1/still-visuals/programs/{program_id}/render
POST /api/v1/still-visuals/programs/{program_id}/evaluate
POST /api/v1/still-visuals/programs/{program_id}/approve
GET  /api/v1/still-visuals/programs/{program_id}/review
```

## 8. Implementation Consequence

The build should not start by hardcoding carousel or SuperVisual rendering separately. It should start with shared still-visual contracts and registry loaders, then implement family-specific routers.

Recommended build order:

1. Add shared still-visual contracts and command states.
2. Implement registry loaders for carousel slide atoms, carousel atlas, single-image compositions, Skia components, provider responsibilities, and eval rubrics.
3. Implement carousel router and `CreateCarouselWorkflow`.
4. Implement SuperVisual grammar atlas and single-image router.
5. Implement provider materialization plans with Ideogram 4, Qwen layered, SAM3, GPT Image 2, Flux 2 Klein 9b, and ComfyUI boundaries.
6. Implement Geometrics/PRETEXT/Skia still render jobs.
7. Implement eval receipts, review read model, approval blockers, and export manifests.

This is not a product phase plan. It is dependency order for building the full system without damaging the architecture.

## 9. Final Verdict

Visual composition content absolutely benefits from the same architectural composition discipline. It is needed.

The correct shape is:

```text
one shared still-visual production architecture
+ family-specific composition grammars
+ primitive role coverage
+ deterministic Skia output
+ eval and approval receipts
```

Carousel is already close at the documentation and registry level. SuperVisuals need the same depth, especially a dedicated visual grammar atlas and stronger subtype separation. Neither carousel nor SuperVisual production is implemented yet in runtime code.

