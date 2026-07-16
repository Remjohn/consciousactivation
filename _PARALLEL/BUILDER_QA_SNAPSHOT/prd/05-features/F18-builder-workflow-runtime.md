---
title: F18 — Builder Workflow Runtime and Agentic Execution Factory
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F18
governing_decisions:
- D001
- D002
- D003
- D006
- D011
- D012
- D013
- D014
- D015
- D017
- D018
- D019
- D020
- D021
- D022
- D023
- D024
- D025
- D026
- D027
- D028
- D029
- D032
- D033
user_journeys:
- UJ-04
- UJ-05
- UJ-07
- UJ-08
- UJ-09
- UJ-10
- UJ-11
- UJ-12
- UJ-13
- UJ-14
functional_requirement_count: 30
---

# F18 — Builder Workflow Runtime and Agentic Execution Factory

**User outcome:** A Builder Maintainer can run the Harness Builder as a reproducible, observable, testable workflow that deliberately combines human authority, bounded agent judgment, and deterministic code.

## Description

This feature turns the approved Builder lifecycle, graphs, contracts, skills, validators, and human gates into a literal executable workflow. Local feedback loops remain implementation details inside a larger information-flow system. The product must know which actor creates value at each node, isolate failure, route evidence, control compute, and prove the complete workflow rather than rely on Pi to follow one sophisticated conversation.

## Brownfield baseline

V2.1 offers deterministic CLI stages, Pi prompts, decision-graph logic, tests, compilation, and readiness. The PRD already defines Phase, Context, Contract, Reference, Dependency, Repair, and Control Tower models. What is missing is a first-class Workflow IR, runtime, router, node execution boundary, isolation policy, workflow profiles, workflow-level tests, promotion pipeline, and incident operations connecting those pieces end to end.

## Required product delta

Add an executable Builder Workflow Runtime with a canonical Workflow IR, explicit human-agent-code Actor Assignment Matrix, specialized Workflow Profile Registry, deterministic routing, phase-local agent execution, code-owned validation, sandboxes, bounded retries and parallelism, node telemetry, workflow integration and fault tests, CI promotion, rollback, and incident/hotfix paths. Derive Release 1 automation from a recorded shadow workflow of the reference harness.

## Traceability

- **Decisions:** D001, D002, D003, D006, D011, D012, D013, D014, D015, D017, D018, D019, D020, D021, D022, D023, D024, D025, D026, D027, D028, D029, D032, D033
- **User journeys:** UJ-04, UJ-05, UJ-07, UJ-08, UJ-09, UJ-10, UJ-11, UJ-12, UJ-13, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-OBS-001, NFR-OBS-002, NFR-OBS-004, NFR-SEC-003, NFR-SEC-004, NFR-COMPAT-002, NFR-PORT-002, NFR-ARCH-001, NFR-ARCH-002, NFR-TEST-001, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-WORKFLOW-006, NFR-WORKFLOW-007, NFR-WORKFLOW-008, NFR-WORKFLOW-009, NFR-WORKFLOW-010, NFR-WORKFLOW-011, NFR-WORKFLOW-012

## Functional Requirements

### FR-181 — Define the canonical Builder Workflow IR

**Requirement:** The Builder must represent each executable Builder workflow as a versioned Workflow IR containing profile identity, nodes, actor assignments, contracts, conditions, routes, budgets, isolation, events, retries, human gates, tests, and promotion status.

**Consequences (testable):**

- The same workflow definition can be validated, rendered, executed, diffed, and migrated from one canonical object.
- A production run cannot execute an unregistered workflow graph assembled only from conversation history.

**Traceability:** Decisions D006, D011, D013, D014; journeys UJ-13.

### FR-182 — Assign one explicit actor model to every node

**Requirement:** Every workflow node must declare deterministic code, bounded agent program, human gate, or governed hybrid as its primary actor and must state why that actor is appropriate.

**Consequences (testable):**

- A node without actor ownership fails Workflow IR validation.
- Mechanical transformations cannot be assigned to an agent-only node without an approved exception and comparison evidence.

