---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-015
title: Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory Animation Scene Packages
product: Activative Intelligence Runtime
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 9
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
controlling_frs:
  - AIR-FR-085
  - AIR-FR-086
  - AIR-FR-087
  - AIR-FR-088
  - AIR-FR-089
  - AIR-FR-090
  - FR-167
controlling_stories:
  - AIR-ST-15.01
  - AIR-ST-15.02
  - AIR-ST-15.03
  - ST-12.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-005
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-006
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: f7e8b5ab03959fb503cbf5b862d4a139d35272e49f708372e40981721505a4a4
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-007
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: e6a2b106a751463bd14be44b6b36bbb14e7f6ff05984fae85c5357d7bc6199ec
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-011
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: c48ef679872bfa3e8bf2bd40ea44c3f4d18da30b3d05d19a99d5131fe26dd00b
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-015 — Derivative Activation Programs, Guest Voice DNA Final Scripts, and Mandatory Animation Scene Packages

This specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`; this document does not make it current, authorize implementation, create schema or release bytes, issue a Development Capsule, or grant build, production, publication, provider, Format 02, VAE Stage 5, or certification authority.

`TS-AIR-005`, `TS-AIR-006`, `TS-AIR-007`, and `TS-AIR-011` are exact hash-pinned drafts in `WRITTEN_PENDING_AUDIT`. Each is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their interfaces are admitted for dependency-safe writing, not represented as ratified or accepted law. A change to any pin reopens the six downstream revision-impact sections identified below.

## 1. Files and authorities read

### 1.1 Authority, lifecycle, and packet lock

| Class | Exact path | State / bytes / SHA-256 | Specific use |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624 bytes; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten sections, evidence, draft-dependency and claim-ceiling rules. |
| Source-package instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | 1,911 bytes; `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Requires authority, feature, Stories, exact Primitive YAMLs and named sources before normative writing. |
| Current Constitution | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; 40,830 bytes; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current authority; preserves source-backed Expression Moments, visual semantic/narrative lineage, wrong-reading locks and separate composition authority until candidate ratification. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION`; 1,288 bytes; `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Candidate is additive and requires separate ratification and implementation authorization. |
| Candidate Constitution | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`; 51,243 bytes; `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | AIR ownership, observed/planned separation, Primitive/archetype/Final Script sequence, DNA, composition and reusable animation-scene laws. |
| Program ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate; 4,263 bytes; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns coalition/Final Script and composition-intent meaning; IE owns source/reaction/moment evidence; operator approval is attributable. |
| Cross-product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate; 4,289 bytes; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR compiles meaning; Pipeline executes and emits authoritative Visual Asset Demands; VAE realizes; Studio projects/captures resolution; Delegation transports. |
| Authority stage | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending; 1,221 bytes; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Writing/audit/revision are permitted; build and capsule are forbidden. |
| Write authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification work only; 1,462 bytes; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes this write while preserving the pre-ratification ceiling. |
| Frozen recovery packets | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 bytes; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-AIR-015-RECOVERY`, exact FRs, Stories, path and dependency law. |
| Wave dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_09_DISPATCH_LOCK.yaml` | `DISPATCHED`; 1,359 bytes; `fc8d9c18285a7512c4936b0c7dd929b0b77819f77d1f25c7419ef7f6dbb4163f` | Freezes the only four admitted upstream drafts and their hashes. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated; 134,201 bytes; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | All required unique F15 sources are byte-available; no optional source is used as authority. |
| Canonical FR ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | frozen; 104,516 bytes; `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns AIR-FR-085–090 and FR-167 to AIR/TS-AIR-015. |
| Canonical traceability | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen; 236,715 bytes; `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact requirement text, Stories, sources, gates and evidence ceilings. |
| Canonical spec ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | frozen; 23,269 bytes; `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Reserves this direct AIR path and seven-FR/four-Story packet. |

### 1.2 Controlling feature, Stories, and source evidence

| Class | Exact path | Bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| F15 feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F15-derivative-activation-final-scripts-and-animation-scene-packages.md` | 42,164; `13b2ec1b96db8a12cd37df9009da85d9d71f5438fa6d882160b1763cb8e7923e` | Approved source-backed semantic package and approved Final Script precede composition; every eligible script yields reusable animation scenes. |
| AIR Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-15.01–15.03 require exact lineage, typed blockers, recovery and three CBAR mandates. |
| Primary donor draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-015-derivative-activation-final-scripts-and-animation-scene-packages.md` | 29,555; `20633a45c8616be662f0b8874b6b5bac23f18051ae009a029110db526c21e8f4` | Candidate design baseline; amended here for current ownership, exact upstream interfaces, deterministic repository and V3.3 structure. |
| AHP Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-12.03 requires one Voice-DNA-constrained, source/coalition-traceable Final Script approved before composition. |
| AHP F28 | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | 14,624; `0a130c459707e309ae323f769b00d0f82f866b8bfddf6eb42546a5de4f78370c` | FR-167 blocks Composition IR, scene programs, visual-generation demands and renderer workspaces until exact approval gates pass. |
| Static/animation doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/AHP_F25_STATIC_ANIMATION_DERIVATIVES.md` (`SRC-AHP-F25-001`) | 17,410; `dbab88c994da95fbead65abfba4984d0efa3cd8a2fb27598997bd9886c37d293` | Category-native derivatives preserve source/voice/identity/batch lineage; animation does not activate Format 02. |
| Role/Final Script doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/F28-psychological-role-archetype-coalition-and-final-script-authority.md` (`SRC-AHP-F28-001`) | 14,624; `0a130c459707e309ae323f769b00d0f82f866b8bfddf6eb42546a5de4f78370c` | Full source → Matrix → Primitive coalition → archetype → Voice DNA → Final Script → composition ordering. |
| Brand doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` (`SRC-BRAND-001`) | 45,066; `61710fe56484b569ce28ddefadbb4c8047e9ae48cadf25291423cf4f200e3dcb` | One frozen Brand Context Version binds identity, visual constitution, libraries and source editing session. |
| Archetype doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_ARCHETYPE_SYSTEM_MIGRATION_PROPOSITION.md` (`SRC-ARCH-001`) | 35,537; `2d7aa11b72c83a95d9240784978e3b9af4944a3e037f18746f8b204bc3287188` | Core archetypes are meaning grammars; asset derivatives are packaging structures and do not define core meaning. |
| Creative architecture | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_Creative_Pipeline_Architecture_V2.md` (`SRC-DOCT-004`) | 61,539; `8b9175d8631eff50b7f6c959ad245b87f9b307577b51e6dd4d2f622fd44175e8` | Typed narrative/scene/composition/layer/animation/renderer stages; composition precedes rendering. |
| Interview evidence | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321; `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | CMF input becomes exact Expression Moment/asset-package evidence rather than an untyped trigger. |
| Exact Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/voice_audio_intimacy/PRM-VOC-009.yaml` | 7,583; `90405cef54e303ca87c2f274e6ac6a39b77cf261b86166a385e2ffb6420d5b80` | Sensory Scene Anchoring; suppress when already overloaded; reject generic/manipulative anchors. |
| Exact Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | 5,071; `2be2e140588e23e43b4461c9443884b09401f6541ea29bdbae8e945e4672e30c` | Intent Governs Style; reject lazy defaults or uncontrolled brand inconsistency. |
| Exact Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | 7,495; `b05b6aabef1d48f0a3bf07f5b4a43febe2fb53445df5e1a8524a6ba0f78f48d5` | What Is / What Could Be oscillation; reject utopian hype and demoralizing pain saturation. |

### 1.3 Admitted draft interfaces

