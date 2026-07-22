---
stepsCompleted:
  - 1
inputDocuments:
  - 'docs/migration/legacy-inventory.md'
  - 'THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md'
  - 'THE CMF STUDIO/CCP V9 â€” Interview-First Expression Engine.md'
  - 'THE CMF STUDIO/CCP V9.1 â€” Expression Capture & Archetype Routing Update.md'
  - 'THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md'
  - 'THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md'
  - 'THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md'
  - 'THE CMF STUDIO/Grill-me.md'
  - 'THE CMF STUDIO/Matrix of Edging.md'
workflowType: 'product-brief'
lastStep: 1
project_name: 'CMF STUDIO'
user_name: 'Emilio'
date: '2026-06-19'
---

# Product Brief: CMF STUDIO

**Date:** 2026-06-19
**Author:** Emilio

---

## 1. Executive Summary and Vision

CMF STUDIO represents the transition from a collection of scattered prompt-based extraction scripts into a greenfield, production-grade, multi-brand agentic application. The primary vision is to build an operating system that transforms researched, authentic human expression into coherent, reusable, evaluated, approved, and publishable media. 

Unlike traditional content repurposing tools that treat video editing as a post-production problem, CMF STUDIO acknowledges that the bottleneck in modern thought leadership is not clipping software, but human expression itself. To solve this, CMF STUDIO operates as an end-to-end "factory" pipeline that begins long before the camera turns on and continues long after the video is rendered. 

The application architecture spans across:
- **Brand Genesis**: Upfront generation and locking of a client's creative universe (actors, props, motions).
- **Research and Context Engineering**: Deep algorithmic preparation for interviews.
- **Interview Intelligence & Narrative State Induction**: Real-time interviewer guidance to pull guests out of "centroid" answers.
- **Complete Expression Sessions**: Synchronization and transcription of the raw captured state.
- **Archetype and Asset Routing**: Deterministic mapping of expression to specific structural formats.
- **Complete Editing Sessions**: Compilation of assets, scripts, and visual instructions.
- **Ideogram 4 Composition Control**: Scene-level composition plates governed by a structured `CompositionJob` JSON contract.
- **CMF Production & Rendering**: Multi-modal rendering (Remotion, Motion Canvas, SCAIL-2).
- **Evaluation and Human Approval**: Rigid scoring protocols ensuring fidelity, negative space compliance, and visual accuracy.
- **Publishing & Brand Memory**: Publer integrations, evidence-backed memory admission, and Neo4j as a rebuildable relationship projection.

CMF STUDIO is a complete expression-to-asset operating system. Its category is not AI clipping, AI script generation, or template content production. It is a production-grade agentic pipeline that activates authentic human expression, extracts production-ready moments, routes them through archetype and CMF render contracts, and emits evaluated, approved, publishable assets with full lineage.

The central engineering truth of CMF STUDIO is that it is a Python-first agentic harness built on Pydantic v2 contracts, DSPy programs, and Pi Coding Agent orchestration. TypeScript and front-end frameworks are strictly relegated to presentation and rendering surfaces (Next.js PWA, Telegram Mini App, Remotion, Motion Canvas). This Product Brief specifies the complete operational doctrine, competitive differentiators, target user segments, risk vectors, and the dependency-ordered full-system build gates required to build the system.

This greenfield mandate does not mean discarding legacy intelligence. The Legacy Repository Inventory identifies 1686 existing files that must be treated as read-only source material for doctrine, registries, fixtures, provider templates, evaluation gates, and reference implementations. CMF STUDIO must preserve valuable legacy assets by migrating them into Pydantic contracts, DSPy programs, durable workflow fixtures, eval targets, and worker assets. It must not import legacy runtime code directly into production.

---

## 2. The Core Problem and Current Workflow Limitations

### 2.1 The "Centroid Answer" Problem
The most pervasive problem in high-level B2B coaching, consulting, and thought leadership is the "centroid answer." When experts are placed in front of a camera, they instinctively default to safe, intellectualized, abstracted summaries of their knowledge. They strip away the messy, visceral reality of their lived experience in favor of bullet points. The result is content that is factually accurate but emotionally dead. No amount of downstream editing, auto-captioning, or b-roll injection can fix a centroid answer because the raw material lacks "charge."

### 2.2 The "Editor-First" Paradigm Failure
Existing AI video tools (Descript, Opus Clip, Riverside) operate on an "editor-first" paradigm. They assume that the source material is already high-quality and that the user's goal is simply to find the best 60 seconds, remove filler words, and add animated captions. While these tools reduce manual editing time, they do nothing to solve the upstream problem of poor expression. Furthermore, they are entirely blind to the nuances of *Brand DNA* and *Voice DNA*, treating every speaker with the same generic "Hormozi-style" visual sheen. 

The business consequence is direct: weak extraction produces weak routeability, weak routeability produces generic assets, and generic assets reduce both trial-pack proof and monthly retention.

### 2.3 Legacy Pipeline Inefficiencies 
Historically, the Conscious Coaching Factory (CCF) / CMF pipeline relied heavily on brute-force extraction. Operators would take raw transcripts and manually hunt for the "best possible moments" to compress into a cinematic short clip. While this produced high-quality outputs, it suffered from severe limitations:
- **Archetypal Myopia**: Because operators were hunting for a specific type of cinematic resonance, they routinely ignored other highly valuable content archetypes (e.g., Data Stories, Audience Mirror Quizzes, Persuasive Micro-Claims).
- **Brand Reinvention**: Every render required the system to "reinvent" the brand's visual language, leading to inconsistent styling, drifting color palettes, and prompt-fatigue.
- **Siloed Intelligence**: Content from one video was isolated from content in another. There was no systemic mechanism to inject contextual boosters from a coach's wider library into a new asset.
- **Operator Burnout**: Manual hunting, diagnosing, and composing required massive cognitive load, creating a hard ceiling on the number of clients a single operator could manage.

