---
document_type: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-016
title: Activation Transfer Fidelity and Source Fidelity
product: Activative Intelligence Runtime
version: 2.1.0-candidate
issued_on: '2026-07-22'
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_build_gate: RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs:
  - AIR-FR-091
  - AIR-FR-092
  - AIR-FR-093
  - AIR-FR-094
  - AIR-FR-095
  - AIR-FR-096
  - FR-168
  - FR-180
controlling_stories:
  - AIR-ST-16.01
  - AIR-ST-16.02
  - AIR-ST-16.03
  - ST-12.04
  - ST-13.04
upstream_draft_dependencies:
  - edge_id: SDE-039
    spec_id: TS-AIR-015
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-016 — Activation Transfer Fidelity and Source Fidelity

## 1. Files and authorities read

### 1.1 Governing authority, authorization, and writing controls

| Class | Exact path | State / bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624 bytes; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten required sections, exact evidence and draft-dependency law. |
| Source-package instructions | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/AGENTS.md` | 1,911 bytes; `fb2836248358c69474cef24d925608534e7da87ec88041b3e9d660039fcc4732` | Requires current authority, feature, Stories, Primitives and named sources before normative writing. |
| Highest current authority | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; 40,830 bytes; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Human reaction and source-backed Expression Moments precede derivatives; wrong-reading locks, semantic lineage, composition and T/V responsibilities remain governed. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION`; 1,288 bytes; `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | The V2.1 bundle is additive and does not silently supersede current authority. |
| Candidate Constitution | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`; 51,243 bytes; `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | AIR owns transfer meaning; exact source packages and Expression Moments are lineage roots; transfer preserves pressure, role, tension and recognition rather than wording alone. |
| Semantic ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate; 4,263 bytes; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns Activation Transfer meaning; IE owns source evidence; Pipeline executes; VAE realizes demands; Independent Evaluation owns evaluation receipts. |
| Product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate; 4,289 bytes; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Products may consume exact objects but cannot seize another product's semantic or execution authority. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | active; 1,221 bytes; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate authority remains non-current; specification work is authorized; build and capsules are prohibited. |
| Write authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification work only; 1,462 bytes; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Permits WRITE through technical convergence with the stated pre-ratification ceiling. |
| Recovery packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 bytes; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-AIR-016-RECOVERY` freezes eight FRs, five Stories, this path and one draft dependency. |
| Wave dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_10_DISPATCH_LOCK.yaml` | `DISPATCHED`; 613 bytes; `5f30228d93e1d5686ebb502721adb1d011ef9fe2353e8d10cb5d58b68ef30a00` | Admits exactly the pinned TS-AIR-015 draft for Wave 10. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated; 134,201 bytes; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Required unique transfer, Matrix, archetype, brand, creative, RSCS and coalition sources are available; source-first V1.1 is superseded history. |
| Source gaps | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_GAP_NOTICE.yaml` | governed; 17,743 bytes; `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | No unavailable source is promoted to authority for this spec. |
| Canonical FR ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | frozen; 104,516 bytes; `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns AIR-FR-091–096, FR-168 and FR-180 to AIR/TS-AIR-016. |
| Canonical traceability | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen; 236,715 bytes; `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Supplies exact requirement text, Stories, source IDs, gates and evidence ceilings. |
| Canonical spec ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | frozen; 23,269 bytes; `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Reserves this direct AIR path and the eight-FR/five-Story packet. |
| Dependency classification | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | corrected; 107,141 bytes; `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | SDE-039 is a WRITE interface dependency, not an acceptance or build gate. |
| Path authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | validated; 18,768 bytes; `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | This path is a permitted `DIRECT_PRODUCT_SPEC_PATH`; no nearer target or ancestor `AGENTS.md` applies. |

### 1.2 Controlling feature, Stories, doctrine, and predecessor evidence

