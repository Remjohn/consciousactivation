---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F13
title: Campaign Activation, Freshness, and Audience Reaction
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Activative Intelligence Runtime
- Atomic Harness Pipeline consumer
- Publishing observation adapters
dependencies:
- F13
source_documents:
- SRC-AI2-CAMPAIGN-001
- SRC-AHP-F23-001
- SRC-CCV-001
active_primitives:
- PRM-PRS-002
- PRM-HUM-021
- EXP-TRS-003
capability_areas:
- CampaignActivationProgram
- CampaignAssetPlan
- ActivationFreshnessProfile
- AudienceReactionReceipt
- CampaignRevision
- FatigueSignal
functional_requirements: AIR-FR-073–AIR-FR-078
governing_decision: AIR-D018

---



# F13 — Campaign Activation, Freshness, and Audience Reaction



## 1. Architectural Claim and User Outcome

**User outcome:** A content batch distributes psychological roles, tensions, directions, archetypes, and primitive coalitions coherently without exhausting one formula or confusing audience response with source reaction.

**Architectural claim:** An asset can be activative in isolation and stale inside a campaign. Campaign intelligence manages sequence, recurrence, relief, escalation, role diversity, and exposure while audience reaction remains a separate evidence domain.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **A canonical source package and approved derivative opportunities exist.** The terminal condition is: **A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision.**

The feature protects the product from this concrete shortcut: **rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls** If that shortcut is accepted, the downstream result is not merely lower quality; **the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth**

The feature is governed by `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `CampaignActivationProgram`, `CampaignAssetPlan`, `ActivationFreshnessProfile`, `AudienceReactionReceipt`, `CampaignRevision`, `FatigueSignal`. The owning products and authorities are Activative Intelligence Runtime, Atomic Harness Pipeline consumer, Publishing observation adapters. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | A canonical source package and approved derivative opportunities exist. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `CampaignActivationProgram` and `CampaignAssetPlan` |
| Evaluated | hard gates and independent judgment pass | `CampaignRevision` |
| Terminal | A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `CampaignActivationProgram` | Activative Intelligence Runtime | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `CampaignAssetPlan` | Atomic Harness Pipeline consumer | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ActivationFreshnessProfile` | Publishing observation adapters | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `AudienceReactionReceipt` | Publishing observation adapters | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `CampaignRevision` | Publishing observation adapters | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `FatigueSignal` | Publishing observation adapters | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 campaign and freshness schemas | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP source-backed batch orchestration | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| CMF recurrence and archetype routing patterns | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/freshness.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `PRM-PRS-002` — Tension-and-Release Narrative Engine | meaning_plane / `persuasion` | Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. | Unresolved Tension — establishing high stakes or a compelling question but failing to deliver a satisfying or commensurate release; Micro-Tension Exhaustion — oscillating between tension and release too rapidly, making the content feel frenetic and exhausting |
| `PRM-HUM-021` — Irony Inversion | meaning_plane / `humor_distortion` | Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. | Irony without conviction — breaking voice through tone markers (caps, emojis, 'just kidding') that expose the reversal prematurely; Irony without Subtext — reversing a statement that has no underlying value judgment, producing confusion rather than comedy |
| `EXP-TRS-003` — Reflective Social Proof (The Status Share) | experience_plane / `trust_branding` | Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. | Overt marketing logic — treating the share as a transaction rather than an identity signal; Generic assets — using stock imagery rather than the user's specific data/face in the share card |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/campaign_activation_freshness_and_audience_reaction.py` and `src/cmf_activative_intelligence/services/campaign_activation_freshness_and_audience_reaction_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F14** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-073 — Compile a Campaign Activation Program

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall sequence source-backed derivative programs with audience segment, role, tension, direction, edge, archetype, primitive signature, format, and intended relationship movement.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **compile a campaign activation program** under the active feature contract
            - **Then** The Runtime shall sequence source-backed derivative programs with audience segment, role, tension, direction, edge, archetype, primitive signature, format, and intended relationship movement, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

### AIR-FR-074 — Enforce role, direction, and archetype diversity

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The campaign shall apply minimum diversity and repetition limits so repeated accusation, regret, inversion, or one archetype formula cannot dominate by local score alone.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **enforce role, direction, and archetype diversity** under the active feature contract
            - **Then** The campaign shall apply minimum diversity and repetition limits so repeated accusation, regret, inversion, or one archetype formula cannot dominate by local score alone, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

### AIR-FR-075 — Maintain an Activation Freshness Profile

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The system shall track prior structures, Primitive coalitions, roles, tensions, visual operators, archetypes, and audience exposure that affect present activation strength.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **maintain an activation freshness profile** under the active feature contract
            - **Then** The system shall track prior structures, Primitive coalitions, roles, tensions, visual operators, archetypes, and audience exposure that affect present activation strength, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

### AIR-FR-076 — Capture audience reaction as a separate evidence stream

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Publishing observations shall produce Audience Reaction Receipts tied to exact asset versions, audience context, platform, exposure window, and measurement limits.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **capture audience reaction as a separate evidence stream** under the active feature contract
            - **Then** Publishing observations shall produce Audience Reaction Receipts tied to exact asset versions, audience context, platform, exposure window, and measurement limits, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

### AIR-FR-077 — Detect campaign counteractivation and fatigue

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The Runtime shall identify defensive repetition, habituation, formula visibility, role overload, edge overuse, and relief deficits across the campaign.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **detect campaign counteractivation and fatigue** under the active feature contract
            - **Then** The Runtime shall identify defensive repetition, habituation, formula visibility, role overload, edge overuse, and relief deficits across the campaign, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

### AIR-FR-078 — Revise campaign programs additively

            **Owning product:** Activative Intelligence Runtime  
            **Primary Story:** `AIR-ST-13.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Campaign revisions shall supersede only affected asset plans or sequencing decisions while preserving published history, source lineage, and prior performance evidence.

            **Trigger and preconditions:** A canonical source package and approved derivative opportunities exist. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable CampaignActivationProgram, CampaignAssetPlan, ActivationFreshnessProfile, AudienceReactionReceipt, CampaignRevision, FatigueSignal state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** Source reaction and audience reaction remain separate.; Campaign diversity is non-compensable.; Freshness is audience- and context-specific.; Performance data cannot silently rewrite semantic authority.

            **Positive acceptance scenario**

            - **Given** A canonical source package and approved derivative opportunities exist.
            - **When** the Runtime performs **revise campaign programs additively** under the active feature contract
            - **Then** Campaign revisions shall supersede only affected asset plans or sequencing decisions while preserving published history, source lineage, and prior performance evidence, and the resulting state is eligible for the feature terminal condition: A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision..
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

            **Downstream proof:** If this requirement is implemented incorrectly, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The immediate consumer is **F14**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation); `AIR-D018`.

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

1. **Premature semantic closure:** rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
