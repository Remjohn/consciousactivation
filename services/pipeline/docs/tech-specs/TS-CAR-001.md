# TS-CAR-001 — Source-Grounded Carousel Runtime and Export Package

| Field | Value |
|---|---|
| Spec ID | `TS-CAR-001` |
| Product and primary owner | Atomic Harness Pipeline |
| Writing packet | `CA-P03-WRITE-TS-CAR-001-RECOVERY` |
| Writing wave | `13` |
| Output path class | `DIRECT_PRODUCT_SPEC_PATH` |
| Quality state | `WRITTEN_PENDING_AUDIT` |
| Authority state | `CANDIDATE_NOT_CURRENT` |
| Specification work authorized | `true` |
| Build authority | `false` |
| Build state | `NOT_BUILD_READY` |
| Maximum pre-ratification state | `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` |
| Controlling requirements | `FR-055` through `FR-060`, `FR-145` |
| Controlling Story | `ST-05.02` |

This is an implementation-grade candidate specification produced under the Prompt 02C specification-work authorization. It does not make V2.1 candidate authority current, authorize implementation, activate a Carousel production profile, certify a renderer or evaluator, create release bytes, or issue a Development Capsule.

## 1. Files and authorities read

### 1.1 Writing law, packet, and dispatch

| Input | SHA-256 | State and use |
|---|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | V3.3 writing law; WRITE only |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact recovery packet |
| `.../PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_13_DISPATCH_LOCK.yaml` | `cbf921af042212cd2fe2f43de067c7145bd931314232bb16bb8120b44135f729` | Wave and upstream lock |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate-authority claim ceiling |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification work only |

The packet permits only this file. No `AGENTS.md` applies to `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/`; repository authority is the explicit Prompt 02 and Prompt 02C path authorization recorded by the packet.

### 1.2 Current and candidate authority

The current Constitution V1.1 remains highest current authority. The V2.1 authority and ownership matrices remain `CANDIDATE_NOT_CURRENT`. The candidate boundary used for this draft is: AIR owns semantic lifecycle and production-program meaning; Interview Expression owns live source/reaction evidence; Builder declares the Harness category/profile and dependencies; Pipeline executes; VAE realizes visual demands; Studio projects and submits typed correction; Delegation transports.

The Pipeline may compile an executable carousel program only from exact upstream semantic objects. It may not author or mutate the approved Final Script, viewer psychological role inside a tension, Primitive Coalition Contract, Coalition Signature, Edge Product, archetype coalition, Brand Context Version, Guest Voice DNA, Visual DNA, Composition Intent, Feature Contracts, T/V route, source authority, or wrong-reading locks.

### 1.3 Controlling requirements and Story

| Input | SHA-256 | Controlled behavior |
|---|---|---|
| `.../prd/features/F10-carousel-category-runtime.md` | `5e40116edfc902b3391fb6898ee31da30cc77200259f46aa05be7ac9a15f2c36` | `FR-055`–`FR-060`: category identity, slide roles, swipe order, continuity, profile authority, export package |
| `.../prd/features/F25-source-grounded-carousel-supervisual-and-2d-animation-derivatives.md` | `dbab88c994da95fbead65abfba4984d0efa3cd8a2fb27598997bd9886c37d293` | `FR-145`: source-grounded Carousel derivative |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | `ST-05.02` and CBAR denial/recovery law |
| `.../planning/spec_assignments/TS-CAR-001.md` | `9170800cd46628e2a42267e7a1b23d65016a1ad485ea0ddb842df1d5908ea086` | Assignment evidence, not the full spec and not path authority |

`ST-05.02` requires one usable source-grounded, slide-native Carousel; exact slide/source lineage; geometry/text checks; sequence evaluation; render hashes; actionable denial; and selective recovery. Its protected law is that Carousel is not flattened into frame-time motion. The concrete defended failure is a false quote, ungrounded visual, or unlabeled transformation producing a misleading derivative or identity drift.

### 1.4 Non-accepted upstream drafts

