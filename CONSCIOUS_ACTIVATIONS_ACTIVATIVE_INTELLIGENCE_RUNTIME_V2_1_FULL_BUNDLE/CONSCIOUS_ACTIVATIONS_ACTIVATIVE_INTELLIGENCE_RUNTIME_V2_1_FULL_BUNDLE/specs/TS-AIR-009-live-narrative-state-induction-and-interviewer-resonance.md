---
type: technical_specification
spec_id: TS-AIR-009
product: Conscious Activations Activative Intelligence Runtime
feature_id: F09
title: Live Narrative State Induction and Interviewer Resonance
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-049
- AIR-FR-050
- AIR-FR-051
- AIR-FR-052
- AIR-FR-053
- AIR-FR-054
controlling_stories:
- AIR-ST-09.01
- AIR-ST-09.02
- AIR-ST-09.03
active_primitives:
- PRM-PSY-008
- EXP-FBK-001
- PRM-PRS-009
target_module: src/cmf_activative_intelligence/live_narrative_state_induction_and_interviewer_resonance.py
target_service: src/cmf_activative_intelligence/services/live_narrative_state_induction_and_interviewer_resonance_service.py
target_test: tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py
---

# TS-AIR-009 — Live Narrative State Induction and Interviewer Resonance

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F09-live-narrative-state-induction-and-interviewer-resonance.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-09.01, AIR-ST-09.02, AIR-ST-09.03 |
| SRC-INT-001 | `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | CCP V9 Interview-First Expression Engine |
| SRC-INT-002 | `sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | CCP V9.1 Expression Capture and Archetype Routing |
| SRC-MOE-001 | `sources/doctrine/MATRIX_OF_EDGING.md` | Matrix of Edging |
| SRC-AI2-LIVE-001 | `sources/ai_v2_predecessor/07_LIFECYCLE_STATE_MACHINES.md` | AI2 lifecycle state machines |
| PRM-PSY-008 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | exact Primitive YAML |
| EXP-FBK-001 | `sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | exact Primitive YAML |
| PRM-PRS-009 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-009.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Narrative State Induction is a closed-loop policy. It observes the current expression state, compares it with the target, proposes the smallest useful Activative Call, calibrates pressure, and knows when to deepen, reset, land, or stop. A weak implementation would continue the prepared interview script despite live defense, overload, or a landed answer, which leads to this concrete failure: pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity

### Solution

Implement the feature as a versioned domain service around `LiveActivativeState`, `InterviewerReactionState`, `ActivativeCall`, `PressureDoseDecision`, `CounteractivationProfile`, `StateTransitionReceipt`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-049` | `AIR-ST-09.01` | `LiveActivativeState` | F10 |
| `AIR-FR-050` | `AIR-ST-09.01` | `InterviewerReactionState` | F10 |
| `AIR-FR-051` | `AIR-ST-09.02` | `ActivativeCall` | F10 |
| `AIR-FR-052` | `AIR-ST-09.02` | `PressureDoseDecision` | F10 |
| `AIR-FR-053` | `AIR-ST-09.03` | `CounteractivationProfile` | F10 |
| `AIR-FR-054` | `AIR-ST-09.03` | `StateTransitionReceipt` | F10 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/live_narrative_state_induction_and_interviewer_resonance.py` with service orchestration in `src/cmf_activative_intelligence/services/live_narrative_state_induction_and_interviewer_resonance_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |
| `PRM-PRS-009` — The McKee Inciting Incident Engine | meaning_plane / `persuasion` | Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. | False Jeopardy — fabricating an inciting incident that feels contrived or hyperbolic, instantly destroying Ethos; Stranded Disequilibrium — introducing a powerful inciting incident but failing to provide a coherent or satisfying path to restoring balance |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-09.01` | `PRM-PSY-008` | Maintain an evidence-bearing live state must preserve Attack Problem Not Person's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-09.02` | `EXP-FBK-001` | Propose bounded next Activative Calls and pressure dose must preserve RIM Feedback Discipline's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-09.03` | `PRM-PRS-009` | Land, reset, or stop without forcing the intended premise must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `LiveActivativeState`, `InterviewerReactionState`, `ActivativeCall`, `PressureDoseDecision`, `CounteractivationProfile`, `StateTransitionReceipt` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/live_narrative_state_induction_and_interviewer_resonance_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-049, AIR-FR-050, AIR-FR-051, AIR-FR-052, AIR-FR-053, AIR-FR-054. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `LiveActivativeState` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-009/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/live_narrative_state_induction_and_interviewer_resonance.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/live_narrative_state_induction_and_interviewer_resonance_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/live_narrative_state_induction_and_interviewer_resonance.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/live_narrative_state_induction_and_interviewer_resonance_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/live_narrative_state_induction_and_interviewer_resonance_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/live_narrative_state_induction_and_interviewer_resonance.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-049: Maintain the Live Activative State

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Maintain the Live Activative State` using exact current inputs
- **Then** The Runtime shall update current expression state, target distance, anchor status, observed signals, pressure history, relationship condition, and available next actions after each meaningful event.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.01` — Maintain an evidence-bearing live state must preserve Attack Problem Not Person's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_049`

### AC-02 — AIR-FR-050: Represent real Interviewer Resonance

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Represent real Interviewer Resonance` using exact current inputs
- **Then** The live state shall preserve the interviewer’s genuine reaction, curiosity, recognition, uncertainty, or stake when it changes the next useful call.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.01` — Maintain an evidence-bearing live state must preserve Attack Problem Not Person's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_050`

### AC-03 — AIR-FR-051: Propose the smallest useful Activative Call

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Propose the smallest useful Activative Call` using exact current inputs
- **Then** The Runtime shall propose a bounded next call linked to the active Interview Asset Contract, observed state, expected transition, and stopping law.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.02` — Propose bounded next Activative Calls and pressure dose must preserve RIM Feedback Discipline's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_051`

### AC-04 — AIR-FR-052: Calibrate pressure dose and distance from overload

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Calibrate pressure dose and distance from overload` using exact current inputs
- **Then** Each call shall declare its pressure dose, expected gain, overload risk, and available relief or affinity-reset path.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.02` — Propose bounded next Activative Calls and pressure dose must preserve RIM Feedback Discipline's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_052`

### AC-05 — AIR-FR-053: Model counteractivation and defense roles

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Model counteractivation and defense roles` using exact current inputs
- **Then** The Runtime shall identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, or performative agreement and adjust the policy accordingly.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.03` — Land, reset, or stop without forcing the intended premise must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_053`

### AC-06 — AIR-FR-054: Choose continue, deepen, reset, land, or stop

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the service executes `Choose continue, deepen, reset, land, or stop` using exact current inputs
- **Then** The Runtime shall make the available transition explicit and shall not continue merely to exhaust a prepared question list.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-09.03` — Land, reset, or stop without forcing the intended premise must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **Test location:** `tests/integration/test_live_narrative_state_induction_and_interviewer_resonance.py::test_air_fr_054`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `LiveActivativeState` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://cmf_studio/src/ccp_studio/contracts/expression_session.py`
- `source://cmf_studio/src/ccp_studio/services/expression_session_service.py`

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
