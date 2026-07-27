# CMF Atomic Harness Builder Next — Combined PRD


---

# 0. Document Purpose and Authority

This sharded Product Requirements Document defines **CMF Atomic Harness Builder Next**, the production-hardening evolution of the existing CMF Atomic Harness Spec Builder V2.1.

The product is a **human-governed harness-development compiler**. It transforms an evidence-saturated atomic candidate into an implementation-authorized Development Capsule containing a typed Harness IR, constitutional specifications, phase-local JIT Skills and composition recipes, an executable Builder Workflow Runtime, module and runtime contracts, evaluation and repair systems, implementation artifacts, observability configuration, and readiness receipts. It does **not** implement the final production harness.

## Intended readers

- CMF product and harness architects;
- Builder maintainers and technical architects;
- format-category stewards;
- JIT Skill and evaluation maintainers;
- implementation leads and coding agents;
- reviewers, ratifiers, and release authorities.

## Authority model

The product uses three complementary authorities:

1. **Deterministic tooling** owns source locking, indexing, schema validation, graph transitions, compilation, dependency resolution, context selection, receipts, and other mechanically checkable work.
2. **Agents and typed model programs** own bounded investigation, semantic inference, multimodal parsing, recommendations, and creative transformations inside authorized phases.
3. **Humans** own constitutional, creative-policy, risk, waiver, and irreversible architectural decisions.

## Document system

This package separates product intent from downstream technical realization:

- `prd/` contains product behavior, globally stable Functional Requirements, cross-cutting Non-Functional Requirements, scope, success metrics, and anti-goals.
- `governance/` contains the 33-decision register, requirement registry, source register, category and target registries, product constitution, and traceability maps.
- `addendum/` preserves architecture-rich context, prior-system lessons, JIT Skill history, and brownfield details that should inform Architecture without bloating the main PRD.
- `handoff/` defines the required next artifacts: Architecture, Epics and Stories, feature technical specifications, and implementation-readiness validation.
- `validation/` contains mechanical checks for IDs, coverage, links, source integrity, and anti-placeholder discipline.

## Stable identifiers

- Product decisions: `D001`–`D033`
- User journeys: `UJ-01`–`UJ-14`
- Features: `F01`–`F18`
- Functional Requirements: `FR-001`–`FR-210`
- Non-Functional Requirements: namespaced `NFR-*`
- Success metrics: `SM-*`; counter-metrics: `SM-C*`
- Anti-goals: `AG-*`
- Assumptions: `A-*`; open questions: `OQ-*`; risks: `R-*`

The glossary is binding. Downstream documents must use its terms exactly or propose a governed glossary change.

## Current phase

This PRD is **draft for review**. The 33-question product-constitution session is complete, and the approved workflow-runtime delta is incorporated without changing the 33 locked decisions. Architecture, UX/control-tower design, epics, stories, and per-feature technical specifications are intentionally downstream.


---

# 1. Vision and Product Promise

## Vision

CMF needs more than a specification generator. It needs a compiler capable of turning visual and repository evidence into an authorized architecture for one high-performing Activative Atomic Harness—while preserving human authority, category-native visual and sequencing intelligence, canonical skill quality, reproducibility, and downstream accountability.

The Builder is the quality multiplier. A weak decision in one harness harms one content product; a weak principle in the Builder propagates into every generated constitution, JIT Skill, module boundary, contract, evaluator, repair route, and implementation story. Conversely, a production-grade Builder compounds quality across the entire CMF harness portfolio.

## Canonical product promise

> **The CMF Atomic Harness Builder Next is a human-governed harness-development compiler that transforms an evidence-saturated atomic candidate into an implementation-authorized Development Capsule comprising a typed Harness IR, constitutional specifications, category-native visual and sequencing architecture, phase-local JIT Skills and composition recipes, module and runtime contracts, evaluation and repair systems, implementation artifacts, and observability receipts. It does not implement or operate the final production harness.**

## Product correction

The current V2.1 Builder is a credible baseline. It already provides source inspection, saturation, atomicity status, guided and provisional Genesis, ratification, decision-graph status, OpenSpec compilation, and readiness. It is not being discarded.

The production-readiness gap is that the current system does not yet make the following first-class and executable:

- specimen-first Visual Syntactic Parsing and category-adapted temporal parsing;
- one canonical Harness IR from which every artifact is compiled;
- an executable Builder Workflow Runtime that assigns humans, agents, and deterministic code to explicit nodes and routes;
- explicit capability, module, phase, context, contract, skill, evaluator, and repair ownership;
- a canonical skill ecology separated from harness adaptations, composition recipes, and ephemeral JIT Execution Capsules;
- deterministic Minimum Complete Context compilation;
- versioned constitutions for four distinct format categories;
- Activative Sequencing Intelligence as a primary capability;
- behavioral skill evaluations, protected benchmarks, and downstream harness-effectiveness proof;
- event-sourced Pi observability;
- precise repair, invalidation, prototype, and implementation-authorization states;
- controlled V2.1 migration and general-certification limits.

## Why now

The system has reached the point where adding more doctrine or more parallel workspaces without a stronger compiler would multiply specification variance. The next investment must make doctrine executable, testable, observable, and traceable so future Atomic Harnesses inherit the right architecture by construction.

## Three success gates

1. **Structural validity** — required IR nodes, artifacts, contracts, references, graphs, and receipts exist and validate.
2. **Implementation readiness** — an implementation team can build the authorized scope without inventing missing constitutional or architectural decisions.
3. **Downstream harness effectiveness** — the implemented harness meets its target-specific accuracy, Activative fidelity, wrong-reading, stability, latency, cost, and repair thresholds.

The Builder is not fully proven at Gate 2. Its ultimate quality is confirmed at Gate 3.


---

# 2. Target Users, Jobs, and Journeys

## 2.1 Primary users and jobs

| ID | User | Role | Jobs to be done |
| --- | --- | --- | --- |
| P-01 | CMF Harness Architect | Primary operator and constitutional decision owner | Compile evidence into a trustworthy Draft Harness Model<br>Review one dependency-ready decision at a time<br>Understand why a run is blocked and what evidence supports each recommendation<br>Authorize implementation without surrendering creative-policy authority |
| P-02 | Format Category Steward | Maintains a canonical format-category constitution and transfer benchmarks | Evolve category ontologies and sequence rules without silently breaking dependent harnesses<br>Inspect category-level regressions and migration impact<br>Keep shared mechanics separate from atomic creative grammar |
| P-03 | JIT Skill Maintainer | Owns canonical skills, adaptations, recipes, and behavioral evaluations | Avoid redundant or monolithic skills<br>Prove behavioral value against controls<br>Trace the exact evaluated artifact into shipped execution capsules |
| P-04 | Implementation Lead or Agent | Consumes an authorized Development Capsule | Receive explicit modules, contracts, test seams, tickets, and acceptance criteria<br>Avoid inventing constitutional decisions during coding<br>Raise implementation contradictions as governed deltas |
| P-05 | Reviewer and Ratifier | Validates evidence, architecture, skill maturity, benchmark performance, and waivers | See independent score dimensions and hard blockers<br>Inspect provenance and decision history<br>Issue human actions through receipted controls |
| P-06 | Builder Maintainer | Evolves V2.1 into the next production-grade compiler | Measure deltas against a stable baseline<br>Prevent regressions and overfitting<br>Maintain schema, compiler, UI, and migration compatibility |

## 2.2 Non-users in Release 1

- General software teams seeking a universal project or agent factory.
- End users consuming finished CMF content; they are downstream beneficiaries, not direct Builder operators.
- Operators who expect the Builder to implement a complete production harness without an authorized Development Capsule and implementation phase.
- Unapproved third-party asset editors or orchestrators outside the versioned Delegation profile.

## 2.3 Key user journeys

### UJ-01 — An architect initializes a governed compilation run

**Persona and context:** CMF Harness Architect.

**Entry state:** The architect has an exact target candidate and source archives or repositories but no authorized harness specification.

**Path:**

1. Select one compilation target and its source profile.
2. Resolve and validate source locations without mutating them.
3. Create a source lock, specimen inventory, and evidence-readiness diagnosis.
4. See blockers and required human actions in the Control Tower.

**Climax:** The Builder proves the workspace is ready for analysis or explains exactly why it is blocked.

**Resolution:** A resumable run exists with stable IDs, hashes, events, and authority boundaries.

### UJ-02 — The Builder parses a specimen corpus before assigning meaning

**Persona and context:** CMF Harness Architect.

**Entry state:** The evidence workspace is locked and contains screenshots, slides, images, or video frames.

**Path:**

1. Normalize every specimen and derive contact sheets or frame inventories.
2. Parse visible components, geometry, hierarchy, relationships, and temporal states.
3. Classify composition variables and preserve observed versus inferred knowledge status.
4. Compare specimens to draft syntax and sequence grammar.

**Climax:** The architect can inspect overlays and trace every candidate invariant to actual specimens.

**Resolution:** A provisional visual and temporal syntax contract feeds saturation and atomicity without masquerading as ratified truth.

### UJ-03 — The architect ratifies an atomic product boundary

**Persona and context:** CMF Harness Architect.

**Entry state:** The Builder has a saturated evidence set and candidate cross-specimen grammars.

**Path:**

1. Compare production promise, persistent instrument, state machine, inputs, runtime, evaluations, and repairs.
2. Review merge, split, variant, family, or insufficient-evidence alternatives.
3. Inspect the evidence and risk of a wrong classification.
4. Ratify or reject the proposed boundary.

**Climax:** One content product receives an explicit, receipted atomicity status.

**Resolution:** The Builder may compile a Draft Harness Model only for the approved boundary.

### UJ-04 — The architect conducts dependency-driven Genesis

**Persona and context:** CMF Harness Architect.

**Entry state:** An unratified Draft Harness Model and typed decision graph exist.

**Path:**

1. Receive one dependency-ready recommendation with evidence and trade-offs.
2. Accept, revise, defer, or reject the recommendation.
3. See the Harness IR update and affected decisions reopen when necessary.
4. Resume later without losing decision memory.

**Climax:** All mandatory constitutional decisions have authority and no blocking contradiction remains.

**Resolution:** The authorized Harness IR becomes eligible for architecture and artifact compilation.

### UJ-05 — The Builder assigns every capability to the right execution form

**Persona and context:** Builder Maintainer.

**Entry state:** The Harness IR defines required transformations but not yet their owners.

**Path:**

1. Evaluate each capability for determinism, judgment, authority, provider dependence, and independent evaluation needs.
2. Reuse canonical modules and skills where possible.
3. Record primary owner, support assets, test seams, and failure owner.
4. Reject giant-agent or giant-prompt ownership where a deeper module boundary is available.

**Climax:** Every capability has an explicit, justified owner and no hidden semantic authority.

**Resolution:** The Builder can compile phases, modules, contracts, skills, and evaluators coherently.

### UJ-06 — A category steward compiles a category-native harness

**Persona and context:** Format Category Steward.

**Entry state:** The atomic harness belongs to one of the five canonical categories.

**Path:**

1. Load the category constitution and applicable format profile.
2. Apply category-specific visual and temporal parsing ontologies.
3. Compile category-owned sequencing intelligence, registries, runtime constraints, evaluations, and repair routes.
4. Overlay atomic creative grammar without moving it into the shared category layer.

**Climax:** The resulting harness is category-native rather than a generic template with a cosmetic skin.

**Resolution:** Category and atomic responsibilities remain separately versioned and traceable.

### UJ-07 — The Builder compiles a phase-local JIT Execution Capsule

**Persona and context:** JIT Skill Maintainer.

**Entry state:** A phase is ready, runtime bindings are present, and an approved composition recipe exists.

**Path:**

1. Resolve authority, dependencies, conflicts, and degradation policies.
2. Select canonical skills, harness adaptations, and active references.
3. Apply the phase Context Budget Policy and exclude inactive branches.
4. Produce instructions, context manifest, contract binding, hashes, and compilation receipt.

**Climax:** The execution model receives the smallest complete authorized context for this exact phase.

**Resolution:** The capsule is reproducible, ephemeral, and linked to the evaluated skill artifacts it contains.

### UJ-08 — A skill maintainer proves a JIT capability works

**Persona and context:** JIT Skill Maintainer.

**Entry state:** A canonical skill or harness adaptation exists but is not production-ready.

**Path:**

1. Run a no-guidance control and capture baseline failures.
2. Run positive, adversarial, missing-evidence, and pressure cases in fresh contexts.
3. Compare skill-only, adaptation, recipe, and full-capsule variants.
4. Store variance, latency, token, and behavioral receipts and promote maturity only if thresholds pass.

**Climax:** The maintained skill demonstrates measurable behavioral value instead of persuasive documentation quality.

**Resolution:** Only the exact evaluated version is eligible for production capsule compilation.

### UJ-09 — A reviewer diagnoses a blocked run in the Control Tower

**Persona and context:** Reviewer and Ratifier.

**Entry state:** A run is blocked by evidence, architecture, skill maturity, benchmark, or authority.

**Path:**

1. Open the phase graph and blocker summary.
2. Inspect evidence, decisions, contracts, skill versions, and failed cases.
3. Choose a governed action such as deeper evidence, targeted repair, waiver, or rejection.
4. Receive a receipt and observe the resulting invalidations and next actions.

**Climax:** The reviewer knows what failed, why, who owns it, and what evidence is required to continue.

**Resolution:** Operational state changes without creating a second source of truth outside the Harness IR and run ledger.

### UJ-10 — The Builder repairs only the responsible layer

**Persona and context:** Builder Maintainer.

**Entry state:** An evaluator reports a typed failure after one or more phases completed.

**Path:**

1. Gather evidence and identify the root cause rather than patch the visible symptom.
2. Select the repair route and freeze unaffected upstream state.
3. Invalidate all and only dependent descendants.
4. Rerun targeted regressions and regenerate affected artifacts.

**Climax:** The failure is resolved without rerunning or rewriting unrelated constitutional work.

**Resolution:** A repair receipt preserves the before/after state and regression evidence.

### UJ-11 — An implementation team receives an authorized Development Capsule

**Persona and context:** Implementation Lead or Agent.

**Entry state:** The Harness IR, architecture, skills, benchmarks, and authorization gates pass.

**Path:**

1. Download the traceable capsule and inspect authorization scope.
2. Use typed contracts, module manifests, interface stubs, fixtures, and dependency-ordered stories.
3. Implement one vertical slice without inventing creative or constitutional policy.
4. Raise genuine contradictions through a governed delta rather than silently modifying the specification.

**Climax:** A working vertical path can be built from the capsule with minimal ungoverned questions.

**Resolution:** Implementation evidence flows back into the Builder benchmark and certification system.

### UJ-12 — A Builder release proves downstream effectiveness

**Persona and context:** Builder Maintainer.

**Entry state:** A new Builder version has passed local structural tests.

**Path:**

1. Compile the primary reference harness with the baseline and candidate Builder versions.
2. Compare specification quality, skill behavior, implementation friction, and resulting harness performance.
3. Run transfer and protected benchmark cases with repeated fresh contexts.
4. Approve, conditionally approve, or reject the release using hard gates.

**Climax:** The team can show whether the Builder change improved the harness it caused to be built.

**Resolution:** General claims remain limited to the benchmark portfolio actually passed.

### UJ-13 — A maintainer runs the Builder as an executable human-agent-code workflow

**Persona and context:** Builder Maintainer.

**Entry state:** The reference harness path has an approved product definition, but the Builder phases are not yet automated as one production workflow.

**Path:**

1. Walk the reference path manually and capture every human action, agent judgment, code operation, contract, condition, and failure route.
2. Compile the captured path into a versioned Builder Workflow IR and select an approved workflow profile.
3. Execute deterministic nodes, phase-local agent programs, validators, and human gates through explicit node contracts.
4. Observe node state, budgets, retries, artifacts, and blockers in the Harness Control Tower.

**Climax:** The same reference compilation can run reproducibly without hiding orchestration inside one Pi conversation or monolithic skill.

**Resolution:** A tested workflow profile can be versioned, promoted, resumed, repaired, and reused for future compilation runs.

### UJ-14 — A maintainer contains and repairs a Builder workflow incident

**Persona and context:** Builder Maintainer.

**Entry state:** A production Builder run reports a node failure, routing defect, false pass, timeout storm, or workflow regression.

**Path:**

1. Classify the incident and freeze affected workflow and artifact versions.
2. Inspect the node inputs, outputs, events, sandbox, validator evidence, and recent workflow changes.
3. Run the specialized repair or hotfix workflow under bounded authority and compute.
4. Re-execute targeted workflow and regression tests before promoting or rolling back the fix.

**Climax:** The incident is resolved without corrupting locked evidence, ratified decisions, unaffected nodes, or protected benchmark truth.

**Resolution:** A complete incident, repair, validation, and promotion receipt remains available for audit and future prevention.


---

# 3. Canonical Glossary

- **Activative Atomic Harness** — An independently versioned production system that owns one recognizable Activative content product, its semantic workcell, visual or temporal grammar, runtime, evaluations, and repairs.
- **Atomic Content Harness** — A compilation target that transforms governed evidence and meaning into one atomic content product.
- **Visual Asset Editor** — A separate compilation target that researches, resolves, edits, generates, versions, and returns visual assets without mutating source meaning, sequence role, or composition purpose.
- **Delegation Contract** — The versioned request, response, error, provenance, and compatibility ABI between a content harness and the Visual Asset Editor.
- **Harness-development compiler** — The Builder product boundary: a system that compiles evidence and decisions into an implementation-authorized Development Capsule without implementing the final harness.
- **Harness IR** — The canonical typed intermediate representation from which all specifications, skills, graphs, contracts, tests, tickets, and receipts are generated.
- **Draft Harness Model** — A provisional, evidence-grounded, explicitly unratified model compiled before Genesis.
- **Genesis** — The dependency-driven human-governed process that challenges and ratifies constitutional decisions in the Draft Harness Model.
- **Knowledge Status** — The epistemic classification of a value: observed, measured, derived, hypothesized, human-decided, or generated.
- **Authority Status** — The governance classification describing whether a value is provisional, ratified, waived, superseded, or invalidated.
- **Visual Syntactic Parsing** — The phase that inventories visible components, normalized geometry, relationships, hierarchy, composition variables, and temporal states before assigning semantic meaning.
- **BBOX + WHY** — A paired record of an element's normalized location and an evidence-backed hypothesis or decision about its compositional purpose.
- **Composition Variable** — A visual property classified as invariant, controlled variable, content slot, optional component, anomaly, or unknown.
- **Visual Syntax** — The cross-specimen grammar of components, relationships, variables, and invariants that makes a visual product recognizable.
- **Temporal Syntax** — The observed grammar of appearance, persistence, motion, transition, timing, sonic relation, and disappearance across time.
- **Activative Sequencing Intelligence** — Category- and format-adapted reasoning that arranges beats, scenes, states, transitions, assets, and sonic cues to create an intended viewer-state transformation.
- **Canonical Format Category** — One of five governed production substrates: Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, or Conversational Activation / Human Expression.
- **Format Profile** — A category-local profile such as one of the short-form editing formats, defining its parsing, sequence, runtime, skill, evaluation, and repair rules.
- **Category Constitution** — A versioned canonical contract governing a format category's ontology, registries, runtime constraints, benchmarks, and migration policy.
- **Capability Ownership Map** — The explicit assignment of every required capability to its primary executor and supporting modules, skills, references, evaluators, or human authority.
- **Canonical Skill** — A reusable, versioned, behaviorally evaluated procedural capability stored in the canonical Skill Capability Registry.
- **Harness-local Skill Adaptation** — An ecological mutation of a Canonical Skill for one atomic harness without creating a new canonical capability.
- **Skill Composition Recipe** — A reusable declaration of which skills, adaptations, reasoning modules, references, and runtime bindings must be combined for a phase or path.
- **JIT Execution Capsule** — An ephemeral, phase-local, reproducibly compiled instruction and context package for one exact invocation.
- **Minimum Complete Context** — The smallest context that still satisfies a phase's responsibility, contracts, active branches, authority, evidence, and completion criteria.
- **Phase Graph** — The typed dependency graph defining what phases run, in what order, with which executors and completion criteria.
- **Context Graph** — The typed graph defining what each phase may load, must exclude, unload, and pass downstream.
- **Reference and Loading Graph** — The versioned policy governing which doctrine, registries, examples, ontologies, or SPR resources may be loaded by each phase or skill.
- **Repair and Invalidation Graph** — The typed map from a failure class to its root-cause owner, permitted repair scope, frozen state, invalidated descendants, regression suite, and escalation policy.
- **Development Capsule** — The authorized implementation handoff containing the Harness IR, readable specifications, contracts, skill packages, graph manifests, justified scaffolding, tests, tickets, and receipts.
- **Implementation Authorization Gate** — The evidence-backed decision that determines whether a capsule is authorized for production implementation, prototype only, ratification, or blocked.
- **Harness Control Tower** — The event-sourced Pi UI that renders authoritative run state, evidence, decisions, phases, skills, contracts, evaluations, costs, repairs, and authorization.
- **Downstream Harness Effectiveness** — The measured quality, accuracy, predictability, cost, latency, repair efficiency, and Activative fidelity of a harness implemented from the Builder's output.
- **Builder Workflow Runtime** — The executable control plane that runs Builder work through typed nodes combining deterministic code, bounded agents, and governed human gates.
- **Builder Workflow IR** — The canonical machine-readable representation of one Builder workflow, including nodes, actors, contracts, conditions, routes, retries, budgets, isolation, events, and promotion state.
- **Workflow Profile** — A versioned specialization of the Builder Workflow Runtime for a class of work such as new harness compilation, source refresh, migration, benchmark regression, repair, or hotfix.
- **Workflow Node** — One independently owned and testable operation in a Builder workflow with explicit actor type, inputs, outputs, validators, failure routes, and completion criteria.
- **Actor Assignment Matrix** — The explicit allocation of each workflow responsibility to human expertise, bounded agent judgment, deterministic code, or an approved hybrid.
- **Shadow Workflow** — A manually observed end-to-end execution used to capture real steps, handoffs, failures, and evidence before automating the workflow.
- **Workflow Router** — The deterministic or bounded component that selects an approved workflow profile from the request, run state, risk, target, and incident class.
- **Execution Sandbox** — An isolated environment with bounded tools, mounted sources, credentials, compute, filesystem, network, and lifetime for a workflow node or implementation task.
- **Workflow Promotion** — The governed movement of a workflow definition from draft through tested and production states using versioned tests, benchmark evidence, migration policy, and rollback capability.


