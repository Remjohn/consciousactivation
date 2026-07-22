# CMF / CCP Studio Engine Build Handoff: What Has Been Built, What Is Ready, and What Comes Next

## 1. Purpose of this handoff

This document is a continuation handoff for CMF / CCP Studio. It is meant to be given to the next chat, along with the codebase, so the next session can continue building without needing to reconstruct the prior conversation. The recent work produced many bundles, integration prompts, backend contracts, services, registries, tests, and operator UI wiring plans. The important next step is not to keep adding random modules. The next step is to understand the current engine state, verify what was actually integrated in the repository, and then move deliberately toward format parity and real operator execution.

The short version is this: CMF Studio is now structurally much stronger, but it is not yet a fully production-ready studio engine. It has a strong typed backend spine, strong documentation, strong governance concepts, and an increasingly complete Format 02 vertical slice. It also has safe abstractions for provider jobs, local render jobs, Remotion/FFmpeg rendering, render QA, workspace artifacts, and pipeline recipes. However, most real execution remains fake, dry-run, or gated. The operator UI is being wired, but may still be partial depending on which prompts have been implemented in the actual codebase. Format 02 has received the most implementation attention. Formats 01, 03, and 04 still need dedicated format engines, composition packs, timeline logic, render QA promise profiles, recipes, and UI surfaces.

The good news is that the project is no longer a loose idea. The docs folder should now contain a substantial architecture trail. The next chat should inspect those docs, run tests, build a readiness matrix, and then continue with missing format engines and operator workflows.

## 2. The core doctrine we are building around

The studio is interview-first and primitive-first. It is not a prompt generator, not a Canva clone, not a one-off image tool, and not simply a video editor. It is a production system that turns human/source truth into brand-aligned media assets through a traceable pipeline. The doctrine is: every asset begins with human or source truth, is interpreted through primitives, grounded by research, shaped by sequencing, prepared through visual schema and composition reasoning, routed through style skills, rendered deterministically, evaluated through receipts, approved by an operator, and remembered through performance.

The contract hierarchy that guided the work so far is:

Doctrine Contract → Primitive Coalition Contract → Archetype Contract → Sequence Contract → Asset Research Contract → Composition Contract → Render Contract → Evaluation Contract.

This matters because it prevents the engine from becoming a bag of unrelated AI calls. The engine should know why a scene exists, what primitive it expresses, what source refs justify it, what format it belongs to, what composition constraints apply, what provider outputs were created, what render job produced the final asset, what QA receipts passed, and what approval event allowed export. Taste is not treated as vague style preference. Taste is encoded as primitive-fit decision-making.

This is also why the system has been built around receipts. ProviderJobReceipt, RenderJobResult, RenderQACompositeReport, PipelineStepReceipt, ApprovalGate, ArtifactRef, and EvaluationReceipt are not paperwork. They are the evidence chain. They let an operator know what happened, what failed, what can be retried, what can be approved, and what should be remembered.

## 3. What has been built so far

The first major group of work strengthened upstream and midstream intelligence. Narrative Story Doctor / Extraction Intelligence compiles source material into meaning. Format Intelligence turns meaning into format realization. The Narrative-to-Format Bridge connects extracted narrative material to format programs. SuperVisual and Carousel adapters began converting expression moments into image and carousel asset programs. Format Engine Draft Wiring made those pieces easier to connect. Composition Intelligence Core and the Format 02 Pack created the first strong composition rules for a real format. Avatar Performance Layer V1 defined what the avatar does: expression plate selection, body pose, gesture, audience proxy, performance function, and the no-lip-sync behavior law.

The Format 02 Golden Path Orchestrator then proved the first serious vertical slice. It connected a health myth fixture through Narrative Story Doctor, Narrative-to-Format Bridge, Format Intelligence, Format 02 composition, Avatar Performance, Video Editing Engine, Remotion input props, OTIO audit, fake proxy render, evaluation, final lock, fake final render, approval, and export pack. Capability Preflight + Provider Menu V1 added a crucial safety layer. Before the studio runs a provider job, render job, avatar library batch, or real rendering pipeline, the operator should know what is configured, missing, degraded, or blocked. The preflight layer establishes capability status, missing blockers, setup offers, provider menu summaries, and sample-first requirements. It prevents silent failure and prevents a pipeline from pretending it is ready when a provider, runtime, or workspace requirement is missing.

