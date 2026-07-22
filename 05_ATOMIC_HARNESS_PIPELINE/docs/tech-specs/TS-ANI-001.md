# TS-ANI-001 — Source-Grounded Non-Format-02 2D Animation Derivative Runtime

```yaml
spec_id: TS-ANI-001
title: Source-Grounded Non-Format-02 2D Animation Derivative Runtime
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Atomic Harness Pipeline
writing_wave: 12
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs: [FR-147, FR-148]
controlling_stories: [ST-05.04]
upstream_drafts:
  - {spec_id: TS-AHP-003, path: 05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md, quality_state: WRITTEN_PENDING_AUDIT, sha256: 072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {spec_id: TS-AIR-015, path: 04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md, quality_state: WRITTEN_PENDING_AUDIT, sha256: 58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {spec_id: TS-AIR-017, path: 04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md, quality_state: WRITTEN_PENDING_AUDIT, sha256: 0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
```

This candidate specification is authorized for technical writing and later independent review only. It creates no implementation, build, provider activation, schema or release bytes, production, publication, certification, Format 02 activation, or Development Capsule authority. Atomic Harness Pipeline owns execution compilation, runtime binding, render orchestration state, derivative evidence, and technical execution receipts. AIR owns Animation Scene Package meaning, approved Final Script, Composition Intent, Visual Narrative Program, Feature Contracts, Primitive/archetype/role-tension/Matrix/Edge and transfer semantics. Pipeline consumes those objects exactly; it does not reconstruct, amend, rank, or replace their meaning.

## 1. Files and authorities read

### 1.1 Writer, packet, dispatch, and claim ceiling

All digests are SHA-256 over the exact bytes read.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current one-spec writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact `CA-P03-WRITE-TS-ANI-001-RECOVERY` packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_12_DISPATCH_LOCK.yaml` | 2,678 | `96f655bbf67a40a38a5cf233cfa9ad3f954466a8dae80ff68dfa87a2a5c9e5a7` | Wave 12 path and exact three-draft lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate authority and acceptance ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-work-only authorization |

No `AGENTS.md` governs the target. The recovery packet classifies `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-ANI-001.md` as `DIRECT_PRODUCT_SPEC_PATH` and allows only this specification plus its five writer receipts.

### 1.2 Constitutional and candidate ownership inputs

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current source, meaning, visual-narrative, lineage, wrong-reading, and product-sovereignty authority |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product authority boundaries |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate unique semantic-object owner ledger |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_PROFILE_ALIAS_REGISTRY.yaml` | 2,279 | `21ad1a618361a14ec62576ce4e1d7ce3c7267e3bd77a1004aa8b996d51c87d57` | Canonical Format 02 identifier, historical aliases, contract-compatible/noncertified state, and no certification inheritance |

Candidate V2.1 ownership is `CANDIDATE_NOT_CURRENT`, admitted solely for specification work. Current Constitution V1.1 remains binding until attributable ratification/adoption.

### 1.3 Canonical requirement and Story inputs

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Canonical spec ID, title, owner, gate, and path |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | `FR-147` and `FR-148` identity/ownership |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact requirement, Story, source, evidence, and claim trace |
| AHP bundle `prd/features/F25-source-grounded-carousel-supervisual-and-2d-animation-derivatives.md` | 17,410 | `dbab88c994da95fbead65abfba4984d0efa3cd8a2fb27598997bd9886c37d293` | Animation and language/voice provenance requirements |
| AHP bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553 | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | `ST-05.04`, CBAR, denial, replay, recovery, and evidence |
| AHP bundle `planning/spec_assignments/TS-ANI-001.md` | 2,843 | `745c325fd3142de2915c394ea9268af01b861eb3d939458e4ec9c8c65b9b1de7` | Assignment brief only; target corrected by Program Control |
| AHP bundle `governance/CURRENT_WRITING_PROFILE.md` | 11,536 | `ba88c5572ae3f7571daac9991a0d325a20f491cb9c0ea7c3816deb3ff3d32956` | Source-first, CBAR, owner, N/A, and claim-ceiling laws |

`FR-147` requires one source-grounded 2D animation derivative through a separately authorized Harness/runtime without Format 02. `FR-148` requires exact language and voice transformation labels, attribution, approval, and lineage. `ST-05.04` denies unauthorized cloned voice, requires every spoken segment and visual idea to trace to source or an approved derivative, and requires exact state, decision, handoff, replay, and selective recovery evidence.

### 1.4 Non-accepted upstream drafts

| Draft | Bytes | SHA-256 | Exact interface consumed |
|---|---:|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md` | 64,377 | `072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed` | Exact `ContentDerivativeJob`, Harness/binding, source-use, route, evaluation, lock, lifecycle, and batch dependency closure |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md` | 93,219 | `58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8` | AIR-owned approved Final Script, `AnimationScenePackage`, scene meaning, semantic production package, and transfer constraints |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md` | 67,346 | `0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81` | AIR-owned Visual Narrative Program, Composition Intent, Feature Contracts, visual requirement intents, locks, and handoff boundary |

All three are `WRITTEN_PENDING_AUDIT` and `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their hashes are frozen by Wave 12. A changed draft reopens governing decisions; architecture/workflows; models/contracts/schemas/APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence. Draft interface detail is not ratified law.

### 1.5 Required and deferred sources

| Source | Bytes | SHA-256 | Disposition and use |
|---|---:|---|---|
| AIR bundle `sources/brownfield/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` (`SRC-AM-001`) | 13,678 | `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | `REQUIRED_AUTHORITY`; Format 02 deferred, Studio supervisory, typed correction, HumanResolution, no hidden mutation |
| AIR bundle `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; human expression/source-first derivative lineage |
| AIR bundle `sources/doctrine/AHP_F25_STATIC_ANIMATION_DERIVATIVES.md` | 17,410 | `dbab88c994da95fbead65abfba4984d0efa3cd8a2fb27598997bd9886c37d293` | Candidate feature copy matching the current F25 bytes |

`SRC-EXT-019` (`github://heygen-com/hyperframes`) and `SRC-EXT-025` (`github://MangoLion/stretchystudio`) are `DEFERRED_REFERENCE`: exact bytes are unavailable, no unique active requirement depends solely on either, and no factual implementation claim here is attributed to them. `SOURCE_GAP_NOTICE.yaml` preserves both non-blocking gaps. Names from the historical assignment do not authorize an adapter, runtime, license, provider, rig, or production route.

### 1.6 Brownfield implementation and test evidence

| File | Bytes | SHA-256 | Disposition |
|---|---:|---|---|
| Studio 2D bundle `01_MASTER_SPEC.md` | 13,021 | `43d55ac6955a40beea9b645a4cd0b0168c1dd5b048af5ea5e09c5346dc405858` | `ADAPT_AS_REFERENCE`; useful character/rig/performance continuity concepts, historical product doctrine only |
| Studio 2D bundle `02_PIPELINE_AND_PROVIDER_ROLES.md` | 4,280 | `a853f5ef9e6894e2e4a531af7e38a57e5c3a6d2746ce5111ebc2b035621e08c3` | `ADAPT_AS_REFERENCE`; narrow-provider boundary vocabulary; provider selections not current |
| Studio 2D bundle `models/two_d_character_models.py` | 12,050 | `f089ec618c0d9b2e2582cb3a2ec571e066d78a238048344078eaed7cf1eb73b4` | `REPLACE_AS_CANONICAL`; useful typed rig/track/timebase vocabulary, but open `Any`, floats, defaults, embedded thresholds/approval, and mixed ownership are invalid current design |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/assembly.py` | 9,304 | `b1bca77b10cc7aac39208746d0f3072936150be5e3f08b081f07a0c97213a3cd` | `ADAPT`; layer, animation, timeline, caption, audio, plan and receipt shapes |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/assembly_planner.py` | 22,947 | `326f315a18ff5d307855ad32b9410862d5b8879aa489751abfc6317d15ee0159` | `REPLACE`; current defaults, float timing, random IDs, partial writes, local authority and synthetic captions cannot be canonical |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/assembly.py` | 2,409 | `5417dc264def882c7f124e15fdc776fa01f5cac4439e4a9abeb254adba835dfc` | `REPLACE`; independent mutable maps do not prove atomic artifact/receipt/command/event/dependency state |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_layer_manifests_animation_plans_edl_captions_and_sonic_plans.py` | 7,525 | `7145a73fbfc48b9c697a1da98a3868f935e479dfb3835eefced8c041461fd689` | `ADAPT`; manifest, source-timing, brand-layer and blocked-receipt scenarios require current authority/determinism corrections |

The target Pipeline root currently contains specifications only. This prompt creates no implementation.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure

An AIR `AnimationScenePackage` is a semantic scene contract, not an executable rig, layer, timeline, audio, caption, runtime, or render program. A `ContentDerivativeJob` authorizes a bounded Pipeline target, not a provider or arbitrary demo. Without a governed execution compiler, a renderer may silently choose scene timing, infer gestures, invent quotes, use a cloned voice, bind an unapproved rig, flatten Composition Intent into coordinates, ignore Feature Contracts, drop source/identity locks, call the result Format 02, or mark a provider callback as accepted output.