| Class / ID | Exact path | Bytes / SHA-256 | Specific fact used |
|---|---|---|---|
| F16 feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F16-activation-transfer-fidelity-and-source-fidelity.md` | 41,953; `e637f444d4a3c0683a4420a6b7b0c869b14d053f9174cda674cb7730620e2acc` | Six AIR FRs require a versioned contract, must-survive properties, explicit transformation freedom, every material handoff, full lineage and wrong-role/centroid denial. |
| AIR Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-16.01–16.03 require exact source/evidence, typed blockers, selective recovery and three exact Primitive mandates. |
| Donor full draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-016-activation-transfer-fidelity-and-source-fidelity.md` | 28,869; `2aa4f37ba4d07efe43db34674c385d88bbf8a8c245ddda65d26145b7a14caf54` | Candidate baseline; amended here for FR-168/FR-180, current ownership, exact upstream contract, strict models and V3.3 evidence. |
| Activation Transfer seed | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/contracts/07_ACTIVATION_TRANSFER_CONTRACT.md` (`SRC-AI2-TRANSFER-001`) | 414; `9a84914ced08453701b150f4d1f3720f8aef688870bc0016bd551a774a5e1580` | Requires source package/Moment refs, generator, roles, invariants, changes, degrees of freedom, compression, collapses, locks, format and evaluation. |
| AHP evaluation/repair | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/AHP_F16_EVALUATION_REPAIR.md` (`SRC-AHP-F16-001`) | 18,469; `0a247a2025ef803df09e8bfc97b9456d73a64cf2f867598135b3c8ba03a668e2` | Deterministic facts and independent judgments remain separate; failures are attributed; repair changes declared dependent units only. |
| AHP Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-12.04 requires full lineage across embodiments; ST-13.04 requires source force, Negative Space and Edge Integrity proof. |
| AHP role/lineage feature | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | 14,624; `0a130c459707e309ae323f769b00d0f82f866b8bfddf6eb42546a5de4f78370c` | FR-168 requires role, tension, coalition and approved Final Script lineage through every embodiment. |
| AHP brand/edge feature | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F30-brand-genesis-voice-visual-dna-distillation-and-anti-centroid-integrity.md` | 14,697; `20765b8509550271f43590293cd3f95387c892c69240ae9d41c5dd1c32d9deb5` | FR-180 requires Source Fidelity, Negative Space and Edge Integrity across every handoff. |
| Matrix doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/MATRIX_OF_EDGING.md` (`SRC-DOCT-001`) | 15,982; `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | An edge is a high-magnitude tension site, not a topic; the Edge Product emerges after evidence and coalition work. |
| Archetype doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_ARCHETYPE_SYSTEM_MIGRATION_PROPOSITION.md` (`SRC-DOCT-002`) | 35,537; `2d7aa11b72c83a95d9240784978e3b9af4944a3e037f18746f8b204bc3287188` | Archetypes are meaning grammars; historical prompts do not become current semantic authority. |
| Brand doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` (`SRC-DOCT-003`) | 45,066; `61710fe56484b569ce28ddefadbb4c8047e9ae48cadf25291423cf4f200e3dcb` | One frozen Brand Context Version binds separate Voice and Visual DNA obligations. |
| Creative architecture | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_CREATIVE_PIPELINE_ARCHITECTURE_V2.md` (`SRC-DOCT-004`) | 61,539; `8b9175d8631eff50b7f6c959ad245b87f9b307577b51e6dd4d2f622fd44175e8` | Composition and execution preserve approved source/semantic programs rather than inventing meaning during editing. |
| RSCS doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/RSCS_RECURSIVE_SIGNAL_COMPRESSION_SYSTEMS.md` (`SRC-DOCT-006`) | 29,832; `bb8ebfcd5c519649b4363731cf11434ce600c71fb5e1d020abb59cbb51b8a330` | Compression is an evaluated transformation, not permission to remove the source charge or tension. |
| Coalition brownfield | `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/primitive_coalition.py` (`SRC-DOCT-009`) | 8,681; `990735d588e03004cbee780cea7e3623361a7fa70991e898ff13f173618cbf08` | Rich coalition shape and hash behavior are useful evidence; local random IDs and fixed thresholds are not imported as AIR law. |
| Superseded predecessor | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` (`SRC-SOURCE-FIRST-001`) | 517,771; `cc1cfa721238b999adb1612e805fad60c61c07c566df19d5044fc9e069651508` | Historical source-first context only; disposition forbids using it as current authority. |
| Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | 5,950; `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7` | Matching Principle preserves the active practical/emotional/social layer and forbids performative or inflexible matching. |
| Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | 5,071; `2be2e140588e23e43b4461c9443884b09401f6541ea29bdbae8e945e4672e30c` | Intent Governs Style; bland default or uncontrolled brand inconsistency are misuse. |
| Primitive | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | 8,179; `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Punctum, Air and Felt Truth protects lived-in evidence while forbidding manufactured messiness, distracting flaws and clarity sacrifice. |

### 1.3 Admitted draft interface

| Edge | Exact path | State / bytes / SHA-256 | Interface consumed | Revision impact if hash changes |
|---|---|---|---|---|
| SDE-039 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md` | `WRITTEN_PENDING_AUDIT`; 93,219 bytes; `58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact source/OAI/Matrix/Primitive/role/archetype/DNA/Final Script/scene lineage; `ActivationTransferContract` and `SemanticProductionPackage` handoff. | Sections 3, 5, 6, 8, 9 and 10. |

The upstream draft is not accepted authority. Its Section 6.8 is an abbreviated inventory of the same candidate `ca.air.activation-transfer-contract/2.1.0-candidate` object. This spec elaborates that object’s required fields and checkpoint behavior; it does not create a second contract. Independent audit must confirm the two draft interfaces converge. A changed upstream hash reopens every listed section before any downstream write may rely on it.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure

A derivative can remain factually related to a source and still destroy what made the source activative. Literal words may survive while the reaction tail disappears; an edit may reverse the audience’s psychological role; a crop may eliminate the separation carried by Negative Space; a polished render may neutralize the Edge Product; an animation may imitate the surface while dropping the Primitive coalition; or a platform adaptation may call authored connective language a quote. Without one immutable transfer contract and evidence at every material handoff, these failures are discovered late, blamed on the wrong product, or “repaired” by rewriting valid source truth.

### 2.2 User and system outcome

An operator can inspect one versioned contract that says what produced the original charge, what must survive, what must change, what may change, what is forbidden, which wrong readings invalidate the derivative, and how each handoff is evaluated. Every assertion, quote, caption, scene, visual proof, voiceover and animation element remains traceable to exact source spans or is explicitly labeled authored connective material. A failure names its checkpoint, violated obligation, responsible owner, safe repair boundary and next admissible action. Valid upstream evidence and unrelated downstream work remain unchanged.

### 2.3 Bounded solution

AIR compiles one immutable `ActivationTransferContract` from the exact `SemanticProductionPackage` and approved lineage supplied by TS-AIR-015. It records typed `MustSurviveProperty` and `TransformationRule` records; declares five material `TransferCheckpoint` obligations; admits immutable handoff evidence without becoming the evidence owner; requires independently produced `ActivationTransferEvaluationReceipt` records; attributes `TransferFailure`; and emits a bounded `TransferRepairRequest` to the product that owns the failed unit. AIR never modifies IE source evidence, a Final Script in place, Pipeline runtime state, VAE production state or Studio canonical state.

### 2.4 In scope

- `ActivationTransferContract` compilation and immutable lifecycle;
- semantic premise, identity stance, emotional/cognitive turn, rhythm, reaction tail, visual cue and participation-role must-survive properties;
- full source → Matrix → Primitive coalition/signature/Edge Product → role/tension → archetype → Voice/Visual DNA → approved Final Script → composition → render lineage;
- explicit transformation permissions for condensation, reordering, rewriting, voice substitution, visual abstraction, animation, crop, timing and platform adaptation;
- source-to-moment, moment-to-script, script-to-composition, composition-to-render and render-to-platform evidence checkpoints;
- Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid and wrong-reading evaluation obligations;
- exact Primitive binding applicability, suppression, conflict and misuse checks for PRM-PSY-001, PRM-VSG-003 and PRM-VSG-021;
- deterministic serialization, immutable refs, idempotency, atomic commits, optimistic concurrency, replay, cancellation, supersession and selective invalidation;
- typed cross-product adapters and non-authoritative projections;
- evidence-bearing `NOT_APPLICABLE` only for profile-conditional dimensions.

### 2.5 Out of scope and non-goals

- capturing or changing Interview Expression source, Reaction Receipt or Expression Moment truth;
- creating source spans, source classifications, reactions, operator approvals, Identity DNA or evidence that does not exist;
- compiling Primitive coalitions, archetype coalitions, DNA, Final Scripts or composition meaning again;
- compiling `AtomicHarnessDefinition`, runtime bindings, authoritative Visual Asset Demands or VAE production plans;
- rendering, editing, generation, publication or provider/model/LoRA selection;
- inventing numeric evaluator thresholds; thresholds and categorical gates come only from a pinned, authorized evaluation profile;
- importing predecessor random identifiers, mutable defaults or fixed evaluation thresholds as current AIR behavior;
- generic creative-safety or content-rights approval authority;
- Format 02 activation, VAE Stage 5, production certification or a Development Capsule.

## 3. Governing decisions and constraints

1. **Current authority remains current.** The V1.1 Constitution remains the highest current authority. V2.1 is `CANDIDATE_NOT_CURRENT`; this document may reach only `WRITTEN_PENDING_AUDIT` now and at most `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` before ratification.
2. **AIR owns transfer-program meaning.** AIR owns the authoritative semantic value of the Activation Transfer Contract and its must-survive, transformation and evaluation obligations. This does not make AIR the owner of source evidence, runtime execution or visual production.
3. **Source truth stays with Interview Expression.** Canonical Interview Source Packages, source spans, Reaction Observations/Receipts and Expression Moments remain IE-owned. AIR stores exact immutable refs, owner, version, hash, lifecycle-at-use, epistemic state and route scope. It cannot normalize, merge, relabel, repair, guess or suppress source evidence.
4. **Approved meaning is referenced, not rebuilt.** Matrix result, Primitive Coalition Contract, Coalition Signature, Edge Product, psychological role/tension, archetype coalition, Brand Context Version, Voice DNA, Visual DNA, RSCS/CCV/SDA/SFL, approved Final Script, Composition Intent and scene package remain exact upstream objects. Generic notes or labels are incompatible.
5. **Transfer fidelity is not verbatim fidelity.** Verbatim material may be activatively dead; adaptation may be faithful. Fidelity means preserving the required pressure, role, tension, recognition, Edge Product, source claim and evidence boundaries while obeying explicit transformation rules.
6. **Every material handoff is visible.** Source-to-moment, moment-to-script, script-to-composition, composition-to-render and render-to-platform each require exact input/output refs and handoff evidence. A later pass cannot compensate for a missing earlier checkpoint.
7. **Lineage is element-level.** Every content-bearing assertion, script segment, quote, caption, scene, visual proof, voiceover and animation element has exact source span support or the governed `OPERATOR_AUTHORED_CONNECTIVE` classification. “Inspired by source” is not a lineage type.
8. **Psychological role and tension are non-compensable.** A result that preserves topic or words but changes the viewer’s role, neutralizes the tension or erases the Edge Product fails, regardless of aesthetic or engagement scores.
9. **Negative Space and Edge Integrity are semantic.** They are not decoration metrics. Category-specific evidence must show whether separation, gaze, hierarchy, asymmetry, pressure and lived-in specificity survived. A profile-defined `NOT_APPLICABLE` decision must prove why a dimension has no semantic role in that artifact.
10. **Wrong-reading locks are monotonic.** All inherited source, OAI, coalition, archetype, DNA, Final Script, scene and composition locks survive. A descendant may add a stricter lock but may not remove or weaken one. Relaxation requires a new authorized upstream version.
11. **Transformation freedom is explicit.** Each governed transformation is `REQUIRED`, `PERMITTED` or `FORBIDDEN` for a derivative kind and checkpoint. Absence is `UNDECLARED` and blocks that transformation; it is never interpreted as permission.
12. **Compression is evidenced.** Condensation and omission cite exact spans, transformation rationale, RSCS trace and preserved obligations. Compression that removes the reaction tail, role, tension, Edge Product, source caveat or authorship disclosure fails.
13. **Exact Primitive physics remains active.** PRM-PSY-001 preserves the active conversation layer without performative or inflexible matching. PRM-VSG-003 subordinates style to intent without blandness or brand incoherence. PRM-VSG-021 protects lived-in evidence without manufactured messiness, distracting defects or obscured meaning. Exact YAML hashes, trigger/suppression decisions and misuse checks are required.
14. **Independent evaluation owns judgment receipts.** AIR may run deterministic contract checks and request evaluation. A distinct evaluator identity produces judgment receipts. Producer self-approval is prohibited, and capability presence does not imply evaluator certification.
15. **No threshold invention.** Required dimensions and hard failures are contract-defined. Numerical thresholds, if a category requires them, come from an exact authorized evaluation-profile version. Missing calibration returns `AIR_TRANSFER_EVALUATION_PROFILE_UNAVAILABLE`, not a guessed score gate.
16. **Failure attribution is evidence-based.** The responsible owner is assigned only when evidence establishes the failing handoff and unit. Unresolved attribution is `UNRESOLVED` and routes to investigation; it cannot become a convenient blame assignment.
17. **Repair cannot rewrite valid upstream truth.** AIR emits semantic repair constraints. Pipeline owns runtime selective-repair plans and execution; VAE owns visual production repair; IE owns source correction; an AIR-owned semantic defect creates a successor AIR object. Every repair targets the smallest permitted unit and dependent descendants.
18. **Product sovereignty remains exact.** Builder declares dependencies; Pipeline executes approved programs and emits Visual Asset Demands; VAE realizes visual demands; Studio projects/corrects through typed commands and `HumanResolutionEpisode`; Delegation transports; Program Control governs authority/release; Independent Evaluation evaluates. None may mutate the contract’s upstream semantic or source authority.
19. **Activative Contract Compiler is not AIR.** Builder’s structural Activative Contract Compiler may bind the exact transfer dependency but may not calculate source charge, decide transformations or evaluate semantic fidelity.
20. **`NOT_APPLICABLE` is closed and evidenced.** Source lineage, source kind, owner, role/tension, Edge Product, required inherited locks and transfer checkpoints cannot be N/A. Conditional visual/sonic dimensions require a pinned profile rule, applicability reason, evidence and maximum claim. Unknown, absent or unassessed is a blocker.
21. **Canonical identity is portable.** Identity-bearing bytes exclude current time, random state, environment variables, hostname, process ID, locale, insertion/traversal order, absolute paths, provider callback order and mutable aliases. Caller-supplied evidence timestamps remain outside the hashed semantic payload where time is necessary.
22. **Historical evidence is immutable.** Supersession, revocation or invalidation never rewrites the old contract, receipt, derivative or source. Historical exact-version replay remains available.
23. **No authorization inference.** A passing transfer receipt is not production acceptance, downstream consumption authorization, implementation readiness, publication permission or certification.
24. **Draft interface caveat.** TS-AIR-015 is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. This spec’s deeper field definitions are a candidate refinement of the same object, not accepted law. Audit changes to either interface reopen Sections 3, 5, 6, 8, 9 and 10.

## 4. Current brownfield architecture

### 4.1 Current repository state

The intended AIR root currently contains only written candidate Tech Specs under `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/`; it has no admitted AIR source, schema, test, repository or runtime implementation for this feature. The future paths in Section 7 are implementation anchors only. Their presence in this specification does not create directories, authorize code or claim implementation coverage.

| Artifact | Actual behavior | Disposition | Migration constraint |
|---|---|---|---|
| Donor `TS-AIR-016-activation-transfer-fidelity-and-source-fidelity.md` | Names six AIR objects and broad lifecycle/evaluation behavior. | `ADAPT` | Add current ownership, FR-168/FR-180, exact TS-AIR-015 interface, strict contracts, atomic repository and V3.3 evidence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md` | Candidate derivative compiler produces approved Final Script, semantic scene and production package carrying a compact transfer contract. | `CONSUME_HASH_PINNED_DRAFT` | Consume exact bytes and refs; treat its Section 6.8 as an abbreviated projection of the same contract; reopen recorded sections on hash drift. |
| `contracts/07_ACTIVATION_TRANSFER_CONTRACT.md` source seed | Enumerates the minimum semantic bridge into a format harness. | `REUSE_AS_CONTRACT_SEED` | Preserve every listed concept, give each a strict field, and do not treat the seed as a released schema. |
| `AHP_F16_EVALUATION_REPAIR.md` | Separates deterministic checks, independent judgment, attribution and bounded repair. | `ADAPT` | Preserve ownership split; AIR does not take Pipeline repair-plan or evaluator authority. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/primitive_coalition.py` | Provides a rich coalition model, canonical hash helper, random UUID defaults and local fixed thresholds. | `ADAPT_EVIDENCE_ONLY` | Reuse no runtime code now; AIR uses caller-supplied IDs and profile-owned thresholds; Studio remains noncanonical for AIR. |
| Donor `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/transfer.py` | Historical URI named by donor but not materialized or admitted as current implementation evidence. | `ARCHIVE_REFERENCE` | No behavior claim or code reuse is derived from unavailable bytes. The available 414-byte contract seed is the only admitted predecessor transfer contract. |
| Donor `source://ai2_predecessor/reference_implementation/activative_intelligence_v2/compiler.py` | Historical URI named by donor but not materialized or admitted as current implementation evidence. | `ARCHIVE_REFERENCE` | No inferred method, signature or behavior may enter the implementation capsule. |
| `AHP_PRD_V1_1_SOURCE_FIRST.md` | Large historical source-first PRD. | `ARCHIVE_AS_SUPERSEDED` | Preserve hash and provenance; current V1.1 Constitution, V2.1 candidate and current ledgers control this spec. |

