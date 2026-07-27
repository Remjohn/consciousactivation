---
type: prd-module
module_id: PRD-CMF-13
title: "OpenMontage-Inspired Production Orchestration Adapters"
status: canonical-draft
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
reference_architecture:
  - "https://github.com/calesthio/OpenMontage"
  - "https://github.com/calesthio/OpenMontage/blob/main/README.md"
  - "https://github.com/calesthio/OpenMontage/blob/main/AGENT_GUIDE.md"
  - "https://github.com/calesthio/OpenMontage/blob/main/docs/ARCHITECTURE.md"
  - "https://github.com/calesthio/OpenMontage/blob/main/docs/PROVIDERS.md"
created_at: 2026-06-25
---

# PRD-CMF-13: OpenMontage-Inspired Production Orchestration Adapters

## 1. Product Requirement

CMF Studio must adapt the operational strengths of OpenMontage as CMF-native architecture patterns, not as copied runtime authority. OpenMontage proves a practical agentic production shape: declarative pipeline manifests, stage director skills, tool discovery, provider menus, scored provider selection, project workspaces, checkpointed stages, render runtime locking, pre-compose validation, post-render QA, cost governance, and agent-facing operating contracts. CMF must absorb those patterns into its existing Python-first, Pydantic-first, interview-first architecture.

This module extends PRD-CMF-07, PRD-CMF-08, PRD-CMF-10, and PRD-CMF-12. It does not replace Brand Context, Interview Brief V2, Complete Expression Sessions, Expression Moments, ContentSequencePrograms, SceneSpecs, CompositionRuntimeBinding, provider receipts, primitive evals, doctrine gates, operator approval, or the Command Bus.

## 2. Integration Laws

| Law | Requirement |
|---|---|
| Reference, not runtime authority | OpenMontage informs adapter design, but CMF owns contracts, receipts, workflows, and state. |
| No AGPL code import without governance | Any direct dependency or copied implementation requires `IntegrationAdapterDecisionReceipt`, license review, and approval. |
| Pipeline manifests are not enough | CMF manifests must bind to Brand Context, source truth, consent, primitives, receipts, and operator review. |
| Skills must be typed | Stage director and vendor skills must produce invocation records, typed outputs, eval receipts, and review blockers. |
| Runtime choice must be locked | Remotion, Motion Canvas, HyperFrames, FFmpeg, or worker routes cannot silently swap after approval. |
| QA must block release | Pre-compose and post-render checks become approval blockers, not advisory notes. |

## 3. Functional Requirements

### FR-CMF-13.01 OpenMontage Reference Adapter Governance

The system must create a CMF-native governance layer for adopting OpenMontage architecture patterns without making OpenMontage a production source of truth. The adapter governance service must register the reference repository, README, Agent Guide, Architecture Guide, Provider Guide, license status, candidate patterns, prohibited uses, and implementation decisions as `IntegrationCandidate` records. Every pattern imported into CMF planning must receive an `IntegrationAdapterDecisionReceipt` that states whether it is `reference_only`, `adapter_now`, `lab_only`, or `blocked`. Because OpenMontage is AGPLv3, direct code copying, vendored runtime imports, or production dependency use must be blocked unless legal and architecture review explicitly approve it. The first approved use should be pattern translation: pipeline manifests become CMF pipeline profiles, director skills become governed stage instruction contracts, provider selection becomes CMF capability scoring, and OpenMontage QA gates become CMF eval targets. Operators must be able to inspect why each pattern was adopted, which CMF objects it maps to, and which shortcuts are forbidden. This feature prevents vague inspiration from becoming uncontrolled dependency drift.

### FR-CMF-13.02 CMF Production Pipeline Manifest Registry

The system must introduce a production pipeline manifest registry inspired by OpenMontage `pipeline_defs`, but upgraded for CMF's interview-first object spine. Each manifest must define stage order, stage owner, director skill contract, entry object, exit object, required tools, fallback tools, human approval policy, review focus, success criteria, eval targets, receipt obligations, and downstream composition targets. Unlike OpenMontage, a CMF manifest cannot start from a generic topic alone when the output is guest-owned content. It must bind to organization, brand workspace, consent state, Brand Context Version, Interview Brief V2, Complete Expression Session, Expression Moment, route, Asset Package Spec, or ContentSequenceProgram according to stage. Manifest activation must pass schema validation and a doctrine gate proving the pipeline does not bypass source truth, primitive evaluation, guest safety, or operator approval. Runtime consumers such as Pi, DSPy programs, provider adapters, Remotion, Motion Canvas, HyperFrames, FFmpeg, and review workbench must read the active manifest snapshot, never a loose YAML file. Manifests must be versioned, hash-backed, and reversible.

