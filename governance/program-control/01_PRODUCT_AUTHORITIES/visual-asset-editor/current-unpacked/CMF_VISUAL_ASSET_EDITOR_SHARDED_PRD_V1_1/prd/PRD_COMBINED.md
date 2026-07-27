---
title: PRD: CMF Visual Asset Editor
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-14'
source: sharded_prd
---

# PRD: CMF Visual Asset Editor

> Combined reading view generated from the canonical shards listed in [`index.md`](index.md). Edit the shards, not this file.


---

# Document Purpose and Authority

This PRD defines the product requirements for an independently versioned **CMF Visual Asset Editor**. The intended readers are CMF product owners, Harness Architects, Visual Runtime specialists, evaluators, infrastructure engineers, implementation agents, and release reviewers.

The PRD is governed by:

- the 28 locked decisions in [`../governance/DECISION_REGISTER.md`](../governance/DECISION_REGISTER.md);
- the frozen upstream architecture in [`../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`](../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml);
- globally stable Functional Requirement and Non-Functional Requirement IDs;
- the source and evidence register;
- the Release 1 Format 02 reference slice.

## Authority order

```text
Validated Atomic Harness Builder architecture
→ approved Visual Asset Editor product constitution
→ this PRD and Requirements Registry
→ future Visual Asset Editor Architecture
→ future Epics, Stories and feature specifications
→ implementation
```

A lower layer may implement or clarify an approved requirement. It may not silently redefine an upstream authority.

## Product separation

The Visual Asset Editor is one of three explicit compilation targets already recognized by the Atomic Harness Builder:

1. Atomic Content Harness;
2. Visual Asset Editor;
3. Content ↔ Visual Asset Delegation Contract.

This PRD governs only the second product. Shared request/response schemas and compatibility policy will be finalized by the separate Delegation PRD.

## Stable identifiers

- Decisions: `D001`–`D028`
- User journeys: `UJ-01`–`UJ-16`
- Features: `F01`–`F22`
- Functional Requirements: `FR-001`–`FR-176`
- Non-Functional Requirements: category-specific `NFR-<GROUP>-NNN`

## Status meaning

`draft_for_review` means the planning decisions have been compiled and mechanically validated, but Architecture has not yet been approved and implementation is not authorized.


---

# Vision and Product Promise

## Vision

The CMF Visual Asset Editor is the autonomous production system that turns an Atomic Content Harness’s authorized visual demand into assets that are visually effective, reproducible, composition-ready, and faithful to the shared Activative doctrine.

It exists because an Atomic Harness should own **meaning, sequence role, Activative purpose, and composition intent**, while a dedicated visual-production system should own the complex and rapidly evolving methods required to materialize that meaning:

- asset reuse and retrieval;
- extraction and transformation;
- deterministic construction and compositing;
- ComfyUI workflows;
- local models, VAEs, LoRAs, controls, and custom nodes;
- cloud and local GPU execution;
- candidate portfolios;
- independent VLM evaluation;
- targeted repair;
- asset memory and steering intelligence;
- immutable delivery and provenance.

## Canonical product promise

> The CMF Visual Asset Editor is an independently versioned, autonomous visual asset-resolution system that transforms validated Visual Asset Demand Contracts into provenance-complete Reference Evidence and production-ready visual assets through governed reuse, retrieval, extraction, transformation, compositing, deterministic construction, generation, animation, or capture requests. It resolves production method, visual materials, image-conditioned geometry, evaluation, repair, compute, and delivery without altering the requesting harness’s authorized meaning, sequence role, Activative purpose, or composition intent.

## Strategic correction

The product is not:

- a universal creative director;
- a manual ComfyUI workstation;
- a one-prompt image generator;
- an unbounded agent swarm;
- a rights-review bureaucracy;
- a vector database presented as memory;
- a provider-specific workflow JSON repository;
- a visual substitute for the Content Harness’s semantic authority.

The product is a governed visual-production factory combining deterministic code, bounded specialist judgment, visual models, independent evaluation, immutable contracts, and exception-only human authority.

## Success hierarchy

```text
Gate 1 — Production validity
The asset is technically complete, reproducible, deliverable, and traceable.

Gate 2 — Demand fidelity
Independent evaluation confirms semantic, Activative, identity,
continuity, visual-property, and wrong-reading compliance.

Gate 3 — Composition effectiveness
The asset works inside its intended BBOX, scene/slide/frame,
visual hierarchy, sequence position, and viewer-state progression.
```

The product is successful only when downstream composition can consume an accepted asset without manual production intervention and can verify every material decision through contracts and receipts.


---

# Users, Jobs, and Journeys

## Primary users and callers

### Atomic Content Harness

Submits typed demands, retains semantic and composition authority, observes execution, receives result contracts, and authorizes demand amendments.

### Visual Asset Editor operator

Supervises budgets, production priorities, experiments, exceptions, capability development, releases, and readiness without performing routine node-level editing.

### Visual Runtime specialist

Builds and certifies ComfyUI workflows, Docker runtimes, custom nodes, model/LoRA/control profiles, compute routing, and recovery.

### Visual evaluation owner

Curates labeled datasets, VLM evaluation profiles, failure taxonomy, calibration, recurrence analysis, and release benchmarks.

### Harness and composition runtime

Consumes accepted assets, geometry, masks, variants, evaluations, and syntax-context receipts.

### Release manager

Approves compatibility, certified scope, implementation readiness, limited production, production promotion, and rollback.

## Jobs to be done

- Produce the correct visual artifact from a rich typed demand without manual production.
- Preserve Content Harness meaning while allowing production methods to evolve independently.
- Select the simplest reliable production route and only the capabilities certified for the task.
- Evaluate both the isolated asset and its actual composition.
- Repair failures causally without destroying correct properties or replaying the entire workflow.
- Learn from controlled production evidence without silently self-modifying.
- Run local and cloud visual compute reproducibly through APIs and containers.
- Know exactly what happened, why it happened, what it cost, and which version was consumed.
- Distinguish beneficial continuity from redundant visual repetition.
- Certify only the asset families and format integrations that have earned production status.

## Key journeys

### UJ-01 — Content Harness requests an autonomous production asset

A registered Atomic Content Harness submits a typed demand, receives an execution ID, observes production events, and consumes an accepted asset result without manual production work.

### UJ-02 — Asset Commander resolves a routine demand

The system validates the demand, selects a Budget Program, compiles a Visual Production Plan, routes compute, evaluates candidates, repairs if needed, and promotes the accepted asset.

### UJ-03 — Format 02 receives a continuity-safe character pose

Minimal Coach Theatre requests a specific identity, pose, expression, gaze, gesture, and composition role and receives an asset with geometry and continuity receipts.

### UJ-04 — Composition runtime verifies asset fit

A downstream composition system places an accepted asset inside the intended scene or slide and validates crop, hierarchy, negative space, gaze, and BBOX effectiveness.

### UJ-05 — Operator inspects an autonomous run

The operator opens the Control Tower to understand plan selection, memory retrieval, GPU execution, candidate evidence, VLM verdicts, repairs, cost, and final lineage.

### UJ-06 — Operator selects a Budget Program

The operator chooses Lean, Standard, Premium, Exploration, Capability Learning, or Custom and receives an estimated candidate, compute, latency, and learning envelope.

### UJ-07 — VLM triggers targeted repair

An evaluator identifies a localized visual failure, emits a typed repair contract, preserves successful properties, and causes only responsible nodes to rerun.

### UJ-08 — System recovers from infrastructure failure

A cloud worker or ComfyUI container fails; the workflow resumes from checkpoints on a compatible runtime without consuming a quality-repair round.

### UJ-09 — System reuses an asset in a new syntax context

Memory retrieval finds an accepted asset, compares its rendered prior uses to the current Visual Syntax context, and distinguishes beneficial recurrence from fatigue.

### UJ-10 — Exploration program creates steering evidence

A controlled candidate portfolio varies declared bindings, records outcomes, and proposes a Steering Recipe without silently changing production defaults.

### UJ-11 — Capability gap creates a LoRA development plan

Repeated evidence-backed failures reveal a reusable identity or visual-language gap and trigger a separate sandboxed adaptation, benchmark, shadow, and promotion workflow.

### UJ-12 — Editor proposes a demand amendment

After exhausting approved routes, the editor returns a typed conflict with evidence and nonbinding alternatives; the owning Content Harness authorizes a new demand version.

### UJ-13 — Evaluator release is certified

A new VLM evaluation profile is measured against labeled accepted, rejected, borderline, recurrence, and repair cases before shadow and limited production.

### UJ-14 — Visual Editor release proves compatibility

A release pins product, contract, registry, workflow, model, LoRA, evaluator, and runtime versions and passes representative old and current demand fixtures.

### UJ-15 — Knowledge retrieval compiles phase-local context

A production or repair node retrieves CMF-OKF knowledge through deterministic filters, typed graph edges, hybrid retrieval, VLM reranking, contradiction coverage, and context budgeting.

### UJ-16 — Release manager authorizes implementation and production scope

The release manager reviews readiness gates, Format 02 evidence, compute proof, benchmarks, known limitations, and rollback readiness before implementation or limited-production authorization.


---

# Canonical Glossary

Downstream Architecture, Epics, Stories, contracts, code, UI, and course material must use these terms consistently.

### Accepted Production Asset

An immutable asset version that passed production validity, demand fidelity, and composition effectiveness and is authorized for declared downstream use.

### Activative Function

The intended contribution of an asset to viewer-state change, recognition, participation, destabilization, reinforcement, or payoff.

### Asset Commander

The workflow authority that validates state, routes plans, enforces budgets, invokes evaluation and repair, promotes assets, and escalates typed exceptions without performing specialist creative analysis.

### Asset Family

A canonical reusable production class governing eligible routes, capabilities, evaluators, geometry, continuity, and delivery.

### Asset Intelligence Hunter

A conditional specialist that retrieves approved internal assets and reference evidence when a resolution route requires them.

### Asset Result Contract

The final typed service response identifying accepted assets, delivery variants, geometry, evaluations, production and budget receipts, limitations, and composition authorization.

### Budget Program

A versioned policy controlling candidates, parallelism, repair rounds, workflow variation, evaluator depth, cost, latency, and learning scope.

### Candidate Portfolio

A bounded, declared set of exploration, repair, or fallback candidates produced under one plan and Budget Program.

### Capability Development Plan

A separate governed plan for developing a reusable LoRA, model adaptation, control, workflow, or evaluator capability from evidence-backed recurring gaps.

### CMF-OKF Profile

A CMF extension of Open Knowledge Format used as a portable human/agent-readable projection of durable knowledge, never as canonical transactional state.

### Composition Effectiveness

Whether the asset performs its intended visual, syntactic, and Activative function when placed inside the actual scene, slide, frame, crop, hierarchy, and neighboring elements.

### Composition Feasibility Analyst

A specialist that converts composition intent into measurable feasibility, geometry, controls, conflicts, and recommendations.

### Composition Geometry

Image- or video-conditioned BBOXes, masks, safe zones, gaze/motion vectors, depth/layer information, crops, and collision analysis returned for downstream composition.

### Composition Intent

The requesting harness’s authoritative definition of canvas, intended region, tolerance, layer, visual weight, reserved/protected regions, direction, crop, and background behavior.

### Constraint Conflict

A typed, evidence-backed statement that an accepted demand cannot be fulfilled under its current constraints after authorized routes and repairs.

### Demand Amendment Proposal

A nonbinding option returned to the owning Content Harness when fulfilling the demand requires authority beyond internal production changes.

### Delivery Variant

An immutable deterministic derivative of an accepted master for a registered canvas, crop, mask, codec, alpha, preview, or downstream profile.

### Editor / Materializer

The deterministic and model execution nodes that implement an approved Visual Production Plan without redesigning it.

### Human Exception

A typed decision package issued only after authorized escalation conditions such as repair exhaustion, cost, capability, evaluator, conflict, or degradation.

### Independent Visual Evaluator

A VLM/deterministic evaluation authority isolated from production and responsible for profile-specific quality contracts.

### JIT Execution Capsule

The smallest complete phase-local prompt/context package compiled from canonical skills, adaptations, plan node, bindings, relevant knowledge, and output contract.

### LoRA Registry

The versioned catalog of LoRA/adaptation capabilities, compatibility, strength envelopes, benchmarks, provenance, failures, and maturity.

### Minimum Complete Context

The smallest authoritative evidence and knowledge set sufficient for one node’s responsibility and output contract.

### Production Binding

The pinned workflow, runtime, model, VAE, LoRA, control, parameter, input, and evaluator configuration compiled for execution.

### Production Validity

Technical integrity, deliverability, metadata completeness, and reproducibility of an asset independent of semantic quality.

### Reference Evidence

Material used to understand, condition, guide, or evaluate production that is not automatically authorized for final composition.

### Resolution Strategy Composer

The specialist that selects the least complex viable multi-method route and emits a typed Visual Production Plan.

### Semantic Sovereignty

The law that the Visual Asset Editor may resolve production but cannot rewrite the requesting Content Harness’s authorized meaning.

### Steering Recipe

A versioned, evidence-backed production intervention with applicability, preservation, bindings, control comparison, regressions, and lifecycle.

### Syntax Context Fingerprint

A comparable representation of an asset’s rendered Visual Syntax role, geometry, relationships, recurrence intent, and appearance.

### Visual Asset Demand

The immutable typed contract defining the requested asset’s family, role, meaning, Activative function, composition, continuity, wrong-reading locks, delivery, evaluation, and execution policy.

### Visual Asset Memory

The governed store of immutable assets, geometry, lineage, evaluations, usage contexts, recurrence verdicts, supersession, and retrieval indexes.

### Visual Capability Registry

The governed versioned catalog of workflows, models, VAEs, LoRAs, controls, custom nodes, evaluator profiles, and runtime profiles.

### Visual Compute Fabric

The hybrid pool and scheduler for isolated local, self-hosted, cloud, autoscaled, and approved external visual compute workers.

### Visual Evaluation Profile

The versioned family/route/context-specific combination of deterministic validators, VLM programs, thresholds, hard gates, failure codes, and repair mappings.

### Visual Production Plan IR

The provider-neutral canonical execution plan compiled from an accepted Visual Asset Demand.

### Visual Production Plan

A versioned instance of the Visual Production Plan IR containing objective, route, stages, capabilities, bindings, budgets, evaluators, fallbacks, and delivery.

### Visual Steering Intelligence

Governed cross-run knowledge that turns controlled production and repair evidence into validated Steering Recipes and routing insights.

### Visual Syntax Context

The scene/slide/frame role, composition function, BBOX, neighboring elements, sequence position, recurrence intent, and Activative purpose in which an asset is rendered.

### Visual Usage Receipt

The immutable record of one asset version’s actual rendered use and syntax/Activative context.

### Wrong-Reading Lock

A demand-level prohibited interpretation or visual pattern that must remain below its configured risk threshold.

### 2D Character Animation

The canonical category whose production substrate is a registry-driven character performance system using identities, poses, expressions, gestures, gaze, props, animation primitives, scene states, and continuity.

### Format 02 Minimal Coach Theatre

The Release 1 reference format profile for 2D Character Animation and the first production-certified Visual Asset Editor integration.

### Provider Artifact

A compiled execution artifact such as ComfyUI workflow JSON or an external API payload derived from the canonical Visual Production Plan.

### Quality Repair Round

One VLM-directed causal correction cycle; no run may exceed three autonomous quality rounds.

### Recurrence Verdict

A VLM classification of beneficial recurrence, neutral reuse, productive variation, redundant repetition, fatiguing pattern, or contradictory recurrence.

### Runtime Profile

A digest-pinned execution environment declaring container, ComfyUI, custom nodes, hardware, API, mounts, concurrency, health, and certification.

### Visual Asset Service

The asynchronous contract-driven public boundary through which registered systems submit demands and receive events, exceptions, and results.

### Architecture Preservation Contract

The machine-readable declaration that the Visual Asset Editor adds an independent product without redesigning validated Atomic Harness Builder architecture.


---

# Product Doctrine and First Principles

## 1. Semantic sovereignty

The Content Harness owns meaning. The Visual Asset Editor owns production resolution. A provider, model, workflow, evaluator, memory item, or operator cannot silently replace the demand’s semantic or Activative obligation.

## 2. Visual syntax is production context

The editor must understand where an asset functions: composition region, syntactic role, sequence position, neighboring elements, visual weight, recurrence intent, and viewer-state purpose. Asset production and memory retrieval without this context are incomplete.

## 3. Provider-neutral plan, provider-specific execution

Visual Production Plan IR is canonical. ComfyUI graphs, model API payloads, container commands, and editing scripts are compiled implementation artifacts.

## 4. Deterministic orchestration, bounded stochastic execution

Code owns routing, lifecycle, contracts, registry compatibility, budget, state, retries, invalidation, and promotion. Models perform bounded analysis, generation, and evaluation within those constraints.

## 5. Independent visual judgment

The production model may create assets. It cannot be the sole judge of its own output. Evaluation must be separately versioned, benchmarked, and traceable.

## 6. Composition effectiveness over standalone beauty

A compelling image that fails inside its actual BBOX, crop, text hierarchy, scene, or sequence is a failed production asset.

## 7. Repair the smallest responsible layer

