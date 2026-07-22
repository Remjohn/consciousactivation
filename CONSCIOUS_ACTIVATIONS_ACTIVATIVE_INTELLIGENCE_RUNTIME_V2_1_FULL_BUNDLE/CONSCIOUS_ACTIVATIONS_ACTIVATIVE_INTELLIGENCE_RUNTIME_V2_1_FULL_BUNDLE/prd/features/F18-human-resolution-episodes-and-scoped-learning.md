---

type: prd_feature_module
product: Conscious Activations Activative Intelligence Runtime
product_id: CA-AIR
feature_id: F18
title: Human Resolution Episodes and Scoped Learning
version: 2.1.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
date: '2026-07-22'
owners:
- Conscious Activations Studio
- Activative Intelligence Runtime
- Human creative authority
dependencies:
- F18
source_documents:
- SRC-AI2-HRE-001
- SRC-STUDIO-AMENDMENT-001
- SRC-AHP-F26-001
active_primitives:
- EXP-FBK-001
- PRM-PSY-008
- EXP-TRS-003
capability_areas:
- HumanResolutionEpisode
- ChangeRequestProgramRef
- ProgrammingMaterialRecord
- ApplicabilityEnvelope
- SteeringRecipeCandidate
- IdentityDNACandidateResolution
functional_requirements: AIR-FR-103–AIR-FR-108
governing_decision: AIR-D023

---



# F18 — Human Resolution Episodes and Scoped Learning



## 1. Architectural Claim and User Outcome

**User outcome:** Every meaningful operator correction becomes attributable, structured programming material without silently becoming universal doctrine or changing live model weights.

**Architectural claim:** Human corrections are not chat residue. They are high-value evidence about wrong readings, taste boundaries, responsible layers, exact changes, and applicability. Capture is automatic; promotion is governed and scoped.

This feature exists because the Activative Intelligence Runtime cannot be implemented as a loose chain of prompts. It must create a visible, versioned semantic state whose owner, evidence, limits, and downstream consequences are inspectable. The entry condition is: **An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.** The terminal condition is: **The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback.**

The feature protects the product from this concrete shortcut: **turn one operator correction into a global default or live weight update** If that shortcut is accepted, the downstream result is not merely lower quality; **local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness**

The feature is governed by `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler). Historical CMF material supplies exact Primitive, archetype, interview, brand, composition, and service evidence. It does not silently become V2.1 authority.

## 2. Core Architecture and Lifecycle Model

        The feature is a bounded lifecycle responsibility. Its canonical objects are `HumanResolutionEpisode`, `ChangeRequestProgramRef`, `ProgrammingMaterialRecord`, `ApplicabilityEnvelope`, `SteeringRecipeCandidate`, `IdentityDNACandidateResolution`. The owning products and authorities are Conscious Activations Studio, Activative Intelligence Runtime, Human creative authority. No one actor gains every one of those responsibilities merely because a single model or service can technically produce several outputs.

        | State | Required condition | Produced object or receipt |
|---|---|---|
| Entry | An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. | intake and eligibility receipt |
| Compiled | inputs are reconciled under the feature contract | `HumanResolutionEpisode` and `ChangeRequestProgramRef` |
| Evaluated | hard gates and independent judgment pass | `SteeringRecipeCandidate` |
| Terminal | The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback. | immutable feature completion or blocker receipt |
| Superseded | an accepted upstream object changes | additive successor plus descendant invalidation receipt |

        The lifecycle follows five rules. First, the input object is loaded by exact identity rather than copied into an unversioned prompt. Second, the feature computes only the semantic or operational responsibility assigned to it. Third, every material field retains its epistemic state. Fourth, evaluation occurs before the object becomes downstream-eligible. Fifth, supersession is additive and invalidates only dependent descendants.

        The feature must remain compatible with the V2.1 master sequence: Identity and audience context → Matrix of Edging → Activation Hypothesis Portfolio → Primitive bindings and coalition → psychological role inside a tension → archetype coalition → Guest Voice DNA Final Script → category-native composition → execution → observation → HumanResolution and scoped learning. A feature may participate in only part of that sequence, but it cannot invent an alternate sequence that bypasses the governing gates.

## 3. Canonical Objects, Schemas, and Contracts

        | Canonical object | Owner | Required purpose |
|---|---|---|
| `HumanResolutionEpisode` | Conscious Activations Studio | primary typed state for this feature; exact lineage and lifecycle are mandatory |
| `ChangeRequestProgramRef` | Activative Intelligence Runtime | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ProgrammingMaterialRecord` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `ApplicabilityEnvelope` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `SteeringRecipeCandidate` | Human creative authority | versioned intermediate or decision object; exact lineage and lifecycle are mandatory |
| `IdentityDNACandidateResolution` | Human creative authority | evaluation, resolution, or terminal evidence; exact lineage and lifecycle are mandatory |

        Every object uses stable IDs, explicit versions, canonical serialization, source references, lifecycle state, field-level epistemic state where material, and additive supersession. A typed contract must distinguish required fields from optional evidence; absence must be represented explicitly rather than filled with a plausible default.

        The object model also preserves four classifications separately: the product that owns the object, the actor that produced the current version, the workflow role that requested it, and the authority that may accept or supersede it. A Hunter may propose a candidate, an Analyst may evaluate it, a Composer may assemble approved ingredients, and a Commander may authorize a transition; none of those role names grants cross-product sovereignty.

        The schemas for this feature are generated or referenced under `contracts/schemas/`. Human-readable contract notes live under `contracts/`. The implementation Tech Spec maps these contracts to proposed target models, repositories, service interfaces, and tests without designing a duplicate canonical object.

