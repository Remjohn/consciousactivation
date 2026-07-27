---
type: technical_specification
spec_id: TS-AIR-012
product: Conscious Activations Activative Intelligence Runtime
feature_id: F12
title: Canonical Interview Source Package and Dual Admission
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-067
- AIR-FR-068
- AIR-FR-069
- AIR-FR-070
- AIR-FR-071
- AIR-FR-072
controlling_stories:
- AIR-ST-12.01
- AIR-ST-12.02
- AIR-ST-12.03
active_primitives:
- PRM-VOC-009
- PRM-VSG-003
- EXP-FBK-001
target_module: src/cmf_activative_intelligence/canonical_interview_source_package_and_dual_admission.py
target_service: src/cmf_activative_intelligence/services/canonical_interview_source_package_and_dual_admission_service.py
target_test: tests/integration/test_canonical_interview_source_package_and_dual_admission.py
---

# TS-AIR-012 — Canonical Interview Source Package and Dual Admission

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F12-canonical-interview-source-package-and-dual-admission.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-12.01, AIR-ST-12.02, AIR-ST-12.03 |
| SRC-SOURCE-FIRST-001 | `sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` | AHP V1.1 Source-First Interview PRD |
| SRC-AI2-SOURCE-001 | `sources/ai_v2_predecessor/contracts/05_CANONICAL_INTERVIEW_SOURCE_PACKAGE.md` | AI2 Canonical Interview Source Package contract |
| SRC-INT-001 | `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | CCP V9 Interview-First Expression Engine |
| PRM-VOC-009 | `sources/cmf_primitive_registry_snapshot/meaning_plane/voice_audio_intimacy/PRM-VOC-009.yaml` | exact Primitive YAML |
| PRM-VSG-003 | `sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | exact Primitive YAML |
| EXP-FBK-001 | `sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

The canonical source package is the trusted root of interview-derived production. It binds media, transcript, speakers, timestamps, tags, reactions, moments, keyframes, provenance, operator source authority, and route scope. A weak implementation would fabricate missing Brief-led history for an imported interview so both admission paths look identical, which leads to this concrete failure: derivatives cite invented planning history or drift across source-package versions

### Solution

Implement the feature as a versioned domain service around `CanonicalInterviewSourcePackage`, `SourceAdmissionRecord`, `SourceVersion`, `TagAssertion`, `SourcePackageReceipt`, `OperatorSourceAuthorityRef`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-067` | `AIR-ST-12.01` | `CanonicalInterviewSourcePackage` | F13 |
| `AIR-FR-068` | `AIR-ST-12.01` | `SourceAdmissionRecord` | F13 |
| `AIR-FR-069` | `AIR-ST-12.02` | `SourceVersion` | F13 |
| `AIR-FR-070` | `AIR-ST-12.02` | `TagAssertion` | F13 |
| `AIR-FR-071` | `AIR-ST-12.03` | `SourcePackageReceipt` | F13 |
| `AIR-FR-072` | `AIR-ST-12.03` | `OperatorSourceAuthorityRef` | F13 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/canonical_interview_source_package_and_dual_admission.py` with service orchestration in `src/cmf_activative_intelligence/services/canonical_interview_source_package_and_dual_admission_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-12.01` | `PRM-VOC-009` | Admit Brief-led and imported interview sources must preserve Sensory Scene Anchoring's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-12.02` | `PRM-VSG-003` | Assemble the exact media, transcript, tag, reaction, and keyframe spine must preserve Intent Governs Style's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-12.03` | `EXP-FBK-001` | Version and publish the canonical source package under operator authority must preserve RIM Feedback Discipline's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `CanonicalInterviewSourcePackage`, `SourceAdmissionRecord`, `SourceVersion`, `TagAssertion`, `SourcePackageReceipt`, `OperatorSourceAuthorityRef` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/canonical_interview_source_package_and_dual_admission_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-067, AIR-FR-068, AIR-FR-069, AIR-FR-070, AIR-FR-071, AIR-FR-072. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `CanonicalInterviewSourcePackage` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-012/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/canonical_interview_source_package_and_dual_admission.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/canonical_interview_source_package_and_dual_admission_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/canonical_interview_source_package_and_dual_admission.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/canonical_interview_source_package_and_dual_admission_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/canonical_interview_source_package_and_dual_admission_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/canonical_interview_source_package_and_dual_admission.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_canonical_interview_source_package_and_dual_admission.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-067: Support Brief-led admission

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Support Brief-led admission` using exact current inputs
- **Then** A completed Activative Interview shall produce a source package that references its Brief, Planned AIP, Interview Asset Contracts, calls, observations, Reaction Receipts, and observed evidence.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.01` — Admit Brief-led and imported interview sources must preserve Sensory Scene Anchoring's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_067`

### AC-02 — AIR-FR-068: Support imported-source admission

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Support imported-source admission` using exact current inputs
- **Then** An imported interview shall become a first-class source package while explicitly declaring which planned activation, anchor, Matrix, or session objects are absent.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.01` — Admit Brief-led and imported interview sources must preserve Sensory Scene Anchoring's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_068`

### AC-03 — AIR-FR-069: Bind exact media, transcript, speakers, timing, and keyframes

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Bind exact media, transcript, speakers, timing, and keyframes` using exact current inputs
- **Then** The source package shall hash and version original video/audio, transcript words and phrases, speaker map, time alignment, audio events, shot map, keyframes, and visual references.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.02` — Assemble the exact media, transcript, tag, reaction, and keyframe spine must preserve Intent Governs Style's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_069`

### AC-04 — AIR-FR-070: Preserve tag provenance and epistemic state

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Preserve tag provenance and epistemic state` using exact current inputs
- **Then** Every planned, observed, inferred, operator-confirmed, rejected, and superseded tag shall retain its source, timestamp or span, author, and lifecycle state.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.02` — Assemble the exact media, transcript, tag, reaction, and keyframe spine must preserve Intent Governs Style's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_070`

### AC-05 — AIR-FR-071: Version source packages additively

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Version source packages additively` using exact current inputs
- **Then** Corrections to transcripts, speaker maps, tags, moments, or references shall create successor package versions and invalidate only dependent derivative programs.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.03` — Version and publish the canonical source package under operator authority must preserve RIM Feedback Discipline's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_071`

### AC-06 — AIR-FR-072: Publish under operator source authority

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the service executes `Publish under operator source authority` using exact current inputs
- **Then** The package shall record the operator-provided source authority and intended route scope as provenance and execution context without introducing a separate creative-policy authority.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and derivatives cite invented planning history or drift across source-package versions. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-12.03` — Version and publish the canonical source package under operator authority must preserve RIM Feedback Discipline's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **Test location:** `tests/integration/test_canonical_interview_source_package_and_dual_admission.py::test_air_fr_072`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `CanonicalInterviewSourcePackage` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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
- `source://cmf_studio/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md`

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
