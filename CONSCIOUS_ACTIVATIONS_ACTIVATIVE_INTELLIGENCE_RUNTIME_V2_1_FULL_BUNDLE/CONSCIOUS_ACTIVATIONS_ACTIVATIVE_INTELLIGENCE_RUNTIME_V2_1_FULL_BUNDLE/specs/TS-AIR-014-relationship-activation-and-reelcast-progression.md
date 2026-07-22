---
type: technical_specification
spec_id: TS-AIR-014
product: Conscious Activations Activative Intelligence Runtime
feature_id: F14
title: Relationship Activation and ReelCast Progression
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-079
- AIR-FR-080
- AIR-FR-081
- AIR-FR-082
- AIR-FR-083
- AIR-FR-084
controlling_stories:
- AIR-ST-14.01
- AIR-ST-14.02
- AIR-ST-14.03
active_primitives:
- PRM-BUS-007
- EXP-PER-003
- EXP-PRG-002
target_module: src/cmf_activative_intelligence/relationship_activation_and_reelcast_progression.py
target_service: src/cmf_activative_intelligence/services/relationship_activation_and_reelcast_progression_service.py
target_test: tests/integration/test_relationship_activation_and_reelcast_progression.py
---

# TS-AIR-014 — Relationship Activation and ReelCast Progression

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F14-relationship-activation-and-reelcast-progression.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-14.01, AIR-ST-14.02, AIR-ST-14.03 |
| SRC-AI2-REL-001 | `sources/ai_v2_predecessor/schemas/relationship_activation_state.schema.json` | AI2 relationship activation models |
| SRC-INT-001 | `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | CCP V9 Interview-First Expression Engine |
| SRC-MOE-001 | `sources/doctrine/MATRIX_OF_EDGING.md` | Matrix of Edging |
| PRM-BUS-007 | `sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-007.yaml` | exact Primitive YAML |
| EXP-PER-003 | `sources/cmf_primitive_registry_snapshot/experience_plane/personalization_identity/EXP-PER-003.yaml` | exact Primitive YAML |
| EXP-PRG-002 | `sources/cmf_primitive_registry_snapshot/experience_plane/progression_replay/EXP-PRG-002.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Relationship activation asks what smallest useful move makes the next relationship state possible. It uses recognition, resonance, participation, evidence, and delivery rather than a universal funnel script. A weak implementation would treat a relationship move as a generic conversion funnel and ignore the current relationship stage, which leads to this concrete failure: a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness

### Solution