Typical unsafe shortcuts include:

- importing a Stretchy or other demo project because it looks suitable even though no current Harness authorizes it;
- treating AIR's semantic scene, BBOX intent, or Feature Contract as exact renderer geometry while losing its reason and allowed variation;
- turning a generated performance into “the participant's reaction” without direct source derivation and disclosure;
- presenting an edited quote, condensation, operator bridge, rerecorded narration, generated voiceover, or synthetic voice as verbatim source audio;
- selecting a voice model or visual provider inside AIR meaning or this general runtime spec;
- using historical PaperCut/Format 02 doctrine to activate `format02_minimal_coach_theatre`;
- generating default captions or audio when exact source/transform evidence is absent;
- storing layer, track, render, and receipt records independently so partial success looks complete;
- using float time and wall-clock/random identity so replay differs by machine;
- accepting a render because technical output exists without independent semantic/identity/source evaluation; or
- rerunning all scenes after a localized source, rig, cue, or evaluation failure.

Each can create a polished but false derivative and make the failure hard to detect or reconstruct.

### 2.2 User and system outcome

A Conscious Content Operator can admit one authorized non-Format-02 animation job and obtain a portable, deterministic execution program whose every spoken segment, caption, visual idea, character/identity reference, rig/layer asset, cue, scene, and render maps to exact upstream authority. Unauthorized voice or rig use is denied before spend. The system records exact runtime, render, evaluation, operator decision, and selective recovery evidence without claiming production readiness or Format 02.

### 2.3 Bounded solution

Pipeline SHALL provide an `AnimationDerivativeExecutionCase` that:

1. admits an exact eligible `ContentDerivativeJob`, Harness/binding, AIR semantic package, AIR scene package, visual handoff, source-use grant, and operator source authority;
2. proves the target is the 2D Character Animation category but not Format 02 or any alias;
3. compiles AIR-owned scene meaning and Composition Intent into a Pipeline-owned immutable `AnimationSceneExecutionProgram` without changing semantic fields;
4. resolves only Harness-authorized rig, layer, runtime, renderer, evaluator, and worker bindings;
5. compiles exact language/voice provenance and disclosures for every spoken/text element;
6. requests missing visual ingredients through separately governed demands rather than generating them implicitly;
7. executes and renders only after all authority, source, identity, capability, contract, and evaluation-precondition gates pass;
8. evaluates technical, source, identity, semantic, composition, Feature Contract, lock, and disclosure conformance independently;
9. records operator acceptance/rejection separately from evaluator and provider results; and
10. supports atomic commit, idempotency, optimistic concurrency, cancellation, selective invalidation, exact replay, and historical reproduction.

### 2.4 In scope

- Non-Format-02 2D animation job admission and explicit Format 02 exclusion.
- Exact consumption of AIR Final Script, Animation Scene Package, Visual Narrative Program, Composition Intent, Feature Contracts, transfer constraints, semantic package, and wrong-reading locks.
- Pipeline execution IR: scenes, rational timebase, layers, rigs, tracks, cues, audio, captions, composition, render, evaluation, disclosure, dependencies, and receipts.
- Harness-authorized runtime/worker/provider binding without provider ownership of meaning.
- Source audio, verbatim quote, disclosed omission, faithful condensation, operator-authored bridge, generated voiceover, synthetic voice, and rerecorded human voice provenance.
- Identity, Visual DNA, source/voice authority, rig/layer lineage, continuity, and generated-performance disclosure.
- Missing visual ingredient demand boundary, exact returned-asset pinning, and no hidden VAE mutation.
- Deterministic serialization/hashing, portability, replay, cancellation, recovery, supersession, revocation, and selective invalidation.
- Candidate/evaluator/operator separation and truthful terminal state.

### 2.5 Out of scope and non-goals

- AIR semantic compilation, scene meaning, Final Script, Primitive/archetype/Matrix/Edge/role-tension, Composition Intent, Feature Contract, or transfer ownership.
- Builder AtomicHarnessDefinition or Harness execution-binding compilation.
- Interview Expression source preparation, quote approval, Reaction Receipt, Expression Moment, Asset Package Spec, or source authority ownership.
- VAE Visual Production Plan, provider/model/LoRA/conditioning selection, candidate visual generation, repair, or production acceptance.
- Character Genesis, rig authoring, voice cloning, model training, provider certification, license approval, or a universal animation authoring Studio.
- Activating Format 02, `format02_minimal_coach_theatre`, historical aliases, PaperCut doctrine, Future Character Performance Studio, or certification inheritance.
- Inventing evaluation thresholds, selecting external GitHub implementations, claiming HyperFrames/Stretchy behavior, or treating parse success as compatibility.
- Publishing code, schema/release bytes, render artifacts, a Development Capsule, build/production/certification, or VAE Stage 5.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty

| Owner | Owned meaning/state | Pipeline may do | Pipeline must not do |
|---|---|---|---|
| Interview Expression | Source, source authority, exact quote/audio/keyframe evidence, Expression Moments, Asset Package Spec, approvals/restrictions | Verify/pin and enforce source-use closure | Rewrite source, guess classification, relax use, or create missing evidence |
| AIR | Final Script, Animation Scene Package, Visual Narrative Program, Composition Intent, Feature Contracts, Primitive/archetype/role-tension/Matrix/Edge/transfer and semantic production meaning | Compile an executable projection preserving every ref/constraint | Reinterpret scenes, change roles/tension, choose new meaning, weaken locks |
| Builder | AtomicHarnessDefinition, category/profile requirements, allowed runtime/capability/evaluator bindings, inheritance law | Consume exact eligible Harness/binding | Invent or mutate Harness/profile/certification |
| Pipeline | Animation execution case/program, exact execution geometry/time, rig/layer/runtime bindings, render orchestration, technical result/evidence | Execute within admitted contracts | Become source, semantic, visual-production, transport, or human authority |
| VAE | Missing visual asset production plan/route/realization/repair/acceptance | Receive separately authorized immutable demands; consume accepted exact results | Preselect provider/model/LoRA/workflow or treat Pipeline acceptance as VAE acceptance |
| Delegation | Contract validation, compatibility, immutable routing, replay protection, transport receipts | Transport released cross-product messages | Change bytes or create meaning |
| Studio / operator | Projection, typed correction requests, scoped human decisions | Approve/reject where explicitly authorized; produce HumanResolutionEpisode | Mutate canonical program through UI state or create hidden global doctrine |

`Activative Contract Compiler != Activative Intelligence Runtime`. Pipeline is neither.

### 3.2 AIR semantic immutability and executable projection

The AIR scene package remains the authoritative source of scene semantic function, viewer-role movement, tension state, What Is/What Could Be phase, character/symbol roles, source/script bindings, semantic Composition Intent, timing intent, BBOX intent/WHY, negative-space purpose, gaze/attention intent, Feature Contracts, visual requirements, identity/continuity constraints, reuse constraints, and inherited locks.

Pipeline compiles exact execution values only within AIR allowed variation and Harness/runtime capabilities. Every derived value records its AIR source ref and derivation rule. If exact execution cannot satisfy an AIR requirement, the result is `UNSUPPORTED_SEMANTIC_REQUIREMENT`, `VISUAL_ASSET_REQUIRED`, or `OWNER_DECISION_REQUIRED`; Pipeline does not silently approximate meaning.

### 3.3 Composition-before-editing and Feature Contracts

AIR Composition Intent and Feature Contracts SHALL be admitted before Timeline/Composition IR. Pipeline then compiles exact canvas geometry, normalized integer BBOXes, layer ordering, time cues, camera/character placement, negative-space zones, text/caption safe areas, and motion tracks. The executable IR retains each intent/feature ref, `why`, allowed variation, deterministic check, judgment dimension, and wrong-reading lock.

Feature realization evidence does not mutate the authoritative contract. An unsupported feature blocks or creates a typed VAE/owner decision. A technically renderable scene with failed gaze, hands, expression, identity, source evidence, composition hierarchy, or lock conformance is not accepted.

### 3.4 Source and language/voice truth

Text transformation and voice realization are orthogonal and both mandatory for spoken or displayed language:

```text
LanguageTransformationClass = VERBATIM_SOURCE | DISCLOSED_OMISSION |
  FAITHFUL_CONDENSATION | OPERATOR_AUTHORED_BRIDGE | GOVERNED_REWRITE

VoiceRealizationClass = SOURCE_AUDIO | RERECORDED_HUMAN_VOICE |
  GENERATED_VOICEOVER | SYNTHETIC_VOICE | NO_VOICE
```

`VERBATIM_SOURCE` requires exact source spans/bytes, speaker, rational source time, transcript revision, and source audio when `SOURCE_AUDIO`. An omission requires exact retained/omitted spans and an export disclosure. A condensation/rewrite requires transformation operations, semantic support, AIR Final Script segment, Voice DNA application, and disclosure. An operator bridge requires attributable approval and cannot claim to be source speech. Synthetic voice requires an exact operator source authorization/identity-use grant permitting the speaker, text class, purpose, audience/platform, provider/model class as governed, and disclosure. Absence or ambiguity fails before runtime binding.

