---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F07
title: Brand Genesis, Voice DNA, Visual DNA, and Distillation Layers
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Brand profile authority
- Human creative authority
dependencies:
- F07
source_documents:
- SRC-BRAND-001
- SRC-RSCS-001
- SRC-CCV-001
- SRC-AHP-F30-001
active_primitives:
- PRM-VOC-009
- PRM-VSG-003
- PRM-VSG-021
capability_areas:
- BrandGenesisSessionRef
- BrandContextVersionRef
- VoiceDNAApplication
- VisualDNAApplication
- DistillationTrace
- CCVVariationPlan
- NegativeSpaceIntent
- EdgeIntegrityReceipt
functional_requirements: AIR-FR-037–AIR-FR-042
governing_decision: AIR-D012

---



# F07 — Brand Genesis, Voice DNA, Visual DNA, and Distillation Layers



## 1. Architectural Claim and User Outcome

**User outcome:** The Runtime preserves the guest’s living expression and brand organism while distilling it into category-native scripts and visual programs without centroid collapse.

**Architectural claim:** Brand Context, Voice DNA, and Visual DNA are versioned source systems, not aesthetic moodboards. RSCS distillation removes noise while retaining identity-bearing signal; CCV creates controlled diversity without random drift.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A source-backed expression, coalition, and archetype route require translation into a script or visual program.** The terminal condition is: **The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence.**

The feature protects the product from this concrete shortcut: **imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence** If that shortcut is accepted, the downstream result is not merely lower quality; **the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world**

The feature is governed by `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `BrandGenesisSessionRef`, `BrandContextVersionRef`, `VoiceDNAApplication`, `VisualDNAApplication`, `DistillationTrace`, `CCVVariationPlan`, `NegativeSpaceIntent`, `EdgeIntegrityReceipt`. The owning products and authorities are Activative Intelligence Runtime, Brand profile authority, Human creative authority. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A source-backed expression, coalition, and archetype route require translation into a script or visual program. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `BrandGenesisSessionRef` and `BrandContextVersionRef` |
| Evaluated | hard gates and independent judgment pass | `NegativeSpaceIntent` |
| Terminal | The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `BrandGenesisSessionRef` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `BrandContextVersionRef` | Brand profile authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `VoiceDNAApplication` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `VisualDNAApplication` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `DistillationTrace` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `CCVVariationPlan` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `NegativeSpaceIntent` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `EdgeIntegrityReceipt` | Human creative authority | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| brand_context.py and service | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| brand_genesis.py and service | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| RSCS and CCV doctrine | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP F30 anti-centroid requirements | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://cmf_studio/src/ccp_studio/contracts/brand_genesis.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://cmf_studio/src/ccp_studio/services/brand_genesis_service.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-VOC-009` — Sensory Scene Anchoring | meaning_plane / `voice_audio_intimacy` | Use vivid sensory cues to build the theater of the mind for the listener. | Sensory overload — so many anchors that the listener cannot form a coherent image; Generic sensory cues — 'imagine a beach at sunset' when the coach lives in a winter city |
| `PRM-VSG-003` — Intent Governs Style | meaning_plane / `visual_sonic_guidance` | Subordinate all stylistic choices to the specific communication intent of the artifact. | Choosing a bland, default style and claiming 'simplicity is the intent' out of laziness; Creating completely inconsistent branding because intent shifts wildly |
| `PRM-VSG-021` — Punctum, Air, and Felt Truth | meaning_plane / `visual_sonic_guidance` | During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. | Manufactured Messiness — Staging a 'messy desk' so perfectly that it looks like an Anthropologie catalog, which the viewer immediately clocks as fake; Distracting Flaws — Allowing a flaw that is so jarring (e.g., terrible audio quality) that it actively prevents the user from receiving the value |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/brand_genesis_voice_visual_dna_and_distillation_layers.py` and `src/cmf_activative_intelligence/services/brand_genesis_voice_visual_dna_and_distillation_layers_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F08** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-037 — Require an active Brand Context Version

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every brand-bearing source, script, or visual program shall reference the active Brand Context Version and its originating Brand Genesis Session.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **require an active brand context version** under the active feature contract
            - **Then** Every brand-bearing source, script, or visual program shall reference the active Brand Context Version and its originating Brand Genesis Session, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

### AIR-FR-038 — Apply Guest Voice DNA to text generation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Writers and composers shall use Voice DNA to preserve cadence, vocabulary, stance, rhetorical movement, and credible emotional range while retaining transformation lineage.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **apply guest voice dna to text generation** under the active feature contract
            - **Then** Writers and composers shall use Voice DNA to preserve cadence, vocabulary, stance, rhetorical movement, and credible emotional range while retaining transformation lineage, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

### AIR-FR-039 — Apply Visual DNA to visual activation programs

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Visual programs shall bind Visual DNA tokens, recurring operators, exclusions, reference families, and composition tendencies without allowing Visual DNA to override the current role and tension.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **apply visual dna to visual activation programs** under the active feature contract
            - **Then** Visual programs shall bind Visual DNA tokens, recurring operators, exclusions, reference families, and composition tendencies without allowing Visual DNA to override the current role and tension, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

### AIR-FR-040 — Record RSCS Distillation Layers

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Every transformed script or semantic program shall record the sequence of signal extraction, compression, simplification, and re-expression used to preserve the Edge Product.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **record rscs distillation layers** under the active feature contract
            - **Then** Every transformed script or semantic program shall record the sequence of signal extraction, compression, simplification, and re-expression used to preserve the Edge Product, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

### AIR-FR-041 — Use CCV for controlled variation

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Variation shall occur within declared combinatorial dimensions and preserve source fidelity, coalition function, archetype geometry, and brand identity rather than producing unconstrained alternatives.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **use ccv for controlled variation** under the active feature contract
            - **Then** Variation shall occur within declared combinatorial dimensions and preserve source fidelity, coalition function, archetype geometry, and brand identity rather than producing unconstrained alternatives, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

### AIR-FR-042 — Evaluate Negative Space and Edge Integrity

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-07.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Independent evaluation shall verify that negative space performs its intended attention or participation function and that the result has not converged toward a generic centroid.

            **Trigger and preconditions:** A source-backed expression, coalition, and archetype route require translation into a script or visual program. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable BrandGenesisSessionRef, BrandContextVersionRef, VoiceDNAApplication, VisualDNAApplication, DistillationTrace, CCVVariationPlan, NegativeSpaceIntent, EdgeIntegrityReceipt state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Voice DNA is applied, not imitated generically.; Visual DNA is distinct from provider style prompts.; Distillation cannot erase the Edge Product.; Negative Space performs a function and cannot be treated as leftover room.

            **Positive acceptance scenario**

            - **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
            - **When** the Runtime performs **evaluate negative space and edge integrity** under the active feature contract
            - **Then** Independent evaluation shall verify that negative space performs its intended attention or participation function and that the result has not converged toward a generic centroid, and the resulting state is eligible for the feature terminal condition: The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The immediate consumer is **F08**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid); `AIR-D012`.

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

1. **Premature semantic closure:** imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