The following are admitted under `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Edge | Draft | State | SHA-256 | Admitted interface |
|---|---|---|---|---|
| `SDE-070` | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-STA-001.md` | `WRITTEN_PENDING_AUDIT` | `423eee94e20ab263fbbc1d10fefd4a687e823491c3eba1ece66acfcf0302e160` | Renderer-neutral Composition IR, deterministic geometry/text/annotation/Skia evidence, static acceptance and replay |
| `SDE-071` | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md` | `WRITTEN_PENDING_AUDIT` | `072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed` | Immutable `ContentDerivativeJob`, source/semantic/Harness closure, job lifecycle and selective invalidation |

Neither draft is represented as accepted law. A hash or accepted-interface change reopens sections 3, 5, 6, 8, 9, and 10: governing decisions; architecture/workflows; data contracts; failure/migration/rollback/recovery/observability; acceptance criteria; testing/completion evidence.

### 1.5 Required current and predecessor evidence

| Source | Class | SHA-256 | Use and disposition |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py` (`SRC-CUR-007`) | `REQUIRED_CURRENT_IMPLEMENTATION` | `cef3bf6673bde2ec501c01099f0efee12b7ad47cb8379c68a58b074a13c35512` | Current category-rule evidence; consume exact declaration, do not import Builder code |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/carousel_engine_service.py` (`SRC-LEG-024`) | `REQUIRED_UNIQUE_EVIDENCE` | `3b9e6042ae490ccc221a923da4d96ccacabb19ace0c908fbbf9b528fe6d8315a` | Legacy workflow evidence; `REPLACE` in Pipeline |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/carousel_render_service.py` (`SRC-LEG-025`) | `REQUIRED_UNIQUE_EVIDENCE` | `2e0477aecc0f12fcd4b5848f4169ee97a9a2804f593c37eb3c31692233173fd1` | Synthetic hash-only renderer; `REPLACE` |
| `THE_CMF_STUDIO(2)/docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` (`SRC-LEG-037`) | `REQUIRED_UNIQUE_EVIDENCE` | `d583495e7e76eeb6a6602c2a264f159826b590103dbdf843ee69777871b71287` | Historical slide-atom/sequence concepts; `ADAPT` under current ownership |
| `THE_CMF_STUDIO(2)/docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` (`SRC-LEG-038`) | `REQUIRED_UNIQUE_EVIDENCE` | `f0656d0b829ef17506adf9d62cff8562d59f24cace817ea0d5d6526045fc1287` | Historical execution/export spine; `ADAPT`, not current provider/authority law |
| `THE_CMF_STUDIO(2)/docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` (`SRC-LEG-039`) | `REQUIRED_UNIQUE_EVIDENCE` | `2cec079f126a53e76ed5677c55963994b92b7f8781cd45d0258ca08ead04a2f7` | Candidate composition evidence; `ARCHIVE_AS_THRESHOLD_AUTHORITY`, selectively adapt grammar concepts |
| `.../sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | `REQUIRED_UNIQUE_EVIDENCE` | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Historical doctrine for source/session/Expression Moment route; current Interview Expression contracts govern |

The historical Atlas’s numerical score weights and cutoffs are not current governed evaluator thresholds. This spec does not adopt them. Historical format codes, slide atoms, provider names, aspect ratios, text budgets, and slide-count ranges are evidence until a current category/profile registry adopts them.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

A Carousel is not a set of disconnected poster images and not a short video sampled into frames. A superficially polished runtime can still fail if it invents slide meaning, paraphrases a quote as verbatim, maps an unapproved archetype, loses the viewer’s role inside the tension, repeats a visual grammar without purpose, renders stale VAE assets, or exports URI-like references without actual bytes. The historical implementation demonstrates this danger: it generates default claims, roles, assets, visual systems, style routes, scores, and render hashes, and can label an export approved without authoritative source closure or independently verified artifacts.

The runtime must instead transform a complete, immutable `ContentDerivativeJob` into a category-native operational sequence, execute exact AIR-owned composition and wrong-reading constraints through the static runtime, and deliver a portable artifact package whose every slide element resolves to source/evidence and approved transformation lineage.

### 2.2 User and system outcome

A Conscious Content Operator receives an ordered Carousel package containing real rendered slide images, a contact-sheet/preview, geometry and evaluation evidence, platform variants, accessible descriptions, and an immutable manifest. The operator can prove:

- why every slide exists and what sequence role it performs;
- how the viewer enters, inhabits, and moves through the approved tension;
- which approved Final Script/source/evidence supports each visible claim or quote;
- which language is verbatim, omitted, condensed, or operator-authored;
- which AIR composition intent, Feature Contracts, identity/continuity constraints, and locks each slide executes;
- which VAE-produced visual assets were consumed without mutation;
- how cross-slide continuity and declared variation were evaluated;
- which exact bytes were accepted, rejected, invalidated, superseded, or delivered.

### 2.3 Bounded solution

Implement a Pipeline-owned Carousel aggregate and compiler that validates the derivative-job closure, applies a current Builder-declared Carousel category/profile contract, compiles typed slide-role and swipe-order execution plans without inventing semantic meaning, creates one TS-STA-compatible static composition child program per slide, coordinates actual deterministic rendering, validates cross-slide continuity, and packages ordered exports with complete source and artifact lineage.

### 2.4 In scope

- Exact admission of a Carousel `ContentDerivativeJob`.
- Category/profile identity and capability validation.
- Deterministic compilation of slide roles and swipe progression from exact upstream semantics and a governed rule profile.
- Element-level source, claim, quote, transformation, identity, and evidence maps.
- Cross-slide recurrence, hierarchy, terminology, identity, composition, and visual-continuity contracts.
- Per-slide Composition IR/static-program handoff and orchestration through the TS-STA interface.
- Real artifact ingestion, ordered manifest, preview/contact sheet, geometry report, alt text, and platform variants.
- Mechanical validation, independent sequence/semantic/visual evaluation, operator decision, typed repair, cancellation, selective invalidation, replay, and historical reproduction.

### 2.5 Out of scope and non-goals

- Authoring AIR semantic meaning, a Final Script, Primitive/archetype coalition, viewer role/tension, Edge Product, Composition Intent, Feature Contract, T/V route, or wrong-reading lock.
- Reconstructing missing Interview Expression source classification, Reaction Receipt, Expression Moment, speaker truth, approval, or provenance.
- Selecting VAE models, LoRAs, workflows, conditioning, Steering Recipes, candidate assets, or production acceptance.
- Treating a historical slide library/atlas, provider workspace, source corpus, UI state, or model response as canonical authority.
- Activating Format 02, 2D animation, frame-time motion, or an animated Carousel derivative.
- Approving publication, category certification, production use, or downstream consumption.
- Implementing source code, canonical schemas, release packages, or a Development Capsule in this writing stage.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty and unique ownership

| Object or decision | Owner | Pipeline permission | Forbidden Pipeline behavior |
|---|---|---|---|
| Activative meaning, approved route, viewer role/tension, Primitive/archetype coalition, Final Script, Edge Product | AIR | Read exact immutable refs; mechanically compile declared execution | Invent, rewrite, weaken, or select new meaning |
| Expression Moment, Reaction Receipt, exact source spans, speaker truth and source approval | Interview Expression/source owner | Validate and reference exact evidence | Synthesize human reaction or source authority |
| Harness category/profile, node dependencies, capability/evaluation requirements | Builder or generated target | Validate exact current binding | Fork the Harness, infer a profile, or claim certification |
| Carousel runtime program, slide execution sequence, per-slide static child orchestration, export package | Pipeline | Own immutable execution versions | Transfer meaning ownership to a renderer or model |
| Composition Intent, BBOX function and WHY, Feature Contracts, T/V semantics and wrong-reading locks | AIR/upstream semantic owner | Preserve exactly and compile allowed geometry through TS-STA | Author missing intent, relax locks, or turn coordinates into meaning |
| Visual Asset Demand | Upstream content target/Pipeline boundary defined by shared authority | Reference exact immutable version and issue only authorized demand | Let VAE mutate demand meaning |
| Visual Production Plan and asset realization | VAE | Consume an exact production-accepted result with separate acknowledgement | Select production route/model or duplicate VAE evaluation |
| Static geometry/text/annotation/Skia program and artifact evidence | Pipeline under TS-STA | Execute child programs | Call renderer output semantic approval |
| Operator correction and HumanResolution | Attributable operator/Studio | Apply typed authorized command to a new version | Hidden in-place edit or manufactured approval |
| Cross-product transport | Delegation | Send immutable envelopes and receipts | Interpret semantic fields or repair content |

### 3.2 Carousel category identity

The category ID is the exact Builder-owned `carousels` identity or its current governed successor. The profile is an immutable category-owned profile reference. The runtime rejects:

- frame-time motion semantics or a timeline as the slide sequence;
- reuse of a profile owned by another category;
- profile aliases not resolved by a governed alias registry;
- a profile represented as certified by structural support alone;
- a slide program missing an approved Final Script or Primitive Coalition Contract;
- any attempt to inherit Format 02 or another profile’s certification.

Slide order is semantic sequence, not elapsed time. A still slide may contain a static annotation cue, but reveal timing or animation requires a separately authorized derivative contract.

### 3.3 Semantic mapping without semantic mutation

The runtime may map exact AIR-owned semantic sequence steps to typed Carousel slide roles only through a versioned, current `CarouselRoleMappingProfile`. Each rule names required source/semantic refs, allowed role IDs, sequence-position constraints, composition-intent requirement, and evidence. When more than one role remains semantically valid and no deterministic rule chooses among them, the runtime emits alternatives for attributable selection. It does not ask a model to manufacture the role.

The approved Final Script is immutable input. Splitting exact approved text across slides is permitted only when the profile and script’s transformation contract authorize segmentation. A condensation, omission, bridge, or headline rewrite requires an exact pre-approved transformation record; the Carousel runtime cannot create editorial wording and then self-approve it.

### 3.4 Swipe-order law

Every slide declares:

- entry viewer state and active psychological role;
- the tension held or changed on this slide;
- the slide’s sequence role and source-supported claim function;
- exact Guest Voice DNA delivery-function refs where applicable;
- the transition contract to the next slide;
- the intended exit viewer state;
- why the slide cannot be removed without breaking the approved sequence.

The first slide admits the viewer into the approved role/tension; intermediate slides deepen, contrast, prove, reframe, or operationalize according to exact AIR sequence semantics; the terminal slide fulfills the approved Activative Call/closure without adding unsupported claims.

### 3.5 Source fidelity and transformation truth

Every visible content element is one of: `VERBATIM_QUOTE`, `DISCLOSED_OMISSION`, `FAITHFUL_CONDENSATION`, `OPERATOR_AUTHORED_BRIDGE`, `APPROVED_FINAL_SCRIPT_TEXT`, `NON_CLAIM_LABEL`, or a registered successor. Each record names exact source spans, speaker, evidence, transformation owner, approval receipt, and displayed disclosure requirement. Unknown transformation types are rejected. A paraphrase cannot carry `VERBATIM_QUOTE`; a quote mismatch is a hard blocker.

For `source_kind: interview_expression`, at least one non-empty Reaction Receipt reference and one non-empty Expression Moment reference remain mandatory in the derivative-job/source closure. Other source kinds may carry those references, and they are validated when supplied. The runtime never guesses a source kind.

### 3.6 Cross-slide continuity and declared variation

Continuity preserves exact identity, terminology, evidence, viewer role/tension, recurring semantic roles, visual recurrence groups, hierarchy, reading order, source attribution, and locks. Continuity does not require visual sameness. Each deliberate variation names a governed dimension, reason, allowed range, affected slides, and authority. Undeclared drift is failure; identical repeated layout without a sequence reason is also failure when the current profile prohibits it.

### 3.7 Composition and wrong-reading locks

AIR-owned Composition Intent precedes syntax. Every slide’s TS-STA child program carries exact intent, BBOX function and WHY, hierarchy/reading path, Feature Contracts, identity/continuity refs, T/V requirement, allowed variation, and full inherited wrong-reading locks. Generative, composited, restyled, cropped, reformatted, or semantically transformative demands require nonempty locks. Child slides inherit all parent locks, may add stricter authorized locks, and may not remove or weaken a lock. Relaxation requires a new authorized upstream demand version.

The Carousel compiler may solve category-native execution choices only within allowed variation. If a required slide has no upstream Composition Intent, it blocks and routes to AIR/upstream authority; it does not use a historical atlas record as substitute meaning.

### 3.8 Evaluation and acceptance separation

Deterministic validators check source matching, text/geometry, sequence indices, category/profile, exact hashes, inherited locks, artifact count, format, and manifests. Independent evaluators inspect sequence progression, source fidelity, semantic/visual hierarchy, identity, swipe coherence, continuity, wrong-reading risk, and format-native effectiveness under a pinned profile. The producer cannot evaluate itself where independence is required.

Pipeline render acceptance, VAE production acceptance, Carousel sequence acceptance, operator approval, delivery authorization, downstream consumption acknowledgement, publication, certification, and production authority are distinct receipts. None is inferred from another.

### 3.9 Determinism, thresholds, and `NOT_APPLICABLE`

Canonical output depends only on immutable inputs and pinned algorithms, registries, fonts, renderers, evaluators, and environment claims. Wall time, random defaults, dictionary order, filesystem order, host paths, environment variables, and provider aliases are excluded.

No threshold, slide-count range, text budget, aspect ratio, atlas score, provider requirement, or repair preference is invented by this spec. Such values must be present in a ratified profile with an exact hash. Historical `0.72`, `0.84`, weighted-score, five-to-twelve-slide, default-character-budget, and `4:5` rules are migration evidence only.

`NOT_APPLICABLE` requires requirement ID, exact governed rule/version/hash, evaluated condition facts, evidence, owner, reason, and claim restriction. It cannot waive source lineage, approved text, category identity, Composition Intent, required Feature Contracts, inherited locks, actual artifact bytes, or evaluation.

### 3.10 Claim ceiling and forbidden behavior

Forbidden behaviors include loose-prompt production, source-less claims, model-created human authority, renderer-owned meaning, producer self-acceptance, synthetic artifact hashes, current-alias-only dependencies, destructive invalidation, silent fallback, cross-category profile reuse, hidden in-place correction, and treating successful parsing as behavioral enforcement.

This spec ends at `WRITTEN_PENDING_AUDIT`. Before ratification it cannot exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; it cannot be `ACCEPTED_FOR_BUILD`, implemented, certified, or used to issue a Development Capsule.

## 4. Current brownfield architecture

### 4.1 Observed components

| Component | Actual observed behavior | Disposition | Migration constraint |
|---|---|---|---|
| Builder `category_runtime_rules.py` | Emits immutable category operating rules with Carousel slide-role, swipe-order, continuity requirements; prohibits frame-time aliasing, certification inheritance, cross-category repair; reports external evidence pending and production/certification false | `REUSE_AS_INPUT_CONTRACT` | Consume published bytes through an adapter; no Pipeline import of Builder source and no readiness uplift |
| `contracts/carousel_engine.py` | Broad Pydantic model set with useful role/sequence/source/render concepts, but random IDs, wall time, mutable records, open dictionaries, strings, defaults, local thresholds/scores and mixed authority | `ADAPT_CONCEPTS_REPLACE_CONTRACTS` | Preserve historical bytes; field-by-field migration with explicit gaps; no automatic approval migration |
| `carousel_engine_service.py` | Sequential in-memory workflow invents claims, roles, assets, visual system, style routes and hypotheses; mutates variants; self-selects/evaluates/exports | `REPLACE` | Do not promote default-generated state; only exact source-linked evidence may migrate |
| `carousel_render_service.py` | Returns URIs and hashes computed from request IDs without rendering/storing image bytes | `REPLACE` | Synthetic receipts remain historical test evidence only |
| `carousel_eval_service.py` | Accepts caller-supplied score defaults and creates local pass/fail | `REPLACE` | No score or PASS migrates as independent evaluation |
| `repositories/carousel_engine.py` | Process-local dictionary stores without aggregate transaction, command/event/idempotency/outbox/dependency bijection | `REPLACE` | Historical snapshots read-only; durable aggregate repository must prove atomicity |
| legacy Carousel tests | Validate useful denials but include a fake end-to-end path and fixed local evaluation | `ADAPT` | Retain negative intent; replace with artifact, ownership, state, determinism and receipt assertions |
| legacy format adapter | Carries source spans/thesis/sequence but uses open dictionaries, random IDs/time and an old authorization surface | `ADAPT` | Strict projection from exact `ContentDerivativeJob`; no source-program mutation |
| TS-CMF-096 | Separates slide meaning from sequence and concrete geometry, but assigns meaning to a historical registry and old primitive rules | `ADAPT` | Current AIR meaning and Builder profile govern; registry is evidence/candidate syntax only |
| TS-CMF-097 | Defines a useful staged source-to-render/export spine and actual-artifact intent, but contains old product paths, provider assumptions, open models and approval conflation | `ADAPT` | TS-STA owns static runtime; current owners and capability registry replace named providers |
| TS-CMF-098 | Separates visual grammar from semantic slide role, but includes an unratified atlas and invented numeric score thresholds | `ARCHIVE_AS_AUTHORITY_ADAPT_GRAMMAR_CONCEPT` | Candidate records require governed adoption; no threshold/profile inheritance |
| Interview-first V9 doctrine | Establishes source/session/Expression Moment multi-derivative lineage and guest truth principle | `ADAPT_AS_LINEAGE_EVIDENCE` | Current Interview Expression and AIR contracts supersede historical object authority |

### 4.2 Brownfield conclusion

There is no current Pipeline source implementation under `05_ATOMIC_HARNESS_PIPELINE`; only candidate Tech Specs exist. No predecessor module is activated by this document. The correct migration is an anti-corruption boundary that reads exact historical records, classifies every field as preserved/transformed/unavailable, and emits either a new immutable candidate record plus migration receipt or a typed blocker. It does not copy the Studio service into Pipeline.

### 4.3 Historical data migration rules

- Random UUIDs, wall-time timestamps, local status, default scores, approval flags, inferred claims, inferred roles, synthetic hashes, and open payloads are non-authoritative.
- A legacy claim migrates only with exact source and transformation lineage.
- A legacy slide meaning/atom/atlas ID migrates only if mapped by a current adopted registry and AIR-owned semantic reference.
- A legacy render receipt migrates only as historical synthetic evidence unless actual bytes and a verified hash exist.
- A legacy approval never becomes current acceptance.
- Missing source, profile, composition, lock, evaluator, or artifact evidence is not guessed.

## 5. Proposed architecture and workflows

### 5.1 Components

| Component | Responsibility |
|---|---|
| `CarouselAdmissionService` | Verify exact derivative job, authority, source, Harness/category/profile, AIR, VAE/static dependencies, locks and claim ceiling |
| `CarouselSemanticCoverageValidator` | Prove required upstream semantic/source objects are present and unchanged; never create them |
| `CarouselRoleAndSwipeCompiler` | Apply a pinned current rule profile to exact AIR sequence steps and emit typed operational roles/transitions |
| `CarouselSourceEvidenceCompiler` | Compile element-level source, claim, quote, transformation, speaker and approval lineage |
| `CarouselContinuityCompiler` | Compile recurrence groups, invariants, allowed variations, terminology and cross-slide dependency constraints |
| `CarouselSlideProgramCompiler` | Bind each role/source/continuity slice to exact AIR Composition Intent and produce a TS-STA child request |
| `CarouselAssetCoordinator` | Validate exact VAE result/production acceptance and record separate Pipeline consumption acknowledgements |
| `CarouselStaticRuntimeCoordinator` | Dispatch and track TS-STA child programs without duplicating static runtime behavior |
| `CarouselSequenceValidator` | Validate ordered artifact/source/geometry/continuity and category-native swipe behavior |
| `CarouselEvaluationCoordinator` | Run deterministic gates and independent profile-pinned judgment evaluations |
| `CarouselExportCompiler` | Build ordered images, contact sheet, geometry report, accessibility data and platform variants from actual bytes |
| `CarouselDecisionService` | Record attributable accept/reject/contest/revision/HumanResolution decisions over exact candidate bytes |
| `CarouselRepository` | Atomic aggregate/artifact/receipt/command/event/dependency/outbox/idempotency/current projection storage |
| `CarouselInvalidationAndReplayService` | Selectively invalidate affected descendants and reproduce historical decisions from exact bytes |

### 5.2 Workflow A — admission and semantic closure

1. `AdmitCarouselJobCommand` supplies the exact `ContentDerivativeJob`, expected Carousel aggregate revision, actor/delegation, authority snapshot, category/profile registry snapshot and idempotency key.
2. Verify job schema/version/hash/owner/lifecycle; derivative kind `carousel`; category identity; profile owner/state; Harness definition and execution binding; runtime capabilities; source-use grant; approved source package; AIR semantic production/transfer refs; approved Final Script; Primitive Coalition Contract; Coalition Signature; Edge Product; viewer role/tension; archetype coalition; Brand Context, Guest Voice DNA and Visual DNA; evaluation/review owners; Composition Intent; Feature Contracts; T/V requirements; inherited locks; output constraints; budget and cancellation law.
3. Verify interview source-kind provenance when applicable. Validate quote/source spans and source restrictions without inferring values.
4. Verify the job is `ADMITTED_NOT_EXECUTION_AUTHORIZED` or the exact future state required by TS-AHP-003; this spec does not grant execution authorization.
5. Freeze `CarouselInputClosure` and emit `CarouselInputsAdmitted` or a typed denial. No slide plan or render attempt exists on denial.

### 5.3 Workflow B — compile slide roles and swipe order

1. Load exact `CarouselRoleMappingProfile` and validate its owner, current lifecycle, category identity, compatibility features and hash.
2. Iterate AIR sequence steps in declared semantic order; never sort by model score or source time unless the upstream sequence says so.
3. For each step, evaluate deterministic role rules against exact Activative function, viewer-state transition, tension operation, source/evidence class, approved text segment, Primitive bindings and profile position constraints.
4. If no role is eligible, block with `CAROUSEL_ROLE_MAPPING_UNSATISFIED`. If multiple roles require taste/new meaning, emit `CarouselRoleSelectionRequired`; the selection is attributable and limited to eligible roles.
5. Compile per-slide entry/inhabit/exit states, semantic job ref, source purpose, delivery-function refs and transition contract. Prove index continuity and a deletion rationale for every slide.
6. Validate that the ordered roles realize the exact upstream Activative sequence and approved closure/Call; emit immutable `CarouselRoleAndSwipePlan` plus rule-evaluation receipt.

### 5.4 Workflow C — compile source/evidence and language transformation map

1. Enumerate every visible text, claim, quote, evidence marker, portrait/keyframe, diagram, logo and attribution element declared by the approved program.
2. Resolve exact source package/span, speaker, evidence, transformation type, approval receipt, restriction and display-disclosure requirement.
3. Compare verbatim text bytes after the exact governed normalization profile. Mismatch blocks; normalization cannot remove semantic punctuation or omissions unless the profile explicitly permits it.
4. Verify condensations/bridges/omissions have an upstream-authorized transformation record. Missing authorization routes to source/AIR/operator ownership.
5. Compile a per-slide and whole-sequence `CarouselSourceEvidenceMap`. Every source-backed assertion must resolve to evidence; every non-claim is explicitly typed.

### 5.5 Workflow D — compile cross-slide continuity

1. Build continuity groups for identity, terminology, role/tension, claim/evidence, visual motifs, hierarchy, reading path, typography, palette, key assets, source attribution, locks and sequence markers.
2. For each group, record exact invariant, allowed variation, governed owner, slides, tolerance profile and failure behavior.
3. Validate that variation supports Carousel-native sequence progression and does not turn continuity into sameness.
4. Detect ungoverned drift, semantic reversal, quote/source conflict, continuity gaps, adjacent repetition prohibited by profile, and cross-slide lock weakening.
5. Emit `CarouselContinuityPlan` and pre-render validation receipt. A blocked group stops only dependent slide programs; shared semantic/source invalidity blocks the sequence.

### 5.6 Workflow E — compile and execute per-slide static programs

1. For each slide, bind the exact role/swipe step, source-evidence entries, continuity obligations, category/profile constraints, AIR Composition Intent/BBOX function and WHY, Feature Contracts, T/V requirements, identity/continuity refs, approved text, VAE assets and complete inherited lock set.
2. Validate every VAE asset against its Visual Asset Demand/result/production-acceptance versions, realization geometry/tolerance, source/identity lineage and current invalidation state. Record a separate Pipeline consumption acknowledgement; do not duplicate VAE production evaluation.
3. Create a `CarouselSlideStaticRequest` compatible with the frozen TS-STA interface and record its child ordinal and parent dependency edges.
4. TS-STA compiles renderer-neutral IR, final-font measurement, deterministic solved geometry, annotation cues, sealed static render program, real artifact ingestion, reparse and evaluation evidence.
5. Carousel coordinates child state but cannot bypass, weaken or locally fork TS-STA gates. A failed slide blocks sequence export; independently valid slide artifacts remain historical and reusable if their dependency closure is unchanged.
6. Store exact child program/artifact/receipt refs. Slide index and declared order, not completion order, govern sequence identity.

### 5.7 Workflow F — sequence validation and evaluation

1. Once all required slide candidates are ingested, mechanically validate count/profile, indices, dimensions, media types, text/source maps, geometry reports, artifact hashes, continuity groups, recurring identities, term consistency, role/swipe transitions, lock realization and ordered manifest.
2. Reparse the ordered artifacts as a sequence and compare observations against role/swipe and continuity plans.
3. Run independent evaluator(s) under a pinned Carousel profile for source fidelity, claim support, slide-role integrity, swipe progression, cross-slide continuity, identity/Visual DNA, hierarchy/readability, composition effectiveness, wrong-reading resistance, and approved closure.
4. No local score defaults or invented threshold apply. Missing profile/evaluator evidence produces a blocker or explicit `EVALUATION_UNAVAILABLE` state according to the exact requirement; it never produces PASS.
5. Emit candidate sequence evaluation and route exact failures to the responsible source, AIR, Builder/profile, VAE, Pipeline static, Pipeline Carousel, evaluator or human-policy layer.

### 5.8 Workflow G — export and operator decision

1. `CompileCarouselExportPackageCommand` pins the accepted candidate slide set and exact target delivery profiles.
2. Verify each requested variant’s dimensions, color profile, format, safe/reserved areas, slide cap, accessibility requirements and packaging features from the pinned profile.
3. Generate actual ordered image files, a contact sheet/preview, geometry report, source/evidence map, alt-text records, evaluation refs, restrictions, and manifest. Optional PDF/document/editable variants are emitted only if their declared capability ran and produced verified bytes.
4. Recompute every file digest and total bundle digest; use relative logical paths only. A URI, filename or provider claim without bytes is failure.
5. An attributable operator reviews exact package/evaluation bytes and records `ACCEPT`, `REJECT`, `CONTEST`, or `REQUEST_REVISION`. Acceptance does not imply delivery/publication/production/certification.
6. Delivery requires a separate authorized command; downstream consumption acknowledgement refers to exact accepted bytes and does not repeat visual evaluation.

### 5.9 Workflow H — correction, cancellation, invalidation and replay

Correction routes narrowly: source/quote/transformation/approval to Interview Expression/source owner/operator; semantic role/tension/Final Script/Composition Intent/Feature/locks to AIR; Harness/category/profile to Builder; missing/incorrect visual realization to VAE; per-slide IR/measurement/geometry/render to TS-STA Pipeline; slide order/continuity/export to Carousel Pipeline; transport to Delegation; unresolved taste to operator/Studio.

Each correction creates a new immutable version. Source-text change invalidates its source map, dependent slide/static program/artifacts, sequence evaluation and exports. One VAE asset change invalidates dependent slide(s) and sequence/export evidence, not unrelated semantic analysis. A role/swipe change invalidates that step and downstream sequence relations. Profile change invalidates affected plans/evaluations. Historical bytes remain addressable.

Cancellation before atomic dispatch prevents work. After dispatch it appends a cancellation event and worker-cancel outbox; late results are quarantined as noncanonical evidence. Exact replay uses stored immutable inputs, profiles, renderer/environment/model responses and artifact bytes. A current-state rerun is a new attempt, not historical replay.

### 5.10 State machine and atomicity

```text
REQUESTED -> INPUTS_ADMITTED -> ROLE_SWIPE_COMPILED -> SOURCE_MAP_COMPILED
 -> CONTINUITY_COMPILED -> SLIDE_PROGRAMS_COMPILED -> SLIDES_RENDERING
 -> SLIDE_ARTIFACTS_INGESTED -> SEQUENCE_VALIDATED -> EVALUATED
 -> EXPORT_COMPILED -> OPERATOR_REVIEW
 -> ACCEPTED | REJECTED | CONTESTED | REVISION_REQUESTED