Generated acting, expression, gesture, gaze, or reaction SHALL be labeled `GENERATED_PERFORMANCE` unless it is a direct, source-timed representation whose provenance permits the narrower claim. A renderer cannot claim generated performance is the participant's actual reaction.

### 3.5 Harness and runtime authority

No demo, project file, historical engine bundle, provider installation, runtime binary, or Studio registry grants production entry. The exact Harness/binding must declare the non-Format-02 profile, required rig/layer/runtime/renderer/audio/caption/evaluator capabilities, compatibility versions, review owners, repair units, execution constraints, and worker trust. Pipeline can select only among eligible declared bindings under a pinned policy; a missing binding blocks.

External provider names in historical/reference material are not active selections. Any future adapter requires exact bytes/version/license/security review, a governed capability binding, fixtures, compatibility tests, worker evidence, and separate build authorization.

### 3.6 Format 02 exclusion

The canonical Format 02 ID is `format02_minimal_coach_theatre`; historical aliases include `minimal_coach_theatre` and the human-readable label. All are rejected for new TS-ANI-001 jobs. Format 02 is `DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS`, contract-compatible only, not benchmarked/certified/production-authorized, and cannot lend certification to this profile.

Every execution case SHALL emit `Format02ExclusionReceipt` proving:

- requested profile and resolved canonical ID are not Format 02/alias;
- no active format ID, Harness ID, runtime route, Studio surface, receipt, export label, or certification claim implies Format 02;
- any historical reference is marked historical/non-authoritative; and
- activation would require a distinct later current Builder Harness, independent validation, regenerated runtime/Studio specs, and authorization.

### 3.7 Wrong-reading locks, identity, and continuity

All source, AIR, Final Script, scene, Composition Intent, Feature Contract, Visual DNA, identity, and Harness locks are inherited. Pipeline may add stricter execution locks; it may not remove or weaken any. Derivative parent-lock evidence is portable and exact. Relaxation requires a new authorized upstream version.

Identity refs must pin source identity, Brand Context Version, Visual DNA, approved art/rig/layer/asset versions, allowed stylization, representation restrictions, and continuity criteria. A technically valid rig outside the locked identity context is incompatible.

### 3.8 Determinism, portability, and evidence-bearing applicability

Canonical identity cannot depend on clock, randomness, environment, host, absolute path, locale, dictionary insertion, filesystem traversal, database order, provider callback order, or mutable latest. Time uses integer ticks in a rational timebase. Normalized geometry uses integer millionths. Sets sort by full immutable-ref tuple; scene/track/cue order is explicit.

Procedural variation uses an explicit seed only when the Harness/profile allows it; the seed is semantic input. A nondeterministic provider result is frozen as exact candidate bytes/hash and never represented as reproducibly regenerated.

`NOT_APPLICABLE` requires a pinned profile rule, evidence, owner, reason, and reopen condition. Missing capability, source, voice authorization, rig, evaluator, or evidence cannot become N/A.

### 3.9 Acceptance, consumption, and claim ceiling

Harness/job admission is not execution authorization. Provider completion is not validation. Independent evaluation pass is not operator acceptance. VAE production acceptance of a visual ingredient is not Pipeline consumption acknowledgement. Pipeline derivative acceptance is not publication/production authorization or format certification.

This spec remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, and build false. Before ratification, no later state exceeds `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` and no Development Capsule may issue.

## 4. Current brownfield architecture

### 4.1 Pipeline target state

`05_ATOMIC_HARNESS_PIPELINE` has documentation only. There is no authorized animation source tree, repository, worker adapter, schema, migration, fixture, or test suite. Future exact paths in section 7 are proposals only.

### 4.2 Historical 2D Character Engine bundle

The bundle separates Character Genesis from Performance Compilation and contains useful concepts: immutable identity/art/rig/performance-library versions, rational-ish canonical timebase, layer/rig/constraint/attachment graphs, acting states, performance tracks/cues, transcript/viseme alignment, choreography, composition, finishing, evaluation, approval, and render receipt.

It is not current authority. Its `TwoDCharacterProgram` mixes semantic, Pipeline, provider, evaluator, and operator state; uses open `Any` dictionaries, binary floats, default values, ungoverned strings, embedded thresholds, nullable lifecycle fields, wall-clock approvals, provider names, and one monolithic status. It also carries PaperCut/Format 02-adjacent historical doctrine. Current design splits ownership, requires exact immutable refs, moves semantics to AIR, execution to Pipeline, production assets to VAE, and decisions/evidence to separate receipts.

### 4.3 Studio assembly predecessor

Studio's assembly contracts/service emit Layer Manifest, Animation Plan, EDL, Timeline, Caption, Audio Mix, Assembly Plan, and receipt. Tests preserve useful intentions: captions remain within source time, source voice cannot be synthetic/SFX/music, rig layers belong to locked Brand Context, manifest hashes reach receipts, and missing plan blocks render.

The implementation writes multiple independent in-memory dictionaries sequentially, generates UUIDs/time during compilation, uses float seconds, accepts open dictionaries at API/service boundaries, supplies default captions/audio/motion, compiles local semantic choices, and may persist intermediate objects before failure. It is `ADAPT` as vocabulary/test evidence and `REPLACE` as canonical implementation.

### 4.4 Studio Architecture Amendment

The required amendment establishes Format 02 deferral, a supervisory Studio, typed exact correction operations, automatic attributable HumanResolutionEpisode capture, category-native modules in one shell, and external bounded workers. Pipeline SHALL preserve those decisions. Studio projection cannot mutate job/program truth, and operator correction creates a typed change program plus selective rerun rather than direct hidden editing.

### 4.5 External reference gaps

Exact HyperFrames and StretchyStudio bytes are absent and deferred. This spec therefore defines no factual API, file format, runtime behavior, license, deterministic property, adapter, or provider claim for either. Historical names remain research backlog only. The same rule applies to any unpinned provider or renderer.

## 5. Proposed architecture and workflows

### 5.1 Components

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `AnimationJobAdmissionService` | Resolve exact job/Harness/binding/AIR/source/authority/profile refs and enforce current state | Fill a missing ref or accept latest/stale/ambiguous values |
| `Format02ExclusionGate` | Resolve canonical profile/aliases and emit exclusion evidence | Activate or certify any format |
| `LanguageVoiceProvenanceValidator` | Validate every text/audio segment, transformation, speaker, authority, approval, disclosure | Infer permission or relabel transformed text/audio |
| `AnimationSceneExecutionCompiler` | Project AIR semantic scenes into exact Pipeline execution scenes under allowed variation | Change semantic role, Composition Intent, Feature Contract, source meaning, or locks |
| `RigLayerBindingResolver` | Select exact approved rig/layer/performance/asset bindings admitted by Harness and identity scope | Author a rig or treat a demo as approved |
| `VisualRequirementDemandGateway` | Emit separately governed demands for unresolved visual requirements and bind returned accepted assets | Select VAE provider/model/workflow or mutate AIR intent |
| `TimelineAudioCaptionCompiler` | Compile canonical tick timebase, tracks, cues, captions, audio mix, disclosures | Generate default language/audio or alter source timing |
| `RuntimeBindingResolver` | Select only compatible Harness-declared runtime/renderer/worker bindings | Treat provider availability as semantic or production authority |
| `AnimationRenderOrchestrator` | Stage immutable program, issue idempotent render jobs, ingest exact artifacts/receipts | Mark provider callback accepted or rewrite program |
| `AnimationEvaluationCoordinator` | Run deterministic checks and independent profile-bound evaluation | Let producer self-evaluate or invent thresholds |
| `AnimationDecisionService` | Apply attributable operator decision to exact candidate/evidence and emit HumanResolution link | Infer acceptance from UI/evaluator/render status |
| `AnimationExecutionRepository` | Atomic compare-and-swap artifact/event/receipt/edge/idempotency/outbox and history | Partial/in-place writes or deletion |
| `AnimationInvalidationProjector` | Traverse typed dependencies and rerun only affected descendants | Blanket rerun or history erasure |

### 5.2 Workflow A — admit and freeze the execution case

1. `OpenAnimationDerivativeExecutionCase` supplies command/idempotency IDs, expected version, actor/delegation, exact `ContentDerivativeJob`, Harness/binding, AIR Semantic Production Package, approved Final Script, Animation Scene Package, visual handoff, source-use grant, category/profile, operator source authority, evaluation/review policy, and intended output constraints.
2. Admission verifies schema/version/hash/owner/lifecycle/compatibility for every ref; current job is `ADMITTED_NOT_EXECUTION_AUTHORIZED`; Harness category is 2D Character Animation; source and AIR packages match the same source/semantic lineage.
3. Format gate canonicalizes profile IDs through the governed registry and rejects Format 02, all aliases, unknown, or ambiguous values.
4. Source/voice validator proves each Final Script segment and intended realization has exact language/voice provenance and allowed use.
5. All inherited locks/restrictions are unioned without weakening. Identity/Visual DNA/Brand Context and scene/source refs are cross-checked.
6. Canonical `AnimationExecutionInputManifest` freezes exact refs, limitations, maximum claim, registry/policy snapshots, and digest. One atomic commit stores case, manifest, command, event, edges, receipt, idempotency record, and outbox.

