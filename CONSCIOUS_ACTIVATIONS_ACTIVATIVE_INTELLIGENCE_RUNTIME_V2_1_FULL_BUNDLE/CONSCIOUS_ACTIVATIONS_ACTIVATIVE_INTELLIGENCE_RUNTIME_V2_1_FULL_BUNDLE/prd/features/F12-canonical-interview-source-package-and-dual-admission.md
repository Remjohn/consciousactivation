---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F12
title: Canonical Interview Source Package and Dual Admission
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Interview Expression
- Operator source authority
- Activative Intelligence Runtime consumer
dependencies:
- F12
source_documents:
- SRC-SOURCE-FIRST-001
- SRC-AI2-SOURCE-001
- SRC-INT-001
active_primitives:
- PRM-VOC-009
- PRM-VSG-003
- EXP-FBK-001
capability_areas:
- CanonicalInterviewSourcePackage
- SourceAdmissionRecord
- SourceVersion
- TagAssertion
- SourcePackageReceipt
- OperatorSourceAuthorityRef
functional_requirements: AIR-FR-067–AIR-FR-072
governing_decision: AIR-D017

---



# F12 — Canonical Interview Source Package and Dual Admission



## 1. Architectural Claim and User Outcome

**User outcome:** Brief-led interviews and imported interviews become equally usable derivative roots without inventing absent planning history.

**Architectural claim:** The canonical source package is the trusted root of interview-derived production. It binds media, transcript, speakers, timestamps, tags, reactions, moments, keyframes, provenance, operator source authority, and route scope.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An Activative Interview session completes or an operator imports an existing interview and transcript.** The terminal condition is: **A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives.**

The feature protects the product from this concrete shortcut: **fabricate missing Brief-led history for an imported interview so both admission paths look identical** If that shortcut is accepted, the downstream result is not merely lower quality; **derivatives cite invented planning history or drift across source-package versions**

The feature is governed by `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `CanonicalInterviewSourcePackage`, `SourceAdmissionRecord`, `SourceVersion`, `TagAssertion`, `SourcePackageReceipt`, `OperatorSourceAuthorityRef`. The owning products and authorities are Interview Expression, Operator source authority, Activative Intelligence Runtime consumer. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An Activative Interview session completes or an operator imports an existing interview and transcript. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `CanonicalInterviewSourcePackage` and `SourceAdmissionRecord` |
| Evaluated | hard gates and independent judgment pass | `SourcePackageReceipt` |
| Terminal | A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `CanonicalInterviewSourcePackage` | Interview Expression | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `SourceAdmissionRecord` | Operator source authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SourceVersion` | Activative Intelligence Runtime consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `TagAssertion` | Activative Intelligence Runtime consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SourcePackageReceipt` | Activative Intelligence Runtime consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `OperatorSourceAuthorityRef` | Activative Intelligence Runtime consumer | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 source package schema | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP source-first PRD F21–F25 | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| CMF Interview Asset Package contracts | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/contracts/expression_session.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/canonical_interview_source_package_and_dual_admission.py` and `src/cmf_activative_intelligence/services/canonical_interview_source_package_and_dual_admission_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F13** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-067 — Support Brief-led admission

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** A completed Activative Interview shall produce a source package that references its Brief, Planned AIP, Interview Asset Contracts, calls, observations, Reaction Receipts, and observed evidence.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **support brief-led admission** under the active feature contract
            - **Then** A completed Activative Interview shall produce a source package that references its Brief, Planned AIP, Interview Asset Contracts, calls, observations, Reaction Receipts, and observed evidence, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

### AIR-FR-068 — Support imported-source admission

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** An imported interview shall become a first-class source package while explicitly declaring which planned activation, anchor, Matrix, or session objects are absent.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **support imported-source admission** under the active feature contract
            - **Then** An imported interview shall become a first-class source package while explicitly declaring which planned activation, anchor, Matrix, or session objects are absent, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

### AIR-FR-069 — Bind exact media, transcript, speakers, timing, and keyframes

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The source package shall hash and version original video/audio, transcript words and phrases, speaker map, time alignment, audio events, shot map, keyframes, and visual references.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **bind exact media, transcript, speakers, timing, and keyframes** under the active feature contract
            - **Then** The source package shall hash and version original video/audio, transcript words and phrases, speaker map, time alignment, audio events, shot map, keyframes, and visual references, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

### AIR-FR-070 — Preserve tag provenance and epistemic state

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every planned, observed, inferred, operator-confirmed, rejected, and superseded tag shall retain its source, timestamp or span, author, and lifecycle state.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **preserve tag provenance and epistemic state** under the active feature contract
            - **Then** Every planned, observed, inferred, operator-confirmed, rejected, and superseded tag shall retain its source, timestamp or span, author, and lifecycle state, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

### AIR-FR-071 — Version source packages additively

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Corrections to transcripts, speaker maps, tags, moments, or references shall create successor package versions and invalidate only dependent derivative programs.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **version source packages additively** under the active feature contract
            - **Then** Corrections to transcripts, speaker maps, tags, moments, or references shall create successor package versions and invalidate only dependent derivative programs, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

### AIR-FR-072 — Publish under operator source authority

            **Owning product:** Interview Expression  
            **Primary Story:** `AIR-ST-12.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The package shall record the operator-provided source authority and intended route scope as provenance and execution context without introducing a separate creative-policy authority.

            **Trigger and preconditions:** An Activative Interview session completes or an operator imports an existing interview and transcript. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CanonicalInterviewSourcePackage, SourceAdmissionRecord, SourceVersion, TagAssertion, SourcePackageReceipt, OperatorSourceAuthorityRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Brief-led and imported admission are both first-class.; Imported sources declare absent planning rather than fabricating it.; Original media remains immutable.; All derivatives bind one exact source-package version.

            **Positive acceptance scenario**

            - **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
            - **When** the Runtime performs **publish under operator source authority** under the active feature contract
            - **Then** The package shall record the operator-provided source authority and intended route scope as provenance and execution context without introducing a separate creative-policy authority, and the resulting state is eligible for the feature terminal condition: A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives..
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

            **Downstream proof:** If this requirement is implemented incorrectly, derivatives cite invented planning history or drift across source-package versions The immediate consumer is **F13**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine); `AIR-D017`.

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

1. **Premature semantic closure:** fabricate missing Brief-led history for an imported interview so both admission paths look identical. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
