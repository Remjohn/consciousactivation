---
type: technical_specification
spec_id: TS-AIR-007
title: Brand Genesis, Voice DNA, Visual DNA, and Distillation Layers
product: Activative Intelligence Runtime
version: 2.1.0-candidate
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
document_class: CANDIDATE_CANONICAL_TECH_SPEC
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
writing_wave: 2
controlling_frs:
  - AIR-FR-037
  - AIR-FR-038
  - AIR-FR-039
  - AIR-FR-040
  - AIR-FR-041
  - AIR-FR-042
  - FR-166
  - FR-175
  - FR-176
  - FR-177
  - FR-178
  - FR-179
controlling_stories:
  - AIR-ST-07.01
  - AIR-ST-07.02
  - AIR-ST-07.03
  - ST-12.03
  - ST-13.01
  - ST-13.02
  - ST-13.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-001
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-007 — Brand Genesis, Voice DNA, Visual DNA, and Distillation Layers

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`; this document does not adopt it as current authority, authorize implementation, create schemas or contract-release bytes, issue a Development Capsule, or confer build, production, or certification status.

`TS-AIR-001` and `TS-AIR-002` are consumed only as hash-pinned `WRITTEN_PENDING_AUDIT` drafts. Each is labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`; neither is represented as ratified or accepted authority. A byte change to either dependency reopens the six downstream revision-impact sections recorded in section 1 and in the draft-dependency receipt.

## 1. Files and authorities read

| Authority class | Exact path | Version/state | SHA-256 | Use |
|---|---|---|---|---|
| Candidate constitutional authority | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`, pending ratification | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Product sovereignty, semantic ownership, identity continuity, evidence ceilings, immutable history, and lifecycle law. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION` | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Confirms candidate status and the separate implementation gate. |
| AIR controlling feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F07-brand-genesis-voice-visual-dna-and-distillation-layers.md` | `2.1.0-draft` | `d3c02834bd4f55ea94bacdbe1077f6b5fc17cb7b0d9b956300d09c5c941e3dda` | AIR-FR-037 through AIR-FR-042 and the F07 terminal condition. |
| AIR Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | `2.1.0-draft` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-07.01 through AIR-ST-07.03, adversarial denial, supersession, and evidence. |
| Source draft/assignment | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-007-brand-genesis-voice-visual-dna-and-distillation-layers.md` | `DRAFT_AFTER_PRD_PENDING_RATIFICATION` | `b9e4879ad0bf7fdba46e4332759cd511f1cb659db31b9d04601ab140e23730c6` | Candidate design input amended to current ownership, imported FRs, and V3.3 structure. |
| AHP F30 feature evidence | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F30-brand-genesis-voice-visual-dna-distillation-and-anti-centroid-integrity.md` | `1.2.0-draft` | `20765b8509550271f43590293cd3f95387c892c69240ae9d41c5dd1c32d9deb5` | FR-175 through FR-179 and the source-to-artifact integrity boundary. |
| AHP F28 feature evidence | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F28-psychological-role-archetype-coalition-and-final-script-authority.md` | `1.2.0-draft` | `0a130c459707e309ae323f769b00d0f82f866b8bfddf6eb42546a5de4f78370c` | FR-166 Voice DNA constrained-script obligation and its Final Script boundary. |
| AHP Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | `1.2.0-draft` | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-12.03 and ST-13.01 through ST-13.03. |
| AHP integration amendment | `.../amendments/AHP_PRD_V1_3_ACTIVATIVE_INTELLIGENCE_INTEGRATION_AMENDMENT.md` | candidate | `125fc4a45eef3d1fe4c42f75d9ff1cf38bbbb9c6bf04c05c2a252a049ae404b6` | Pipeline executes exact AIR semantic programs and may not duplicate their compilation. |
| Cross-product source ledger | `.../amendments/CROSS_PRODUCT_OWNERSHIP_AND_HANDOFF_LEDGER.md` | candidate | `04bfd499ffff5f049b2da77aee2e67e400b1c3eabf4ab0f5b6b9ea79897600b6` | AIR-plus-operator ownership of archetype/Final Script meaning and typed consumer limits. |
| Program Control authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR compiles semantic programs; Pipeline executes; Studio projects/corrects; VAE realizes. |
| Program Control ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | One authoritative owner per semantic value; human approvals remain attributable. |
| Canonical FR ledger | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | frozen Prompt 02 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns all twelve active FRs to AIR and TS-AIR-007. |
| Canonical traceability | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen Prompt 02 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact requirement text, primary Stories, evidence, and source IDs. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Required unique evidence is available; superseded references cannot support claims. |
| Specification-work authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active, specification only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes WRITE and later technical review, not build. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Sets `CANDIDATE_NOT_CURRENT` and the pre-ratification ceiling. |
| Wave dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_02_DISPATCH_LOCK.yaml` | Wave 2 dispatched | `3bfa468af8f2be9e89160c4ec3beebe47e87c90397efe18d309c6095d4c78585` | Pins the only two admitted upstream drafts. |
| F01 upstream draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` | Immutable refs, epistemic assertions, commands, receipts, hashing, lifecycle, and invalidation. |
| F02 upstream draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5` | Exact identity/brand refs, Context Premise, Matrix, Edge Product, and anti-centroid inputs. |
| Brand doctrine | `.../sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` | `SRC-BRAND-001`; required unique evidence | `61710fe56484b569ce28ddefadbb4c8047e9ae48cadf25291423cf4f200e3dcb` | Brand Genesis, frozen Brand Context Version, approved reusable libraries, and negative-space context. |
| RSCS doctrine | `.../sources/doctrine/RSCS_RECURSIVE_SIGNAL_COMPRESSION_SYSTEMS.md` | `SRC-RSCS-001`; required unique evidence | `bb8ebfcd5c519649b4363731cf11434ce600c71fb5e1d020abb59cbb51b8a330` | Saturation, collision, compression, evaluation, recursion, and reality contact. |
| CCV doctrine | `.../sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | `SRC-CCV-001`; required unique evidence | `0869ff50e4bdaba3dc1854183100826d0de9568b9ed5558bf68b4590834a62c4` | Axis-labelled variation, coalition/fatality, routeability, and anti-centroid laws. |
| AHP F30 source module | `.../sources/doctrine/F30-brand-genesis-voice-visual-dna-distillation-and-anti-centroid-integrity.md` | `SRC-AHP-F30-001`; required unique evidence | `20765b8509550271f43590293cd3f95387c892c69240ae9d41c5dd1c32d9deb5` | Composite feature evidence reconciled into the twelve canonical FRs. |
| Archetype migration evidence | `THE_CMF_STUDIO(2)/CCP Archetype System Migration Proposition.docx.md` | `SRC-DOCT-002`; required unique evidence | `2d7aa11b72c83a95d9240784978e3b9af4944a3e037f18746f8b204bc3287188` | Schema-driven archetypes, Voice DNA constraint, and separation of research/Matrix from templates. |
| Creative architecture evidence | `THE_CMF_STUDIO(2)/CCP_Creative_Pipeline_Architecture_V2.md` | `SRC-DOCT-004`; required unique evidence | `8b9175d8631eff50b7f6c959ad245b87f9b307577b51e6dd4d2f622fd44175e8` | Identity compilation, deterministic execution, composition-before-rendering, and visual negative space. |
| Meaning registry evidence | `THE_CMF_STUDIO(2)/docs/registry-specs/Meaning_Primitive_Registry_Spec.md` | `SRC-DOCT-007`; required unique evidence | `1851f4e8e07beb6e1886e91f45d8bb12cf38d6fc8af8f20e314788d6d47d7e5f` | Meaning-side steerability, coalition compatibility, validation, and packet boundary. |
| Experience registry evidence | `THE_CMF_STUDIO(2)/docs/registry-specs/Experience_Primitive_Registry_Spec.md` | `SRC-DOCT-008`; required unique evidence | `5cb5f1b568c84e41bbbf2ccbb18b938ccee5de1c6cab5cbee96343d88adaee72` | Separates user-state/flow primitives from meaning primitives. |
| SDA snapshot | `.../sources/cmf_sda_registry_snapshot/SOURCE_SNAPSHOT_MANIFEST.json` | `SRC-SDA-001`; 14 members verified | manifest `d9012f38f869dbaba5742e8eefe27e33f6a8b1be2ea9df2f3016b7566bd8676f`; digest `ded8e22b39a4bbefa394b86a7b379f880ef83f56c8f901b12eb5dfac5f642200` | Exact existential invariants, representation/archetypal geometries, composition grammar, and crosswalks. |
| SFL snapshot | `.../sources/cmf_sfl_registry_snapshot/SOURCE_SNAPSHOT_MANIFEST.json` | `SRC-SFL-001`; 30 members verified | manifest `c5e1dbf182743276a577bd2e915030eb32b5731d1f268c1d2ba3fb07dfb63aa0`; digest `327cc36abee9428e416fab6b4d1880a26c02bf4082b16a52f6184c7dfdbb7ad1` | Exact functions, compression rules, surface/function crosswalks, and failure/mutation corpus. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/voice_audio_intimacy/PRM-VOC-009.yaml` | exact `PRM-VOC-009` | `90405cef54e303ca87c2f274e6ac6a39b77cf261b86166a385e2ffb6420d5b80` | Sensory Scene Anchoring, overload/generic/manipulative misuse, and suppression. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | exact `PRM-VSG-003` | `2be2e140588e23e43b4461c9443884b09401f6541ea29bdbae8e945e4672e30c` | Intent Governs Style and anti-laziness constraints. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | exact `PRM-VSG-021` | `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Punctum, Air, Felt Truth, and manufactured-messiness/distracting-flaw misuse. |
| Studio predecessor contract | `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/brand_genesis.py` | predecessor | `c5a46f4c3009ca576e3d62542461d07f998c408e5f308dd5fb81d73488710238` | Existing intake/session/ref structures and portability gaps. |
| Studio predecessor service | `THE_CMF_STUDIO(2)/src/ccp_studio/services/brand_genesis_service.py` | predecessor | `276e6b1648383a185dff2c1955ecab36e134118c33bcdf11f083f684e6d7e89c` | Existing validation, consent/source checks, state writes, and command handling. |
| Studio predecessor repository | `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/brand_genesis_sessions.py` | predecessor | `97c581a17ec99cbc24c7d9a988dd213ad5dc7fcd4b0477bc8cacfef5b3a2a513` | In-memory mutable projection behavior. |
| Studio predecessor test | `THE_CMF_STUDIO(2)/tests/cmf_studio/test_brand_genesis_intake_and_session_creation.py` | predecessor evidence | `f8eea24891d428fa5230f1bc11130f0797a20b1c61a33f7edcc7e9e220af9cde` | Existing positive, consent, missing-evidence, brand-scope, and legacy-Voice-DNA cases. |