| Edge | Exact path | State / bytes / SHA-256 | Interface consumed | Revision-impact sections |
|---|---|---|---|---|
| SDE-035 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-005.md` | `WRITTEN_PENDING_AUDIT`; 44,990; `5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `PrimitiveCoalitionContract`, `CoalitionSignature`, `EdgeProduct`, evaluation and wrong-reading/routeability evidence. | sections 3, 5, 6, 8, 9, 10 |
| SDE-036 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-006.md` | `WRITTEN_PENDING_AUDIT`; 47,369; `f7e8b5ab03959fb503cbf5b862d4a139d35272e49f708372e40981721505a4a4`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `PsychologicalRoleTensionContract`, `ArchetypeCoalitionProgram`, exact SDA/SFL and route receipt. | sections 3, 5, 6, 8, 9, 10 |
| SDE-037 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-007.md` | `WRITTEN_PENDING_AUDIT`; 72,140; `e6a2b106a751463bd14be44b6b36bbb14e7f6ff05984fae85c5357d7bc6199ec`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Brand Context, Voice DNA, Visual DNA, Distillation Trace, CCV, SDA/SFL, Voice-constrained draft and Edge Integrity evidence. | sections 3, 5, 6, 8, 9, 10 |
| SDE-038 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-011.md` | `WRITTEN_PENDING_AUDIT`; 104,994; `c48ef679872bfa3e8bf2bd40ea44c3f4d18da30b3d05d19a99d5131fe26dd00b`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact IE-owned evidence refs through AIR-owned `ObservedActivativeIntelligencePack`, claim limits, wrong-reading updates and immutable lifecycle. | sections 3, 5, 6, 8, 9, 10 |

No upstream draft is copied into a local fork. Exact refs, versions, hashes, owners, lifecycle-at-use, limitations and evaluation state cross this boundary. A changed pin blocks advancement until the six listed sections are explicitly reviewed and revised where affected.

### 1.4 Brownfield implementation evidence

| Exact path | Bytes / SHA-256 | Actual behavior and disposition |
|---|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/archetype_subsystem_compiler_service.py` | 599; `510cd7ec05485f397e3f371c396f98654c2e901cc5f6b1c67aa38810175eae0d` | Chains score → archetype program → delivery recipe with no source/authority/evaluation/receipt gate. `REPLACE` as semantic service; retain only orchestration-order evidence. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/narrative_story_doctor_service.py` | 43,880; `64d9e906e9f9d93c4d95bc17c54a469bf8071782b6abf5e75ada688a02dd7cff` | Useful source-span and derivative fixture ideas, but embeds heuristic strings/floats/defaults, mutable repository writes, inferred moments, delivery recipes and a Format 02 path. `ADAPT` fixtures and pure helpers; `REPLACE` ownership/state/approval behavior. |

`04_ACTIVATIVE_INTELLIGENCE_RUNTIME` currently contains specification documentation only. Every implementation path in section 7 is prospective and forbidden until ratification or applicable adoption, independent acceptance, a Development Capsule and separate build authorization.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem and user outcome

An approved quote, Expression Moment, or observed activation is source evidence, not a Final Script. If a renderer, layout, model, Pipeline node or Studio projection starts composition from loose quotes or generic copy, the words, Primitive physics, archetype sequence, visual world and animation opportunities can each encode a different meaning. The output may look polished while hiding an unresolved script, flattening the guest into a brand centroid, misrepresenting observed evidence, or forcing expensive composition to be rebuilt after semantic repair.

The operator needs one reproducible gate that proves:

- every admitted source ingredient and observed-evidence claim is exact, current or historically eligible, and owned by its source product;
- one category-specific Derivative Activation Program preserves the psychological role inside the tension, full Primitive coalition, archetype coalition, Edge Product, Brand Context, Guest Voice DNA, Visual DNA, distillation and transfer obligations;
- every script segment declares whether it is verbatim, an omission, condensation, adaptation, connective operator-authored language or rewrite;
- an independent evaluator and attributable operator approval act on the exact Final Script bytes;
- no composition, animation program, visual-generation demand or renderer workspace starts before that approval; and
- every eligible approved script yields a reusable, composition-ready semantic 2D Animation Scene Package even if the current derivative renders none or only selected scenes.

### 2.2 Bounded solution

AIR opens an immutable `DerivativeActivationCase` from exact IE evidence and exact AIR semantic programs. It freezes a `DerivativeInputManifest`; compiles a category-specific `DerivativeActivationProgram`; issues bounded JIT Writer/Composer requests containing approved ingredients only; admits exact proposal bytes; validates every `ScriptSegmentLineage`; independently evaluates one `FinalScriptPackageCandidate`; records an attributable operator decision; publishes an immutable `ApprovedFinalScriptPackage`; compiles a semantic `AnimationScenePackage`; and assembles a portable `SemanticProductionPackage` for Builder dependency declaration and Pipeline execution.

AIR never mutates IE evidence, substitutes generic text, creates Pipeline execution state, emits the authoritative Visual Asset Demand, selects VAE production methods, or renders media. The scene package contains AIR-owned semantic composition intent and typed visual requirement intents. Pipeline compiles executable category-native programs and authoritative Visual Asset Demands from those exact inputs without reinterpreting meaning.

### 2.3 In scope

- exact source, Expression Moment, Reaction Receipt and observed-intelligence references and claim ceilings;
- complete Matrix, Primitive coalition/signature/Edge Product, psychological-role/tension, archetype and DNA lineage;
- category/profile compatibility admission without claiming unsupported certification;
- bounded JIT writer/composer request and proposal admission contracts;
- segment-level language/voice transformation lineage;
- deterministic Final Script validation, independent evaluation and attributable operator approval;
- AIR-owned composition intent and reusable semantic 2D Animation Scene Packages;
- Activation Transfer Contract and immutable Semantic Production Package;
- commands, events, state transitions, atomic commit, idempotency, concurrency, cancellation, replay, supersession and selective invalidation;
- migration from attributable predecessor evidence only, losslessly or with a typed blocker.

### 2.4 Out of scope and non-goals

- live source activation, transcript correction, Reaction Receipt or Expression Moment resolution;
- redefining Identity DNA, Context Premise, Matrix, Primitive, coalition, Edge Product, archetype, Brand/Voice/Visual DNA or observed evidence;
- AtomicHarnessDefinition compilation, Pipeline execution, editing, provider/runtime/model/LoRA selection, VAE production planning, candidate generation, production evaluation or production acceptance;
- directly emitting Delegation `VisualAssetDemand` bytes; AIR emits semantic requirement intent only;
- product-local Studio mutation, hidden approval, generic creative-safety/content-rights authority or automatic global learning;
- activating Format 02, inheriting Format 02 certification, VAE Stage 5, code, schemas, generated types, contract release bytes, a Development Capsule, build, production or certification.

## 3. Governing decisions and constraints

1. **AIR owns derivative semantic meaning.** AIR owns `DerivativeActivationProgram`, Final Script semantic compilation, Primitive/archetype/Brand–Voice–Visual lineage, `ActivationTransferContract`, semantic `CompositionIntent`, `AnimationScenePackage`, and `SemanticProductionPackage`. Pipeline executes approved programs; it cannot reconstruct or rewrite their meaning.
2. **Human script authority remains attributable.** AIR may compile and validate a Final Script candidate, but only an exact, scoped operator decision can produce `OPERATOR_APPROVED`. Model, evaluator, Pipeline, Studio projection, renderer, Builder, VAE and Delegation cannot grant that state.
3. **Interview Expression evidence is referenced, never absorbed.** Source packages, Reaction Observations/Receipts, Expression Moments, approvals and negative/borderline evidence remain IE-owned. AIR pins exact refs/hashes/lifecycle-at-use and does not normalize, relabel, suppress, repair or create an AIR-local authoritative copy.
4. **Observed intelligence remains evidence-bounded.** A derivative using observed human behavior pins the exact AIR-011 pack and underlying IE evidence handoff. Its maximum claim, unresolved inferences, alternatives, limitations, planned-observed delta and wrong-reading updates travel into the derivative. A derivative cannot upgrade an inferred or unresolved claim to observed truth.
5. **No flattened lineage.** `source_notes`, `creative_context`, `brand_style`, `archetype_name`, `primitive_ids` or generic metadata cannot replace typed refs to the source package, Moments, receipts, Matrix, coalition, signature, Edge Product, role/tension, archetype program, Brand Context, Voice DNA, Visual DNA, Distillation Trace, CCV, SDA/SFL and evaluation receipts.
6. **Primitive coalition is a full contract.** AIR-005's ordered roles, relations, conflicts, exclusions, misuse risks, suppression decisions, Coalition Signature, fatality/routeability evidence and Edge Product are all preserved. An ID list or embedding is incompatible.
7. **Psychological role and archetype geometry are load-bearing.** AIR-006's role, tension, recognition, stance, movement, counteractivation, transfer invariants, one-primary archetype, bounded support/transition roles, exclusions, SDA/SFL and anti-centroid locks are preserved. A theme or format label is insufficient.
8. **Brand, Voice DNA and Visual DNA remain separate.** One exact Brand Context Version binds separate Voice and Visual contracts. Voice DNA constrains non-verbatim language; Visual DNA constrains the visual world without replacing category-native composition. Neither can be represented as a mood adjective.
9. **RSCS and CCV remain inspectable.** Saturation, collision, compression, evaluation and recursion records precede Final Script approval. Variants change declared axes only; random seeds, temperature or wording differences do not prove meaningful diversity.
10. **Final Script approval is a non-compensable gate.** No Composition IR, VideoEditProgram, animation scene execution program, authoritative Visual Asset Demand or renderer workspace may be compiled before one exact Final Script passes source, Voice DNA, archetype, Primitive, Activative, wrong-reading, independent-evaluation and operator-approval gates.
11. **AIR scene packages are semantic, not production plans.** `AnimationScenePackage` declares scene meaning, sequence role, psychological role, timing intent, BBOX intent, identity/continuity, composition intent and visual requirement intents. Pipeline turns them into executable composition/editing programs and authoritative Visual Asset Demands. VAE owns production planning and realization.
12. **Every eligible Final Script has a reusable scene package.** Eligibility cannot be satisfied by saying animation is not the current output. A zero-render decision may be valid, but the composition-ready semantic package still exists unless a governed category/profile applicability decision proves the script ineligible.
13. **Active Primitive physics is exact.** `PRM-VOC-009` must use source-specific sensory cues without overload/generic/manipulative anchoring. `PRM-VSG-003` requires every style intent to serve communication rather than laziness or uncontrolled inconsistency. `PRM-PRS-015` preserves grounded What Is/What Could Be oscillation without hype or demoralizing saturation. Their activation, suppression, misuse and conflict fields are evaluated separately.
14. **Wrong-reading locks are monotonic.** All parent source, OAI, coalition, archetype, DNA and Final Script locks are inherited. Descendants may add stricter locks; they cannot remove or weaken one. Relaxation requires a new authorized upstream version, not a local repair.
15. **`NOT_APPLICABLE` is evidence-bearing.** A dimension may be N/A only when a pinned profile declares it conditional, an applicability decision names the condition, and evidence proves it. Source lineage, role/tension, coalition, Voice DNA for transformed text, approval, inherited locks and required transfer fields cannot be N/A.
16. **Producer and evaluator are independent.** Deterministic gates may run in the producer service. An independent evaluation receipt with distinct actor/authority context is required before operator approval eligibility. Evaluator capability does not imply certification.
17. **Operator resolution is scoped.** Studio may project alternatives and submit a typed command backed by a `HumanResolutionEpisode`. The episode records a decision but does not mutate canonical state directly or promote a global rule automatically.
18. **Canonical identity is portable.** Identity-bearing serialization excludes current time, randomness, environment, hostname, process ID, locale, filesystem traversal/insertion order, absolute paths, provider callback order and mutable “latest” aliases. Times are caller-supplied evidence outside the canonical payload where needed.
19. **History is additive.** Revisions and approvals create immutable successor versions. Supersession and invalidation never overwrite source evidence, prior scripts, evaluations, rejected alternatives, HumanResolutionEpisodes, scene packages or production packages.
20. **Draft interfaces remain drafts.** The four pinned specs control interface detail only. They do not become current authority through this write. Any pin drift reopens sections 3, 5, 6, 8, 9 and 10.
21. **Activative Contract Compiler is not AIR.** Builder declares exact dependencies and compiles AtomicHarnessDefinition structure. It does not compile this semantic meaning. AIR does not compile the Harness or execute it.
22. **Claim ceiling is explicit.** This document ends at `WRITTEN_PENDING_AUDIT`. Before attributable ratification, no later state may exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; build, capsule, product adoption, production and certification remain false.
23. **Current V1.1 remains current.** This candidate architecture cannot override the current Constitution or its composition-authority boundary. Any adoption-time conflict between V1.1 and candidate V2.1 requires attributable ratification/amendment before implementation; the writer does not silently resolve it as current law.

## 4. Current brownfield architecture

| Artifact | Actual behavior | Disposition | Migration constraint |
|---|---|---|---|
| Donor TS-AIR-015 | Names the six principal objects, six AIR FRs, three Primitives, broad lifecycle and scene-package outcome. | `ADAPT` | Add FR-167/ST-12.03, current ownership, four exact upstream interfaces, full lineage, strict types, atomic repository, portability and V3.3 evidence. |
| AIR-005 draft | Full Primitive coalition/signature/Edge Product interface. | `CONSUME_HASH_PINNED_DRAFT` | Preserve all roles, exclusions, conflicts, misuse, evaluation and locks; no local schema fork. |
| AIR-006 draft | Role/tension and archetype coalition interface. | `CONSUME_HASH_PINNED_DRAFT` | Preserve role geometry, one-primary coalition, SDA/SFL, exclusions and route receipt. |
| AIR-007 draft | Brand Context, separate Voice/Visual DNA, RSCS/CCV/SDA/SFL and Voice-constrained draft. | `CONSUME_HASH_PINNED_DRAFT` | Final Script gate consumes exact draft/trace/evaluation refs and never self-approves F07 output. |
| AIR-011 draft | AIR-owned observed semantic pack over immutable IE evidence. | `CONSUME_HASH_PINNED_DRAFT` | Preserve pack/source/evidence refs, lifecycle, epistemic state, maximum claim, limitations, alternatives and wrong-reading updates. |
| `ArchetypeSubsystemCompilerService` | Selects a max-scored archetype and immediately derives a delivery recipe. | `REPLACE` | No score-only archetype choice, delivery recipe before Final Script, hidden product authority or unreceipted result. |
| `NarrativeStoryDoctorService` | Heuristically normalizes source, invents default expression candidates, chooses strings/floats, creates derivative packets and writes mutable in-memory state. | `ADAPT` as fixture vocabulary; `REPLACE` as current compiler | Preserve exact source spans and useful negative cases only. Reject default moments, generic fallbacks, unpinned floats, Format 02 inference, mutable “latest” and sequential partial writes. |
| Historical Core Archetype / Asset Derivative documents | Separate meaning grammar from packaging structure. | `ACTIVATE_AS_EVIDENCE` | Resolve exact registry member/version/hash; never choose by filename or popularity. |
| Creative Pipeline animation examples | Provide composition-layer, BBOX, layer and animation-plan vocabulary. | `ADAPT_AS_NONAUTHORITATIVE_REFERENCE` | AIR owns semantic intent only. Renderer/provider/runtime selection stays downstream. |
| Current AIR product root | Contains `docs/` and no product source tree. | `PRESERVE` | Section 7 paths are proposed only; this prompt creates no source tree or implementation artifact. |

Migration from a predecessor object is legal only when each required field maps to exact evidence. A legacy archetype name becomes a candidate ref, not an approved coalition. A raw quote becomes a `VERBATIM` segment only when offsets/hash/speaker resolve. A heuristic expression candidate cannot become an approved Expression Moment. A delivery recipe cannot become a Final Script, Composition Intent or Animation Scene Package. Missing classification, source, role/tension, coalition, DNA, approval, wrong-reading, evaluation or authority produces a typed migration blocker while preserving the historical bytes.

## 5. Proposed architecture and workflows

### 5.1 Components and authority boundaries

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `DerivativeEvidenceAdmissionPort` | Resolve exact IE source/Moment/Receipt evidence and AIR OAI pack with owner, lifecycle, max claim and limitations. | Mutate IE, guess source kind, omit adverse evidence or upgrade claims. |
| `SemanticDependencyResolver` | Resolve exact Matrix, coalition, role/tension, archetype, Brand/Voice/Visual, RSCS/CCV/SDA/SFL and profile refs. | Use “latest”, flatten contracts or rebuild upstream meaning. |
| `DerivativeActivationCompiler` | Compile category-specific semantic objective, allowed ingredients, transfer requirements, locks and composition-intent envelope. | Compile AtomicHarnessDefinition, execution bindings or VAE production strategy. |
| `JitAuthoringContextCompiler` | Emit least-context, role-specific Writer/Composer requests from approved ingredients and constraints. | Give unrestricted source, unapproved candidates or hidden authority to a model. |
| `ScriptProposalAdmissionService` | Store exact proposals, validate segment lineage and reject invented/verbatim-mislabeled content. | Silently edit proposal bytes or accept generic copy. |
| `FinalScriptEvaluatorGateway` | Run deterministic gates and obtain independent semantic evaluation. | Allow producer self-approval or unpinned evaluator/profile. |
| `FinalScriptApprovalService` | Apply attributable operator decision to exact candidate/evaluation bytes and create successor state. | Infer approval from UI state, evaluation pass or model confidence. |
| `AnimationScenePackageCompiler` | Compile reusable semantic scenes, composition intent, timing/BBOX intent and visual requirement intents. | Emit authoritative Visual Asset Demands, select models/LoRAs or render. |
| `SemanticProductionPackageAssembler` | Seal approved script, lineage, scene package, transfer, evaluation, limitations and dependency graph for consumers. | Reinterpret meaning or omit stale/invalidation state. |
| `DerivativeProgramRepository` | Atomically store immutable command/artifact/event/edge/receipt/idempotency/current-alias/outbox records. | Partial commits, mutation, path-derived identity or receipt/artifact mismatch. |

Pure domain compilation imports no clock, random source, filesystem, network, provider SDK, Studio, Pipeline, VAE, Builder or Delegation module. External model proposals and independent evaluation responses are persisted as exact input artifacts before deterministic admission.

### 5.2 Workflow A — open and freeze the derivative case

1. Accept `OpenDerivativeActivationCase` with caller-supplied command/idempotency IDs, expected stream version, actor/authority refs, target category/profile, derivative objective, campaign/sequence role and exact source/semantic refs.
2. Resolve the IE source package, approved Expression Moment(s), required Reaction Receipt(s), source authority, restrictions, negative/borderline evidence and lifecycle-at-use. Unknown, stale-current or ineligible refs fail; historical eligible refs remain exact.
3. Resolve the exact AIR-011 observed pack when observed claims are used. If no published observed pack is required, record `NoObservedPackDecision` with profile rule and evidence; do not synthesize observed meaning from source notes.
4. Resolve exact AIR-005/006/007 objects and evaluations. Require one current-compatible Matrix/coalition/signature/Edge/role/archetype/Brand Context/Voice DNA/Visual DNA dependency set.
5. Resolve exact category/profile compatibility without inferring certification. A structurally supported or contract-compatible profile stays at that state.
6. Freeze `DerivativeInputManifest` with every positive/adverse ref, version, hash, owner, lifecycle-at-use, epistemic/claim ceiling, limitation and inherited lock. Canonically sort set-like refs by `(schema_id, object_id, version, sha256)`.
7. Commit case, manifest, command, event, dependency edges and receipt atomically. An idempotent exact replay returns the original result; same key/different canonical command bytes returns conflict.

### 5.3 Workflow B — compile the Derivative Activation Program

1. Validate that source ingredients support the requested derivative objective and the role/tension/Edge Product remains category-routeable.
2. Preserve the full Primitive coalition and archetype coalition without projection into labels. Evaluate active F15 Primitive bindings against exact trigger/suppression/misuse/conflict fields.
3. Compile `DerivativeActivationProgramCandidate` containing approved source ingredients, category/profile, campaign role, role/tension, Matrix/coalition/Edge/archetype, Brand/Voice/Visual, observed-evidence binding, RSCS/CCV/SDA/SFL, transfer requirements, wrong-reading locks and required evaluation dimensions.
4. Run deterministic completeness, owner, lifecycle, epistemic, category/profile, Primitive, anti-centroid, lock-inheritance and compatibility gates.
5. Store accepted candidate or typed blocker. Compilation does not yet authorize composition.

### 5.4 Workflow C — bounded JIT writing and composing

1. `CreateJitAuthoringRequest` selects role `WRITER` or `COMPOSER`, an exact authoring skill/binding and the minimum context required for one operation.
2. Writer context contains exact approved source spans, allowed transformation classes, active Voice DNA, role/tension, Edge Product, archetype sequence, coalition obligations, Distillation Trace, category copy function, wrong-reading locks and disallowed claims. Composer context additionally contains approved segment candidates and scene-function requirements, but no production route.
3. A model/program returns `ScriptProposalArtifact` bytes plus segment proposals and reasoning/evidence refs. The response is stored unchanged. Model sampling may be nondeterministic; each byte set has its own exact hash and never becomes canonical merely because it was returned.
4. `AdmitScriptProposal` validates each segment. Verbatim text must byte/offset/hash-match source; transformed language must cite source/evidence and transformation operations; operator-authored connective lines must cite the exact semantic bridge they serve and cannot introduce a source claim.
5. Rejected alternatives, generic/centroid drafts and failure reasons remain immutable evidence. A new attempt is a new proposal, not an overwrite.

### 5.5 Workflow D — evaluate and approve the Final Script

1. `AssembleFinalScriptCandidate` orders admitted segments and binds script-level source, role/tension, coalition, archetype, Voice/Visual DNA, RSCS, transfer, scene opportunity and lock refs.
2. Deterministic gates verify source/transform lineage, exact Voice DNA application, sequence/archetype obligations, Primitive coverage/misuse, active Brand Context, observed-evidence ceiling, inherited locks, required scene opportunities and no unresolved current dependency.
3. `RequestFinalScriptEvaluation` stores exact candidate/profile/evaluator-binding bytes. The independent evaluator returns per-dimension findings for source fidelity, Voice DNA, role/tension, Matrix/Edge survival, Primitive coalition, archetype geometry, Activative transfer, observed-evidence bounds, anti-centroid integrity, wrong-reading locks, category function and animation-scene feasibility.
4. No weighted aggregate can compensate for a failed mandatory dimension. Verdict is `VALIDATED`, `REJECTED`, `CONTESTED` or `NEEDS_MORE_EVIDENCE`.
5. `ResolveFinalScriptApproval` accepts an exact operator decision referencing candidate and evaluation. `APPROVE` creates `ApprovedFinalScriptPackage`; `REJECT` or `REQUEST_REVISION` preserves the candidate and yields a typed next action. A hidden UI toggle is invalid.
6. Only `OPERATOR_APPROVED` exact bytes become composition-eligible. The approval does not itself authorize build or production.

### 5.6 Workflow E — compile reusable Animation Scene Package

1. For every eligible approved Final Script, derive semantic scene boundaries from script segments, archetype sequence, role/tension movement, source media role, PRM-PRS-015 oscillation, Visual DNA, SDA/SFL and transfer requirements.
2. Each scene declares its semantic/sequence role, source/script refs, psychological movement, character or symbolic roles, composition intent, duration/frame intent, BBOX intent with reason, negative-space function, props/environments/diagram/quote/reference needs, identity/continuity requirements, wrong-reading locks and candidate reuse roles.
3. `VisualRequirementIntent` describes a missing ingredient and its semantic constraints. It is not a Delegation or Pipeline `VisualAssetDemand` and carries `authoritative_visual_asset_demand: false`.
4. Scenes may be designated `B_ROLL`, `CAROUSEL_COMPONENT`, `SUPERVISUAL_COMPONENT`, `FULL_ANIMATION_SCENE` or a governed non-Format-02 route. Reuse preserves the exact originating script/coalition/scene version and adds a new usage receipt.
5. A current derivative may render zero scenes only when a governed execution decision records that choice. The semantic scene package remains complete and eligible for later exact consumption.
6. AIR evaluates scene-package semantic completeness independently from Pipeline composition execution and VAE production feasibility. It cannot claim renderer output.

### 5.7 Workflow F — seal and hand off the Semantic Production Package

1. `AssembleSemanticProductionPackage` requires exact approved script, derivative program, scene package, Activation Transfer Contract, source/observed lineage, evaluations, limitations, category/profile and dependency/invalidation graph.
2. Canonical validation proves every referenced object exists, is eligible for this package version and preserves all inherited locks and maximum claims.
3. Atomic publication commits the package, receipt, event, edges, current alias and outbox intent. No consumer notification is sent before commit.
4. Builder may declare exact dependencies; Pipeline may accept/reject the package through public compatibility and lifecycle rules. Rejection cannot mutate AIR state.
5. Pipeline compiles category-native execution/composition, emits authoritative Visual Asset Demands and records consumption. VAE production acceptance is separate from Pipeline consumption acknowledgement.

### 5.8 Supersession, cancellation, invalidation and replay

- Source, Moment, Reaction Receipt, OAI, Matrix, coalition, archetype, Brand/Voice/Visual, profile or evaluator successor versions do not mutate active cases. New work may select an eligible successor; accepted cases remain pinned.
- Material upstream supersession marks only typed descendants stale: affected segment candidates, script candidates/approvals, scenes and production packages. Unrelated derivatives and historical assets remain readable.
- Relaxing a wrong-reading lock requires a new authorized upstream object. A downstream successor cannot do it.
- Cancellation before commit discards staging; after commit it appends cancellation/invalidation state. A late proposal/evaluation is retained as noncanonical evidence and cannot resurrect the case.
- Replay resolves exact historical commands, source/evidence bytes, all four upstream interfaces, model proposal/evaluation bytes, operator resolution, profiles/rulesets, events and invalidation view. It never calls a current model or uses “latest”.

## 6. Data models, contracts, schemas, and APIs

All schemas below are candidate interfaces for this specification, not created release bytes. Implementations must use closed models, reject unknown fields, avoid untyped dictionaries and implied defaults, and use canonical UTF-8 JSON with lexicographically ordered object keys, arrays sorted only when the field is declared set-like, integers for integral measures, integer micros for weights, and lowercase SHA-256 hex.

### 6.1 Shared types

`ImmutableRef`:

```text
schema_id: nonempty governed identifier
object_id: nonempty stable identifier
version: nonempty immutable version
sha256: exactly 64 lowercase hex characters
owner_product: governed ProductId
lifecycle_state_at_use: governed enum
```

`EvidenceBearingApplicability<T>` is a closed union:

- `APPLICABLE { value: T, profile_rule_ref: ImmutableRef, evidence_refs: nonempty ImmutableRef[] }`
- `NOT_APPLICABLE { profile_rule_ref: ImmutableRef, condition_code: governed code, evidence_refs: nonempty ImmutableRef[] }`

It has no null/unknown branch. Unknown or unassessed produces a blocker, not N/A.

`InheritedWrongReadingLock`:

```text
lock_id: stable identifier
origin_ref: ImmutableRef
lock_kind: SOURCE_FIDELITY | IDENTITY | ROLE_TENSION | PRIMITIVE_MISUSE |
           ARCHETYPE_GEOMETRY | VOICE_DNA | VISUAL_DNA | OBSERVED_CLAIM |
           COMPOSITION | CATEGORY | OTHER_GOVERNED
