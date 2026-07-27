---
type: technical_specification
spec_id: TS-AIR-002
product: Conscious Activations Activative Intelligence Runtime
feature_id: F02
title: Identity, Context Premise, Resonance, and Matrix of Edging
version: 2.1.0-draft
status: DRAFT_AFTER_PRD_PENDING_RATIFICATION
date: '2026-07-22'
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
controlling_frs:
- AIR-FR-007
- AIR-FR-008
- AIR-FR-009
- AIR-FR-010
- AIR-FR-011
- AIR-FR-012
controlling_stories:
- AIR-ST-02.01
- AIR-ST-02.02
- AIR-ST-02.03
active_primitives:
- PRM-PSY-001
- PRM-PSY-008
- PRM-PRS-015
target_module: src/cmf_activative_intelligence/identity_context_resonance_and_matrix_of_edging.py
target_service: src/cmf_activative_intelligence/services/identity_context_resonance_and_matrix_of_edging_service.py
target_test: tests/integration/test_identity_context_resonance_and_matrix_of_edging.py
---

# TS-AIR-002 — Identity, Context Premise, Resonance, and Matrix of Edging

## 1. Files Read

| Class / ID | Exact file or source | Reason |
|---|---|---|
| Current authority | `CURRENT_AUTHORITY.md; doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | product and constitutional laws |
| PRD feature | `prd/features/F02-identity-context-resonance-and-matrix-of-edging.md` | controlling requirements and boundaries |
| Stories | `planning/EPICS_AND_VERTICAL_STORIES.md` | AIR-ST-02.01, AIR-ST-02.02, AIR-ST-02.03 |
| SRC-INT-001 | `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | CCP V9 Interview-First Expression Engine |
| SRC-INT-002 | `sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | CCP V9.1 Expression Capture and Archetype Routing |
| SRC-MOE-001 | `sources/doctrine/MATRIX_OF_EDGING.md` | Matrix of Edging |
| SRC-BRAND-001 | `sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` | CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3 |
| SRC-RSCS-001 | `sources/doctrine/RSCS_RECURSIVE_SIGNAL_COMPRESSION_SYSTEMS.md` | RSCS Recursive Signal Compression Systems |
| SRC-CCV-001 | `sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | CCV Combinatorial Controlled Variation |
| PRM-PSY-001 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | exact Primitive YAML |
| PRM-PSY-008 | `sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | exact Primitive YAML |
| PRM-PRS-015 | `sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | exact Primitive YAML |
| Brownfield | `source://cmf_studio/src/ccp_studio/contracts/brand_genesis.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/src/ccp_studio/services/brand_genesis_service.py` | exact predecessor review before implementation |
| Brownfield | `source://cmf_studio/Matrix of Edging.md` | exact predecessor review before implementation |

No implementation work begins from this spec until every listed source is available to the implementation agent and its exact bytes are recorded in the Development Capsule.

## 2. Overview

### Problem

Identity DNA and Context Premise do not become useful merely by coexisting. The Runtime must expose the broad signal, pressure field, resonance, contradiction, and role possibilities that can produce genuine expression. A weak implementation would use topic similarity as a substitute for identity, resonance, and Matrix survival, which leads to this concrete failure: the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers

### Solution

Implement the feature as a versioned domain service around `IdentityDNAReference`, `AudienceContextPremise`, `InterviewerResonanceContext`, `RelationshipContext`, `MatrixOfEdgingProgram`, `BroadSignal`, `EdgeProductCandidate`, `IdentityDNACandidateObservation`. Deterministic code owns identity, lifecycle legality, source and Primitive resolution, eligibility, hashing, dependency traversal, and receipts. Bounded model programs may propose or transform candidates only through typed inputs, explicit applicability, independent evaluation, and fallback.

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
| `AIR-FR-007` | `AIR-ST-02.01` | `IdentityDNAReference` | F03 |
| `AIR-FR-008` | `AIR-ST-02.01` | `AudienceContextPremise` | F03 |
| `AIR-FR-009` | `AIR-ST-02.02` | `InterviewerResonanceContext` | F03 |
| `AIR-FR-010` | `AIR-ST-02.02` | `RelationshipContext` | F03 |
| `AIR-FR-011` | `AIR-ST-02.03` | `MatrixOfEdgingProgram` | F03 |
| `AIR-FR-012` | `AIR-ST-02.03` | `BroadSignal` | F03 |

