---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F03
title: "Workflow Node Execution Kernel and Bounded Role Taxonomy"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-013–FR-018"
---

# F03 — Workflow Node Execution Kernel and Bounded Role Taxonomy

## 1. Product claim and user outcome

**User outcome:** The Pipeline executes explicit Workflow Nodes within governed Phase boundaries and keeps actor, ownership, role, authority, and product boundary distinct.

Provide the smallest auditable unit of execution and represent Hunters, Analysts, Composers, Commanders, humans, deterministic modules, models, and products without hidden ownership. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

The owning product is the Atomic Harness Pipeline unless an FR explicitly assigns Interview Expression, VAE, Delegation, Studio, Program Control, or an external runtime.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-CUR-007` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py | Category-native runtime plan requirements, evaluation dimensions and repair units. |
| `SRC-CUR-008` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py | Current broad Capability Ownership graph and explicit handoff evidence. |
| `SRC-CUR-010` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py | Execution-free Workflow Node, edge, authority and validation contracts. |
| `SRC-LEG-001` | `ADAPT` | src/ccp_studio/contracts/studio_pipeline_recipe_harness.py | Old recipe/step contracts become a compatibility input to Workflow IR; they cannot define current meaning. |
| `SRC-LEG-002` | `ADAPT` | src/ccp_studio/services/pipeline_run_service.py | Reuse run-state behavior after durable-state and receipt reconciliation. |
| `SRC-LEG-003` | `ADAPT` | src/ccp_studio/services/pipeline_step_run_service.py | Map legacy steps to current Workflow Nodes. |

## 5. Workflow integration

Validated upstream state → feature behavior → typed output and receipt → downstream handoff → evaluation, invalidation, and replay.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-013 — Compile phases into Workflow Nodes

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Each phase shall contain explicit Workflow Nodes that reference the capabilities they realize and the typed handoffs between them.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Compile phases into Workflow Nodes` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then each phase shall contain explicit Workflow Nodes that reference the capabilities they realize and the typed handoffs between them and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


### FR-014 — Declare four independent classifications

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Every Workflow Node shall declare execution actor, Capability Ownership class, workflow role and product boundary.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Declare four independent classifications` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then every Workflow Node shall declare execution actor, Capability Ownership class, workflow role and product boundary and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


### FR-015 — Schedule dependencies deterministically

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The scheduler shall enforce acyclic dependencies, gate conditions, eligible parallelism and deterministic ready-order behavior.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Schedule dependencies deterministically` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the scheduler shall enforce acyclic dependencies, gate conditions, eligible parallelism and deterministic ready-order behavior and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


### FR-016 — Validate every handoff

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** A downstream node may start only from a producer output that passed its declared contract and handoff validation.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Validate every handoff` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then a downstream node may start only from a producer output that passed its declared contract and handoff validation and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


### FR-017 — Represent humans and products explicitly

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Human authority and independent product calls shall be visible Workflow Nodes rather than hidden tool calls.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Represent humans and products explicitly` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then human authority and independent product calls shall be visible Workflow Nodes rather than hidden tool calls and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


### FR-018 — Emit immutable node receipts

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Every node attempt shall record inputs, JIT Capsule, implementation, actions, output, validation, status, timing, cost and lineage.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Emit immutable node receipts` within feature F03.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Every node has one declared actor and owner.
- Handoffs are typed and validated.
- Roles never imply authority beyond their assigned node.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then every node attempt shall record inputs, JIT Capsule, implementation, actions, output, validation, status, timing, cost and lineage and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts, linked to an immutable requirement receipt.

**Governing decisions:** D009, D010, D011, D020, D037  
**Exact source references:** SRC-CUR-007, SRC-CUR-008, SRC-CUR-010, SRC-LEG-001, SRC-LEG-002, SRC-LEG-003


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes graph validation, scheduling tests, handoff conformance, actor/role matrices, and node receipts. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

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