The `...` AIR paths expand beneath `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE`. All listed required unique evidence was byte-readable. `SRC-SPEC-001` is `SUPERSEDED`, unavailable, non-unique, and was not used to support a claim.

The two upstream drafts control assumptions in sections 3, 5, 6, 8, 9, and 10. Any change to either pinned path, state, or SHA blocks advancement and reopens all six sections for explicit revision-impact review.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

Without F07, the system can attach a generic “warm, premium, authentic” label to interchangeable copy and visuals, summarize away the source’s costly exposure, randomize candidates by seed, or fill every visual gap until the Edge Product disappears. The operator needs a reproducible semantic program that proves exactly which active Brand Context, Voice DNA, Visual DNA, source spans, RSCS layers, CCV axes, SDA/SFL crosswalks, Negative Space functions, Primitive constraints, and Edge Product survived into each candidate.

### Bounded solution

Implement an immutable AIR F07 compiler that:

1. resolves one exact active Brand Context Version and its originating Brand Genesis Session;
2. keeps Voice DNA and Visual DNA as separate versioned semantic contracts;
3. applies Voice DNA to non-verbatim text while marking quotations and preserving source/transformation lineage;
4. applies Visual DNA to semantic visual programs without overriding the current psychological role, tension, Primitive coalition, or Edge Product;
5. records RSCS saturation, collision, compression, evaluation, and recursion as a loss-auditable Distillation Trace;
6. generates controlled variants only along declared CCV axes and exact SDA/SFL crosswalk obligations;
7. independently evaluates functional Negative Space and anti-centroid Edge Integrity; and
8. hands a pinned `BrandSemanticProgramBundle` to Pipeline for execution without transferring semantic authority.

### In scope

- immutable Brand Genesis references and Brand Context Versions;
- separate Voice DNA and Visual DNA contracts and application receipts;
- Voice-DNA-constrained script drafts, including verbatim-versus-transformed spans;
- RSCS Distillation Traces and rejected-centroid evidence;
- CCV Variation Plans and meaningful-diversity evidence;
- exact SDA/SFL Context Packets, hard-negative obligations, Negative Space intents, and Edge Integrity receipts;
- canonical hashing, atomic commit, idempotency, optimistic concurrency, supersession, descendant invalidation, cancellation, replay, and historical reproduction;
- versioned adaptation of the named Studio predecessor without restoring Studio as canonical semantic authority.

### Out of scope and non-goals

- ratification, implementation, build, production, certification, or a Development Capsule;
- live interview capture, Reaction Receipt, Expression Moment, or source-package ownership;
- Primitive or archetype definition, coalition formation, Matrix reinterpretation, or Edge Product invention;
- final operator approval of the archetype-coalition Final Script, which is governed separately by `FR-167` / `TS-AIR-015`;
- AtomicHarnessDefinition compilation, Pipeline execution, VAE production planning or realization, Studio canonical state, or Delegation transport;
- provider prompt, renderer, or composition-layout details;
- a generic creative-safety/content-rights approval authority. Operator-supplied source authority, provenance, lineage, approvals, and product sovereignty remain explicit; technical security remains operational;
- activating Format 02 or VAE Stage 5.

## 3. Governing decisions and constraints

