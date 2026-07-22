---
type: technical_specification
spec_id: TS-AIR-014
title: Relationship Activation and ReelCast Progression
version: 2.1.0-candidate
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Activative Intelligence Runtime
feature_id: F14
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED
output_path_class: DIRECT_PRODUCT_SPEC_PATH
date: '2026-07-22'
controlling_frs:
  - AIR-FR-079
  - AIR-FR-080
  - AIR-FR-081
  - AIR-FR-082
  - AIR-FR-083
  - AIR-FR-084
controlling_stories:
  - AIR-ST-14.01
  - AIR-ST-14.02
  - AIR-ST-14.03
upstream_drafts:
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-003
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-014 — Relationship Activation and ReelCast Progression

This is specification work only. The V2.1 authority package is `CANDIDATE_NOT_CURRENT`. This document is `WRITTEN_PENDING_AUDIT`; it is not accepted, adopted for build, implemented, production-eligible, or certified. It creates no Development Capsule and grants no build authority.

## 1. Files and authorities read

### Authority, requirements, and workflow inputs

| Class | Exact path | SHA-256 | Lifecycle state and fact used |
|---|---|---|---|
| Current AIR authority marker | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Candidate pending human ratification; separate Capsule required for implementation. |
| AIR Constitution candidate | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | `CANDIDATE_NOT_CURRENT`; relationship activation is a distinct evidence-bearing domain and must not fabricate trust. |
| Controlling feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F14-relationship-activation-and-reelcast-progression.md` | `c6c8c02213c6656cbb5b8d632f22888b0911543cac4b2408c95c0e89641eaf80` | Candidate PRD module; controls AIR-FR-079 through AIR-FR-084. |
| Controlling Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45db8df2010592fd7da0` | Candidate planning source; AIR-ST-14.01 through AIR-ST-14.03 require positive, adversarial, supersession, and downstream-denial evidence. |
| Prior full draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-014-relationship-activation-and-reelcast-progression.md` | `9467223ad328f45a33ce3581232bb788639af63b243e8cdbb101dc2d49a25172` | Draft assignment source; amended to the V3.3 ten-section contract, exact draft interfaces, and current ownership decisions. |
| Root instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Requires exact source, Primitive, authority, feature, Story, and brownfield review; no applicable `AGENTS.md` exists under the prospective `04_ACTIVATIVE_INTELLIGENCE_RUNTIME` root. |
| Writer skill | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | V3.3 one-spec writer law; writer cannot audit or accept its own output. |
| Recovery packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-AIR-014-RECOVERY`; one exact product-spec path, Wave 3. |
| Wave dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_03_DISPATCH_LOCK.yaml` | `e8137e45a267767fd3e0b2f5bdc278ac66d570187b34b4a48ef282db84bdca65` | Dispatches TS-AIR-014 with the two frozen upstream draft hashes below. |
| Specification-work authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | `ACTIVE_SPECIFICATION_WORK_ONLY`; write and independent technical lifecycle allowed, build forbidden. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Ratification pending; ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. |
| Path registry | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/PATH_OWNERSHIP_REGISTRY.yaml` | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | Reserves this exact direct AIR product-spec path to lane B. |
| Write-authority matrix | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | `PASS_EXPLICIT_PROMPT02_AND_PROMPT02C_SPECIFICATION_PATH_AUTHORIZATION`. |
| Canonical spec ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | TS-AIR-014 is a full draft queued for Gate B; implementation and production are false. |
| Canonical FR ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Each controlling FR has AIR as primary owner and this spec as its sole canonical spec. |
| FR traceability ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Preserves exact FR wording, Story ownership, evidence, and claim ceiling. |
| Source disposition ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | SRC-AI2-REL-001, SRC-INT-001, and SRC-MOE-001 are readable `REQUIRED_UNIQUE_EVIDENCE`. |
| Source-gap registry | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_GAP_NOTICE.yaml` | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | No unresolved required source gap applies to TS-AIR-014. |
| Ownership matrices | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml`; `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39`; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns semantic programs; Interview Expression owns live source/reaction evidence; Studio projects/corrects; Pipeline executes; VAE realizes; Delegation transports. |

The reconciliation input lock (`ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456`), dependency DAG (`1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb`), dependency-stage classification (`4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8`), and writing-wave DAG (`24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60`) were also read. Edges `SDE-013` and `SDE-014` are `WRITE_INTERFACE_DEPENDENCY`; neither acceptance nor build state blocks WRITE.

### Frozen upstream drafts

| Edge | Exact path | State | Bytes | SHA-256 | Admitted interface |
|---|---|---:|---:|---|---|
| `SDE-013` | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT` | 52,295 | `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5` | Immutable refs, field-level epistemic assertions, Identity/Context/Resonance/Matrix refs, coarse relationship-stage evidence, canonical serialization, descendant invalidation. |
| `SDE-014` | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md` | `WRITTEN_PENDING_AUDIT` | 74,824 | `ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c` | Activation-hypothesis and portfolio refs, source-kind and interview-provenance rules, diversity signatures, eligibility gates, comparative evaluation, stopping, promotion, replay. |

Both inputs are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their interface detail is not ratified law. A change to either pinned hash reopens sections 3, 5, 6, 8, 9, and 10 of this spec before it may advance.

### Required unique evidence and brownfield sources

| Source | Exact path | SHA-256 | Fact extracted |
|---|---|---|---|
| `SRC-AI2-REL-001` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/schemas/relationship_activation_state.schema.json` | `2829512d2e6aeb4bd695cd5c9f2382d76ac3b16c755c50ab8443fa2aaf7ecc1c` | Defines the historical 12-stage relationship sequence, exact immutable refs, and basic transition fields; it lacks current ownership, evidence, receipts, and epistemic contracts. |
| `SRC-INT-001` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | A Complete Expression Session is the source wrapper; asset delivery is a reciprocity and relationship-deepening mechanism, not proof of response by itself. |
| `SRC-MOE-001` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/MATRIX_OF_EDGING.md` | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Matrix selects pressure; experience Primitives govern delivery; broad signal precedes a sharpened Edge Product. |
| Current schema evidence | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/contracts/schemas/relationship_activation_state.schema.json` | `2829512d2e6aeb4bd695cd5c9f2382d76ac3b16c755c50ab8443fa2aaf7ecc1c` | Byte-identical to the predecessor schema; therefore evidence, not an already-current V2.1 schema. |
| Predecessor models | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/reference_implementation/models.py` | `f392c940349c3c5f9586a359fd8497ce1b8368de1b6654357deb146a686efd97` | Reusable strict-model skeletons exist, but float scores, incomplete lineage, and unversioned F14 semantics require adaptation. |
| Relationship portfolio fixture | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/examples/08_james_relationship_activation_portfolio.json` | `c7df4d047af815790ca2de8694f1b354b4cc9594bb32a4117ce458e3ce41ac53` | Useful migration fixture for selected/rejected candidate history; float confidence and free-text stopping are not canonical V2.1 forms. |
| Studio predecessor | `THE_CMF_STUDIO(2)/CCP V9.1 Expression Capture & Archetype Routing Update.md` | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Preserves Complete Expression Session and asset-routing evidence; it does not make Studio the relationship state owner. |
| `PRM-BUS-007` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-007.yaml` | `12d1aaf5ee3657e7169a4c3daa875e21719b9a83d857cf6a8c66e716484ea360` | Social Media as Relationship; guards against over-familiarity, friend-zone avoidance of offers, and fake authenticity. |
| `EXP-PER-003` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/experience_plane/personalization_identity/EXP-PER-003.yaml` | `449dbbc29dee8421d6c818af18eeaa7597280db39a7672ef99774520efd228a8` | Cumulative Investment; a commitment follows delivered value and cannot be an extractive ask. |
| `EXP-PRG-002` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/experience_plane/progression_replay/EXP-PRG-002.yaml` | `f46d8adb09bebe1a533dc84794c0a35f1dc02a4248d2c363ec5d517d34e9598e` | Progression reveals appropriate next complexity; forbids endless tutorial and invisible future value. |

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

Disconnected comments, DMs, invitations, interviews, deliveries, and offers let a system behave as if every person were at the same trust stage. That produces two correctness failures: a premature ask fabricates readiness and damages trust; an unnecessarily weak ask ignores observed readiness and loses the next meaningful move. Planned asset value may also be misreported as delivered relationship evidence, or a local response may be generalized into a universal formula.

