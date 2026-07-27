# CMF Video Editing Engine MCDA Synthesis

Date: 2026-06-24
Status: audit-synthesis
Question: Does `THE CMF STUDIO/deep-research-report.md` define the right production video editing engine for CMF, how does it compare to current CMF specs and runtime code, and what is missing before the engine is truly build-ready?

## 1. Executive Verdict

The deep research report is architecturally strong and should be treated as the integration target for the CMF video editing engine. Its strongest contribution is not a tool recommendation. Its strongest contribution is the missing compiler abstraction:

```text
Interview-first source context
-> VideoEditProgram
-> deterministic render contract
-> OTIO audit/interchange artifact
-> eval gates
-> operator approval
-> final render and receipts
```

Current CMF specs already cover many required sub-systems: four canonical video formats, transcript beat maps, composition JSON, Brand Genesis binding, reaction templates, PaperCut animation, deterministic rendering, sonic timeline, provider operations, eval receipts, and operator review. However, those specs remain fragmented. They do not yet define one canonical `VideoEditProgram` as the master compile object that binds all sub-workflows into a frame-accurate, source-faithful video edit.

Current runtime code has useful foundations, but it does not yet implement the full engine. It has `SceneSpec`, `RenderContract`, `ReactionTemplateRoute`, deterministic renderer services, assembly/sonic timeline services, provider registries, and approval gates. It does not yet have a canonical `VideoEditProgram`, OTIO audit export, transcript-clocked full edit compiler, or unified four-format video render workflow.

Highest-confidence conclusion:

```text
The report is the right integration blueprint.
The specs are mostly aligned but not unified.
The runtime code is partial and cannot yet deliver the full CMF video editing engine.
```

## 2. Sources Compared