1. **AIR owns semantic compilation; Pipeline executes.** The lower AHP F30 wording that the Pipeline “compiles” this behavior is constrained by the V1.3 integration amendment and Program Control matrices. AIR owns brand/Voice DNA/Visual DNA/distillation/variation semantic program meaning; Pipeline retrieves, validates, binds, executes, evaluates, and invalidates exact programs without rebuilding meaning.
2. **Human and source authority remain attributable.** AIR compiles versioned Brand Context, Voice DNA, and Visual DNA semantics from authorized evidence. New canonical values or creative boundaries require attributable operator/human approval. A model proposal is not an approval or source fact.
3. **Brand Genesis execution is not silently re-owned.** Studio may project onboarding and capture typed operator commands; source/consent systems retain their operational responsibilities. AIR registers exact accepted evidence and owns the semantic lifecycle result, not every upstream UI or asset-generation step.
4. **One active context is resolved, never guessed.** Every brand-bearing program pins one Brand Context Version and originating Brand Genesis Session. Zero active versions, two active versions, a stale alias, or an unresolved precedence conflict blocks compilation.
5. **Voice DNA and Visual DNA are distinct contracts.** Voice DNA constrains cadence, syntax, vocabulary, pressure, intimacy, rhetorical movement, credible emotional range, sensory anchoring, and anti-draft behavior. Visual DNA constrains identity geometry, visual constitution, material language, color, typography, texture, motion, reference families, exclusions, and functional Negative Space. Neither is a tone adjective or moodboard label.
6. **Source fidelity precedes both DNA contracts.** DNA adapts truthful expression; it cannot rewrite a source claim, manufacture lived experience, change the Matrix/Edge Product, or turn planned material into observed human truth.
7. **Verbatim status is explicit.** Quoted language is stored as a source-span reference with `VERBATIM`; altered language is `TRANSFORMED` with an operation trace. A transformed span may never retain the verbatim label.
8. **RSCS order is non-compensable.** Saturation precedes collision detection; collision precedes compression; evaluation tests reality contact; recursion records repair. A fluent summary cannot skip a layer, and later model confidence cannot replace absent source density.
9. **CCV is controlled expansion, not randomness.** Every variation axis, coordinate, invariant, allowed range, and interaction is declared. Seed or temperature differences alone are not meaningful variation. Source, role/tension, Edge Product, coalition, archetype geometry, and brand identity remain invariant unless the plan explicitly declares a governed axis allowed to vary.
10. **SDA and SFL remain separate.** SDA carries invariant semantic and representation/archetypal geometry. SFL carries delivery function, compression, surface constraints, and known failure patterns. Surface adaptation may alter delivery but cannot corrupt invariant geometry.
11. **Registry entries are exact.** SDA/SFL snapshot digest plus each selected entry ID, version, and SHA are pinned. Missing crosswalks remain unresolved; the compiler cannot infer a nearest entry by similarity.
12. **Negative Space is active structure.** Linguistic, visual, temporal, and participatory absence must have a named attention, recognition, tension, or participation function. Unused room is not automatically Negative Space, and filling governed absence is a semantic defect.
13. **Edge Integrity is tested at the F07 handoff.** The independent evaluator compares source/Matrix/Edge Product, Voice/Visual applications, distillation losses, variants, and Negative Space. Technical polish cannot compensate for centroid flattening, lost psychological role, or neutralized tension.
14. **Primitive bindings are exact.** `PRM-VOC-009`, `PRM-VSG-003`, and `PRM-VSG-021` are referenced by ID/version/hash with trigger, suppression, misuse, conflict, and local-job fields. A prose summary does not substitute for their source YAML.
15. **Primitive misuse is enforceable.** Sensory overload, generic/manipulative sensory cues, lazy default styling, arbitrary brand inconsistency, manufactured messiness, and distracting flaws are typed rejection or repair causes.
16. **F07 does not approve the Final Script.** It produces a `VoiceDNAConstrainedScriptDraft` and evidence package. `TS-AIR-015` later performs the separate source, Voice DNA, archetype, Primitive, Activative, and operator approval gate before composition.
17. **Independent evaluation cannot be self-issued.** Producer and evaluator must have different actor and authority contexts. A score generated inside the compiler does not create eligibility.
18. **History is additive.** Brand Context, DNA, distillation, variation, and integrity changes create immutable successors with typed edges. Historical artifacts remain replayable; current consumers reject stale descendants.
19. **F01 and F02 are draft interfaces.** Their types are used only under the exact dispatch-lock hashes and `DRAFT_DEPENDENCY_NOT_ACCEPTED` labels. No draft detail is represented as ratified law.
20. **Claim ceiling remains specification-only.** The document must remain `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, `specification_work_authorized: true`, `build_authority: false`, with a ceiling of `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` before ratification.

## 4. Current brownfield architecture

### Reusable behavior and evidence

The Studio predecessor captures Brand Genesis intake, brand/source scoping, source and quality refs, consent refs, Voice DNA refs, visual-constitution input, Negative Space input, missing-evidence reports, start receipts, and operator-visible blocked state. Its test suite proves positive intake/start, denial when source use is outside the recorded operational scope, non-fabrication of missing brand evidence, cross-brand isolation, and denial of raw legacy Voice DNA.

The doctrine predecessors supply useful object names and failure examples. They do not confer current semantic ownership on Studio or Pipeline, and their mutable examples are not canonical F07 contracts.

### Brownfield disposition

| Exact path/surface | Actual behavior | Disposition | Migration constraint |
|---|---|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/brand_genesis.py` | Mutable Pydantic objects; UUID/time generated in constructors; lists/open strings; storage prefix and path in semantic objects; Voice DNA reference but no immutable Brand Context/Voice/Visual semantic content hash. | `ADAPT` | Preserve explicit values and operational evidence; replace generated identity/time, storage paths, and generic refs with caller-supplied immutable refs and closed types. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/brand_genesis_service.py` | Validates required intake, source, operational consent, brand scope, accepted quality, and legacy Voice DNA; writes a session before validation completes and then overwrites status. | `ADAPT` for validations; `REPLACE` transaction boundary | Preserve attributable source authority and scope evidence without inventing a generic approval authority; atomically commit artifact/edges/receipt/command. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/brand_genesis_sessions.py` | In-memory dictionaries overwrite sessions, store reports and receipts separately, pick latest receipt by wall-clock time, and lack concurrency/idempotency/invalidation. | `REPLACE` for canonical persistence | Historical imports retain exact source bytes and aliases; no record becomes authoritative merely because it was latest in memory. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_brand_genesis_intake_and_session_creation.py` | Five focused positive/adversarial tests with random IDs and a `sys.path` mutation. | `ACTIVATE` as regression evidence | Port fixtures to deterministic caller-supplied IDs and the governed test environment; add full F07 semantic/lifecycle evidence. |
| Brand doctrine JSON examples | Brand Workspace, Genesis Session, Context Version, expression/editing session, and library IDs are illustrative and partly product-local. | `ADAPT` | Keep stable concepts, replace open objects and local status with exact AIR refs and Program Control ownership. |
| Creative pipeline `Creative State Object` | One mutable job object combines semantic intent, production state, outputs, errors, and receipts. | `ARCHIVE_AS_CANONICAL`; `REUSE` only as migration fixture | Split AIR immutable semantic artifacts from Pipeline runtime projections; never restore one mutable cross-product owner. |
| Creative pipeline Visual Negative Space object | Records forbidden styles/moods/motifs and counter-signals. | `ADAPT` | Add typed modality/function, evidence, inheritance, evaluation profile, and Edge Product lineage. |
| SDA/SFL snapshots | Immutable manifest members and crosswalk/failure-corpus seeds; 14 SDA and 30 SFL members pass manifest verification. | `REUSE_AS_PINNED_INPUT` | Runtime selects exact entries; missing category/surface mappings block or remain explicit, never guessed. |

No current AIR product code exists for this feature. The only current AIR product artifacts at writing time are candidate specifications; therefore predecessor behavior is reported as predecessor evidence, not as an AIR implementation claim.

## 5. Proposed architecture and workflows

### Components and responsibilities

1. `BrandContextCompiler` validates a Brand Genesis evidence package and creates immutable candidate Brand Context/Voice DNA/Visual DNA objects. It cannot approve its own candidate.
2. `BrandContextActivationService` applies an attributable human resolution receipt and projects exactly one active Brand Context per brand and scope.
3. `VoiceDNAApplicationCompiler` creates source-crosswalked non-verbatim text while preserving quotations, Edge Product, archetype program refs, and Distillation lineage.
4. `VisualDNAApplicationCompiler` emits semantic visual constraints, not provider prompts or production plans, and preserves role/tension and composition-intent dependencies.
5. `RSCSDistillationEngine` performs and records saturation, collision detection, compression, evaluation, and bounded recursion.
6. `CCVVariationPlanner` declares axes, coordinates, invariants, diversity obligations, and candidate survival; it does not render candidates.
7. `SdaSflCrosswalkResolver` pins exact snapshot members and compiles invariant geometry plus delivery-function obligations.
8. `F07IndependentIntegrityEvaluator` verifies Voice/Visual DNA, source contact, Negative Space, anti-centroid Edge Integrity, Primitive misuse, and crosswalk completeness from an independent identity.
9. `BrandSemanticRepository` atomically persists immutable artifacts, edges, command records, receipts, projections, invalidations, and replay indexes.
10. `PipelineBrandProgramAdapter` exposes an exact `BrandSemanticProgramBundle`; Pipeline may validate and execute it but cannot reinterpret its semantic values.

### Lifecycle

Candidate semantic objects use `PROPOSED -> INDEPENDENTLY_EVALUATED -> PENDING_HUMAN_RESOLUTION -> ACTIVE -> SUPERSEDED | REVOKED`. A rejected candidate remains immutable as `REJECTED`. Distillation and variation artifacts use `COMPILED -> INDEPENDENTLY_EVALUATED -> DOWNSTREAM_ELIGIBLE | BLOCKED -> SUPERSEDED`. No transition overwrites an artifact.

### Workflow A — compile and activate Brand Context

1. Receive `CompileBrandContextCommand` with caller-supplied command/event identities, expected aggregate version, exact Brand Genesis/source/identity refs, operator/source authority refs, and desired scope.
2. Resolve F01 epistemic/authority refs and the F02 identity/context set under their pinned draft hashes.
3. Validate brand scope, exact source hashes, source-authority evidence, predecessor import status, and the separate Voice/Visual contract inputs.
4. Compile `BrandContextVersion`, `VoiceDNAContract`, `VisualDNAContract`, `BrandNegativeSpaceProfile`, and a candidate receipt. Do not activate.
5. An independent evaluator checks evidence and contrastive fixtures. A human-resolution command referencing the exact evaluation receipt may activate the version.
6. In one transaction, append the version, activation edge, displaced-active supersession edge if authorized, projection update, command record, and receipt. If two active candidates have no explicit resolution, block.

### Workflow B — apply Voice DNA to a script draft

1. Receive `CompileVoiceDNAConstrainedDraftCommand` pinned to one active Brand Context, exact source spans, Matrix/Edge Product, archetype program refs, transformation purpose, category, and surface.
2. Partition input into `VERBATIM`, `PARAPHRASE`, `COMPRESSION`, `SYNTHESIS`, and `OPERATOR_SUPPLIED` segments. Only exact source bytes may be `VERBATIM`.
3. Run RSCS Workflow D when any non-verbatim compression or synthesis is required.
4. Apply closed Voice DNA dimensions and `PRM-VOC-009` only when its trigger conditions hold. Respect suppression conditions and preserve sensory evidence source.
5. Emit `VoiceDNAApplication` and `VoiceDNAConstrainedScriptDraft` with source-span crosswalk, transformation lineage, contrastive evidence, and unresolved caveats.
6. Hand the draft to the later Final Script approval boundary. F07 never emits `FINAL_SCRIPT_APPROVED`.

### Workflow C — apply Visual DNA to a visual semantic program

1. Receive `CompileVisualDNAApplicationCommand` with active Brand Context, role/tension, Edge Product, archetype/Primitive program, category, output surface, and composition-intent refs.
2. Bind exact Visual DNA tokens, recurring operators, exclusions, reference families, material/color/typography/texture/motion constraints, and Negative Space intents.
3. Apply `PRM-VSG-003` so every stylistic constraint names its communication intent. Reject arbitrary trend/style choices and lazy defaulting.
4. Apply `PRM-VSG-021` as a protection/evaluation obligation for source-backed felt-truth evidence, not an instruction to fabricate messiness.
5. Emit a semantic `VisualDNAApplication`; do not select provider, LoRA, workflow, conditioning, candidate asset, or production acceptance.

### Workflow D — produce an RSCS Distillation Trace

1. `SATURATION`: record admitted source spans, identity/context, Matrix/Edge Product, and category constraints; calculate source coverage without generating copy.
2. `COLLISION_DETECTION`: record source-backed prediction violations, costly exposure, recognition, contradictions, asymmetries, and omissions. Flat facts remain evidence but cannot be promoted to a collision.
3. `COMPRESSION`: create candidate representations that increase density while preserving irreducibility, emergence, and specificity. Record every discarded signal and reason.
4. `EVALUATION`: independently test generic reproducibility, cross-source interchangeability, first-order verifiability, source contact, role/tension, and Edge Product survival.
5. `RECURSION`: repair only failed layers, link predecessor/candidate hashes, and stop on pass, bounded-attempt exhaustion, cancellation, or insufficient evidence.

### Workflow E — plan CCV variation and SDA/SFL delivery

1. Receive `PlanControlledVariationCommand` with a passed Distillation Trace, exact invariant refs, active DNA refs, category/surface, and requested candidate count.
2. Resolve exact SDA snapshot and select applicable invariant, representation, archetypal, and species-composition refs. Resolve exact SFL functions, compression rules, crosswalks, surface constraints, and failure/mutation corpus refs.
3. Declare each variable axis and its allowed coordinates. Freeze source, role/tension, Edge Product, coalition function, and protected identity dimensions.
4. Generate or accept candidate semantic programs; record coordinates and deterministic candidate IDs. Random seed may be recorded but cannot be the only differentiator.
5. Compare candidates for semantic distance, coordinate coverage, source fidelity, crosswalk conformance, and known failure patterns.
6. Emit `CCVVariationPlan`, `SdaSflContextPacket`, candidate refs, rejected-candidate refs, and a comparison receipt.

### Workflow F — independent terminal evaluation and handoff

1. An independent evaluator loads exact source/F01/F02/brand/DNA/distillation/variation/SDA/SFL/Primitive dependencies.
2. It evaluates source fidelity, Voice continuity, Visual DNA, Negative Space function, Primitive misuse, anti-centroid charge, role/tension, Edge Product, crosswalk coverage, and downstream routeability separately; scores cannot compensate across non-compensable dimensions.
3. Passing produces `EdgeIntegrityReceipt` and a `BrandSemanticProgramBundle` eligibility edge. Failure identifies the responsible AIR layer and bounded repair input.
4. Pipeline acknowledges and pins the bundle for execution. Its acknowledgement is consumption evidence, not semantic acceptance or product certification.

### Workflow G — idempotency, cancellation, supersession, invalidation, and replay

Every command is idempotent over exact canonical command bytes plus dependency snapshot. Cancellation requested before atomic commit produces no semantic artifact; cancellation racing after commit creates a compensating cancellation/invalidation record, never deletion. A late asynchronous model result whose task, context, or dependency version is stale is stored as rejected evidence and cannot update the current projection. Supersession traverses typed material-dependency edges, invalidates only descendants, and leaves historical exact-hash replay available.

## 6. Data models, contracts, schemas, and APIs

All models are immutable, reject unknown fields, avoid `Any` and untyped maps, use explicit non-empty tuples and closed enums, encode normalized scores as integers in `[0, 1_000_000]`, and use caller-supplied canonical UTC timestamps and stable IDs. `ImmutableRef`, `AuthorityRef`, `ActorRef`, `EvidenceRef`, `EpistemicAssertion`, and `SemanticObjectVersion` follow the pinned F01 draft. Identity/context/Matrix/Edge Product refs follow the pinned F02 draft. Both interfaces remain draft-dependent.

### Brand Context and DNA contracts

```text
BrandGenesisSessionRef
  session_ref: ImmutableRef
  brand_ref: ImmutableRef
  source_package_refs: tuple[ImmutableRef, ...]
  source_authority_ref: AuthorityRef
  operational_scope_receipt_refs: tuple[ImmutableRef, ...]
  operator_resolution_ref: ImmutableRef
  predecessor_import_ref: ImmutableRef | null

