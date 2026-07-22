---
type: technical_specification
spec_id: TS-AIR-018
product: Conscious Activations Activative Intelligence Runtime
feature_id: F18
title: Human Resolution Episodes and Scoped Learning
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-103
- AIR-FR-104
- AIR-FR-105
- AIR-FR-106
- AIR-FR-107
- AIR-FR-108
controlling_stories:
- AIR-ST-18.01
- AIR-ST-18.02
- AIR-ST-18.03
active_primitives:
- EXP-FBK-001
- PRM-PSY-008
- EXP-TRS-003
target_module: src/cmf_activative_intelligence/human_resolution_episodes_and_scoped_learning.py
target_service: src/cmf_activative_intelligence/services/human_resolution_episodes_and_scoped_learning_service.py
target_test: tests/integration/test_human_resolution_episodes_and_scoped_learning.py
---

# TS-AIR-018 — Human Resolution Episodes and Scoped Learning

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F18-human-resolution-episodes-and-scoped-learning.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-18.01, AIR-ST-18.02, AIR-ST-18.03 |
| SRC-AI2-HRE-001 | `sources/ai_v2_predecessor/contracts/09_HUMAN_RESOLUTION_EPISODE.md` | AI2 Human Resolution Episode contract |
| SRC-STUDIO-AMENDMENT-001 | `sources/brownfield/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | Conscious Activations Studio Architecture Amendment V2.1 |
| SRC-AHP-F26-001 | `sources/doctrine/AHP_F26_HUMAN_RESOLUTION.md` | AHP F26 Human Resolution and Revision Compiler |
| EXP-FBK-001 | `sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | exact Primitive YAML |
| PRM-PSY-008 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | exact Primitive YAML |
| EXP-TRS-003 | `sources/cmf_primitive_registry_snapshot/experience_plane/trust_branding/EXP-TRS-003.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | exact predecessor review before implementation |
| Brownfield | `source://studio_amendment/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Human corrections are not chat residue. They are high-value evidence about wrong readings, taste boundaries, responsible layers, exact changes, and applicability. Capture is automatic; promotion is governed and scoped. A weak implementation would turn one operator correction into a global default or live weight update, which leads to this concrete failure: local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness

### Solution

Implement the feature as a versioned domain service around `HumanResolutionEpisode`, `ChangeRequestProgramRef`, `ProgrammingMaterialRecord`, `ApplicabilityEnvelope`, `SteeringRecipeCandidate`, `IdentityDNACandidateResolution`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-103` | `AIR-ST-18.01` | `HumanResolutionEpisode` | F19 |
| `AIR-FR-104` | `AIR-ST-18.01` | `ChangeRequestProgramRef` | F19 |
| `AIR-FR-105` | `AIR-ST-18.02` | `ProgrammingMaterialRecord` | F19 |
| `AIR-FR-106` | `AIR-ST-18.02` | `ApplicabilityEnvelope` | F19 |
| `AIR-FR-107` | `AIR-ST-18.03` | `SteeringRecipeCandidate` | F19 |
| `AIR-FR-108` | `AIR-ST-18.03` | `IdentityDNACandidateResolution` | F19 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://studio_amendment/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/human_resolution_episodes_and_scoped_learning.py` with service orchestration in `src/cmf_activative_intelligence/services/human_resolution_episodes_and_scoped_learning_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `EXP-TRS-003` — Reflective Social Proof (The Status Share) | experience_plane / `trust_branding` | Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. | Overt marketing logic — treating the share as a transaction rather than an identity signal; Generic assets — using stock imagery rather than the user's specific data/face in the share card |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-18.01` | `EXP-FBK-001` | Capture every meaningful HumanResolutionEpisode must preserve RIM Feedback Discipline's core move while denying the shortcut to turn one operator correction into a global default or live weight update. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-18.02` | `PRM-PSY-008` | Attribute the decision and index programming material must preserve Attack Problem Not Person's core move while denying the shortcut to turn one operator correction into a global default or live weight update. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-18.03` | `EXP-TRS-003` | Promote scoped recipes, model data, and Identity DNA observations through evidence must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to turn one operator correction into a global default or live weight update. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `HumanResolutionEpisode`, `ChangeRequestProgramRef`, `ProgrammingMaterialRecord`, `ApplicabilityEnvelope`, `SteeringRecipeCandidate`, `IdentityDNACandidateResolution` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/human_resolution_episodes_and_scoped_learning_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-103, AIR-FR-104, AIR-FR-105, AIR-FR-106, AIR-FR-107, AIR-FR-108. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `HumanResolutionEpisode` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-018/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/human_resolution_episodes_and_scoped_learning.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/human_resolution_episodes_and_scoped_learning_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/human_resolution_episodes_and_scoped_learning.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/human_resolution_episodes_and_scoped_learning_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/human_resolution_episodes_and_scoped_learning_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/human_resolution_episodes_and_scoped_learning.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_human_resolution_episodes_and_scoped_learning.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-103: Capture every meaningful human resolution

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Capture every meaningful human resolution` using exact current inputs
- **Then** Approvals, rejections, candidate selections, revisions, direct manipulations, tool overrides, taste explanations, and publication decisions shall emit immutable HumanResolutionEpisodes.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.01` — Capture every meaningful HumanResolutionEpisode must preserve RIM Feedback Discipline's core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_103`

### AC-02 — AIR-FR-104: Attribute each resolution to the responsible layer

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Attribute each resolution to the responsible layer` using exact current inputs
- **Then** The episode shall identify whether the issue originated in source understanding, Activative Intelligence, primitive binding, archetype routing, script, retrieval, model, composition, tool, runtime, evaluator, or operator policy.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.01` — Capture every meaningful HumanResolutionEpisode must preserve RIM Feedback Discipline's core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_104`

### AC-03 — AIR-FR-105: Index resolutions automatically as programming material

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Index resolutions automatically as programming material` using exact current inputs
- **Then** Accepted, rejected, repaired, and contradictory episodes shall become retrievable records and candidate SFT, preference, repair, hard-negative, or evaluator examples with exact lineage.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.02` — Attribute the decision and index programming material must preserve Attack Problem Not Person's core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_105`

### AC-04 — AIR-FR-106: Prohibit automatic global promotion and live weight mutation

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Prohibit automatic global promotion and live weight mutation` using exact current inputs
- **Then** Production use may append evidence and indexes but shall not update live weights, canonical Skills, Primitive registries, archetype authority, or doctrine without a release process.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.02` — Attribute the decision and index programming material must preserve Attack Problem Not Person's core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_106`

### AC-05 — AIR-FR-107: Promote Steering Recipes and learned claims within applicability envelopes

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Promote Steering Recipes and learned claims within applicability envelopes` using exact current inputs
- **Then** Promotion shall require repeated evidence, control comparisons, regression cases, scope, lifecycle, rollback, and human authority.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.03` — Promote scoped recipes, model data, and Identity DNA observations through evidence must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_107`

### AC-06 — AIR-FR-108: Resolve Identity DNA candidate observations explicitly

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the service executes `Resolve Identity DNA candidate observations explicitly` using exact current inputs
- **Then** Identity observations may be accepted, rejected, narrowed, or superseded through a separate profile-resolution event linked to source evidence and HumanResolutionEpisodes.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-18.03` — Promote scoped recipes, model data, and Identity DNA observations through evidence must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to turn one operator correction into a global default or live weight update.
- **Test location:** `tests/integration/test_human_resolution_episodes_and_scoped_learning.py::test_air_fr_108`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `HumanResolutionEpisode` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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
- `source://studio_amendment/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip`

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