Preserve everything already correct. Change only causal bindings. Rerun only invalidated nodes. Stop after three VLM-directed quality rounds.

## 8. Repetition is contextual

Repeated identity, visual world, motif, or instrument may strengthen continuity. Fatigue is a VLM judgment about rendered Visual Syntax context and progression—not raw usage count.

## 9. Minimum Complete Context

Specialists and evaluators receive the smallest authoritative context needed for their responsibility. Memory retrieval is authority-filtered, graph-aware, multimodal, contradiction-aware, and receipted.

## 10. Evidence before production policy

One successful candidate does not become a Steering Recipe. One failed request does not trigger LoRA training. Production policy changes require controlled comparison, benchmark evidence, shadow use, and promotion.

## 11. Quality-first budget programs

Higher budgets authorize controlled exploration and learning, not indiscriminate generation. Quality hard gates remain constant across budget programs.

## 12. Immutable assets and reproducible compute

Every accepted asset pins its demand, plan, source evidence, workflow, model, VAE, LoRA, controls, custom nodes, container, evaluator, parameters, geometry, cost, and lineage.

## 13. Exception-only human authority

Ordinary production is autonomous. Humans resolve typed authority, cost, conflict, capability, evaluator, or degradation exceptions—not routine ComfyUI work.

## 14. Certified scope honesty

Represented architecture is not production support. Asset families, workflows, evaluators, runtime profiles, and format integrations must earn certified scope.

## 15. Architecture preservation

The Visual Asset Editor extends the validated Atomic Harness Builder architecture. It does not replace Harness IR, JIT architecture, workflow runtime, Control Tower, repair doctrine, category constitutions, or Development Capsule governance.


---

# Feature Index


- [F01 — Product Constitution, Semantic Sovereignty, and Autonomous Authority](05-features/F01-product-constitution-autonomous-authority.md) — A registered caller can rely on an autonomous editor that resolves production without rewriting the caller’s authorized meaning. **FRs:** FR-001–FR-008.
- [F02 — Visual Asset Demand Contract, Intake, and Authority Validation](05-features/F02-visual-asset-demand-intake.md) — A Content Harness can submit one immutable, typed demand that gives the editor enough authority and constraints to produce the correct asset without relying on conversational context. **FRs:** FR-009–FR-016.
- [F03 — Canonical Asset Ontology and Reference/Production Separation](05-features/F03-asset-ontology-reference-production.md) — A caller and the editor can describe asset production needs with reusable families while preserving one harness-specific role and Activative purpose. **FRs:** FR-017–FR-024.
- [F04 — Immutable Asset Lifecycle, Lineage, Supersession, and Delivery Variants](05-features/F04-immutable-asset-lifecycle.md) — A downstream consumer can always identify the exact accepted master, understand how it was made, and determine whether a newer version supersedes it. **FRs:** FR-025–FR-032.
- [F05 — Composition Intent, Feasibility, and Image-Conditioned Geometry](05-features/F05-composition-intent-image-conditioned-geometry.md) — A Content Harness can declare where and how an asset must function, and downstream composition receives measured geometry rather than a vague visual suggestion. **FRs:** FR-033–FR-040.
- [F06 — Governed Multi-Method Resolution and Strategy Routing](05-features/F06-multi-method-resolution-routing.md) — A demand is fulfilled through the simplest reliable route or hybrid route rather than being sent indiscriminately to generation. **FRs:** FR-041–FR-048.
- [F07 — Dynamic Specialist Workcell and Authority Boundaries](05-features/F07-dynamic-specialist-workcell.md) — A demand activates only the analysis and production authorities needed for its actual route while preserving isolated evaluation and deterministic command. **FRs:** FR-049–FR-056.
- [F08 — Visual Capability Registry for Workflows, Models, LoRAs, Controls, and Runtimes](05-features/F08-visual-capability-registry.md) — A production plan can select only capabilities whose purpose, compatibility, quality, cost, and failure behavior are known and tested. **FRs:** FR-057–FR-064.
- [F09 — Visual Production Plan IR and Provider-Specific Compilation](05-features/F09-visual-production-plan-ir.md) — A validated demand becomes one inspectable, provider-neutral execution specification before ComfyUI or any other provider receives work. **FRs:** FR-065–FR-072.
- [F10 — Event-Sourced, Resumable Visual Production Runtime](05-features/F10-event-sourced-production-runtime.md) — A long-running visual job can execute, fail, recover, repair, and complete without losing state or replaying unrelated expensive work. **FRs:** FR-073–FR-080.
- [F11 — Visual Asset Memory, Syntax-Aware Reuse, and Contextual Recurrence](05-features/F11-visual-asset-memory-recurrence.md) — A new demand can reuse prior assets and lessons intelligently without confusing repetition with failure or continuity with fatigue. **FRs:** FR-081–FR-088.
- [F12 — Hybrid Containerized Visual Compute Fabric](05-features/F12-hybrid-visual-compute-fabric.md) — A production plan can run reproducibly on compatible local or cloud compute without dependency drift or operator-managed GPU sessions. **FRs:** FR-089–FR-096.
- [F13 — Governed LoRA, Adapter, Control, and Workflow Capability Development](05-features/F13-visual-capability-development.md) — A recurring production gap can become a reusable, tested capability without training new resources for every difficult request. **FRs:** FR-097–FR-104.
- [F14 — Visual Evaluation Profiles and Independent VLM Quality System](05-features/F14-visual-evaluation-profiles.md) — A candidate is judged against the right family, composition, syntax, continuity, and temporal criteria rather than by a universal aesthetic score. **FRs:** FR-105–FR-112.
- [F15 — Typed Visual Repair, Invalidation, and Bounded Reruns](05-features/F15-repair-invalidation-reruns.md) — A failed candidate can be corrected surgically while identity, composition, environment, and other successful properties remain stable. **FRs:** FR-113–FR-120.
- [F16 — Budget Programs, Candidate Portfolios, and Quality-First Selection](05-features/F16-budget-programs-candidate-portfolios.md) — Operators and callers can choose how much exploration, learning, cost, and latency a demand receives without weakening quality authority. **FRs:** FR-121–FR-128.
- [F17 — Visual Steering Intelligence, CMF-OKF Knowledge, and Smart Retrieval](05-features/F17-steering-intelligence-cmf-okf-retrieval.md) — A production or repair node receives the smallest authoritative memory that matches its demand, Visual Syntax context, capability, and failure rather than scanning a generic archive. **FRs:** FR-129–FR-136.
- [F18 — Control Tower Specialization and Supervisory Console](05-features/F18-control-tower-supervisory-console.md) — An operator can understand and govern every autonomous production run without becoming a manual editor or trusting an opaque black box. **FRs:** FR-137–FR-144.
- [F19 — Asynchronous Visual Asset Service and Delegation Boundary](05-features/F19-asynchronous-service-delegation.md) — A Content Harness can submit, observe, cancel, amend, and consume visual production through stable contracts without understanding internal ComfyUI workflows. **FRs:** FR-145–FR-152.
- [F20 — Constraint Conflicts, Feasibility Evidence, and Amendment Proposals](05-features/F20-constraint-conflicts-amendments.md) — When an authorized demand cannot be fulfilled, the editor explains the exact conflict and offers bounded alternatives without returning an attractive but semantically compromised approximation. **FRs:** FR-153–FR-160.
- [F21 — Benchmark Portfolio, Staged Certification, and Release 1 Format 02 Slice](05-features/F21-benchmarks-certification-release1.md) — A release can prove exactly which visual capabilities are reliable and avoid claiming support for untested asset families. **FRs:** FR-161–FR-168.
- [F22 — Independent Versioning, Architecture Preservation, Readiness, and Development Capsule](05-features/F22-versioning-readiness-development-capsule.md) — The Visual Asset Editor can evolve independently while preserving upstream Builder authority, cross-product compatibility, and a verifiable path from PRD to implementation. **FRs:** FR-169–FR-176.


---

# F01 — Product Constitution, Semantic Sovereignty, and Autonomous Authority

**User outcome:** A registered caller can rely on an autonomous editor that resolves production without rewriting the caller’s authorized meaning.

## Description

The product constitution fixes the editor’s production promise, authority boundary, operator role, three quality gates, and exception-only human intervention.

## Brownfield baseline

V2.1 already defines semantic sovereignty, the immutable Activative Visual Asset Program, reference/production separation, geometry return, and independent editor versioning, but assumes a heavier seven-lane workcell and rights layer.

## Required product delta

Preserve the validated upstream architecture while making routine production autonomous, removing the standalone Rights Analyst, and expressing semantic non-mutation, human exceptions, and layered success as enforceable product requirements.

## Traceability

- **Decisions:** D001, D002, D004, D010, D028
- **User journeys:** UJ-01, UJ-02, UJ-05, UJ-16
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-UX-001, NFR-UX-002, NFR-UX-003, NFR-UX-004, NFR-UX-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-001 — Enforce the complete visual asset-resolution promise

**Requirement:** The service must accept an authorized Visual Asset Demand and resolve it through any approved combination of reuse, retrieval, extraction, transformation, compositing, deterministic construction, generation, animation, or capture request.

**Consequences (testable):

- A run may select and combine only routes registered as eligible for the requested family, role, and demand.

- A system limited to a single generation or manipulation route fails product-conformance validation.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-002 — Preserve semantic sovereignty

**Requirement:** No production node, specialist, memory result, workflow fallback, evaluator, repair, or operator action may change the authorized semantic intent, Activative function, sequence role, composition role, identity, continuity, or wrong-reading locks in place.

**Consequences (testable):

- Every accepted asset can be traced to unchanged authoritative demand fields or to a newer explicitly authorized demand version.

- Any silent substitution produces a constitutional hard-gate failure and blocks asset promotion.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-003 — Operate autonomously inside authorized boundaries

**Requirement:** Routine demand validation, planning, memory retrieval, capability selection, candidate production, evaluation, repair, promotion, and delivery must execute without manual intervention.

**Consequences (testable):

- A fully passing routine run reaches COMPLETED without an approval click, manual prompt edit, candidate selection, or job restart.

- A workflow that pauses for ordinary operator approval fails the no-routine-manual-work acceptance test.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-004 — Limit human intervention to typed exceptions

**Requirement:** Human review may be requested only for max-repair exhaustion, unauthorized cost, unresolved capability gaps, blocking constraint conflicts, unresolved evaluator contradiction, or explicit degraded-result authority.

**Consequences (testable):

- Every human intervention contains a typed trigger, evidence, attempted repairs, preserved state, choices, and consequences.

- Unstructured requests such as 'please review' without an authorized exception code are rejected.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-005 — Apply three acceptance gates

**Requirement:** An asset is accepted only after production validity, demand fidelity, and intended-composition effectiveness pass their required profiles.

**Consequences (testable):

- The final result receipt contains separate verdicts and evidence for all three gates.

- A high aggregate score cannot compensate for failure in any mandatory gate.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-006 — Separate human authority from production execution

**Requirement:** The operator may govern budgets, production priorities, experimental scope, cost ceilings, exception choices, and capability promotion, but does not normally manipulate ComfyUI graphs or generation parameters.

**Consequences (testable):

- The supervisory console exposes policy and exception controls while normal runs retain autonomous node execution.

- A production path requiring routine node-level operator work is outside certified scope.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-007 — Keep lightweight source provenance without a rights workcell

**Requirement:** Source type, origin reference, allowed-source policy result, generated/retrieved/supplied classification, and transformation lineage must be captured deterministically without a standalone Rights Analyst.

**Consequences (testable):

- Every delivered asset contains provenance metadata sufficient to reconstruct its source class and derivation.

- Missing provenance blocks promotion, but routine production does not enter a manual legal-review lane.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-008 — Authorize Architecture before implementation

**Requirement:** Approval of this PRD permits Architecture work only; implementation begins after the formal Visual Asset Editor Implementation Authorization Gate passes.

**Consequences (testable):

- The readiness receipt identifies the exact evidence, contracts, reference slice, compute proof, evaluators, benchmarks, and Development Capsule used for authorization.

- A PRD-approved but architecture-unvalidated package cannot receive IMPLEMENTATION_AUTHORIZED.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F02 — Visual Asset Demand Contract, Intake, and Authority Validation

**User outcome:** A Content Harness can submit one immutable, typed demand that gives the editor enough authority and constraints to produce the correct asset without relying on conversational context.

## Description

The Visual Asset Demand is the provider-neutral semantic and production boundary between the requesting harness and the editor.

## Brownfield baseline

V2.1 defines an immutable Activative Visual Asset Program and delegation principles, but the new product needs a concrete asynchronous intake, validation, authority, idempotency, and versioning model.

## Required product delta

Define the canonical demand contract, optional notes policy, validation gates, caller registration, immutable versions, references to large media, execution policies, and blocker behavior.

## Traceability

- **Decisions:** D003, D009, D019, D023, D024, D027, D028
- **User journeys:** UJ-01, UJ-03, UJ-12, UJ-14
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-009 — Require a typed Visual Asset Demand

**Requirement:** Every production request must reference a schema-valid, versioned Visual Asset Demand containing asset family, harness role, Activative semantic lineage, Activation Contract, semantic intent, Visual Semantic Pack, Visual Narrative Program, applicable Feature Contracts, T/V somatic route request, Activative function, non-empty wrong-reading locks, composition intent, continuity, delivery, evaluation, and execution-policy fields.

**Consequences (testable):

- Contract validation can enumerate every missing or invalid field before plan compilation.

- Natural-language-only requests are rejected with INVALID_DEMAND.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-010 — Treat notes as non-authoritative enrichment

**Requirement:** Optional notes may explain preferences or context but must be tagged as untrusted enrichment and cannot override typed fields, hard gates, budgets, or authority.

**Consequences (testable):

- A conflict detector reports notes that contradict the typed demand and preserves the typed value.

- A note containing prompt-like instructions cannot alter workflow, tool, or evaluator policy.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-011 — Version demands immutably

**Requirement:** Once accepted for execution, a Visual Asset Demand version is immutable; material changes require a new version with supersession and amendment provenance.

**Consequences (testable):

- Each execution pins one exact demand version and retains it after completion.

- In-place edits to an accepted demand fail contract-authority validation.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-012 — Validate caller identity and delegation authority

**Requirement:** Only registered Content Harnesses, orchestration systems, or authorized operators may submit, cancel, choose high-cost programs, enable experimental capability, accept degradation, or request capability development.

**Consequences (testable):

- Submission receipts record caller identity, scope, and permitted actions.

- An unauthorized action returns a typed authorization failure without starting production.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-013 — Use idempotent submission keys

**Requirement:** The asynchronous service must require or derive an idempotency key from caller, harness, request ID, and demand version.

**Consequences (testable):

- Repeated identical submissions return the existing execution record rather than duplicating GPU work.

- A changed demand with a reused key is rejected as an idempotency conflict.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-014 — Reference large inputs by stable URI and hash

**Requirement:** Images, videos, masks, character references, composition renders, and other large inputs must remain in governed storage and enter contracts through versioned references and content hashes.

**Consequences (testable):

- The intake validator proves referenced objects exist, are readable, and match declared hashes.

- Embedded unbounded media payloads or hash mismatches block acceptance.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-015 — Return a typed submission receipt

**Requirement:** A valid submission must immediately return execution identity, accepted demand version, Budget Program, initial status, estimate class, status resource, and event endpoint information.

**Consequences (testable):

- The caller can begin observing a run without waiting for GPU completion.

- An HTTP success without a durable execution and receipt is nonconformant.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-016 — Block unresolved authority and dependency gaps

**Requirement:** Intake or pre-plan validation must identify missing upstream authority, unavailable required references, unsupported category/profile combinations, and contradictory hard constraints before production resources are committed.

**Consequences (testable):

- The service emits a typed blocker with responsible owner and next action.

- The system may not invent missing semantic or composition values to make a demand executable.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F03 — Canonical Asset Ontology and Reference/Production Separation

**User outcome:** A caller and the editor can describe asset production needs with reusable families while preserving one harness-specific role and Activative purpose.

## Description

This feature defines canonical asset families, subtypes, role bindings, Reference Evidence, Production Assets, and explicit promotion.

## Brownfield baseline

V2.1 distinguishes reference evidence from production assets and defines broad asset responsibilities. The product requires a formal shared ontology that supports routing and evaluation without flattening harness-specific meaning.

## Required product delta

Create a versioned ontology for eight families, extendable subtypes, harness roles, asset classes, typed relationships, promotion rules, and certification scope.

## Traceability

- **Decisions:** D005, D006, D007, D025, D026, D027
- **User journeys:** UJ-01, UJ-03, UJ-09, UJ-14
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-017 — Maintain eight canonical asset families

**Requirement:** The ontology must initially define documentary/photographic evidence, human/character assets, illustrated/generated scenes, UI/screen surfaces, diagrammatic/informational assets, typography/graphic elements, compositing/scene components, and motion/temporal assets.

**Consequences (testable):

- Every demand selects one registered family and compatible subtype.

- Unknown families cannot route to production until governed ontology extension.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-018 — Bind harness-specific roles and Activative functions

**Requirement:** A canonical family record must be combined with a requesting harness role, sequence or scene position, visual-syntax function, and Activative function.

**Consequences (testable):

- Two demands may share an asset family while retaining distinct semantic and composition roles.

- The ontology may not replace or generalize away the harness-specific role.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-019 — Represent Reference Evidence explicitly