### 5.3 Workflow B — compile scene execution program

For each ordered AIR scene:

1. Copy exact semantic source refs and immutable intent refs; never copy them into locally editable fields.
2. Resolve the scene's category-native Harness node/template/capability declarations. A missing node/template blocks the scene.
3. Compile rational time windows from AIR duration/frame intent and Final Script/audio timing. If multiple legal timings exist and Harness policy cannot select deterministically, emit `HUMAN_SELECTION_REQUIRED` rather than change meaning.
4. Compile exact composition geometry from AIR Composition Intent/BBOX intent under allowed variation. Each coordinate/track/layer retains derivation and intent `why`.
5. Resolve source and approved VAE/library assets by exact version/hash, identity context, use grant, and lifecycle. Unresolved visual requirement becomes an immutable demand request through the owning boundary.
6. Resolve exact rig, layer, performance-library, costume/prop, font, audio, caption, runtime, renderer, worker, and evaluator bindings from Harness-compatible registries.
7. Compile language/voice disclosure overlays and export metadata; disclosures cannot be suppressed by a template.
8. Compile deterministic checks and independent evaluation plan from Feature Contracts, locks, source truth, identity, composition, and runtime requirements.
9. Canonically serialize the scene program and its dependency closure. Any unsupported field blocks; no silent dropping.

All scenes and shared bindings assemble into immutable `AnimationSceneExecutionProgramCandidate`. Compilation has no provider side effect.

### 5.4 Workflow C — resolve visual assets without authority leakage

An AIR `VisualRequirementIntent` is nonauthoritative for production. Pipeline compiles a separate immutable demand only under the appropriate downstream spec/contract and retains the AIR intent ref, semantic/asset role, Composition Intent, Feature Contracts, identity/continuity, source/reference needs, allowed variation, restrictions, locks, evaluation profile, and priority. It does not add a provider/model/LoRA/workflow choice.

VAE may accept/reject the demand and own plan/realization/repair/production acceptance. Pipeline binds only a returned exact accepted result that matches demand version/hash and remains current. VAE production acceptance does not imply Pipeline has consumed it. `AcknowledgeAnimationAssetConsumption` records exact use in a particular scene/program; rejection or staleness leaves the scene blocked.

### 5.5 Workflow D — validate and authorize render candidate

1. `ValidateAnimationSceneExecutionProgram` checks every dependency, source/voice record, time interval, composition mapping, layer/rig identity, Feature Contract check, lock, disclosure, category/profile, Format 02 exclusion, compatibility feature, and output constraint.
2. Deterministic failures produce typed blockers. Judgment dimensions require an independent evaluator binding; capability presence does not imply certification.
3. `PrepareAnimationRenderCandidate` creates a sealed portable bundle manifest with canonical program bytes, exact inputs/assets/runtime/worker configuration, output declaration, and no machine path.
4. `AuthorizeAnimationRender` is a separate scoped operational command requiring current job/Harness authority, candidate validation, worker trust, budget/quota, and review policy. It is not product implementation or production authorization.
5. A render authorization is single-program-version-specific. Any semantic or identity change requires a new upstream version and recompilation.

### 5.6 Workflow E — render, ingest, evaluate, and decide

1. Orchestrator issues an idempotent render attempt with exact candidate bundle hash, runtime/worker binding, attempt ID, cancellation token, and output contract.
2. Worker stages only manifest members, verifies every hash, rejects unsafe paths/archive members, runs in a bounded workspace, and emits technical logs/receipt plus artifact bytes/hashes. Provider/model output is candidate evidence only.
3. Ingestion verifies output count/type/codec/dimensions/duration/timebase/audio/caption/disclosure and exact attempt identity. Late/stale/mismatched callbacks are stored as noncanonical evidence.
4. Deterministic evaluation checks quote diffs, voice/source metadata, source timing, identity refs, composition geometry, Feature Contract facts, inherited locks, runtime/rig integrity, disclosure presence, and Format 02 exclusion.
5. Independent evaluation checks semantic/source fidelity, role/tension/transfer survival, identity/Visual DNA, generated-performance truth, composition intent, feature realization, continuity, animation quality, and wrong-reading risk using a pinned profile.
6. An attributable operator decision accepts, rejects, contests, or requests typed revision for the exact render/evaluation bytes. It creates a HumanResolutionEpisode ref. Producer/evaluator cannot approve.
7. Accepted derivative remains a Pipeline artifact with claim ceiling and usage restrictions. Publication and downstream consumption remain separate.

### 5.7 Workflow F — correction, recovery, and replay

Typed correction targets the smallest owner/layer:

- source/quote/voice authorization -> Interview Expression or operator source authority;
- Final Script/scene meaning/Composition Intent/Feature Contract -> AIR;
- Harness/category/profile capability -> Builder;
- execution geometry/timing/track/runtime binding -> Pipeline;
- visual asset feasibility/realization -> VAE;
- transport -> Delegation;
- operator interpretation/taste -> Studio HumanResolution.

Pipeline correction creates a new immutable successor and reruns only dependent validation/render/evaluation nodes. It cannot patch upstream meaning. Replay resolves exact historical commands, source/AIR/Harness/program/assets/runtime/evaluator/worker outputs/operator decisions and invalidation view; it never calls current models or substitutes latest.

### 5.8 State machines and events

```text
Case: REQUESTED -> INPUTS_ADMITTED -> EXECUTION_PROGRAM_COMPILED
           |             |                       |
           +-> BLOCKED   +-> CANCELLED           +-> VISUAL_ASSETS_PENDING
EXECUTION_PROGRAM_COMPILED -> VALIDATED -> RENDER_AUTHORIZED -> RENDERING
          -> RENDER_CANDIDATE_INGESTED -> EVALUATED -> OPERATOR_REVIEW
          -> ACCEPTED | REJECTED | CONTESTED | REVISION_REQUESTED
Any immutable version may later be SUPERSEDED | INVALIDATED | REVOKED.
```

Events include `AnimationInputsAdmitted`, `Format02Excluded`, `AnimationProgramCompiled`, `AnimationProgramBlocked`, `AnimationAssetDemandRequested`, `AnimationAssetConsumed`, `AnimationProgramValidated`, `AnimationRenderAuthorized`, `AnimationRenderStarted`, `AnimationRenderCandidateIngested`, `AnimationRenderCandidateLate`, `AnimationEvaluated`, `AnimationOperatorDecisionRecorded`, `AnimationRevisionRequested`, `AnimationAccepted`, `AnimationRejected`, `AnimationSuperseded`, `AnimationInvalidated`, `AnimationRevoked`, and `AnimationCommandCancelled`.

### 5.9 Atomicity, idempotency, concurrency, and cancellation

Each mutating command atomically commits aggregate/version, canonical artifact, command record, event, decision/attempt/evaluation receipt, dependency edges, idempotency record, current alias, and durable outbox. Any failure rolls all back. Failure receipts use a separate explicit failure transaction and cannot look successful.

Same idempotency scope/key and canonical request returns the original result; changed bytes fail collision. Compare-and-swap expected version serializes admission, render authorization, operator decision, correction, supersession, and cancellation. Cancellation before render commit prevents dispatch; after commit it appends cancellation and attempts worker cancellation. A late result cannot resurrect a cancelled/superseded version.

## 6. Data models, contracts, schemas, APIs, commands, and events

### 6.1 Contract-wide scalar and reference rules

Every stored object is immutable, schema-identified, versioned, and canonically serialized. Contract fields have no implicit current-version lookup.

| Type | Required fields and invariants |
|---|---|
| `ImmutableRef` | `object_kind`, `object_id`, `version`, `sha256`, `schema_id`; all non-empty; digest is lowercase 64-hex |
| `ArtifactRef` | `ImmutableRef` plus `media_type`, `byte_length`, `content_address`; no absolute filesystem path |
| `RationalTime` | signed `numerator`, positive `denominator`; reduced before canonicalization |
| `RationalRate` | positive `numerator`, positive `denominator`; reduced before canonicalization |
| `TimeRange` | `start`, `duration`; start nonnegative, duration positive, common declared timebase |
| `NormalizedRect` | integer millionths `x`, `y`, `width`, `height`; each within `[0,1000000]`; rectangle remains inside canvas |
| `TypedExtension` | registered `namespace`, `type_id`, `schema_version`, `sha256`, `payload`; unknown required extensions reject, unknown optional extensions are preserved byte-for-byte |
| `ActorRef` | stable `actor_id`, `actor_kind`, `authority_scope`; no display name as identity |

Canonical JSON is UTF-8, Unicode NFC, object keys sorted lexicographically, arrays preserved in declared semantic order, integers in base-10 without leading zeros, no floats, no NaN/infinity, no insignificant whitespace, and no platform path separators. Digest input excludes transport headers, wall-clock observation time, host name, process ID, environment variables, and mutable aliases. Set-like arrays declare a sort key in their schema; ordered timelines retain input order and reject equal-order ambiguity.

### 6.2 Admission manifest

`AnimationExecutionInputManifestV1` is the exact compilation input:

