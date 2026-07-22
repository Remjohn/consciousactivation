---
type: technical_specification
spec_id: TS-AIR-020
product: Conscious Activations Activative Intelligence Runtime
feature_id: F20
title: Programmed Models, Independent Evaluation, Product Integration, and Evidence
  Promotion
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_C_EVIDENCE_PROMOTION_AND_PRODUCTIZATION
controlling_frs:
- AIR-FR-115
- AIR-FR-116
- AIR-FR-117
- AIR-FR-118
- AIR-FR-119
- AIR-FR-120
controlling_stories:
- AIR-ST-20.01
- AIR-ST-20.02
- AIR-ST-20.03
active_primitives:
- PRM-BUS-001
- EXP-PRG-002
- EXP-TRG-005
target_module: src/cmf_activative_intelligence/programmed_models_independent_evaluation_and_product_integration.py
target_service: src/cmf_activative_intelligence/services/programmed_models_independent_evaluation_and_product_integration_service.py
target_test: tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py
---

# TS-AIR-020 — Programmed Models, Independent Evaluation, Product Integration, and Evidence Promotion

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F20-programmed-models-independent-evaluation-and-product-integration.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-20.01, AIR-ST-20.02, AIR-ST-20.03 |
| SRC-AI2-MODEL-001 | `sources/ai_v2_predecessor/reference_implementation/models.py` | AI2 reference implementation models |
| SRC-AHP-MODEL-001 | `sources/doctrine/AHP_F07_PROGRAMMED_MODELS.md` | AHP Programmed Model and learned claims feature |
| SRC-HARNESS-RESEARCH-001 | `sources/research/Better_Harnesses_Smaller_Models.pdf` | Better Harnesses, Smaller Models research paper |
| SRC-RECENT-001 | `sources/research/Efficient_Skill_Grounding_RECENT.pdf` | Efficient Skill Grounding via Code Refactoring with Small Language Models |
| PRM-BUS-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-001.yaml` | exact Primitive YAML |
| EXP-PRG-002 | `sources/cmf_primitive_registry_snapshot/experience_plane/progression_replay/EXP-PRG-002.yaml` | exact Primitive YAML |
| EXP-TRG-005 | `sources/cmf_primitive_registry_snapshot/experience_plane/trigger_timing/EXP-TRG-005.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/dspy_signatures.py` | exact predecessor review before implementation |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

A Programmed Model is a versioned learned capability claim inside a governed harness. It is not Activative authority. Better harnesses, retrieval, Skills, Primitive coalitions, and execution bindings should carry stable task difficulty before larger models or new training are used. A weak implementation would use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation, which leads to this concrete failure: a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient

### Solution

Implement the feature as a versioned domain service around `ProgrammedModelArtifact`, `LearnedCapabilityClaim`, `ModelProgramBinding`, `HarnessProfile`, `IndependentEvaluationReceipt`, `ProductHandoffReceipt`, `PromotionReceipt`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-115` | `AIR-ST-20.01` | `ProgrammedModelArtifact` | cross-product release and evidence |
| `AIR-FR-116` | `AIR-ST-20.01` | `LearnedCapabilityClaim` | cross-product release and evidence |
| `AIR-FR-117` | `AIR-ST-20.02` | `ModelProgramBinding` | cross-product release and evidence |
| `AIR-FR-118` | `AIR-ST-20.02` | `HarnessProfile` | cross-product release and evidence |
| `AIR-FR-119` | `AIR-ST-20.03` | `IndependentEvaluationReceipt` | cross-product release and evidence |
| `AIR-FR-120` | `AIR-ST-20.03` | `ProductHandoffReceipt` | cross-product release and evidence |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/dspy_signatures.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/programmed_models_independent_evaluation_and_product_integration.py` with service orchestration in `src/cmf_activative_intelligence/services/programmed_models_independent_evaluation_and_product_integration_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-BUS-001` — Perception and Guidance Stack | meaning_plane / `design_business` | Design visuals, text hierarchy, and action cues as one integrated system that controls where the eye goes and what the hand does next. | Dark Patterns — Using strong affordances to trick the user into an unintended action; Visual Noise — Adding fake depth or contrast that doesn't actually route attention |
| `EXP-PRG-002` — Discover -> On-board -> Immerse -> Master -> Replay | experience_plane / `progression_replay` | Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. | The Endless Tutorial — trapping users in the On-boarding phase for so long that they get bored and quit before experiencing the real product.; Feature Hiding as a Bug — making the UI so minimal that users don't even know what the product is supposed to do. |
| `EXP-TRG-005` — First Major Win-State | experience_plane / `trigger_timing` | Gate all social and expansion triggers behind a mathematically proven, hard-won success state, completely suppressing them during onboarding or failure. | Participation Trophies — lowering the bar for a 'win' so everyone gets it immediately.; Interrupting the actual Fiero moment with a clunky marketing funnel. |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-20.01` | `PRM-BUS-001` | Register Programmed Models and model-specific harnesses must preserve Perception and Guidance Stack's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-20.02` | `EXP-PRG-002` | Evaluate claims independently and integrate products through typed handoffs must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-20.03` | `EXP-TRG-005` | Promote evidence-backed capability claims and bounded release states must preserve First Major Win-State's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `ProgrammedModelArtifact`, `LearnedCapabilityClaim`, `ModelProgramBinding`, `HarnessProfile`, `IndependentEvaluationReceipt`, `ProductHandoffReceipt`, `PromotionReceipt` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/programmed_models_independent_evaluation_and_product_integration_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-115, AIR-FR-116, AIR-FR-117, AIR-FR-118, AIR-FR-119, AIR-FR-120. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `ProgrammedModelArtifact` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-020/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/programmed_models_independent_evaluation_and_product_integration.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/programmed_models_independent_evaluation_and_product_integration_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/programmed_models_independent_evaluation_and_product_integration.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/programmed_models_independent_evaluation_and_product_integration_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/programmed_models_independent_evaluation_and_product_integration_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/programmed_models_independent_evaluation_and_product_integration.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-115: Register exact Programmed Model artifacts and claims

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Register exact Programmed Model artifacts and claims` using exact current inputs
- **Then** Every learned implementation shall pin base model, tokenizer, adapter or checkpoint, runtime, training lineage, supported inputs, applicability envelope, limitations, and exact hashes.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.01` — Register Programmed Models and model-specific harnesses must preserve Perception and Guidance Stack's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_115`

