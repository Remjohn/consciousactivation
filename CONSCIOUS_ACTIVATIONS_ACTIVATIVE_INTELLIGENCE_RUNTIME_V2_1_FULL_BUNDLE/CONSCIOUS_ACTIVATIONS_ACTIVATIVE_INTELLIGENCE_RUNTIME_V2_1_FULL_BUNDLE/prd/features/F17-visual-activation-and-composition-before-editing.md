---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F17
title: Visual Activation, Composition-Before-Editing, and Production Handoff
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Atomic Harness Builder/Pipeline consumers
- Visual Asset Editor
dependencies:
- F17
source_documents:
- SRC-AI2-VISUAL-001
- SRC-AHP-F09-001
- SRC-AHP-F15-001
- SRC-VISUAL-DOCTRINE-001
active_primitives:
- PRM-VSG-001
- PRM-VSG-024
- PRM-VSG-021
- PRM-BUS-006
capability_areas:
- VisualSemanticCandidate
- VisualNarrativeProgram
- VisualResearchPack
- RealLifeReferencePack
- FeatureContract
- VisualActivationHandoff
- CompositionIntent
functional_requirements: AIR-FR-097–AIR-FR-102
governing_decision: AIR-D022

---



# F17 — Visual Activation, Composition-Before-Editing, and Production Handoff



## 1. Architectural Claim and User Outcome

**User outcome:** The Runtime translates approved semantic activation into a visual program grounded in research, real-life reference, composition function, primitive contracts, and category-native handoffs before editing begins.

**Architectural claim:** Visual generation is downstream of Visual Research, Real-Life Reference, Visual DNA, and Composition. Editing should realize an approved composition program, not discover the meaning by moving assets until something looks polished.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.** The terminal condition is: **A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics.**

The feature protects the product from this concrete shortcut: **start editing or generation before composition intent, negative space, and real-life reference research are resolved** If that shortcut is accepted, the downstream result is not merely lower quality; **editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference**

The feature is governed by `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `VisualSemanticCandidate`, `VisualNarrativeProgram`, `VisualResearchPack`, `RealLifeReferencePack`, `FeatureContract`, `VisualActivationHandoff`, `CompositionIntent`. The owning products and authorities are Activative Intelligence Runtime, Atomic Harness Builder/Pipeline consumers, Visual Asset Editor. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `VisualSemanticCandidate` and `VisualNarrativeProgram` |
| Evaluated | hard gates and independent judgment pass | `VisualActivationHandoff` |
| Terminal | A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `VisualSemanticCandidate` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `VisualNarrativeProgram` | Atomic Harness Builder/Pipeline consumers | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `VisualResearchPack` | Visual Asset Editor | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `RealLifeReferencePack` | Visual Asset Editor | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `FeatureContract` | Visual Asset Editor | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `VisualActivationHandoff` | Visual Asset Editor | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `CompositionIntent` | Visual Asset Editor | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 visual semantic/narrative/feature schemas | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP composition and VAE boundary features | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| CMF visual composition and asset-package contracts | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/contracts/primitive_coalition.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/registries/sda/` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/registries/sfl/` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VSG-001` — Composition as Eye-Path Engineering | meaning_plane / `visual_sonic_guidance` | Structure visual elements within the frame to force a specific sequence of eye movement. | Over-engineering the path to the point where the composition feels forced or unnatural; Applying visual rules to sonic or text-only artifacts |
| `PRM-VSG-024` — Space as Psychological Relationship | meaning_plane / `visual_sonic_guidance` | Before finalizing a visual, define the psychological relationship between the subject and the room/landscape. If the character feels trapped, compose the shot to make the walls literally close in on them. If the character feels lost, place them in a vast, empty space that visually overwhelms their scale. Force the environment to express the internal state of the subject. | The Empty Void — Placing the subject in so much negative space that the image feels unfinished or accidental, rather than intentionally 'vast'; Claustrophobia by Accident — Filming with a tight crop purely out of convenience, unintentionally making the audience feel anxious or trapped |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |
| `PRM-BUS-006` — Hierarchy as Attention Routing | meaning_plane / `design_business` | Assign distinct, uncompetitive visual weights to different semantic roles in the content, ensuring the viewer's eye is routed exactly where it needs to go, in the exact order it needs to go there. | Too Many Levels — Creating 6 different levels of hierarchy that confuse rather than clarify; Arbitrary Emphasis — Bolding random words in a sentence just for 'pop', breaking the semantic meaning |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/visual_activation_and_composition_before_editing.py` and `src/cmf_activative_intelligence/services/visual_activation_and_composition_before_editing_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F18** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-097 — Generate visual semantic candidates from the approved semantic package

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall propose visual metaphors, evidence structures, real-life scenes, graphic relations, and composition strategies tied to the viewer role, tension, coalition, archetype, Voice/Visual DNA, and transfer contract.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **generate visual semantic candidates from the approved semantic package** under the active feature contract
            - **Then** The Runtime shall propose visual metaphors, evidence structures, real-life scenes, graphic relations, and composition strategies tied to the viewer role, tension, coalition, archetype, Voice/Visual DNA, and transfer contract, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

