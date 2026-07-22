---
type: technical_specification
spec_id: TS-AIR-015
product: Conscious Activations Activative Intelligence Runtime
feature_id: F15
title: Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory
  Animation Scene Packages
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
- AIR-FR-085
- AIR-FR-086
- AIR-FR-087
- AIR-FR-088
- AIR-FR-089
- AIR-FR-090
controlling_stories:
- AIR-ST-15.01
- AIR-ST-15.02
- AIR-ST-15.03
active_primitives:
- PRM-VOC-009
- PRM-VSG-003
- PRM-PRS-015
target_module: src/cmf_activative_intelligence/derivative_activation_final_scripts_and_animation_scene_packages.py
target_service: src/cmf_activative_intelligence/services/derivative_activation_final_scripts_and_animation_scene_packages_service.py
target_test: tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py
---

# TS-AIR-015 — Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory Animation Scene Packages

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F15-derivative-activation-final-scripts-and-animation-scene-packages.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-15.01, AIR-ST-15.02, AIR-ST-15.03 |
| SRC-AHP-F25-001 | `sources/doctrine/AHP_F25_STATIC_ANIMATION_DERIVATIVES.md` | AHP F25 source-grounded static and animation derivatives |
| SRC-AHP-F28-001 | `sources/doctrine/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | AHP F28 psychological role and archetype coalition |
| SRC-BRAND-001 | `sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` | CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3 |
| SRC-ARCH-001 | `sources/doctrine/CCP_ARCHETYPE_SYSTEM_MIGRATION_PROPOSITION.md` | CCP Archetype System Migration Proposition |
| PRM-VOC-009 | `sources/cmf_primitive_registry_snapshot/meaning_plane/voice_audio_intimacy/PRM-VOC-009.yaml` | exact Primitive YAML |
| PRM-VSG-003 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | exact Primitive YAML |
| PRM-PRS-015 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/narrative_story_doctor_service.py` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Quotes and Expression Moments are ingredients, not final scripts. JIT Skill writers and Composers transform approved source material through Voice DNA, Primitive coalitions, archetype geometry, and operator approval before composition. A weak implementation would begin composition from raw quotes or generic copy before archetype-coalition Final Script approval, which leads to this concrete failure: copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment

### Solution

Implement the feature as a versioned domain service around `DerivativeActivationProgram`, `FinalScriptPackage`, `ScriptSegmentLineage`, `ArchetypeCoalitionProgram`, `AnimationScenePackage`, `SemanticProductionPackage`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-085` | `AIR-ST-15.01` | `DerivativeActivationProgram` | F16 |
| `AIR-FR-086` | `AIR-ST-15.01` | `FinalScriptPackage` | F16 |
| `AIR-FR-087` | `AIR-ST-15.02` | `ScriptSegmentLineage` | F16 |
| `AIR-FR-088` | `AIR-ST-15.02` | `ArchetypeCoalitionProgram` | F16 |
| `AIR-FR-089` | `AIR-ST-15.03` | `AnimationScenePackage` | F16 |
| `AIR-FR-090` | `AIR-ST-15.03` | `SemanticProductionPackage` | F16 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/src/ccp_studio/services/narrative_story_doctor_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/derivative_activation_final_scripts_and_animation_scene_packages.py` with service orchestration in `src/cmf_activative_intelligence/services/derivative_activation_final_scripts_and_animation_scene_packages_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-15.01` | `PRM-VOC-009` | Compile a category-specific Derivative Activation Program must preserve Sensory Scene Anchoring's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-15.02` | `PRM-VSG-003` | Write and approve the archetype-coalition Final Script must preserve Intent Governs Style's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-15.03` | `PRM-PRS-015` | Compose mandatory reusable 2D animation scene packages and hand off production must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `DerivativeActivationProgram`, `FinalScriptPackage`, `ScriptSegmentLineage`, `ArchetypeCoalitionProgram`, `AnimationScenePackage`, `SemanticProductionPackage` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/derivative_activation_final_scripts_and_animation_scene_packages_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-085, AIR-FR-086, AIR-FR-087, AIR-FR-088, AIR-FR-089, AIR-FR-090. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `DerivativeActivationProgram` shared envelope

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
| `primitive_bindings` | `array<PrimitiveBinding>` | exact YAML versions and local functions |
| `coalition_signature` | `CoalitionSignature?` | structural identity of compatible bindings |
| `edge_product_ref` | `ImmutableRef?` | surviving pressure-role product |
| `psychological_role` | `string` | viewer or participant role inside the tension |
| `tension` | `string` | unresolved pressure that makes the role meaningful |
| `voice_dna_ref` | `ImmutableRef?` | exact Guest Voice DNA version |
| `final_script_approval_ref` | `ImmutableRef?` | operator approval and version |

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-015/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/derivative_activation_final_scripts_and_animation_scene_packages.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/derivative_activation_final_scripts_and_animation_scene_packages_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/derivative_activation_final_scripts_and_animation_scene_packages.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/derivative_activation_final_scripts_and_animation_scene_packages_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/derivative_activation_final_scripts_and_animation_scene_packages_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/derivative_activation_final_scripts_and_animation_scene_packages.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-085: Compile a Derivative Activation Program

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Compile a Derivative Activation Program` using exact current inputs
- **Then** Each short, Carousel, SuperVisual, animation scene, or relationship asset shall declare source ingredients, viewer role, tension, Edge Product, primitive coalition, archetype coalition, Voice/Visual DNA, and transfer requirements.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.01` — Compile a category-specific Derivative Activation Program must preserve Sensory Scene Anchoring's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_085`