BrandContextVersion
  semantic_object: SemanticObjectVersion
  brand_ref: ImmutableRef
  originating_genesis_ref: ImmutableRef
  identity_dna_ref: ImmutableRef
  voice_dna_ref: ImmutableRef
  visual_dna_ref: ImmutableRef
  negative_space_profile_ref: ImmutableRef
  micro_semiotic_library_ref: ImmutableRef | null
  approved_reference_family_refs: tuple[ImmutableRef, ...]
  scope: BrandContextScope
  activation_state: PROPOSED | PENDING_HUMAN_RESOLUTION | ACTIVE |
                    REJECTED | SUPERSEDED | REVOKED
  authority_ref: AuthorityRef
  evaluation_receipt_ref: ImmutableRef
  human_resolution_ref: ImmutableRef | null
```

`BrandContextScope` is a closed tuple of brand, campaign applicability, category applicability, locale, and validity interval. An `ACTIVE` object requires both independent evaluation and attributable human resolution.

```text
VoiceDNAContract
  semantic_object: SemanticObjectVersion
  brand_context_ref: ImmutableRef
  cadence_rules: tuple[VoiceRule, ...]
  syntax_rules: tuple[VoiceRule, ...]
  vocabulary_rules: tuple[VoiceRule, ...]
  stance_rules: tuple[VoiceRule, ...]
  rhetorical_movement_rules: tuple[VoiceRule, ...]
  emotional_range_rules: tuple[VoiceRule, ...]
  intimacy_and_pressure_rules: tuple[VoiceRule, ...]
  sensory_anchor_rules: tuple[VoiceRule, ...]
  anti_draft_rules: tuple[VoiceRule, ...]
  forbidden_genericity_patterns: tuple[PatternRef, ...]
  contrastive_fixture_refs: tuple[ImmutableRef, ...]
  source_evidence_refs: tuple[EvidenceRef, ...]

VoiceRule
  rule_id: StableId
  dimension: VoiceDimension
  instruction: NonEmptyText
  evidence_refs: tuple[EvidenceRef, ...]
  activation_conditions: tuple[NonEmptyText, ...]
  suppression_conditions: tuple[NonEmptyText, ...]
  prohibited_misreadings: tuple[NonEmptyText, ...]
