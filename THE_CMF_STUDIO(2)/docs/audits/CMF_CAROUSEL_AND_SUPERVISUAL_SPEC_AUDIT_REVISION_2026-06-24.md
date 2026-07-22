---
title: "CMF Carousel and SuperVisual Spec Audit and Revision"
status: "revised"
created_at: "2026-06-24"
protocols:
  - "docs/architecture/april_updates/TRIGGER_COMMAND_AUDIT.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Audit.md"
  - "docs/architecture/april_updates/TRIGGER_COMMAND_REVISION.md"
  - "docs/architecture/april_updates/PROMPT_Spec_Revision.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md"
scope:
  - "TS-CMF-095"
  - "TS-CMF-096"
  - "TS-CMF-097"
  - "TS-CMF-098"
  - "TS-CMF-099"
  - "TS-CMF-100"
  - "TS-CMF-101"
  - "TS-CMF-102"
  - "TS-CMF-103"
  - "TS-CMF-104"
  - "TS-CMF-105"
---

# CMF Carousel and SuperVisual Spec Audit and Revision

## 1. Audit Scope

This audit reviews the carousel and SuperVisual still-image specification chain after integration of:

- `CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE`;
- `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE`;
- the existing still visual Geometrics/Skia runtime;
- CMF content asset codes for `CAR-*`, `SPV-*`, `VPL-*`, `TWQ-*`, `MEM-*`, and `RCT-SEED`.

The legacy audit protocol says to audit one spec at a time. For this subsystem pass, each spec was evaluated independently under the same five lenses, then revised as a connected chain because the errors were cross-spec handoff errors.

## 2. Sources Read

