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
