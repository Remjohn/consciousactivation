# CCP Studio V2 — Agent Start Here

**Canonical package:** CCP Studio Greenfield Agent Context V2 — Python / Pydantic / DSPy / Pi Runtime  
**Intended reader:** Pi Coding Agent, specialist coding agents, architecture reviewers, and the human operator  
**Status:** authoritative build contract  
**Product:** CCP Studio, including Brand Genesis, Research and Context Engineering, Interview Intelligence, Complete Expression Sessions, Conscious Media Factory production, Telegram operator cockpit, publishing, and learning memory  
**Read order:** this file → `04_ADR_001_PYTHON_PYDANTIC_DSPY_PI_RUNTIME.md` → `01_CCP_STUDIO_GREENFIELD_MASTER_SPEC.md` → `02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` → `03_IMPLEMENTATION_SEQUENCE_AND_RELEASE_GATES.md` → `05_LEGACY_MIGRATION_AND_REPOSITORY_DIRECTIVE.md`

---

## 1. Mission

Build a greenfield, production-grade, multi-brand agentic application that transforms researched, authentic human expression into coherent, reusable, evaluated, approved, and publishable media.

The application is **not only an editor**. Its complete operating chain is:

```text
Brand Genesis
→ Research and Context Engineering
→ Context Premise Formation
→ Interview Intelligence
→ Complete Expression Session
→ Expression Moment Extraction
→ Archetype and Asset Routing
→ Complete Editing Sessions
→ CMF Composition / Animation / Rendering
→ Evaluation and Human Approval
→ Publishing
→ Brand, Interviewer, and Route Memory
```

The human interviewer creates the shared field. The system researches, prepares, observes, structures, retrieves, compiles, renders, evaluates, remembers, and routes.

The central engineering truth is:

> CCP Studio is a Python-first agentic harness with TypeScript presentation and rendering surfaces. It is not a TypeScript SaaS application with Python utilities.

---

## 2. Canonical Runtime Decision

The source-of-truth runtime is:

```text
Python
+ Pydantic v2 contracts
+ DSPy programs and evaluations
+ Pi Coding Agent orchestration
+ FastAPI application boundary
+ durable workflows and typed commands
```

TypeScript is intentionally restricted to the runtimes where it is naturally required:

```text
Next.js PWA
Telegram Mini App
Remotion renderer
Motion Canvas renderer
browser preview components
generated contract consumers
```

The contract direction is one-way:

```text
Pydantic models
→ JSON Schema / OpenAPI
→ generated TypeScript types
→ optional generated Zod validators
→ PWA, Mini App, and renderer consumption
```

TypeScript and Zod do **not** define canonical business contracts.

---

## 3. Non-Negotiable Architecture Decisions

1. **Greenfield runtime.** The legacy repository is read-only reference material and a migration source. No legacy runtime dependency is allowed.
2. **Python owns the Harness.** Domain contracts, registry logic, agent orchestration, workflow commands, evaluation, provider routing, receipts, and publishing policy live in Python.
3. **Pydantic owns semantic contracts.** Every command, event, registry entry, workflow input, provider request, and receipt is represented by a versioned Pydantic model.
4. **DSPy owns structured reasoning programs.** Research synthesis, Context Premise formation, Interview Asset Contract compilation, extraction, routing, and calibrated evaluation are DSPy modules/signatures where appropriate.
5. **Pi Coding Agent is the primary orchestrator.** Pi plans and coordinates work through approved tools, DSPy programs, commands, and workflows. Pi does not directly mutate databases or become the persistence layer.
6. **Durable workflow state is separate from agent state.** Temporal or an equivalent Python-compatible workflow engine owns long-running execution, retries, signals, and resumability.
7. **Registry-first.** Existing large registries must be migrated into versioned Pydantic contracts before feature code depends on them.
8. **Brand-scoped everything.** Every mutable production object carries `organization_id`, `brand_id`, and the applicable `brand_context_version_id`.
9. **Versioned context.** Render and interview jobs never read floating “latest” identity or style data. They use frozen context snapshots.
10. **One agent, multiple surfaces.** PWA chat, Telegram bot, Telegram Mini App, and live-interview cues use the same Python Agent Gateway, thread model, tool registry, and permissions.
11. **Typed commands, not invisible autonomy.** The agent proposes or executes schema-validated Pydantic commands. High-impact actions require human confirmation.
12. **Human truth before production.** Research, Context Premises, Interviewer Resonance, Matrix of Edging, Narrative State Induction, First-Line Anchors, and Depth Anchors precede editing.
13. **Complete Expression Session before Complete Editing Session.** One human expression event may produce many downstream media jobs.
14. **Orchestration over generation.** Each model has a narrow capability contract. No model is treated as a universal creative engine.
15. **Deterministic identity substrate.** Identity conditioning model versions are pinned to worker image digests; approved reference assets are immutable and hash-addressed.
16. **Batch-first compute.** GPU workers start for queued batches, checkpoint each asset, upload receipts, and terminate. Do not run idle GPU infrastructure.
17. **No one-tap public publishing.** CMF approves first; Publer publishes second; public scheduling/publishing requires confirmation.
18. **Authentic primary voice.** The coach or guest’s primary message uses authentic recorded audio. Synthetic voice must not impersonate the primary speaker.
19. **No public half-release.** Internal increments are allowed; public release occurs only after the Production Release Gate in document 03 passes.

---

## 4. Product Naming and Module Boundaries

The full application is **CCP Studio**.

`CMF` remains the production subsystem, not the whole product.

```text
CCP Studio
├── Python Harness Runtime
│   ├── Pydantic Contract Kernel
│   ├── Registry Kernel
│   ├── DSPy Program Registry
│   ├── Pi Orchestrator
│   ├── Command Bus
│   ├── Workflow Runtime
│   └── Evaluation / Receipt Chain
├── Brand Genesis
├── Research & Context Engine
├── Interview Intelligence Studio
├── Complete Expression Sessions
├── CMF Production
├── Review & Approval
├── Publishing
├── Brand / Interviewer Memory
└── Agent Gateway
```

The primary PWA is the **CCP Studio Control Tower**.

Telegram is the **Agentic Operator Cockpit**:

- bot: notifications, conversational commands, approval requests;
- Mini App: preview, contextual chat, lightweight review actions;
- same Python Agent Gateway and same thread state as the PWA.

---

## 5. Immediate Agent Boot Sequence

Do not begin by building UI screens.

Execute in this order:

1. Freeze and inventory the legacy repository.
2. Create a read-only registry/source map and migration ledger.
3. Approve `ADR-001` establishing Python, Pydantic, DSPy, and Pi as the Harness runtime.
4. Scaffold the Python-first hybrid monorepo exactly as described in the master specification.
5. Implement the Pydantic contract kernel and JSON Schema export.
6. Implement generated TypeScript contract output for the PWA, Telegram Mini App, and Remotion.
7. Implement the registry kernel and migrate representative entries from every registry family.
8. Implement DSPy program contracts, evaluation fixtures, and program-version metadata.
9. Implement tenant/brand scoping, audit logging, idempotency, domain events, and the Python command bus.
10. Implement the Agent Gateway and Pi orchestration boundary.
11. Implement durable workflow skeletons before connecting external model providers.
12. Implement Brand Genesis end to end.
13. Implement Research, Interview Intelligence, and Complete Expression Sessions.
14. Implement CMF production routes and provider adapters.
15. Implement PWA, Telegram bot, and Mini App as surfaces over the same backend.
16. Implement publishing, learning loops, evaluation, failure recovery, and release hardening.
17. Do not publicly launch until all release gates pass.

Before substantive feature work, produce:

```text
docs/migration/legacy-inventory.md
docs/migration/registry-source-map.md
docs/migration/migration-ledger.md
docs/adr/ADR-001-python-pydantic-dspy-pi-runtime.md
docs/adr/ADR-002-greenfield-runtime.md
docs/adr/ADR-003-registry-kernel.md
docs/adr/ADR-004-brand-context-versioning.md
docs/adr/ADR-005-agent-command-bus.md
docs/adr/ADR-006-durable-workflows.md
docs/adr/ADR-007-provider-adapters.md
docs/adr/ADR-008-tenant-isolation.md
docs/adr/ADR-009-publishing-safety.md
```

---

## 6. What the Agent Must Never Do

- Never make TypeScript, Zod, React state, or Remotion props the source of truth for domain semantics.
- Never invent missing registry content without marking it as a proposal.
- Never mutate an approved or locked Brand Context Version.
- Never use unapproved identity references in production.
- Never call provider SDKs directly from domain logic.
- Never let Pi, DSPy, or any LLM write directly to production tables.
- Never use Pi conversation history as workflow persistence.
- Never publish content because a model classified it as safe.
- Never hide workflow state in chat history.
- Never conflate expression states with content archetypes.
- Never treat Ideogram output as the canonical final text layer.
- Never treat Qwen-Image-Layered as a rigging engine or SAM3 as a semantic layer-stack generator.
- Never over-script a guest or falsify a landing.
- Never allow Telegram UI state to become the system of record.
- Never import legacy runtime code to save time.
- Never omit receipts, provenance, or audit events from production actions.

---

## 7. Definition of Success

The finished application can:

1. onboard a brand and manufacture a locked creative universe;
2. prepare the operator to conduct a better interview through research and context engineering;
3. assist during the interview without replacing human presence;
4. convert one Complete Expression Session into traceable expression moments and asset routes;
5. render coherent assets across all required CMF routes;
6. review and revise from PWA or Telegram using the same agent;
7. safely schedule approved content through Publer;
8. retain the brand’s visual, linguistic, narrative, and performance memory across future sessions;
9. recover from workflow or worker failure without losing completed work;
10. prove every output’s lineage from source truth to publication;
11. regenerate all frontend and renderer types from Pydantic without semantic drift;
12. replace a model provider without rewriting domain rules.

Read the ADR and master specification in full before implementation.

---

# ADR-001 — Python, Pydantic, DSPy, and Pi as the CCP Studio Harness Runtime

**Status:** Accepted  
**Decision owner:** CCP Studio architecture  
**Applies to:** all greenfield runtime code, registry migration, agents, workflows, provider adapters, evaluation, and publishing  
**Supersedes:** the TypeScript-first default in CCP Studio Greenfield Agent Context V1

---

## 1. Context

CCP Studio is not a conventional CRUD SaaS application with optional AI features. It is a schema-driven agentic production Harness responsible for:

- Brand Genesis and immutable Brand Context Versions;
- large archetype, derivative, reaction, render-mode, primitive, and evaluation registries;
- research and Context Premise formation;
- Interviewer Resonance and Matrix of Edging;
- Interview Asset Contract compilation;
- Complete Expression Sessions and expression-moment extraction;
- Complete Editing Sessions and CMF routing;
- provider selection, evaluation receipts, approval, publishing, and memory;
- long-running batch and human-in-the-loop workflows.

The existing system gravity is Python-oriented:

- Pydantic contracts;
- DSPy reasoning and compilation pipelines;
- Python agents and emotional/semantic models;
- Pi Coding Agent as the intended primary orchestrator;
- large registries and evaluation logic that already map naturally to typed Python objects.

A previous greenfield specification defaulted to TypeScript, Zod, NestJS/Fastify, and Drizzle. That default would force the core intelligence to cross a language boundary, duplicate contracts, weaken the existing Harness, and relegate Pi/DSPy to secondary utilities.

---

## 2. Decision

CCP Studio will use a **Python-first Harness runtime**.

### Canonical runtime

```text
Python
+ Pydantic v2
+ DSPy
+ Pi Coding Agent
+ FastAPI
+ SQLAlchemy/Alembic
+ Temporal Python SDK
```

### Controlled TypeScript runtimes

```text
Next.js PWA
Telegram Mini App
Remotion
Motion Canvas
browser preview components
```

TypeScript is a presentation and rendering runtime. It is not the source of truth for domain semantics or orchestration.

---

## 3. Contract Authority

The authoritative chain is:

```text
Pydantic models
→ JSON Schema
→ OpenAPI
→ generated TypeScript types
→ optional generated Zod validators
→ UI and renderer consumption
```

Rules:

1. All domain objects, commands, events, workflows, registry entries, provider jobs, render contracts, and receipts originate as Pydantic models.
2. Generated TypeScript artifacts are not edited by hand.
3. Zod is permitted for generated or UI-local validation only.
4. SQLAlchemy models map persistence and do not redefine business semantics.
5. Contract drift fails CI.

---

## 4. Pi Coding Agent Role

Pi is the primary behind-the-scenes orchestrator.

Pi receives a scoped `AgentExecutionContext` containing:

- authenticated actor and permissions;
- organization and brand;
- frozen Brand Context Version;
- active expression/editing/publishing object;
- relevant registry bundle;
- approved tools and DSPy programs;
- cost, consent, provider, and publishing policies.

Pi may plan, retrieve, call approved tools, invoke DSPy programs, propose commands, coordinate specialist agents, request confirmation, and repair failed workflows.

Pi may not:

- write directly to business tables;
- invent command types outside the registry;
- bypass confirmation or policy;
- mutate locked context;
- use conversation history as durable workflow state;
- publish directly.

Every state-changing action passes through a Pydantic `AgentCommand` and the Command Bus.

---

## 5. DSPy Role

DSPy is the structured reasoning/program layer, not the database or workflow engine.

Representative DSPy programs include:

- `ResearchSynthesisProgram`;
- `ContextPremiseCompiler`;
- `ContextPremiseAdversary`;
- `InterviewerResonanceCompiler`;
- `InterviewAssetContractCompiler`;
- `ExpressionMomentExtractor`;
- `ArchetypeRouteCompiler`;
- `SceneSpecCompiler`;
- `ReferenceSelectionProgram`;
- `EvaluationProgram`;
- `RepairProposalProgram`.

Every production program has a pinned version, typed inputs/outputs, evaluation set, threshold, provider policy, and fallback.

A DSPy result is never trusted solely because it parses. It must pass Pydantic validation, grounding checks, business rules, and the applicable human gate.

---

## 6. Durable Workflow Boundary

Pi and DSPy decide and compile. Temporal or an approved equivalent persists execution.

Durable workflows own:

- retries;
- timers;
- human approval waits;
- batch fan-out/fan-in;
- provider polling;
- resumability;
- cancellation;
- compensation;
- workflow versioning.

This separation prevents agent reasoning state from becoming operational state.

---

## 7. TypeScript Boundary

TypeScript applications may:

- display and edit drafts;
- call Python APIs;
- submit typed command requests;
- preview assets;
- render a versioned `RenderContract`;
- stream progress and agent responses.

They may not own:

- Brand Context semantics;
- registry compatibility;
- archetype routing;
- identity selection policy;
- Context Premise logic;
- evaluation thresholds;
- approval policy;
- public publishing authority.

Remotion is an execution target. The Python CMF engine compiles the render contract; Remotion renders it.

---

## 8. Repository Consequences

The repository must have a Python application nucleus and isolated TypeScript leaf apps.

The old repository remains read-only reference material. Legacy registries are migrated to Pydantic entries and fixtures rather than rewritten as TypeScript source objects.

---

## 9. Operational Consequences

Benefits:

- preserves existing Python intelligence;
- makes Pydantic contracts and DSPy programs first-class;
- allows Pi to orchestrate without crossing a Node service boundary;
- reduces semantic duplication;
- keeps frontend and Remotion development idiomatic;
- makes providers replaceable;
- keeps durable state outside chat and model traces.

Costs:

- requires generated contract tooling between Python and TypeScript;
- requires disciplined cross-runtime integration tests;
- requires separate dependency management for Python and TypeScript leaf apps;
- requires clear renderer contracts.

These costs are accepted.

---

## 10. Compliance Test

A contribution violates this ADR if any answer is “yes”:

- Does a TypeScript interface define a canonical domain object not generated from Pydantic?
- Does an LLM or Pi write directly to the database?
- Does a DSPy program return unvalidated state-changing payloads?
- Does a renderer decide business routing or publishing policy?
- Does chat history contain the only copy of workflow state?
- Does domain code import a provider SDK directly?
- Does the legacy runtime become a production dependency?

---

## 11. Final Rule

> CCP Studio is a Python-first agentic Harness with TypeScript surfaces and renderers. Pi orchestrates; DSPy compiles reasoning; Pydantic governs contracts; durable workflows execute; humans approve consequential actions.

---

# CCP Studio V2 — Greenfield Python-First Agentic Application Master Specification

## Brand Genesis, Interview Intelligence, Complete Expression Sessions, Conscious Media Factory, Agentic Telegram, Publishing, and Learning Memory

**Document type:** canonical product, domain, systems, and engineering specification  
**Project:** Conscious Coaching Platform / Conscious Rivers / Conscious Media Factory  
**Application name:** CCP Studio  
**Version:** 2.0 — Python / Pydantic / DSPy / Pi implementation context  
**Status:** authoritative build contract; supersedes the V1 TypeScript-first runtime assumption  
**Primary audience:** Pi Coding Agent, specialist coding agents, architecture reviewers, human operator  
**Supersedes for implementation:** fragmented implementation assumptions spread across CCP V5, V8, V9, V9.1, CMF Creative Pipeline V2, CMF Brand Genesis V3, and the Archetype Migration Proposition  
**Preserves:** the philosophical, interview, registry, creative, evaluation, and identity doctrines from those documents

---

# 0. Canonical Position

CCP Studio is a multi-brand, research-grounded, interview-first, agentic creative operating system.

It is not:

- a generic AI editor,
- a social scheduler with AI features,
- a collection of prompts,
- a Telegram bot with hidden state,
- a ComfyUI wrapper,
- a video-template factory,
- or a client portal that begins with software onboarding.

It is a stateful production harness that helps the operator:

1. understand a brand and its audience;
2. manufacture a reusable, versioned creative universe;
3. research guests, topics, cultural context, and live audience tensions;
4. become a better interviewer through context engineering and structured preparation;
5. capture authentic human expression;
6. extract high-value expression moments without distorting their meaning;
7. route those moments through typed content and media registries;
8. compile them into coherent visual assets;
9. evaluate and approve outputs;
10. publish safely;
11. learn from every interview, revision, render, and post.

The complete system chain is:

```text
Brand Genesis
→ Brand Context Lock
→ Research Field
→ Context Premise Formation
→ Interviewer Pre-Induction
→ Interview Asset Contracts
→ Complete Expression Session
→ Expression Moment Extraction
→ Archetype / Derivative / Render Routing
→ Complete Editing Sessions
→ Composition / Asset Retrieval / Animation / Rendering
→ Evaluation
→ Human Approval
→ Publishing
→ Brand + Interviewer + Route Memory
```

The interview is the source event. Editing is the visible phenotype of captured expression.

The Harness runtime is explicitly Python-first:

```text
Pydantic contracts
→ DSPy programs
→ Pi Coding Agent orchestration
→ typed commands and durable workflows
→ provider workers and deterministic renderers
```

TypeScript remains a controlled leaf runtime for the PWA, Telegram Mini App, Remotion, Motion Canvas, and browser preview components. It does not own domain contracts, registry semantics, agent policy, workflow state, evaluation, or publishing authority.

---

# 1. Source Doctrine and Reconciliation

This document consolidates several prior architectural lines.

## 1.1 V5: The Harness Is the Product

The new runtime preserves the V5 execution law:

> Intelligence is only valuable when expressed through a testable orchestration harness.

Repeatable mechanics must exist as typed schemas, executable tools, durable workflows, evaluations, and receipts. Prompt prose may inform a compiler, but cannot itself be the production architecture.

V5’s Complete Editing Session remains the atomic downstream media-production boundary.

## 1.2 V9: Interview-First Expression

V9 changed the launch center of gravity:

```text
Activation
→ Articulation
→ Asset Creation
→ Narrative Memory
→ Product Expansion
```

The system begins with a meaningful conversation, not with forcing the client into Telegram or asking them to understand a content-production system.

The human interviewer creates the relational field. The backend multiplies what becomes expressible inside it.

## 1.3 V9.1: Operational Capture

V9.1 makes the interview executable:

- every interview is a Complete Expression Session;
- every content-intended question is an Interview Asset Contract;
- every answer may yield one or more Expression Moments;
- every route becomes a Complete Editing Session;
- every output receives an Evaluation Receipt.

## 1.4 Archetype Migration: Schemas Replace Prompt Monoliths

The old prompt stack contains valuable intelligence but combined too many concerns.

The new system separates:

```text
meaning structure
≠ asset packaging
≠ meme mechanism
≠ reaction form
≠ render mode
≠ evaluation
```

The five mandatory content registries are:

1. Core Content Archetypes;
2. Asset Derivative Schemas;
3. Meme Mechanism Schemas;
4. Reaction Archetype Schemas;
5. CMF Render Mode Schemas.

## 1.5 CMF V2/V3: Creative Harness and Brand Genesis

The media system is model-agnostic and renderer-agnostic.

The new missing upstream creative object is Brand Genesis:

```text
Brand Genesis Session
→ Brand Context Version
→ reusable creative libraries
→ future expression sessions
→ coherent outputs
```

Onboarding is not administrative setup. It is the manufacturing of the client’s reusable creative universe.

## 1.6 Reconciliation of Telegram Doctrine

There is no contradiction between “Telegram comes later for clients” and “Telegram is a first-class application surface.”