### FR-CMF-13.03 Stage Director Skill Contract Binding

The system must convert OpenMontage's stage director skill pattern into CMF `StageDirectorSkillSpec` contracts. Each stage skill must define how an agent, DSPy program, deterministic service, or human queue should perform the stage, but it cannot mutate canonical state directly. A valid stage director skill must declare its pipeline stage, allowed active object scope, required context bundle, required primitives, approved tools, required source artifacts, output schema, review criteria, blocker types, and receipt type. The skill must also distinguish stable operational skills from JIT skills used for interview engineering, narrative induction, extraction lenses, visual prompt shaping, and eval interpretation. When a stage runs, the system must record a `StageSkillInvocationReceipt` containing skill version, input object hashes, agent or service identity, tool calls requested, outputs created, review status, and blockers. This pattern preserves OpenMontage's readable agent operating guides while making them compatible with CMF's Pydantic contract authority, AgentRoleSpec registry, Command Bus, and receipt chain. Hidden prompt text or undocumented skill behavior must block production use.

### FR-CMF-13.04 Capability Tool Registry and Provider Menu

The system must build a CMF capability registry and provider menu modeled on OpenMontage's tool registry, but scoped to CMF's provider, renderer, research, editing, and evaluation boundaries. Each tool capability record must state name, capability family, provider, runtime type, stability, dependencies, credential boundary, input schema, output schema, fallback options, resource profile, cost estimator, retry policy, allowed brand-scope behavior, consent requirements, and linked skills. The provider menu must summarize configured and unavailable capabilities for operators before expensive work begins: video generation, image generation, layer extraction, segmentation, TTS, music, SFX, background removal, research, transcription, Remotion, Motion Canvas, HyperFrames, FFmpeg, ComfyUI, and publishing adapters. CMF must not hardcode provider availability in prompts or specs; Pi and the Operations Board must query the registry. The menu must explain what the system can produce now, what requires credentials or GPU workers, what is blocked by consent or license state, and what quality tradeoffs apply. Provider menu snapshots must become receipt-backed evidence for production planning. The same snapshot must support audit replay.

### FR-CMF-13.05 Scored Provider Selector and Capability Router

The system must implement a scored provider selector inspired by OpenMontage's seven-dimension ranking, adapted to CMF's stricter production standards. For each capability request, the selector must score candidate providers across task fit, output quality, control surface, reliability, cost efficiency, latency, continuity, consent compatibility, brand fit, source-lineage support, reproducibility, and primitive/eval compatibility. The selector must support explicit operator preference, but it cannot obey a preference that violates consent, budget, capability status, or route doctrine. Each provider decision must write a `ProviderSelectionReceipt` with all candidates considered, scores, chosen provider, rejected options, reason, cost estimate, expected artifact type, fallback policy, and required evals. Selectors must route Ideogram 4, GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, ComfyUI workers, LavaSR, TTS, music, stock footage, Remotion, Motion Canvas, HyperFrames, and FFmpeg through one governance model. This feature is operationally critical because CMF must choose tools based on the asset's function, not whatever provider is most fashionable or easiest to call. Score weights must be registry-configurable.

### FR-CMF-13.06 Brand-Scoped Project Workspace and Checkpoint Runtime

The system must create a brand-scoped project workspace and checkpoint runtime inspired by OpenMontage `projects/<project-name>/`, but governed by CMF tenant isolation and receipt lineage. Every production run must create a workspace rooted in organization, brand, guest, source artifact, session, asset package, and pipeline run IDs. The workspace must separate canonical JSON artifacts, source media, provider raw outputs, generated assets, audio, subtitles, render manifests, QA reports, and final deliverables. Checkpoints must persist each stage state as `pending`, `in_progress`, `awaiting_human`, `completed`, `failed`, `quarantined`, or `superseded`, with canonical artifact hashes and receipt references. Resuming a workflow must use the latest valid checkpoint and must never rerun paid provider work unless the retry policy permits it and a new receipt is written. Unlike OpenMontage's gitignored workspace convention, CMF must store durable workspace metadata in Postgres and object storage, with short-lived UI access links. This feature gives operators resumability without manual folders, hidden scripts, or cross-brand confusion. Workspace naming must be deterministic and collision-safe.

### FR-CMF-13.07 Reference Video and Existing Footage Intake Adapter