```

```text
VisualDNAContract
  semantic_object: SemanticObjectVersion
  brand_context_ref: ImmutableRef
  identity_geometry_rules: tuple[VisualRule, ...]
  visual_constitution_rules: tuple[VisualRule, ...]
  material_language_rules: tuple[VisualRule, ...]
  color_rules: tuple[VisualRule, ...]
  typography_rules: tuple[VisualRule, ...]
  texture_rules: tuple[VisualRule, ...]
  motion_rules: tuple[VisualRule, ...]
  composition_tendencies: tuple[VisualRule, ...]
  reference_family_refs: tuple[ImmutableRef, ...]
  exclusion_rules: tuple[VisualRule, ...]
  negative_space_profile_ref: ImmutableRef
  contrastive_fixture_refs: tuple[ImmutableRef, ...]
  source_evidence_refs: tuple[EvidenceRef, ...]
```

`VisualRule` has `rule_id`, closed `VisualDimension`, instruction, communication-intent ref, evidence refs, activation/suppression conditions, and prohibited misreadings. Provider/model/LoRA fields are forbidden in this semantic contract.

### Application contracts

```text
TextSpanLineage
  output_span_id: StableId
  output_start_utf8: NonNegativeInteger
  output_end_utf8: PositiveInteger
  treatment: VERBATIM | PARAPHRASE | COMPRESSION | SYNTHESIS | OPERATOR_SUPPLIED
  source_span_refs: tuple[EvidenceRef, ...]
  transformation_step_refs: tuple[ImmutableRef, ...]
  epistemic_state: EpistemicState

VoiceDNAApplication
  semantic_object: SemanticObjectVersion
  brand_context_ref: ImmutableRef
  voice_dna_ref: ImmutableRef
  matrix_edge_product_ref: ImmutableRef
  archetype_program_ref: ImmutableRef
  distillation_trace_ref: ImmutableRef
  span_lineage: tuple[TextSpanLineage, ...]
  applied_rule_refs: tuple[ImmutableRef, ...]
  suppressed_rule_refs: tuple[SuppressedRule, ...]
  primitive_binding_refs: tuple[ImmutableRef, ...]
  output_text_sha256: Sha256
  evaluation_receipt_ref: ImmutableRef | null

VoiceDNAConstrainedScriptDraft
  semantic_object: SemanticObjectVersion
  application_ref: ImmutableRef
  category_ref: ImmutableRef
  surface_ref: ImmutableRef
  script_segments: tuple[ScriptSegment, ...]
  unresolved_caveats: tuple[TypedCaveat, ...]
  final_script_approval_state: NOT_APPLICABLE_F07_DRAFT_ONLY
```

```text
VisualDNAApplication
  semantic_object: SemanticObjectVersion
  brand_context_ref: ImmutableRef
  visual_dna_ref: ImmutableRef
  psychological_role_ref: ImmutableRef
  tension_ref: ImmutableRef
  edge_product_ref: ImmutableRef
  primitive_program_ref: ImmutableRef
  archetype_program_ref: ImmutableRef
  composition_intent_ref: ImmutableRef
  category_ref: ImmutableRef
  output_surface_ref: ImmutableRef
  applied_rule_refs: tuple[ImmutableRef, ...]
  negative_space_intent_refs: tuple[ImmutableRef, ...]
  wrong_reading_constraint_refs: tuple[ImmutableRef, ...]
  evaluation_obligations: tuple[EvaluationObligation, ...]
```

### RSCS, CCV, SDA/SFL, and integrity contracts

```text
DistillationTrace
  semantic_object: SemanticObjectVersion
  source_input_refs: tuple[ImmutableRef, ...]
  edge_product_ref: ImmutableRef
  layers: tuple[DistillationLayerRecord, ...]
  rejected_draft_refs: tuple[ImmutableRef, ...]
  final_representation_refs: tuple[ImmutableRef, ...]
  source_coverage_micros: Integer[0..1_000_000]
  density_gain_micros: Integer[0..1_000_000]
  reality_contact_receipt_ref: ImmutableRef

DistillationLayerRecord
  ordinal: NonNegativeInteger
  kind: SATURATION | COLLISION_DETECTION | COMPRESSION | EVALUATION | RECURSION
  input_refs: tuple[ImmutableRef, ...]
  output_refs: tuple[ImmutableRef, ...]
  source_span_refs: tuple[EvidenceRef, ...]
  collision_refs: tuple[ImmutableRef, ...]
  discarded_signals: tuple[DiscardedSignal, ...]
  invariant_checks: tuple[InvariantCheck, ...]
  actor_ref: ActorRef
  receipt_ref: ImmutableRef
```

The first four layer kinds are mandatory and ordered. At least one `RECURSION` layer is required when evaluation initially fails; otherwise a typed `NO_RECURSION_REQUIRED_PASS` receipt closes the sequence.

```text
CCVVariationPlan
  semantic_object: SemanticObjectVersion
  distillation_trace_ref: ImmutableRef
  invariant_refs: tuple[ImmutableRef, ...]
  axes: tuple[VariationAxis, ...]
  candidate_coordinates: tuple[CandidateCoordinate, ...]
  candidate_refs: tuple[ImmutableRef, ...]
  rejected_candidate_refs: tuple[ImmutableRef, ...]
  sda_sfl_context_ref: ImmutableRef
  diversity_evaluation_ref: ImmutableRef
  stopping_condition: TARGET_COVERAGE_REACHED | NO_MORE_SURVIVORS |
                      BOUNDED_BUDGET_EXHAUSTED | CANCELLED

VariationAxis
  axis_id: StableId
  kind: ARCHETYPE_REGISTER | EMOTIONAL_REGISTER | VOICE_REGISTER | INTENSITY |
        AUDIENCE_MATURITY | REPRESENTATION_GEOMETRY | CATEGORY_COMPOSITION
  allowed_coordinates: tuple[AxisCoordinate, ...]
  fixed_invariant_refs: tuple[ImmutableRef, ...]
  interaction_constraints: tuple[AxisInteractionConstraint, ...]
```

```text
SdaSflContextPacket
  semantic_object: SemanticObjectVersion
  sda_snapshot_digest: Sha256
  sfl_snapshot_digest: Sha256
  archetype_ref: ImmutableRef
  primitive_coalition_ref: ImmutableRef
  category_ref: ImmutableRef
  surface_ref: ImmutableRef
  existential_invariant_refs: tuple[RegistryEntryRef, ...]
  representation_geometry_refs: tuple[RegistryEntryRef, ...]
  archetypal_geometry_refs: tuple[RegistryEntryRef, ...]
  species_composition_refs: tuple[RegistryEntryRef, ...]
  sfl_function_refs: tuple[RegistryEntryRef, ...]
  sfl_compression_rule_refs: tuple[RegistryEntryRef, ...]
  sda_crosswalk_refs: tuple[RegistryEntryRef, ...]
  sfl_crosswalk_refs: tuple[RegistryEntryRef, ...]
  surface_constraint_refs: tuple[RegistryEntryRef, ...]
  hard_negative_refs: tuple[RegistryEntryRef, ...]
  mutation_suite_refs: tuple[RegistryEntryRef, ...]
  unresolved_required_crosswalks: tuple[CrosswalkGap, ...]
```

A packet with non-empty `unresolved_required_crosswalks` cannot become downstream eligible.

```text
NegativeSpaceIntent
  intent_id: StableId
  modality: LINGUISTIC | VISUAL | TEMPORAL | PARTICIPATORY
  function: ATTENTION_CHANNEL | PARTICIPATION_GAP | TENSION_RESERVOIR |
            RECOGNITION_DELAY | IDENTITY_BOUNDARY | RHYTHMIC_BREATH
  protected_absence: NonEmptyText
  evidence_refs: tuple[EvidenceRef, ...]
  edge_product_ref: ImmutableRef
  prohibited_fill_patterns: tuple[PatternRef, ...]
  observable_checks: tuple[EvaluationObligation, ...]