The release doctrine is:

- clients are not forced into Telegram before experiencing value;
- the operator can use Telegram from the beginning;
- a client may later receive limited preview/chat access;
- Telegram never owns canonical state;
- the PWA and Telegram use the same Agent Gateway and domain backend.

## 1.7 Runtime Reconciliation: Python Owns the Harness

Earlier greenfield notes defaulted to a TypeScript-first SaaS stack. That default is rejected because it conflicts with the existing and intended CCP computational substrate:

- Pydantic domain contracts;
- DSPy signatures, modules, optimizers, and evaluations;
- Python-based emotional, archetype, and orchestration logic;
- Pi Coding Agent as the primary behind-the-scenes orchestrator;
- a large Python-oriented registry and agent estate.

The corrected doctrine is:

```text
Python / Pydantic / DSPy / Pi
= Harness, contracts, orchestration, evaluation, workflows, provider policy

TypeScript / React / Remotion
= operator surfaces, browser interaction, and deterministic video rendering
```

The new runtime may preserve TypeScript where the target technology requires it, but TypeScript may not become a competing source of business truth.

---

# 2. Governing Laws

These laws override implementation convenience.

## Law 1 — Human Activation Remains the Source

The system can research, prepare, cue, structure, render, evaluate, and remember. It cannot replace the human relationship that produces genuine disclosure, conviction, humor, insight, or change.

## Law 2 — Truth Before Asset Yield

Do not force an answer into an asset because a deliverable quota exists. The source expression must remain truthful, dignified, and contextually intact.

## Law 3 — Negative Space Precedes Positive Generation

Every linguistic, visual, and behavioral generation task must load the applicable negative-space constraints first.

Negative Space includes:

- words the brand would never use;
- claims the brand cannot responsibly make;
- visual clichés;
- forbidden aesthetics;
- identity distortions;
- manipulative emotional tactics;
- unwanted stereotypes;
- motion styles that make the brand feel childish;
- unsafe or misleading health, legal, financial, or psychological claims.

## Law 4 — Every Question Is a Contract

A content-intended question is represented by an Interview Asset Contract with:

- target expression states;
- target archetypes;
- First-Line Anchors;
- Depth Anchors;
- expected source material;
- repair follow-ups;
- clip-start logic;
- landing evaluations;
- potential asset routes.

## Law 5 — First Line Steers; Depth Prevents Centroid; Landing Is Evaluated

The first line creates a clean start and expression lane. The Depth Anchor resists generic abstraction. The landing remains open to authentic discovery.

## Law 6 — Context Premises Are Explicit and Temporary

A Context Premise is an evidence-backed working hypothesis, not a hidden assumption or permanent truth. It carries provenance, confidence, expiry, and question implications.

## Law 7 — Expression States Are Not Archetypes

Expression states induce how a person speaks. Archetypes define the repeatable meaning structure of the resulting content.

Correct:

```text
Expression State
→ Archetype Route
→ Asset Derivative
→ CMF Render Mode
```

Incorrect:

```text
Expression State = Asset Type
```

## Law 8 — Assets Are Compiled, Not Randomly Generated

Every output is traceable to:

- source evidence or expression;
- brand context version;
- registry bundle version;
- selected archetype and derivative;
- selected visual assets;
- provider/model versions;
- workflow and renderer versions;
- human approval event.

## Law 9 — Identity Is Compiled, Not Improvised

Production identity uses:

- fixed identity-conditioning stack versions pinned to the worker container;
- approved reference assets in object storage;
- immutable hashes;
- approved runtime selection logic.

The runtime agent may retrieve and select; it may not mutate the identity substrate.

## Law 10 — Models Are Replaceable Capabilities

Domain logic calls provider interfaces, never model-specific SDKs.

No architectural decision may depend on one vendor retaining a feature forever.

## Law 11 — Human Review Is a Product Feature

Identity assets, avatar rigs, micro-semiotic anchors, sensitive expression routes, final renders, and public publishing all have explicit review gates.

## Law 12 — One Agent, Multiple Surfaces

PWA, Telegram Bot, Mini App, and Live Interview mode are context surfaces over one Agent Gateway. They do not create independent agent memories.

## Law 13 — Workflow State Is Not Chat State

All durable progress lives in domain objects and workflows. Chat can reference state but cannot substitute for it.

## Law 14 — GPUs Are Summoned, Not Parked

Expensive model workers run batch jobs, checkpoint each unit, upload results, write receipts, and stop.

## Law 15 — Every Session Trains the System

Each completed session updates, after approval:

- guest/client profile;
- interviewer profile;
- context-premise performance;
- anchor success;
- depth-anchor success;
- archetype fit;
- edge survival;
- asset route performance;
- composition preferences;
- micro-semiotic anchor performance;
- motion and SFX preferences;
- publishing performance.

## Law 16 — No Public Half-Release

Implementation proceeds in internal waves. Public release is blocked until the full production release gate passes.

## Law 17 — Contract Authority Flows From Python

Pydantic models are the canonical semantic contracts for the application. JSON Schema, OpenAPI, generated TypeScript types, optional Zod validators, database mappings, workflow payloads, and renderer props are projections of those contracts.

Pi and DSPy may reason over, propose, and compile those contracts. They may not bypass them.

---

# 3. Product Scope

## 3.1 In Scope

CCP Studio must include:

### Brand and Tenant Operations

- organizations and users;
- brand workspaces;
- roles and permissions;
- Brand Genesis Sessions;
- Brand Context Versions;
- consent and likeness governance;
- identity and creative libraries;
- brand memory.

### Research and Interview Intelligence

- guest dossier;
- brand research;
- audience reality research;
- research evidence and citations;
- Context Premise Map;
- Interviewer Resonance Context;
- Matrix of Edging Brief;
- Narrative State Map;
- Interview Asset Contracts;
- interview deck compiler;
- live interview cues;
- post-session interviewer learning.

### Expression Capture

- recording configuration;
- pre-session quality gate;
- recording artifact ingestion;
- transcript ingestion and synchronization;
- timestamped anchor hits;
- expression moment extraction;
- source-grounded asset routing.

### Creative Production

- asset package compilation;
- Complete Editing Sessions;
- SceneSpecs and Composition Plans;
- approved asset retrieval;
- composition-provider integration;
- image-generation and image-edit integration;
- layer decomposition and segmentation;
- avatar rigs;
- motion recipes and SFX plans;
- deterministic and generative render routes;
- render receipts and evaluations.

### Review and Publishing

- PWA review;
- Telegram preview/chat/actions;
- approval and revision workflows;
- publishing intents;
- Publer integration;
- platform-specific captions and schedules;
- publishing status and performance ingestion.

### Reliability

- workflow durability;
- idempotency;
- audit log;
- observability;
- backups;
- error recovery;
- golden tests;
- provider fallbacks.

## 3.2 Not In Scope for the First Public Release

These may be represented by contracts but are not allowed to compromise the core release:

- a public marketplace;
- a full community platform;
- client-facing coaching interventions inside Telegram;
- billing/subscriptions beyond what is required to operate;
- autonomous clinical advice;
- autonomous public replies to comments;
- fully automated synthetic voice impersonation;
- training a custom LoRA for every brand by default;
- replacing human interviewers with avatars.

## 3.3 Release-Required User Journeys

The public release is incomplete unless these journeys work end to end:

1. create a brand and complete Brand Genesis;
2. prepare an interview from research to approved Interview Asset Contracts;
3. conduct or ingest a Complete Expression Session;
4. extract and approve Expression Moments;
5. compile a Guest Asset Pack or equivalent package;
6. render and review assets through required CMF routes;
7. revise from PWA and Telegram using the same agent thread;
8. schedule approved content through Publer;
9. update brand and interviewer memory;
10. reproduce an output from pinned inputs and receipts.

---

# 4. Greenfield Runtime and Legacy Reference Strategy

## 4.1 Decision

The new application is a greenfield runtime.

The legacy repository is valuable because it contains:

- registries;
- prompt families;
- production examples;
- evaluation heuristics;
- primitive taxonomies;
- render experiments;
- integration code;
- prior schemas.

It is not allowed to determine the new runtime topology.

## 4.2 Legacy Access Mode

Mount or copy the old repository under:

```text
legacy-reference/
```

Rules:

- read-only;
- no production runtime imports;
- no shared database;
- no direct API calls to legacy services;
- no “temporary” dependency that becomes permanent;
- provenance recorded for every migrated object.

## 4.3 Migration Ledger

Create a ledger with at least:

```text
legacy_path
legacy_object_name
legacy_type
new_registry_type
new_schema_id
migration_status
semantic_changes
examples_preserved
tests_created
owner
review_status
deprecation_note
```

Migration statuses:

```text
unreviewed
classified
mapped
converted
validated
approved
deprecated
blocked
```

## 4.4 Migration Rules

1. A new topic is not a new archetype.
2. A new repeatable meaning structure may be a new archetype.
3. A packaging structure belongs in Asset Derivatives.
4. A humor psychology belongs in Meme Mechanisms.
5. A participatory response form belongs in Reaction Archetypes.
6. A physical production route belongs in CMF Render Modes.
7. Prompt examples become fixtures, not hidden runtime behavior.
8. No schema enters `active` status without validation examples and an evaluation rubric.

## 4.5 Legacy Test Fixtures

Preserve successful historical outputs as:

```text
fixtures/legacy-golden/
```

Each fixture should include:

- source inputs;
- old prompt or process;
- expected semantic structure;
- expected route;
- unacceptable distortions;
- migration notes.

The new compiler does not have to reproduce old wording. It must preserve the valuable mechanics.

---

# 5. High-Level System Architecture

## 5.1 Product Modules

```text
CCP Studio
│
├── Identity & Access
├── Organization / Brand Workspace
├── Registry Kernel
├── Agent Gateway
├── Brand Genesis Engine
├── Research & Context Engine
├── Interview Intelligence Studio
├── Complete Expression Session Engine
├── Asset Compilation Engine
├── Conscious Media Factory
├── Evaluation & Approval
├── Publishing
├── Memory & Analytics
└── Infrastructure / Workflow Runtime
```

## 5.2 Surface Topology

```text
┌──────────────────────────────────────────────┐
│ CCP Studio PWA                              │
│ Full control, deep review, live interview    │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│ Telegram Bot + Mini App                     │
│ Chat, preview, lightweight actions, alerts   │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│ Agent Gateway                               │
│ Context assembly, tools, commands, policy    │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│ Modular Domain API                          │
└──────────┬──────────────┬────────────────────┘
           │              │
┌──────────▼──────┐  ┌────▼───────────────────┐
│ Registry Kernel │  │ Durable Workflow Engine │
└──────────┬──────┘  └────┬───────────────────┘
           │              │
┌──────────▼──────────────▼────────────────────┐
│ Postgres + Outbox + pgvector                 │
│ Neo4j derived relationship projection        │
│ Object storage                               │
└──────────┬───────────────────────────────────┘
           │
┌──────────▼───────────────────────────────────┐
│ CPU / GPU / Render / Publishing Workers      │
└──────────────────────────────────────────────┘
```

## 5.3 Deployment Principle

Use a modular monolith for domain logic and separate workers for asynchronous/heavy execution.

Do not begin with many networked microservices.

Module boundaries must be explicit enough to split later without rewriting domain rules.

## 5.4 Canonical Implementation Stack

The following stack is the accepted default and is formalized by `ADR-001`:

```text
Primary language/runtime: Python 3.12+ with a pinned project version
Domain contracts: Pydantic v2
Agent program runtime: DSPy
Primary orchestrator: Pi Coding Agent through the Python Agent Gateway
API/application boundary: FastAPI + OpenAPI
Database: PostgreSQL
Persistence mapping: SQLAlchemy 2.x + Alembic
Vector search: pgvector
Graph projection: Neo4j
Durable workflows: Temporal Python SDK or an approved equivalent
Batch dispatch: workflow activities + cloud batch adapters
Object storage: GCS primary, S3 overflow/scratch adapter
Python workspace: uv workspace and locked dependency sets
PWA: Next.js + TypeScript strict mode
Telegram bot: Python service sharing the Agent Gateway
Telegram Mini App: Next.js / TypeScript
Default video renderer: Remotion TypeScript worker
Procedural renderers: Motion Canvas TypeScript and Manim Python
Infrastructure: Docker + Terraform
Observability: OpenTelemetry
Testing: pytest, contract fixtures, workflow tests, and calibrated DSPy evaluations
Static quality: Ruff plus strict type checking with mypy or Pyright
```

A small `pnpm` workspace may be used for the TypeScript leaf applications. It is not the root runtime or the contract authority.

## 5.5 Contract Projection Chain

The canonical contract projection is:

```text
Pydantic domain / registry / command models
→ generated JSON Schema
→ FastAPI OpenAPI
→ generated TypeScript interfaces
→ optional generated Zod validators for client-side validation
→ PWA, Mini App, and Remotion inputs
```

Rules:

- Pydantic is authoritative.
- ORM entities do not silently redefine domain semantics.
- TypeScript types are generated artifacts and must not be edited by hand.
- Client-side Zod may validate UX payloads but may not become a shadow domain model.
- Renderer input is a versioned Pydantic `RenderContract` serialized to JSON.

## 5.6 Canonical Sources of Truth

- Pydantic packages own semantic contract definitions.
- PostgreSQL owns transactional business state.
- Object storage owns immutable binary assets.
- Registry bundles are versioned Python/data artifacts validated at boot.
- Temporal owns durable workflow execution state, not business truth.
- Neo4j is a derived relationship projection, not the transactional source of truth.
- Search/vector indexes are rebuildable projections.
- Pi/DSPy reasoning traces are evidence and telemetry, not canonical workflow state.
- Telegram and Publer are external surfaces/adapters, never canonical state.

## 5.7 Runtime Responsibility Split

### Python Harness owns

- domain and registry contracts;
- command and event schemas;
- Registry Kernel;
- DSPy program registry;
- Pi orchestration and tool policy;
- Brand Genesis, research, interview, expression, and CMF application services;
- durable workflow definitions;
- evaluation, receipts, and audit;
- provider routing and publishing policy.

### TypeScript leaf runtimes own

- PWA and Telegram Mini App interaction;
- Remotion and Motion Canvas rendering;
- browser previews and local UI state;
- generated contract consumers.

TypeScript leaf runtimes may request commands and render approved contracts. They may not decide brand truth, archetype routing, identity policy, evaluation thresholds, or publishing authority.

---

# 6. Tenant, Brand, and Context Architecture

## 6.1 Organization and Brand

An `Organization` is the administrative/security boundary.

A `BrandWorkspace` is the creative and narrative boundary.

One organization may manage multiple brands. Every brand has its own:

- identity;
- voice;
- visual constitution;
- audience;
- research memory;
- interviews;
- asset libraries;
- publishing accounts;
- evaluation history.

## 6.2 Required Scoping Fields

Every brand-owned database row must contain:

```text
organization_id
brand_id
created_at
updated_at
created_by
```

Every production or historical output must also contain the applicable:

```text
brand_context_version_id
registry_bundle_version_id
```

Missing brand context is a hard failure for any production job.

## 6.3 Brand Context Version

The Brand Context Version is the immutable creative and narrative snapshot used by interviews and renders.

It references, rather than duplicates, approved versioned components.

```json
{
  "brand_context_version_id": "bcv_01J...",
  "organization_id": "org_01J...",
  "brand_id": "brand_01J...",
  "status": "locked",
  "business_intelligence_version_id": "biv_...",
  "tribe_soul_version_id": "tsv_...",
  "character_lexicon_version_id": "clv_...",
  "voice_dna_version_id": "vdv_...",
  "negative_space_version_id": "nsv_...",
  "visual_constitution_version_id": "vcv_...",
  "identity_pack_version_id": "ipv_...",
  "acting_library_version_id": "alv_...",
  "papercut_rig_version_id": "prv_...",
  "micro_semiotic_anchor_library_version_id": "msav_...",
  "prop_library_version_id": "plv_...",
  "motion_library_version_id": "mlv_...",
  "sfx_library_version_id": "slv_...",
  "composition_preference_version_id": "cpv_...",
  "publishing_profile_version_id": "ppv_...",
  "registry_bundle_version_id": "rbv_...",
  "content_hash": "sha256:...",
  "locked_at": "2026-06-18T12:00:00Z"
}
```

## 6.4 Lock and Fork Semantics

A locked context is immutable.

To change it:

```text
locked context v1
→ create draft fork v2
→ edit component versions
→ evaluate
→ approve
→ lock v2
→ make v2 active for new work
```

Historical jobs remain attached to v1.

## 6.5 Session Context Snapshot

A session may need time-sensitive research that should not become permanent brand truth.

Create a `SessionContextSnapshot` containing:

- active Brand Context Version;
- current research evidence;
- active Context Premises;
- campaign;
- product/offer;
- audience segment;
- temporal events;
- session goal;
- content constraints.

This snapshot is also immutable once a Complete Expression Session starts.

## 6.6 Isolation

Implement:

- PostgreSQL row-level security;
- object-storage prefixes and IAM isolation;
- encrypted provider tokens;
- signed short-lived asset URLs;
- audit records for cross-brand access;
- brand-scoped agent context assembly;
- optional dedicated worker pool for sensitive brands.

The operator may switch brands. The agent must never implicitly carry one brand’s context into another brand.

---

# 7. Canonical Domain Chain

The primary lifecycle is:

```text
Organization
→ BrandWorkspace
→ BrandGenesisSession
→ BrandContextVersion
→ ResearchField
→ InterviewPreparation
→ CompleteExpressionSession
→ ExpressionMoment
→ ArchetypeRoute
→ AssetPackageSpec
→ CompleteEditingSession
→ CreativeState
→ RenderOutput
→ EvaluationReceipt
→ ApprovalEvent
→ PublishingIntent
→ PublishingResult
→ BrandMemoryEvent
```

## 7.1 Object Responsibility Table

| Object | Responsibility |
|---|---|
| BrandWorkspace | Stable brand container |
| BrandGenesisSession | Onboarding workflow that manufactures reusable substrate |
| BrandContextVersion | Immutable approved creative/narrative snapshot |
| ResearchField | Evidence collection for a specific research objective |
| ContextPremise | Temporary evidence-backed working hypothesis |
| InterviewPreparation | Aggregates dossier, audience brief, resonance, edging, state map, contracts |
| InterviewAssetContract | Atomic planned question and its production intent |
| CompleteExpressionSession | Atomic human expression/capture event |
| ExpressionMoment | Approved or candidate source segment with meaning and timestamps |
| ArchetypeRoute | Meaning/derivative/reaction/render classification |
| AssetPackageSpec | Planned deliverables from one session |
| CompleteEditingSession | Atomic downstream media-production boundary |
| CreativeState | Evolving state for one creative job |
| EvaluationReceipt | Scores, evidence, failures, provider versions, and decision |
| PublishingIntent | Internal approved schedule/publish request |
| BrandMemoryEvent | Approved learning extracted from outcomes |

## 7.2 IDs and Versioning

Use sortable unique IDs such as UUIDv7 or ULID.

Versioned objects carry:

```text
semantic_version
status
parent_version_id
content_hash
created_by
approved_by
approved_at
```

## 7.3 Immutability Rules

Immutable after lock/completion:

- consent record versions;
- Brand Context Versions;
- registry bundle versions;
- source recordings;
- source transcript revisions once cited by an approved moment;
- approved expression moment boundaries;
- execution receipts;
- approval events;
- publishing results.

Corrections create superseding records. Do not rewrite history.

---

# 8. Registry Kernel

## 8.1 Purpose

The Registry Kernel turns the accumulated CCP intelligence into executable, validated, versioned contracts.

It is the first subsystem to implement because every later engine depends on it.

## 8.2 Mandatory Registries

### A. Core Content Archetypes

Repeatable meaning structures such as:

- Transformation Story;
- Witness Story;
- Backstory Reveal;
- Confessional Turn;
- Conceptual Contrast;
- Visual Timeline;
- Worst Case Scenario;
- Shocking Comparison;
- Myth Debunk;
- Core Educator / Explainer;
- Challenger / Frame Breaker;
- Authority Proof Stack;
- Observational Humor;
- Industry Hypocrisy Exposure.

### B. Asset Derivative Schemas

Packaging and transformation structures such as:

- Dopamine Cliff Carousel;
- Relief Peak Carousel;
- Dilemma Poll;
- Persuasive Micro-Claim;
- Thought Whisperer Extract;
- Mirror Prompt;
- Tension Poll;
- Quote-to-Question;
- Scene-to-Principle;
- Identity Mirror;
- Data Story Post.

### C. Meme Mechanisms

Psychological humor mechanisms such as:

- Benign Violation;
- Incongruity;
- Relief;
- Superiority with ethical limits;
- Micro-Contradiction;
- Tribal Absurdity;
- Status Satire.

### D. Reaction Archetypes

Participatory response forms such as:

- Validation Reaction;
- Solo Reaction;
- Vote Then React;
- Debate with Jury;
- Reaction Duel;
- Reaction Seed;
- Blind Rank Defense;
- Redemption Round.

### E. CMF Render Modes

Physical production routes such as:

- Personal-Brand Commentary;
- Cinematic Story Commentary;
- Paper-Cut Explainer;
- Animated Avatar Explainer;
- Living Commentary Reaction;
- Conscious Reactions Editing;
- Meme / Dance / Reaction;
- Cinematic Metaphor;
- Data Story;
- Quiz / Ranking;
- Carousel Static / Motion.

## 8.3 Supporting Registries

Also implement:

- Expression State Registry;
- Narrative State Transition Registry;
- Primitive Registry;
- Coalition Signature Registry;
- Edge Product Registry;
- Visual Style Constitution Registry;
- Motion Recipe Registry;
- SFX Mapping Registry;
- Micro-Semiotic Anchor Category Registry;
- Evaluation Rubric Registry;
- Provider Capability Registry;
- Platform Constraint Registry;
- Consent Policy Registry;
- Failure Taxonomy Registry.

## 8.4 Standard Registry Entry

```json
{
  "schema_id": "archetype.myth_debunk.v1",
  "registry_type": "core_content_archetype",
  "name": "Myth Debunk",
  "version": "1.0.0",
  "status": "active",
  "description": "Expose a false belief and replace it with an evidence-grounded frame.",
  "required_source_material": [
    "myth",
    "why_it_is_believed",
    "counter_evidence",
    "replacement_frame"
  ],
  "beat_structure": [
    "name_myth",
    "show_cost",
    "reveal_mechanism",
    "teach_replacement"
  ],
  "preferred_induction_routes": [
    ["authority", "edge_pressure", "teaching"]
  ],
  "compatible_derivatives": [
    "asset_derivative.scene_to_principle.v1",
    "asset_derivative.dopamine_cliff_carousel.v1"
  ],
  "compatible_render_modes": [
    "cmf.paper_cut_explainer.v1",
    "cmf.personal_brand_commentary.v1"
  ],
  "evaluation_rubric_id": "eval.archetype.myth_debunk.v1",
  "examples": [],
  "provenance": {
    "legacy_paths": [],
    "approved_by": "..."
  }
}
```

## 8.5 Registry Bundle

A `RegistryBundleVersion` pins compatible versions of all active registries.

```json
{
  "registry_bundle_version_id": "rbv_...",
  "version": "1.0.0",
  "entries": {
    "core_archetypes": [],
    "asset_derivatives": [],
    "meme_mechanisms": [],
    "reaction_archetypes": [],
    "cmf_render_modes": [],
    "supporting_registries": []
  },
  "validation_status": "passed",
  "content_hash": "sha256:..."
}
```

Every Interview Asset Contract and Complete Editing Session references a bundle version.

## 8.6 Compiler Principle

Registry entries do not store one giant final prompt.

They store:

- semantic requirements;
- constraints;
- compatible routes;
- evaluation logic;
- examples;
- prompt fragments where useful.

A compiler builds the task-specific prompt or tool request from:

```text
registry contract
+ Brand Context
+ Session Context
+ source evidence/expression
+ provider capability
+ platform constraints
```

## 8.7 Validation

At application boot:

1. load all registry files;
2. validate entries through canonical Pydantic models;
3. verify generated JSON Schema is current;
4. validate cross-references;
5. detect version conflicts;
6. detect missing rubrics;
7. detect circular route rules;
8. calculate content hashes;
9. refuse production mode if the active bundle is invalid.

---

# 9. Agent Runtime

## 9.0 Harness Composition

The agent runtime is a layered Python harness, not a freeform chatbot:

```text
PWA / Telegram / system event
→ Python Agent Gateway
→ scoped AgentExecutionContext
→ Pi Coding Agent orchestrator
→ DSPy program and tool selection
→ Pydantic AgentCommand proposal
→ policy / permission / idempotency validation
→ durable workflow or synchronous application service
→ provider / renderer / publisher adapter
→ receipt, audit event, and projection update
```

### Pi Coding Agent responsibilities

Pi may:

- inspect repository and registry state;
- plan multi-step work;
- choose approved DSPy programs and tools;
- propose typed commands;
- coordinate specialist agents;
- explain decisions;
- request confirmation;
- observe workflow and evaluation results;
- open repair or revision loops.

Pi may not:

- directly mutate PostgreSQL;
- write around the Command Bus;
- treat its chat transcript as persistence;
- silently change a registry or Brand Context Version;
- publish without the required confirmation;
- bypass provider, consent, or cost policy.

### DSPy responsibilities

DSPy owns structured reasoning programs where learned or calibrated compilation is valuable, including:

- research synthesis;
- Context Premise formation and adversarial review;
- Interview Asset Contract compilation;
- expression-moment extraction;
- archetype and derivative routing;
- composition-plan compilation;
- reference retrieval/ranking;
- evaluation and repair proposals.

Every production DSPy program must declare:

```text
program_id
program_version
input Pydantic model
output Pydantic model
model/provider policy
training or optimization provenance
evaluation dataset version
quality threshold
fallback behavior
```

DSPy output remains a proposal until domain validation and policy accept it.

## 9.1 One Agent Gateway

All conversational surfaces connect to a single `AgentGateway`.

The gateway is responsible for:

- authentication;
- brand and object scope;
- thread selection;
- context assembly;
- model selection;
- tool availability;
- policy evaluation;
- command proposal;
- confirmation handling;
- response streaming;
- audit logging.

## 9.2 Agent Thread

A thread is anchored to a user and may optionally be anchored to a brand or active object.

```json
{
  "thread_id": "thread_...",
  "organization_id": "org_...",
  "user_id": "user_...",
  "brand_id": "brand_...",
  "surface": "telegram_mini_app",
  "active_object": {
    "type": "render_output",
    "id": "render_..."
  },
  "mode": "production_review",
  "created_at": "...",
  "last_activity_at": "..."
}
```

The thread does not contain the only copy of workflow state.

## 9.3 Context Assembly

The gateway assembles only relevant context:

```text
user permissions
+ active brand context
+ active object snapshot
+ relevant registry entries
+ relevant research/evidence
+ recent thread messages
+ applicable negative space
+ available tools
```

Do not dump the entire brand or registry corpus into every call.

Use retrieval with explicit provenance.

## 9.4 Agent Modes

```text
brand_genesis
research
interview_preparation
live_interview
post_session_extraction
production_planning
render_review
publishing
system_administration
```

Mode determines available tools and response behavior.

## 9.5 Model Routing

Use a provider-agnostic reasoning gateway.

Recommended task policy:

### Local Qwen-class model

Use for:

- schema extraction;
- classification;
- registry retrieval;
- metadata generation;
- transcript chunk processing;
- draft route proposals;
- deterministic command formatting;
- low-risk summaries;
- batch evaluations after calibration.

Do not hardwire architecture to a specific marketing name. Pin a tested model artifact, quantization, tokenizer, context window, and serving image in the Provider Capability Registry.

### Premium external reasoning models

Use selectively for:

- difficult research synthesis;
- adversarial context-premise review;
- complex interview planning;
- high-stakes factual or psychological review;
- final evaluation disputes;
- tasks where local quality is below an approved threshold.

## 9.6 Tool and Command Separation

Tools read data or perform controlled operations.

The LLM must not write database records directly.

It emits a Pydantic-validated `AgentCommand`:

```json
{
  "command_id": "cmd_...",
  "command_type": "REQUEST_RENDER_REVISION",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "actor_user_id": "user_...",
  "target": {
    "type": "render_output",
    "id": "render_..."
  },
  "payload": {
    "revision_note": "Reduce mascot motion and use a warmer expression."
  },
  "idempotency_key": "...",
  "confirmation_level": "human_confirm",
  "status": "proposed"
}
```

The Command Bus validates:

- permissions;
- schema;
- current state;
- brand scope;
- confirmation;
- idempotency;
- policy.

## 9.7 Permission Levels

| Level | Example | Execution |
|---|---|---|
| Read | summarize brand, explain receipt | immediate |
| Safe draft | draft questions, propose route | immediate, no external effect |
| Reversible write | save note, create draft | may execute with audit |
| Expensive action | generate 64 assets, start GPU batch | explicit confirmation or policy |
| Identity mutation | approve identity asset, lock context | human confirmation |
| Public effect | schedule/publish | two-step confirmation |
| Destructive | delete/export personal data | elevated role and confirmation |

## 9.8 Agent Memory

Separate:

- conversational memory;
- brand memory;
- interviewer memory;
- workflow state;
- research evidence;
- performance analytics.

Only approved learning enters durable brand/interviewer memory.

Model speculation never becomes memory automatically.

## 9.9 Prompt Injection and External Content

Research documents, websites, uploaded files, and transcripts are untrusted content.

The agent must:

- distinguish instructions from evidence;
- ignore instructions contained in source materials;
- retain source provenance;
- mark facts, quotes, and inferences separately;
- never grant tools based on document content;
- sanitize HTML and file metadata.

---

# 10. Application Surfaces

## 10.1 CCP Studio PWA

The PWA is the complete operating surface.

Primary navigation:

```text
Home
Brands
Research
Interviews
Assets
Production
Review
Publishing
Memory
Registries
System
```

### Required Pages

#### Portfolio Dashboard

- all brands;
- pending approvals;
- upcoming interviews;
- render batches;
- failed workflows;
- publishing calendar;
- system health.

#### Brand Dashboard

- active Brand Context;
- current campaigns;
- recent expression sessions;
- active asset packages;
- content calendar;
- publishing account health;
- recent learning.

#### Brand Genesis Wizard

- intake;
- consent;
- source photos/video;
- source QC;
- business/tribe/lexicon/semiotic intake;
- identity summary;
- 64 acting assets;
- avatar rig;
- prop and anchor libraries;
- motion/SFX;
- context lock.

#### Interview Intelligence Studio

- research evidence;
- guest dossier;
- audience reality brief;
- Context Premises;
- interviewer pre-induction chat;
- Matrix of Edging;
- Narrative State Map;
- Interview Asset Contracts;
- deck review.

#### Live Interview Mode

- current contract;
- concise next cue;
- follow-up options;
- timestamp marker;
- “strong moment” marker;
- recording quality indicators;
- no clutter.

#### Expression Session Review

- recordings;
- transcript;
- anchor hits;
- expression moments;
- source playback;
- route candidates;
- approval.

#### Production Board

Kanban states:

```text
planned
ready
queued
generating
rendering
auto_evaluated
needs_review
revision_requested
approved
scheduled
published
failed
archived
```

#### Render Review

- media preview;
- source expression;
- route;
- selected assets;
- Brand Context hash;
- provider/workflow versions;
- evaluation receipt;
- compare revisions;
- approve/reject/revise;
- publishing preparation.

#### Publishing Calendar

- channel previews;
- captions;
- schedule;
- Publer state;
- failures;
- performance.

## 10.2 Telegram Bot

The bot handles:

- natural-language agent chat;
- notifications;
- quick commands;
- confirmation requests;
- deep links into the Mini App or PWA.

Example:

```text
Brand: Maison Naturopathie
Asset: Myth Debunk 03
Status: needs review
Identity 0.93 | Emotion 0.88 | Style 0.94

[Preview] [Chat] [Approve] [Revise]
```

## 10.3 Telegram Mini App

The Mini App is intentionally narrow.

Screens:

1. preview;
2. chat with the same agent;
3. evaluation summary;
4. revision form;
5. approve/reject;
6. publishing confirmation;
7. active batch status.

It is not a full editing timeline.

## 10.4 Telegram Authentication

The backend validates Telegram initialization data server-side, maps it to a CCP user, and enforces the same permissions as the PWA.

Never trust client-supplied brand or user IDs without server validation.

## 10.5 Shared Agent Continuity

A user can begin in PWA, continue in Telegram, and return without losing context.

Messages reference the same thread and active object.

Actions update domain state, so all surfaces remain synchronized.

## 10.6 Optional Client Review

Client access is role-based and disabled by default.

When enabled, a client may:

- preview assets for their brand;
- comment;
- approve or request revision;
- chat with the same agent under restricted tools.

Clients cannot:

- switch brands;
- modify locked identity context;
- access internal research notes without permission;
- publish without assigned rights.
# 11. Brand Genesis Engine

## 11.1 Purpose

Brand Genesis creates the approved, reusable, versioned substrate that lets every later interview and production job remain coherent.

Its result is not merely a profile. It is a locked `BrandContextVersion` and a `genesis_clearance_certificate`.

## 11.2 Genesis Stages

```text
1. Client and business intake
2. Consent and governance
3. Source media intake and QC
4. Business Intelligence
5. Tribe Soul / audience intelligence
6. Character Lexicon
7. Voice DNA and Negative Space
8. Semiotic and visual constitution
9. Identity summary
10. Realistic acting library
11. Paper-cut avatar system
12. Props and visual objects
13. Micro-Semiotic Anchor Library
14. Motion and SFX libraries
15. Composition preferences
16. Publishing profile
17. Adversarial validation
18. Human approval
19. Brand Context lock
```

## 11.3 Intake

Collect structured data:

- legal/client identity;
- brand name;
- business model;
- offers;
- audience segments;
- geography and languages;
- platforms;
- brand goals;
- content categories;
- perceived competitors;
- example content liked/disliked;
- forbidden claims;
- visual preferences;
- cultural sensitivities;
- humor boundaries;
- public-risk tolerance.

Free text is allowed, but the output must become typed objects.

## 11.4 Consent

Consent is versioned and explicit.

At minimum cover:

- storage and processing of source photos/video/audio;
- synthetic realistic images;
- stylized avatars;
- facial-expression and body-language derivatives;
- memes and humorous contexts;
- motion transfer;
- social publication;
- future reuse;
- model training prohibition or permission;
- retention and deletion;
- human review;
- third-party providers.

A provider job must verify consent compatibility before execution.

## 11.5 Source Media Requirements

Recommended:

```text
5–10 photographs:
- front neutral
- smile
- serious
- 3/4 left
- 3/4 right
- full body
- natural candid
- professional image
- expressive image
- optional seated/casual

Optional high-value input:
- 30–60 second vertical talking video
```

Photos provide identity evidence. Video provides performance evidence.

## 11.6 Source QC

Auto-check:

- face visibility;
- resolution;
- blur;
- lighting;
- occlusion;
- duplicate similarity;
- angle diversity;
- expression diversity;
- full-body availability;
- consent coverage.

Failures do not silently proceed. The app requests replacement media.

## 11.7 Business, Audience, and Language Substrate

Brand Genesis must also produce:

### Business Intelligence

- offer;
- transformation promise;
- evidence;
- differentiation;
- acceptable claims;
- business constraints.

### Tribe Soul

- demographics;
- cultural context;
- aspirations;
- anxieties;
- objections;
- rituals;
- social pressure;
- inside jokes;
- ordinary-life objects;
- identity tensions.

### Character Lexicon

- signature terms;
- idioms;
- metaphors;
- phrase patterns;
- forbidden clichés;
- platform-specific variations.

### Voice DNA

- Positive Space;
- Negative Space;
- Emotional DNA;
- source hierarchy;
- confidence and provenance.

The first version may be incomplete. It must state confidence and evolve from future authentic recordings.

## 11.8 Identity Summary

The identity summary describes stable visible traits and explicit no-change constraints.

```json
{
  "identity_summary_id": "ids_...",
  "stable_traits": [
    "face shape",
    "skin-tone range",
    "hair silhouette",
    "body proportions",
    "signature clothing"
  ],
  "do_not_change": [
    "do not alter apparent age",
    "do not narrow the face",
    "do not replace natural hair texture",
    "do not over-smooth skin",
    "do not change body type"
  ],
  "approved_style_modes": [
    "realistic_reference",
    "photo_paper_cutout",
    "editorial_papercut_avatar"
  ],
  "evidence_assets": []
}
```

Human approval is required before generating the acting library.

---

# 12. Identity Pack and 64-State Acting Library

## 12.1 Identity Pack

The Identity Pack is a versioned production artifact.

It contains:

- identity summary;
- approved source references;
- identity-conditioning stack version;
- container image digest;
- conditioning workflow hash;
- allowed reference-selection rules;
- forbidden runtime mutations.

```json
{
  "identity_pack_version_id": "ipv_...",
  "brand_id": "brand_...",
  "worker_image_digest": "sha256:...",
  "conditioning_stack": [
    {
      "capability": "face_identity_conditioning",
      "version": "..."
    },
    {
      "capability": "reference_image_conditioning",
      "version": "..."
    }
  ],
  "approved_reference_album_id": "album_...",
  "runtime_mutable": false
}
```

## 12.2 Determinism

Identity behavior is reproducible when the following are pinned:

- worker image digest;
- model weights;
- workflow graph;
- approved references and hashes;
- provider settings;
- seed where supported;
- precision and runtime;
- post-processing.

Identity determinism is not identical to pixel determinism. Receipts must state what was pinned.

## 12.3 Acting, Not Posing

The library is organized around communicative performance.

Primary retrieval hierarchy:

```text
communicative intent
→ emotion
→ body language
→ gesture
→ facial expression
→ energy
→ framing/orientation
→ layout utility
```

## 12.4 8 × 8 Matrix

Emotions:

```text
confident
warm
reflective
serious
challenging
playful
urgent
celebratory
```

Gesture/body-language families:

```text
open_hands_explaining
pointing_directing
inviting_open_palms
grounded_authority
thinking_hand_to_face
emphasis_gesture
uncertainty_shrug
dynamic_uplift
```

These produce 64 required cells.

## 12.5 Generation

Use the approved image-asset provider, initially GPT Image 2, through the `ImageAssetProvider` interface.

Generate by emotional family in batches.

Each request contains:

- source identity references;
- stable-trait summary;
- no-change constraints;
- target acting cell;
- wardrobe constraints;
- framing and background rules;
- output purpose;
- provider/model version.

## 12.6 Review Lifecycle

```text
draft
→ generation_requested
→ generated
→ auto_qc_passed | auto_qc_failed
→ awaiting_human_review
→ approved | needs_fix | rejected
→ locked
```

Review reasons are structured:

```text
likeness_drift
age_drift
body_type_drift
hair_drift
emotion_unclear
gesture_unclear
hands_broken
wrong_energy
unusable_crop
wardrobe_drift
visual_artifact
```

The fix loop stores both free-form notes and tags.

Rejected patterns update visual Negative Space only after human approval.

## 12.7 Reference Retrieval

Initial weighted score:

```text
0.30 communicative intent
0.25 emotion
0.20 gesture
0.15 body language
0.05 facial expression
0.05 framing/layout
```

Weights are configurable per render mode.

Fallback:

1. prefer emotion and intent;
2. choose nearest gesture;
3. mark low confidence;
4. require stricter human review;
5. never use an unapproved image.

Use one primary body/gesture reference and, where provider capability supports it, one secondary face/expression anchor.

## 12.8 LoRA Policy

Do not train a brand LoRA by default.

A LoRA becomes a deliberate versioned migration only when measured production evidence shows:

- repeated identity failures;
- recurring reference gaps;
- unacceptable edit resistance;
- excessive regeneration cost;
- insufficient camera-angle coverage.

Training requires a separate consent check, dataset review, model card, evaluation suite, and rollback path.

---

# 13. Paper-Cut Avatar and Rig System

## 13.1 Purpose

The paper-cut avatar is a reusable deterministic actor for:

- explainers;
- meme visuals;
- carousels;
- polls;
- reactions;
- branded reels;
- narrative diagrams;
- CTAs.

It is separate from the realistic acting library.

## 13.2 Asset Set

### Heads / Expressions

```text
neutral
warm_smile
big_smile
serious
focused
surprised
thinking
skeptical
concerned
playful
celebratory
```

### Eyes / Brows

```text
neutral
happy
wide
blink_closed
skeptical
concerned
focused_squint
```

### Mouth Shapes

```text
closed
small_open
wide_open
smile_open
oo
ee
m_b_p
frown
```

### Body Parts

```text
torso
head
neck
left_upper_arm
left_forearm
left_hand
right_upper_arm
right_forearm
right_hand
left_leg
right_leg
feet
shadow
```

### Gestures

```text
point_left
point_right
open_hands
hand_on_chin
arms_crossed
one_hand_up
celebration
shrug
```

## 13.3 Asset Creation Route

```text
approved identity references
→ image-asset generation
→ semantic layer decomposition
→ precision segmentation
→ character-specific hidden-part repair if needed
→ image edit/edge repair
→ layer review
→ rig manifest
→ preview tests
→ approval and lock
```

## 13.4 Rig Manifest

The rig is data, not hidden editor state.

It contains:

- layer IDs and URIs;
- z-order;
- anchors/pivots;
- parent/child relationships;
- bone constraints;
- swappable expressions;
- mouth maps;
- gesture presets;
- motion affordances;
- coordinate system;
- version and hash.

## 13.5 Rigging Providers

Use a `RigProvider` adapter.

Potential implementations:

- Stretchy Studio integration;
- custom cutout-rig authoring;
- future open-source rig tools.

The production renderer must not depend on an editor-only proprietary project file. Export a canonical rig manifest and assets.

## 13.6 Preview Gate

Required previews:

- blink;
- small nod;
- head bob;
- open-hands explanation;
- point;
- shrug;
- expression swap;
- mouth flap;
- stop-motion jitter;
- silhouette at mobile size.

The rig cannot lock until these pass.

---

# 14. Visual Constitution and Micro-Semiotic Anchoring