Project Workspace + Artifact Store V1 created the physical storage model. It introduced client workspaces, workspace path policies, run artifact directories, ArtifactRef, ArtifactManifest, ArtifactLineage, and ArtifactReceipt. The workspace convention keeps brand files, references, avatar libraries, templates, run assets, provider outputs, renders, exports, and receipts under a deterministic folder structure. It also enforces safe paths and keeps ArtifactRef as a pointer rather than a raw binary container.

Template Preview Atlas V1 created deterministic preview read models for SuperVisual, Carousel, and Format 02 templates. It outputs SVG previews and thumbnail URIs without provider calls or render calls. This is important because operators need to evaluate layout and structure before spending provider or render resources.

Video Editing Engine V1 created the timeline and render-contract layer. It owns timing, tracks, captions, sound, render contracts, revision, and export. It does not own extraction, format intelligence, composition, visual research, or provider decisions. It includes laws such as: 16:9 source material can exist but is not final short-form output, source refs are required, final render requires approval, Format 01 uses A-roll as the story spine, Format 02 requires locked composition and no-lip-sync avatar, Format 03 requires proof/reaction logic, and Format 04 requires controlled memetic spacing. V1 still uses fake rendering.

Avatar Asset Production + Rig Export V1 filled the physical avatar gap. Avatar Performance says what the avatar does. Avatar Asset Production says how the avatar physically exists. It added AvatarCharacterSpec, PSD layer requirements, face plate approval sets, paper body layer sets, Stretchy Studio import manifests, Spine and DragonBones export manifests, avatar action timelines, Remotion avatar layer payloads, CharacterQAReport, and rig continuity receipts. The hard law is no lip sync: no phoneme keys, no viseme keys, no jaw driver, no mouth-flap clips. It is manifest-only and does not call Stretchy Studio, Spine, DragonBones, or Remotion.

Local Render Worker V1 created worker registration, capability declarations, render jobs, queues, leases, heartbeats, fake results, and worker health receipts. It supports template_preview_render, avatar_state_preview_render, proxy_video_render, final_video_render, thumbnail_render, carousel_preview_render, and supervisual_preview_render. It is still fake by default. The point was to create the worker lifecycle before turning on real render execution.

Remotion + FFmpeg Render Adapter V1.1 created gated dry-run command planning for Remotion Node.js + @remotion/skia and FFmpeg finishing. It preserves the Complete Editing Session render state wrapper, research refs, asset refs, scene specs, composition refs, provider receipts, evaluation receipts, the seven-layer composition model, allowed/banned motion vocabulary, and memetic sound moderation. Real local execution is not default. It requires explicit execution_mode=real_local, tested runtime capability, local worker lease id, and allow_subprocess_execution=true.

Provider Runtime Ideogram + Flux V1 created provider governance. Ideogram is defined as the composition plate generator. Flux is defined as the reference-based object editor. It added ProviderCapabilityProfile, ProviderJob, ProviderJobInput, ProviderJobOutput, ProviderJobReceipt, ProviderCostEstimate, ProviderDecisionLog, ProviderRetryPolicy, ProviderSampleApprovalGate, and ProviderOutputAssetRef. It enforces sample-first approval: one scene sample, one face plate sample, one template preview sample, then batch. V1 fake-executes and does not call provider APIs.

Studio Pipeline Recipe Harness V1 generalized the Golden Path into reusable recipes. It added PipelineRecipe, PipelineRun, PipelineStepRun, PipelineStepReceipt, PipelineArtifactRef, PipelineApprovalGate, PipelineRunBlocker, PipelineRunSummary, and recipe catalog services. It includes format02_golden_path, avatar_library_generation, supervisual_from_expression_moment, carousel_from_expression_moment, and format01_story_video. Its most important law is that it must reuse the existing orchestration spine and must not create a parallel harness.

Render QA V1 added operational QA receipts. It validates playability, duration, dimensions, fps, audio levels, frame samples, caption burn, visual regression screenshots, character consistency, motion promise, and delivery promise. It aligns with V9.1 rendered asset metrics: identity consistency, composition quality, style consistency, emotional accuracy, platform fit, negative space compliance, hook strength, shareability, and routeability. It does not call ffprobe, FFmpeg, Remotion, providers, subprocesses, or local workers. It compiles receipts from observations supplied later by workers/adapters.