### 4.2 Reuse boundary

No current code is silently “activated.” Contract nouns, doctrine, tests described by accepted future capsules and exact source facts may be adapted. Random identifiers, mutable “latest” resolution, local thresholds, open dictionaries, hidden defaults, direct cross-product imports and historical authority assumptions are rejected. Any later reuse requires a Development Capsule with exact source bytes, license/dependency review, behavior comparison and target allowlist.

## 5. Proposed architecture and workflows

### 5.1 Component boundaries

| Component | Owns | Must not do |
|---|---|---|
| `TransferInputAdmissionService` | Verify exact TS-AIR-015 package, source/OAI/semantic refs, owners, versions, hashes, lifecycle-at-use and claim ceilings. | Read mutable aliases, invent missing source evidence or normalize IE objects. |
| `ActivationTransferContractCompiler` | Compile must-survive properties, transformation rules, checkpoints, evaluation obligations, locks and target audience/format into one immutable AIR object. | Compile a Final Script, Harness, execution plan, VAD or VAE production strategy. |
| `SourceTransformationLineageValidator` | Verify element-level source or connective classification, quote accuracy and transformation legality. | Repair source text, decide source truth or relabel unsupported content. |
| `TransferCheckpointService` | Open checkpoint cases and admit exact producer/consumer evidence with typed ownership. | Treat notification, job success or local QA as semantic fidelity. |
| `DeterministicTransferValidator` | Verify refs, hashes, states, permissions, inherited locks, quote bytes, lineage completeness and applicability. | Emit independent judgment or certify an evaluator. |
| `TransferEvaluationGateway` | Persist exact request/binding/profile and receive a separately owned evaluation receipt. | Let the producing service approve itself or invent profile thresholds. |
| `TransferEvaluationAdmissionService` | Validate evaluator independence, profile, evaluated hashes, dimension completeness and verdict consistency. | Change evaluator findings, collapse failed dimensions into an average or promote contested evidence. |
| `TransferFailureAttributionService` | Bind failure to checkpoint, violated contract item, evidence, owner and smallest permissible repair scope. | Guess responsibility when evidence is ambiguous. |
| `TransferRepairRequestCompiler` | Emit semantic constraints and invalidation boundary to the responsible owner. | Build or execute Pipeline/VAE/IE repair plans; mutate upstream objects. |
| `ActivationTransferRepository` | Atomically store immutable commands, artifacts, events, edges, receipts, idempotency records, current aliases and outbox intents. | Partial commits, in-place mutation, receipt/artifact imbalance or path-derived identity. |
| `TransferStatusProjection` | Project current/historical state for Studio and Program Control. | Become canonical state or accept hidden UI mutations. |

Pure domain and compiler modules import no clock, random source, environment, filesystem traversal, network, provider SDK, Pipeline, VAE, Studio, Builder or Delegation implementation module.

### 5.2 Workflow A — compile and activate the transfer contract

1. `CompileActivationTransferContract` provides caller-supplied `command_id`, `idempotency_key`, expected stream version, exact TS-AIR-015 `SemanticProductionPackage` ref/hash and target derivative kind/category/profile/audience segment.
2. Admission resolves the package and its exact source package, Expression Moments, Reaction Receipts where applicable, OAI binding, Matrix, coalition, signature, Edge Product, role/tension, archetype, Brand/Voice/Visual, approved Final Script, composition-intent, scene, transfer seed, evaluation, approval, locks and maximum claim.
3. The compiler derives no new source truth. It maps governed upstream statements into typed `MustSurviveProperty` records and explicit `TransformationRule` records. Every mapped record retains origin refs and epistemic state.
4. The compiler declares all five checkpoints, their producer/consumer owners, required evidence, non-compensable dimensions and authorized evaluation profile refs.
5. Deterministic validation rejects missing lineage, stale refs, owner mismatch, incomplete transformation policy, weakened locks, claim escalation and unproved N/A.
6. One atomic commit stores command, contract, event, dependency edges, receipt, current alias, idempotency result and outbox intent. The contract becomes `ACTIVE` only after its compile receipt passes deterministic admission. It does not authorize production.

### 5.3 Workflow B — source-to-moment and moment-to-script evidence