---

# 4. Doctrine and Product Principles

These principles are binding product behavior. Architecture may choose mechanisms, but it may not weaken their observable consequences.

## P-01 — One Harness, One Content Product

An atomic harness owns one recognizable production promise. Examples, topics, or variants do not create separate harnesses unless the production grammar materially changes.

## P-02 — Evidence Before Inference

Material claims and recommendations remain tied to locked sources, with uncertainty and contradictory authority preserved.

## P-03 — Visual Syntax Before Meaning

The Builder parses components, geometry, relationships, composition variables, and temporal states before assigning visual function or Activative meaning.

## P-04 — Saturation Before Compression

The Builder covers the required evidence surface and records gaps before it generalizes, classifies, or specifies.

## P-05 — Human-Governed Constitution

Agents recommend; humans ratify constitutional, creative-policy, risk, waiver, and irreversible decisions.

## P-06 — One Typed Source of Truth

The Harness IR is authoritative. Documents, OpenSpec, skills, contracts, tests, tickets, and receipts are compiled views.

## P-07 — Deterministic Orchestration, Bounded Stochasticity

Code owns invocation, dependencies, context, validation, routing, and receipts; models perform bounded judgment and creative transformations.

## P-08 — Rich Internal Work, Sparse Handoff

A phase may reason over rich local context but passes minimal complete typed contracts downstream.

## P-09 — Canonical Skill Ecology First

Reuse, adapt, or compose tested capabilities before authorizing a new canonical skill.

## P-10 — JIT Means Phase-Local Compilation

The runtime assembles an ephemeral Execution Capsule from resolved bindings and active branches, not one permanent monolithic prompt.

## P-11 — Minimum Complete Context

A phase receives the smallest context that still satisfies responsibility, evidence, authority, contracts, and completion criteria.

## P-12 — No Production Skill Without Behavioral Evidence

Structure and persuasive prose do not prove a skill changes model behavior reliably.

## P-13 — No Average Compensates a Hard Failure

Evidence, constitutional, atomicity, contract, benchmark-integrity, or false-readiness failures block release regardless of composite score.

## P-14 — Smallest Responsible Repair

Repair the root cause at the responsible layer, invalidate every dependent result, and preserve still-supported state.

## P-15 — No Status Without Evidence

Every meaningful state and human action is backed by events, receipts, and authoritative data.

## P-16 — Shared Activative Core, Category-Owned Form

Activative meaning is shared; visual, temporal, registry, runtime, evaluation, and repair form is category-, profile-, and harness-owned.

## P-17 — Sequencing Is Intelligence

Viewer-state progression, scene or slide roles, timing, continuity, prediction gaps, and payoff are primary Activative capabilities.

## P-18 — Downstream Performance Is the Final Proof

The Builder is evaluated by the harness it causes to be built, not only by its document output.

## P-19 — Controlled Evolution

V2.1 changes through tests, dual compilation, migration receipts, and reference-harness evidence.

## P-20 — Prove One Path Before Generality

Release 1 proves one complete reference harness. General certification requires transfer across the agreed portfolio.

## P-21 — Workflow Over Isolated Loops

A feedback loop is one local edge. The product must engineer the complete end-to-end information flow, actor placement, conditions, validation, and terminal outcomes.

## P-22 — Humans, Agents, and Code in Deliberate Roles

Use deterministic code for precise repeatable work, bounded agents for uncertain judgment, and humans for authority and high-impact ambiguity.

## P-23 — Separate Code from Skill Execution

Production validation, state mutation, routing, and mechanical transformations execute as explicit code-owned nodes rather than hidden tool calls inside one skill.

## P-24 — Manual Before Automation

Release 1 automation is derived from a recorded shadow workflow that exposes the real work, handoffs, failures, and evidence before orchestration is encoded.

## P-25 — Scale Compute Only When It Improves Accepted Outcomes

Additional agents, candidates, or sandboxes require dependency independence, evaluation, budget, and evidence that they improve quality, latency, or risk-adjusted cost.


---

# 5. Features and Functional Requirements

The product is decomposed into coherent behavioral features. Functional Requirements use globally stable IDs so downstream Architecture, Epics, Stories, technical specifications, tests, events, and receipts can reference them even when feature grouping evolves.

| Feature | Title | FR range | FRs | Governing decisions |
| --- | --- | --- | --- | --- |
| F01 | [Governed Product Lifecycle and Run Constitution](05-features/F01-governed-product-lifecycle.md) | FR-001–FR-008 | 8 | D001, D002, D004, D006, D025, D027, D033 |
| F02 | [Configured Evidence Workspace, Source Lock, and Saturation](05-features/F02-configured-evidence-workspace.md) | FR-009–FR-018 | 10 | D003, D005, D006, D007, D022, D023, D028 |
| F03 | [Visual Syntax First and Draft Activative Understanding](05-features/F03-visual-syntax-first.md) | FR-019–FR-031 | 13 | D003, D007, D011, D012, D013, D014, D030, D031 |
| F04 | [Atomicity Classification and Draft Harness Model](05-features/F04-atomicity-draft-harness-model.md) | FR-032–FR-040 | 9 | D008, D009, D010, D011, D030, D031, D033 |
| F05 | [Dependency-Driven Genesis and Human Authority](05-features/F05-dependency-driven-genesis.md) | FR-041–FR-050 | 10 | D002, D009, D010, D011, D019, D025, D027, D028 |
| F06 | [Canonical Harness IR and Artifact Compiler](05-features/F06-canonical-harness-ir.md) | FR-051–FR-059 | 9 | D003, D011, D014, D017, D018, D025, D029, D033 |
| F07 | [Capability Ownership, Modules, Phases, Contexts, and Contracts](05-features/F07-capability-module-phase-contract.md) | FR-060–FR-071 | 12 | D012, D013, D014, D015, D019, D026, D033 |
| F08 | [Reference, SPR, and Minimum Complete Context](05-features/F08-reference-spr-context.md) | FR-072–FR-080 | 9 | D016, D017, D018, D019, D020, D033 |
| F09 | [Canonical Skill Ecology and Skill Design Compiler](05-features/F09-canonical-skill-ecology.md) | FR-081–FR-090 | 10 | D012, D016, D017, D021, D033 |
| F10 | [Skill Composition Recipes and Deterministic JIT Execution Capsules](05-features/F10-skill-composition-jit-capsules.md) | FR-091–FR-102 | 12 | D017, D018, D019, D020, D021, D033 |
| F11 | [Behavioral Evaluation, Benchmark Portfolio, Maturity, and Scorecards](05-features/F11-behavioral-evaluation-benchmarks.md) | FR-103–FR-116 | 14 | D003, D021, D022, D023, D024, D027, D032 |
| F12 | [Event-Sourced Harness Control Tower and Observability](05-features/F12-harness-control-tower.md) | FR-117–FR-126 | 10 | D024, D025, D026, D027, D029 |
| F13 | [Repair, Invalidation, Readiness, and Implementation Authorization](05-features/F13-repair-readiness-authorization.md) | FR-127–FR-136 | 10 | D003, D019, D021, D024, D025, D026, D027, D033 |
| F14 | [Canonical Format Categories, Format Profiles, and Activative Sequencing](05-features/F14-format-categories-sequencing.md) | FR-137–FR-150 | 14 | D004, D007, D008, D013, D030, D031, D032, D033 |
| F15 | [Traceable Development Capsule and Implementation Handoff](05-features/F15-development-capsule-handoff.md) | FR-151–FR-159 | 9 | D001, D003, D011, D015, D021, D027, D029, D032 |
| F16 | [Controlled V2.1 Migration, Compatibility, and Release Governance](05-features/F16-v2-migration-release.md) | FR-160–FR-169 | 10 | D003, D022, D024, D028, D032, D033 |
| F17 | [Three Explicit Compilation Target Profiles](05-features/F17-three-compilation-targets.md) | FR-170–FR-180 | 11 | D001, D004, D005, D006, D011, D013, D027, D029, D032, D033 |
| F18 | [Builder Workflow Runtime and Agentic Execution Factory](05-features/F18-builder-workflow-runtime.md) | FR-181–FR-210 | 30 | D001, D002, D003, D006, D011, D012, D013, D014, D015, D017, D018, D019, D020, D021, D022, D023, D024, D025, D026, D027, D028, D029, D032, D033 |

## Requirements discipline

- Requirements state **capabilities and observable consequences**, not implementation technologies.
- Brownfield context identifies what V2.1 or the prior system already provides and the required delta.
- Architecture owns technical mechanisms and public interfaces.
- Epics group requirements into independently valuable outcomes after Architecture is approved.
- Stories must fit one development-agent context, avoid future dependencies, and carry Given/When/Then acceptance criteria.


---

# F01 — Governed Product Lifecycle and Run Constitution

**User outcome:** A Harness Architect can create, resume, inspect, and govern a compilation run whose target, lifecycle, authority, and legal transitions are explicit.

## Description

This feature turns the Builder from a collection of commands into a governed compiler product. It establishes the run as a versioned constitutional object rather than an informal agent session.

## Brownfield baseline

V2.1 already initializes runs, resolves sources, tracks a decision graph, supports guided and provisional modes, compiles OpenSpec, and issues readiness results. Its lifecycle is valuable but does not yet govern all new IR, category, skill, benchmark, observability, and downstream-certification states.

## Required product delta

Extend the working lifecycle into a target-profiled state machine with explicit events, waivers, resumability, constitutional boundaries, and downstream certification feedback.

## Traceability

- **Decisions:** D001, D002, D004, D006, D025, D027, D033
- **User journeys:** UJ-01, UJ-04, UJ-09, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-TRACE-002, NFR-OBS-001

## Functional Requirements

### FR-001 — Select one explicit compilation target

**Requirement:** The Builder must require each run to select exactly one target profile: Atomic Content Harness, Visual Asset Editor, or Content↔Asset Delegation Contract.

**Consequences (testable):**

- Initialization fails when no target or multiple targets are supplied.
- The selected profile governs required sources, phases, decisions, artifacts, evaluations, and authorization gates.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-002 — Create a stable run identity

**Requirement:** The Builder must create a stable run identifier, target identifier, compiler version binding, operator identity, timestamps, and status before any evidence work begins.

**Consequences (testable):**

- All events and artifacts reference the same run identifier.
- A resumed run preserves identity rather than creating a hidden replacement run.

**Traceability:** Decisions D005, D025; journeys UJ-01.

### FR-003 — Enforce a typed lifecycle state machine

**Requirement:** The Builder must represent the approved lifecycle as typed states and transitions whose prerequisites, actors, outputs, and terminal conditions are machine-validated.

**Consequences (testable):**

- A transition cannot occur when its declared prerequisites are incomplete.
- Illegal transitions produce a blocking event and do not mutate authoritative state.

**Traceability:** Decisions D006, D027; journeys UJ-01, UJ-09.

### FR-004 — Apply target-specific lifecycle profiles

**Requirement:** The shared top-level lifecycle must delegate internal phases, decision nodes, artifacts, and gates to the selected target profile without flattening target-specific behavior.

**Consequences (testable):**

- The three targets can share lifecycle names while producing different required work.
- A target profile cannot omit a shared constitutional stage without an approved waiver.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-005 — Govern lifecycle waivers

**Requirement:** The Builder must support explicit human-authorized lifecycle waivers that state the skipped obligation, rationale, risk, affected decisions, downstream provisional states, and expiration condition.

**Consequences (testable):**

- A waiver generates a receipt and appears in the Control Tower.
- A waiver cannot convert a blocked production gate into full authorization unless the target profile permits that exact waiver class.

**Traceability:** Decisions D002, D006, D027; journeys UJ-09.

### FR-006 — Emit an event for every authoritative transition

**Requirement:** Every state transition, blocker, waiver, decision, invalidation, repair, authorization, and certification update must append a typed event to the Run Ledger.

**Consequences (testable):**

- The current run state can be reconstructed from the IR snapshot plus ledger events.
- No UI-only state change is accepted as authoritative.

**Traceability:** Decisions D025; journeys UJ-09.

### FR-007 — Resume without replaying human decisions

**Requirement:** The Builder must resume an interrupted run from its latest valid checkpoint while preserving ratified decisions, evidence locks, event history, and outstanding actions.

**Consequences (testable):**

- A resumed run does not ask already resolved Genesis questions unless their dependencies were invalidated.
- Corrupted or incompatible checkpoints block with a diagnostic rather than silently resetting.

**Traceability:** Decisions D010, D025; journeys UJ-04.

### FR-008 — Enforce the Builder product boundary

**Requirement:** The lifecycle must prevent the Builder from silently crossing from harness-development compilation into final production-harness implementation.

**Consequences (testable):**

- Generated production logic is rejected unless it is explicitly authorized prototype scaffolding or a deterministic compiler-owned mechanism.
- The Development Capsule records implementation scope and exclusions.

**Traceability:** Decisions D001, D029, D033; journeys UJ-11.

## Known failure and edge conditions

- A target profile is selected after evidence has already been interpreted.
- A lifecycle stage is skipped without a waiver receipt.
- The UI reports progress that is absent from the ledger.
- A resumed run loses or silently rewrites a ratified decision.

## Explicitly out of scope

- Implementing the final content, asset, or delegation runtime.
- General-purpose project management outside the three target profiles.
- Technology selection for storage, queues, or deployment; these belong to Architecture.


---

# F02 — Configured Evidence Workspace, Source Lock, and Saturation

**User outcome:** A Harness Architect can prove exactly which sources and specimens were available, inspected, missing, contradictory, and sufficient before synthesis begins.

## Description

This feature operationalizes Saturation Before Compression. Source presence alone is insufficient: the Builder must establish coverage, provenance, gaps, and authority before it may classify or design.

## Brownfield baseline

V2.1 already reads directories and ZIP archives, validates required sources, creates SOURCE_INSPECTION, SOURCE_LOCK, EVIDENCE_INDEX, SPECIMEN_INDEX, and a saturation report. Its source configuration is generic and some embedded references are not automatically registered.

## Required product delta

Introduce target-specific source profiles, richer coverage contracts, contradiction authority, gap classes, source readiness diagnostics, and explicit waiver effects while retaining read-only archive support.

## Traceability

- **Decisions:** D003, D005, D006, D007, D022, D023, D028
- **User journeys:** UJ-01, UJ-02, UJ-03, UJ-12
- **Cross-cutting NFRs:** NFR-REL-004, NFR-TRACE-001, NFR-TRACE-004, NFR-SEC-003, NFR-SCALE-001

## Functional Requirements

### FR-009 — Define target-specific source profiles

**Requirement:** The Builder must define required, recommended, optional, and prohibited source roles independently for each compilation target and category profile.

**Consequences (testable):**

- A Content Harness, Visual Asset Editor, and Delegation run may require different source sets.
- The resolved profile is stored and versioned with the run.

**Traceability:** Decisions D005, D006; journeys UJ-01.

### FR-010 — Run source-readiness diagnostics before initialization

**Requirement:** The Builder must inspect configured paths, archive readability, source type, expected role, and version hints before committing the run to analysis.

**Consequences (testable):**

- Missing required sources block with actionable diagnostics.
- Recommended or optional omissions are recorded without pretending they were inspected.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-011 — Read directories and archives without mutating sources

**Requirement:** The Builder must index approved directory and ZIP sources in place while preserving source immutability and recorded hashes.

**Consequences (testable):**

- No source file is modified, renamed, or unpacked into its origin by the Builder.
- Derived artifacts are written only to approved run or workspace output locations.

**Traceability:** Decisions D005, D028; journeys UJ-01.

### FR-012 — Require a real target candidate boundary

**Requirement:** The exact target candidate must resolve to a real accessible directory or another target type explicitly supported by its profile; internal archive paths may not be treated as traversable directories without deterministic extraction.

**Consequences (testable):**

- Invalid target boundaries block before specimen indexing.
- The resolved target replaces any placeholder target binding in the run configuration.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-013 — Create an immutable source lock

**Requirement:** The Builder must record source identifiers, canonical paths, cryptographic hashes, sizes, timestamps where available, roles, precedence, and authority status in a Source Lock.

**Consequences (testable):**

- Every evidence reference resolves to one locked source version.
- Changing a locked source creates a new source version and invalidates affected evidence rather than mutating history.

**Traceability:** Decisions D005, D025; journeys UJ-01.

### FR-014 — Build a queryable evidence index

**Requirement:** The Builder must index relevant files, archive entries, documents, schemas, registries, code, media, and prior implementations with provenance and semantic role metadata.

**Consequences (testable):**

- Material Builder recommendations can cite stable evidence references.
- The index distinguishes found content from merely configured sources.

**Traceability:** Decisions D003, D005; journeys UJ-01, UJ-03.

### FR-015 — Inventory every target specimen

**Requirement:** The Builder must assign stable IDs, hashes, media types, dimensions or duration, source paths, duplicate relationships, and analysis status to every target specimen.

**Consequences (testable):**

- All target media is accounted for or explicitly unreadable.
- Duplicates remain traceable but are not silently treated as independent evidence.

**Traceability:** Decisions D007, D023; journeys UJ-02.

### FR-016 — Evaluate a measurable saturation contract

**Requirement:** Each target profile must define the required source coverage, specimen coverage, evidence categories, prior-art inspection, contradiction detection, and traceability conditions needed for saturation.

**Consequences (testable):**

- Saturation cannot pass solely because files exist.
- The saturation matrix shows each required obligation and its evidence.

**Traceability:** Decisions D003, D007; journeys UJ-01, UJ-02.