### 3.2 Existing backend and predecessor integration

| Exact predecessor path | Required disposition | Integration law |
|---|---|---|
| `source://cmf_studio/src/ccp_studio/contracts/brand_genesis.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/src/ccp_studio/services/brand_genesis_service.py` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |
| `source://cmf_studio/Matrix of Edging.md` | `REVIEW_THEN_REUSE_OR_ADAPT` | preserve tested contract or execution behavior; replace obsolete ownership, fake-result assumptions, and stale semantic constants |

The initial target path is `src/cmf_activative_intelligence/identity_context_resonance_and_matrix_of_edging.py` with service orchestration in `src/cmf_activative_intelligence/services/identity_context_resonance_and_matrix_of_edging_service.py`. Shared immutable models belong under `src/cmf_activative_intelligence/domain/`; persistence behind `src/cmf_activative_intelligence/repositories/`; cross-product adapters behind `src/cmf_activative_intelligence/adapters/`. These are proposed paths, not an implementation allowlist until a Development Capsule is issued.

### 3.3 Active Primitive physics

| Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |

The implementation loads these YAML files at build or registry-ingest time and stores their exact hashes. It does not hard-code a summary in model prompts as a substitute for the source Primitive. Tests must exercise at least one activation condition, one misuse or conflict case, and one suppression or inapplicability case per active Primitive where the YAML supplies them.

### 3.4 CBAR mandate enforcement

| Story | Primitive | Canonical mandate | Enforcement mechanism |
|---|---|---|---|
| `AIR-ST-02.01` | `PRM-PSY-001` | Assemble identity, audience, interviewer, and relationship context must preserve Matching Principle's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-02.02` | `PRM-PSY-008` | Compile Matrix broad signal and survived Edge Product must preserve Attack Problem Not Person's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. | schema gate + domain validator + independent evaluator + downstream denial fixture |
| `AIR-ST-02.03` | `PRM-PRS-015` | Propose Identity DNA candidate observations without mutation must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. | schema gate + domain validator + independent evaluator + downstream denial fixture |

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
- Implement or extend `IdentityDNAReference`, `AudienceContextPremise`, `InterviewerResonanceContext`, `RelationshipContext`, `MatrixOfEdgingProgram`, `BroadSignal`, `EdgeProductCandidate`, `IdentityDNACandidateObservation` under `src/cmf_activative_intelligence/domain/`.
- Generate JSON Schemas and canonical examples. Add positive, contradictory, stale, superseded, and missing-evidence fixtures.
### Stage 2 — Repository and lifecycle service
- Implement immutable create/read/supersede/replay operations in `src/cmf_activative_intelligence/services/identity_context_resonance_and_matrix_of_edging_service.py` and a repository port.
- Commit state transition, dependency edges, and receipt atomically. Add idempotency and duplicate-command behavior.
### Stage 3 — Feature compiler or resolver
- Implement the exact behavior required by AIR-FR-007, AIR-FR-008, AIR-FR-009, AIR-FR-010, AIR-FR-011, AIR-FR-012. Separate deterministic eligibility and contract checks from model or agent proposals.
- Add candidate search only where the Story and claim require it; preserve rejected candidates and stopping evidence.
### Stage 4 — Independent evaluation and repair
- Implement deterministic gates, feature-specific evaluator profile, failure attribution, descendant invalidation, and bounded repair.
### Stage 5 — Cross-product handoff and Studio projection
- Emit typed handoff receipts to the exact downstream owner. Add noncanonical read models and typed operator commands.
### Stage 6 — Migration and evidence
- Import eligible predecessor fixtures through a versioned adapter. Run clean-environment tests, replay, rollback, and claim-ceiling validation.
## 5. Primary Output Schema

