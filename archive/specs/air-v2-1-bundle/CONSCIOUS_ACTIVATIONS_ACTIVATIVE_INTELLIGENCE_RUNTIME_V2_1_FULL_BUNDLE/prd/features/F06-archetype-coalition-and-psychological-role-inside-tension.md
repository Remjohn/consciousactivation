---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F06
title: Archetype Coalition and Psychological Role Inside a Tension
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Archetype registry authority
- Human creative authority
dependencies:
- F06
source_documents:
- SRC-ARCH-001
- SRC-ARCH-002
- SRC-SDA-001
- SRC-SFL-001
- SRC-AHP-F28-001
active_primitives:
- PRM-PSY-001
- PRM-PRS-002
- PRM-HUM-021
capability_areas:
- CoreContentArchetypeRef
- DerivativeArchetypeRef
- PsychologicalRoleTensionContract
- ArchetypeCoalitionProgram
- ArchetypeRouteReceipt
- SDARef
- SFLRef
functional_requirements: AIR-FR-031–AIR-FR-036
governing_decision: AIR-D011

---



# F06 — Archetype Coalition and Psychological Role Inside a Tension



## 1. Architectural Claim and User Outcome

**User outcome:** Every content or relationship program gives the participant a specific psychological role inside a source-backed tension and organizes that activation through an eligible archetype coalition.

**Architectural claim:** Content activates when it gives the viewer a psychological role inside a tension. Archetypes are not content templates; they are interaction geometries that organize a Primitive coalition, role, tension, evidence, and sequence.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A validated Edge Product and current activation domain are available.** The terminal condition is: **The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry.**

The feature protects the product from this concrete shortcut: **select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension** If that shortcut is accepted, the downstream result is not merely lower quality; **the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative**

The feature is governed by `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `CoreContentArchetypeRef`, `DerivativeArchetypeRef`, `PsychologicalRoleTensionContract`, `ArchetypeCoalitionProgram`, `ArchetypeRouteReceipt`, `SDARef`, `SFLRef`. The owning products and authorities are Activative Intelligence Runtime, Archetype registry authority, Human creative authority. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A validated Edge Product and current activation domain are available. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `CoreContentArchetypeRef` and `DerivativeArchetypeRef` |
| Evaluated | hard gates and independent judgment pass | `SDARef` |
| Terminal | The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `CoreContentArchetypeRef` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `DerivativeArchetypeRef` | Archetype registry authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `PsychologicalRoleTensionContract` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ArchetypeCoalitionProgram` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ArchetypeRouteReceipt` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SDARef` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SFLRef` | Human creative authority | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| V9 archetype inventory | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| archetype_subsystem_compiler_service.py | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| SDA and SFL registries | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP F28 archetype coalition requirements | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/reference/conscious-rivers/src/ccp/harness/intelligence/archetype_prompts/` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PSY-001` — Matching Principle | meaning_plane / `psychological_diagnostics` | Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. | Layer Inflexibility — detecting the initial layer and refusing to shift when the client naturally transitions to a different layer.; Performative Matching — using the vocabulary of a layer without genuine alignment or empathy, which clients detect as manipulation. |
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |
| `PRM-HUM-021` — Irony Inversion | meaning_plane / `humor_distortion` | Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. | Irony without conviction — breaking voice through tone markers (caps, emojis, 'just kidding') that expose the reversal prematurely; Irony without Subtext — reversing a statement that has no underlying value judgment, producing confusion rather than comedy |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/archetype_coalition_and_psychological_role_inside_tension.py` and `src/cmf_activative_intelligence/services/archetype_coalition_and_psychological_role_inside_tension_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F07** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-031 — Select a source-supported Core Content Archetype

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall select or propose a Core Content Archetype only when its interaction geometry fits the Edge Product, source evidence, audience state, and intended movement.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **select a source-supported core content archetype** under the active feature contract
            - **Then** The Runtime shall select or propose a Core Content Archetype only when its interaction geometry fits the Edge Product, source evidence, audience state, and intended movement, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

### AIR-FR-032 — Select derivative archetype and route

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Each derivative shall declare its content archetype, asset derivative route, category, and route scope instead of inheriting a generic content type.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **select derivative archetype and route** under the active feature contract
            - **Then** Each derivative shall declare its content archetype, asset derivative route, category, and route scope instead of inheriting a generic content type, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

### AIR-FR-033 — Declare the participant psychological role inside the tension

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every audience- or relationship-facing program shall name the role the person is invited to inhabit, the tension that makes the role meaningful, and the action or recognition the role enables.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **declare the participant psychological role inside the tension** under the active feature contract
            - **Then** Every audience- or relationship-facing program shall name the role the person is invited to inhabit, the tension that makes the role meaningful, and the action or recognition the role enables, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

### AIR-FR-034 — Compile bounded multi-archetype coalitions

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** When more than one archetype is used, the Runtime shall declare primary, supporting, transition, and excluded archetypes and prevent geometry conflict or centroid blending.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **compile bounded multi-archetype coalitions** under the active feature contract
            - **Then** When more than one archetype is used, the Runtime shall declare primary, supporting, transition, and excluded archetypes and prevent geometry conflict or centroid blending, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

### AIR-FR-035 — Bind SDA and SFL references

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The archetype program shall resolve the applicable Story Design Archetype and Story Function Layer references required to preserve narrative function and derivative routing.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **bind sda and sfl references** under the active feature contract
            - **Then** The archetype program shall resolve the applicable Story Design Archetype and Story Function Layer references required to preserve narrative function and derivative routing, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

### AIR-FR-036 — Issue an Archetype Route Receipt

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-06.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The accepted route shall record Edge Product fit, role/tension contract, coalition structure, alternatives rejected, source lineage, and approval state.

            **Trigger and preconditions:** A validated Edge Product and current activation domain are available. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CoreContentArchetypeRef, DerivativeArchetypeRef, PsychologicalRoleTensionContract, ArchetypeCoalitionProgram, ArchetypeRouteReceipt, SDARef, SFLRef state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Archetypes never replace source truth.; The viewer role and tension are explicit before composition.; Archetype coalitions are source- and format-dependent.; One archetype may lead while others support; unbounded hybridization is rejected.

            **Positive acceptance scenario**

            - **Given** A validated Edge Product and current activation domain are available.
            - **When** the Runtime performs **issue an archetype route receipt** under the active feature contract
            - **Then** The accepted route shall record Edge Product fit, role/tension contract, coalition structure, alternatives rejected, source lineage, and approval state, and the resulting state is eligible for the feature terminal condition: The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The immediate consumer is **F07**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition); `AIR-D011`.

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

1. **Premature semantic closure:** select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