### FR-017 — Classify evidence gaps and authority conflicts

**Requirement:** The Builder must distinguish missing evidence, unreadable evidence, sparse target evidence, contradictory sources, contradictory authority, and unresolved provenance.

**Consequences (testable):**

- Each gap class has a defined blocker or waiver policy.
- Higher-precedence canonical sources are not silently overridden by lower-precedence references.

**Traceability:** Decisions D005, D007; journeys UJ-01, UJ-09.

### FR-018 — Issue typed saturation outcomes

**Requirement:** The Builder must issue PASS, PASS_WITH_LIMITATIONS, BLOCKED_MISSING_EVIDENCE, BLOCKED_CONTRADICTORY_AUTHORITY, or INSUFFICIENT_TARGET_EVIDENCE with evidence and downstream consequences.

**Consequences (testable):**

- PASS_WITH_LIMITATIONS requires a human waiver and marks affected decisions provisional.
- A blocked saturation outcome prevents atomicity and Genesis.

**Traceability:** Decisions D007, D027; journeys UJ-01, UJ-09.

## Known failure and edge conditions

- A configured source is counted as inspected even though no relevant content was indexed.
- A duplicate specimen inflates evidence strength.
- A missing canonical registry is replaced by an invented local concept.
- Genesis starts despite a blocking saturation status.

## Explicitly out of scope

- General enterprise knowledge management.
- Editing or repairing upstream repositories.
- Automatically resolving substantive contradictions without the declared authority model.


---

# F03 — Visual Syntax First and Draft Activative Understanding

**User outcome:** A Harness Architect can inspect a provenance-preserving draft of what is visibly and temporally present before the Builder generalizes format grammar or proposes Activative meaning.

## Description

This feature introduces Visual Syntactic Parsing as a mandatory hybrid capability. It separates measured and observed composition from function hypotheses, cross-specimen grammar, sequence hypotheses, and draft Activative intelligence.

## Brownfield baseline

The existing Builder doctrine requires Visual Syntax First and BBOX + WHY, but it does not yet implement a production-grade multimodal parse IR, category-adapted temporal parsing, knowledge-status transitions, or interactive overlays.

## Required product delta

Create deterministic specimen preprocessing, typed multimodal parsing, parsing ontologies, validators, independent evaluators, cross-specimen induction, and selective human correction before atomicity.

## Traceability

- **Decisions:** D003, D007, D011, D012, D013, D014, D030, D031
- **User journeys:** UJ-02, UJ-03, UJ-06, UJ-09
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-004, NFR-EVAL-001, NFR-EVAL-002, NFR-CAT-001

## Functional Requirements

### FR-019 — Normalize every visual specimen

**Requirement:** The Builder must deterministically derive stable specimen and frame or slide identities, canvas metadata, aspect ratios, ordering, hashes, and analysis-ready representations.

**Consequences (testable):**

- Every parse output references a normalized specimen identity.
- Normalization failures remain visible and block complete specimen coverage.

**Traceability:** Decisions D007; journeys UJ-02.

### FR-020 — Detect duplicate and near-duplicate visual evidence

**Requirement:** The Builder must calculate exact duplicate relationships and may propose near-duplicate clusters without discarding provenance.

**Consequences (testable):**

- Exact duplicates are not counted as independent support for an invariant.
- Near-duplicate proposals retain confidence and human-review status.

**Traceability:** Decisions D007, D023; journeys UJ-02.

### FR-021 — Produce a typed specimen-level visual syntactic parse

**Requirement:** For every visual specimen, the Builder must identify major components, regions, containers, overlays, sequence markers, images, text roles, and category-relevant state elements using a typed schema.

**Consequences (testable):**

- Every salient component has a stable component ID and knowledge status.
- Omitted or uncertain components are represented explicitly rather than invented or hidden.

**Traceability:** Decisions D007, D012; journeys UJ-02.

### FR-022 — Use a canonical parsing ontology with category adaptations

**Requirement:** Visual Syntactic Parsing must use a canonical capability ontology extended by the selected category and format profile rather than one universal vision prompt.

**Consequences (testable):**

- Carousel parsing can represent slide roles while 2D Character Animation can represent character states.
- Category vocabulary does not leak into unrelated categories.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-023 — Measure normalized component geometry

**Requirement:** Every major spatial component must include validated normalized bounding boxes or an explicit geometry-unavailable status.

**Consequences (testable):**

- BBOX coordinates remain inside the canvas and use one declared coordinate system.
- Geometry validation is deterministic and independent of semantic interpretation.

**Traceability:** Decisions D007, D012; journeys UJ-02.

### FR-024 — Build a spatial relationship graph

**Requirement:** The Builder must record relationships such as alignment, containment, pairing, overlap, anchoring, ordering, gaze, and category-specific scene relations between valid component IDs.

**Consequences (testable):**

- Relationship targets must exist and pass schema validation.
- The graph distinguishes observed spatial relations from inferred functional relations.

**Traceability:** Decisions D007, D014; journeys UJ-02.

### FR-025 — Parse hierarchy and reading order

**Requirement:** The Builder must draft attention hierarchy, reading order, typography roles, color roles, negative-space behavior, and density using evidence-linked fields.

**Consequences (testable):**

- The parse can explain which component dominates first attention and why that conclusion is provisional or measured.
- Typography and color roles are not promoted into invariants from a single unexplained instance.

**Traceability:** Decisions D007; journeys UJ-02.

### FR-026 — Classify composition variables

**Requirement:** The Builder must classify material visual properties as invariant, controlled variable, content slot, optional component, specimen anomaly, or unknown with confidence and supporting specimens.

**Consequences (testable):**

- A topic, niche, or replacement copy cannot become a layout invariant without cross-specimen evidence.
- Single-instance features default to anomaly or unknown unless another authority justifies promotion.

**Traceability:** Decisions D007, D008; journeys UJ-02, UJ-03.

### FR-027 — Parse temporal syntax for time-based evidence

**Requirement:** For video and animation categories, the Builder must identify appearance, persistence, motion, pose or state change, transition, timing, cut, sonic relation, and disappearance across frames or shots.

**Consequences (testable):**

- Temporal relationships use stable state or beat identifiers.
- Static-only categories do not receive artificial motion requirements.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-028 — Separate BBOX observation from WHY hypotheses

**Requirement:** The Builder must store measured geometry separately from visual-function hypotheses and require evidence, confidence, alternatives, and knowledge status for every proposed WHY.

**Consequences (testable):**

- A function hypothesis cannot overwrite a measured or observed field.
- Human ratification can promote an interpretation without rewriting its original provenance.

**Traceability:** Decisions D007, D011; journeys UJ-02.

### FR-029 — Induce cross-specimen visual grammar

**Requirement:** After all relevant specimens are parsed, the Builder must compare them to propose persistent instruments, component grammar, variants, optional branches, anomalies, and forbidden mutations.

**Consequences (testable):**

- Every candidate invariant cites multiple supporting specimens or an explicit canonical authority.
- Competing grammar hypotheses and unresolved evidence are retained for atomicity and Genesis.

**Traceability:** Decisions D007, D008; journeys UJ-02, UJ-03.

### FR-030 — Draft category-native sequence grammar

**Requirement:** The Builder must propose slide-role, scene-role, state-transition, pacing, and operator grammar appropriate to the selected category and format profile.

**Consequences (testable):**

- The sequence draft references observed temporal or cross-frame evidence.
- Sequencing hypotheses remain provisional until Genesis.

**Traceability:** Decisions D007, D030, D031; journeys UJ-02, UJ-06.

### FR-031 — Draft Activative hypotheses after syntax

**Requirement:** Only after syntactic and function parsing may the Builder propose recognition mechanism, hidden pressure, viewer role, prediction gap, intended reaction, memetic expression, and wrong-reading risks.

**Consequences (testable):**

- Activative fields are marked hypothesized and cite the visual or source evidence that motivated them.
- Generated subject matter or business strategy cannot masquerade as specimen observation.

**Traceability:** Decisions D007, D030; journeys UJ-02, UJ-04.

## Known failure and edge conditions

- Semantic meaning is assigned before the component inventory is complete.
- A generated dish example is treated as source evidence.
- One decorative element is promoted into an invariant.
- A video format is parsed only as static screenshots without temporal states.
- Character pose or gaze is ignored in the 2D Character Animation category.

## Explicitly out of scope

- Final media generation.
- Automatic ratification of visual meaning.
- Replacing expert visual review when confidence or category impact is high.


---

# F04 — Atomicity Classification and Draft Harness Model

**User outcome:** A Harness Architect can approve one evidence-backed product boundary and receive a coherent provisional model for Genesis.

## Description

This feature prevents both one-workspace-per-example duplication and premature universal engines. It converts visual, temporal, semantic, runtime, evaluation, and repair evidence into an explicit atomicity decision.

## Brownfield baseline

V2.1 supports atomicity statuses and the prior Builder bundle contains atomicity doctrine. The current system does not yet consume a full Visual Syntax IR, quantify wrong-boundary consequences, or compile the complete Draft Harness Model from one typed source.

## Required product delta

Add a typed atomicity classifier, comparative evidence packets, human ratification, and a provisional Harness IR projection that Genesis can challenge.

## Traceability

- **Decisions:** D008, D009, D010, D011, D030, D031, D033
- **User journeys:** UJ-03, UJ-04, UJ-06
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-004, NFR-CAT-001, NFR-CAT-002, NFR-EVAL-003

## Functional Requirements

### FR-032 — Compare candidate product boundaries

**Requirement:** The Builder must compare specimens or candidate groups across production promise, persistent visual instrument, composition grammar, state machine, semantic workcell, input contract, asset program, runtime ownership, evaluation failures, and repair behavior.

**Consequences (testable):**

- The comparison exposes shared and materially different dimensions.
- Topic, labels, aspect ratio, or folder names alone cannot decide the boundary.

**Traceability:** Decisions D008; journeys UJ-03.

### FR-033 — Assign one typed atomicity status

**Requirement:** Each candidate must receive exactly one status: atomic_harness_candidate, variant_of_existing, dish_family_candidate, format_family_only, needs_clustering, needs_partition, or insufficient_evidence.

**Consequences (testable):**

- The status is schema-validated and evidence-linked.
- A non-atomic status blocks Harness Genesis for that candidate boundary.

**Traceability:** Decisions D008; journeys UJ-03.

### FR-034 — Explain merge and split recommendations

**Requirement:** For every proposed merge or split, the Builder must state what is shared, what differs, whether configuration is sufficient, which evidence supports the conclusion, and which capability or state would break under the alternative.

**Consequences (testable):**

- A merge explains why one runtime and evaluator can safely generate all members.
- A split explains the material grammar, sequencing, runtime, or failure difference.

**Traceability:** Decisions D008, D033; journeys UJ-03.

### FR-035 — Assess wrong-boundary risk

**Requirement:** The Builder must describe the likely implementation, creative, evaluation, migration, and maintenance consequences if the proposed atomicity decision is wrong.

**Consequences (testable):**

- The risk record distinguishes over-splitting from over-merging.
- High-risk uncertainty requires more evidence or a prototype-only path.

**Traceability:** Decisions D008, D027; journeys UJ-03.

### FR-036 — Require human atomicity ratification

**Requirement:** A human Harness Architect must approve, revise, or reject the proposed product boundary before the Builder compiles a Genesis-ready model.

**Consequences (testable):**

- Ratification records the chosen boundary, rejected alternatives, evidence, and rationale.
- The agent cannot self-ratify an atomicity recommendation.

**Traceability:** Decisions D002, D008; journeys UJ-03.

### FR-037 — Compile a Draft Harness Model

**Requirement:** After atomicity ratification, the Builder must compile a provisional model containing identity, production promise, syntax, composition variables, sequence grammar, draft Activative intelligence, inputs and outputs, capabilities, runtime hypotheses, evaluations, repairs, evidence gaps, and category ownership.

**Consequences (testable):**

- All fields derive from locked evidence or explicit hypotheses in the Harness IR.
- The model is complete enough to generate dependency-ready Genesis questions.

**Traceability:** Decisions D009, D011; journeys UJ-04.

### FR-038 — Mark the Draft Harness Model unratified

**Requirement:** Every constitutional field in the Draft Harness Model must carry authority and knowledge status so provisional hypotheses cannot be mistaken for approved design.

**Consequences (testable):**

- Unratified fields are visibly identified in documents and Control Tower views.
- A downstream compiler cannot consume an unratified field when its contract requires ratified authority.

**Traceability:** Decisions D009, D011; journeys UJ-04.

### FR-039 — Expose gaps, confidence, and alternatives

**Requirement:** The Draft Harness Model must retain unresolved evidence gaps, confidence, alternative hypotheses, and decisions required rather than compressing them into a falsely certain narrative.

**Consequences (testable):**

- Each unresolved item maps to a Genesis node or evidence action.
- Low confidence is not hidden by polished prose.

**Traceability:** Decisions D003, D009; journeys UJ-04.

### FR-040 — Freeze the ratified boundary for Genesis

**Requirement:** Genesis may challenge downstream constitutional fields but may not broaden, merge, or split the approved harness boundary without reopening the atomicity decision and invalidating affected work.

**Consequences (testable):**

- Boundary changes follow a formal invalidation event.
- A Genesis answer cannot silently turn an atomic harness into a category-level engine.

**Traceability:** Decisions D008, D010, D033; journeys UJ-04.

## Known failure and edge conditions

- A folder name becomes the harness identity without comparison.
- Two grammars are merged because their topics match.
- The Draft Harness Model presents hypotheses as final decisions.
- Genesis silently broadens the atomic scope.

## Explicitly out of scope

- Implementing the atomic harness.
- Certifying generality beyond the compared specimens.
- Creating category-level abstractions before repeated harness evidence exists.


---

# F05 — Dependency-Driven Genesis and Human Authority

**User outcome:** A Harness Architect can resolve the harness constitution through one evidence-backed decision at a time, resume safely, and see downstream consequences.

## Description

Genesis is the human-governed constitutional compiler. It transforms the unratified Draft Harness Model into an authorized Harness IR through typed decisions rather than an unstructured interview or fixed universal questionnaire.

## Brownfield baseline

V2.1 already has decision definitions, dependency graphs, guided and YOLO modes, ratification, status, and cascade locking. The next Builder must bind decisions directly to IR nodes, evidence, invalidation, category profiles, skills, benchmarks, and authorization.

## Required product delta

Retain the working decision engine while formalizing decision schemas, one-question facilitation, typed effects, contradiction reopening, authority transitions, and Control Tower inspection.

## Traceability

- **Decisions:** D002, D009, D010, D011, D019, D025, D027, D028
- **User journeys:** UJ-04, UJ-09, UJ-11
- **Cross-cutting NFRs:** NFR-REL-002, NFR-TRACE-002, NFR-TRACE-004, NFR-UX-002, NFR-OBS-002

## Functional Requirements

### FR-041 — Define typed Genesis decision nodes

**Requirement:** Every Genesis choice must declare a stable decision ID, target-profile applicability, question, rationale, required evidence, dependencies, options, recommendation policy, authority owner, affected IR paths, invalidation edges, and completion rule.

**Consequences (testable):**

- Decision nodes validate before they enter a run.
- The same decision definition can be versioned without rewriting prior run history.

**Traceability:** Decisions D010, D011; journeys UJ-04.

### FR-042 — Unlock only dependency-ready decisions

**Requirement:** The decision engine must expose a node only when its prerequisite evidence, authority, contracts, and earlier decisions are satisfied.

**Consequences (testable):**

- An operator cannot accidentally answer a decision whose meaning depends on unresolved upstream choices.
- Blocked dependencies are visible with required actions.

**Traceability:** Decisions D010, D019; journeys UJ-04, UJ-09.

### FR-043 — Ask one primary constitutional question per turn

**Requirement:** Guided Genesis must present and resolve one primary decision at a time, keeping any clarification inside that decision before advancing.

**Consequences (testable):**

- The run ledger records one decision outcome per completed turn.
- The agent does not batch unrelated constitutional questions into a single approval request.

**Traceability:** Decisions D010; journeys UJ-04.

### FR-044 — Present an evidence-backed recommendation

**Requirement:** For each decision, the agent must summarize relevant evidence, current Draft Harness Model state, viable alternatives, trade-offs, downstream consequences, and a clear recommended option.

**Consequences (testable):**

- Recommendations cite stable evidence and decision references.
- The recommendation distinguishes facts from inference and does not imply human ratification.

**Traceability:** Decisions D002, D010; journeys UJ-04.

### FR-045 — Record human answer and final decision separately

**Requirement:** The Builder must preserve the operator's answer, agent interpretation, final normalized decision, rationale, authority, timestamp, and any dissent or uncertainty.

**Consequences (testable):**

- A later audit can reconstruct what the human actually said and what was written into the IR.
- Ambiguous answers remain unresolved until normalized and confirmed.

**Traceability:** Decisions D002, D010; journeys UJ-04.

### FR-046 — Update the Harness IR transactionally

**Requirement:** Completing a decision must update all declared IR fields, append a decision event, recompute dependencies, and either commit all effects or none.

**Consequences (testable):**

- Partial decision writes cannot leave the IR inconsistent.
- Generated documents are marked stale until their affected views are recompiled.

**Traceability:** Decisions D010, D011; journeys UJ-04.

### FR-047 — Reopen affected decisions on contradiction

**Requirement:** When new evidence or a later decision conflicts with a resolved node, the Builder must identify the contradiction, reopen the affected node and descendants, and preserve the prior decision as superseded history.

**Consequences (testable):**

- No contradiction is resolved by silently overwriting a ratified value.
- The Control Tower shows the reopening cause and blast radius.

**Traceability:** Decisions D010, D026; journeys UJ-04, UJ-09.

### FR-048 — Support provisional autonomous drafting with ratification

**Requirement:** The Builder may generate provisional decisions in an approved autonomous draft mode, but every required constitutional decision must be ratified before full authorization.

**Consequences (testable):**

- Provisional decisions carry a distinct authority status.
- The ratification list identifies the exact evidence, recommendation, and downstream fields for each pending decision.

**Traceability:** Decisions D002, D010, D027; journeys UJ-04.

### FR-049 — Define a cascade-locked terminal state

**Requirement:** Genesis must reach a terminal state only when all required decisions are resolved, all mandatory IR fields have sufficient authority, no blocking contradiction remains, and all provisional decisions requiring ratification are closed.

**Consequences (testable):**

- Cascade lock is computed, not declared by the agent.
- A later invalidation moves the run out of cascade-locked status.

**Traceability:** Decisions D010, D027; journeys UJ-04.

### FR-050 — Persist complete decision receipts and resumable memory

**Requirement:** The Builder must generate a decision register, per-decision receipts, dependency graph snapshot, and append-only memory sufficient to resume or audit Genesis without loading the full conversation.

**Consequences (testable):**

- A resumed run reconstructs current authority from structured state.
- Conversation prose may support audit but is not the sole memory mechanism.

**Traceability:** Decisions D010, D025; journeys UJ-04.

## Known failure and edge conditions

- A fixed questionnaire asks irrelevant questions while missing category-specific decisions.
- The agent presents several dependent decisions in one approval.
- A later contradiction overwrites history.
- Cascade lock is issued while required provisional decisions remain.

## Explicitly out of scope

- Replacing the human authority owner for constitutional decisions.
- Using Genesis to implement production code.
- Treating agent recommendations as ratification.


---

# F06 — Canonical Harness IR and Artifact Compiler

**User outcome:** All product truth is maintained once in a typed, versioned representation and compiled into consistent human and machine artifacts.

## Description

This feature is the core anti-drift mechanism. The Harness IR stores evidence, knowledge status, authority, decisions, product constitution, architecture intent, skills, graphs, evaluations, repairs, budgets, and implementation traceability.

## Brownfield baseline

V2.1 already generates structured evidence, decision, OpenSpec, and readiness artifacts, but the documents and schemas are not yet views over one complete canonical IR spanning the new architecture.

## Required product delta

Introduce a versioned IR schema, transactional mutation model, artifact compilers, provenance hashes, compatibility migrations, and cross-artifact consistency validation.

