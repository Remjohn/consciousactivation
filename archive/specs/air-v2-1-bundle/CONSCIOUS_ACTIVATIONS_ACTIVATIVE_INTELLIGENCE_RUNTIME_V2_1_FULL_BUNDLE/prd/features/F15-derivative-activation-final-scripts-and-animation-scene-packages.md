---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F15
title: Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory
  Animation Scene Packages
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Human script authority
- Atomic Harness Pipeline consumer
dependencies:
- F15
source_documents:
- SRC-AHP-F25-001
- SRC-AHP-F28-001
- SRC-BRAND-001
- SRC-ARCH-001
active_primitives:
- PRM-VOC-009
- PRM-VSG-003
- PRM-PRS-015
capability_areas:
- DerivativeActivationProgram
- FinalScriptPackage
- ScriptSegmentLineage
- ArchetypeCoalitionProgram
- AnimationScenePackage
- SemanticProductionPackage
functional_requirements: AIR-FR-085–AIR-FR-090
governing_decision: AIR-D020

---



# F15 — Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory Animation Scene Packages



## 1. Architectural Claim and User Outcome

**User outcome:** Every derivative begins from an approved source-backed semantic production package, and every eligible script yields reusable 2D animation scene compositions even when a complete animation short is not immediately rendered.

**Architectural claim:** Quotes and Expression Moments are ingredients, not final scripts. JIT Skill writers and Composers transform approved source material through Voice DNA, Primitive coalitions, archetype geometry, and operator approval before composition.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An approved Expression Moment, source package, campaign role, and derivative objective exist.** The terminal condition is: **A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning.**

The feature protects the product from this concrete shortcut: **begin composition from raw quotes or generic copy before archetype-coalition Final Script approval** If that shortcut is accepted, the downstream result is not merely lower quality; **copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment**

The feature is governed by `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `DerivativeActivationProgram`, `FinalScriptPackage`, `ScriptSegmentLineage`, `ArchetypeCoalitionProgram`, `AnimationScenePackage`, `SemanticProductionPackage`. The owning products and authorities are Activative Intelligence Runtime, Human script authority, Atomic Harness Pipeline consumer. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An approved Expression Moment, source package, campaign role, and derivative objective exist. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `DerivativeActivationProgram` and `FinalScriptPackage` |
| Evaluated | hard gates and independent judgment pass | `AnimationScenePackage` |
| Terminal | A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `DerivativeActivationProgram` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `FinalScriptPackage` | Human script authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ScriptSegmentLineage` | Atomic Harness Pipeline consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ArchetypeCoalitionProgram` | Atomic Harness Pipeline consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `AnimationScenePackage` | Atomic Harness Pipeline consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SemanticProductionPackage` | Atomic Harness Pipeline consumer | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AHP derivative and Final Script requirements | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| JIT Skill compiler service | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| asset_package contracts | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| V9 archetype routing | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/src/ccp_studio/services/narrative_story_doctor_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `PRM-PRS-015` — The What Is / What Could Be Contrast Engine | meaning_plane / `persuasion` | Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. | Over-Hyping the Future — painting a 'what could be' that is so utopian and disconnected from reality that the audience rejects it as impossible; Walloping with 'What Is' — spending so much time on the audience's current pain that they become demoralized and tune out before the solution is offered |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/derivative_activation_final_scripts_and_animation_scene_packages.py` and `src/cmf_activative_intelligence/services/derivative_activation_final_scripts_and_animation_scene_packages_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F16** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-085 — Compile a Derivative Activation Program

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Each short, Carousel, SuperVisual, animation scene, or relationship asset shall declare source ingredients, viewer role, tension, Edge Product, primitive coalition, archetype coalition, Voice/Visual DNA, and transfer requirements.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **compile a derivative activation program** under the active feature contract
            - **Then** Each short, Carousel, SuperVisual, animation scene, or relationship asset shall declare source ingredients, viewer role, tension, Edge Product, primitive coalition, archetype coalition, Voice/Visual DNA, and transfer requirements, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

### AIR-FR-086 — Use JIT Skill writers and Composers for text transformation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Writers and Composers shall receive only approved source ingredients, relevant Voice DNA, coalition and archetype context, route rules, and transformation constraints.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **use jit skill writers and composers for text transformation** under the active feature contract
            - **Then** Writers and Composers shall receive only approved source ingredients, relevant Voice DNA, coalition and archetype context, route rules, and transformation constraints, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

### AIR-FR-087 — Preserve script-segment transformation lineage

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every verbatim quote, condensation, adaptation, connective line, or rewrite shall identify its source spans, transformation class, authoring program, and approval state.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **preserve script-segment transformation lineage** under the active feature contract
            - **Then** Every verbatim quote, condensation, adaptation, connective line, or rewrite shall identify its source spans, transformation class, authoring program, and approval state, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

### AIR-FR-088 — Require operator approval of the Final Script

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** No composition may begin until the complete archetype-coalition Final Script has been reviewed and approved or explicitly superseded by the operator.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **require operator approval of the final script** under the active feature contract
            - **Then** No composition may begin until the complete archetype-coalition Final Script has been reviewed and approved or explicitly superseded by the operator, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

### AIR-FR-089 — Compose a reusable 2D Animation Scene Package for every eligible script

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The system shall create composition-ready scene programs, visual references, character or symbolic roles, timing, BBOX intent, and asset demands that can serve as B-roll, slide elements, or complete animation scenes.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **compose a reusable 2d animation scene package for every eligible script** under the active feature contract
            - **Then** The system shall create composition-ready scene programs, visual references, character or symbolic roles, timing, BBOX intent, and asset demands that can serve as B-roll, slide elements, or complete animation scenes, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

### AIR-FR-090 — Emit an immutable Semantic Production Package

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-15.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The approved Final Script, coalition, archetype program, animation scene package, source lineage, transfer contract, and evaluation requirements shall be packaged for Builder/Harness/Pipeline consumption.

            **Trigger and preconditions:** An approved Expression Moment, source package, campaign role, and derivative objective exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable DerivativeActivationProgram, FinalScriptPackage, ScriptSegmentLineage, ArchetypeCoalitionProgram, AnimationScenePackage, SemanticProductionPackage state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Text may be verbatim, condensed, adapted, or rewritten, but lineage is explicit.; Guest Voice DNA governs transformed text.; Final Script approval precedes composition.; Animation scene packaging does not activate deferred Format 02.

            **Positive acceptance scenario**

            - **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
            - **When** the Runtime performs **emit an immutable semantic production package** under the active feature contract
            - **Then** The approved Final Script, coalition, archetype program, animation scene package, source lineage, transfer contract, and evaluation requirements shall be packaged for Builder/Harness/Pipeline consumption, and the resulting state is eligible for the feature terminal condition: A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning..
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

            **Downstream proof:** If this requirement is implemented incorrectly, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The immediate consumer is **F16**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition); `AIR-D020`.

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

1. **Premature semantic closure:** begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
