---
type: technical_specification
spec_id: TS-AIR-011
product: Conscious Activations Activative Intelligence Runtime
feature_id: F11
title: Expression Moments and Observed Activative Intelligence
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-061
- AIR-FR-062
- AIR-FR-063
- AIR-FR-064
- AIR-FR-065
- AIR-FR-066
controlling_stories:
- AIR-ST-11.01
- AIR-ST-11.02
- AIR-ST-11.03
active_primitives:
- PRM-VOC-009
- PRM-VSG-021
- PRM-PRS-002
target_module: src/cmf_activative_intelligence/expression_moments_and_observed_activative_intelligence.py
target_service: src/cmf_activative_intelligence/services/expression_moments_and_observed_activative_intelligence_service.py
target_test: tests/integration/test_expression_moments_and_observed_activative_intelligence.py
---

# TS-AIR-011 — Expression Moments and Observed Activative Intelligence

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F11-expression-moments-and-observed-activative-intelligence.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-11.01, AIR-ST-11.02, AIR-ST-11.03 |
| SRC-AI2-EXPRESSION-001 | `sources/ai_v2_predecessor/contracts/04_EXPRESSION_MOMENT.md` | AI2 Expression Moment contract |
| SRC-SOURCE-FIRST-001 | `sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` | AHP V1.1 Source-First Interview PRD |
| SRC-INT-002 | `sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | CCP V9.1 Expression Capture and Archetype Routing |
| PRM-VOC-009 | `sources/cmf_primitive_registry_snapshot/meaning_plane/voice_audio_intimacy/PRM-VOC-009.yaml` | exact Primitive YAML |
| PRM-VSG-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | exact Primitive YAML |
| PRM-PRS-002 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-002.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

An Expression Moment is not a catchy sentence. It is a bounded unit of real expression whose premise, reaction, context, identity role, and route potential survive extraction. A weak implementation would extract the shortest quotable phrase and omit the premise or reaction tail, which leads to this concrete failure: a line becomes quotable only because its qualifying premise and emotional tail were removed

### Solution

Implement the feature as a versioned domain service around `ExpressionMomentCandidate`, `ExpressionMoment`, `ExpressionMomentDecision`, `ObservedActivativeIntelligencePack`, `ExpressionResolutionReceipt`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-061` | `AIR-ST-11.01` | `ExpressionMomentCandidate` | F12 |
| `AIR-FR-062` | `AIR-ST-11.01` | `ExpressionMoment` | F12 |
| `AIR-FR-063` | `AIR-ST-11.02` | `ExpressionMomentDecision` | F12 |
| `AIR-FR-064` | `AIR-ST-11.02` | `ObservedActivativeIntelligencePack` | F12 |
| `AIR-FR-065` | `AIR-ST-11.03` | `ExpressionResolutionReceipt` | F12 |
| `AIR-FR-066` | `AIR-ST-11.03` | `ExpressionResolutionReceipt` | F12 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/expression_moments_and_observed_activative_intelligence.py` with service orchestration in `src/cmf_activative_intelligence/services/expression_moments_and_observed_activative_intelligence_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-11.01` | `PRM-VOC-009` | Discover and bound complete Expression Moments must preserve Sensory Scene Anchoring's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-11.02` | `PRM-VSG-021` | Resolve moment lifecycle and routeability must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-11.03` | `PRM-PRS-002` | Compile the Observed Activative Intelligence Pack must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `ExpressionMomentCandidate`, `ExpressionMoment`, `ExpressionMomentDecision`, `ObservedActivativeIntelligencePack`, `ExpressionResolutionReceipt` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/expression_moments_and_observed_activative_intelligence_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-061, AIR-FR-062, AIR-FR-063, AIR-FR-064, AIR-FR-065, AIR-FR-066. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `ExpressionMomentCandidate` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-011/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/expression_moments_and_observed_activative_intelligence.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/expression_moments_and_observed_activative_intelligence_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/expression_moments_and_observed_activative_intelligence.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/expression_moments_and_observed_activative_intelligence_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/expression_moments_and_observed_activative_intelligence_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/expression_moments_and_observed_activative_intelligence.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_expression_moments_and_observed_activative_intelligence.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-061: Discover Expression Moment candidates from complete evidence

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Discover Expression Moment candidates from complete evidence` using exact current inputs
- **Then** The system shall use transcript, Reaction Receipts, audio events, keyframes, planned context, observed tags, and source continuity to propose moment candidates.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.01` — Discover and bound complete Expression Moments must preserve Sensory Scene Anchoring's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_061`

### AC-02 — AIR-FR-062: Set boundaries that preserve premise and reaction tail

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Set boundaries that preserve premise and reaction tail` using exact current inputs
- **Then** Candidate boundaries shall include the minimum source context needed to prevent quote collapse, preserve the cause of the expression, and retain the relevant reaction tail.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.01` — Discover and bound complete Expression Moments must preserve Sensory Scene Anchoring's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_062`

### AC-03 — AIR-FR-063: Score moment qualities and routeability

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Score moment qualities and routeability` using exact current inputs
- **Then** The resolver shall evaluate completeness, specificity, identity signal, pressure survival, emotional or cognitive turn, audiovisual usability, and eligible derivative routes.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.02` — Resolve moment lifecycle and routeability must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_063`

### AC-04 — AIR-FR-064: Maintain an explicit Expression Moment lifecycle

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Maintain an explicit Expression Moment lifecycle` using exact current inputs
- **Then** Candidates shall move through proposed, observed, borderline, approved, rejected, superseded, and revoked states with immutable decisions and evidence.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.02` — Resolve moment lifecycle and routeability must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_064`

### AC-05 — AIR-FR-065: Compile an Observed Activative Intelligence Pack

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Compile an Observed Activative Intelligence Pack` using exact current inputs
- **Then** The Runtime shall compile actual roles, directions, pressures, urges, edges, primitive and archetype evidence, reactions, limitations, and planned–observed deltas from approved source evidence.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.03` — Compile the Observed Activative Intelligence Pack must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_065`

### AC-06 — AIR-FR-066: Handoff approved source expression without losing authority

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the service executes `Handoff approved source expression without losing authority` using exact current inputs
- **Then** The Observed AIP shall reference exact source packages and moments and shall not grant the derivative producer authority to reinterpret the guest’s meaning.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and a line becomes quotable only because its qualifying premise and emotional tail were removed. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-11.03` — Compile the Observed Activative Intelligence Pack must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **Test location:** `tests/integration/test_expression_moments_and_observed_activative_intelligence.py::test_air_fr_066`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `ExpressionMomentCandidate` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://cmf_studio/src/ccp_studio/services/expression_session_service.py`
- `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md`

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