### AC-02 — AIR-FR-086: Use JIT Skill writers and Composers for text transformation

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Use JIT Skill writers and Composers for text transformation` using exact current inputs
- **Then** Writers and Composers shall receive only approved source ingredients, relevant Voice DNA, coalition and archetype context, route rules, and transformation constraints.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.01` — Compile a category-specific Derivative Activation Program must preserve Sensory Scene Anchoring's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_086`

### AC-03 — AIR-FR-087: Preserve script-segment transformation lineage

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Preserve script-segment transformation lineage` using exact current inputs
- **Then** Every verbatim quote, condensation, adaptation, connective line, or rewrite shall identify its source spans, transformation class, authoring program, and approval state.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.02` — Write and approve the archetype-coalition Final Script must preserve Intent Governs Style's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_087`

### AC-04 — AIR-FR-088: Require operator approval of the Final Script

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Require operator approval of the Final Script` using exact current inputs
- **Then** No composition may begin until the complete archetype-coalition Final Script has been reviewed and approved or explicitly superseded by the operator.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.02` — Write and approve the archetype-coalition Final Script must preserve Intent Governs Style's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_088`

### AC-05 — AIR-FR-089: Compose a reusable 2D Animation Scene Package for every eligible script

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Compose a reusable 2D Animation Scene Package for every eligible script` using exact current inputs
- **Then** The system shall create composition-ready scene programs, visual references, character or symbolic roles, timing, BBOX intent, and asset demands that can serve as B-roll, slide elements, or complete animation scenes.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.03` — Compose mandatory reusable 2D animation scene packages and hand off production must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_089`

### AC-06 — AIR-FR-090: Emit an immutable Semantic Production Package

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the service executes `Emit an immutable Semantic Production Package` using exact current inputs
- **Then** The approved Final Script, coalition, archetype program, animation scene package, source lineage, transfer contract, and evaluation requirements shall be packaged for Builder/Harness/Pipeline consumption.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary; a weak implementation would continue and copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-15.03` — Compose mandatory reusable 2D animation scene packages and hand off production must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **Test location:** `tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py::test_air_fr_090`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `DerivativeActivationProgram` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py`
- `source://cmf_studio/src/ccp_studio/services/narrative_story_doctor_service.py`

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
