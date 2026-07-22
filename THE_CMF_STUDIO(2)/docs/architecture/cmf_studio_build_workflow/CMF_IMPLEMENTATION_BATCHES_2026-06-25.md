---
title: "CMF Studio Implementation Batches"
status: "active-plan"
created_at: "2026-06-25"
owner: "Codex / CMF Studio Build Workflow"
source_index: "THE CMF STUDIO/docs/tech-specs/README.md"
scope:
  completed_foundation:
    - "TS-CMF-001 through TS-CMF-070"
    - "TS-CMF-071 and TS-CMF-077 as existing validation anchors"
  active_implementation_specs:
    - "TS-CMF-072 through TS-CMF-076"
    - "TS-CMF-078 through TS-CMF-106"
    - "TS-CMF-110 through TS-CMF-135"
  intentionally_unused:
    - "TS-CMF-107"
    - "TS-CMF-108"
    - "TS-CMF-109"
batch_count: 3
---

# CMF Studio Implementation Batches

## 1. Purpose

This document splits the remaining CMF Studio implementation work into three executable batches. The split is not by document numbering alone. It follows dependency physics:

1. Build the composition contract spine first so every later renderer, provider, and UI surface has canonical objects to call.
2. Build the asset and program compilers next so carousels, SuperVisuals, PaperCut, 2D characters, sequencing, and video editing become executable.
3. Build orchestration, stage manifests, QA, approval, UI read models, cost governance, and final release hardening last.

The first foundation batch, `TS-CMF-001` through `TS-CMF-070`, already has implementation evidence in code/tests and build receipts. `TS-CMF-071` and `TS-CMF-077` also have code/test anchors and should be regression-tested during Batch 1 instead of rebuilt from scratch.

## 2. Batch Overview

| Batch | Name | Spec Count | Primary Outcome | Must Finish Before |
|---|---:|---:|---|---|
| Batch 1 | Composition Spine and Primitive-Gated Runtime Contracts | 20 | Reaction/composition runtime contracts, registries, beat maps, visual feel gates, layer manifests, provider-safe template conversion, composition eval and approval workbench. | Any production carousel, SuperVisual, 2D character, or video edit compiler. |
| Batch 2 | Asset and Program Compilers | 24 | Animation Studio, headless 2D rendering, Geometrics/Skia, carousel builder, single-image/SuperVisual runtime, `VideoEditProgram`, 2D character programs, and conscious sequencing. | Stage orchestration, QA, final review, and release workbench. |
| Batch 3 | Production Orchestration, QA, Review, and Release Hardening | 16 | OpenMontage-native production manifest pattern, stage director, tool/provider registries, project workspace checkpoints, reference media, render runtime locks, QA gates, budget governance, still visual parent program, and approval workbench. | End-to-end operator-ready build completion. |

## 3. Global Build Rules

Every batch must follow these rules:

- Implement inside `THE CMF STUDIO/src/ccp_studio`, `THE CMF STUDIO/registries`, `THE CMF STUDIO/tests/cmf_studio`, and `THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow`.
- Extend existing contracts, services, repositories, APIs, workflows, generated TypeScript, and tests rather than replacing the built foundation.
- Preserve existing completed specs unless a new spec explicitly requires an adapter or extension.
- Write or update build receipts in `THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts`.
- Run target tests after each spec cluster and a broader regression after each batch.
- Add audit/revision receipts when a spec fails implementation readiness before coding.
- All composition-bearing objects must load `registries/evals/composition/cmf_composition_primitive_triads.v1.json` and validate exact registered primitive IDs.
- No production output may be approved without source refs, receipts, eval gates, approval blocker state, and operator-readable review evidence.

## 4. Batch 1 - Composition Spine and Primitive-Gated Runtime Contracts

### Scope

Batch 1 implements the missing runtime spine between existing editing sessions and the later media compilers. It makes composition JSON, visual feel, transcript timing, Brand Genesis binding, reaction clips, and composition evals first-class backend objects.

### Specs