The operator outcome is one inspectable, immutable relationship progression in which every stage, proposed call, smallest commitment, response, ReelCast step, asset delivery, and scoped learning is supported by exact evidence and can be replayed, superseded, or denied.

### Bounded solution

Implement a relationship-domain application service that:

1. consumes exact F02 Context Premise, relationship-stage evidence, Matrix of Edging, and F03 Activation Hypothesis Portfolio refs without re-owning them;
2. adapts the selected relationship hypotheses to the current detailed ReelCast stage;
3. deterministically rejects illegal or overclaiming moves before independent comparison;
4. selects the smallest useful commitment under explicit Primitive and evidence constraints;
5. records each ReelCast state transition and its own receipt;
6. admits delivery, response, use, and operator interpretation as different evidence kinds;
7. emits scoped relationship-learning candidates that cannot influence future calls outside their applicability envelope; and
8. commits artifacts, dependency edges, command records, events, and receipts atomically.

### In scope

- AIR-FR-079 through AIR-FR-084 and AIR-ST-14.01 through AIR-ST-14.03;
- the six F14 canonical contract surfaces plus a scoped learning candidate;
- deterministic stage legality, idempotency, optimistic concurrency, immutable versions, canonical hashing, replay, supersession, and descendant invalidation;
- source-kind preservation and interview-provenance validation when supplied;
- typed interfaces to F02/F03, Interview Expression, Independent Evaluation, Studio HumanResolution, and downstream F15;
- lossless-or-blocked migration of the V2 relationship schema and fixtures;
- explicit Primitive activation, suppression, misuse, and coalition evidence.

### Out of scope and non-goals

- conducting the live interview, owning Reaction Receipts, resolving Expression Moments, or creating a Canonical Interview Source Package;
- generating a Final Script, composition, visual demand, rendered asset, production acceptance, or publication decision;
- treating the relationship operator, Studio, Pipeline, VAE, Delegation, or a model as the owner of AIR semantic lifecycle state;
- turning `PRM-BUS-007` into generic funnel automation or turning `EXP-PER-003` into lock-in behavior;
- inventing source classification, relationship history, response, use, approval, trust, identity, Voice DNA, or audience evidence;
- activating Format 02, VAE Stage 5, build work, production, certification, or a Development Capsule;
- changing TS-AIR-002 or TS-AIR-003 or representing either draft as accepted.

## 3. Governing decisions and constraints

### Product sovereignty and object ownership

1. AIR owns the semantic relationship lifecycle, relationship hypotheses adaptation, calls, progression program, and scoped-learning candidates.
2. The authorized relationship operator owns attributable choice, approval, rejection, and interpretation. Human authority is represented by exact `AuthorityRef` and `HumanResolutionEpisode` refs, never by a boolean alone.
3. Interview Expression owns live source activation, Reaction Observations and Receipts, Expression Moment resolution, Complete Expression Session evidence, and the Canonical Interview Source Package. AIR validates and references these objects but cannot manufacture or amend them.
4. Independent Evaluation owns evaluation receipts. A call compiler, selector, or relationship service cannot approve itself.
5. Studio is a projection and typed command surface. It may capture a `HumanResolutionEpisode`; it cannot mutate canonical relationship state directly.
6. Pipeline, VAE, and Delegation have no semantic repair authority here. Delegation transports an immutable message; it does not reinterpret the relationship.
7. F15 may consume an eligible F14 terminal ref and may reject it from its public receipts. It cannot silently repair it.

### Semantic and evidence laws

- Relationship, source, and audience activation remain distinct domains, even when they share Identity DNA, Context Premise, Matrix, or evidence refs.
- F02's coarse `RelationshipStage` is an epistemic assertion about relationship context. F14's detailed `ReelCastStage` is a transition state machine. They are related by an explicit mapping and are not aliases.
- Source kind is the exact shared closed `SourceKind` contract. Unknown or ambiguous source kind is rejected; migration cannot guess it.
- For `interview_expression`, at least one nonempty Reaction Receipt ref and at least one nonempty Expression Moment ref are required by the shared provenance contract. For other source kinds these refs are optional but validated when present.
- Planned value, planned delivery, attempted delivery, successful delivery, recipient response, demonstrated use, and operator interpretation are separate evidence types. None implies the next.
- An inferred readiness assertion cannot outrank observed or operator-confirmed evidence. A high score cannot compensate for missing required evidence or an illegal stage transition.
- The Matrix supplies evidence-backed tension sites and Edge Product candidates. Relationship call selection cannot start from topic similarity or invent a new Matrix.
- A candidate portfolio remains plural until a typed stopping receipt exists. Rejected, repaired, and superseded candidates remain replayable.
- Every wrong-reading lock inherited from source, Matrix, hypothesis, and relationship context is preserved. This feature may add stricter relationship locks; it may not weaken inherited locks.

### Primitive application and misuse prevention

| Primitive | Local job | Activation / suppression law | Non-compensable misuse denial |
|---|---|---|---|
| `PRM-BUS-007` | Require each move to advance, clarify, protect, or truthfully conclude a relationship rather than optimize a broadcast metric. | Apply to ongoing social or direct relationship work; suppress when the current operation is a non-relationship static reference or explicitly governed cold campaign. | Reject over-familiarity, fake intimacy, scripted vulnerability, and endless friendliness that avoids an evidenced offer. |
| `EXP-PER-003` | Permit the smallest durable commitment only after a real reward or value-bearing event and when cognitive load is appropriate. | The triggering reward/delivered-value ref is mandatory when this Primitive is active; suppress during high-friction work or immediately after failure/shame. | Reject pre-reward extraction, invisible stored value, and worthless labor. |
| `EXP-PRG-002` | Make the next ReelCast step visible and stage-appropriate while preserving later stages as discoverable. | Advance only on exact completion evidence; do not expose an advanced state as complete early. | Reject premature advanced asks, endless onboarding, and hiding all future value. |

When multiple Primitives are active, the relationship program records their exact bindings, order, conflicts, suppression decisions, `CoalitionSignature` ref, `EdgeProduct` ref, and `PrimitiveMisuseRisk` evaluation. A list of IDs is not a coalition.

### Claim ceiling and prohibited behavior

The maximum current state is `WRITTEN_PENDING_AUDIT`; before ratification the maximum later state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. `ACCEPTED_FOR_BUILD`, implementation authorization, a Development Capsule, production authority, certification, and VAE Stage 5 are forbidden. Deterministic local tests could later prove only structural and synthetic behavior; they cannot prove real relationship effectiveness or production readiness.

### Draft-dependency caveat and revision impact

TS-AIR-002 and TS-AIR-003 are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. This spec adopts their exact pinned interface shapes only for specification writing. If either hash changes, the following sections are reopened: `governing_decisions`, `proposed_architecture_and_workflows`, `data_models_contracts_schemas_and_apis`, `failure_migration_rollback_recovery_observability`, `acceptance_criteria`, and `testing_and_completion_evidence`.

## 4. Current brownfield architecture

The intended AIR repository currently contains specification documents only; no `src/`, tests, migrations, repository implementation, or released F14 schema exists under `04_ACTIVATIVE_INTELLIGENCE_RUNTIME`. Therefore every runtime path in sections 7 and 10 is prospective and requires later ratification, independent acceptance, and a Development Capsule.