The legacy inventory also shows that the old system contains reusable intelligence that should not be lost: 244 cognitive primitives, SDA/SFL registries, 96 archetype prompts, 34 creative subsystems, Voice DNA verification services, audio composition engines, CBAR gate packs, ERA3 spec-writing protocols, and TTT tonal transition methodology. The failure was not the existence of these assets; it was their scattered runtime form and lack of typed orchestration.

CMF STUDIO solves these problems by moving from a manual extraction model to a deterministic, contract-driven induction and composition factory while migrating the highest-value legacy intelligence into the new Python-first Harness.

---

## 3. Competitive Moat and Unique Differentiators

CMF STUDIOâ€™s competitive moat is constructed around six proprietary doctrines and architectures that are entirely absent from mainstream AI content tools.

### 3.1 Narrative State Induction (Human Activation Protocol)
CMF STUDIO's most profound differentiator is that it operates upstream of the recording. The system treats the interview not as a Q&A, but as an **Interview Asset Contract**. Each question in a generated interview deck (e.g., the Claude Ntahuga Interview Deck V4) carries precise structural mandates:
- **Target Archetypes**: Identifying exactly what format the answer will fuel (e.g., Conceptual Contrast, Authority Proof Stack).
- **Target Emotional Arc**: Specifying the required emotional transition (e.g., "Authority â†’ Vulnerability â†’ Invitation").
- **First-Line Anchors**: Prepared starting phrases (Cinematic, Emotional, Reels Hook) designed to give the guest a clean, clip-ready runway.
- **Depth Anchors**: Real-time transition phrases deployed by the Operator to pull the guest out of abstraction (e.g., "Before we talk about the history, what did that specific scene do to the young Claude who was standing there?").

This protocol cannot be shipped as SaaS software because it relies on real-time human cognitive routing by the Operator. CMF STUDIO creates the conditions in which high-charge input becomes possible.

CMF STUDIO therefore performs two levels of extraction. First, it extracts from the guest before capture through research, Context Premise, Emotional DNA/Voice DNA where available, Matrix of Edging, Narrative State Induction, First-Line Anchors, and Depth Anchors. Second, it extracts from the transcript and source artifacts after capture through Expression Moment extraction, archetype routing, asset derivative routing, and evaluation receipts.

### 3.2 The Matrix of Edging (Controlled Tension Architecture)
The Matrix of Edging is a proprietary eight-stage force matrix that governs how tension and meaning move through the system. Instead of relying on a generic "hook score," the Matrix systematically organizes force:
1. **Research Pass**: Identifying live pressure points.
2. **Provocation Pass**: Formulating questions that crack the facade.
3. **Authentication Pass**: Validating whether the response is real or performed.
4. **Primitive Pass**: Detecting available meaning transforms (Irony Inversion, Tribal Reference, What-Is/What-Could-Be, Analogy Bridge, Stakes as Personal Why).
5. **Coalition Pass**: Organizing multiple primitives into a structural force.
6. **Edge Pass**: Defining the final tension object.
7. **Routing Pass**: Mapping the edge to a CMF archetype path.
8. **Benchmark Pass**: Tracking "coalition fatality" (when a theoretical edge dies in execution).

This systematic architecture ensures that tension is deliberately engineered and tracked for survival, providing a level of meaning-space control that competitors cannot replicate.

### 3.3 Brand Genesis V3 (Versioned Creative Substrate)
Unlike standard tools that generate visuals dynamically per clip, CMF STUDIO requires a massive upfront manufacturing phase known as Brand Genesis. This creates a versioned, frozen creative universe for each client:
- **64-State Acting Library**: An 8x8 matrix of acting references (8 emotional families Ã— 8 gesture families) ensuring a mathematically complete range of expressions.
- **Paper-Cut Avatar Rig**: A fully separated 2D rig featuring layered heads, facial expressions, eye/brow variants, mouth shapes, and body layers, all rigged with bone constraints for deterministic animation in Remotion or Motion Canvas.
- **Micro-Semiotic Anchoring**: The deliberate placement of culturally specific, subtle visual cues (e.g., yellow-and-blue budget-supermarket-coded socks for a French audience) designed to trigger tribal recognition, humor, and organic comments without distracting from the main subject. Each anchor is scored for legal risk, subtlety, and comment potential.

Once the Brand Context v1 is locked, all future rendering retrieves from this frozen universe, guaranteeing absolute visual consistency and eliminating generative style drift.

### 3.4 The Complete Editing Session Container (Full Lineage Auditing)
Every asset produced by CMF STUDIO exists inside a "Complete Editing Session" object. This container acts as an immutable receipt, carrying the full lineage of the asset:
- Source Expression Session ID
- Source Expression Moment ID
- Core Archetype & Asset Derivative
- CMF Route & Visual Style
- Selected Acting References & Composition Hashes
- Multi-dimensional Evaluation Receipt (Identity consistency, emotion match, negative space compliance, hook strength, motion restraint).

This provenance tracking ensures that assets are fully auditable, reproducible, and verifiable, making the system a true factory rather than a random generation script.

Minimal lineage receipt shape:

```json
{
  "complete_editing_session_id": "ces_2026_0001",
  "source_expression_session_id": "xes_2026_0001",
  "source_expression_moment_id": "xem_2026_0042",
  "brand_context_version_id": "bcv_001_locked",
  "archetype_route": "myth_debunk",
  "asset_derivative": "paper_cut_explainer",
  "scene_spec_id": "scene_0001",
  "composition_job_id": "ideogram_comp_0001",
  "render_contract_id": "render_0001",
  "evaluation_receipt_id": "eval_0001",
  "approval_state": "pending_review"
}
```