**Requirement:** Material used for understanding, conditioning, identity, pose, environment, composition, continuity, evaluation, or inspiration must be stored as Reference Evidence unless explicitly promoted.

**Consequences (testable):

- Reference records state relationships to demands and production plans.

- Reference Evidence cannot be emitted as an authorized final asset by default.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-020 — Represent Production Assets explicitly

**Requirement:** A Production Asset must be an immutable, evaluated artifact authorized for one or more declared downstream uses and linked to its demand, plan, lineage, geometry, and receipts.

**Consequences (testable):

- Downstream composition can verify production authorization from the asset record.

- An unpromoted candidate or reference cannot satisfy an Asset Result Contract.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-021 — Require explicit reference-to-production promotion

**Requirement:** When a reference is reused or transformed into production, the system must record the promotion event, transformation, evaluator results, source policy, and new immutable Production Asset identity.

**Consequences (testable):

- Promotion preserves the original reference record and creates a distinct production lineage.

- Folder movement or filename change alone cannot promote an asset.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-022 — Publish subtype capability requirements

**Requirement:** Each subtype must declare eligible routes, required controls, compatible workflows/models, evaluator dimensions, geometry needs, continuity rules, and delivery types.

**Consequences (testable):

- The router can determine whether certified capabilities exist before plan execution.

- A subtype without capability requirements remains structurally represented but uncertified.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-023 — Version and migrate ontology records

**Requirement:** Asset-family and subtype changes must be versioned, compatibility-scoped, and migration-tested against dependent demands, plans, memory records, and results.

**Consequences (testable):

- Existing assets preserve the ontology version used at production time.

- A taxonomy rename cannot silently reinterpret historical records.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

### FR-024 — Expose certified scope separately from represented scope

**Requirement:** The ontology and UI must mark each family/subtype as represented, experimental, limited-production, production-certified, deprecated, or retired.

**Consequences (testable):

- Release 1 reports Format 02 character-and-scene capabilities as certified scope only after benchmarks pass.

- Structurally defined families cannot be marketed or routed as production-ready.

**Traceability:** Decisions D005, D006, D007, D025, D026, D027; journeys UJ-01, UJ-03, UJ-09, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F04 — Immutable Asset Lifecycle, Lineage, Supersession, and Delivery Variants

**User outcome:** A downstream consumer can always identify the exact accepted master, understand how it was made, and determine whether a newer version supersedes it.

## Description

The asset lifecycle separates reference, planning, candidate, evaluation, repair, acceptance, delivery, consumption, rejection, and supersession states.

## Brownfield baseline

V2.1 defines production asset artifacts, asset memory, usage receipts, and geometry packs. The new system needs an immutable lifecycle across autonomous production and repair.

## Required product delta

Define state transitions, immutable versions, parent/child derivation, master/variant roles, supersession notifications, in-progress invalidation, and historical preservation.

## Traceability

- **Decisions:** D007, D008, D013, D014, D017, D018, D023, D027
- **User journeys:** UJ-01, UJ-04, UJ-07, UJ-09, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-025 — Create immutable asset versions

**Requirement:** Every material candidate, repair, composite, accepted master, or meaningfully changed output must receive an immutable asset ID/version and content hash.

**Consequences (testable):

- A version can be reproduced or audited after later repairs and supersession.

- Overwriting asset bytes under an existing accepted version is prohibited.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-026 — Enforce explicit lifecycle transitions

**Requirement:** Asset state changes must follow registered transitions from Reference Evidence or Resolution Planned through Candidate, Evaluation, Accepted Production Asset, Delivery Variant, and Consumed states, with typed failure states.

**Consequences (testable):

- Illegal transitions are rejected and emitted to the Control Tower.

- A rejected candidate cannot jump directly to accepted without new evaluation.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-027 — Record typed derivation relationships

**Requirement:** Every version must declare parents and relationships such as generated-from, extracted-from, transformed-from, composited-from, targeted-repair-of, delivery-variant-of, or supersedes.

**Consequences (testable):

- Lineage traversal reconstructs all sources and production steps.

- An accepted asset with an orphaned material parent fails promotion.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-028 — Separate accepted masters from delivery variants

**Requirement:** The accepted master is the canonical production asset; deterministic crops, codecs, masks, previews, thumbnails, and profile-specific outputs are immutable variants linked to it.

**Consequences (testable):

- Consumers can request a declared variant without changing master identity.

- A variant cannot silently become the new master.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-029 — Notify downstream consumers of supersession

**Requirement:** When a new accepted version supersedes another, in-progress dependent compositions receive an event and revalidation requirement while published content remains bound to its historical version.

**Consequences (testable):

- The system can list all affected in-progress and completed consumers.

- Supersession may not mutate already-published artifacts automatically.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-030 — Preserve evaluation and production receipts by version

**Requirement:** Each asset version must reference its exact plan, workflow, compute, candidate, geometry, evaluator, repair, budget, and acceptance receipts.

**Consequences (testable):

- A reviewer can prove why one version passed and another failed.

- Receipts from a parent version cannot be reused as acceptance evidence for an altered child without revalidation.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-031 — Support deterministic reuse of valid variants

**Requirement:** Repeated requests for an existing valid delivery profile may return the stored immutable variant when source master, profile version, and dependencies are unchanged.

**Consequences (testable):

- Idempotent variant generation avoids duplicate transformations.

- A profile-version change creates and evaluates a new variant rather than overwriting the old one.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-032 — Expose lifecycle and lineage in the Control Tower

**Requirement:** The supervisory console must render asset state, versions, parents, repairs, accepted master, variants, usage, supersession, and pending invalidations.

**Consequences (testable):

- Operators can navigate from a result contract to every contributing artifact and receipt.

- A lifecycle status shown without authoritative event or record is invalid.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F05 — Composition Intent, Feasibility, and Image-Conditioned Geometry

**User outcome:** A Content Harness can declare where and how an asset must function, and downstream composition receives measured geometry rather than a vague visual suggestion.

## Description

The editor must translate authoritative composition intent into feasible production controls and return image-conditioned geometry without changing the requested syntactic role.

## Brownfield baseline

V2.1 already defines two geometry stages: harness-side BBOX intent plus WHY, followed by editor-side masks, gaze, safe zones, crops, depth, and final BBOX recommendations.

## Required product delta

Formalize Composition Intent, feasibility analysis, tolerance, reserved regions, protected regions, collision simulation, geometry return, conflict handling, and composition-context evaluation.

## Traceability

- **Decisions:** D004, D009, D012, D017, D018, D024
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-033 — Require typed Composition Intent

**Requirement:** Applicable demands must declare canvas profile, intended region, tolerance, layer, visual weight, depth, directional constraints, reserved regions, crop policy, protected regions, and background policy.

**Consequences (testable):

- The plan compiler can map each composition requirement to production and evaluation nodes.

- Ambiguous prose such as 'leave room for text' is insufficient when a typed field exists.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-034 — Run composition-feasibility analysis before expensive production

**Requirement:** The system must test whether subject count, camera distance, gesture, gaze, protected regions, text reservations, and intended BBOX can coexist with available capabilities and budget.

**Consequences (testable):

- Blocking conflicts are detected before full candidate generation when simulation can establish infeasibility.

- The system may not consume the full candidate budget for a geometrically impossible plan.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-035 — Compile composition controls from intent

**Requirement:** The production plan must translate composition intent into masks, regional conditioning, pose/depth/edge controls, camera constraints, background extension, transparency, and workflow-specific bindings as supported.

**Consequences (testable):

- Each compiled control traces to one demand field or feasibility result.

- Provider parameters without a governing composition reason are rejected from the canonical binding.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-036 — Return image-conditioned geometry

**Requirement:** Accepted assets must return detected subject, face, hands, gesture, object, and focal BBOXes; gaze or motion vectors; negative-space regions; safe crops; masks; depth/layer data; and collision results as applicable.

**Consequences (testable):

- Downstream composition can validate fit without rerunning the full production model.

- An asset requiring geometry that lacks the applicable geometry pack cannot be authorized for composition.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-037 — Respect composition tolerance

**Requirement:** The editor may adjust geometry only within declared tolerance or through an internal production method that preserves the requested role and function.

**Consequences (testable):

- The result contract records requested versus realized geometry and tolerance consumption.

- A change outside tolerance triggers a demand amendment proposal rather than silent relocation.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-038 — Evaluate assets in rendered composition context

**Requirement:** The evaluation graph must place candidates in the target scene, slide, or frame with text and neighboring elements before composition-effectiveness approval.

**Consequences (testable):

- Evaluation evidence includes the rendered composition hash and detected collisions or hierarchy outcomes.

- Standalone asset quality cannot substitute for composition-context evaluation.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-039 — Generate deterministic delivery geometry variants

**Requirement:** After master acceptance, the system may derive registered crop, mask, transparency, and canvas variants and return each with inherited geometry and fresh profile validation.

**Consequences (testable):

- Delivery variants retain protected regions and focal visibility.

- A crop that removes the required action or subject evidence fails variant authorization.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-040 — Return typed composition conflicts and recommendations

**Requirement:** When requirements remain infeasible after approved repairs and fallbacks, the system must return conflict evidence and nonbinding geometry or route alternatives to the owning Content Harness.

**Consequences (testable):

- The original demand remains immutable and each option states semantic and Activative impact.

- The editor cannot accept its own out-of-tolerance amendment.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F06 — Governed Multi-Method Resolution and Strategy Routing

**User outcome:** A demand is fulfilled through the simplest reliable route or hybrid route rather than being sent indiscriminately to generation.

## Description

The Resolution Strategy Composer chooses among reuse, retrieve, extract, transform, composite, deterministic construction, generate, animate, and request capture.

## Brownfield baseline

V2.1 allows reuse, research, editing, deterministic assets, requested capture, and grounded generation. The new product must make route selection explicit, budget-aware, benchmarked, and repairable.

## Required product delta

Define route eligibility, route planning, hybrid sequencing, route comparison, fallback, source preparation, route-level receipts, and route-learning evidence.

## Traceability

- **Decisions:** D005, D006, D010, D011, D012, D018, D019, D020
- **User journeys:** UJ-01, UJ-02, UJ-07, UJ-09, UJ-10
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-041 — Register canonical production routes

**Requirement:** The capability registry must define reuse, retrieve, extract, transform, composite, deterministic construction, generate, animate, and request-capture routes with inputs, outputs, eligible families, required capabilities, evaluators, and certification status.

**Consequences (testable):

- The router can validate route eligibility before planning.

- An unregistered route cannot execute in production.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-042 — Select the least complex reliable route

**Requirement:** Strategy selection must rank eligible routes by expected semantic fidelity, Activative effectiveness, composition fit, continuity, feasibility, latency, cost, repairability, and reproducibility.

**Consequences (testable):

- The plan records selected and rejected alternatives with evidence.

- Generation-first selection without comparison fails routing evaluation when a simpler certified route can satisfy the demand.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-043 — Support governed hybrid routes

**Requirement:** A production plan may sequence multiple routes when one route cannot satisfy the demand alone, such as retrieval plus extraction plus transformation plus compositing.

**Consequences (testable):

- Every stage has typed contracts, dependencies, validators, and lineage relationships.

- A hybrid plan cannot hide an unsupported or uncertified stage.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-044 — Prefer governed asset reuse when suitable

**Requirement:** Before acquiring or generating new material, the system must query Visual Asset Memory for semantically, Activatively, compositionally, and continuity-compatible accepted assets and account for contextual recurrence.

**Consequences (testable):

- The reuse decision includes suitability and recurrence evidence.

- Low raw similarity alone cannot exclude a strong syntax-context match, and high similarity alone cannot authorize a poor role match.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-045 — Prepare and validate source/control inputs

**Requirement:** Retrieval, extraction, generation, animation, and compositing routes must normalize references, masks, pose/depth maps, identity inputs, environments, documents, frames, and control assets before downstream execution.

**Consequences (testable):

- Prepared inputs receive hashes, geometry, class, and validation status.

- A production node cannot consume unvalidated or mismatched control inputs.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-046 — Define route-specific fallback policies

**Requirement:** Each route profile must declare fallback routes, compatibility constraints, quality impact, budget impact, and conditions that prohibit fallback.

**Consequences (testable):

- Infrastructure or capability failure can select an approved alternative without changing demand authority.

- A fallback that weakens a hard semantic or composition requirement must return a conflict instead.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-047 — Emit route and strategy receipts

**Requirement:** Every run must preserve route candidates, selected strategy, expected and actual costs, capability bindings, fallbacks used, and reasons for route changes.

**Consequences (testable):

- Control Tower views can explain why a route was chosen and whether it changed during repair.

- An accepted asset without a reconstructable resolution strategy is nonconformant.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-048 — Learn route effectiveness without self-modifying silently

**Requirement:** Cross-run evidence may update routing statistics and propose Steering Recipes or profile changes only through the governed learning lifecycle.

**Consequences (testable):

- The system can compare expected and realized route performance by family and syntax context.

- One successful or failed run cannot rewrite route defaults automatically.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F07 — Dynamic Specialist Workcell and Authority Boundaries

**User outcome:** A demand activates only the analysis and production authorities needed for its actual route while preserving isolated evaluation and deterministic command.

## Description

The workcell compiles from explicit authorities rather than one general visual editor agent or one mandatory fixed chain.

## Brownfield baseline

V2.1 defines seven authority lanes including a Rights Analyst. The new design retains the valuable responsibilities, removes the standalone rights layer, adds autonomous command, and makes activation conditional.

## Required product delta

Define authority manifests, activation rules, typed handoffs, the Asset Commander, specialist boundaries, deterministic policy services, independent evaluation, and no hidden orchestration.

## Traceability

- **Decisions:** D002, D010, D012, D013, D017, D018, D022
- **User journeys:** UJ-02, UJ-05, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-049 — Register specialist authorities

**Requirement:** The product must define Asset Intelligence Hunter, Activative Visual Analyst, Composition Feasibility Analyst, Resolution Strategy Composer, Editor/Materializer, Independent Visual Evaluator, and Asset Commander authority manifests.

**Consequences (testable):

- Each manifest declares owned decisions, inputs, outputs, tools, prohibited decisions, maturity, and evaluation profile.

- A specialist cannot act outside its declared authority.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-050 — Compile the smallest sufficient workcell

**Requirement:** The Asset Commander must activate specialists based on demand, route, capability, evaluation, and repair needs rather than run every specialist for every request.

**Consequences (testable):

- A simple crop may skip research and generation; a new character scene activates the required analysis, plan, production, and evaluation authorities.

- Unnecessary specialist activation is visible in cost and workflow tests.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-051 — Keep semantic interpretation bounded

**Requirement:** The Activative Visual Analyst may translate authorized intent into production-facing visible requirements and failure indicators but may not change the demand.

**Consequences (testable):

- Its output traces each production-facing requirement to a demand field.

- A newly invented subject, message, sequence role, or wrong-reading rule is rejected.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-052 — Keep feasibility analysis measurable

**Requirement:** The Composition Feasibility Analyst must output geometry constraints, conflicts, tolerances, supported controls, and evidence rather than aesthetic preference alone.

**Consequences (testable):

- Its result can be validated against simulation or candidate geometry.

- An unsupported qualitative feasibility conclusion cannot block or redirect production.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-053 — Separate strategy from materialization

**Requirement:** The Resolution Strategy Composer owns the typed route and capability plan; Editor/Materializer nodes execute the approved plan and cannot independently redesign it.

**Consequences (testable):

- Execution receipts prove which plan and bindings were materialized.

- Materializer-side changes beyond permitted runtime variation require a plan amendment.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-054 — Use deterministic policy services for source and registry checks

**Requirement:** Source classification, provenance capture, allowed-source policy, registry compatibility, budget enforcement, contract validation, and lifecycle transitions must be code-owned services rather than reasoning-agent lanes.

**Consequences (testable):

- Policy outcomes are reproducible and independently testable.

- No routine Rights Analyst or manual rights queue appears in the certified workcell.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-055 — Keep evaluation independent from production

**Requirement:** The Independent Visual Evaluator must receive the demand, candidate, composition render, relevant context, and profile without production-model self-approval or unnecessary producer reasoning history.

**Consequences (testable):

- Evaluator identity and profile are pinned in the acceptance receipt.

- A candidate approved only by its producing model is ineligible.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-056 — Make the Asset Commander a workflow authority, not a creative agent

**Requirement:** The Asset Commander controls state, routing, budgets, node validation, evaluation invocation, repair limits, promotion, and escalation but does not perform specialist creative analysis itself.

**Consequences (testable):

- Commander decisions are deterministic or based on typed specialist/evaluator contracts.

- A general-agent Commander that silently combines all roles fails authority-separation tests.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F08 — Visual Capability Registry for Workflows, Models, LoRAs, Controls, and Runtimes

**User outcome:** A production plan can select only capabilities whose purpose, compatibility, quality, cost, and failure behavior are known and tested.

## Description

The registry is the governed discovery and compatibility layer for ComfyUI and other visual production resources.

## Brownfield baseline

V2.1 anticipates provider routing and adapters but does not define the full versioned capability catalog needed for autonomous local-model production.

## Required product delta

Create registry schemas, status and maturity, compatibility edges, benchmark evidence, parameter envelopes, runtime binding, experimental promotion, and change impact.