| Exact brownfield source | Actual behavior | Disposition | Reason and migration constraint |
|---|---|---|---|
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/schemas/relationship_activation_state.schema.json` | Strict object with a historical 12-stage enum, source refs, last-call/reaction refs, next transitions, smallest commitment, and locks. | `ADAPT` | Preserve historical field meanings and stage evidence; add semantic version, ownership, epistemic assertions, receipts, concurrency, dependency edges, and current F14 stages. Never treat defaults as evidence. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/reference_implementation/models.py::RelationshipActivationState` | Pydantic-style strict model for historical stages; no immutable object envelope, command history, or stage receipts. | `ADAPT` | Reuse strict validation pattern only. Replace float scoring and incomplete lineage with current typed contracts. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/reference_implementation/models.py::ActivationHypothesisPortfolio` | Validates candidate IDs and selection existence but uses embedded candidates, floats, and free-text stop reason. | `ADAPT` | Consume the exact F03 portfolio by ref; migrate the fixture losslessly or block. Do not create a second F03 portfolio authority. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/reference_implementation/models.py::ActivativeCall` | Holds domain, state, source, premise, edge, roles, pressure, call text, commitment, and locks. | `ADAPT` | Split semantic call, delivery attempt, reaction evidence, and acceptance receipts. Preserve text lineage and pressure ceiling. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/examples/08_james_relationship_activation_portfolio.json` | Two relationship candidates and one selected route with float confidence. | `ACTIVATE` | Use as a migration/negative fixture. Integer-micro conversion is allowed only by an explicit numeric migration policy; original bytes/hash stay linked. |
| `THE_CMF_STUDIO(2)/CCP V9.1 Expression Capture & Archetype Routing Update.md` | Establishes Complete Expression Session quality and derivative routing evidence. | `REUSE` as evidence | Interview Expression owns session and source objects. AIR consumes their refs; Studio does not inherit ownership. |
| Prior TS-AIR-014 draft | Provides feature boundaries, object names, tasks, and basic acceptance. | `ADAPT` | Retain controlling intent; replace generic envelopes, duplicated authority, and non-exhaustive failure behavior with this implementation-grade contract. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | Defines F02 refs, epistemic assertions, coarse relationship stage, deterministic serialization, and invalidation semantics. | `REUSE` as pinned draft interface | Must remain hash-pinned and labeled non-accepted until audit/ratification. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md` | Defines candidate, portfolio, comparative evaluation, stopping, and promotion interfaces. | `REUSE` as pinned draft interface | F14 uses refs and relationship-specific evaluation overlays; it does not duplicate F03 search. |

There is no current implementation to describe as production behavior. Historical schemas and source bundles are evidence, not active release bytes or proof of runtime readiness.

## 5. Proposed architecture and workflows

### Components and responsibilities

1. `RelationshipActivationApplicationService` authenticates commands, resolves exact prior state, enforces optimistic concurrency, coordinates deterministic policies, and commits one transaction.
2. `RelationshipEvidenceResolver` loads source messages, F02 context, Matrix evidence, delivery evidence, Interview Expression refs, and HumanResolution refs by immutable identity. It cannot infer missing classifications.
3. `RelationshipStagePolicy` validates the detailed `ReelCastStage` transition graph and coarse F02 stage consistency.
4. `RelationshipHypothesisAdapter` consumes one exact F03 portfolio and emits relationship-stage eligibility results. It cannot add a hypothesis that is absent from F03.
5. `SmallestCommitmentSelector` applies stage, evidence, pressure, Primitive, effort, and reversibility constraints before independent evaluation.
6. `ReelCastProgressionCompiler` produces an ordered program of distinct steps and required receipts. It never marks a step complete from intent alone.
7. `DeliveryEvidenceResolver` separates planned, attempted, delivered, responded-to, used, and interpreted evidence.
8. `RelationshipLearningCompiler` emits scoped candidates with explicit applicability and promotion gates. It cannot update a global model or rule.
9. `RelationshipEvaluationPort` submits eligible candidates to an evaluator whose binding identity differs from every producing binding.
10. `RelationshipRepository` stores immutable artifacts, commands, events, dependency edges, receipts, and idempotency records atomically.
11. `InterviewExpressionRelationshipPort` reads or transports Interview-owned refs; it cannot write them.
12. `RelationshipProjectionPort` publishes reconstructable Studio projections and accepts only typed, attributable operator commands.

### Detailed transition graph

The current F14 `ReelCastStage` values are:

`UNOBSERVED`, `OBSERVED`, `PUBLICLY_RECOGNIZED`, `REPLIED`, `IDEA_ELEVATED`, `MICRO_COMMITTED`, `REELCAST_PROPOSED`, `INTERVIEW_BRIEF_ACCEPTED`, `SCHEDULED`, `COMPLETE_EXPRESSION_SESSION_COMPLETED`, `ASSET_PACKAGE_READY`, `ASSET_DELIVERED`, `OFFER_REVEALED`, `CLIENT`.

The policy is versioned. Its minimum legal forward edges are:

```text
UNOBSERVED -> OBSERVED
OBSERVED -> PUBLICLY_RECOGNIZED | REPLIED
PUBLICLY_RECOGNIZED -> REPLIED
REPLIED -> IDEA_ELEVATED | MICRO_COMMITTED | OFFER_REVEALED
IDEA_ELEVATED -> MICRO_COMMITTED | REELCAST_PROPOSED | OFFER_REVEALED
MICRO_COMMITTED -> REELCAST_PROPOSED | OFFER_REVEALED
REELCAST_PROPOSED -> INTERVIEW_BRIEF_ACCEPTED
INTERVIEW_BRIEF_ACCEPTED -> SCHEDULED
SCHEDULED -> COMPLETE_EXPRESSION_SESSION_COMPLETED
COMPLETE_EXPRESSION_SESSION_COMPLETED -> ASSET_PACKAGE_READY
ASSET_PACKAGE_READY -> ASSET_DELIVERED
ASSET_DELIVERED -> OFFER_REVEALED
OFFER_REVEALED -> CLIENT
```

An apparent skip is legal only when the pinned policy lists the edge and the command supplies the evidence/authority required for every semantic distinction skipped. `RESET`, `PAUSE`, `DECLINE`, and `CANCEL` are outcomes with receipts, not fabricated forward stages. A decline may leave the current state unchanged while adding evidence. Rollback never moves canonical history backward; it creates a successor state whose current stage is justified by a new resolution.

### Workflow A — establish or update relationship state (AIR-FR-079)

1. Accept `RecordRelationshipEvidenceCommand` with `command_id`, `idempotency_key`, `expected_state_ref`, subject, exact source kind, evidence refs, actor, authority, and transition intent.
2. Resolve the exact current state and F02 Context Premise. Reject stale refs, ambiguous source kind, or a coarse-stage assertion unsupported by evidence.
3. Validate interview provenance when `source_kind=interview_expression`; preserve but do not re-own Reaction Receipt and Expression Moment refs.
4. Normalize each material assertion into `EpistemicAssertion`: stage, recognition, unresolved tension, commitment, delivered value, evidence limitation, and any operator interpretation.
5. Compute the legal transition set from the pinned policy, never from model output.
6. Commit the successor state, dependency edges, event, command record, and `RelationshipReceipt` atomically. An identical idempotency replay returns the original receipt; a different payload under the same key fails.

### Workflow B — adapt and compare relationship hypotheses (AIR-FR-080)

1. Accept `CompileRelationshipHypothesesCommand` pinned to current F14 state, F02 Context/Matrix refs, and one F03 `ActivationHypothesisPortfolio`.
2. Verify the portfolio remains current, contains relationship-domain candidates, has required source provenance, and has not been invalidated.
3. Produce one `RelationshipCandidateAssessment` per candidate for the closed move kinds `RECOGNITION`, `MIRRORING`, `DIRECT_CLOSE`, `MICRO_COMMITMENT`, `INVITATION`, `INTERVIEW`, `ASSET_DELIVERY`, or `RESET`.
4. Apply hard gates: source/authority, current stage, coarse/detailed-stage consistency, pressure ceiling, inherited locks, Primitive activation/suppression/misuse, delivery-evidence kind, and downstream eligibility.
5. Submit two or more eligible assessments to independent comparative evaluation. If fewer than two survive, emit `INSUFFICIENT_COMPARABLE_CANDIDATES` unless the pinned policy explicitly permits a deterministic single legal move with evidence.
6. Preserve all assessments and rejection reasons. Selection requires an F03 stopping receipt and an F14 stage-fit receipt.

### Workflow C — choose the smallest useful commitment and call (AIR-FR-081)

1. For each eligible candidate, compile a `MicroCommitment` whose effort, reversibility, evidence yield, pressure dose, and next-state value are explicit.
2. If `EXP-PER-003` is active, require a real `delivered_reward_ref` before asking for durable investment and suppress the ask during high-friction or shame/failure state.
3. Compare commitments by the pinned policy. “Smallest” means the lowest authorized burden that creates specified meaningful evidence or unlocks the next valid state; it does not mean the shortest text.
4. Compile a `RelationshipActivativeCall` from one selected hypothesis/commitment, preserving source, Matrix/Edge, psychological role/tension where applicable, call-text lineage, intended response, pressure ceiling, and locks.
5. Require independent evaluation and attributable operator authorization where the policy says the call may create a material commitment or offer. Delivery of the call is an external attempt receipt and does not imply response.

