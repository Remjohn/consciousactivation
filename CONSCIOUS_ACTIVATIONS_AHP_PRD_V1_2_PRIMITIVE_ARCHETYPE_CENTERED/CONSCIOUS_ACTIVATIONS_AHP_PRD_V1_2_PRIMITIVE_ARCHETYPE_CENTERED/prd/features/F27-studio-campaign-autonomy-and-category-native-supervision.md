---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F27
title: "Studio Campaign Autonomy and Category-Native Supervision"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-157–FR-162"
---

# F27 — Studio Campaign Autonomy and Category-Native Supervision

## 1. Product claim and user outcome

**User outcome:** Operators order, supervise, correct, and ship campaigns through one Studio shell while Atomic Harnesses conduct the work.

Launch source-backed batches, route category modules, enforce autonomy modes, package exceptions, and govern delivery/publication. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

Studio owns projections and typed operator commands; canonical state remains in product services.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Studio modules do not own canonical state.
- SHADOW cannot publish.
- Human gates occur only at declared authority boundaries.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-AM-001` | `AMENDMENT_INPUT` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-AM-002` | `AMENDMENT_INPUT` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-INT-001` | `ADAPT` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-MIG-001` | `REFERENCE` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-CUR-004` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py | Canonical AtomicHarnessDefinition structure and execution-free status. |
| `SRC-CUR-010` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py | Execution-free Workflow Node, edge, authority and validation contracts. |

## 5. Workflow integration

Campaign order → source/Harness/binding validation → autonomy mode → execution projections → exception review → correction → ship/export/publish.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-157 — Launch campaigns from source packages or Asset Package Specs

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** The Studio shall let an authorized operator select a workspace/project, inspect or complete a Canonical Interview Source Package, choose target outputs and Harnesses, set seed/taste direction, budget, deadline, autonomy mode, and launch a governed content batch.

**Trigger and preconditions:** An operator wants to produce a batch from an interview source.

**Required output or state transition:** A Campaign Order, validated batch plan, bindings, budget reservation, and launch receipt.

**Authority and invariants:**
- The Studio cannot invent missing Harnesses.
- Source/source authority eligibility precedes launch.
- Order data does not bypass product contracts.

**Acceptance scenarios**

- **Primary success:** Given an imported interview source, when the operator selects one short and one Carousel, then the Studio validates both Harnesses and launches one coordinated batch.
- **Adversarial or denial case:** Given a requested Format 02 output before activation, when the order is validated, then that job is blocked and the rest may proceed if eligible.
- **Evidence required:** Order schema, source/Harness validation, budget checks, autonomy binding, and launch receipt.

**Governing decisions:** D046, D048  
**Exact source references:** SRC-AM-001, SRC-AM-002, SRC-INT-001


### FR-158 — Operate one shared Studio shell with category-native modules

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** The product shall provide one shared workspace, project, campaign, run, review, evidence, artifact, worker, provider, budget, and publishing shell while registering Interview Expression, Video Production, Static Composition, Visual Asset, and Knowledge/Programmed Model modules behind current product boundaries.

**Trigger and preconditions:** An operator navigates across source, production, review, or learning work.

**Required output or state transition:** Shared shell routes and category-module read/action contracts.

**Authority and invariants:**
- Modules do not duplicate canonical state or authority.
- A module loads only relevant tools and evidence.
- Future Character Performance remains deferred.

**Acceptance scenarios**

- **Primary success:** Given a source-led batch, when the operator moves from Interview to Video to Static review, then all modules display the same source and campaign identities.
- **Adversarial or denial case:** Given a module attempting to own VAE state locally, when architecture tests run, then the duplication is rejected.
- **Evidence required:** Route/read-model integration tests, shared identity consistency, product-boundary tests, and accessibility review.

**Governing decisions:** D048  
**Exact source references:** SRC-AM-001, SRC-MIG-001


### FR-159 — Support AUTOPILOT, REVIEW_BEFORE_SHIP, CHECKPOINTED, and SHADOW modes

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Campaign and Harness bindings shall declare one autonomy mode, allowed human gates, publication authority, exception policy, and mode changes, with mature Harnesses targeting AUTOPILOT or REVIEW_BEFORE_SHIP rather than continuous manual editing.

**Trigger and preconditions:** A campaign is configured or its governance mode changes.

**Required output or state transition:** A versioned autonomy policy and mode-specific workflow behavior.

**Authority and invariants:**
- Mode changes are authorized and receipted.
- SHADOW never publishes.
- AUTOPILOT still escalates genuine authority or operator-owned creative conflicts.

**Acceptance scenarios**

- **Primary success:** Given CHECKPOINTED mode, when a declared creative gate is reached, then the Studio pauses with a complete decision package.
- **Adversarial or denial case:** Given AUTOPILOT mode and a deterministic validation pass, when no human-owned conflict exists, then the system does not ask for approval.
- **Evidence required:** Mode transition tests, gate/publish enforcement, exception simulations, and receipts.

**Governing decisions:** D048  
**Exact source references:** SRC-AM-001, SRC-AM-002


### FR-160 — Provide exception-only review packages and attributable decisions

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** When human attention is required, the Studio shall present the exact issue, source and current state, candidates or alternatives, evaluator evidence, authority owner, costs and downstream effects, and permitted actions without forcing the operator to inspect raw logs or rebuild the work.

**Trigger and preconditions:** A human gate, taste boundary, policy conflict, budget change, or unrecoverable exception occurs.

**Required output or state transition:** A structured ReviewPackage and subsequent HumanResolutionEpisode.

**Authority and invariants:**
- Only assigned authority sees actionable decisions.
- Deterministic facts are not disguised as creative choices.
- Unavailable evidence is disclosed.

**Acceptance scenarios**

- **Primary success:** Given two valid composition candidates with unresolved taste, when review opens, then the operator sees their source lineage, differences, evaluations, and expected downstream effects.
- **Adversarial or denial case:** Given a worker crash with an automatic retry policy, when no human action is needed, then it remains an operational incident rather than a creative review.
- **Evidence required:** Review completeness tests, role/permission checks, decision receipts, and operator usability evidence.

**Governing decisions:** D048, D052  
**Exact source references:** SRC-AM-001, SRC-AM-002


### FR-161 — Ship, export, or publish only under explicit authority and evidence

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** The Studio shall permit final acceptance, export, scheduling, or publication only when the derivative and campaign satisfy required technical, semantic, source authority, evaluation, lineage, and autonomy-mode gates, and shall record the human or policy authority responsible.

**Trigger and preconditions:** A derivative or batch is proposed for delivery or publication.

**Required output or state transition:** A publish/export command, delivery artifacts, metadata, signed URLs or integrations, usage records, and publication receipt.

**Authority and invariants:**
- Review-before-ship requires final acceptance.
- Source authority and revocation are rechecked at publish time.
- Publication does not imply certification.

**Acceptance scenarios**

- **Primary success:** Given a passed short in REVIEW_BEFORE_SHIP mode, when the operator approves, then the final artifact and source/evidence bundle are exported and the decision is captured.
- **Adversarial or denial case:** Given a passed SHADOW artifact, when publish is requested, then the command is denied.
- **Evidence required:** Delivery-profile validation, source-authority checks, mode/authority tests, artifact hashes, and publication receipt.

**Governing decisions:** D048, D054  
**Exact source references:** SRC-AM-001, SRC-AM-002


### FR-162 — Route each Harness to the correct supervisory surfaces and live read models

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Every Atomic Harness or derivative job shall declare its primary and supporting Studio surfaces, operator-entry policy, visible evidence, permitted commands, and realtime projections without allowing the Studio plugin to change Harness meaning or runtime ownership.

**Trigger and preconditions:** A Harness is imported, bound, or launched.

**Required output or state transition:** A StudioSurfaceBinding and validated module/read-model/action configuration.

**Authority and invariants:**
- UI plugins are nonauthoritative projections.
- Unsupported surfaces cannot infer tools or state.
- Module version changes are compatibility-tested.

**Acceptance scenarios**

- **Primary success:** Given a short-video Harness, when imported, then Video Production is primary and Visual Asset and Knowledge/Model modules are supporting surfaces with bounded commands.
- **Adversarial or denial case:** Given a plugin that exposes an ungranted provider action, when binding validation runs, then the plugin/action is rejected.
- **Evidence required:** Surface-binding schema, permission/action tests, realtime projection tests, and compatibility receipt.

**Governing decisions:** D048, D049  
**Exact source references:** SRC-AM-001, SRC-CUR-004, SRC-CUR-010


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes campaign launch, module routing, autonomy tests, review packages, publication controls, and live read-model consistency. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

## 9. Risks, mitigations, and stop conditions

| Risk | Concrete consequence | Mitigation |
|---|---|---|
| Authority drift | A predecessor, external project, UI, model, or renderer is treated as current product authority. | Require exact source disposition, current authority validation, and product-boundary tests. |
| False completion | A synthetic URI, dry-run, unverified command, or model self-report is promoted as a real result. | Require actual files, hashes, independent validation, and artifact-class labels. |
| Over-broad automation | A model or agent gains tools, context, or authority beyond the current node. | Use JIT context, node-local tool grants, sandboxes, and explicit escalation. |
| Hidden mutation | Accepted meaning, source, program, or human preference changes without a versioned record. | Use immutable versions, typed commands, receipts, and selective invalidation. |

**Stop conditions**

- The behavior would create a second semantic or canonical state owner.
- A required source, authority, contract, primitive coalition, archetype, Final Script, runtime, evaluator, or human decision is unavailable or unverified.
- The implementation would treat migration evidence or an external project as current authority.
- The change would imply real output, production readiness, or certification beyond available evidence.

## 10. Planning and implementation handoff

This module is implementation-ready only after its FRs have one primary vertical Story owner, its Stories pass CBAR hardening, its candidate Tech Specs identify exact existing code and target paths, and Program Control issues a bounded Development Capsule. Until then, this module is a product-authority draft.

*This feature module belongs to the Conscious Activations Atomic Harness Pipeline PRD V1.1 source-first reconciliation package.*