### 3.5 Eval-Gated Voice-DNA Boost Inserts (MOSS-TTS + LavaSR)
CMF STUDIO implements a groundbreaking "10â€“20% Boost Pass" utilizing voice cloning, governed by strict semantic and ethical constraints (The Voice-DNA Boost Policy).
- **The Architecture**: MOSS-TTS serves as the primary voice cloning engine, delivering high-fidelity, highly expressive synthetic audio matching the speaker's exact prosody. LavaSR serves as the audio restoration equalizer, cleaning raw source audio and normalizing synthetic inserts so they blend seamlessly.
- **The Protocol**: When the `SemanticCritic` evaluates a finalized video asset and detects a structural failure (e.g., a missing transition, an abrupt cut, a semantic gap), the system initiates a repair hierarchy.
- **The Hierarchy**: 1. Re-cut existing source -> 2. Verbatim fragment search -> 3. Prior approved quote -> 4. Human pickup request -> 5. Voice-DNA Boost Insert.
- **The Constraint**: Synthetic voice bridges are strictly capped at `min(7 seconds, 15% of final video duration)`. They are never allowed to deliver primary claims, medical advice, or core confessions.
- **Visual Covering**: Generated audio is NEVER placed over a visible talking head. It must be covered by Editorial Paper-Cut scenes, B-roll, or diagrams, preserving visual authenticity while repairing the semantic flow.

### 3.6 ImageCritic Automated Visual Evaluation
CMF STUDIO replaces massive manual human QC grids with an automated visual scoring layer utilizing the ImageCritic model. ImageCritic evaluates the 64-state acting references during Brand Genesis, scoring likeness, gesture clarity, hand quality, and paper texture consistency. Furthermore, it acts as a gatekeeper in the render pipeline, scoring output frames for composition clarity, negative space compliance, and style drift. When ImageCritic detects a failure, it generates targeted fix instructions for the Flux 2 Klein 9b / GPT Image 2 repair pipeline, creating a self-correcting visual loop.

### 3.7 Ideogram 4 CompositionJob and Scene Reproducibility

Ideogram 4 is a first-class composition-control provider for CMF STUDIO. It must be treated as a Composition Director, not as the final identity renderer and not as the canonical final text layer. Its role is to transform a structured scene specification into a usable composition plate: subject placement, visual hierarchy, text area, visual flow, metaphor objects, prop density, paper-cut arrangement, color balance, micro-semiotic anchor placement, and first-frame visual hook.

The Ideogram route must be governed by a structured `CompositionJob` JSON contract. At minimum, this contract carries `composition_job_id`, `scene_id`, `provider: ideogram_4`, `purpose: composition_plate`, compiled prompt, `prompt_hash`, constraints, and output requirements. The constraints must preserve aspect ratio, subject position, text area, visual flow, style, and any route-specific composition requirements. The output requirements must explicitly state that Ideogram must leave usable text space, produce discrete objects or layerable regions where needed, and must not finalize client identity.

The Ideogram output is a composition plate plus composition analysis, not the final production asset. Flux 2 Klein 9b, GPT Image 2, Qwen-Image-Layered, SAM3, Remotion, Motion Canvas, and brand-layer rebuilds may refine identity, layer separation, animation, final text, and platform formatting downstream. For premium production, the system should extract the Ideogram layout plan and rebuild the scene using approved brand layers and Remotion-rendered text. For faster routes, the flattened Ideogram plate may be used as a background plate only when evaluation gates allow it.

For reproducibility, every Complete Editing Session must preserve the `CompositionJob`, prompt hash, provider metadata, composition plate URI, composition analysis, downstream edit jobs, selected brand layers, final text-rendering plan, evaluation receipts, and human approval state. Scene reproducibility must therefore include both the legacy CMF beat-fingerprint/manifest lineage and the Ideogram composition JSON lineage.

### 3.7A Legacy Intentional Orchestration Modules

The old CCF and CMF modules are not merely reusable assets. They are intentional orchestration modules. Their value is not only in prompts, templates, or reference code, but in the causal order they encode: why research comes before induction, why induction comes before extraction, why primitive coalitions precede archetype routing, why sonic intent can govern visual timing, why scene containers exist before scene components, and why validation must preserve directional integrity rather than only aesthetic quality.

CMF STUDIO must therefore migrate the orchestration logic of the legacy system as first-class product intelligence:

- **CCF intentional orchestration:** CRAL/SCRE research, broad signal detection, Context Premise, Emotional DNA, Voice DNA, Matrix of Edging, primitive candidate survival, coalition signatures, edge products, archetype containers, JIT Skill compilers, anti-centroid checks, export governance, and benchmark memory.
- **CMF intentional orchestration:** sonic-first media logic, narrative-core extraction, visual trinity, scene containers, scene components, creative subsystems, A/B/C/D/E-roll asset roles, deterministic visual control, SVRE/Aurore visual research, asset licensing, scene reproducibility, render manifests, and quality gates.
- **Biological orchestration model:** DNA/truth -> RNA/contextual transcription -> force -> delivery -> variation -> phenotype -> evaluation. Legacy modules must declare where they sit in this chain.
- **Voice and Emotional DNA:** Emotional DNA is the root system that explains why Voice DNA construction patterns exist. The system must preserve the distinction between what a guest believes, how they construct expression, and the emotional path that turns activation into language.
- **Context Premise:** Audience-side intelligence must not collapse into a persona summary. It should preserve trigger depth, hermeneutical gaps, moral-emotional vectors, coping trajectory, and audience/guest or audience/coach matching logic where source evidence allows.
- **Asset engines:** Previous image, scene, audio, caption, timeline, visual research, and asset hunting engines must be migrated as contracts, fixtures, worker assets, scoring logic, and evals. Provider names or execution services that have been superseded are legacy context only; the orchestration logic remains the valuable part.

This is the product reason the Legacy Inventory matters. We are not copying an old codebase. We are preserving the intentional machinery that made the old system more than generic generation.

| Legacy orchestration source | Greenfield target | Required proof |
|---|---|---|
| CRAL/SCRE research | `CRALFinding`, `ResearchField`, `ResearchEvidence`, `ContextPremiseCompiler` | cited evidence, source role, confidence, freshness, contradiction notes |
| Context Premise and Audience Trigger logic | `ContextPremise`, `AudienceDeepTriggerMap`, `TriggerMatch` | depth mode, hermeneutical gap, moral-emotional vector, audience/guest match |
| Emotional DNA and Voice DNA | `EmotionalDNAProfile`, `VoiceDNAProfile`, negative-space and calibration receipts | belief/content distinction, construction mechanics, emotional path, forbidden drift |
| Matrix of Edging and primitive coalitions | `MatrixOfEdgingBrief`, `PrimitiveCandidatePacket`, `CoalitionSignature`, `EdgeProduct` | broad signal, candidate survival, anti-centroid pressure, route implication |
| JIT Skill compilers and anti-draft layers | `SkillInvocationRecord`, DSPy program spec, validation contract, critic report | dependency resolution, contrastive prompt layer, draft/critic/synthesis receipt |
| CMF scene containers/components/subsystems | `SceneSpec`, `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision` | why this scene exists, what component fills it, which gates were consulted |
| SVRE/Aurore and asset engines | `VisualResearchQuery`, `AssetResearchManifest`, `ImageResolutionMap`, `LicensingDecision` | candidate pool, score, license/provenance, selected/rejected reason |