### Workflow D — compile and advance ReelCast progression (AIR-FR-082)

1. Compile `ReelCastProgressionProgram` from the current state and exact eligible route.
2. Materialize distinct required steps for public recognition/comment, reply or DM, micro-commitment, Interview Brief, scheduling, Complete Expression Session, Asset Package, delivery, and next offer when those steps apply.
3. Each step declares its owner, entry evidence, completion evidence, allowed successors, timeout/cancellation behavior, and receipt kind.
4. `AdvanceReelCastStageCommand` names exactly one expected stage and target stage. The service validates both and appends one successor version; it cannot bulk-mark steps complete.
5. Interview-owned milestones require exact Interview Expression refs. Missing evidence blocks rather than producing placeholder IDs.

### Workflow E — record delivery and scoped learning (AIR-FR-083 and AIR-FR-084)

1. `RecordAssetDeliveryEvidenceCommand` accepts exact asset/package, recipient, delivery attempt, delivery acknowledgement, and channel refs. Only a successful delivery receipt may support `ASSET_DELIVERED`.
2. Response and demonstrated use are later evidence events. No response is represented as unknown, not rejection or approval.
3. Operator interpretation enters through `ApplyRelationshipResolutionCommand`, produces a HumanResolutionEpisode ref, and creates a successor state; a Studio projection never writes hidden state.
4. `CompileRelationshipLearningCandidateCommand` binds evidence to person, audience, stage, platform, interaction type, validity window, exclusions, and confidence in integer micros.
5. Learned/model-derived candidates also require model/harness version, dataset and evaluator lineage, baseline comparison, shadow result, fallback, rollback, and applicability envelope.
6. Retrieval may return the candidate only when every applicability dimension matches. Promotion to a rule, recipe, dataset, or model is a separate governed release path.

### Atomicity, idempotency, concurrency, cancellation, and replay

- One write transaction contains the immutable artifact, typed dependency edges, event, command record, idempotency record, and receipt. All succeed or none become visible.
- `expected_state_ref` provides optimistic concurrency. A stale command fails without partial state.
- `idempotency_key` is scoped by aggregate and command kind. Same key plus same canonical input hash returns the original result; same key plus different hash yields `AIR_F14_IDEMPOTENCY_CONFLICT`.
- Cancellation is accepted only before the terminal commit. A late provider or evaluator result is stored as orphan/late evidence and cannot advance state automatically.
- Replay resolves exact versions and policy/evaluator bindings. It never consults current time, environment, filesystem ordering, or mutable “latest” aliases.

## 6. Data models, contracts, schemas, and APIs

All contracts are immutable, reject unknown fields, use closed enums and typed tagged unions, require nonempty identifiers, and prohibit `Any`, open dictionaries, implied defaults, mutable default containers, and unversioned owner strings. Shared `ImmutableRef`, `AuthorityRef`, `ActorRef`, `EvidenceRef`, `EpistemicAssertion<T>`, `SemanticObjectVersion`, source-kind, and interview-provenance shapes are reused from the exact pinned upstream draft chain; this dependency remains revision-sensitive.

### Shared scalars and enums

- `Sha256`: lowercase `[a-f0-9]{64}`.
- `NonEmptyText`: normalized Unicode, 1–16,384 characters, no NUL.
- `UtcInstant`: RFC 3339 UTC supplied by a trusted command boundary; excluded from semantic-ID derivation unless the governed contract explicitly makes time semantic.
- `Micros`: integer `0..1_000_000`; floats are rejected.
- `SourceKind`: the shared closed source discriminator; F14 may not fork or extend it locally.
- `EpistemicState`: `PLANNED | OBSERVED | INFERRED | OPERATOR_CONFIRMED | REJECTED | SUPERSEDED`.
- `RelationshipLifecycleState`: `DRAFT | EVALUATED | ELIGIBLE | ACTIVE | BLOCKED | SUPERSEDED | INVALIDATED | CANCELLED`.
- `RelationshipMoveKind`: `RECOGNITION | MIRRORING | DIRECT_CLOSE | MICRO_COMMITMENT | INVITATION | INTERVIEW | ASSET_DELIVERY | RESET`.
- `RelationshipEvidenceKind`: `SOURCE_MESSAGE | PUBLIC_RECOGNITION | DIRECT_REPLY | COMMITMENT | INTERVIEW_BRIEF | SESSION_COMPLETION | ASSET_PACKAGE | DELIVERY_ATTEMPT | DELIVERY_ACKNOWLEDGEMENT | RECIPIENT_RESPONSE | DEMONSTRATED_USE | OPERATOR_INTERPRETATION | DECLINE | CANCELLATION`.

### `RelationshipActivationState` — `ca.air.relationship-activation-state/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `object_version` | `SemanticObjectVersion` | AIR; immutable identity, version, hash, lifecycle, owner, producer, authority. |
| `subject_ref` | `ImmutableRef` | Human/source authority; nonempty exact person/prospect identity. |
| `source_kind` | `SourceKind` | Source owner; mandatory, known, never guessed. |
| `interview_provenance` | `InterviewProvenance?` | Interview Expression; required for `interview_expression`, otherwise optional and validated when present. |
| `context_premise_ref` | `ImmutableRef` | AIR F02; exact current eligible premise. |
| `matrix_of_edging_ref` | `ImmutableRef` | AIR F02; exact current Matrix version. |
| `coarse_relationship_stage` | `EpistemicAssertion<RelationshipStage>` | AIR F02; evidence-bearing context assertion. |
| `reelcast_stage` | `ReelCastStage` | AIR F14; one closed detailed stage. |
| `progression_policy_ref` | `ImmutableRef` | Program Control/AIR; exact transition policy. |
| `prior_interaction_refs` | `tuple<EvidenceRef,0..n>` | Evidence owners; stable sorted by `(occurred_at, evidence_id, sha256)`. |
| `recognition_assertions` | `tuple<EpistemicAssertion<NonEmptyText>,0..n>` | AIR compiles; observed/confirmed claims require evidence. |
| `unresolved_tension_refs` | `tuple<ImmutableRef,0..n>` | AIR F02 Matrix; cannot be free-text substitutes. |
| `commitment_refs` | `tuple<ImmutableRef,0..n>` | AIR F14; exact accepted/declined commitments. |
| `delivered_value_assertions` | `tuple<EpistemicAssertion<DeliveredValue>,0..n>` | AIR compiles; delivery must use delivery evidence, not plan refs. |
| `evidence_limitations` | `tuple<EvidenceLimitation,0..n>` | Evidence owner/AIR; each has code, scope, consequence, and missing refs. |
| `current_portfolio_ref` | `ImmutableRef?` | AIR F14; absent before compilation. |
| `current_call_ref` | `ImmutableRef?` | AIR F14; absent before selection. |
| `current_program_ref` | `ImmutableRef?` | AIR F14; absent before ReelCast compilation. |
| `last_relationship_receipt_ref` | `ImmutableRef?` | AIR F14; exact latest event receipt for this version. |
| `inherited_wrong_reading_lock_refs` | `tuple<ImmutableRef,1..n>` | Upstream owner; preserved and stable-sorted. |
| `added_wrong_reading_lock_refs` | `tuple<ImmutableRef,0..n>` | AIR/operator-authorized; may only strengthen. |
| `next_allowed_stages` | `tuple<ReelCastStage,0..n>` | AIR derived deterministically from stage and policy; canonical sorted enum order. |
| `supersedes_ref` | `ImmutableRef?` | AIR; required after version 1. |

`DeliveredValue` is a closed record: `{asset_or_service_ref, delivery_attempt_ref, delivery_acknowledgement_ref, recipient_response_ref?, demonstrated_use_ref?, operator_interpretation_ref?}`. Presence of a later field never rewrites an earlier one.

### `RelationshipHypothesisPortfolio` — `ca.air.relationship-hypothesis-portfolio/2.1.0-candidate`

This object does not duplicate the F03 portfolio. It is an F14 stage-fit overlay.

