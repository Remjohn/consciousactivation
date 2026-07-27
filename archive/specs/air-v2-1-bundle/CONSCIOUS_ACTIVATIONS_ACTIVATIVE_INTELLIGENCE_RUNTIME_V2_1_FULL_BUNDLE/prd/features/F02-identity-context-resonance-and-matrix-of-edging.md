---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F02
title: Identity, Context Premise, Resonance, and Matrix of Edging
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Interview Expression
- Human profile authority
dependencies:
- F02
source_documents:
- SRC-INT-001
- SRC-INT-002
- SRC-MOE-001
- SRC-BRAND-001
- SRC-RSCS-001
- SRC-CCV-001
active_primitives:
- PRM-PSY-001
- PRM-PSY-008
- PRM-PRS-015
capability_areas:
- IdentityDNAReference
- AudienceContextPremise
- InterviewerResonanceContext
- RelationshipContext
- MatrixOfEdgingProgram
- BroadSignal
- EdgeProductCandidate
- IdentityDNACandidateObservation
functional_requirements: AIR-FR-007–AIR-FR-012
governing_decision: AIR-D007

---



# F02 — Identity, Context Premise, Resonance, and Matrix of Edging



## 1. Architectural Claim and User Outcome

**User outcome:** The Runtime forms a source-backed broad signal and Edge Product from real identity, audience, interviewer, and relationship context without mutating human-owned identity truth.

**Architectural claim:** Identity DNA and Context Premise do not become useful merely by coexisting. The Runtime must expose the broad signal, pressure field, resonance, contradiction, and role possibilities that can produce genuine expression.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.** The terminal condition is: **The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation.**

The feature protects the product from this concrete shortcut: **use topic similarity as a substitute for identity, resonance, and Matrix survival** If that shortcut is accepted, the downstream result is not merely lower quality; **the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers**

The feature is governed by `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `IdentityDNAReference`, `AudienceContextPremise`, `InterviewerResonanceContext`, `RelationshipContext`, `MatrixOfEdgingProgram`, `BroadSignal`, `EdgeProductCandidate`, `IdentityDNACandidateObservation`. The owning products and authorities are Activative Intelligence Runtime, Interview Expression, Human profile authority. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `IdentityDNAReference` and `AudienceContextPremise` |
| Evaluated | hard gates and independent judgment pass | `EdgeProductCandidate` |
| Terminal | The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `IdentityDNAReference` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `AudienceContextPremise` | Interview Expression | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `InterviewerResonanceContext` | Human profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `RelationshipContext` | Human profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `MatrixOfEdgingProgram` | Human profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `BroadSignal` | Human profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `EdgeProductCandidate` | Human profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `IdentityDNACandidateObservation` | Human profile authority | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| Matrix contracts and compiler service | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Brand Context and Brand Genesis contracts | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Identity DNA references in current Builder contracts | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/contracts/brand_genesis.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/src/ccp_studio/services/brand_genesis_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/Matrix of Edging.md` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/identity_context_resonance_and_matrix_of_edging.py` and `src/cmf_activative_intelligence/services/identity_context_resonance_and_matrix_of_edging_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F03** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-007 — Load immutable identity and brand context references

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall resolve exact Identity DNA, Brand Context Version, Brand Genesis Session, Voice DNA, and Visual DNA references required by the current activation objective.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **load immutable identity and brand context references** under the active feature contract
            - **Then** The Runtime shall resolve exact Identity DNA, Brand Context Version, Brand Genesis Session, Voice DNA, and Visual DNA references required by the current activation objective, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

### AIR-FR-008 — Compile the audience Context Premise

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall represent the audience situation, self-perception, pressure, desired movement, probable defenses, and relationship stage as a versioned Context Premise.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **compile the audience context premise** under the active feature contract
            - **Then** The Runtime shall represent the audience situation, self-perception, pressure, desired movement, probable defenses, and relationship stage as a versioned Context Premise, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

### AIR-FR-009 — Represent Interviewer Resonance and relationship context

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Source activation shall include the interviewer’s real resonance, lived stake, curiosity, and current relationship context when those conditions materially affect the guest response.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **represent interviewer resonance and relationship context** under the active feature contract
            - **Then** Source activation shall include the interviewer’s real resonance, lived stake, curiosity, and current relationship context when those conditions materially affect the guest response, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
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
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

### AIR-FR-010 — Compile the Matrix broad signal

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Matrix compiler shall intersect guest truth, audience reality, interviewer or relationship resonance, and current objective to produce a broad signal before edge candidates are ranked.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **compile the matrix broad signal** under the active feature contract
            - **Then** The Matrix compiler shall intersect guest truth, audience reality, interviewer or relationship resonance, and current objective to produce a broad signal before edge candidates are ranked, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

### AIR-FR-011 — Form an Edge Product candidate from survived pressure

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall form an Edge Product only from edges that survive source evidence, identity fit, counteractivation analysis, and the relevant planned or observed state.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **form an edge product candidate from survived pressure** under the active feature contract
            - **Then** The Runtime shall form an Edge Product only from edges that survive source evidence, identity fit, counteractivation analysis, and the relevant planned or observed state, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

### AIR-FR-012 — Propose Identity DNA candidate observations without mutation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-02.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime may emit evidence-linked Identity DNA candidate observations from repeated or strong expression, but canonical Identity DNA changes require a separate operator resolution.

            **Trigger and preconditions:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable IdentityDNAReference, AudienceContextPremise, InterviewerResonanceContext, RelationshipContext, MatrixOfEdgingProgram, BroadSignal, EdgeProductCandidate, IdentityDNACandidateObservation state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Identity DNA remains human-owned.; The Matrix of Edging is not a generic topic brainstorm.; Interviewer Resonance is evidence-bearing context, not a fabricated persona.; An Edge Product is formed only after candidate survival and, where applicable, reaction evidence.

            **Positive acceptance scenario**

            - **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
            - **When** the Runtime performs **propose identity dna candidate observations without mutation** under the active feature contract
            - **Then** The Runtime may emit evidence-linked Identity DNA candidate observations from repeated or strong expression, but canonical Identity DNA changes require a separate operator resolution, and the resulting state is eligible for the feature terminal condition: The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The immediate consumer is **F03**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D007`.

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

1. **Premature semantic closure:** use topic similarity as a substitute for identity, resonance, and Matrix survival. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