### 3.8 Greenfield Legacy Extraction Doctrine
CMF STUDIO's moat is strengthened by preserving the proven intelligence embedded in the legacy CCP/CMF repository without inheriting its runtime fragmentation. The legacy repository is a read-only source of truth for primitives, archetype psychology, sonic constraints, Voice DNA verification, CBAR auditing, ERA3 spec discipline, TTT tonal management, ComfyUI worker templates, and CMF engine reference behavior.

The system must extract these assets into explicit migration targets:
- **Pydantic Registry Contracts** for cognitive primitives, SDA/SFL registries, archetype schemas, creative subsystem configs, CBAR gate packs, TTT tonal profiles, and Voice DNA calibration receipts.
- **DSPy Programs** for Context Premise compilation, Interview Asset Contract compilation, anti-draft calibration, CBAR auditing, and TTT transition evaluation.
- **Worker Assets and Reference Ports** for ComfyUI JSON templates, audio ducking/separation behavior, caption rendering, timeline generation, and CMF render assembly.
- **Fixtures and Evaluation Gates** for failure corpora, golden examples, spec audit tests, audio continuity tests, and registry validation.

This preserves the hard-won intelligence of the existing system while preventing direct legacy imports, hidden shell dependencies, untyped prompt stacks, and duplicated TypeScript domain logic.

---

## 4. Target Users and Audience Segmentation

### 4.1 The Operator (Internal Production Team)
The Operator is the internal human intelligence driving the system. The Operator manages the PWA Control Tower and the Telegram Bot (Agentic Operator Cockpit). Their role is radically different from a traditional video editor. They do not cut clips on a timeline; instead, they act as Creative Directors and Interviewers. They conduct Narrative State Induction during live recordings, review evaluation receipts, provide feedback on synthetic Voice-DNA generation, and explicitly approve publishing intents. The Operator relies on the agents to self-correct based on feedback. 

### 4.2 The Guest / Client (The Source of Expression)
The Guest is the B2B buyer of the service. They do not interact with the software UI. Their journey consists of Client Intake, Likeness Consent, Photo Upload, the live Expression Session (interview), and the receipt of the Guest Asset Pack. Guests are segmented into:
- **Expression-Latent Experts**: The highest-priority segment. These are experts with deep knowledge and client success stories who freeze up or become overly abstract on camera. The Narrative State Induction protocol is built specifically to activate them.
- **Expression-Ready Experts**: Established speakers who already produce strong material. They require less upstream induction but benefit massively from the scaling power of the factory pipeline.
- **Multi-Platform Thought Leaders**: Clients with existing vast video libraries. They benefit from the Multi-Source Ingestion pipeline, allowing the system to cross-reference up to 20 past videos to compose new asset packages.

### 4.3 The Audience (Downstream Consumers)
The end consumers never see the system, but the system's routing logic is entirely built around their psychological environments. Audience segmentation is strictly tied to specific social platforms, eliminating generic formats like "Newsletters" in favor of focused archetype routing:
- **LinkedIn**: An audience seeking authority, professional insights, and conceptual clarity. Highly text-tolerant. 
  - *Archetype Bias (Video)*: Core Educator, Personal-Brand Commentary, Conceptual Contrast. 
  - *Archetype Bias (Text)*: Thought Whisperer Extract, Persuasive Micro-Claim, Data Story.
- **Instagram Reels**: A fast-paced, hook-driven, emotional audience operating in a 15â€“60s window. 
  - *Archetype Bias (Video)*: Cinematic Story, Paper-Cut Explainer, Myth Debunk, Relief Peak Carousel.
- **TikTok**: A tribal, fast-scrolling audience that rewards authenticity, humor, and cultural recognition. 
  - *Archetype Bias (Video)*: Challenger/Frame Breaker, Meme Observations, Reaction Seeds, Micro-Semiotic Anchor heavy edits.

### 4.4 Commercial Scope and Valid Content Formats

CMF STUDIO has only two customer-facing content charges:

- `$29/week` for trial Guest Asset Packs.
- `$99/month` for the Monthly Asset Engine.

The product must not introduce Starter, Pro, Enterprise, credit bundles, hidden content tiers, or newsletter packages as customer-facing offers. Internal policy objects may still govern entitlement, usage, provider budget, render volume, storage retention, Publer profiles, trial expiration, and cost exposure, but the public content offer remains simple.

The trial Guest Asset Pack is the first paid proof unit. When source material supports it, the pack compiles:

- 4 short videos;
- 2 carousels;
- 2 meme visuals;
- 2 poll visuals;
- 2-3 reaction seeds.

Valid CMF content formats are routed through the archetype and asset derivative registries. The initial valid format set includes short videos, carousels, meme visuals, poll visuals, reaction seeds, data stories, personal-brand commentary, paper-cut explainers, myth debunks, challenger/frame-breakers, conceptual contrasts, persuasive micro-claims, and visual proof assets. Newsletters are explicitly out of scope for CMF STUDIO.

---

## 5. Product Architecture and Execution Doctrine

The core mandate for the build is absolute adherence to the Greenfield DSPy architecture. **We do not operate on an MVP basis.** The system must be built in full, following dependency order, without exposing a misleading partial product. 