```text
schema_id, manifest_id, version
content_derivative_job_ref
harness_definition_ref, harness_binding_ref
source_package_ref, source_kind
source_authority_grant_ref, identity_use_grant_refs[]
approved_final_script_ref, animation_scene_package_ref
visual_narrative_program_ref, composition_intent_refs[]
feature_contract_refs[], visual_semantic_pack_ref?
reaction_receipt_refs[], expression_moment_refs[]
wrong_reading_locks[], parent_derivative_refs[], parent_lock_evidence_refs[]
category_id, profile_id, requested_output_profile_ref
compatibility_profile_ref, evaluation_profile_ref
required_capabilities[], admitted_extensions[]
```

The manifest requires category `2d_character_animation`, excludes the canonical Format 02 identifier and every governed alias, and requires exact version/hash on every reference. `source_kind=interview_expression` requires at least one non-empty Reaction Receipt ref and Expression Moment ref, as already governed by the shared source/provenance boundary. Non-interview kinds validate any supplied interview provenance but do not fabricate it. Unknown source kinds, profiles, capability names, or required extension types fail closed.

`parent_derivative_refs` and `parent_lock_evidence_refs` are both required for a derivative of a prior derivative and both empty for a root derivative. The validator computes the complete ancestor lock union. The submitted lock set must be a semantic superset; same lock ID with weaker scope, qualifier, enforcement mode, or evidence obligation is rejection, not override.

### 6.3 Language and voice provenance

Pipeline stores a `SpokenSegmentProvenanceV1` per spoken or displayed language segment:

```text
segment_id, scene_id, time_range
language_transformation_class
rendered_text, rendered_text_sha256
source_span_refs[], source_text_sha256?
transformation_receipt_ref?
omission_ranges[], disclosure_text?, disclosure_placement?
authority_grant_ref, operator_approval_ref?
voice_realization_class
source_audio_ref?, source_speaker_ref?
voice_asset_ref?, voice_model_ref?, voice_authorization_ref?
identity_use_grant_ref?
lineage_parent_refs[]
```

`language_transformation_class` is exactly one of `VERBATIM_SOURCE`, `DISCLOSED_OMISSION`, `FAITHFUL_CONDENSATION`, `OPERATOR_AUTHORED_BRIDGE`, or `GOVERNED_REWRITE`. `voice_realization_class` is exactly one of `SOURCE_AUDIO`, `RERECORDED_HUMAN_VOICE`, `GENERATED_VOICEOVER`, `SYNTHETIC_VOICE`, or `NO_VOICE`.

Rules are structural and behavioral:

- `VERBATIM_SOURCE` requires exact normalized text equality to joined source spans and forbids omission ranges.
- `DISCLOSED_OMISSION` requires exact retained-token order, explicit omission ranges, and a rendered disclosure.
- `FAITHFUL_CONDENSATION` requires a transformation receipt and operator approval; it must not use a verbatim disclosure.
- `OPERATOR_AUTHORED_BRIDGE` requires operator authorship and must not cite a source span as if quoted.
- `GOVERNED_REWRITE` requires an upstream authorized rewrite receipt and is never represented as source speech.
- `SOURCE_AUDIO` requires exact audio/source-speaker refs and alignment evidence.
- `RERECORDED_HUMAN_VOICE` requires performer identity, authorization, and disclosure.
- `GENERATED_VOICEOVER` requires approved text, model/asset lineage where applicable, authority, and disclosure.
- `SYNTHETIC_VOICE` requires explicit synthetic-voice and identity-use authorization for the exact speaker/text/scope plus disclosure; a general source-use grant is insufficient.
- `NO_VOICE` forbids audio and voice-model refs.

The compiler never generates missing text, alignment, source span, authorization, or disclosure. A scene cannot be render-authorized while a segment's source/voice relation is unresolved.

### 6.4 Animation execution program

`AnimationSceneExecutionProgramV1` contains:

```text
schema_id, program_id, version, program_sha256
input_manifest_ref, compilation_policy_ref
scene_units[], composition_execution_ir_ref
layer_manifest_ref, rig_binding_refs[], performance_track_refs[]
audio_track_refs[], caption_track_ref?
visual_asset_demand_refs[], runtime_worker_binding_ref
format02_exclusion_receipt_ref
evaluation_plan_ref, disclosure_manifest_ref
wrong_reading_lock_refs[], feature_contract_refs[]
dependency_edges[], claim_ceiling
compiled_by_command_ref, predecessor_program_ref?
```

Each `AnimationSceneExecutionUnitV1` carries `scene_id`, AIR scene ref, semantic purpose ref, role/tension/transfer refs, exact duration policy, executable layer/track refs, Composition Intent refs, Feature Contract refs, visual demand refs, entry/exit continuity refs, source/voice segment refs, inherited locks, and evaluation obligations. Semantic fields remain references to AIR bytes. Pipeline fields describe execution only.

`CompositionExecutionIRV1` stores canvas, rational timebase, ordered shots/scenes, normalized geometry, z-order, transitions, track bindings, safe-area facts, and the exact AIR Composition Intent ref plus `intent_reason_ref` and `allowed_variation_ref`. A geometry value cannot replace or reinterpret those references. Any variation outside an allowed range is an upstream amendment request.

`LayerManifestV1` is an ordered collection of `LayerBindingV1` records: `layer_id`, `asset_role`, asset/version ref, scene refs, normalized bounds, z-index, opacity millionths, blend-mode enum, visibility ranges, transform-track ref, mask ref, color-treatment ref, continuity key, and lock refs. Missing required asset refs are represented by unresolved Visual Asset Demands; they are never filled from a mutable latest asset.

`RigRuntimeBindingV1` includes rig definition ref, character/identity ref, Visual DNA ref, skeleton/control-set version, layer-to-control bindings, supported cue types, forbidden controls, continuity constraints, runtime adapter ID/version/hash, capability profile ref, and validator receipt ref. An adapter may reject unsupported semantics but may not discard a cue, identity constraint, lock, or Feature Contract.

`PerformanceTrackV1` holds ordered typed cues with rational timing. Cue types are `POSE`, `GESTURE`, `EXPRESSION`, `GAZE`, `MOUTH_SHAPE`, `CAMERA_RELATION`, and `TRANSITION`. Each cue contains its AIR semantic cue ref, realization parameters within allowed variation, source-evidence ref when representing observed behavior, generated-performance label otherwise, and lock refs. A generated cue may not be labeled as an observed participant reaction.

`RuntimeWorkerBindingV1` pins worker protocol, runtime/adapter/container/model identifiers and versions, capability set, input/output schema hashes, deterministic-mode declaration, seed policy if an authorized stochastic component exists, execution limits, trust status, and compatibility receipt. Provider names are implementation registry values, not semantic authorities.

### 6.5 Render, evaluation, decision, and exclusion records

`RenderAttemptV1` pins program, worker binding, canonical request hash, attempt ordinal, idempotency key, authorized output slots, and dispatch receipt. `RenderCandidateBundleV1` contains exact artifacts, media metadata, timebase, scene/track coverage, audio/caption bindings, disclosure placements, worker output receipt, logs/metrics refs, and attempt ref. Artifact refs are content-addressed; URI policy allows repository-relative logical paths or governed object-store IDs, never machine-absolute paths.

`AnimationEvaluationPlanV1` pins deterministic validators and an independent evaluator profile. Its dimensions are: source/quote fidelity, voice/disclosure authority, AIR semantic preservation, identity/Visual DNA, role/tension/transfer, Composition Intent, Feature Contract realization, wrong-reading locks including derivative inheritance, temporal/track integrity, continuity, technical media integrity, generated-performance truth, and Format 02 exclusion. Thresholds, rubric versions, evaluator/model/runtime versions, and conflict policy come only from the pinned profile. This specification invents none.

`AnimationEvaluationReceiptV1` records candidate/ref hashes, per-dimension inputs/results/evidence, deterministic validator results, independent evaluation result, conflict status, profile hash, executor identity, and claim ceiling. Missing evidence is `NOT_EVALUATED_MISSING_REQUIRED_EVIDENCE`, never zero, false, or `NOT_APPLICABLE`. `NOT_APPLICABLE` requires an enumerated rule ID, rule version, rationale, and validator evidence; it cannot waive source, identity, disclosure, lock, or Format 02 exclusion obligations.

`AnimationOperatorDecisionV1` identifies exact candidate and evaluation bytes, decision enum, attributable actor, authority scope, reasons, requested corrections, HumanResolutionEpisode ref, and decision sequence. Acceptance is Pipeline production acceptance for the exact candidate. It is not publication, downstream consumption acknowledgement, production certification, or a reusable approval of later bytes.

`Format02ExclusionReceiptV1` records input profile/category claims, canonical ID, matched-alias scan, active-registry hash, no-inherited-certification result, and validation policy ref. Any active claim or alias that would execute Format 02 fails admission. Merely resembling a historical composition does not activate certification and cannot be used as proof of Format 02 conformance.

### 6.6 Commands, query APIs, and events

Commands are explicit request schemas:

| Command | Required authority and result |
|---|---|
| `AdmitAnimationExecution` | Source/identity grants, derivative job, Harness binding, AIR package, expected case version -> admitted case or typed denial |
| `CompileAnimationExecutionProgram` | Admitted immutable inputs and expected version -> program plus compilation and Format 02 exclusion receipts |
| `AttachAnimationVisualAssetResult` | Exact demand/result/production-acceptance refs and expected version -> consumed binding or rejection; acknowledgement is distinct |
| `ValidateAnimationExecutionProgram` | Exact program and pinned validators -> validation receipt |
| `AuthorizeAnimationRender` | Valid program, complete asset bindings, operator/run authority, expected version -> immutable attempt and outbox message |
| `IngestAnimationRenderCandidate` | Exact attempt, worker result, transport receipt -> candidate or late/stale evidence |
| `EvaluateAnimationRenderCandidate` | Exact candidate/profile -> immutable evaluation receipt |
| `RecordAnimationOperatorDecision` | Exact candidate/evaluation, attributable actor, expected version -> decision and HumanResolution ref |
| `RequestAnimationRevision` | Typed target, exact predecessor, owner route -> new revision intent; never in-place mutation |
| `CancelAnimationCommand` | Command/case/version and reason -> cancellation state and cancellation outbox |
| `InvalidateAnimationDependency` | Exact changed/ref revoked plus cause -> dependency traversal and invalidation projection |

All mutating commands require `command_id`, `idempotency_scope`, `idempotency_key`, `issued_at` as evidence-only metadata, actor, expected aggregate version, compatibility profile, payload hash, and causation/correlation IDs. `issued_at` never contributes to semantic artifact identity.

Read APIs are version-addressed: `GetAnimationCase`, `GetAnimationProgram`, `GetAnimationCandidate`, `GetAnimationEvaluation`, `GetAnimationDecision`, `GetAnimationDependencyGraph`, `GetAnimationReplayBundle`, and `ListAnimationCaseVersions`. A caller must explicitly request `current` projection or exact version. Exact historical reads never redirect to current.

Every successful mutation appends one or more typed events listed in section 5.8. Event envelopes pin event schema/version, aggregate/version, command, causation/correlation, payload digest, compatibility profile, and previous-event digest. Replay consumes committed events and content-addressed artifacts; external worker callbacks are replay evidence, not re-executed calls.

### 6.7 Repository and dependency invariants

The repository transaction boundary stores together:

1. aggregate snapshot/version;
2. canonical object bytes and content address;
3. command and idempotency records;
4. event(s) and hash-chain link;
5. success receipt(s);
6. dependency edges and invalidation projection;
7. outbox entries; and
8. current alias when applicable.

A program without a compilation receipt, a candidate without artifact bytes, an artifact without its attempt, a decision without candidate/evaluation, a dispatch without outbox, or a receipt without the referenced state is a corruption error. Repository validation checks both directions. The dependency graph includes source package, spans, authority grants, Identity/Voice/Visual DNA, AIR semantic programs, derivative job/Harness, parent derivatives/locks, visual assets/VAE results, runtime/adapter/model, evaluator/profile, candidate, decision, and consumption acknowledgements.

### 6.8 Compatibility and migration

Compatibility is negotiated by required semantic features, not parse success. Admission pins source/profile/schema/capability versions. Adapters must emit an `AdapterCoverageReceipt` listing every input semantic field, destination location, preservation mode, and unsupported feature. Dropped or generic-notes mappings fail. Unknown required enum/extension/cue/lock/evaluation dimension fails.

Migration reads exact old bytes and creates a new immutable version plus `MigrationReceiptV1` containing source/target schemas, migrator version/hash, field-by-field disposition, source and target hashes, authorization, validation, and predecessor edge. It never guesses source kind, quote class, voice class, identity, scene intent, lock, Feature Contract, Composition Intent, profile, or runtime. Missing required meaning yields `MIGRATION_BLOCKED_MISSING_SEMANTICS` and preserves the historical source. Active accepted attempts remain pinned to negotiated versions; deprecation does not rewrite them.

## 7. Implementation location, module boundaries, and import law

These are future implementation paths only; this writing factory creates none.

```text
05_ATOMIC_HARNESS_PIPELINE/
  src/atomic_harness_pipeline/animation/
    domain/
      models.py
      enums.py
      invariants.py
      events.py
      failures.py
    application/
      commands.py
      handlers.py
      queries.py
      ports.py
      invalidation.py
      replay.py
    compilation/
      admission.py
      provenance.py
      scene_program.py
      composition_ir.py
      layers.py
      rig_binding.py
      timing.py
      format02_exclusion.py
    evaluation/
      deterministic.py
      coordinator.py
      decision.py
    infrastructure/
      persistence.py
      outbox.py
      object_store.py
      runtime_adapters.py
      delegation_adapter.py
    api/
      schemas.py
      routes.py
  tests/
    unit/animation/
    contract/animation/
    integration/animation/
    replay/animation/
    portability/animation/
    fixtures/animation/
```

`domain` imports only standard library and approved shared primitives. `application` imports domain and ports, never infrastructure. `compilation` imports domain/application contracts and exact externally owned generated contract packages, not product source internals. `evaluation` consumes pinned evaluation contracts and cannot approve. `infrastructure` implements ports and is the only layer importing provider SDKs, persistence clients, object-store clients, or Delegation transports. `api` maps external transport to application commands; it contains no authority or business decisions.

Pipeline may import externally owned versioned schemas/types but must not copy or fork AIR, Builder, Interview Expression, VAE, or Delegation schemas into local authority. Tests may use fixtures but cannot import production-only provider clients into domain tests. Architecture tests enforce import edges and forbidden source ownership, not exact source-text snapshots.

## 8. Failures, migration, rollback, recovery, observability, security, and operations

### 8.1 Typed failures and owning route

| Failure code | Trigger | Owner/route | Retry |
|---|---|---|---|
| `ANI_INPUT_REF_UNRESOLVED` | Any required exact ref unavailable/hash mismatch | Supplying owner | No until corrected |
| `ANI_SOURCE_KIND_UNKNOWN` | Unknown/ambiguous source kind | Interview Expression/upstream | No |
| `ANI_INTERVIEW_PROVENANCE_MISSING` | Interview source lacks Reaction Receipt or Expression Moment | Interview Expression/upstream | No |
| `ANI_SOURCE_AUTHORITY_DENIED` | Source-use/identity grant absent, expired, revoked, or out of scope | Operator/source authority | No |
| `ANI_LANGUAGE_PROVENANCE_INVALID` | Quote/omission/condensation/bridge/rewrite invariant fails | Upstream author/IE | No |
| `ANI_VOICE_AUTHORITY_DENIED` | Synthetic/rerecorded/generated voice lacks exact authority/disclosure | Operator/source authority | No |
| `ANI_FORMAT02_ACTIVE_OR_ALIAS` | Canonical ID or governed alias is active | Builder/Program Control | No |
| `ANI_SEMANTIC_INPUT_INCOMPLETE` | AIR scene/Composition Intent/Feature Contract meaning absent | AIR | No |
| `ANI_LOCK_INHERITANCE_WEAKENED` | Parent lock absent or weaker | Builder/Pipeline request producer | No |
| `ANI_HARNESS_CAPABILITY_UNSUPPORTED` | Category/profile/runtime requirement not declared | Builder/Pipeline registry | No |
| `ANI_RIG_BINDING_UNSUPPORTED` | Rig/control adapter cannot preserve required cue/identity/lock | Pipeline | No; alternate authorized binding |
| `ANI_VISUAL_ASSET_PENDING` | VAE-owned asset result unavailable | VAE | Wait; no default substitute |
| `ANI_VISUAL_ASSET_STALE` | Demand/result/version or consumption status mismatch | VAE/Pipeline | No; obtain current result |
| `ANI_PROGRAM_VALIDATION_FAILED` | Deterministic contract check fails | Pipeline or named upstream owner | No until corrected |
| `ANI_RENDER_DISPATCH_FAILED` | Outbox/transport/worker dispatch fails | Pipeline/Delegation | Bounded retry same attempt |
| `ANI_RENDER_RESULT_LATE` | Result targets cancelled/superseded/revoked attempt | Pipeline evidence store | Never canonicalize |
| `ANI_RENDER_RESULT_MISMATCH` | Output count/type/hash/metadata/attempt mismatch | Worker/Pipeline adapter | Bounded retry/new attempt |
| `ANI_EVALUATION_EVIDENCE_MISSING` | Required deterministic or independent evidence absent | Pipeline/evaluator | Retry evaluation only |
| `ANI_EVALUATION_CONFLICT` | Independent and deterministic results conflict | Operator/Studio | No automatic approval |
| `ANI_CONCURRENCY_CONFLICT` | Expected aggregate version stale | Caller | Reload and reissue explicitly |
| `ANI_IDEMPOTENCY_COLLISION` | Same key with different canonical request | Caller/security | No |
| `ANI_DEPENDENCY_INVALIDATED` | Accepted program/candidate depends on changed/revoked bytes | Owning correction route | Recompile affected descendants |
| `ANI_STORAGE_ATOMICITY_FAILURE` | Any transaction participant fails | Pipeline operations | Retry full transaction safely |
| `ANI_REPLAY_ARTIFACT_MISSING` | Historical content-addressed byte unavailable | Pipeline operations | Incident; no substitution |