## Traceability

- **Decisions:** D003, D011, D014, D017, D018, D025, D029, D033
- **User journeys:** UJ-04, UJ-05, UJ-07, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-003, NFR-TRACE-001, NFR-TRACE-003, NFR-MAINT-001

## Functional Requirements

### FR-051 — Maintain one canonical typed Harness IR

**Requirement:** The Builder must store the authorized product definition in one machine-readable Harness IR whose schema covers identity, evidence, syntax, Activative semantics, phases, contexts, contracts, modules, skills, references, evaluators, repairs, budgets, implementation units, and authorization.

**Consequences (testable):**

- Every material product value has one authoritative IR location.
- Generated documents do not create independent authoritative meanings.

**Traceability:** Decisions D011; journeys UJ-04, UJ-11.

### FR-052 — Attach provenance and authority metadata to material values

**Requirement:** Every material IR node must support evidence references, knowledge status, confidence where applicable, authority status, decision source, version, timestamps, and dependency impact.

**Consequences (testable):**

- Observed, measured, derived, hypothesized, human-decided, and generated values remain distinguishable.
- A value without required provenance fails validation.

**Traceability:** Decisions D007, D011; journeys UJ-02, UJ-04.

### FR-053 — Version IR schemas and migrations

**Requirement:** The Builder must version the Harness IR schema and provide explicit compatibility and migration rules for supported prior versions.

**Consequences (testable):**

- A run cannot be loaded under an incompatible schema without a migration or explicit block.
- Migration events preserve the original version and transformation receipt.

**Traceability:** Decisions D011, D028; journeys UJ-12.

### FR-054 — Compile sharded human-readable specifications

**Requirement:** The artifact compiler must generate readable, linkable, sharded specifications from the IR, including product, visual syntax, Activative program, runtime architecture, skill system, evaluation, repair, and handoff views appropriate to the target.

**Consequences (testable):**

- Every generated section identifies its governing IR nodes.
- Recompilation updates affected shards without changing unrelated authoritative content.

**Traceability:** Decisions D011, D029; journeys UJ-11.

### FR-055 — Compile OpenSpec as a governed view

**Requirement:** The Builder must generate OpenSpec changes, schemas, and implementation governance from the Harness IR while keeping the IR authoritative.

**Consequences (testable):**

- An OpenSpec artifact records its source IR hash and compiler version.
- Manual OpenSpec edits require a formal delta back into the IR or remain non-authoritative.

**Traceability:** Decisions D011, D028; journeys UJ-11.

### FR-056 — Compile machine artifacts from the same IR

**Requirement:** The Builder must compile registries, contracts, graphs, skill manifests, evaluation manifests, repair policies, dashboard configuration, fixtures, traceability maps, and implementation tickets from the same IR.

**Consequences (testable):**

- Every artifact has source IR node references and a content hash.
- Conflicting values across generated artifacts fail the consistency gate.

**Traceability:** Decisions D011, D029; journeys UJ-05, UJ-11.

### FR-057 — Protect generated authoritative artifacts from silent manual drift

**Requirement:** The Builder must distinguish generated authoritative views, editable proposals, and operator annotations and must detect manual changes to generated authoritative files.

**Consequences (testable):**

- An unauthorized edit fails integrity validation or is captured as a proposed IR delta.
- Operator notes can coexist without being mistaken for compiled truth.

**Traceability:** Decisions D011, D033; journeys UJ-11.

### FR-058 — Bind artifacts to compiler and source hashes

**Requirement:** Every generated artifact must record the Builder/compiler version, source IR hash, source node set, generation timestamp, and artifact hash in a manifest.

**Consequences (testable):**

- The exact artifact used by implementation or evaluation can be proven.
- Stale artifacts are detectable after IR changes.

**Traceability:** Decisions D011, D021, D029; journeys UJ-08, UJ-11.

### FR-059 — Validate cross-artifact consistency and completeness

**Requirement:** The Builder must validate that all required target-profile artifacts exist, all references resolve, all requirement and decision IDs are covered, and all generated views agree with the Harness IR.

**Consequences (testable):**

- A missing or contradictory compiled view blocks readiness.
- The validation report lists the exact IR nodes and artifacts involved.

**Traceability:** Decisions D003, D011, D027; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- A Markdown file contains a decision absent from the IR.
- Two generated schemas use different field names for one contract.
- An OpenSpec edit silently changes the constitution.
- An evaluated skill package differs from the artifact listed in the IR.

## Explicitly out of scope

- Selecting the implementation language or database technology.
- Treating all operator notes as authoritative product state.
- Guaranteeing backward compatibility beyond versions explicitly supported by migration policy.


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


---

# F08 — Reference, SPR, and Minimum Complete Context

**User outcome:** Each model-driven phase receives exactly the authoritative doctrine, references, evidence, and creative priming needed for its current responsibility—no more and no less.

## Description

This feature formalizes progressive disclosure and prevents context sediment. It distinguishes canonical references, branch-specific resources, SPR packs, runtime bindings, and phase outputs, and governs their loading and influence.

## Brownfield baseline

Current CMF skills and briefs contain rich doctrine and large contextual packages, but loading behavior is often expressed in prose or broad dependency lists. V2.1 does not yet compile context budgets and must-not-influence rules into each harness runtime.

## Required product delta

Create a reference registry, loading graph, phase context policies, SPR governance, budget ranking, approved compression/retrieval behavior, and auditable context manifests.

## Traceability

- **Decisions:** D016, D017, D018, D019, D020, D033
- **User journeys:** UJ-05, UJ-06, UJ-07, UJ-08
- **Cross-cutting NFRs:** NFR-PERF-002, NFR-PERF-003, NFR-TRACE-001, NFR-SEC-002, NFR-MAINT-002

## Functional Requirements

### FR-072 — Maintain a versioned reference registry

**Requirement:** The Builder must register doctrine, ontologies, registries, examples, counterexamples, templates, provider guidance, rights rules, and SPR resources with stable IDs, versions, hashes, owners, authority, and content roles.

**Consequences (testable):**

- A required reference cannot be named only in prose or by an unregistered ghost variable.
- Reference updates have dependency impact and migration visibility.

**Traceability:** Decisions D016, D019; journeys UJ-07.

### FR-073 — Support explicit loading policies

**Requirement:** Each reference must use a declared loading mode such as always, phase_local, skill_local, conditional, retrieval_only, human_only, or forbidden_at_runtime.

**Consequences (testable):**

- A reference loads only in permitted phases and conditions.
- The compilation receipt explains why each loaded reference was selected.

**Traceability:** Decisions D016; journeys UJ-07.

### FR-074 — Define influence boundaries for references

**Requirement:** References must be able to declare the decisions or outputs they may inform and the domains they must not influence.

**Consequences (testable):**

- A visual parsing ontology cannot determine business strategy or coach identity.
- An evaluator does not receive a creative SPR unless its evaluation protocol explicitly requires it.

**Traceability:** Decisions D016, D021; journeys UJ-06, UJ-08.

### FR-075 — Compile progressive disclosure pointers

**Requirement:** Canonical skills and phase instructions must inline only universally required procedure and use typed context pointers for branch-specific or heavy reference material.

**Consequences (testable):**

- Inactive branches do not consume capsule context.
- A missing required pointer target blocks compilation rather than being improvised.

**Traceability:** Decisions D016, D017, D020; journeys UJ-07.

### FR-076 — Govern SPR as phase-local creative priming

**Requirement:** The Builder must treat Sparse Priming Representation as a conditional creative-presence resource loaded only after evidence, meaning, authority, and wrong-reading locks required by the phase are resolved.

**Consequences (testable):**

- SPR may influence authorized creative search but not rewrite evidence or constitutional decisions.
- SPR is excluded from independent evaluation unless the evaluation design explicitly measures its effect.

**Traceability:** Decisions D016, D017, D030; journeys UJ-06, UJ-07.

### FR-077 — Compile a Context Budget Policy per phase

**Requirement:** Every model-driven phase must declare hard and soft token, latency, and cost budgets, required versus optional context classes, compression permissions, retrieval policies, and budget-failure behavior.

**Consequences (testable):**

- A phase's budget is visible before execution.
- Budget rules are target, category, and model-policy aware.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-078 — Rank context by functional necessity

**Requirement:** The JIT compiler must prioritize phase responsibility, output contract, ratified decisions, bindings, canonical procedure, harness adaptation, direct evidence, constraints, conditional references, examples, and enrichment in that order unless the profile specifies a justified override.

**Consequences (testable):**

- Optional examples cannot displace required evidence or contracts.
- The context manifest records priority decisions.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-079 — Block rather than silently truncate required context

**Requirement:** If required context exceeds the approved budget, the Builder must block and recommend phase splitting, typed compression, retrieval, deduplication, reference redesign, model-policy change, or an authorized budget increase.

**Consequences (testable):**

- Required text is never cut mid-procedure without an approved compiler rule.
- The blocker identifies which resources caused the overflow.

**Traceability:** Decisions D020, D033; journeys UJ-07, UJ-09.

### FR-080 — Emit a complete context manifest

**Requirement:** Every JIT Execution Capsule must list included, excluded, summarized, retrieved, and compressed resources; their hashes; their token contribution; and the rationale for each decision.

**Consequences (testable):**

- A reviewer can reproduce the capsule's context selection.
- Excluded future-phase or evaluator resources are visible rather than silently ignored.

**Traceability:** Decisions D018, D020, D025; journeys UJ-07, UJ-09.

## Known failure and edge conditions

- All available references are loaded because they might be useful.
- An SPR pack influences evidence interpretation.
- Required doctrine is silently summarized below its binding precision.
- A capsule exceeds its context budget without an event.

## Explicitly out of scope

- Authoring every reference resource inside the Builder PRD.
- Using context size as a proxy for intelligence.
- Allowing phase implementers to bypass registered loading rules.


---

# F09 — Canonical Skill Ecology and Skill Design Compiler

**User outcome:** A JIT Skill Maintainer can discover, reuse, adapt, design, compile, and evaluate capabilities without skill sprawl or monolithic prompt documents.

## Description

This feature turns the existing CCP skill doctrine into a canonical capability ecology. It preserves the original CCSB separation between strategic Skill Design Brief and modular implementation while incorporating progressive disclosure, leading words, behavioral testing, and atomic-harness ownership.

## Brownfield baseline

The current system contains real umbrella skills, a detailed Skill Authoring Guide, canonical reasoning modules, Hunter/Analyst/Composer/Commander lanes, and a CCSB design. It lacks one authoritative capability registry, a typed skill IR, consistent distinction between illustrated and production-ready skills, and automated behavioral gates.

## Required product delta

Create a maturity-gated Skill Capability Registry, capability-gap analysis, typed Skill Design Brief compiler, harness adaptations, progressively disclosed packages, and eval-bound artifact identity.

## Traceability

- **Decisions:** D012, D016, D017, D021, D033
- **User journeys:** UJ-05, UJ-07, UJ-08, UJ-11
- **Cross-cutting NFRs:** NFR-EVAL-001, NFR-EVAL-002, NFR-TRACE-003, NFR-MAINT-002, NFR-PORT-001

## Functional Requirements

### FR-081 — Maintain a Canonical Skill Capability Registry

**Requirement:** The Builder must maintain a versioned registry of reusable procedural capabilities with stable IDs, names, responsibilities, input and output contracts, authority lane, failure modes, reasoning modules, maturity, artifact availability, and evaluation receipts.

**Consequences (testable):**

- The registry distinguishes packaged, reference-illustrated, capability-illustrated, experimental, tested, stable, deprecated, and superseded entries.
- A runtime cannot treat a merely illustrated skill as production-ready.

**Traceability:** Decisions D017, D021; journeys UJ-08.

### FR-082 — Organize canonical skills by authority lane

**Requirement:** Every canonical skill must declare its Hunter, Analyst, Composer, or Commander lane without turning the lane into a monolithic agent or nested skill hierarchy.

**Consequences (testable):**

- The lane describes authority and responsibility, not autonomous identity.
- Flat skills remain orchestrator-invoked and independently testable.

**Traceability:** Decisions D012, D017; journeys UJ-05.

### FR-083 — Track skill maturity and plasticity

**Requirement:** Canonical skills and adaptations must use governed maturity states with promotion, change, regression, deprecation, and migration rules.

**Consequences (testable):**

- Stable skills cannot be behaviorally changed without required regression coverage.
- New skills begin in draft or evaluation-pending state.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-084 — Run a formal skill necessity and capability-gap test

**Requirement:** Before creating a JIT Skill, the Builder must determine whether deterministic code, a schema, validator, tool, inline instruction, external reference, human decision, existing canonical skill, or adapter can reliably satisfy the capability.

**Consequences (testable):**

- A rejected skill candidate records the chosen alternative owner.
- A new canonical skill requires evidence that no approved capability covers the need.

**Traceability:** Decisions D012, D017, D033; journeys UJ-05, UJ-08.

### FR-085 — Prefer reuse, adaptation, or adapter composition

**Requirement:** The Builder must attempt exact canonical reuse, harness-local ecological adaptation, or a bounded adapter before authorizing a new canonical capability.

**Consequences (testable):**

- Adaptations preserve the canonical skill's procedural DNA and declare local mutations.
- Overlapping canonical skills trigger redundancy review rather than silent duplication.

**Traceability:** Decisions D017; journeys UJ-08.

### FR-086 — Compile a typed Skill Design Brief

**Requirement:** Every new or materially adapted skill must begin from a reviewable structured brief covering intent, target, context, trigger or program invocation, inputs, action, method, modules, constraints, output artifact, success criteria, failure evidence, and runtime budgets.

**Consequences (testable):**

- The brief remains legible to a product owner before SKILL.md generation.
- Dynamic values are parameterized and no instance-specific content is promoted into the reusable capability.

**Traceability:** Decisions D017, D019; journeys UJ-08.

### FR-087 — Use leading words as tested behavioral anchors

**Requirement:** A skill may declare one or more compact leading words or phrases only when they encode a clear behavioral prior, reduce instruction duplication, and are evaluated against the target failure mode.

**Consequences (testable):**

- The test measures behavioral adoption rather than phrase repetition.
- Weak or colliding leading words are removed through no-op and variance testing.

**Traceability:** Decisions D017, D021; journeys UJ-08.

### FR-088 — Compile portable progressively disclosed skill packages

**Requirement:** The Builder must compile the typed skill definition into a compact SKILL.md plus only justified references, schemas, scripts, examples, templates, evaluation cases, and a manifest.

**Consequences (testable):**

- The main SKILL.md contains the active procedure and checkable completion criteria.
- Heavy or branch-specific reference is loaded through governed context pointers.

**Traceability:** Decisions D016, D017; journeys UJ-07, UJ-08.

### FR-089 — Bind skill packages to evaluation assets

**Requirement:** Every skill package must identify its baseline controls, positive cases, adversarial cases, counterexamples, scoring rubric, maturity requirements, and latest evaluation receipt.

**Consequences (testable):**

- A required production skill without an eligible receipt blocks authorization.
- The evaluated package hash matches the package available to capsule compilation.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-090 — Detect skill no-ops, sediment, and redundancy

**Requirement:** The Builder must analyze whether skill content changes behavior over control, duplicates canonical meaning, contains stale or unreachable branches, or repeats guidance already enforced by code or contracts.

**Consequences (testable):**

- No-op guidance is removed or converted into a stronger tested mechanism.
- The registry preserves one source of truth for each canonical procedural capability.

**Traceability:** Decisions D017, D021, D033; journeys UJ-08.

## Known failure and edge conditions

- A new skill is generated for every model phase.
- A runtime-compiled prompt is promoted into the canonical registry.
- A stable skill is rewritten offline without failure evidence.
- A giant SKILL.md embeds every branch and reference.
- The agent repeats a leading word but the target behavior does not improve.

## Explicitly out of scope

- Making the Skill Registry a universal marketplace.
- Treating skills as autonomous agents.
- Encoding deterministic calculations or routing as prose when code can own them.


---

# F10 — Skill Composition Recipes and Deterministic JIT Execution Capsules

**User outcome:** A generated harness can compile a reproducible, phase-local prompt/program context from approved skills, adaptations, bindings, evidence, references, and contracts at the moment it is needed.

## Description

This feature preserves the original CCP JIT idea—resolving dependent variables and archetype or format branches into a final compiled execution program—while replacing one large monolith with typed, phase-local capsules.

## Brownfield baseline

The Achievement Story Design Brief and CCSB architecture already describe invariant blocks, runtime variables, module composition, compilation gates, and final assembled skills. The new architecture must distinguish durable capabilities from ephemeral execution contexts and make assembly deterministic and receipted.

## Required product delta

Create harness-local adaptations, composition recipes, runtime binding schemas, deterministic assembly, dependency and precedence resolution, degradation policies, context manifests, capsule identity, and unload rules.

## Traceability

- **Decisions:** D017, D018, D019, D020, D021, D033
- **User journeys:** UJ-07, UJ-08, UJ-11
- **Cross-cutting NFRs:** NFR-REL-001, NFR-PERF-002, NFR-PERF-003, NFR-TRACE-003, NFR-PORT-002

## Functional Requirements

### FR-091 — Represent harness-local skill adaptations

**Requirement:** The Harness IR must define how a canonical skill's ontology, procedure, completion criteria, references, failure modes, and evaluation mutate for one atomic harness without creating a new canonical skill identity.

**Consequences (testable):**

- The adaptation records its canonical base version and local delta.
- Changes outside the allowed adaptation surface require canonical skill review.

**Traceability:** Decisions D017; journeys UJ-07, UJ-08.

### FR-092 — Define Skill Composition Recipes

**Requirement:** The Builder must compile reusable recipes declaring the canonical skills, adaptations, reasoning modules, reference branches, runtime bindings, output contracts, and evaluation hooks required for a phase or execution path.

**Consequences (testable):**

- Recipes are parameterized and contain no instance-specific resolved values.
- The recipe compiler validates compatibility among all selected components.

**Traceability:** Decisions D017; journeys UJ-07.

### FR-093 — Compile runtime binding schemas

**Requirement:** Every recipe must declare required, optional, conditional, derived, and forbidden runtime variables; their types; sources; authority; dependencies; defaults; and missing-value behavior.

**Consequences (testable):**

- A missing required binding is detected before prompt assembly.
- Hardcoded instance values cannot replace declared dynamic inputs.

**Traceability:** Decisions D019; journeys UJ-07.

### FR-094 — Assemble capsules through deterministic code

**Requirement:** The generated harness must use a deterministic JIT compiler—not a free-form model decision—to select authorized skills, versions, branches, references, bindings, contracts, and context for a ready phase.

**Consequences (testable):**

- Identical compiler inputs produce the same capsule bytes or an explicit nondeterminism receipt.
- The execution model cannot choose to omit a required skill or load an unauthorized branch.

**Traceability:** Decisions D018; journeys UJ-07.

### FR-095 — Resolve binding dependencies before compilation

**Requirement:** The JIT compiler must topologically resolve upstream contracts, human decisions, deterministic derived values, and conditional variables before assembling instructions.

**Consequences (testable):**

- Circular dependencies block with a traceable diagnostic.
- A downstream binding is recomputed when an upstream value changes.

**Traceability:** Decisions D019; journeys UJ-07.

### FR-096 — Apply typed authority and precedence rules

**Requirement:** The compiler must resolve conflicts using field-specific authority and precedence rules rather than a generic prompt-time judgment.

**Consequences (testable):**

- A ratified constitutional value cannot be overridden by an unratified runtime suggestion.
- Every conflict resolution or block is receipted.

**Traceability:** Decisions D019; journeys UJ-07, UJ-09.

### FR-097 — Enforce approved degradation policies

**Requirement:** When a value or reference is unavailable, the compiler may continue only through a target- and field-specific degradation policy that defines substitutes, quality impact, provisional status, and authorization ceiling.

**Consequences (testable):**

- The model cannot invent a required missing value.
- Degraded capsules are visibly marked and cannot exceed their allowed readiness state.