## Traceability

- **Decisions:** D011, D015, D016, D017, D019, D025, D027
- **User journeys:** UJ-02, UJ-10, UJ-11, UJ-13, UJ-14
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-057 — Register ComfyUI workflow profiles

**Requirement:** Every workflow profile must declare version, status, supported operations and asset families, required controls, compatible models and runtime profiles, geometry features, expected resources, benchmarks, known failures, and compiler adapter.

**Consequences (testable):

- The router can prove a workflow satisfies the plan’s capability requirements.

- Ad hoc workflow JSON cannot run as a production profile.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-058 — Register models, checkpoints, and VAEs

**Requirement:** Model records must pin architecture, hash, supported resolutions and operations, compatible text encoders/VAEs/workflows, VRAM, strengths, weaknesses, licensing/source policy class, benchmarks, and certified scope.

**Consequences (testable):

- Production binding fails when a required model relationship is incompatible.

- A filename alone cannot identify a production model.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-059 — Register LoRAs and adapters

**Requirement:** LoRA and adapter records must define base-model compatibility, intended capabilities, strength envelope, prohibited combinations, known failures, benchmark evidence, training provenance, and maturity.

**Consequences (testable):

- The compiler validates every stack and strength before execution.

- An experimental or incompatible LoRA cannot silently enter a production run.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-060 — Register conditioning and control profiles

**Requirement:** ControlNet, IP-Adapter, pose, depth, edge, mask, identity, regional prompting, camera, motion, and other controls must declare required inputs, applicable workflows, controllability, limits, and evaluator requirements.

**Consequences (testable):

- Plans can request capabilities independent of provider-specific node names.

- A missing control dependency creates a capability blocker rather than best-effort improvisation.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-061 — Register compute runtime profiles

**Requirement:** Runtime profiles must pin container digest, ComfyUI and Python/CUDA compatibility, custom-node lockfile, hardware class, model mounts, API, health checks, concurrency, timeouts, cache behavior, and certification.

**Consequences (testable):

- The scheduler chooses only profiles compatible with every bound capability.

- A worker with an unregistered environment cannot receive production jobs.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-062 — Maintain typed compatibility relationships

**Requirement:** The registry must model requires, compatible-with, conflicts-with, supersedes, validated-on, and prohibited-with relationships across workflows, models, VAEs, LoRAs, controls, nodes, evaluators, and runtimes.

**Consequences (testable):

- Registry validation catches broken or cyclic mandatory dependencies.

- Compatibility cannot be inferred only from names or human memory.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-063 — Promote capabilities through maturity states

**Requirement:** New or changed capabilities must move through experimental, benchmarked, shadow, limited-production, production, deprecated, and retired states with evidence and rollback.

**Consequences (testable):

- Production routing excludes capabilities below the requested policy level.

- Registry edits cannot change an active run’s pinned bindings.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-064 — Expose capability evidence and change impact

**Requirement:** The Control Tower and architecture tools must show benchmark results, cost and latency envelopes, known limitations, dependent plans/harnesses, and required regression suites for each capability.

**Consequences (testable):

- A proposed registry update calculates its blast radius before promotion.

- A capability with unknown dependent certified paths cannot be removed.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F09 — Visual Production Plan IR and Provider-Specific Compilation

**User outcome:** A validated demand becomes one inspectable, provider-neutral execution specification before ComfyUI or any other provider receives work.

## Description

The Visual Production Plan IR is the canonical production plan, while provider graphs and API payloads are compiled artifacts.

## Brownfield baseline

V2.1 defines asset demand and resolution concepts, but not a canonical plan that separates product authority from ComfyUI graph structure.

## Required product delta

Define plan identity, objectives, route stages, capability requirements, constraints, preservation/mutability, evaluation, budget, fallbacks, provider compilation, and plan versioning.

## Traceability

- **Decisions:** D003, D005, D009, D011, D012, D013, D018, D019, D024
- **User journeys:** UJ-01, UJ-02, UJ-03, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-065 — Compile every accepted demand into a Visual Production Plan

**Requirement:** Before provider execution, the service must create a schema-valid, versioned plan referencing the exact demand, objective, route, stages, inputs, outputs, capabilities, budgets, evaluations, fallbacks, and delivery requirements.

**Consequences (testable):

- Every execution node traces to one plan node and one authoritative need.

- Direct demand-to-ComfyUI execution without a canonical plan is prohibited.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-066 — Declare preservation and mutable bindings

**Requirement:** The plan must separate fields and properties that must be preserved from provider bindings, candidate variables, and repair variables that may change.

**Consequences (testable):

- Repair validation can prove no protected property was altered.

- A binding not declared mutable cannot be changed by generation or repair.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-067 — Model typed stages and dependencies

**Requirement:** Plan stages must declare actor/executor class, dependencies, contracts, checkpoints, expected artifacts, validators, invalidation, and eligible parallelism.

**Consequences (testable):

- The plan graph validator identifies orphan outputs, unavailable capabilities, illegal cycles, and unsatisfied dependencies.

- A stage lacking an output contract cannot unlock downstream work.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-068 — Express capability requirements provider-neutrally

**Requirement:** Plans must request functions such as identity conditioning, pose control, regional conditioning, inpainting, transparent extraction, or temporal consistency rather than hard-code ComfyUI node IDs as product requirements.

**Consequences (testable):

- Capability resolution can bind a different certified provider without changing plan meaning.

- Provider-specific terminology cannot become the sole canonical representation.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-069 — Compile deterministic provider graphs

**Requirement:** A versioned compiler must bind approved workflows, models, LoRAs, controls, runtimes, parameters, inputs, and output paths into ComfyUI JSON or another provider payload.

**Consequences (testable):

- The provider artifact includes a source plan hash and compiler version.

- Manual runtime graph editing invalidates the compiled identity unless captured as a new governed profile.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-070 — Compile evaluation and repair subgraphs

**Requirement:** The plan compiler must generate the required deterministic validation, VLM evaluation, composition simulation, recurrence/continuity comparison, repair, and delivery nodes alongside production.

**Consequences (testable):

- The execution graph contains every acceptance hard gate before promotion.

- A production graph that omits the applicable evaluator cannot be certified.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-071 — Version and amend plans without mutating demands

**Requirement:** Internal route, workflow, model, control, or runtime changes permitted by the demand create a new plan version with reason and impact while preserving the demand version.

**Consequences (testable):

- Valid prior outputs are reused when dependency analysis allows.

- Demand-authority changes cannot be disguised as plan revisions.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-072 — Preserve plan-to-execution reproducibility

**Requirement:** The service must retain the plan, compiled graphs, compiler identities, bindings, input hashes, events, outputs, and receipts needed to reproduce or audit the run.

**Consequences (testable):

- A dry-run can validate plan capability and budget without GPU execution.

- An accepted asset whose executed graph cannot be reconciled with its plan fails traceability.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F10 — Event-Sourced, Resumable Visual Production Runtime

**User outcome:** A long-running visual job can execute, fail, recover, repair, and complete without losing state or replaying unrelated expensive work.

## Description

The runtime specializes the validated Builder Workflow Runtime for visual production and separates deterministic, model, VLM, compute, delivery, and human-exception nodes.

## Brownfield baseline

V2.1 has deterministic CLI lifecycle and receipts; the new editor requires asynchronous GPU jobs, production graphs, queueing, checkpoints, events, and infrastructure recovery.

## Required product delta

Define node schema, scheduler, events, checkpoint/resume, infrastructure/quality separation, timeouts, retries, cancellation, parallelism, isolation, and terminal states.

## Traceability

- **Decisions:** D013, D015, D017, D018, D019, D021, D023, D027
- **User journeys:** UJ-02, UJ-05, UJ-07, UJ-08, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-073 — Execute typed production nodes

**Requirement:** Every runtime node must declare actor type, inputs, outputs, dependencies, validations, timeout, infrastructure retries, checkpoint behavior, invalidation, event types, and eligible runtime profiles.

**Consequences (testable):

- The scheduler refuses incomplete node definitions.

- An opaque long-running job without typed stages is outside certified scope.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-074 — Persist an append-only production event stream

**Requirement:** The runtime must emit ordered typed events for plan compilation, queueing, node start/completion/failure, candidate creation, evaluation, repair, promotion, packaging, cancellation, and exceptions.

**Consequences (testable):

- Run state can be reconstructed from authoritative events plus immutable artifacts.

- A UI-only status change without an event is invalid.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-075 — Checkpoint successful nodes

**Requirement:** Committed node inputs, outputs, bindings, validation receipts, side effects, and dependency versions must be checkpointed for resume and targeted repair.

**Consequences (testable):

- An interrupted run resumes from the first invalid or incomplete node.

- Successful retrieval, control preparation, or deterministic transforms are not repeated without invalidation.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-076 — Separate infrastructure retries from quality repairs

**Requirement:** Container crashes, GPU loss, network timeout, cache corruption, or provider unavailability must use operational retry/fallback policies independent of the three VLM-directed quality rounds.

**Consequences (testable):

- Receipts report infrastructure attempts and quality rounds separately.

- An infrastructure failure cannot consume or reset the quality-repair count.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-077 — Enforce bounded timeouts, retries, and circuit breakers

**Requirement:** Each node/profile must declare timeout, retryable and non-retryable failures, maximum operational attempts, backoff, fallback, and circuit-breaker behavior.

**Consequences (testable):

- Exhaustion produces a typed terminal or exception state with preserved evidence.

- The runtime cannot loop indefinitely on an unavailable provider or recurring error.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-078 — Run dependency-safe bounded parallelism

**Requirement:** The scheduler may parallelize independent input preparation, candidate production, evaluation, or delivery work only within Budget Program concurrency and shared-resource constraints.

**Consequences (testable):

- Cancellation and failure of one branch do not corrupt valid siblings.

- Parallel nodes with shared mutable state are rejected unless an explicit merge protocol exists.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-079 — Support governed cancellation and backpressure

**Requirement:** Authorized callers may cancel non-promoted work; the service may communicate capacity, queue, and estimated-delay states without lowering quality gates.

**Consequences (testable):

- Cancellation preserves events, created artifacts, learning evidence, and cost receipts.

- Backpressure cannot silently switch to uncertified or degraded production.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-080 — Define explicit terminal states

**Requirement:** Runs must end in COMPLETED, INVALID_DEMAND, CAPABILITY_GAP, COST_APPROVAL_REQUIRED, HUMAN_REVIEW_REQUIRED, DEPENDENCY_UNAVAILABLE, PRODUCTION_FAILED, CANCELLED, or another registered terminal state.

**Consequences (testable):

- Every terminal state has required evidence, owner, and allowed next action.

- A stalled run cannot remain indefinitely in a nonterminal status without heartbeat or escalation.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F11 — Visual Asset Memory, Syntax-Aware Reuse, and Contextual Recurrence

**User outcome:** A new demand can reuse prior assets and lessons intelligently without confusing repetition with failure or continuity with fatigue.

## Description

Memory stores immutable assets and rendered usage context, then retrieves through semantic, composition, continuity, syntax, and recurrence criteria.

## Brownfield baseline

V2.1 includes asset memory, usage receipts, fatigue records, and geometry; the new design adds VLM comparison of rendered Visual Syntax contexts and governed reuse scoring.

## Required product delta

Define memory records, usage receipts, contextual embeddings, recurrence labels, retrieval scoring, continuity, supersession, syntax fingerprints, and feedback to planning.

## Traceability

- **Decisions:** D006, D008, D009, D014, D017, D020, D021
- **User journeys:** UJ-03, UJ-04, UJ-09, UJ-15
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-081 — Store rich Visual Asset Memory records

**Requirement:** Accepted assets must be indexed by family/subtype, semantic roles, Activative functions, identities, environments, palette, expression, pose, geometry, production, evaluation, lineage, lifecycle, and certified uses.

**Consequences (testable):

- The memory record can answer both production and composition suitability questions.

- A generic embedding-only asset record is insufficient.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-082 — Create one Visual Usage Receipt per rendered use

**Requirement:** Every composition use must record asset version, harness, category, format profile, scene/slide, sequence position, syntactic role, composition function, BBOX/layer, neighboring elements, Activative function, transformation, recurrence intent, and rendered-context reference.

**Consequences (testable):

- The exact rendered use is inspectable independently of the source asset.

- Usage count without context cannot drive fatigue decisions.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-083 — Generate syntax-context fingerprints

**Requirement:** The system must derive comparable representations from the Visual Syntax Parse, composition geometry, neighboring relationships, recurrence intent, and rendered appearance for each use.

**Consequences (testable):

- Retrieval and recurrence evaluation can compare different files that express the same visual pattern.

- File identity alone cannot represent contextual similarity.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-084 — Classify recurrence contextually with a VLM

**Requirement:** Recurrence must be labeled beneficial recurrence, neutral reuse, productive variation, redundant repetition, fatiguing pattern, or contradictory recurrence using rendered context and sequence function.

**Consequences (testable):

- The VLM provides evidence and comparison references for its verdict.

- Previous usage frequency cannot automatically reject a candidate.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-085 — Retrieve assets through constraint-aware suitability

**Requirement:** Reuse ranking must combine semantic, Activative, composition, geometry, identity/continuity, syntax-role, transformation feasibility, quality, lifecycle, and recurrence signals.

**Consequences (testable):

- The result explains inclusion, exclusions, recommended route, and any transformation required.

- High visual similarity cannot compensate for wrong role or continuity.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-086 — Prioritize valid reuse before new production

**Requirement:** The Resolution Strategy Composer must evaluate exact reuse, deterministic variant, transformation, and composite reuse before new acquisition or generation when they can meet the demand.

**Consequences (testable):

- The plan records why reuse passed or failed.

- New generation without a memory query is nonconformant for asset families with memory enabled.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-087 — Preserve continuity without creating false fatigue

**Requirement:** Character identity, visual world, persistent format instruments, and deliberate motifs may repeat when the current syntax context and sequence purpose justify recurrence.

**Consequences (testable):

- Continuity-positive recurrence can be exempted from raw-frequency penalties through explicit evidence.

- A model that penalizes required character identity repetition fails recurrence benchmarks.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-088 — Invalidate or warn on superseded memory

**Requirement:** Superseded, regressed, deprecated, or contextually unsafe assets and recipes must be excluded or penalized according to lifecycle policy, and affected in-progress uses must revalidate.

**Consequences (testable):

- Historical use remains visible with the version that was actually consumed.

- A superseded asset cannot be returned as current production-ready without an explicit compatibility exception.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F12 — Hybrid Containerized Visual Compute Fabric

**User outcome:** A production plan can run reproducibly on compatible local or cloud compute without dependency drift or operator-managed GPU sessions.

## Description

The compute fabric schedules immutable runtime profiles, model mounts, caches, jobs, health, artifacts, and failover across approved worker classes.

## Brownfield baseline

Current bundles describe provider routing but do not supply the product requirements for ComfyUI containers, GPU APIs, custom-node locks, local/cloud parity, autoscaling, and queue operations.

## Required product delta

Define runtime profiles, scheduler inputs, containers, model storage, API job control, health, isolation, caching, local/cloud execution, external fallback, telemetry, and recovery.

## Traceability

- **Decisions:** D011, D013, D015, D019, D021, D023, D025, D027
- **User journeys:** UJ-02, UJ-05, UJ-08, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005

## Functional Requirements

### FR-089 — Support a hybrid compute pool

**Requirement:** The scheduler must support certified local workstation GPUs, self-hosted GPU servers, cloud GPU instances, autoscaled temporary workers, and approved external providers through common job contracts.

**Consequences (testable):

- The plan can route according to capability, policy, queue, cost, and availability.

- No single permanent ComfyUI server is required as a product assumption.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-090 — Use immutable container runtime profiles

**Requirement:** Self-hosted jobs must run from digest-pinned OCI images containing approved ComfyUI, Python/CUDA, custom-node lockfile, compiler adapter, API executor, health probes, and telemetry agent.

**Consequences (testable):

- Execution receipts identify the exact image and environment.

- Mutable in-place package installation on a production worker invalidates certification.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-091 — Manage models and LoRAs as versioned mounted resources

**Requirement:** Weights must be hash-verified, registered, mounted or cached separately from container images, and associated with storage, compatibility, and eviction policy.

**Consequences (testable):

- The scheduler confirms every required weight is available or transferable before job start.

- Unverified model files cannot be loaded by production workers.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-092 — Expose a uniform asynchronous worker API

**Requirement:** Certified worker adapters must support submit, status, heartbeat/progress, cancel, result retrieval, logs/receipts, and failure classification.

**Consequences (testable):

- The runtime can replace one compatible worker without changing the canonical plan.

- A worker requiring manual desktop interaction is outside autonomous production scope.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-093 — Route by capability and expected value

**Requirement:** Scheduling must consider workflow/model/control requirements, VRAM, GPU class, queue delay, warm model cache, data locality, expected runtime, cost, privacy policy, maturity, and fallback.

**Consequences (testable):

- The selected runtime and alternatives are preserved in the plan receipt.

- Fastest-available routing cannot bypass compatibility or certification.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-094 — Enforce worker and job isolation

**Requirement:** Jobs must not mutate canonical workflows, model weights, accepted assets, registry state, other jobs, or authoritative demands; experimental custom nodes run in isolated profiles.

**Consequences (testable):