1. `SOURCE_TO_EXPRESSION_MOMENT` consumes IE-owned source package/span/keyframe/timing/speaker, Reaction Receipt and approved Expression Moment refs. IE supplies evidence; AIR does not regenerate the Moment.
2. The checkpoint proves the selected Moment retains its source context, reaction tail, identity/audience pressure, route authority and epistemic limits. For imported sources, absent planned/live history remains explicitly absent.
3. `EXPRESSION_MOMENT_TO_FINAL_SCRIPT` consumes the exact TS-AIR-015 segment lineage and approved Final Script refs. Verbatim claims are byte/offset exact. Omission, condensation, adaptation, rewrite and operator-authored bridge/connective classifications remain disclosed.
4. A conflict between source and derivative becomes `AIR_TRANSFER_SOURCE_EVIDENCE_CONFLICT`. The corrective action is a new source resolution or derivative successor from the owning product, never an AIR edit to source evidence.

### 5.4 Workflow C — script-to-composition and composition-to-render evidence

1. `FINAL_SCRIPT_TO_COMPOSITION` binds the exact approved Final Script, AIR-owned Composition Intent, category-native semantic production package and Pipeline-compiled composition program.
2. Pipeline may execute the approved program and emit authoritative Visual Asset Demands. It returns exact program/version/hash, input bindings, deterministic validation and composition evidence. It cannot reinterpret source, Edge Product, coalition, role/tension or Final Script.
3. `COMPOSITION_TO_RENDER` binds the approved composition program, exact source/asset bindings, VAD versions, VAE delivery/result refs where applicable, render evidence and observed composition/temporal reparse.
4. VAE controls provider, model, LoRA, conditioning, candidate generation, production evaluation and targeted production repair. The transfer contract constrains semantic acceptance but does not select those production methods.
5. Negative Space, Edge Integrity, source-media role, hierarchy, gaze, separation, asymmetry, punctum/felt truth and wrong-reading evidence are evaluated under the pinned category profile. Attractive polish cannot compensate for a failed semantic dimension.

### 5.5 Workflow D — render-to-platform evidence

1. `RENDER_TO_PLATFORM` binds exact accepted render/result bytes, export/transcode/crop/caption/timing transformations, platform profile and published-candidate bytes.
2. Deterministic checks verify no unauthorized crop, aspect/timing change, quote mutation, source attribution loss, caption drift, color/audio substitution or metadata downgrade violates the contract.
3. Independent evaluation covers remaining judgment dimensions under an exact platform/category profile. Publication is still a separate human/product authority action.
4. A platform variant is a new immutable descendant with its own lineage and receipt. It never replaces the master or silently inherits production/certification claims.

### 5.6 Workflow E — independent evaluation, failure attribution and repair request

1. `RequestTransferEvaluation` freezes contract, checkpoint, candidate/evidence hashes, evaluator binding and evaluation profile. Deterministic blockers run before judgment.
2. A distinct evaluator returns one outcome for every required dimension: `PASS`, `FAIL`, `NOT_APPLICABLE` or `NEEDS_MORE_EVIDENCE`, each with reason/evidence refs. N/A must carry the exact applicability rule.
3. `ApplyTransferEvaluation` verifies producer/evaluator separation, exact evaluated bytes, complete dimensions and profile certification state. The service records, but does not rewrite, findings.
4. A mandatory `FAIL` or `NEEDS_MORE_EVIDENCE` prevents checkpoint pass. No aggregate score can compensate. `CONTESTED` evidence routes to attributable human resolution without becoming a pass.
5. Failure attribution names one of `SOURCE_EVIDENCE`, `AIR_SEMANTIC_PROGRAM`, `BUILDER_DEPENDENCY`, `PIPELINE_COMPOSITION_OR_RUNTIME`, `VAE_PRODUCTION`, `PLATFORM_ADAPTATION`, `EVALUATION`, `HUMAN_DECISION` or `UNRESOLVED` and cites evidence.
6. `IssueTransferRepairRequest` names only the failed unit, dependent invalidation boundary, preserved refs, prohibited mutations, required re-evidence and owner. Pipeline/VAE/IE/AIR then use their own governed lifecycle to create successor artifacts.

### 5.7 Supersession, invalidation, cancellation, idempotency and replay

- Contracts and evidence are immutable. Any material change creates a successor and `supersedes_ref`.
- A source package/Moment/Reaction/OAI/Matrix/coalition/archetype/DNA/Final Script/composition/profile successor does not rewrite accepted work. New work may choose an eligible successor; active accepted delegations remain pinned.
- Revocation or material invalidation traverses typed dependency edges and invalidates only dependent checkpoints, variants and results. Unrelated derivatives stay valid; historical artifacts remain reproducible.
- A command retry with the same idempotency key and identical canonical request returns the stored result/receipt. Different bytes under the same key fail `AIR_TRANSFER_IDEMPOTENCY_COLLISION`.
- Optimistic concurrency compares expected stream version before commit. A loser fails without partial artifacts or outbox delivery.
- Cancellation before atomic commit removes staging. Cancellation after commit appends a cancellation/invalidation event. A late evaluation/result is stored as noncanonical evidence and cannot resurrect the case.
- Replay folds exact persisted events and artifacts under their pinned schema/profile/registry versions. It performs no network, model, filesystem discovery or “latest” lookup. The first divergence names event and expected/observed hashes.

## 6. Data models, contracts, schemas, and APIs

### 6.1 Common strict types and serialization

All models are closed (`additionalProperties: false`), use no `Any`, untyped maps or hidden defaults, and validate before storage.

`ImmutableRef`:

```text
object_id: nonempty string
schema_id: nonempty string
version: nonempty immutable version string
content_sha256: lowercase 64-hex
owner_product: governed ProductId
lifecycle_state_at_use: governed nonempty state
authority_ref: ImmutableRef | null only for the root authority record
```

`SourceSpanRef`:

```text
source_package_ref: ImmutableRef
artifact_ref: ImmutableRef
speaker_ref: ImmutableRef | null
start_byte: nonnegative integer | null
end_byte_exclusive: positive integer | null
start_ms: nonnegative integer | null
end_ms_exclusive: positive integer | null
keyframe_ref: ImmutableRef | null
transcript_sha256: lowercase 64-hex | null
```

At least one exact byte range, temporal range or keyframe ref is required. Range ends exceed starts. Canonical JSON uses UTF-8, NFC strings, lexicographic object keys, declared list order, decimal integers and no NaN/Infinity. `canonical_hash = sha256(canonical_json(payload excluding canonical_hash and evidence timestamps))`. Caller-supplied IDs are required; random default factories are forbidden.

### 6.2 `ActivationTransferContract`

Schema: `ca.air.activation-transfer-contract/2.1.0-candidate`.

```text
contract_id, version, lifecycle_state: DRAFT | ACTIVE | SUPERSEDED | REVOKED
source_package_ref: ImmutableRef
source_kind: interview_expression | public_comment | direct_message_reply | authored_source |
             live_premise | research_synthesis | operator_supplied | legacy_migrated
expression_moment_refs: nonempty ordered ImmutableRef[]
reaction_receipt_refs: ordered ImmutableRef[]
source_activation_ref: ImmutableRef
observed_activative_intelligence_binding: PublishedObservedPack | NoObservedPackDecision
original_activation_generator: OriginalActivationGenerator
source_role: PsychologicalRoleRef
target_audience_role: PsychologicalRoleRef
viewer_role_tension_ref: ImmutableRef
matrix_result_ref, primitive_coalition_ref, coalition_signature_ref, edge_product_ref: ImmutableRef
archetype_coalition_ref, brand_context_version_ref, voice_dna_ref, visual_dna_ref: ImmutableRef
approved_final_script_ref, derivative_activation_program_ref, semantic_production_package_ref: ImmutableRef
must_survive_properties: nonempty ordered MustSurviveProperty[]
transformation_rules: nonempty ordered TransformationRule[]
required_changes: nonempty ordered RequiredChange[]
permitted_compression: CompressionPolicy
forbidden_collapses: nonempty ordered ForbiddenCollapse[]
participation_or_movement_requirements: nonempty ordered ParticipationRequirement[]
source_media_role: PRIMARY_SPINE | SUPPORTING_EVIDENCE | QUOTED_EVIDENCE | CONTEXT_ONLY
target_derivative_kind, target_category_profile_ref, target_audience_segment_ref: governed values/refs
transfer_checkpoints: exactly five ordered TransferCheckpoint[]
required_evaluation_dimensions: nonempty ordered EvaluationDimensionRequirement[]
wrong_reading_locks: nonempty ordered InheritedWrongReadingLock[]
limitations: ordered Limitation[]
maximum_claim: governed ClaimCeiling
authority_ref, supersedes_ref, dependency_refs, canonical_hash
```

`OriginalActivationGenerator` holds exact source spans/Moment/Reaction/OAI refs; observed or inferred epistemic state per statement; source pressure/recognition/turn/reaction-tail descriptions; and evidence limitations. It cannot contain a free-floating generated summary without source refs.

