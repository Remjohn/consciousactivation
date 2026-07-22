---
type: technical_specification
spec_id: TS-AIR-016
product: Conscious Activations Activative Intelligence Runtime
feature_id: F16
title: Activation Transfer Fidelity and Source Fidelity
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-091
- AIR-FR-092
- AIR-FR-093
- AIR-FR-094
- AIR-FR-095
- AIR-FR-096
controlling_stories:
- AIR-ST-16.01
- AIR-ST-16.02
- AIR-ST-16.03
active_primitives:
- PRM-PSY-001
- PRM-VSG-003
- PRM-VSG-021
target_module: src/cmf_activative_intelligence/activation_transfer_fidelity_and_source_fidelity.py
target_service: src/cmf_activative_intelligence/services/activation_transfer_fidelity_and_source_fidelity_service.py
target_test: tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py
---

# TS-AIR-016 — Activation Transfer Fidelity and Source Fidelity

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F16-activation-transfer-fidelity-and-source-fidelity.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-16.01, AIR-ST-16.02, AIR-ST-16.03 |
| SRC-AI2-TRANSFER-001 | `sources/ai_v2_predecessor/contracts/07_ACTIVATION_TRANSFER_CONTRACT.md` | AI2 Activation Transfer Contract |
| SRC-AHP-F16-001 | `sources/doctrine/AHP_F16_EVALUATION_REPAIR.md` | AHP F16 evaluation and selective repair |
| SRC-SOURCE-FIRST-001 | `sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` | AHP V1.1 Source-First Interview PRD |
| PRM-PSY-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | exact Primitive YAML |
| PRM-VSG-003 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | exact Primitive YAML |
| PRM-VSG-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/transfer.py` | exact predecessor review before implementation |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Activation can decay at every handoff. An Activation Transfer Contract states what produced the original charge, what must survive, what may change, which role must remain available, and what would destroy the intended activation. A weak implementation would preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product, which leads to this concrete failure: the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension

### Solution

Implement the feature as a versioned domain service around `ActivationTransferContract`, `MustSurviveProperty`, `PermittedTransformation`, `SourceTransformationLineage`, `ActivationTransferEvaluationReceipt`, `TransferFailure`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-091` | `AIR-ST-16.01` | `ActivationTransferContract` | F17 |
| `AIR-FR-092` | `AIR-ST-16.01` | `MustSurviveProperty` | F17 |
| `AIR-FR-093` | `AIR-ST-16.02` | `PermittedTransformation` | F17 |
| `AIR-FR-094` | `AIR-ST-16.02` | `SourceTransformationLineage` | F17 |
| `AIR-FR-095` | `AIR-ST-16.03` | `ActivationTransferEvaluationReceipt` | F17 |
| `AIR-FR-096` | `AIR-ST-16.03` | `TransferFailure` | F17 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/transfer.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/activation_transfer_fidelity_and_source_fidelity.py` with service orchestration in `src/cmf_activative_intelligence/services/activation_transfer_fidelity_and_source_fidelity_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-16.01` | `PRM-PSY-001` | Identify the original source charge and must-survive properties must preserve Matching Principle's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-16.02` | `PRM-VSG-003` | Declare permitted transformations and exact lineage must preserve Intent Governs Style's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-16.03` | `PRM-VSG-021` | Measure transfer fidelity and repair the responsible handoff must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `ActivationTransferContract`, `MustSurviveProperty`, `PermittedTransformation`, `SourceTransformationLineage`, `ActivationTransferEvaluationReceipt`, `TransferFailure` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/activation_transfer_fidelity_and_source_fidelity_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-091, AIR-FR-092, AIR-FR-093, AIR-FR-094, AIR-FR-095, AIR-FR-096. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `ActivationTransferContract` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-016/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/activation_transfer_fidelity_and_source_fidelity.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/activation_transfer_fidelity_and_source_fidelity_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/activation_transfer_fidelity_and_source_fidelity.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/activation_transfer_fidelity_and_source_fidelity_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/activation_transfer_fidelity_and_source_fidelity_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/activation_transfer_fidelity_and_source_fidelity.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-091: Compile an Activation Transfer Contract

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Compile an Activation Transfer Contract` using exact current inputs
- **Then** The Runtime shall state the original activation source, participant role, tension, Edge Product, expression evidence, must-survive properties, permitted transformations, and destructive wrong readings.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the derivative preserves surface wording but drops the source pressure, role, tension, coalition, or Edge Product; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.01` — Identify the original source charge and must-survive properties must preserve Matching Principle's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_091`

### AC-02 — AIR-FR-092: Identify must-survive source and activation properties

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Identify must-survive source and activation properties` using exact current inputs
- **Then** The contract shall distinguish semantic premise, identity stance, emotional or cognitive turn, rhythm, reaction tail, visual cue, and participation role that materially carry the source charge.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.01` — Identify the original source charge and must-survive properties must preserve Matching Principle's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_092`

### AC-03 — AIR-FR-093: Declare permitted transformations and creative degrees of freedom

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Declare permitted transformations and creative degrees of freedom` using exact current inputs
- **Then** The contract shall explicitly allow or forbid condensation, reordering, rewriting, voice substitution, visual abstraction, animation, crop, timing, and platform adaptation by derivative type.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.02` — Declare permitted transformations and exact lineage must preserve Intent Governs Style's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_093`

### AC-04 — AIR-FR-094: Evaluate transfer fidelity at every material handoff

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Evaluate transfer fidelity at every material handoff` using exact current inputs
- **Then** Source-to-moment, moment-to-script, script-to-composition, composition-to-render, and render-to-platform handoffs shall emit transfer evidence and failure attribution.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the derivative preserves surface wording but drops the source pressure, role, tension, coalition, or Edge Product; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.02` — Declare permitted transformations and exact lineage must preserve Intent Governs Style's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_094`

### AC-05 — AIR-FR-095: Preserve complete source and transformation lineage

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Preserve complete source and transformation lineage` using exact current inputs
- **Then** Every derivative assertion, scene, caption, quote, visual proof, voiceover, and animation element shall be traceable to source spans or clearly labeled original connective material.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.03` — Measure transfer fidelity and repair the responsible handoff must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_095`

### AC-06 — AIR-FR-096: Reject wrong-role and centroid transfer failures

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the service executes `Reject wrong-role and centroid transfer failures` using exact current inputs
- **Then** A derivative shall fail when it preserves surface content but changes the intended psychological role, neutralizes the tension, erases the Edge Product, or converges toward generic centroid expression.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-16.03` — Measure transfer fidelity and repair the responsible handoff must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **Test location:** `tests/integration/test_activation_transfer_fidelity_and_source_fidelity.py::test_air_fr_096`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `ActivationTransferContract` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/transfer.py`
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
