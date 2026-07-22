---
type: technical_specification
spec_id: TS-AIR-005
product: Conscious Activations Activative Intelligence Runtime
feature_id: F05
title: Primitive Coalition Contract, Coalition Signature, Edge Product, and Steering
  Recipes
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-025
- AIR-FR-026
- AIR-FR-027
- AIR-FR-028
- AIR-FR-029
- AIR-FR-030
controlling_stories:
- AIR-ST-05.01
- AIR-ST-05.02
- AIR-ST-05.03
active_primitives:
- PRM-PRS-002
- PRM-PRS-009
- PRM-PRS-015
target_module: src/cmf_activative_intelligence/primitive_coalition_signature_edge_product_and_steering_recipes.py
target_service: src/cmf_activative_intelligence/services/primitive_coalition_signature_edge_product_and_steering_recipes_service.py
target_test: tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py
---

# TS-AIR-005 — Primitive Coalition Contract, Coalition Signature, Edge Product, and Steering Recipes

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F05-primitive-coalition-signature-edge-product-and-steering-recipes.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-05.01, AIR-ST-05.02, AIR-ST-05.03 |
| SRC-PRIM-001 | `sources/doctrine/MEANING_PRIMITIVE_REGISTRY_SPEC.md` | Meaning Primitive Registry specification |
| SRC-PRIM-002 | `sources/doctrine/EXPERIENCE_PRIMITIVE_REGISTRY_SPEC.md` | Experience Primitive Registry specification |
| SRC-PRIM-003 | `sources/cmf_primitive_registry_snapshot` | CMF full primitive YAML snapshot |
| SRC-MOE-001 | `sources/doctrine/MATRIX_OF_EDGING.md` | Matrix of Edging |
| SRC-AHP-F29-001 | `sources/doctrine/F29-primitive-first-coalition-composition-and-evaluation.md` | AHP F29 primitive-first coalition composition and evaluation |
| PRM-PRS-002 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-002.yaml` | exact Primitive YAML |
| PRM-PRS-009 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-009.yaml` | exact Primitive YAML |
| PRM-PRS-015 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/primitive_coalition_compiler_service.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

No single primitive constitutes the creative recipe. The coalition defines primary force, supporting behaviors, suppression, conflict, signature, Edge Product, and misuse risks. Steering Recipes are evidence-backed operationalizations of proven coalitions. A weak implementation would treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation, which leads to this concrete failure: the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode

### Solution

Implement the feature as a versioned domain service around `PrimitiveCoalitionContract`, `CoalitionSignature`, `EdgeProduct`, `PrimitiveMisuseRisk`, `PrimitiveEvaluationReceipt`, `SteeringRecipeCandidate`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

### In scope

- domain models and generated schemas for the controlling objects
- immutable repository and lifecycle transitions
- exact source, Primitive, product-owner, and epistemic-state validation
- feature-specific compilation or decision service
- independent evaluation and typed blocker outcomes
- HumanResolution capture, observability, replay, supersession, and descendant invalidation
- typed cross-product input and output adapters

### Non-goals

- creating a second Activative Constitution, Primitive definition, archetype authority, source package, Atomic Harness, or workflow state store
- letting a model, renderer, provider, or UI projection own semantic acceptance
- starting downstream composition or production before the feature terminal gate passes
- claiming real-human, audience, external-product, or production evidence from local structural tests

## 3. Context for Development

### 3.1 Architecture traceability

