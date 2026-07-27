---
type: technical_specification
spec_id: TS-AIR-001
product: Conscious Activations Activative Intelligence Runtime
feature_id: F01
title: Constitutional Authority, Activation Domains, and Epistemic State
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-001
- AIR-FR-002
- AIR-FR-003
- AIR-FR-004
- AIR-FR-005
- AIR-FR-006
controlling_stories:
- AIR-ST-01.01
- AIR-ST-01.02
- AIR-ST-01.03
active_primitives:
- PRM-PSY-008
- PRM-VSG-003
- EXP-FBK-001
target_module: src/cmf_activative_intelligence/constitutional_authority_activation_domains_and_epistemic_state.py
target_service: src/cmf_activative_intelligence/services/constitutional_authority_activation_domains_and_epistemic_state_service.py
target_test: tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py
---

# TS-AIR-001 — Constitutional Authority, Activation Domains, and Epistemic State

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F01-constitutional-authority-activation-domains-and-epistemic-state.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-01.01, AIR-ST-01.02, AIR-ST-01.03 |
| SRC-AI2-001 | `sources/ai_v2_predecessor/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2.md` | Activative Intelligence Lifecycle Constitution V2 |
| SRC-AHP-001 | `sources/doctrine/AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED.md` | AHP PRD V1.2 primitive/archetype-centered combined PRD |
| SRC-DOCTRINE-001 | `sources/spec_methods/CURRENT_WRITING_PROFILE_AHP_V1_2.md` | Current Conscious Activations writing and doctrine profile |
| PRM-PSY-008 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | exact Primitive YAML |
| PRM-VSG-003 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | exact Primitive YAML |
| EXP-FBK-001 | `sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/lifecycle.py` | exact predecessor review before implementation |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

The Runtime cannot activate, transform, or learn from a semantic object until it knows what kind of activation the object belongs to and what the available evidence permits the system to believe. A weak implementation would collapse one object-level status across fields so implementation becomes simpler, which leads to this concrete failure: a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim

### Solution

Implement the feature as a versioned domain service around `ActivationDomainDeclaration`, `EpistemicAssertion`, `SemanticObjectVersion`, `LifecycleTransitionReceipt`, `PlannedObservedDelta`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-001` | `AIR-ST-01.01` | `ActivationDomainDeclaration` | F02 |
| `AIR-FR-002` | `AIR-ST-01.01` | `EpistemicAssertion` | F02 |
| `AIR-FR-003` | `AIR-ST-01.02` | `SemanticObjectVersion` | F02 |
| `AIR-FR-004` | `AIR-ST-01.02` | `LifecycleTransitionReceipt` | F02 |
| `AIR-FR-005` | `AIR-ST-01.03` | `PlannedObservedDelta` | F02 |
| `AIR-FR-006` | `AIR-ST-01.03` | `PlannedObservedDelta` | F02 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/lifecycle.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/constitutional_authority_activation_domains_and_epistemic_state.py` with service orchestration in `src/cmf_activative_intelligence/services/constitutional_authority_activation_domains_and_epistemic_state_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-01.01` | `PRM-PSY-008` | Establish activation-domain and truth-state authority must preserve Attack Problem Not Person's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-01.02` | `PRM-VSG-003` | Version semantic decisions without rewriting history must preserve Intent Governs Style's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-01.03` | `EXP-FBK-001` | Prove lifecycle and epistemology claims must preserve RIM Feedback Discipline's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `ActivationDomainDeclaration`, `EpistemicAssertion`, `SemanticObjectVersion`, `LifecycleTransitionReceipt`, `PlannedObservedDelta` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/constitutional_authority_activation_domains_and_epistemic_state_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-001, AIR-FR-002, AIR-FR-003, AIR-FR-004, AIR-FR-005, AIR-FR-006. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `ActivationDomainDeclaration` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-001/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/constitutional_authority_activation_domains_and_epistemic_state.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/constitutional_authority_activation_domains_and_epistemic_state_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/constitutional_authority_activation_domains_and_epistemic_state.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/constitutional_authority_activation_domains_and_epistemic_state_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/constitutional_authority_activation_domains_and_epistemic_state_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/constitutional_authority_activation_domains_and_epistemic_state.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-001: Declare exactly one activation domain

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Declare exactly one activation domain` using exact current inputs
- **Then** Every activative program and semantic object shall declare exactly one primary activation domain—source, relationship, audience, campaign, or derivative—and may reference other domains only through typed handoffs.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.01` — Establish activation-domain and truth-state authority must preserve Attack Problem Not Person's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_001`

### AC-02 — AIR-FR-002: Preserve field-level epistemic state

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Preserve field-level epistemic state` using exact current inputs
- **Then** Every material field shall declare whether it is planned, observed, inferred, operator-confirmed, rejected, or superseded instead of inheriting one undifferentiated object status.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.01` — Establish activation-domain and truth-state authority must preserve Attack Problem Not Person's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_002`

### AC-03 — AIR-FR-003: Version and supersede semantic objects additively

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Version and supersede semantic objects additively` using exact current inputs
- **Then** Semantic changes shall create immutable successor versions with explicit supersession and invalidation edges; prior versions remain replayable.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.02` — Version semantic decisions without rewriting history must preserve Intent Governs Style's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_003`

### AC-04 — AIR-FR-004: Prevent planned intent from manufacturing observed truth

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Prevent planned intent from manufacturing observed truth` using exact current inputs
- **Then** The Runtime shall reject any transition that treats a Brief, hypothesis, intended role, or planned tag as evidence that a human expression or audience reaction occurred.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.02` — Version semantic decisions without rewriting history must preserve Intent Governs Style's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_004`

### AC-05 — AIR-FR-005: Compile cross-domain semantic lineage

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Compile cross-domain semantic lineage` using exact current inputs
- **Then** Every handoff between source, relationship, audience, campaign, and derivative activation shall preserve the originating objects, transformations, and authority boundaries.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.03` — Prove lifecycle and epistemology claims must preserve RIM Feedback Discipline's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_005`

### AC-06 — AIR-FR-006: Issue lifecycle and epistemology evaluation receipts

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the service executes `Issue lifecycle and epistemology evaluation receipts` using exact current inputs
- **Then** Independent evaluation shall verify domain fit, epistemic correctness, lifecycle legality, and claim ceiling before a semantic object becomes eligible downstream.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-01.03` — Prove lifecycle and epistemology claims must preserve RIM Feedback Discipline's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **Test location:** `tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py::test_air_fr_006`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `ActivationDomainDeclaration` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/lifecycle.py`
- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py`

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