| Order | Spec | Build Role |
|---:|---|---|
| 1 | `TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | Bind reaction templates to the migrated scene-builder runtime. |
| 2 | `TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Make composition JSON the source of truth for previews and renderer props. |
| 3 | `TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` | Implement stacked reaction clip composition: upper reaction UI, lower human cutouts. |
| 4 | `TS-CMF-075-operator-composition-and-template-approval-workbench.md` | Build the immediate approval workbench for composition templates. |
| 5 | `TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | Add OSS adapter evaluation gates before production import. |
| 6 | `TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Register the four canonical video formats and doctrine gates. |
| 7 | `TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md` | Add route-specific visual feel contracts and primitive gates. |
| 8 | `TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Bind composition runtime to transcript timing and Brand Genesis. |
| 9 | `TS-CMF-081-composition-template-family-registry-and-content-asset-codes.md` | Implement template family registry and content asset code extensions. |
| 10 | `TS-CMF-082-brand-genesis-substrate-resolver-for-composition-runtime.md` | Resolve Brand Genesis substrate for composition runtime. |
| 11 | `TS-CMF-083-expression-lineage-and-interview-asset-contract-binding.md` | Bind expression lineage and Interview Asset Contract to compositions. |
| 12 | `TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md` | Compile transcript beats into timeline cues. |
| 13 | `TS-CMF-085-64-state-acting-and-avatar-performance-selector.md` | Select acting/avatar performance states. |
| 14 | `TS-CMF-086-papercut-rig-layer-motion-and-sfx-runtime.md` | Implement PaperCut rig, layer, motion, and SFX runtime contracts. |
| 15 | `TS-CMF-087-micro-semiotic-anchor-selection-and-risk-gate.md` | Add micro-semiotic anchor selection and risk gates. |
| 16 | `TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Bridge Ideogram composition direction into production templates. |
| 17 | `TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Add generative asset layer extraction and repair queue. |
| 18 | `TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Compile renderer props for downstream Remotion/Motion Canvas/Skia surfaces. |
| 19 | `TS-CMF-091-open-source-adapter-template-conversion-and-sandboxing.md` | Convert approved OSS references into sandboxed adapter templates. |
| 20 | `TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Add composition eval fixtures and operator approval workbench integration. |

### Implementation Slices

| Slice | Specs | Primary Files |
|---|---|---|
| 1A - Reaction and composition truth | `072` through `076` | `contracts/composition.py`, `contracts/reaction_editing.py`, `services/composition_service.py`, `services/reaction_editing_service.py`, `api/v1/compositions.py`, `api/v1/review.py`. |
| 1B - Format, feel, and transcript binding | `078` through `084` | New/extended composition registries, beat-map contracts, visual-feel contracts, transcript cue compiler, eval registries. |
| 1C - Performance, PaperCut, Ideogram, adapters, eval workbench | `085` through `092` | Acting/PaperCut contracts, renderer prop compiler, adapter conversion service, composition eval fixtures, review read models. |

### Batch 1 Exit Criteria

- All Batch 1 contracts validate with Pydantic v2.
- Composition JSON is canonical; preview assets cannot replace it.
- Reaction, PaperCut, Ideogram, and OSS adapter paths all emit receipts.
- Route-specific primitive triads use exact registered primitive IDs.
- Transcript beat maps can be converted into timeline cues.
- Operator can see composition evidence, blocker state, and approval state.
- Target tests pass for Batch 1 plus regression tests for `TS-CMF-071` and `TS-CMF-077`.

### Batch 1 Verification Commands

```powershell
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio/test_reaction_editing_template_routing.py
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio/test_doctrine_test_harness.py
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "composition or reaction or doctrine or primitive or beat_map or papercut or ideogram"
```

## 5. Batch 2 - Asset and Program Compilers

### Scope

Batch 2 makes the actual content compilers executable. It builds the asset factories and program-level runtimes for still visuals, carousels, SuperVisuals, 2D character animation, conscious sequencing, and the video edit parent compiler.

### Specs

| Order | Spec | Build Role |
|---:|---|---|
| 1 | `TS-CMF-093-animation-studio-migration-and-operator-rig-editor.md` | Migrate Animation Studio and rig-edit operator surface. |
| 2 | `TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | Add headless 2D frame rendering and avatar export worker. |
| 3 | `TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Restore Skia/SAM3/PRETEXT Geometrics runtime for still visuals. |
| 4 | `TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Add queryable carousel slide atom library. |
| 5 | `TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` | Implement carousel builder compiler and Skia export runtime. |
| 6 | `TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` | Integrate Carousel Composition Atlas and router. |
| 7 | `TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Implement single image and SuperVisual router/runtime. |
| 8 | `TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md` | Add single image registry loader and schema parity. |
| 9 | `TS-CMF-101-single-image-router-format-family-and-archetype-selection.md` | Add output-family-aware single image router. |
| 10 | `TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md` | Add SuperVisual composition families and primitive feel contracts. |
| 11 | `TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md` | Plan provider jobs and layer materialization for still visuals. |
| 12 | `TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md` | Compile Skia scenes and render bindings. |
| 13 | `TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md` | Add still visual eval, review, and golden fixtures. |
| 14 | `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md` | Implement `VideoEditProgram`, OTIO audit, and render runtime. |
| 15 | `TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md` | Add 2D character object model and Character Genesis. |
| 16 | `TS-CMF-111-two-d-character-provider-adapters-rig-authoring-and-asset-promotion.md` | Add 2D character provider adapters and rig asset promotion. |
| 17 | `TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md` | Compile `TwoDCharacterProgram` from transcript/performance intelligence. |
| 18 | `TS-CMF-113-two-d-character-render-runtime-evals-approval-and-repair.md` | Add 2D character render/eval/approval/repair runtime. |
| 19 | `TS-CMF-114-conscious-sequencing-contract-kernel-and-registries.md` | Add conscious sequencing contract kernel and registries. |
| 20 | `TS-CMF-115-interview-brief-v2-sequence-hypothesis-and-expression-acquisition-plan.md` | Add Interview Brief V2 procurement and expression acquisition plan. |
| 21 | `TS-CMF-116-live-ingredient-coverage-tracker-and-cue-suppression-policy.md` | Add live ingredient coverage and cue suppression. |
| 22 | `TS-CMF-117-expression-ingredient-inventory-and-relation-graph.md` | Add source-grounded expression ingredient inventory. |
| 23 | `TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | Compile `ContentSequenceProgram` and handoff to composition engines. |
| 24 | `TS-CMF-119-sequence-eval-gates-learning-and-package-sequencing.md` | Add sequence eval, package learning, and sequencing receipts. |

