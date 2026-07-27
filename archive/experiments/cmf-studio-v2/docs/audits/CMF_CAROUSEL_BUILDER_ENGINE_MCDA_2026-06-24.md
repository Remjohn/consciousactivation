# CMF Carousel Builder Engine MCDA Synthesis

Date: 2026-06-24
Status: audit-synthesis
Question: Does the deep research report match what CMF currently has, and what is missing before the carousel builder engine is truly functional?

## 1. Sources Compared

| Source | Role In Comparison |
|---|---|
| `THE CMF STUDIO/deep-research-report.md` | Target architecture for a Carousel Builder Engine using Ideogram 4, Qwen-Image-Layered, SAM3, rough notation, Skia, Pydantic, DSPy, Pi, PWA, and Telegram. |
| `THE CMF STUDIO/docs/architecture.md` | Canonical CMF system architecture, Python-first harness, Command Bus, durable workflows, PWA, Telegram, provider boundaries, and receipt chain. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md` | Ideogram-to-production bridge. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Qwen/SAM3/repair queue specification. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Renderer prop compiler and component harness. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Eval and review workbench. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` | Still visual Geometrics runtime using Skia, SAM3, PRETEXT, and Qwen. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` | Carousel slide atom registry and sequence builder. |
| `THE CMF STUDIO/registries/composition/carousel_slide_composition_library.v1.json` | Machine-readable carousel slide atom registry. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Current runtime renderer contract. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Current runtime deterministic rendering service. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Current provider capability registry implementation. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Current Ideogram CompositionJob and CompositionPlate contracts. |

## 2. Alternatives Scored

| Alternative | Meaning |
|---|---|
| A1 Deep Research Target | The architecture proposed by `deep-research-report.md`. |
| A2 Current CMF Specs | The current documented CMF spec chain, especially TS-CMF-088, 089, 090, 092, 095, and 096. |
| A3 Current CMF Runtime Code | What is currently implemented in `src/ccp_studio`. |

Scoring scale:

```text
5 = complete / production-aligned
4 = strong but missing some operational detail
3 = partial and usable, but incomplete
2 = specified weakly or disconnected
1 = mostly absent
0 = absent or contradictory
```

Weighted score formula:

```text
weighted_score = weight * score / 5
```

## 3. MCDA Criteria

| ID | Criterion | Weight | Why It Matters |
|---|---:|---:|---|
| C1 | Canonical context envelope | 10 | Carousel generation must start from brand, expression, asset package, target platform, and visual/voice DNA instead of loose prompts. |
| C2 | End-to-end carousel orchestration | 12 | A real engine needs a single workflow/command chain, not scattered service fragments. |
| C3 | Carousel slide semantics | 8 | Carousels need slide atoms with composition meaning, not generic templates. |
| C4 | Provider role boundaries | 8 | Ideogram, Qwen, SAM3, Skia, Remotion, and repair models must not be treated as interchangeable. |
| C5 | Ideogram composition bridge | 8 | Ideogram should direct composition but not own final text, final identity, or final geometry. |
| C6 | Layer extraction and editability | 8 | Qwen/SAM3 must produce editable layer/mask manifests, not decorative raster outputs. |
| C7 | Deterministic still rendering and export | 12 | Carousels require Skia/CanvasKit PNG/PDF export as final truth. |
| C8 | Rough annotation parity | 6 | Rough notation must become a reproducible annotation manifest, not a DOM-only effect. |
| C9 | Eval, QC, and primitive gates | 10 | A visually strong slide still fails if it violates source truth, primitives, OCR, layout, consent, or brand policy. |
| C10 | Operator review surfaces | 6 | PWA and Telegram must review the same canonical evidence/read model. |
| C11 | Contract/codegen authority | 6 | Python/Pydantic must generate frontend/runtime contract projections. |
| C12 | Implementation readiness and risk control | 6 | Licensing, provider cost, caching, workflow retries, and operational gates must be explicit. |

Total weight: 100.

## 4. Score Matrix

| Criterion | Weight | A1 Deep Research Target | A2 Current CMF Specs | A3 Current Runtime Code |
|---|---:|---:|---:|---:|
| C1 Canonical context envelope | 10 | 4.0 | 4.0 | 3.0 |
| C2 End-to-end carousel orchestration | 12 | 5.0 | 2.5 | 1.5 |
| C3 Carousel slide semantics | 8 | 3.5 | 4.5 | 1.0 |
| C4 Provider role boundaries | 8 | 5.0 | 5.0 | 3.5 |
| C5 Ideogram composition bridge | 8 | 5.0 | 4.5 | 3.0 |
| C6 Layer extraction and editability | 8 | 5.0 | 4.5 | 2.5 |
| C7 Deterministic still rendering and export | 12 | 5.0 | 4.0 | 1.0 |
| C8 Rough annotation parity | 6 | 5.0 | 4.0 | 1.0 |
| C9 Eval, QC, and primitive gates | 10 | 4.0 | 4.5 | 3.0 |
| C10 Operator review surfaces | 6 | 4.0 | 4.0 | 3.0 |
| C11 Contract/codegen authority | 6 | 4.0 | 4.0 | 3.5 |
| C12 Implementation readiness and risk control | 6 | 3.5 | 3.5 | 2.5 |

## 5. Weighted Results

| Alternative | Weighted Score / 100 | Interpretation |
|---|---:|---|
| A1 Deep Research Target | 89.4 | Strong target architecture. It is coherent, integrated, and closer to a complete carousel compiler than our current spec chain. |
| A2 Current CMF Specs | 80.8 | Strong conceptual/spec alignment, but fragmented. The pieces are mostly documented but not bound into one carousel engine spec/workflow. |
| A3 Current Runtime Code | 46.0 | Partial runtime foundation. Important contracts and provider registry records exist, but the actual carousel compiler and Skia still-render path are not implemented. |

## 6. Evidence-Based Findings

### Finding 1: The Report Is Correct About The Architecture Shape

The report's recommended shape is:

```text
CreateCarouselRequest
-> CarouselSpec
-> Ideogram composition
-> Qwen layered decomposition
-> SAM3 cleanup
-> rough annotation manifest
-> QC and provenance
-> Skia final PNG/PDF export
-> PWA/Telegram approval
```

This aligns with CMF doctrine and the current architecture. It is not generic advice. It correctly treats the product as a typed compiler and render system.

### Finding 2: Current CMF Specs Are Close, But Not Integrated

Current specs cover the parts:

| Capability | Current Spec Coverage |
|---|---|
| Ideogram as composition director | TS-CMF-088 |
| Qwen/SAM3 repair and layer pipeline | TS-CMF-089 |
| Renderer prop compiler | TS-CMF-090 |
| Operator eval/review | TS-CMF-092 |
| Skia/PRETEXT/Geometrics still rendering | TS-CMF-095 |
| Carousel slide atoms and sequence builder | TS-CMF-096 |

But the specs do not yet define one integrated carousel compiler workflow that binds all these parts into a single command lifecycle.

### Finding 3: Current Code Confirms The Gap

Runtime evidence:

- `contracts/deterministic_rendering.py` only defines `DeterministicRenderer.remotion` and `DeterministicRenderer.motion_canvas`.
- `services/deterministic_rendering_service.py` defaults to Remotion or Motion Canvas and produces `.mp4` style preview/final URIs.
- Provider capabilities include `qwen_image_layered`, `sam3`, `gpt_image_2`, `flux_2_klein_9b`, `ideogram_4`, Remotion, and Motion Canvas, but there is no `skia.still_render.v1` capability in the current provider registry.
- `TS-CMF-095` specifies Skia as the still visual renderer, but that specification has not yet been implemented in runtime code.
- `TS-CMF-096` defines `CarouselSequencePlan` in a spec, but no Python contract/service currently implements `CarouselSlideAtom`, `CarouselSlideCompositionPlan`, `CarouselSequencePlan`, or `CarouselCompositionLibraryReceipt`.

### Finding 4: My Previous Claim Was Directionally Right But Under-Specified

The earlier conclusion should be sharpened:

```text
The report is not merely "aligned" with CMF.
It is the missing integration blueprint between our fragmented specs and a real carousel compiler runtime.
```

The highest-confidence statement is:

```text
CMF has the conceptual and registry foundation for the carousel engine.
CMF does not yet have the implemented end-to-end Carousel Builder Engine.
```

## 7. Capability Gap Table

| Capability | Report | Current Specs | Current Code | Gap |
|---|---|---|---|---|
| `CreateCarouselRequest` | Explicit | Not as one spec | Missing | Add canonical request contract. |
| `CarouselSpec` | Explicit | Partial via TS-CMF-096 and SceneSpec | Missing | Add carousel compiler contract. |
| `CreateCarouselWorkflow` | Explicit | Missing as integrated workflow | Missing | Add workflow and command lifecycle. |
| Slide atom library | Implied | Strong in TS-CMF-096 and JSON registry | Missing | Implement loader/service/contracts. |
| Ideogram composition | Strong | Strong TS-CMF-088 | Partial | Extend to `generate`, `remix`, `edit`, webhook/persistence. |
| Qwen layered | Strong | Strong TS-CMF-089 | Provider shell only | Implement layer extraction service and manifest normalization. |
| SAM3 cleanup | Strong | Strong TS-CMF-089/095 | Provider shell only | Implement mask/safe-zone contracts and service calls. |
| Rough notation | Strong | Present in TS-CMF-090/094/095 | Missing | Implement annotation cue manifest and renderer parity. |
| Skia still render | Strong | Strong TS-CMF-095 | Missing | Add Skia renderer contract, provider capability, service route, PNG/PDF outputs. |
| PNG/PDF/PPTX export | Strong | Partial | Missing | Add still export manifest and platform export service. |
| PWA review | Strong | Present | Partial | Bind carousel evidence read model. |
| Telegram review | Strong | Present | Partial | Keep as quick review, not full editing surface. |
| ImageCritic governance | Nuanced | Existing ImageCritic references, less nuanced | Service exists as scoring style | Reclassify as gated reference-guided repair, not primary aesthetic judge. |

## 8. MCDA Synthesis

The report should be accepted as a high-quality target architecture, but not as proof that CMF already has the engine. It exposes a precise integration gap.

The correct next move is not to rewrite all existing specs. The correct next move is to add a binding spec and then implement it:

```text
TS-CMF-097: Carousel Builder Engine, Compiler Workflow, and Skia Export Runtime
```

This spec should bind:

- `CreateCarouselRequest`;
- `TargetPlatformSpec`;
- `VoiceVisualDNA`;
- `CarouselSpec`;
- `CarouselSequencePlan`;
- `CarouselSlideCompositionPlan`;
- `LayerManifest`;
- `TextAnnotationCueManifest`;
- `GeometricsLayoutPlan`;
- `SkiaRenderJob`;
- `StillVisualRenderManifest`;
- `CarouselExportManifest`;
- `CarouselBuilderReceipt`;
- `CreateCarouselWorkflow`;
- PWA/Telegram review read model.

## 9. Recommended Priority

| Priority | Action | Why |
|---:|---|---|
| 1 | Write TS-CMF-097 as the integrated Carousel Builder Engine spec. | It prevents the existing specs from remaining fragmented. |
| 2 | Add Python contracts for carousel request/spec/sequence/receipt. | Runtime cannot execute spec-only objects. |
| 3 | Add carousel registry loader for `carousel_slide_composition_library.v1.json`. | This turns slide atoms into queryable runtime data. |
| 4 | Add Skia as a deterministic renderer target and provider capability. | Current runtime cannot produce final still carousel PNG/PDF truth. |
| 5 | Add `CreateCarouselWorkflow` orchestration shell. | This binds planning, providers, QC, render, export, and approval. |
| 6 | Add tests/golden fixtures for one `CAR-LST` and one `CAR-JUX`. | Without fixtures, visual doctrine remains subjective. |

## 10. Final Answer

Yes, I am more sure after MCDA, but the wording must be precise:

```text
The research report is architecturally superior as an integrated target.
Our current CMF specs are mostly aligned but fragmented.
Our current runtime code is not yet sufficient to execute that carousel engine.
```

Therefore, the next artifact should be an integrated spec and implementation plan, not another small patch to TS-CMF-096 alone.