### 5.1 The Python-First Runtime
The legacy system's reliance on isolated scripts and disjointed typescript UI is deprecated. The new canonical runtime is exclusively Python.
- **Semantic Contracts**: Pydantic v2 entirely owns the semantic contracts. Every command, event, registry entry, and workflow input is a versioned Pydantic model. TypeScript interfaces are strictly generated downstream from Pydantic schemas.
- **Structured Reasoning**: DSPy owns all structured reasoning. Research synthesis, Context Premise formation, extraction, routing, and calibrated evaluations are all executed as DSPy modules/signatures, completely eliminating massive monolithic prompt strings.
- **Orchestration**: The Pi Coding Agent orchestrates the system. Pi plans and coordinates work through the approved tool registry and durable workflows.
- **Durable Workflows**: Temporal (or an equivalent durable execution engine) manages all long-running processes, ensuring that rendering jobs, transcription queues, and batch generations survive process restarts and infrastructure failures.
- **Provider and GPU Workers**: ComfyUI executes only through a self-hosted Docker GPU worker using approved workflow templates and typed parameters. The target infrastructure is a 24GB or 32GB VRAM GPU node on AWS or Google Cloud. Runtime agents may request approved templates; they may not mutate arbitrary ComfyUI graphs in production.
- **Canonical State and Projection**: PostgreSQL owns canonical business state. Neo4j is a rebuildable relationship projection for deep relationship querying across brands, guests, sessions, expression moments, archetypes, assets, approvals, providers, publishing events, and memory. Neo4j must never become the only source of truth for production decisions.

### 5.2 The Agent Gateway
The application features a single Python Agent Gateway that serves multiple presentation surfaces simultaneously:
- **The PWA Control Tower**: The deep-work dashboard for extensive brand management, genesis wizards, and complex editing boards.
- **The Telegram Operator Cockpit**: A mobile-first interface featuring a Bot for real-time notifications/approvals and a Mini App for lightweight previewing and contextual chat. 

Commands are typed, idempotent, and heavily audited. The agent cannot directly mutate production databases without executing an approved command through the Command Bus.

### 5.3 Legacy Migration Doctrine
The legacy repository is a migration source, not a production dependency. CMF STUDIO must apply the Greenfield Rule: legacy files may be inventoried, hashed, copied as worker assets where appropriate, ported, rewritten, or transformed into contracts and fixtures, but they must not be imported as live runtime modules to accelerate delivery.

The migration target for each retained legacy asset must define:
- legacy type and registry family;
- canonicality confidence;
- valuable mechanics;
- known defects and limitations;
- target Python package;
- Pydantic contract target;
- DSPy program target when applicable;
- TypeScript leaf target only when the asset belongs to UI or rendering;
- fixture target;
- evaluation target;
- migration status and reviewer.

This doctrine is required because CMF STUDIO is both a greenfield product and a continuity project. The product must preserve the psychological, sonic, visual, and architectural intelligence of CCP/CMF while replacing scattered scripts, monolithic prompts, disjointed shells, and untyped state with governed contracts.

### 5A. Canonical Pipeline and Agent Team Topology

The full support artifact for this section is `docs/cmf-studio-pipeline-map.md`. The Product Brief carries the compressed canonical version so every downstream PRD, architecture, epic, story, and tech spec inherits the same operating spine.

CMF STUDIO is not one autonomous agent generating assets. It is an agentic production team operating through typed workflow contracts. Agents can operate autonomously only inside a shared pipeline where every action consumes validated state and emits a Pydantic object, receipt, human decision, or memory event.

The end-to-end spine is:

```text
Legacy Inventory and Migration Ledger
-> Workspace, Commercial Scope, Consent, and Brand Setup
-> Brand Genesis and Brand Context Version
-> Research and Context Engineering
-> Interview Intelligence and Narrative State Induction
-> Complete Expression Session
-> Expression Moment Extraction
-> Archetype, Derivative, Reaction, and CMF Route Selection
-> Asset Package Spec
-> Complete Editing Sessions
-> SceneSpec, Creative State, and Render Contract
-> Composition Control, Asset Research, and Provider Jobs
-> Renderer Routing, Assembly, and Render Output
-> Evaluation, Human Review, Revision, and Approval
-> Publishing Intent and Publer Scheduling
-> Brand, Interviewer, Route, Rejection, and Performance Memory
-> Neo4j Relationship Projection
```

| Stage | Sub-workflow | Logical agent team | Primary emitted object |
|---|---|---|---|
| 0 | Legacy inventory and migration | Migration Steward, Pi Orchestrator, Architecture Reviewer | `MigrationLedgerEntry`, `LegacyOrchestrationIntentRecord` |
| 1 | Workspace, commercial scope, and consent | Agent Gateway, Tenant/Policy service, Operator | Brand Workspace, entitlement and consent policies |
| 2 | Brand Genesis | Brand Intake, Identity/Asset role, Evaluation Agent | `BrandContextVersion`, Identity Pack, acting library, rig manifest |
| 3 | Research and context engineering | Guest Research, Audience Reality, Evidence Critic, Context Premise, Claim Safety | `GuestDossier`, `AudienceRealityBrief`, `ContextPremise`, `AudienceDeepTriggerMap` |
| 4 | Interview intelligence | Pre-Induction, Matrix of Edging, Narrative State Induction, Asset Contract Agent | `InterviewAssetContract`, `InterviewDeck`, `MatrixOfEdgingBrief` |
| 5 | Complete Expression Session | Operator, Live Interview Assistant, Capture workflow | recording artifacts, transcript, anchor hits, session receipt |
| 6 | Extraction and routing | Post-Session Extraction, JIT Skill compilers, Archetype/Derivative routers | `ExpressionMoment`, `AssetRouteReceipt`, `AssetPackageSpec` |
| 7 | Complete Editing Session | CMF Asset Producer, SceneSpec Compiler, Renderer Router | `CompleteEditingSession`, `SceneSpec`, `RenderContract` |
| 8 | Composition and asset research | Ideogram adapter, SVRE/Aurore role, Provider adapters | `CompositionJob`, `AssetResearchManifest`, provider receipts |
| 9 | Rendering and assembly | Remotion, Motion Canvas, Manim/HyperFrames when valid, Audio/Caption services | render output, layer/timeline/caption/audio manifests |
| 10 | Evaluation, review, publishing, memory | Evaluation Agent, Reviewer, Publer Adapter, Memory Admission workflow | `EvaluationReceipt`, approval event, `PublishingIntent`, memory receipt |