### Proposed `IdentityDNAReference` shared envelope

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
| T1 Source lock and adapter audit | `development-capsules/TS-AIR-002/SOURCE_LOCK.yaml` | all source and Primitive hashes reproduce |
| T2 Domain model implementation | `src/cmf_activative_intelligence/identity_context_resonance_and_matrix_of_edging.py` | type checks, schema generation, canonical-hash tests |
| T3 Service and lifecycle | `src/cmf_activative_intelligence/services/identity_context_resonance_and_matrix_of_edging_service.py` | idempotent create/supersede/replay tests |
| T4 Contracts and examples | `contracts/schemas/identity_context_resonance_and_matrix_of_edging.schema.json` | valid and invalid fixtures |
| T5 Independent evaluator | `src/cmf_activative_intelligence/evaluation/identity_context_resonance_and_matrix_of_edging_evaluator.py` | calibration and disagreement fixtures |
| T6 Cross-product adapter | `src/cmf_activative_intelligence/adapters/identity_context_resonance_and_matrix_of_edging_handoff.py` | producer/consumer conformance receipt |
| T7 Studio read model and command | `src/cmf_activative_intelligence/projections/identity_context_resonance_and_matrix_of_edging.py` | projection does not become canonical state |
| T8 Integration and regression suite | `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py` | all Story, CBAR, replay, and invalidation cases pass |

## 8. Acceptance Criteria

### AC-01 — AIR-FR-007: Load immutable identity and brand context references

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Load immutable identity and brand context references` using exact current inputs
- **Then** The Runtime shall resolve exact Identity DNA, Brand Context Version, Brand Genesis Session, Voice DNA, and Visual DNA references required by the current activation objective.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.01` — Assemble identity, audience, interviewer, and relationship context must preserve Matching Principle's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_007`

### AC-02 — AIR-FR-008: Compile the audience Context Premise

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Compile the audience Context Premise` using exact current inputs
- **Then** The Runtime shall represent the audience situation, self-perception, pressure, desired movement, probable defenses, and relationship stage as a versioned Context Premise.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.01` — Assemble identity, audience, interviewer, and relationship context must preserve Matching Principle's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_008`

### AC-03 — AIR-FR-009: Represent Interviewer Resonance and relationship context

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Represent Interviewer Resonance and relationship context` using exact current inputs
- **Then** Source activation shall include the interviewer’s real resonance, lived stake, curiosity, and current relationship context when those conditions materially affect the guest response.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.02` — Compile Matrix broad signal and survived Edge Product must preserve Attack Problem Not Person's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_009`

### AC-04 — AIR-FR-010: Compile the Matrix broad signal

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Compile the Matrix broad signal` using exact current inputs
- **Then** The Matrix compiler shall intersect guest truth, audience reality, interviewer or relationship resonance, and current objective to produce a broad signal before edge candidates are ranked.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.02` — Compile Matrix broad signal and survived Edge Product must preserve Attack Problem Not Person's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_010`

### AC-05 — AIR-FR-011: Form an Edge Product candidate from survived pressure

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Form an Edge Product candidate from survived pressure` using exact current inputs
- **Then** The Runtime shall form an Edge Product only from edges that survive source evidence, identity fit, counteractivation analysis, and the relevant planned or observed state.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.03` — Propose Identity DNA candidate observations without mutation must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_011`

### AC-06 — AIR-FR-012: Propose Identity DNA candidate observations without mutation

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the service executes `Propose Identity DNA candidate observations without mutation` using exact current inputs
- **Then** The Runtime may emit evidence-linked Identity DNA candidate observations from repeated or strong expression, but canonical Identity DNA changes require a separate operator resolution.
- **And** the output carries exact source, product, lifecycle, epistemic, Primitive, evaluator, and descendant evidence required by the controlling contract.
- **Failure example:** the input is stale, contradictory, unresolved, or cannot support the claimed state transition; a weak implementation would continue and the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers. The correct implementation emits a typed blocker before downstream eligibility.
- **CBAR reference:** `AIR-ST-02.03` — Propose Identity DNA candidate observations without mutation must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **Test location:** `tests/integration/test_identity_context_resonance_and_matrix_of_edging.py::test_air_fr_012`

### AC-07 — Replay and supersession

- Given an accepted object and a valid successor upstream version, when supersession is applied, then only typed descendants become stale and the prior path remains historically replayable.
- Failure example: the service rewrites the existing `IdentityDNAReference` or invalidates unrelated products. This fails the immutable-history and descendant-only mandates.

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

- `source://cmf_studio/src/ccp_studio/contracts/brand_genesis.py`
- `source://cmf_studio/src/ccp_studio/services/brand_genesis_service.py`
- `source://cmf_studio/Matrix of Edging.md`

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