**Traceability:** Decisions D002, D012, D015; journeys UJ-05, UJ-13.

### FR-183 — Model typed nodes, conditions, and feedback edges

**Requirement:** The Workflow IR must represent node prerequisites, entry conditions, success and failure exits, conditional routes, approved feedback loops, terminal states, and downstream invalidation.

**Consequences (testable):**

- A feedback edge cannot exist without retry limits, failure ownership, and a terminal condition.
- The graph validator identifies unreachable nodes, orphan outputs, illegal cycles, and conditions without outcomes.

**Traceability:** Decisions D006, D013, D014, D026; journeys UJ-10, UJ-13.

### FR-184 — Compile workflows from approved product graphs

**Requirement:** The Builder Workflow Runtime must compile its executable node graph from the governed lifecycle, target profile, capability ownership, phase, context, contract, dependency, repair, and authorization definitions rather than maintain an unrelated orchestration model.

**Consequences (testable):**

- A changed contract or phase dependency regenerates and revalidates the affected workflow definition.
- A workflow node cannot bypass a lifecycle or authorization prerequisite represented in the product graphs.

**Traceability:** Decisions D006, D011, D012, D013, D014, D019, D026, D027; journeys UJ-13.

### FR-185 — Maintain a versioned Workflow Profile Registry

**Requirement:** The product must register specialized workflows for materially different work classes, initially including new harness compilation, incremental evidence refresh, V2.1 migration, skill regression, category-constitution change, benchmark regression, repair, incident hotfix, and re-certification as they become release-scoped.

**Consequences (testable):**

- Every profile declares allowed inputs, target and risk classes, required nodes, human gates, budgets, tests, and certification state.
- An uncertified or non-release-scoped profile cannot be selected for production work.

**Traceability:** Decisions D006, D021, D022, D028, D032; journeys UJ-12, UJ-13, UJ-14.

### FR-186 — Route requests through an explicit Workflow Router

**Requirement:** A deterministic or bounded classifier must select an eligible Workflow Profile from request type, compilation target, run state, risk, incident class, and registry policy before execution begins.

**Consequences (testable):**

- Routing returns the selected profile, version, confidence or deterministic rule, alternatives, and reason.
- Ambiguous high-risk routing blocks for human selection rather than choosing silently.

**Traceability:** Decisions D002, D006, D012, D019, D025; journeys UJ-09, UJ-13, UJ-14.

### FR-187 — Require a manual shadow workflow before production automation

**Requirement:** The selected Release 1 reference path must first be executed and observed end to end with every human action, agent judgment, deterministic operation, handoff, condition, failure, cost, and artifact recorded before the workflow is promoted for automation.

**Consequences (testable):**

- The shadow trace maps each observed step to a proposed Workflow IR node or documents why it is intentionally excluded.
- A production node without shadow, prior-system, or benchmark evidence requires explicit architecture justification.

**Traceability:** Decisions D003, D022, D028, D032; journeys UJ-12, UJ-13.

### FR-188 — Separate deterministic code execution from agent execution

**Requirement:** The runtime must invoke deterministic transforms, validators, linters, schema checks, graph checks, parsers, and state mutations as code-owned nodes outside the agent skill or prompt that consumes their results.

**Consequences (testable):**

- An agent cannot claim a deterministic check passed without a recorded code execution result.
- Code failure is returned as a structured contract to the responsible node instead of being hidden in free-form agent output.

**Traceability:** Decisions D012, D014, D015, D018, D033; journeys UJ-05, UJ-13.

### FR-189 — Execute agent nodes through evaluated phase-local capsules

**Requirement:** Every agent-owned node must run from a versioned typed model program or agent adapter using the exact approved JIT Execution Capsule, input contracts, model policy, and tool permissions for that node.

**Consequences (testable):**

- The run records capsule, skill, recipe, model, adapter, input, and output identities.
- An agent node cannot inherit unrestricted session history or unapproved future-stage instructions.