Implement the feature as a versioned domain service around `RelationshipActivationState`, `RelationshipHypothesisPortfolio`, `RelationshipActivativeCall`, `MicroCommitment`, `ReelCastProgressionProgram`, `RelationshipReceipt`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-079` | `AIR-ST-14.01` | `RelationshipActivationState` | F15 |
| `AIR-FR-080` | `AIR-ST-14.01` | `RelationshipHypothesisPortfolio` | F15 |
| `AIR-FR-081` | `AIR-ST-14.02` | `RelationshipActivativeCall` | F15 |
| `AIR-FR-082` | `AIR-ST-14.02` | `MicroCommitment` | F15 |
| `AIR-FR-083` | `AIR-ST-14.03` | `ReelCastProgressionProgram` | F15 |
| `AIR-FR-084` | `AIR-ST-14.03` | `RelationshipReceipt` | F15 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/relationship_activation_and_reelcast_progression.py` with service orchestration in `src/cmf_activative_intelligence/services/relationship_activation_and_reelcast_progression_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-BUS-007` — Social Media as Relationship | meaning_plane / `design_business` | Treat every piece of content not as an end in itself, but as a touchpoint designed to advance a relationship, build trust, or invite further connection. | Over-Familiarity — Treating the audience like therapists and over-sharing irrelevant personal drama; The Friend Zone — Building great relationships but being too afraid to ever make a business offer |
| `EXP-PER-003` — Cumulative Investment | experience_plane / `personalization_identity` | Immediately after delivering a variable reward (like a high Delivery Score), prompt the user to make a small, permanent investment in the platform (e.g., 'Save this vocal take to your Master Archive' or 'Pin this stance to your public profile'). | The Extractive Ask — Forcing investment before delivering the reward, causing instant churn.; Invisible Storage — Allowing the user to store value, but never showing them the accrued value (e.g., a hidden database instead of a beautiful 'Archive' UI), neutralizing the retention effect. |
| `EXP-PRG-002` — Discover -> On-board -> Immerse -> Master -> Replay | experience_plane / `progression_replay` | Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. | The Endless Tutorial — trapping users in the On-boarding phase for so long that they get bored and quit before experiencing the real product.; Feature Hiding as a Bug — making the UI so minimal that users don't even know what the product is supposed to do. |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-14.01` | `PRM-BUS-007` | Represent the current relationship state and hypotheses must preserve Social Media as Relationship's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-14.02` | `EXP-PER-003` | Select the smallest useful commitment must preserve Cumulative Investment's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-14.03` | `EXP-PRG-002` | Progress through ReelCast and asset delivery with scoped learning must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `RelationshipActivationState`, `RelationshipHypothesisPortfolio`, `RelationshipActivativeCall`, `MicroCommitment`, `ReelCastProgressionProgram`, `RelationshipReceipt` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/relationship_activation_and_reelcast_progression_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-079, AIR-FR-080, AIR-FR-081, AIR-FR-082, AIR-FR-083, AIR-FR-084. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `RelationshipActivationState` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-014/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/relationship_activation_and_reelcast_progression.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/relationship_activation_and_reelcast_progression_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/relationship_activation_and_reelcast_progression.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/relationship_activation_and_reelcast_progression_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/relationship_activation_and_reelcast_progression_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/relationship_activation_and_reelcast_progression.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_relationship_activation_and_reelcast_progression.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-079: Maintain a Relationship Activation State

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Maintain a Relationship Activation State` using exact current inputs
- **Then** The Runtime shall represent current relationship stage, prior interactions, expressed recognition, unresolved tension, commitments, delivered value, and evidence limits.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.01` — Represent the current relationship state and hypotheses must preserve Social Media as Relationship's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_079`

### AC-02 — AIR-FR-080: Generate relationship activation hypotheses

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Generate relationship activation hypotheses` using exact current inputs
- **Then** The Runtime shall compare recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset hypotheses appropriate to the current stage.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.01` — Represent the current relationship state and hypotheses must preserve Social Media as Relationship's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_080`

### AC-03 — AIR-FR-081: Select the smallest useful commitment

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Select the smallest useful commitment` using exact current inputs
- **Then** The selected move shall ask for the minimum action that creates meaningful evidence or makes the next state possible without pretending greater trust exists.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.02` — Select the smallest useful commitment must preserve Cumulative Investment's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_081`

### AC-04 — AIR-FR-082: Represent ReelCast progression explicitly

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Represent ReelCast progression explicitly` using exact current inputs
- **Then** Public comment, reply or DM, micro-commitment, Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer shall be separate states and receipts.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.02` — Select the smallest useful commitment must preserve Cumulative Investment's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_082`

### AC-05 — AIR-FR-083: Treat asset delivery as relationship evidence

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Treat asset delivery as relationship evidence` using exact current inputs
- **Then** A delivered source-backed asset shall update relationship state only from the actual delivery, response, use, and operator interpretation rather than from planned value.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.03` — Progress through ReelCast and asset delivery with scoped learning must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_083`

### AC-06 — AIR-FR-084: Capture scoped relationship learning

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the service executes `Capture scoped relationship learning` using exact current inputs
- **Then** Relationship learnings shall carry person, audience, stage, platform, interaction type, and applicability limits before they influence future calls.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence; a weak implementation would continue and a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-14.03` — Progress through ReelCast and asset delivery with scoped learning must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **Test location:** `tests/integration/test_relationship_activation_and_reelcast_progression.py::test_air_fr_084`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `RelationshipActivationState` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py`
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
