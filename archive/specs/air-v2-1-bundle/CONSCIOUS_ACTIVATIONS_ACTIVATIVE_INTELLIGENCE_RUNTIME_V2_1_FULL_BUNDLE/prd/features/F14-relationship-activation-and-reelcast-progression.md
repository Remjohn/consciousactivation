---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F14
title: Relationship Activation and ReelCast Progression
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Relationship operator
- Interview Expression
dependencies:
- F14
source_documents:
- SRC-AI2-REL-001
- SRC-INT-001
- SRC-MOE-001
active_primitives:
- PRM-BUS-007
- EXP-PER-003
- EXP-PRG-002
capability_areas:
- RelationshipActivationState
- RelationshipHypothesisPortfolio
- RelationshipActivativeCall
- MicroCommitment
- ReelCastProgressionProgram
- RelationshipReceipt
functional_requirements: AIR-FR-079–AIR-FR-084
governing_decision: AIR-D019

---



# F14 — Relationship Activation and ReelCast Progression



## 1. Architectural Claim and User Outcome

**User outcome:** Public interaction, replies, micro-commitments, interviews, asset delivery, and offers form an evidence-bearing relationship progression rather than disconnected outreach steps.

**Architectural claim:** Relationship activation asks what smallest useful move makes the next relationship state possible. It uses recognition, resonance, participation, evidence, and delivery rather than a universal funnel script.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.** The terminal condition is: **The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust.**

The feature protects the product from this concrete shortcut: **treat a relationship move as a generic conversion funnel and ignore the current relationship stage** If that shortcut is accepted, the downstream result is not merely lower quality; **a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness**

The feature is governed by `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `RelationshipActivationState`, `RelationshipHypothesisPortfolio`, `RelationshipActivativeCall`, `MicroCommitment`, `ReelCastProgressionProgram`, `RelationshipReceipt`. The owning products and authorities are Activative Intelligence Runtime, Relationship operator, Interview Expression. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `RelationshipActivationState` and `RelationshipHypothesisPortfolio` |
| Evaluated | hard gates and independent judgment pass | `ReelCastProgressionProgram` |
| Terminal | The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `RelationshipActivationState` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `RelationshipHypothesisPortfolio` | Relationship operator | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `RelationshipActivativeCall` | Interview Expression | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `MicroCommitment` | Interview Expression | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ReelCastProgressionProgram` | Interview Expression | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `RelationshipReceipt` | Interview Expression | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 relationship state and call schemas | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| ReelCast and Interview Expression pathways | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Mirroring/affinity concepts in Matrix and Interview doctrine | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-BUS-007` — Social Media as Relationship | meaning_plane / `design_business` | Treat every piece of content not as an end in itself, but as a touchpoint designed to advance a relationship, build trust, or invite further connection. | Over-Familiarity — Treating the audience like therapists and over-sharing irrelevant personal drama; The Friend Zone — Building great relationships but being too afraid to ever make a business offer |
| `EXP-PER-003` — Cumulative Investment | experience_plane / `personalization_identity` | Immediately after delivering a variable reward (like a high Delivery Score), prompt the user to make a small, permanent investment in the platform (e.g., 'Save this vocal take to your Master Archive' or 'Pin this stance to your public profile'). | The Extractive Ask — Forcing investment before delivering the reward, causing instant churn.; Invisible Storage — Allowing the user to store value, but never showing them the accrued value (e.g., a hidden database instead of a beautiful 'Archive' UI), neutralizing the retention effect. |
| `EXP-PRG-002` — Discover -> On-board -> Immerse -> Master -> Replay | experience_plane / `progression_replay` | Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. | The Endless Tutorial — trapping users in the On-boarding phase for so long that they get bored and quit before experiencing the real product.; Feature Hiding as a Bug — making the UI so minimal that users don't even know what the product is supposed to do. |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/relationship_activation_and_reelcast_progression.py` and `src/cmf_activative_intelligence/services/relationship_activation_and_reelcast_progression_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F15** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-079 — Maintain a Relationship Activation State

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall represent current relationship stage, prior interactions, expressed recognition, unresolved tension, commitments, delivered value, and evidence limits.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **maintain a relationship activation state** under the active feature contract
            - **Then** The Runtime shall represent current relationship stage, prior interactions, expressed recognition, unresolved tension, commitments, delivered value, and evidence limits, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

### AIR-FR-080 — Generate relationship activation hypotheses

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall compare recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset hypotheses appropriate to the current stage.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **generate relationship activation hypotheses** under the active feature contract
            - **Then** The Runtime shall compare recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset hypotheses appropriate to the current stage, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

### AIR-FR-081 — Select the smallest useful commitment

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The selected move shall ask for the minimum action that creates meaningful evidence or makes the next state possible without pretending greater trust exists.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **select the smallest useful commitment** under the active feature contract
            - **Then** The selected move shall ask for the minimum action that creates meaningful evidence or makes the next state possible without pretending greater trust exists, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

### AIR-FR-082 — Represent ReelCast progression explicitly

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Public comment, reply or DM, micro-commitment, Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer shall be separate states and receipts.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **represent reelcast progression explicitly** under the active feature contract
            - **Then** Public comment, reply or DM, micro-commitment, Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer shall be separate states and receipts, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

### AIR-FR-083 — Treat asset delivery as relationship evidence

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** A delivered source-backed asset shall update relationship state only from the actual delivery, response, use, and operator interpretation rather than from planned value.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **treat asset delivery as relationship evidence** under the active feature contract
            - **Then** A delivered source-backed asset shall update relationship state only from the actual delivery, response, use, and operator interpretation rather than from planned value, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

### AIR-FR-084 — Capture scoped relationship learning

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-14.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Relationship learnings shall carry person, audience, stage, platform, interaction type, and applicability limits before they influence future calls.

            **Trigger and preconditions:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable RelationshipActivationState, RelationshipHypothesisPortfolio, RelationshipActivativeCall, MicroCommitment, ReelCastProgressionProgram, RelationshipReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Relationship activation is distinct from source and audience activation.; The next move is stage-appropriate.; Direct close and micro-commitment are different programs.; Asset delivery is evidence, not merely a marketing touch.

            **Positive acceptance scenario**

            - **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
            - **When** the Runtime performs **capture scoped relationship learning** under the active feature contract
            - **Then** Relationship learnings shall carry person, audience, stage, platform, interaction type, and applicability limits before they influence future calls, and the resulting state is eligible for the feature terminal condition: The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The immediate consumer is **F15**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging); `AIR-D019`.

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

1. **Premature semantic closure:** treat a relationship move as a generic conversion funnel and ignore the current relationship stage. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
