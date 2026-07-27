---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F20
title: Programmed Models, Independent Evaluation, Product Integration, and Evidence
  Promotion
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Program Control
- Model Program engineers
- Cross-product owners
dependencies:
- F20
source_documents:
- SRC-AI2-MODEL-001
- SRC-AHP-MODEL-001
- SRC-HARNESS-RESEARCH-001
- SRC-RECENT-001
active_primitives:
- PRM-BUS-001
- EXP-PRG-002
- EXP-TRG-005
capability_areas:
- ProgrammedModelArtifact
- LearnedCapabilityClaim
- ModelProgramBinding
- HarnessProfile
- IndependentEvaluationReceipt
- ProductHandoffReceipt
- PromotionReceipt
functional_requirements: AIR-FR-115–AIR-FR-120
governing_decision: AIR-D025

---



# F20 — Programmed Models, Independent Evaluation, Product Integration, and Evidence Promotion



## 1. Architectural Claim and User Outcome

**User outcome:** The Runtime uses the smallest reliable specialized model or deterministic program for each bounded capability while preserving semantic sovereignty, independent evaluation, and cross-product contracts.

**Architectural claim:** A Programmed Model is a versioned learned capability claim inside a governed harness. It is not Activative authority. Better harnesses, retrieval, Skills, Primitive coalitions, and execution bindings should carry stable task difficulty before larger models or new training are used.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.** The terminal condition is: **An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible.**

The feature protects the product from this concrete shortcut: **use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation** If that shortcut is accepted, the downstream result is not merely lower quality; **a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient**

The feature is governed by `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `ProgrammedModelArtifact`, `LearnedCapabilityClaim`, `ModelProgramBinding`, `HarnessProfile`, `IndependentEvaluationReceipt`, `ProductHandoffReceipt`, `PromotionReceipt`. The owning products and authorities are Activative Intelligence Runtime, Program Control, Model Program engineers, Cross-product owners. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `ProgrammedModelArtifact` and `LearnedCapabilityClaim` |
| Evaluated | hard gates and independent judgment pass | `ProductHandoffReceipt` |
| Terminal | An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `ProgrammedModelArtifact` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `LearnedCapabilityClaim` | Program Control | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ModelProgramBinding` | Model Program engineers | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `HarnessProfile` | Cross-product owners | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `IndependentEvaluationReceipt` | Cross-product owners | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ProductHandoffReceipt` | Cross-product owners | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `PromotionReceipt` | Cross-product owners | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 reference implementation | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP Programmed Model requirements | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Builder harness and JIT architecture | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Harness adaptation and localized grounding research | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/dspy_signatures.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-BUS-001` — Perception and Guidance Stack | meaning_plane / `design_business` | Design visuals, text hierarchy, and action cues as one integrated system that controls where the eye goes and what the hand does next. | Dark Patterns — Using strong affordances to trick the user into an unintended action; Visual Noise — Adding fake depth or contrast that doesn't actually route attention |
| `EXP-PRG-002` — Discover -> On-board -> Immerse -> Master -> Replay | experience_plane / `progression_replay` | Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. | The Endless Tutorial — trapping users in the On-boarding phase for so long that they get bored and quit before experiencing the real product.; Feature Hiding as a Bug — making the UI so minimal that users don't even know what the product is supposed to do. |
| `EXP-TRG-005` — First Major Win-State | experience_plane / `trigger_timing` | Gate all social and expansion triggers behind a mathematically proven, hard-won success state, completely suppressing them during onboarding or failure. | Participation Trophies — lowering the bar for a 'win' so everyone gets it immediately.; Interrupting the actual Fiero moment with a clunky marketing funnel. |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/programmed_models_independent_evaluation_and_product_integration.py` and `src/cmf_activative_intelligence/services/programmed_models_independent_evaluation_and_product_integration_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **cross-product release and evidence** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-115 — Register exact Programmed Model artifacts and claims

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every learned implementation shall pin base model, tokenizer, adapter or checkpoint, runtime, training lineage, supported inputs, applicability envelope, limitations, and exact hashes.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **register exact programmed model artifacts and claims** under the active feature contract
            - **Then** Every learned implementation shall pin base model, tokenizer, adapter or checkpoint, runtime, training lineage, supported inputs, applicability envelope, limitations, and exact hashes, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

### AIR-FR-116 — Adapt the harness before increasing model size or training scope

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The system shall diagnose instruction, knowledge, retrieval, tool, context, and planning failures and improve context, tools, checks, or orchestration before assuming a larger model is required.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **adapt the harness before increasing model size or training scope** under the active feature contract
            - **Then** The system shall diagnose instruction, knowledge, retrieval, tool, context, and planning failures and improve context, tools, checks, or orchestration before assuming a larger model is required, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