**Traceability:** Decisions D013, D017, D018, D019, D020, D021; journeys UJ-07, UJ-13.

### FR-190 — Validate every node before releasing its outputs

**Requirement:** A node output must pass all declared deterministic validators, semantic evaluators, authority checks, and completion criteria before its contract becomes consumable by downstream nodes.

**Consequences (testable):**

- A failed validation prevents downstream scheduling and emits a typed blocker.
- The validator set and exact evidence are recorded with the node completion receipt.

**Traceability:** Decisions D003, D014, D021, D024, D027; journeys UJ-09, UJ-13.

### FR-191 — Return structured failure context only to the responsible node

**Requirement:** When a validator or evaluator fails, the runtime must package the minimal complete failure evidence and route it to the root-cause owner defined by the Repair and Invalidation Graph rather than replay the entire run.

**Consequences (testable):**

- Unrelated nodes do not receive or rerun from the failure unless their contracts are invalidated.
- The feedback package identifies failed criteria, evidence, allowed repair scope, frozen state, and regression requirements.

**Traceability:** Decisions D014, D020, D026; journeys UJ-10, UJ-14.

### FR-192 — Require root-cause investigation before workflow repair

**Requirement:** The repair workflow must reproduce and localize a workflow failure, compare working and failing paths, state a testable root-cause hypothesis, and gather evidence before modifying the responsible node, route, skill, or contract.

**Consequences (testable):**

- A repair proposal without a reproduced or evidenced failure remains blocked.
- Repeated failed repairs trigger architecture escalation rather than indefinite patch accumulation.

**Traceability:** Decisions D024, D026, D033; journeys UJ-10, UJ-14.

### FR-193 — Enforce bounded retries, timeouts, and circuit breakers

**Requirement:** Every retryable node and feedback edge must declare maximum attempts, backoff or scheduling policy, timeout, retryable failure classes, non-retryable failures, circuit-breaker condition, and escalation destination.

**Consequences (testable):**

- The runtime cannot enter an unbounded self-correction loop.
- Exhausted retries terminate in a typed blocked or failed state with preserved evidence.

**Traceability:** Decisions D006, D019, D024, D026, D033; journeys UJ-09, UJ-14.

### FR-194 — Support idempotent checkpoints and resume

**Requirement:** The runtime must checkpoint committed node inputs, outputs, validation receipts, side effects, selected profile, and next eligible nodes so interrupted workflows resume without duplicating successful work.

**Consequences (testable):**

- Resume reuses committed deterministic results when their dependencies and versions remain valid.
- A changed dependency invalidates only affected checkpoints and records the reason.

**Traceability:** Decisions D006, D011, D019, D025, D026; journeys UJ-04, UJ-13.

### FR-195 — Isolate workflow nodes and implementation tasks

**Requirement:** Architecture must assign worktree, process, container, or stronger sandbox isolation to nodes and implementation stories according to tool risk, source sensitivity, concurrency, and reproducibility needs.

**Consequences (testable):**

- Parallel writers cannot mutate the same authoritative branch or workspace without an explicit merge protocol.
- Sandbox cleanup, artifact extraction, and failure preservation are testable.

**Traceability:** Decisions D012, D015, D025, D029; journeys UJ-11, UJ-13.

### FR-196 — Apply least-privilege tool, source, secret, and network access

**Requirement:** Each sandbox or agent node must receive only the sources, tools, credentials, filesystem paths, network destinations, and write permissions declared by its node contract.

**Consequences (testable):**

- A node cannot access unrelated source archives or protected benchmark labels.
- Secrets are injected through runtime mechanisms and never persisted in capsules, IR, logs, or Development Capsules.

**Traceability:** Decisions D012, D014, D016, D020, D033; journeys UJ-13, UJ-14.

### FR-197 — Parallelize only dependency-independent work

**Requirement:** The scheduler may run deterministic scans, candidate generation, evaluator repetitions, or implementation tasks in parallel only when the Workflow IR proves independence and defines concurrency, cancellation, merge, and conflict policy.

