---
type: technical_specification
spec_id: TS-AIR-013
product: Conscious Activations Activative Intelligence Runtime
feature_id: F13
title: Campaign Activation, Freshness, and Audience Reaction
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-073
- AIR-FR-074
- AIR-FR-075
- AIR-FR-076
- AIR-FR-077
- AIR-FR-078
controlling_stories:
- AIR-ST-13.01
- AIR-ST-13.02
- AIR-ST-13.03
active_primitives:
- PRM-PRS-002
- PRM-HUM-021
- EXP-TRS-003
target_module: src/cmf_activative_intelligence/campaign_activation_freshness_and_audience_reaction.py
target_service: src/cmf_activative_intelligence/services/campaign_activation_freshness_and_audience_reaction_service.py
target_test: tests/integration/test_campaign_activation_freshness_and_audience_reaction.py
---

# TS-AIR-013 — Campaign Activation, Freshness, and Audience Reaction

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F13-campaign-activation-freshness-and-audience-reaction.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-13.01, AIR-ST-13.02, AIR-ST-13.03 |
| SRC-AI2-CAMPAIGN-001 | `sources/ai_v2_predecessor/contracts/08_CAMPAIGN_ACTIVATION_PROGRAM.md` | AI2 Campaign Activation Program contract |
| SRC-AHP-F23-001 | `sources/doctrine/AHP_F23_BATCH_ARCHETYPE_ROUTING.md` | AHP F23 source-backed batch and archetype routing |
| SRC-CCV-001 | `sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | CCV Combinatorial Controlled Variation |
| PRM-PRS-002 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-002.yaml` | exact Primitive YAML |
| PRM-HUM-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | exact Primitive YAML |
| EXP-TRS-003 | `sources/cmf_primitive_registry_snapshot/experience_plane/trust_branding/EXP-TRS-003.yaml` | exact Primitive YAML |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/freshness.py` | exact predecessor review before implementation |
| Brownfield | `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

An asset can be activative in isolation and stale inside a campaign. Campaign intelligence manages sequence, recurrence, relief, escalation, role diversity, and exposure while audience reaction remains a separate evidence domain. A weak implementation would rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls, which leads to this concrete failure: the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth

### Solution

Implement the feature as a versioned domain service around `CampaignActivationProgram`, `CampaignAssetPlan`, `ActivationFreshnessProfile`, `AudienceReactionReceipt`, `CampaignRevision`, `FatigueSignal`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-073` | `AIR-ST-13.01` | `CampaignActivationProgram` | F14 |
| `AIR-FR-074` | `AIR-ST-13.01` | `CampaignAssetPlan` | F14 |
| `AIR-FR-075` | `AIR-ST-13.02` | `ActivationFreshnessProfile` | F14 |
| `AIR-FR-076` | `AIR-ST-13.02` | `AudienceReactionReceipt` | F14 |
| `AIR-FR-077` | `AIR-ST-13.03` | `CampaignRevision` | F14 |
| `AIR-FR-078` | `AIR-ST-13.03` | `FatigueSignal` | F14 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/freshness.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/campaign_activation_freshness_and_audience_reaction.py` with service orchestration in `src/cmf_activative_intelligence/services/campaign_activation_freshness_and_audience_reaction_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |
| `PRM-HUM-021` — Irony Inversion | meaning_plane / `humor_distortion` | Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. | Irony without conviction — breaking voice through tone markers (caps, emojis, 'just kidding') that expose the reversal prematurely; Irony without Subtext — reversing a statement that has no underlying value judgment, producing confusion rather than comedy |
| `EXP-TRS-003` — Reflective Social Proof (The Status Share) | experience_plane / `trust_branding` | Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. | Overt marketing logic — treating the share as a transaction rather than an identity signal; Generic assets — using stock imagery rather than the user's specific data/face in the share card |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-13.01` | `PRM-PRS-002` | Compile a coordinated Campaign Activation Program must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-13.02` | `PRM-HUM-021` | Protect role, direction, archetype, and structure freshness must preserve Irony Inversion's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-13.03` | `EXP-TRS-003` | Capture audience response and revise the campaign additively must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `CampaignActivationProgram`, `CampaignAssetPlan`, `ActivationFreshnessProfile`, `AudienceReactionReceipt`, `CampaignRevision`, `FatigueSignal` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/campaign_activation_freshness_and_audience_reaction_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-073, AIR-FR-074, AIR-FR-075, AIR-FR-076, AIR-FR-077, AIR-FR-078. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `CampaignActivationProgram` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-013/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/campaign_activation_freshness_and_audience_reaction.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/campaign_activation_freshness_and_audience_reaction_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/campaign_activation_freshness_and_audience_reaction.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/campaign_activation_freshness_and_audience_reaction_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/campaign_activation_freshness_and_audience_reaction_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/campaign_activation_freshness_and_audience_reaction.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-073: Compile a Campaign Activation Program

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Compile a Campaign Activation Program` using exact current inputs
- **Then** The Runtime shall sequence source-backed derivative programs with audience segment, role, tension, direction, edge, archetype, primitive signature, format, and intended relationship movement.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.01` — Compile a coordinated Campaign Activation Program must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_073`

### AC-02 — AIR-FR-074: Enforce role, direction, and archetype diversity

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Enforce role, direction, and archetype diversity` using exact current inputs
- **Then** The campaign shall apply minimum diversity and repetition limits so repeated accusation, regret, inversion, or one archetype formula cannot dominate by local score alone.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.01` — Compile a coordinated Campaign Activation Program must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_074`

### AC-03 — AIR-FR-075: Maintain an Activation Freshness Profile

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Maintain an Activation Freshness Profile` using exact current inputs
- **Then** The system shall track prior structures, Primitive coalitions, roles, tensions, visual operators, archetypes, and audience exposure that affect present activation strength.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.02` — Protect role, direction, archetype, and structure freshness must preserve Irony Inversion's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_075`

### AC-04 — AIR-FR-076: Capture audience reaction as a separate evidence stream

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Capture audience reaction as a separate evidence stream` using exact current inputs
- **Then** Publishing observations shall produce Audience Reaction Receipts tied to exact asset versions, audience context, platform, exposure window, and measurement limits.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.02` — Protect role, direction, archetype, and structure freshness must preserve Irony Inversion's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_076`

### AC-05 — AIR-FR-077: Detect campaign counteractivation and fatigue

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Detect campaign counteractivation and fatigue` using exact current inputs
- **Then** The Runtime shall identify defensive repetition, habituation, formula visibility, role overload, edge overuse, and relief deficits across the campaign.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.03` — Capture audience response and revise the campaign additively must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_077`

### AC-06 — AIR-FR-078: Revise campaign programs additively

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the service executes `Revise campaign programs additively` using exact current inputs
- **Then** Campaign revisions shall supersede only affected asset plans or sequencing decisions while preserving published history, source lineage, and prior performance evidence.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit; a weak implementation would continue and the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-13.03` — Capture audience response and revise the campaign additively must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **Test location:** `tests/integration/test_campaign_activation_freshness_and_audience_reaction.py::test_air_fr_078`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `CampaignActivationProgram` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/freshness.py`
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