- Fault-injection tests prove cross-job and registry containment.

- A compromised or failed worker can be quarantined without corrupting stored artifacts.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-095 — Recover from worker and provider failure

**Requirement:** The fabric must detect missed heartbeats, container crashes, unavailable GPUs, corrupted caches, API timeouts, and partial uploads, then retry or fail over according to profile policy.

**Consequences (testable):

- Recovery resumes from committed workflow checkpoints and preserves quality-round counts.

- The operator is not required to restart routine failed jobs.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-096 — Prove local and cloud reference execution

**Requirement:** Implementation authorization requires one self-hosted/local and one cloud container profile to execute representative Format 02 workflows with equivalent contracts, receipts, recovery, and benchmark behavior.

**Consequences (testable):

- The proof pins hardware, image, nodes, weights, workflow, and results.

- Architecture cannot claim a hybrid fabric based only on design documents.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F13 — Governed LoRA, Adapter, Control, and Workflow Capability Development

**User outcome:** A recurring production gap can become a reusable, tested capability without training new resources for every difficult request.

## Description

Capability development is a separate evidence-driven workflow for reusable visual gaps, not an automatic fallback inside ordinary production.

## Brownfield baseline

Legacy University material anticipated LoRA and local-model work, while the current Builder architecture defines capability ownership and maturity. The Visual Editor PRD must connect those principles to production evidence and registry promotion.

## Required product delta

Define gap qualification, evidence sufficiency, dataset contracts, sandboxed training, baseline comparisons, evaluator coverage, contamination/regression tests, shadow use, promotion, rollback, and cost authorization.

## Traceability

- **Decisions:** D016, D019, D020, D025, D026, D027, D028
- **User journeys:** UJ-10, UJ-11, UJ-13, UJ-16
- **Cross-cutting NFRs:** NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-097 — Detect reusable capability gaps

**Requirement:** A gap may be proposed only when representative demands or repeated repairs show an unmet recurring identity, character, environment, visual-language, pose, motion, control, workflow, or evaluator capability.

**Consequences (testable):

- The proposal includes failed certified alternatives, expected reuse, and affected syntax contexts.

- One unattractive candidate or ordinary stochastic failure cannot trigger training.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-098 — Require evidence-sufficiency analysis

**Requirement:** Before training or adaptation, the system must assess reference count, diversity, quality, identity consistency, captions, rights/source policy class, duplicates, exclusions, and coverage of intended conditions.

**Consequences (testable):

- Insufficient evidence produces a typed blocker and collection plan.

- Training cannot begin from an undocumented or contradictory dataset.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-099 — Compile a typed Capability Development Plan

**Requirement:** The plan must declare capability goal, target base, dataset contract, preprocessing, training method, hyperparameter search, compute budget, baseline, evaluation profiles, promotion path, rollback, and prohibited use.

**Consequences (testable):

- Every training job traces to the approved plan.

- Ad hoc notebook training cannot create a registry-eligible production capability.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-100 — Prepare datasets in isolated, reproducible pipelines

**Requirement:** Dataset normalization, deduplication, captioning, cropping, quality inspection, train/validation splits, and manifests must execute in versioned sandboxes with immutable source references.

**Consequences (testable):

- The exact training dataset can be reconstructed and diffed.

- Untracked manual dataset edits invalidate the training receipt.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-101 — Benchmark against relevant controls

**Requirement:** New LoRAs, adapters, controls, workflows, or model adaptations must be compared with base model, current registered controls, existing stacks, and other credible alternatives on representative demands and syntax contexts.

**Consequences (testable):

- The benchmark measures intended improvement, responsiveness, diversity, overfitting, contamination, composition control, cost, latency, and regressions.

- A capability cannot be promoted solely from showcase outputs.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-102 — Detect contamination and compatibility regressions

**Requirement:** Evaluation must test identity drift, style leakage, prompt insensitivity, forbidden combinations, base-model incompatibility, unwanted memorization, composition degradation, and failure outside declared applicability.

**Consequences (testable):

- Critical regression blocks promotion and is linked to evidence.

- A capability that improves one target while breaking certified shared behavior cannot enter production silently.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-103 — Use staged registry promotion

**Requirement:** Successful capability candidates must move through experimental, benchmarked, shadow, limited-production, and production states with pinned versions and approved applicability.

**Consequences (testable):

- Shadow decisions are compared against the current baseline without controlling accepted assets.

- An experimental LoRA cannot be selected under production-only policy.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-104 — Preserve rollback and deprecation

**Requirement:** Every promoted capability must retain its predecessor, migration/compatibility notes, dependent paths, rollback procedure, and retirement criteria.

**Consequences (testable):

- A production regression can revert routing to the preceding certified version without losing run reproducibility.

- Deleting or replacing the only copy of a capability used by historical assets is prohibited.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F14 — Visual Evaluation Profiles and Independent VLM Quality System

**User outcome:** A candidate is judged against the right family, composition, syntax, continuity, and temporal criteria rather than by a universal aesthetic score.

## Description

Evaluation profiles compile deterministic checks and independent VLM programs into a typed, versioned acceptance system.

## Brownfield baseline

V2.1 defines evaluation and readiness but not the required multimodal product, composition, recurrence, temporal, and evaluator-certification system.

## Required product delta

Define evaluation profile registry, deterministic validation, asset/composition/syntax/temporal VLM programs, failure taxonomy, evidence regions, hard gates, confidence, arbitration, profile versioning, and evaluator benchmarks.

## Traceability

- **Decisions:** D004, D010, D017, D018, D020, D025, D027
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-09, UJ-13
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-105 — Register asset-family-aware evaluation profiles

**Requirement:** Each certified asset family, subtype, route, and composition context must map to an evaluation profile declaring deterministic validators, VLM programs, required contexts, dimensions, thresholds, hard gates, failure codes, repair mappings, and applicability.

**Consequences (testable):

- The plan compiler selects the exact profile before candidate production.

- A universal unversioned evaluator cannot approve every asset class.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-106 — Run deterministic technical validation first

**Requirement:** Code-owned validators must check file integrity, dimensions, aspect ratio, duration/frame rate, codec, alpha, masks, blank/corrupt output, metadata, receipt completeness, and budget before semantic evaluation.

**Consequences (testable):

- Technical failures are localized without spending VLM evaluation unnecessarily.

- A candidate failing a technical hard gate cannot be promoted by VLM preference.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-107 — Run independent asset-level VLM evaluation

**Requirement:** The evaluator must compare the isolated candidate with required subject, action, expression, pose, gesture, gaze, identity, environment, visual properties, semantic intent, Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, somatic route, wrong-reading locks, and artifact quality.

**Consequences (testable):

- Failures include evidence regions/time ranges and calibrated confidence.

- The producing model’s self-description cannot substitute for independent inspection.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-108 — Run composition-level VLM evaluation

**Requirement:** Applicable candidates must be rendered inside their intended BBOX, layers, text reservations, neighboring elements, sequence role, and feed/viewing profile before composition-effectiveness approval.

**Consequences (testable):

- Evaluation checks hierarchy, focal visibility, negative space, crop safety, gaze/motion direction, collision, zero-second hook, pattern matching, pattern interruption, viewer-role progression, prediction gap, payoff, affinity, anticipation residue, anti-cliché strength, no-text survival where applicable, and Activative function.

- Standalone beauty or correctness cannot compensate for a failed composed use.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-109 — Run syntax-aware recurrence and continuity evaluation

**Requirement:** The evaluator must compare the candidate’s proposed rendered use against relevant Visual Usage Receipts, syntax fingerprints, identities, environments, sequence roles, and recurrence intent.

**Consequences (testable):

- It classifies recurrence and explains whether continuity or progression is helped or harmed.

- Raw usage frequency cannot be the sole fatigue signal.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-110 — Run temporal evaluation where applicable

**Requirement:** Motion and video profiles must evaluate frame-to-frame identity, motion, gesture completion, camera continuity, flicker, artifacts, loop integrity, duration, and timing against sequence purpose.

**Consequences (testable):

- Temporal failures include time ranges and responsible production layers.

- A passing first frame cannot approve a failing animation.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-111 — Synthesize verdicts with hard-gate precedence

**Requirement:** The evaluation contract must preserve per-layer verdicts, dimensions, evidence, failure codes, repair owner, and confidence; acceptance requires all applicable hard gates.

**Consequences (testable):

- Weighted rankings are calculated only among eligible passing candidates.

- High technical or aesthetic scores cannot hide a failed semantic, Activative, role, wrong-reading, feature-contract, visual-narrative, no-text, or composition gate.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-112 — Certify evaluator versions independently

**Requirement:** VLM programs and threshold profiles must pass labeled accepted/rejected/borderline, recurrence, temporal, responsible-layer, and repair usefulness benchmarks before shadow and production promotion.

**Consequences (testable):

- Acceptance receipts pin evaluator model, program, profile, thresholds, and context hashes.

- A newer model version cannot replace the production evaluator without regression evidence.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F15 — Typed Visual Repair, Invalidation, and Bounded Reruns

**User outcome:** A failed candidate can be corrected surgically while identity, composition, environment, and other successful properties remain stable.

## Description

The VLM emits causal repair contracts; the runtime changes only permitted bindings and reruns the smallest invalidated graph region.

## Brownfield baseline

V2.1 includes repair doctrine and amendment requests; the new product needs concrete failure ownership across generation controls, deterministic edits, workflows, models, evaluation, and demand conflicts.

## Required product delta

Define failure taxonomy, repair contracts, preservation, mutable/prohibited bindings, invalidation, repair hierarchy, three-round policy, causal-change proof, learning, and escalation.

## Traceability

- **Decisions:** D002, D013, D017, D018, D020, D024
- **User journeys:** UJ-07, UJ-08, UJ-10, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-113 — Emit a typed repair contract for every quality rerun

**Requirement:** The evaluator must identify failure code, severity, evidence region/time range, responsible layer, preserved properties, permitted and prohibited changes, invalidated nodes, reusable outputs, expected correction evidence, and repair round.

**Consequences (testable):

- The runtime can validate the repair before applying it.

- Free-form 'try again' instructions cannot trigger a quality rerun.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-114 — Preserve successful properties explicitly

**Requirement:** Repair plans must freeze all accepted identities, expressions, geometry, palette, environment, text-safe regions, continuity, and semantic properties not responsible for the failure.

**Consequences (testable):

- Post-repair evaluation compares preserved properties with the parent candidate.

- A repair that fixes one failure by drifting a preserved property is rejected.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-115 — Apply the least disruptive repair hierarchy

**Requirement:** The system must prefer deterministic correction, then parameter correction, conditioning correction, workflow/capability substitution, and finally approved resolution-strategy amendment according to the failure and plan.

**Consequences (testable):

- The selected level and rejected lower levels are receipted.

- A full regeneration cannot be the default when a deterministic or local repair can resolve the issue.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-116 — Require causal production changes

**Requirement:** Every quality rerun must modify at least one binding or execution route plausibly responsible for the diagnosed failure, except evaluator-authorized stochastic seed exploration.

**Consequences (testable):

- The repair receipt records old and new values and causal hypothesis.

- Repeated identical bindings with only an unexplained new seed fail the blind-retry guard.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-117 — Rerun only invalidated nodes

**Requirement:** The Repair and Invalidation Graph must preserve valid references, masks, controls, background plates, runtime bindings, and deterministic transformations while rescheduling affected production and evaluation nodes.

**Consequences (testable):

- Repair cost and time reflect the reduced graph region.

- Unrelated expensive stages cannot be replayed without dependency invalidation.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-118 — Enforce three quality-repair rounds

**Requirement:** The system may perform at most three VLM-directed quality rounds: local correction, strengthened/substituted controls, and approved fallback route or strategy.

**Consequences (testable):

- Round exhaustion emits HUMAN_REVIEW_REQUIRED or CAPABILITY_GAP with the best evidence and attempts.

- A fourth autonomous quality round is constitutionally blocked.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-119 — Separate repair from demand amendment

**Requirement:** Repairs may use only mutable plan bindings and internal production alternatives authorized by the accepted demand; semantic or out-of-tolerance changes must become amendment proposals.

**Consequences (testable):

- The repair validator rejects prohibited field changes.

- An evaluator cannot lower a quality threshold to declare its repair successful.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-120 — Capture repair effectiveness for steering and regression

**Requirement:** Every repair must record failure context, syntax role, changed bindings, cost, latency, outcome, preserved-property regressions, and candidate/evaluator versions for later Steering Recipe and registry analysis.

**Consequences (testable):

- Repeated failure patterns can trigger routing warnings or capability-gap proposals.

- Learning evidence cannot directly mutate production defaults.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F16 — Budget Programs, Candidate Portfolios, and Quality-First Selection

**User outcome:** Operators and callers can choose how much exploration, learning, cost, and latency a demand receives without weakening quality authority.

## Description

Budget Programs configure candidate counts, parallelism, repair limits, workflow variation, evaluator depth, experimentation, and cost/time ceilings.

## Brownfield baseline

The current architecture has cost profiles but not a product-level menu connecting compute budgets to candidate portfolio design and controlled learning.

## Required product delta

Define six programs, custom policies, estimates, portfolio classes, controlled variation, quality-first selection, early stop, adaptive expansion, cost receipts, and authorization.

## Traceability

- **Decisions:** D002, D019, D020, D021, D022, D025
- **User journeys:** UJ-02, UJ-05, UJ-06, UJ-10
- **Cross-cutting NFRs:** NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-121 — Register six Budget Programs

**Requirement:** The product must define Lean, Standard, Premium, Exploration, Capability Learning, and Custom programs with candidate, parallelism, workflow diversity, evaluator, repair, time, cost, and learning semantics.

**Consequences (testable):

- Each run pins one program version in its plan and receipt.

- A raw GPU setting without program semantics cannot be selected as the primary policy.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-122 — Expose program selection in the supervisory menu

**Requirement:** Authorized operators and callers must be able to select an eligible Budget Program and see expected cost, latency, candidate count, evaluator depth, experimental scope, and learning outputs before execution.

**Consequences (testable):

- The UI distinguishes production and learning budgets.

- High-cost or experimental programs require the caller authority defined by policy.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-123 — Compile bounded candidate portfolios

**Requirement:** Each plan must declare initial and maximum candidates, maximum parallel jobs, exploration dimensions, fixed properties, candidate classes, selection policy, and budget ceilings.

**Consequences (testable):

- The scheduler cannot exceed portfolio or Budget Program limits.

- Candidate generation without declared purpose or limit is prohibited.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-124 — Use controlled variation for exploration

**Requirement:** Exploration and Capability Learning portfolios must vary declared factors while preserving comparable baselines, fixed variables, hypothesis, and measurement plan.

**Consequences (testable):

- The system can attribute quality differences to tested interventions.

- Indiscriminate random prompt/seed sweeps do not qualify as learning evidence.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-125 — Filter hard-gate failures before ranking

**Requirement:** Every candidate must pass technical, semantic, Activative, composition, and applicable continuity/temporal hard gates before quality/cost/latency ranking.

**Consequences (testable):

- Ineligible candidates remain available for diagnosis but cannot win.

- The first completed candidate or highest aesthetic score cannot override failed gates.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-126 — Select the best validated candidate within budget

**Requirement:** Among eligible candidates, the selector must use the registered ranking profile across fidelity, effectiveness, continuity, distinctiveness, technical quality, editability, repair risk, cost, and latency.

**Consequences (testable):

- The selected candidate and credible alternatives are receipted.

- Completion speed is only a declared constraint or tie-breaker, never the sole winner criterion.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-127 — Support adaptive expansion and early stopping

**Requirement:** The portfolio may expand when evidence shows valuable unresolved uncertainty and may stop when a passing candidate exceeds high-confidence thresholds and further expected value is low.

**Consequences (testable):

- Expansion and early stop decisions include evaluator evidence and remaining budget.

- The system cannot exhaust a high budget automatically when a strong accepted asset already exists.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-128 — Emit complete budget and portfolio receipts

**Requirement:** Each run must report estimated versus actual cost/time, GPU seconds, candidates created/evaluated/passing, parallelism, repairs, early stopping, selected asset, and learning artifacts.

**Consequences (testable):

- Operators can compare quality gain per additional cost across programs.

- Hidden candidate or evaluator cost fails cost-governance validation.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F17 — Visual Steering Intelligence, CMF-OKF Knowledge, and Smart Retrieval

**User outcome:** A production or repair node receives the smallest authoritative memory that matches its demand, Visual Syntax context, capability, and failure rather than scanning a generic archive.

## Description

The product converts validated production evidence into governed Steering Recipes and publishes durable knowledge through a stricter CMF-OKF profile while canonical state remains typed and transactional.

## Brownfield baseline

OKF offers portable Markdown/frontmatter, progressive disclosure, and graph links, but it is intentionally minimally opinionated. CMF requires typed authority, lifecycle, compatibility, retrieval facets, evidence, and operational references layered above it.

## Required product delta

Define Steering Recipe lifecycle, CMF-OKF profile, concept projection, indexes, authority filters, typed edges, hybrid multimodal retrieval, VLM reranking, contradiction coverage, Minimum Complete Context, and no silent self-modification.

## Traceability

- **Decisions:** D014, D019, D020, D021, D027
- **User journeys:** UJ-09, UJ-10, UJ-15
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-129 — Capture steering evidence from production

