---
type: technical_specification
spec_id: TS-AIR-017
product: Conscious Activations Activative Intelligence Runtime
feature_id: F17
title: Visual Activation, Composition-Before-Editing, and Production Handoff
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-097
- AIR-FR-098
- AIR-FR-099
- AIR-FR-100
- AIR-FR-101
- AIR-FR-102
controlling_stories:
- AIR-ST-17.01
- AIR-ST-17.02
- AIR-ST-17.03
active_primitives:
- PRM-VSG-001
- PRM-VSG-024
- PRM-VSG-021
- PRM-BUS-006
target_module: src/cmf_activative_intelligence/visual_activation_and_composition_before_editing.py
target_service: src/cmf_activative_intelligence/services/visual_activation_and_composition_before_editing_service.py
target_test: tests/integration/test_visual_activation_and_composition_before_editing.py
---

# TS-AIR-017 — Visual Activation, Composition-Before-Editing, and Production Handoff

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F17-visual-activation-and-composition-before-editing.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-17.01, AIR-ST-17.02, AIR-ST-17.03 |
| SRC-AI2-VISUAL-001 | `sources/ai_v2_predecessor/schemas/visual_narrative_program.schema.json` | AI2 visual narrative schema |
| SRC-AHP-F09-001 | `sources/doctrine/AHP_F09_COMPOSITION_IR.md` | AHP F09 Composition IR and static runtime |
| SRC-AHP-F15-001 | `sources/doctrine/AHP_F15_VAE_DELEGATION_GNM.md` | AHP F15 VAE Delegation and GNM boundary |
| SRC-VISUAL-DOCTRINE-001 | `sources/doctrine/CCP_CREATIVE_PIPELINE_ARCHITECTURE_V2.md` | CCP Creative Pipeline Architecture V2 |
| PRM-VSG-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | exact Primitive YAML |
| PRM-VSG-024 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-024.yaml` | exact Primitive YAML |
| PRM-VSG-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | exact Primitive YAML |
| PRM-BUS-006 | `sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-006.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/registries/sda/` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/registries/sfl/` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Visual generation is downstream of Visual Research, Real-Life Reference, Visual DNA, and Composition. Editing should realize an approved composition program, not discover the meaning by moving assets until something looks polished. A weak implementation would start editing or generation before composition intent, negative space, and real-life reference research are resolved, which leads to this concrete failure: editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference

### Solution