**Traceability:** Decisions D019, D027; journeys UJ-07.

### FR-098 — Compile Minimum Complete Context

**Requirement:** The compiler must assemble the smallest complete authorized context for the active phase using the Context Budget Policy and Reference and Loading Graph.

**Consequences (testable):**

- Inactive archetype, format, or evaluator branches are excluded.
- All completion criteria and required evidence remain present.

**Traceability:** Decisions D020; journeys UJ-07.

### FR-099 — Emit a complete JIT capsule package

**Requirement:** Each compilation must produce a typed Execution Capsule, compiled instructions or program input, context manifest, resolved binding manifest, output-contract binding, and compilation receipt.

**Consequences (testable):**

- The package can be executed without consulting hidden conversation history.
- A reviewer can inspect every included and excluded component.

**Traceability:** Decisions D018, D020; journeys UJ-07.

### FR-100 — Bind exact versions and hashes

**Requirement:** The capsule must record canonical skill versions, adaptation versions, recipe version, reference hashes, evidence lock, model policy, compiler version, output contract, and compiled prompt or program hash.

**Consequences (testable):**

- Evaluation and production can prove they used the same capsule identity.
- Changing any bound input yields a distinct capsule identity.

**Traceability:** Decisions D018, D021; journeys UJ-08.

### FR-101 — Treat capsules as ephemeral phase-local artifacts

**Requirement:** A JIT Execution Capsule must declare its owning phase, lifetime, unload policy, downstream exposure, and prohibition against automatic canonical promotion.

**Consequences (testable):**

- Downstream phases receive the typed output contract rather than inherited capsule context by default.
- Expired capsules remain auditable but are not reused under changed bindings.

**Traceability:** Decisions D017, D020; journeys UJ-07.

### FR-102 — Preserve deterministic assembly and bounded stochastic execution

**Requirement:** The runtime architecture must keep context selection, dependency resolution, validation, and routing deterministic while assigning only the bounded semantic or creative transformation to the model program.

**Consequences (testable):**

- The capability ownership map can identify which part of an execution was stochastic.
- Critical orchestration cannot migrate into prompt prose without an approved architecture delta.

**Traceability:** Decisions D012, D018, D033; journeys UJ-05, UJ-07.

## Known failure and edge conditions

- The agent freely decides what context to include.
- A fixed prompt loads every possible branch.
- A missing binding is filled with plausible invented content.
- A capsule is reused after upstream decisions change.
- A compiled capsule is registered as a canonical skill without a capability-gap process.

## Explicitly out of scope

- Executing the final model call inside the Builder specification product.
- Selecting one mandatory model provider.
- Promoting every legacy design brief unchanged into a runtime capsule.


---

# F11 — Behavioral Evaluation, Benchmark Portfolio, Maturity, and Scorecards

**User outcome:** The Builder team can prove which capabilities and Builder versions improve real harness design and downstream performance, while preventing averages from concealing critical failures.

## Description

This feature makes 'best' empirical. It evaluates each skill layer, the Builder specification output, implementation friction, and the resulting harness using real, adversarial, transfer, and protected cases with repeated-run stability.

## Brownfield baseline

V2.1 has structural validation and readiness receipts, and the Activative bundle has reference evaluators and goldens, but the current checks are not a full behavioral benchmark and some evaluators rely on field-presence heuristics rather than semantic quality.

## Required product delta

Create layered skill evaluation, staged benchmark targets, protected corpora, controlled mutations, multidimensional scorecards, hard gates, repeated fresh-context statistics, and downstream feedback ingestion.

## Traceability

- **Decisions:** D003, D021, D022, D023, D024, D027, D032
- **User journeys:** UJ-08, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-TRACE-003

## Functional Requirements

### FR-103 — Evaluate every skill-system layer

**Requirement:** The Builder must define distinct evaluation suites for Canonical Skills, harness adaptations, composition recipes, JIT capsules, and end-to-end phase behavior.

**Consequences (testable):**

- A passing canonical skill does not automatically certify a faulty harness adaptation.
- Evaluation failures route to the responsible layer.

**Traceability:** Decisions D021, D026; journeys UJ-08.

### FR-104 — Require a no-guidance control

**Requirement:** Behavior-shaping skills and prompt guidance must be compared with a realistic control that omits the candidate guidance.

**Consequences (testable):**

- If the control does not exhibit the target failure, the Builder flags the skill's necessity claim.
- Improvements are reported as deltas, not only absolute scores.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-105 — Run repeated fresh-context trials

**Requirement:** Important stochastic evaluations must execute multiple fresh-context repetitions per variant and record mean, minimum, variance, failure frequency, and confidence estimates.

**Consequences (testable):**

- Single lucky runs cannot support maturity promotion.
- The evaluation manifest declares repetition count and randomization policy.

**Traceability:** Decisions D021, D024; journeys UJ-08, UJ-12.

### FR-106 — Generate positive, adversarial, missing-evidence, and pressure cases

**Requirement:** Skill and phase suites must include correct applications, near-misses, counterexamples, insufficient inputs, contradictions, tempting irrelevant context, and pressure to violate a rule.

**Consequences (testable):**

- The suite tests whether the capability knows when not to apply.
- Pressure scenarios require the agent to act rather than merely recite doctrine.

**Traceability:** Decisions D021, D023; journeys UJ-08.

### FR-107 — Promote maturity only through stored receipts

**Requirement:** Draft, evaluation_pending, experimental, tested, stable, deprecated, and superseded maturity transitions must require target-specific evaluation evidence and regression policies.

**Consequences (testable):**

- A required skill below the target's maturity threshold blocks full authorization.
- A stable skill change triggers all required dependent regressions.

**Traceability:** Decisions D021, D027; journeys UJ-08.

### FR-108 — Verify evaluated artifact identity

**Requirement:** The evaluation system must bind exact source IR, skill package, adaptation, recipe, capsule, compiler, model policy, dataset, and scoring versions.

**Consequences (testable):**

- The shipped artifact hash matches the evaluated artifact hash.
- A changed dependency invalidates the applicable receipt.

**Traceability:** Decisions D021; journeys UJ-08.

### FR-109 — Maintain a staged benchmark portfolio

**Requirement:** The Builder must use one mandatory primary reference harness, contrasting transfer harnesses, and later Visual Asset Editor and Delegation targets before general certification.

**Consequences (testable):**

- Release 1 cannot claim generality beyond its passed reference slice.
- Transfer targets are selected for materially different visual, sequencing, runtime, or asset grammars.

**Traceability:** Decisions D022, D032; journeys UJ-12.

### FR-110 — Maintain a layered versioned benchmark corpus

**Requirement:** Each benchmark target must contain real specimens, expert goldens, known failures, adversarial near-misses, incomplete or contradictory evidence, controlled mutations, transfer cases, and protected release cases.

**Consequences (testable):**

- Every case has stable IDs, expected behavior, scoring rules, and source provenance.
- Protected labels are not exposed to the Builder during ordinary development runs.

**Traceability:** Decisions D023; journeys UJ-12.

### FR-111 — Generate controlled mutation tests

**Requirement:** The benchmark system must support one-variable mutations such as preserving topic while changing grammar, preserving grammar while changing topic, removing a sequence invariant, swapping semantic polarity, or injecting irrelevant style evidence.

**Consequences (testable):**

- The expected decision explains which invariant changed.
- Mutation cases test causal understanding rather than visual similarity.

**Traceability:** Decisions D023; journeys UJ-02, UJ-03, UJ-12.

### FR-112 — Protect release-gate benchmark integrity

**Requirement:** Protected benchmark access, label changes, scoring changes, and case retirement must be governed, versioned, and audited.

**Consequences (testable):**

- A release report discloses any benchmark change since the baseline.
- Known answer leakage is a hard release failure.

**Traceability:** Decisions D023, D024; journeys UJ-12.

### FR-113 — Score independent quality dimensions

**Requirement:** Builder evaluation must report evidence understanding, visual and temporal understanding, atomicity, product architecture, skill system, evaluation and repair quality, implementation readiness, and downstream performance as separate dimensions.

**Consequences (testable):**

- The full scorecard remains visible even when a composite trend score is calculated.
- Target profiles may define additional category-specific dimensions.

**Traceability:** Decisions D024; journeys UJ-12.

### FR-114 — Enforce hard release gates

**Requirement:** Critical unsupported decisions, evidence failures, wrong atomicity, contract contradictions, silent rewrites, untested required skills, benchmark leakage, false readiness, and anti-goal violations must fail release regardless of average score.

**Consequences (testable):**

- Each hard gate maps to a test or review receipt.
- A high composite score cannot override a failed hard gate.

**Traceability:** Decisions D024, D033; journeys UJ-12.

### FR-115 — Report repeated-run stability

**Requirement:** Release reports must include distribution and dominant failure patterns for stochastic dimensions rather than a single run score.

**Consequences (testable):**

- Thresholds may include minimum and variance limits in addition to mean score.
- A highly variable candidate can fail despite a strong best run.

**Traceability:** Decisions D024; journeys UJ-12.

### FR-116 — Ingest downstream implementation and harness results

**Requirement:** The Builder benchmark system must accept implementation questions, spec deltas, test failures, latency and cost, repair rounds, first-pass acceptance, human preference, wrong-reading outcomes, and certification results linked to the Builder version that produced the capsule.

**Consequences (testable):**

- Builder quality can be compared causally across releases.
- Downstream evidence updates benchmarks through governed online refinement rather than unreviewed batch rewrites.

**Traceability:** Decisions D003, D022, D028; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- A skill is approved because its Markdown looks complete.
- One successful run is presented as proof.
- A composite average hides a wrong atomicity decision.
- Protected benchmark answers enter development context.
- A Builder release is evaluated only on structural artifact counts.

## Explicitly out of scope

- Training foundation models.
- Optimizing benchmarks without domain-expert governance.
- Defining final numeric thresholds before baseline calibration.


---

# F12 — Event-Sourced Harness Control Tower and Observability

**User outcome:** Operators can see what is happening, why, what evidence supports it, who owns the next action, what changed, what was invalidated, and what remains before authorization.

## Description

The Pi Control Tower is the human-facing control plane for the Builder. It renders authoritative state from the Harness IR, Run Ledger, Decision Register, Artifact Registry, and receipts and provides only governed, receipted actions.

## Brownfield baseline

V2.1 exposes CLI status and filesystem artifacts. Parallel workspaces include runbooks and verification, but there is no unified live visual interface for specimen overlays, phase graphs, decisions, skills, contracts, evaluation, repair, cost, and readiness.

## Required product delta

Define event schemas, read models, dashboard manifests, evidence viewers, graph views, cost telemetry, human command surfaces, and integrity rules preventing the UI from becoming a second source of truth.

## Traceability

- **Decisions:** D024, D025, D026, D027, D029
- **User journeys:** UJ-01, UJ-02, UJ-04, UJ-08, UJ-09, UJ-10, UJ-11
- **Cross-cutting NFRs:** NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-UX-001, NFR-UX-002

## Functional Requirements

### FR-117 — Show a run overview

**Requirement:** The Control Tower must display target, category and format profile, lifecycle stage, overall status, active blockers, pending human decisions, authorization trajectory, elapsed time, and actual versus budgeted cost and tokens.

**Consequences (testable):**

- Every status links to its authoritative event or receipt.
- Unknown or stale data is shown explicitly rather than inferred.

**Traceability:** Decisions D025; journeys UJ-01, UJ-09.

### FR-118 — Render the Phase and Context Graphs

**Requirement:** Operators must be able to inspect each phase's state, dependencies, executor, active capsule, inputs, outputs, completion criteria, context manifest, failure owner, and timestamps.

**Consequences (testable):**

- Blocked phases display missing prerequisites and next actions.
- Parallel and invalidated paths are visually distinguishable.

**Traceability:** Decisions D013, D025; journeys UJ-09.

### FR-119 — Expose evidence and visual understanding

**Requirement:** The Control Tower must provide source coverage, specimen inventory, contact sheets, frame or slide navigation, parse overlays, BBOX maps, relationship graphs, composition variables, confidence, knowledge status, gaps, and contradictions.

**Consequences (testable):**

- Clicking a component reveals supporting specimens and function hypotheses.
- Human corrections produce governed events and do not edit source evidence.

**Traceability:** Decisions D007, D025; journeys UJ-02, UJ-09.

### FR-120 — Expose Genesis decisions and authority

**Requirement:** The UI must show decision dependencies, recommendations, evidence, human answers, final decisions, authority status, reopened nodes, waivers, and downstream effects.

**Consequences (testable):**

- The operator can distinguish provisional, ratified, superseded, and invalidated decisions.
- Decision actions invoke the same governed command path as CLI or API actions.

**Traceability:** Decisions D010, D025; journeys UJ-04, UJ-09.

### FR-121 — Expose skills, recipes, and capsules

**Requirement:** The UI must show selected canonical skills, harness adaptations, composition recipes, maturity, behavioral results, loaded references, context inclusion and exclusion, capsule hashes, budgets, and model policy.

**Consequences (testable):**

- An ineligible skill is visibly linked to the blocker it creates.
- The exact evaluated and compiled identities can be compared.

**Traceability:** Decisions D017, D018, D021, D025; journeys UJ-08, UJ-09.

### FR-122 — Expose contracts and module ownership

**Requirement:** Operators must be able to inspect producer and consumer graphs, contract versions and authority, module ownership, test seams, compatibility, and invalidation edges.

**Consequences (testable):**

- Orphan contracts and ownership conflicts are highlighted.
- The view traces from a requirement to its module and contract.

**Traceability:** Decisions D014, D015, D025; journeys UJ-05, UJ-09.

### FR-123 — Expose evaluations and repair history

**Requirement:** The UI must show score dimensions, hard gates, failed cases, repetition distributions, dominant failure patterns, root-cause owner, repair attempts, invalidated artifacts, and before/after results.

**Consequences (testable):**

- A reviewer can move from a score failure to the exact evidence and repair route.
- Repair history remains append-only.

**Traceability:** Decisions D024, D025, D026; journeys UJ-09, UJ-10.

### FR-124 — Track cost, latency, and context usage

**Requirement:** Every deterministic and stochastic operation must report timing, tokens where applicable, model or provider, retries, cache behavior, and budget status to the observability system.

**Consequences (testable):**

- The UI can aggregate per phase, run, target, skill, and accepted Development Capsule.
- Cost data does not replace quality dimensions.

**Traceability:** Decisions D020, D024, D025; journeys UJ-07, UJ-12.

### FR-125 — Provide governed human actions

**Requirement:** The Control Tower may support approve, reject, request evidence, correct a parse, ratify, waive, trigger targeted repair, compare releases, freeze, and export actions only through typed commands that validate authority and append receipts.

**Consequences (testable):**

- Unauthorized actions are rejected without state mutation.
- Every successful action shows its event and affected state.

**Traceability:** Decisions D002, D025, D027; journeys UJ-09.

### FR-126 — Prevent the UI from becoming a second source of truth

**Requirement:** All Control Tower read models must derive from authoritative IR, ledger, registries, and receipts; UI caches and local component state may not define product truth.

**Consequences (testable):**

- A rebuild from authoritative stores reproduces the displayed run state.
- Conflicting cache data is discarded or marked stale.

**Traceability:** Decisions D011, D025, D033; journeys UJ-09.

## Known failure and edge conditions

- A phase is shown as passed without a receipt.
- The UI corrects an IR value directly without a command event.
- A visual overlay hides low confidence or missing specimens.
- Cost is tracked only after final completion.
- A stale dashboard continues to display authorization.

## Explicitly out of scope

- A general analytics platform unrelated to Builder operations.
- Replacing canonical Markdown/JSON exports.
- Selecting a specific frontend framework in the PRD.


---

# F13 — Repair, Invalidation, Readiness, and Implementation Authorization

**User outcome:** A reviewer can resolve failures at the smallest responsible layer and authorize only the exact implementation scope supported by evidence, architecture, skill maturity, benchmarks, and human decisions.

## Description

This feature separates failure diagnosis, repair, readiness, and authorization. It prevents whole-run resets, symptom patches, false completion, and implementation that outruns its evidence.

## Brownfield baseline

V2.1 produces readiness receipts and supports non-PASS states. The next Builder must connect every failure to typed repair ownership, precise invalidation, targeted regression, prototype-only authorization, and Control Tower evidence.

## Required product delta

Create failure taxonomy, root-cause protocol, Repair and Invalidation Graph, escalation, readiness hard gates, authorization outcomes, prototype charters, and immutable receipts.

## Traceability

- **Decisions:** D003, D019, D021, D024, D025, D026, D027, D033
- **User journeys:** UJ-09, UJ-10, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-004, NFR-TRACE-003, NFR-EVAL-003, NFR-OBS-002, NFR-SEC-001

## Functional Requirements

### FR-127 — Define a typed failure taxonomy

**Requirement:** The Builder must classify evidence, visual parse, atomicity, authority, contract, module, skill, capsule, benchmark, budget, provider, observability, migration, and downstream implementation failures with stable codes.

**Consequences (testable):**

- Every blocking failure maps to one primary taxonomy entry.
- Unknown failures remain explicit and require triage rather than being forced into an unrelated repair route.

**Traceability:** Decisions D026; journeys UJ-09, UJ-10.

### FR-128 — Require root-cause investigation before repair

**Requirement:** A repair may not be proposed until the Builder records the observed symptom, reproduction or evidence, affected boundary, competing hypotheses, and selected root cause with confidence.

**Consequences (testable):**

- The repair receipt links to the root-cause record.
- Repeated guess-and-patch attempts trigger escalation.

**Traceability:** Decisions D026; journeys UJ-10.

### FR-129 — Compile a Repair and Invalidation Graph

**Requirement:** For each known failure class, the Builder must define the responsible phase or capability, permitted repair fields, frozen state, invalidated descendants, regression suite, escalation conditions, and authority needed.

**Consequences (testable):**

- A repair cannot edit fields outside its permitted scope.
- All declared descendants become stale or invalidated after the repair.

**Traceability:** Decisions D026; journeys UJ-10.

### FR-130 — Preserve unaffected upstream state

**Requirement:** Targeted repairs must retain source locks, measured observations, ratified decisions, contracts, and artifacts that remain supported by evidence.

**Consequences (testable):**

- The repair plan lists preserved and invalidated state before mutation.
- A local rendering defect cannot rewrite Activative policy.

**Traceability:** Decisions D026, D033; journeys UJ-10.

### FR-131 — Rerun targeted regression suites

**Requirement:** After repair, the Builder must rerun all tests and benchmarks required by the repaired capability and every affected descendant, including protected cases where policy permits.

**Consequences (testable):**

- A repair is not complete until required regressions pass or remain visibly blocked.
- Regression scope is derived from dependency impact rather than manually guessed.

**Traceability:** Decisions D021, D026; journeys UJ-10.

### FR-132 — Escalate repeated or constitutional failures

**Requirement:** The Builder must require human review when a repair changes a ratified constitutional decision, broadens the harness boundary, modifies a stable canonical skill, encounters contradictory doctrine, or fails repeatedly beyond the configured threshold.

**Consequences (testable):**

- Escalation freezes further automated repair of the affected scope.
- The Control Tower displays options, evidence, and affected authority.

**Traceability:** Decisions D002, D026; journeys UJ-09, UJ-10.

### FR-133 — Evaluate an evidence-backed readiness gate

**Requirement:** Readiness must validate evidence saturation, atomicity, constitutional authority, Harness IR consistency, phases, contexts, contracts, modules, skill maturity, benchmark results, repair coverage, observability, budgets, and target-specific requirements.

**Consequences (testable):**

- Document completeness alone cannot satisfy readiness.
- Each readiness result lists every passed and failed hard gate.

**Traceability:** Decisions D003, D027; journeys UJ-11.

### FR-134 — Issue typed authorization outcomes

**Requirement:** The Builder must issue AUTHORIZED_FOR_IMPLEMENTATION, AUTHORIZED_FOR_PROTOTYPE_ONLY, NEEDS_RATIFICATION, BLOCKED_EVIDENCE, BLOCKED_SKILL_MATURITY, BLOCKED_BENCHMARK, BLOCKED_ARCHITECTURE, or another target-profiled blocking status.