### AIR-FR-098 — Require Visual Research and Real-Life Reference before generation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Visual candidates shall cite specimens, real environments, human references, object behavior, or documented visual systems before generated assets are requested where such reference is applicable.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **require visual research and real-life reference before generation** under the active feature contract
            - **Then** Visual candidates shall cite specimens, real environments, human references, object behavior, or documented visual systems before generated assets are requested where such reference is applicable, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

### AIR-FR-099 — Compile composition intent before editing or rendering

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall define hierarchy, reading path, subject relationships, BBOX function, negative space, sequence role, and intended viewer state before timeline or canvas operations are authorized.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **compile composition intent before editing or rendering** under the active feature contract
            - **Then** The Runtime shall define hierarchy, reading path, subject relationships, BBOX function, negative space, sequence role, and intended viewer state before timeline or canvas operations are authorized, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

### AIR-FR-100 — Compile feature-level visual contracts

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Required gaze, hands, facial expression, props, evidence, text, scale, depth, motion, sonic cues, and wrong-reading locks shall be represented as independently testable Feature Contracts.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **compile feature-level visual contracts** under the active feature contract
            - **Then** Required gaze, hands, facial expression, props, evidence, text, scale, depth, motion, sonic cues, and wrong-reading locks shall be represented as independently testable Feature Contracts, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

### AIR-FR-101 — Emit a bounded Visual Activation Handoff

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The handoff shall include semantic authority, visual narrative, composition intent, asset requirements, allowed variation, source references, and evaluation profile for AHP or VAE consumption.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **emit a bounded visual activation handoff** under the active feature contract
            - **Then** The handoff shall include semantic authority, visual narrative, composition intent, asset requirements, allowed variation, source references, and evaluation profile for AHP or VAE consumption, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

### AIR-FR-102 — Reparse rendered visual syntax and activation function

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-17.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The completed composition shall be reparsed into observed hierarchy, BBOX relationships, gaze, reading order, timing, and role/tension evidence for comparison with intent.

            **Trigger and preconditions:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable VisualSemanticCandidate, VisualNarrativeProgram, VisualResearchPack, RealLifeReferencePack, FeatureContract, VisualActivationHandoff, CompositionIntent state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Visual Research precedes generation.; Real-Life Reference precedes generated approximation when applicable.; Composition precedes editing.; VAE and renderers realize meaning; they do not invent it.

            **Positive acceptance scenario**

            - **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
            - **When** the Runtime performs **reparse rendered visual syntax and activation function** under the active feature contract
            - **Then** The completed composition shall be reparsed into observed hierarchy, BBOX relationships, gaze, reading order, timing, and role/tension evidence for comparison with intent, and the resulting state is eligible for the feature terminal condition: A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The immediate consumer is **F18**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2); `AIR-D022`.

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

1. **Premature semantic closure:** start editing or generation before composition intent, negative space, and real-life reference research are resolved. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