`PublishedObservedPack` requires the exact TS-AIR-011/OAI ref and IE handoff evidence. `NoObservedPackDecision` requires a pinned profile rule, reason, evidence and maximum claim that forbids observed-human assertions.

Positive example: a contract binds one approved interview Moment, its nonempty Reaction Receipt, the role/tension and Edge Product, declares condensation permitted with source disclosure, forbids role reversal and generic-centroid smoothing, and requires all five checkpoints. Negative example: a contract with `source_role: null`, no Reaction Receipt for interview expression, or `rewriting` omitted from transformation rules fails before identity is assigned.

### 6.3 `MustSurviveProperty`, `TransformationRule`, and `RequiredChange`

`MustSurviveProperty`:

```text
property_id
kind: SEMANTIC_PREMISE | IDENTITY_STANCE | COGNITIVE_TURN | EMOTIONAL_TURN |
      RHYTHM | REACTION_TAIL | VISUAL_CUE | PARTICIPATION_ROLE |
      PSYCHOLOGICAL_ROLE_TENSION | EDGE_PRODUCT | PRIMITIVE_COALITION_FUNCTION |
      ARCHETYPE_FUNCTION | VOICE_DNA | VISUAL_DNA | NEGATIVE_SPACE |
      EDGE_INTEGRITY | SOURCE_MEDIA_ROLE
statement: nonempty string
epistemic_state: OBSERVED | INFERRED | OPERATOR_CONFIRMED | PLANNED
evidence_refs: nonempty ordered ImmutableRef[]
source_span_refs: ordered SourceSpanRef[]
required_at_checkpoints: nonempty ordered TransferCheckpointKind[]
preservation_test: typed PredicateRef
failure_severity: BLOCKING | REQUIRES_HUMAN_RESOLUTION
```

`TransformationRule`:

```text
rule_id
transformation: CONDENSATION | REORDERING | REWRITING | VOICE_SUBSTITUTION |
                VISUAL_ABSTRACTION | ANIMATION | CROP | TIMING | PLATFORM_ADAPTATION
policy: REQUIRED | PERMITTED | FORBIDDEN
derivative_kinds: nonempty governed DerivativeKind[]
applicable_checkpoints: nonempty TransferCheckpointKind[]
constraints: nonempty ordered TransformationConstraint[]
required_disclosures: ordered DisclosureRequirement[]
preserved_property_refs: nonempty MustSurvivePropertyRef[]
evidence_refs: nonempty ImmutableRef[]
```

Every contract has exactly one rule per governed transformation and derivative kind. Duplicate or conflicting rules fail. `RequiredChange` names the current source condition, required target condition, why the change is necessary, permitted method classes, protected properties and proof obligation. It cannot authorize a change to source truth.

### 6.4 `SourceTransformationLineage`

Schema: `ca.air.source-transformation-lineage/2.1.0-candidate`.

```text
lineage_id, version, contract_ref, checkpoint_kind
input_ref, output_ref, output_content_sha256
elements: nonempty ordered LineageElement[]
producer_product, consumer_product, produced_by
transformation_rule_refs: nonempty ordered TransformationRuleRef[]
preserved_property_refs: nonempty ordered MustSurvivePropertyRef[]
inherited_wrong_reading_lock_refs: nonempty ordered WrongReadingLockRef[]
dependency_refs, supersedes_ref, canonical_hash
```

`LineageElement`:

```text
element_id
element_kind: ASSERTION | SCRIPT_SEGMENT | QUOTE | CAPTION | SCENE | VISUAL_PROOF |
              VOICEOVER | ANIMATION_ELEMENT | CROP | TIMING_EVENT | PLATFORM_TEXT
output_locator: typed TextRange | TimeRange | SceneElementRef | AssetRegionRef
transformation_class: VERBATIM | DISCLOSED_OMISSION | CONDENSATION | ADAPTATION |
                      REWRITE | OPERATOR_AUTHORED_CONNECTIVE | NON_SEMANTIC_DERIVATIVE
source_span_refs: ordered SourceSpanRef[]
semantic_support_refs: ordered ImmutableRef[]
operator_authorship_ref: ImmutableRef | null
disclosure_ref: ImmutableRef | null
epistemic_state, maximum_claim
```

`VERBATIM` requires nonempty exact spans and byte equality after the single profile-declared line-ending normalization. `OPERATOR_AUTHORED_CONNECTIVE` requires attributable authorship and disclosure and cannot carry a source quote claim. Other content-bearing classes require source spans or explicit semantic support and the exact transformation rule. A generic note is invalid.

### 6.5 `TransferCheckpoint` and evidence

`TransferCheckpointKind` is closed and ordered:

1. `SOURCE_TO_EXPRESSION_MOMENT` — producer IE, consumer AIR;
2. `EXPRESSION_MOMENT_TO_FINAL_SCRIPT` — producer AIR, consumer AIR/Builder dependency view;
3. `FINAL_SCRIPT_TO_COMPOSITION` — producer AIR, consumer Pipeline;
4. `COMPOSITION_TO_RENDER` — producer Pipeline/VAE by object ownership, consumer Pipeline;
5. `RENDER_TO_PLATFORM` — producer Pipeline, consumer governed publication surface.

`TransferCheckpoint` includes checkpoint ID/kind, producer/consumer products, required input/output schemas, required deterministic validators, judgment dimension requirements, evidence-profile ref, permitted transformations, hard-failure refs and downstream eligibility rule.

`MaterialHandoffEvidence`:

```text
evidence_id, version, contract_ref, checkpoint_ref
producer_product, consumer_product
input_refs: nonempty ImmutableRef[]
output_refs: nonempty ImmutableRef[]
lineage_ref: ImmutableRef
deterministic_validation_receipt_refs: nonempty ImmutableRef[]
observed_composition_or_timing_refs: ordered ImmutableRef[]
producer_acknowledgement_ref, consumer_acknowledgement_ref
submitted_at: caller-supplied UTC timestamp outside semantic hash
canonical_hash
```

Acknowledgement proves receipt and contract identity only. It is not production acceptance, consumption authorization or independent fidelity evaluation.

### 6.6 `ActivationTransferEvaluationReceipt` and `DoctrineIntegrityEvidence`

Schema: `ca.independent-evaluation.activation-transfer-receipt/2.1.0-candidate`; authoritative value owner is Independent Evaluation.

```text
evaluation_receipt_id, version
contract_ref, checkpoint_ref, handoff_evidence_ref
evaluated_input_refs, evaluated_output_refs, evaluated_hashes
evaluation_profile_ref, evaluator_binding_ref, evaluator_actor
producer_actor_refs: nonempty ordered ActorRef[]
deterministic_gate_receipt_refs: nonempty ordered ImmutableRef[]
dimension_results: nonempty ordered TransferDimensionResult[]
doctrine_integrity: DoctrineIntegrityEvidence
verdict: PASS | FAIL | NEEDS_MORE_EVIDENCE | CONTESTED
failure_refs: ordered TransferFailureRef[]
limitations, maximum_claim, canonical_hash
```

Required dimension families are source fidelity, source disclosure, epistemic fidelity, source/target role, tension, Edge Product, Primitive coalition function/misuse, archetype function, Voice DNA, Visual DNA, Reaction-tail survival, Negative Space, Edge Integrity / Anti-Centroid, source-media role, composition/temporal function, wrong-reading locks and category/platform function. The exact applicable set is profile-bound; all omitted required dimensions fail validation.

`TransferDimensionResult` contains dimension ID, applicability `APPLICABLE | NOT_APPLICABLE`, outcome `PASS | FAIL | NEEDS_MORE_EVIDENCE`, reason code, evidence refs and profile-rule ref. N/A has no `PASS` outcome and requires a profile rule proving conditionality.

`DoctrineIntegrityEvidence` binds intended and observed role/tension, Negative Space function, edge/asymmetry relations, source-media role, Primitive outcomes, Visual Syntax or temporal reparse refs, operator calibration ref when required and exact differences. It does not invent a universal numeric score.

### 6.7 `TransferFailure` and `TransferRepairRequest`

`TransferFailure` — `ca.air.transfer-failure/2.1.0-candidate`:

```text
failure_id, version, contract_ref, checkpoint_ref
code: governed TransferFailureCode
violated_property_refs, transformation_rule_refs, wrong_reading_lock_refs
evidence_refs: nonempty ImmutableRef[]
attribution: SOURCE_EVIDENCE | AIR_SEMANTIC_PROGRAM | BUILDER_DEPENDENCY |
             PIPELINE_COMPOSITION_OR_RUNTIME | VAE_PRODUCTION | PLATFORM_ADAPTATION |
             EVALUATION | HUMAN_DECISION | UNRESOLVED
responsible_owner: ProductId | UNRESOLVED
failed_unit_refs: nonempty ImmutableRef[]
preserved_unit_refs: ordered ImmutableRef[]
dependent_invalidation_roots: ordered ImmutableRef[]
next_admissible_action: governed ActionCode
maximum_claim, canonical_hash
```