## 14.1 Editorial 2.5D Paper-Cut Style

Official style ID:

```text
visual.editorial_2_5d_papercut_reel.v1
```

Core feeling:

```text
credible + warm + handmade + premium + educational
```

Motion principle:

> Paper gently coming alive.

## 14.2 Material Constitution

Allowed:

- textured cream paper;
- colored paper and felt;
- handmade cut edges;
- soft offset shadows;
- slight misalignment;
- physical paper depth;
- restrained grain;
- real portrait cutouts;
- simple black mascot;
- legible editorial typography.

Forbidden by default:

- glossy generic 3D;
- sterile SaaS vectors;
- excessive neon gradients;
- photoreal skin inside a fully illustrated body unless intentional;
- excessive bouncing;
- generic sticker clutter;
- smooth corporate motion that destroys paper materiality;
- mystical glow overuse in evidence-led health content.

## 14.3 Micro-Semiotic Anchoring

Definition:

> The deliberate placement of small, culturally recognizable cues that trigger identification, locality, humor, trust, or tribal recognition without becoming the main message.

The cue should produce:

```text
“They know our world.”
```

not:

```text
“They are trying too hard to be relatable.”
```

## 14.4 Anchor Categories

```text
ordinary_life_object
local_brand_cue
cultural_ritual
work_tool
health_object
family_object
status_marker
place_marker
digital_habit
tribal_joke
```

## 14.5 Anchor Library

Each brand has an approved versioned library.

```json
{
  "anchor_id": "msa_...",
  "name": "budget supermarket-coded socks",
  "category": "ordinary_life_object",
  "cultural_context": "French fitness audience",
  "audience_signal": "everyday budget fitness humor",
  "visual_description": "...",
  "preferred_placements": ["feet"],
  "prominence": "subtle_but_visible",
  "effects": ["recognition", "humor", "comment_trigger"],
  "risks": {
    "trademark": "medium",
    "stereotype": "low",
    "distraction": "low"
  },
  "approved": true
}
```

## 14.6 Research Relationship

The anchor library comes from:

- Tribe Soul;
- audience research;
- interviewer observations;
- comments and community language;
- real objects in client/guest stories;
- performance evidence from prior posts.

It is the visual extension of Audience Reality.

## 14.7 Anchor Rules

- normally use zero to three;
- never force one into every frame;
- prefer audience-native ordinary details over generic topic symbols;
- exact trademarks require rights review;
- “coded” visual cues may be used when appropriate;
- stereotype and dignity checks are mandatory;
- anchors must not distort the source message.

## 14.8 Anchor Evaluation

Score:

- recognition;
- subtlety;
- audience fit;
- brand fit;
- legibility;
- comment potential;
- distraction risk;
- stereotype risk;
- legal risk.

Results update the anchor library only after review.

---

# 15. Props, Motions, and Sound Libraries

## 15.1 Paper Object Library

Required classes:

```text
headline_strips
subtitle_strips
note_cards
number_badges
arrows
underlines
stars
bursts
plants
leaves
mountains
clouds
dots
squiggles
mascot_poses
icons
stamps
checks
x_marks
```

Each asset carries:

- semantic type;
- palette;
- visual constitution version;
- alpha/edge quality;
- dimensions;
- anchor point;
- compatible motions;
- approval state;
- provenance.

## 15.2 Motion Primitive Library

Motion primitives are reusable low-level behaviors:

```text
paper_pop_in
paper_slide
paper_drop
small_bounce
rotation_settle
slow_push_in
parallax_drift
micro_jitter
underline_draw
circle_draw
stamp_hit
avatar_nod
avatar_point
expression_swap
blink
mouth_flap
mascot_wave
```

## 15.3 Motion Recipes

Recipes combine primitives into archetype-aware timelines.

Initial required recipes:

1. Myth Busted;
2. Three Tips;
3. Stop the Scroll;
4. Conceptual Contrast;
5. Quote to Question;
6. Scene to Principle;
7. Poll / Dilemma;
8. Avatar Reaction;
9. Visual Timeline;
10. Ranking / Quiz Reveal.

## 15.4 Motion Constitution

Default constraints:

```json
{
  "motion_language": "paper_gently_coming_alive",
  "intensity": "restrained",
  "max_simultaneous_moving_layers": 4,
  "base_camera_motion": "slow_push_in",
  "max_camera_scale": 1.035,
  "max_bouncy_events_per_10_seconds": 2,
  "typography_sync_required": true,
  "decorative_motion_intensity": "low"
}
```

Every movement must:

1. direct attention;
2. reveal meaning;
3. add tactile realism; or
4. mark an emotional beat.

Otherwise remove it.

## 15.5 SFX Library

Categories:

```text
paper_pop
paper_slide
paper_rustle
paper_tap
tape_stick
scissors_snip
marker_scribble
marker_underline
felt_plop
soft_whoosh
tiny_ding
wooden_click
stamp_hit
camera_snap
blink_pop
arrow_boop
leaf_rustle
```

## 15.6 SFX Plan

The plan maps timeline events to approved sounds.

Voice remains dominant.

Default sound rules:

- maximum four noticeable SFX per ten seconds;
- duck under speech;
- no cartoon overload;
- brand-specific intensity;
- no sound without licensing/provenance metadata.

---

# 16. Research and Context Engine

## 16.1 Purpose

This engine exists so the app improves the operator’s interviewing, rather than only editing the result.

Its output is an evidence-backed interview field.

## 16.2 Research Objects

### ResearchEvidence

```json
{
  "evidence_id": "ev_...",
  "research_field_id": "rf_...",
  "source_type": "web|book|uploaded_file|prior_interview|comment|analytics",
  "source_uri_or_asset_id": "...",
  "title": "...",
  "author": "...",
  "published_at": "...",
  "captured_at": "...",
  "claim": "...",
  "excerpt_or_summary": "...",
  "fact_or_inference": "fact",
  "confidence": 0.9,
  "temporal_sensitivity": "high",
  "citation_data": {}
}
```

### Guest Dossier

Contains:

- biography and work;
- recurring themes;
- strongest scenes;
- public language;
- prior interview patterns;
- contradictions;
- emotional territory;
- likely expression states;
- risks and boundaries;
- audience overlap;
- evidence references.

### Audience Reality Brief

Contains:

- current anxieties;
- recurring comments;
- social debates;
- search questions;
- objections;
- cultural language;
- identity tensions;
- ordinary objects and rituals;
- Micro-Semiotic Anchor candidates;
- temporal relevance.

### Context Premise

A premise is a working hypothesis.

```json
{
  "context_premise_id": "cp_...",
  "statement": "The guest's strongest material is the emotional cost that made the method necessary.",
  "evidence_ids": ["ev_1", "ev_2"],
  "confidence": 0.78,
  "status": "active",
  "valid_for": "interview_preparation",
  "expires_at": "...",
  "guest_implication": "...",
  "audience_implication": "...",
  "question_implication": "Begin with the originating scene, not methodology.",
  "risk_if_wrong": "...",
  "review_notes": []
}
```

Premises are never stored as facts.

## 16.3 Human Evidence Bias

For high-stakes content:

- research must be source-grounded;
- claims need provenance;
- disputed claims show disagreement;
- the interviewer may ask about an experience without asserting unverified facts;
- the content pipeline may not strengthen a claim beyond the speaker’s evidence.

## 16.4 Research Workflow

```text
define objective
→ collect source candidates
→ de-duplicate
→ assess quality and recency
→ extract evidence
→ separate fact/inference
→ generate dossier and audience brief
→ propose Context Premises
→ adversarial review
→ human review
→ freeze Interview Research Snapshot
```

## 16.5 Research Agents

Logical roles:

- Guest Research Agent;
- Audience Reality Agent;
- Evidence Critic;
- Context Premise Agent;
- Cultural/Semiotic Agent;
- Claim Safety Agent.

These may be implemented by one runtime with role-specific contracts. Do not create 76 independent services.

---

# 17. Interview Intelligence Studio

## 17.1 Three-Context Engine

The best question emerges from:

```text
Guest Truth
+ Interviewer Resonance
+ Audience Reality
= High-Identification Question
```

### Guest Truth

What the guest has lived, built, taught, suffered, witnessed, misunderstood, reconciled, failed to say, or learned late.

### Interviewer Resonance

What genuinely moved or confused the interviewer, what feels alive, what feels fake, and where a small reflection may make the exchange mutual.

### Audience Reality

What the intended audience is carrying now.

## 17.2 Interviewer Pre-Induction

Before finalizing the interview, the same agent interviews the operator.

Required prompts include:

- Which scene stayed with you?
- Where did you feel implicated?
- What do you understand emotionally?
- What remains unclear?
- What audience are you holding in mind?
- What would make the conversation alive rather than literary?
- What would you ask without a camera?
- Where might you share a small reflection?
- What do you refuse to fake?
- Which expression state should open?

Output: `InterviewerResonanceContext`.

## 17.3 Matrix of Edging

The Matrix of Edging selects meaningful tension. It does not manufacture extremity.

Two phases:

### Broad Primary Signal

Before the answer:

- relevant;
- emotionally alive;
- broad enough for surprise;
- not a forced conclusion.

### Edge Product Formation

After expression:

- sharpen the surviving tension;
- identify primitive activation;
- form coalition signature;
- create an execution-ready edge product.

Law:

> The first edge is broad enough to elicit truth; the second is sharp enough to organize force.

## 17.4 Expression States

Primary states:

```text
cinematic
vulnerability
authority
teaching
invitation
```

Supporting states may include recognition, humor, warning, reflection, and edge pressure, but the registry controls their definitions.

## 17.5 Narrative State Map

The map defines:

- opening state;
- transitions;
- which contracts serve each state;
- emotional intensity;
- recovery/grounding points;
- topics to avoid or handle carefully;
- time allocation.

## 17.6 Interview Asset Contract

```json
{
  "contract_id": "iac_...",
  "brand_id": "brand_...",
  "guest_id": "guest_...",
  "target_archetypes": ["archetype.transformation_story.v1"],
  "target_derivatives": ["asset_derivative.scene_to_principle.v1"],
  "target_expression_states": ["cinematic", "vulnerability"],
  "edge_product_hypothesis": "expertise formed as a survival response",
  "main_question": "...",
  "first_line_anchors": {
    "cinematic": "...",
    "emotional": "...",
    "reels_hook": "..."
  },
  "depth_anchor": "...",
  "followups": {
    "flat": "...",
    "abstract": "...",
    "historical": "...",
    "over_rehearsed": "...",
    "not_clip_ready": "..."
  },
  "expected_source_material": [],
  "clip_start_rule": "selected_first_line_anchor",
  "landing_eval_targets": [],
  "potential_asset_routes": [],
  "safety_notes": [],
  "evidence_ids": []
}
```

## 17.7 Interview Deck Compiler

The deck is a sequence of contracts with:

- state progression;
- narrative arc;
- time budget;
- fallback branches;
- must-ask and optional questions;
- grounding moments;
- asset coverage targets.

It is not a static list of questions.

## 17.8 Human Control

The operator may deviate at any time.

The app records:

- planned question;
- actual question;
- spontaneous follow-up;
- why the operator deviated;
- outcome.

This becomes interviewer learning.

---

# 18. Live Interview Copilot

## 18.1 Design Goal

Make the operator more perceptive, not more scripted.

The interface should be quiet and glanceable.

## 18.2 Live Inputs

Where technically and consensually available:

- live or low-latency transcript;
- current contract;
- elapsed time;
- operator markers;
- recording quality;
- recent answer context.

## 18.3 Live Outputs

Allowed cues:

```text
Ask for a scene.
Go deeper on cost.
Bring it back to the body.
This is becoming abstract.
Strong moment — mark timestamp.
Let the silence breathe.
Do not interrupt.
Possible follow-up: “What changed inside you then?”
```

## 18.4 Cue Object

```json
{
  "cue_id": "cue_...",
  "session_id": "xes_...",
  "timestamp": "...",
  "cue_type": "followup_if_abstract",
  "text": "Can you bring us back to the exact room and moment?",
  "reason": "answer shifted into generalized history",
  "confidence": 0.82,
  "source_contract_id": "iac_...",
  "display_priority": "medium"
}
```

## 18.5 Non-Interference Rules

- do not flood cues;
- do not cue while the guest is emotionally landing unless safety requires;
- do not force asset quotas;
- do not present speculative facts as prompts;
- do not encourage manipulative disclosure;
- provide one primary cue and optional alternatives;
- the operator can mute the copilot.

## 18.6 Interviewer Skill Memory

After the session, evaluate:

- which questions induced the intended state;
- which follow-ups worked;
- which cues the operator accepted or ignored;
- interruption timing;
- depth and specificity;
- guest comfort;
- conversational naturalness;
- asset yield;
- deviations that produced better truth.

The goal is a growing `InterviewerProfile`, not dependence on cues.
# 19. Complete Expression Session Engine

## 19.1 Purpose

The Complete Expression Session is the atomic human-expression and capture object.

It is not a media render job.

One Complete Expression Session may produce many Expression Moments and Complete Editing Sessions.

## 19.2 Session Schema

```json
{
  "expression_session_id": "xes_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "session_context_snapshot_id": "scs_...",
  "guest_id": "guest_...",
  "interviewer_id": "user_...",
  "session_type": "remote_single_guest_interview",
  "session_goal": "guest_asset_pack",
  "conversation_language": "fr",
  "system_label_language": "en",
  "recording_configuration": {},
  "research_snapshot_id": "irs_...",
  "interview_preparation_id": "ip_...",
  "interview_asset_contract_ids": [],
  "pre_session_quality_gate": {},
  "recording_artifact_ids": [],
  "transcript_revision_id": null,
  "timestamped_anchor_hits": [],
  "expression_moment_ids": [],
  "asset_package_spec_id": null,
  "evaluation_receipt_id": null,
  "status": "scheduled"
}
```

## 19.3 Recording Doctrine

Remote default:

```text
Laptop / Meet = conversation
Phone-native vertical video = master
Meeting recording = backup
```

The app includes a calibration page for:

- vertical orientation;
- face position;
- safe zones;
- lighting;
- audio;
- storage/battery reminder;
- background clutter;
- test recording.

## 19.4 Quality Gate

A session may start with warnings, but the system records:

```text
orientation
framing
lighting
stability
audio
file safety
consent
```

If master capture is unusable, the operator explicitly accepts the risk.

## 19.5 Recording Artifacts

Artifacts include:

- phone master video;
- call backup;
- separate audio;
- calibration clip;
- transcript;
- time-alignment data;
- upload checksums.

Originals are immutable.

## 19.6 Transcript

The transcript preserves:

- speaker;
- timestamps;
- language;
- pauses/fillers where relevant;
- confidence;
- edits;
- synchronization to source media.

Corrections create revisions.

## 19.7 Anchor Hits

Detect:

- selected First-Line Anchor;
- variants;
- Depth Anchor response;
- strong spontaneous openings;
- operator markers.

Do not require exact word-for-word repetition if the authentic opening is better.

---

# 20. Post-Session Extraction

## 20.1 Expression Moment

An Expression Moment is a bounded source segment that may support one or more assets.

```json
{
  "expression_moment_id": "em_...",
  "expression_session_id": "xes_...",
  "source_artifact_id": "video_...",
  "transcript_revision_id": "tr_...",
  "start_ms": 863000,
  "end_ms": 918000,
  "verbatim_text": "...",
  "language": "fr",
  "expression_states": ["cinematic", "vulnerability"],
  "source_contract_id": "iac_...",
  "anchor_hit_ids": [],
  "meaning_summary": "...",
  "edge_product_candidates": [],
  "archetype_candidates": [],
  "asset_route_candidates": [],
  "truth_integrity_notes": [],
  "review_status": "candidate"
}
```

## 20.2 Extraction Targets

Agents detect:

- complete stories;
- vulnerable specificities;
- teaching mechanisms;
- strong claims;
- contrasts;
- metaphors;
- micro-contradictions;
- signature phrases;
- reactions;
- polls/questions;
- data claims requiring verification;
- visual metaphors;
- Micro-Semiotic Anchor candidates from lived detail.

## 20.3 Grounding

Every extracted summary or route must link back to source timestamps and transcript text.

No source link means no production route.

## 20.4 Moment Approval

Human review can:

- adjust boundaries;
- merge/split;
- reject;
- redact;
- mark sensitive;
- approve for specific uses;
- forbid meme/humor reuse;
- require guest approval.

## 20.5 Archetype Route

A route combines:

```text
source moment
+ core archetype
+ asset derivative
+ optional meme mechanism
+ optional reaction archetype
+ CMF render mode
```

Each classification includes confidence and rationale.

## 20.6 Asset Package Spec

For a Guest Asset Pack, default target:

```text
4 videos
2 carousels
2 meme visuals
2 poll visuals
2–3 reaction seeds
```

This is a target, not permission to manufacture weak assets.

The spec states:

- selected moments;
- diversity across archetypes/states;
- routes;
- required approvals;
- expected costs;
- dependencies;
- fallback routes.

## 20.7 Post-Session Evaluation

Evaluate:

- capture quality;
- state induction;
- clean starts;
- depth;
- landing quality;
- authenticity;
- clipability;
- narrative density;
- emotional range;
- archetype coverage;
- asset yield;
- guest comfort;
- interviewer performance.

---

# 21. Complete Editing Session and Creative State

## 21.1 Complete Editing Session

The Complete Editing Session is the atomic media-production boundary.

```json
{
  "complete_editing_session_id": "ces_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "registry_bundle_version_id": "rbv_...",
  "source_expression_session_id": "xes_...",
  "source_expression_moment_id": "em_...",
  "asset_package_spec_id": "aps_...",
  "asset_type": "short_video",
  "core_archetype_id": "archetype.myth_debunk.v1",
  "asset_derivative_id": "asset_derivative.scene_to_principle.v1",
  "cmf_render_mode_id": "cmf.paper_cut_explainer.v1",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "platform_targets": ["instagram_reels", "tiktok", "youtube_shorts"],
  "status": "planned"
}
```

## 21.2 Creative State

The evolving state object includes:

```json
{
  "creative_state_id": "cs_...",
  "complete_editing_session_id": "ces_...",
  "stage": "scene_spec_validated",
  "source_context": {},
  "scene_spec": {},
  "composition_plan": null,
  "selected_assets": [],
  "provider_jobs": [],
  "layer_manifest_id": null,
  "rig_manifest_id": null,
  "animation_plan_id": null,
  "sfx_plan_id": null,
  "render_route": null,
  "render_output_ids": [],
  "evaluation_receipt_ids": [],
  "manual_review_flags": [],
  "errors": [],
  "lineage": []
}
```

Required stages:

```text
created
→ source_validated
→ brief_compiled
→ scene_spec_validated
→ assets_selected
→ composition_ready
→ edit_ready
→ layers_ready
→ animation_ready
→ render_ready
→ rendered
→ evaluated
→ needs_review
→ approved | revision_requested | rejected
→ publishing_ready
```

Not every route uses every stage, but skipped stages are explicitly `not_applicable`.

---

# 22. Provider Capability Architecture

## 22.1 Principle

Each external or local model is a replaceable provider behind an interface.

Provider selection considers:

- capability;
- quality;
- cost;
- latency;
- privacy;
- current availability;
- licensing;
- deterministic controls;
- accepted input/output formats.

## 22.2 Required Provider Interfaces

```text
ReasoningProvider
ResearchProvider
EmbeddingProvider
TranscriptionProvider
CompositionProvider
ImageAssetProvider
ImageEditProvider
IdentityConditioningProvider
LayerDecompositionProvider
SegmentationTrackingProvider
CharacterDecompositionProvider
RigProvider
RendererProvider
MotionTransferProvider
VideoGenerationProvider
PublishingProvider
```

## 22.3 Provider Capability Record

```json
{
  "provider_capability_id": "pc_...",
  "provider": "qwen",
  "model_or_service": "Qwen-Image-Layered",
  "capability": "semantic_rgba_layer_decomposition",
  "version": "...",
  "container_digest": "sha256:...",
  "input_contract": "...",
  "output_contract": "...",
  "supports_batch": true,
  "supports_seed": false,
  "data_policy": "...",
  "approved_status": "approved"
}
```

## 22.4 Exact Tool Roles

### Ideogram 4 — Composition Provider

Role:

- spatial composition;
- poster/editorial layout;
- subject placement;
- visual hierarchy;
- text-area planning;
- prop density;
- metaphor staging;
- palette and visual flow;
- Micro-Semiotic Anchor placement proposals.

Not responsible for:

- final identity;
- final editable typography;
- rigging;
- final layer stack;
- deterministic animation.

Production rule: use it as composition intelligence. Rebuild final text and approved assets where editability matters.

### GPT Image 2 — Image Asset Provider / Iterative Edit Provider

Role:

- realistic acting-reference generation;
- paper-cut avatar sheets;
- expression/mouth/gesture sheets;
- prop packs;
- background and metaphor packs;
- iterative repair/fix requests;
- stylized brand asset generation.

Not responsible for:

- canonical layer hierarchy;
- final skeleton;
- publishing;
- uncensored identity mutation.

### Flux 2 Klein 9b - Image Edit Provider

Role:

- character replacement;
- identity-preserving adaptation;
- integrating selected acting references into a composition;
- local repair;
- style harmonization;
- edge/lighting cleanup;
- production refinement.

It receives a composition, approved reference(s), Brand Context, and constrained edit contract.

### Qwen-Image-Layered — Layer Decomposition Provider

Exact role:

> Convert a flattened RGB composition into a semantically separated multi-RGBA layer stack.

Use for:

- Ideogram/Flux 2 Klein 9b paper-cut scene decomposition;
- poster layer recovery;
- prop-sheet separation;
- recovering editable layers from flattened comps.

It is not:

- a precision tracker;
- a skeleton generator;
- a final rigging engine.

### SAM3 — Segmentation and Tracking Provider

Exact role:

> Produce precise object/person masks and track selected concepts through image/video sequences.

Use for:

- cleaning Qwen-generated layer masks;
- isolating a client from real interview footage;
- tracking the subject or prop across video;
- separating hands, plants, cups, notes, or hero objects;
- alpha cutouts and rotoscoping support.

It is not:

- a semantic full-scene layer-stack planner;
- a hidden-part completion engine;
- a rig generator.

### See-Through — Character Decomposition Provider

Exact role:

> Assist with character/body-part decomposition and hidden-region completion for animation-oriented 2D/2.5D characters.

Use selectively for:

- paper-cut avatar body-part separation;
- character-specific layer recovery;
- hidden regions behind limbs;
- candidate rig assets.

Because its strongest demonstrated domain may not exactly match every client style, all outputs require QC and a fallback route.

### Stretchy Studio / Custom Rigging — Rig Provider

Role:

- anchor and pivot authoring;
- parent/child skeleton;
- mesh/deformation where useful;
- expression and gesture presets;
- export to canonical rig manifest.

Do not let the project file become the only source of rig truth.

### Remotion — Default Renderer Provider

Role:

- final deterministic compilation;
- vertical video;
- real footage + overlays;
- paper-cut explainers;
- subtitles;
- text;
- SFX;
- social packaging;
- carousels rendered as video;
- final assembly of outputs from other renderers/providers.

### Motion Canvas — Procedural Explainer Renderer

Use for:

- framework diagrams;
- vector explainers;
- voice-synchronized teaching;
- procedural motions where React video templates are insufficient.

### Manim — Data / Procedural Story Renderer

Use for:

- bar-chart races;
- timelines;
- data stories;
- abstract diagrams;
- generated visual metaphors based on procedural geometry.

Final packaging may still occur in Remotion.

### HyperFrames — Agent-Native HTML Motion Renderer

Use for:

- rapid agent-authored HTML/CSS/JS compositions;
- lightweight motion graphics;
- prototype render modes;
- cases where browser-native scene generation is an advantage.

It is not the default final compiler.

### SCAIL-2 — Motion Transfer Provider

Use for:

- memes;
- dance clips;
- reaction formats;
- known reusable motion assets;
- specific character replacement/motion-transfer cases.

Do not route complex cinematic storytelling here.

### Video Generation Provider

Use for:

- cinematic metaphors;
- complex camera movement;
- atmospheric films;
- scene motion that is impractical to construct deterministically.

Final packaging, captions, and approvals remain in CMF.

### Self-Hosted ComfyUI Docker - GPU Workflow Execution Provider

Role:

- execute versioned ComfyUI workflow graphs;
- batch identity-conditioned image editing;
- batch layer repair;
- batch model inference;
- return assets and execution metadata.

The worker runs as a hosted ComfyUI Docker instance on AWS or Google Cloud using a 24GB or 32GB VRAM GPU node. The worker adapter must not expose arbitrary graph mutation to the agent in production. Use approved workflow templates and typed parameters.

### Publer — Publishing Provider

Role:

- connected social accounts;
- media upload;
- draft/schedule/publish operations;
- job-status retrieval;
- post/analytics retrieval where available.

CMF remains the source of truth for approvals, captions, schedule intent, and provenance.

## 22.5 Provider Receipts

Every provider call stores:

- input hashes;
- provider and model version;
- workflow/template version;
- parameters;
- seed where applicable;
- start/end time;
- cost estimate/actual;
- output hashes;
- error/retry history;
- data policy route;
- container digest for local workers.

---

# 23. Composition System

## 23.1 SceneSpec

The SceneSpec is renderer-independent.

It contains:

- asset type;
- aspect ratio/duration;
- source message;
- text hierarchy;
- emotional intent;
- subject;
- gesture/body language;
- main metaphor;
- visual flow;
- objects;
- Micro-Semiotic Anchors;
- safe zones;
- style;
- motion intent;
- platform constraints.

## 23.2 Composition Plan

The Composition Plan translates SceneSpec into explicit spatial constraints.

```json
{
  "layout_template": "headline_top_notes_left_avatar_lower_right",
  "canvas": {"width": 1080, "height": 1920},
  "regions": [
    {"id": "headline", "bbox": [80, 80, 920, 250]},
    {"id": "notes", "bbox": [80, 390, 580, 1050]},
    {"id": "avatar", "bbox": [600, 780, 420, 980]}
  ],
  "visual_flow": "top_to_left_to_avatar",
  "text_safe_zones": [],
  "anchor_placements": [],
  "density": "medium"
}
```

## 23.3 Ideogram Route

### Fast Route

```text
SceneSpec
→ Ideogram composition plate
→ overlay approved text/avatar
→ light Remotion animation
```

Use for lower-cost or short-lived assets.

### Reconstructed Premium Route

```text
SceneSpec
→ Ideogram composition plate
→ composition analysis
→ approved asset retrieval
→ deterministic scene reconstruction
→ final text in Remotion/SVG
→ layer animation
```

Use for reusable premium production.

## 23.4 Text Rule

Final production text is rendered deterministically wherever possible.

Do not regenerate an entire AI image to fix a typo.

## 23.5 Composition Library

Store approved composition patterns with:

- scene types;
- object density;
- audience/platform;
- performance;
- compatible motion recipes;
- brand adaptations;
- negative examples.

The agent may retrieve and adapt, not blindly reuse.

---

# 24. Layer Decomposition, Segmentation, and Repair

## 24.1 Standard Pipeline

```text
flattened composition
→ Qwen-Image-Layered semantic RGBA decomposition
→ SAM3 precision mask refinement
→ See-Through character-specific decomposition if required
→ Flux 2 Klein 9b/GPT Image 2 repair of missing/fused regions
→ layer QC
→ LayerManifest
→ optional RigManifest
```

## 24.2 Why All Are Needed

- Qwen-Image-Layered solves scene-level semantic decomposition.
- SAM3 solves precision and tracking.
- See-Through solves character-oriented decomposition and hidden regions.
- Flux 2 Klein 9b/GPT Image 2 repairs visual gaps.
- human review resolves ambiguous hero assets.

They are not interchangeable.

## 24.3 Layer Manifest

Each layer records:

```text
layer_id
semantic_type
asset_uri
alpha_uri
z_index
bbox
anchor
parent
casts_shadow
shadow_layer_id
alpha_quality
edge_quality
semantic_confidence
motion_affordances
review_state
```

## 24.4 Required QC

Hard failures:

- client fused to background;
- text baked when editable text is required;
- missing hero object;
- broken alpha at face/hands;
- incorrect z-order;
- shadow irreparably fused;
- layer too small for intended motion;
- hidden body region not reconstructed.

## 24.5 Video Cutout Route

For real interview footage:

```text
source video
→ SAM3 subject segmentation/tracking
→ temporal mask smoothing
→ edge/halo correction
→ alpha video or foreground/background composite
→ Remotion
```

Do not use Qwen-Image-Layered as a video tracker.

---

# 25. Animation and Rendering

## 25.1 Animation Plan

```json
{
  "animation_plan_id": "anim_...",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "fps": 30,
  "duration_frames": 900,
  "motion_recipe_id": "motion.myth_busted.v1",
  "events": [],
  "camera": {},
  "global_texture_motion": {},
  "sfx_plan_id": "sfxplan_..."
}
```

## 25.2 Timeline Events

Each event contains:

- frame/time;
- target layer;
- motion primitive;
- duration;
- easing/style;
- expression change;
- SFX;
- synchronization source;
- priority.

## 25.3 Audio Synchronization

Primary authentic audio drives:

- sentence/phrase timings;
- typography reveals;
- annotation strokes;
- avatar expression changes;
- pauses;
- SFX ducking.

## 25.4 Renderer Router

Decision logic:

```text
Real coach footage with branded overlays?
→ Remotion

Layered paper-cut explainer?
→ Remotion, optional Motion Canvas segment

Procedural framework or voice-synced diagram?
→ Motion Canvas, package in Remotion

Data story / bar-chart race / timeline?
→ Manim or Motion Canvas, package in Remotion

Quiz / ranking / Goal-style component video?
→ Remotion

Meme/dance/reaction motion transfer?
→ SCAIL-2, package in Remotion

Cinematic atmospheric scene?
→ video generation provider, package in Remotion

Fast HTML-native motion prototype?
→ HyperFrames
```

## 25.5 Bar-Chart Race Route

```text
validated dataset
→ data story analysis
→ highlight event detection
→ narrative beat plan
→ Manim/Motion Canvas animation
→ annotations and voice sync
→ Remotion brand packaging
→ evaluation
```

The system should not only animate ranks; it should identify meaningful overtakes, inflection points, and narrative emphasis.

## 25.6 Quiz / Ranking Route

```text
validated facts
→ quiz/ranking spec
→ question/timer/reveal components
→ brand assets and micro-semiotic anchors
→ Remotion
→ evaluation
```

## 25.7 Render Receipts

Record:

- source IDs;
- Brand Context hash;
- Registry Bundle hash;
- selected assets;
- renderer version;
- code commit;
- container digest;
- environment;
- fonts/assets hashes;
- output hash;
- duration/resolution;
- warnings.

---

# 26. Evaluation, Review, and Approval

## 26.1 Evaluation Layers

### Research Evaluation

- source quality;
- recency;
- claim grounding;
- contradiction handling;
- fact/inference separation.

### Interview Evaluation

- state induction;
- anchor success;
- depth;
- specificity;
- authenticity;
- naturalness;
- guest comfort;
- landing;
- asset routeability.

### Identity Asset Evaluation

- likeness;
- age/body/hair consistency;
- emotional clarity;
- gesture/body language;
- hands;
- crop;
- artifact level.

### Composition Evaluation

- hierarchy;
- text safety;
- metaphor clarity;
- density;
- visual flow;
- micro-semiotic anchor subtlety;
- platform fit.

### Animation Evaluation

- restraint;
- attention guidance;
- voice synchronization;
- paper tactility;
- SFX discipline;
- client authority;
- legibility.

### Final Asset Evaluation

- source truth preserved;
- archetype fit;
- identity;
- emotion;
- style;
- Negative Space;
- hook;
- shareability;
- routeability;
- legal/safety;
- platform constraints.

## 26.2 Configurable Thresholds

Scores are calibration aids, not objective truth.

Initial candidate thresholds may be configured per brand/route, for example:

```text
identity >= 0.86
emotion >= 0.82
composition >= 0.85
style >= 0.88
negative_space >= 0.95
```

Never approve solely because a score passes.

## 26.3 Hard Fail Conditions

- wrong identity;
- source meaning distorted;
- fabricated claim;
- missing consent;
- severe visual artifact;
- unreadable text;
- broken hero-frame face/hands;
- unsafe claim;
- prohibited visual style;
- demeaning stereotype;
- unapproved trademark usage;
- synthetic primary voice impersonation;
- wrong brand or platform;
- missing provenance;
- public publishing without confirmation.

## 26.4 Approval Event

```json
{
  "approval_event_id": "ae_...",
  "object_type": "render_output",
  "object_id": "render_...",
  "decision": "approved|needs_fix|rejected",
  "reviewer_user_id": "user_...",
  "notes": "...",
  "tags": [],
  "created_at": "..."
}
```

Approvals are append-only.

## 26.5 Revision

A revision request creates:

- structured issues;
- desired outcome;
- preserved elements;
- allowed provider route;
- new Creative State branch;
- comparison link.

Do not overwrite the prior output.

---

# 27. Publishing

## 27.1 PublishingIntent

The internal publishing object exists before Publer.

It contains:

- approved render;
- brand;
- platform variants;
- captions;
- schedule;
- account mapping;
- approval;
- compliance notes.

## 27.2 Flow

```text
render approved
→ platform adaptations compiled
→ PublishingIntent drafted
→ operator review
→ explicit confirmation
→ media upload to Publer
→ schedule/draft request
→ external job ID stored
→ status polling/webhook
→ publication result
→ performance ingestion
```

## 27.3 Safety

- no one-tap public publishing;
- Telegram “schedule” opens a confirmation step;
- account and platform are displayed;
- time zone is explicit;
- duplicate-post checks;
- idempotency keys;
- revoked token handling;
- rollback/cancel where platform allows.

## 27.4 Publer Is an Adapter

CMF owns:

- asset;
- approval;
- caption;
- schedule intent;
- source lineage;
- platform strategy.

Publer owns external delivery.

## 27.5 Performance Memory

Import available metrics and relate them to:

- archetype;
- opening;
- expression state;
- render mode;
- composition;
- anchor;
- motion recipe;
- platform;
- posting time.

Do not optimize only for views. Maintain truth, brand fit, and audience quality metrics.
# 28. Memory and Learning Architecture

## 28.1 Memory Types

### Brand Memory

- approved language and visual preferences;
- rejected patterns;
- identity observations;
- audience cues;
- high-performing anchors;
- approved compositions;
- route performance;
- platform behavior.

### Guest Memory

- prior sessions;
- boundaries;
- themes;
- expression-state strengths;
- stories already used;
- recurring metaphors;
- approvals.

### Interviewer Memory

- question strengths;
- follow-up patterns;
- interruption habits;
- accepted/ignored cues;
- state-induction performance;
- authentic curiosity themes.

### Production Memory

- provider reliability;
- workflow failures;
- average regeneration count;
- route cost;
- layer QC performance;
- renderer compatibility.

## 28.2 Memory Admission

A candidate memory is proposed from an event.

It enters durable memory only when:

- evidence is linked;
- confidence is stated;
- scope is clear;
- it does not conflict with consent;
- it is approved by policy or human review.

## 28.3 Postgres and Neo4j

PostgreSQL stores canonical records.

Neo4j projects relationships such as:

```text
Brand USES Anchor
Guest EXPRESSED Theme
Question INDUCED State
DepthAnchor UNLOCKED ExpressionMoment
ExpressionMoment ROUTED_TO Archetype
Asset USED MotionRecipe
Post PERFORMED_WITH AudienceSegment
```

Projection failures must not block transactional work. They are retried from domain events.

## 28.4 Vector Retrieval

Use pgvector for:

- transcript semantic search;
- similar expression moments;
- registry example retrieval;
- prior question retrieval;
- micro-semiotic anchor retrieval;
- composition retrieval.

Vector similarity never overrides brand scope or approval status.

---

# 29. Data Architecture

## 29.1 Core Tables

### Identity and tenancy

```text
organizations
users
organization_memberships
brand_workspaces
brand_memberships
roles
api_credentials
audit_log
```

### Brand Genesis

```text
brand_genesis_sessions
consent_records
source_media
source_media_qc
business_intelligence_versions
tribe_soul_versions
character_lexicon_versions
voice_dna_versions
negative_space_versions
visual_constitution_versions
identity_summaries
identity_pack_versions
acting_library_versions
acting_references
papercut_rig_versions
avatar_layers
facial_expression_assets
mouth_shape_assets
prop_library_versions
paper_object_assets
micro_semiotic_anchor_library_versions
micro_semiotic_anchors
motion_library_versions
motion_primitives
motion_recipes
sfx_library_versions
sfx_assets
composition_preference_versions
publishing_profile_versions
brand_context_versions
genesis_clearance_certificates
```

### Registries

```text
registry_entries
registry_entry_versions
registry_bundles
registry_bundle_entries
migration_ledger
registry_validation_runs
```

Registry source may live in version-controlled files; database tables provide active bundle metadata and audit.

### Research and Interview Intelligence

```text
research_fields
research_evidence
guest_profiles
guest_dossiers
audience_reality_briefs
context_premises
interviewer_profiles
interviewer_resonance_contexts
matrix_of_edging_briefs
narrative_state_maps
interview_preparations
interview_asset_contracts
interview_decks
live_interview_cues
```

### Expression

```text
complete_expression_sessions
recording_configurations
quality_gate_results
recording_artifacts
transcripts
transcript_segments
anchor_hits
expression_moments
expression_moment_reviews
archetype_routes
asset_package_specs
asset_package_items
```

### Production

```text
complete_editing_sessions
creative_states
scene_specs
composition_plans
asset_selections
provider_jobs
layer_manifests
layers
rig_manifests
animation_plans
sfx_plans
render_jobs
render_outputs
evaluation_receipts
evaluation_scores
revision_requests
approval_events
```

### Publishing and Learning

```text
publishing_intents
publishing_variants
external_media_assets
publishing_jobs
publishing_results
post_metrics
brand_memory_events
interviewer_memory_events
provider_performance
operator_notifications
agent_threads
agent_messages
agent_commands
domain_events
outbox_events
```

## 29.2 Database Conventions

- `snake_case`;
- UUIDv7/ULID primary IDs;
- UTC timestamps;
- explicit status enums;
- optimistic concurrency version;
- soft delete only where legally appropriate;
- immutable records append rather than update;
- JSONB only for bounded extensibility, not to avoid modeling;
- all queries brand-scoped;
- RLS tests mandatory.

## 29.3 Domain Events

Examples:

```text
BrandWorkspaceCreated
BrandGenesisStarted
ConsentRecorded
IdentitySummaryApproved
ActingReferenceGenerated
ActingReferenceApproved
PaperCutRigApproved
BrandContextLocked
ResearchFieldCompleted
ContextPremiseApproved
InterviewPreparationApproved
ExpressionSessionStarted
RecordingArtifactIngested
TranscriptCompleted
ExpressionMomentApproved
AssetPackageCompiled
EditingSessionCreated
RenderCompleted
EvaluationFailed
EvaluationPassed
RevisionRequested
RenderApproved
PublishingIntentConfirmed
PostPublished
BrandMemoryUpdated
```

Use the transactional outbox pattern.

## 29.4 Object Storage

Canonical path pattern:

```text
organizations/{organization_id}/
  brands/{brand_id}/
    genesis/{genesis_session_id}/
    source/photos/
    source/videos/
    identity/{identity_pack_version_id}/
    acting/{acting_library_version_id}/
    papercut/{rig_version_id}/
    props/{prop_library_version_id}/
    anchors/{anchor_library_version_id}/
    motions/{motion_library_version_id}/
    sfx/{sfx_library_version_id}/
    research/{research_field_id}/
    expression/{expression_session_id}/
    editing/{editing_session_id}/
    renders/{render_output_id}/
    publishing/{publishing_intent_id}/
```

Objects use immutable names/content hashes. Friendly names exist in metadata.

---

# 30. Durable Workflow Architecture

## 30.1 Why Durable Workflows

The system contains:

- multi-hour external generations;
- batch jobs;
- human approvals;
- retries;
- provider failures;
- long gaps between interview and delivery;
- versioned business logic.

Use the Temporal Python SDK or an approved equivalent durable workflow engine. Pi and DSPy orchestrate decisions; the workflow engine owns resumability, timers, retries, signals, and long-running execution.

## 30.2 Workflow Rules

- workflows orchestrate; activities perform side effects;
- activities are idempotent;
- all external requests have idempotency keys;
- human approval is a durable signal;
- provider callbacks/polls signal workflows;
- each completed unit checkpoints;
- workflow versions are explicit;
- no long-running state stored only in process memory.

## 30.3 Core Workflows

### BrandGenesisWorkflow

```text
create session
→ validate consent
→ ingest/QC source media
→ compile business/tribe/lexicon/voice drafts
→ approve identity summary
→ generate 64 acting assets in batches
→ review gate
→ generate paper-cut avatar pack
→ decompose and rig
→ rig review gate
→ generate prop/anchor/motion/SFX libraries
→ final adversarial evaluation
→ human approval
→ lock Brand Context
→ issue Genesis Clearance Certificate
```

### InterviewPreparationWorkflow

```text
define interview objective
→ research guest
→ research audience
→ build evidence graph
→ propose Context Premises
→ interviewer pre-induction
→ Matrix of Edging
→ Narrative State Map
→ compile Interview Asset Contracts
→ deck review
→ freeze Interview Preparation
```

### CompleteExpressionSessionWorkflow

```text
schedule
→ quality gate
→ start
→ record markers/cues
→ finish
→ ingest recordings
→ transcribe/synchronize
→ extract anchor hits
→ extract expression moments
→ human review
→ evaluate session
→ compile Asset Package Spec
```

### CompleteEditingSessionWorkflow

```text
validate source and context
→ compile brief
→ retrieve assets
→ create SceneSpec
→ route renderer/providers
→ execute composition/edit/layer jobs
→ create Animation/SFX plan
→ render
→ evaluate
→ review
→ approve or branch revision
```

### PublishingWorkflow

```text
compile platform variants
→ create PublishingIntent
→ confirmation
→ upload media
→ schedule/publish through adapter
→ monitor result
→ ingest performance
→ create learning event
```