The system must adapt OpenMontage's reference video entry point into a CMF intake adapter for inspiration videos, existing interviews, guest footage, and competitor/reference compositions. When an operator provides a YouTube URL, local file, Reel, Short, or long interview, the system must classify whether it is inspiration, source footage, existing interview transcript, or prohibited/unlicensed material. For inspiration, the adapter must extract pacing, hook, scene structure, motion grammar, subtitle behavior, framing, visual hierarchy, and emotional logic without copying protected creative expression. For source footage, it must run consent, media inspection, transcription, diarization, scene detection, frame sampling, and provenance capture. The output must be a `ReferenceVideoAnalysisReceipt` or `SourceFootageInspectionReceipt` linked to Brand Context, Interview Brief V2, ContentSequenceProgram, and CompositionRuntimeBinding where applicable. Operators must receive differentiated CMF-native concepts, not carbon copies. This feature directly supports the user's expected composition references while preventing the system from mistaking visual inspiration for approved production assets or source truth. Copyright risk must be explicit, reviewable, and actionable.

### FR-CMF-13.08 Real-Footage Corpus and Source Media Retrieval Adapter

The system must add a real-footage retrieval path inspired by OpenMontage's documentary montage pipeline while preserving CMF's SVRE/Aurore, licensing, and evidence requirements. The adapter must support open and licensed footage sources such as internal archives, approved guest footage, brand-owned B-roll, Pexels, Pixabay, Wikimedia, NASA, Archive.org, and future search providers behind capability contracts. Retrieved clips must be indexed by visual embedding, transcript or caption, license, source URL, duration, resolution, emotional role, symbolic role, composition use, route fit, and brand compatibility. The system must distinguish direct-use footage, reference-only footage, metaphor footage, archival evidence, and prohibited material. A `RealFootageCorpusReceipt` must record query, candidates, ranking rationale, license evidence, download hash, clip rights, and selected asset-roll role. This requirement is essential because CMF cannot rely only on generated stills or prompt-based visuals. Cinematic Story Commentary, Living Commentary Reactions, and Challenger assets often need actual motion, memory-object inserts, environmental texture, or archival proof to avoid flat slideshow output. Candidate expiry and takedown status must be tracked.

### FR-CMF-13.09 Render Runtime Selection and Locking

The system must formalize render runtime selection as an approval-gated decision inspired by OpenMontage's Remotion, HyperFrames, and FFmpeg runtime lock. CMF must expose available render routes for each production plan: Remotion, Motion Canvas, HyperFrames, FFmpeg, ComfyUI worker, video generation provider, or hybrid assembly. The selector must explain what each runtime is best at for the specific asset: transcript-timed social video, PaperCut/2D motion, GSAP/HTML kinetic typography, simple cuts, GPU-generated plates, real-footage assembly, or reaction UI overlays. Once approved, the chosen runtime must be written into the render contract, composition handoff, edit decisions, and provider receipts. Silent swaps are forbidden. If the selected runtime becomes unavailable, the system must raise a structured blocker with alternatives, cost, quality impact, and required operator approval. This prevents a high-motion Conscious Reactions clip from degrading into still-image Ken Burns, or a PaperCut explainer from becoming flat corporate animation. Runtime choice must be inspectable in the review workbench and Operations Board. Drift detection must compare approved and executed runtime.

### FR-CMF-13.10 Pre-Compose Delivery Promise and Slideshow Risk Gate

The system must implement a pre-compose validation gate inspired by OpenMontage's delivery promise enforcement and slideshow risk scoring, upgraded with CMF primitive and doctrine checks. Before any render starts, the system must validate that the approved SceneSpec, ContentSequenceProgram, CompositionRuntimeBinding, render contract, selected assets, caption plan, music/SFX plan, timing map, and runtime route can actually deliver the promised format. The gate must block mismatches such as motion-led video using mostly static assets, reaction UI unrelated to transcript beats, PaperCut scenes without layer materiality, cinematic clips without emotional pacing, or educational explainers with no concept-motion mapping. Slideshow risk must score repetition, decorative visuals, weak motion, unsupported cinematic claims, typography overreliance, missing source footage, and primitive triad failure. The output must be a `PreComposeValidationReceipt` with pass, warning, or blocking verdicts and exact repair commands. This feature operationalizes the user's demand that visual compositions respect doctrines and primitives before rendering, rather than being judged only after a pretty preview exists. Waivers must require human approval.

### FR-CMF-13.11 Post-Render Self-Review and Media QA Gate

