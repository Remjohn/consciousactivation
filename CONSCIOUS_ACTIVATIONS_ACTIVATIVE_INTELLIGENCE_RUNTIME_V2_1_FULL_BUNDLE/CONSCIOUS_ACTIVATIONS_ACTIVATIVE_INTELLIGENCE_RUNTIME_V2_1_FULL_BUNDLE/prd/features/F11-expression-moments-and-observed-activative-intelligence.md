---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F11
title: Expression Moments and Observed Activative Intelligence
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Interview Expression
- Activative Intelligence Runtime
- Human expression authority
dependencies:
- F11
source_documents:
- SRC-AI2-EXPRESSION-001
- SRC-SOURCE-FIRST-001
- SRC-INT-002
active_primitives:
- PRM-VOC-009
- PRM-VSG-021
- PRM-PRS-002
capability_areas:
- ExpressionMomentCandidate
- ExpressionMoment
- ExpressionMomentDecision
- ObservedActivativeIntelligencePack
- ExpressionResolutionReceipt
functional_requirements: AIR-FR-061–AIR-FR-066
governing_decision: AIR-D016

---



# F11 — Expression Moments and Observed Activative Intelligence



## 1. Architectural Claim and User Outcome

**User outcome:** The system resolves complete, source-backed expression moments and compiles what actually emerged into an Observed Activative Intelligence Pack.

**Architectural claim:** An Expression Moment is not a catchy sentence. It is a bounded unit of real expression whose premise, reaction, context, identity role, and route potential survive extraction.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.** The terminal condition is: **Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not.**

The feature protects the product from this concrete shortcut: **extract the shortest quotable phrase and omit the premise or reaction tail** If that shortcut is accepted, the downstream result is not merely lower quality; **a line becomes quotable only because its qualifying premise and emotional tail were removed**

The feature is governed by `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `ExpressionMomentCandidate`, `ExpressionMoment`, `ExpressionMomentDecision`, `ObservedActivativeIntelligencePack`, `ExpressionResolutionReceipt`. The owning products and authorities are Interview Expression, Activative Intelligence Runtime, Human expression authority. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `ExpressionMomentCandidate` and `ExpressionMoment` |
| Evaluated | hard gates and independent judgment pass | `ObservedActivativeIntelligencePack` |
| Terminal | Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `ExpressionMomentCandidate` | Interview Expression | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `ExpressionMoment` | Activative Intelligence Runtime | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ExpressionMomentDecision` | Human expression authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ObservedActivativeIntelligencePack` | Human expression authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ExpressionResolutionReceipt` | Human expression authority | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 expression moment schema | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| V9.1 expression capture and routing | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP source-package features F21–F22 | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/services/expression_session_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/CCP V9.1 Expression Capture & Archetype Routing Update.md` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/expression_moments_and_observed_activative_intelligence.py` and `src/cmf_activative_intelligence/services/expression_moments_and_observed_activative_intelligence_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F12** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-061 — Discover Expression Moment candidates from complete evidence

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The system shall use transcript, Reaction Receipts, audio events, keyframes, planned context, observed tags, and source continuity to propose moment candidates.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **discover expression moment candidates from complete evidence** under the active feature contract
            - **Then** The system shall use transcript, Reaction Receipts, audio events, keyframes, planned context, observed tags, and source continuity to propose moment candidates, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

### AIR-FR-062 — Set boundaries that preserve premise and reaction tail

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Candidate boundaries shall include the minimum source context needed to prevent quote collapse, preserve the cause of the expression, and retain the relevant reaction tail.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **set boundaries that preserve premise and reaction tail** under the active feature contract
            - **Then** Candidate boundaries shall include the minimum source context needed to prevent quote collapse, preserve the cause of the expression, and retain the relevant reaction tail, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
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
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

### AIR-FR-063 — Score moment qualities and routeability

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The resolver shall evaluate completeness, specificity, identity signal, pressure survival, emotional or cognitive turn, audiovisual usability, and eligible derivative routes.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **score moment qualities and routeability** under the active feature contract
            - **Then** The resolver shall evaluate completeness, specificity, identity signal, pressure survival, emotional or cognitive turn, audiovisual usability, and eligible derivative routes, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

### AIR-FR-064 — Maintain an explicit Expression Moment lifecycle

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Candidates shall move through proposed, observed, borderline, approved, rejected, superseded, and revoked states with immutable decisions and evidence.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **maintain an explicit expression moment lifecycle** under the active feature contract
            - **Then** Candidates shall move through proposed, observed, borderline, approved, rejected, superseded, and revoked states with immutable decisions and evidence, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

### AIR-FR-065 — Compile an Observed Activative Intelligence Pack

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall compile actual roles, directions, pressures, urges, edges, primitive and archetype evidence, reactions, limitations, and planned–observed deltas from approved source evidence.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **compile an observed activative intelligence pack** under the active feature contract
            - **Then** The Runtime shall compile actual roles, directions, pressures, urges, edges, primitive and archetype evidence, reactions, limitations, and planned–observed deltas from approved source evidence, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

### AIR-FR-066 — Handoff approved source expression without losing authority

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-11.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Observed AIP shall reference exact source packages and moments and shall not grant the derivative producer authority to reinterpret the guest’s meaning.

            **Trigger and preconditions:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ExpressionMomentCandidate, ExpressionMoment, ExpressionMomentDecision, ObservedActivativeIntelligencePack, ExpressionResolutionReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Moment boundaries preserve premise and reaction tail.; Observed AIP cannot copy unconfirmed planned fields.; Rejections remain negative evidence.; Expression approval is separate from derivative-route approval.

            **Positive acceptance scenario**

            - **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
            - **When** the Runtime performs **handoff approved source expression without losing authority** under the active feature contract
            - **Then** The Observed AIP shall reference exact source packages and moments and shall not grant the derivative producer authority to reinterpret the guest’s meaning, and the resulting state is eligible for the feature terminal condition: Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, a line becomes quotable only because its qualifying premise and emotional tail were removed The immediate consumer is **F12**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing); `AIR-D016`.

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

1. **Premature semantic closure:** extract the shortest quotable phrase and omit the premise or reaction tail. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