### Implementation Slices

| Slice | Specs | Primary Files |
|---|---|---|
| 2A - Animation and still visual substrate | `093` through `095` | Animation Studio contracts, headless 2D renderer, Geometrics/Skia runtime, asset/layer manifests. |
| 2B - Carousel and SuperVisual compilers | `096` through `105` | Carousel and single-image contracts, registry loaders, routers, provider planners, Skia scene compiler, eval fixtures. |
| 2C - Video and 2D character programs | `106`, `110` through `113` | `contracts/video_edit_program.py`, `contracts/two_d_character.py`, OTIO exporter, character provider adapters, render/eval/repair services. |
| 2D - Sequencing and interview procurement | `114` through `119` | Sequencing registries, Interview Brief V2, live coverage, ingredient inventory, `ContentSequenceProgram`, sequence evals. |

### Batch 2 Exit Criteria

- Carousel, SuperVisual, single image, 2D character, sequence, and video edit parent objects exist as Pydantic contracts.
- Registry loaders validate migrated bundles from `THE CMF STUDIO` only.
- Skia/Geometrics and video render contracts are deterministic and receipt-backed.
- `VideoEditProgram` can produce proxy/final render contracts and OTIO audit manifests.
- `TwoDCharacterProgram` can compile transcript-timed character performance.
- `ContentSequenceProgram` can hand off to still visual and video compilers without fabricated guest truth.
- Golden and negative fixtures exist for each compiler family.

### Batch 2 Verification Commands

```powershell
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "carousel or single_image or supervisual or skia or geometrics"
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "two_d_character or papercut or animation or avatar"
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "video_edit or otio or sequence or interview_brief"
```

## 6. Batch 3 - Production Orchestration, QA, Review, and Release Hardening

### Scope

Batch 3 turns the compilers into an operator-ready production system. It adapts the OpenMontage architecture into CMF-native stage orchestration, project workspaces, provider selection, reference footage handling, runtime locking, QA, budget controls, approval protocols, and still visual parent workbench.

### Specs

| Order | Spec | Build Role |
|---:|---|---|
| 1 | `TS-CMF-120-openmontage-reference-adapter-governance.md` | Govern OpenMontage as architectural reference only. |
| 2 | `TS-CMF-121-production-pipeline-manifest-registry.md` | Add production pipeline manifest registry. |
| 3 | `TS-CMF-122-stage-director-skill-contract-binding.md` | Bind Stage Director to skills and stage artifacts. |
| 4 | `TS-CMF-123-capability-tool-registry-and-provider-menu.md` | Add tool/capability registry and provider menu. |
| 5 | `TS-CMF-124-scored-provider-selector-and-capability-router.md` | Add scored provider selector and capability router. |
| 6 | `TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md` | Add brand-scoped project workspaces and checkpoints. |
| 7 | `TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md` | Add reference video and existing footage intake. |
| 8 | `TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md` | Add real footage corpus and retrieval adapter. |
| 9 | `TS-CMF-128-render-runtime-selection-and-locking.md` | Add render runtime selection and locking. |
| 10 | `TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` | Add pre-compose QA and slideshow-risk gate. |
| 11 | `TS-CMF-130-post-render-self-review-and-media-qa-gate.md` | Add post-render self-review and media QA. |
| 12 | `TS-CMF-131-budget-cost-and-resource-governance.md` | Add budget, cost, and resource governance. |
| 13 | `TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` | Add canonical stage artifacts and human approval protocol. |
| 14 | `TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md` | Add parent `StillVisualCompositionProgram`. |
| 15 | `TS-CMF-134-supervisual-visual-grammar-atlas-router-and-primitive-feel-matrix.md` | Add SuperVisual visual grammar atlas and primitive feel matrix. |
| 16 | `TS-CMF-135-still-visual-runtime-api-review-read-model-and-approval-workbench.md` | Add still visual runtime API, review read model, and approval workbench. |

