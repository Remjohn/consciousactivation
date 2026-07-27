---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F02
title: "Atomic Harness Intake and Execution Binding"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-007–FR-012"
---

# F02 — Atomic Harness Intake and Execution Binding

## 1. Product claim and user outcome

**User outcome:** The Pipeline consumes the existing AtomicHarnessDefinition and binds it to approved implementations without creating a second Harness truth.

Turn an immutable Builder product into an executable deployment binding while keeping meaning and implementation separate. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

The owning product is the Atomic Harness Pipeline unless an FR explicitly assigns Interview Expression, VAE, Delegation, Studio, Program Control, or an external runtime.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-CUR-004` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py | Canonical AtomicHarnessDefinition structure and execution-free status. |
| `SRC-CUR-008` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py | Current broad Capability Ownership graph and explicit handoff evidence. |
| `SRC-CUR-010` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py | Execution-free Workflow Node, edge, authority and validation contracts. |
| `SRC-LEG-001` | `ADAPT` | src/ccp_studio/contracts/studio_pipeline_recipe_harness.py | Old recipe/step contracts become a compatibility input to Workflow IR; they cannot define current meaning. |

## 5. Workflow integration

Validated upstream state → feature behavior → typed output and receipt → downstream handoff → evaluation, invalidation, and replay.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-007 — Load exact AtomicHarnessDefinition

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The Pipeline shall ingest a portable AtomicHarnessDefinition package and verify schema, identity, hash, authority, lineage, category/profile and invalidation state.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Load exact AtomicHarnessDefinition` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the Pipeline shall ingest a portable AtomicHarnessDefinition package and verify schema, identity, hash, authority, lineage, category/profile and invalidation state and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


### FR-008 — Validate the complete Harness graph

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The intake gate shall reconcile capabilities, responsibility modules, phases, handoffs, context manifests, Skills, evaluation requirements and repair laws.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Validate the complete Harness graph` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the intake gate shall reconcile capabilities, responsibility modules, phases, handoffs, context manifests, Skills, evaluation requirements and repair laws and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


### FR-009 — Compile HarnessExecutionBindingManifest

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** A separate immutable binding shall map every executable requirement to deterministic modules, Model Programs, Agent Programs, humans, products and runtime embodiments.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Compile HarnessExecutionBindingManifest` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then a separate immutable binding shall map every executable requirement to deterministic modules, Model Programs, Agent Programs, humans, products and runtime embodiments and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


### FR-010 — Forbid semantic mutation by binding

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** A binding may choose an implementation but may not change the Harness purpose, phase semantics, declared invariants, creative degrees of freedom or wrong-reading locks.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Forbid semantic mutation by binding` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then a binding may choose an implementation but may not change the Harness purpose, phase semantics, declared invariants, creative degrees of freedom or wrong-reading locks and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


### FR-011 — Fail on unresolved ownership

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** A required capability without an explicit eligible implementation, human gate or external-product route shall block execution before any side effect.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Fail on unresolved ownership` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then a required capability without an explicit eligible implementation, human gate or external-product route shall block execution before any side effect and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


### FR-012 — Support supersession and invalidation

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Bindings and imported Harnesses shall support immutable supersession, revocation, migration impact and historical replay.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Support supersession and invalidation` within feature F02.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Builder remains canonical.
- Bindings select implementations but do not mutate Harness semantics.
- Unresolved capability ownership blocks side effects.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then bindings and imported Harnesses shall support immutable supersession, revocation, migration impact and historical replay and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay, linked to an immutable requirement receipt.

**Governing decisions:** D006, D007, D008, D032, D033  
**Exact source references:** SRC-CUR-004, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes schema/hash validation, graph reconciliation, binding manifest, compatibility tests, supersession and replay. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

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