| Source | Role In Comparison |
|---|---|
| `THE CMF STUDIO/deep-research-report.md` | Target architecture for the video editing engine. Defines `VideoEditProgram`, transcript-clocked editing, Remotion spine, Motion Canvas/Manim sub-engines, FFmpeg finishing, OTIO audit artifact, four format grammars, eval gates, and operator approval. |
| `THE CMF STUDIO/docs/architecture.md` | Canonical CMF architecture context: Python-first harness, Command Bus, durable workflows, registries, receipts, PWA/Telegram review, provider boundaries. |
| `TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Canonical four-video output set and doctrine crosswalk. |
| `TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime binding to transcript timing, Brand Genesis, open-source mechanics, route feel, primitive triads, and approval blockers. |
| `TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md` | Transcript beat map and semantic cue compiler. |
| `TS-CMF-086-papercut-rig-layer-motion-and-sfx-runtime.md` | PaperCut rig/layer/motion/SFX runtime, primitive triad, doctrine gates. |
| `TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` | Reaction clip renderer, upper/lower zone composition, background removal, beat sync, receipts. |
| `TS-CMF-071` through `TS-CMF-075` | Reaction editing template routing, scene template binding, composition JSON registry, reaction renderer, operator composition approval. |
| `TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine-driven tests and primitive eval coverage. |
| `TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md` | Visual-feel separation and primitive gates. |
| `TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Deterministic render contract around Remotion and Motion Canvas. |
| `TS-CMF-047-audio-caption-timeline-and-mix-assembly.md` | Audio, captions, timeline, and mix assembly. |
| `TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Generative asset factory, Qwen/SAM3/layer extraction, repair queue. |
| `TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Renderer prop compiler and component harness. |
| `TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval fixtures and operator workbench. |
| `TS-CMF-093-animation-studio-migration-and-operator-rig-editor.md` | Animation Studio migration and rig editor. |
| `TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md` | Headless 2D frame renderer and avatar export worker. |
| `src/ccp_studio/contracts/scene_spec.py` | Current runtime `SceneSpec` and `RenderContract` authority. |
| `src/ccp_studio/services/scene_spec_compiler.py` | Current scene and render contract compiler. |
| `src/ccp_studio/contracts/reaction_editing.py` | Current reaction template registry and route receipt contracts. |
| `src/ccp_studio/services/reaction_editing_service.py` | Current reaction template route planning service. |
| `src/ccp_studio/contracts/deterministic_rendering.py` | Current deterministic rendering contracts. |
| `src/ccp_studio/services/deterministic_rendering_service.py` | Current deterministic renderer execution service. |
| `src/ccp_studio/contracts/sonic_timeline.py` | Current sonic timeline, audio, caption, and review read model contracts. |
| `src/ccp_studio/services/sonic_timeline_service.py` | Current sonic timeline service. |

## 3. Alternatives Scored

| Alternative | Meaning |
|---|---|
| A1 Deep Research Target | The engine architecture proposed by `deep-research-report.md`. |
| A2 Current CMF Specs | The current documented CMF spec chain around video formats, composition, timing, render, eval, and approval. |
| A3 Current CMF Runtime Code | What is currently implemented in `THE CMF STUDIO/src/ccp_studio`. |

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

## 4. MCDA Criteria

| ID | Criterion | Weight | Why It Matters |
|---|---:|---:|---|
| C1 | Canonical structured input envelope | 9 | The engine must compile from Brand Context, Interview Brief, Interview Asset Contract, Transcript Beat Map, Expression Moments, Voice/Visual DNA, Primitive Evaluations, Doctrines, Asset Package Spec, Scene Templates, and Format Targets, not loose prompts. |
| C2 | Single integrated `VideoEditProgram` contract | 10 | CMF needs one master edit-program object that binds format, beats, scenes, layers, captions, audio, providers, evals, approvals, and receipts. |
| C3 | Transcript-clocked timing and beat alignment | 10 | CMF is interview-first. Edits must follow guest/interviewer meaning beats, source timestamps, pauses, reactions, and expression anchors. |
| C4 | Four format-specific composition grammars | 10 | Cinematic Story Commentary, Educational/Explainer, Challenger/Frame Breaker, and Reaction/Recognition cannot share one generic visual language. |
| C5 | Living/Conscious reaction compositing and background removal | 8 | Reaction formats require upper/lower composition, human proof, SAM3/background removal, safe zones, and beat-synced mechanics. |
| C6 | PaperCut/2D animation and explainer runtime | 8 | Educational/Explainer requires material layer logic, rig states, PaperCut motion, avatar states, diagrams, annotation, SFX, and primitive validation. |
| C7 | Deterministic render spine and frame-accurate output | 10 | Final output needs a reliable render spine using Remotion, Motion Canvas/Manim only where fit, and FFmpeg for finishing. |
| C8 | OTIO/audit interchange and reconstructability | 7 | Operators and future audits need an editorial manifest with media refs, beat IDs, source anchors, metadata namespaces, approvals, and diffability. |
| C9 | Provider role boundaries and deterministic/generative split | 8 | GPT Image 2, FLUX, Qwen layered, SAM3, ComfyUI, Remotion, Motion Canvas, Manim, FFmpeg, and OTIO must have bounded roles. |
| C10 | Eval gates, primitive/doctrine compliance, and approval blockers | 8 | Outputs must satisfy primitives, doctrines, source fidelity, layout safety, voice/identity safety, and operator approval before final export. |
| C11 | Operator review UI and evidence read model | 6 | The operator must inspect source, route, composition, preview, eval failures, approvals, and repair paths without confusing guests or assets. |
| C12 | Implementation readiness and operational risk control | 6 | Build readiness requires contracts, workflow retries, worker boundaries, cost controls, asset hashes, fixture coverage, and clear failure modes. |

Total weight: 100.

## 5. Score Matrix

| Criterion | Weight | A1 Deep Research Target | A2 Current CMF Specs | A3 Current Runtime Code |
|---|---:|---:|---:|---:|
| C1 Canonical structured input envelope | 9 | 4.5 | 4.5 | 3.0 |
| C2 Single integrated `VideoEditProgram` contract | 10 | 5.0 | 3.0 | 1.5 |
| C3 Transcript-clocked timing and beat alignment | 10 | 5.0 | 4.5 | 2.5 |
| C4 Four format-specific composition grammars | 10 | 4.5 | 5.0 | 1.5 |
| C5 Living/Conscious reaction compositing and background removal | 8 | 4.5 | 4.5 | 2.0 |
| C6 PaperCut/2D animation and explainer runtime | 8 | 4.5 | 4.5 | 2.0 |
| C7 Deterministic render spine and frame-accurate output | 10 | 5.0 | 4.0 | 3.0 |
| C8 OTIO/audit interchange and reconstructability | 7 | 5.0 | 2.5 | 0.5 |
| C9 Provider role boundaries and deterministic/generative split | 8 | 4.5 | 4.0 | 2.5 |
| C10 Eval gates, primitive/doctrine compliance, approval blockers | 8 | 4.0 | 4.5 | 2.5 |
| C11 Operator review UI and evidence read model | 6 | 3.5 | 4.0 | 2.5 |
| C12 Implementation readiness and operational risk control | 6 | 3.5 | 3.5 | 2.5 |

## 6. Weighted Results

| Alternative | Weighted Score / 100 | Interpretation |
|---|---:|---|
| A1 Deep Research Target | 90.5 | Strongest integrated target. It defines the right compiler shape, render spine, timing model, audit artifact, and approval workflow. |
| A2 Current CMF Specs | 81.6 | Strongly aligned but fragmented. Most parts exist as specs, but no single master video edit compiler binds them end to end. |
| A3 Current CMF Runtime Code | 43.5 | Useful partial foundation. Scene/render, reaction routing, deterministic rendering, sonic timeline, approval, and provider shells exist, but the full video editing engine is not implemented. |

## 7. Evidence-Based Findings

### Finding 1: The Report Correctly Frames The Engine As A Compiler

The report's central claim is correct:

```text
The engine is not an AI editor.
It is a compiler for interview-derived video composition.
```

That maps directly to CMF doctrine. The guest interview, research, Brand Context, Expression Moments, transcript beat map, primitives, and asset package must define meaning before any timeline is rendered.

The report also correctly says the compiler should produce two outputs:

| Output | Why It Matters |
|---|---|
| Domain-native render contract | Gives Python harness and render workers a CMF-native object with route, beats, scenes, captions, layers, provider jobs, eval gates, and approvals. |
| OTIO audit/interchange artifact | Gives operators, downstream tools, and future audits a standard editorial map with clips, tracks, transitions, markers, source anchors, and namespaced metadata. |

This is the biggest gap in current CMF: we have scene/render objects, but not one master `VideoEditProgram`.

### Finding 2: Current Specs Already Carry The Right Doctrine And Format Logic

Current specs are not empty. They already encode important CMF truth:

| Capability | Current Spec Coverage |
|---|---|
| Canonical four-video output set | TS-CMF-078 defines Cinematic Story Commentary, Educational/Explainer, Challenger/Frame Breaker, and Reaction/Recognition Clip. |
| Doctrine crosswalk | TS-CMF-078 maps formats to doctrine coverage, source-backed routing, eval receipts, and operator approval. |
| Composition JSON and Brand Genesis binding | TS-CMF-080 binds templates to Brand Context, transcript timing, route feel, source lineage, and primitive triads. |
| Transcript beat maps | TS-CMF-084 defines composition beats, cue manifests, transcript timestamps, frame ranges, and primitive references. |
| PaperCut runtime | TS-CMF-086 defines layer depth, rig states, motion jobs, SFX cues, tactile materiality, and primitive triad gates. |
| Reaction composition | TS-CMF-071 through TS-CMF-074 define reaction templates, upper/lower zone logic, background removal, beat sync, and render receipts. |
| Eval and approval | TS-CMF-077, TS-CMF-079, TS-CMF-092 define doctrine tests, route feel gates, primitive coverage, and operator approval blockers. |
| Renderer pipeline | TS-CMF-043, TS-CMF-047, TS-CMF-090 define deterministic rendering, captions/audio/timeline, and renderer prop compilation. |

The issue is integration. The specs define strong organs, but the video engine still needs a spine.

### Finding 3: Current Runtime Code Confirms A Partial Foundation, Not A Full Engine

Runtime evidence shows the same split:

| Runtime Area | Current State |
|---|---|
| `SceneSpec` and `RenderContract` | Present in `contracts/scene_spec.py` and compiled by `services/scene_spec_compiler.py`. Useful scene-level foundation. |
| Reaction template routing | Present in `contracts/reaction_editing.py` and `services/reaction_editing_service.py`, including versus, tier list, blind ranking, elimination, mirror quiz, authority ladder, and related route receipts. |
| Deterministic rendering | Present in `contracts/deterministic_rendering.py` and `services/deterministic_rendering_service.py`, mostly as render-contract execution rather than full edit-program compilation. |
| Sonic timeline | Present in `contracts/sonic_timeline.py` and `services/sonic_timeline_service.py`, covering audio, captions, timeline manifests, ducking, synthetic voice policy checks, and review read model. |
| Approval gates | Present via approval gate contracts and services. |
| Provider shell | Present through provider job and provider operation services. |
| `VideoEditProgram` | Missing as a canonical contract. |
| OTIO export/audit | Missing as an explicit contract/service. |
| Transcript-clocked full edit compiler | Missing as one integrated workflow. |
| Four-format render workflow | Missing as one unified compile-to-render lifecycle. |

Therefore, current runtime is not production-complete for the full CMF video editing system.

### Finding 4: The Report Is Stronger Than Current Specs On OTIO And Integrated Runtime Shape

The report is ahead of current specs on:

- `VideoEditProgram` as a named master object;
- OTIO as audit/interchange artifact;
- metadata namespaces for brand, interview, primitive eval, source provenance, and approval;
- a clear split between deterministic final rendering and generative asset contribution;
- role placement of React video editor tooling as operator UI, not source of truth;
- Remotion as master spine with Motion Canvas/Manim as sub-scene engines;
- frame-perfect video extraction, safe-zone, audio finishing, and final encode framing.

Current CMF specs imply several of these, but they do not yet force them through one object and one workflow.

### Finding 5: The Report Is Weaker Than CMF Specs On Internal Doctrine Specificity

The report is strong architecturally, but it is less CMF-specific than our specs in several places:

| Area | Report Limitation | CMF Requirement |
|---|---|---|
| Nine doctrines | Mentions doctrines generally, but does not deeply encode CMF's exact doctrine crosswalk. | TS-CMF-078 and TS-CMF-077 must remain governing sources. |
| Primitive triads | Mentions primitive evaluations, but does not define exact primitive role coverage. | Every composition target must validate at least three primitives across meaning, delivery, and material/format roles. |
| Interview-first lineage | Strong conceptually, but should be bound to CMF objects. | Must bind Interview Brief, Interview Asset Contract, Expression Moments, Route Candidate, Brand Context, and source provenance. |
| Agent/harness ownership | Does not fully map to Pi harness departments, agents, sub-agents, hooks, skills, and command handlers. | Video engine must run through CMF command/workflow contracts, not isolated render scripts. |
| Guest workspace boundaries | Implied, not foregrounded. | Every artifact must stay scoped to organization, brand, guest, source, and asset package. |
| Composition JSON registry | Implied via templates, but not CMF-specific enough. | Composition families and assets need registry codes, versioning, approval state, and content asset codes. |

So the report should be adopted as architecture shape, not as a replacement for CMF doctrine.

## 8. Capability Gap Table

| Capability | Deep Research Report | Current CMF Specs | Current Runtime Code | Gap |
|---|---|---|---|---|
| `VideoEditProgram` | Explicit, central | Implied through `SceneSpec`, `RenderContract`, `FourVideoFormatPlan`, composition runtime binding | Missing | Add canonical contract and compiler. |
| `CreateVideoEditProgramRequest` | Implied by structured inputs | Partial across editing session, asset package, beat map, scene specs | Missing | Add request object with all required IDs and policy refs. |
| Canonical structured input envelope | Strong | Strong but distributed | Partial | One request must bind Brand Context, Interview Brief, IAC, Expression Moments, beat maps, primitives, doctrines, assets, format targets. |
| Transcript-clocked edit timing | Strong | Strong in TS-CMF-084 and TS-CMF-080 | Partial timeline/caption support exists, but no full transcript-clocked edit compiler | Implement full beat-to-scene-to-frame compiler. |
| Four format-specific grammars | Strong | Strong in TS-CMF-078, TS-CMF-079, TS-CMF-080 | Mostly missing at render-program level | Add format-specific composition contracts and validators. |
| Cinematic Story Commentary | Strong | Good in TS-CMF-078/080/084 | Scene/render foundations only | Add cinematic composition grammar and evals. |
| Educational/Explainer | Strong | Strong in TS-CMF-086/093/094 | Partial/missing runtime execution | Implement PaperCut/2D explainer program binding. |
| Challenger/Frame Breaker | Strong around Conscious Reactions | Good in TS-CMF-078/071/080 | Reaction routing exists; final renderer workflow missing | Bind debate/ranking/poll mechanics to VideoEditProgram. |
| Reaction/Recognition Clip | Strong | Strong in TS-CMF-071 through 074 | Route registry exists; full compositing/render workflow incomplete | Implement upper/lower reaction composition render path. |
| Background removal / SAM3 masks | Strong | Strong in TS-CMF-074/089/095 | Provider shell likely only | Add tracked subject layer contracts and preview checks. |
| PaperCut materiality and rig | Good | Very strong in TS-CMF-086/093/094 | Not fully implemented | Add runtime rig manifest compiler and renderer worker. |
| Remotion master spine | Strong | Strong in TS-CMF-043/074/080/090 | Partial deterministic renderer | Upgrade from scene render to full program render. |
| Motion Canvas sub-engine | Strongly bounded | Strong | Partial route references | Treat as alpha/image-sequence subscene worker, not master truth. |
| Manim sub-engine | Strongly bounded | Present in TS-CMF-080 | Not visible as runtime path | Add only for procedural diagrams/math-like explainers. |
| FFmpeg finishing | Strong | Strong in TS-CMF-047 | Partial sonic/audio manifests; final encode pipeline not enough | Add final media finishing service bound to edit program. |
| OTIO audit/interchange | Strong, explicit | Weak/mostly missing | Missing | Add OTIO manifest contract, exporter, metadata namespace policy. |
| React video editor role | Correctly scoped as UI shell | TS-CMF-080 references it as not source of truth | UI not fully built | Use for operator review/timeline interaction only. |
| Eval gates | Good | Strong | Partial eval/approval foundations | Bind evals as hard gates on `VideoEditProgram`. |
| Operator approval | Good | Strong | Partial review and approval services | Add edit-program review read model and approval blockers. |
| Reconstructability | Strong via OTIO + hashes | Partial via receipts/hashes | Partial receipts, no OTIO | Add source-to-render reconstructability receipt. |

## 9. Technology Role Fit Matrix

| Component | Report Role | CMF Fit | Decision |
|---|---|---|---|
| Remotion | Master render spine, JSON input props, timeline primitives, server-side render | Excellent fit for deterministic timeline and composition execution | Adopt as primary video render spine. |
| Motion Canvas | Specialist 2D subscene engine for authored motion and camera-like panel choreography | Good fit for PaperCut/diagram subscenes when Remotion components are not enough | Use as subscene worker, not master timeline. |
| Manim | Precise procedural animation, diagrams, math-like scenes | Good but narrow fit | Use only for symbolic/procedural explainers. |
| FFmpeg | Final media plumbing, overlays, loudness, ducking, concat, encode | Mandatory fit | Keep as final finishing and validation layer. |
| OTIO | Audit/interchange artifact, not live runtime | Excellent missing fit | Add as required audit artifact. |
| React video editor / OpenVideo | Operator UI shell and timeline preview | Useful only as UI reference/adaptable shell | Do not let it become source of truth. |
| SAM3 | Tracked masks, subject separation, background removal | Strong fit for reaction/living commentary and visual asset prep | Use for mask/layer worker. |
| Qwen-Image-Layered | Layer extraction/decomposition for generated or composed visuals | Strong fit for editable layered assets | Use upstream of renderer, not as final compositor. |
| GPT Image 2 / FLUX 2 Klein 9B | Asset generation, edits, plates, metaphor objects | Good fit when doctrine permits generated assets | Bound by source fidelity, identity safety, and operator approval. |
| ComfyUI Docker GPU worker | Orchestrated self-hosted image/video generation pipelines | Good fit for provider execution on 24GB/32GB VRAM GPU | Worker only; not final truth source. |
| Rough Notation | Animated emphasis and annotation language | Strong for explainers, reactions, and callout emphasis | Register as deterministic annotation cue manifest. |

## 10. Per-Criterion Analysis

### C1: Canonical Structured Input Envelope

A1 scores 4.5 because it names the right inputs: `BrandContext`, `InterviewBrief`, `InterviewAssetContract`, `TranscriptBeatMap`, `ExpressionMoments`, `VoiceVisualDNA`, `PrimitiveEvaluations`, `Doctrines`, `AssetPackageSpec`, `SceneTemplates`, and `FormatTargets`.

A2 scores 4.5 because current specs include these ideas across multiple specs, but not in one explicit request object.

A3 scores 3.0 because runtime code has many adjacent contracts, but no canonical video edit request envelope.

Required repair:

```text
CreateVideoEditProgramRequest
```

must become a Pydantic contract.

### C2: Single Integrated `VideoEditProgram` Contract

A1 scores 5.0 because this is the report's central idea.

A2 scores 3.0 because current specs have `FourVideoFormatPlan`, `SceneSpec`, `RenderContract`, `CompositionRuntimeBinding`, beat maps, and receipts, but no master edit program.

A3 scores 1.5 because code has scene/render-level objects, but no edit-program authority.

Required repair:

```text
VideoEditProgram
VideoEditScene
VideoEditTrack
VideoEditLayer
VideoEditBeatBinding
VideoEditProgramReceipt
```

### C3: Transcript-Clocked Timing And Beat Alignment

A1 scores 5.0 because it clearly rejects generic timeline editing and centers transcript-clocked beat windows.

A2 scores 4.5 because TS-CMF-084 and TS-CMF-080 already specify beat maps, transcript-to-frame mapping, semantic beat roles, cues, captions, SFX, and primitive refs.

A3 scores 2.5 because sonic timeline and assembly services exist, but the full transcript-to-edit-program compiler is not implemented.

Required repair:

```text
TranscriptClock
TranscriptBeatMapRef
TimelineCuePlan
BeatToSceneBinding
```

inside the video edit program.

### C4: Four Format-Specific Composition Grammars

A1 scores 4.5 because it distinguishes cinematic, educational/explainer, living commentary, and conscious reactions with different visual languages.

A2 scores 5.0 because CMF specs define the canonical four-video set and explicitly block same-feel flattening.

A3 scores 1.5 because runtime code has reaction route templates, but not a full four-format render grammar.

Required repair:

```text
FormatCompositionContract
SV-CSC grammar
SV-EDU grammar
SV-FRB grammar
SV-RRC grammar
```

### C5: Living/Conscious Reaction Compositing And Background Removal

A1 scores 4.5 because it defines human proof, reaction latency, SAM3 masks, upper/lower balance, safe zones, and deterministic UI mechanics.

A2 scores 4.5 because TS-CMF-071 through TS-CMF-074 and TS-CMF-080 cover this well.

A3 scores 2.0 because reaction template routing exists, but full masked render/composition execution is incomplete.

Required repair:

```text
TrackedSubjectLayer
ReactionUpperZonePlan
ReactionLowerHumanLayerPlan
ReactionLatencyEval
```

### C6: PaperCut/2D Animation And Explainer Runtime

A1 scores 4.5 because it correctly separates educational/explainer from cinematic and names Motion Canvas/Manim as sub-engines.

A2 scores 4.5 because TS-CMF-086, TS-CMF-093, and TS-CMF-094 deeply specify PaperCut, rigs, animation studio migration, and headless rendering.

A3 scores 2.0 because the old/new runtime bridge is not fully implemented.

Required repair:

```text
PaperCutSceneBinding
RigPerformanceStateBinding
PaperMaterialityCue
ExplainerSubsceneArtifact
```

### C7: Deterministic Render Spine And Frame-Accurate Output

A1 scores 5.0 because it correctly picks Remotion as master spine and FFmpeg as final finishing layer.

A2 scores 4.0 because the specs already name these components but still need one binding spec.

A3 scores 3.0 because deterministic render services exist, but operate below full edit-program orchestration.

Required repair:

```text
VideoRenderContract
FrameRangePlan
RenderWorkerJob
FinalMediaEncodeManifest
```

### C8: OTIO/Audit Interchange And Reconstructability

A1 scores 5.0 because it explicitly requires OTIO and metadata namespaces.

A2 scores 2.5 because current specs have receipts, hashes, and lineage, but not a strong OTIO artifact.

A3 scores 0.5 because no explicit OTIO contract/service was found.

Required repair:

```text
OTIOAuditManifest
OTIOMetadataNamespacePolicy
ExportVideoEditProgramToOTIOCommand
```

This is the biggest concrete missing piece from current CMF specs/code.

### C9: Provider Role Boundaries And Deterministic/Generative Split

A1 scores 4.5 because it sharply separates deterministic final truth from generative asset creation.

A2 scores 4.0 because CMF specs repeatedly enforce provider boundaries, but the video-specific split needs one canonical contract.

A3 scores 2.5 because provider operations exist, but the full worker orchestration and boundary enforcement are partial.

Required repair:

```text
ProviderRoleAssignment
GenerativeAssetPermission
DeterministicRenderObligation
ProviderJobPlan
```

### C10: Eval Gates, Primitive/Doctrine Compliance, Approval Blockers

A1 scores 4.0 because it defines hard gates but does not fully encode CMF primitive/doctrine specificity.

A2 scores 4.5 because TS-CMF-077, TS-CMF-079, TS-CMF-080, TS-CMF-084, and TS-CMF-086 are strong.

A3 scores 2.5 because eval/approval services exist, but are not bound to a full video edit program.

Required repair:

```text
VideoEditEvalGateSet
PrimitiveTriadCoverageReport
DoctrineVideoFormatEvalReceipt
VideoEditApprovalBlocker
```

### C11: Operator Review UI And Evidence Read Model

A1 scores 3.5 because it names operator review but does not deeply specify the CMF operator workbench.

A2 scores 4.0 because CMF specs repeatedly define PWA/Telegram/read-model expectations.

A3 scores 2.5 because review/approval services exist, but no full video edit program review surface exists.

Required repair:

```text
VideoEditProgramReviewReadModel
TimelineEvidencePanel
FormatSlotEvidencePanel
OperatorRepairAction
```

### C12: Implementation Readiness And Operational Risk Control

A1 scores 3.5 because the report is technically strong, but still a research report, not an implementation spec.

A2 scores 3.5 because current specs are detailed but fragmented.

A3 scores 2.5 because foundations exist, but integration and execution are incomplete.

Required repair:

```text
Workflow retry/resume/cancel semantics
artifact hash policy
fixture/golden render suite
provider cost and cache policy
worker boundary policy
```

## 11. Required Binding Spec

The next spec should be:

```text
TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md
```

Purpose:

```text
Bind the video editing report, current CMF specs, and current runtime foundations into one canonical edit-program compiler and render workflow.
```

It must define:

| Object | Purpose |
|---|---|
| `CreateVideoEditProgramRequest` | Canonical command input for a video edit compile. |
| `VideoEditProgram` | Master edit program. |
| `VideoEditProgramScene` | Scene-level units with source, format, layer, timing, and render bindings. |
| `TranscriptClock` | Source transcript timing authority. |
| `BeatToSceneBinding` | Mapping from semantic transcript beat to scene actions, captions, SFX, UI states, and motion. |
| `FormatCompositionContract` | Format-specific grammar and route constraints. |
| `VideoLayerManifest` | Human, generated, graphic, caption, background, annotation, and UI layers. |
| `TrackedSubjectLayerManifest` | SAM3/background-removal subject layers. |
| `PaperCutSubsceneManifest` | PaperCut rig/layer/motion/SFX output for explainer routes. |
| `CaptionLayoutPlan` | Caption timing, safe zones, line groups, emphasis, and collision tests. |
| `AudioMixPlan` | Source voice, interviewer voice, SFX, music, ducking, loudness, and final mix. |
| `ProviderJobPlan` | Bounded generative/deterministic worker jobs. |
| `VideoRenderContract` | Remotion/Motion Canvas/Manim/FFmpeg render route and worker props. |
| `OTIOAuditManifest` | Editorial interchange artifact with source anchors and metadata namespaces. |
| `VideoEditEvalGateSet` | Required evals and blockers. |
| `VideoEditProgramReceipt` | Final source-to-render receipt. |
| `VideoEditProgramReviewReadModel` | Operator review surface model. |

## 12. Required Workflow

The binding workflow should be:

```text
CreateVideoEditProgramRequest
-> validate brand/workspace/source scope
-> load Interview Brief / Interview Asset Contract / Expression Moments
-> load TranscriptBeatMap and source provenance
-> select canonical video format slot and route
-> compile FormatCompositionContract
-> compile VideoEditProgram
-> compile ProviderJobPlan
-> generate or attach assets
-> normalize layer manifests and tracked subject layers
-> compile captions, audio, motion, annotations, and render props
-> render proxy preview
-> run doctrine, primitive, source, layout, face, caption, audio, and format evals
-> emit blockers if failed
-> operator review / repair / approve
-> lock VideoEditProgram
-> render final master
-> export OTIOAuditManifest
-> emit VideoEditProgramReceipt
```

Hard gates:

| Gate | Blocker Code |
|---|---|
| Missing source transcript anchors | `VIDEO_EDIT_SOURCE_TIMING_MISSING` |
| Missing Brand Context or guest scope | `VIDEO_EDIT_BRAND_SCOPE_MISSING` |
| Unsupported four-format route | `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED` |
| Format grammar collapse | `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE` |
| Primitive triad missing | `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED` |
| Doctrine eval missing | `VIDEO_EDIT_DOCTRINE_EVAL_MISSING` |
| Human mask unsafe | `VIDEO_EDIT_SUBJECT_MASK_UNSAFE` |
| Caption collision or unsafe platform zone | `VIDEO_EDIT_CAPTION_LAYOUT_FAILED` |
| Synthetic/generated asset source drift | `VIDEO_EDIT_GENERATED_ASSET_SOURCE_DRIFT` |
| Audio mix hides source voice | `VIDEO_EDIT_AUDIO_SOURCE_INTELLIGIBILITY_FAILED` |
| OTIO export missing | `VIDEO_EDIT_OTIO_AUDIT_MISSING` |
| Operator approval missing | `VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED` |

## 13. Recommended Priority

| Priority | Action | Why |
|---:|---|---|
| 1 | Write `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md`. | This binds the report to CMF specs and prevents another fragmented implementation. |
| 2 | Add Python contracts for `CreateVideoEditProgramRequest`, `VideoEditProgram`, `VideoEditProgramReceipt`, and `OTIOAuditManifest`. | Runtime cannot execute a report or scattered specs. |
| 3 | Add `video_edit_program_service.py`. | This becomes the compiler service that calls existing scene, reaction, beat, asset, sonic, render, eval, and approval services. |
| 4 | Add `otio_export_service.py`. | Reconstructability and downstream audit require a standard interchange artifact. |
| 5 | Add four format grammar registries. | Prevents same-feel slop across Cinematic, Explainer, Frame Breaker, and Reaction formats. |
| 6 | Add render worker plan and proxy/final render receipts. | Separates preview from final master and preserves hashes. |
| 7 | Add golden fixtures for all four video formats. | Proves the system respects CMF standards visually and structurally. |
| 8 | Add operator review read model for edit programs. | Makes approvals inspectable instead of blind. |
| 9 | Add CI/eval tests that block missing primitive/doctrine/source/OTIO coverage. | Prevents future shortcuts from passing as complete work. |

## 14. Final Synthesis

The deep research report should be accepted, but in a precise way:

```text
Accept the report as the video editing engine integration blueprint.
Do not treat it as a replacement for CMF doctrines, primitives, registries, or specs.
Use it to create the missing VideoEditProgram binding spec and runtime.
```

The correct next move is not to build directly from the report and not to keep patching isolated specs. The correct next move is:

```text
TS-CMF-106 -> Python contracts -> compiler service -> OTIO exporter -> four-format fixtures -> operator review/eval gates -> final render path.
```

That gives CMF the thing it is currently missing: one accountable, interview-first, source-backed, doctrine-validated video editing engine that can actually compile and render the four canonical video formats.
