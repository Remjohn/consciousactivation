---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-017
title: Visual Activation, Composition-Before-Editing, and Production Handoff
product: Activative Intelligence Runtime
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 11
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs: [AIR-FR-097, AIR-FR-098, AIR-FR-099, AIR-FR-100, AIR-FR-101, AIR-FR-102]
controlling_stories: [AIR-ST-17.01, AIR-ST-17.02, AIR-ST-17.03]
upstream_draft_dependencies:
  - {spec_id: TS-AIR-015, quality_state: WRITTEN_PENDING_AUDIT, sha256: 58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {spec_id: TS-AIR-016, quality_state: WRITTEN_PENDING_AUDIT, sha256: 5e4437baff399f65a2b0b63c6f3a43e91145fbd188dbcb503bf67cc09e24cddc, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-AIR-017 - Visual Activation, Composition-Before-Editing, and Production Handoff

This specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`. This document does not make it current, authorize implementation, create schema or release bytes, issue a Development Capsule, authorize VAE Stage 5, or grant build, production, publication, provider, Format 02, evaluator-certification, or product-certification authority.

`TS-AIR-015` and `TS-AIR-016` are hash-pinned upstream drafts in `WRITTEN_PENDING_AUDIT`. Each is `DRAFT_DEPENDENCY_NOT_ACCEPTED`: its public interface is admitted for dependency-safe writing but is not represented as ratified or accepted law. A hash change reopens sections 3, 5, 6, 8, 9, and 10.

## 1. Files and authorities read

### 1.1 Authority, packet, lifecycle, and ownership inputs

| Class | Exact path | State / bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten sections, typed evidence, draft-dependency and claim-ceiling rules. |
| Source-package instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | 1,911; `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Composition follows approved Final Script; models, tools, renderers and external products do not own meaning. |
| Highest current authority | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; 40,830; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Visual semantics, narrative, Feature Contracts, T/V route, BBOX intent and wrong-reading locks precede exact Visual Syntax composition. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION`; 1,288; `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Candidate authority is additive and requires ratification and separate implementation authorization. |
| Candidate Constitution | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`; 51,243; `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | AIR owns temporal semantic programs; approved source, coalition, role/tension, archetype, DNA, Final Script and transfer meaning constrain visual activation. |
| Semantic ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate; 4,263; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns Composition Intent and category-native production-program meaning; Pipeline executes; VAE realizes typed demands without mutation. |
| Product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate; 4,289; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Pipeline owns exact execution and authoritative Visual Asset Demand emission; VAE owns Visual Production Plan, method selection, generation, production evaluation, repair and delivery. |
| Authority stage | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending; 1,221; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Writing, audit and revision are permitted; build and capsules are forbidden. |
| Write authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification work only; 1,462; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes this write with a pre-ratification ceiling. |
| Recovery packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-AIR-017-RECOVERY` freezes path, six FRs, three Stories and two write-interface edges. |
| Wave lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_11_DISPATCH_LOCK.yaml` | `DISPATCHED`; 1,412; `b83a4cea34e30954467510ad39f153375ef2ae64200ab2988fe109fbd35874cd` | Freezes exact TS-AIR-015/016 states and hashes. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | current; 134,201; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | All four F17 required unique sources are byte-available. |
| Canonical ledgers | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv`; `CANONICAL_FR_LEDGER.csv`; `FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen; hashes `acb0bd4b...`, `bb631307...`, `5c3a8dda...` | Fix spec identity, requirement text, owners, Stories, gate and claim ceiling. |

### 1.2 Controlling feature, Stories, exact sources, and Primitives

| Class / ID | Exact path | Bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| F17 feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F17-visual-activation-and-composition-before-editing.md` | 43,780; `464b6ee12ee2d408edfdf2ff17fb271db3ca0caa436419949ad2440b68f71a44` | AIR-FR-097-102 require research-grounded candidates, semantic composition intent, Feature Contracts, bounded handoff and rendered-result reparse. |
| Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-17.01-17.03 require exact inputs, no fabricated authority, selective invalidation, replay and CBAR denial evidence. |
| Donor full draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-017-visual-activation-and-composition-before-editing.md` | 30,282; `f946c95b51505e20d6658abd381a87e46c8156583843f2aa272033240e584ba8` | Structural baseline; amended for current ownership, strict models, exact upstream interfaces, repository invariants and V3.3 evidence. |
| `SRC-AI2-VISUAL-001` | `.../sources/ai_v2_predecessor/schemas/visual_narrative_program.schema.json` | 4,335; `1f1d9d5229156b2a9dfe0467f0879a1d057310825de1e0a774cac4f3188ffb46` | Useful beat/order, activation direction, transfer, Feature Contract and wrong-reading fields; default-empty and legacy harness fields require adaptation. |
| `SRC-AHP-F09-001` | `.../sources/doctrine/AHP_F09_COMPOSITION_IR.md` | 18,941; `68db87fa583d639af2ebdc707e9f94e7bca50af9b981dca1dd9c2f6be8eef456` | Pipeline exact Composition IR owns measured geometry, BBOX plus function, text measurement, deterministic layout and renderer artifacts. |
| `SRC-AHP-F15-001` | `.../sources/doctrine/AHP_F15_VAE_DELEGATION_GNM.md` | 18,207; `eb65e84b126369a3067464a0dc9bd7c0dec72ebd168111cdb7f1fdef69333f44` | Pipeline emits immutable VAD; VAE owns provider routing and production; result use requires separate downstream acknowledgement. |
| `SRC-VISUAL-DOCTRINE-001` | `.../sources/doctrine/CCP_CREATIVE_PIPELINE_ARCHITECTURE_V2.md` | 61,539; `8b9175d8631eff50b7f6c959ad245b87f9b307577b51e6dd4d2f622fd44175e8` | Composition precedes rendering; provider examples remain historical implementation evidence, not current semantic or provider authority. |
| `PRM-VSG-001` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-001.yaml` | 5,040; `568cd44028280d169316748ee58268e76ea3222423339eb6990b344268234698` | Eye path must be deliberate without forced over-engineering or applying visual rules to nonvisual artifacts. |
| `PRM-VSG-024` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-024.yaml` | 7,685; `8289b1968a104acd622ddedcad3c88a8977c7de523217fe14fb892809b0467e7` | Space expresses psychological relationship; empty-void, accidental claustrophobia and flat-Z-axis misuse must be tested. |
| `PRM-VSG-021` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | 8,179; `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Protect source-backed felt truth without manufactured messiness, distracting flaws or clarity sacrifice. |
| `PRM-BUS-006` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/design_business/PRM-BUS-006.yaml` | 6,533; `6abfae7c921e5768d459ceeb57b073ba9ba2865ad03e907bcb3361a72b391133` | Distinct semantic weights route attention; too many levels, arbitrary emphasis and inverted hierarchy fail. |

Ellipses in the display paths above abbreviate only the repeated bundle prefix shown in full in earlier rows. The files-read receipt records complete paths.

### 1.3 Admitted upstream drafts

| Edge | Exact path | State / bytes / SHA-256 | Interface consumed | Revision impact |
|---|---|---|---|---|
| SDE-044 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md` | `WRITTEN_PENDING_AUDIT`; 93,219; `58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Approved Final Script, Derivative Activation Program, semantic animation scenes and `SemanticProductionPackage` exact refs. | Sections 3, 5, 6, 8, 9, 10. |
| SDE-045 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-016.md` | `WRITTEN_PENDING_AUDIT`; 83,156; `5e4437baff399f65a2b0b63c6f3a43e91145fbd188dbcb503bf67cc09e24cddc`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `ActivationTransferContract`, must-survive properties, transformation freedoms, wrong-reading locks, checkpoints and source-fidelity evidence. | Sections 3, 5, 6, 8, 9, 10. |

The drafts are read-only interface inputs. This spec neither copies them into a local fork nor expands their authority. Downstream refs include owner, exact version/hash, lifecycle-at-use and limitation state.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure and outcome

Without a typed semantic visual stage, editing or image generation becomes an accidental meaning engine. A provider may produce an attractive image before the system has decided what the audience must recognize, which psychological role they enter, what relation negative space must express, which real-life evidence grounds the metaphor, or which wrong reading invalidates it. Later polish can conceal centroid placement, decorative references, weakened source fidelity, a dead eye path, or a production decision that silently changed the Final Script's intent.

The operator needs one inspectable path from the exact approved Final Script and Activation Transfer Contract to an AIR-owned visual semantic program, followed by Pipeline-owned execution and VAE-owned production realization. The user can see why each visual element exists, what may vary, what must survive, who owns every field, which evidence supports it, and why a render passed, failed or requires bounded repair.

### 2.2 Bounded solution

AIR opens an immutable `VisualActivationCase`, admits exact TS-AIR-015/016 inputs, compiles research questions and evidence-backed `VisualSemanticCandidate` records, selects one candidate through deterministic gates plus independent judgment, publishes a `VisualSemanticPack`, compiles a `VisualNarrativeProgram`, `CompositionIntent`, T/V route request and typed `FeatureContract` records, and publishes a `VisualActivationHandoff`.

The handoff contains `VisualRequirementIntent` records only. The Atomic Harness Pipeline validates the handoff, compiles category-native exact Composition IR, and emits authoritative immutable Visual Asset Demands where assets are missing. VAE compiles its own Visual Production Plan, chooses routes/models/LoRAs/conditioning, produces/evaluates/repairs candidates, accepts production output and delivers an Asset Result. VAE cannot mutate AIR objects or the Pipeline demand. AIR may later admit exact render/result observations and compile a `VisualReparseReceipt` comparing observed hierarchy, BBOX relationships, gaze, reading order, timing, role/tension and locks with intent; it does not convert that comparison into VAE production acceptance or Pipeline consumption acknowledgement.

### 2.3 In scope

- AIR-FR-097-102 and AIR-ST-17.01-17.03;
- exact source/semantic/Final Script/transfer admission;
- evidence-backed visual research requirement and reference citation;
- visual semantic candidate proposal, deterministic screening, independent comparison and selection;
- Visual Semantic Pack and Visual Narrative Program compilation;
- AIR-owned semantic Composition Intent, BBOX intent with WHY, T/V route requests and Feature Contracts;
- monotonic wrong-reading-lock inheritance;
- bounded nonauthoritative visual requirement intents and handoff;
- result observation admission and semantic reparse against intent;
- immutable lifecycle, atomic commits, idempotency, concurrency, cancellation, replay, supersession and selective invalidation;
- typed Pipeline, VAE, Delegation, Studio and independent-evaluation boundaries.

### 2.4 Out of scope and non-goals

- changing source, Reaction Receipt, Expression Moment, OAI, coalition, archetype, DNA, approved Final Script or transfer semantics;
- compiling an AtomicHarnessDefinition or running Pipeline nodes;
- exact pixel BBOX, typography measurement, timeline/canvas editing, renderer routing or authoritative VAD emission;
- VAE Visual Production Plan, provider/model/LoRA/conditioning selection, generation, production repair or acceptance;
- Delegation envelopes or transport semantics;
- Studio canonical state or hidden UI mutation;
- invention of evaluator thresholds, real-world performance claims, certification, Format 02 activation or VAE Stage 5;
- generic creative-safety/content-rights approval authority. Operator source authority, provenance, technical security and product sovereignty remain explicit.

## 3. Governing decisions and constraints

### 3.1 Precedence and product sovereignty

1. Current V1.1 remains highest current authority. The V2.1 Constitution, ownership matrices and F17 are candidate authority admitted only for specification work.
2. The candidate Program Control ownership matrices resolve a stale F17 object-owner table: AIR owns visual activation, Visual Semantic Pack, Visual Narrative Program, semantic Feature Contracts and semantic Composition Intent; Pipeline owns exact category-native execution, exact BBOX/WHY and authoritative VAD; VAE owns production planning and realization. This correction must be independently audited before ratification.
3. AIR must preserve TS-AIR-015/016 refs exactly. A missing field is blocked, not reconstructed as generic notes.
4. AIR may propose through bounded models, but deterministic validators own identity, version, source resolution, lifecycle legality, canonical hashing, lock inheritance and owner checks. A producer cannot approve itself.
5. `Activative Contract Compiler != Activative Intelligence Runtime`. Builder may declare exact dependencies and evaluation requirements but cannot compile or revise semantic visual meaning.

### 3.2 Composition-before-editing law

The lawful sequence is:

`ApprovedFinalScriptPackage -> ActivationTransferContract -> visual research evidence -> VisualSemanticPack -> VisualNarrativeProgram -> semantic CompositionIntent + FeatureContracts + T/V route -> VisualActivationHandoff -> Pipeline Composition IR/VAD -> VAE realization -> result observation -> independent evaluation/reparse`.

AIR's `BBOXIntent` declares semantic function, attention order, protected absence and WHY. Pipeline's Composition IR owns final normalized/pixel geometry, measured text, collision resolution and renderer-neutral placement. VAE may report feasibility and realized geometry but cannot change the authoritative semantic function.

### 3.3 Source, epistemic and reference fidelity

- Every visual assertion cites exact source/semantic refs and one of `PLANNED`, `OBSERVED`, `INFERRED`, `OPERATOR_CONFIRMED`, `REJECTED`, or `SUPERSEDED`.
- A real-life reference citation identifies specimen/environment/human/object behavior/documented system, provenance, applicability and permitted use. A filename, URL title or model memory is not evidence.
- Reference unavailability is explicit. AIR may issue a bounded research request, select another supported candidate, or block; it cannot fabricate a reference.
- Visual DNA constrains visual expression but does not overwrite psychological role, Matrix, coalition, Edge Product, source evidence or operator-approved Final Script.
- Exact active Primitive YAMLs are resolved by ID and hash. Names or summaries do not substitute for their trigger, suppression, conflict and misuse rules.

### 3.4 Wrong-reading locks and Feature Contracts

- Generative, composited, restyled or semantically transformative requirements carry nonempty wrong-reading locks.
- Every descendant inherits all applicable source, TS-AIR-015, TS-AIR-016, coalition, DNA and parent visual-program locks. It may add stricter locks, never remove or weaken one.
- Relaxation requires a new authorized upstream semantic version; neither Pipeline, VAE, Studio nor Delegation may relax in place.
- Feature Contracts are typed, versioned AIR semantic intent. VAE owns feasibility and realization evidence; realization cannot mutate the Feature Contract.
- `NOT_APPLICABLE` requires a pinned category/profile rule, evaluated condition, evidence ref and claim limit. Missing inspection is not N/A.

### 3.5 Active Primitive jobs

- `PRM-VSG-001` requires a deliberate eye path and rejects forced, unnatural routing.
- `PRM-VSG-024` requires environment/space to carry the intended psychological relationship and rejects accidental void, accidental claustrophobia and ignored depth.
- `PRM-VSG-021` requires source-backed felt truth where applicable and rejects manufactured messiness or clarity-destroying flaws.
- `PRM-BUS-006` requires distinct, noncompetitive semantic weights and rejects arbitrary emphasis, too many hierarchy levels and inverted importance.

No numeric threshold is invented from historic Studio defaults. Judgment dimensions use an exact evaluation profile with attributable calibration; absent calibration blocks judgment or yields `NOT_EVALUATED`, never a fabricated PASS.

### 3.6 Claim ceiling and explicitly forbidden behavior

The writer state is `WRITTEN_PENDING_AUDIT`; authority is `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; maximum pre-ratification later status is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Forbidden behavior includes hidden semantic mutation, AIR-emitted VAD bytes, AIR provider selection, VAE upstream mutation, Pipeline semantic reinterpretation, model self-approval, current-time/random/path-dependent identity, invented source/reference evidence, unsupported profile inference, Format 02 certification inheritance and production claims from structural tests.

## 4. Current brownfield architecture

`04_ACTIVATIVE_INTELLIGENCE_RUNTIME` currently contains specifications but no authorized implementation tree. All implementation paths in section 7 are prospective. Brownfield evidence is handled as follows:

| Exact path | Actual behavior | Disposition | Constraint |
|---|---|---|---|
| `.../specs/TS-AIR-017-visual-activation-and-composition-before-editing.md` | Full candidate draft with useful lifecycle and test outline but generic envelopes and stale ownership mapping. | `ADAPT` | Preserve FR/Story intent; replace ownership, strict contracts, repository law and evidence detail. |
| `.../sources/ai_v2_predecessor/schemas/visual_narrative_program.schema.json` | Closed legacy VNP with beats, directions, transfer ref, Feature Contract refs and locks; includes default-empty arrays and legacy `format_harness`. | `ADAPT` | New object uses exact immutable refs, owners, epistemic state, lifecycle, nonempty invariants and compatibility receipt; no in-place schema mutation. |
| `.../sources/doctrine/AHP_F09_COMPOSITION_IR.md` | Defines Pipeline-owned renderer-neutral geometry, BBOX+function, typography measurement, layout solving and real render artifacts. | `REUSE_AS_INTERFACE_EVIDENCE` | AIR emits semantic BBOX intent; it does not implement exact Composition IR. |
| `.../sources/doctrine/AHP_F15_VAE_DELEGATION_GNM.md` | Defines Pipeline demand/result boundary and VAE provider sovereignty. | `REUSE_AS_INTERFACE_EVIDENCE` | AIR produces nonauthoritative requirement intents; Pipeline owns VAD and VAE owns production. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/primitive_coalition.py` | Rich coalition models plus random UUID defaults, open maps and hard-coded evaluation thresholds. | `ADAPT` | Consume exact accepted AIR coalition refs; do not import UUID/default-threshold/hash behavior. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/composition_runtime.py` | Many typed composition/runtime/provider objects mixed in Studio namespace, random IDs and provider-specific jobs. | `SPLIT_AND_ADAPT` | Reuse fixture ideas; move semantic meaning to AIR, exact execution to Pipeline, production to VAE, projection to Studio. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/composition_runtime_service.py` | Mutable in-memory orchestration, default routes/zones, provider calls and operator approval. | `REPLACE` | Do not import hidden defaults, provider ownership, local canonical state or invented thresholds. |
| `THE_CMF_STUDIO(2)/registries/sda/registry_manifest.yaml`; `registries/sfl/registry_manifest.yaml` | Versioned manifest shapes for semantic geometry and function layers. | `ADAPT_AS_REGISTRY_EVIDENCE` | Exact entries must be separately source-locked; manifest counts are not semantic proof. |

Historical Ideogram/Flux/Skia/SAM3/GNM examples remain implementation research. No provider is selected or activated by this spec.

## 5. Proposed architecture and workflows

### 5.1 Components and responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| `VisualActivationAdmissionService` | Resolve exact TS-AIR-015/016 objects, owner, state, hashes, profiles and active Primitive refs. | Infer missing lineage or accept stale aliases. |
| `VisualResearchCompiler` | Compile typed research questions and admit exact reference evidence; record gaps and applicability. | Fabricate specimens or treat generated approximation as real-life evidence. |
| `VisualSemanticCandidateCompiler` | Produce bounded candidate proposals from approved semantic inputs; preserve rejected candidates. | Select by polish alone or alter source/Final Script/transfer. |
| `VisualSemanticSelector` | Run deterministic hard gates then independent profile-bound comparison; publish selected semantic pack. | Self-approve or invent thresholds. |
| `VisualNarrativeCompiler` | Compile ordered attention states, viewer-role progression, recognition carrier, pattern match/interrupt, payoff and residue. | Let T/V or format geometry substitute for a weak carrier. |
| `CompositionIntentCompiler` | Compile hierarchy, eye path, spatial relationship, negative space, BBOX intent with WHY, sequence role and intended viewer state. | Emit exact renderer geometry, timeline edits or provider prompts. |
| `FeatureContractCompiler` | Compile independently testable semantic requirements for gaze, hands, expression, props, evidence, text, scale, depth, motion, sonic cues and locks. | Declare VAE feasibility or realized result. |
| `VisualActivationHandoffPublisher` | Atomically publish exact semantic refs, nonauthoritative requirement intents, profile and limitations. | Emit authoritative VAD or Delegation envelope bytes. |
| `VisualResultObservationService` | Admit exact Pipeline/VAE result refs and evidence without mutating them. | Convert production acceptance into downstream consumption. |
| `VisualReparseService` | Compare observed visual syntax/activation evidence with AIR intent and emit typed findings/repair scope. | Perform production repair or rewrite intent. |
| `VisualActivationRepository` | Atomic stream/artifact/edge/receipt/idempotency/outbox storage and historical replay. | Store state without artifacts/receipts or expose mutable latest aliases as identity. |

### 5.2 State machines

`VisualActivationCaseState` is one of:

`OPEN -> INPUTS_LOCKED -> RESEARCH_READY -> CANDIDATES_PROPOSED -> SEMANTIC_SELECTED -> NARRATIVE_COMPILED -> INTENT_COMPILED -> FEATURES_COMPILED -> EVALUATED -> HANDOFF_ELIGIBLE -> HANDOFF_PUBLISHED`.

Any pre-publication state may transition to `BLOCKED`, `CANCELLED` or additive `SUPERSEDED`. `HANDOFF_PUBLISHED` remains immutable. Result evaluation uses a separate stream:

`RESULT_OBSERVED -> REPARSE_VALIDATED -> REPARSE_EVALUATED -> CONFORMS | REPAIR_REQUIRED | REJECTED | CONTESTED`.

`CONFORMS` is semantic conformance evidence only. It is not VAE production acceptance, Pipeline consumption acknowledgement, certification or publication authority.

### 5.3 Commands, events, and atomicity

Commands are `OpenVisualActivationCase`, `LockVisualActivationInputs`, `RegisterVisualReferenceEvidence`, `ProposeVisualSemanticCandidates`, `SelectVisualSemanticCandidate`, `CompileVisualNarrativeProgram`, `CompileCompositionIntent`, `CompileFeatureContracts`, `EvaluateVisualActivation`, `PublishVisualActivationHandoff`, `RegisterVisualResultObservation`, `ReparseVisualResult`, `RecordVisualReparseEvaluation`, `CancelVisualActivation`, and `SupersedeVisualActivation`.

Every command contains `command_id`, `idempotency_key`, `case_ref`, `expected_stream_version`, actor and authority refs, exact input refs, profile refs and requested transition. On success one transaction commits command record, canonical artifact bytes, content hash, stream event, dependency edges, receipt, idempotency record, current alias and durable outbox. On failure none becomes visible. Exact replay of the same key/input returns the original receipt; same key/different bytes fails `AIR_VISUAL_IDEMPOTENCY_COLLISION`; stale expected version fails without mutation.

Events are past-tense typed facts such as `VisualActivationInputsLocked`, `ReferenceEvidenceRegistered`, `VisualSemanticCandidatesProposed`, `VisualSemanticPackPublished`, `VisualNarrativeProgramCompiled`, `CompositionIntentCompiled`, `FeatureContractsCompiled`, `VisualActivationEvaluated`, `VisualActivationHandoffPublished`, `VisualResultObserved`, `VisualResultReparsed`, `VisualActivationSuperseded`, and `VisualActivationCancelled`.

### 5.4 End-to-end workflow

1. Admission proves exact approved TS-AIR-015 Final Script/Semantic Production Package and eligible TS-AIR-016 Activation Transfer Contract. It records source kind, epistemic state, category/profile and limitations.
2. Research compiler derives closed questions from recognition intent, audience visual world, native objects/rituals/status/loss/violation traces and category cliches. Applicable candidates require exact reference evidence.
3. Bounded candidate generation may propose metaphors, evidence structures, real-life scenes, graphic relations and composition strategies. Each candidate cites source/semantic/transfer/Primitive/DNA refs and records wrong-reading risk. Rejected proposals remain historical.
4. Deterministic gates reject missing refs, stale inputs, unsupported profile, flattened coalition, lock weakening, fabricated references and owner violations. An independent evaluator compares surviving candidates using the pinned profile; uncalibrated judgment blocks.
5. AIR publishes one selected `VisualSemanticPack`, then compiles the narrative beats and viewer-role progression. `CompositionIntent` and Feature Contracts are derived only after the carrier and narrative job are fixed.
6. Handoff publication binds all exact objects plus nonauthoritative visual requirement intents. Pipeline may reject stale/incompatible/unsupported handoffs; it may not repair semantic intent silently.
7. Pipeline executes exact category-native composition and emits immutable VAD versions. VAE independently plans and realizes each accepted demand. Delegation transports without interpretation.
8. AIR admits returned result evidence by exact ref. Deterministic reparse checks measurable hierarchy/BBOX/gaze/order/timing facts; independent judgment compares role/tension, felt truth and source fidelity. Failures route the smallest typed repair to the owning product.

### 5.5 Cancellation, late results, supersession, and repair

Cancellation races serialize by expected stream version: either publish commits and cancellation becomes a later additive record, or cancellation commits and publish fails. Late producer/evaluator results are retained as `LATE_NONCANONICAL_EVIDENCE`. A material upstream successor traverses typed edges only. Semantic changes produce a new AIR version; exact layout/render failures route to Pipeline; production failures route to VAE; transport failures route to Delegation; operator interpretation disputes route to Studio/HumanResolution without hidden canonical mutation.

## 6. Data models, contracts, schemas, and APIs

### 6.1 Common closed types and identity

All models reject unknown fields. No `Any`, open dictionary or implied default is allowed. `ImmutableRef` contains `object_id: NonEmptyString`, `version: NonEmptyString`, `sha256: Hex64`, `owner_product: ProductId`, `schema_id: NonEmptyString`, and `lifecycle_state_at_use: LifecycleState`. `ActorRef` contains exact actor, implementation and authority-context refs. `EvidenceRef` adds `evidence_kind`, `epistemic_state`, `locator`, `claim_limit` and `source_owner`.

Canonical bytes use one governed UTF-8 canonical JSON profile. Object members are ordered by profile; set-like collections are sorted by their complete immutable-ref tuple; narrative beats and reading paths retain declared order; numbers use governed decimal/integer forms; Unicode normalization is fixed; absent optional values are explicit union variants rather than omitted defaults. Content identity excludes receipt timestamps, storage paths, process/environment values and random IDs. IDs are derived from object kind plus canonical payload hash or are caller-supplied stable IDs validated against the payload.

### 6.2 Core AIR objects

#### `VisualActivationCase` - `ca.air.visual-activation-case/2.1.0-candidate`

Required fields: `case_id`, `case_version`, `state`, `source_package_refs[1..n]`, `expression_moment_refs[0..n]`, `semantic_production_package_ref`, `approved_final_script_ref`, `activation_transfer_contract_ref`, `primitive_coalition_ref`, `archetype_coalition_ref`, `brand_context_ref`, `voice_dna_ref`, `visual_dna_ref`, `category_id`, `profile_id`, `format_harness_ref`, `evaluation_profile_ref`, `operator_source_authority_ref`, `wrong_reading_lock_refs[1..n]`, `limitations`, and `content_sha256`.

Cross-field rules: interview sources retain required Reaction Receipt and Expression Moment provenance from upstream; non-interview sources do not invent them; all semantic refs share compatible source/Brand Context/Final Script lineages; current eligibility is evaluated by exact version, never mutable latest.

#### `VisualReferenceEvidence`

Fields: `evidence_id`, `reference_kind` (`SPECIMEN`, `REAL_ENVIRONMENT`, `HUMAN_REFERENCE`, `OBJECT_BEHAVIOR`, `DOCUMENTED_VISUAL_SYSTEM`, `SOURCE_FRAME`), `source_ref`, `locator`, `provenance_ref`, `observed_properties`, `applicability_statement`, `permitted_semantic_uses`, `prohibited_uses`, `epistemic_state`, `captured_by`, `owner_product`, `limitations`, `supersedes_ref?`, `content_sha256`.

Generated approximations cannot use a real-life reference kind. Unavailable evidence produces `VisualReferenceGap`, never an empty evidence array represented as complete.

#### `VisualSemanticCandidate` and `VisualSemanticPack`

Candidate fields: `candidate_id`, `case_ref`, `recognition_intent`, `viewer_role`, `role_inside_tension_ref`, `recognition_carrier`, `activation_directions[1..n]`, `visual_world_refs`, `reference_evidence_refs`, `metaphor_relations`, `source_evidence_bindings`, `primitive_binding_refs`, `archetype_ref`, `voice_dna_ref`, `visual_dna_ref`, `transfer_property_refs`, `category_profile_ref`, `composition_potential`, `wrong_reading_lock_refs`, `wrong_reading_risks`, `epistemic_state`, `producer_binding_ref`, `limitations`, `content_sha256`.

The pack contains `pack_id`, `selected_candidate_ref`, `rejected_candidate_refs`, deterministic-validation receipt, independent-evaluation receipt, selection-reason evidence, profile ref, exact upstream refs, inherited locks and hash. A selection reason is a typed evidence record, not free-text authority.

#### `VisualNarrativeProgram` - `ca.air.visual-narrative-program/2.1.0-candidate`

Required fields: `program_id`, `visual_semantic_pack_ref`, `activation_transfer_contract_ref`, `format_harness_ref`, `category_profile_ref`, `activation_directions`, `viewer_role_progression`, `pattern_match`, `pattern_interrupt`, `attention_state_sequence`, `beats[1..n]`, `prediction_gap`, `payoff`, `affinity_field?`, `anticipation_residue?`, `feature_contract_intent_refs`, `tv_route_request_refs`, `bbox_intent_refs`, `wrong_reading_lock_refs[1..n]`, `evaluation_profile_ref`, `limitations`, `content_sha256`.

Each `VisualNarrativeBeat` contains `beat_id`, ordered index, `attention_state`, `visual_job`, `recognition_carrier_ref`, `viewer_role_before`, `viewer_role_after`, `source_support_refs`, `operator_refs`, `feature_contract_refs`, `tv_route_request_refs`, `bbox_intent_refs`, `expected_payoff`, and `wrong_reading_lock_refs`. Empty default arrays from the predecessor schema are not silently accepted when the field is semantically required.

#### `CompositionIntent` - `ca.air.composition-intent/2.1.0-candidate`

Fields: `composition_intent_id`, `program_ref`, `sequence_role`, `semantic_hierarchy[1..n]`, `reading_path[1..n]`, `subject_relationships[1..n]`, `spatial_psychology`, `negative_space_intents[1..n]`, `bbox_intents[1..n]`, `depth_relationships`, `intended_viewer_state`, `identity_continuity_refs`, `tv_route_request_refs`, `feature_contract_refs`, `allowed_variation`, `forbidden_collapses`, `wrong_reading_lock_refs[1..n]`, `evaluation_profile_ref`, `limitations`, `content_sha256`.

`BBOXIntent` fields are `intent_id`, `semantic_target_ref`, `attention_function`, `relative_priority`, `reading_predecessor_refs`, `protected_absence`, `relationship_constraints`, `category_geometry_class`, `why_evidence_refs`, `allowed_variation`, and `forbidden_outcomes`. It contains no provider job and no authoritative final pixel coordinates. Pipeline compiles exact BBOX+WHY under its Composition IR while preserving this ref.

#### `FeatureContract` - `ca.air.visual-feature-contract/2.1.0-candidate`

Fields: `feature_contract_id`, `feature_kind` (`GAZE`, `HANDS`, `FACIAL_EXPRESSION`, `POSTURE`, `WITNESS`, `PROP`, `OBJECT_PUNCTUM`, `EVIDENCE`, `TEXT`, `SCALE`, `DEPTH`, `MOTION`, `SONIC_CUE`, `NEGATIVE_SPACE`, `IDENTITY_CONTINUITY`), `semantic_job`, `required_state`, `prohibited_states`, `source_support_refs`, `composition_intent_ref`, `applicability` (`REQUIRED` or evidenced `NOT_APPLICABLE` union), `allowed_variation`, `wrong_reading_lock_refs`, `deterministic_checks`, `judgment_profile_dimension_refs`, `feasibility_owner: VisualAssetEditor`, `realization_owner: VisualAssetEditor`, `semantic_owner: ActivativeIntelligenceRuntime`, `content_sha256`.

VAE feasibility or realization receipts refer to the contract and report `SUPPORTED`, `UNSUPPORTED`, `REALIZED`, `PARTIAL`, or `FAILED`; they never replace `required_state` or `semantic_job`.

### 6.3 Handoff, demand boundary, and result reparse

`VisualRequirementIntent` contains `intent_id`, `asset_family`, `semantic_role`, `sequence_role`, `composition_intent_ref`, `feature_contract_refs`, `identity_continuity_refs`, `geometry_need`, `permitted_variation`, `preservation_lock_refs`, `source_reference_refs`, `evaluation_profile_ref`, `priority`, `limitations`, and `authority_class: NONAUTHORITATIVE_REQUIREMENT_INTENT`. It contains no provider/model/LoRA/workflow/conditioning choice, price, deadline reservation or Delegation envelope fields.

`VisualActivationHandoff` contains exact refs to the case, semantic pack, narrative program, Composition Intent, all Feature Contracts, all requirement intents, category/profile/harness, source and DNA lineage, transfer contract, inherited locks, evaluation profile, limitations, producer/evaluator receipts, compatibility requirements and content hash. `owner_product` is AIR. The consumer may reject it but cannot mutate it.

Pipeline converts eligible requirement intents into its own immutable `VisualAssetDemand` versions and exact Composition IR. A demand records the AIR handoff ref. VAE accepts/rejects the demand, then owns Visual Production Plan and production. `ProductionAcceptanceReceipt` and `AssetResult` remain VAE-owned. Pipeline's `ConsumptionAcknowledgement` is separate and cannot be inferred from production acceptance.

`VisualResultObservation` contains exact demand/result/render refs, producer and acceptance refs, actual artifact hashes, measured geometry refs, limitations, production lifecycle-at-use and observation evidence. `VisualReparseReceipt` contains intended refs, observed hierarchy, BBOX relationships, gaze, reading order, timing, feature outcomes, lock outcomes, role/tension comparison, deterministic findings, independent judgment refs, decision (`CONFORMS`, `REPAIR_REQUIRED`, `REJECTED`, `CONTESTED`), responsible-owner attribution or `UNRESOLVED`, repair-scope refs and hash. It never changes the observed result or upstream intent.

### 6.4 Validation and compatibility

Validation order is schema -> exact ref/hash -> owner -> lifecycle -> source/epistemic -> lineage -> category/profile -> Primitive/Feature/lock inheritance -> deterministic composition-intent rules -> independent evaluation binding. Parsing without enforcement fails. Unknown enum/schema/profile versions fail closed. Adapters preserve every required field, owner and claim ceiling. Migrations create new immutable versions and receipts; they never guess source class, reference evidence, Composition Intent, profile support or locks.

Active cases remain pinned to negotiated versions. Deprecated versions remain historically reproducible. A consumer that supports syntax but cannot enforce a required feature, lock, reference or evaluation dimension returns `AIR_VISUAL_COMPATIBILITY_FEATURE_UNSUPPORTED`.

### 6.5 Positive and negative contract examples

Positive requirement intent:

```yaml
intent_id: vri_7f2a
asset_family: source_grounded_portrait_cutout
semantic_role: witness_after_recognition
sequence_role: payoff
composition_intent_ref: {object_id: ci_91aa, version: v1, sha256: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", owner_product: ActivativeIntelligenceRuntime}
feature_contract_refs: ["fc_gaze_01", "fc_hands_02"]
geometry_need: subject_bbox_and_protected_negative_space
permitted_variation: preserve_identity_gaze_relation_and_witness_distance
preservation_lock_refs: ["lock_no_triumphal_smile", "lock_no_centroid_crop"]
authority_class: NONAUTHORITATIVE_REQUIREMENT_INTENT
```

Negative examples include `provider: flux`, `lora_id`, `workflow: comfyui`, absent source refs, free-text `preserve vibe`, empty locks for a generated portrait, `not_applicable: true` without evidence, exact pixels represented as AIR authority, a VAE result overwriting `semantic_role`, or a rendered-result pass represented as downstream consumption. Each fails before publication.

### 6.6 Repository and public ports

Public ports are typed command handlers and read ports: `VisualActivationCommandPort.handle(CommandEnvelope) -> CommandReceipt`, `VisualActivationReadPort.get(ImmutableRef)`, `VisualActivationHistoryPort.replay(case_id, through_stream_version)`, `VisualActivationHandoffPort.publish(VisualActivationHandoff)`, and `VisualResultObservationPort.register(VisualResultObservation)`. Cross-product adapters depend only on released external contracts and local ports; they do not import another product's internal modules.

## 7. Implementation stages and exact target paths

These paths are future targets only. A ratified/adopted authority, independent acceptance, Development Capsule and explicit build authorization are required before any creation.

| Stage | FR / Story | Exact future paths | Completion evidence |
|---|---|---|---|
| 0 source and contract lock | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-017/SOURCE_LOCK.yaml` | Ratified authority, accepted upstream hashes, exact source/Primitive/profile and path allowlist. |
| 1 strict domain models | FR-097-102; all Stories | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/visual_activation.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/visual_narrative.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/composition_intent.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/visual_feature_contract.py` | Closed types, schema/model parity, canonical hash vectors, owner invariants. |
| 2 repository and lifecycle | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/visual_activation.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_activation_lifecycle_service.py` | Atomic parity, idempotency, concurrency, cancellation, replay and invalidation evidence. |
| 3 research and semantic candidates | FR-097, FR-098; ST-17.01 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_research_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_semantic_candidate_compiler.py` | Exact reference citations, gap denial, rejected-candidate corpus and independent selection. |
| 4 narrative, intent and features | FR-099, FR-100; ST-17.02 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_narrative_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/composition_intent_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_feature_contract_compiler.py` | Carrier-before-route, BBOX-intent/WHY, negative space, four Primitive and lock tests. |
| 5 handoff | FR-101; ST-17.03 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_activation_handoff_service.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/atomic_harness_pipeline_visual_activation.py` | AIR/Pipeline schema and authority conformance; no VAD/provider fields. |
| 6 result observation/reparse | FR-102; ST-17.03 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/visual_result_reparse_service.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/visual_activation_evaluator.py` | Deterministic observation, independent judgment, attribution and bounded repair routing. |
| 7 projection | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/projections/visual_activation.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/studio_visual_activation_commands.py` | Reconstructable read model and typed commands; no Studio canonical mutation. |
| 8 contracts and migrations | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/visual_activation/*.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/ai2_visual_narrative_to_v2_1.py` | Generated schema artifacts under separate release authority; lossless-or-blocked receipts. |

No files in this table are created by this writing step.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures and ownership

| Code | Meaning | Responsible owner / next action |
|---|---|---|
| `AIR_VISUAL_UPSTREAM_INELIGIBLE` | Final Script, semantic package or transfer contract missing/stale/unapproved. | AIR; admit exact eligible successor. |
| `AIR_VISUAL_REFERENCE_REQUIRED` | Applicable real-life/reference evidence absent. | AIR research boundary; acquire evidence or choose supported candidate. |
| `AIR_VISUAL_REFERENCE_FABRICATION` | Generated/inferred material represented as observed reference. | AIR; reject and preserve evidence. |
| `AIR_VISUAL_LINEAGE_FLATTENED` | Required source/Matrix/coalition/role/archetype/DNA/transfer field reduced to notes. | AIR; recompile from exact refs. |
| `AIR_VISUAL_COMPOSITION_PREMATURE` | Edit/render/demand requested before semantic intent and gates. | Pipeline admission; block execution. |
| `AIR_VISUAL_LOCK_WEAKENED` | Descendant removes or weakens inherited lock. | Producer attempting change; new authorized AIR version required. |
| `AIR_VISUAL_PROFILE_UNSUPPORTED` | Category/profile or required feature unavailable. | Consumer; reject without fallback guessing. |
| `AIR_VISUAL_EVALUATION_PROFILE_UNAVAILABLE` | Judgment rule/calibration missing. | Independent evaluation; remain unevaluated/blocked. |
| `AIR_VISUAL_AUTHORITY_VIOLATION` | AIR emits VAD/provider plan, or consumer mutates semantic object. | Violating product; deny command. |
| `AIR_VISUAL_RESULT_STALE` | Demand/result/render is superseded, revoked or mismatched. | Pipeline/VAE owner; supply eligible version. |
| `AIR_VISUAL_REPAIR_OWNER_UNRESOLVED` | Evidence cannot attribute semantic/execution/production fault. | Studio/operator diagnosis; no repair mutation. |
| `AIR_VISUAL_ATOMIC_COMMIT_FAILED` | Any command/artifact/event/edge/receipt member fails. | AIR repository; rollback all staged members. |
| `AIR_VISUAL_REPLAY_DIVERGENCE` | Recomputed bytes differ from historical bytes. | AIR; stop at first divergence. |

Deterministic retry is allowed for transient storage/transport after proving idempotency. Semantic or judgment failure uses a new bounded proposal/repair command, not blind retry. Provider production retries belong to VAE. Transport retries belong to Delegation.

### 8.2 Migration and compatibility

The AI2 VNP adapter maps exact legacy beats/directions/transfer/locks into a new immutable candidate. Missing owner, epistemic, category/profile, source support, BBOX intent, Feature Contract or lock evidence is `UNAVAILABLE_FROM_PREDECESSOR`; if required, migration blocks. Default-empty arrays are not upgraded to deliberate absence. Provider-specific Creative Pipeline objects migrate only as historical evidence or owned Pipeline/VAE artifacts. Studio composition records are split by owner; no monolithic object becomes AIR state.

Each migration emits source/target hashes, adapter version, field map, omitted-field decisions, limitation/claim ceiling and lossless-or-blocked verdict. Historical objects remain readable and are never mutated.

### 8.3 Rollback, cancellation, replay, and invalidation

Rollback changes the active service/profile/adapter for new work; it never rewrites artifacts created under the failed version. Atomic staging prevents orphan artifacts or receipts. Durable outbox retry occurs only after commit. Cancellation and publish/evaluation races use optimistic concurrency. Late evidence is historical and noncanonical.

Typed dependency edges include `USES_FINAL_SCRIPT`, `USES_SEMANTIC_PRODUCTION_PACKAGE`, `USES_TRANSFER_CONTRACT`, `USES_REFERENCE_EVIDENCE`, `USES_VISUAL_SEMANTIC_PACK`, `USES_VISUAL_NARRATIVE_PROGRAM`, `USES_COMPOSITION_INTENT`, `USES_FEATURE_CONTRACT`, `INHERITS_LOCK`, `EMITS_REQUIREMENT_INTENT`, `REALIZES_DEMAND`, `OBSERVES_RESULT`, and `EVALUATES`. Material successor/revocation traverses affected edges only. Historical assets/results and the exact context at acceptance remain replayable; stale aliases cannot be consumed.

### 8.4 Observability

Structured events record command/transaction/case/object IDs, exact refs/hashes, owners, epistemic/lifecycle states, category/profile, Primitive refs, reference kinds, candidate/selection/evaluator bindings, intent/feature/lock counts, demand/result refs, failure/attribution codes, stream version, idempotent replay, commit outcome and invalidation fan-out. Raw sensitive source text is excluded by default; evidence uses refs/locators.

Metrics include admission blockers, reference gaps/fabrication denials, candidate rejection reasons, source/coalition/DNA lineage gaps, lock inheritance failures, composition-premature denials, Primitive misuse, profile unsupported, evaluator unavailable/disagreement, VAD/provider boundary denials, result mismatch/staleness, repair attribution, invalidation fan-out, atomic rollback, idempotent replay, concurrency conflict, late evidence and replay divergence. Metrics are operational evidence, not semantic truth or certification.

## 9. Behavior-specific acceptance criteria

### AC-01 - AIR-FR-097 / AIR-ST-17.01: source-grounded visual semantic candidates

**Given** exact eligible Final Script, Semantic Production Package and Activation Transfer Contract, **when** candidates are compiled, **then** each metaphor, evidence structure, real-life scene, graphic relation and composition strategy cites role/tension, coalition, archetype, Voice/Visual DNA, transfer and source evidence. A generic attractive image with no recognition carrier fails. **Evidence:** candidate corpus, input crosswalk, rejection receipts. **Layer:** domain/integration.

### AC-02 - AIR-FR-098 / AIR-ST-17.01: applicable real-life reference before approximation

**Given** a candidate whose claim depends on a specimen, environment, human reference, object behavior or documented visual system, **when** selection runs, **then** exact provenance/applicability evidence exists before generation is requested. A generated office labeled real-life reference fails `AIR_VISUAL_REFERENCE_FABRICATION`. **Evidence:** reference pack/gap receipt. **Layer:** contract/adversarial.

### AC-03 - AIR-FR-099 / AIR-ST-17.02: semantic composition intent precedes execution

**Given** a selected semantic pack and narrative, **when** Composition Intent compiles, **then** hierarchy, reading path, subject relationships, BBOX function with WHY, negative space, depth, sequence role and intended viewer state are explicit before timeline/canvas/render authorization. Editing first and reverse-engineering intent later fails. **Evidence:** intent, denial receipt. **Layer:** architecture/integration.

### AC-04 - AIR-FR-100 / AIR-ST-17.02: independently testable Feature Contracts

**Given** gaze, hands, expression, props, evidence, text, scale, depth, motion, sonic or lock obligations, **when** features compile, **then** each has typed required/prohibited states, source support, applicability, variation, locks and evaluation dimensions. `important: good hands` fails. **Evidence:** Feature Contract set and negative fixtures. **Layer:** schema/contract.

### AC-05 - AIR-FR-101 / AIR-ST-17.03: bounded immutable handoff

**Given** evaluated semantic objects, **when** handoff publishes, **then** exact semantic authority, narrative, intent, requirement intents, allowed variation, sources, profiles and limitations are bound without provider/model/LoRA/workflow choices. AIR-emitted VAD or VAE plan fields fail. **Evidence:** handoff hash and Pipeline consumer report. **Layer:** contract/architecture.

### AC-06 - AIR-FR-102 / AIR-ST-17.03: rendered-result reparse

**Given** exact eligible result/render evidence, **when** reparse runs, **then** observed hierarchy, BBOX relations, gaze, reading order, timing, Feature Contract outcomes and role/tension are compared with exact intent. A visually polished result that reverses eye path or removes witness distance fails. **Evidence:** observation, deterministic findings, independent evaluation receipt. **Layer:** integration/evaluation.

### AC-07 - current constitutional visual sequence

**Given** a visual branch, **when** its dependency graph is inspected, **then** semantic pack precedes narrative, Feature Contracts and Composition Intent; Pipeline exact syntax precedes render; T/V cannot rescue a dead carrier; Visual Asset Demand remains Pipeline-owned. A single provider prompt substituting for the sequence fails. **Evidence:** DAG/architecture test. **Layer:** architecture.

### AC-08 - active Primitive CBAR

**Given** the four exact Primitive YAMLs, **when** candidate, intent and result are evaluated, **then** eye path, spatial psychology, felt truth and hierarchy are checked with trigger/suppression/misuse/conflict evidence. Forced scan path, accidental empty void, manufactured messiness or arbitrary emphasis each fail independently. **Evidence:** per-Primitive decision receipts. **Layer:** CBAR/adversarial.

### AC-09 - Composition Intent versus exact Composition IR

**Given** AIR BBOX intent and a Pipeline layout, **when** boundaries are checked, **then** AIR owns semantic function/WHY and Pipeline owns exact geometry/measurement/execution while preserving the AIR ref. AIR pixel placement or Pipeline semantic rewrite fails. **Evidence:** contract/import boundary test. **Layer:** architecture.

### AC-10 - Feature Contract versus VAE realization

**Given** an AIR Feature Contract and VAE feasibility/realization evidence, **when** the result is admitted, **then** VAE reports support/outcome without changing required state, semantic job or locks. A VAE adapter weakening a gaze obligation fails. **Evidence:** before/after hash and VAE conformance fixture. **Layer:** cross-product contract.

### AC-11 - wrong-reading lock monotonicity

**Given** all upstream and parent locks, **when** pack, narrative, intent, handoff, demand and result relationships are inspected, **then** every applicable lock survives and only stricter additions occur. Removing a lock for a smaller crop fails; relaxation requires a new authorized AIR semantic version. **Evidence:** ancestry diff. **Layer:** unit/contract.

### AC-12 - source and epistemic sovereignty

**Given** planned, observed, inferred and operator-confirmed evidence, **when** visual claims compile, **then** states and source owners remain distinct. AIR cannot turn an inferred audience visual into observed human reaction or reconstruct missing interview provenance. **Evidence:** owner/epistemic crosswalk. **Layer:** contract/architecture.

### AC-13 - evidenced NOT_APPLICABLE

**Given** a profile-conditional feature, **when** N/A is asserted, **then** the exact profile rule, condition, evidence and claim limit support it. Source lineage, composition intent, required locks and required feature states reject N/A. Empty evidence or evaluator omission fails. **Evidence:** positive/negative N/A fixtures. **Layer:** schema/evaluation.

### AC-14 - production acceptance versus consumption acknowledgement

**Given** a VAE production-accepted Asset Result, **when** lifecycle is projected, **then** Pipeline consumption remains a separate exact acknowledgement and AIR reparse remains separate semantic evidence. Inferring consumption or publication from production acceptance fails. **Evidence:** three-receipt lifecycle fixture. **Layer:** integration/governance.

### AC-15 - category/profile and Format 02 truth

**Given** a category/profile, **when** compatibility resolves, **then** only supported features and exact certification state are reported. Format 02 remains deferred; conversational/interview structural profiles inherit no production certification. Unsupported geometry/evaluation requirements fail rather than silently downgrade. **Evidence:** compatibility fixtures. **Layer:** contract/policy.

### AC-16 - deterministic identity and portability

**Given** identical logical inputs in fresh processes and extracted roots with changed clocks, random seeds, environment, locale, insertion and traversal order, **when** objects compile, **then** canonical bytes/hashes match and contain no absolute machine paths. Random IDs/current timestamps in content identity fail. **Evidence:** two-process hash matrix and path scan. **Layer:** determinism/clean environment.

### AC-17 - atomicity, idempotency and optimistic concurrency

**Given** fault injection at every commit member, exact retry, byte-different key collision and two expected-version writers, **when** commands execute, **then** all state/artifact/event/edge/receipt/idempotency/alias/outbox members commit or none; exact retry returns the original receipt; collision fails; one writer wins. **Evidence:** repository parity/fault matrix. **Layer:** integration.

### AC-18 - replay, cancellation and selective invalidation

**Given** a published handoff plus material upstream change/cancellation/late result, **when** recovery runs, **then** races serialize, late evidence stays noncanonical, affected descendants alone become stale and historical bytes replay without current models/latest refs. Global deletion or over-invalidation fails. **Evidence:** event replay and fan-out graph. **Layer:** recovery.

### AC-19 - producer/evaluator/owner separation

**Given** proposal, evaluation, Pipeline execution and VAE realization actors, **when** authorities are inspected, **then** producer does not self-approve, evaluator owns only evaluation receipts, Pipeline does not reinterpret semantics, VAE does not own Composition Intent, and Delegation does not interpret meaning. **Evidence:** identity/import/command boundary suite. **Layer:** architecture/security.

### AC-20 - claim ceiling

**Given** every structural and synthetic test passes, **when** status is reported, **then** this spec remains `WRITTEN_PENDING_AUDIT`, authority `CANDIDATE_NOT_CURRENT`, build false and certification/production false. An `ACCEPTED_FOR_BUILD`, Development Capsule or production claim fails. **Evidence:** lifecycle assertion. **Layer:** governance.

## 10. Testing and completion evidence

### 10.1 Exact future test paths

| Exact path | Required tests and evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_admission.py` | Exact TS-AIR-015/016 refs, owner/state/hash/profile, stale/ambiguous/missing denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_reference_evidence.py` | Six reference kinds, provenance/applicability, generated-approximation denial and explicit gap. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_semantic_candidates.py` | Source/role/coalition/archetype/DNA/transfer coverage, rejection preservation and anti-centroid cases. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_visual_narrative_program.py` | Ordered attention states/beats, carrier-before-route, role progression, payoff/residue and no default-empty loophole. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_composition_intent.py` | Hierarchy, reading path, spatial psychology, negative space, BBOX intent+WHY and no pixel/provider authority. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_feature_contracts.py` | All feature kinds, required/prohibited states, applicability union, lock inheritance and VAE report immutability. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_not_applicable.py` | Exact profile rule/evidence/claim limit and mandatory-dimension denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/visual_activation/test_canonical_hash.py` | Clock/random/env/path/locale/map/traversal independence and ordered-vs-set-like collections. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/schema/test_air_f17_schema_model_parity.py` | Closed schemas, required fields, unions, unknown-field/enum denial and canonical examples. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_ts_air_015_016_visual_interface.py` | Exact draft/accepted pins, public-field convergence, no local fork and downstream revision trigger. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_visual_activation_pipeline_handoff.py` | Pipeline consumes immutable handoff, compiles exact Composition IR/VAD, preserves intent and rejects stale/unsupported input. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_visual_activation_vae_boundary.py` | VAE owns plan/provider/production, cannot mutate intent/Feature Contracts/demand, and production acceptance is not consumption. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/cbar/test_air_f17_active_primitives.py` | Exact four YAML hashes plus trigger/suppression/misuse/conflict and no invented thresholds. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_visual_activation_and_composition_before_editing.py` | AIR-ST-17.01-17.03 and AIR-FR-097-102 complete path with typed blockers. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_visual_activation_repository.py` | Fault at every commit member, response-loss retry, collision, optimistic race, artifact/receipt parity and outbox. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_rendered_visual_reparse.py` | Observed hierarchy/BBOX/gaze/order/timing/role comparison, stale result and bounded attribution. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_visual_activation_candidate_evaluation.py` | Independent evaluator, profile/calibration unavailable, candidate rejection and no self-approval. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_visual_intent_result_conformance.py` | Wrong role, collapsed space, lost punctum, inverted hierarchy and non-compensable lock failures. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_air_f17_product_boundaries.py` | AIR/Builder/Pipeline/VAE/Studio/Delegation/Evaluation ownership; no VAD/provider/exact-render imports. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_ai2_visual_narrative_to_v2_1.py` | Lossless-or-blocked mapping, no guessed owner/source/profile/lock and immutable migration receipt. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_visual_activation_replay_cancellation_invalidation.py` | Cancellation race orderings, late evidence, selective fan-out, exact historical replay and first divergence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_air_f17_portability.py` | Two fresh processes/extracted layouts; no undeclared file, absolute path, environment, clock or random dependency. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_imported_interview_to_visual_activation.py` | Imported interview source -> observed semantics -> approved Final Script -> transfer -> visual activation -> Format 07/SuperVisual/animation handoff -> result reparse. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/regression/test_current_v1_1_visual_branch.py` | Current V1.1 semantic/narrative/Feature/T-V/BBOX/wrong-reading/Visual Syntax separation remains unweakened. |

### 10.2 Adversarial corpus

Required cases include missing/stale Final Script or transfer; planned claim represented as observed; unknown source kind; invented Reaction Receipt/Expression Moment; reference title without bytes; generated approximation labeled real; generic metaphor; missing real-life reference; source-interchangeable carrier; flattened Matrix/coalition/role/archetype/DNA; dead carrier rescued by T/V; forced eye path; empty-void and accidental-claustrophobia geometry; ignored depth; manufactured messiness; clarity-destroying punctum; too many hierarchy levels; arbitrary emphasis; missing/weak lock; invalid N/A; unsupported profile; Format 02 certification inference; uncalibrated evaluator; producer self-evaluation; AIR-emitted VAD; AIR provider/LoRA selection; Pipeline semantic rewrite; VAE Feature Contract mutation; Delegation interpretation; production acceptance inferred as consumption; stale result; contested attribution forced to one owner; absolute path/current time/random identity; partial commit; orphan receipt/artifact; idempotency collision; concurrency race; late result; invalidation overreach; lossy migration; and unauthorized acceptance/build/capsule/production claim.

### 10.3 Later completion evidence and Build Receipt

A later authorized builder must provide ratified/adopted authority and independently accepted spec hashes; exact accepted/re-audited TS-AIR-015/016 interfaces; a bounded Development Capsule and source/Primitive/profile/path locks; schema/model/generated-type parity; requirement-to-code/test/receipt traceability; deterministic two-process hash matrix; atomic fault matrix; replay/cancellation/invalidation proof; migration receipts; Pipeline and VAE consumer conformance; independent evaluator binding/calibration state; imported-interview reference-slice proof; clean extracted-layout and absolute-path scan; unresolved limitations; and the maximum supported claim.

The Build Receipt, if later authorized, must distinguish structural implementation, synthetic proof, external consumer conformance, evaluator certification, production eligibility and publication authority. None is inferred from another. This document issues no Build Receipt or Development Capsule.

Final writer state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later pre-ratification ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. The next admissible lifecycle action is independent Tech Spec audit by a different agent.