prohibition: nonempty canonical text
evidence_refs: nonempty ImmutableRef[]
inheritance: REQUIRED
strength: BASE | STRICTER_DESCENDANT
```

### 6.2 `DerivativeInputManifest` — `ca.air.derivative-input-manifest/2.1.0-candidate`

Required fields:

```text
manifest_id, case_id, input_set_sha256
source_package_ref: ImmutableRef owned by Interview Expression
expression_moment_refs: nonempty ordered ImmutableRef[] owned by Interview Expression
reaction_receipt_refs: ordered ImmutableRef[] owned by Interview Expression
negative_and_borderline_evidence_refs: ordered ImmutableRef[]
source_authority_ref, source_restriction_refs
observed_binding: PublishedObservedPack | NoObservedPackDecision
planned_activative_pack_ref, context_premise_ref, matrix_result_ref
primitive_coalition_ref, coalition_signature_ref, edge_product_ref
psychological_role_tension_ref, archetype_coalition_program_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
distillation_trace_ref, ccv_plan_ref
sda_refs, sfl_refs
category_profile_ref, derivative_objective_ref, campaign_or_sequence_role_ref
evaluation_profile_refs, compatibility_profile_ref
inherited_wrong_reading_locks: nonempty ordered InheritedWrongReadingLock[]
limitations: ordered Limitation[]
maximum_claim: governed ClaimCeiling
authority_ref, frozen_by_command_ref, canonical_hash
```

`PublishedObservedPack` requires the exact AIR-011 pack/evaluation and IE evidence-handoff refs. `NoObservedPackDecision` requires a profile rule, reason, evidence, and maximum claim that forbids observed assertions. Empty arrays are legal only where the controlling profile explicitly permits none; they never erase required owner/lifecycle fields.

### 6.3 `DerivativeActivationProgram` — `ca.air.derivative-activation-program/2.1.0-candidate`

Required fields:

```text
program_id, version, case_ref, input_manifest_ref
category_profile_ref, derivative_kind, derivative_objective_ref
campaign_or_sequence_role_ref
source_ingredient_bindings: nonempty ordered SourceIngredientBinding[]
viewer_role_tension_ref, matrix_result_ref
primitive_coalition_ref, coalition_signature_ref, edge_product_ref
archetype_coalition_program_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
observed_intelligence_binding
distillation_trace_ref, ccv_plan_ref, sda_refs, sfl_refs
active_primitive_bindings: nonempty ordered PrimitiveBindingRef[]
jit_authoring_constraints: JitAuthoringConstraints
composition_intent_envelope: CompositionIntentEnvelope
animation_scene_requirement: EvidenceBearingApplicability<AnimationSceneRequirement>
activation_transfer_requirements: nonempty ordered TransferRequirement[]
wrong_reading_locks: nonempty ordered InheritedWrongReadingLock[]
required_evaluation_dimensions: nonempty governed EvaluationDimension[]
authority_ref, lifecycle_state, dependency_refs, supersedes_ref, canonical_hash
```

`derivative_kind` is a governed category/profile capability, not a free string. `composition_intent_envelope` contains semantic spatial/temporal/attention/relationship requirements and explicit nonauthority for renderer/provider selection. It cannot contain VAE workflow/model/LoRA choices.

Lifecycle: `CANDIDATE -> DETERMINISTICALLY_VALIDATED -> AUTHORING_ELIGIBLE -> SCRIPT_PENDING -> SCRIPT_APPROVED -> SCENE_PACKAGE_COMPILED -> PRODUCTION_PACKAGE_PUBLISHED`; exact versions may later become `SUPERSEDED`, `INVALIDATED`, `REVOKED` or `CANCELLED`. A blocked candidate remains `REJECTED` or `NEEDS_MORE_EVIDENCE` and cannot skip states.

### 6.4 `JitAuthoringRequest` and `ScriptProposalArtifact`

`JitAuthoringRequest` — `ca.air.jit-authoring-request/2.1.0-candidate`:

```text
request_id, program_ref
role: WRITER | COMPOSER
skill_ref, authoring_binding_ref, deterministic_baseline_ref
allowed_source_ingredient_refs: nonempty ImmutableRef[]
allowed_transformation_classes: nonempty TransformationClass[]
voice_dna_ref, role_tension_ref, edge_product_ref, archetype_program_ref
primitive_coalition_ref, distillation_trace_ref, category_function_ref
required_scene_functions, transfer_requirements, wrong_reading_locks
forbidden_claim_codes, maximum_claim, tool_grants, output_contract_ref
authority_ref, expires_at_evidence_ref, canonical_hash
```

`tool_grants` is a closed tuple of named capabilities with resource scope and no cross-product write grant. `expires_at_evidence_ref` is caller-supplied operational evidence and excluded from semantic identity.

`ScriptProposalArtifact` stores exact returned bytes, producer identity/binding, request ref/hash, candidate segment records, provider/model response metadata as a typed attachment, deterministic-baseline comparison, and proposal hash. It is immutable and never carries approval.

### 6.5 `ScriptSegmentLineage` — `ca.air.script-segment-lineage/2.1.0-candidate`

```text
segment_id, ordinal, segment_text_sha256, canonical_text
transformation_class: VERBATIM | DISCLOSED_OMISSION | CONDENSATION |
                      ADAPTATION | OPERATOR_AUTHORED_BRIDGE | REWRITE