## 30.4 Batch Job Behavior

For each expensive worker:

```text
claim batch
→ warm/load model
→ for each item:
    validate input hashes
    execute
    upload output
    write receipt
    mark item complete
→ release/terminate
```

A preemption loses at most the in-progress item.

## 30.5 Failure Taxonomy

```text
validation_failure
consent_failure
research_grounding_failure
provider_unavailable
provider_policy_rejection
composition_failure
identity_failure
emotion_mismatch
reference_gap
layer_decomposition_failure
segmentation_failure
rig_failure
renderer_failure
evaluation_failure
publishing_failure
external_auth_failure
workflow_timeout
human_review_timeout
```

Every failure maps to:

- retry policy;
- fallback;
- human escalation;
- cost limit;
- terminal state.

---

# 31. Infrastructure and Deployment

## 31.1 Environment Model

```text
local
development
staging
production
```

Staging must have isolated provider credentials and synthetic/test brands.

## 31.2 GCP Primary

Recommended primary control plane:

- Cloud Run or GKE Autopilot for API and CPU workers;
- Cloud SQL PostgreSQL;
- GCS;
- Artifact Registry;
- Secret Manager;
- Cloud Logging/Monitoring or OpenTelemetry backend;
- GCP Batch / Spot GPU jobs;
- managed DNS/load balancer.

## 31.3 AWS Secondary

Use AWS for:

- overflow GPU batch capacity;
- specific accelerator availability;
- disaster-recovery copies if justified;
- S3 scratch/mirror;
- AWS Batch/Spot.

Avoid unnecessary cross-cloud transfers. Copy only the job inputs/outputs required for overflow execution.

## 31.4 Local Inference

A local Qwen-class endpoint may serve:

- routing;
- extraction;
- schema tasks;
- drafts.

Expose it through a secure provider gateway.

The production system must have health checks and a configured fallback if the local machine is offline.

## 31.5 Containers

Pin:

- base image;
- CUDA/runtime;
- model weights;
- workflow files;
- Python dependencies and TypeScript leaf-runtime dependencies;
- fonts;
- ffmpeg version;
- renderer version.

All containers produce SBOMs and image digests.

## 31.6 GPU Cost Discipline

- no idle GPU;
- batch compatible work;
- cost estimate before expensive command confirmation;
- per-brand/job budgets;
- spot/preemptible where retry-safe;
- model weight cache;
- output checkpointing;
- maximum retry and spend caps.

## 31.7 Infrastructure as Code

Terraform must provision:

- environments;
- networks;
- service identities;
- buckets;
- database;
- secrets;
- queues/workflow workers;
- monitoring;
- batch compute;
- backup policies.

Manual cloud console changes are treated as drift.

---

# 32. Security, Privacy, and Governance

## 32.1 Data Classes

Classify:

```text
public
internal
confidential_brand
sensitive_personal
biometric_likeness
authentication_secret
```

Photos, voice, face embeddings, identity packs, and personal interview disclosures are sensitive.

## 32.2 Encryption

- TLS in transit;
- managed encryption at rest;
- field/envelope encryption for provider tokens;
- signed URLs;
- no secrets in logs;
- KMS-backed key rotation where practical.

## 32.3 Consent Enforcement

Every provider job checks:

- asset owner;
- consent version;
- allowed transformation;
- allowed third party;
- allowed publication context;
- retention.

## 32.4 Audit

Audit:

- brand access;
- asset download;
- identity generation;
- approval;
- context lock;
- agent command;
- publishing;
- consent change;
- export/deletion.

## 32.5 Telegram Security

- validate Mini App init data server-side;
- webhook secret;
- map Telegram identity to CCP user;
- enforce role and brand scope;
- expire deep links;
- no sensitive assets in unprotected public URLs.

## 32.6 Provider Data Policy

The Provider Capability Registry states:

- data retention;
- training use;
- region;
- privacy tier;
- acceptable content;
- contract status.

Sensitive brands can prohibit certain providers.

## 32.7 Right to Delete and Export

Implement:

- brand export;
- source asset export;
- model-derived asset export;
- deletion workflow;
- legal hold;
- downstream provider deletion requests where supported;
- tombstone/audit strategy.

## 32.8 Safety and Dignity

The system must not:

- manipulate guests into disclosure;
- exploit unresolved trauma;
- misrepresent their words;
- generate humiliating likenesses without consent;
- use micro-semiotic anchors as stereotypes;
- fabricate medical authority;
- publish sensitive clips without the required approval.

---

# 33. Observability

## 33.1 Correlation

Every operation carries:

```text
trace_id
workflow_id
organization_id
brand_id
session_id
editing_session_id
provider_job_id
agent_command_id
```

## 33.2 Metrics

### Product

- brands onboarded;
- context lock time;
- acting-asset approval rate;
- interview prep time;
- expression moment yield;
- asset package completion;
- approval turnaround;
- posts published.

### Quality

- identity pass rate;
- anchor success;
- depth success;
- route accuracy;
- average revisions;
- motion/style pass;
- source truth failures;
- publishing failures.

### Cost

- cost by brand;
- cost by provider;
- GPU minutes;
- cost per approved asset;
- regeneration cost;
- storage and egress.

### Reliability

- workflow success;
- queue age;
- provider error;
- batch interruption;
- retry count;
- time to recovery.

## 33.3 Logs

Structured JSON logs.

Do not log:

- raw secrets;
- complete sensitive transcripts by default;
- unredacted face embeddings;
- provider credentials.

## 33.4 Traces

Trace across:

```text
agent request
→ command
→ workflow
→ provider job
→ render
→ evaluation
→ approval
→ publishing
```

## 33.5 Alerts

Alert on:

- cross-brand authorization attempt;
- production registry invalid;
- failed context lock;
- stuck workflow;
- GPU spend threshold;
- repeated identity failure;
- publication mismatch;
- provider credential expiry;
- backup failure.

---

# 34. Testing Strategy

## 34.1 Test Pyramid

### Unit

- schema validation;
- registry compatibility;
- scoring;
- state transitions;
- permission rules;
- compilers.

### Integration

- database/RLS;
- object storage;
- Temporal activities;
- provider adapters with recorded fixtures;
- Telegram auth;
- Publer sandbox/draft flow;
- Remotion rendering.

### Contract

Every provider adapter passes the same capability contract tests.

### Workflow

Test retries, human signals, timeouts, cancellation, and idempotency.

### Golden

Use approved legacy and new scenarios.

### End-to-End

Run complete brand-to-publication paths in staging.

## 34.2 Golden Scenarios

At minimum:

1. holistic-health Brand Genesis and paper-cut Myth Debunk;
2. identity/belonging guest interview with cinematic and carousel routes;
3. real coach footage with SAM3 cutout and Remotion overlays;
4. data story/bar-chart race;
5. Goal-style quiz/ranking;
6. meme/dance motion transfer;
7. cinematic metaphor;
8. Telegram revision and Publer schedule confirmation;
9. provider failure and resume;
10. context-version update preserving historical reproducibility.

## 34.3 Evaluation Calibration

Model judges require human-calibrated sets.

Maintain:

- pass examples;
- borderline examples;
- hard failures;
- brand-specific exceptions;
- inter-rater comparisons.

## 34.4 Security Tests

- RLS cross-tenant attempts;
- Telegram initData tampering;
- signed URL expiry;
- prompt injection in research;
- permission escalation;
- duplicate publish;
- leaked secret scan;
- malicious file upload.

## 34.5 Performance Tests

- large transcripts;
- 64-asset generation batch;
- concurrent brands;
- render queue bursts;
- Telegram webhook load;
- Publer rate limits;
- object-storage upload/download.

---

# 35. Repository Structure

```text
ccp-studio/
├── pyproject.toml
├── uv.lock
├── package.json                         # TypeScript leaf-workspace only
├── pnpm-workspace.yaml                  # PWA / Mini App / renderers only
├── apps/
│   ├── api/                             # FastAPI composition root
│   ├── telegram-bot/                    # Python bot/webhook surface
│   ├── workflow-worker/                 # Temporal Python workflows/activities
│   ├── batch-dispatcher/                # Python cloud batch dispatch
│   ├── studio-web/                      # Next.js PWA, TypeScript
│   ├── telegram-mini-app/               # Next.js Mini App, TypeScript
│   ├── remotion-renderer/               # Remotion, TypeScript
│   ├── motion-canvas-renderer/           # TypeScript, optional route
│   └── registry-admin/                  # PWA route/app over Python APIs
├── python/
│   └── ccp_studio/
│       ├── contracts/                   # Pydantic source of truth
│       │   ├── domain/
│       │   ├── commands/
│       │   ├── events/
│       │   ├── providers/
│       │   ├── workflows/
│       │   └── rendering/
│       ├── registries/
│       │   ├── kernel/
│       │   ├── core_archetypes/
│       │   ├── asset_derivatives/
│       │   ├── meme_mechanisms/
│       │   ├── reaction_archetypes/
│       │   ├── cmf_render_modes/
│       │   └── supporting/
│       ├── dspy_runtime/
│       │   ├── signatures/
│       │   ├── modules/
│       │   ├── optimizers/
│       │   ├── evaluators/
│       │   └── program_registry/
│       ├── pi_orchestrator/
│       │   ├── gateway/
│       │   ├── contexts/
│       │   ├── planning/
│       │   ├── policies/
│       │   └── specialist_agents/
│       ├── command_bus/
│       ├── workflows/
│       ├── brand_engine/
│       ├── research_engine/
│       ├── interview_engine/
│       ├── expression_engine/
│       ├── asset_compiler/
│       ├── cmf_engine/
│       ├── evaluation_engine/
│       ├── memory_engine/
│       ├── publishing/
│       ├── providers/
│       │   ├── local_qwen/
│       │   ├── openai_image/
│       │   ├── ideogram/
│       │   ├── flux/
│       │   ├── qwen_image_layered/
│       │   ├── sam3/
│       │   ├── see_through/
│       │   ├── manim/
│       │   ├── scail2/
│       │   ├── video_generation/
│       │   ├── comfyui_gpu/
│       │   └── publer/
│       ├── persistence/
│       ├── storage/
│       ├── observability/
│       ├── security/
│       └── settings/
├── generated/
│   ├── json-schema/                     # generated from Pydantic
│   ├── openapi/
│   ├── typescript/                      # generated interfaces
│   └── zod/                             # optional generated client validators
├── registries/                          # versioned data entries, not runtime code
├── infrastructure/
│   ├── terraform/
│   ├── docker/
│   └── environments/
├── fixtures/
│   ├── legacy-golden/
│   ├── dspy-evals/
│   ├── provider-recordings/
│   └── e2e/
├── docs/
│   ├── adr/
│   ├── runbooks/
│   ├── migration/
│   └── product/
├── scripts/
├── legacy-reference/                    # mounted/read-only during migration
└── tests/
    ├── unit/
    ├── contracts/
    ├── integration/
    ├── workflows/
    ├── dspy/
    ├── security/
    └── e2e/
```

## 35.1 Dependency Direction

```text
PWA / Mini App / renderer apps
→ generated TypeScript contracts
→ Python API

Python application services
→ domain contracts + registry kernel
→ command bus / workflow interfaces

Pi orchestrator
→ DSPy program registry + approved tools
→ typed commands

provider adapters
→ provider contracts + infrastructure

domain and registry packages
↛ provider SDKs
↛ React / TypeScript packages
```

The Python domain must import and test without any frontend or provider SDK installed.

## 35.2 Engineering Standards

### Python Harness

- Python version pinned and reproducible;
- Pydantic v2 for canonical contracts;
- no untyped dictionaries across domain boundaries;
- strict static checking with mypy or Pyright;
- Ruff formatting/linting;
- pytest for unit, contract, workflow, integration, and end-to-end tests;
- SQLAlchemy/Alembic mappings must not redefine domain meaning;
- DSPy programs versioned and evaluated against pinned fixtures;
- Pi actions expressed through approved tools and Pydantic commands;
- commands and activities idempotent;
- exhaustive state-machine handling;
- provider calls wrapped behind capability contracts;
- no hidden environment-dependent behavior.

### TypeScript Surfaces

- TypeScript strict mode;
- generated domain types are read-only artifacts;
- no hand-authored shadow schemas for canonical objects;
- local Zod validation may be generated from Pydantic schemas;
- UI state never becomes workflow state;
- Remotion and Motion Canvas consume versioned render contracts;
- no business routing or publishing policy inside renderer code.

### All Runtimes

- migrations reviewed;
- all public APIs documented;
- every side effect has telemetry and receipts;
- no feature without tests, provenance, failure behavior, and rollback notes.

---

# 36. API and Command Surface

## 36.1 External API Groups

```text
/auth
/organizations
/brands
/brand-genesis
/registries
/research
/interview-preparations
/expression-sessions
/expression-moments
/asset-packages
/editing-sessions
/renders
/evaluations
/approvals
/publishing
/agent
/telegram
/webhooks
/system
```

## 36.2 Agent Commands

Required families:

### Brand

```text
CREATE_BRAND
START_BRAND_GENESIS
REQUEST_IDENTITY_SUMMARY
GENERATE_ACTING_BATCH
REQUEST_ASSET_FIX
APPROVE_GENESIS_ASSET
LOCK_BRAND_CONTEXT
FORK_BRAND_CONTEXT
```

### Research / Interview

```text
START_RESEARCH_FIELD
ADD_CONTEXT_PREMISE
APPROVE_CONTEXT_PREMISE
START_INTERVIEWER_PREINDUCTION
COMPILE_INTERVIEW_CONTRACTS
APPROVE_INTERVIEW_DECK
MARK_LIVE_MOMENT
```

### Expression

```text
INGEST_RECORDING
REQUEST_TRANSCRIPTION
APPROVE_EXPRESSION_MOMENT
REJECT_EXPRESSION_MOMENT
COMPILE_ASSET_PACKAGE
```

### Production

```text
CREATE_EDITING_SESSION
GENERATE_COMPOSITION
SELECT_APPROVED_ASSETS
REQUEST_IMAGE_EDIT
DECOMPOSE_LAYERS
REFINE_MASKS
BUILD_RIG
GENERATE_ANIMATION_PLAN
START_RENDER
REQUEST_RENDER_REVISION
APPROVE_RENDER
```

### Publishing

```text
CREATE_PUBLISHING_INTENT
UPDATE_PLATFORM_VARIANT
REQUEST_PUBLISHING_CONFIRMATION
CONFIRM_SCHEDULE
CANCEL_SCHEDULE
SYNC_PUBLISHING_STATUS
```

## 36.3 Webhooks

- Telegram;
- provider callbacks;
- Publer;
- upload completion;
- batch job events.

All webhooks:

- verify signature/secret;
- persist raw envelope safely;
- deduplicate;
- enqueue processing;
- return quickly.

---

# 37. Documentation and ADR Requirements

Before implementation choices become dependencies, maintain ADRs for:

```text
greenfield runtime
modular monolith
contract technology
database and RLS
workflow engine
agent command bus
provider adapters
Brand Context immutability
registry bundles
Neo4j projection
object storage
Telegram surface
publishing safety
identity determinism
authentic voice policy
GPU batch strategy
```

Runbooks required:

- provider outage;
- failed render;
- identity drift;
- stuck workflow;
- wrong publication;
- credential rotation;
- data export/deletion;
- restore from backup;
- registry rollback;
- Brand Context rollback.

---

# 38. Public Release Position

The product released publicly is not a partial editor.

It is a complete CCP Studio production loop.

Internal development may expose incomplete screens to the operator, but external clients must not encounter broken chains or workflows that end in manual mystery.

The release artifact must include:

- PWA;
- agentic Telegram bot/Mini App;
- Brand Genesis;
- Interview Intelligence;
- Complete Expression Sessions;
- CMF production;
- evaluation/review;
- publishing;
- memory;
- security/observability/recovery.

Detailed sequence and gates are in document 03.

---

# 39. Final Doctrine

The final implementation must preserve these truths:

> The interview is not raw material for editing. It is the source event.

> The app should make the operator a better interviewer before it makes them a faster editor.

> Onboarding is the manufacturing of a reusable creative universe.

> Micro-Semiotic Anchoring makes the audience feel recognized before the message is explained.

> Editorial 2.5D Paper-Cut animation should feel like paper gently coming alive.

> Qwen-Image-Layered, SAM3, See-Through, editing models, rigging tools, and renderers solve different stages and should be orchestrated rather than conflated.

> The backend should retrieve, compose, animate, evaluate, publish, and remember from approved context—not reinvent the brand every time.

> The agent is not the system of record. The agent is the intelligent operator of a stateful, typed, auditable production system.

---

# CCP Studio V2 — Pydantic Domain Contracts, Commands, Events, and State Machines

**Companion to:** `01_CCP_STUDIO_GREENFIELD_MASTER_SPEC.md`  
**Purpose:** provide an implementation-oriented catalog of the canonical objects and durable state transitions  
**Rule:** these examples define semantics. Implementation must encode them as canonical Pydantic v2 models, then project them into JSON Schema, OpenAPI, generated TypeScript types, optional client-side Zod validators, database mappings, DSPy input/output models, and workflow payloads.

---

# 1. Contract Conventions

## 1.0 Contract Authority

Pydantic is the sole semantic contract authority.

Rules:

1. Every canonical object is a versioned `BaseModel` or a discriminated union of Pydantic models.
2. Immutable historical objects use frozen model configuration and content hashes.
3. Commands, events, provider jobs, workflow inputs, render contracts, receipts, and registry entries must reject unknown or invalid fields according to their compatibility policy.
4. SQLAlchemy models are persistence mappings, not competing domain contracts.
5. DSPy signatures consume and return Pydantic-compatible structures. A DSPy prediction is validated before it enters domain state.
6. JSON Schema and OpenAPI are generated from the Python source models.
7. TypeScript interfaces and optional Zod validators are generated outputs. Hand edits are forbidden.
8. Backward compatibility is tested at the Pydantic/model-migration layer.
9. Pi Coding Agent may propose contract instances but may not invent unregistered command types at runtime.

Recommended package split:

```text
ccp_studio.contracts.domain
ccp_studio.contracts.commands
ccp_studio.contracts.events
ccp_studio.contracts.providers
ccp_studio.contracts.workflows
ccp_studio.contracts.rendering
```

---


## 1.1 Envelope

All commands, events, and provider jobs use a common envelope.

```json
{
  "schema_version": "1.0.0",
  "id": "01J...",
  "organization_id": "01J...",
  "brand_id": "01J...",
  "brand_context_version_id": "01J... or null",
  "correlation_id": "01J...",
  "causation_id": "01J... or null",
  "idempotency_key": "string",
  "actor": {
    "type": "user|agent|workflow|system|provider",
    "id": "..."
  },
  "created_at": "ISO-8601 UTC"
}
```

## 1.2 Common Versioned Fields

```json
{
  "version_id": "01J...",
  "semantic_version": "1.0.0",
  "parent_version_id": null,
  "status": "draft|in_review|approved|locked|deprecated",
  "content_hash": "sha256:...",
  "created_by": "user-or-agent-id",
  "approved_by": null,
  "approved_at": null
}
```

## 1.3 Common Review Fields

```json
{
  "review_status": "not_requested|awaiting_review|approved|needs_fix|rejected",
  "review_notes": [],
  "review_tags": [],
  "last_review_event_id": null
}
```

## 1.4 Source Reference

```json
{
  "source_type": "recording|transcript|research_evidence|uploaded_file|registry|asset",
  "source_id": "...",
  "start_ms": null,
  "end_ms": null,
  "line_range": null,
  "claim_scope": "supports|contradicts|contextualizes",
  "note": null
}
```

---

# 2. Brand Contracts

## 2.1 BrandWorkspace

```json
{
  "brand_id": "brand_...",
  "organization_id": "org_...",
  "name": "Maison Naturopathie",
  "slug": "maison-naturopathie",
  "status": "genesis|active|paused|archived",
  "primary_language": "fr",
  "supported_languages": ["fr", "en"],
  "industry": "holistic_health",
  "default_time_zone": "Europe/Paris",
  "active_brand_context_version_id": null,
  "publishing_profile_version_id": null,
  "created_at": "...",
  "updated_at": "..."
}
```

## 2.2 BrandGenesisSession

```json
{
  "brand_genesis_session_id": "bgs_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "status": "draft",
  "current_stage": "client_intake",
  "input_source_media_ids": [],
  "consent_record_version_id": null,
  "business_intelligence_version_id": null,
  "tribe_soul_version_id": null,
  "character_lexicon_version_id": null,
  "voice_dna_version_id": null,
  "negative_space_version_id": null,
  "visual_constitution_version_id": null,
  "identity_summary_id": null,
  "identity_pack_version_id": null,
  "acting_library_version_id": null,
  "papercut_rig_version_id": null,
  "prop_library_version_id": null,
  "anchor_library_version_id": null,
  "motion_library_version_id": null,
  "sfx_library_version_id": null,
  "composition_preference_version_id": null,
  "publishing_profile_version_id": null,
  "output_brand_context_version_id": null,
  "genesis_clearance_certificate_id": null,
  "errors": [],
  "created_at": "...",
  "updated_at": "..."
}
```

## 2.3 ConsentRecordVersion

