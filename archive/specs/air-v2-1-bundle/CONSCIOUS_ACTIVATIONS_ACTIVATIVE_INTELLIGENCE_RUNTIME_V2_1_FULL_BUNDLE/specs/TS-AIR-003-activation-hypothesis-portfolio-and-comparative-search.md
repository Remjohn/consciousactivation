---
type: technical_specification
spec_id: TS-AIR-003
product: Conscious Activations Activative Intelligence Runtime
feature_id: F03
title: Activation Hypothesis Portfolio and Comparative Search
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-013
- AIR-FR-014
- AIR-FR-015
- AIR-FR-016
- AIR-FR-017
- AIR-FR-018
controlling_stories:
- AIR-ST-03.01
- AIR-ST-03.02
- AIR-ST-03.03
active_primitives:
- PRM-PSY-001
- PRM-PRS-015
- PRM-HUM-021
target_module: src/cmf_activative_intelligence/activation_hypothesis_portfolio_and_comparative_search.py
target_service: src/cmf_activative_intelligence/services/activation_hypothesis_portfolio_and_comparative_search_service.py
target_test: tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py
---

# TS-AIR-003 — Activation Hypothesis Portfolio and Comparative Search

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F03-activation-hypothesis-portfolio-and-comparative-search.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-03.01, AIR-ST-03.02, AIR-ST-03.03 |
| SRC-AI2-002 | `sources/ai_v2_predecessor/05_PRODUCT_REQUIREMENTS_V2.md` | Integrated Activative Intelligence V2 Product Requirements |
| SRC-AHP-PORTFOLIO-001 | `sources/doctrine/AHP_F08_CANDIDATE_SEARCH.md` | AHP adaptive candidate search feature |
| SRC-CBAR-001 | `sources/spec_methods/SKILL_CBAR_Epic_Story_Hardening.md` | CBAR Epic and Story Hardening Skill |
| SRC-MOE-001 | `sources/doctrine/MATRIX_OF_EDGING.md` | Matrix of Edging |
| PRM-PSY-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | exact Primitive YAML |
| PRM-PRS-015 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | exact Primitive YAML |
| PRM-HUM-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/candidate_search.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

A single first answer is a convergence accident. Activative Intelligence needs portfolios that vary role, tension, pressure, direction, primitive coalition, and relationship move while preserving hard source and authority constraints. A weak implementation would accept the first fluent hypothesis and skip comparative search, which leads to this concrete failure: the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly

### Solution

Implement the feature as a versioned domain service around `ActivationHypothesis`, `ActivationHypothesisPortfolio`, `HypothesisGateResult`, `ComparativeEvaluationReceipt`, `SearchStoppingReceipt`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-013` | `AIR-ST-03.01` | `ActivationHypothesis` | F04 |
| `AIR-FR-014` | `AIR-ST-03.01` | `ActivationHypothesisPortfolio` | F04 |
| `AIR-FR-015` | `AIR-ST-03.02` | `HypothesisGateResult` | F04 |
| `AIR-FR-016` | `AIR-ST-03.02` | `ComparativeEvaluationReceipt` | F04 |
| `AIR-FR-017` | `AIR-ST-03.03` | `SearchStoppingReceipt` | F04 |
| `AIR-FR-018` | `AIR-ST-03.03` | `SearchStoppingReceipt` | F04 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/candidate_search.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/activation_hypothesis_portfolio_and_comparative_search.py` with service orchestration in `src/cmf_activative_intelligence/services/activation_hypothesis_portfolio_and_comparative_search_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |
| `PRM-HUM-021` — Irony Inversion | meaning_plane / `humor_distortion` | Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. | Irony without conviction — breaking voice through tone markers (caps, emojis, 'just kidding') that expose the reversal prematurely; Irony without Subtext — reversing a statement that has no underlying value judgment, producing confusion rather than comedy |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-03.01` | `PRM-PSY-001` | Generate meaningfully different activation hypotheses must preserve Matching Principle's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-03.02` | `PRM-PRS-015` | Compare candidates under non-compensable gates must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-03.03` | `PRM-HUM-021` | Converge while preserving rejections and stopping evidence must preserve Irony Inversion's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `ActivationHypothesis`, `ActivationHypothesisPortfolio`, `HypothesisGateResult`, `ComparativeEvaluationReceipt`, `SearchStoppingReceipt` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/activation_hypothesis_portfolio_and_comparative_search_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-013, AIR-FR-014, AIR-FR-015, AIR-FR-016, AIR-FR-017, AIR-FR-018. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `ActivationHypothesis` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-003/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/activation_hypothesis_portfolio_and_comparative_search.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/activation_hypothesis_portfolio_and_comparative_search_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/activation_hypothesis_portfolio_and_comparative_search.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/activation_hypothesis_portfolio_and_comparative_search_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/activation_hypothesis_portfolio_and_comparative_search_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/activation_hypothesis_portfolio_and_comparative_search.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-013: Generate a strategically diverse hypothesis portfolio

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Generate a strategically diverse hypothesis portfolio` using exact current inputs
- **Then** The Runtime shall generate multiple eligible activation hypotheses that differ in psychological role, tension, direction, pressure path, primitive coalition, or relationship move rather than merely surface wording.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.01` — Generate meaningfully different activation hypotheses must preserve Matching Principle's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_013`

### AC-02 — AIR-FR-014: Apply hard eligibility gates before scoring

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Apply hard eligibility gates before scoring` using exact current inputs
- **Then** Source fidelity, epistemic legality, identity fit, domain fit, operator constraints, and fatal primitive conflicts shall remove ineligible hypotheses before comparative scoring.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.01` — Generate meaningfully different activation hypotheses must preserve Matching Principle's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_014`

### AC-03 — AIR-FR-015: Score hypotheses against the current objective

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Score hypotheses against the current objective` using exact current inputs
- **Then** Eligible hypotheses shall be compared against the current source, audience, relationship stage, desired state transition, counteractivation risk, freshness, and downstream derivative potential.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.02` — Compare candidates under non-compensable gates must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_015`

### AC-04 — AIR-FR-016: Preserve rejected and repaired hypotheses

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Preserve rejected and repaired hypotheses` using exact current inputs
- **Then** The portfolio shall retain rejected, superseded, and repaired candidates with exact reasons, responsible layers, and possible future applicability.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the responsible layer is unknown or the proposed repair would regenerate valid upstream work; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.02` — Compare candidates under non-compensable gates must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_016`

### AC-05 — AIR-FR-017: Use explicit search stopping laws

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Use explicit search stopping laws` using exact current inputs
- **Then** Search shall stop on a decisive eligible winner, shared defect, exhausted diversity, budget boundary, or operator-owned ambiguity rather than arbitrary iteration count.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.03` — Converge while preserving rejections and stopping evidence must preserve Irony Inversion's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_017`

### AC-06 — AIR-FR-018: Promote one selected hypothesis into a planned program

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the service executes `Promote one selected hypothesis into a planned program` using exact current inputs
- **Then** Promotion shall create a new Planned Activative Intelligence object that references the complete portfolio and evaluation receipt without erasing alternatives.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state; a weak implementation would continue and the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-03.03` — Converge while preserving rejections and stopping evidence must preserve Irony Inversion's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search.
- **Test location:** `tests/integration/test_activation_hypothesis_portfolio_and_comparative_search.py::test_air_fr_018`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `ActivationHypothesis` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/candidate_search.py`

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