**Requirement:** Candidate portfolios, evaluations, repairs, syntax contexts, bindings, costs, and final outcomes must produce structured evidence suitable for recurring pattern analysis.

**Consequences (testable):

- Evidence distinguishes correlation, controlled comparison, and validated intervention.

- Raw winning prompts cannot be promoted directly as production knowledge.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-130 — Compile versioned Visual Steering Recipes

**Requirement:** A Steering Recipe must define applicability, failure/success pattern, compatible workflows and assets, intervention, preserved properties, evidence, observed runs, control comparison, regression cases, cost effect, lifecycle, and authority.

**Consequences (testable):

- Recipes are independently inspectable and benchmarkable.

- A recipe without applicability boundaries cannot enter shadow routing.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-131 — Promote recipes through governed learning states

**Requirement:** Recipes must move through proposed, experimental, validated, shadow, limited-production, production, deprecated, and retired states with minimum evidence and rollback.

**Consequences (testable):

- Production routing uses only policy-eligible recipe states.

- A single successful run cannot alter defaults.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-132 — Publish durable knowledge through CMF-OKF

**Requirement:** The product must project selected workflows, models, LoRAs, failure patterns, repair patterns, Steering Recipes, syntax usage contexts, benchmarks, and operator knowledge into OKF-compatible Markdown with CMF frontmatter extensions.

**Consequences (testable):

- Concepts remain readable, version-controllable, portable, and linked to canonical records.

- OKF documents cannot become the authoritative lifecycle or execution store.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-133 — Define typed CMF knowledge relationships

**Requirement:** CMF-OKF concepts and the retrieval graph must support explicit edges such as derived-from, validated-by, compatible-with, contradicts, supersedes, repairs, failed-under, applies-to, observed-in, consumed-by, and shares-syntax-with.

**Consequences (testable):

- Graph traversal can distinguish evidence, compatibility, contradiction, and succession.

- Untyped prose links alone cannot govern production retrieval.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-134 — Apply authority and compatibility filters before similarity search

**Requirement:** Retrieval must first filter by lifecycle, authority, category, format, asset family, syntax role, Activative function, failure code, workflow/model compatibility, validity, and current demand constraints.

**Consequences (testable):

- Incompatible or superseded concepts are excluded or marked explicitly.

- Semantic similarity cannot override hard eligibility.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-135 — Use hybrid multimodal retrieval and VLM reranking

**Requirement:** Eligible memory must be ranked using lexical search, text embeddings, image embeddings, composition embeddings, syntax fingerprints, graph proximity, evidence quality, and VLM comparison with current demand, composition, failure, and preservation constraints.

**Consequences (testable):

- Results include scores, reasons, conflicts, and exclusions.

- The system cannot rely solely on one vector index.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-136 — Compile Minimum Complete Context with contradiction coverage

**Requirement:** The JIT retrieval compiler must select only relevant frontmatter, body sections, typed contract references, exceptions, superseding knowledge, failure cases, and material conflicting evidence needed by the current node.

**Consequences (testable):

- The compilation receipt records included, excluded, compressed, and unavailable resources.

- The model may not receive the entire memory corpus by default.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F18 — Control Tower Specialization and Supervisory Console

**User outcome:** An operator can understand and govern every autonomous production run without becoming a manual editor or trusting an opaque black box.

## Description

The existing event-sourced Harness Control Tower remains the platform architecture; this feature defines Visual Asset Editor views, controls, exception packages, and analytics.

## Brownfield baseline

The validated Builder PRD already establishes evidence-backed statuses, events, receipts, phase/contract views, and human actions. The Visual Editor adds GPU, candidate, asset, memory, and evaluation projections.

## Required product delta

Define demand/plan/run dashboards, candidate/evaluation viewers, lineage, syntax-context recurrence, compute operations, Budget Program menu, exceptions, policies, accessibility, and cross-run analytics.

## Traceability

- **Decisions:** D002, D014, D019, D020, D021, D022, D023, D024
- **User journeys:** UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16
- **Cross-cutting NFRs:** NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-UX-001, NFR-UX-002, NFR-UX-003, NFR-UX-004, NFR-UX-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-137 — Render a live Visual Asset Demand overview

**Requirement:** The Control Tower must show caller, demand version, harness/category/profile, asset role, Activative function, composition intent, selected Budget Program, current state, blockers, expected cost/latency, and next authorized action.

**Consequences (testable):

- Every displayed value links to its authoritative contract or event.

- The dashboard cannot infer or edit demand authority from UI-only state.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-138 — Visualize the Visual Production Plan and node graph

**Requirement:** Operators must inspect stages, dependencies, actor/executor, capabilities, bindings, status, checkpoints, invalidation, retries, runtime placement, and events.

**Consequences (testable):

- The graph distinguishes infrastructure and quality paths.

- An opaque 'generating' spinner is insufficient for production observability.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-139 — Compare candidates and evaluation evidence

**Requirement:** The console must support side-by-side candidate, composition render, score, hard-gate, evidence region/time range, failure code, recurrence, cost, and repair comparison.

**Consequences (testable):

- The selected asset and rejected alternatives retain reasons.

- The operator is not required to manually approve passing routine candidates.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-140 — Expose asset lineage and usage context

**Requirement:** Operators must navigate from accepted assets to references, candidates, repairs, master, delivery variants, geometry, prior and current syntax contexts, usage receipts, recurrence verdicts, and supersession.

**Consequences (testable):

- Published and in-progress consumers are distinguishable.

- A lineage view may not omit rejected or repaired branches needed for audit.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-141 — Expose compute, queue, and worker health

**Requirement:** The console must show queued/running jobs, runtime profile, GPU class, model cache, worker heartbeat, timeout, retries, failover, cost, and capacity conditions.

**Consequences (testable):

- Operational failures can be diagnosed without logging into the ComfyUI worker desktop.

- Secrets and unrestricted worker shell access are not exposed through standard views.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-142 — Provide policy-first operator controls

**Requirement:** Authorized users must select Budget Program, production priority, experimental policy, cost/time ceilings, post-failure behavior, cancellation, and capability-development authorization through governed controls.

**Consequences (testable):

- Actions are validated against caller scope and generate receipts.

- Routine controls do not include manual seed, prompt, LoRA-strength, or node editing.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-143 — Present typed human-exception packages

**Requirement:** After authorized escalation, the UI must show trigger, best candidate, passing and failing dimensions, attempted repairs, cost, preserved state, recommended choices, consequences, and downstream authority owner.

**Consequences (testable):

- The chosen response creates a typed event or new demand/plan version.

- An operator cannot silently override a constitutional hard gate from a generic approve button.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-144 — Provide cross-run quality and operations analytics

**Requirement:** The Control Tower must report completion, first-pass acceptance, repair rounds, human exceptions, failure codes, recurrence judgments, route/workflow/model performance, cost, latency, capability gaps, and benchmark drift by asset family and syntax context.

**Consequences (testable):

- Metrics can drive governed learning proposals and regression investigation.

- Analytics cannot update production registry policy without the promotion process.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F19 — Asynchronous Visual Asset Service and Delegation Boundary

**User outcome:** A Content Harness can submit, observe, cancel, amend, and consume visual production through stable contracts without understanding internal ComfyUI workflows.

## Description

The service boundary exposes demands, receipts, events, exceptions, and results while preserving product independence and preparing the separate Delegation PRD.

## Brownfield baseline

V2.1 contains a content-asset delegation module and schemas, but the Visual Editor PRD must define service obligations and leave shared schema ownership to the Delegation PRD.

## Required product delta

Define API behavior, submissions, idempotency, status/events, object references, cancellation, backpressure, result delivery, caller authorization, compatibility, and shared-boundary handoff.

## Traceability

- **Decisions:** D003, D008, D009, D023, D024, D027, D028
- **User journeys:** UJ-01, UJ-04, UJ-08, UJ-12, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-145 — Expose an asynchronous submission API

**Requirement:** The service must accept an authorized demand reference, execution policy, callbacks or event subscription, and idempotency key, then return a durable execution ID and submission receipt without holding the connection for GPU completion.

**Consequences (testable):

- Long-running candidate, repair, and learning runs remain observable after submission.

- A synchronous request-response-only interface is insufficient.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-146 — Publish versioned execution status

**Requirement:** The service must expose registered states from ACCEPTED through validation, planning, capability resolution, queue, production, evaluation, repair, promotion, packaging, and completion plus typed terminal exceptions.

**Consequences (testable):

- Callers can poll or subscribe without controlling internal nodes.

- Unregistered ambiguous states cannot appear in the public contract.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-147 — Emit versioned Visual Asset Events

**Requirement:** Events must identify event/run/demand versions, state, candidate/round when applicable, reason/failure, references, timestamps, and compatibility version.

**Consequences (testable):

- Consumers can rebuild relevant delegation state from events.

- Internal log prose cannot serve as the only integration event.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-148 — Return a provenance-complete Asset Result Contract

**Requirement:** Completed results must list accepted assets and variants, geometry, evaluations, production, budget, syntax-context, authorization, limitations, and downstream action.

**Consequences (testable):

- Downstream composition can validate every referenced artifact and hash.

- A raw image URL alone is not a completed service response.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-149 — Support authorized cancellation

**Requirement:** Registered callers may cancel non-promoted work according to state and policy; cancellation preserves events, artifacts, compute receipts, and reusable learning evidence.

**Consequences (testable):

- The final cancellation receipt identifies work stopped and work retained.

- Cancellation cannot delete accepted historical assets or canonical evidence.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-150 — Communicate backpressure without quality degradation

**Requirement:** The service may return queue depth, capacity, expected delay, runtime alternatives, and scheduling policy while preserving quality thresholds and demand authority.

**Consequences (testable):

- Callers can choose to wait, cancel, or authorize a compatible cost/latency change.

- Load cannot silently route to uncertified capabilities or reduce candidate/evaluator gates.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-151 — Enforce delegation authorization

**Requirement:** Only authorized callers may submit demands, select high-cost or experimental programs, cancel runs, authorize amendments, accept degraded results, or request capability development.

**Consequences (testable):

- All public actions are scoped and receipted.

- An internal service identity cannot impersonate the owning Content Harness for semantic amendments.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-152 — Prepare the separate Delegation PRD handoff

**Requirement:** This PRD must enumerate required shared contracts, responsibility boundaries, versioning, compatibility, amendment flow, error taxonomy, and test fixtures while explicitly deferring final shared schema authority to the Content Harness ↔ Visual Asset Editor Delegation PRD.

**Consequences (testable):

- Architecture can proceed with representative fixtures but not silently freeze cross-product contracts as editor-only property.

- Any shared-boundary conflict is recorded for the Delegation planning session.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F20 — Constraint Conflicts, Feasibility Evidence, and Amendment Proposals

**User outcome:** When an authorized demand cannot be fulfilled, the editor explains the exact conflict and offers bounded alternatives without returning an attractive but semantically compromised approximation.

## Description

Constraint conflicts preserve the immutable demand and distinguish internal plan amendments from demand-level and constitutional amendments.

## Brownfield baseline

V2.1 includes asset amendment requests; the new product needs autonomous conflict detection after repairs/fallbacks and a typed cross-product amendment lifecycle.

## Required product delta

Define conflict codes, evidence, internal versus external authority, amendment options, impact analysis, new demand versions, reuse after amendment, degraded acceptance, and upstream governance.

## Traceability

- **Decisions:** D002, D003, D009, D018, D024, D027
- **User journeys:** UJ-03, UJ-07, UJ-12, UJ-16
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-153 — Detect and classify blocking demand conflicts

**Requirement:** The system must identify contradictory semantic, composition, continuity, control, capability, budget, timing, or delivery constraints that remain infeasible after authorized routes and repairs.

**Consequences (testable):

- The conflict contract identifies code, severity, evidence, attempts, and responsible authority.

- The editor cannot hide a conflict by producing the closest-looking result.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-154 — Preserve the accepted demand during conflict handling

**Requirement:** Conflict analysis and amendment options must reference but never mutate the accepted demand version.

**Consequences (testable):

- The Control Tower shows the unchanged demand and all proposed changes separately.

- An amendment proposal cannot become effective through plan or UI state alone.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-155 — Allow internal production amendments within demand authority

**Requirement:** The editor may version its plan to change approved workflow, model, LoRA, controls, runtime, candidate strategy, or permitted route when all demand constraints remain satisfied.

**Consequences (testable):

- The plan amendment states reason, invalidation, budget impact, and preserved authority.

- Internal amendments cannot relax semantic or out-of-tolerance composition requirements.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-156 — Return demand-level amendment proposals to the owner

**Requirement:** Changes to subject, visible action, Activative function, sequence role, identity, continuity, wrong-reading locks, protected geometry outside tolerance, or quality threshold must be proposed to the owning Content Harness.

**Consequences (testable):

- Each option describes expected feasibility, semantic/Activative impact, cost, and evidence.

- The editor cannot approve or select the owner’s demand amendment.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-157 — Route constitutional amendments upstream

**Requirement:** Proposals that alter asset ontology, category grammar, authority boundaries, production hard gates, Builder architecture, or canonical shared doctrine must enter the validated Builder governance process.

**Consequences (testable):

- The editor provides evidence without modifying upstream constitutions.

- A local release cannot redefine a category or Builder law.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-158 — Create a new demand version for accepted amendments

**Requirement:** When the owner accepts an option, the caller must submit a new Visual Asset Demand version with supersession, amendment source, reason, preserved authority, and changed fields.

**Consequences (testable):

- Dependency analysis determines which prior work can be reused.

- The original failed demand and conflict remain immutable.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-159 — Govern degraded acceptance

**Requirement:** A below-threshold result may be accepted only through a new demand version or owner-authorized exception identifying the relaxed requirement, risk, limitation, and downstream visibility, and only when no constitutional hard gate is violated.

**Consequences (testable):

- The Asset Result Contract records degradation explicitly.

- A standard operator approval cannot bypass meaning-related gates.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-160 — Benchmark conflict and amendment behavior

**Requirement:** The portfolio must include impossible geometry, contradictory identity/continuity, unsupported capability, inadequate budget, and semantic-relaxation cases to verify correct conflict classification and authority routing.

**Consequences (testable):

- The system is scored on refusing silent substitution and proposing useful bounded options.

- A model that always rejects or always compromises fails the benchmark.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F21 — Benchmark Portfolio, Staged Certification, and Release 1 Format 02 Slice

**User outcome:** A release can prove exactly which visual capabilities are reliable and avoid claiming support for untested asset families.

## Description

The certification system evaluates end-to-end production, evaluators, repairs, recurrence, infrastructure, compatibility, and the real Format 02 reference path.

## Brownfield baseline

The Builder PRD already uses staged reference benchmarks and hard gates. The Visual Editor requires multimodal production datasets, evaluator labels, GPU recovery, and one fully consumed Atomic Harness asset path.

## Required product delta

Define corpus layers, dimensions, evaluator benchmark, fault tests, promotion, release receipts, Format 02 reference fixtures, limited scope, local/cloud proof, and one capability-development cycle.

## Traceability

- **Decisions:** D004, D017, D018, D019, D020, D025, D026, D027, D028
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-161 — Maintain a layered visual benchmark corpus

**Requirement:** The portfolio must contain representative real demands, behavior goldens, known failures, adversarial cases, controlled mutations, incomplete/conflicting demands, recurrence contexts, repair cases, capability-transfer cases, and out-of-distribution cases.

**Consequences (testable):

- Each case declares expected behavior, hard gates, scoring, and protected labels.

- Showcase assets alone cannot certify the system.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-162 — Score independent dimensions with hard gates

**Requirement:** Certification must report semantic fidelity, Activative fidelity, composition effectiveness, syntax conformance, identity/continuity, technical validity, temporal stability where applicable, provenance/reproducibility, repair precision, evaluator accuracy, cost, latency, and intervention.

**Consequences (testable):

- A failed constitutional dimension blocks promotion regardless of average.

- One composite score cannot replace the full scorecard.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-163 — Benchmark the VLM evaluator itself

**Requirement:** The evaluator set must include accepted, rejected, borderline, identity drift, wrong action, composition failure, beneficial recurrence, fatiguing recurrence, temporal failure, repairable and nonrepairable cases.

**Consequences (testable):

- Metrics include hard-failure recall, false rejection, failure-code and responsible-layer accuracy, recurrence judgment, repair usefulness, and confidence calibration.

- An evaluator cannot certify its own benchmark labels.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-164 — Test repair precision and preservation

**Requirement:** Repair benchmarks must verify root-cause layer, allowed binding changes, frozen properties, selective invalidation, improvement, regression absence, and three-round stop behavior.

**Consequences (testable):

- Before/after assets and receipts are retained.

- A repair process that routinely redoes the whole asset or drifts identity cannot pass.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-165 — Test compute and workflow recovery

**Requirement:** Certification must inject container crash, GPU loss, API timeout, model-cache corruption, missing node, queue interruption, worker replacement, checkpoint restore, and provider fallback failures.

**Consequences (testable):

- State, lineage, and quality-round counts remain correct after recovery.

- Manual worker intervention cannot be required for the certified routine path.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-166 — Use staged capability and product promotion

**Requirement:** Workflows, models, LoRAs, evaluators, Steering Recipes, runtime profiles, and product releases must move through experimental, benchmarked, shadow, limited-production, and certified-production stages with rollback.