EdgeIntegrityReceipt
  receipt_ref: ImmutableRef
  producer_ref: ActorRef
  evaluator_ref: ActorRef
  source_fidelity: PASS | FAIL
  voice_continuity: PASS | FAIL
  visual_dna_conformance: PASS | FAIL
  role_tension_survival: PASS | FAIL
  edge_product_survival: PASS | FAIL
  negative_space_function: PASS | FAIL
  anti_centroid_charge: PASS | FAIL
  primitive_misuse: PASS | FAIL
  sda_sfl_conformance: PASS | FAIL
  responsible_failure_layer: F07Layer | null
  evidence_refs: tuple[ImmutableRef, ...]
  repair_request_ref: ImmutableRef | null
```

All receipt dimensions pass independently for eligibility. There is no average threshold that can compensate for a failed non-compensable dimension.

### Terminal handoff

```text
BrandSemanticProgramBundle
  semantic_object: SemanticObjectVersion
  brand_context_ref: ImmutableRef
  voice_application_ref: ImmutableRef | null
  visual_application_ref: ImmutableRef | null
  script_draft_ref: ImmutableRef | null
  distillation_trace_ref: ImmutableRef
  variation_plan_ref: ImmutableRef | null
  sda_sfl_context_ref: ImmutableRef
  negative_space_intent_refs: tuple[ImmutableRef, ...]
  edge_integrity_receipt_ref: ImmutableRef
  f01_contract_ref: ImmutableRef
  f02_contract_ref: ImmutableRef
  downstream_consumer: ATOMIC_HARNESS_PIPELINE
  consumption_constraints: tuple[NonEmptyText, ...]