Several UI/backend wiring prompts were also produced: connect Video Timeline Workbench to Local Render Worker, wire client workspace and reference upload UI, wire Pipeline Run Monitor UI, and audit/deprecate legacy render runtime paths. These are prompts rather than bundles because they require inspecting real routes, existing screens, fixtures, and backend router conventions.

## 4. Current readiness of CMF Studio

The studio is now strong as an architecture and backend contract system. It is not yet complete as an end-user product or fully automated media factory. A realistic readiness matrix would say:

Conceptual and doctrine readiness is high. The engine has a clear object spine and strong boundaries between extraction, format, composition, provider runtime, render runtime, QA, approval, publishing, and memory.

Backend contract readiness is high. Most major layers have contracts, services, registries, tests, and documentation. The codebase should now have enough structure for future agents to continue without rethinking the foundation.

Format 02 fake/dry-run readiness is medium-high. It has the strongest vertical path, including avatar performance, avatar physical assets, provider samples, template preview, timeline contracts, worker jobs, Remotion payloads, and render QA. Real production readiness for Format 02 is medium because actual provider calls, real image outputs, real Remotion execution, real file uploads, and complete operator approvals still require controlled wiring.

Format 01 readiness is medium-low. It has doctrine and some video editing laws, but it needs a dedicated Format 01 Story Video Engine. This format should be interview-led and A-roll-led. A-roll must remain the story spine. B-roll must have story function. There should be no filler B-roll. The engine needs A-roll beat selection, emotional arc mapping, B-roll story-function classification, quote/caption alignment, sonic contrast planning, and Format 01 render QA promises.

Format 03 readiness is low-medium. The idea is clear: living commentary reactions with proof/reaction layout, upper proof surface, lower coach or reaction layer, Rough Notation, proof legibility, and reaction timing. But it needs contracts, composition packs, timeline rules, proof-card artifact models, split-frame profiles, legibility QA, and preview links.

Format 04 readiness is low-medium. The idea is conscious reaction/ranking/debate/tier/score content with controlled memetic energy. It needs its own debate/ranking contracts, tier-board layouts, evidence refs, source tension gates, memetic cue plans, motion moderation, and platform-specific render QA.

Operator UI readiness is medium if all wiring prompts have been implemented. The UI should now be moving toward operator-first control: workspaces, references, Video Timeline Workbench render jobs, pipeline run monitor, and run details. But the UI likely still needs provider sample approval, render QA panels, format-specific workbench panels, and real execution controls.

Real execution readiness is low-medium. The architecture is ready to gate real execution safely, but the default remains fake/dry-run. That is correct. Real execution should only be enabled after provider secrets, preflight, local worker capability tests, artifact storage, render QA observation bridges, and approval UI are proven.

Overall, CMF Studio is currently best described as a well-structured production operating system with one strong format vertical slice and many shared downstream systems. It is not yet format-complete and not yet fully real-execution-ready.

## 5. The Format 02 imbalance and why it happened

The sequence focused heavily on Format 02 because Format 02 forced the hardest production infrastructure. A paper-cut avatar explainer requires avatar identity, face plates, body layers, rig manifests, expression states, no-lip-sync rules, real object cutouts, template previews, provider sample approval, scene composition, Remotion layer payloads, render worker contracts, and QA. Building Format 02 first was useful because it forced the system to solve many shared problems that other formats also need.

However, your concern is right: Format 01, Format 03, and Format 04 cannot remain only doctrine. If the studio is interview-first, Format 01 is absolutely central. It is likely the most important video format for the initial product, because the first product is the interview and Guest Asset Pack. Format 02 is powerful, but it should not define the whole studio.

The next phase should therefore be called Format Parity + Operator Execution. It should ensure that each major format has a real engine pack, recipe, UI read model, test fixture, and QA promise.

## 6. What must be built next for Format 01

Format 01 should be the A-roll-led interview story video engine. Its core law is that A-roll is the story spine. The primary material is the human voice, interview, or direct source. B-roll exists only when it performs a story function: proof, memory, contrast, breath, transition, stakes, context, or emotional landing. No filler B-roll should pass.

The next bundle should probably be:

CCP_FORMAT01_STORY_VIDEO_ENGINE_V1_INTEGRATION_BUNDLE.zip

Suggested contracts:

ArollStorySpine, ArollBeatSegment, InterviewQuoteMoment, EmotionalArcMap, StoryTurn, BrollStoryFunction, MemoryObjectCue, SonicContrastCue, CaptionAlignmentPlan, Format01TimelinePlan, Format01CompositionPlan, Format01RenderPromise, Format01QAProfile, Format01ApprovalReceipt.