Pi orchestrates this pipeline through the Python Agent Gateway. Pi reads the active production object, selects the next valid stage, resolves the correct role contract, JIT skill, DSPy program, provider adapter, or deterministic service, writes a pre-execution `ValidationContract`, proposes a typed `AgentCommand`, and waits for receipts. Pi does not directly mutate production tables, publish publicly, change locked Brand Context Versions, bypass consent, or approve its own output.

The harness uses strict durable workflows for macro production state and small bounded loops inside reversible tasks:

- **Macro DAG/state machine**: Brand Genesis, Complete Expression Session, Complete Editing Session, provider jobs, rendering, approval, publishing, and memory admission.
- **Bounded autonomous loops**: schema repair, extraction refinement, section assembly, visual candidate scoring, local render retries, caption cleanup, and prompt-hash repair.
- **Independent validation**: Workers produce outputs, but Validators judge against the pre-written contract, source evidence, primitives, policies, and hard gates.
- **Human/policy gates**: identity approval, likeness use, locked Brand Context changes, billing, publishing, unsupported psychological claims, provider policy changes, and failed consent/source-truth gates.

Every handoff must preserve the object spine:

```text
MigrationLedgerEntry
-> BrandWorkspace
-> BrandGenesisSession
-> BrandContextVersion
-> ResearchField / ResearchEvidence
-> GuestDossier
-> AudienceRealityBrief
-> ContextPremise
-> EmotionalDNAProfile / VoiceDNAProfile
-> MatrixOfEdgingBrief
-> InterviewAssetContract
-> CompleteExpressionSession
-> ExpressionMoment
-> AssetRouteReceipt
-> AssetPackageSpec
-> CompleteEditingSession
-> SceneSpec
-> CompositionJob
-> ProviderJobReceipt
-> RenderOutput
-> EvaluationReceipt
-> ApprovalEvent
-> PublishingIntent
-> MemoryAdmissionReceipt
```

This map is required because autonomy without shared choreography becomes local optimization. CMF STUDIO's agents may act like a team only because the pipeline defines their role, authority, inputs, outputs, gates, and handoffs.

---

## 6. Dependency-Ordered Full-System Build Gates

The build process follows dependency-ordered full-system gates as defined in the `03_IMPLEMENTATION_SEQUENCE_AND_RELEASE_GATES.md` specification. These gates are not MVP phases and do not authorize partial product planning. They exist to preserve dependency order while building the documented system in full. Public launches are prohibited until the final Production Release Gates pass.

### Build Gate 0: Repository Archaeology and Decision Freeze
**Objective**: Understand existing value and lock in the architecture.
- Freeze the legacy repository into a read-only state.
- Inventory all 1686 legacy files and classify them as doctrine, registry, fixture, reference implementation, provider template, worker asset, or deprecated runtime.
- Inventory all legacy prompt families, primitive taxonomies, schemas, evaluation rubrics, SDA/SFL registries, cognitive primitives, archetype prompts, creative subsystem configs, CBAR gates, TTT methodology, Voice DNA services, audio engines, caption engines, and ComfyUI templates.
- Create or update the migration ledger with canonicality confidence, target Python packages, Pydantic contract targets, DSPy program targets, fixture targets, evaluation targets, known defects, reviewer, and content hash.
- Enforce the Greenfield Rule: no direct production imports from the legacy runtime.
- Draft and approve the 9 fundamental Architectural Decision Records (ADRs), including the Python/DSPy runtime and the Voice-DNA Boost synthetic exception.

### Build Gate 1: Contract and Registry Kernel
**Objective**: Create the language the entire application will speak.
- Scaffold the Python-first hybrid monorepo.
- Implement canonical Pydantic v2 contracts and JSON Schema/OpenAPI generation pipelines.
- Generate TypeScript interfaces and establish CI drift checks.
- Migrate the core legacy registries into structured Pydantic models.
- Implement the DSPy program registry and evaluation fixtures.

### Build Gate 2: Control Plane and Data Spine
**Objective**: Build the durable, secure stateful core.
- Implement PostgreSQL schema with Row Level Security (RLS), brand workspaces, and tenant isolation.
- Implement the Python Command Bus, Domain Event Outbox, and Audit Logging.
- Scaffold the Temporal cluster and Python workflow-worker skeleton.

### Build Gate 3: Agent Gateway and Shared Surfaces Foundation
**Objective**: Create one intelligent operator across PWA and Telegram.
- Build the Python Agent Gateway context assembly and Pi orchestration boundary.
- Establish the PWA chat shell and the Telegram Bot/Mini App interfaces.
- Implement permission and confirmation policies for high-impact commands.

### Build Gate 4: Full Brand Genesis
**Objective**: Onboard a brand into a locked creative universe.
- Build the Client Intake and Consent workflows (including explicit Voice-Clone consent).
- Integrate GPT Image 2, Flux 2 Klein 9b, and specific approved providers for the batch generation of the 64-cell Acting Library.
- Implement ImageCritic for auto-QC of generated assets.
- Integrate Qwen-Image-Layered and SAM3 adapters for the Paper-Cut Rig generation.
- Implement the Genesis Clearance Certificate and Brand Context Version lock.

### Build Gate 5: Research and Interview Intelligence
**Objective**: Make the application improve interviewing before any editing begins.
- Build the Guest Dossier and Audience Reality Brief compilers.
- Implement the Context Premise workflow and the Evidence Critic.
- Implement the Matrix of Edging state map and the DSPy Interview Asset Contract compiler to generate the live interview deck.

### Build Gate 6: Complete Expression Sessions
**Objective**: Capture, synchronize, extract, and evaluate authentic expression.
- Implement transcript provider integration and precise timestamp alignment.
- Implement anchor hit detection and deterministic expression moment extraction.
- Map extracted moments to Archetype Routes and generate the Asset Package Spec.