### AC-02 — AIR-FR-116: Adapt the harness before increasing model size or training scope

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Adapt the harness before increasing model size or training scope` using exact current inputs
- **Then** The system shall diagnose instruction, knowledge, retrieval, tool, context, and planning failures and improve context, tools, checks, or orchestration before assuming a larger model is required.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.01` — Register Programmed Models and model-specific harnesses must preserve Perception and Guidance Stack's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_116`

### AC-03 — AIR-FR-117: Use independent, layer-specific evaluation

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Use independent, layer-specific evaluation` using exact current inputs
- **Then** Deterministic gates shall run first; semantic, Primitive, archetype, transfer, visual, and relationship judgments shall use independent calibrated evaluators and human labels where required.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.02` — Evaluate claims independently and integrate products through typed handoffs must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_117`

### AC-04 — AIR-FR-118: Preserve cross-product ownership through typed handoffs

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Preserve cross-product ownership through typed handoffs` using exact current inputs
- **Then** Program Control, Interview Expression, Builder, AHP, VAE, Delegation, and Studio shall exchange exact objects and receipts without duplicating semantic or execution ownership.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.02` — Evaluate claims independently and integrate products through typed handoffs must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_118`

### AC-05 — AIR-FR-119: Promote capability claims through evidence lifecycle

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Promote capability claims through evidence lifecycle` using exact current inputs
- **Then** Claims shall move through proposed, experimental, validated, shadow, limited-production, production, deprecated, retired, and revoked states with rollback and focused regression.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.03` — Promote evidence-backed capability claims and bounded release states must preserve First Major Win-State's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_119`

### AC-06 — AIR-FR-120: Generate a bounded release-readiness and implementation handoff

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the service executes `Generate a bounded release-readiness and implementation handoff` using exact current inputs
- **Then** The product shall emit exact Stories, Tech Specs, source dispositions, target paths, tests, evidence gaps, and authority gates; planning completeness shall not imply production readiness or certification.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-20.03` — Promote evidence-backed capability claims and bounded release states must preserve First Major Win-State's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **Test location:** `tests/integration/test_programmed_models_independent_evaluation_and_product_integration.py::test_air_fr_120`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `ProgrammedModelArtifact` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/dspy_signatures.py`
- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py`

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