Suggested tests:

A-roll source refs are required. The story spine cannot be empty. B-roll cannot be included without a story function. Every cut must map to direction, feeling, or tempo. Quote moments preserve transcript/source refs. Emotional arc must have a beginning, turn, and landing. Captions align to A-roll beats. Sonic cues cannot overpower dialogue. Format 01 render promise must validate duration, platform fit, captions, audio, and story continuity.

This will make the studio feel much more like an interview-first production engine rather than only an avatar explainer engine.

## 7. What must be built next for Format 03

Format 03 should be the Living Commentary Reactions engine. Its core structure is proof plus reaction. The proof surface may be a quote, screenshot, source clip, article snippet, chart, or claim card. The reaction layer is the coach/commentator, not the main evidence. Rough Notation timing helps direct attention. Proof legibility is a major QA requirement.

Suggested bundle:

CCP_FORMAT03_LIVING_COMMENTARY_REACTIONS_V1_INTEGRATION_BUNDLE.zip

Suggested contracts:

ProofSurface, SourceQuoteProofCard, ScreenshotProofRef, ReactionCoachLayer, RoughNotationCue, SplitReactionFrameProfile, CommentaryBeat, ProofLegibilityReceipt, ReactionBalanceReceipt, Format03TimelinePlan, Format03CompositionPlan, Format03RenderPromise, Format03QAProfile.

Suggested tests:

Proof source refs are required. Proof text must remain legible. Reaction layer cannot obscure proof. Rough Notation cues must point to valid proof regions. Split frame must obey safe areas. Reaction timing must not precede the proof it reacts to. Render QA must include proof legibility and caption safety.

## 8. What must be built next for Format 04

Format 04 should be the Conscious Reactions / Debate / Ranking / Tier / Score engine. This format can be more energetic and memetic, but it must remain evidence-bound. It should not become unsupported hot-take content. High arousal is allowed only when source tension justifies it. Memetic sound cues must remain moderated.

Suggested bundle:

CCP_FORMAT04_CONSCIOUS_REACTIONS_V1_INTEGRATION_BUNDLE.zip

Suggested contracts:

DebateFrame, RankingBoard, TierScoreCard, ClaimEvidenceRef, SourceTensionReceipt, MemeticCuePlan, ScoreJustification, ReactionPacingPlan, Format04TimelinePlan, Format04CompositionPlan, Format04RenderPromise, Format04QAProfile, MemeticModerationReceipt.

Suggested tests:

Every ranking or score requires evidence refs. Tier labels must be justified. High-arousal pacing requires source tension. Memetic cues must respect spacing. Claims cannot be unsupported. Debate frames cannot distort source meaning. Render QA must validate motion, captions, platform fit, and memetic moderation.

## 9. Shared next steps after format parity

After Format 01, 03, and 04 are built, update the Pipeline Recipe Harness. Add or strengthen recipes for format01_story_video, format03_living_commentary, and format04_conscious_reactions. Ensure each recipe maps to the existing orchestration spine, has approval gates, artifact refs, render QA steps, and pipeline monitor read models.

Then wire Provider Sample Approval UI. Provider Runtime already enforces sample-first batch gates, but an operator needs a screen to see sample outputs, cost estimates, decision logs, retries, blockers, and approval state. The provider sample approval screen is critical before real Ideogram/Flux execution.

Then wire Render QA into Video Workbench and Pipeline Run Monitor. Operators should see FFprobe validation, frame sampling, audio analysis, caption burn, visual regression, character QA, motion downgrade, delivery promise, and composite report status. A failed render should show exactly why it cannot advance.

Then enable real execution carefully. Real provider calls should only be enabled after provider capability preflight, secrets/config validation, sample approval UI, workspace storage, artifact manifests, and retry/cost governance are working. Real render execution should only be enabled after Local Render Worker health, Remotion capability, FFmpeg capability, ffprobe capability, output storage, and Render QA observation bridges are proven.

Finally, run the legacy render deprecation audit and migrate old Python/C++ Skia paths only after tests prove the Remotion Node.js + @remotion/skia path is the replacement. Do not delete blindly.

## 10. The exact first task for the next chat

The next chat should not start by building. It should first audit the actual repository state. Use this prompt:

“Here is the CMF Studio codebase and this handoff document. First inspect docs/architecture, src/ccp_studio/contracts, src/ccp_studio/services, tests/cmf_studio, registries/canonical, and operator-web. Do not write code yet. Produce a readiness matrix covering all integrated bundles, tests, backend routes, operator-web routes, fake/dry-run/real execution paths, and format coverage for Formats 01, 02, 03, and 04. Then recommend the next implementation bundle. Pay special attention to Format 01, Format 03, Format 04 parity, Render QA integration, provider sample approval UI, and real execution gating.”

The likely recommendation after that audit should be Format 01 Story Video Engine V1, unless the codebase shows a more urgent broken integration.

## 11. Final assessment

CMF Studio is now past the architecture-discovery stage. The project has a serious backbone: source truth, brand context, extraction, format routing, composition, avatar assets, provider jobs, render jobs, QA receipts, approvals, recipes, workspaces, and operator read models. The weakness is not conceptual clarity. The weakness is format parity and real execution wiring.

Format 02 is the strongest because it was used as the first golden path. Format 01, 03, and 04 need equal treatment. Operator UI should continue to be built for internal operators running the backend, not for early self-serve clients. The first product remains the interview and Guest Asset Pack, with software/community later. That means the near-term engine should help operators run interviews, ingest references, generate governed assets, review samples, validate renders, approve exports, and create reusable production memory.

The next phase should therefore focus on three things: format parity, operator execution, and controlled real runtime enablement. If those are handled in that order, CMF Studio can become a real production engine rather than a collection of isolated generators.


## 12. Additional handoff note

The next team should treat every implemented module as a candidate that must be verified against the actual repository. Some bundles were designed as clean overlays, but real repositories often contain older names, duplicate concepts, partially integrated adapters, fixture-only screens, or backend routes that differ from the planned names. The correct process is inspect, map, test, then implement. Do not assume that because a bundle exists, its integration is complete. Do not assume that because a UI screen exists, it is backed by live services. Do not assume that because a service has a real-execution method, real execution is safe. The studio should keep fake and dry-run paths until preflight, worker capability, provider approval, artifact storage, render QA, and operator approval are all proven.

---

Approximate word count: 3233

## 12. Practical readiness matrix for the next session

The next session should create a concrete readiness matrix, not just a prose summary. The matrix should include every major layer and answer five questions: does the code exist, do tests exist, do docs exist, is the path fake/dry-run/real, and what must happen next. A useful first draft is below.

Brand/source/interview intake is foundational but should be checked. The repo has PRD material describing the interview-first flow, source artifact manifests, brand context versions, and expression sessions. The next chat should verify whether the operator UI can actually create a client workspace, brand workspace, brand context version, and source/reference assets. If this wiring is incomplete, the engine will have downstream contracts but no clean operator entry point.

Narrative Story Doctor and Extraction Intelligence should be treated as upstream compiler infrastructure. Their readiness depends on whether tests still pass and whether the contracts connect to actual expression sessions and interview briefs. The next chat should inspect whether extracted expression moments can be listed in the operator UI and used by SuperVisual, Carousel, Format 01, Format 02, Format 03, or Format 04 flows.

Format Intelligence should be considered the meaning-to-format router. It is useful only if each target format has enough implementation behind it. At present, Format 02 is the strongest. Format 01, 03, and 04 should be marked “doctrine exists, operational parity missing” unless the codebase shows new work not reflected in this handoff.

Composition Intelligence and Template Preview should be marked medium-to-high for Format 02 and partial for other formats. Template Preview Atlas is valuable because it gives operators deterministic previews before expensive generation. The next implementation phase should extend preview semantics for Format 01, 03, and 04 instead of only paper-cut explainer scenes.

Avatar Performance and Avatar Asset Production should be marked medium-high for Format 02. They are less relevant to Format 01 unless a coach avatar overlay is used, and very relevant to Format 03/04 if those formats include reaction coach layers. The no-lip-sync law should remain global for the avatar system. If future formats need talking-head video, that should be a separate source-video/A-roll system, not a lip-synced avatar system.

Provider Runtime should be marked governance-ready but real-execution-not-ready. It is strong for Ideogram and Flux role separation and sample-first gates. It still needs real adapter clients, provider secrets/config handling, sample approval UI, cost/usage tracking, and artifact materialization before real generation. The next chat should not add real provider calls until operator sample approval exists.

Local Render Worker should be marked lifecycle-ready but fake-only. It can register workers, create jobs, lease jobs, heartbeat, and complete fake results. Real execution should not be enabled until runtime capabilities are tested on the local machine and linked to Capability Preflight.