### AIR-FR-117 — Use independent, layer-specific evaluation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Deterministic gates shall run first; semantic, Primitive, archetype, transfer, visual, and relationship judgments shall use independent calibrated evaluators and human labels where required.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **use independent, layer-specific evaluation** under the active feature contract
            - **Then** Deterministic gates shall run first; semantic, Primitive, archetype, transfer, visual, and relationship judgments shall use independent calibrated evaluators and human labels where required, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

### AIR-FR-118 — Preserve cross-product ownership through typed handoffs

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Program Control, Interview Expression, Builder, AHP, VAE, Delegation, and Studio shall exchange exact objects and receipts without duplicating semantic or execution ownership.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **preserve cross-product ownership through typed handoffs** under the active feature contract
            - **Then** Program Control, Interview Expression, Builder, AHP, VAE, Delegation, and Studio shall exchange exact objects and receipts without duplicating semantic or execution ownership, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

### AIR-FR-119 — Promote capability claims through evidence lifecycle

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Claims shall move through proposed, experimental, validated, shadow, limited-production, production, deprecated, retired, and revoked states with rollback and focused regression.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **promote capability claims through evidence lifecycle** under the active feature contract
            - **Then** Claims shall move through proposed, experimental, validated, shadow, limited-production, production, deprecated, retired, and revoked states with rollback and focused regression, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

### AIR-FR-120 — Generate a bounded release-readiness and implementation handoff

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-20.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The product shall emit exact Stories, Tech Specs, source dispositions, target paths, tests, evidence gaps, and authority gates; planning completeness shall not imply production readiness or certification.

            **Trigger and preconditions:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ProgrammedModelArtifact, LearnedCapabilityClaim, ModelProgramBinding, HarnessProfile, IndependentEvaluationReceipt, ProductHandoffReceipt, PromotionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Models do not own meaning.; The producing implementation does not approve itself.; The smallest reliable implementation wins within evidence.; Cross-product ownership remains explicit.; Format 02 remains deferred until its current Harness is independently validated.

            **Positive acceptance scenario**

            - **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
            - **When** the Runtime performs **generate a bounded release-readiness and implementation handoff** under the active feature contract
            - **Then** The product shall emit exact Stories, Tech Specs, source dispositions, target paths, tests, evidence gaps, and authority gates; planning completeness shall not imply production readiness or certification, and the resulting state is eligible for the feature terminal condition: An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The immediate consumer is **cross-product release and evidence**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models); `AIR-D025`.

## 10. Validation, Risks, Stop Conditions, and Completion Law

### Required gates

| Gate | Pass condition | Failure consequence |
|---|---|---|
| Source and identity | every source, Primitive, archetype evidence item, and upstream object resolves to exact version/hash | feature remains blocked; no inferred replacement |
| Product ownership | producer, evaluator, human authority, and downstream consumer are explicit | transition is illegal |
| Epistemology | planned, observed, inferred, confirmed, rejected, and superseded fields remain distinct | object cannot enter JIT context or composition |
| Primitive physics | exact YAML loaded; coalition compatibility, misuse, signature, and Edge Product evaluated where applicable | candidate is ineligible regardless of fluency or polish |
| Psychological role | role, tension, recognition, and counteractivation are explicit where audience activation is claimed | output is not approved as Activative |
| Final Script and composition | approved Guest Voice DNA Final Script and category composition program exist before editing/generation where applicable | production node does not start |
| Independent evaluation | producer does not approve itself; deterministic checks precede judgment | no promotion or terminal acceptance |
| Replay and invalidation | exact context, decisions, results, and descendant edges are reproducible | release evidence fails |

### Feature-specific risks

1. **Premature semantic closure:** use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
2. **Centroid drift:** the system may choose fluent, polished, broadly acceptable output that weakens the Edge Product. Mitigation: Primitive, Voice/Visual DNA, psychological-role, and anti-centroid gates are non-compensable.
3. **Product-boundary leakage:** one service may attempt to repair or approve an upstream object. Mitigation: typed handoffs, owning-product checks, and descendant-only invalidation.
4. **Over-learning:** a local correction may be generalized beyond evidence. Mitigation: automatic capture, explicit applicability envelopes, shadow evaluation, and release-controlled promotion.

### Stop conditions

- a required source or exact Primitive YAML is unavailable;
- the role, tension, Edge Product, or product owner cannot be established;
- the feature would require inventing a human reaction, source fact, Voice DNA, Visual DNA, or approval;
- the implementation duplicates a current canonical object or crosses product sovereignty;
- independent evaluation cannot distinguish the claimed success from a polished failure;
- a real-human, audience, external-product, or production claim is requested without corresponding evidence.

**Completion law:** this feature is planning-complete only when all six FRs have one primary Story and one controlling Tech Spec, all active Primitive IDs resolve to exact source YAMLs, brownfield dispositions are explicit, positive and adversarial scenarios pass, and the feature’s terminal object can be denied downstream when its evidence is invalid. Planning completion does not authorize implementation or production.