| Field | Type | Owner and validation |
|---|---|---|
| `object_version` | `SemanticObjectVersion` | AIR F14. |
| `relationship_state_ref` | `ImmutableRef` | AIR F14; current and eligible. |
| `base_activation_portfolio_ref` | `ImmutableRef` | AIR F03; exact pinned portfolio. |
| `candidate_assessment_refs` | `tuple<ImmutableRef,1..n>` | AIR F14; one per F03 candidate, no omissions. |
| `move_kinds_compared` | `tuple<RelationshipMoveKind,1..8>` | AIR; unique canonical enum order. |
| `hard_gate_result_refs` | `tuple<ImmutableRef,1..n>` | Independent/deterministic evaluators; complete before evaluation. |
| `comparative_evaluation_ref` | `ImmutableRef?` | Independent Evaluation; required after `EVALUATED`. |
| `selected_candidate_ref` | `ImmutableRef?` | AIR F03 candidate; requires both F03 stop and F14 stage-fit pass. |
| `selected_commitment_ref` | `ImmutableRef?` | AIR F14; required when selection asks for an action. |
| `stopping_receipt_ref` | `ImmutableRef?` | AIR F03/F14 combined stopping evidence. |
| `rejected_assessment_refs` | `tuple<ImmutableRef,0..n>` | AIR; immutable reasons remain retrievable. |
| `supersedes_ref` | `ImmutableRef?` | AIR. |

`RelationshipCandidateAssessment` contains `candidate_ref`, `relationship_state_ref`, `move_kind`, `coarse_stage_fit`, `detailed_stage_fit`, `pressure_fit`, `evidence_fit`, `primitive_binding_refs`, `primitive_misuse_risk_refs`, `lock_refs`, `eligible`, and closed `reason_codes`. It contains no model-written free-form verdict as an authority field.

### `MicroCommitment` — `ca.air.micro-commitment/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `object_version` | `SemanticObjectVersion` | AIR F14. |
| `relationship_state_ref` | `ImmutableRef` | AIR F14. |
| `candidate_assessment_ref` | `ImmutableRef` | AIR F14; must be eligible. |
| `action_kind` | `REPLY | NAME_ONE_EXAMPLE | CONFIRM_INTEREST | ACCEPT_BRIEF | SCHEDULE | ATTEND_SESSION | ACKNOWLEDGE_DELIVERY | REVIEW_ASSET | CONSIDER_OFFER | CUSTOM` | AIR policy; `CUSTOM` requires a governed kind registry ref. |
| `action_description` | `NonEmptyText` | AIR semantic program; source/call lineage required. |
| `effort_class` | `TRIVIAL | LOW | MODERATE | HIGH` | AIR policy. |
| `reversibility` | `FULL | PARTIAL | IRREVERSIBLE` | AIR policy; irreversible asks require operator authorization. |
| `meaningful_evidence_kind` | `RelationshipEvidenceKind` | AIR policy; exact expected evidence. |
| `next_stage_if_completed` | `ReelCastStage?` | AIR policy; null when the action gathers evidence without stage advance. |
| `pressure_dose` | `integer 0..5` | AIR; cannot exceed candidate or state ceiling. |
| `delivered_reward_ref` | `ImmutableRef?` | Evidence owner; mandatory when `EXP-PER-003` is active. |
| `primitive_binding_refs` | `tuple<ImmutableRef,1..n>` | AIR exact registry bindings. |
| `suppression_reason_codes` | `tuple<CommitmentSuppressionCode,0..n>` | AIR; if nonempty the commitment is ineligible. |
| `operator_authorization_ref` | `ImmutableRef?` | Human authority; mandatory for policy-declared material asks. |

### `RelationshipActivativeCall` — `ca.air.relationship-activative-call/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `object_version` | `SemanticObjectVersion` | AIR owns semantic program. |
| `relationship_state_ref` | `ImmutableRef` | AIR F14 current version. |
| `selected_hypothesis_ref` | `ImmutableRef` | AIR F03 exact candidate. |
| `selected_commitment_ref` | `ImmutableRef?` | AIR F14; required for commitment-bearing calls. |
| `move_kind` | `RelationshipMoveKind` | AIR F14. |
| `recognized_premise` | `EpistemicAssertion<NonEmptyText>` | AIR; must not overclaim fact. |
| `edge_product_ref` | `ImmutableRef` | AIR F02. |
| `psychological_role` | `NonEmptyText?` | AIR; required when the call makes an audience-role claim. |
| `tension_ref` | `ImmutableRef` | AIR F02 Matrix. |
| `call_text` | `NonEmptyText` | AIR; transformation/source lineage below is mandatory. |
| `call_text_lineage` | `tuple<TextSpanLineage,1..n>` | Source/AIR; labels `VERBATIM | CONDENSED | ADAPTED | AUTHORED`. |
| `intended_response_kind` | `RelationshipEvidenceKind` | AIR policy. |
| `pressure_dose` | `integer 0..5` | AIR; bounded. |
| `primitive_binding_refs` | `tuple<ImmutableRef,1..n>` | AIR. |
| `wrong_reading_lock_refs` | `tuple<ImmutableRef,1..n>` | Upstream/AIR; inherited set is a subset. |
| `evaluation_receipt_ref` | `ImmutableRef` | Independent Evaluation; producer identity differs. |
| `operator_authorization_ref` | `ImmutableRef?` | Human authority when policy requires. |

Sending or showing the call creates a separate `CallDeliveryAttempt` receipt. A compiled or sent call is not a response and cannot advance relationship stage by itself.

### `ReelCastProgressionProgram` — `ca.air.reelcast-progression-program/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `object_version` | `SemanticObjectVersion` | AIR F14. |
| `relationship_state_ref` | `ImmutableRef` | AIR F14 start version. |
| `transition_policy_ref` | `ImmutableRef` | AIR/Program Control. |
| `ordered_step_refs` | `tuple<ImmutableRef,1..n>` | AIR; topologically ordered and unique. |
| `current_step_ref` | `ImmutableRef?` | AIR; absent after terminal/cancelled. |
| `required_interview_contract_refs` | `tuple<ImmutableRef,0..n>` | AIR planned contracts; do not imply execution. |
| `primitive_coalition_contract_ref` | `ImmutableRef` | AIR; exact bindings/order/conflicts/signature/Edge Product. |
| `pause_reset_cancel_policy_ref` | `ImmutableRef` | AIR; exact behavior. |
| `downstream_f15_eligibility_contract_ref` | `ImmutableRef` | AIR; public denial surface. |
| `evaluation_receipt_ref` | `ImmutableRef` | Independent Evaluation. |
| `supersedes_ref` | `ImmutableRef?` | AIR. |

Each `ReelCastProgressionStep` has `step_id`, `stage_from`, `stage_to`, `owner_product`, `entry_evidence_kinds`, `required_input_refs`, `completion_evidence_kind`, `completion_receipt_ref?`, `allowed_next_step_refs`, `timeout_policy_ref`, and `status` (`PENDING | ELIGIBLE | ACTIVE | COMPLETED | DECLINED | CANCELLED | INVALIDATED`). Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer are never collapsed into one step or receipt.

### `RelationshipReceipt` and scoped learning

`RelationshipReceipt` — `ca.air.relationship-receipt/2.1.0-candidate` — is a tagged union with kinds `STATE_RECORDED`, `HYPOTHESES_COMPILED`, `CALL_SELECTED`, `CALL_DELIVERY_ATTEMPTED`, `COMMITMENT_COMPLETED`, `STAGE_ADVANCED`, `DELIVERY_RECORDED`, `RESPONSE_RECORDED`, `LEARNING_CAPTURED`, `BLOCKED`, `CANCELLED`, `INVALIDATED`, `SUPERSEDED`, and `REPLAYED`. Every variant includes `receipt_version`, `command_ref`, `prior_state_ref?`, `result_state_ref?`, `input_refs`, `actor_ref`, `authority_ref`, `policy_refs`, `result_code`, `reason_codes`, `dependency_edge_refs`, and `content_sha256`. A successful variant cannot contain a failed mandatory gate.

`RelationshipLearningCandidate` — `ca.air.relationship-learning-candidate/2.1.0-candidate` — includes `object_version`, `learning_assertion`, `epistemic_state`, `evidence_refs`, `person_scope_ref`, `audience_scope_ref`, `stage_scope`, `platform_scope`, `interaction_type_scope`, `valid_from`, `valid_until?`, `exclusion_scopes`, `confidence_micros`, `model_or_deterministic_binding_ref`, `dataset_lineage_refs`, `evaluation_receipt_ref`, `baseline_comparison_ref`, `shadow_result_ref`, `fallback_ref`, `rollback_ref`, `promotion_state` (`CANDIDATE_ONLY | APPROVED_SCOPED | REJECTED | SUPERSEDED`), and `human_resolution_ref?`. It cannot be retrieved as an approved rule while `CANDIDATE_ONLY`.