Remotion/FFmpeg Adapter should be marked dry-run-ready and real-gated. It is the target replacement path for legacy render sidecars, but the codebase should not assume real Remotion or FFmpeg are installed. Real execution needs a dedicated environment configuration and test plan.

Pipeline Recipe Harness should be marked control/read-model-ready. Its purpose is to generalize Golden Path orchestration into recipes without creating a second engine. The next chat should inspect whether it was mapped to the existing orchestration spine or whether it remains a recipe-layer wrapper. If it is not mapped yet, that mapping should be done before building complex pipeline run controls.

## 13. Recommended next bundle sequence

The next bundle sequence should be format parity first, then operator approval, then real execution.

First, build Format 01 Story Video Engine V1. This should become the core interview-led video path. It should handle A-roll source refs, transcript segments, emotional arc, quote moments, B-roll story functions, memory object cues, sonic contrast, captions, and timeline plans. It should explicitly reject filler B-roll. It should output a Format01TimelinePlan and Format01RenderPromise that can feed Video Editing Engine and Render QA.

Second, build Format 03 Living Commentary Reactions V1. This should focus on proof surfaces, source quotes, screenshots, reaction layers, Rough Notation, split-screen layouts, proof legibility, and reaction balance. It should include contracts for ProofSurface, ReactionCoachLayer, RoughNotationCue, ProofLegibilityReceipt, ReactionBalanceReceipt, and Format03TimelinePlan. This format should be designed for evidence-led commentary, not generic reaction content.

Third, build Format 04 Conscious Reactions V1. This should cover debate frames, rankings, tier boards, scorecards, claim evidence refs, source tension, memetic cue plans, and pacing. It should use the memetic moderation laws already started in the Remotion adapter and Render QA layer.

Fourth, update Pipeline Recipe Harness to include real recipes for Format 03 and Format 04 and strengthen Format 01. The harness should map each format’s steps into existing orchestration stages, approval gates, provider sample steps, render QA steps, and export steps.

Fifth, build Provider Sample Approval UI. This should show Ideogram scene samples, Flux face plate/object edit samples, template preview samples, cost estimates, decision logs, retry policy, blockers, and approval status. Batch generation should stay locked until the three sample approvals are complete.

Sixth, wire Render QA into the Video Workbench and Pipeline Run Monitor. A render should not merely show a preview URL. It should show whether playability, duration, frame sampling, audio, captions, visual regression, character consistency, motion promise, and delivery promise passed.

Seventh, implement real observation bridges for Render QA. This can include ffprobe metadata collection, frame sampling extraction, audio loudness analysis, caption detection, screenshot baselines, and character/style comparison. These should run through Local Render Worker, not arbitrary service calls.

Eighth, enable real Remotion/FFmpeg execution behind explicit gates. Only after the worker has tested capabilities and Capability Preflight passes should the system allow real local rendering. Tests must still prove that default paths do not accidentally execute subprocesses.

Ninth, add real provider adapters for Ideogram and Flux. This should happen after Provider Sample Approval UI and workspace artifact storage are stable. Real provider outputs must produce ProviderJobReceipt and ProviderOutputAssetRef records.

Tenth, complete the legacy render deprecation migration. Python/C++ Skia sidecars should be marked and eventually removed only after replacement tests prove Remotion Node.js + @remotion/skia covers the old use cases.

## 14. Questions the next chat must answer from the codebase

Before implementing anything, the next chat should verify repository reality: which prompts were actually run, whether backend and operator-web tests pass, whether UI routes are fixture-backed or live, whether Render QA duplicates adapter QA contracts, whether Pipeline Recipe Harness is mapped to the orchestration spine, and whether Format 01, 03, and 04 are real contracts or only doctrine. It should also confirm that no provider or render path executes by default, because real execution must stay behind preflight, worker, and approval gates. The most important final question is: what is the next smallest production-grade vertical slice after Format 02? The likely answer is Format 01, because it is the closest to the interview-first product and Guest Asset Pack.

## 15. Handoff principle

The next phase should convert documented architecture into reliable operator workflows. The correct order is: verify repository reality, close format parity gaps, expose approvals and QA, then enable real execution behind gates. Do not add more provider or render code until the operator path can safely control it. Do not add UI that lacks backend truth. The studio needs both: typed backend evidence and operator-first surfaces.





---

Approximate word count: 4392