Failures include `failure_id`, code, owner, command/ref hashes, stage, retry class, affected objects, required correction, evidence refs, and claim ceiling. Messages must preserve safe context without source content or credentials.

### 8.2 Rollback, retry, cancellation, and partial results

Compilation has no externally visible success until the atomic transaction commits. Rollback removes staged object bytes or leaves them unreachable and garbage-collectable; it never emits a success receipt. Outbox dispatch begins only after commit. A worker retry uses the same immutable program and attempt identity only for transport-safe retry; a changed runtime/model/input creates a new attempt.

Partial scene results may be stored under the attempt but are never a complete candidate unless the authorized output profile explicitly allows partial delivery and the receipt enumerates missing slots and consumption restrictions. Partial delivery does not permit acceptance of missing required scenes, disclosures, locks, or evaluation evidence. Cancellation, supersession, invalidation, and revocation are append-only state transitions. They do not delete historical bytes.

### 8.3 Selective invalidation and historical reproduction

Invalidation traverses typed dependency edges. A changed source span invalidates its language segments, alignment, affected scene units, composition/render candidates, evaluations, and decisions, not unrelated scenes. A changed rig invalidates bound scene execution and descendants, not AIR scene meaning. A revoked voice grant invalidates every voice artifact/track/candidate using it. A strengthened parent lock invalidates descendants lacking it. A new current runtime or evaluator does not invalidate historical accepted work unless a governed revocation says so.

Historical reproduction resolves exact stored bytes for source, authorities, AIR programs, Harness/job, compiler policy, adapter/runtime/model, assets, program, attempts, evaluator, worker outputs, decisions, and environment manifest. `BIT_EXACT_REPLAY` is claimed only if the pinned runtime declares and proves it; otherwise the system performs `EVIDENCE_REPRODUCTION` from preserved bytes and labels a rerender as a new attempt. Current aliases, network calls, wall-clock values, environment discovery, and mutable provider endpoints are forbidden during evidence replay.

### 8.4 Observability and operational controls

Metrics include admission outcomes by typed reason, compilation latency, unresolved asset demands, validation failures, outbox lag, render attempts/retries/late callbacks, evaluation completeness/conflicts, operator decision latency, cancellation effectiveness, invalidation fanout, replay completeness, and repository invariant failures. Logs carry case/program/attempt/correlation IDs and digests, never raw interview text/audio, credentials, biometric embeddings, private endpoints, or unredacted provider responses. Traces connect command, transaction, outbox, Delegation transport, worker, ingestion, evaluation, and decision.

Operational dashboards distinguish written specification, implementation availability, provider connectivity, local validation, production authorization, acceptance, publication, certification, and consumption. None is inferred from another. Alerts exist for hash mismatch, orphaned state/receipt, outbox gap, stale result, missing historical byte, invalidation failure, unauthorized voice/identity use, and Format 02 alias admission.

### 8.5 Security, provenance, and sovereignty

Operator-supplied source authority, provenance, lineage, approvals, and product sovereignty are preserved; this specification adds no generic creative-safety or content-rights approval authority. Technical security enforces authenticated actors, least-privilege command scopes, signed/hash-pinned messages where governed, secret isolation, encryption at rest/in transit, content-address verification, audit logging, replay/idempotency protection, archive/path traversal rejection, decompression limits, media parsing isolation, and worker result authentication.

Untrusted archive members reject absolute paths, drive prefixes, UNC paths, parent traversal, alternate data streams, symlinks/reparse points where unsupported, case-fold collisions, duplicate normalized names, device names, and decompression bombs. Materialization occurs under an isolated job root using normalized relative paths. Output manifests never contain the machine root.

## 9. Acceptance criteria and failure examples

Each criterion is for later independent audit and implementation evidence; it is not acceptance in this writing prompt.

### AC-ANI-001 — exact admission identity

**Given** an `ST-05.04` derivative job with exact Harness, source, AIR, profile, and compatibility refs, **when** admission runs, **then** it stores one hash-pinned input manifest and rejects any mutable/latest lookup. Failure example: `visual_narrative_program_id` without version/hash. Evidence: admission receipt plus contract test. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-002 — interview provenance enforcement

**Given** `source_kind=interview_expression`, **when** Reaction Receipt or Expression Moment refs are empty, **then** admission returns `ANI_INTERVIEW_PROVENANCE_MISSING`. Failure example: source kind accepted with generic notes. Evidence: negative contract fixture and typed failure. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-003 — no guessed source classification

**Given** an unknown or absent governed source kind, **when** admission runs, **then** it fails without deriving classification from filenames or content. Failure example: `.mp4` guessed as interview. Evidence: property/negative test. Trace: `FR-147`.

### AC-ANI-004 — verbatim exactness

**Given** a `VERBATIM_SOURCE` segment, **when** normalized rendered text differs from its source spans, **then** validation returns `ANI_LANGUAGE_PROVENANCE_INVALID`. Failure example: a paraphrase labeled verbatim. Evidence: quote-diff receipt. Trace: `FR-148`, `ST-05.04`.

### AC-ANI-005 — disclosed omission

**Given** a `DISCLOSED_OMISSION` segment, **when** retained order, omission ranges, or rendered disclosure is absent, **then** render authorization fails. Failure example: ellipsis removed without disclosure. Evidence: provenance and disclosure validator receipts. Trace: `FR-148`.

### AC-ANI-006 — condensation and bridge distinction

**Given** condensed source meaning or operator bridge text, **when** it is represented as source speech, **then** validation fails; valid records use the correct transformation class and approval. Failure example: operator connective sentence attributed to guest. Evidence: classification fixtures. Trace: `FR-148`, `ST-05.04`.

### AC-ANI-007 — synthetic voice denial

**Given** cloned/synthetic voice reading new text without an exact synthetic-voice and identity-use grant, **when** compilation or authorization runs, **then** it returns `ANI_VOICE_AUTHORITY_DENIED`. Failure example: general interview consent treated as clone authority. Evidence: denial receipt. Trace: `FR-148`, `ST-05.04` invalid case.

### AC-ANI-008 — generated performance truth

**Given** a generated gesture or expression without direct observed-source evidence, **when** its cue is emitted, **then** it carries a generated-performance label and cannot claim actual participant reaction. Failure example: synthesized smile labeled Reaction Receipt evidence. Evidence: cue validator and semantic evaluation. Trace: `FR-147`.

### AC-ANI-009 — AIR meaning remains immutable

**Given** AIR-owned scene purpose, role/tension, Matrix/Edge, transfer, Final Script, or Composition Intent, **when** Pipeline compiles execution, **then** it references exact AIR bytes and creates no replacement semantic value. Failure example: runtime compiler rewrites scene purpose to fit a rig. Evidence: field-coverage receipt. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-010 — Composition Intent retained beside geometry

**Given** exact executable geometry, **when** the Composition IR is inspected, **then** it includes the source Composition Intent, reason, and allowed-variation refs. Failure example: only x/y/width/height remain. Evidence: schema and serialization test. Trace: `FR-147`.

### AC-ANI-011 — Feature Contract preservation

**Given** applicable Feature Contracts, **when** rig/layer/runtime adapters compile the scene, **then** every typed/versioned reference and realization obligation remains addressable; unsupported realization blocks. Failure example: Feature Contracts copied into generic notes. Evidence: adapter coverage receipt. Trace: `FR-147`.

### AC-ANI-012 — wrong-reading-lock monotonicity

**Given** parent derivative locks, **when** a child program is compiled, **then** it includes every inherited lock at equal or stronger force and cites portable parent-lock evidence. Failure example: child omits an inherited identity lock. Evidence: RC4-compatible inheritance validator receipt. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-013 — Format 02 remains inactive

**Given** canonical `format02_minimal_coach_theatre` or any governed alias in an active request, **when** admission runs, **then** it rejects and emits a Format 02 exclusion failure; no certification is inherited. Failure example: `minimal_coach_theatre` accepted as an alias workaround. Evidence: alias-registry fixtures and exclusion receipt. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-014 — no unauthorized demo/runtime route

**Given** a runtime, adapter, rig, or demo not declared by the exact Harness/capability profile, **when** binding runs, **then** it returns `ANI_HARNESS_CAPABILITY_UNSUPPORTED` or `ANI_RIG_BINDING_UNSUPPORTED`. Failure example: historical Stretchy assignment heading treated as production authorization. Evidence: negative binding test. Trace: `FR-147`.

### AC-ANI-015 — VAE boundary

**Given** missing visual ingredients, **when** compilation reaches asset binding, **then** Pipeline emits immutable Visual Asset Demands and waits for exact VAE result/production-acceptance bytes; it does not generate VAE-owned production plans. Failure example: Pipeline chooses a LoRA/model and accepts its image. Evidence: integration contract test. Trace: `FR-147`.

### AC-ANI-016 — production acceptance differs from consumption