`TransferRepairRequest` names the failure, owner, target unit, protected upstream refs, permitted transformation rules, required evidence, invalidation boundary and prohibited mutations. It is not a Pipeline repair plan or VAE production plan. `UNRESOLVED` attribution can request diagnosis only.

Core failure codes:

| Code | Condition |
|---|---|
| `AIR_TRANSFER_SOURCE_REF_MISSING` | Exact source package/span/Moment evidence is absent. |
| `AIR_TRANSFER_SOURCE_EVIDENCE_CONFLICT` | Derivative and owner-supplied source evidence conflict. |
| `AIR_TRANSFER_INTERVIEW_PROVENANCE_MISSING` | Interview source lacks required Reaction Receipt or Expression Moment refs. |
| `AIR_TRANSFER_MUST_SURVIVE_INCOMPLETE` | A governed property or checkpoint is absent. |
| `AIR_TRANSFER_TRANSFORMATION_UNDECLARED` | Requested transformation has no exact rule. |
| `AIR_TRANSFER_TRANSFORMATION_FORBIDDEN` | Requested transformation is explicitly forbidden. |
| `AIR_TRANSFER_ROLE_DRIFT` | Target psychological role changes without authorization. |
| `AIR_TRANSFER_TENSION_NEUTRALIZED` | The required tension is flattened. |
| `AIR_TRANSFER_EDGE_PRODUCT_LOST` | Edge Product no longer survives. |
| `AIR_TRANSFER_CENTROID_COLLAPSE` | Generic/smoothed output replaces edge, asymmetry or source specificity. |
| `AIR_TRANSFER_NEGATIVE_SPACE_COLLAPSE` | Required separation/absence/hierarchy function is lost. |
| `AIR_TRANSFER_LINEAGE_GAP` | A content-bearing element lacks exact source/support or connective disclosure. |
| `AIR_TRANSFER_WRONG_READING_LOCK_WEAKENED` | A descendant removes or weakens an inherited lock. |
| `AIR_TRANSFER_EVALUATOR_NOT_INDEPENDENT` | Producer and evaluator authority contexts overlap illegally. |
| `AIR_TRANSFER_EVALUATION_PROFILE_UNAVAILABLE` | Required profile or calibration is absent. |
| `AIR_TRANSFER_NOT_APPLICABLE_UNPROVED` | N/A lacks an exact profile rule and evidence. |
| `AIR_TRANSFER_STALE_DEPENDENCY` | Any pinned input is stale, revoked or hash-mismatched. |
| `AIR_TRANSFER_IDEMPOTENCY_COLLISION` | Same idempotency key carries different canonical request bytes. |
| `AIR_TRANSFER_CONCURRENCY_CONFLICT` | Expected stream version is not current. |
| `AIR_TRANSFER_ATOMIC_COMMIT_FAILED` | Command/artifact/event/edge/receipt/outbox commit did not complete atomically. |
| `AIR_TRANSFER_REPLAY_DIVERGENCE` | Replay yields a different artifact/event hash. |
| `AIR_TRANSFER_AUTHORITY_VIOLATION` | A product attempts a mutation it does not own. |

### 6.8 Commands, events, repository, and APIs

Commands:

- `CompileActivationTransferContract`
- `ActivateTransferContract`
- `RegisterMaterialHandoffEvidence`
- `RequestTransferEvaluation`
- `ApplyTransferEvaluation`
- `AttributeTransferFailure`
- `IssueTransferRepairRequest`
- `SupersedeActivationTransferContract`
- `InvalidateTransferDescendants`
- `CancelTransferCase`
- `ReplayTransferCase`

Successful events mirror the commands: `ActivationTransferContractCompiled`, `ActivationTransferContractActivated`, `MaterialHandoffEvidenceRegistered`, `TransferEvaluationRequested`, `TransferEvaluationApplied`, `TransferFailureAttributed`, `TransferRepairRequested`, `ActivationTransferContractSuperseded`, `TransferDescendantsInvalidated`, `TransferCaseCancelled`, `TransferCaseReplayed`.

Every command envelope contains command ID, idempotency key, expected stream version, actor identity/type/workflow role, owner product, exact input refs/hashes, authority ref, context capsule ref and caller-supplied requested-at evidence. Results are the closed union `Committed<T> | Blocked<TransferFailure> | IdempotentReplay<T> | ConcurrencyConflict`.

`ActivationTransferRepository.commit(transaction)` atomically writes:

```text
command_record
immutable_artifacts[]
events[]
dependency_edges[]
operation_receipt
idempotency_record
current_alias_updates[]
outbox_intents[]
```

Cardinality validation requires every stored state transition to have one command and receipt, every receipt artifact ref to resolve, every edge endpoint to exist, and no outbox delivery before commit. Reads are by exact ref/version/hash; “latest” is a separately stored alias never used during replay.

Cross-product APIs use typed transport envelopes only. AIR exposes contract/evidence admission and exact status reads; Pipeline/VAE/IE/Studio do not import AIR internals. Delegation validates transport and authority but does not interpret transfer semantics.

## 7. Implementation stages and exact target paths

No path below may be created or changed until ratification and a separate bounded Development Capsule authorize it.