### Commands, events, and repository interfaces

Every command includes `command_id`, `idempotency_key`, `expected_state_ref?`, `actor_ref`, `authority_ref`, `requested_at`, `input_refs`, `policy_refs`, and a typed payload. Commands are:

- `RecordRelationshipEvidenceCommand`;
- `CompileRelationshipHypothesesCommand`;
- `SelectMicroCommitmentCommand`;
- `CompileRelationshipCallCommand`;
- `RecordCallDeliveryAttemptCommand`;
- `AdvanceReelCastStageCommand`;
- `RecordAssetDeliveryEvidenceCommand`;
- `ApplyRelationshipResolutionCommand`;
- `CompileRelationshipLearningCandidateCommand`;
- `SupersedeRelationshipStateCommand`;
- `InvalidateRelationshipDescendantsCommand`;
- `CancelRelationshipProgramCommand`;
- `ReplayRelationshipStateCommand`.

Events mirror completed command semantics and never carry untyped payloads. The repository port is:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_state(subject_ref: ImmutableRef, state_ref: ImmutableRef) -> RelationshipActivationState
lookup_idempotency(aggregate_id: NonEmptyText, command_kind: CommandKind, key: NonEmptyText) -> IdempotencyRecord | null
commit(transaction: RelationshipCommitBundle, expected_prior_ref: ImmutableRef | null) -> RelationshipReceipt
list_descendants(root_ref: ImmutableRef, edge_types: tuple<RelationshipEdgeType, ...>) -> tuple<ImmutableRef, ...>
read_events(aggregate_id: NonEmptyText, through_version: PositiveInteger) -> tuple<RelationshipEvent, ...>
```

`RelationshipCommitBundle` is closed and contains exactly one command record, zero or one new primary artifact, zero or more supporting artifacts, one or more events, all dependency edges, one idempotency record, and one receipt. The repository validates that every stored state has its receipt and every success receipt resolves its artifacts.

### Canonical serialization, hashing, compatibility, and examples

Canonical bytes are UTF-8 JSON with normalized strings, lexicographically sorted object keys, closed enum values, integers only, and arrays sorted only where the field contract declares set semantics. Ordered progression steps and interaction history preserve semantic order. Hashes and IDs exclude absolute paths, environment variables, current time, random state, process IDs, machine names, and filesystem traversal order. `content_sha256 = SHA-256(canonical_payload_without_content_sha256)`. Semantic IDs are derived from schema ID, owner, aggregate ID, version, and content hash; externally supplied evidence IDs are preserved as refs.

Positive example:

```yaml
schema_id: ca.air.relationship-activation-state/2.1.0-candidate
subject_ref: {object_id: person-james, version: 1, sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}
source_kind: direct_message_reply
reelcast_stage: REPLIED
context_premise_ref: {object_id: context-james, version: 3, sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb}
matrix_of_edging_ref: {object_id: matrix-james, version: 2, sha256: cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc}
evidence_limitations:
  - {code: NO_INTERVIEW_YET, scope: source_activation, consequence: DO_NOT_CLAIM_EXPRESSION_EVIDENCE, missing_refs: []}