Implement the feature as a versioned domain service around `VisualSemanticCandidate`, `VisualNarrativeProgram`, `VisualResearchPack`, `RealLifeReferencePack`, `FeatureContract`, `VisualActivationHandoff`, `CompositionIntent`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-097` | `AIR-ST-17.01` | `VisualSemanticCandidate` | F18 |
| `AIR-FR-098` | `AIR-ST-17.01` | `VisualNarrativeProgram` | F18 |
| `AIR-FR-099` | `AIR-ST-17.02` | `VisualResearchPack` | F18 |
| `AIR-FR-100` | `AIR-ST-17.02` | `RealLifeReferencePack` | F18 |
| `AIR-FR-101` | `AIR-ST-17.03` | `FeatureContract` | F18 |
| `AIR-FR-102` | `AIR-ST-17.03` | `VisualActivationHandoff` | F18 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/registries/sda/` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/registries/sfl/` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/visual_activation_and_composition_before_editing.py` with service orchestration in `src/cmf_activative_intelligence/services/visual_activation_and_composition_before_editing_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VSG-001` — Composition as Eye-Path Engineering | meaning_plane / `visual_sonic_guidance` | Structure visual elements within the frame to force a specific sequence of eye movement. | Over-engineering the path to the point where the composition feels forced or unnatural; Applying visual rules to sonic or text-only artifacts |
| `PRM-VSG-024` — Space as Psychological Relationship | meaning_plane / `visual_sonic_guidance` | Before finalizing a visual, define the psychological relationship between the subject and the room/landscape. If the character feels trapped, compose the shot to make the walls literally close in on them. If the character feels lost, place them in a vast, empty space that visually overwhelms their scale. Force the environment to express the internal state of the subject. | The Empty Void — Placing the subject in so much negative space that the image feels unfinished or accidental, rather than intentionally 'vast'; Claustrophobia by Accident — Filming with a tight crop purely out of convenience, unintentionally making the audience feel anxious or trapped |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |
| `PRM-BUS-006` — Hierarchy as Attention Routing | meaning_plane / `design_business` | Assign distinct, uncompetitive visual weights to different semantic roles in the content, ensuring the viewer's eye is routed exactly where it needs to go, in the exact order it needs to go there. | Too Many Levels — Creating 6 different levels of hierarchy that confuse rather than clarify; Arbitrary Emphasis — Bolding random words in a sentence just for 'pop', breaking the semantic meaning |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-17.01` | `PRM-VSG-001` | Compile visual activation candidates from research and reference must preserve Composition as Eye-Path Engineering's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-17.02` | `PRM-VSG-024` | Define composition intent and feature contracts before editing must preserve Space as Psychological Relationship's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-17.03` | `PRM-VSG-021` | Handoff to Pipeline/VAE and reparse the rendered result must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `VisualSemanticCandidate`, `VisualNarrativeProgram`, `VisualResearchPack`, `RealLifeReferencePack`, `FeatureContract`, `VisualActivationHandoff`, `CompositionIntent` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/visual_activation_and_composition_before_editing_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-097, AIR-FR-098, AIR-FR-099, AIR-FR-100, AIR-FR-101, AIR-FR-102. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `VisualSemanticCandidate` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-017/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/visual_activation_and_composition_before_editing.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/visual_activation_and_composition_before_editing_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/visual_activation_and_composition_before_editing.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/visual_activation_and_composition_before_editing_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/visual_activation_and_composition_before_editing_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/visual_activation_and_composition_before_editing.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_visual_activation_and_composition_before_editing.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-097: Generate visual semantic candidates from the approved semantic package

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Generate visual semantic candidates from the approved semantic package` using exact current inputs
- **Then** The Runtime shall propose visual metaphors, evidence structures, real-life scenes, graphic relations, and composition strategies tied to the viewer role, tension, coalition, archetype, Voice/Visual DNA, and transfer contract.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.01` — Compile visual activation candidates from research and reference must preserve Composition as Eye-Path Engineering's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_097`

### AC-02 — AIR-FR-098: Require Visual Research and Real-Life Reference before generation

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Require Visual Research and Real-Life Reference before generation` using exact current inputs
- **Then** Visual candidates shall cite specimens, real environments, human references, object behavior, or documented visual systems before generated assets are requested where such reference is applicable.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.01` — Compile visual activation candidates from research and reference must preserve Composition as Eye-Path Engineering's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_098`

### AC-03 — AIR-FR-099: Compile composition intent before editing or rendering

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Compile composition intent before editing or rendering` using exact current inputs
- **Then** The Runtime shall define hierarchy, reading path, subject relationships, BBOX function, negative space, sequence role, and intended viewer state before timeline or canvas operations are authorized.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.02` — Define composition intent and feature contracts before editing must preserve Space as Psychological Relationship's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_099`

### AC-04 — AIR-FR-100: Compile feature-level visual contracts

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Compile feature-level visual contracts` using exact current inputs
- **Then** Required gaze, hands, facial expression, props, evidence, text, scale, depth, motion, sonic cues, and wrong-reading locks shall be represented as independently testable Feature Contracts.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.02` — Define composition intent and feature contracts before editing must preserve Space as Psychological Relationship's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_100`

### AC-05 — AIR-FR-101: Emit a bounded Visual Activation Handoff

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Emit a bounded Visual Activation Handoff` using exact current inputs
- **Then** The handoff shall include semantic authority, visual narrative, composition intent, asset requirements, allowed variation, source references, and evaluation profile for AHP or VAE consumption.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.03` — Handoff to Pipeline/VAE and reparse the rendered result must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_101`

### AC-06 — AIR-FR-102: Reparse rendered visual syntax and activation function

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the service executes `Reparse rendered visual syntax and activation function` using exact current inputs
- **Then** The completed composition shall be reparsed into observed hierarchy, BBOX relationships, gaze, reading order, timing, and role/tension evidence for comparison with intent.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry; a weak implementation would continue and editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-17.03` — Handoff to Pipeline/VAE and reparse the rendered result must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **Test location:** `tests/integration/test_visual_activation_and_composition_before_editing.py::test_air_fr_102`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `VisualSemanticCandidate` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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
- `source://cmf_studio/registries/sda/`
- `source://cmf_studio/registries/sfl/`

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