```json
{
  "consent_record_version_id": "crv_...",
  "brand_id": "brand_...",
  "subject_person_id": "person_...",
  "permissions": {
    "store_source_photos": true,
    "store_source_video": true,
    "generate_realistic_derivatives": true,
    "generate_stylized_avatar": true,
    "generate_memes": false,
    "use_motion_transfer": false,
    "publish_socially": true,
    "reuse_future_sessions": true,
    "train_custom_model": false,
    "use_external_image_provider": true
  },
  "allowed_providers": [],
  "prohibited_contexts": [],
  "retention_policy_id": "...",
  "signed_at": "...",
  "revoked_at": null,
  "document_asset_id": "..."
}
```

## 2.4 BrandContextVersion

```json
{
  "brand_context_version_id": "bcv_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "semantic_version": "1.0.0",
  "status": "locked",
  "components": {
    "business_intelligence_version_id": "biv_...",
    "tribe_soul_version_id": "tsv_...",
    "character_lexicon_version_id": "clv_...",
    "voice_dna_version_id": "vdv_...",
    "negative_space_version_id": "nsv_...",
    "visual_constitution_version_id": "vcv_...",
    "identity_pack_version_id": "ipv_...",
    "acting_library_version_id": "alv_...",
    "papercut_rig_version_id": "prv_...",
    "prop_library_version_id": "plv_...",
    "anchor_library_version_id": "msav_...",
    "motion_library_version_id": "mlv_...",
    "sfx_library_version_id": "slv_...",
    "composition_preference_version_id": "cpv_...",
    "publishing_profile_version_id": "ppv_...",
    "registry_bundle_version_id": "rbv_..."
  },
  "content_hash": "sha256:...",
  "locked_at": "...",
  "locked_by": "user_..."
}
```

## 2.5 GenesisClearanceCertificate

```json
{
  "certificate_id": "gcc_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "requirements": {
    "consent_valid": true,
    "identity_summary_approved": true,
    "acting_library_complete": true,
    "papercut_rig_approved": true,
    "negative_space_approved": true,
    "visual_constitution_approved": true,
    "registries_valid": true
  },
  "validation_run_ids": [],
  "issued_at": "...",
  "issued_by": "workflow_..."
}
```

---

# 3. Identity and Creative Library Contracts

## 3.1 ActingReference

```json
{
  "acting_reference_id": "act_...",
  "brand_id": "brand_...",
  "acting_library_version_id": "alv_...",
  "asset_id": "asset_...",
  "emotion_primary": "confident",
  "emotion_secondary": "warm",
  "communicative_intent": "explain_important_idea",
  "gesture_family": "open_hands_explaining",
  "body_language": "upright_open",
  "facial_expression": "confident_half_smile",
  "energy_level": "medium_high",
  "framing": "medium_shot",
  "orientation": "front_3_4_right",
  "layout_bias": "left_subject_text_right",
  "hand_visibility": "both",
  "quality_scores": {
    "likeness": 0.93,
    "emotion": 0.88,
    "gesture": 0.9,
    "hands": 0.86,
    "crop": 0.95
  },
  "review_status": "approved",
  "content_hash": "sha256:..."
}
```

## 3.2 ActingLibraryVersion

```json
{
  "acting_library_version_id": "alv_...",
  "brand_id": "brand_...",
  "matrix_definition": {
    "emotions": [],
    "gesture_families": []
  },
  "cell_reference_ids": {},
  "coverage": {
    "required": 64,
    "approved": 64,
    "missing_cells": []
  },
  "status": "locked",
  "content_hash": "sha256:..."
}
```

## 3.3 RigManifest

```json
{
  "rig_manifest_version_id": "prv_...",
  "brand_id": "brand_...",
  "type": "2d_cutout_rig",
  "coordinate_system": {
    "width": 1080,
    "height": 1920,
    "origin": "top_left"
  },
  "layers": [
    {
      "layer_id": "torso",
      "asset_id": "asset_torso",
      "z_index": 10,
      "anchor": [0.5, 0.15],
      "parent_layer_id": null,
      "motion_affordances": ["translate", "rotate_small", "scale_small"]
    }
  ],
  "bones": [
    {
      "bone_id": "neck",
      "parent_layer_id": "torso",
      "child_layer_id": "head",
      "rotation_min_deg": -8,
      "rotation_max_deg": 8
    }
  ],
  "expression_presets": {},
  "gesture_presets": {},
  "mouth_map": {},
  "preview_validation_run_id": "val_...",
  "status": "locked",
  "content_hash": "sha256:..."
}
```

## 3.4 MicroSemioticAnchor

```json
{
  "micro_semiotic_anchor_id": "msa_...",
  "brand_id": "brand_...",
  "library_version_id": "msav_...",
  "name": "budget supermarket-coded socks",
  "category": "ordinary_life_object",
  "cultural_context": "French fitness audience",
  "audience_segment_ids": [],
  "visual_description": "...",
  "preferred_placements": ["feet"],
  "prominence": "subtle_but_visible",
  "recognition_effects": ["relatability", "humor", "comment_trigger"],
  "risk_scores": {
    "trademark": 0.35,
    "stereotype": 0.1,
    "distraction": 0.12
  },
  "approved_asset_ids": [],
  "review_status": "approved"
}
```

## 3.5 MotionRecipe

```json
{
  "motion_recipe_id": "motion.myth_busted.v1",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "compatible_archetype_ids": ["archetype.myth_debunk.v1"],
  "beats": [
    {
      "beat_id": "hook",
      "relative_duration": 0.12,
      "required_layer_classes": ["headline_strip"],
      "actions": ["headline_strip_slide_in", "background_slow_push"]
    },
    {
      "beat_id": "myth",
      "relative_duration": 0.2,
      "actions": ["note_drop", "underline_draw"]
    },
    {
      "beat_id": "debunk",
      "relative_duration": 0.15,
      "actions": ["stamp_pop", "note_micro_shake", "x_draw"]
    },
    {
      "beat_id": "truth",
      "relative_duration": 0.38,
      "actions": ["line_reveal", "parallax_drift"]
    },
    {
      "beat_id": "cta",
      "relative_duration": 0.15,
      "actions": ["cta_slide_up", "camera_settle"]
    }
  ],
  "constraints": {
    "max_simultaneous_motion": 4,
    "max_bounces_per_10s": 2
  }
}
```

---

# 4. Research and Interview Contracts

## 4.1 ResearchField

```json
{
  "research_field_id": "rf_...",
  "brand_id": "brand_...",
  "objective": "Prepare an interview about identity and belonging.",
  "scope": {
    "guest_id": "guest_...",
    "audience_segment_ids": [],
    "time_horizon": "current_plus_historical"
  },
  "status": "collecting",
  "evidence_ids": [],
  "quality_gate": {},
  "completed_at": null
}
```

## 4.2 ResearchEvidence

```json
{
  "evidence_id": "ev_...",
  "research_field_id": "rf_...",
  "source_type": "official_web",
  "source_locator": "...",
  "title": "...",
  "author": "...",
  "published_at": "...",
  "captured_at": "...",
  "summary": "...",
  "claim": "...",
  "classification": "fact|quote|inference|opinion",
  "confidence": 0.9,
  "temporal_sensitivity": "high",
  "citation_payload": {},
  "content_hash": "sha256:..."
}
```

## 4.3 ContextPremise

```json
{
  "context_premise_id": "cp_...",
  "research_field_id": "rf_...",
  "statement": "...",
  "evidence_ids": [],
  "confidence": 0.78,
  "status": "proposed|approved|rejected|expired",
  "guest_implication": "...",
  "audience_implication": "...",
  "question_implication": "...",
  "risk_if_wrong": "...",
  "expires_at": "...",
  "approved_by": null
}
```

## 4.4 InterviewerResonanceContext

```json
{
  "interviewer_resonance_context_id": "irc_...",
  "interviewer_id": "user_...",
  "guest_id": "guest_...",
  "research_field_id": "rf_...",
  "scenes_that_resonate": [],
  "personal_implication": [],
  "unresolved_curiosities": [],
  "authentic_emotional_bridges": [],
  "questions_that_feel_alive": [],
  "questions_to_avoid": [],
  "self_centering_risks": [],
  "recommended_opening_state": "cinematic",
  "source_thread_id": "thread_..."
}
```

## 4.5 MatrixOfEdgingBrief

```json
{
  "matrix_of_edging_brief_id": "moe_...",
  "research_field_id": "rf_...",
  "broad_primary_signals": [],
  "tension_sites": [
    {
      "boundary": "identity imposed vs identity claimed",
      "magnitude": 0.88,
      "evidence_ids": [],
      "risk": "medium"
    }
  ],
  "candidate_edge_products": [],
  "primitive_candidates": [],
  "safety_constraints": [],
  "status": "approved"
}
```

## 4.6 InterviewAssetContract

Use the full object from the master specification. Required fields:

```text
contract_id
question
target_expression_states
target_archetypes
target_derivatives
edge_product_hypothesis
first_line_anchors
depth_anchor
repair_followups
expected_source_material
clip_start_rule
landing_eval_targets
potential_asset_routes
safety_notes
evidence_ids
```

---

# 5. Expression Contracts

## 5.1 CompleteExpressionSession

Required object fields:

```text
expression_session_id
brand_id
brand_context_version_id
session_context_snapshot_id
guest_id
interviewer_id
session_type
session_goal
recording_configuration
interview_preparation_id
interview_asset_contract_ids
recording_artifact_ids
transcript_revision_id
anchor_hit_ids
expression_moment_ids
asset_package_spec_id
evaluation_receipt_id
status
```

## 5.2 ExpressionMoment

Required fields:

```text
expression_moment_id
expression_session_id
source_artifact_id
transcript_revision_id
start_ms
end_ms
verbatim_text
expression_states
source_contract_id
meaning_summary
edge_product_candidates
route_candidates
sensitivity
allowed_uses
review_status
```

## 5.3 ArchetypeRoute

```json
{
  "archetype_route_id": "route_...",
  "expression_moment_id": "em_...",
  "core_archetype_id": "archetype.conceptual_contrast.v1",
  "asset_derivative_id": "asset_derivative.identity_mirror.v1",
  "meme_mechanism_id": null,
  "reaction_archetype_id": null,
  "cmf_render_mode_id": "cmf.paper_cut_explainer.v1",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "confidence": 0.86,
  "rationale": "...",
  "registry_bundle_version_id": "rbv_...",
  "review_status": "approved"
}
```

## 5.4 AssetPackageSpec

```json
{
  "asset_package_spec_id": "aps_...",
  "expression_session_id": "xes_...",
  "package_type": "guest_asset_pack",
  "target_counts": {
    "short_video": 4,
    "carousel": 2,
    "meme_visual": 2,
    "poll_visual": 2,
    "reaction_seed": 3
  },
  "items": [
    {
      "package_item_id": "...",
      "expression_moment_id": "em_...",
      "archetype_route_id": "route_...",
      "asset_type": "short_video",
      "priority": "required",
      "status": "planned"
    }
  ],
  "diversity_constraints": {
    "minimum_expression_states": 3,
    "minimum_archetypes": 3,
    "minimum_render_modes": 2
  },
  "review_status": "approved"
}
```

---

# 6. Production Contracts

## 6.1 CompleteEditingSession

Required fields:

```text
complete_editing_session_id
brand_id
brand_context_version_id
registry_bundle_version_id
source_expression_session_id
source_expression_moment_id
asset_package_spec_id
asset_type
core_archetype_id
asset_derivative_id
cmf_render_mode_id
visual_style_id
platform_targets
status
```

## 6.2 SceneSpec

```json
{
  "scene_spec_id": "scene_...",
  "complete_editing_session_id": "ces_...",
  "format": "vertical_video",
  "aspect_ratio": "9:16",
  "duration_seconds": 30,
  "platform_targets": ["instagram_reels"],
  "source_message": {
    "verbatim_or_approved_copy": "...",
    "source_references": []
  },
  "text_hierarchy": {
    "headline": "MYTHS BUSTED",
    "subtitle": "Holistic health edition",
    "body_points": []
  },
  "emotional_intent": "compassionate_authority",
  "subject": {
    "identity_pack_version_id": "ipv_...",
    "acting_intent": "serious_open_explain",
    "position": "lower_right",
    "scale": "medium"
  },
  "composition": {
    "layout_family": "headline_top_notes_left_avatar_lower_right",
    "main_metaphor": "...",
    "visual_flow": "top_to_left_to_avatar",
    "density": "medium",
    "text_safe_area": "left_middle"
  },
  "objects": [],
  "micro_semiotic_anchor_ids": [],
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "motion_intent": {
    "recipe_id": "motion.myth_busted.v1",
    "intensity": "restrained"
  }
}
```

## 6.3 AssetSelection

```json
{
  "asset_selection_id": "sel_...",
  "complete_editing_session_id": "ces_...",
  "selected": [
    {
      "role": "primary_acting_reference",
      "asset_id": "act_...",
      "score": 0.91,
      "reason": "best communicative intent and gesture match"
    },
    {
      "role": "secondary_face_anchor",
      "asset_id": "act_...",
      "score": 0.88,
      "reason": "best identity clarity"
    }
  ],
  "low_confidence": false
}
```

## 6.4 ProviderJob

```json
{
  "provider_job_id": "pj_...",
  "complete_editing_session_id": "ces_...",
  "capability": "image_edit",
  "provider_capability_id": "pc_...",
  "workflow_template_id": "wf_...",
  "input_asset_hashes": [],
  "parameters": {},
  "idempotency_key": "...",
  "status": "queued",
  "cost_budget": {},
  "external_job_id": null,
  "receipt_id": null
}
```

## 6.5 LayerManifest

```json
{
  "layer_manifest_id": "lm_...",
  "source_asset_id": "asset_...",
  "layers": [
    {
      "layer_id": "layer_avatar",
      "semantic_type": "portrait_cutout",
      "asset_id": "asset_...",
      "mask_asset_id": "mask_...",
      "z_index": 30,
      "bbox": [620, 780, 380, 1020],
      "anchor": [0.5, 0.9],
      "parent_layer_id": null,
      "alpha_quality": 0.92,
      "edge_quality": 0.89,
      "semantic_confidence": 0.95,
      "motion_affordances": ["drift", "scale_small", "expression_swap"],
      "review_status": "approved"
    }
  ],
  "required_layers_present": true,
  "text_baked": false,
  "review_status": "approved"
}
```

## 6.6 AnimationPlan

```json
{
  "animation_plan_id": "anim_...",
  "complete_editing_session_id": "ces_...",
  "fps": 30,
  "duration_frames": 900,
  "motion_recipe_id": "motion.myth_busted.v1",
  "events": [
    {
      "event_id": "aev_1",
      "start_frame": 0,
      "duration_frames": 20,
      "target_layer_id": "headline",
      "primitive_id": "paper_slide_in",
      "parameters": {},
      "sync_reference": "audio_phrase_1",
      "sfx_asset_id": "sfx_paper_slide"
    }
  ],
  "global": {
    "camera_motion": "slow_push_in",
    "jitter_px": 0.7,
    "rotation_jitter_deg": 0.3
  }
}
```

## 6.7 EvaluationReceipt

```json
{
  "evaluation_receipt_id": "eval_...",
  "object_type": "render_output",
  "object_id": "render_...",
  "rubric_version_ids": [],
  "scores": {
    "source_truth": 0.98,
    "identity": 0.92,
    "emotion": 0.87,
    "composition": 0.9,
    "style": 0.94,
    "motion_restraint": 0.89,
    "micro_semiotic_anchor": 0.84,
    "negative_space": 0.97,
    "platform_fit": 0.91
  },
  "hard_failures": [],
  "warnings": [],
  "evidence": [],
  "decision": "needs_human_review",
  "evaluator_versions": [],
  "created_at": "..."
}
```

---

# 7. Agent Runtime and Command Contracts

## 7.1 AgentExecutionContext

The Agent Gateway builds this immutable, request-scoped object before Pi or a specialist agent may act.

```json
{
  "execution_context_id": "actx_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "registry_bundle_version_id": "rbv_...",
  "user": {
    "user_id": "user_...",
    "roles": ["owner"],
    "permissions": ["render.review", "publishing.schedule"]
  },
  "surface": "pwa|telegram_bot|telegram_mini_app|system",
  "mode": "brand_genesis|research|interview_preparation|live_interview|post_session_extraction|production_planning|render_review|publishing|system_administration",
  "thread_id": "thread_...",
  "active_object": {
    "type": "render_output",
    "id": "render_...",
    "version": 3
  },
  "retrieved_context_refs": [],
  "available_tool_ids": [],
  "available_dspy_program_ids": [],
  "provider_policy_id": "pp_...",
  "cost_policy_id": "cp_...",
  "consent_policy_id": "consent_policy_...",
  "confirmation_policy_id": "confirm_...",
  "expires_at": "...",
  "context_hash": "sha256:..."
}
```

The context may contain references to sensitive objects, but tools must retrieve the minimum required data at execution time. It is not a dump of the entire brand corpus.

## 7.2 DSPyProgramSpec

```json
{
  "program_id": "dspy.interview_asset_contract_compiler",
  "program_version": "1.2.0",
  "status": "approved",
  "input_model": "InterviewContractCompilerInput@1.0.0",
  "output_model": "InterviewAssetContract@2.0.0",
  "signature_id": "sig_...",
  "module_class": "InterviewAssetContractCompiler",
  "optimizer": {
    "type": "approved_optimizer_or_none",
    "artifact_id": "opt_..."
  },
  "model_policy_id": "model_policy_interview_high_quality",
  "evaluation_dataset_version_id": "evalset_...",
  "minimum_scores": {
    "grounding": 0.95,
    "contract_validity": 1.0,
    "human_acceptance": 0.85
  },
  "fallback_program_id": "dspy.interview_asset_contract_compiler_safe",
  "artifact_hash": "sha256:..."
}
```

Production DSPy programs are versioned assets. Changing a signature, optimizer artifact, demonstration set, evaluation threshold, or output model requires a new program version.

## 7.3 AgentCommand

```json
{
  "command_id": "cmd_...",
  "command_type": "APPROVE_RENDER",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "actor_user_id": "user_...",
  "thread_id": "thread_...",
  "target_type": "render_output",
  "target_id": "render_...",
  "payload": {},
  "confirmation_level": "human_confirm",
  "idempotency_key": "...",
  "status": "proposed",
  "created_at": "..."
}
```

## 7.4 Command Status

```text
proposed
→ awaiting_confirmation
→ confirmed
→ executing
→ succeeded | failed | cancelled | rejected
```

## 7.5 Command Result

```json
{
  "command_result_id": "...",
  "command_id": "cmd_...",
  "status": "succeeded",
  "created_object_ids": [],
  "domain_event_ids": [],
  "message": "Render approved.",
  "error": null
}
```

---

# 8. State Machines

## 8.1 Brand Genesis

```text
draft
→ intake_in_progress
→ consent_pending
→ source_qc
→ intelligence_compilation
→ identity_summary_review
→ acting_library_generation
→ acting_library_review
→ avatar_generation
→ layer_and_rig_build
→ rig_review
→ library_generation
→ final_validation
→ context_lock_pending
→ completed

Failure/alternate:
any_state → blocked
any_review → needs_fix
blocked → resumed | cancelled
```

Lock is impossible unless required components are approved.

## 8.2 Acting Reference

```text
draft
→ generation_requested
→ generated
→ auto_qc_passed | auto_qc_failed
→ awaiting_human_review
→ approved | needs_fix | rejected
needs_fix → generation_requested
approved → locked
locked → deprecated
```

## 8.3 Interview Preparation

```text
draft
→ research_collecting
→ evidence_review
→ premises_proposed
→ interviewer_preinduction
→ edging_compiled
→ state_map_compiled
→ contracts_compiled
→ deck_review
→ approved
→ frozen
```

## 8.4 Complete Expression Session

```text
draft
→ scheduled
→ calibration_pending
→ ready
→ live
→ capture_complete
→ uploading
→ transcribing
→ extracting
→ moment_review
→ package_compilation
→ evaluating
→ completed
```

Alternate:

```text
live → interrupted
uploading → missing_artifact
transcribing → failed
any → cancelled
```

## 8.5 Expression Moment

```text
candidate
→ awaiting_review
→ approved | rejected | needs_boundary_fix | sensitive_hold
needs_boundary_fix → candidate
approved → routed
routed → production_allowed
```

## 8.6 Complete Editing Session

```text
planned
→ ready
→ compiling
→ assets_selected
→ provider_jobs_running
→ layer_preparation
→ animation_planning
→ render_queued
→ rendering
→ rendered
→ auto_evaluating
→ needs_review
→ approved | revision_requested | rejected
revision_requested → compiling
approved → publishing_ready
```

## 8.7 Provider Job

```text
created
→ queued
→ dispatched
→ running
→ succeeded | retryable_failed | terminal_failed | cancelled
retryable_failed → queued
```

## 8.8 Publishing Intent

```text
draft
→ ready_for_review
→ approved
→ confirmation_pending
→ confirmed
→ uploading_media
→ scheduling
→ scheduled
→ published
```

Alternate:

```text
scheduling → failed
scheduled → cancelled
published → metrics_syncing
```

---

# 9. Domain Events and Projection Rules