Any eligible state may transition to CANCELLED, SUPERSEDED, INVALIDATED or REVOKED.
```

Each state mutation atomically commits aggregate/version, canonical artifact bytes, command, events, success/failure receipt, dependency edges, idempotency record, current projection and outbox. Partial success is not visible as the next state. Same idempotency scope/key plus identical canonical request returns the original outcome; different bytes fail. Compare-and-swap expected revision prevents concurrent role selection, child-set selection, export or operator-decision races.

## 6. Data models, contracts, schemas, and APIs

### 6.1 Canonical rules

All records are immutable, closed and versioned. No untyped open dictionaries, implied defaults, random IDs, wall-clock-derived identity, NaN/infinity, absolute paths or mutable aliases are permitted. Canonical JSON is UTF-8, NFC, lexicographically keyed, integer/fixed-point for governed numbers, schema-ordered where order is semantic, schema-sorted for set-like arrays, and has one terminal newline. Hashes are lowercase SHA-256 over canonical bytes excluding self-hash, storage locator, observation time and transport retry metadata.

`ImmutableRef` contains object kind/ID, immutable version, schema ID/version, lowercase content hash, owner product, authority owner, lifecycle state at use and relative logical URI. Unknown enum values or unsupported required extensions reject. Current-only references are invalid.

### 6.2 Input closure

Schema `ca.pipeline.carousel-input-closure/2.1.0-candidate`:

```text
CarouselInputClosure {
  closure_id: ContentAddressedId
  derivative_job_ref: ImmutableRef
  batch_program_ref: ImmutableRef
  authority_snapshot_ref: ImmutableRef
  source_use_grant_ref: ImmutableRef
  source_package_ref: ImmutableRef
  source_inventory_ref: ImmutableRef
  reaction_receipt_refs: ordered ImmutableRef[*]
  expression_moment_refs: ordered ImmutableRef[*]
  semantic_production_package_ref: ImmutableRef
  activation_transfer_contract_ref: ImmutableRef
  approved_final_script_ref: ImmutableRef
  primitive_coalition_contract_ref: ImmutableRef
  coalition_signature_ref: ImmutableRef
  matrix_result_ref: ImmutableRef
  edge_product_ref: ImmutableRef
  viewer_role_tension_ref: ImmutableRef
  archetype_coalition_ref: ImmutableRef
  brand_context_ref: ImmutableRef
  guest_voice_dna_ref: ImmutableRef
  visual_dna_ref: ImmutableRef
  category_profile_ref: ImmutableRef
  harness_definition_ref: ImmutableRef
  harness_execution_binding_ref: ImmutableRef
  composition_program_ref: ImmutableRef
  feature_contract_refs: ordered ImmutableRef[1..N]
  tv_route_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  wrong_reading_lock_refs: ordered ImmutableRef[1..N]
  evaluation_profile_ref: ImmutableRef
  review_policy_ref: ImmutableRef
  runtime_capability_refs: ordered ImmutableRef[1..N]
  production_eligible: false
  certified: false
  canonical_hash: Sha256
}
```

The closure does not copy authoritative semantic payloads into a Pipeline-owned replacement. It carries exact references plus the minimum validated projections needed for execution.

### 6.3 Role and swipe-order plan

Schema `ca.pipeline.carousel-role-swipe-plan/2.1.0-candidate`:

```text
CarouselRoleAndSwipePlan {
  plan_id: ContentAddressedId
  input_closure_ref: ImmutableRef
  role_mapping_profile_ref: ImmutableRef
  category_id: CarouselCategoryId
  profile_ref: ImmutableRef
  sequence_purpose_ref: ImmutableRef
  slides: ordered CarouselSlideStep[2..N]
  sequence_closure_ref: ImmutableRef
  rule_evaluation_receipt_ref: ImmutableRef
  alternatives_resolution_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  canonical_hash: Sha256
}

