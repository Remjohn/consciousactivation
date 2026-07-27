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
