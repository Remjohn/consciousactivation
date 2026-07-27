# Legacy CMF Hunter Mapping

This note documents how the Narrative Story Doctor + Content Extraction Intelligence V1 layer coexists with the current repo and the legacy CMF reference material. The new layer is a shared compiler layer under `src/ccp_studio`; it does not delete, replace, or directly import legacy CMF runtime code in this branch.

## Current Repo Findings

The exact legacy folders named in the integration prompt are not live at the project root:

- `cmf/SKILL.md`
- `cmf/hunters/`
- `cmf/analysts/`
- `cmf/composers/`
- `cmf/commanders/`
- `cmf/narrative/`
- `commands/cmf-hunt.md`
- `commands/cmf-beat-cluster.md`
- `agents/cmf/`
- `intelligence/`
- `src/ccp/`

The current production namespace is `src/ccp_studio`, and the existing extraction stack already lives there:

- `src/ccp_studio/contracts/extraction.py`
- `src/ccp_studio/repositories/extraction.py`
- `src/ccp_studio/services/extraction_service.py`
- `src/ccp_studio/dspy_programs/extraction_compilers.py`
- `src/ccp_studio/api/v1/extraction.py`

Legacy CMF reference material is preserved under `reference/conscious-rivers/src/ccp/harness/cmf/assembler/`, including:

- `beat_cluster_parser.py`
- `pipeline_commander.py`
- `render_orchestrator.py`
- `scene_intelligence_loader.py`
- `schemas/dep_vid_001_beat_cluster.schema.json`
- `schemas/dep_vid_035_scene_intelligence_runtime.schema.json`

Canonical role and visual-preproduction anchors already exist in:

- `registries/canonical/ontology/master_glossary.v1.json`
- `registries/canonical/skills/shared/visual_preproduction/`
- `docs/architecture/visual-preproduction/`
- `docs/cmf-studio-intelligence-operating-model.md`
- `docs/cmf-studio-agent-factory-architecture.md`

## Mapping Table

| Legacy / Current Role | Old Path Or Anchor | New Role | Preserve | Wrap Later | Do Not Do In This Branch |
|---|---|---|---|---|---|
| Story Doctor | New V1 compiler layer plus existing extraction stack | `NarrativeStoryDoctorService` reverse compiler | Brief-as-prior doctrine, source span discipline, expected-vs-actual comparison | Wrap old hunter outputs into `NarrativeStoryDoctorRun` and `ExtractionQualityReceipt` | Do not make Interview Brief evidence |
| Arc Selection Guide | `reference/.../beat_cluster_parser.py`, arc stage and beat type logic | `compile_clusters`, `compile_delivery_recipe`, `compile_format_fit` | Arc-specific beat meaning, deterministic timing/ordering discipline | Adapter from beat clusters into `NarrativeCluster` and `DeliveryRecipeProgram` | Do not re-analyze approved beat clusters as loose prompts |
| Hunters | Existing `ExtractionService`, `AnchorHitDetector`, `ExpressionMomentCandidateCompiler`; reference beat cluster parser | Future hunter backend adapter behind `NarrativeStoryDoctorService` | Zero-paraphrase source spans, timestamps, candidate hunting from large source space | `ExpressionMomentHunterBackendAdapter` that emits `ExpressionIngredientInventory` | Do not delete or rewrite existing extraction service |
| Analysts | Current source/eval receipts; visual analyst skills | `SourceFidelityReceipt`, `ExtractionQualityReceipt`, `ExtractionCommanderVerdict` | Unsupported-claim blocking, invented-claim rejection, confidence limits | Source truth and quality critic adapters | Do not let LLM judgment override deterministic gates |
| Composers | Visual preproduction skills and reference scene intelligence loader | Engine packet compiler services | Typed packets, source refs, frame/route constraints | Bridge packets into SuperVisual, Carousel, Video, and Visual Preproduction services | Do not create provider jobs from loose narrative prose |
| Commanders | `reference/.../pipeline_commander.py`; current command bus patterns | `ExtractionCommanderService` | Authorization before production, state/receipt discipline | Durable command/workflow integration after API/runtime phase | Do not add API endpoints in this branch |
| Beat Cluster Extractor | `reference/.../beat_cluster_parser.py` | `TranscriptBeatMap`, `NarrativeCluster`, `ClusterMeaningGraph` compiler inputs | Beat order, arc stage, transition intent, frame timing | Beat-cluster-to-cluster adapter | Do not collapse clusters into generic summaries |
| Visual Researcher | `registries/canonical/skills/shared/visual_preproduction/02_visual_schema.research.compile.skill.yaml` | Downstream visual preproduction backend for engine packets | Source evidence, VisualSchema, familiarity elements, PRIMAL/VAE path | Use `SuperVisualExtractionPacket` and `VideoExtractionPacket` as source-backed inputs | Do not perform unmanaged asset search |
| Storyboard Composer | `registries/canonical/ontology/master_glossary.v1.json`; visual preproduction skills | Storyboard ingredient and beat visual plan compiler | StoryboardCommanderVerdict, typed visual beat plans | Connect extraction packets to visual preproduction packet freeze | Do not bypass Storyboard Commander for full-batch work |
| CAC Composer / Analyst | Canonical ontology and style-route docs/registries | Style-route-specific composer/critic after extraction packet | CAC source-grounded ambient cinema constraints | CAC route production specs from `VideoExtractionPacket` or `SuperVisualExtractionPacket` | Do not invent cinematic metaphors without source/reference input |
| GMG Composer / Analyst | Canonical ontology and style-route docs/registries | GMG route composer/critic after extraction packet | One primary style route per provider job, route fit checks | GMG route production specs after primitive/archetype fit | Do not average GMG experts |

## Coexistence Contract

1. `NarrativeStoryDoctorService` is added under `src/ccp_studio` because Contract Convergence has frozen canonical paths there and the live repo has no `src/ccp` runtime namespace.
2. Existing `ExtractionService` remains the source-backed expression candidate service. The new V1 service is a deterministic compiler scaffold that can later call or wrap it.
3. Existing visual-preproduction, style-route, provider, SuperVisual, and Carousel systems remain independent backends. They should consume extraction packets later; they should not be rewritten here.
4. The legacy CMF reference code is preserved as source material for adapters. It is not imported directly in this branch because its paths, schemas, and runtime assumptions are not canonical V1 `ccp_studio` contracts.

## Adapter Backlog

1. Build `LegacyHunterAdapter` around current `ExtractionService`.
2. Build `BeatClusterAdapter` from reference beat clusters to `TranscriptBeatMap` and `NarrativeCluster`.
3. Build `VisualResearchAdapter` from extraction packets to Visual Preproduction input objects.
4. Build `StoryboardComposerAdapter` from engine packets to storyboard ingredient and beat visual plans.
5. Build `StyleRouteExtractionAdapter` for CAC, GMG, Paper-Cut, Documentary Proof, and UI Reaction Surface route production specs.
6. Build `ExtractionCommanderWorkflowAdapter` to bind authorization into durable runtime state.

## Explicit Non-Goals For This Branch

- No UI.
- No API endpoints.
- No real DSPy execution.
- No real provider execution.
- No database migrations.
- No direct SuperVisual, Carousel, or Video service refactor.
- No deletion of current extraction services or legacy reference files.