CarouselSlideStep {
  slide_id: StableSlideId
  slide_index: PositiveUInt
  upstream_sequence_step_ref: ImmutableRef
  slide_role_ref: GovernedSlideRoleRef
  activative_function_ref: ImmutableRef
  semantic_job_ref: ImmutableRef
  entry_viewer_state_ref: ImmutableRef
  psychological_role_tension_ref: ImmutableRef
  tension_operation_ref: ImmutableRef
  exit_viewer_state_ref: ImmutableRef
  guest_voice_delivery_function_refs: ordered ImmutableRef[*]
  approved_script_segment_refs: ordered ImmutableRef[1..N]
  source_purpose_ref: ImmutableRef
  transition_to_next_ref_or_terminal: ImmutableRef | TERMINAL
  deletion_necessity_proof: NecessityProof
  applicable_feature_contract_refs: ordered ImmutableRef[1..N]
  wrong_reading_lock_refs: ordered ImmutableRef[1..N]
}
```

Indices must equal `1..N`; no duplicate slide ID; every upstream sequence step is covered exactly as the mapping profile requires; terminal transition exists only on the last slide. A `GovernedSlideRoleRef` is a member of the pinned category profile, not a free string or historical enum.

### 6.4 Source/evidence and transformation map

Schema `ca.pipeline.carousel-source-evidence-map/2.1.0-candidate`:

```text
CarouselSourceEvidenceMap {
  map_id: ContentAddressedId
  source_package_ref: ImmutableRef
  slides: ordered SlideEvidenceMap[2..N]
  sequence_level_evidence_refs: ordered ImmutableRef[*]
  coverage_receipt_ref: ImmutableRef
  canonical_hash: Sha256
}