**Consequences (testable):**

- Only the full authorized state permits production implementation.
- The status is recomputed after invalidation or new evidence.

**Traceability:** Decisions D027; journeys UJ-11.

### FR-135 — Govern prototype-only authorization

**Requirement:** A prototype authorization must define the empirical question, allowed implementation scope, permitted artifacts, provisional decisions, required evidence return, disposal or migration policy, budget, and promotion conditions.

**Consequences (testable):**

- Prototype code cannot be mistaken for authorized production logic.
- Prototype results flow back to the relevant decision, benchmark, or architecture node.

**Traceability:** Decisions D027, D032; journeys UJ-11, UJ-12.

### FR-136 — Generate immutable readiness and authorization receipts

**Requirement:** Every readiness and authorization decision must bind the exact Harness IR, source lock, category and profile versions, skill and benchmark receipts, waivers, compiler version, status, scope, and signatories.

**Consequences (testable):**

- Implementation can verify the capsule and receipt identity before starting.
- A changed dependency invalidates the prior authorization.

**Traceability:** Decisions D021, D027, D029; journeys UJ-11.

## Known failure and edge conditions

- The Builder reruns the full pipeline for a local parse defect.
- A repair changes a ratified decision without reopening Genesis.
- Readiness passes because every file exists.
- Prototype-only work is deployed as production.
- An authorization receipt remains valid after its source IR changes.

## Explicitly out of scope

- Automatically resolving all implementation contradictions without human or architecture review.
- Guaranteeing that an authorized design will never require a governed delta.
- Treating a prototype as a substitute for benchmark certification.


---

# F14 — Canonical Format Categories, Format Profiles, and Activative Sequencing

**User outcome:** Each Atomic Content Harness is compiled through the correct category and format constitution, preserving shared Activative meaning while generating category-native conversational, visual, temporal, registry, runtime, evaluation, and repair architecture.

## Description

This feature establishes the nested content architecture: Shared Activative Core → Canonical Format Category → Category Format Profile → Atomic Harness. It recognizes sequencing as intelligence, gives 2D Character Animation its own registry-driven production substrate, and recognizes Conversational Activation / Human Expression as a full category whose source material is human reaction.

## Brownfield baseline

The Visual Syntax corpus contains eight short-form editing formats, Carousel and Supervisual corpora, and reference doctrine. Existing parallel packs classify atomic harnesses, but the Builder does not yet enforce five category constitutions or category-adapted parsing and sequencing as one typed system.

## Required product delta

Create the Shared Activative Core contract, five category constitutions, format profiles, character and sequence registries, category-native skill requirements, and atomic overlay rules with regression and migration governance.

## Traceability

- **Decisions:** D004, D007, D008, D013, D030, D031, D032, D033
- **User journeys:** UJ-02, UJ-03, UJ-05, UJ-06, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-CAT-001, NFR-CAT-002, NFR-CAT-003, NFR-EVAL-004, NFR-PORT-002

## Functional Requirements

### FR-137 — Define a constitution-complete Shared Activative Core

**Requirement:** The Builder must provide a category-independent Activative contract covering source premise, Coach or Guest Identity DNA, Context Premise, resonance, Matrix of Edging, Activative Intelligence Pack identity, hidden pressure, activation directions, roles, stance, stakes, identity urges, participation design, intended reaction, smallest useful commitment, evidence provenance, evaluation contract, and wrong-reading locks.

**Consequences (testable):**

- The shared core supplies meaning without owning final conversational, visual, or temporal form.
- Sparse downstream tokens retain references to the rich frozen Activative Intelligence objects, and category or harness layers cannot silently rewrite them.

**Traceability:** Decisions D030; journeys UJ-06.

### FR-138 — Insert a mandatory category layer

**Requirement:** Every Atomic Content Harness must bind exactly one Canonical Format Category between the Shared Activative Core and its atomic constitution.

**Consequences (testable):**

- Category selection occurs before category-specific parsing and architecture compilation.
- A harness cannot combine category laws without an explicit multi-surface product decision outside this PRD's atomic boundary.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-139 — Support five canonical categories

**Requirement:** The initial category registry must include Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression with stable IDs and governance owners.

**Consequences (testable):**

- Every content harness maps to one of the five or blocks as an unsupported category candidate.
- Category names and IDs are used consistently across IR, documents, benchmarks, and UI.

**Traceability:** Decisions D031; journeys UJ-06.

### FR-140 — Govern versioned category constitutions

**Requirement:** Each category must own a versioned constitution defining production surface, specimen types, visual and temporal parsing, composition ontology, sequence model, runtime families, canonical skill requirements, registries, evaluation dimensions, repair classes, observability, compatibility, benchmarks, and migration policy.

**Consequences (testable):**

- A constitution change triggers impact analysis across dependent profiles and harnesses.
- No category is production-certified without its required benchmark suite.

**Traceability:** Decisions D031; journeys UJ-06, UJ-12.

### FR-141 — Support category-local format profiles

**Requirement:** A category constitution must support governed format profiles that specialize parsing, sequencing, state, runtime, skill, evaluation, and repair rules before the atomic harness overlay.

**Consequences (testable):**

- Profiles remain versioned and independently benchmarkable.
- A format profile is not treated as a cosmetic theme variable.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-142 — Represent the edited-video format mapping

**Requirement:** The Short-Form Edited Video category must support the governed profiles for Format 01 Story Video, Format 03 Living Commentary, Format 04 Conscious Reaction, Format 05 Silent Dialogue Theatre, Format 06 Data Scale Race, Format 07 Direct Coaching A-Roll, and Format 08 Poetic Quote Theatre.

**Consequences (testable):**

- The mapping is canonical and does not silently include Format 02.
- Each profile may resolve into one or more atomic harnesses through evidence-based classification.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-143 — Represent Format 02 under 2D Character Animation

**Requirement:** The 2D Character Animation category must initially contain the Format 02 Minimal Coach Theatre profile and must not be collapsed into generic edited video.

**Consequences (testable):**

- Its category profile requires character-performance and continuity architecture.
- General icon or data animation does not automatically enter the character category.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-144 — Compile 2D character-performance registries

**Requirement:** The Format 02 profile must require versioned character identity, pose, expression, gesture, gaze, prop and attachment, animation primitive, character state, scene relationship, camera and framing, transition, sonic cue, and compatibility registries as applicable.

**Consequences (testable):**

- Semantic character states resolve to stable registry IDs before runtime composition.
- Invalid pose, expression, gesture, or prop combinations fail compatibility validation.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-145 — Use category-specific syntax parsing

**Requirement:** The syntax-parsing capability must load category and format ontologies appropriate to the production substrate, including conversational turn and Expression Moment parsing where applicable.

**Consequences (testable):**

- Carousels parse slide roles; Supervisuals parse one-frame hierarchy; video parses time states; 2D animation parses character performance; conversational harnesses parse Activative Calls, reactions, turn relationships, timecodes, expression functions, landings, and micro-commitments.
- The canonical parser procedure remains reusable while category output fields remain distinct.

**Traceability:** Decisions D007, D030, D031; journeys UJ-02, UJ-06.

### FR-146 — Use category-specific temporal, conversational, and sequence parsing

**Requirement:** Sequence-bearing categories must derive observed and hypothesized structure using category-native state, beat, turn, transition, continuity, pacing, silence, and sonic relationships.

**Consequences (testable):**

- Carousels represent swipe sequence without pretending to have frame-time motion.
- Supervisuals declare one-frame attention order, while conversational profiles represent question → reaction → follow-up → elevation/close without scripting the guest landing.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-147 — Compile category-adapted Activative Sequencing Intelligence

**Requirement:** Every sequence-bearing harness must receive a format-adapted capability that translates ratified Activative meaning and parsed syntax into viewer or participant roles, state beats, prediction gaps, scene, slide, or conversational-turn roles, transitions, asset or expression states, pacing, silence or sonic cues, payoff, intended reaction, and smallest useful commitment.

**Consequences (testable):**

- Sequence decisions cite Activative contracts and category-native syntax.
- Sequencing is independently evaluated and repairable rather than hidden inside final composition or generic question generation.

**Traceability:** Decisions D030; journeys UJ-06.

### FR-148 — Compile category-owned runtime, evaluation, and repair rules

**Requirement:** Each category and profile must contribute its own runtime constraints, invariant tests, quality dimensions, wrong-reading classes, continuity checks, repair ownership, and required telemetry.

**Consequences (testable):**

- A Supervisual is not evaluated by video pacing metrics.
- A 2D character continuity failure routes to character-state or scene composition rather than generic visual style repair.

**Traceability:** Decisions D031; journeys UJ-06, UJ-10.

### FR-149 — Preserve atomic creative ownership

**Requirement:** The atomic harness overlay must own its exact production promise, semantic workcell, visual or temporal grammar, legal variables, composition templates, evaluation thresholds, and repair behavior that are not proven category mechanisms.

**Consequences (testable):**

- Category abstractions cannot absorb atomic creative policy merely because two harnesses look related.
- Proposed reuse requires implemented evidence and regression coverage.

**Traceability:** Decisions D008, D030, D033; journeys UJ-03, UJ-06.

### FR-150 — Govern category and profile migration

**Requirement:** Category and format-profile changes must generate compatibility analysis, dependent-harness regression plans, migration artifacts, deprecation policy, and receipts.

**Consequences (testable):**

- Stable dependent harnesses remain pinned until explicitly migrated.
- A category change cannot silently alter an authorized Development Capsule.

**Traceability:** Decisions D031; journeys UJ-06, UJ-12.

## Known failure and edge conditions

- Format 02 is listed as a cosmetic short-form style.
- Interview Expression or ReelCast blocks as unsupported because the registry recognizes only visual surfaces.
- Conversational questions are generated from topics without a typed Activative Intelligence Pack.
- One universal parser prompt ignores character state or temporal grammar.
- Carousel sequencing is treated as static template duplication.
- Atomic creative logic is moved into a shared category engine before reuse is proven.
- Activative sequencing is reduced to a timeline export step.

## Explicitly out of scope

- Defining every future format profile in Release 1.
- Merging the five categories into one schema with mostly optional fields.
- Building the actual character assets or render runtime inside the Builder.


---

# F15 — Traceable Development Capsule and Implementation Handoff

**User outcome:** An implementation team receives the smallest complete package needed to build the authorized harness without inventing architecture or carrying speculative boilerplate.

## Description

This feature materializes the Builder product promise. It packages the Harness IR and compiled views with contracts, skills, graphs, justified scaffolding, fixtures, vertical-slice stories, authorization, and traceability.

## Brownfield baseline

V2.1 compiles an OpenSpec package and readiness receipt, while the parallel workspaces provide empty implementation directories. The next Builder must generate an integrated, traceable capsule whose scaffolding is justified by approved responsibilities and whose stories are implementation-ready.

## Required product delta

Define capsule structure, artifact provenance, interface stubs, test assets, dependency-ordered vertical stories, implementation-delta handling, and downstream telemetry return.

## Traceability

- **Decisions:** D001, D003, D011, D015, D021, D027, D029, D032
- **User journeys:** UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-003, NFR-TEST-001, NFR-PORT-001, NFR-MAINT-001

## Functional Requirements

### FR-151 — Generate a versioned Development Capsule

**Requirement:** The Builder must package authorization, Harness IR, readable specifications, contracts, skill bindings and adaptations, runtime graphs, module manifests, tests, implementation planning, and observability configuration into one versioned handoff.

**Consequences (testable):**

- The capsule manifest lists every file, hash, source IR node, and authorization status.
- The package validates independently after export.

**Traceability:** Decisions D029; journeys UJ-11.

### FR-152 — Maintain requirement-to-artifact traceability

**Requirement:** Every generated contract, module, skill, test, story, and dashboard element must map to governing decisions, FRs or NFRs, and Harness IR nodes.

**Consequences (testable):**

- The implementation team can navigate from an acceptance criterion to its source doctrine and contract.
- Unmapped generated artifacts fail capsule validation.

**Traceability:** Decisions D011, D029; journeys UJ-11.

### FR-153 — Generate only justified scaffolding

**Requirement:** The Builder may create schema classes, interface stubs, module shells, manifests, fixtures, and configuration only when an approved IR responsibility, contract, test seam, or runtime need justifies them.

**Consequences (testable):**

- Speculative generic services and placeholder business logic are excluded.
- Every scaffold records the IR node that requires it.

**Traceability:** Decisions D001, D015, D029, D033; journeys UJ-11.

### FR-154 — Provide typed interfaces and contract examples

**Requirement:** The capsule must include machine-validatable schemas or interface definitions, positive examples, negative examples, version compatibility rules, and producer-consumer mappings for each required contract.

**Consequences (testable):**

- Examples validate against the same schema shipped to implementation.
- Breaking changes are visible and governed.

**Traceability:** Decisions D014, D029; journeys UJ-11.

### FR-155 — Provide executable test and benchmark fixtures

**Requirement:** The capsule must include contract, unit-seam, behavioral, integration, golden, adversarial, and benchmark fixtures required by the authorized implementation scope.

**Consequences (testable):**

- The first vertical slice can run meaningful tests without inventing datasets.
- Protected benchmark labels are excluded or accessed through their governed mechanism.

**Traceability:** Decisions D021, D023, D029; journeys UJ-11.

### FR-156 — Generate dependency-ordered vertical stories

**Requirement:** The implementation plan must decompose authorized scope into stories that deliver complete testable behavior, fit one development-agent context, use only previous-story dependencies, and map to FRs, NFRs, contracts, modules, and acceptance criteria.

**Consequences (testable):**

- Stories are not organized as database, API, and UI horizontal layers.
- Every FR is covered by at least one story before readiness.

**Traceability:** Decisions D029, D032; journeys UJ-11.

### FR-157 — Define a first working vertical-slice plan

**Requirement:** The capsule must identify the narrowest end-to-end reference path that proves evidence, one core transformation, one format projection, evaluation, observability, and targeted repair for the selected reference harness.

**Consequences (testable):**

- The path produces a demonstrable output and receipts.
- It does not require future stories to function.

**Traceability:** Decisions D022, D032; journeys UJ-11, UJ-12.

### FR-158 — Govern implementation-discovered deltas

**Requirement:** When implementation reveals a genuine contradiction or missing decision, the team must create a typed delta linked to the affected IR nodes rather than silently altering constitutional or creative policy in code.

**Consequences (testable):**

- The delta identifies whether PRD, Architecture, Harness IR, skill, contract, or benchmark must change.
- Affected authorization is suspended or scoped until the delta is resolved.

**Traceability:** Decisions D010, D026, D029; journeys UJ-11.

### FR-159 — Ingest implementation and certification feedback

**Requirement:** The Builder must accept structured implementation questions, delta outcomes, tests, defects, runtime metrics, repair history, and certification evidence and link them to the Builder and capsule versions that caused them.

**Consequences (testable):**

- Feedback updates benchmark and migration evidence through governed events.
- Stable doctrine is not batch-rewritten without failure-local analysis.

**Traceability:** Decisions D003, D022, D028, D029; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- The capsule contains empty directories with no approved purpose.
- A story requires a future story to become testable.
- Implementation changes the production promise directly in code.
- A generated interface has no requirement or contract trace.
- The capsule's authorization hash does not match its IR.

## Explicitly out of scope

- Writing all production implementation code.
- Selecting the team's git-hosting or deployment workflow.
- Providing protected benchmark answers directly in the package.


---

# F16 — Controlled V2.1 Migration, Compatibility, and Release Governance

**User outcome:** Builder Maintainers can evolve the proven V2.1 baseline in measurable increments, preserve valuable behavior, and limit production claims to demonstrated transfer.

## Description

This feature prevents a greenfield rewrite from discarding working saturation, Genesis, ratification, OpenSpec, and readiness logic. Each architectural increment must prove its value through tests and the reference harness.

## Brownfield baseline

V2.1 is executable and tested and already implements several core mechanisms. It also has portability, source-configuration, embedded-reference, generic profile, and production-depth limitations identified during prior analysis.

## Required product delta

Create capability inventory, baseline fixtures, old-to-new mappings, dual compilation, compatibility layers, deprecation governance, migration receipts, staged release claims, and reference-harness continuous integration.

## Traceability

- **Decisions:** D003, D022, D024, D028, D032, D033
- **User journeys:** UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-COMPAT-001, NFR-COMPAT-002, NFR-REL-001, NFR-EVAL-003, NFR-TRACE-002

## Functional Requirements

### FR-160 — Inventory V2.1 capabilities and artifacts

**Requirement:** Before modification, the project must produce a machine-readable inventory of V2.1 commands, schemas, decision nodes, prompts, references, tests, artifacts, workflows, and known limitations.

**Consequences (testable):**

- Each item has a retain, adapt, replace, deprecate, or remove-after-evidence classification.
- The inventory is versioned against the exact V2.1 source hash.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-161 — Map V2.1 concepts into the next architecture

**Requirement:** The migration plan must map existing source saturation, atomicity, Genesis, ratification, OpenSpec, readiness, and Pi assets into Harness IR, target profiles, graphs, skill ecology, benchmarks, and authorization.

**Consequences (testable):**

- Unmapped behavior is explicitly reviewed rather than silently lost.
- One-to-many and deprecated mappings include rationale.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-162 — Support baseline and candidate dual compilation

**Requirement:** During migration, the same eligible target must be compilable through the retained V2.1 baseline and candidate Builder for comparison.

**Consequences (testable):**

- The comparison uses locked inputs and declares unavoidable schema or profile differences.
- Candidate improvements and regressions are visible per dimension.

**Traceability:** Decisions D022, D028; journeys UJ-12.

### FR-163 — Require evidence for retention, adaptation, or deprecation

**Requirement:** A working V2.1 behavior may be changed or removed only with a documented product rationale, replacement path, tests, migration effect, and benchmark evidence proportional to its risk.

**Consequences (testable):**

- Aesthetic preference alone cannot justify removing a proven workflow.
- Deprecated behavior remains available through the declared compatibility window.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-164 — Run regression suites at every migration increment

**Requirement:** Each increment must add failing tests or benchmark cases for the intended delta, implement the minimum correction, and rerun V2.1 compatibility plus reference-harness suites.

**Consequences (testable):**

- A migration increment cannot rely solely on code review.
- Regression results are stored in the release ledger.

**Traceability:** Decisions D021, D028; journeys UJ-12.

### FR-165 — Define compatibility and alias policy

**Requirement:** The Architecture must define which V2.1 CLI commands, configuration fields, artifact names, and status values remain supported, aliased, migrated, or rejected.

**Consequences (testable):**

- Compatibility behavior is explicit and testable.
- Aliases do not hide materially different semantics.

**Traceability:** Decisions D028; journeys UJ-11, UJ-12.

### FR-166 — Generate migration and deprecation receipts

**Requirement:** Every migrated run, artifact, schema, skill, or configuration must record source version, target version, transformations, warnings, losses, and validation results.

**Consequences (testable):**

- Operators can audit what changed during migration.
- Irreversible or lossy migrations require explicit approval.

**Traceability:** Decisions D025, D028; journeys UJ-09, UJ-12.

### FR-167 — Prove Release 1 through one complete reference path

**Requirement:** Release 1 must implement the complete Builder spine and use it to specify, implement, evaluate, repair, and certify one Atomic Content Harness vertical slice.

**Consequences (testable):**

- The release report includes downstream harness results, not only Builder unit tests.
- The reference harness remains a continuous integration target for later releases.

**Traceability:** Decisions D003, D022, D032; journeys UJ-11, UJ-12.

### FR-168 — Limit certification of unproven categories and targets

**Requirement:** Release 1 may include structural profiles for other categories, Visual Asset Editor, and Delegation Contract, but must mark them uncertified until their required benchmarks and transfer gates pass.

**Consequences (testable):**

- The Control Tower and documentation distinguish structural support from production certification.
- Uncertified profiles cannot issue full production authorization.

**Traceability:** Decisions D004, D032, D033; journeys UJ-12.