next_allowed_stages: [IDEA_ELEVATED, MICRO_COMMITTED, OFFER_REVEALED]
```

Negative example: a payload with `source_kind: dm_maybe`, `reelcast_stage: ASSET_DELIVERED`, and only an asset-plan ref is rejected with `AIR_F14_UNKNOWN_SOURCE_KIND` and `AIR_F14_DELIVERY_EVIDENCE_MISSING`; no source kind or delivery is inferred.

Compatibility is semantic, not parse-only. A consumer declares required schema IDs, features, source kinds, receipt kinds, stage-policy version, and Primitive support. An adapter may rename or split fields only when it preserves every constraint, evidence ref, lock, owner, and epistemic state. Parse-without-enforcement fails conformance.

## 7. Implementation stages and exact target paths

These are future implementation targets, not authorized changes in this writing prompt.

| Stage / task | Exact future path | FR / Story | Required evidence |
|---|---|---|---|
| 0. Capsule and source lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-014/SOURCE_LOCK.yaml` | all | Only after ratification, independent acceptance, and Capsule authorization; must pin this spec, sources, upstream accepted bytes, and allowlist. |
| 1. Domain models and enums | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/relationship_activation.py` | 079–084 / 14.01–14.03 | Type/unknown-field/immutability/hash tests and schema generation. |
| 1. Shared contract models | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/contracts/relationship_activation.py` | 079–084 | Exact closed commands, events, receipts, evidence, provenance, and compatibility features. |
| 1. Schemas | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/relationship_activation_state.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/relationship_hypothesis_portfolio.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/relationship_activative_call.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/micro_commitment.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/reelcast_progression_program.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/relationship_receipt.schema.json` | 079–084 | Generated from accepted domain types; schema round-trip and negative fixtures. |
| 2. Transition and commitment policies | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/policies/relationship_stage_policy.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/policies/smallest_commitment_policy.py` | 079, 081, 082 / 14.01, 14.02 | Exhaustive transition table, Primitive activation/suppression/misuse, stage/coarse-stage consistency. |
| 3. Application service | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/relationship_activation_service.py` | 079–084 | Command orchestration, hard gates, independent evaluation, typed blockers. |
| 3. Repository port | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/relationship_repository.py` | all | Atomic state/artifact/receipt/command/idempotency/event/edge contract. |
| 4. Independent evaluator adapter | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/relationship_activation_evaluator.py` | 080, 081, 084 | Producer/evaluator identity separation, calibration, baseline, fallback, shadow evidence. |
| 4. Interview Expression port | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/interview_expression_relationship_port.py` | 082, 083 / 14.02, 14.03 | Read-only exact refs; missing provenance/session/package evidence blocks. |
| 4. Studio projection adapter | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/projections/relationship_activation_projection.py` | 083, 084 / 14.03 | Reconstructable projection and typed HumanResolution commands; no hidden writes. |
| 5. V2 migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/relationship_activation_v2_to_v2_1.py` | 079–084 | New immutable artifacts, explicit stage mapping, no guessed source/evidence/owner. |
| 6. Fixtures | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/fixtures/relationship_activation/` | all | Positive, adversarial, stale, contradictory, idempotent, concurrent, migrated, invalidated, and historical replay cases. |
| 6. Unit and contract tests | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/test_relationship_stage_policy.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/test_smallest_commitment_policy.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_relationship_activation_contracts.py` | all | Exhaustive field and policy tests. |
| 6. Integration tests | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_relationship_activation_and_reelcast_progression.py` | all Stories | End-to-end state, hypothesis, call, progression, delivery, learning, replay, invalidation. |
| 6. Architecture tests | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_relationship_product_boundaries.py` | all | AIR cannot import Studio/VAE/provider implementations or write Interview-owned objects. |
| 6. Clean-environment proof | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reproducibility/test_relationship_activation_reproduction.py` | all | Two fresh processes yield byte-identical deterministic outputs from the same frozen inputs. |

Each task requires one later Build Receipt linking exact accepted spec hash, code hashes, tests, fixtures, environment, and claim ceiling. This document does not issue that receipt.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Required behavior |
|---|---|---|
| `AIR_F14_REQUIRED_SOURCE_UNAVAILABLE` | A required source or exact Primitive YAML cannot resolve. | Block before compilation; do not reconstruct. |
| `AIR_F14_UPSTREAM_DRAFT_DRIFT` | TS-AIR-002 or TS-AIR-003 hash differs from the dispatch lock. | Block and reopen the six revision-impact sections. |
| `AIR_F14_UNKNOWN_SOURCE_KIND` | Source kind is absent, unknown, or ambiguous. | Reject; never guess or map by filename. |
| `AIR_F14_INTERVIEW_PROVENANCE_MISSING` | Interview expression lacks Reaction Receipt or Expression Moment refs. | Reject before eligibility. |
| `AIR_F14_STATE_VERSION_CONFLICT` | `expected_state_ref` is not current. | Return current ref; commit nothing. |
| `AIR_F14_IDEMPOTENCY_CONFLICT` | Same key is reused with a different canonical command hash. | Reject and preserve the original receipt. |
| `AIR_F14_ILLEGAL_STAGE_TRANSITION` | Requested edge is absent from the pinned policy or lacks evidence. | Emit blocker; do not advance. |
| `AIR_F14_COARSE_STAGE_CONTRADICTION` | Detailed stage overclaims or contradicts F02 evidence. | Block or require attributable resolution. |
| `AIR_F14_STALE_PORTFOLIO` | F03 portfolio or an upstream evidence ref is invalidated/superseded. | Mark dependent F14 objects stale; prohibit call selection. |
| `AIR_F14_INSUFFICIENT_COMPARABLE_CANDIDATES` | Comparative selection is requested without enough eligible candidates. | Stop or use only an explicitly authorized deterministic single-move rule. |
| `AIR_F14_PRIMITIVE_MISUSE` | A call violates activation/suppression/misuse constraints. | Non-compensable failure; ranking cannot override. |
| `AIR_F14_PRESSURE_CEILING_EXCEEDED` | Call/commitment pressure exceeds evidence or policy. | Reject and preserve candidate evidence. |
| `AIR_F14_EXTRACTIVE_COMMITMENT` | Durable investment is asked before delivered value or during suppression. | Reject with `EXP-PER-003` evidence. |
| `AIR_F14_DELIVERY_EVIDENCE_MISSING` | Planned/attempted delivery is presented as completed delivery. | Keep prior stage; record limitation. |
| `AIR_F14_RESPONSE_FABRICATION` | Missing response/use is inferred from delivery or silence. | Reject assertion; retain `UNKNOWN`. |
| `AIR_F14_SELF_EVALUATION` | Producer and evaluator binding identities match. | Reject evaluation receipt. |
| `AIR_F14_SCOPE_LEAK` | Learning candidate is retrieved/promoted outside applicability. | Deny retrieval/promotion and emit incident receipt. |
| `AIR_F14_ATOMIC_COMMIT_FAILED` | Any artifact, edge, command, event, idempotency, or receipt write fails. | Roll back entire transaction; no partial visibility. |
| `AIR_F14_LATE_RESULT` | Evaluation/provider result arrives after cancel/supersede. | Store as late evidence only; no state advancement. |
| `AIR_F14_REPLAY_DIVERGENCE` | Replayed canonical bytes/hash differ. | Fail evidence gate; preserve both diagnostics, never overwrite history. |

Retries are allowed only for transient transport/storage failures with the same command and idempotency identity. Quality repair creates a new command, new artifact version, explicit predecessor ref, and repair reason; it is not a retry.

### Migration and compatibility

The V2-to-V2.1 adapter produces new immutable artifacts and a migration receipt. The historical stage mapping is exact where evidence permits:

| V2 value | V2.1 target | Additional evidence required |
|---|---|---|
| `unobserved` | `UNOBSERVED` | none beyond subject identity and source classification |
| `observed` | `OBSERVED` | source evidence ref |
| `publicly_recognized` | `PUBLICLY_RECOGNIZED` | public recognition evidence |
| `replied` | `REPLIED` | public or direct reply evidence |
| `idea_elevated` | `IDEA_ELEVATED` | exact elevation evidence |
| `micro_committed` | `MICRO_COMMITTED` | completed commitment receipt |
| `reelcast_proposed` | `REELCAST_PROPOSED` | call delivery attempt and proposal evidence |
| `scheduled` | `SCHEDULED` | accepted brief and scheduling evidence; missing accepted brief blocks |
| `recorded` | `COMPLETE_EXPRESSION_SESSION_COMPLETED` | exact Interview Expression session completion ref; otherwise block |
| `asset_delivered` | `ASSET_DELIVERED` | asset/package plus delivery acknowledgement; otherwise block |
| `offer_revealed` | `OFFER_REVEALED` | exact offer evidence and authority |
| `client` | `CLIENT` | exact accepted commercial relationship evidence |

No V2 value maps automatically to `INTERVIEW_BRIEF_ACCEPTED` or `ASSET_PACKAGE_READY`; these new distinctions require evidence. Missing source kind, owner, Primitive version, epistemic state, stage evidence, or receipt causes `MIGRATION_BLOCKED_MISSING_REQUIRED_FIELD`. The original bytes/hash and legacy ID remain linked. Deprecated schemas remain readable for historical replay and do not become current-write formats.

### Rollback, invalidation, cancellation, and recovery

- Code or policy rollback restores a pinned prior implementation binding for new commands; artifacts produced under the failed binding remain reproducible and may be invalidated by receipt.
- Upstream supersession traverses typed material edges and invalidates only dependent F14 portfolios, calls, commitments, programs, and learning candidates. Unrelated people and interactions remain current.
- A completed delivery or historical response is never erased. Revocation changes current eligibility and produces a receipt; historical reproduction remains possible.
- Cancellation races are decided by repository commit order. If cancellation wins, later results are late evidence. If terminal commit wins, cancellation returns the terminal receipt and cannot rewrite it.
- Recovery replays through the last valid transaction and compares canonical hashes. A state without its receipt, or a receipt without referenced artifacts, is corruption and blocks continuation.

### Observability and operational security

Structured events include `command_id`, `idempotency_key_hash`, `transaction_id`, `aggregate_id`, prior/result refs, policy refs, source kind, coarse/detailed stage, result code, reason codes, evaluator binding ref, dependency counts, duration micros, and correlation ref. Logs carry refs and hashes, not unrestricted DMs, interview text, identity payloads, or secrets.

Metrics include illegal transitions, unsupported stage assertions, source-kind/provenance rejection, extractive-commitment denial, pressure violations, portfolio hard-gate rejection, self-evaluation attempts, delivery/response distinction failures, concurrency conflicts, idempotent replays/conflicts, cancellation races, invalidation fan-out, scope-leak denials, migration blockers, atomic rollbacks, and replay divergence. Metrics are operational evidence, never semantic authority.

Technical access control, tenant isolation, secret handling, retention, and transport security remain mandatory operational concerns. This spec does not create a generic creative-safety or content-rights approver and does not displace operator-supplied source authority, provenance, lineage, approvals, or product sovereignty.

## 9. Behavior-specific acceptance criteria

Each criterion names the controlling requirement, pass condition, concrete failure, evidence, and responsible test layer. These criteria define future verification; they are not executed by this writer.

1. **AIR-FR-079 / AIR-ST-14.01 — evidence-bearing current state.** Given a direct reply and exact F02 refs, when `RecordRelationshipEvidenceCommand` executes against the expected state, then a successor records stage, prior interactions, recognition, unresolved tensions, commitments, delivered-value evidence, and limitations with field-level epistemic states. A state that reports `ASSET_DELIVERED` from an asset plan fails. Evidence: state/command/event/dependency/receipt bundle. Layer: integration and contract.
2. **AIR-FR-079 / AIR-ST-14.01 — stage contradiction denial.** Given F02 says `UNKNOWN` or supplies no readiness evidence, when a high-trust F14 stage is requested, then `AIR_F14_COARSE_STAGE_CONTRADICTION` commits no successor. A model-confidence score cannot make the transition pass. Evidence: blocker receipt and unchanged aggregate hash. Layer: unit and integration.
3. **AIR-FR-080 / AIR-ST-14.01 — diverse relationship moves.** Given a current stage and F03 portfolio with meaningfully different candidates, when F14 adapts it, then recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset are considered only where applicable; each F03 candidate has one assessment and all rejections remain. Dropping a rejected candidate or inventing a new candidate fails. Evidence: F03/F14 cross-reference and assessment set. Layer: contract and integration.
4. **AIR-FR-080 / AIR-ST-14.01 — hard gates precede comparison.** Given one stage-illegal but fluent candidate, when comparison runs, then the hard gate rejects it before scoring. A high aesthetic or confidence score cannot compensate. Evidence: ordered gate/evaluation receipts and evaluator identity. Layer: unit and adversarial integration.
5. **AIR-FR-081 / AIR-ST-14.02 — smallest useful commitment.** Given two legal commitments, when selection runs, then the chosen action is the lowest burden that yields the declared meaningful evidence or unlocks the next valid state under the pinned policy. Choosing the shortest text despite irreversible burden fails. Evidence: policy ref, candidate assessments, comparison receipt, selected commitment. Layer: unit and integration.
6. **AIR-FR-081 / AIR-ST-14.02 — Cumulative Investment timing.** Given no delivered reward or a current shame/high-friction signal, when a durable investment is proposed, then `AIR_F14_EXTRACTIVE_COMMITMENT` blocks it. Asking the recipient to upload/store value before receiving value is the concrete failure. Evidence: Primitive binding, suppression decision, blocker. Layer: Primitive contract and adversarial integration.
7. **AIR-FR-082 / AIR-ST-14.02 — distinct ReelCast states.** Given a route from public recognition to asset delivery, when the program compiles, then public recognition, reply/DM, micro-commitment, Interview Brief, scheduling, Complete Expression Session, Asset Package, delivery, and next offer are distinct applicable steps and receipt kinds. One `recorded_and_delivered` flag fails. Evidence: program and step schemas. Layer: schema/contract.
8. **AIR-FR-082 / AIR-ST-14.02 — no stage skipping.** Given a `REELCAST_PROPOSED` state without an accepted Interview Brief, when `SCHEDULED` is requested, then the transition blocks. A calendar event alone cannot synthesize brief acceptance. Evidence: stage-policy decision and unchanged state. Layer: unit and integration.
9. **AIR-FR-083 / AIR-ST-14.03 — delivery is observed evidence.** Given an asset package and successful delivery acknowledgement, when delivery is recorded, then state may advance to `ASSET_DELIVERED` while response and use remain absent/unknown. Marking the recipient “engaged” from delivery alone fails. Evidence: separate delivery, response, use, and state refs. Layer: integration.
10. **AIR-FR-083 / AIR-ST-14.03 — operator interpretation is attributable.** Given delivery and later response evidence, when the operator interprets its meaning through Studio, then a typed command and HumanResolutionEpisode ref create an additive state successor. Direct UI mutation or an unattributed boolean fails. Evidence: command, HumanResolution ref, before/after refs. Layer: cross-product contract and integration.
11. **AIR-FR-084 / AIR-ST-14.03 — scoped learning.** Given one successful DM-to-interview episode, when learning is compiled, then person, audience, stage, platform, interaction type, validity, exclusions, evidence, and confidence micros are mandatory. Reusing it for another platform or audience without envelope match fails. Evidence: learning candidate and retrieval denial. Layer: unit, retrieval, and integration.
12. **AIR-FR-084 / AIR-ST-14.03 — model evidence ceiling.** Given model-assisted learning, when the candidate is stored, then model/harness version, dataset/evaluation lineage, applicability, baseline, shadow result, fallback, and rollback refs are present and promotion remains separate. Treating a local model result as a current global rule fails. Evidence: candidate and promotion-state receipt. Layer: contract and architecture.
13. **Source-kind and interview provenance.** Given `interview_expression`, when any F14 command validates inputs, then at least one Reaction Receipt and one Expression Moment ref must resolve; given a non-interview kind, those refs are optional but validated if present. Guessing source kind from a transcript path fails. Evidence: positive/negative conformance fixtures. Layer: contract.
14. **Primitive and lock inheritance.** Given upstream locks and active exact Primitive bindings, when a call is compiled, then all locks survive and every activation, suppression, misuse, conflict, signature, and Edge Product decision is recorded. Removing a lock to make a candidate score higher fails. Evidence: lineage diff and Primitive evaluation receipt. Layer: Primitive contract and integration.
15. **Independent evaluation.** Given a producer binding, when its own identity signs the evaluation, then `AIR_F14_SELF_EVALUATION` rejects the result. Separate deployment name with the same governed binding identity still fails. Evidence: producer/evaluator binding refs. Layer: architecture and integration.
16. **Idempotency and concurrency.** Given an identical command/key, replay returns byte-identical original receipt; given the same key/different payload, it fails; given stale expected state, it commits nothing. Duplicate state versions, receipt-only commits, or hidden lost updates fail. Evidence: repository transaction log. Layer: repository integration.
17. **Atomic rollback.** Given injected failure after artifact write but before receipt/edge write, when commit aborts, then none of artifact, state, edge, event, idempotency, or receipt is visible. Any orphan fails. Evidence: fault-injection ledger. Layer: repository integration.
18. **Supersession, invalidation, and replay.** Given an F02/F03 input is superseded, when dependency traversal runs, then only typed descendants become ineligible, historical state remains loadable, and replay under old refs reproduces old hashes. Rewriting or deleting old evidence fails. Evidence: invalidation receipt and dual replay. Layer: integration and reproducibility.
19. **Downstream denial.** Given a terminal F14 program with missing or stale evaluation/evidence, when F15 checks only its public contract and receipts, then it denies eligibility without internal database access. Silent repair or consumption fails. Evidence: producer/consumer conformance receipt. Layer: cross-spec integration.
20. **Claim ceiling.** Given all synthetic tests pass, when completion is reported, then the claim remains implementation-development evidence only and production eligibility/certification remain false until later authorized gates. A test PASS represented as real relationship effectiveness fails. Evidence: Build Receipt claim fields. Layer: completion governance.

## 10. Testing and completion evidence

### Exact future test suites

| Test path | Named coverage |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/test_relationship_stage_policy.py` | every legal/illegal edge; coarse/detailed mapping; skip, pause, decline, cancel, correction, policy version; deterministic ordering. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/test_smallest_commitment_policy.py` | burden/evidence ordering, pressure ceiling, reversibility, EXP-PER-003 timing/suppression/misuse, deterministic ties. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_relationship_activation_contracts.py` | all six schemas, unknown fields, closed enums, source kind, interview provenance, owner/ref/hash validation, positive/negative examples. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_relationship_f02_f03_interfaces.py` | exact F02 Context/Matrix/coarse-stage refs and F03 portfolio/stopping/evaluation refs; no local forks; upstream hash drift denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_relationship_activation_and_reelcast_progression.py` | AC 1–12 and 19, including distinct ReelCast steps, delivery/response/use separation, HumanResolution, scoped learning. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_relationship_repository_atomicity.py` | idempotency, optimistic concurrency, command record, artifact/receipt parity, event/edge parity, fault-injected rollback. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_relationship_invalidation_and_replay.py` | selective descendant invalidation, cancellation race, late results, old-version reproduction, successor replay. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migrations/test_relationship_activation_v2_to_v2_1.py` | every V2 stage mapping, missing-brief/session/package blockers, float policy, original hash preservation, no guessed fields. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_relationship_product_boundaries.py` | no Studio/VAE/provider implementation imports; Interview-owned objects read-only; producer/evaluator separation; AIR semantic ownership. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reproducibility/test_relationship_activation_reproduction.py` | two fresh-process runs with controlled locale/timezone/environment produce identical canonical bytes, IDs, events, and receipts. |

### Fixture matrix

Required fixtures include all shared source kinds; valid and missing interview provenance; every stage and edge; unknown/contradictory coarse stage; each move kind; all three Primitive activation/suppression/misuse cases; inherited-lock weakening; planned, attempted, delivered, responded, used, and interpreted asset evidence; declined/no-response paths; portfolio duplicates and insufficient diversity; stale/superseded inputs; self-evaluation; integer-micro boundaries; same/different idempotency replay; concurrent commands; mid-commit failures at every repository write; cancellation and late results; scoped-learning match/mismatch; complete/incomplete V2 migration; absolute-path/environment/time/random/traversal-order contamination; and downstream F15 denial.

### Required completion evidence

A later authorized implementation must produce:

1. a Development Capsule that pins a ratified/accepted spec hash and exact path allowlist;
2. generated schema hashes plus valid/invalid conformance fixtures;
3. unit, contract, integration, migration, architecture, and affected-regression results;
4. two clean fresh-process deterministic runs with byte/hash comparison;
5. atomic rollback and artifact/receipt/command/edge parity evidence;
6. independent evaluator identity, calibration, baseline, fallback, shadow, and applicability evidence;
7. cross-product Interview Expression and F15 producer/consumer conformance receipts;
8. selective invalidation, historical replay, cancellation, and late-result evidence;
9. source/Primitive/ownership locks and no absolute machine-path leakage; and
10. a governed Build Receipt that states implementation coverage, remaining external proof, production eligibility `false`, and certification `false` unless separately authorized evidence changes those fields.

The writer has issued no audit, revision, re-audit, acceptance, Capsule, build, implementation, release, production, or certification artifact. The next permitted lifecycle step for this exact spec is independent audit by a different agent.