Each successful command emits domain events.

Events are immutable and processed through the outbox.

Example:

```json
{
  "event_id": "evt_...",
  "event_type": "RenderApproved",
  "aggregate_type": "render_output",
  "aggregate_id": "render_...",
  "aggregate_version": 4,
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "payload": {
    "approval_event_id": "ae_..."
  },
  "occurred_at": "..."
}
```

Projection consumers:

- read models;
- Neo4j;
- search/vector index;
- operator notifications;
- analytics;
- workflow signals;
- audit enrichment.

A projection failure never rewrites or loses the source event.

---

# 10. Idempotency and Concurrency

## 10.1 Idempotency

Required for:

- agent commands;
- provider jobs;
- uploads;
- webhooks;
- render starts;
- publish/schedule;
- workflow signals.

## 10.2 Optimistic Concurrency

Mutable aggregates carry a version.

A command must state expected version or be conflict-safe.

Examples:

- two reviewers approving the same asset;
- Telegram and PWA revision at the same time;
- brand context fork while a session is starting.

## 10.3 Context Freeze

When an interview starts or editing job becomes `ready`, store the exact context IDs/hashes.

Later changes do not leak into the active job.

---

# 11. Receipt Chain

The receipt chain links:

```text
Research Evidence Receipt
→ Interview Preparation Receipt
→ Expression Session Receipt
→ Expression Moment Approval
→ Asset Route Receipt
→ Provider Receipts
→ Render Receipt
→ Evaluation Receipt
→ Approval Event
→ Publishing Receipt
```

A public asset must be traceable through the full chain.

---

# 12. Minimum Schema/Test Deliverables

The coding agent must create:

```text
python/ccp_studio/contracts/**/*.py
generated/json-schema/*.json
generated/openapi/openapi.json
generated/typescript/**/*.ts
generated/zod/**/*.ts                 # optional generated validators
docs/contracts/*.md
tests/contracts/test_*.py
fixtures/contracts/*.json
```

Every contract requires:

- valid fixture;
- invalid fixtures;
- backward-compatibility test;
- migration test where versioned;
- human-readable documentation.

No API, workflow, database mapping, DSPy module, frontend, or renderer may define a conflicting shadow type. Contract generation must be reproducible in CI, and generated TypeScript artifacts must be checked for drift.

---

# CCP Studio V2 — Python-First Implementation Sequence, Migration Plan, and Production Release Gates

**Companion to:** Master Specification and Domain Contracts  
**Operating rule:** build internally in coherent waves, but do not publicly release an incomplete chain.

---

# 1. Delivery Philosophy

“No MVP” does not mean “write the whole codebase in one pass.”

It means:

- do not ship a misleading partial product;
- do not let temporary architecture become permanent;
- implement foundations in dependency order;
- keep every internal increment executable and testable;
- release only when the complete brand-to-publication journey works.

The development unit is an **internally complete vertical slice**. The release unit is the **whole production loop**.

---

# 2. Wave 0 — Repository Archaeology and Decision Freeze

## Objective

Understand existing value before implementing the greenfield runtime.

## Tasks

1. Freeze the legacy repository.
2. Record current branches, deployments, databases, provider integrations, and secrets.
3. Inventory:
   - registry files;
   - prompt families;
   - primitive taxonomies;
   - schemas;
   - evaluation rubrics;
   - render templates;
   - provider code;
   - test fixtures;
   - dead/duplicated code.
4. Create the migration ledger.
5. Identify canonical registry sources when duplicates exist.
6. Hash source artifacts.
7. Approve the Python / Pydantic / DSPy / Pi runtime ADR before any framework scaffolding.
8. Define data-classification and consent requirements.

## Required Outputs

```text
docs/migration/legacy-inventory.md
docs/migration/registry-source-map.md
docs/migration/migration-ledger.csv
docs/migration/dependency-risk-map.md
docs/adr/ADR-001-python-pydantic-dspy-pi-runtime.md
docs/adr/ADR-002-greenfield-runtime.md
docs/adr/ADR-003-registry-kernel.md
docs/adr/ADR-004-brand-context-versioning.md
docs/adr/ADR-005-agent-command-bus.md
docs/adr/ADR-006-durable-workflows.md
docs/adr/ADR-007-provider-adapters.md
docs/adr/ADR-008-tenant-isolation.md
docs/adr/ADR-009-publishing-safety.md
```

## Exit Gate

- every high-value legacy registry has an owner and migration status;
- no unknown production dependency remains;
- greenfield stack ADRs are approved;
- legacy runtime is read-only.

---

# 3. Wave 1 — Contract and Registry Kernel

## Objective

Create the language the entire application will speak.

## Tasks

1. Scaffold monorepo.
2. Implement common IDs, envelopes, versioning, review fields, and source references.
3. Implement canonical Pydantic v2 contracts and JSON Schema/OpenAPI generation.
4. Generate TypeScript interfaces and optional Zod validators from Pydantic.
5. Establish contract-drift checks in CI.
6. Implement registry entry schemas as Pydantic models.
7. Migrate the five core registries.
8. Migrate supporting registries.
9. Build Registry Bundle validation.
10. Add legacy golden fixtures.
11. Add registry admin inspection UI only after the kernel works.
12. Create compatibility and cross-reference tests.
13. Create the DSPy program registry contract and representative typed signatures.

## Exit Gate

- active registry bundle validates at boot;
- no missing cross-reference;
- no active schema lacks an evaluation rubric;
- old prompt examples are represented as fixtures;
- a compiler can retrieve and combine registry contracts without using a monolithic prompt.

---

# 4. Wave 2 — Control Plane and Data Spine

## Objective

Build the durable, secure stateful application core.

## Tasks

1. Authentication and organizations.
2. Brand workspaces and roles.
3. PostgreSQL schema and RLS.
4. Object storage abstraction.
5. Audit log.
6. Domain event and outbox.
7. Temporal cluster/namespace and Python workflow-worker skeleton.
8. Python Command Bus with Pydantic command validation.
9. Agent threads and messages.
10. OpenTelemetry.
11. secret management.
12. backup/restore rehearsal.

## Exit Gate

- cross-brand RLS tests pass;
- commands are idempotent;
- events publish through outbox;
- workflows survive process restart;
- assets upload with correct brand scope and signed access;
- audit records cover all mutations;
- backup restoration succeeds in staging.

---

# 5. Wave 3 — Agent Gateway and Shared Surfaces Foundation

## Objective

Create one intelligent operator across PWA and Telegram.

## Tasks

1. Python Agent Gateway context assembly.
2. Pi Coding Agent orchestration boundary.
3. DSPy program registry and typed signature execution.
4. mode-specific tool registry.
5. model/provider routing.
6. Pydantic command proposals.
7. permission and confirmation policies.
8. PWA chat shell consuming generated TypeScript contracts.
9. Python Telegram bot webhook.
10. Telegram Mini App authentication and shell.
11. cross-surface thread continuity.
12. prompt-injection and untrusted-content guards.
13. tests proving Pi/DSPy cannot bypass the Command Bus or durable workflows.

## Exit Gate

- the same thread works in PWA and Telegram;
- the agent never crosses brands;
- expensive/public commands require confirmation;
- the agent cannot directly write production tables;
- all tool activity is audited;
- Telegram tampering tests pass.

---

# 6. Wave 4 — Full Brand Genesis

## Objective

Onboard a brand into a locked creative universe.

## Tasks

### Intake and Consent

- client and business intake;
- likeness/voice/derivative consent;
- source photo/video upload;
- source QC.

### Strategic Identity

- Business Intelligence;
- Tribe Soul;
- Character Lexicon;
- initial Voice DNA;
- linguistic Negative Space;
- visual constitution and visual Negative Space;
- identity summary approval.

### Acting Library

- provider adapter for GPT Image 2/current approved asset provider;
- batch generation of 64 cells;
- auto-QC;
- approval/fix/reject grid;
- immutable library lock.

### Paper-Cut Actor

- avatar asset generation;
- Qwen-Image-Layered adapter;
- SAM3 adapter;
- See-Through adapter/fallback;
- edit/repair provider;
- canonical Rig Manifest;
- preview tests;
- approval.

### Creative Libraries

- props;
- Micro-Semiotic Anchors;
- motions;
- SFX;
- composition preferences;
- publishing profile.

### Lock

- adversarial validation;
- Genesis Clearance Certificate;
- Brand Context Version lock.

## Exit Gate

A real brand can:

1. upload source media;
2. approve identity;
3. approve all 64 acting cells;
4. approve a functioning paper-cut rig;
5. approve props/anchors/motion/SFX;
6. lock Brand Context v1;
7. reproduce the exact locked context from hashes.

No production session may begin without this gate unless explicitly using a legacy/manual context with a waiver.

---

# 7. Wave 5 — Research and Interview Intelligence

## Objective

Make the application improve interviewing before any editing begins.

## Tasks

1. Research Field and Evidence objects.
2. source provenance and citation support.
3. Guest Dossier compiler.
4. Audience Reality Brief compiler.
5. Context Premise workflow.
6. Evidence Critic/adversarial review.
7. Interviewer Pre-Induction chat.
8. Interviewer Resonance Context.
9. Matrix of Edging.
10. Narrative State Map.
11. Interview Asset Contracts.
12. Deck compiler and review.
13. Live Interview mode UI and cue contract.
14. Interviewer Profile and learning events.

## Exit Gate

For a real guest/topic, the system can:

- show the evidence behind its assumptions;
- distinguish facts and inferences;
- interview the operator;
- create approved Context Premises;
- generate a stateful interview deck;
- produce repair follow-ups;
- explain why every question exists;
- preserve human freedom to deviate.

A human reviewer must judge the final deck as meaningfully better than a generic researched interview.

---

# 8. Wave 6 — Complete Expression Sessions

## Objective

Capture, synchronize, extract, and evaluate authentic expression.

## Tasks

1. recording configuration;
2. calibration/quality gate;
3. session start/stop and markers;
4. recording upload;
5. transcript provider and revisions;
6. timestamp alignment;
7. anchor hit detection;
8. expression moment extraction;
9. source playback review;
10. sensitivity and allowed-use controls;
11. archetype routes;
12. Asset Package Spec;
13. session and interviewer evaluation.

## Exit Gate

One real interview produces:

- immutable source artifacts;
- synchronized transcript;
- approved moments with source timestamps;
- approved routes;
- an Asset Package Spec;
- post-session learning;
- no fabricated or ungrounded output.

---

# 9. Wave 7 — Complete CMF Production

## Objective

Compile approved expression into every required production route.

## Tasks

### Common

- Complete Editing Session;
- Creative State;
- SceneSpec;
- asset retrieval;
- provider receipts;
- Evaluation Receipts;
- revision branches.

### Composition and Image

- Ideogram 4 Composition Provider;
- GPT Image asset/edit provider;
- Flux 2 Klein 9b edit provider;
- approved workflow templates;
- reference selection.

### Layering and Rig

- Qwen-Image-Layered semantic decomposition;
- SAM3 precision masks/tracking;
- See-Through character route;
- repair/edit route;
- layer QC;
- Rig Provider.

### Deterministic Render Routes

- Personal-Brand Commentary;
- Paper-Cut Explainer;
- Animated Avatar Explainer;
- Carousel Static/Motion;
- Quiz/Ranking;
- Data Story;
- Living/Conscious Reactions.

### Generative/Special Routes

- SCAIL-2 motion transfer;
- cinematic video generation;
- HyperFrames route;
- final Remotion packaging.

### Sound

- authentic primary audio;
- subtitle sync;
- motion/SFX plan;
- sound doctrine.

## Exit Gate

Golden test outputs pass for:

1. real-footage commentary;
2. paper-cut explainer;
3. animated avatar;
4. carousel;
5. meme and poll;
6. data story/bar-chart race;
7. quiz/ranking;
8. SCAIL motion-transfer sample;
9. cinematic sample.

Each has full receipts and can be revised without losing lineage.

---

# 10. Wave 8 — Review, Telegram Cockpit, and Publishing

## Objective

Operate the whole system from the PWA and on the move.

## Tasks

1. portfolio and brand dashboards;
2. production board;
3. render comparison;
4. Telegram notifications;
5. Mini App preview/chat;
6. revision commands;
7. approval events;
8. Publishing Intent;
9. platform variants;
10. Publer media upload;
11. draft/schedule/publish adapter;
12. status synchronization;
13. performance ingestion.

## Exit Gate

- a render notification arrives in Telegram;
- the operator previews it in the Mini App;
- chat has the correct brand/object context;
- a revision command branches correctly;
- approval is reflected in PWA;
- publishing requires explicit confirmation;
- Publer status is reconciled;
- duplicate scheduling is prevented.

---

# 11. Wave 9 — Memory, Hardening, and Operational Readiness

## Objective

Make the system safe and sustainable.

## Tasks

1. Brand Memory admissions.
2. Interviewer Memory.
3. Neo4j projection.
4. performance correlations.
5. provider cost/performance reporting.
6. runbooks.
7. penetration/security test.
8. restore drills.
9. provider outage/fallback tests.
10. load and batch tests.
11. user acceptance.
12. documentation completion.
13. release candidate freeze.

## Exit Gate

- memory is evidence-based and reversible;
- Neo4j can rebuild from events;
- system recovers from provider outage;
- backups restore;
- spend alerts work;
- no P0/P1 security defects;
- operator can complete the full workflow without developer intervention.

---

# 12. Production Release Gate

Public launch is prohibited until all conditions pass.

## 12.1 Functional Gate

- Brand Genesis complete;
- Interview Intelligence complete;
- Complete Expression Session complete;
- full CMF routes complete;
- PWA complete;
- Telegram Bot/Mini App complete;
- Publer flow complete;
- memory update complete.

## 12.2 Data Gate

- 100% brand scoping;
- locked context versioning;
- receipt chain;
- audit trail;
- export/delete flow;
- consent enforcement.

## 12.3 Reliability Gate

- workflow resume;
- idempotency;
- provider retry/fallback;
- batch checkpoint;
- backup/restore;
- queue monitoring.

## 12.4 Quality Gate

- approved golden tests;
- calibrated evaluations;
- identity and source-truth hard failures at zero in release set;
- motion/style review;
- interviewer plan judged high quality.

## 12.5 Security Gate

- RLS test;
- Telegram auth test;
- provider token protection;
- prompt-injection test;
- file-upload security;
- least privilege;
- no public asset exposure.

## 12.6 Operational Gate

- runbooks;
- cost dashboards;
- alerting;
- support/admin tools;
- incident ownership;
- provider terms/data-policy review.

## 12.7 Human Acceptance Gate

The operator must complete at least one real brand cycle:

```text
onboarding
→ interview preparation
→ interview
→ asset package
→ render
→ revision
→ approval
→ publishing
→ memory update
```

without direct database edits or ad hoc developer scripts.

---

# 13. Initial Backlog for the Coding Agent

The first approved implementation backlog is:

1. create the Python-first hybrid monorepo;
2. write and approve runtime, greenfield, registry, workflow, and security ADRs;
3. build the legacy inventory script;
4. build the migration-ledger format;
5. implement common Pydantic contracts;
6. implement JSON Schema and OpenAPI generation;
7. generate TypeScript interfaces and optional Zod validators;
8. establish CI drift checks for generated contracts;
9. implement registry Pydantic schemas;
10. migrate one archetype of each registry type;
11. implement registry validation and bundle signing/hash rules;
12. implement the DSPy Program Registry and representative signatures;
13. implement organization/brand persistence mappings;
14. implement RLS;
15. implement audit log;
16. implement domain event/outbox;
17. implement Temporal Python bootstrap;
18. implement the Python command bus;
19. implement the Python Agent Gateway skeleton;
20. implement Pi orchestration context and approved tool boundaries;
21. implement PWA/Telegram shared thread identity;
22. implement Brand Genesis workflow skeleton;
23. implement source media upload/QC;
24. implement consent enforcement;
25. implement identity summary review;
26. implement 64-cell library schema and review grid;
27. implement provider capability registry;
28. implement image asset provider contract;
29. implement paper-cut rig contracts;
30. implement Brand Context lock;
31. implement research evidence and Context Premises;
32. implement interviewer pre-induction;
33. implement DSPy Interview Asset Contract compiler;
34. implement Complete Expression Session;
35. implement Complete Editing Session;
36. implement render/provider adapters;
37. implement evaluation and approval;
38. implement Publer adapter;
39. implement complete release gates.

The agent should submit architecture, migrations, and tests in small reviewed pull requests while preserving the final no-half-release doctrine.

---

# 14. Pull Request Definition of Done

Every PR must include:

- linked requirement/ADR;
- domain impact;
- Pydantic schemas, generated projections, and affected types;
- tests;
- migration if needed;
- observability;
- security/brand-scope review;
- documentation;
- rollback note.

A PR fails review if it:

- introduces an untyped payload or a hand-authored shadow contract;
- calls a provider from domain code;
- hides state in Pi/DSPy/chat context;
- lacks idempotency for side effects;
- lacks brand scoping;
- bypasses approval;
- imports legacy runtime code;
- creates a duplicate registry truth.

---

# 15. Agent Reporting Cadence

At the end of each internal wave, report:

```text
Completed
Evidence/tests
Architectural deviations
Unresolved risks
Cost impact
Security impact
Migration status
Next-wave prerequisites
```

Do not report “done” based on file count. Report against exit gates.

---

# 16. Final Execution Directive

Build the system in dependency order, with production-quality boundaries from the first commit.

The greenfield codebase should be smaller and more legible than the legacy system even though the product is broader, because intelligence lives in registries, contracts, workflows, and reusable provider capabilities rather than duplicated prompt logic.

The final product must make the operator:

- more informed before the interview;
- more present during the interview;
- more perceptive after the interview;
- faster and more coherent in production;
- safer in approval and publishing;
- smarter with every completed session.

That is the release.

---

# Legacy Migration and Repository Directive

**Purpose:** prevent the previous TypeScript-first assumption from propagating into migration work or implementation plans.

---

## 1. Greenfield Rule

The new application is greenfield, but the old repository remains a high-value reference source.

```text
Old repository
= read-only registry, doctrine, fixture, example, and provider-code source

New repository
= production runtime
```

No legacy module may become a production dependency without a reviewed exception ADR.

---

## 2. What Must Be Recovered

Inventory and migrate:

- core content archetypes;
- asset derivatives;
- meme mechanisms;
- reaction archetypes;
- CMF render modes;
- primitive families;
- Voice DNA and Negative Space schemas;
- Context Premise logic;
- Interview Asset Contract patterns;
- evaluation rubrics;
- provider adapters with reusable mechanics;
- golden examples and failure fixtures;
- Remotion compositions worth preserving;
- Python agents and DSPy modules worth extracting.

Do not migrate dead orchestration merely because it exists.

---

## 3. Correct Migration Target

Legacy semantic content must target:

```text
Pydantic registry entries
Pydantic domain contracts
DSPy signatures/modules
Python tools and policies
golden JSON fixtures
evaluation datasets
```

It must not target hand-authored TypeScript/Zod domain models.

Existing Remotion code may be preserved or rewritten inside the TypeScript renderer boundary, but it must consume render contracts generated by the Python CMF engine.

---

## 4. Required Legacy Inventory Language

Any repository inventory must describe the target architecture as:

> Python-first Harness using Pydantic, DSPy, and Pi Coding Agent orchestration, with TypeScript restricted to the PWA, Telegram Mini App, Remotion/Motion Canvas, and generated contract consumers.

Remove or correct claims such as:

- “rewrite the platform as a Next.js/TypeScript monorepo”;
- “Zod is the canonical schema source”;
- “all agents become TypeScript services”;
- “Remotion types define media contracts.”

Acceptable language:

- “hybrid monorepo with Python nucleus and TypeScript leaf apps”;
- “Pydantic-to-TypeScript generated contracts”;
- “Remotion migration behind a Python-issued RenderContract”;
- “legacy Python/DSPy logic evaluated for extraction into the new Harness.”

---

## 5. Migration Ledger Fields

Each legacy item must record:

```text
legacy_path
legacy_type
registry_family_or_domain
canonicality_confidence
source_owner
runtime_language
valuable_mechanics
known_defects
migration_target_python_package
pydantic_contract_target
dspy_program_target
typescript_leaf_target_if_any
fixture_target
evaluation_target
status
reviewer
content_hash
```

---

## 6. Rewrite Rule for legacy-inventory.md

The repository’s `docs/migration/legacy-inventory.md` must be regenerated or patched so that:

1. Python is the primary runtime.
2. Pydantic is the contract authority.
3. DSPy and Pi are first-class Harness components.
4. TypeScript is restricted to UI/rendering.
5. Existing Python agents are assessed for extraction, not automatic deletion or rewrite.
6. Existing registries migrate to Pydantic/data packages.
7. Existing Remotion templates migrate behind renderer contracts.
8. No legacy code is imported into production merely to accelerate delivery.

---

## 7. Acceptance Gate

Migration planning is not approved until searches for the following stale assumptions return no authoritative occurrences:

```text
Language: TypeScript
Zod at all boundaries
Zod as canonical contracts
NestJS as core agent runtime
Drizzle as domain model
rewrite all agents in TypeScript
```

References describing the allowed TypeScript surfaces are valid.