**Consequences (testable):

- The release receipt identifies authorized scope and unresolved limitations.

- Passing unit tests alone cannot authorize production.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-167 — Prove the complete Format 02 vertical slice

**Requirement:** Release 1 must process real Minimal Coach Theatre demands for character identity, pose, expression, gesture, gaze, environment, composition, continuity, syntax role, Activative function, wrong-reading locks, candidates, repair, geometry, result, and downstream composition consumption without routine manual work.

**Consequences (testable):

- The reference slice runs on one local/self-hosted and one cloud Docker GPU profile.

- A good standalone image that is not consumed and evaluated in the Format 02 composition does not complete the slice.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-168 — Represent broader scope honestly

**Requirement:** All eight asset families may have schemas, registries, interfaces, and benchmark placeholders, but only capabilities that pass their required portfolio and release receipt may be routed as production-certified.

**Consequences (testable):

- UI and compatibility manifests expose limited and uncertified scope.

- Release 1 cannot imply full video, documentary retrieval, advanced diagrams, UI reconstruction, or other uncertified production support.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# F22 — Independent Versioning, Architecture Preservation, Readiness, and Development Capsule

**User outcome:** The Visual Asset Editor can evolve independently while preserving upstream Builder authority, cross-product compatibility, and a verifiable path from PRD to implementation.

## Description

This feature governs product/version relationships, architecture protection, compatibility manifests, migration, readiness states, and the implementation handoff.

## Brownfield baseline

The Atomic Harness Builder architecture and V2.1 target profile are already validated. The new product must preserve them, add the editor-specific delta, and defer shared delegation schemas to a separate PRD.

## Required product delta

Define architecture-preservation contract, version taxonomy, compatibility manifest, pinned runs, migrations, readiness states, compute/evaluator proof, Development Capsule, rollback, and implementation prohibitions.

## Traceability

- **Decisions:** D001, D003, D021, D023, D025, D026, D027, D028
- **User journeys:** UJ-01, UJ-13, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-169 — Preserve the validated Atomic Harness Builder architecture

**Requirement:** The product must treat the Builder lifecycle, Harness IR, Capability Ownership Map, Phase/Context/Contract graphs, JIT Skill architecture, Workflow Runtime, Control Tower, Repair doctrine, Development Capsule, category constitutions, and Content Harness semantic authority as frozen upstream contracts.

**Consequences (testable):

- The preservation contract maps each editor feature to compatible upstream mechanisms.

- An editor implementation cannot redesign these systems without a governed upstream amendment.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-170 — Version product and internal capability layers independently

**Requirement:** The editor product, public contracts, Visual Production Plan IR, capability registries, evaluation profiles, compute profiles, CMF-OKF profile, and category certifications must each declare versions and compatibility.

**Consequences (testable):

- Active runs pin exact versions and hashes.

- A registry update cannot silently alter an in-flight run.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-171 — Publish a release compatibility manifest

**Requirement:** Every release must declare supported Builder target profiles, delegation contract versions, plan IR, category/format profiles, registries, runtimes, certified scope, migration need, and rollback support.

**Consequences (testable):

- Compatibility tests cover every claimed combination.

- Undeclared compatibility cannot be inferred from successful manual use.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-172 — Classify patch, minor, and major change behavior

**Requirement:** Patch changes fix implementation without contract behavior change; minor changes add backward-compatible optional behavior; major changes alter mandatory contracts, lifecycle, authority, hard gates, or canonical IR and require migration.

**Consequences (testable):

- Release tooling validates the declared class against actual schema and behavior changes.

- Breaking changes cannot ship under patch or minor version.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-173 — Run representative compatibility and rollback tests

**Requirement:** Before release, the system must execute current and declared older demand fixtures, Format 02 reference cases, result parsing, geometry, events/exceptions, registry bindings, and rollback to the preceding certified release.

**Consequences (testable):

- Results appear in the release receipt.

- A release with an untested claimed compatibility path cannot be certified.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-174 — Enforce implementation readiness states

**Requirement:** The lifecycle must distinguish PRD_DRAFT, PRD_APPROVED, ARCHITECTURE_IN_PROGRESS, ARCHITECTURE_VALIDATED, CONTRACT_FIXTURES_READY, REFERENCE_SLICE_READY, IMPLEMENTATION_AUTHORIZED, LIMITED_PRODUCTION_CERTIFIED, and PRODUCTION_CERTIFIED.

**Consequences (testable):

- Each state has typed evidence and transition gates.

- PRD_APPROVED cannot be interpreted as implementation authorization.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-175 — Generate a traceable Visual Asset Editor Development Capsule

**Requirement:** Implementation authorization must package approved PRD, decisions, requirements, Architecture, preservation contract, public/internal schemas, representative fixtures, Format 02 reference slice, benchmarks, compatibility, epics/stories, feature specs, and readiness receipt with source traceability.

**Consequences (testable):

- Every generated implementation artifact maps to requirements and architecture nodes.

- A folder of ungoverned scaffolding does not satisfy the capsule.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-176 — Enforce binding implementation prohibitions

**Requirement:** Readiness must block monolithic general-agent workflows, producer self-approval, blind retries, more than three quality rounds, frequency-only fatigue, OKF as operational truth, uncontrolled high-budget generation, one-failure LoRA training, silent demand relaxation, uncertified scope claims, routine manual ComfyUI operation, or upstream architecture mutation.

**Consequences (testable):

- The readiness report names each prohibition and evidence of compliance.

- Any known violation forces a blocked authorization result.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.


---

# Cross-Cutting Non-Functional Requirements

These requirements apply across feature boundaries. Feature shards reference the full applicable groups through stable IDs.

## Semantic and Activative Integrity (`NFR-SEM`)

### NFR-SEM-001 — Preserve demand authority

**Requirement:** The system must not change authorized semantic intent, Activative function, sequence role, composition role, identity, continuity, or wrong-reading constraints outside a new approved demand version.

### NFR-SEM-002 — Separate observation from inference

**Requirement:** Visual observations, derived geometry, VLM interpretations, generated proposals, and human-authorized decisions must remain explicitly typed and traceable.

### NFR-SEM-003 — Hard-gate meaning failures

**Requirement:** A technically attractive asset with failed semantic or Activative fidelity must be ineligible for acceptance.

### NFR-SEM-004 — Preserve category and format context

**Requirement:** Evaluation, memory, and routing must retain the requesting category, format profile, atomic harness, and Visual Syntax role.

### NFR-SEM-005 — Prevent silent demand degradation

**Requirement:** Budget, queue pressure, provider failure, or workflow fallback must not lower semantic or composition quality thresholds without a typed amendment.

## Reliability and Recovery (`NFR-REL`)

### NFR-REL-001 — Idempotent submissions

**Requirement:** Identical demand versions and idempotency keys must not create duplicate production runs.

### NFR-REL-002 — Resumable workflows

**Requirement:** Committed nodes must resume from checkpoints after interruption without replaying valid work.

### NFR-REL-003 — Bounded quality repair

**Requirement:** Quality repair must stop after three rounds and transition to a typed terminal or exception state.

### NFR-REL-004 — Failure containment

**Requirement:** A node or worker failure must not mutate unrelated jobs, accepted assets, canonical registries, or authoritative contracts.

### NFR-REL-005 — Rollback readiness

**Requirement:** Certified releases and capability versions must support rollback with preserved asset and execution lineage.

## Performance and Latency (`NFR-PERF`)

### NFR-PERF-001 — Budget-class latency targets

**Requirement:** Each Budget Program must define expected queue, production, evaluation, and total wall-clock envelopes.

### NFR-PERF-002 — Node-level timing

**Requirement:** Every production and evaluation node must emit start, completion, duration, queue, and wait telemetry.

### NFR-PERF-003 — Efficient checkpoint reuse

**Requirement:** Repairs and resumes must reuse non-invalidated deterministic work, references, controls, and accepted intermediate assets.

### NFR-PERF-004 — Adaptive early stopping

**Requirement:** Candidate exploration may stop when a passing candidate exceeds configured confidence and expected additional value is low.

### NFR-PERF-005 — No hidden latency degradation

**Requirement:** Model, workflow, container, or evaluator updates must be benchmarked for p50 and p95 latency changes before promotion.

## Cost and Compute Governance (`NFR-COST`)

### NFR-COST-001 — Pre-execution estimate

**Requirement:** Every production plan must estimate GPU time, candidate count, evaluator depth, storage, and monetary cost before execution.

### NFR-COST-002 — Hard budget enforcement

**Requirement:** Runs must block or request approval before exceeding the selected Budget Program or caller authorization.

### NFR-COST-003 — Cost-per-accepted-asset accounting

**Requirement:** Receipts must report total and marginal cost, failed candidate cost, repair cost, and accepted-output cost.

### NFR-COST-004 — Compute-value routing

**Requirement:** The router must select the least costly certified capability expected to meet required quality and latency.

### NFR-COST-005 — Learning budget separation

**Requirement:** Exploration and capability-learning compute must be labeled separately from ordinary production cost.

## Traceability and Reproducibility (`NFR-TRACE`)

### NFR-TRACE-001 — Immutable execution identity

**Requirement:** Each run must pin demand, plan, workflow, model, VAE, LoRA, control, custom-node, container, evaluator, and runtime identities and hashes.

### NFR-TRACE-002 — Asset lineage completeness

**Requirement:** Every Production Asset and delivery variant must trace to source evidence, parent versions, transformations, candidates, evaluations, and promotion events.

### NFR-TRACE-003 — Contract-to-output traceability

**Requirement:** Every accepted asset must trace to the exact demand fields and quality gates it satisfies.

### NFR-TRACE-004 — Knowledge provenance

**Requirement:** Every CMF-OKF concept and Steering Recipe must reference canonical records, evidence, benchmarks, authority class, and validity.

### NFR-TRACE-005 — Published-version preservation

**Requirement:** Published compositions must remain linked to the exact asset versions they used even after supersession.

## Observability and Control Tower (`NFR-OBS`)

### NFR-OBS-001 — Event completeness

**Requirement:** Every meaningful lifecycle transition, blocker, repair, amendment, cost change, and promotion must emit a typed event.

### NFR-OBS-002 — Evidence-backed status

**Requirement:** The Control Tower must show why a status exists and link to the governing contract, node, receipt, and evidence.

### NFR-OBS-003 — Operational drill-down

**Requirement:** Operators must inspect demand, plan, memory retrieval, candidate, evaluation, repair, compute, and delivery state without accessing hidden reasoning.

### NFR-OBS-004 — Cross-run analytics

**Requirement:** The product must aggregate completion, failure, repair, cost, latency, intervention, recurrence, and capability-gap metrics.

### NFR-OBS-005 — Human action receipts

**Requirement:** Every operator exception, budget authorization, degraded acceptance, cancellation, or promotion action must be receipted.

## Security and Isolation (`NFR-SEC`)

### NFR-SEC-001 — Least privilege

**Requirement:** Nodes and workers receive only declared sources, object-store paths, credentials, tools, models, network destinations, and write permissions.

### NFR-SEC-002 — Sandboxed experimental capability

**Requirement:** Uncertified workflows, nodes, models, LoRAs, or custom nodes must run in isolated experimental environments.

### NFR-SEC-003 — Secret hygiene

**Requirement:** Secrets must never be embedded in demands, plans, capsules, events, OKF concepts, artifacts, or logs.

### NFR-SEC-004 — Untrusted input handling

**Requirement:** Natural-language notes, reference files, workflow metadata, and retrieved knowledge must be treated as data and cannot override system authority.

### NFR-SEC-005 — Asset and model integrity

**Requirement:** Downloaded or mounted models, LoRAs, custom nodes, and containers must be hash-verified against approved registry records.

## Compatibility and Versioning (`NFR-COMPAT`)

### NFR-COMPAT-001 — Versioned service contracts

**Requirement:** Demand, event, result, geometry, evaluation, repair, budget, and exception contracts must declare semantic versions.

### NFR-COMPAT-002 — Backward-compatible minor evolution

**Requirement:** Minor releases may add optional fields or capabilities without breaking declared compatible callers.

### NFR-COMPAT-003 — Explicit major migrations

**Requirement:** Breaking contract, lifecycle, hard-gate, or authority changes require major versions, migration plans, compatibility tests, and rollback.

### NFR-COMPAT-004 — Pinned run dependencies

**Requirement:** An active run may not silently adopt newer registry, workflow, model, evaluator, or runtime versions.

### NFR-COMPAT-005 — Compatibility manifest

**Requirement:** Every product release must publish tested Builder profile, delegation contract, category profile, registry, and runtime compatibility.

## Evaluation and Certification (`NFR-EVAL`)

### NFR-EVAL-001 — Independent evaluation

**Requirement:** The production model or materializer cannot be the sole approver of its own output.

### NFR-EVAL-002 — Profile-specific hard gates

**Requirement:** Each asset family and production route must use a certified evaluation profile with explicit thresholds and failure codes.

### NFR-EVAL-003 — Evaluator calibration

**Requirement:** VLM evaluators must be tested for failure recall, false rejection, failure-code accuracy, responsible-layer accuracy, recurrence judgment, and confidence calibration.

### NFR-EVAL-004 — Protected release benchmarks

**Requirement:** Certification must include representative, adversarial, mutation, repair, recurrence, recovery, and compatibility cases not exposed as runtime hints.

### NFR-EVAL-005 — No average compensation

**Requirement:** Aggregate scores cannot compensate for failed semantic, Activative, composition, technical-validity, reproducibility, or evaluator hard gates.

## Memory and Knowledge Retrieval (`NFR-MEM`)

### NFR-MEM-001 — Contextual usage memory

**Requirement:** Memory must store rendered use, Visual Syntax role, Activative function, composition relationships, recurrence intent, and VLM verdict.

### NFR-MEM-002 — Authority-aware retrieval

**Requirement:** Retrieval must filter knowledge by lifecycle status, authority class, compatibility, category, format, asset family, and current contract.

### NFR-MEM-003 — Hybrid multimodal retrieval

**Requirement:** Search must support lexical, semantic, image, composition, syntax-fingerprint, and graph signals.

### NFR-MEM-004 — Contradiction and exception coverage

**Requirement:** Context compilation must include applicable counterexamples, exceptions, superseding knowledge, and material contradictions.

### NFR-MEM-005 — Minimum Complete Context

**Requirement:** Retrieval must compile the smallest sufficient knowledge package and record included, excluded, and compressed resources.

## Visual Compute Fabric (`NFR-COMPUTE`)

### NFR-COMPUTE-001 — Immutable runtime profiles

**Requirement:** Self-hosted jobs must use digest-pinned container images, ComfyUI versions, custom-node lockfiles, and system dependencies.

### NFR-COMPUTE-002 — Capability-aware scheduling

**Requirement:** Jobs must route by required workflow, model, control, VRAM, queue, cache locality, cost, latency, and certified fallback.

### NFR-COMPUTE-003 — Worker health and recovery

**Requirement:** Workers must expose health checks, job heartbeats, cancellation, timeout, artifact extraction, and replacement behavior.

### NFR-COMPUTE-004 — Resource isolation

**Requirement:** Concurrent jobs must not mutate models, workflows, assets, caches, or execution state belonging to other jobs.

### NFR-COMPUTE-005 — Local-cloud equivalence testing

**Requirement:** Certified local and cloud profiles must pass equivalent representative demand, output-contract, and recovery tests.

## Supervisory Experience and Accessibility (`NFR-UX`)

### NFR-UX-001 — Policy-first controls

**Requirement:** The primary UI must expose budgets, priorities, experiment policies, exceptions, and authorization rather than requiring node-level production work.

### NFR-UX-002 — Clear exceptional decisions

**Requirement:** Human-review packages must explain trigger, attempted repairs, preserved state, unresolved dimensions, choices, and consequences.

### NFR-UX-003 — Visual evidence inspection

**Requirement:** Operators must inspect candidate comparisons, BBOX evidence, VLM evidence regions, composition renders, lineage, and recurrence contexts.

### NFR-UX-004 — Accessible Control Tower

**Requirement:** Core supervisory surfaces must support keyboard navigation, readable status language, sufficient contrast, and non-color-only state cues.

### NFR-UX-005 — No routine approval burden

**Requirement:** Passing routine jobs must complete without operator approval, manual candidate selection, prompt editing, or job restart.

## Workflow Runtime (`NFR-WORKFLOW`)

### NFR-WORKFLOW-001 — Typed production nodes

**Requirement:** Every node must declare actor type, inputs, outputs, dependencies, validators, timeouts, retries, checkpoint, invalidation, and events.

### NFR-WORKFLOW-002 — Deterministic orchestration

**Requirement:** Routing, dependency resolution, contract validation, lifecycle transitions, and budget enforcement must be code-owned.

### NFR-WORKFLOW-003 — Infrastructure-quality separation

**Requirement:** Infrastructure retries and quality repairs must be independently classified, metered, and limited.

### NFR-WORKFLOW-004 — Dependency-safe parallelism

**Requirement:** Parallel candidates or preparation nodes require proven independence, bounded concurrency, cancellation, and merge semantics.

### NFR-WORKFLOW-005 — Workflow integration testing

**Requirement:** Tests must verify gating, resume, selective invalidation, service events, compute failover, and terminal-state correctness.

