---
title: F07 — Capability Ownership, Modules, Phases, Contexts, and Contracts
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F07
governing_decisions:
- D012
- D013
- D014
- D015
- D019
- D026
- D033
user_journeys:
- UJ-05
- UJ-06
- UJ-07
- UJ-10
- UJ-11
functional_requirement_count: 12
---

# F07 — Capability Ownership, Modules, Phases, Contexts, and Contracts

**User outcome:** An implementation team receives a coherent architecture in which every capability, phase, module, contract, context, and failure has an explicit owner and test seam.

## Description

This feature compiles the execution architecture from the Harness IR. It prevents one giant prompt, a universal creative state machine, technology-layer fragmentation, and hidden semantic authority.

## Brownfield baseline

V2.1 produces substantial architecture and workcell specifications, but capability ownership, phase context, module seams, sparse handoffs, and invalidation are not yet one executable graph system.

## Required product delta

Add typed capability classification, responsibility-centered modules, harness-specific phase and context graphs, versioned contracts, and dependency-aware ownership validation.

## Traceability

- **Decisions:** D012, D013, D014, D015, D019, D026, D033
- **User journeys:** UJ-05, UJ-06, UJ-07, UJ-10, UJ-11
- **Cross-cutting NFRs:** NFR-ARCH-001, NFR-ARCH-002, NFR-REL-004, NFR-TEST-001, NFR-PORT-002

## Functional Requirements

### FR-060 — Inventory every required capability

**Requirement:** The Builder must derive a complete capability inventory from the production promise, category and format profiles, visual and sequence grammar, contracts, evaluations, repairs, and target profile.

**Consequences (testable):**

- Every required transformation or judgment maps to a capability record.
- Capabilities omitted from architecture but required by acceptance criteria fail coverage validation.

**Traceability:** Decisions D012; journeys UJ-05.

### FR-061 — Assign an explicit capability ownership type

**Requirement:** Each capability must be assigned to deterministic_module, typed_model_program, jit_skill, external_reference, human_decision, independent_evaluator, tool_or_provider_adapter, or hybrid_pipeline.

**Consequences (testable):**

- The ownership assignment includes rationale and forbidden ownership forms.
- A capability cannot remain implicitly owned by a general agent.

**Traceability:** Decisions D012; journeys UJ-05.

### FR-062 — Use reliability and cost criteria for ownership

**Requirement:** Ownership decisions must consider mechanical determinism, semantic judgment, reuse, authority, evaluation independence, provider dependence, testability, latency, cost, and the cheapest reliable execution form.

**Consequences (testable):**

- Deterministic math and schema validation are not delegated to language-model reasoning.
- High-stakes judgment is not assigned solely on lowest token price.

**Traceability:** Decisions D003, D012; journeys UJ-05.

### FR-063 — Represent hybrid capability pipelines

**Requirement:** Capabilities requiring multiple execution forms must declare ordered components, contracts, authority boundaries, and failure ownership rather than being forced into one owner type.

**Consequences (testable):**

- Visual Syntactic Parsing can combine deterministic preprocessing, multimodal inference, JIT guidance, validation, evaluation, and human review.
- Each hybrid stage remains independently testable and observable.

**Traceability:** Decisions D007, D012; journeys UJ-02, UJ-05.

### FR-064 — Compile responsibility-centered modules

**Requirement:** The Builder must group capabilities into modules with one cohesive responsibility, small public interfaces, owned contracts and invariants, explicit exclusions, dependencies, failure modes, and a reason for the boundary.

**Consequences (testable):**

- A module can be understood and tested through its interface without reading its internals.
- Creative policy remains atomic unless reuse is proven.

**Traceability:** Decisions D015, D033; journeys UJ-05, UJ-11.

### FR-065 — Declare test seams for every module

**Requirement:** Each module must declare its public test seams, expected fixtures, contract tests, failure injections, and observable outputs.

**Consequences (testable):**

- Implementation stories can reference stable seams instead of internal methods.
- A module without a meaningful public seam is flagged for boundary review.

**Traceability:** Decisions D015; journeys UJ-11.

### FR-066 — Compile a harness-specific Phase Graph

**Requirement:** The Builder must derive phases, dependencies, executors, parallelism, inputs, outputs, completion criteria, failure owners, and invalidation edges appropriate to the atomic harness.

**Consequences (testable):**

- Different harnesses may have different phase graphs while sharing control-plane protocols.
- A phase cannot run before all required predecessor contracts have valid authority.

**Traceability:** Decisions D013; journeys UJ-05, UJ-06.

### FR-067 — Represent sequential and parallel phase dependencies

**Requirement:** The Phase Graph must distinguish strict sequence, parallel-safe work, joins, retries, human gates, and terminal states.

**Consequences (testable):**

- Parallel phases cannot mutate shared authoritative state without a declared merge protocol.
- Join phases block until every required input contract is valid.

**Traceability:** Decisions D013, D025; journeys UJ-05.

### FR-068 — Compile a phase-specific Context Graph

**Requirement:** For every phase, the Builder must define included evidence, decisions, contracts, skills, references, exclusions, conditional loads, unload behavior, and downstream exposure policy.

**Consequences (testable):**

- Future-phase instructions are excluded when they would cause premature completion.
- Downstream phases receive structured outputs rather than inherited prompt history by default.

**Traceability:** Decisions D013, D020; journeys UJ-07.

### FR-069 — Use versioned typed phase handoff contracts

**Requirement:** Every authoritative phase output must use a versioned contract that declares producer, consumers, required and optional fields, provenance, authority, validation, compatibility, mutability, and invalidation behavior.

**Consequences (testable):**

- A consumer rejects incompatible or insufficient-authority contracts.
- Human-readable reports remain views, not the authoritative handoff.

**Traceability:** Decisions D014; journeys UJ-05, UJ-07.

### FR-070 — Prohibit silent downstream rewriting

**Requirement:** A downstream phase may accept, challenge, request repair, or derive from an upstream contract but may not silently modify it.

**Consequences (testable):**

- Challenges create typed events and route to the responsible owner.
- Derived contracts preserve their source contract references.

**Traceability:** Decisions D014, D026; journeys UJ-10.

### FR-071 — Validate ownership and dependency impact

**Requirement:** The Builder must detect orphan capabilities, multiple conflicting primary owners, circular phase dependencies, hidden contract consumers, and missing invalidation edges before readiness.

**Consequences (testable):**

- Every capability, module, phase, and contract has exactly the ownership cardinality permitted by its schema.
- Impact analysis identifies descendants affected by a proposed change.

**Traceability:** Decisions D012, D013, D014, D026; journeys UJ-05, UJ-10.

## Known failure and edge conditions

- A general agent is the undocumented owner of several semantic decisions.
- Modules are split by folders such as prompts and schemas rather than responsibility.
- A downstream phase edits upstream JSON in place.
- A phase context includes the entire repository and conversation by default.

## Explicitly out of scope

- Final implementation file layout beyond approved module and interface constraints.
- Premature extraction of a universal creative module.
- Provider-specific internals that do not affect the public contract.