| Stage | Exact future paths | FR / Story and evidence boundary |
|---|---|---|
| 0 — capsule and source lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-016/DEVELOPMENT_CAPSULE.yaml`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-016/SOURCE_LOCK.yaml` | All eight FRs/five Stories; accepted spec, ratification, exact upstream hash and allowed paths required. |
| 1 — strict domain types | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/domain/immutable_ref.py`; `activation_transfer_contract.py`; `must_survive_property.py`; `transformation_rule.py`; `source_transformation_lineage.py`; `transfer_checkpoint.py`; `evaluation_receipt.py`; `transfer_failure.py`; `repair_request.py` | AIR-FR-091–096, FR-168, FR-180; closed types, owner and canonical identity. |
| 2 — ports and repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/ports/source_evidence.py`; `semantic_dependencies.py`; `evaluation_gateway.py`; `handoff_evidence.py`; `repository.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/activation_transfer_repository.py` | Exact reads, cross-product isolation, atomicity, idempotency, concurrency and replay. |
| 3 — compilation and admission | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/services/input_admission.py`; `contract_compiler.py`; `lineage_validator.py`; `checkpoint_service.py`; `evaluation_admission.py`; `failure_attribution.py`; `repair_request_compiler.py`; `invalidation.py`; `replay.py` | AIR-ST-16.01–16.03 and no-source-rewrite law. |
| 4 — schemas and fixtures | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.activation-transfer-contract.schema.json`; `air.source-transformation-lineage.schema.json`; `air.material-handoff-evidence.schema.json`; `independent-evaluation.activation-transfer-receipt.schema.json`; `air.transfer-failure.schema.json`; `air.transfer-repair-request.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/fixtures/air_f16/positive/`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/fixtures/air_f16/negative/` | Schema/model parity, all checkpoint and adversarial vectors; no shared release bytes without separate authorization. |
| 5 — cross-product adapters | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/adapters/interview_expression_source.py`; `derivative_semantic_package.py`; `pipeline_handoff.py`; `visual_asset_editor_evidence.py`; `studio_human_resolution.py`; `delegation_transport.py` | Preserve owner/version/hash/lifecycle/claim and forbid local schema forks or hidden writes. |
| 6 — deterministic and independent evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/evaluation/deterministic_transfer_validator.py`; `source_fidelity_evaluator.py`; `doctrine_integrity_evaluator.py`; `wrong_role_centroid_evaluator.py` | Exact mechanical gates, separate evaluator identity and profile-pinned judgment; no invented thresholds. |
| 7 — migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/migrations/ai2_transfer_contract_to_v2_1.py`; `studio_coalition_evidence_to_air_refs.py` | New immutable artifacts only; lossless mapping or typed block; no source classification guess. |
| 8 — status projection | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/projections/transfer_status.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/activation_transfer/api/commands.py`; `queries.py` | Studio/Program Control projection and typed commands without canonical-state takeover. |

Implementation order is domain → repository → compiler/admission → contracts → adapters → evaluation → migration/projection. Each stage remains unstarted until authorized; writing this order is not a build instruction.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Fail closed and preserve source truth

Missing source refs, ambiguous source kind, unknown transformation, stale dependencies, owner conflict, missing interview provenance, unsupported profile, incomplete lineage, weakened locks, unresolved role/tension, missing evaluator independence and unproved applicability return typed blockers. No fallback fills values from filenames, summaries, embeddings, model memory or a similar previous artifact. Parsing without behavioral enforcement is incompatible.

### 8.2 Retry versus semantic repair

Transport and storage failures may retry identical canonical bytes under the same idempotency key. Evaluation service unavailability may retry the same request with the same pinned binding or an explicitly governed fallback binding, producing separate attempt evidence. Source gaps, lineage failures, wrong-role drift, Edge loss, Negative Space collapse, Primitive misuse, DNA drift, wrong-reading weakening and evaluator disagreement are semantic conditions: they require new evidence, a successor derivative, a new evaluation or human resolution. Changing a random seed or rerunning unchanged bytes is not repair.

### 8.3 Migration and compatibility

- The 414-byte predecessor contract is a semantic seed, not a schema. Migration maps every supplied field into the strict V2.1 candidate and blocks if source/Moment refs, roles, must-survive obligations, transformation rules, prohibited collapses, locks, target format or evaluation cannot be established.
- `AHP_PRD_V1_1_SOURCE_FIRST.md` stays historical. It cannot supply current source truth or authority.
- Studio coalition evidence may be referenced only after owner/schema/hash mapping. Random UUIDs become preserved historical IDs, never regenerated; local thresholds remain historical data and do not become AIR defaults.
- A missing classification is never guessed. Migration emits `MIGRATION_BLOCKED_SOURCE_CLASSIFICATION_REQUIRED` and preserves the original bytes.
- Migrations create new immutable objects with migration receipt, source hash, adapter version, field map, omitted-field decisions and maximum claim. They do not mutate historical records.
- Active cases remain pinned to versions negotiated at activation. Deprecation does not invalidate historical work; a materially revoked dependency triggers selective invalidation through explicit edges.

### 8.4 Rollback, cancellation, and recovery

Rollback restores the last known-good executable/service/profile alias for new work; it never rewrites artifacts created under the failed version. A partially staged transaction leaves no canonical artifact, receipt, edge or outbox. If commit succeeds and notification fails, the durable outbox retries. Cancellation and completion races serialize by stream version; exactly one transition wins. Late results are preserved with `LATE_NONCANONICAL_EVIDENCE` and cannot change current state. Recovery recomputes from exact event/artifact bytes and reports the first divergence.

### 8.5 Invalidation propagation

Dependency edges are typed: `DERIVED_FROM_SOURCE`, `OBSERVES_REACTION`, `USES_MOMENT`, `USES_OAI`, `USES_MATRIX`, `USES_COALITION`, `USES_EDGE`, `USES_ROLE_TENSION`, `USES_ARCHETYPE`, `USES_DNA`, `USES_FINAL_SCRIPT`, `USES_COMPOSITION`, `USES_PROFILE`, `EVALUATES`, `VARIANT_OF`. A successor alone does not invalidate an accepted case. Revocation, material contradiction, explicit amendment or evaluator/profile invalidation traverses affected edge types. Historical artifacts/results remain exact and readable; current aliases point to eligible successors only after a governed transition.

### 8.6 Observability

Structured logs/events contain command/transaction/contract/checkpoint IDs, input/output refs and hashes, producer/consumer owners, source kind, lifecycle-at-use, transformation classes, property/rule/lock refs, evaluation profile/binding, dimension outcomes, failure/attribution codes, invalidation fan-out, stream version, idempotent replay and commit result. They exclude raw sensitive source text by default and never become semantic authority.

Metrics include admission blockers by code; transformation coverage; lineage gaps by element kind; checkpoint latency; deterministic versus judgment failures; role/tension/Edge/Negative-Space/centroid failures; N/A denials; evaluator disagreement; unresolved attribution; repair scope size; invalidation fan-out; idempotent replay; concurrency conflict; atomic rollback; late result; replay divergence and portable clean-room reproduction. Metrics do not imply production quality or certification.

## 9. Behavior-specific acceptance criteria

### AC-01 — AIR-FR-091 / AIR-ST-16.01: complete transfer contract

**Given** an exact eligible TS-AIR-015 Semantic Production Package, **when** contract compilation runs, **then** one immutable contract identifies source package/Moments, original activation generator, source and audience roles, role/tension, Edge Product, expression evidence, all must-survive properties, every transformation rule, required changes, forbidden collapses, locks, target format/segment and evaluation contract. **Failure example:** a compact object with only a free-text “preserve intent” note fails `AIR_TRANSFER_MUST_SURVIVE_INCOMPLETE`. **Evidence:** contract, dependency graph and compile receipt. **Layer:** contract/integration.

### AC-02 — AIR-FR-092 / AIR-ST-16.01: source charge is typed and evidenced

**Given** source-backed observed and inferred statements, **when** must-survive compilation runs, **then** semantic premise, identity stance, emotional/cognitive turn, rhythm, reaction tail, visual cue, participation role, role/tension and Edge Product carry exact evidence and epistemic state. **Failure example:** a model invents a reaction tail from a transcript summary. **Evidence:** property records and adversarial denial. **Layer:** unit/contract.

### AC-03 — AIR-FR-093 / AIR-ST-16.02: transformation freedom is closed

**Given** a derivative kind, **when** its contract is activated, **then** condensation, reordering, rewriting, voice substitution, visual abstraction, animation, crop, timing and platform adaptation are each exactly `REQUIRED`, `PERMITTED` or `FORBIDDEN`, with constraints and disclosures. **Failure example:** absent crop policy is treated as permission. **Evidence:** schema matrix and negative fixture. **Layer:** unit/schema.

### AC-04 — AIR-FR-094 / AIR-ST-16.02: every material handoff emits evidence

**Given** a derivative proceeds through source, script, composition, render and platform stages, **when** checkpoint admission runs, **then** all five ordered checkpoints carry exact input/output refs, lineage, deterministic receipts and independent evaluation as required. **Failure example:** a final render pass is used to conceal missing moment-to-script evidence. **Evidence:** checkpoint graph and admission receipts. **Layer:** integration/reference slice.

### AC-05 — AIR-FR-095 / AIR-ST-16.03: element-level lineage

**Given** assertions, captions, quotes, scenes, proofs, voiceover and animation elements, **when** lineage validation runs, **then** each cites exact spans/support and legal transformation or attributable disclosed connective authorship. **Failure example:** polished bridge copy is labeled verbatim without byte equality. **Evidence:** lineage object and negative vectors. **Layer:** unit/schema.

### AC-06 — AIR-FR-096 / AIR-ST-16.03: wrong-role and centroid failure is non-compensable

**Given** an attractive derivative that changes audience role, neutralizes tension or replaces the Edge Product with generic expression, **when** evaluation runs, **then** it fails regardless of aesthetic or engagement dimensions. **Failure example:** a broadly motivational visual scores well on polish but removes the intended witness role. **Evidence:** independent evaluation receipt and typed failure. **Layer:** evaluation/integration.

### AC-07 — FR-168 / ST-12.04: full lineage survives every embodiment

**Given** a source-backed derivative and a reused scene, **when** either is evaluated, **then** source spans, Matrix, Primitive bindings/coalition/signature/Edge, role/tension, archetype, Voice/Visual context, approved Final Script, composition and render history are all exact refs. **Failure example:** a B-roll reuse carries only an asset ID and loses doctrine lineage. **Evidence:** cross-format lineage graph and reuse receipt. **Layer:** architecture/reference slice.

### AC-08 — FR-180 / ST-13.04: Source Fidelity, Negative Space and Edge Integrity

**Given** intended composition/temporal obligations and observed output evidence, **when** doctrine-integrity evaluation runs, **then** source force, psychological role, asymmetry, functional Negative Space, edge relations, source-media role and anti-centroid constraints receive explicit profile-bound outcomes. **Failure example:** centering/cropping removes the separation that carried the tension while technical QA passes. **Evidence:** doctrine receipt, reparse and operator calibration where required. **Layer:** evaluation/reference slice.

### AC-09 — Interview Expression sovereignty and provenance

**Given** `source_kind: interview_expression`, **when** admission runs, **then** at least one nonempty Reaction Receipt ref and one approved Expression Moment ref resolve to IE-owned exact versions; AIR never reconstructs either. **Failure example:** transcript text alone is upgraded to an interview Moment. **Evidence:** owner/provenance validation. **Layer:** contract/architecture.

### AC-10 — non-interview provenance remains truthful

**Given** a non-interview governed source kind, **when** contract compilation runs, **then** interview provenance is optional but validated if supplied, and absent live/interview history is declared absent rather than synthesized. **Failure example:** migrated public commentary is assigned a fictional Reaction Receipt. **Evidence:** source-kind fixtures and migration receipt. **Layer:** schema/migration.

### AC-11 — exact Primitive semantics and applicability

**Given** the F16 bindings, **when** validation/evaluation runs, **then** exact PRM-PSY-001, PRM-VSG-003 and PRM-VSG-021 YAML hashes, trigger/suppression state, core move, conflicts and misuse modes are evaluated separately. **Failure example:** “authenticity” prose substitutes for Punctum misuse checks. **Evidence:** Primitive decision and evaluation receipts. **Layer:** unit/evaluation.

### AC-12 — evidenced `NOT_APPLICABLE`

**Given** a profile-conditional visual dimension, **when** N/A is proposed, **then** a pinned profile rule, applicability fact, evidence and claim ceiling support it; mandatory source/role/Edge/lineage/lock dimensions reject N/A. **Failure example:** Negative Space is marked N/A because the evaluator did not inspect it. **Evidence:** N/A positive/negative fixtures. **Layer:** schema/evaluation.

### AC-13 — wrong-reading inheritance is monotonic

**Given** parent locks and a descendant variant, **when** contract and evidence validation run, **then** every parent lock remains and stricter child locks may be added. **Failure example:** a platform crop variant drops a lock because the layout is smaller. **Evidence:** lock ancestry graph and denial receipt. **Layer:** unit/contract.

### AC-14 — independent evaluator and no certification inference

**Given** producer and evaluator bindings, **when** a receipt is admitted, **then** distinct authority contexts and complete profile dimensions are proven; capability presence does not set evaluator certification or production eligibility. **Failure example:** the same model instance generates and approves a candidate. **Evidence:** binding comparison and status assertion. **Layer:** architecture/evaluation.

### AC-15 — no invented thresholds

**Given** an evaluation dimension requiring calibration, **when** the pinned profile lacks its threshold or categorical rule, **then** evaluation blocks `AIR_TRANSFER_EVALUATION_PROFILE_UNAVAILABLE`. **Failure example:** a service hard-codes 0.86 from historical Studio code. **Evidence:** profile-resolution test and threshold-provenance receipt. **Layer:** unit/architecture.

### AC-16 — bounded repair without source rewrite

**Given** a localized render crop failure, **when** failure attribution and repair request run, **then** the request targets the crop and dependent variants, preserves source/Moment/OAI/Final Script/composition refs, and routes execution to the owning product. **Failure example:** AIR edits the source quote to fit the crop. **Evidence:** repair request and authority denial. **Layer:** integration/architecture.

### AC-17 — unresolved attribution stays unresolved

**Given** evidence cannot distinguish Pipeline composition from VAE realization failure, **when** attribution runs, **then** owner is `UNRESOLVED` and only diagnosis is allowed. **Failure example:** the system assigns VAE to keep the workflow moving. **Evidence:** contested attribution fixture. **Layer:** unit/integration.

### AC-18 — selective invalidation and historical reproduction

**Given** a revoked source span or profile, **when** invalidation runs, **then** only descendants connected by affected typed edges become stale; unrelated work remains current and old artifacts replay exactly. **Failure example:** all derivatives are invalidated by a mutable “latest” lookup. **Evidence:** fan-out map and historical replay receipt. **Layer:** recovery/integration.

### AC-19 — atomic commit, idempotency and concurrency

**Given** a fault at every commit member, duplicate request and two expected-version writers, **when** repository tests run, **then** no partial canonical state exists, identical retries return the original receipt, byte-different collisions fail and exactly one writer commits. **Failure example:** evidence is stored without its receipt. **Evidence:** fault matrix and repository parity report. **Layer:** integration.

### AC-20 — deterministic clean-context replay and portability

**Given** the same logical inputs in clean extracted directories, different insertion/traversal orders, clocks, random seeds and environments, **when** compilation and replay run, **then** canonical bytes/hashes match and no absolute machine path appears. **Failure example:** a current timestamp changes contract identity. **Evidence:** two-process hash matrix and path scan. **Layer:** clean environment/recovery.

### AC-21 — product authority boundaries

**Given** Builder, Pipeline, VAE, Studio or Delegation attempts to alter a contract/source/Final Script semantic field, **when** the command enters AIR, **then** `AIR_TRANSFER_AUTHORITY_VIOLATION` blocks it; typed evidence and owned successor requests remain allowed. **Failure example:** Delegation rewrites a role field while transporting. **Evidence:** architecture import/command boundary suite. **Layer:** architecture/integration.

### AC-22 — claim and authorization ceiling

**Given** every local structural and synthetic test passes, **when** status is reported, **then** the spec remains `WRITTEN_PENDING_AUDIT`, candidate authority remains non-current, build authority is false and no production/certification/publication claim is issued. **Failure example:** a transfer pass is represented as production authorization. **Evidence:** status and receipt assertions. **Layer:** governance/regression.

## 10. Testing and completion evidence

### 10.1 Exact future test paths

| Exact path | Required tests and evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_contract_compiler.py` | Complete field matrix, exact upstream refs, must-survive mapping, no source synthesis, stable ordering and duplicate/conflict denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_transformation_rules.py` | Nine transformation kinds, required/permitted/forbidden closure, disclosures, compression and undeclared denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_source_transformation_lineage.py` | All element/transformation classes, byte/time/region locators, authored connective disclosure and generic-note rejection. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_checkpoint_state_machine.py` | Five ordered checkpoints, legal/illegal state transitions, no later-pass compensation and claim ceiling. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_not_applicable.py` | Exact profile rule, evidence and prohibited mandatory N/A cases. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_wrong_reading_inheritance.py` | Parent-lock parity, stricter child lock, weakening/relaxation denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/activation_transfer/test_primitive_physics.py` | Exact three YAML hashes, activation/suppression, conflicts and every misuse mode. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/schema/test_air_f16_schema_model_parity.py` | Closed schemas, required fields, unions, unknown enums/properties, cross-field invariants and canonical examples. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_ts_air_015_transfer_interface.py` | Exact upstream hash/state, same schema identity, full-field refinement, no local fork and recorded audit-revision trigger. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contracts/test_transfer_consumer_conformance.py` | Builder dependency declaration, Pipeline evidence, VAE result evidence, Studio projection and Delegation transport preserve exact refs/owners/claims. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_activation_transfer_repository.py` | Atomic fault points, receipt/artifact/edge parity, idempotent retry/collision, optimistic race and outbox-after-commit. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_five_transfer_checkpoints.py` | End-to-end evidence order, owner boundaries, hard failures and downstream eligibility. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_transfer_failure_and_repair_request.py` | Evidence-based attribution, unresolved attribution, smallest scope, protected refs and owner routing. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_source_fidelity_and_wrong_role.py` | Verbatim-but-dead, adapted-but-faithful, role drift, tension neutralization, Edge loss and non-compensable outcomes. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_negative_space_edge_integrity.py` | Profile-bound Negative Space, asymmetry, source-media role, Punctum/clarity misuse and anti-centroid cases without invented thresholds. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/evaluation/test_transfer_evaluator_independence.py` | Separate identities, complete dimensions, contested state, calibration unavailable and no certification inference. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_activation_transfer_product_boundaries.py` | IE/AIR/Builder/Pipeline/VAE/Studio/Delegation/Evaluation ownership and no cross-product internal imports. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_ai2_transfer_contract_to_v2_1.py` | Complete mapping, lossless-or-blocked behavior, no guessed source class/history and immutable migration receipt. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_activation_transfer_replay_cancellation_invalidation.py` | Cancellation races, late evaluation, typed descendant fan-out, historical replay and first divergence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_activation_transfer_portability.py` | Two fresh processes/layouts; clock/random/env/order/path independence; no absolute path leakage. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_imported_interview_activation_transfer.py` | Imported source package → observed semantics → approved Final Script → Format 07/SuperVisual/animation scene → composition/render/platform evaluation, correction and replay. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/regression/test_current_v1_1_transfer_lineage.py` | Current V1.1 source/Expression Moment/visual semantics/wrong-reading/T/V boundaries remain unweakened. |

### 10.2 Required completion evidence after later authorized build

A later builder, not this writer, must produce a Build Receipt that contains: accepted spec and ratification refs; Development Capsule and exact source lock; implementation/test file hashes; schema/model parity; all positive/negative/adversarial fixtures; exact upstream accepted or re-audited TS-AIR-015 hash; deterministic two-process matrix; atomic fault matrix; replay/invalidation results; architecture boundary scan; clean extracted-layout result; absolute-path scan; imported-interview reference-slice evidence; independent evaluator binding/calibration state; remaining limitations; and maximum supported claim.

The required later evidence distinguishes structural implementation, synthetic proof, external product conformance, evaluator certification, production eligibility and publication authority. None is inferred from another.

### 10.3 Writer completion state

This document is `WRITTEN_PENDING_AUDIT`. It has not been independently audited, revised, re-audited, accepted for build, adopted into current authority, implemented, certified or granted a Development Capsule. The V2.1 authority is `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; the later pre-ratification ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