### Implementation Slices

| Slice | Specs | Primary Files |
|---|---|---|
| 3A - Production manifest and stage director | `120` through `122` | Production manifest contracts, Stage Director service, skill artifact binding. |
| 3B - Tools, providers, workspace checkpoints | `123` through `128` | Capability registry, scored provider selector, workspace/checkpoint service, footage intake/retrieval adapters. |
| 3C - QA, budget, approval protocol | `129` through `132` | Pre-compose QA, post-render QA, resource governance, human approval protocol. |
| 3D - Still visual parent program and workbench | `133` through `135` | `StillVisualCompositionProgram`, SuperVisual grammar atlas, still visual API/review/read model/workbench. |

### Batch 3 Exit Criteria

- Every compiler can run inside a stage manifest with visible source, provider, eval, approval, and render receipts.
- Provider selection is scored and governed by capability, cost, reproducibility, source scope, and doctrine fit.
- Reference footage and real footage retrieval are source-safe and reviewable.
- Render runtime selection is locked before final output.
- Pre-compose and post-render QA block low-integrity outputs.
- Budget/cost governance prevents uncontrolled provider spend.
- Human approval protocol works across video and still visual assets.
- PWA/Telegram review surfaces expose read models, blockers, repair commands, and approval receipts.

### Batch 3 Verification Commands

```powershell
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "production or stage or provider or workspace or footage"
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio -k "qa or budget or approval or still_visual or workbench"
python -m pytest THE\ CMF\ STUDIO/tests/cmf_studio
```

## 7. Start Here - Batch 1 Immediate Execution Plan

Start with Batch 1 Slice 1A. The first implementation wave should be:

1. Re-run regression tests for the existing anchors:
   - `test_reaction_editing_template_routing.py`;
   - `test_doctrine_test_harness.py`;
   - `test_doctrine_and_primitive_evals.py`.
2. Implement `TS-CMF-072` and `TS-CMF-073` together because scene-template binding and composition JSON approval are one boundary.
3. Implement `TS-CMF-074` only after the composition JSON registry can produce stable renderer props.
4. Implement `TS-CMF-075` after `072` through `074`, because the approval workbench depends on their read models.
5. Implement `TS-CMF-076` before importing or adapting any external template/runtime reference.
6. Write build receipts for each spec and a Batch 1 Slice 1A checkpoint receipt.

### Batch 1 First Slice Definition of Done

- `SceneTemplateRuntimeBinding` contract exists.
- `CompositionTemplateJson` registry exists.
- Reaction clip renderer contract supports upper reaction UI and lower human cutout composition.
- Operator workbench can show template binding, approved JSON, preview refs, eval blockers, and approval state.
- OSS adapter evaluation blocks direct imports without license/security/reproducibility/doctrine/primitive receipts.
- Tests prove preview assets cannot replace canonical composition JSON.

## 8. Build Receipt Policy

Each completed spec must get one build receipt:

```text
THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts/TS-CMF-XXX-<slug>-build.md
```

Each batch should also get one batch-level receipt:

```text
THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts/BATCH-01-composition-spine-build.md
THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts/BATCH-02-asset-program-compilers-build.md
THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts/BATCH-03-production-orchestration-build.md
```

Every receipt must include:

- specs implemented;
- source files changed;
- tests run;
- tests not run and why;
- doctrine/primitive gates touched;
- known residual risk;
- next dependency unlocked.

## 9. Non-Negotiable Constraints

- Do not implement from legacy folders directly. Migrate or transform into `THE CMF STUDIO` registries, fixtures, contracts, or worker assets.
- Do not create newsletter formats.
- Do not treat MVP phasing as a product strategy. Implement the full documented system, but stage the build into dependency-safe batches.
- Do not allow generative providers to own final text, identity, source truth, or canonical composition state.
- Do not approve generated visuals or videos without at least three registered primitives across meaning, delivery, and format/material roles.
- Do not render final assets without source provenance, eval receipts, blocker state, and operator approval.
- Do not let UI editors become hidden sources of truth; they must issue structured commands back to canonical backend objects.
