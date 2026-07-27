---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F09
title: Live Narrative State Induction and Interviewer Resonance
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Interview Expression
- Human interviewer
dependencies:
- F09
source_documents:
- SRC-INT-001
- SRC-INT-002
- SRC-MOE-001
- SRC-AI2-LIVE-001
active_primitives:
- PRM-PSY-008
- EXP-FBK-001
- PRM-PRS-009
capability_areas:
- LiveActivativeState
- InterviewerReactionState
- ActivativeCall
- PressureDoseDecision
- CounteractivationProfile
- StateTransitionReceipt
functional_requirements: AIR-FR-049–AIR-FR-054
governing_decision: AIR-D014

---



# F09 — Live Narrative State Induction and Interviewer Resonance



## 1. Architectural Claim and User Outcome

**User outcome:** The live interview adapts to the guest’s actual state instead of following a static script while preserving human interviewer authority.

**Architectural claim:** Narrative State Induction is a closed-loop policy. It observes the current expression state, compares it with the target, proposes the smallest useful Activative Call, calibrates pressure, and knows when to deepen, reset, land, or stop.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An armed Interview Asset Contract enters a live or simulated source-activation session.** The terminal condition is: **Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction.**

The feature protects the product from this concrete shortcut: **continue the prepared interview script despite live defense, overload, or a landed answer** If that shortcut is accepted, the downstream result is not merely lower quality; **pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity**

The feature is governed by `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `LiveActivativeState`, `InterviewerReactionState`, `ActivativeCall`, `PressureDoseDecision`, `CounteractivationProfile`, `StateTransitionReceipt`. The owning products and authorities are Activative Intelligence Runtime, Interview Expression, Human interviewer. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An armed Interview Asset Contract enters a live or simulated source-activation session. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `LiveActivativeState` and `InterviewerReactionState` |
| Evaluated | hard gates and independent judgment pass | `CounteractivationProfile` |
| Terminal | Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `LiveActivativeState` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `InterviewerReactionState` | Interview Expression | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ActivativeCall` | Human interviewer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `PressureDoseDecision` | Human interviewer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `CounteractivationProfile` | Human interviewer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `StateTransitionReceipt` | Human interviewer | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 live state and Activative Call schemas | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| V9 Narrative State Induction | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Interviewer Resonance doctrine | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |
| `PRM-PRS-009` — The McKee Inciting Incident Engine | meaning_plane / `persuasion` | Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. | False Jeopardy — fabricating an inciting incident that feels contrived or hyperbolic, instantly destroying Ethos; Stranded Disequilibrium — introducing a powerful inciting incident but failing to provide a coherent or satisfying path to restoring balance |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/live_narrative_state_induction_and_interviewer_resonance.py` and `src/cmf_activative_intelligence/services/live_narrative_state_induction_and_interviewer_resonance_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F10** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-049 — Maintain the Live Activative State

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall update current expression state, target distance, anchor status, observed signals, pressure history, relationship condition, and available next actions after each meaningful event.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **maintain the live activative state** under the active feature contract
            - **Then** The Runtime shall update current expression state, target distance, anchor status, observed signals, pressure history, relationship condition, and available next actions after each meaningful event, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
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

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

### AIR-FR-050 — Represent real Interviewer Resonance

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The live state shall preserve the interviewer’s genuine reaction, curiosity, recognition, uncertainty, or stake when it changes the next useful call.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **represent real interviewer resonance** under the active feature contract
            - **Then** The live state shall preserve the interviewer’s genuine reaction, curiosity, recognition, uncertainty, or stake when it changes the next useful call, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
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
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

### AIR-FR-051 — Propose the smallest useful Activative Call

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall propose a bounded next call linked to the active Interview Asset Contract, observed state, expected transition, and stopping law.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **propose the smallest useful activative call** under the active feature contract
            - **Then** The Runtime shall propose a bounded next call linked to the active Interview Asset Contract, observed state, expected transition, and stopping law, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
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

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

### AIR-FR-052 — Calibrate pressure dose and distance from overload

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Each call shall declare its pressure dose, expected gain, overload risk, and available relief or affinity-reset path.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **calibrate pressure dose and distance from overload** under the active feature contract
            - **Then** Each call shall declare its pressure dose, expected gain, overload risk, and available relief or affinity-reset path, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
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

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

### AIR-FR-053 — Model counteractivation and defense roles

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, or performative agreement and adjust the policy accordingly.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **model counteractivation and defense roles** under the active feature contract
            - **Then** The Runtime shall identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, or performative agreement and adjust the policy accordingly, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

### AIR-FR-054 — Choose continue, deepen, reset, land, or stop

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-09.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall make the available transition explicit and shall not continue merely to exhaust a prepared question list.

            **Trigger and preconditions:** An armed Interview Asset Contract enters a live or simulated source-activation session. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable LiveActivativeState, InterviewerReactionState, ActivativeCall, PressureDoseDecision, CounteractivationProfile, StateTransitionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** The interviewer remains a real participant, not a neutral API.; The Runtime proposes; human delivery and judgment remain attributable.; Pressure is calibrated, not maximized.; No next call may ignore a detected defense or overload state.

            **Positive acceptance scenario**

            - **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
            - **When** the Runtime performs **choose continue, deepen, reset, land, or stop** under the active feature contract
            - **Then** The Runtime shall make the available transition explicit and shall not continue merely to exhaust a prepared question list, and the resulting state is eligible for the feature terminal condition: Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction..
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

            **Downstream proof:** If this requirement is implemented incorrectly, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The immediate consumer is **F10**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines); `AIR-D014`.

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

1. **Premature semantic closure:** continue the prepared interview script despite live defense, overload, or a landed answer. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