**Given** a VAE production-accepted result, **when** Pipeline binds it, **then** it records a separate consumption acknowledgement after validating demand/result/version/locks. Failure example: VAE acceptance automatically marks asset consumed. Evidence: lifecycle test. Trace: `FR-147`.

### AC-ANI-017 — deterministic canonical program

**Given** identical immutable inputs in fresh processes with randomized map insertion, filesystem order, timezone, locale, environment, and working directory, **when** compilation runs, **then** canonical program bytes and digest are identical. Failure example: layer order follows directory traversal. Evidence: cross-process determinism suite. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-018 — atomic commit

**Given** injected failure at every repository write point, **when** a mutating command runs, **then** no success-visible artifact, receipt, command, event, dependency, alias, or outbox subset remains. Failure example: program stored without compilation receipt. Evidence: transaction fault-injection suite. Trace: `ST-05.04` CBAR.

### AC-ANI-019 — idempotency and concurrency

**Given** repeated identical command identity, **when** handled twice, **then** the original response is returned; changed payload with same key fails; stale expected version loses. Failure example: duplicate render dispatch. Evidence: concurrency/idempotency tests. Trace: `ST-05.04`.

### AC-ANI-020 — render output integrity

**Given** a worker callback, **when** output slot, type, codec, dimensions, duration, timebase, artifact hash, or attempt identity differs, **then** it cannot become a canonical candidate. Failure example: callback for superseded attempt attached to current. Evidence: worker-contract fixtures. Trace: `FR-147`.

### AC-ANI-021 — complete independent evaluation

**Given** a render candidate, **when** evaluation is requested, **then** every pinned deterministic and independent dimension produces result/evidence or a governed typed absence; missing evidence cannot become pass or N/A. Failure example: no identity evidence scored zero then threshold-passed. Evidence: evaluation matrix receipt. Trace: `FR-147`, `ST-05.04`.

### AC-ANI-022 — no capability/certification conflation

**Given** a runtime or evaluator capability declaration, **when** status is projected, **then** it does not imply evaluator certification, Format 02 certification, production authority, or build readiness. Failure example: `EVALUATE` presence sets certified. Evidence: status-projection test. Trace: `FR-147`.

### AC-ANI-023 — operator decision exactness

**Given** an attributable operator decision, **when** recorded, **then** it references exact candidate/evaluation hashes and HumanResolutionEpisode; another candidate cannot inherit it. Failure example: approval keyed only by case ID. Evidence: decision contract and stale-reference tests. Trace: `ST-05.04`.

### AC-ANI-024 — selective invalidation

**Given** a changed quote span, voice grant, rig, visual asset, runtime, or evaluation profile, **when** invalidation runs, **then** only exact dependent descendants are marked stale while unrelated scenes remain current. Failure example: changed scene quote leaves accepted candidate consumable. Evidence: dependency-graph integration tests. Trace: `ST-05.04` selective recovery.

### AC-ANI-025 — historical reproduction

**Given** an invalidated or superseded accepted candidate, **when** historical reproduction is requested, **then** exact source, semantic, program, asset, runtime, output, evaluation, and decision bytes remain retrievable without current aliases or network calls. Failure example: replay silently uses latest rig. Evidence: offline replay bundle test. Trace: `ST-05.04`.

### AC-ANI-026 — path and archive safety

**Given** malicious archive members or absolute machine paths, **when** ingestion/materialization runs, **then** traversal, drive/UNC, symlink/reparse, collision, device-name, and bomb inputs reject and generated manifests remain portable. Failure example: `../../voice.wav`. Evidence: security fixture suite. Trace: `FR-147`.

### AC-ANI-027 — no orphaned state or receipts

**Given** repository validation, **when** any program/candidate/decision/artifact/receipt/command/event/outbox/dependency counterpart is absent, **then** the case is quarantined as corruption and cannot advance. Failure example: accepted decision without evaluation artifact. Evidence: bidirectional invariant tests. Trace: `ST-05.04` CBAR.

### AC-ANI-028 — acceptance and publication remain separate

**Given** Pipeline production acceptance, **when** status is read, **then** publication, downstream consumption, certification, production eligibility, and build authority remain false/independent until their own governed receipts. Failure example: accepted render automatically publishable. Evidence: lifecycle projection tests. Trace: `FR-147`.

## 10. Testing strategy, completion evidence, and claim ceiling

### 10.1 Required test layers

| Layer | Required coverage |
|---|---|
| Unit | Scalar normalization, canonical JSON, quote diff, omission rules, voice matrix, source-kind/interview provenance, Format 02 alias scan, lock-strength comparison, rational timing, geometry, adapter field coverage, state transitions |
| Property/model | Random ordering/environment independence; time-range boundaries; monotonic lock inheritance; idempotency equivalence/collision; state-machine illegal transitions; normalized path invariants |
| Contract | Exact AIR scene/Composition Intent/Feature Contract consumption; AHP job/Harness; IE source package; VAE demand/result/ack; Delegation envelope; runtime worker; evaluation profile |
| Integration | Admit -> compile -> VAE asset bind -> validate -> dispatch -> ingest -> evaluate -> HumanResolution -> accept; denial and correction branches |
| Persistence | Atomic fault injection at every write; optimistic concurrency; command/event/receipt/artifact/outbox/dependency bijection; restart recovery |
| Replay | Offline exact historical bundle, invalidated/superseded versions, late callbacks, current-alias isolation, evidence reproduction vs rerender distinction |
| Security/portability | Archive/path attacks, content-address mismatch, unsigned callback, secret/redaction checks, clean extracted-layout run, no absolute-path leakage |
| Evaluation | Required dimensions, unsupported profile rejection, missing evidence, deterministic/independent conflict, N/A governance, capability/certification separation |
| Architecture | Import layer rules; no AIR/Builder/IE/VAE/Delegation schema fork; no provider SDK in domain/application; no exact-source brittleness |

### 10.2 Mandatory fixture set

Fixtures include: a valid imported-interview quote-driven explainer; missing Reaction Receipt; missing Expression Moment; unknown source kind; exact verbatim; invalid paraphrase-as-verbatim; valid/invalid disclosed omission; condensation; operator bridge; source audio; rerecorded human voice; generated voiceover; denied synthetic voice; generated gesture labeling; inherited derivative locks; weakened child lock; canonical and alias Format 02 attempts; unauthorized runtime; unsupported rig cue; VAE result version mismatch; stale callback; partial result; missing evaluation dimension; evaluator conflict; cancellation races; invalidation fanout; archive traversal; absolute path; and an offline historical replay bundle.

The positive reference slice starts with one hash-pinned imported interview source package and operator grants, uses exact Reaction Receipt and Expression Moment refs, consumes AIR Final Script/AnimationScenePackage/Visual Narrative Program/Composition Intent/Feature Contracts, admits an AHP derivative job, compiles a non-Format-02 scene program, obtains any required VAE assets, renders through a pinned worker, evaluates source/voice/semantic/identity/composition/lock/feature/technical dimensions, records HumanResolution, and reproduces the evidence offline. It must not require Format 02, Stretchy, HyperFrames, a particular provider, or unpinned external bytes.

### 10.3 Determinism and portability proof

The proof executes canonical compilation and replay at least twice in fresh processes while varying current time, timezone, locale, random seed, hash seed, environment variables, working directory, path separator assumptions, mapping insertion order, and fixture traversal order. It compares exact canonical bytes/digests. An authorized stochastic renderer pins the governed seed and runtime/model/environment but is not thereby claimed deterministic; its returned bytes are preserved as historical evidence.

Generated artifacts are scanned for Windows drive paths, UNC paths, POSIX home/temp roots, repository root, usernames, hostnames, process IDs, timestamps used as semantic IDs, and unresolved environment expansions. Failure blocks completion evidence.

### 10.4 Completion evidence package for later lifecycle stages

A future implementation completion claim requires, at minimum:

1. implemented-file manifest with exact hashes and import-boundary report;
2. requirement/Story/acceptance/test trace matrix for `FR-147`, `FR-148`, and `ST-05.04`;
3. schema and generated-type validation reports;
4. all fixture and test results in two fresh processes;
5. compilation and static-analysis results;
6. deterministic serialization/hash and portability reports;
7. atomicity, concurrency, idempotency, cancellation, invalidation, and replay evidence;
8. source/language/voice authority and disclosure evidence;
9. AIR semantic, Composition Intent, Feature Contract, identity, lock, and Format 02 exclusion receipts;
10. VAE demand/result/production acceptance and distinct consumption acknowledgement evidence;
11. runtime worker compatibility, render output, independent evaluation, and HumanResolution receipts;
12. no-orphan repository invariant report; and
13. independent audit, revision when required, re-audit, and attributable acceptance/ratification/adoption receipts at their governed stages.

### 10.5 Current writing completion state

This document completes only the one-spec writing assignment:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
format02_state: DEFERRED_NOT_ACTIVE
product_adoption_claim: false
implementation_created: false
development_capsule_created: false
```

The next permitted action for this specification is independent audit under Prompt 04. Changes to any pinned upstream draft reopen the six recorded revision-impact sections before acceptance. No sentence in this specification authorizes code, a provider, VAE Stage 5, a shared contract release, Format 02, build, production, publication, or certification.