**Consequences (testable):**

- A dependency or shared-write conflict prevents parallel scheduling.
- Cancellation of one branch does not corrupt completed sibling results.

**Traceability:** Decisions D013, D014, D019, D024; journeys UJ-12, UJ-13.

### FR-198 — Use quality-gated candidate races

**Requirement:** When multiple agents or sandboxes generate competing candidates, selection must follow declared evidence, contract, quality, cost, and latency gates rather than accept the first completed candidate automatically.

**Consequences (testable):**

- A faster candidate that fails a hard gate cannot win.
- The selection receipt records every candidate considered, gate results, arbitration method, and compute spent.

**Traceability:** Decisions D003, D021, D024, D033; journeys UJ-08, UJ-12, UJ-13.

### FR-199 — Route model and compute by task complexity and risk

**Requirement:** The runtime must select model tier, candidate count, evaluator strength, tool access, and compute budget using an explicit policy informed by node responsibility, ambiguity, risk, expected value, and prior benchmark performance.

**Consequences (testable):**

- Mechanical work is not automatically assigned to the most expensive model.
- A lower-cost route that increases turns or failure rate can be rejected using total-cost and reliability evidence.

**Traceability:** Decisions D003, D012, D020, D024; journeys UJ-12, UJ-13.

### FR-200 — Isolate independent evaluators from generator context

**Requirement:** Evaluation nodes must receive the minimum contracts, rubric, evidence, candidate, and provenance required for judgment and must not inherit generator reasoning, preferred answers, or hidden benchmark labels.

**Consequences (testable):**

- Generator and evaluator contexts are separately receipted.
- A self-evaluation may be advisory but cannot satisfy an independent hard gate alone.

**Traceability:** Decisions D014, D020, D021, D024; journeys UJ-08, UJ-12, UJ-13.

### FR-201 — Place human gates according to authority and operational risk

**Requirement:** Workflow Profiles must declare required human planning, ratification, waiver, incident, release, and final-review gates and may remove them only through an approved evidence-backed policy change.

**Consequences (testable):**

- Constitutional and irreversible decisions cannot be bypassed by an autonomous route.
- Low-risk automated nodes can continue without unnecessary operator interruptions when their gates and evidence pass.

**Traceability:** Decisions D002, D006, D010, D024, D027; journeys UJ-04, UJ-09, UJ-13, UJ-14.

### FR-202 — Expose workflow queues and status transitions

**Requirement:** The runtime must represent queued, eligible, running, waiting-human, blocked, retrying, cancelled, passed, failed, and superseded node states and make their transitions observable and queryable.

**Consequences (testable):**

- A node cannot be simultaneously authoritative in conflicting states.
- The Control Tower can show why a queued node is not yet eligible.

**Traceability:** Decisions D006, D025; journeys UJ-09, UJ-13, UJ-14.

### FR-203 — Emit node-level workflow telemetry

**Requirement:** Every node execution must report actor, workflow and node version, start and end time, latency, deterministic compute, model tokens and cost, tool calls, retries, cache use, sandbox identity, artifacts, validation, and final status.

**Consequences (testable):**

- Telemetry can be aggregated by workflow profile, target, phase, skill, model, release, and authorized capsule.
- Missing mandatory telemetry prevents a production completion claim.

**Traceability:** Decisions D024, D025, D027; journeys UJ-09, UJ-12, UJ-13.

### FR-204 — Test complete workflow behavior at public seams

**Requirement:** The Builder must maintain end-to-end tests proving routing, node contracts, validation, feedback, resume, human gates, authorization, observability, and artifact identity across the reference workflow.

**Consequences (testable):**

- A module test pass cannot substitute for a failed workflow integration test.
- Workflow tests assert externally observable state, events, contracts, and artifacts rather than private implementation details.

**Traceability:** Decisions D003, D022, D023, D024, D032; journeys UJ-12, UJ-13.

### FR-205 — Run workflow fault-injection and recovery tests