The system must add a post-render QA gate inspired by OpenMontage's ffprobe, frame sampling, audio analysis, delivery promise checks, and subtitle verification. Every rendered asset must produce a `PostRenderReviewReceipt` before operator approval. The QA service must inspect duration, resolution, frame rate, codec, file size, black frames, frozen frames, broken overlays, off-canvas text, caption presence, caption timing, audio silence, clipping, loudness, music ducking, human cutout alignment, render artifact visibility, brand watermark or logo rules, and platform profile compatibility. CMF-specific checks must validate source lineage, Brand Context Version, Expression Moment binding, primitive triad evidence, doctrine eval receipts, consent compatibility, and composition family rules. Failures must map to actionable repair commands such as re-render captions, adjust crop, replace asset, repair audio mix, regenerate layer mask, rerun runtime binding, or escalate to human review. The rendered file cannot enter final approval, publishing intent, memory admission, or package sequencing until this QA gate passes or receives an explicit waiver receipt. QA sampling must be deterministic.

### FR-CMF-13.12 Budget, Cost, and Resource Governance

The system must adapt OpenMontage's estimate, reserve, and reconcile cost lifecycle into CMF's provider and worker governance. Before provider jobs, GPU workers, render batches, music generation, video generation, image generation, TTS, stock retrieval, or paid API calls execute, the system must estimate cost, check budget policy, reserve budget, and present approval thresholds when needed. After execution, it must reconcile actual spend, store provider-reported usage, output hashes, retry count, worker time, GPU tier, and cost variance. Budget rules must be brand-scoped and package-aware: monthly guest packs, trial packs, experimental renders, failed jobs, and operator-approved retries must be visible separately. A `CostGovernanceReceipt` must link provider selection, capability menu state, job receipts, render receipts, and operations board read models. The system must support observe, warn, and cap modes, but public production should block surprise spend. This feature matters because CMF uses multiple expensive providers and self-hosted GPU infrastructure; without explicit cost governance, the factory can become operationally unpredictable even when the creative output is good.

### FR-CMF-13.13 Canonical Stage Artifacts, Human Approval, and Reviewer Protocol

The system must create a canonical stage artifact and reviewer protocol inspired by OpenMontage's schema-validated artifacts, checkpoints, reviewer skill, and human approval policy. Each CMF production stage must produce one or more typed artifacts such as `ResearchBrief`, `InterviewBriefV2`, `ExpressionIngredientInventory`, `ContentSequenceProgram`, `SceneSpec`, `AssetManifest`, `EditDecisionList`, `CompositionRuntimeBinding`, `RenderReport`, `EvaluationReceipt`, or `ApprovalPacket`. Stage completion must be impossible unless the artifact validates against Pydantic and JSON Schema, links required receipts, and records review outcome. Reviewer logic must be doctrine-aware: critical findings block, suggestions record warnings, and repeated repair loops escalate to operator decision. Human approval policy must be declared per stage and visible before execution. Creative stages should pause for approval; mechanical stages may continue only when prior approvals and gates are satisfied. This feature keeps OpenMontage's practical artifact discipline while reinforcing CMF's higher standard: models and agents may recommend, but operators approve public truth, final creative direction, publishing readiness, and waivers. Reviewer outcomes must remain replayable from receipts, source artifacts, and validated schema snapshots.

## 4. Tech Spec Crosswalk

| Requirement | Planned Tech Spec |
|---|---|
| FR-CMF-13.01 | `TS-CMF-120-openmontage-reference-adapter-governance.md` |
| FR-CMF-13.02 | `TS-CMF-121-production-pipeline-manifest-registry.md` |
| FR-CMF-13.03 | `TS-CMF-122-stage-director-skill-contract-binding.md` |
| FR-CMF-13.04 | `TS-CMF-123-capability-tool-registry-and-provider-menu.md` |
| FR-CMF-13.05 | `TS-CMF-124-scored-provider-selector-and-capability-router.md` |
| FR-CMF-13.06 | `TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md` |
| FR-CMF-13.07 | `TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md` |
| FR-CMF-13.08 | `TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md` |
| FR-CMF-13.09 | `TS-CMF-128-render-runtime-selection-and-locking.md` |
| FR-CMF-13.10 | `TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` |
| FR-CMF-13.11 | `TS-CMF-130-post-render-self-review-and-media-qa-gate.md` |
| FR-CMF-13.12 | `TS-CMF-131-budget-cost-and-resource-governance.md` |
| FR-CMF-13.13 | `TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` |