| FR | Story | Canonical output | Downstream consumer |
|---|---|---|---|
| `AIR-FR-025` | `AIR-ST-05.01` | `PrimitiveCoalitionContract` | F06 |
| `AIR-FR-026` | `AIR-ST-05.01` | `CoalitionSignature` | F06 |
| `AIR-FR-027` | `AIR-ST-05.02` | `EdgeProduct` | F06 |
| `AIR-FR-028` | `AIR-ST-05.02` | `PrimitiveMisuseRisk` | F06 |
| `AIR-FR-029` | `AIR-ST-05.03` | `PrimitiveEvaluationReceipt` | F06 |
| `AIR-FR-030` | `AIR-ST-05.03` | `SteeringRecipeCandidate` | F06 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/src/ccp_studio/services/primitive_coalition_compiler_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/primitive_coalition_signature_edge_product_and_steering_recipes.py` with service orchestration in `src/cmf_activative_intelligence/services/primitive_coalition_signature_edge_product_and_steering_recipes_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |
| `PRM-PRS-009` — The McKee Inciting Incident Engine | meaning_plane / `persuasion` | Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. | False Jeopardy — fabricating an inciting incident that feels contrived or hyperbolic, instantly destroying Ethos; Stranded Disequilibrium — introducing a powerful inciting incident but failing to provide a coherent or satisfying path to restoring balance |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-05.01` | `PRM-PRS-002` | Compile a complete Primitive Coalition Contract must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-05.02` | `PRM-PRS-009` | Resolve Coalition Signature and Edge Product must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-05.03` | `PRM-PRS-015` | Promote evidence into Steering Recipes and Primitive Evaluation Receipts must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |

### 3.5 Technical decisions

1. Canonical objects are immutable Pydantic-style models with `extra=forbid`, stable serialization, and SHA-256 identity.
2. Object payload and lifecycle events are stored separately so historical versions remain replayable.
3. Field-level epistemic states are explicit for material claims; one object status cannot erase field differences.
4. Primitive and archetype evidence is resolved through exact registry adapters before model inference.
5. Deterministic hard gates run before any learned ranking or judgment.
6. The producer and independent evaluator use separate implementation identities and evidence stores.
7. Human decisions enter through typed commands and emit HumanResolutionEpisodes; no hidden UI mutation is authoritative.
8. Cross-product writes occur only through the owning adapter or Delegation contract.
## 4. Implementation Plan

### Stage 0 — Source and contract lock
- Materialize a Development Capsule containing this spec, controlling feature, Stories, source lock, selected Primitive YAMLs, predecessor files, and exact target allowlist.
- Reconcile current product versions and cross-product contract pins. Fail if any owner or source remains ambiguous.
### Stage 1 — Domain models and schemas
- Implement or extend `PrimitiveCoalitionContract`, `CoalitionSignature`, `EdgeProduct`, `PrimitiveMisuseRisk`, `PrimitiveEvaluationReceipt`, `SteeringRecipeCandidate` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/primitive_coalition_signature_edge_product_and_steering_recipes_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-025, AIR-FR-026, AIR-FR-027, AIR-FR-028, AIR-FR-029, AIR-FR-030. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `PrimitiveCoalitionContract` shared envelope

| Field | Type | Purpose |
|---|---|---|
| `id` | `string` | stable object identity |
| `version` | `string` | immutable semantic version |
| `content_sha256` | `hex string` | canonical object hash |
| `lifecycle_state` | `enum` | current state under the controlling state machine |
| `epistemic_state` | `enum or field map` | planned, observed, inferred, operator-confirmed, rejected, or superseded as applicable |
| `source_refs` | `array<ImmutableRef>` | exact source and predecessor identities |
| `owner_product` | `string` | product sovereignty owner |
| `produced_by` | `actor identity` | deterministic module, model program, agent program, or human |
| `evaluation_receipt_refs` | `array<ImmutableRef>` | independent and deterministic verdicts |
| `supersedes_ref` | `ImmutableRef?` | additive successor relation |
| `primitive_bindings` | `array<PrimitiveBinding>` | exact YAML versions and local functions |
| `coalition_signature` | `CoalitionSignature?` | structural identity of compatible bindings |
| `edge_product_ref` | `ImmutableRef?` | surviving pressure-role product |

### State-transition envelope

```yaml
command_id: string
expected_prior_version: immutable_ref | null
input_refs: [immutable_ref]
requested_transition: string
actor:
  actor_id: string
  actor_type: deterministic_module | model_program | agent_program | human
  workflow_role: hunter | analyst | composer | commander | interviewer | evaluator
product_owner: string
context_capsule_ref: immutable_ref
result_ref: immutable_ref | null
blocker:
  code: string
  responsible_owner: string
  next_admissible_action: string
receipt_ref: immutable_ref
```

Schema implementations must extend existing AI2 models where compatible. They may not duplicate the same object under a new name merely to simplify a local service.

## 6. Backward Compatibility, Migration, Fallback, and Rollback

- **V2 compatibility:** preserve readable V2 object versions and provide an explicit V2→V2.1 adapter that marks absent Primitive, archetype, brand, role/tension, and Final Script fields as unavailable rather than inferred.
- **CMF predecessor compatibility:** import only files with an approved REUSE/ADAPT disposition. Historical archetype prompts remain evidence and cannot become live profiles automatically.
- **Fallback:** when the feature-specific learned implementation is unavailable or outside evidence, use the deterministic baseline or approved stronger-model path declared in the binding. Silent substitution is prohibited.
- **Rollback:** restore the last known-good service/model/registry version while preserving incidents and outputs produced under the failed version.
- **Invalidation:** superseding an upstream object invalidates typed descendants only; it does not rewrite historical artifacts or HumanResolutionEpisodes.
- **Format 02:** no migration path in this spec may activate Format 02. That requires a current independently validated Atomic Harness.
## 7. Implementation Tasks

| Task | Exact target | Completion evidence |
|---|---|---|
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-005/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/primitive_coalition_signature_edge_product_and_steering_recipes.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/primitive_coalition_signature_edge_product_and_steering_recipes_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/primitive_coalition_signature_edge_product_and_steering_recipes.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/primitive_coalition_signature_edge_product_and_steering_recipes_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/primitive_coalition_signature_edge_product_and_steering_recipes_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/primitive_coalition_signature_edge_product_and_steering_recipes.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-025: Compile primary, support, suppression, and conflict roles

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Compile primary, support, suppression, and conflict roles` using exact current inputs
- **Then** A Primitive Coalition Contract shall classify every bound primitive by functional role and state why the coalition requires or excludes it.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.01` — Compile a complete Primitive Coalition Contract must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_025`