### Build Gate 7: Complete CMF Production
**Objective**: Compile approved expression into every required production route.
- Implement the Complete Editing Session container and SceneSpec compilation.
- Implement deterministic render routes using Remotion (Personal-Brand Commentary, Paper-Cut Explainer, Carousels).
- Implement generative/special routes (SCAIL-2 motion transfer).
- **Implement the Voice-DNA Boost Insert pipeline**: Integrate LavaSR for audio restoration and MOSS-TTS for synthetic bridge generation, governed by the SemanticCritic and VoiceContinuityCritic.

### Build Gate 8: Review, Telegram Cockpit, and Publishing
**Objective**: Operate the whole system from the PWA and on the move.
- Build the production boards, render comparison screens, and Telegram notification routing.
- Implement approval events and the Publishing Intent object.
- Deploy the Publer API adapter for draft scheduling and status synchronization.

### Build Gate 9: Memory, Hardening, and Operational Readiness
**Objective**: Make the system safe, sustainable, and capable of learning.
- Implement Brand Memory and Interviewer Memory updates.
- Implement the Neo4j rebuildable relationship projection for deep relationship querying.
- Conduct penetration testing, restore drills, and provider outage fallback tests.
- Complete the Final Human Acceptance Gate: The Operator must complete one real brand cycle from onboarding to publishing without manual database edits.

---

## 7. Risks, Constraints, and Governance

### 7.1 Contract Precision Bottleneck
Because the system is designed to allow agents to self-correct based on Operator feedback, the system scales only if the underlying Pydantic contracts and DSPy program schemas are incredibly precise. Vague contracts will result in endless regeneration loops and Operator burnout. **Mitigation**: Rigid enforcement of the Registry Validation Bundle; no schema goes live without a corresponding evaluation rubric.

### 7.2 Voice DNA Training Data Quality Decay
Voice cloning models (MOSS-TTS) are highly sensitive to input quality. If an interview recorded on a noisy phone line or a highly compressed Zoom call is fed into the Voice DNA trainer, the resulting synthetic bridge inserts will sound metallic and ruin authenticity. **Mitigation**: Mandatory integration of LavaSR as a preprocessing gate. Any audio falling below the restoration threshold is permanently barred from the Voice DNA training pool.

### 7.3 Visual Style Drift
The entire premise of Brand Genesis is that the brand's visual identity is locked. However, subsequent generations (e.g., creating a new specific prop using Flux 2 Klein 9b) risk drifting away from the core aesthetic of the 2.5D Paper-Cut style. **Mitigation**: ImageCritic operates as a hard gate. All new generated visual assets must pass an automated style-consistency check against the locked Brand Context v1 reference images before they can be used in a SceneSpec.

### 7.4 Multi-Source Composition Coherence
When the CMF factory stitches together a video from five different source recordings taken months apart, the resulting asset can feel disjointed due to jarring shifts in pacing, vocal energy, and emotional register. **Mitigation**: The deployment of the `VoiceContinuityCritic` alongside the `SemanticCritic`. This evaluator specifically scores cross-segment coherence. When a jarring cut is detected, the system mandates a Voice-DNA Boost Insert or an Editorial visual cutaway to smooth the psychological transition for the audience.

### 7.5 Synthetic Voice Ethical & Architectural Exemption (ADR Required)
The foundational CCF V5 Sound Doctrine strictly prohibits synthetic voice from delivering a coach's primary message. The introduction of MOSS-TTS creates a policy conflict. **Mitigation**: The implementation of `ADR-002: Voice-DNA Boost Insert Exception`. This explicitly limits synthetic voice generation to structural bridges, context setups, and clarifying connectors, hard-capped at 7 seconds or 15% of the video duration, requiring visual covering and provenance B-flags. Legal and consent exposure is managed externally via client relationship agreements.

### 7.6 Legacy Migration Drift
The legacy repository contains valuable doctrine and working mechanics, but also scattered scripts, old service boundaries, shell-coupled modules, disjointed TypeScript shells, and monolithic prompts. The risk is that implementation teams import legacy modules directly to save time, causing the greenfield architecture to inherit hidden dependencies and untyped state. **Mitigation**: Build Gate 0 migration ledger enforcement, content hashing, reviewer approval, explicit Pydantic/DSPy migration targets, fixture/eval requirements, and CI checks that prevent direct legacy runtime imports into production packages.

### 7.7 Spec Governance Drift
Because CMF STUDIO is built from dense legacy doctrine, multiple spec files, and orchestration-bearing modules, downstream documents can drift by preserving feature names while losing causal order. **Mitigation**: Product Brief, PRD, architecture, epics/stories, and tech specs must pass MCDA/spec-quality evaluation before being treated as frozen. Each eval must score legacy inventory fidelity, pipeline clarity, contract traceability, full-system completeness, evaluation/governance strength, and implementation specificity.

---

## 8. Deep Architectural Specifications (Appendix A)

To ensure this brief provides complete context for the engineering build, the following section details the exact structural contracts and specific primitives that power the CMF STUDIO factory. These are not conceptual outlines; they are the literal architectural blueprints that the DSPy and Pydantic layers must execute.

### 8.1 The Matrix of Edging Primitives in Detail

The Primitive Pass (Stage 4 of the Matrix of Edging) relies on detecting and utilizing specific meaning transforms. The DSPy signatures must be trained to extract these from the raw transcript.

**1. Irony Inversion**
- **Definition**: Exposing the contradiction between what is widely believed and what is actually true based on the guest's lived experience.
- **System Task**: The system searches the transcript for statements where the guest says "People think X, but the reality is Y."
- **Archetype Route**: Highly effective for the *Myth Debunk* and *Challenger/Frame Breaker* archetypes.

**2. Tribal Reference**
- **Definition**: Language, symbols, or shared grievances specific to a niche subculture.
- **System Task**: The system uses the Audience Reality Brief to score the guest's language against known tribal markers. 
- **Archetype Route**: Powers the *Meme Observation* and *Personal-Brand Commentary* archetypes.