## Governance and Authority (`NFR-GOV`)

### NFR-GOV-001 — Upstream architecture preservation

**Requirement:** The product must not alter the validated Atomic Harness Builder architecture or shared Activative authority model.

### NFR-GOV-002 — Demand-owner authority

**Requirement:** Only the owning Content Harness may approve demand-level semantic, Activative, sequence, or composition amendments.

### NFR-GOV-003 — Registry promotion governance

**Requirement:** Capabilities and knowledge move through explicit experimental, benchmarked, shadow, limited, production, deprecated, and retired states.

### NFR-GOV-004 — Implementation authorization

**Requirement:** Architecture and implementation may proceed only through the formal readiness gates and receipts defined by the product.

### NFR-GOV-005 — Certified-scope honesty

**Requirement:** The product must clearly distinguish structurally represented, experimental, limited-production, and fully certified asset families and profiles.


---

# Asset Families and Release Scope

## Canonical asset-family ontology

### AF-01 — Documentary and Photographic Evidence

Real-world/editorial photography, archival evidence, screenshots, documents, products, places, events, and human action.

### AF-02 — Human and Character Assets

Real-person portraits, non-identifiable human subjects, 2D characters, identities, poses, expressions, gestures, gaze, props, and interactions.

### AF-03 — Illustrated and Generated Scenes

Symbolic tableaux, narrative/editorial illustration, conceptual scenes, environment plates, and object studies.

### AF-04 — UI, Interface, and Screen Surfaces

App interfaces, chat surfaces, dashboards, social posts, browser frames, device mockups, and data panels.

### AF-05 — Diagrammatic and Informational Assets

Charts, graphs, frameworks, matrices, timelines, maps, comparison boards, processes, and annotated proof.

### AF-06 — Typography and Graphic Elements

Titles, labels, badges, quote cards, captions, numbers, verdict markers, shape systems, and textures.

### AF-07 — Compositing and Scene Components

Cutouts, foreground/background plates, overlays, masks, shadows, reflections, particles, and depth layers.

### AF-08 — Motion and Temporal Assets

Video clips, loops, transitions, animated backgrounds, character animation, kinetic typography, camera moves, and effects.

## Certification states

```text
represented
→ experimental
→ benchmarked
→ shadow
→ limited-production
→ production-certified
→ deprecated
→ retired
```

A family may be represented structurally without being eligible for production routing.

## Release 1 production claim

Release 1 is anchored to **AF-02 Human and Character Assets** for the **2D Character Animation** category and **Format 02 Minimal Coach Theatre**. The certified slice must cover:

- character identity;
- pose;
- expression;
- gesture;
- gaze;
- held or interacted-with props;
- simple environment/scene plate;
- transparent character cutout;
- continuity;
- composition-conditioned geometry;
- ComfyUI generation and transformation;
- independent VLM evaluation;
- targeted repair;
- immutable promotion and result delivery;
- downstream Remotion composition consumption.

A limited subset of AF-03 may be used for environment or simple illustrated scene support, but it must be separately identified in the release receipt.

## Structurally represented, initially uncertified

- complex documentary acquisition and external retrieval;
- advanced UI reconstruction;
- advanced data visualization;
- long-form or multi-shot video generation;
- complex character animation and lip sync;
- advanced VFX;
- general-purpose human capture operations.

The product and Control Tower must not imply production support for these capabilities before their own benchmark and certification gates pass.


---

# Success Metrics and Counter-Metrics

### SM-01 — End-to-end autonomous completion rate

**Class:** Primary

**Definition/target:** At least 90% of in-scope Format 02 production demands complete without human intervention after the limited-production learning period.

### SM-02 — Semantic hard-gate pass precision

**Class:** Primary

**Definition/target:** At least 98% of accepted assets satisfy expert-labeled semantic and Activative requirements; no known constitutional failure is accepted.

### SM-03 — Composition effectiveness

**Class:** Primary

**Definition/target:** At least 92% of accepted assets pass composition-context evaluation and downstream composition validation without asset regeneration.

### SM-04 — First-pass candidate acceptance

**Class:** Secondary

**Definition/target:** Measure and improve the percentage of demands with at least one passing candidate in the initial portfolio; do not optimize by lowering gates.

### SM-05 — Median quality-repair rounds

**Class:** Secondary

**Definition/target:** Median at or below one for mature in-scope workflows, with a constitutional maximum of three.

### SM-06 — Recovery success

**Class:** Primary

**Definition/target:** At least 99% of injected recoverable infrastructure failures resume or fail over without loss of committed state or quality-round corruption.

### SM-07 — Asset reproducibility

**Class:** Primary

**Definition/target:** 100% of accepted assets preserve sufficient pinned identity to reconstruct plan, workflow, compute, model, LoRA, controls, evaluator, and lineage.

### SM-08 — Budget conformance

**Class:** Secondary

**Definition/target:** At least 95% of completed runs remain within selected Budget Program cost and wall-clock ceilings, excluding explicit approvals.

### SM-09 — Evaluator hard-failure recall

**Class:** Primary

**Definition/target:** Production evaluator profiles meet release-specific hard-failure recall and false-rejection thresholds on protected labeled cases.

### SM-10 — Repair precision

**Class:** Primary

**Definition/target:** At least 90% of successful repairs modify the labeled responsible layer while preserving all expert-labeled frozen properties.

### SM-11 — Syntax-aware recurrence accuracy

**Class:** Primary

**Definition/target:** VLM recurrence verdicts meet the protected benchmark threshold across beneficial, productive, redundant, fatiguing, and contradictory cases.

### SM-12 — Memory retrieval usefulness

**Class:** Secondary

**Definition/target:** Retrieved knowledge improves or preserves quality and cost over no-memory control without increasing authority violations.

### SM-13 — Cost per accepted asset

**Class:** Secondary

**Definition/target:** Track by family, workflow, Budget Program, and repair round; optimize only after hard quality gates are maintained.

### SM-14 — Human exception rate

**Class:** Secondary

**Definition/target:** Routine production exception rate trends below 5% in certified scope without suppressing valid conflict or capability-gap reporting.

### SM-C1 — Raw candidate count

**Class:** Counter

**Definition/target:** Do not optimize for producing more candidates; candidate count is a budgeted means, not product value.

### SM-C2 — Number of models, LoRAs, workflows, or agents

**Class:** Counter

**Definition/target:** Do not treat registry size or compute fan-out as evidence of capability.

### SM-C3 — Standalone aesthetic score

**Class:** Counter

**Definition/target:** Do not optimize beauty independently of semantic, Activative, composition, continuity, and editability requirements.

### SM-C4 — Zero human intervention at any cost

**Class:** Counter

**Definition/target:** Do not hide legitimate authority, capability, conflict, or degraded-result exceptions to make automation statistics look better.


---

# Non-Goals and Binding Anti-Goals

1. The product does not implement or redesign the Atomic Harness Builder.
2. The product does not own Content Harness meaning, Activative policy, sequence role, or final composition authority.
3. The product does not use ComfyUI JSON as the canonical product specification.
4. The product does not route all work through one general visual-editor agent.
5. The product does not require the same fixed specialist chain for every request.
6. The product does not include a standalone Rights Analyst or routine manual rights-review layer.
7. The product does not treat editing as proof that provenance is unnecessary.
8. The product does not let production models approve their own output.
9. The product does not accept the first passing or fastest candidate by default.
10. The product does not run blind retries without a causal binding or route change.
11. The product does not exceed three autonomous quality-repair rounds.
12. The product does not judge visual fatigue from usage frequency alone.
13. The product does not use OKF, a vector database, or embeddings as canonical operational truth.
14. The product does not load the entire knowledge corpus into every model context.
15. The product does not turn a single successful candidate into a production Steering Recipe.
16. The product does not train a LoRA because one normal demand failed.
17. The product does not let high Budget Programs become uncontrolled random generation.
18. The product does not silently relax an accepted Visual Asset Demand.
19. The product does not claim production support for structurally represented but uncertified asset families.
20. The product does not require routine manual ComfyUI graph, prompt, seed, LoRA, or mask manipulation.
21. The product does not allow in-flight runs to adopt unpinned capability or runtime updates.
22. The product does not allow a local product release to change category constitutions or shared Activative doctrine.
23. The product does not substitute a beautiful asset for failed composition effectiveness.
24. The product does not authorize implementation because the PRD is complete.


---

# MVP and Release Plan

## Release 1 goal

Prove the complete autonomous production spine through one real **Format 02 Minimal Coach Theatre** integration.

```text
Visual Asset Demand
→ asynchronous submission
→ Visual Production Plan IR
→ smart memory retrieval
→ capability and compute routing
→ containerized ComfyUI execution
→ candidate portfolio
→ deterministic + VLM evaluation
→ composition evaluation
→ syntax-aware recurrence
→ targeted repair
→ immutable asset promotion
→ Asset Result Contract
→ downstream Remotion composition
```

## Release 1 in scope

- AF-02 character identity, pose, expression, gesture, gaze, simple prop interaction;
- transparent cutouts and simple character/environment scenes;
- identity and sequence continuity;
- reuse, deterministic transform, generation, mask/background removal, inpaint/outpaint, simple composite, variants;
- local/self-hosted and cloud Docker GPU runtime proof;
- Lean, Standard, and Exploration polished presets;
- Premium, Capability Learning, and Custom defined and available only under advanced/experimental policy until certified;
- one real capability-development lifecycle, preferably a character-identity or Minimal Coach Theatre visual-language LoRA;
- CMF-OKF concepts and smart retrieval for workflows, failures, repairs, Steering Recipes, and syntax usage;
- full Control Tower views and exception packages;
- representative shared contract fixtures pending the separate Delegation PRD.

## Release 1 out of scope for certification

- broad documentary sourcing;
- advanced long-form video generation;
- full UI reproduction;
- advanced charts/diagrams;
- complex multi-character temporal continuity;
- lip sync;
- general LoRA factory for arbitrary asset types;
- all-provider support;
- universal visual editing.

## Release sequence

### R1 — Format 02 limited production

Complete the reference slice and certify declared character/scene scope.

### R2 — Transfer and second family certification

Add a materially different asset family such as illustrated editorial scenes or documentary evidence.

### R3 — Broader visual compute and temporal capability

Certify selected motion/video and advanced compositing routes.

### R4 — General Visual Asset Editor certification

Require cross-family benchmark coverage, mature delegation contracts, and production operations evidence.


---

# Risks and Mitigations

### R-01 — Semantic drift during production

**Risk:** A model or workflow changes meaning while producing a visually attractive asset.

**Mitigation:** Typed demand authority, protected bindings, independent VLM hard gates, amendment flow.

### R-02 — Evaluator overconfidence or bias

**Risk:** The VLM approves wrong actions or rejects valid recurrence.

**Mitigation:** Labeled evaluator benchmarks, calibration, secondary evaluation on uncertainty, shadow promotion.

### R-03 — ComfyUI/custom-node drift

**Risk:** Mutable dependencies break reproducibility or production consistency.

**Mitigation:** Digest-pinned containers, node lockfiles, capability registry, local/cloud parity tests.

### R-04 — GPU cost explosion

**Risk:** High candidate counts, video models, or repairs exceed value.

**Mitigation:** Budget Programs, estimates, hard ceilings, adaptive early stop, cost-per-accepted-asset analytics.

### R-05 — False memory relevance

**Risk:** Semantic search retrieves attractive but incompatible knowledge.

**Mitigation:** Authority filters, typed graph, compatibility, syntax fingerprints, VLM reranking, contradiction coverage.

### R-06 — Skill/memory sediment

**Risk:** Steering knowledge grows noisy and contradictory.

**Mitigation:** CMF-OKF lifecycle, supersession, indexes, maturity, validity windows, retrieval evaluation.

### R-07 — Capability sprawl

**Risk:** Too many LoRAs, models, workflows, and adapters fragment routing.

**Mitigation:** Capability-gap threshold, control comparison, expected reuse, registry deduplication, deprecation.

### R-08 — Reference-slice overfitting

**Risk:** The product works only for Format 02.

**Mitigation:** Provider-neutral IR, structurally represented families, transfer benchmarks, later family certification.

### R-09 — Architecture collision

**Risk:** Editor design rewrites the validated Builder or Content Harness authority.

**Mitigation:** Architecture Preservation Contract, upstream amendment route, readiness prohibition tests.

### R-10 — Manual-operation creep

**Risk:** Operators become permanent ComfyUI technicians.

**Mitigation:** Autonomous workflow, policy-first console, exception-only human states, no-routine-manual-work metric.

### R-11 — Visual repetition misclassification

**Risk:** Continuity is rejected or repeated visual arguments are missed.

**Mitigation:** Rendered syntax usage receipts, VLM recurrence labels, protected recurrence benchmarks.

### R-12 — Repair-induced drift

**Risk:** A local repair changes identity, geometry, or semantic properties that were already correct.

**Mitigation:** Typed preserve lists, causal binding changes, before/after evaluation, selective invalidation.

### R-13 — Public contract instability

**Risk:** Independent releases break Content Harness callers.

**Mitigation:** Semantic versions, compatibility manifest, representative fixtures, separate Delegation PRD, rollback.

### R-14 — OKF authority confusion

**Risk:** Readable knowledge files become treated as transactional truth.

**Mitigation:** Explicit projection-only doctrine, canonical resource URIs, hashes, typed store precedence, validator checks.


---

# Assumptions and Open Questions

## Assumptions

- **A-01:** The validated Atomic Harness Builder architecture remains the upstream authority.
- **A-02:** Format 02 Visual Asset Demands and Visual Syntax fixtures can be curated before implementation authorization.
- **A-03:** A VLM or evaluator ensemble can be benchmarked sufficiently for limited production; specific model choice remains an Architecture decision.
- **A-04:** At least one local/self-hosted and one cloud GPU environment can run the required ComfyUI workflow and model stack.
- **A-05:** The separate Delegation PRD will finalize cross-product schema ownership and compatibility policy.
- **A-06:** CMF-OKF v1 will remain compatible with the minimal OKF 0.1 format while adding CMF-specific fields and typed edges.
- **A-07:** Routine source-provenance classification can be deterministic without a dedicated rights workcell.
- **A-08:** Remotion remains the downstream composition owner for the Format 02 reference path; the Visual Asset Editor returns assets and geometry, not final edited shorts.

## Open questions

### OQ-01 — Which exact Format 02 atomic production promise and specimen set will be the canonical Release 1 benchmark target?

Owner: Product/Format 02 Architecture; block: Architecture finalization.

### OQ-02 — Which image-generation base model and VLM evaluator should be the initial benchmark controls?

Owner: Visual Runtime/Evaluation Architecture; block: compute proof.

### OQ-03 — Which cloud GPU provider and object-storage implementation should Architecture select?

Owner: Infrastructure Architecture; block: implementation, not PRD.

### OQ-04 — Which shared contract fields will be finalized by the Delegation PRD versus editor-internal schemas?

Owner: Delegation product planning; block: cross-product implementation.

### OQ-05 — What protected labeled dataset size is sufficient for initial evaluator and recurrence certification?

Owner: Evaluation Architecture; block: limited-production gate.

### OQ-06 — Which character identity or visual-language gap should be used for the Release 1 capability-development proof?

Owner: Format 02/Visual Runtime; block: capability-development story.


---

# Implementation Readiness Handoff

## What this PRD authorizes

The approved PRD authorizes the creation of:

- Visual Asset Editor Architecture;
- representative contract fixtures;
- Format 02 reference-slice design;
- benchmark and evaluator design;
- Epics and Stories after Architecture validation;
- feature technical specifications.

It does not authorize production implementation.

## Required sequence

```text
PRD review and approval
→ Architecture
→ UX/Supervisory Console contract where needed
→ representative delegation fixtures
→ Format 02 reference-slice evidence
→ Epics and vertical Stories
→ feature technical specifications
→ implementation-readiness audit
→ Development Capsule
→ IMPLEMENTATION_AUTHORIZED
```

## Architecture must resolve

- canonical data and storage boundaries;
- Visual Production Plan IR and compiler;
- event-sourced workflow runtime;
- asynchronous service transport;
- capability and compatibility registries;
- ComfyUI workflow/compiler approach;
- model/LoRA/control/runtime registry implementation;
- local/cloud compute fabric;
- object storage and immutable artifact identity;
- VLM evaluation architecture and labeled data;
- Visual Asset Memory and smart retrieval;
- CMF-OKF projection/indexing;
- Control Tower projections and supervisory UX;
- security, isolation, observability, migration, and rollback.

## Implementation authorization blockers

Implementation remains blocked until:

- the Architecture Preservation Contract passes;
- representative input/output/exception contracts exist;
- the Format 02 demand and composition fixtures are complete;
- local and cloud compute proof plans are executable;
- evaluator benchmark design and initial labeled set are approved;
- Release 1 benchmark manifest exists;
- Budget Program semantics are finalized;
- Epics/Stories cover every FR and NFR;
- the Development Capsule and readiness receipt pass.


## Constitutional alignment requirements

Technical specifications must implement the amended Visual Asset Demand and Visual Quality Evaluation contracts, preserve Expression Moment and Activative Intelligence lineage, enforce non-empty wrong-reading locks, and prove that the VAE consumes rather than invents Visual Semantics, Visual Narrative, Feature Contracts, and T/V requests.
