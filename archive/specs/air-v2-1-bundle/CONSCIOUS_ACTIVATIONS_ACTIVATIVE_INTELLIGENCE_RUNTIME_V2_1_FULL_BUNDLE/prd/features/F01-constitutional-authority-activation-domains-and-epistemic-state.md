---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F01
title: Constitutional Authority, Activation Domains, and Epistemic State
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Program Control
- Activative Intelligence Runtime
dependencies:
- Program Control
source_documents:
- SRC-AI2-001
- SRC-AHP-001
- SRC-DOCTRINE-001
active_primitives:
- PRM-PSY-008
- PRM-VSG-003
- EXP-FBK-001
capability_areas:
- ActivationDomainDeclaration
- EpistemicAssertion
- SemanticObjectVersion
- LifecycleTransitionReceipt
- PlannedObservedDelta
functional_requirements: AIR-FR-001–AIR-FR-006
governing_decision: AIR-D006

---



# F01 — Constitutional Authority, Activation Domains, and Epistemic State



## 1. Architectural Claim and User Outcome

**User outcome:** Every semantic claim enters the system with an explicit activation domain, epistemic state, version, owner, and lifecycle consequence.

**Architectural claim:** The Runtime cannot activate, transform, or learn from a semantic object until it knows what kind of activation the object belongs to and what the available evidence permits the system to believe.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.** The terminal condition is: **A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt.**

The feature protects the product from this concrete shortcut: **collapse one object-level status across fields so implementation becomes simpler** If that shortcut is accepted, the downstream result is not merely lower quality; **a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim**

The feature is governed by `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `ActivationDomainDeclaration`, `EpistemicAssertion`, `SemanticObjectVersion`, `LifecycleTransitionReceipt`, `PlannedObservedDelta`. The owning products and authorities are Program Control, Activative Intelligence Runtime. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `ActivationDomainDeclaration` and `EpistemicAssertion` |
| Evaluated | hard gates and independent judgment pass | `LifecycleTransitionReceipt` |
| Terminal | A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `ActivationDomainDeclaration` | Program Control | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `EpistemicAssertion` | Activative Intelligence Runtime | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SemanticObjectVersion` | Activative Intelligence Runtime | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `LifecycleTransitionReceipt` | Activative Intelligence Runtime | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `PlannedObservedDelta` | Activative Intelligence Runtime | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 predecessor lifecycle schemas and state machines | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Builder activative contract compiler evidence | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Program Control authority and claim ceilings | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/lifecycle.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/constitutional_authority_activation_domains_and_epistemic_state.py` and `src/cmf_activative_intelligence/services/constitutional_authority_activation_domains_and_epistemic_state_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F02** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-001 — Declare exactly one activation domain

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every activative program and semantic object shall declare exactly one primary activation domain—source, relationship, audience, campaign, or derivative—and may reference other domains only through typed handoffs.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **declare exactly one activation domain** under the active feature contract
            - **Then** Every activative program and semantic object shall declare exactly one primary activation domain—source, relationship, audience, campaign, or derivative—and may reference other domains only through typed handoffs, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

### AIR-FR-002 — Preserve field-level epistemic state

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every material field shall declare whether it is planned, observed, inferred, operator-confirmed, rejected, or superseded instead of inheriting one undifferentiated object status.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **preserve field-level epistemic state** under the active feature contract
            - **Then** Every material field shall declare whether it is planned, observed, inferred, operator-confirmed, rejected, or superseded instead of inheriting one undifferentiated object status, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

### AIR-FR-003 — Version and supersede semantic objects additively

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Semantic changes shall create immutable successor versions with explicit supersession and invalidation edges; prior versions remain replayable.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **version and supersede semantic objects additively** under the active feature contract
            - **Then** Semantic changes shall create immutable successor versions with explicit supersession and invalidation edges; prior versions remain replayable, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

### AIR-FR-004 — Prevent planned intent from manufacturing observed truth

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall reject any transition that treats a Brief, hypothesis, intended role, or planned tag as evidence that a human expression or audience reaction occurred.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **prevent planned intent from manufacturing observed truth** under the active feature contract
            - **Then** The Runtime shall reject any transition that treats a Brief, hypothesis, intended role, or planned tag as evidence that a human expression or audience reaction occurred, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

### AIR-FR-005 — Compile cross-domain semantic lineage

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every handoff between source, relationship, audience, campaign, and derivative activation shall preserve the originating objects, transformations, and authority boundaries.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **compile cross-domain semantic lineage** under the active feature contract
            - **Then** Every handoff between source, relationship, audience, campaign, and derivative activation shall preserve the originating objects, transformations, and authority boundaries, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

### AIR-FR-006 — Issue lifecycle and epistemology evaluation receipts

            **Owning product:** Program Control  
            **Primary Story:** `AIR-ST-01.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Independent evaluation shall verify domain fit, epistemic correctness, lifecycle legality, and claim ceiling before a semantic object becomes eligible downstream.

            **Trigger and preconditions:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable ActivationDomainDeclaration, EpistemicAssertion, SemanticObjectVersion, LifecycleTransitionReceipt, PlannedObservedDelta state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source, relationship, and audience activation remain distinct programs.; Planned intent never becomes observed truth by implication.; Rejected and superseded claims remain available as negative and historical evidence.; Activative Contract Compiler is not represented as the Activative Intelligence Runtime.

            **Positive acceptance scenario**

            - **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
            - **When** the Runtime performs **issue lifecycle and epistemology evaluation receipts** under the active feature contract
            - **Then** Independent evaluation shall verify domain fit, epistemic correctness, lifecycle legality, and claim ceiling before a semantic object becomes eligible downstream, and the resulting state is eligible for the feature terminal condition: A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt..
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

            **Downstream proof:** If this requirement is implemented incorrectly, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The immediate consumer is **F02**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile); `AIR-D006`.

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

1. **Premature semantic closure:** collapse one object-level status across fields so implementation becomes simpler. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