source_span_bindings: ordered SourceSpanBinding[]
semantic_support_refs: nonempty ImmutableRef[]
authoring_request_ref, proposal_ref, authoring_binding_ref
voice_dna_application_ref: EvidenceBearingApplicability<ImmutableRef>
distillation_operation_refs, archetype_function_ref, category_function_ref
epistemic_state, maximum_claim
approval_state: PROPOSED | ADMITTED | REJECTED | INCLUDED_IN_APPROVED_SCRIPT |
                SUPERSEDED | INVALIDATED
evaluation_finding_refs, wrong_reading_locks, canonical_hash
```

Validation rules:

- `VERBATIM` requires nonempty source spans whose ordered bytes equal the canonical text; no Voice rewrite is applicable.
- `DISCLOSED_OMISSION` requires exact retained/omitted offsets and disclosure text.
- `CONDENSATION`, `ADAPTATION` and `REWRITE` require source spans, transformation operations and applicable Voice DNA evidence.
- `OPERATOR_AUTHORED_BRIDGE` may lack a verbatim span only when semantic support refs and an attributable operator/authoring program prove it introduces no source claim; it still requires applicable Voice DNA.
- A transformed segment cannot retain `VERBATIM`; missing source does not become an empty tuple.

Positive example: a condensation cites two exact source spans, an RSCS compression step, Voice DNA application and the script objective. Negative example: polished copy marked verbatim but differing by one word fails `AIR_DERIVATIVE_VERBATIM_MISMATCH`.

### 6.6 `FinalScriptPackage` and approval receipt

`FinalScriptPackage` — `ca.air.final-script-package/2.1.0-candidate`:

```text
script_id, version, program_ref, input_manifest_ref
ordered_segment_refs: nonempty ImmutableRef[]
source_span_crosswalk_ref, script_sequence_ref
viewer_role_tension_ref, matrix_result_ref
primitive_coalition_ref, coalition_signature_ref, edge_product_ref
archetype_coalition_program_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
observed_intelligence_binding, distillation_trace_ref
script_composition_intents: nonempty CompositionIntent[]
animation_opportunity_refs: ordered AnimationOpportunity[]
activation_transfer_contract_ref
wrong_reading_locks, limitations, maximum_claim
deterministic_gate_receipt_ref
independent_evaluation_receipt_ref: ImmutableRef | absent_until_evaluated
operator_decision_ref: ImmutableRef | absent_until_decided
lifecycle_state, dependency_refs, supersedes_ref, canonical_hash
```

The two conditionally absent receipt fields are represented by the lifecycle-specific schema variant, not nullable fields or implied defaults. Candidate variants cannot claim composition eligibility.

`FinalScriptApprovalReceipt` — `ca.air.final-script-approval-receipt/2.1.0-candidate`:

```text
receipt_id, script_candidate_ref, evaluation_receipt_ref
decision: APPROVE | REJECT | REQUEST_REVISION | SUPERSEDE
operator_actor_ref, operator_authority_ref, human_resolution_ref
decision_reason_codes, scoped_notes_attachment_ref
approved_dependency_snapshot_ref, resulting_script_ref
composition_eligible: boolean
decision_recorded_at_evidence_ref, command_record_ref
repository_transaction_id, canonical_hash
```

`composition_eligible` is true only for `APPROVE` when every mandatory evaluator finding passes and dependency snapshot remains eligible. The decision time is evidence, not a generated identity source.

### 6.7 `AnimationScenePackage` — `ca.air.animation-scene-package/2.1.0-candidate`

```text
package_id, version, approved_final_script_ref, derivative_program_ref
scene_refs: nonempty ordered AnimationScene[]
shared_identity_and_continuity_refs
visual_dna_ref, sda_refs, sfl_refs
activation_transfer_contract_ref
source_and_observed_lineage_refs
wrong_reading_locks, evaluation_profile_ref
semantic_evaluation_receipt_ref
render_decision: RENDER_ALL | RENDER_SELECTED | DEFER_RENDER_PRESERVE_PACKAGE
selected_scene_refs: ordered ImmutableRef[]
lifecycle_state, dependency_refs, supersedes_ref, canonical_hash
```

`AnimationScene`:

```text
scene_id, ordinal, script_segment_refs, source_span_refs
scene_role: B_ROLL | CAROUSEL_COMPONENT | SUPERVISUAL_COMPONENT |
            FULL_ANIMATION_SCENE | GOVERNED_CATEGORY_COMPONENT