### AC-02 — AIR-FR-026: Compute a stable Coalition Signature

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Compute a stable Coalition Signature` using exact current inputs
- **Then** The Runtime shall derive a versioned Coalition Signature that identifies the coalition’s distinctive activation geometry across source, script, composition, and experience.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.01` — Compile a complete Primitive Coalition Contract must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_026`

### AC-03 — AIR-FR-027: Evaluate coalition conflicts and Primitive Misuse Risk

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Evaluate coalition conflicts and Primitive Misuse Risk` using exact current inputs
- **Then** The Runtime shall test fatal conflicts, overload, misuse modes, anti-patterns, and role collapse before the coalition becomes eligible.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.02` — Resolve Coalition Signature and Edge Product must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_027`

### AC-04 — AIR-FR-028: Compile the Edge Product

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Compile the Edge Product` using exact current inputs
- **Then** The coalition shall emit an Edge Product that states the distinctive pressure, role, tension, and usable creative consequence produced by the survived combination.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.02` — Resolve Coalition Signature and Edge Product must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_028`

### AC-05 — AIR-FR-029: Use coalitions as the basis of Steering Recipes

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Use coalitions as the basis of Steering Recipes` using exact current inputs
- **Then** A Steering Recipe candidate shall reference the coalition, applicability envelope, intervention, preserved properties, evidence, failures, and rollback rather than free-floating taste instructions.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.03` — Promote evidence into Steering Recipes and Primitive Evaluation Receipts must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_029`

### AC-06 — AIR-FR-030: Issue Primitive Evaluation Receipts

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the service executes `Issue Primitive Evaluation Receipts` using exact current inputs
- **Then** Independent evaluation shall report primitive presence, function, interactions, misuse, coalition integrity, Edge Product fidelity, and failure attribution.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-05.03` — Promote evidence into Steering Recipes and Primitive Evaluation Receipts must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **Test location:** `tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py::test_air_fr_030`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `PrimitiveCoalitionContract` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

### AC-08 — Human Resolution equivalence

- Given an operator makes the same semantic correction through natural language and direct manipulation, when both compile successfully, then they produce equivalent typed change semantics and HumanResolution evidence.
- Failure example: direct manipulation bypasses attribution or changes hidden canonical state. The command is rejected and the projection is restored from canonical records.

## 9. Dependencies

### Internal

- Program Control authority and current status receipt.
- V2.1 Constitution, source register, Primitive inventory, archetype evidence registry, and decision register.
- Immutable object, lifecycle, receipt, dependency, JIT context, evaluation, HumanResolution, and cross-product handoff services.
- Controlling upstream feature objects and downstream consumer contracts.

### Brownfield

- `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py`
- `source://cmf_studio/src/ccp_studio/services/primitive_coalition_compiler_service.py`

### External or model dependencies

- Any model, embedding system, VLM, renderer, provider, or orchestration framework must be pinned in a separate implementation binding and cannot become semantic authority.
- Technical security, isolation, and secret management remain mandatory even though creative direction is operator-governed.
## 10. Testing and Evidence Strategy

1. **Schema tests:** valid, missing-field, unknown-field, stale-version, contradictory-state, and canonical-hash fixtures.
2. **Primitive tests:** exact YAML resolution, core-move preservation, conflict, misuse, and name-similarity rejection.
3. **Domain tests:** every FR positive and adversarial scenario plus all lifecycle transitions.
4. **CBAR tests:** each Story shortcut is implemented as a negative fixture and must fail for the exact mandate reason.
5. **Repository tests:** idempotency, optimistic concurrency, atomic receipt commit, replay, supersession, and descendant invalidation.
6. **Model-program tests:** applicability, tool grants, JIT context, baseline comparison, independent evaluation, fallback, and out-of-envelope escalation.
7. **Cross-product conformance:** producer and consumer both validate exact schema, authority, lifecycle, and limitations.
8. **Studio tests:** projections are reconstructable; commands are typed; natural-language and direct-manipulation paths emit equivalent HumanResolution evidence.
9. **Clean-environment tests:** install and run the complete suite without absolute paths, undeclared files, or hidden local state.
10. **Evidence claim:** local structural tests may support implementation-development claims only. Real source activation, audience effectiveness, external integration, production, and certification remain separate evidence classes.