**Requirement:** Production Workflow Profiles must be tested against agent errors, malformed contracts, code failures, timeouts, lost events, sandbox termination, stale checkpoints, unavailable providers, and partial parallel failure.

**Consequences (testable):**

- Each injected failure reaches the expected contained state and repair or escalation route.
- The run can be reconstructed and resumed or safely rolled back after the fault.

**Traceability:** Decisions D022, D023, D024, D026; journeys UJ-12, UJ-14.

### FR-206 — Promote workflow definitions through CI and release gates

**Requirement:** Workflow IR schemas, profiles, routers, node adapters, validation policies, and sandbox policies must pass versioned tests and benchmark gates before promotion from draft to tested and production.

**Consequences (testable):**

- A workflow change cannot be activated in production because a Markdown or prompt file changed locally.
- Promotion binds exact workflow, code, capsule compiler, contract, test, and benchmark identities.

**Traceability:** Decisions D003, D021, D022, D024, D028; journeys UJ-12, UJ-13.

### FR-207 — Version, migrate, and roll back workflow profiles

**Requirement:** The product must support explicit compatibility, migration, deprecation, dual-run comparison, and rollback for Workflow IR, node contracts, routes, and profile versions.

**Consequences (testable):**

- An in-flight run remains bound to its compatible workflow version unless a governed migration occurs.
- A rollback restores the previous validated profile without losing incident or migration history.

**Traceability:** Decisions D011, D025, D028; journeys UJ-12, UJ-14.

### FR-208 — Provide specialized incident and hotfix workflows

**Requirement:** The Workflow Profile Registry must support a constrained incident path for severe Builder failures such as corrupted source lock, JIT compiler regression, benchmark leakage, false readiness, or stable-skill regression.

**Consequences (testable):**

- The hotfix path limits scope, requires explicit human approval at declared gates, and runs targeted verification before promotion.
- Emergency status does not authorize mutation of protected evidence, benchmark labels, or constitutional decisions.

**Traceability:** Decisions D002, D024, D025, D026, D027, D028; journeys UJ-09, UJ-14.

### FR-209 — Measure workflow cost, latency, quality, and intervention

**Requirement:** Every Workflow Profile must define and report p50/p95 node and end-to-end latency, deterministic compute, model tokens and cost, retry rate, first-pass pass rate, failure containment, operator interventions, and cost per authorized Development Capsule.

**Consequences (testable):**

- Performance comparisons include accepted quality and hard-gate results, not speed or price alone.
- Budget regressions are visible before workflow promotion.

**Traceability:** Decisions D003, D020, D024, D025; journeys UJ-12, UJ-13.

### FR-210 — Reject monolithic skill-owned production workflows

**Requirement:** The Builder must fail architecture and readiness when a production workflow hides multiple independently testable nodes, deterministic checks, routing conditions, and human gates inside one large SKILL.md, prompt, or unrestricted agent session.

**Consequences (testable):**

- A simple experimental prototype may receive prototype-only authorization with explicit scope and disposal rules.
- Production approval requires separated node ownership, contracts, validators, observability, and workflow tests.

**Traceability:** Decisions D001, D012, D013, D014, D017, D027, D033; journeys UJ-11, UJ-13.

## Known failure and edge conditions

- One Pi skill or conversation performs planning, execution, validation, retry, and authorization without separable node evidence.
- The fastest candidate is accepted before quality and contract gates run.
- A retry loop has no terminal condition or escalates cost indefinitely.
- A sandbox can access unrelated sources, protected labels, or persistent secrets.
- A failed node causes the entire run to restart or corrupts previously ratified state.
- A workflow is promoted because its component tests pass while end-to-end routing or resume behavior fails.
- Human review is removed to increase automation without evidence that the decision class is safe.

## Explicitly out of scope

- A general-purpose software-factory platform for arbitrary organizations or non-CMF products.
- Selecting the final workflow engine, container platform, queue, or cloud provider in the PRD.
- Maximizing the number of agents, sandboxes, or parallel branches as a success target.
- Removing constitutional human authority from the Harness Builder.