SlideEvidenceMap {
  slide_id: StableSlideId
  elements: ordered ContentElementEvidence[1..N]
}

ContentElementEvidence {
  element_id: StableElementId
  element_kind: HEADLINE | BODY | QUOTE | EVIDENCE_LABEL | ATTRIBUTION |
                IMAGE | PORTRAIT | KEYFRAME | DIAGRAM | LOGO | CTA | NON_CLAIM
  displayed_content_sha256: Sha256
  source_kind: GovernedSourceKind
  source_span_refs: ordered ImmutableRef[*]
  evidence_refs: ordered ImmutableRef[*]
  speaker_identity_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  transformation_type: VERBATIM_QUOTE | DISCLOSED_OMISSION | FAITHFUL_CONDENSATION |
                       OPERATOR_AUTHORED_BRIDGE | APPROVED_FINAL_SCRIPT_TEXT | NON_CLAIM_LABEL
  transformation_record_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  approval_receipt_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  required_display_disclosure_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  restrictions: ordered RestrictionRef[*]
}
```

Positive example: an exact quote element links displayed bytes, source transcript span, speaker, `VERBATIM_QUOTE`, source approval and restriction refs. Negative example: a shortened sentence labeled verbatim with no omission record fails `CAROUSEL_QUOTE_MISMATCH`.

### 6.5 Continuity plan

Schema `ca.pipeline.carousel-continuity-plan/2.1.0-candidate`:

```text
CarouselContinuityPlan {
  plan_id: ContentAddressedId
  role_swipe_plan_ref: ImmutableRef
  continuity_profile_ref: ImmutableRef
  groups: ordered ContinuityGroup[1..N]
  variation_decisions: ordered VariationDecision[*]
  pre_render_validation_receipt_ref: ImmutableRef
  canonical_hash: Sha256
}

ContinuityGroup {
  group_id: StableGroupId
  dimension: IDENTITY | TERMINOLOGY | SOURCE_CLAIM | ROLE_TENSION | HIERARCHY |
             READING_PATH | VISUAL_MOTIF | TYPOGRAPHY | COLOR | ASSET_RECURRENCE |
             ATTRIBUTION | WRONG_READING_LOCK | SEQUENCE_MARKER
  owner_ref: OwnerRef
  participating_slide_ids: ordered StableSlideId[1..N]
  invariant_ref: ImmutableRef
  allowed_variation_ref: ImmutableRef
  evaluation_rule_ref: ImmutableRef
  failure_scope: SLIDE_LOCAL | SLIDE_SET | SEQUENCE
}
```

A variation decision cannot alter an AIR-owned semantic invariant. Recurring asset use requires exact asset version and a sequence reason; continuity never authorizes stale or revoked assets.

### 6.6 Slide static request and artifact binding

Schema `ca.pipeline.carousel-slide-static-request/2.1.0-candidate`:

```text
CarouselSlideStaticRequest {
  request_id: ContentAddressedId
  carousel_program_ref: ImmutableRef
  slide_step_ref: ImmutableRef
  source_evidence_slice_ref: ImmutableRef
  continuity_obligation_refs: ordered ImmutableRef[1..N]
  semantic_composition_intent_ref: ImmutableRef
  bbox_function_and_why_refs: ordered ImmutableRef[1..N]
  feature_contract_refs: ordered ImmutableRef[1..N]
  tv_route_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  identity_continuity_refs: ordered ImmutableRef[1..N]
  approved_text_refs: ordered ImmutableRef[1..N]
  visual_asset_consumption_refs: ordered VisualAssetConsumptionRef[*]
  inherited_wrong_reading_lock_refs: ordered ImmutableRef[1..N]
  added_stricter_lock_refs: ordered ImmutableRef[*]
  static_output_profile_ref: ImmutableRef
  static_evaluation_profile_ref: ImmutableRef
  child_ordinal: PositiveUInt
  canonical_hash: Sha256
}

CarouselSlideArtifactBinding {
  slide_id: StableSlideId
  static_request_ref: ImmutableRef
  static_composition_ir_ref: ImmutableRef
  solved_plan_ref: ImmutableRef
  geometry_report_ref: ImmutableRef
  render_program_ref: ImmutableRef
  artifact_refs: ordered ArtifactRef[1..N]
  reparse_receipt_ref: ImmutableRef
  static_evaluation_ref: ImmutableRef
  static_acceptance_ref: ImmutableRef
  dependency_refs: ordered ImmutableRef[1..N]
}
```

The complete parent lock set must be a subset of each child request’s effective lock set by exact identity or governed successor relation. Any weakening fails before static compilation.

### 6.7 Carousel program

Schema `ca.pipeline.carousel-runtime-program/2.1.0-candidate`:

```text
CarouselRuntimeProgram {
  program_id: ContentAddressedId
  version: ImmutableVersion
  lifecycle_state: CarouselLifecycleState
  input_closure_ref: ImmutableRef
  role_swipe_plan_ref: ImmutableRef
  source_evidence_map_ref: ImmutableRef
  continuity_plan_ref: ImmutableRef
  slide_static_request_refs: ordered ImmutableRef[2..N]
  slide_dependency_graph_ref: ImmutableRef
  category_profile_ref: ImmutableRef
  export_profile_refs: ordered ImmutableRef[1..N]
  evaluation_profile_ref: ImmutableRef
  review_policy_ref: ImmutableRef
  claim_ceiling: ClaimCeiling
  production_eligible: false
  certified: false
  supersedes_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  canonical_hash: Sha256
}
```

Program identity preserves declared slide order. Completion order and worker scheduling are excluded from canonical identity.

### 6.8 Sequence evaluation

```text
CarouselSequenceObservation {
  observation_id: ContentAddressedId
  program_ref: ImmutableRef
  ordered_slide_artifact_refs: ordered ArtifactRef[2..N]
  observed_source_labels: ordered SourceLabelObservation[*]
  observed_role_transition_refs: ordered ObservationRef[*]
  continuity_observations: ordered ContinuityObservation[1..N]
  geometry_readability_observations: ordered ObservationRef[1..N]
  lock_realization_observations: ordered ObservationRef[1..N]
  canonical_hash: Sha256
}

CarouselSequenceEvaluation {
  evaluation_id: ContentAddressedId
  observation_ref: ImmutableRef
  evaluation_profile_ref: ImmutableRef
  evaluator_refs: ordered ImmutableRef[1..N]
  deterministic_gate_results: ordered GateResult[1..N]
  judgment_dimension_results: ordered DimensionResult[1..N]
  failure_attributions: ordered FailureAttribution[*]
  verdict: PASS | FAIL | CONTESTED | EVALUATOR_UNAVAILABLE
  limitations: ordered Limitation[*]
  canonical_hash: Sha256
}
```

The evaluation profile defines dimensions, evidence and thresholds. A producer ID cannot equal an independent evaluator ID where separation is required.

### 6.9 Export package

Schema `ca.pipeline.carousel-export-package/2.1.0-candidate`:

```text
CarouselExportPackage {
  package_id: ContentAddressedId
  carousel_program_ref: ImmutableRef
  accepted_candidate_set_ref: ImmutableRef
  ordered_slide_artifacts: ordered CarouselExportSlide[2..N]
  contact_sheet_ref: ArtifactRef
  preview_ref: ArtifactRef
  geometry_report_ref: ArtifactRef
  source_evidence_map_ref: ImmutableRef
  continuity_report_ref: ImmutableRef
  evaluation_ref: ImmutableRef
  accessibility_manifest_ref: ArtifactRef
  platform_variants: ordered PlatformVariant[1..N]
  restrictions: ordered RestrictionRef[*]
  approval_state: CANDIDATE_NOT_REVIEWED | ACCEPTED | REJECTED | CONTESTED
  operator_decision_ref_or_not_applicable: ImmutableRef | ApplicabilityDecision
  delivery_authorized: false
  production_eligible: false
  certified: false
  package_sha256: Sha256
}

CarouselExportSlide {
  slide_id: StableSlideId
  slide_index: PositiveUInt
  primary_image_ref: ArtifactRef
  variant_refs: ordered ArtifactRef[*]
  alt_text_record_ref: ImmutableRef
  static_receipt_ref: ImmutableRef
  source_evidence_slice_ref: ImmutableRef
  geometry_report_slice_ref: ImmutableRef
}