## 4. Architectural Correction and Brownfield Reconciliation

        V2 correctly modeled the temporal lifecycle, but it did not fully integrate the current Primitive, archetype, Brand Genesis, Voice DNA, Visual DNA, RSCS, CCV, SDA, SFL, Final Script, and Composition-Before-Editing laws. The current correction keeps the useful V2 objects and state machines while making the production-semantic dependencies explicit.

        | Predecessor asset | Disposition | V2.1 use |
|---|---|---|
| AI2 HumanResolution schema | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| Studio V2.1 human-resolution architecture | `REUSE_AS_EVIDENCE` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| AHP HumanResolution and Revision Compiler features | `ADAPT` | preserve tested structure and examples; replace obsolete authority and add V2.1 contracts |
| `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/models.py` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |
| `source://studio_amendment/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | `EXACT_SOURCE_REVIEW_REQUIRED` | implementation spec must inspect this path before assigning target ownership |

        Brownfield source is classified before implementation as REUSE, ADAPT, ACTIVATE, REPLACE, or ARCHIVE. Tested pure models, hashing, validators, receipts, registries, and rejection fixtures are preferred for reuse. Services that perform the right execution but own obsolete semantics are adapted behind current interfaces. Historical prompts and archetype files remain evidence and candidate data, not current authority. Fake provider outputs, synthetic URIs represented as real artifacts, and monolithic Studio ownership remain archived behavior.

## 5. Deep Mechanism: Psychological Role, Primitive Physics, and Archetype Consequence

        The feature is interpreted through the central Activative law: **content activates when it gives the viewer a psychological role inside a tension.** For source-activation features, the equivalent question is which role and tension permit the human source to enter a more truthful expression state. For relationship features, the question is which bounded role and micro-commitment fit the current relationship stage. For production features, the question is whether the approved source charge survives into the audience role.

        | Primitive | Plane / family | Core move | Load-bearing constraint |
|---|---|---|---|
| `EXP-FBK-001` — RIM Feedback Discipline | experience_plane / `feedback_scoring` | Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. | Notification Spam — confusing 'Immediate' with 'Constant', pinging the user for every tiny background event until they mute the bot.; Vanity Metrics — giving them a score that goes up arbitrarily (e.g., '10 points for logging in') which contains no meaning about their actual skill. |
| `PRM-PSY-008` — Attack Problem Not Person | meaning_plane / `psychological_diagnostics` | Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. | Toxic Positivity — softening the critique so much that the actual problem is never clearly named or addressed; Passive Aggression — using identity-protecting language as a thin veil for condescension, which clients detect instantly |
| `EXP-TRS-003` — Reflective Social Proof (The Status Share) | experience_plane / `trust_branding` | Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. | Overt marketing logic — treating the share as a transaction rather than an identity signal; Generic assets — using stock imagery rather than the user's specific data/face in the share card |

        These Primitive selections are not decorative citations. The implementation must load their exact YAMLs, including core moves, activation and suppression conditions, misuse modes, conflicts, examples, and source provenance. Their local jobs must appear in a Primitive Binding. When more than one Primitive is active, the program must state their ordering, compatibility, conflicts, Coalition Signature, Edge Product contribution, and Primitive Misuse Risk.

        Archetype evidence becomes relevant only after the coalition is coherent. The archetype cannot be selected by filename similarity or because it historically performed well. It must carry the present psychological role, tension, Guest Voice DNA, source evidence, and category geometry. The operator-approved Final Script then becomes the semantic authority consumed by composition.

## 6. Implementation and Runtime Integration

The proposed primary target modules are `src/cmf_activative_intelligence/human_resolution_episodes_and_scoped_learning.py` and `src/cmf_activative_intelligence/services/human_resolution_episodes_and_scoped_learning_service.py`. The controlling Tech Spec may split those targets when one product boundary or independent runtime requires it, but it may not place the entire feature inside one generic agent.

Implementation begins with exact model and schema validation, then immutable repository operations, then domain services, then independent evaluation, then cross-product handoff. Learned responsibilities are added only after the contract, deterministic baseline, retrieval surface, tools, benchmark, fallback, and HumanResolution capture exist.

The Runtime should prefer deterministic code for identity, hashing, lifecycle legality, exact eligibility, dependency traversal, source alignment, and contract enforcement. Small Programmed Models are appropriate for bounded classification, candidate proposal, tool compilation, script transformation, and diagnosis after the harness reduces ambiguity. Stronger models are teachers and difficult-case planners, not hidden authority. Every execution records the active context, model or deterministic implementation, tools, outputs, evaluation, and fallback.

## 7. Workflow and Cross-Product Integration

Upstream objects are admitted only through typed references. The feature produces objects consumed by **F19** and any explicitly named cross-product handoff. Interview Expression owns live source activation and source resolution; the Activative Intelligence Runtime owns semantic lifecycle programs; the Builder declares dependencies; the Pipeline executes approved derivative programs; the VAE realizes visual demands; Delegation carries product messages; the Studio captures attributable human resolutions.

Every handoff includes exact object version, content hash, source lineage, lifecycle status, epistemic state, owning product, evaluation receipt, limitations, and invalidation relationships. The consumer may reject an object that is stale, unsupported, outside applicability, or missing required evidence. It may not repair an upstream semantic object silently.

The JIT context compiler supplies only the context required by the current bounded role. Hunters receive discovery evidence; Analysts receive full evidence and contradictions; Composers receive approved ingredients and contracts; Commanders receive alternatives, receipts, gates, and stopping laws. The same unrestricted prompt is not given to every role.

## 8. Operator Experience, Supervision, and Self-Translation

The Studio presents this feature as an inspectable lifecycle rather than a black-box generation button. The operator can see the source objects, current state, candidate alternatives, Primitive and archetype dependencies, evaluation evidence, blockers, and exact next admissible actions. The Studio remains a projection and command surface; canonical state remains in the owning product.

A meaningful operator approval, rejection, comparison, revision, direct manipulation, or explanation emits a `HumanResolutionEpisode`. The episode records the before-state, request or action, responsible layer, exact change program, affected descendants, output, evaluation, and applicability. Capture and retrieval indexing are automatic. Promotion to a Steering Recipe, Programmed Model dataset, evaluator rule, archetype authority, Primitive change, Voice DNA update, or Identity DNA observation requires its own evidence and release path.

The product’s self-translation principle is that source activation, expression, and operator resolution become structured derivative and learning material without requiring the operator to reconstruct the production graph manually. The system automates the repeatable work while preserving human semantic and creative authority at genuine boundaries.

## 9. Functional Requirements and Behavior-Specific Acceptance


### AIR-FR-103 — Capture every meaningful human resolution

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Approvals, rejections, candidate selections, revisions, direct manipulations, tool overrides, taste explanations, and publication decisions shall emit immutable HumanResolutionEpisodes.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **capture every meaningful human resolution** under the active feature contract
            - **Then** Approvals, rejections, candidate selections, revisions, direct manipulations, tool overrides, taste explanations, and publication decisions shall emit immutable HumanResolutionEpisodes, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

### AIR-FR-104 — Attribute each resolution to the responsible layer

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.01`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** The episode shall identify whether the issue originated in source understanding, Activative Intelligence, primitive binding, archetype routing, script, retrieval, model, composition, tool, runtime, evaluator, or operator policy.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **attribute each resolution to the responsible layer** under the active feature contract
            - **Then** The episode shall identify whether the issue originated in source understanding, Activative Intelligence, primitive binding, archetype routing, script, retrieval, model, composition, tool, runtime, evaluator, or operator policy, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
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

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