```

### Commands, events, and repository API

Commands are the closed union `CompileBrandContextCommand`, `ActivateBrandContextCommand`, `CompileVoiceDNAConstrainedDraftCommand`, `CompileVisualDNAApplicationCommand`, `CompileDistillationTraceCommand`, `PlanControlledVariationCommand`, `EvaluateF07IntegrityCommand`, `SupersedeF07ObjectCommand`, `InvalidateF07DescendantsCommand`, `CancelF07TaskCommand`, and `ReplayF07Command`.

Each command contains `command_id`, `idempotency_key`, `aggregate_id`, `expected_aggregate_version`, `actor_ref`, `authority_ref`, caller-supplied `issued_at`, exact input refs, and `command_payload_sha256`. Events and receipts carry exact inputs/outputs, reason codes, transaction ID, and lineage edges.

The repository supports `load_exact`, `load_current_projection`, `begin`, `stage_artifact`, `stage_edge`, `stage_receipt`, `stage_command_record`, `stage_projection`, `commit`, `rollback`, `list_material_descendants`, and `replay`. Commit is legal only when artifact, edge, receipt, command record, and projection are mutually referential; receipt-only or artifact-only state is rejected.

### Canonical serialization and examples

Canonical bytes use UTF-8 without BOM, Unicode NFC, LF newlines, lexicographically sorted object keys, declared tuple order, lowercase SHA-256, explicit schema ID/version, and no absolute path, current time, random value, environment variable, storage location, or filesystem traversal dependency.

Positive example: a quote span retains its source byte offsets and `VERBATIM`, adjacent rewritten copy is `COMPRESSION`, the Distillation Trace points to the same Edge Product, the candidate varies `REPRESENTATION_GEOMETRY`, and the active Brand Context/Voice/Visual hashes remain fixed.

Negative example: three candidates differ only by seed, all use “bold premium authenticity,” the source-span list is empty, and visual whitespace has no declared function. The plan fails controlled variation, source fidelity, Voice/Visual DNA, and Negative Space gates even if the render is polished.

## 7. Implementation stages and exact target paths

Implementation is not authorized. If later ratified, technically accepted, and issued a bounded Development Capsule, the work is staged as follows:

| Stage | Future exact target paths | FR/Story coverage and gate |
|---|---|---|
| 1 — domain kernel | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/brand_context.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/dna_contracts.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/distillation.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/controlled_variation.py` | AIR-FR-037–042; FR-166; FR-175–179. Closed immutable models and invariants only. |
| 2 — schemas and fixtures | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f07.brand-context.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f07.dna-application.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f07.distillation-variation.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f07.integrity-receipt.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/fixtures/f07/` | Schema/model round-trip, closed fields, positive/adversarial examples. No shared contract release. |
| 3 — persistence/lifecycle | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/brand_semantic_repository.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/brand_context_service.py` | FR-175; AIR-FR-037. Atomic activation, one-active invariant, idempotency, concurrency, supersession, invalidation, replay. |
| 4 — semantic compilers | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/brand_program_compiler.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/rscs_distillation_engine.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/ccv_variation_planner.py` | AIR-FR-038–041; FR-166; FR-176–178. Producer-only behavior, no self-evaluation. |
| 5 — registry resolver | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/sda_sfl_registry_adapter.py` | FR-179 / ST-13.03. Exact snapshot/member resolution and hard-negative obligations. |
| 6 — independent evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f07_integrity_evaluator.py` | AIR-FR-042 / AIR-ST-07.03. Non-compensable independent receipt. |
| 7 — predecessor migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/studio_brand_genesis_v1_to_air_f07.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/studio_brand_genesis_adapter.py` | Preserve explicit predecessor evidence; block absent semantic meaning; no ownership transfer. |
| 8 — product handoff | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/pipeline_brand_program_handoff.py` | Typed bundle to Pipeline; consumption acknowledgement cannot mutate or approve semantics. |

Stages 3–8 cannot start until later build prerequisites pin accepted F01/F02 interfaces and the applicable AIR Primitive/archetype/Final Script boundaries. Final Script approval remains a separate later gate; Stage 4 may emit only a constrained draft.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Required behavior |
|---|---|---|
| `AIR_F07_UPSTREAM_DRAFT_DRIFT` | F01 or F02 path/state/SHA differs from Wave 2 lock. | Stop advancement and reopen sections 3, 5, 6, 8, 9, and 10. |
| `AIR_F07_BRAND_CONTEXT_REQUIRED` | No active version exists for required brand/scope/time. | Block before script, visual, distillation, or variation work. |
| `AIR_F07_BRAND_CONTEXT_AMBIGUOUS` | Multiple active versions have unresolved precedence. | Require attributable human resolution; do not pick newest. |
| `AIR_F07_BRAND_CONTEXT_STALE` | Command pins a superseded/revoked context or mismatched hash. | Reject and identify current successor without rewriting command. |
| `AIR_F07_DNA_CONTEXT_MISMATCH` | Voice/Visual DNA belongs to a different Brand Context Version. | Block both applications. |
| `AIR_F07_VOICE_GENERICITY` | Copy is interchangeable, violates contrastive fixtures, or loses cadence/stance. | Reject or issue bounded Voice repair request. |
| `AIR_F07_VISUAL_STYLE_WITHOUT_INTENT` | Visual rule has no communication-intent/source/role-tension support. | Reject under PRM-VSG-003. |
| `AIR_F07_VERBATIM_LINEAGE_INVALID` | Modified output is marked verbatim or offsets/hash do not match. | Reject and preserve source bytes. |
| `AIR_F07_SOURCE_CROSSWALK_MISSING` | Non-verbatim claim has no source/transformation lineage. | Block draft eligibility. |
| `AIR_F07_RSCS_ORDER_INVALID` | Compression occurs before saturation/collision or a required layer is missing. | Reject trace. |
| `AIR_F07_RSCS_REALITY_CONTACT_FAILED` | Candidate is trivially generic, source-interchangeable, or unverifiable. | Retain rejected draft and recurse or stop. |
| `AIR_F07_EDGE_PRODUCT_LOST` | Distillation/variation removes or reverses the pinned Edge Product/role/tension. | Non-compensable failure; invalidate dependent candidates. |
| `AIR_F07_CCV_AXIS_UNDECLARED` | Candidate differs on an undeclared or forbidden dimension. | Reject candidate and record axis drift. |
| `AIR_F07_CCV_SEED_ONLY_VARIATION` | Candidates differ only by seed/temperature or surface wording. | Fail meaningful-diversity evaluation. |
| `AIR_F07_SDA_SFL_SNAPSHOT_DRIFT` | Snapshot/member ID/version/hash differs from pin. | Block resolution; never use registry latest. |
| `AIR_F07_REQUIRED_CROSSWALK_MISSING` | Required archetype/Primitive/category/surface crosswalk is absent. | Emit typed gap; no nearest-match inference. |
| `AIR_F07_SFL_HARD_NEGATIVE_MATCH` | Candidate matches dead polish, false depth, synthetic authority, overresolved meaning, or empty motivational smoothness. | Reject or route to responsible semantic repair layer. |
| `AIR_F07_NEGATIVE_SPACE_UNGOVERNED` | Claimed Negative Space lacks modality/function/evidence/checks. | Treat as unused space and fail integrity. |
| `AIR_F07_NEGATIVE_SPACE_FILLED` | Candidate fills a protected absence or removes participation/tension function. | Reject candidate or invalidate descendant. |
| `AIR_F07_PRIMITIVE_MISUSE` | Sensory overload/genericity/manipulation, lazy style, manufactured messiness, or distracting flaw is detected. | Fail Primitive dimension and identify exact binding/misuse code. |
| `AIR_F07_SELF_EVALUATION` | Producer and evaluator share actor/authority context. | Deny terminal eligibility. |
| `AIR_F07_FINAL_SCRIPT_APPROVAL_FORBIDDEN` | F07 attempts to mark its draft as approved Final Script. | Deny authority transition and refer to TS-AIR-015 gate. |
| `AIR_F07_STALE_EXPECTED_VERSION` | Aggregate version changed before commit. | Roll back all staged writes; return current exact ref. |
| `AIR_F07_IDEMPOTENCY_CONFLICT` | Same key, different command bytes/dependency snapshot. | Reject without state change or receipt reuse. |
| `AIR_F07_LATE_RESULT_STALE` | Async result returns after cancellation/supersession/context change. | Store as rejected evidence only. |
| `AIR_F07_NON_ATOMIC_STATE` | Artifact/edge/receipt/command/projection set is incomplete. | Roll back or quarantine; never expose partial current state. |

### Retry, quality repair, and cancellation

Transport/transient failures may retry the identical command and dependency snapshot under the same idempotency key. Semantic failures require a new repair command referencing the blocker receipt and changing only the responsible layer. Retrying a generic draft with a new seed is not repair. Cancellation before commit aborts staged writes; cancellation after commit emits an additive cancellation/invalidation record. Late results cannot resurrect a cancelled or superseded projection.

### Migration and compatibility

The Studio adapter preserves source bytes/hash, legacy ID, brand/org scope, recorded times, source/quality/operational-scope refs, Voice DNA reference kind, visual input, Negative Space input, and existing blocker state. It emits new immutable candidate objects and a migration receipt. It never infers absent Brand Context precedence, DNA semantic rules, source classification, epistemic state, Primitive binding, SDA/SFL crosswalk, or human approval.

Migration outcomes are `MIGRATED_CANDIDATE_PENDING_EVALUATION`, `MIGRATED_WITH_NONAUTHORITATIVE_ATTACHMENT`, or `BLOCKED_REQUIRED_MEANING_MISSING`. Existing `raw_legacy_reference` remains blocked. Historical predecessor state stays readable and is not overwritten.

Compatibility is semantic: a consumer must support the exact schema version, required object types, snapshot digests, Primitive bindings, and non-compensable evaluation dimensions. An adapter may add representation metadata; it may not remove constraints or flatten Voice/Visual/RSCS/CCV/SDA/SFL meaning into notes.

### Rollback, recovery, and invalidation

Rollback removes only uncommitted staging. Recovery inspects transaction journal plus staged content hashes and either completes the same atomic commit when every precondition remains true or records a rollback receipt. It cannot synthesize missing receipts. Superseding Brand Context, DNA, source, Matrix/Edge Product, Primitive, archetype, SDA/SFL snapshot, or evaluation receipt invalidates only material descendants. Exact historical versions and rejected candidates remain reproducible.

### Observability

Events/logs include refs and hashes rather than unrestricted brand/source payloads: `command_id`, `transaction_id`, `aggregate_id`, `brand_context_ref`, `input_hashes`, `output_hashes`, `actor_ref`, `authority_ref`, `reason_codes`, `rscs_layer` where applicable, `axis_ids`, `snapshot_digests`, `dependency_state`, `duration_micros`, and `correlation_id`. Metrics include ambiguous/stale context, DNA mismatches, genericity, verbatim violations, RSCS layer failures, source-density loss, CCV coordinate coverage, seed-only rejection, SDA/SFL gaps, hard-negative matches, Negative Space violations, Primitive misuse, self-evaluation, idempotent replays, conflicts, rollback/recovery, invalidation fan-out, and replay divergence. Telemetry is evidence, not semantic authority.

## 9. Behavior-specific acceptance criteria

### AC-01 — AIR-FR-037 / AIR-ST-07.01: active Brand Context

- **Given** a brand-bearing source or program with one independently evaluated, human-activated Brand Context Version and exact originating Genesis ref,
- **When** F07 resolves its brand context,
- **Then** the output pins Brand Context, Genesis, Identity DNA, Voice DNA, Visual DNA, Negative Space, authority, version, and hashes and becomes eligible for later F07 work.
- **Failure example:** two active versions exist and the compiler chooses the newest timestamp; expected result is `AIR_F07_BRAND_CONTEXT_AMBIGUOUS` with no artifact.
- **Evidence/test:** `BrandContextResolutionReceipt`; contract plus integration tests.

### AC-02 — AIR-FR-038 / AIR-ST-07.01: apply Guest Voice DNA

- **Given** exact source spans, active Voice DNA, Edge Product, archetype-program ref, and a declared transformation purpose,
- **When** non-verbatim text is compiled,
- **Then** cadence, vocabulary, stance, rhetorical movement, credible emotional range, and transformation lineage are preserved in a `VoiceDNAApplication`.
- **Failure example:** polished motivational copy fits no contrastive Voice fixture and could belong to any creator; expected result is `AIR_F07_VOICE_GENERICITY`.
- **Evidence/test:** source-span crosswalk, contrastive fixtures, Voice evaluation receipt; integration and adversarial tests.

### AC-03 — AIR-FR-039 / AIR-ST-07.02: apply Visual DNA without overriding tension

- **Given** active Visual DNA, exact role/tension/Edge Product, composition intent, category, and surface refs,
- **When** the visual semantic application is compiled,
- **Then** Visual DNA tokens/operators/exclusions/reference families/tendencies are bound while the role and tension remain byte-pinned.
- **Failure example:** a provider-style trend replaces tactile identity and neutralizes the confrontational role; expected result is `AIR_F07_VISUAL_STYLE_WITHOUT_INTENT` or `AIR_F07_EDGE_PRODUCT_LOST`.
- **Evidence/test:** VisualDNA application and independent reparse receipt; contract, architecture, and reference-slice tests.

### AC-04 — AIR-FR-040 / AIR-ST-07.02: record RSCS layers

- **Given** saturated source evidence and a requested transformed script or semantic program,
- **When** distillation runs,
- **Then** ordered saturation, collision, compression, evaluation, and required recursion records link all inputs, outputs, losses, rejected drafts, and Edge Product checks.
- **Failure example:** a clean summary is created before collision detection and omits costly exposure; expected result is `AIR_F07_RSCS_ORDER_INVALID` or `AIR_F07_RSCS_REALITY_CONTACT_FAILED`.
- **Evidence/test:** immutable `DistillationTrace` and rejected draft; domain, integration, and replay tests.

### AC-05 — AIR-FR-041 / AIR-ST-07.03: controlled CCV variation

- **Given** a passed Distillation Trace, frozen invariants, and declared variation axes,
- **When** multiple candidates are planned,
- **Then** every candidate records coordinates, meaningful differences, invariant conformance, source fidelity, and survival; undeclared axes are absent.
- **Failure example:** three outputs differ only by random seed and wording; expected result is `AIR_F07_CCV_SEED_ONLY_VARIATION`.
- **Evidence/test:** CCV plan, candidate-coordinate matrix, diversity receipt; property and integration tests.

### AC-06 — AIR-FR-042 / AIR-ST-07.03: Negative Space and Edge Integrity

- **Given** a completed F07 candidate and an independent evaluator,
- **When** integrity evaluation runs,
- **Then** source, Voice, Visual, role/tension, Edge Product, Negative Space, anti-centroid, Primitive, and SDA/SFL dimensions each pass before eligibility.
- **Failure example:** an attractive program fills every visual pause and dissolves the viewer’s role; expected result is failed `negative_space_function` and `edge_product_survival`, regardless of polish.
- **Evidence/test:** `EdgeIntegrityReceipt`; independent evaluation and adversarial corpus tests.

### AC-07 — FR-166 / ST-12.03: Voice-DNA-constrained text-bearing content

- **Given** a derivative requiring headline, claim, slide copy, caption, overlay, voiceover, or animation text,
- **When** F07 compiles the draft,
- **Then** non-verbatim text passes through active Voice DNA, source evidence, Edge Product, archetype program, and Distillation Trace while exact quotations remain marked `VERBATIM`.
- **Failure example:** a quotation is lightly rewritten but still labelled verbatim; expected result is `AIR_F07_VERBATIM_LINEAGE_INVALID`.
- **Evidence/test:** `VoiceDNAConstrainedScriptDraft` plus span crosswalk and VoiceContinuity receipt; unit and integration tests. Final approval is not issued here.

### AC-08 — FR-175 / ST-13.01: Genesis and active context binding

- **Given** a brand-bound campaign or derivative,
- **When** a JIT semantic dependency bundle is requested,
- **Then** the accepted Genesis evidence and one active Brand Context Version are pinned before script, visual research, Primitive selection, or composition.
- **Failure example:** the request carries only a brand ID and relies on mutable “latest”; expected result is `AIR_F07_BRAND_CONTEXT_REQUIRED`.
- **Evidence/test:** JIT inclusion and supersession/replay receipts; service and clean-environment tests.

### AC-09 — FR-176 / ST-13.01: separate Voice and Visual contracts

- **Given** a derivative that contains both text and visuals,
- **When** DNA constraints are resolved,
- **Then** independent Voice and Visual contract hashes, rules, evaluations, and operator labels are present; source fidelity is upstream of both.
- **Failure example:** one `style: authentic premium` field is used for both modalities; schema validation rejects the flattened contract.
- **Evidence/test:** contrastive Voice/Visual fixtures and version pins; schema, domain, and architecture tests.

### AC-10 — FR-177 / ST-13.02: RSCS before later script approval

- **Given** a dense source answer being reduced to category-native copy or scene programs,
- **When** a draft is proposed for the later Final Script gate,
- **Then** its complete Distillation Trace proves saturation, source-backed collisions, denser representations, reality-contact evaluation, rejected centroid drafts, and bounded recursion.
- **Failure example:** the draft is fluent but no source-specific claim requires first-order evidence; it fails reality contact and cannot proceed to TS-AIR-015.
- **Evidence/test:** density benchmark, source-contact receipt, rejected drafts; integration and adversarial tests.

### AC-11 — FR-178 / ST-13.03: meaningful archetype/composition variation

- **Given** one Edge Product and a request for category-compatible candidates,
- **When** CCV planning varies archetype register, emotion, Voice register, intensity, audience maturity, representation geometry, or composition axes,
- **Then** coordinates and invariants are explicit and the portfolio demonstrates semantic diversity without source/brand drift.
- **Failure example:** an undeclared intensity increase turns recognition into hype; expected result is `AIR_F07_CCV_AXIS_UNDECLARED` and candidate rejection.
- **Evidence/test:** axis matrix, comparative source-fidelity receipt, candidate survival evidence; property, integration, and mutation tests.

### AC-12 — FR-179 / ST-13.03: SDA/SFL crosswalks

- **Given** an active archetype, Primitive coalition, category, and output surface,
- **When** semantic geometry and delivery function are compiled,
- **Then** exact SDA invariant/geometry and SFL function/compression/surface/failure refs are pinned in one `SdaSflContextPacket`; Pipeline consumes the packet without reinterpreting it.
- **Failure example:** a video-to-carousel adaptation preserves words but reverses archetypal geometry or matches overresolved-meaning corpus; expected result is a crosswalk or hard-negative blocker.
- **Evidence/test:** snapshot/member hashes, context packet, surface comparison and failure-corpus receipt; registry-contract, integration, and handoff tests.

### Cross-cutting acceptance

Fresh-process determinism must reproduce exact artifacts and receipts; idempotent replay must not create another version; concurrent expected-version commands cannot both commit; injected failure cannot leave receipt-only or artifact-only state; supersession invalidates only material descendants; historical versions remain replayable; compiler and evaluator identities differ; migration never guesses missing meaning; and all metadata preserves the candidate-authority claim ceiling.

## 10. Testing and completion evidence

### Required future test suites

| Test path | Named evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f07_brand_context.py` | One-active invariant, scope, exact refs, human activation, supersession, and stale denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f07_dna_contracts.py` | Separate closed Voice/Visual models, verbatim lineage, genericity, intent-governed style, and Primitive misuse. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f07_distillation.py` | RSCS ordering, collisions, discarded-signal trace, density, reality contact, and recursion. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f07_controlled_variation.py` | Axis declaration, coordinate coverage, invariants, seed-only rejection, Negative Space, and anti-centroid behavior. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/serialization/test_f07_canonical_hash.py` | Insertion/traversal/environment/path/time/random independence in two fresh processes. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f07_schemas.py` | Schema identity, unknown-field rejection, tagged unions, integer micros, exact refs, and model/schema parity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f07_sda_sfl_snapshots.py` | All 14 SDA and 30 SFL manifest members, exact crosswalk refs, gaps, and hard-negative corpus. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_brand_genesis_voice_visual_dna_and_distillation_layers.py` | AIR-FR-037–042 and FR-166/175–179 end-to-end with terminal bundle and denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f07_atomic_commit_idempotency_concurrency.py` | Failure injection, no orphan state, exact replay, conflict denial, and one winner. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f07_product_authority_boundaries.py` | AIR semantic ownership; Pipeline execution only; no Studio/VAE/Builder/Interview mutation; no generic approval authority. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_studio_brand_genesis_v1_to_air_f07.py` | Explicit-field preservation, historical aliases, raw legacy denial, and blocks for missing meaning. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_f07_cancellation_replay_invalidation.py` | Cancellation races, stale late results, descendant-only invalidation, rollback recovery, and historical reproduction. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_f07_portability.py` | Clean extracted layout and absence of absolute path, locale, current-time, random, and environment dependence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_f07_pipeline_handoff.py` | Pipeline pins/executes exact bundle and cannot mutate semantics; stale/failed bundle rejected. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_f07_to_final_script_gate.py` | Voice-constrained draft reaches TS-AIR-015 boundary without F07 self-approval. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/regression/test_studio_brand_genesis_predecessor_cases.py` | Ports the five named Studio positive/adversarial cases into deterministic fixtures. |

### Required adversarial and mutation corpus

The evidence run must include absent/ambiguous/stale Brand Context, mixed DNA contexts, raw legacy Voice DNA, generic motivational copy, altered quotation marked verbatim, missing source crosswalk, visual trend without intent, Visual DNA override of role/tension, sensory overload, generic/manipulative sensory anchoring, lazy default style, arbitrary brand inconsistency, manufactured messiness, distracting flaw, compression-before-saturation, no collision, lost costly exposure, trivially generic output, undeclared axis, seed-only variation, reversed SDA geometry, missing SFL surface crosswalk, dead polish, false depth, synthetic authority, overresolved meaning, empty motivational smoothness, ungoverned/filled Negative Space, lost Edge Product, producer self-evaluation, F07 Final Script self-approval, context supersession, idempotency conflict, concurrent activation, mid-commit failure, cancellation race, stale late result, and migration with absent classification.

### Completion evidence and claim ceiling

Future implementation completion would require all named suites to pass twice in fresh processes, Python/source compilation, schema/generated-type parity, canonical fixture hashes, SDA/SFL member verification, requirement-to-test/receipt coverage, independent evaluation, clean-room replay, migration evidence, product-boundary proof, and an independently audited Build Receipt issued only after ratification and a Development Capsule.

This document issues none of those artifacts. Its only completion state is `WRITTEN_PENDING_AUDIT`. It remains `CANDIDATE_NOT_CURRENT`, is authorized for specification work only, has `build_authority: false`, and may advance no higher than `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` before attributable ratification. It grants no current product adoption, implementation, build, production, Format 02, VAE Stage 5, or certification authority.