**3. What-Is vs. What-Could-Be**
- **Definition**: The structural gap between the painful current reality of the audience and the liberated future state.
- **System Task**: Identifying sequential statements where the guest describes a point of failure followed immediately by a principle of success.
- **Archetype Route**: The foundation of the *Before vs After Contrast* and *Transformation Story* archetypes.

**4. The Analogy Bridge**
- **Definition**: Using a concrete, physical-world example to explain a complex, abstract concept.
- **System Task**: Detecting phrases like "It's like when you..." or "Imagine a..." within the transcript.
- **Archetype Route**: Essential for the *Paper-Cut Explainer* and *Core Educator* archetypes.

**5. Stakes as Personal Why**
- **Definition**: Connecting a high-level business or philosophical point directly back to the guest's deepest personal pain or motivation.
- **System Task**: Identifying emotional shifts (detected via VoiceContinuityCritic pitch/pacing analysis or text sentiment) where the guest drops the corporate mask and speaks intimately.
- **Archetype Route**: The core of the *Cinematic Story* and *Thought Whisperer Extract*.

### 8.2 The Brand Genesis Paper-Cut Avatar Rig Specifications

The Paper-Cut style is the signature aesthetic of CMF STUDIO. It relies on a rigorous, programmatic decomposition of source imagery.

**Layer Separation (Qwen-Image-Layered & SAM3)**
When the Brand Genesis workflow generates the 64-state acting library, it cannot simply save flat JPEGs. The system must process each image through semantic segmentation:
1. **Background Removal**: Isolating the subject completely.
2. **Head/Body Separation**: Severing the head from the torso to allow for programmatic nodding, tilting, and Bobble-head physics in Remotion.
3. **Facial Feature Extraction**: Using SAM3 (Segment Anything Model) to precisely isolate eyebrows, pupils, and mouth shapes. 
4. **The Rig Manifest**: The final output is not just an image folder, but a JSON `RigManifest` that defines the exact pivot points (anchor coordinates) for the neck, shoulders, and jawline. 

This allows the CMF Render engine to take a static generated image and make it "speak" and react dynamically to the audio track, without having to run expensive, non-deterministic video generation models for every frame.

### 8.3 Pydantic Contract Boundaries

The Python-first architecture strictly enforces state through Pydantic. Here is the operational logic for the core objects:

**The `BrandContextVersion` Object**
This object is strictly immutable once locked. It contains the hashes of the 64-state acting library, the `RigManifest`, the approved `VoiceDNA` model pointer, and the `MicroSemioticAnchor` dictionary. Render jobs only ever accept a locked version hash. If the operator decides to change a prop (e.g., replacing the "budget socks" with "luxury shoes"), a new `BrandContextVersion` must be generated, reviewed by ImageCritic, and explicitly locked.

**The `InterviewAssetContract` Object**
Generated by the Research & Context Engine before the interview, this object dictates the interview's structure. It lists the exact questions to ask, the required `FirstLineAnchor` for each, and the intended `ArchetypeRoute`. During the interview, the Operator's UI (Telegram Cockpit or PWA) reads this contract to prompt the Operator on what to ask next and how to steer the guest.

**The `CompleteEditingSession` Object**
This is the master compilation receipt. It joins the extracted audio moment (`ExpressionMomentID`), the archetype structural instructions (`ArchetypeRoute`), the visual instructions (`SceneSpec`), and the visual assets (`BrandContextVersion`). It is this object that is sent to the Remotion or Motion Canvas renderer.

### 8.4 DSPy Evaluation and Calibrated Receipts

In legacy systems, LLM evaluation was done via massive prompts ending with "Rate this from 1 to 10." In CMF STUDIO V2, evaluation is programmatic and calibrated using DSPy signatures.

**SemanticCritic (DSPy Module)**
- **Inputs**: The source transcript, the extracted moment, the Archetype Contract.
- **Task**: Determine if the extracted moment fulfills the promise of the Archetype Contract without altering the factual truth of the source transcript.
- **Output**: A strict JSON evaluation receipt with floating-point confidence scores. A score below 0.85 triggers the Voice-DNA Boost Insert workflow (if the failure is structural bridging) or outright rejection (if the failure is factual drift).

**ImageCritic (HVision-NKU Integration)**
- **Inputs**: The generated 64-state image, the original client reference photo, the style guide negative prompt.
- **Task**: Score likeness (does this look like the client?), gesture clarity (is the hand pointing correctly?), and style adherence (does this look like a paper-cut, or did it drift into photorealism?).
- **Output**: Generates targeted repair prompts (e.g., "The fingers on the left hand are blended; apply localized inpainting").

**VoiceContinuityCritic (Audio Evaluation)**
- **Inputs**: The raw source audio file, the generated MOSS-TTS audio file, the composite mixed track.
- **Task**: Evaluate prosody matching, background noise continuity, and pacing. 
- **Output**: A pass/fail flag. If failed, it adjusts the `speech_rate` and `pitch_contour` parameters and requests a regeneration from MOSS-TTS.

### 8.5 The Operator Cockpit Workflow (Telegram Integration)

The system must support high-velocity operations without trapping the Operator at a desktop workstation.

1. **The Notification**: When a `CompleteEditingSession` finishes rendering, the Python command bus fires an event.
2. **The Delivery**: The Telegram Bot receives the event and sends a compressed preview video directly to the Operator's chat, along with the `EvaluationReceipt` summary.
3. **The Micro-Action**: The Operator can reply directly in the chat with inline commands:
   - `/approve`: Locks the asset and queues it in Publer.
   - `/reject [reason]`: Sends the asset back to the DSPy agents with the reason appended to the `SceneSpec`.
   - `/boost [instruction]`: Explicitly triggers the Voice-DNA Boost Insert if the Operator feels the pacing is off, bypassing the automated trigger.
4. **The Deep Work Transition**: If the asset requires structural changes, the Operator clicks a deeply-linked URL in the Telegram message that opens the specific `CompleteEditingSession` in the Next.js PWA Control Tower, bringing the exact state into the desktop environment without losing context.

This workflow guarantees that the Operator remains the final arbiter of taste and truth, while the agents handle the heavy lifting of generation, rendering, and QC.

---
**END OF PRODUCT BRIEF**