PlatformVariant {
  target_profile_ref: ImmutableRef
  ordered_artifact_refs: ordered ArtifactRef[2..N]
  delivery_manifest_ref: ArtifactRef
  transformation_receipt_ref: ImmutableRef
}
```

Every artifact carries media type, byte length, dimensions where applicable, color profile, content address, lowercase SHA-256 and relative logical filename. A package with a missing file, duplicate slide index, mismatched digest, stale child or unsupported target is invalid.

### 6.10 Commands, events, repository, and API

Commands:

```text
AdmitCarouselJob
CompileCarouselRoleAndSwipePlan
ResolveCarouselRoleSelection
CompileCarouselSourceEvidenceMap
CompileCarouselContinuityPlan
CompileCarouselSlidePrograms
AuthorizeCarouselSlideExecution
RecordCarouselSlideOutcome
ValidateCarouselSequence
EvaluateCarouselSequence
CompileCarouselExportPackage
RecordCarouselOperatorDecision
AuthorizeCarouselDelivery
RequestCarouselCorrection
CancelCarouselCommand
SupersedeCarouselProgram
InvalidateCarouselDescendants
ReplayCarouselDecision
```

Events include `CarouselInputsAdmitted`, `CarouselAdmissionDenied`, `CarouselRoleSwipeCompiled`, `CarouselRoleSelectionRequired`, `CarouselSourceMapCompiled`, `CarouselContinuityCompiled`, `CarouselSlideProgramsCompiled`, `CarouselSlideExecutionAuthorized`, `CarouselSlideOutcomeRecorded`, `CarouselSequenceValidated`, `CarouselSequenceEvaluated`, `CarouselExportCompiled`, `CarouselOperatorDecisionRecorded`, `CarouselDeliveryAuthorized`, `CarouselCorrectionRequested`, `CarouselCommandCancelled`, `CarouselSuperseded`, `CarouselInvalidated`, `CarouselRevoked`, and `CarouselHistoricalReplayVerified`.

Every command contains command ID, idempotency key, actor/delegation scope, aggregate ID/version, expected revision, authority/profile snapshots, causation/correlation, cancellation ref and canonical request hash. Callers cannot supply accepted/certified/production state.

Future API:

```text
POST /v2/pipeline/carousels:admit
POST /v2/pipeline/carousels/{id}/versions/{version}:compile-sequence
POST /v2/pipeline/carousels/{id}/versions/{version}:compile-slides
POST /v2/pipeline/carousels/{id}/versions/{version}:validate
POST /v2/pipeline/carousels/{id}/versions/{version}:evaluate
POST /v2/pipeline/carousels/{id}/versions/{version}:compile-export
POST /v2/pipeline/carousels/{id}/versions/{version}:decide
POST /v2/pipeline/carousels/{id}/versions/{version}:invalidate
GET  /v2/pipeline/carousels/{id}/versions/{version}
GET  /v2/pipeline/carousels/{id}/versions/{version}/lineage
GET  /v2/pipeline/carousels/{id}/versions/{version}/receipts
```

HTTP success is transport success, not acceptance. Responses identify exact version/hash/receipt and claim ceiling.

`CarouselRepository` provides exact-version get, compare-and-swap atomic append, content blob storage, command/idempotency lookup, dependency traversal, current projection, outbox and historical reconstruction. An in-memory adapter implements the identical contract for tests and returns copies/immutable values; it cannot expose live shared state.

### 6.11 Compatibility, supersession, and migration

Compatibility is semantic, not parse-only. Negotiation requires features for source-element lineage, category-native role/swipe plan, Composition Intent preservation, full lock inheritance, per-slide TS-STA handoff, real artifact ingestion, continuity evidence, selective invalidation, portable export and the requested profile capabilities. Unsupported required features reject.

Adapters cannot drop source/provenance/transformation, semantic refs, profile/owner, Feature Contracts, T/V, locks, sequence order, continuity, evaluation or restrictions. Migration produces new immutable artifacts and a receipt linking old/new hashes, preserved fields, unavailable fields, blockers and claim ceiling. Active historical runs remain pinned to negotiated versions; deprecation does not erase reproducible history.

## 7. Implementation stages and exact target paths

No path in this section is created or modified by this writing prompt. A later authorized Development Capsule must bound the work further.

### 7.1 Stage 0 — contract/profile adoption gate

Validate ratified authority, adopted TS-AHP-003 and TS-STA-001 interfaces, current Carousel category/profile registry, source/transformation contracts, evaluator profile, and runtime capabilities. Map `FR-055`, `FR-059`, AC-01 through AC-05.

### 7.2 Stage 1 — domain contracts

```text
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/domain/models.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/domain/source_evidence.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/domain/role_swipe.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/domain/continuity.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/domain/lifecycle.py
```

Implement strict immutable contracts and canonicalization. Map `FR-055`–`FR-058`, `FR-145`, AC-06 through AC-16.

### 7.3 Stage 2 — application services and ports

```text
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/commands.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/admission.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/compiler.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/evaluation.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/export.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/application/invalidation.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/ports/static_runtime.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/ports/source_products.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/ports/repository.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/ports/evaluation.py
```

Map `FR-056`–`FR-060`, `FR-145`, AC-07 through AC-23.

### 7.4 Stage 3 — persistence, adapters, and workers

```text
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/adapters/persistence/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/adapters/static_runtime/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/adapters/source_products/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/adapters/evaluation/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/workers/orchestration.py
```

Adapters consume published contracts only; they do not import product source trees. Map `FR-058`–`FR-060`, AC-17 through AC-26.

### 7.5 Stage 4 — API and projections

```text
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/api/commands.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/api/queries.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/carousel/projections/operator_read_model.py
```

Transport adapters remain decision-free. Operator projections show exact slide/source, candidate/evaluation, blocker, lineage and claim-ceiling evidence. Map `FR-060`, `FR-145`, AC-22 through AC-28.

### 7.6 Exact future test paths

```text
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/unit/test_admission.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/unit/test_role_swipe_compiler.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/unit/test_source_evidence.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/unit/test_continuity.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/unit/test_export_manifest.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/contracts/test_carousel_schemas.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/contracts/test_static_runtime_interface.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/integration/test_source_to_export.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/integration/test_atomic_repository.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/integration/test_selective_invalidation.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/integration/test_historical_replay.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/architecture/test_import_boundaries.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/security/test_untrusted_inputs.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/portability/test_fresh_process_reproduction.py
05_ATOMIC_HARNESS_PIPELINE/tests/carousel/reference_slice/test_imported_interview_carousel.py
```

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Meaning | Recovery owner/action |
|---|---|---|
| `CAROUSEL-JOB-INELIGIBLE` | Derivative job state/category/owner/hash is invalid | Batch/Pipeline owner; new valid job |
| `CAROUSEL-CATEGORY-MISMATCH` | Not exact Carousel category or cross-category profile reuse | Builder/profile owner |
| `CAROUSEL-PROFILE-UNRATIFIED` | Requested profile lacks current authority | Builder/Program Control; no production claim |
| `CAROUSEL-SEMANTIC-CLOSURE-INCOMPLETE` | Required AIR meaning/Final Script/Primitive/archetype/Composition ref absent | AIR/upstream owner; no reconstruction |
| `CAROUSEL-SOURCE-KIND-UNKNOWN` | Missing/unknown/ambiguous source kind | Source owner; never guess |
| `CAROUSEL-INTERVIEW-PROVENANCE-INCOMPLETE` | Interview source lacks Reaction Receipt or Expression Moment refs | Interview Expression |
| `CAROUSEL-ROLE-MAPPING-UNSATISFIED` | No governed role fits an AIR step | Profile/AIR owner |
| `CAROUSEL-ROLE-SELECTION-REQUIRED` | Multiple eligible roles require meaning/taste decision | Attributable human/AIR route |
| `CAROUSEL-SWIPE-SEQUENCE-INVALID` | Entry/transition/exit or index/deletion proof fails | Pipeline compiler or AIR if semantic |
| `CAROUSEL-QUOTE-MISMATCH` | Displayed quote does not match source under governed normalization | Source/operator; new transformation record |
| `CAROUSEL-TRANSFORMATION-UNAUTHORIZED` | Condensation/omission/bridge lacks approval | Source/AIR/operator |
| `CAROUSEL-SOURCE-EVIDENCE-ORPHAN` | A source-backed assertion has no evidence | Source owner |
| `CAROUSEL-CONTINUITY-DRIFT` | Ungoverned identity/term/role/visual drift | Attributed group owner |
| `CAROUSEL-COMPOSITION-INTENT-MISSING` | Slide lacks exact AIR intent | AIR; no atlas substitution |
| `CAROUSEL-LOCK-INHERITANCE-VIOLATION` | Child removes/weakens parent lock | Pipeline compiler/upstream amendment only |
| `CAROUSEL-VAE-ASSET-STALE` | Visual result/demand/acceptance relation is stale or invalid | VAE/upstream demand owner |
| `CAROUSEL-STATIC-CHILD-FAILED` | TS-STA child blocked/failed | Exact TS-STA failure owner |
| `CAROUSEL-ARTIFACT-BYTES-MISSING` | Claimed output has no actual retrievable bytes | Worker/storage owner |
| `CAROUSEL-SEQUENCE-EVALUATOR-UNAVAILABLE` | Required independent evaluator/profile absent | Evaluation owner; no synthetic PASS |
| `CAROUSEL-EXPORT-PROFILE-UNSUPPORTED` | Target capability/profile unsupported | Profile/runtime owner |
| `CAROUSEL-EXPORT-HASH-MISMATCH` | Export bytes differ from manifest | Pipeline export/storage owner |
| `CAROUSEL-IDEMPOTENCY-CONFLICT` | Key reused with different canonical command | Caller |
| `CAROUSEL-REVISION-CONFLICT` | Compare-and-swap expected revision stale | Caller rereads/retries |
| `CAROUSEL-ATOMIC-COMMIT-FAILED` | Success bundle not wholly committed | Safe retry after reconciliation |
| `CAROUSEL-CANCELLED-LATE-RESULT` | Worker result arrived after cancel/supersession | Quarantine; never resurrect |
| `CAROUSEL-REPLAY-DEPENDENCY-UNAVAILABLE` | Exact historical dependency cannot be read | Evidence owner; never substitute |
| `CAROUSEL-LEGACY-EVIDENCE-INCOMPLETE` | Legacy record lacks required current evidence | Migration owner; block current promotion |

Failures contain stable code, responsible layer, exact refs/hashes, retry class, safe operator message and next admissible action. They do not expose credentials, restricted source content or unredacted prompts in external logs.

### 8.2 Retry, quality repair, cancellation, and partial result

Infrastructure retry is allowed only for the same pinned canonical request and idempotent worker key. A timeout with uncertain completion is reconciled before retry. Semantic or quality failures create a new correction command/version; they are not transport retries.

A slide child may finish while another fails, but the sequence cannot reach export-candidate state until all required children are current and validated. Valid child artifacts remain stored and may be reused only when their exact dependency closure still matches. Cancellation cannot delete committed evidence; late results are stored as noncanonical attempt evidence.

### 8.3 Atomic rollback

Each success commit is all-or-nothing across aggregate state, artifacts/refs, receipt, command, events, dependency edges, idempotency and outbox. If an artifact blob is written before a metadata transaction aborts, it remains unreachable and is garbage-collected only after safe retention verification. Compensation never deletes a blob referenced by any historical receipt.

### 8.4 Selective invalidation and historical replay

The dependency graph includes source package/span, transformation/approval, AIR objects, Harness/profile, locks, VAE assets, static child inputs/artifacts, continuity groups, evaluators, export profiles and operator decisions. Invalidation first emits a proposed affected set and proof, then atomically updates current consumability. Broad regeneration is prohibited without an exact governed incident scope.

Historical replay reads exact stored bytes and historical model/worker responses. Current-state rerun creates a successor. A revoked result remains reproducible but cannot be consumed as current.

### 8.5 Migration and backward compatibility

Legacy data is read through a quarantined adapter. Every field receives `PRESERVED`, `TRANSFORMED_WITH_RULE`, `UNAVAILABLE`, or `REJECTED_AS_NONAUTHORITATIVE`. Migration never infers source kind, profile authority, semantic role, Composition Intent, locks, approval, evaluator result or actual artifact bytes. It produces a new immutable record and migration receipt or `CAROUSEL-LEGACY-EVIDENCE-INCOMPLETE`.

Compatibility requires exact shared feature support, not successful parsing. Unknown required fields/extensions block. Optional unknown extensions preserve bytes and cannot affect semantics until adopted. Active historical executions remain pinned to negotiated versions.

### 8.6 Rollback and degraded operation

Rollback disables new admissions/exports for the faulty version and restores the last compatible implementation/profile for new commands only. It does not rewrite current or historical artifacts. If VAE, static render, evaluator, storage or delivery capability is unavailable, only profile-declared unaffected work may proceed; no fake URI/hash, local default provider, or producer self-score is emitted. A preview is never substituted for a final artifact.

### 8.7 Observability

Metrics: admission/denial by code; role-mapping alternatives; quote/transformation failures; source coverage; slide-child duration/failure; continuity failures by dimension; evaluator availability; sequence verdicts; artifact byte/hash mismatch; export variants; atomic rollback; idempotency conflict; cancellation/late result; invalidation breadth; replay success; and consumption acknowledgement.

Traces carry batch/job/carousel/slide/static-child/attempt/capsule/receipt correlations without raw restricted content. Logs use IDs, versions, hashes, codes and counts. Alerts cover source-less accepted elements, ineligible profile use, lock weakening, missing artifact/receipt counterpart, producer/evaluator identity collision, broad invalidation, stale-child export, cross-tenant access and deterministic replay drift.

## 9. Behavior-specific acceptance criteria

### AC-01 — Carousel category identity

**Given** a frame-time motion plan or profile owned by another category, **when** admission runs, **then** it returns `CAROUSEL-CATEGORY-MISMATCH` before slide compilation. Failure example: short-video timeline reused as slide order. Evidence: admission receipt. Test layer: contract/integration. Trace: `FR-055`, `ST-05.02`.

### AC-02 — Profile truth

**Given** a historical atlas/profile or structurally supported profile without current authority, **when** production eligibility is requested, **then** it returns `CAROUSEL-PROFILE-UNRATIFIED`; certification remains false. Failure example: historical TS-CMF-098 threshold treated as current. Evidence: authority/profile receipt. Test layer: governance integration. Trace: `FR-059`, `ST-05.02`.

### AC-03 — Complete semantic closure

**Given** a missing approved Final Script or Primitive Coalition Contract, **when** admission runs, **then** no plan is produced and `CAROUSEL-SEMANTIC-CLOSURE-INCOMPLETE` names AIR/upstream ownership. Failure example: compiler invents a “clean educational” script. Evidence: denial receipt. Test layer: unit/contract. Trace: `FR-055`, `FR-056`.

### AC-04 — Interview provenance

**Given** `interview_expression` without nonempty Reaction Receipt and Expression Moment refs, **when** admitted, **then** it fails; non-interview source validates supplied refs but does not require them. Failure example: interview quote accepted from transcript text alone. Evidence: parameterized provenance tests. Test layer: contract. Trace: `FR-145`, `ST-05.02`.

### AC-05 — No guessed source kind

**Given** an unknown or ambiguous source kind, **when** source closure is validated, **then** `CAROUSEL-SOURCE-KIND-UNKNOWN` is returned and no classification is inferred. Evidence: negative fixture and receipt. Test layer: unit. Trace: `FR-145`.

### AC-06 — Typed role mapping

**Given** a complete AIR sequence and current mapping profile, **when** compilation runs, **then** each upstream step maps to a profile-owned slide role with rule evidence and no semantic mutation. Failure example: model invents a “viral hook” role not in the profile. Evidence: role rule receipt. Test layer: unit/property. Trace: `FR-056`.

### AC-07 — Human resolution for genuine alternatives

**Given** two eligible roles with no deterministic rule winner, **when** mapping runs, **then** `CAROUSEL-ROLE-SELECTION-REQUIRED` exposes only eligible alternatives and no model selection becomes current. Evidence: alternatives/decision receipt. Test layer: application integration. Trace: `FR-056`, `ST-05.02`.

### AC-08 — Swipe progression

**Given** an approved viewer role/tension and Activative sequence, **when** swipe plan compiles, **then** entry, tension operation, exit, transition, delivery functions and deletion necessity are explicit for every slide. Failure example: two adjacent slides have no semantic transition. Evidence: swipe-plan receipt. Test layer: unit/integration. Trace: `FR-057`.

### AC-09 — Carousel is not frame-time motion

**Given** a slide plan containing timecodes, FPS-driven state or animation-only transition as semantic order, **when** validated, **then** it fails before static child creation. Evidence: category-native syntax test. Test layer: contract. Trace: `FR-055`, `ST-05.02`.

### AC-10 — Verbatim quote fidelity

**Given** displayed bytes differ from the governed source span, **when** labeled `VERBATIM_QUOTE`, **then** `CAROUSEL-QUOTE-MISMATCH` blocks. Failure example: omitted phrase without disclosure. Evidence: byte/normalization diff. Test layer: unit. Trace: `FR-145`, `ST-05.02`.

### AC-11 — Transformation truth

**Given** a condensation, omission or operator bridge, **when** no exact approved transformation record exists, **then** `CAROUSEL-TRANSFORMATION-UNAUTHORIZED` blocks. Evidence: source map and negative fixture. Test layer: contract/integration. Trace: `FR-145`.

### AC-12 — Every assertion resolves to evidence

**Given** a factual headline without source/evidence refs, **when** source map compiles, **then** `CAROUSEL-SOURCE-EVIDENCE-ORPHAN` blocks that slide and sequence export. Evidence: coverage receipt. Test layer: unit/property. Trace: `FR-145`.

### AC-13 — Cross-slide continuity

**Given** recurring identity, terminology and hierarchy constraints, **when** the continuity plan and rendered sequence are validated, **then** invariants hold and every allowed variation has a governed reason. Failure example: the speaker identity changes between slides. Evidence: continuity report. Test layer: integration/evaluation. Trace: `FR-058`.

### AC-14 — Variation is not sameness

**Given** a profile prohibiting unjustified adjacent repetition, **when** identical visual grammar repeats without a sequence reason, **then** continuity validation fails without inventing a numeric cutoff. Evidence: profile rule receipt. Test layer: unit/evaluation. Trace: `FR-058`.

### AC-15 — AIR Composition Intent preserved

**Given** a slide’s AIR Composition Intent and BBOX function/WHY, **when** static child input is compiled, **then** all refs and allowed-variation rules are exact; missing intent blocks rather than invoking a historical atlas as authority. Evidence: coverage mapping. Test layer: contract. Trace: `FR-056`, `FR-145`.

### AC-16 — Wrong-reading locks are monotonic

**Given** parent locks and a generated/composited slide, **when** the child request compiles, **then** all parent locks are inherited, stricter locks may be added, and weakening/removal fails. Evidence: lock-subset proof. Test layer: property/contract. Trace: `FR-055`, `FR-145`.

### AC-17 — VAE ownership preserved

**Given** a required produced visual asset, **when** consumed, **then** the exact Demand/result/production-acceptance relation and current hash are validated; Pipeline records a separate acknowledgement and does not select production methods. Evidence: VAE consumption receipt. Test layer: cross-product contract. Trace: `FR-145`.

### AC-18 — TS-STA interface conformance

**Given** a valid slide program, **when** dispatched, **then** its request contains exact source, semantic, composition, text, Feature, T/V, identity, asset, lock and profile refs accepted by the pinned TS-STA contract. Failure example: slide sends only pixels and generic notes. Evidence: contract test. Test layer: integration. Trace: `FR-060`, `FR-145`.

### AC-19 — Actual artifacts required

**Given** a worker returns URI and claimed digest without readable bytes, **when** ingestion runs, **then** `CAROUSEL-ARTIFACT-BYTES-MISSING` blocks. Evidence: storage/worker receipt. Test layer: integration. Trace: `FR-060`, `ST-05.02`.

### AC-20 — Ordered export package

**Given** current accepted candidate slide artifacts, **when** export compiles, **then** ordered images, exact manifest, preview/contact sheet, geometry report, accessibility data and supported variants contain verified hashes. Failure example: duplicate index or missing file. Evidence: portable package validation. Test layer: integration. Trace: `FR-060`, `FR-145`.

### AC-21 — Independent evaluation

**Given** all mechanical checks pass, **when** an independent evaluator required by profile is unavailable or identical to the producer, **then** no PASS/acceptance is emitted. Evidence: evaluator-binding receipt. Test layer: architecture/integration. Trace: `FR-058`, `ST-05.02`.

### AC-22 — Acceptance boundaries

**Given** VAE production acceptance, static render acceptance and a passing sequence evaluation, **when** no attributable Carousel operator decision/delivery authorization exists, **then** export remains non-deliverable. Evidence: state-transition test. Test layer: application. Trace: `FR-059`, `FR-060`.

### AC-23 — Atomic commit

**Given** failure at each persistence step, **when** a Carousel mutation commits, **then** no partial visible state/artifact/receipt/command/event/dependency/outbox relation remains. Evidence: fault-injection matrix. Test layer: repository integration. Trace: `ST-05.02` selective recovery/evidence.

### AC-24 — Idempotency and concurrency

**Given** an idempotency key replay, **when** bytes match, **then** the original result returns; different bytes conflict. Two commands at one expected revision produce one commit and one revision conflict. Evidence: concurrency receipt. Test layer: repository. Trace: `ST-05.02`.

### AC-25 — Cancellation and late result

**Given** a slide worker returns after cancellation/supersession, **when** result ingestion occurs, **then** it is quarantined as noncanonical evidence and cannot resurrect/export the sequence. Evidence: race test. Test layer: workflow integration. Trace: `ST-05.02`.

### AC-26 — Selective invalidation

**Given** one source span, VAE asset or slide static program changes, **when** invalidation runs, **then** only dependent slide/sequence/export descendants become ineligible; unrelated child artifacts and historical receipts remain. Evidence: branching dependency test. Test layer: integration. Trace: `FR-058`, `ST-05.02`.

### AC-27 — Deterministic portable replay

**Given** identical pinned inputs across fresh processes, traversal orders, clocks, locales, roots and environment values, **when** compilation/replay runs, **then** plan/package canonical bytes and hashes match and contain no machine path. Evidence: reproduction matrix. Test layer: portability. Trace: `FR-060`, `ST-05.02`.

### AC-28 — Claim ceiling

**Given** all writing or future technical tests pass while candidate authority is unratified, **when** status is emitted, **then** quality is at most `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, build/production/certification/delivery remain false, and no Development Capsule exists. Evidence: status-policy test. Test layer: governance. Trace: packet authority rule.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