### AIR-FR-105 — Index resolutions automatically as programming material

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Accepted, rejected, repaired, and contradictory episodes shall become retrievable records and candidate SFT, preference, repair, hard-negative, or evaluator examples with exact lineage.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **index resolutions automatically as programming material** under the active feature contract
            - **Then** Accepted, rejected, repaired, and contradictory episodes shall become retrievable records and candidate SFT, preference, repair, hard-negative, or evaluator examples with exact lineage, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
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

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

### AIR-FR-106 — Prohibit automatic global promotion and live weight mutation

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.02`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Production use may append evidence and indexes but shall not update live weights, canonical Skills, Primitive registries, archetype authority, or doctrine without a release process.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **prohibit automatic global promotion and live weight mutation** under the active feature contract
            - **Then** Production use may append evidence and indexes but shall not update live weights, canonical Skills, Primitive registries, archetype authority, or doctrine without a release process, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
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

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

### AIR-FR-107 — Promote Steering Recipes and learned claims within applicability envelopes

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Promotion shall require repeated evidence, control comparisons, regression cases, scope, lifecycle, rollback, and human authority.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **promote steering recipes and learned claims within applicability envelopes** under the active feature contract
            - **Then** Promotion shall require repeated evidence, control comparisons, regression cases, scope, lifecycle, rollback, and human authority, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
            - **And** the result records the active Primitive bindings, epistemic state, product owner, evaluator, and descendant dependencies when applicable.

            **Adversarial denial scenario**

            - **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence
            - **When** the same operation is requested
            - **Then** the Runtime emits a typed blocker before the invalid state becomes downstream-eligible.
            - **And** no missing source truth, Primitive meaning, human decision, or product authority is synthesized to make the request pass.

            **Required evidence**

            - exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

### AIR-FR-108 — Resolve Identity DNA candidate observations explicitly

            **Owning product:** Conscious Activations Studio  
            **Primary Story:** `AIR-ST-18.03`  
            **Lifecycle:** `NEW_V2_1_OR_DEEPENED`  
            **Requirement:** Identity observations may be accepted, rejected, narrowed, or superseded through a separate profile-resolution event linked to source evidence and HumanResolutionEpisodes.

            **Trigger and preconditions:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result. Exact inputs, source references, product ownership, active versions, and prerequisite receipts must resolve before the operation begins.

            **Required output or transition:** The operation produces or updates the applicable HumanResolutionEpisode, ChangeRequestProgramRef, ProgrammingMaterialRecord, ApplicabilityEnvelope, SteeringRecipeCandidate, IdentityDNACandidateResolution state and moves toward the terminal condition without changing upstream meaning or hiding uncertainty.

            **Invariants:** One correction is not universal doctrine.; Capture and indexing are automatic.; Live weights and canonical Skills are not rewritten by production usage.; Direct UI changes and language requests produce equivalent typed evidence.

            **Positive acceptance scenario**

            - **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
            - **When** the Runtime performs **resolve identity dna candidate observations explicitly** under the active feature contract
            - **Then** Identity observations may be accepted, rejected, narrowed, or superseded through a separate profile-resolution event linked to source evidence and HumanResolutionEpisodes, and the resulting state is eligible for the feature terminal condition: The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback..
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

            **Downstream proof:** If this requirement is implemented incorrectly, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The immediate consumer is **F19**, which must be able to deny the object using only its public contract and receipts.

            **Sources and decision:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler); `AIR-D023`.

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

1. **Premature semantic closure:** turn one operator correction into a global default or live weight update. Mitigation: candidate and hard-gate evidence remains visible until a lawful stopping condition.
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
