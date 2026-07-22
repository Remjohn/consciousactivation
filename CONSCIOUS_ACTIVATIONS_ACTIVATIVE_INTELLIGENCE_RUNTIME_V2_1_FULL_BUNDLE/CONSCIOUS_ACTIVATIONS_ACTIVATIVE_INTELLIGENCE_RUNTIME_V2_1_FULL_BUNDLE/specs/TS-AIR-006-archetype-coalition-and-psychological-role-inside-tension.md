---
type: technical_specification
spec_id: TS-AIR-006
product: Conscious Activations Activative Intelligence Runtime
feature_id: F06
title: Archetype Coalition and Psychological Role Inside a Tension
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-031
- AIR-FR-032
- AIR-FR-033
- AIR-FR-034
- AIR-FR-035
- AIR-FR-036
controlling_stories:
- AIR-ST-06.01
- AIR-ST-06.02
- AIR-ST-06.03
active_primitives:
- PRM-PSY-001
- PRM-PRS-002
- PRM-HUM-021
target_module: src/cmf_activative_intelligence/archetype_coalition_and_psychological_role_inside_tension.py
target_service: src/cmf_activative_intelligence/services/archetype_coalition_and_psychological_role_inside_tension_service.py
target_test: tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py
---

# TS-AIR-006 — Archetype Coalition and Psychological Role Inside a Tension

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F06-archetype-coalition-and-psychological-role-inside-tension.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-06.01, AIR-ST-06.02, AIR-ST-06.03 |
| SRC-ARCH-001 | `sources/doctrine/CCP_ARCHETYPE_SYSTEM_MIGRATION_PROPOSITION.md` | CCP Archetype System Migration Proposition |
| SRC-ARCH-002 | `sources/cmf_archetype_prompt_snapshot` | CMF archetype prompt evidence snapshot |
| SRC-SDA-001 | `sources/cmf_sda_registry_snapshot` | CMF SDA registry snapshot |
| SRC-SFL-001 | `sources/cmf_sfl_registry_snapshot` | CMF SFL registry snapshot |
| SRC-AHP-F28-001 | `sources/doctrine/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | AHP F28 psychological role and archetype coalition |
| PRM-PSY-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | exact Primitive YAML |
| PRM-PRS-002 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-002.yaml` | exact Primitive YAML |
| PRM-HUM-021 | `sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/reference/conscious-rivers/src/ccp/harness/intelligence/archetype_prompts/` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Content activates when it gives the viewer a psychological role inside a tension. Archetypes are not content templates; they are interaction geometries that organize a Primitive coalition, role, tension, evidence, and sequence. A weak implementation would select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension, which leads to this concrete failure: the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative

### Solution