- Admission: category/profile, exact refs, lifecycle, source kind, interview provenance, semantic closure, capability and lock gates.
- Role/swipe: deterministic mapping, alternatives, index continuity, terminal transition, deletion necessity, no frame-time fields.
- Source map: exact quote normalization, omissions, condensations, bridges, source restrictions, non-claim handling, total evidence coverage.
- Continuity: invariant groups, variation rules, repeated assets/grammar, terminology, identity, role/tension and lock monotonicity.
- Export: stable ordering, file set, digest/byte/dimension/profile checks, unsupported optional variants and actual-byte requirements.
- Domain: canonicalization, enum rejection, no mutable defaults/open fields, lifecycle transition and strict N/A evidence.

### 10.2 Contract and architecture tests

- TS-AHP-003 `ContentDerivativeJob` adapter preserves every required field and owner.
- TS-STA child request/response/receipt adapter preserves Composition Intent, BBOX function/WHY, Feature Contracts, T/V, locks, source/text and actual artifacts.
- Interview Expression source/provenance and transformation adapter does not invent authority.
- VAE result adapter preserves Demand authority and production/consumption distinction.
- Delegation envelope carries immutable bytes without interpreting fields.
- AST/import tests prove Pipeline domain does not import AIR, Builder, VAE, Studio or Delegation source trees; application imports ports, not concrete adapters.
- Producer and independent evaluator identities cannot collide where prohibited.