| Source | Use |
|---|---|
| `docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit structure. |
| `docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Section-targeted revision discipline. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section spec shape and CBAR/primitive requirements. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Shared deterministic still visual runtime. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Carousel slide atom and sequence layer. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` | Integrated carousel builder workflow. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` | Carousel visual grammar atlas router. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Single Image/SuperVisual umbrella. |
| `THE CMF STUDIO/CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/*` | Source atlas, models, registry, and corpus mapping. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/*` | Source single-image engine bundle. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Format code and subtype truth. |

## 3. Audit Report

### PASS

No spec passed with zero flags before revision because the subsystem had cross-spec handoff issues.

### FLAGS

**[TS-CMF-096] | LENS 5 | SEVERITY: CRITICAL**
- **Finding:** TS-CMF-096 jumped from slide atoms directly to Geometrics, bypassing the TS-CMF-098 atlas router.
- **Location:** Frontmatter exit object, Architecture Traceability, Implementation Plan, schema fields, tasks, acceptance criteria.
- **Required Action:** Change TS-CMF-096 to output atlas-router-ready sequence plans, not Geometrics-ready plans.
- **Revision Applied:** Yes.

**[TS-CMF-098] | LENS 2 | SEVERITY: CRITICAL**
- **Finding:** TS-CMF-098 referenced canonical atlas registry paths that were not present in `THE CMF STUDIO/registries`.
- **Location:** Existing Backend Integration, Implementation Plan, Dependencies.
- **Required Action:** Stage the atlas registry and evidence CSV in canonical registry paths and require schema normalization before runtime truth.
- **Revision Applied:** Yes.

**[TS-CMF-098] | LENS 4 | SEVERITY: WARNING**
- **Finding:** The router specified candidate retrieval and scoring but lacked an explicit selected-score threshold and below-minimum-candidate-pool rule.
- **Location:** Router Score Formula, Acceptance Criteria.
- **Required Action:** Add a minimum score and candidate-pool blocker.
- **Revision Applied:** Yes.

**[TS-CMF-099] | LENS 3 | SEVERITY: CRITICAL**
- **Finding:** TS-CMF-099 owned too much: registry loading, routing, SuperVisual semantics, provider planning, Skia compilation, eval, review, and fixtures.
- **Location:** Overview, Implementation Plan, Tasks, Acceptance Criteria.
- **Required Action:** Keep TS-CMF-099 as umbrella and create buildable child specs.
- **Revision Applied:** Yes.

**[TS-CMF-099] | LENS 2 | SEVERITY: WARNING**
- **Finding:** Primitive role coverage was described but implementation ownership was not sufficiently separated for SuperVisuals.
- **Location:** ADR-05 Primitives and Tasks.
- **Required Action:** Add a SuperVisual-specific primitive and visual-feel spec for `SPV-CON`, `SPV-SYM`, and `SPV-PRM`.
- **Revision Applied:** Yes via TS-CMF-102.

**[TS-CMF-099] | LENS 4 | SEVERITY: WARNING**
- **Finding:** Provider responsibility boundaries existed in the umbrella but needed their own materialization spec to prevent provider execution drift.
- **Location:** Provider responsibilities, Implementation Plan, Tasks.
- **Required Action:** Add a provider job planner spec that enforces Ideogram/GPT Image/Flux/Qwen/SAM3 ownership boundaries.
- **Revision Applied:** Yes via TS-CMF-103.

**[CROSS-SPEC] | LENS 5 | SEVERITY: CRITICAL**
- **Finding:** `TS-CMF-100` had been reserved in a prior video-editing MCDA, but Single Image/SuperVisual decomposition needed the next contiguous numbers.
- **Location:** `docs/audits/CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md`.
- **Required Action:** Move the future video editing binding spec to `TS-CMF-106`.
- **Revision Applied:** Yes.

## 4. Revision Log

| Target | Revision |
|---|---|
| `registries/composition/carousel_composition_atlas.v1.json` | Staged from the carousel atlas source bundle. |
| `registries/composition/evidence/carousel_corpus_mapping.v1.csv` | Staged from the carousel atlas source bundle. |
| `TS-CMF-096` | Changed output from direct Geometrics readiness to atlas-router readiness. |
| `TS-CMF-098` | Added canonical staged registry files, schema-normalization warning, router minimum-score rule, and candidate-pool blocker. |
| `TS-CMF-099` | Added decomposition boundary requiring TS-CMF-100 through TS-CMF-105 before implementation can be complete. |
| `TS-CMF-100` | Added contracts, registry loader, and TypeScript parity spec. |
| `TS-CMF-101` | Added output-family-aware single-image router spec. |
| `TS-CMF-102` | Added SuperVisual primitive triad and visual-feel spec. |
| `TS-CMF-103` | Added provider job planner and layer materialization spec. |
| `TS-CMF-104` | Added Skia scene compiler and render binding spec. |
| `TS-CMF-105` | Added eval, review, and golden fixture runtime spec. |
| `docs/tech-specs/README.md` | Added `TS-CMF-100` through `TS-CMF-105` and decomposition note. |
| `CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md` | Moved future video edit compiler reference from `TS-CMF-100` to `TS-CMF-106`. |

## 5. Current System Shape After Revision

### Carousel Chain

```text
TS-CMF-096
CarouselSlideAtom / CarouselSequencePlan
-> TS-CMF-098
CompositionRouterDecision / CarouselSlideVisualGrammarPlan
-> TS-CMF-095
GeometricsLayoutPlan / SkiaRenderJob
-> TS-CMF-097
CarouselBuilderReceipt / export lifecycle
```

### SuperVisual and Single Image Chain

```text
TS-CMF-100
SingleImageRegistryBundle
-> TS-CMF-101
SingleImageRouterDecision
-> TS-CMF-102
SuperVisualCompositionBrief / PrimitiveTriadReceipt
-> TS-CMF-103
ProviderJobPlan / LayerMaterializationReceipt
-> TS-CMF-104
SingleImageSceneSpecV2 / SkiaRenderReceipt
-> TS-CMF-105
EvaluationReceipt / ReviewReadModel / ProductionRecord
```

## 6. Remaining Implementation Blockers

| Blocker | Why It Still Matters |
|---|---|
| The carousel atlas JSON is staged, not normalized into the final CMF production schema. | TS-CMF-098 now explicitly blocks runtime truth until schema metadata and hash validation pass. |
| Child specs TS-CMF-100 through TS-CMF-105 are newly written and still need implementation. | They repair the superficial one-spec problem, but code is not built yet. |
| Skia still rendering remains a downstream implementation dependency. | Both carousels and SuperVisuals rely on TS-CMF-095 being implemented. |
| PWA/Telegram review read models still need code. | Specs define evidence parity, but implementation must expose it. |
| Golden visual fixtures must be created. | Specs require them; they are not yet generated assets. |

## 7. Summary Statistics

| Metric | Count |
|---|---:|
| Specs reviewed before revision | 5 |
| Specs added by revision | 6 |
| Specs modified by revision | 4 |
| Registry files staged | 2 |
| Critical findings | 3 |
| Warning findings | 3 |
| Notes | 0 |
| Cross-spec consistency issues repaired | 2 |