### FR-169 — Require portfolio evidence for general Builder certification

**Requirement:** The Builder may claim general production readiness only after successful transfer across materially different atomic harnesses, all five category constitutions, the Visual Asset Editor, and the Delegation Contract according to their target gates.

**Consequences (testable):**

- The certification statement lists the exact portfolio and versions passed.
- A new unsupported category or target remains outside the claim.

**Traceability:** Decisions D022, D032, D033; journeys UJ-12.

## Known failure and edge conditions

- V2.1 is deleted before parity and benchmark comparison.
- A new architecture is declared better because it has more artifacts.
- An alias maps an old command to materially different behavior without warning.
- Release 1 claims all five categories are production-certified.

## Explicitly out of scope

- Maintaining every historical artifact forever.
- Guaranteeing zero migration effort for unsupported private extensions.
- Changing the product boundary to preserve accidental V2.1 behavior.


---

# F17 — Three Explicit Compilation Target Profiles

**User outcome:** The Builder can compile Atomic Content Harnesses, Visual Asset Editors, and Delegation Contracts through shared governance while preserving the distinct evidence, decisions, IR, artifacts, benchmarks, and authorization each product requires.

## Description

This feature keeps the Builder product-specific rather than universal. It uses one control plane and one IR framework with explicit target-profile extensions, preventing a Content Harness model from being incorrectly reused for asset authority or ABI design.

## Brownfield baseline

V2.1 already exposes three modules with separate prompt paths and approximate artifact sets. The next architecture must make those differences first-class in source profiles, Genesis, capability ownership, evaluation, repair, Development Capsules, and certification.

## Required product delta

Create three versioned target profiles, shared and target-local IR schemas, lifecycle and decision extensions, output packages, cross-target compatibility checks, and certification boundaries.

## Traceability

- **Decisions:** D001, D004, D005, D006, D011, D013, D027, D029, D032, D033
- **User journeys:** UJ-01, UJ-05, UJ-06, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-ARCH-001, NFR-CAT-001, NFR-COMPAT-001, NFR-SEC-003, NFR-PORT-002

## Functional Requirements

### FR-170 — Maintain three versioned target profiles

**Requirement:** The Builder must register Atomic Content Harness, Visual Asset Editor, and Content↔Asset Delegation Contract as explicit versioned compilation targets sharing only proven control-plane and IR abstractions.

**Consequences (testable):**

- Each run selects one profile with a stable version.
- A profile declares its required extensions and forbidden cross-target assumptions.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-171 — Compile the Atomic Content Harness profile

**Requirement:** The content profile must cover evidence and specimens, Visual Syntax First, atomicity, Activative semantics, category and format profiles, sequencing, assets, runtime, JIT skills, evaluation, repair, and content-harness authorization.

**Consequences (testable):**

- Category constitution and atomic production promise are mandatory.
- The profile does not grant asset-editing authority beyond its demand contract.

**Traceability:** Decisions D004, D030, D031; journeys UJ-02, UJ-06.

### FR-172 — Compile the Visual Asset Editor profile

**Requirement:** The asset-editor profile must cover asset taxonomy, demand-contract intake, semantic non-mutation, source and rights provenance, research and provider routing, transformation authority, quality, versions, receipts, repair, and editor authorization.

**Consequences (testable):**

- The editor cannot change content meaning, sequence role, or composition purpose without a new request.
- Representative real demand contracts are required evidence for production certification.

**Traceability:** Decisions D004; journeys UJ-11, UJ-12.

### FR-173 — Compile the Delegation Contract profile

**Requirement:** The delegation profile must cover request and response ABI, ownership boundaries, compatibility, idempotency, timeouts, retries, partial results, errors, provenance, reconciliation, version negotiation, and certification between one content harness and one asset editor.

**Consequences (testable):**

- The ABI cannot redefine either product's constitution.
- Representative request, response, and failure examples are required.

**Traceability:** Decisions D004; journeys UJ-11, UJ-12.

### FR-174 — Use target-specific source profiles

**Requirement:** Each compilation target must declare its own required repositories, contracts, examples, prior implementations, doctrine, and target folder expectations.

**Consequences (testable):**

- The Visual Asset Editor can require visual research and asset-intelligence sources not mandatory for every content harness.
- Delegation compilation may use compiled product changes and representative ABI fixtures instead of the full specimen corpus.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-175 — Use target-specific Harness IR profiles

**Requirement:** The canonical Harness IR must provide a shared governance spine plus typed target-local sections and validation rules for content, editor, and delegation products.

**Consequences (testable):**

- Target-local fields are not represented as an uncontrolled sea of optional properties.
- Cross-target shared nodes have identical semantics and version policy.

**Traceability:** Decisions D011; journeys UJ-05.

### FR-176 — Use target-specific Genesis decision graphs

**Requirement:** Each target must define the constitutional decisions, dependencies, evidence, ratification owners, and cascade-lock conditions appropriate to its authority and product promise.

**Consequences (testable):**

- Content format decisions are not asked during a pure delegation run unless they affect the ABI.
- Asset semantic-authority decisions are mandatory for the editor profile.

**Traceability:** Decisions D006, D010; journeys UJ-04.

### FR-177 — Compile target-specific artifact sets

**Requirement:** Each target profile must declare its required specifications, contracts, skills, graphs, tests, benchmarks, observability views, Development Capsule contents, and readiness receipts.

**Consequences (testable):**

- Missing target-required artifacts block readiness.
- Artifact counts are not forced to be equal across profiles.

**Traceability:** Decisions D029; journeys UJ-11.

### FR-178 — Apply target-specific evaluation and authorization gates

**Requirement:** The score dimensions, hard blockers, skill maturity, benchmark corpus, repair routes, and implementation authorization criteria must be profile-specific while preserving shared evidence and integrity gates.

**Consequences (testable):**

- A content visual-syntax benchmark cannot substitute for editor provenance testing.
- The Delegation Contract cannot be production-authorized before both endpoint specifications are compatible and sufficiently mature.

**Traceability:** Decisions D021, D024, D027; journeys UJ-12.

### FR-179 — Prevent universal-profile flattening

**Requirement:** The Builder must reject attempts to model all three targets as one generic agent schema whose meaning depends on optional fields and prose conventions.

**Consequences (testable):**

- Shared abstractions require demonstrated semantic equivalence.
- Target-specific responsibilities remain explicit in IR and documentation.

**Traceability:** Decisions D004, D033; journeys UJ-05.

### FR-180 — Validate cross-target compatibility

**Requirement:** Where products interact, the Builder must validate content demand contracts, editor response contracts, delegation versions, ownership, provenance, error semantics, and authorization compatibility.

**Consequences (testable):**

- A mismatch generates a typed compatibility blocker and repair route.
- Compatibility results identify which target owns each correction.

**Traceability:** Decisions D004, D014, D026; journeys UJ-10, UJ-11.

## Known failure and edge conditions

- One generic profile uses dozens of optional fields to represent all targets.
- The Content Harness directly owns asset transformation policy.
- A Delegation Contract is compiled before its endpoint contracts exist.
- Structural support is presented as production certification.

## Explicitly out of scope

- Arbitrary agent or workflow types beyond the three named targets.
- Implementing the Visual Asset Editor or Delegation runtime in Release 1 unless selected by the reference-slice scope.
- Guaranteeing compatibility with unspecified third-party editors.


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


---

# 6. Cross-Cutting Non-Functional Requirements

## Reliability and execution integrity

### NFR-REL-001 — Deterministic replay

Given identical locked sources, ratified decisions, compiler versions, and configuration, deterministic Builder stages must reproduce byte-identical authoritative artifacts or record an explicit nondeterminism exception.

### NFR-REL-002 — Resumability

Every run must resume after interruption from the last committed authoritative event without replaying completed human decisions.

### NFR-REL-003 — Idempotent compilation

Recompiling an unchanged Harness IR must not create semantically different artifacts or duplicate ledger events.

### NFR-REL-004 — Failure isolation

A phase failure must not corrupt locked evidence, ratified decisions, or unaffected artifacts.

## Performance, cost, and context budgets

### NFR-PERF-001 — Interactive Control Tower

Common Control Tower status and detail queries should render within 2 seconds at the reference-corpus scale, excluding intentional long-running model operations.

### NFR-PERF-002 — Compilation budget visibility

Every stochastic phase and JIT capsule must declare expected token, latency, and cost budgets and emit actual usage.

### NFR-PERF-003 — No hidden budget overflow

A phase that exceeds its hard context or cost budget must block, degrade through an approved policy, or request authorization; it may not continue silently.

### NFR-PERF-004 — Parallel-safe work

Independent deterministic scans, benchmark repetitions, and evaluator tasks should support bounded parallel execution without shared-state conflicts.

## Corpus and workload scale

### NFR-SCALE-001 — Corpus-scale evidence processing

The Builder must inventory and index the reference-corpus scale without losing source coverage, stable identities, or bounded parallelism; exact thresholds are calibrated in Architecture and benchmarks.

## Traceability and provenance

### NFR-TRACE-001 — End-to-end provenance

Every material requirement, IR value, generated artifact, decision, benchmark result, and authorization state must be traceable to its source evidence or governing decision.

### NFR-TRACE-002 — Append-only operational history

Run and human-action history must be append-only or cryptographically superseded; destructive history editing is prohibited.

### NFR-TRACE-003 — Evaluated artifact identity

Production eligibility must bind exact source-IR, skill, recipe, capsule, compiler, and evaluation-receipt hashes.

### NFR-TRACE-004 — Knowledge-status integrity

No system component may promote generated or hypothesized content into observed or ratified status without the required authority transition.

## Observability

### NFR-OBS-001 — Event completeness

Every lifecycle transition, blocker, decision, waiver, invalidation, repair, benchmark verdict, and authorization change must emit a typed event.

### NFR-OBS-002 — Evidence-backed status

Every displayed status must link to the criteria, events, artifacts, or receipts that justify it.

### NFR-OBS-003 — No second source of truth

The Control Tower may mutate state only through governed commands that update the Harness IR or run ledger and emit receipts.

### NFR-OBS-004 — Exportability

Operators must be able to export machine-readable run state, scorecards, decision history, artifacts, and receipts without scraping the UI.

## Builder workflow runtime and execution factory

### NFR-WORKFLOW-001 — Reproducible workflow routing

Given the same request classification, target profile, risk state, and workflow registry version, the router must select the same workflow profile or emit an explicit nondeterminism receipt.

### NFR-WORKFLOW-002 — Explicit actor ownership

Every workflow node must identify whether its primary actor is deterministic code, a bounded agent program, a human gate, or a governed hybrid; undocumented general-agent ownership is prohibited.

### NFR-WORKFLOW-003 — Typed node handoffs

Every node-to-node handoff must use a versioned contract with validated producer, consumer, authority, error, and completion semantics.

### NFR-WORKFLOW-004 — Bounded control flow

Retries, loops, timeouts, fan-out, arbitration, and fallback routes must have declared limits and terminal conditions; unbounded autonomous looping is prohibited.

### NFR-WORKFLOW-005 — Idempotent workflow resume

A workflow must resume from committed node state without duplicating successful side effects, replaying ratified human actions, or silently changing the selected profile.

### NFR-WORKFLOW-006 — Failure containment

A failed node, agent, tool, sandbox, or workflow profile must not corrupt locked sources, ratified decisions, protected benchmarks, or unaffected workflow branches.

### NFR-WORKFLOW-007 — Sandbox least privilege

Node sandboxes must receive only approved tools, sources, secrets, network access, storage, compute, and lifetime required by the node contract.

### NFR-WORKFLOW-008 — Bounded parallelism

Parallel execution is allowed only for dependency-independent work with explicit concurrency, budget, merge, cancellation, and conflict policies.

### NFR-WORKFLOW-009 — Risk-aware model and compute routing

Model tier, repetition count, candidate fan-out, evaluator strength, and compute budget must be selected by explicit task-complexity, risk, and expected-value policy and recorded in the run.

### NFR-WORKFLOW-010 — Workflow observability

Every workflow node and route must emit start, completion, validation, failure, retry, cancellation, cost, latency, and artifact events sufficient to reconstruct execution.

### NFR-WORKFLOW-011 — Workflow-level testability

Every production workflow profile must support contract tests, end-to-end integration tests, fault injection, resume tests, route tests, and rollback tests at stable public seams.

### NFR-WORKFLOW-012 — Versioned promotion and rollback

Workflow definitions, routers, node contracts, and execution policies must be versioned, maturity-gated, promotable through CI, and rollback-safe with migration receipts.

## Security, authority, and source safety

### NFR-SEC-001 — Source immutability

Configured source repositories, archives, and specimens are read-only evidence unless an explicit import or migration action creates a new governed copy.

### NFR-SEC-002 — Path and archive safety

The Builder must prevent archive traversal, unsafe extraction, executable surprise, and unbounded recursive ingestion.

### NFR-SEC-003 — Authority enforcement

Only authorized actors may ratify constitutional decisions, approve waivers, freeze category constitutions, or issue implementation authorization.

### NFR-SEC-004 — Secret isolation

Credentials and provider secrets must never be written into Harness IR, generated skills, execution capsules, logs, or exported Development Capsules.

## Architecture integrity

### NFR-ARCH-001 — Explicit ownership integrity

Every capability, phase, module, contract, skill, evaluator, repair, and human gate must have the ownership cardinality permitted by its schema; undocumented general-agent ownership is prohibited.

### NFR-ARCH-002 — Executable graph integrity

Phase, context, contract, dependency, loading, and repair graphs must be acyclic where execution requires a DAG, explicitly model approved loops, and fail validation on unresolved cycles or orphan nodes.

## Testability

### NFR-TEST-001 — Public-seam testability

Every implementation module and behaviorally significant skill must expose stable public seams and fixtures sufficient for contract, behavioral, integration, benchmark, and adversarial testing without coupling tests to hidden internals.

## Category and atomic ownership

### NFR-CAT-001 — Category isolation

Category and format-profile ontologies, registries, parsing fields, runtime rules, and evaluators must not leak into unrelated categories unless a shared abstraction is explicitly proven and versioned.

### NFR-CAT-002 — Atomic creative ownership

Creative production promise, semantic workcell, visual or temporal grammar, legal variables, and format-native evaluation remain atomic-harness-owned unless implemented transfer evidence authorizes extraction.

### NFR-CAT-003 — Sequence fidelity

For sequence-bearing products, the compiled architecture must preserve required viewer-state progression, scene or slide roles, timing or swipe logic, continuity, payoff, and intended reaction through typed contracts and category-appropriate evaluation.

## Evaluation and benchmark integrity

### NFR-EVAL-001 — Protected benchmark integrity

Protected release cases and expected labels must be access-controlled and excluded from training or prompt construction paths.

### NFR-EVAL-002 — Repeated-run measurement

Critical stochastic benchmark cases must run in fresh contexts with recorded repetition count, variance, minimum, mean, and failure frequency.

### NFR-EVAL-003 — Independent evaluation

A generator or reasoning phase may not be the sole authority approving its own output.

### NFR-EVAL-004 — Category-appropriate evaluation

Evaluation dimensions, thresholds, fixtures, and repair routes must reflect the selected category and format profile; metrics from one production substrate may not substitute for another without an explicit equivalence test.

## Compatibility and migration

### NFR-COMPAT-001 — V2.1 compatibility

Existing V2.1 runs and compiled packages must remain readable or receive an explicit migration path with loss and incompatibility receipts.

### NFR-COMPAT-002 — Schema evolution

IR, contract, event, category, and skill schemas must be versioned and support documented compatibility and migration rules.

### NFR-COMPAT-003 — Artifact deprecation

Deprecated outputs must include replacement guidance, affected consumers, removal gates, and regression evidence.

## Portability and adapter boundaries

### NFR-PORT-001 — Portable source profiles

Source profiles must use resolvable URIs or paths and support local directories and archives without requiring one machine-specific layout.

### NFR-PORT-002 — Runtime adapter boundary

Core IR and compilation logic must not be coupled irreversibly to one model provider or one agent harness.

## Operator experience and accessibility

### NFR-UX-001 — Accessible Control Tower

The Pi UI must support keyboard navigation, readable status semantics, non-color-only indicators, and accessible evidence inspection.

### NFR-UX-002 — Progressive disclosure

The UI and generated documents must lead with decisions, blockers, and evidence and disclose lower-level technical detail on demand.

## Maintainability and evolution

### NFR-MAINT-001 — Single-source generation

Readable documents and executable artifacts must be compiled from canonical IR or registries rather than independently maintained duplicates.

### NFR-MAINT-002 — Skill ecology maintainability

Canonical skill duplication, relation cycles, unsupported dependencies, and maturity violations must be detectable automatically.

### NFR-MAINT-003 — Category migration safety

A category-constitution change must identify dependent harnesses, run the required benchmark portfolio, and issue a migration receipt before release.


---

# 7. Canonical Format Category Constitutions

Every Atomic Content Harness is compiled through the following ownership hierarchy:

```text
Shared Activative Core
        ↓
Canonical Format Category
        ↓
Category-local Format Profile
        ↓
Atomic Harness Constitution
```

The shared Activative Core owns meaning and activation. Categories and format profiles own their production substrate. Atomic harnesses own the exact production promise and creative grammar.

## Short-Form Edited Video (`short_form_edited_video`)

Time-based edited short videos whose production grammar is owned by one of the governed editing format profiles.

**Current governed profiles:**

- `format01_story_video`
- `format03_living_commentary`
- `format04_conscious_reaction`
- `format05_silent_dialogue_theatre`
- `format06_data_scale_race`
- `format07_direct_coaching_a_roll`
- `format08_poetic_quote_theatre`

## 2D Character Animation (`2d_character_animation`)

Registry-driven character-performance systems using identities, poses, expressions, gestures, gaze, props, animation primitives, scene relationships, and continuity-aware state transitions.

**Current governed profiles:**

- `format02_minimal_coach_theatre`

## Carousels (`carousels`)

Multi-slide static packages whose meaning depends on slide-role grammar, swipe progression, cross-slide continuity, and package coherence.

**Current governed profiles:** to be classified and registered through category-specific evidence; existing parallel workspaces remain source inputs.

## Supervisuals (`supervisuals`)

Single-frame high-density visual products whose quality depends on one-frame hierarchy, feed-size legibility, immediate recognition, and a precise static composition grammar.

**Current governed profiles:** to be classified and registered through category-specific evidence; existing parallel workspaces remain source inputs.

## Conversational Activation / Human Expression (`conversational_activation_expression`)

Human-reaction surfaces compile an Activative Intelligence Pack into Activative Calls, adaptive turn logic, Reaction Receipts, Expression Moments, micro-commitments, elevation/close logic, and human-reviewed Identity DNA amendment proposals.

**Current governed profiles:**

- `public_comment`
- `reply_dm`
- `reelcast_expression`
- `interview_expression`

All four profiles are structurally supported and `UNCERTIFIED` in Release 1. Builder compiles, validates, preserves lineage, and emits handoffs; external content harnesses own conversation/interview execution and the human identity authority owns any Identity DNA merge.

## Required constitution fields

Every category constitution must define:

- production surface and specimen types;
- visual, temporal, conversational-turn, and expression parsing ontologies as applicable;
- composition-variable taxonomy;
- sequence and viewer-state model;
- required primitive and asset registries;
- canonical skill requirements and adaptations;
- runtime families and continuity constraints;
- evaluation dimensions, hard failures, and repair classes;
- observability views and event requirements;
- benchmark suite, compatibility, deprecation, and migration policy.

## 2D Character Animation distinction

Format 02 Minimal Coach Theatre belongs to the separate **2D Character Animation** category because its production substrate is a registry-driven character performance system. Its constitution must support character identity, pose, expression, gesture, gaze, prop, animation primitive, scene relationship, camera/framing, transition, sonic cue, compatibility, continuity, and state-transition registries. This category does not automatically absorb generic motion graphics, animated data, or illustrated tableaux.

## Activative Sequencing Intelligence