Implement the feature as a versioned domain service around `CoreContentArchetypeRef`, `DerivativeArchetypeRef`, `PsychologicalRoleTensionContract`, `ArchetypeCoalitionProgram`, `ArchetypeRouteReceipt`, `SDARef`, `SFLRef`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-031` | `AIR-ST-06.01` | `CoreContentArchetypeRef` | F07 |
| `AIR-FR-032` | `AIR-ST-06.01` | `DerivativeArchetypeRef` | F07 |
| `AIR-FR-033` | `AIR-ST-06.02` | `PsychologicalRoleTensionContract` | F07 |
| `AIR-FR-034` | `AIR-ST-06.02` | `ArchetypeCoalitionProgram` | F07 |
| `AIR-FR-035` | `AIR-ST-06.03` | `ArchetypeRouteReceipt` | F07 |
| `AIR-FR-036` | `AIR-ST-06.03` | `SDARef` | F07 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/reference/conscious-rivers/src/ccp/harness/intelligence/archetype_prompts/` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/archetype_coalition_and_psychological_role_inside_tension.py` with service orchestration in `src/cmf_activative_intelligence/services/archetype_coalition_and_psychological_role_inside_tension_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |
| `PRM-HUM-021` — Irony Inversion | meaning_plane / `humor_distortion` | Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. | Irony without conviction — breaking voice through tone markers (caps, emojis, 'just kidding') that expose the reversal prematurely; Irony without Subtext — reversing a statement that has no underlying value judgment, producing confusion rather than comedy |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-06.01` | `PRM-PSY-001` | Route the Edge Product into a supported archetype must preserve Matching Principle's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-06.02` | `PRM-PRS-002` | Define the psychological role inside the tension must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-06.03` | `PRM-HUM-021` | Lock archetype coalition geometry and route evidence must preserve Irony Inversion's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `CoreContentArchetypeRef`, `DerivativeArchetypeRef`, `PsychologicalRoleTensionContract`, `ArchetypeCoalitionProgram`, `ArchetypeRouteReceipt`, `SDARef`, `SFLRef` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/archetype_coalition_and_psychological_role_inside_tension_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-031, AIR-FR-032, AIR-FR-033, AIR-FR-034, AIR-FR-035, AIR-FR-036. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `CoreContentArchetypeRef` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-006/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/archetype_coalition_and_psychological_role_inside_tension.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/archetype_coalition_and_psychological_role_inside_tension_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/archetype_coalition_and_psychological_role_inside_tension.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/archetype_coalition_and_psychological_role_inside_tension_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/archetype_coalition_and_psychological_role_inside_tension_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/archetype_coalition_and_psychological_role_inside_tension.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-031: Select a source-supported Core Content Archetype

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Select a source-supported Core Content Archetype` using exact current inputs
- **Then** The Runtime shall select or propose a Core Content Archetype only when its interaction geometry fits the Edge Product, source evidence, audience state, and intended movement.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.01` — Route the Edge Product into a supported archetype must preserve Matching Principle's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_031`

### AC-02 — AIR-FR-032: Select derivative archetype and route

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Select derivative archetype and route` using exact current inputs
- **Then** Each derivative shall declare its content archetype, asset derivative route, category, and route scope instead of inheriting a generic content type.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.01` — Route the Edge Product into a supported archetype must preserve Matching Principle's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_032`

### AC-03 — AIR-FR-033: Declare the participant psychological role inside the tension

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Declare the participant psychological role inside the tension` using exact current inputs
- **Then** Every audience- or relationship-facing program shall name the role the person is invited to inhabit, the tension that makes the role meaningful, and the action or recognition the role enables.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.02` — Define the psychological role inside the tension must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_033`

### AC-04 — AIR-FR-034: Compile bounded multi-archetype coalitions

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Compile bounded multi-archetype coalitions` using exact current inputs
- **Then** When more than one archetype is used, the Runtime shall declare primary, supporting, transition, and excluded archetypes and prevent geometry conflict or centroid blending.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.02` — Define the psychological role inside the tension must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_034`

### AC-05 — AIR-FR-035: Bind SDA and SFL references

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Bind SDA and SFL references` using exact current inputs
- **Then** The archetype program shall resolve the applicable Story Design Archetype and Story Function Layer references required to preserve narrative function and derivative routing.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.03` — Lock archetype coalition geometry and route evidence must preserve Irony Inversion's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_035`

### AC-06 — AIR-FR-036: Issue an Archetype Route Receipt

- **Given** A validated Edge Product and current activation domain are available.
- **When** the service executes `Issue an Archetype Route Receipt` using exact current inputs
- **Then** The accepted route shall record Edge Product fit, role/tension contract, coalition structure, alternatives rejected, source lineage, and approval state.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension; a weak implementation would continue and the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-06.03` — Lock archetype coalition geometry and route evidence must preserve Irony Inversion's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **Test location:** `tests/integration/test_archetype_coalition_and_psychological_role_inside_tension.py::test_air_fr_036`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `CoreContentArchetypeRef` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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
- `source://cmf_studio/reference/conscious-rivers/src/ccp/harness/intelligence/archetype_prompts/`

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