semantic_function, viewer_role_movement, tension_state
what_is_what_could_be_phase: WHAT_IS | WHAT_COULD_BE | TRANSITION | RESOLUTION
character_or_symbolic_roles, composition_intent
duration_intent: FrameRangeIntent | DurationMicrosIntent
bbox_intents: ordered BBoxIntent[]
negative_space_intents, gaze_and_attention_intents
pose_expression_keyframe_intents, prop_environment_diagram_quote_intents
visual_reference_requirements, identity_continuity_requirements
visual_requirement_intents: ordered VisualRequirementIntent[]
reuse_constraints, inherited_wrong_reading_locks
```

`BBoxIntent` uses integer normalized millionths `(x, y, width, height)` and a nonempty `why` tied to semantic/attention function. `VisualRequirementIntent` contains requirement ID, semantic/asset role, exact source/reference needs, identity and continuity constraints, composition intent ref, locks and acceptance dimensions; it declares `authoritative_visual_asset_demand: false`. It is not a provider prompt or VAE plan.

### 6.8 `ActivationTransferContract` and `SemanticProductionPackage`

`ActivationTransferContract` — `ca.air.activation-transfer-contract/2.1.0-candidate`:

```text
contract_id, version, source_activation_ref, observed_pack_binding
viewer_role_tension_ref, edge_product_ref
primitive_coalition_ref, archetype_coalition_ref, final_script_ref
must_survive_invariants: nonempty TransferInvariant[]
counteractivation_risks, participation_or_movement_requirements
source_media_role, category_profile_ref
required_evaluation_dimensions, wrong_reading_locks
maximum_claim, authority_ref, canonical_hash
```

`SemanticProductionPackage` — `ca.air.semantic-production-package/2.1.0-candidate`:

```text
package_id, version, derivative_program_ref, approved_final_script_ref
animation_scene_package_ref, activation_transfer_contract_ref
source_package_ref, expression_moment_refs, reaction_receipt_refs
observed_pack_binding
matrix_result_ref, primitive_coalition_ref, coalition_signature_ref, edge_product_ref
psychological_role_tension_ref, archetype_coalition_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
distillation_trace_ref, ccv_plan_ref, sda_refs, sfl_refs
category_profile_ref, compatibility_profile_ref
evaluation_receipt_refs, operator_approval_receipt_ref
limitations, maximum_claim, wrong_reading_locks
consumer_requirements: nonempty ConsumerRequirement[]
dependency_graph_digest, lifecycle_state, supersedes_ref, canonical_hash
```

Consumers receive exact refs and restrictions; they do not receive generic notes as substitutes. Publication means the AIR semantic package is eligible for a separately authorized consumer decision. It does not mean an Atomic Harness exists, a Pipeline run is authorized, a VAE asset is accepted, or production is certified.

### 6.9 Independent evaluation

`FinalScriptEvaluationReceipt` is owned by Independent Evaluation and requires:

```text
receipt_id, subject_ref, evaluation_profile_ref, evaluator_binding_ref
producer_identity_ref, evaluator_identity_ref
findings: nonempty ordered EvaluationFinding[]
verdict: VALIDATED | REJECTED | CONTESTED | NEEDS_MORE_EVIDENCE
maximum_claim, limitations, evidence_refs
ruleset_and_model_artifact_refs, canonical_hash
```

Mandatory findings are source fidelity; source/observed claim ceiling; Voice DNA; Visual DNA constraint preservation; role/tension; Matrix/Edge Product; Primitive local function/coalition/misuse; archetype geometry; RSCS; anti-centroid; category function; transfer; wrong-reading inheritance; segment provenance; animation-scene opportunity completeness; and producer/evaluator independence. Each finding is `PASS`, `FAIL` or evidence-bearing `NOT_APPLICABLE`; no scalar average creates a verdict.

### 6.10 Commands, events, repository and APIs

Commands:

- `OpenDerivativeActivationCase`
- `CompileDerivativeActivationProgram`
- `CreateJitAuthoringRequest`
- `AdmitScriptProposal`
- `AssembleFinalScriptCandidate`
- `RequestFinalScriptEvaluation`
- `ApplyFinalScriptEvaluation`
- `ResolveFinalScriptApproval`
- `CompileAnimationScenePackage`
- `AssembleSemanticProductionPackage`
- `SupersedeDerivativeArtifact`
- `InvalidateDerivativeDescendants`
- `CancelDerivativeCase`
- `ReplayDerivativeCase`

Events mirror successful transitions: `DerivativeCaseOpened`, `DerivativeInputsFrozen`, `DerivativeProgramCompiled`, `JitAuthoringRequested`, `ScriptProposalStored`, `ScriptSegmentsAdmitted`, `FinalScriptCandidateAssembled`, `FinalScriptEvaluated`, `FinalScriptDecisionResolved`, `FinalScriptApproved`, `AnimationScenePackageCompiled`, `SemanticProductionPackagePublished`, `DerivativeArtifactSuperseded`, `DerivativeDescendantsInvalidated`, `DerivativeCaseCancelled`.

Repository port:

```text
commit(expected_stream_version, command_record, artifacts, events,
       dependency_edges, receipts, idempotency_record, current_alias_update,
       outbox_intents) -> Committed | Replayed | Conflict | Blocked