Every sequence-bearing harness must compile a category- and format-adapted capability that joins parsed visual/temporal syntax with ratified Activative meaning. It must express viewer-state before and after each beat, sequence role, prediction gap, recognition mechanism, asset and character states, timing or swipe logic, transition, continuity, sonic function, payoff, intended reaction, evaluation, and repair ownership.

At runtime, **Activation First** governs semantic order. During harness development, **Visual Syntax First** governs evidence discovery. The development law cannot be used to let a parser, generator, editor, or Delegation implementation invent upstream meaning.


---

# 8. Success Metrics and Counter-Metrics

Exact numeric thresholds that require empirical calibration remain Architecture and benchmark work. The PRD defines what must be measured and which failures can never be averaged away.

## Primary and secondary metrics

| ID | Metric | Target or definition |
| --- | --- | --- |
| SM-01 | Unsupported constitutional decision rate | 0 critical unsupported decisions in any release-gate reference run; target <1% material decisions requiring post-implementation correction. |
| SM-02 | Atomicity classification accuracy | Meet the category-specific threshold on protected merge/split/variant/family cases; no critical boundary error in the primary reference harness. |
| SM-03 | Visual-syntax accuracy | Meet protected benchmark thresholds for salient component recall, relationship accuracy, composition-variable classification, and cross-specimen invariant precision. |
| SM-04 | Implementation invention rate | Fewer than 5% of implementation-blocking decisions are invented outside the authorized Development Capsule in the reference slice. |
| SM-05 | First-pass implementation readiness | At least 90% of Development Capsule acceptance checks pass before implementation begins; all blockers are explicit. |
| SM-06 | Skill behavioral lift | Every required production skill or adaptation demonstrates statistically meaningful lift over its no-guidance control on its target behavior. |
| SM-07 | JIT context efficiency | Required capsules meet their phase completeness criteria while reducing irrelevant or inactive context against the monolithic baseline. |
| SM-08 | Downstream harness effectiveness | Each certified profile meets its category-native baseline on accuracy, Activative fidelity, role/reaction integrity, Expression Moment provenance where applicable, wrong-reading rate, first-pass acceptance, latency, and cost per accepted output. |
| SM-09 | Repair localization | At least 90% of benchmarked failures are repaired without rerunning unaffected constitutional or evidence phases. |
| SM-10 | Run observability completeness | 100% of mandatory lifecycle, semantic-lineage, Reaction Receipt, Expression Moment, external handoff, repair, benchmark, waiver, and authorization transitions produce valid events and receipts. |
| SM-11 | Builder release stability | Required stochastic benchmark dimensions meet both mean and minimum thresholds with bounded variance across fresh-context repetitions. |
| SM-12 | V2.1 migration safety | No retained V2.1 capability regresses without an approved deprecation or replacement receipt; all existing supported artifacts are readable or migratable. |
| SM-13 | Workflow autonomous completion rate | Measure the percentage of reference and transfer runs that complete all non-human-gated nodes without unplanned operator intervention while preserving every hard gate. |
| SM-14 | Workflow route accuracy | The selected workflow profile must match expert-labeled request, risk, target, and incident classes on protected routing cases, with zero critical hotfix-versus-normal-flow errors. |
| SM-15 | Workflow failure containment | 100% of benchmarked node failures preserve locked evidence, ratified decisions, protected cases, and unaffected branch state. |
| SM-16 | Cost and latency per authorized capsule | Track p50/p95 end-to-end and per-node latency, deterministic compute, model tokens, retries, and total cost for each authorized Development Capsule and workflow profile. |

## Counter-metrics — do not optimize

| ID | Counter-metric | Why it is dangerous |
| --- | --- | --- |
| SM-C01 | Artifact count | More generated documents are not evidence of quality and must not be optimized. |
| SM-C02 | Question count | A larger Genesis tree is not intrinsically better; ask only dependency-relevant decisions. |
| SM-C03 | Canonical skill count | Skill proliferation is a failure mode, not a success metric. |
| SM-C04 | Total context tokens | Consuming more context must not be mistaken for deeper understanding. |
| SM-C05 | Composite score alone | A high average must never conceal a hard evidentiary, constitutional, atomicity, or contract failure. |
| SM-C06 | Automation percentage | More autonomous decisions are not better when authority should remain human or deterministic. |
| SM-C07 | Agent and sandbox count | More agents, candidates, worktrees, or sandboxes do not imply a better workflow and must not be optimized independently of accepted quality and cost. |
| SM-C08 | Fastest candidate completion | The first finished candidate must not win unless it also satisfies the declared quality, evidence, contract, and authorization gates. |

## Hard-gate principle

The Builder may calculate composite trend scores, but the following classes remain non-compensable: unsupported constitutional decisions, critical evidence failures, wrong atomicity, contract contradictions, silent knowledge promotion, untested required skills, benchmark leakage, false readiness, category flattening, and anti-goal violations.


---

# 9. Non-Goals and Binding Anti-Goals

These are enforceable product boundaries. Architecture must provide validators, hard gates, or review mechanisms for each anti-goal.

## AG-001 — Implement the final production harness

The Builder may generate justified scaffolding and test assets but may not silently implement production business or creative logic.

## AG-002 — Become a universal agent factory

The product compiles three explicit CMF target types and must not generalize beyond proven abstractions.

## AG-003 — Collapse atomic harnesses into a universal creative engine

Atomic production promises, visual grammar, sequence policy, and evaluation remain harness-owned unless reuse is proven through implementations.

## AG-004 — Flatten the five canonical categories

Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression retain separate constitutions and runtime laws.

## AG-005 — Treat editing Formats 01–08 as cosmetic themes

Format profiles represent materially different visual, temporal, sonic, state, and sequencing systems.

## AG-006 — Infer meaning before parsing syntax

Observed components and temporal states must precede visual-function and Activative hypotheses.

## AG-007 — Promote unsupported knowledge

Generated or hypothesized values cannot silently become observed, measured, or ratified.

## AG-008 — Turn every difficult capability into a skill

Deterministic modules, typed programs, references, human authority, and independent evaluators must be considered first.

## AG-009 — Confuse canonical skills and runtime capsules

Ephemeral compiled prompts are not automatically reusable canonical capabilities.

## AG-010 — Ship untested required skills

A structurally valid skill without behavioral evaluation cannot support production authorization.

## AG-011 — Let the model own critical orchestration

Phase invocation, dependency resolution, skill selection, reference loading, budgets, validation, and repair routing are deterministic control-plane responsibilities.

## AG-012 — Use accumulated conversation history as the main interface

Authoritative phase handoffs are typed contracts; history is audit material only.

## AG-013 — Silently truncate required context

Budget pressure must block, redesign, retrieve, compress through an approved policy, or receive authorization.

## AG-014 — Repair outside the responsible layer

Repair and invalidation must follow the typed graph and preserve still-supported state.

## AG-015 — Issue readiness from document completeness

Authorization depends on evidence, architecture, skill maturity, benchmark, observability, and human gates.

## AG-016 — Hide operational state

Important transitions, failures, costs, waivers, and actions must be observable and receipted.

## AG-017 — Claim general readiness from one harness

Release 1 proves one path; general certification requires transfer across the agreed portfolio.

## AG-018 — Duplicate authoritative truth across artifacts

Documents and code-generation manifests must compile from canonical IR or registries.

## AG-019 — Hide a production workflow inside one skill or agent session

A production Builder workflow must separate orchestration, deterministic code, bounded agent execution, validation, and human authority into explicit nodes.

## AG-020 — Use unbounded retry or self-correction loops

Every retry, repair, candidate race, and feedback edge requires a limit, terminal state, failure owner, and escalation policy.

## AG-021 — Parallelize by default

Parallel agents and sandboxes are authorized only when dependencies, evaluation, merge semantics, and expected value justify the extra compute and risk.

## AG-022 — Remove human gates merely to increase automation

Human authority may be reduced only after benchmark and operational evidence proves the affected decision class is safe to automate.


---

# 10. MVP Scope and Release Plan

## Release 1 objective

Release 1 establishes the complete architectural spine and proves it through **one fully implemented and certified Atomic Content Harness vertical slice**. It is not a thin schema-only MVP.

### Production-complete in Release 1

- V2.1 brownfield inventory, compatibility baseline, and dual-run comparison;
- typed Harness IR and artifact compiler;
- Builder Workflow IR, Workflow Profile Registry, deterministic router, node executor, workflow tests, and incident path derived from the reference shadow workflow;
- configured evidence workspace, source lock, saturation, and Visual Syntax First;
- evidence-based atomicity and Draft Harness Model;
- dependency-driven Genesis and human ratification;
- capability ownership, responsibility-centered modules, phase/context/contract graphs;
- one production-ready category constitution, format profile, and atomic reference harness;
- canonical skill bindings, harness adaptations, composition recipes, deterministic JIT compiler, and capsule receipts;
- behavioral skill evaluation and the primary benchmark suite;
- Repair and Invalidation Graph;
- Pi Harness Control Tower with workflow-node, sandbox, route, retry, budget, and incident observability for the reference path;
- Development Capsule, prototype and implementation authorization, one implemented vertical path, and downstream certification.

### Structurally supported but not production-certified in Release 1

- the remaining four category constitutions and their format/profile schemas, including the four `UNCERTIFIED` Conversational Activation / Human Expression profiles;
- Visual Asset Editor target profile;
- Content↔Asset Delegation Contract target profile;
- broader benchmark and transfer portfolio.

Structural support must be labeled **uncertified** and may not issue full production authorization.

## Suggested release progression

1. **Release 1 — Reference path:** one Atomic Content Harness, one category/profile, full Builder spine, implemented vertical slice, and downstream proof.
2. **Release 2 — Category transfer:** materially different harnesses across the remaining category architectures.
3. **Release 3 — Visual Asset Editor:** downstream product work outside this repository; Builder scope is limited to contract compilation and validation.
4. **Release 4 — Delegation Contract:** downstream protocol work outside this repository; Builder scope is limited to versioned handoff compilation and certification evidence.
5. **Release 5 — General Builder certification:** complete agreed benchmark portfolio and bounded general production claim.

## Release 1 reference target

The specific reference harness remains open (`OQ-001`). Selection must balance narrowness, evidence quality, representative sequencing or visual intelligence, implementation feasibility, and ability to exercise the new Builder spine without requiring unbuilt unrelated systems.

## Out of scope for Release 1

- simultaneous production certification of all categories and targets;
- a universal agent or creative factory;
- full migration of every legacy archetype brief;
- implementation of every generated production harness;
- fixed final technology choices before Architecture.


---

# 11. Risks and Mitigations

| ID | Risk | Failure mode | Mitigation |
| --- | --- | --- | --- |
| R-001 | Meta-framework overbuilding | The project may perfect abstractions without producing a real harness. | Keep one reference harness as a continuous integration target and require a working vertical slice in Release 1. |
| R-002 | Benchmark overfitting | The Builder may learn visible labels instead of general rules. | Use protected release cases, controlled mutations, transfer targets, and independent expert review. |
| R-003 | Visual parser unreliability | Multimodal parsing may omit or misclassify important components and states. | Use typed outputs, multiple views, deterministic geometry checks, independent evaluators, and selective human ratification. |
| R-004 | Skill sprawl | Every new capability may be expressed as another large skill. | Enforce canonical reuse, capability-gap analysis, no-op controls, progressive disclosure, and maturity gates. |
| R-005 | Category flattening | Shared infrastructure may absorb category or atomic creative policy. | Use explicit ownership tests, category constitutions, dependency impact analysis, and benchmark transfer gates. |
| R-006 | IR and document divergence | Readable documents may drift from machine state. | Compile documents from IR, hash artifacts, prohibit manual authoritative edits, and validate round-trip traceability. |
| R-007 | Control Tower becomes a second source of truth | UI state may diverge from the run ledger. | Use command/event architecture, authoritative reads from IR and ledger, and receipted mutations only. |
| R-008 | V2.1 migration damage | A rewrite may lose working Genesis, ratification, OpenSpec, or readiness behavior. | Inventory retained capabilities, run dual compilation, preserve compatibility, and deprecate only with regression evidence. |
| R-009 | Excessive phase fragmentation | Too many model calls may increase latency and lose useful coupling. | Compile phases from responsibility and risk, use deterministic code for mechanical work, and benchmark merged versus isolated calls. |
| R-010 | Human-review overload | The architecture may require too many approvals and visual corrections. | Limit human gates to constitutional or high-impact ambiguity and use confidence, batching, and progressive disclosure. |
| R-011 | Provider coupling | The system may assume one model or tool behavior. | Keep typed program and adapter boundaries, record model policy, and test critical capabilities across supported runtimes. |
| R-012 | Downstream feedback arrives too late | Builder defects may only become visible after expensive implementation. | Use prototype-only authorization, early vertical slices, implementation-question logging, and online benchmark refinement. |
| R-013 | Workflow runtime becomes a second meta-framework | The team may build a broad orchestration platform before proving the reference Builder path. | Implement only the nodes and profiles exercised by the reference harness, then extract reusable workflow mechanisms from evidence. |
| R-014 | Router misclassification | A normal compilation, migration, repair, or hotfix may be sent through the wrong workflow profile. | Use typed request classification, protected route cases, human escalation for uncertain high-risk classes, and recorded router confidence. |
| R-015 | Sandbox and parallel-compute sprawl | Isolation and candidate fan-out may multiply cost, stale environments, and merge complexity. | Set workflow-level concurrency and compute budgets, automatic cleanup, quality-gated races, and per-profile cost telemetry. |
| R-016 | Automation hides operational ignorance | The workflow may appear autonomous while no one understands node behavior or failure propagation. | Require a shadow workflow, node-level contracts, fault injection, run reconstruction, and operator drill procedures before production promotion. |


---

# 12. Assumptions and Open Questions

## Assumptions

- **A-001:** V2.1 remains the operational baseline throughout the first migration increments.
- **A-002:** The five canonical categories are Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression; D031 remains historical evidence and the V1.2 constitutional amendment defines its current effect.
- **A-003:** Pi is the primary authoring and Control Tower environment, but core IR and compilation logic remain adapter-bounded.
- **A-004:** Exact performance and behavioral thresholds will be calibrated against baseline and reference-harness runs rather than invented in the PRD.
- **A-005:** OpenSpec remains a generated implementation-governance view, not the canonical source of truth.
- **A-006:** The first release may structurally support all target types and categories without claiming their production certification.
- **A-007:** The Builder Workflow Runtime is part of the Builder product, while generated harness Phase Graphs remain outputs compiled for downstream harness implementations.
- **A-008:** Release 1 automation is derived from a recorded manual shadow workflow for the selected reference harness rather than invented solely from diagrams.

## Open questions

### OQ-001

**Question:** Which atomic harness is the Release 1 primary reference: F04 Progressive Blind Ranking, CAR Visual Design Audit Tutorial, or another candidate?

**Disposition:** Owner: Product lead; resolve before Architecture finalization.

### OQ-002

**Question:** Which canonical category constitution is production-complete first?

**Disposition:** Owner: Product lead and category steward; expected to follow reference-harness selection.

### OQ-003

**Question:** Which storage technologies implement the Harness IR, event ledger, artifact registry, and benchmark receipts?

**Disposition:** Owner: Architecture; PRD constrains behavior, not technology.

### OQ-004

**Question:** Which multimodal model policy or ensemble provides the first Visual Syntactic Parsing implementation?

**Disposition:** Owner: Architecture and benchmark team.

### OQ-005

**Question:** How are protected benchmark labels governed, access-controlled, and changed?

**Disposition:** Owner: Evaluation governance.

### OQ-006

**Question:** What exact quantitative thresholds define production maturity for each score dimension?

**Disposition:** Owner: Benchmark calibration after baseline runs.

### OQ-007

**Question:** What is the exact Pi custom-UI implementation surface and deployment model for the Control Tower?

**Disposition:** Owner: UX/Architecture.

### OQ-008

**Question:** Which existing capabilities seed version 1 of the Canonical Skill Capability Registry, and which are only illustrated references?

**Disposition:** Owner: Skill architecture audit.

### OQ-009

**Question:** How broadly should legacy Design Briefs such as Achievement Story be migrated into archetype constitutions, composition recipes, and binding schemas in Release 1?

**Disposition:** Owner: Product lead and migration steward.

### OQ-010

**Question:** Does the first reference slice require a production Visual Asset Editor dependency, a stubbed delegation boundary, or no asset delegation?

**Disposition:** Owner: Product lead after reference-harness selection.

### OQ-011

**Question:** Which workflow-runtime technology, queue, and state-machine implementation should execute the Builder Workflow IR?

**Disposition:** Owner: Architecture; compare Pi extensions, local process orchestration, durable workflow engines, and adapter boundaries.

### OQ-012

**Question:** What isolation policy should use worktrees, containers, or stronger sandboxes for each node and implementation story class?

**Disposition:** Owner: Architecture and security; calibrate against source sensitivity, tool risk, cost, and reproducibility.

### OQ-013

**Question:** Which initial workflow profiles are mandatory in Release 1 beyond new harness compilation and benchmark regression?

**Disposition:** Owner: Product lead and Builder maintainer; decide after the reference shadow workflow.


---

# 13. Implementation-Readiness Handoff

This PRD is complete enough to enter **Architecture**, not implementation. The next workflow must preserve stable IDs and resolve technical mechanisms without rewriting product behavior.

## Required Architecture outputs

- canonical Harness IR schema, mutation model, storage, versioning, and migration;
- lifecycle, phase, context, contract, reference-loading, dependency, repair, and authorization graph architecture;
- Builder Workflow IR, Workflow Profile Registry, Actor Assignment Matrix, router, scheduler, node executor, isolation, CI promotion, rollback, and incident architecture;
- deterministic control-plane boundaries and typed model-program interfaces;
- category-native visual, temporal, conversational-turn, Reaction Receipt, and Expression Moment parsing architecture;
- Activation First runtime lineage and Visual Syntax First harness-development evidence-order enforcement;
- Visual Semantic Pack → Visual Narrative Program → feature contracts → Composition Asset Pack → Visual Syntax handoff → T/V route contracts;
- non-mutating, contract-only Visual Asset Editor and Delegation handoffs without external runtime implementation;
- Canonical Skill Capability Registry, skill compiler, recipe compiler, and JIT Execution Capsule compiler;
- benchmark, protected-case, evaluator, and maturity architecture;
- event schema, Run Ledger, artifact registry, read models, and Pi Control Tower architecture;
- V2.1 compatibility, dual-run, migration, and deprecation architecture;
- Development Capsule build and validation architecture;
- deployment, security, privacy, access, and operational constraints.

Architecture must map every significant mechanism to FR/NFR IDs and identify technical requirements that must enter Epic and Story planning.

## Epics and Stories prerequisites

The epic workflow must read the complete PRD, approved Architecture, and Control Tower UX contract when available. It must:

1. extract every FR and NFR without summarizing away detail;
2. extract Architecture and UX implementation requirements;
3. create a complete requirements inventory and coverage map;
4. organize epics around independently valuable operator or downstream outcomes, not technical layers;
5. size stories for one development-agent context;
6. prohibit future-story dependencies;
7. use Given/When/Then acceptance criteria, including edge and failure cases;
8. validate complete FR/NFR/Architecture/UX coverage before implementation readiness.

## Feature technical specifications

After approved epics and stories, each major feature receives a technical specification containing:

- mapped FRs, NFRs, decisions, stories, and source evidence;
- files and existing V2.1 behavior read;
- problem, solution, scope, and excluded scope;
- architecture traceability and public interfaces;
- states, flows, contracts, events, error and degradation behavior;
- observability, authority, security, budgets, and compatibility;
- implementation tasks tied to stories;
- positive, negative, failure, benchmark, and adversarial acceptance examples;
- unit, contract, integration, behavioral, and regression test plans.

## Readiness rule

Implementation may begin only after the PRD, Architecture, Epics/Stories, required feature specifications, benchmark design, Control Tower UX contract, and traceability audit have passed their respective gates. Release 1 may receive a narrowly scoped prototype authorization where a declared empirical question cannot be resolved through documentation alone.