### 10.3 Integration and reference-slice tests

The imported-interview reference slice shall run from an exact approved source package through AIR semantic program and `ContentDerivativeJob`, Carousel role/swipe and source maps, per-slide static child programs, real image bytes, sequence evaluation, operator correction/HumanResolution, export package, selective invalidation and replay.

Fixtures include:

- a valid five-slide teaching route whose exact count is fixture/profile-owned, not a universal default;
- verbatim quote, disclosed omission, approved condensation and non-claim label;
- source-attractive but unsupported headline;
- role/tension and archetype mismatch;
- repeated visual motif with valid sequence reason and without one;
- identity/terminology drift;
- stale VAE asset and weakened derivative lock;
- text overflow and missing glyph from TS-STA;
- missing required slide bytes, digest mismatch and unsupported platform variant;
- evaluator unavailable/producer collision;
- post-completion source revocation and one-slide repair.

### 10.4 Atomicity, replay, cancellation, and historical evidence

Run repository contract tests against durable and in-memory adapters. Inject failure before/after each blob, aggregate, command, event, receipt, dependency, idempotency and outbox write. Exercise concurrent role selection, export selection, operator decision and invalidation. Race cancellation with child dispatch and completion. Prove exact historical replay without current provider/registry lookup and distinct current-state rerun semantics.

### 10.5 Determinism, portability, security, and performance

Run twice in fresh processes while varying dictionary insertion, child completion, filesystem traversal, clock/timezone, locale, random state, machine root, environment ordering, host and process ID. Assert identical canonical plans, source maps, continuity plans, child-request ordering, manifest and package digest. Scan artifacts for drive letters, UNC/device paths, user/temp roots, hostnames and unsafe archive members.

Security tests enforce tenant/program/source-purpose partitioning, path/archive traversal rejection, MIME/dimension/decompression limits, bounded slide/count/bytes/graph expansion from pinned profiles, inert treatment of retrieved text, least-privilege worker credentials, restricted-source redaction and tool grants. Performance evidence reports per-stage latency, memory, artifact bytes, worker costs and bounded parallel slide execution without changing semantic order.

### 10.6 Evaluation evidence

Required later evidence includes source/quote transformation precision, orphan-claim rate, role/swipe contract conformance, continuity and variation coverage, lock realization, geometry/text/readability results, independent semantic/visual sequence evaluation, actual artifact integrity, portable export validation and operator decision. Thresholds and benchmarks must be current, category/profile-specific and attributable. This spec invents none.

### 10.7 Required future Build Receipt

A future Build Receipt, issued only after ratification/adoption and a bounded Development Capsule, must contain:

1. exact implementation and test file manifest/hashes;
2. requirements/Story/AC traceability;
3. current category/profile/evaluator authority and capability receipts;
4. upstream TS-AHP-003 and TS-STA-001 adopted interface hashes;
5. source/VAE/Delegation integration conformance;
6. full regression and clean-environment results;
7. deterministic fresh-process and portability matrix;
8. real artifact and export fixture manifests;
9. fault-injection, concurrency, cancellation, invalidation and replay evidence;
10. architecture/security audit and no product-sovereignty violation;
11. current claim ceiling, production eligibility false unless separately authorized, and certification state;
12. attributable independent audit/revision/re-audit/acceptance records.

This section defines evidence; it does not issue a Build Receipt.

### 10.8 Draft-dependency revision impacts

`TS-STA-001` and `TS-AHP-003` were consumed as `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Any changed hash or accepted interface affecting their ownership, static child contract, derivative job, lifecycle, failure, compatibility, invalidation, evaluation or claim ceiling requires review and revision where applicable in sections 3, 5, 6, 8, 9 and 10. Until a downstream-impact receipt closes that review, this draft is stale for later acceptance; historical bytes remain reproducible.

### 10.9 Writing completion declaration

Packet `CA-P03-WRITE-TS-CAR-001-RECOVERY` has completed WRITE only. The exact state is `WRITTEN_PENDING_AUDIT`; candidate authority remains `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; production eligibility and certification remain false; and the pre-ratification ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. No self-audit, revision, re-audit, acceptance, implementation, Development Capsule, contract release, production authorization or publication decision has occurred.