get_exact(ref) -> artifact_with_lifecycle
get_command(command_id) -> command_record
get_receipt(ref) -> receipt
find_by_idempotency_key(key) -> prior_result | absent
list_dependencies(ref, edge_type, cursor) -> page
list_descendants(ref, edge_type, cursor) -> page
replay(stream_id, through_version) -> replay_result
```

Commit rejects state without command/event/receipt, receipt without every exact artifact, approval without independent evaluation/operator decision, scene package without approved script, production package without transfer/dependency graph, and any partial edge set.

Read APIs expose exact versions only; a separate current-alias lookup returns ref plus lifecycle/invalidation status. There is no generic mutable patch. Handoff APIs are typed: `get_semantic_production_package(ref)`, `validate_consumer_compatibility(ref, manifest)`, and `acknowledge_consumption(ref, consumer_receipt)`. Consumption acknowledgement cannot duplicate or replace semantic/visual evaluation.

### 6.11 Canonical examples

Positive case: an interview derivative pins one IE source package, two approved Expression Moments, their Reaction Receipts, one published AIR-011 pack, exact AIR-005/006/007 programs, three Primitive YAML versions, one operator-approved Final Script, four reusable scenes and a transfer contract. Reordering set-like evidence refs yields the same hash; changing script order changes it.

Negative cases:

- `{ "source_notes": "good emotional moment", "voice": "authentic", "archetype": "witness" }` — flattened, unowned and unhashed;
- a rewritten sentence marked `VERBATIM` — false provenance;
- a Final Script with evaluator pass but no operator decision — not composition-eligible;
- an Animation Scene Package containing `model: flux` or `lora: coach-v3` — VAE production-authority leak;
- an AIR object marked `visual_asset_demand` — Pipeline ownership violation;
- `not_applicable: true` without profile rule and evidence — missing proof;
- a child scene omitting an inherited wrong-reading lock — invalid weakening;
- a package selecting `format02` because a predecessor route emitted it — deferred-profile violation.

## 7. Implementation stages and exact target paths

Every path is a proposed future path. None may be created from this writing state. Ratified or adopted authority, independently accepted specs and upstream interfaces, an exact Development Capsule and separate build authorization are required.

| Stage | Exact future paths | FR / Story and evidence boundary |
|---|---|---|
| 0 — capsule and source lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-015/DEVELOPMENT_CAPSULE.yaml`; `SOURCE_LOCK.yaml` | All seven FRs/four Stories; requires ratification and exact accepted upstream hashes. |
| 1 — domain models | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/domain/input_manifest.py`; `derivative_activation_program.py`; `script_lineage.py`; `final_script.py`; `animation_scene_package.py`; `semantic_production_package.py`; `activation_transfer.py` | AIR-FR-085–090, FR-167; pure closed invariants and canonical serialization. |
| 2 — ports and repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/ports/evidence_admission.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/ports/semantic_dependencies.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/ports/authoring_gateway.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/ports/evaluation_gateway.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/ports/repository.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/derivative_program_repository.py` | Atomicity, idempotency, concurrency, exact reads, dependency parity and replay. |
| 3 — services | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/evidence_admission.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/program_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/jit_authoring_context.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/script_proposal_admission.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/final_script_lifecycle.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/animation_scene_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/services/production_package_assembler.py` | AIR-ST-15.01–15.03 and ST-12.03 workflows. |
| 4 — schemas/examples | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.derivative-input-manifest.schema.json`; `air.derivative-activation-program.schema.json`; `air.script-segment-lineage.schema.json`; `air.final-script-package.schema.json`; `air.animation-scene-package.schema.json`; `air.activation-transfer-contract.schema.json`; `air.semantic-production-package.schema.json`; `contracts/fixtures/air_f15/` | Schema/model parity, closed unions, positive/negative vectors; no shared release bytes without separate authorization. |
| 5 — adapters | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/adapters/interview_expression_evidence.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/adapters/observed_intelligence.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/adapters/primitive_archetype_brand.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/adapters/pipeline_semantic_package.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/adapters/studio_human_resolution.py` | Preserve owner/lifecycle/limits; no local schema fork, IE write, Pipeline execution or Studio canonical state. |
| 6 — independent evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/evaluation/final_script_evaluator.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/evaluation/animation_scene_semantic_evaluator.py` | All non-compensable dimensions and distinct evaluator identity. |
| 7 — migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/derivative_activation/migrations/studio_story_doctor_to_air_f15.py` | Lossless-or-blocked migration with historical bytes/aliases retained. |
| 8 — tests/evidence | Exact paths in section 10 | Every acceptance criterion, adversarial case, claim ceiling and reference-slice handoff. |

No stage creates or modifies Builder source, Pipeline source, VAE, Delegation, Studio predecessor state, Format 02 artifacts or a production contract release. `VisualRequirementIntent` adoption by Pipeline is a later consumer implementation responsibility.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Condition | Owner / required outcome |
|---|---|---|
| `AIR_DERIVATIVE_DRAFT_INTERFACE_HASH_MISMATCH` | Any AIR-005/006/007/011 pin drifts. | Controller/spec lifecycle: block and reopen sections 3, 5, 6, 8, 9, 10. |
| `AIR_DERIVATIVE_SOURCE_EVIDENCE_MISSING_OR_STALE` | IE source/Moment/Receipt/handoff cannot resolve or is ineligible. | IE/evidence admission: block; never guess or repair locally. |
| `AIR_DERIVATIVE_OBSERVED_CLAIM_EXCEEDED` | Script/program exceeds OAI or underlying maximum claim. | AIR semantic validator: reject/lower claim or obtain eligible successor evidence. |
| `AIR_DERIVATIVE_NEGATIVE_EVIDENCE_DROPPED` | Named rejected/borderline/contradictory evidence is omitted. | Admission: reject frozen manifest. |
| `AIR_DERIVATIVE_SEMANTIC_DEPENDENCY_STALE` | Matrix/coalition/archetype/DNA/profile ref is stale or invalid. | Dependency resolver: block before authoring. |
| `AIR_DERIVATIVE_LINEAGE_FLATTENED` | Required contracts become notes, labels or ID-only arrays. | Schema/adapter: reject as semantically incompatible. |
| `AIR_DERIVATIVE_PRIMITIVE_COALITION_INCOMPLETE` | Roles, conflicts, exclusions, misuse, signature or Edge Product evidence is absent. | AIR-005 boundary: reject; no list-only fallback. |
| `AIR_DERIVATIVE_ROLE_TENSION_OR_ARCHETYPE_INVALID` | Role/tension is generic, primary count invalid, or archetype geometry conflicts. | AIR-006 boundary: reject or repair upstream. |
| `AIR_DERIVATIVE_BRAND_CONTEXT_AMBIGUOUS` | Zero/multiple active Brand Context versions or mixed Voice/Visual refs. | AIR-007 boundary: block exact resolution. |
| `AIR_DERIVATIVE_VERBATIM_MISMATCH` | Claimed verbatim bytes/offsets/speaker/hash differ. | Segment admission: reject and preserve proposal/source bytes. |
| `AIR_DERIVATIVE_TRANSFORMATION_LINEAGE_MISSING` | Condensation/adaptation/rewrite lacks source, operation, Voice DNA or authoring ref. | Segment admission: reject. |
| `AIR_DERIVATIVE_GENERIC_OR_CENTROID_SCRIPT` | Script is source-interchangeable or loses Edge/role/archetype force. | Evaluation: non-compensable reject. |
| `AIR_DERIVATIVE_PRIMITIVE_MISUSE` | Exact F15 Primitive trigger/suppression/misuse/conflict fails. | Responsible semantic layer: reject or issue bounded repair. |
| `AIR_DERIVATIVE_WRONG_READING_WEAKENED` | Descendant removes or relaxes parent lock. | Validator: reject; only authorized upstream successor can relax. |
| `AIR_DERIVATIVE_NA_INVALID` | Required dimension is N/A or lacks profile/evidence. | Schema/evaluator: reject. |
| `AIR_DERIVATIVE_EVALUATOR_NOT_INDEPENDENT` | Producer and evaluator identities/authority context conflict. | Evaluation gateway: reject eligibility. |
| `AIR_DERIVATIVE_OPERATOR_APPROVAL_REQUIRED` | Composition/scene/package requested without exact operator approval. | Lifecycle: retain candidate; block all composition descendants. |
| `AIR_DERIVATIVE_HIDDEN_UI_APPROVAL` | Projection/direct manipulation attempts canonical state mutation. | Studio adapter: reject and restore projection. |
| `AIR_DERIVATIVE_SCENE_PACKAGE_INCOMPLETE` | Eligible script lacks reusable scenes or required semantic fields. | Scene compiler: block package publication. |
| `AIR_DERIVATIVE_VAD_AUTHORITY_LEAK` | AIR emits an authoritative Visual Asset Demand. | Architecture gate: reject; retain semantic requirement intent only. |
| `AIR_DERIVATIVE_PRODUCTION_STRATEGY_LEAK` | AIR scene contains provider/model/LoRA/workflow selection. | Architecture gate: reject; VAE owns that decision. |
| `AIR_DERIVATIVE_CATEGORY_PROFILE_UNSUPPORTED` | Category/profile/features incompatible or certification is overstated. | Compatibility: reject without hidden fallback. |
| `AIR_DERIVATIVE_FORMAT02_DEFERRED` | Any path activates/inherits Format 02 certification. | Policy: deny request. |
| `AIR_DERIVATIVE_IDEMPOTENCY_CONFLICT` | Same key, different canonical command/dependency bytes. | Repository: return conflict; write nothing. |
| `AIR_DERIVATIVE_CONCURRENT_MODIFICATION` | Expected stream version is stale. | Repository: return exact current head; write nothing. |
| `AIR_DERIVATIVE_ATOMIC_COMMIT_FAILED` | Any artifact/event/edge/receipt/alias/outbox member fails. | Repository: roll back all staged state. |
| `AIR_DERIVATIVE_LATE_RESULT_STALE` | Proposal/evaluation arrives after cancel/supersession/dependency change. | Orchestration: quarantine as noncanonical evidence. |
| `AIR_DERIVATIVE_MIGRATION_MEANING_MISSING` | Legacy state lacks required source/role/coalition/DNA/approval/locks. | Migration: preserve bytes and emit blocker; infer nothing. |

Failure records contain safe exact refs/hashes, field/invariant, owner, retryability, responsible repair layer, affected descendants and next admissible action. They do not log unrestricted source text, human-sensitive observations, secrets, absolute paths or provider payloads.

### 8.2 Retry versus semantic repair

Transport/storage failures may retry identical bytes under the same idempotency key. A model/evaluator retry is separately stored with exact response bytes and pinned binding. Source gaps, stale dependencies, lineage failure, claim-ceiling excess, genericity, Primitive misuse, archetype conflict, DNA drift, wrong-reading weakening, evaluator disagreement and missing operator approval are semantic failures. They require a new evidence, proposal, evaluation or operator-resolution command; changing a seed is not repair.

### 8.3 Migration and compatibility

- Compatibility is semantic, not parse-only. Consumers/adapters preserve and enforce owner, exact refs/hashes, lifecycle-at-use, epistemic/max claim, limitations, adverse evidence, coalition roles/conflicts, archetype geometry, DNA, transforms, approval, locks, transfer and invalidation.
- Migration creates new immutable candidate artifacts linked by `migrated_from`. Historical UUID/time/path values remain attachments; they do not enter new canonical identity.
- Predecessor default Expression Moments, generic Edge text, score-max archetype choice, delivery recipes, invented source timing and Format 02 route cannot be promoted automatically.
- Missing source classification, transformation class, approval or semantic constraint is never guessed. The outcome is `MIGRATED_CANDIDATE_PENDING_EVALUATION` or `BLOCKED_REQUIRED_MEANING_MISSING`.
- Active historical consumer handoffs remain pinned to negotiated versions. Deprecation does not corrupt historical replay.

### 8.4 Rollback, cancellation and recovery

Deployment rollback selects a last-known-good implementation/profile for new commands while preserving artifacts produced under every prior binding. Transaction rollback removes only uncommitted staging. Recovery verifies command/artifact/event/edge/receipt/idempotency/alias/outbox parity and either completes the identical prepared transaction when every precondition still holds or records a rollback incident; it cannot synthesize a receipt.

Cancellation racing with commit has two legal outcomes: cancel wins and no candidate transition commits, or commit wins and a later additive cancellation/invalidation record is appended. Late provider/evaluator results never change current state. Selective invalidation follows typed material edges and retains unaffected scripts/scenes/packages.

### 8.5 Observability

Structured events contain command/transaction/case IDs, exact ref/hash sets, owner/lifecycle state, category/profile, proposal/evaluator binding, finding/reason codes, segment transformation counts, Primitive decision codes, operator-decision state, scene/reuse counts, stream version, idempotent replay, commit outcome and invalidation fan-out. Metrics include source admission failures, observed-claim bounds, flattened-lineage denials, genericity, verbatim mismatch, transformation gaps, Primitive misuse, DNA mismatch, approval wait time, evaluator disagreement, scene completeness, VAD/production-strategy boundary denials, N/A misuse, rollback/recovery and replay divergence. Metrics are operational evidence, not semantic authority or certification.

## 9. Behavior-specific acceptance criteria

### AC-01 — AIR-FR-085 / AIR-ST-15.01: compile one complete Derivative Activation Program

**Given** exact approved source, Moment, campaign role, objective and eligible AIR semantic dependencies, **when** the program compiles, **then** it declares category/profile, source ingredients, role/tension, Matrix, coalition/signature/Edge, archetype, Brand/Voice/Visual, observed binding, transfer, locks and evaluation requirements without flattening. **Failure example:** `primitive_ids` plus `archetype: witness` and generic notes fails. **Evidence:** input manifest, program and dependency graph. **Layer:** domain/contract/integration.

### AC-02 — AIR-FR-086 / AIR-ST-15.01: bounded JIT Writer and Composer context

**Given** an authoring-eligible program, **when** a Writer or Composer request is issued, **then** it contains approved ingredients only, exact Voice DNA, coalition/archetype, route/category rules, transformation classes, maximum claim, locks and least-privilege tools. **Failure example:** unrestricted transcript/current-latest context or a cross-product write grant fails. **Evidence:** context-diff and tool-grant receipt. **Layer:** unit/security/integration.

### AC-03 — AIR-FR-087 / AIR-ST-15.02: preserve every script-segment transformation

**Given** a proposal containing verbatim, condensation, bridge and rewrite segments, **when** admission runs, **then** each segment has exact source spans as applicable, transformation class/operations, authoring program, Voice DNA application, epistemic/claim state and approval lifecycle. **Failure example:** a one-word-changed quote marked verbatim fails `AIR_DERIVATIVE_VERBATIM_MISMATCH`. **Evidence:** segment crosswalk and denial receipt. **Layer:** unit/contract/adversarial.

### AC-04 — AIR-FR-088 / AIR-ST-15.02: attributable operator approval

**Given** a deterministically valid, independently evaluated candidate, **when** an attributable operator approves exact bytes, **then** one immutable approved successor and approval receipt are committed. **Failure example:** evaluator pass, model confidence or UI toggle without operator command remains noneligible. **Evidence:** evaluation, HumanResolution and approval receipt. **Layer:** authority/integration.

### AC-05 — FR-167 / ST-12.03: no composition before approval

**Given** a draft or evaluated-but-unapproved script, **when** Composition IR, VideoEditProgram, animation execution program, authoritative Visual Asset Demand or renderer workspace is requested, **then** the request fails `AIR_DERIVATIVE_OPERATOR_APPROVAL_REQUIRED` before downstream work. **Failure example:** a renderer-ready layout cannot conceal the missing script gate. **Evidence:** cross-product denial receipt. **Layer:** architecture/integration.

### AC-06 — AIR-FR-089 / AIR-ST-15.03: reusable scene package for every eligible script

**Given** an approved eligible Final Script, **when** scene compilation runs, **then** at least one reusable semantic scene records script/source refs, role/tension movement, sequence role, timing/BBOX-with-WHY, composition intent, identity/continuity, visual requirements, locks and reuse roles. **Failure example:** `animation_not_current_output` cannot omit the package; it may only set `DEFER_RENDER_PRESERVE_PACKAGE`. **Evidence:** scene package and completeness receipt. **Layer:** domain/integration.

### AC-07 — AIR-FR-090 / AIR-ST-15.03: immutable Semantic Production Package

**Given** exact approved script, scene package and transfer contract, **when** publication runs, **then** one immutable package binds full source/observed/Matrix/Primitive/archetype/DNA/RSCS/CCV/SDA/SFL/evaluation/approval/lock lineage for Builder and Pipeline consumption. **Failure example:** a package missing rejected evidence or using latest aliases fails. **Evidence:** package, hash and consumer validation receipt. **Layer:** contract/integration.

### AC-08 — source-kind and observed-evidence sovereignty

**Given** IE-owned source/Moment/Reaction evidence and AIR-011 observed intelligence, **when** admitted, **then** owners, exact bytes, lifecycle-at-use, maximum claim, adverse evidence and limitations remain unchanged. **Failure example:** AIR relabels an inferred role as observed or reconstructs a missing Reaction Receipt. **Evidence:** owner/hash crosswalk and claim-bound denial. **Layer:** adapter/architecture.

### AC-09 — complete Primitive coalition preservation

**Given** AIR-005 coalition/signature/Edge refs, **when** a derivative compiles, **then** every role, relation, conflict, exclusion, suppression, misuse, fatality/routeability and evaluation ref is reachable from the program. **Failure example:** three Primitive IDs with no local functions or conflict decision fails. **Evidence:** graph coverage receipt. **Layer:** contract/integration.

### AC-10 — psychological role and archetype coalition preservation

**Given** AIR-006 role/tension and archetype program, **when** script/scene functions are compiled, **then** role, tension, recognition, stance, movement, counteractivation, transfer invariants, one primary archetype, bounded support/transition roles, exclusions and SDA/SFL refs survive. **Failure example:** a theme label or multiple primaries fails. **Evidence:** semantic reparse and archetype receipt. **Layer:** integration/adversarial.

### AC-11 — Brand Context, Voice DNA and Visual DNA coherence

**Given** AIR-007 exact Brand Context and separate DNA contracts, **when** text and scene intents compile, **then** non-verbatim text is Voice constrained, visual intent is Visual constrained, both share one active context, and neither overwrites role/tension or source truth. **Failure example:** `style: authentic premium` or mixed context versions fails. **Evidence:** DNA application/cross-context denial receipts. **Layer:** contract/integration.

### AC-12 — exact F15 Primitive CBAR

**Given** the three exact Primitive YAMLs, **when** candidate script/scenes are evaluated, **then** PRM-VOC-009 requires source-specific sensory anchors without overload/genericity/manipulation; PRM-VSG-003 ties style to intent without lazy default/inconsistency; PRM-PRS-015 preserves grounded What Is/What Could Be oscillation without hype or demoralization. **Failure example:** fashionable but intentless scenes or utopian copy fail even when aesthetically strong. **Evidence:** per-Primitive binding and misuse receipts. **Layer:** CBAR/adversarial.

### AC-13 — RSCS, CCV, anti-centroid and rejected alternatives

**Given** dense source expression and multiple authoring candidates, **when** Final Script evaluation runs, **then** ordered RSCS layers, declared CCV axes, source reality contact, rejected centroid candidates and independent comparison remain inspectable. **Failure example:** three seed-only generic variants fail. **Evidence:** Distillation Trace, coordinate matrix and rejection corpus. **Layer:** property/integration.

### AC-14 — wrong-reading lock monotonicity

**Given** source/OAI/coalition/archetype/DNA parent locks, **when** a script, scene or package is created, **then** all parent locks are inherited and any additions are strictly stronger. **Failure example:** a scene removes a source-fidelity lock to fit a visual concept. **Evidence:** parent-child lock diff. **Layer:** unit/contract.

### AC-15 — Visual Asset Demand and VAE authority boundary

**Given** a scene needing a missing visual ingredient, **when** AIR compiles it, **then** AIR emits only a `VisualRequirementIntent` marked nonauthoritative; Pipeline later owns authoritative demand emission and VAE owns production strategy. **Failure example:** AIR selects a model/LoRA or emits Delegation demand bytes. **Evidence:** import/schema boundary denial. **Layer:** architecture.

### AC-16 — category/profile truth and Format 02 deferral

**Given** a target category/profile, **when** compatibility checks run, **then** exact feature support and current certification state are preserved; unsupported requirements fail. **Failure example:** an old `compile_format02_packet` route or Format 02 certification is inferred into this package. **Evidence:** compatibility and Format 02 exclusion receipts. **Layer:** contract/policy.

### AC-17 — evidence-bearing `NOT_APPLICABLE`

**Given** a conditional evaluation dimension, **when** N/A is claimed, **then** the exact profile rule, condition and evidence are present. Required source, role/tension, coalition, transformed-text Voice DNA, approval, locks and transfer dimensions reject N/A. **Failure example:** empty arrays or `not_applicable: true` fail. **Evidence:** schema/evaluator receipt. **Layer:** unit/adversarial.

### AC-18 — deterministic identity and portability

**Given** identical frozen inputs, **when** compilation runs in fresh processes and roots with changed clock/random/environment/locale/order, **then** manifests, programs, scripts, scenes, packages and receipts are byte-identical. **Failure example:** absolute path, timestamp or traversal order changes a hash. **Evidence:** canonical vector matrix. **Layer:** determinism/clean environment.

### AC-19 — atomicity, idempotency and optimistic concurrency

**Given** fault injection at every commit member plus exact retry and concurrent expected-version commands, **when** commit runs, **then** all command/artifact/event/edge/receipt/idempotency/alias/outbox members are visible or none; exact retry returns original result; only one concurrent writer wins. **Failure example:** script without receipt or approval without exact script is impossible. **Evidence:** transaction/race trace. **Layer:** repository.

### AC-20 — replay, supersession and selective invalidation

**Given** an approved package and a material upstream successor, **when** dependency analysis runs, **then** only typed material descendants become stale, unrelated branches remain eligible and exact history replays without current models/latest refs. **Failure example:** deleting prior scenes or invalidating every derivative fails. **Evidence:** invalidation graph and historical replay hashes. **Layer:** recovery.

### AC-21 — producer/evaluator/approver separation

**Given** one producer, evaluator and operator decision, **when** identities and authority are inspected, **then** evaluator is independent and approval is attributable/scoped. **Failure example:** producer self-evaluation or evaluator self-approval fails. **Evidence:** identity/authority receipt. **Layer:** architecture/security.

### AC-22 — candidate-authority claim ceiling

**Given** pending V2.1 ratification, **when** writer completion and later lifecycle projection are evaluated, **then** this spec is `WRITTEN_PENDING_AUDIT`, candidate authority is `CANDIDATE_NOT_CURRENT`, specification work is authorized, build is false and the ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. **Failure example:** `ACCEPTED_FOR_BUILD`, capsule or production claim fails. **Evidence:** lifecycle policy test. **Layer:** governance.

## 10. Testing and completion evidence

### 10.1 Exact future test paths

| Exact path | Required tests and evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_input_manifest.py` | Owner/lifecycle/max-claim/adverse-evidence completeness, exact sorting, OAI present/no-pack union and stale denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_program_compiler.py` | All seven FR dependencies, full coalition/role/DNA lineage, category admission and no flattening. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_script_segment_lineage.py` | Six transformation classes, byte/offset verbatim checks, bridge constraints, Voice DNA and epistemic/claim state. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_final_script_lifecycle.py` | Every legal/illegal state, independent evaluation, operator approval, supersession and composition denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_animation_scene_package.py` | Scene roles, timing/BBOX-with-WHY, composition intent, reuse, render deferral and required package completeness. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/derivative_activation/test_wrong_reading_inheritance.py` | Parent lock preservation, stricter additions and relaxation denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/serialization/test_air_f15_canonical_hash.py` | Clock/random/env/path/locale/insertion/traversal independence and ordered-vs-set-like behavior. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f15_schemas.py` | Closed schema/model parity, unknown-field rejection, lifecycle variants, N/A union and positive/negative examples. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f15_upstream_interfaces.py` | Exact AIR-005/006/007/011 pins, owners, lifecycle, semantic enforcement and no local forks. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/cbar/test_air_f15_active_primitives.py` | Exact PRM-VOC-009, PRM-VSG-003, PRM-PRS-015 hashes, trigger/suppression/misuse/conflict and downstream denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_derivative_activation_final_scripts_and_animation_scene_packages.py` | AIR-ST-15.01–15.03, AIR-FR-085–090 complete workflow with typed blockers. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_fr167_final_script_before_composition.py` | ST-12.03/FR-167 denial of Composition IR, VideoEditProgram, animation execution, VAD and renderer workspace before approval. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_air_f15_atomic_repository.py` | Fault at every commit member, response-loss retry, idempotency collision, optimistic race and receipt/artifact parity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_air_f15_jit_authoring.py` | Least context, exact proposal storage, deterministic baseline comparison, unsupported tool denial and no hidden approval. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_air_f15_independent_evaluation.py` | All mandatory dimensions, non-compensable failures, N/A law and producer/evaluator separation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_air_f15_product_authority_boundaries.py` | IE/AIR/Builder/Pipeline/VAE/Studio/Delegation/Evaluation ownership, no VAD/provider/LoRA leak, no generic approval authority. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_studio_story_doctor_to_air_f15.py` | Exact historical preservation, defaults/heuristics/Format 02 denial and lossless-or-blocked result. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_air_f15_replay_cancellation_invalidation.py` | Both cancellation race orderings, late results, selective invalidation, exact historical replay and first divergence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_air_f15_portability.py` | Clean extracted layout; no undeclared file, absolute path, environment, current-time or random dependency. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_imported_interview_to_semantic_production_package.py` | Source package → IE evidence → OAI → coalition/archetype/DNA → approved Final Script → scene package → transfer/package. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_air_f15_pipeline_handoff.py` | Pipeline exact consumption/rejection, no semantic reinterpretation, Pipeline-owned VAD compilation and stale-package denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/regression/test_studio_story_doctor_f15_predecessor_cases.py` | Port useful source-span/derivative cases while proving heuristic defaults and mutable behavior are not restored. |

### 10.2 Required adversarial corpus

The suite must include missing/ambiguous/stale source; unknown source kind; invented Reaction Receipt; unapproved Moment; omitted negative evidence; OAI claim-ceiling excess; planned claim represented as observed; stale Matrix/coalition/archetype/DNA; Primitive ID list with no roles; coalition fatality; multiple primary archetypes; generic role/tension; mixed Brand Context; generic Voice; altered quote marked verbatim; transformation without source; operator bridge introducing a source claim; compression before saturation; seed-only CCV; centroid script; source-interchangeable sensory cue; sensory overload/manipulation; intentless style; brand inconsistency; utopian What-Could-Be; demoralizing What-Is; weakened wrong-reading lock; invalid N/A; producer self-evaluation; missing operator approval; hidden UI mutation; no scene package; scene with no BBOX WHY; AIR-emitted VAD; AIR model/LoRA selection; unsupported category/profile; Format 02 activation; current-time/random UUID/absolute path; insertion/traversal drift; partial commit; idempotency conflict; stale expected version; cancellation/late result; invalidation overreach; lossy migration; and unauthorized acceptance/build/capsule/production claim.

### 10.3 Completion evidence and handoff ceiling

Future implementation completion requires:

- exact ratified/adopted authority and independently accepted hashes for this spec and all four upstream interfaces;
- a bounded Development Capsule with exact source/Primitive/predecessor/test/target-path locks;
- schema/model/generated-type parity and canonical positive/negative fixture hashes;
- requirement-to-code/test/receipt traceability for all seven FRs and four Stories;
- per-Primitive CBAR, source/observed evidence, coalition/archetype/DNA and wrong-reading conformance matrices;
- independent evaluator evidence and attributable operator approval fixtures;
- atomicity, idempotency, concurrency, cancellation, replay, migration, selective invalidation and clean-environment proofs;
- full tests twice in fresh processes plus source compilation/type checks;
- imported-interview reference-slice and Pipeline consumer conformance without semantic reinterpretation;
- independent Tech Spec audit, revision if required and independent re-audit by agents other than this writer.

A future Build Receipt must bind ratified authority, accepted specs, exact capsule, implementation revision, source/Primitive/profile locks, test/evaluation/migration/replay evidence and the supported claim ceiling. This document issues no Build Receipt or capsule.

Final writer state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later acceptance ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. The next admissible lifecycle action is independent Tech Spec audit by a different agent.
