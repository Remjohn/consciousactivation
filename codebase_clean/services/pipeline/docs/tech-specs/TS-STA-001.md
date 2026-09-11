# TS-STA-001 — Composition IR, PRETEXT, Geometry, Annotation, and Skia Runtime

```yaml
spec_id: TS-STA-001
title: Composition IR, PRETEXT, Geometry, Annotation, and Skia Runtime
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Atomic Harness Pipeline
writing_wave: 12
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs: [FR-049, FR-050, FR-051, FR-052, FR-053, FR-054]
controlling_stories: [ST-05.01]
upstream_drafts:
  - {spec_id: TS-AHP-003, path: 05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md, quality_state: WRITTEN_PENDING_AUDIT, sha256: 072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {spec_id: TS-AIR-017, path: 04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md, quality_state: WRITTEN_PENDING_AUDIT, sha256: 0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
```

This candidate specification is authorized for technical writing and later independent review only. It creates no implementation, schema, contract release, provider, model, production, publication, certification, or Development Capsule authority. AIR owns visual-activation meaning, Visual Narrative Program, semantic Composition Intent, Feature Contracts, T/V requests, BBOX intent with WHY, and wrong-reading locks. Atomic Harness Pipeline consumes those exact bytes and owns renderer-neutral executable Composition IR, deterministic measurement and layout, annotation compilation, render orchestration, real static artifact evidence, and consumption acknowledgement. VAE owns production feasibility, visual production realization, accepted asset geometry, and production acceptance. No execution step may reconstruct or mutate AIR meaning or weaken inherited locks.

## 1. Files and authorities read

### 1.1 Writer packet, dispatch, and lifecycle ceiling

All digests are SHA-256 over the exact bytes read.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current one-spec writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact packet `CA-P03-WRITE-TS-STA-001-RECOVERY` |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_12_DISPATCH_LOCK.yaml` | 2,678 | `96f655bbf67a40a38a5cf233cfa9ad3f954466a8dae80ff68dfa87a2a5c9e5a7` | Wave 12 disjoint path and exact two-draft lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate authority remains non-current |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Write/review only; build and production false |

No `AGENTS.md` governs the target. The recovery packet authorizes only `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-STA-001.md` and its five writer receipts as `DIRECT_PRODUCT_SPEC_PATH` outputs.

### 1.2 Current and candidate authority

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current visual semantics, lineage, Visual Syntax, Feature Contract, T/V, BBOX/WHY, and wrong-reading authority |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product boundaries |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR meaning; Pipeline execution; VAE realization |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md` (`SRC-CUR-014`) | 7,065 | `10cf37d637aa85a9efa40ae236a801322025b3757825469c3923a9a8c96e49e6` | Required current VAE authority: requested role/function remain upstream; VAE returns feasible image-conditioned geometry and conflict evidence |

Candidate V2.1 ownership is `CANDIDATE_NOT_CURRENT`. It may control this technical proposal because Prompt 02C explicitly authorizes candidate specification work; it does not become current authority by being cited.

### 1.3 Requirements, Story, and source governance

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Exact title, owner, lane, gate, and canonical target |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | `FR-049` through `FR-054` |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact FR/Story/source/evidence trace |
| AHP `prd/features/F09-composition-ir-geometry-typography-annotation-and-skia-static-runtime.md` | 18,941 | `68db87fa583d639af2ebdc707e9f94e7bca50af9b981dca1dd9c2f6be8eef456` | Renderer-neutral IR, functional BBOX, final-font measurement, deterministic solver, annotations, real artifacts |
| AHP `planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553 | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | `ST-05.01`, CBAR defense, denial, replay, selective recovery |
| AHP `planning/spec_assignments/TS-STA-001.md` | 3,697 | `59d8fc1eb4fa8295e5ca2855739d3f3e8d0d2edc34901990d5d42f315652e90f` | Assignment brief; its historical target grants no path authority |
| AHP `governance/CURRENT_WRITING_PROFILE.md` | 11,536 | `ba88c5572ae3f7571daac9991a0d325a20f491cb9c0ea7c3816deb3ff3d32956` | Source-first, CBAR, owner, N/A, evidence, and claim laws |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | 134,201 | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Required/deferred source classification |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_GAP_NOTICE.yaml` | 17,743 | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Existing non-blocking external-source gaps |

### 1.4 Non-accepted upstream drafts

| Draft | Bytes | SHA-256 | Interface consumed |
|---|---:|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md` | 64,377 | `072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed` | `ContentDerivativeJob`, exact Harness/category/profile, source restrictions, capabilities, evaluation, lifecycle, and wrong-reading inheritance |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md` | 67,346 | `0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81` | Visual Activation Handoff, Visual Narrative Program, Composition Intent, Feature Contracts, BBOX/WHY, locks, VAE handoff, and visual reparse boundary |

Both are `WRITTEN_PENDING_AUDIT` and `DRAFT_DEPENDENCY_NOT_ACCEPTED`. A hash change reopens governing decisions; architecture/workflows; data models/contracts/schemas/APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence. Their proposed interface detail is not represented as ratified law.

### 1.5 Required predecessor evidence

| Source | Bytes | SHA-256 | Current disposition |
|---|---:|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/composition_runtime.py` (`SRC-LEG-004`) | 32,024 | `b0416bbf0b708467c01d8d80aa17c6137ea1b2865cb8b0b9aae039dcfa53fbe3` | `ADAPT`: useful canvas/zone/layer/runtime/evidence vocabulary; replace mixed authority, floats, open dicts, defaults, random IDs, wall time |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/composition_runtime_service.py` (`SRC-LEG-005`) | 46,290 | `83e3f84032bc4538262b03da223739886e575b4d3245fabea184d6cd9d3fc9d1` | `REPLACE`: useful workflow evidence; hard-coded layouts/scores, inferred meaning, synthetic refs, independent writes cannot be canonical |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/asset_program_compilers.py` (`SRC-LEG-028`) | 28,865 | `b8f018ae42956618e2466465faeb33912824e005c5c7878fb266d7c985638ca3` | `ADAPT`: Geometrics/Skia/annotation concepts; replace deprecated sidecar authority and open shapes |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/asset_program_compiler_service.py` (`SRC-LEG-029`) | 44,636 | `b4726def1d6917ab2dfc399972d89418e9ae2bcfc4f72bfe5d7612dd312f48fc` | `REPLACE`: static scene path emits synthetic refs, defaults, fixed scores and local approval |
| `THE_CMF_STUDIO(2)/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` (`SRC-LEG-033`) | 9,409 | `402b57e027aecd3daba2dced3add91bcc1d2b107c5dc2166adec8ea3678740af` | `ARCHIVE` as migration/audit evidence; no current authority |
| `THE_CMF_STUDIO(2)/docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` (`SRC-LEG-036`) | 22,534 | `b2b313874608c07707b7e4e8c51a3900754960d535265409c3b70e144d2195e5` | `ADAPT`: preserve measure/solve/render/evaluate evidence spine; replace old ownership, provider requirements, floats/open maps, fixed thresholds |

The related predecessor repositories, APIs, and tests were also read. Independent mutable maps, service-global instances, mutable request defaults, untyped dictionaries, current-time/random identifiers, and tests that assert synthetic strings or local self-approval are evidence of behavior to replace, not current implementation authority.

`SRC-EXT-008`, `SRC-EXT-009`, and `SRC-EXT-015` are `DEFERRED_REFERENCE`. Exact bytes are unavailable, no unique current requirement depends solely on them, and this specification attributes no API, license, deterministic, compatibility, or implementation fact to them. The governed contracts below define the required PRETEXT-compatible measurement, Rough Annotation, and Skia worker behavior without reconstructing those sources.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure

AIR's semantic Composition Intent describes hierarchy, reading path, spatial psychology, BBOX function with WHY, negative space, depth, intended viewer state, Feature Contracts, and locks. It is not executable pixel geometry. A VAE Asset Result may contain accepted assets, masks, focal regions, protected regions, crops, gaze, depth, and recommended BBOXes, but VAE cannot choose a different semantic role. A static renderer that jumps directly from prose or assets to pixels can silently:

- flatten `BBOX + function + WHY` into coordinates;
- measure final text with an unpinned font or approximate character count;
- resolve collisions according to iteration or filesystem order;
- cover a face, hand, evidence object, identity feature, negative-space intent, or required text reservation;
- change hierarchy or reading order to make a local layout fit;
- render baked/generated text instead of the approved exact text;
- let a hand-drawn annotation become decorative emphasis with no semantic job;
- accept a synthetic URI or model response instead of real render bytes;
- let preview and final use different plans, fonts, assets, renderer versions, or cue paths;
- treat VAE production acceptance as Pipeline consumption or render acceptance;
- drop parent wrong-reading locks in a crop/size derivative;
- claim deterministic rendering from an unpinned environment; or
- approve the producer's own polished output without reparse and independent evaluation.

### 2.2 User/system outcome

A static composition operator receives one inspectable, deterministic, source-grounded static artifact package whose canvas, layers, exact assets, text, functional BBOXes, hierarchy, reading order, measured typography, collisions, annotations, provenance, Transformation Contract, and inherited locks are reconstructable from immutable bytes. A typed denial names cause, owner, and next admissible action before an invalid composition becomes accepted state.

### 2.3 Bounded solution

Pipeline admits an exact `ContentDerivativeJob` and AIR Visual Activation Handoff; acknowledges exact VAE Asset Results separately; compiles renderer-neutral `StaticCompositionIR`; measures text through a pinned measurement adapter under final font conditions; solves geometry deterministically within AIR/VAE constraints; compiles typed annotation cues; seals a Skia worker request; stores actual hash-addressed artifacts; runs deterministic reparse plus independent evaluation; and records an attributable operator decision. Every mutation is versioned, atomic, idempotent, concurrency-safe, invalidatable, and replayable.

### 2.4 In scope

- General static execution primitives shared by Carousels, SuperVisuals, single-image compositions, previews, diagnostic plates, and registered static output profiles.
- Exact Composition IR, functional region/BBOX, layer hierarchy, reading order, text measurement, geometry solving, annotation cues, render packets, artifact/evaluation/decision receipts.
- Consumption of AIR meaning and locks; consumption acknowledgement of VAE results.
- Determinism, portability, atomicity, replay, invalidation, migration, typed failures, and evidence.

### 2.5 Out of scope and non-goals

- AIR semantic compilation, Final Script, visual candidate meaning, Visual Narrative Program, Composition Intent, Feature Contracts, T/V route meaning, Primitive/archetype/Matrix/role-tension/transfer reconstruction.
- Builder Harness/category/profile mutation or category-specific Carousel/SuperVisual sequence semantics owned by later specs.
- VAE production planning, provider/model/LoRA/conditioning/mask generation, candidate evaluation/repair/production acceptance.
- Browser screenshot fallback, provider selection, external library adoption, UI editor, publication, certification, Format 02, VAE Stage 5, code, schema bytes, or shared release bytes.

## 3. Governing decisions and constraints

### 3.1 Unique ownership

| Object/decision | Owner | Pipeline permission | Forbidden Pipeline behavior |
|---|---|---|---|
| Visual activation meaning, Visual Semantic Pack, Visual Narrative Program | AIR | Read exact immutable refs | Rebuild, summarize as authority, or alter |
| Semantic Composition Intent, BBOX function/WHY, Feature Contracts, T/V route request, locks | AIR | Compile exact execution syntax within allowed variation | Change semantic job, hierarchy, reading path, role, required state, or lock |
| Atomic Harness/category/profile/Feature dependencies | Builder | Validate exact execution binding | Infer a missing profile or rewrite Harness |
| Visual Asset Demand and exact Composition IR | Pipeline | Own immutable execution versions | Transfer demand ownership to VAE or renderer |
| Visual Production Plan and image-conditioned asset realization | VAE | Consume exact production-accepted result after independent acknowledgement | Pick production route/model or silently alter requested role |
| Static worker embodiment | Pipeline infrastructure | Execute sealed request and return bytes | Become semantic or acceptance authority |
| Cross-product transport | Delegation | Carry immutable envelope/receipts | Interpret or repair meaning |
| Operator correction | Studio/operator | Submit typed command/HumanResolution | Hidden in-place mutation |

### 3.2 Composition-before-rendering and semantic retention

`VisualActivationHandoff -> StaticCompositionIR -> TextMeasurementSet -> SolvedCompositionPlan -> StaticRenderProgram -> RenderArtifactSet -> Reparse/Evaluation -> OperatorDecision` is the required order. The executable plan always retains exact upstream refs and the reason/allowed-variation behind each constraint. Pixels or coordinates alone never prove conformance.

### 3.3 BBOX means geometry plus function

Every region carries normalized geometry, `region_function`, `semantic_job_ref`, `why_ref`, hierarchy/reading-order role, strength, tolerance policy, protected/reserved relations, applicable Feature Contracts, and wrong-reading locks. Coordinates without function or function without coordinates are invalid. Pipeline may resolve exact geometry within allowed variation; outside-tolerance movement creates an amendment/conflict route to the upstream owner.

### 3.4 Final-font measurement law

Text measurement is valid only for exact approved text bytes, language/script/direction, font artifact hash, face/index, axes/features, size, line height, letter/word spacing, shaping/measurement adapter/version/hash, width/height constraints, hyphenation/wrapping policy, and pixel-density/render profile. Measurement is mechanical evidence, not editorial permission. Overflow cannot trigger automatic rewriting, quote changes, font substitution, or hierarchy mutation.

### 3.5 Deterministic solving and rendering

Determinism requires canonical integer/fixed-point values, stable input ordering, pinned algorithms/adapters/fonts/assets/color profiles/renderer/runtime/environment, explicit tie-breakers, no wall clock/random/process/environment/filesystem dependency, and real artifact hashing. A seed is not sufficient if any unpinned component remains. If a governed rendering environment cannot guarantee bit identity, it may emit `ENVIRONMENT_PINNED_REPRODUCIBLE` rather than `BIT_EXACT_DETERMINISTIC`; claim level is evidence, not marketing.

### 3.6 Annotation law

An annotation cue is renderer-neutral syntax with a target, semantic job, cue type, z-order, reveal/static timing, deterministic seed/path or exact path hash, style tokens resolved by a pinned registry, and lock/Feature refs. It cannot invent emphasis, cover protected evidence, change reading order, or substitute for semantic meaning. Unsupported optional cues may be omitted only through a governed applicability rule proving meaning survives; required cues block.

### 3.7 Wrong-reading locks

Generative, composited, restyled, cropped, reformatted, or semantically transformative demands require nonempty locks. Every derivative inherits the complete parent lock set, may add stricter locks, and may not remove/weaken one. Relaxation requires a new authorized upstream demand/version. Pipeline validates portable parent-lock evidence before compilation and records realization evidence after reparse/evaluation.

### 3.8 `NOT_APPLICABLE`, evaluation, and acceptance

Missing required data is never `NOT_APPLICABLE`. N/A requires a typed decision with requirement ID, exact rule/version/hash, condition, evidence, owner, reason, and claim restriction. It cannot waive source lineage, exact text, BBOX function, required Feature Contracts, inherited locks, required measurement, artifact bytes, or evaluation.

The producing compiler/solver/renderer does not independently approve judgment output. Mechanical validators run first; an independent evaluator assesses semantic/visual conformance under a pinned profile; an attributable operator owns acceptance where required. VAE production acceptance, Pipeline asset consumption acknowledgement, Pipeline static render acceptance, AIR visual reparse, downstream consumption, publication, certification, and production authority remain separate receipts.

### 3.9 Draft-dependency caveat and claim ceiling

TS-AHP-003 and TS-AIR-017 are non-accepted interfaces. Any hash change reopens the six named sections. This spec finishes only `WRITTEN_PENDING_AUDIT`; before ratification it cannot exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, cannot be `ACCEPTED_FOR_BUILD`, and cannot receive a Development Capsule.

## 4. Current brownfield architecture

| Component | Actual behavior observed | Disposition | Migration constraint |
|---|---|---|---|
| `contracts/composition_runtime.py` | Pydantic zones/layers/templates/runtime/eval records with useful relationships; extensive UUID defaults, wall time, floats, open dicts, local primitive thresholds, broad mixed video/still authority | `ADAPT` | Map only typed concepts; exact field-level receipt; no automatic upgrade of defaults/open payloads |
| `services/composition_runtime_service.py` | Builds default zones/layers, synthetic refs, inferred beats/anchors, hard-coded scores/thresholds and approval; writes multiple repository maps sequentially | `REPLACE` | Historical objects remain readable; no current authority or accepted-state migration without exact semantics |
| `contracts/asset_program_compilers.py` | Defines Geometrics scene, legacy Skia binding, single-image scene and render receipts; also flags old Skia sidecar routes deprecated | `ADAPT` | Preserve useful scene/render vocabulary; replace dict/float/default/deprecated authority and mixed product concepts |
| `services/asset_program_compiler_service.py` | Emits deterministic-looking hashes over synthetic plans, default scene/assets, fixed validation IDs/scores and local self-approval | `REPLACE` | Synthetic refs cannot become artifact evidence; approved flags do not migrate as acceptance |
| predecessor repositories | Independent in-memory maps and `put_*` calls without aggregate transaction, command/idempotency/event/outbox/dependency bijection | `REPLACE` | Historical evidence only; migration validates both artifact and receipt counterparts |
| predecessor APIs | Process-global services, request defaults/open dictionaries, high-level calls that hide authority, version, hash, idempotency and expected version | `REPLACE` | New transport maps exact commands only; no business decision in route layer |
| `CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Historical audit of a proposed execution spine | `ARCHIVE` | Retain hash/trace; no current claim |
| `TS-CMF-095...md` | Historical measure/solve/render/evaluate design, fixed provider assumptions and old ownership | `ADAPT` | Preserve evidence spine; current owners/contracts/claim limits govern |
| predecessor tests | Assert synthetic strings, counts, fixed local approval and deprecated renderer refs; useful negative path and relationship examples | `ADAPT` | Replace string-presence tests with contract, bytes, state, determinism, authority, and failure evidence |

There is no current Pipeline implementation at the target root. This prompt creates only this specification. No predecessor module is activated by reference.

## 5. Proposed architecture and workflows

### 5.1 Components

| Component | Responsibility |
|---|---|
| `StaticCompositionAdmissionService` | Verify exact job/Harness/AIR/VAE refs, lifecycle, source, profile, capabilities, locks, authority, and claim ceiling |
| `CompositionIntentCoverageValidator` | Prove every AIR intent/Feature/lock/T-V/BBOX item is preserved or governed N/A; never reinterpret |
| `VaeGeometryConsumptionService` | Validate demand/result/production-acceptance versions and record separate consumption acknowledgement |
| `CompositionIrCompiler` | Compile renderer-neutral canvas/regions/layers/text/hierarchy/reading order/provenance/Transformation Contract |
| `TextMeasurementCoordinator` | Bind pinned PRETEXT-compatible adapter, final font/assets/config, and store exact measurement set |
| `DeterministicGeometrySolver` | Resolve constraints with pinned priority/tie-break rules and emit complete collision decisions |
| `AnnotationCueCompiler` | Compile typed Rough Annotation cues and deterministic path/style/timing evidence |
| `StaticRenderProgramCompiler` | Seal exact solved plan/assets/fonts/cues/renderer/evaluation obligations |
| `SkiaWorkerGateway` | Dispatch idempotent sealed jobs through infrastructure/Delegation and authenticate returned artifacts |
| `StaticArtifactIngestionService` | Validate actual bytes, count, type, size, profile, content hash, program/attempt identity, portability |
| `StaticReparseService` | Mechanically derive observed hierarchy, geometry, reading order, collisions, text, cue and lock facts from exact artifacts |
| `StaticEvaluationCoordinator` | Run deterministic checks and independent profile-pinned judgment evaluation; no approval authority |
| `StaticOperatorDecisionService` | Record attributable exact-byte decision and HumanResolution ref |
| `StaticCompositionRepository` | Atomic state/artifact/receipt/command/event/dependency/idempotency/outbox/current projection |
| `StaticInvalidationAndReplayService` | Traverse exact dependency edges, selectively invalidate, and reproduce historical evidence offline |

### 5.2 Workflow A — admission and authority closure

1. `AdmitStaticComposition` receives an exact `ContentDerivativeJob`, Builder Harness/execution binding, AIR Visual Activation Handoff, requested output profile, source/identity/brand/DNA refs, required VAE results, and expected case version.
2. Resolve every reference by schema, version, hash, owner, lifecycle, compatibility, and claim ceiling. Unknown/stale/current-alias-only refs reject.
3. Validate category/profile and static capability; later category specs may narrow but never weaken this base runtime.
4. Validate source restrictions, approved exact text, Transformation Contract, parent-derivative chain, complete locks, Feature Contracts, T/V requirements, Composition Intent, and evaluation profile.
5. For each VAE asset, validate exact Visual Asset Demand/Asset Result/Production Acceptance relation, requested versus realized geometry/tolerance, inherited locks, and result currency. Commit a distinct Pipeline consumption acknowledgement.
6. Emit `StaticCompositionInputsAdmitted` or typed denial. No render or artifact identity exists on denial.

### 5.3 Workflow B — renderer-neutral Composition IR

1. Compiler creates canvas/profile and ordered layer/region identities from exact AIR intent plus category plan.
2. Every AIR BBOX intent becomes one or more `FunctionalRegion` records retaining its function, WHY, sequence role, hierarchy, reading path, allowed variation, Feature Contract and locks.
3. Bind accepted VAE asset refs and image-conditioned geometry without replacing upstream function. Out-of-tolerance geometry creates `STATIC_GEOMETRY_AUTHORITY_CONFLICT`.
4. Bind exact text/source/transformation provenance and exact font artifact/config. Baked or generated text cannot substitute.
5. Compile layer hierarchy, clipping/masks, reserved/protected regions, negative-space constraints, asset transformations, annotation intent, and output obligations.
6. Validate total upstream field coverage and emit immutable `StaticCompositionIR` plus compilation/coverage receipts.

### 5.4 Workflow C — measurement and solving

1. For every final text layer, build a hash-pinned `TextMeasurementRequest` including exact text/font/layout configuration.
2. Pinned adapter returns line/grapheme ranges, advances, ink/logical bounds, baselines, width/height, overflow and missing-glyph evidence in fixed-point units.
3. Reject request/result mismatch, unpinned fallback font, missing glyph, ambiguous direction, overflow, or nonfinal configuration.
4. Solver consumes immutable Composition IR and measurement set. It applies a profile-pinned priority graph: hard authority/locks/protected identity/evidence -> exact required text/legibility -> semantic hierarchy/reading path -> Feature/BBOX function -> negative space/depth -> allowed optional material/annotation. The profile, not code defaults, contains tolerances.
5. Stable constraint IDs and tie-break keys make iteration/order irrelevant. Every accepted, moved, scaled, wrapped, clipped, omitted-under-rule, or blocked item receives a `ConstraintResolution`.
6. Solver emits one or more immutable variants only when the profile authorizes alternatives. Selection is an explicit later command, never “first valid” unless the profile says so.

### 5.5 Workflow D — annotation and sealed rendering

1. Compile each applicable annotation to target, semantic job, type, deterministic style registry ref, z-order, timing, seed policy, exact geometry/path hash, collision envelope, Feature/lock refs, and fallback/applicability rule.
2. Validate cue path against protected regions, reading order, text bounds and output profile. Decorative/unowned emphasis rejects.
3. `SelectSolvedStaticVariant` records the exact selected plan and evidence. `CompileStaticRenderProgram` pins all refs and a Skia worker/runtime capability binding.
4. `AuthorizeStaticRender` atomically creates attempt, sealed request bytes/hash and outbox. Dispatch occurs only after commit.
5. Worker returns authenticated artifacts and manifest. Ingestion reads actual bytes, recomputes hashes, validates counts/media/dimensions/colorspace/alpha/profile, and stores content-addressed artifacts. A URI or claimed hash without bytes is failure.

### 5.6 Workflow E — reparse, evaluation, and decision

1. Mechanical reparse reads exact artifacts and program to observe text, bounds, hierarchy, reading order, protected-region collisions, image placement, cue realization, empty/overfull regions, and output-profile facts.
2. Compare observations with exact Composition Intent, solved plan, Feature Contracts, VAE geometry/tolerance, locks, approved text, and render program.
3. Deterministic validators emit pass/fail/typed missing evidence. Independent evaluator judges semantic hierarchy, attention path, source truth, identity/Visual DNA, composition effectiveness, negative space, wrong-reading risk, and category/profile dimensions under a pinned profile.
4. Conflict or missing evidence blocks automatic acceptance. An attributable operator accepts, rejects, contests, or requests a typed correction for exact artifact/evaluation bytes and records a HumanResolutionEpisode ref.
5. Render acceptance remains separate from publication, category certification, production eligibility, and downstream consumption.

### 5.7 Workflow F — correction, invalidation, and replay

Correction routes to the narrow owner: source/text/authorization -> source owner/operator; semantic hierarchy/Composition Intent/Feature/locks -> AIR; Harness/profile -> Builder; VAE asset/geometry -> VAE; executable IR/measurement/solver/render -> Pipeline; transport -> Delegation; taste/interpretation -> operator/Studio. Pipeline never “fixes” missing meaning.

A correction creates a new immutable version and invalidates only typed descendants. Changed text/font invalidates its measurement, dependent constraints, plan/program/render/evaluation/decision; unrelated layers remain. Changed AIR intent invalidates dependent executable syntax; changed VAE asset invalidates its binding/geometry and dependent outputs. Historical bytes remain addressable.

Replay resolves exact stored input, program, font, adapter, solver, renderer/runtime/environment, artifact, evaluator, and decision bytes. It does not call current providers or mutable registries. A rerender is a new attempt; evidence replay is not represented as identical pixel reproduction unless the environment proves it.

### 5.8 State machine and atomicity

```text
REQUESTED -> INPUTS_ADMITTED -> IR_COMPILED -> TEXT_MEASURED -> GEOMETRY_SOLVED
 -> VARIANT_SELECTED -> RENDER_PROGRAM_COMPILED -> VALIDATED -> RENDER_AUTHORIZED
 -> RENDERING -> ARTIFACTS_INGESTED -> REPARSED -> EVALUATED -> OPERATOR_REVIEW
 -> ACCEPTED | REJECTED | CONTESTED | REVISION_REQUESTED
Any immutable version may later become CANCELLED | SUPERSEDED | INVALIDATED | REVOKED.
```

Each mutation atomically commits aggregate/version, canonical artifact bytes, command, events, success receipts, dependency edges, idempotency record, current projection, and outbox. Any failure rolls back the whole success transaction. Same idempotency scope/key plus identical canonical request returns the original result; different bytes fail collision. Compare-and-swap expected version prevents concurrent selection/authorization/decision races. Cancellation before dispatch commit prevents work; after commit it appends cancellation and worker-cancel outbox. Late results remain noncanonical evidence and cannot resurrect stale state.

## 6. Data models, contracts, schemas, and APIs

### 6.1 Canonical scalar rules

Every contract is closed, immutable, schema/version identified, owner identified, and content hashed. No field is `Any`, an untyped dictionary, or an implied default.

| Type | Fields and invariants |
|---|---|
| `ImmutableRef` | `object_kind`, `object_id`, `version`, lowercase 64-hex `sha256`, `schema_id`, `owner_product`; no current-only ref |
| `ArtifactRef` | `ImmutableRef`, `media_type`, `byte_length`, `content_address`, optional registered logical filename; no absolute path or URI without stored bytes |
| `FixedPoint` | signed integer `value`, positive integer `scale`; schema declares unit and permitted scale |
| `NormalizedRect` | integer millionths `x`, `y`, `width`, `height`; positive size and within `[0,1000000]` canvas |
| `PixelRect` | signed integer micropixels `x`, `y`, `width`, `height`; width/height positive |
| `Rational` | signed numerator, positive denominator, reduced before hashing |
| `ColorValue` | registered colorspace/profile ref plus integer channel values; no implicit sRGB |
| `TypedExtension` | registered namespace/type/version/hash/payload; unknown required extensions reject, unknown optional extensions preserve bytes |
| `ApplicabilityDecision` | requirement, `APPLICABLE` or `NOT_APPLICABLE`, exact rule ref/hash, condition facts, evidence refs, owner, reason, claim restriction |

Canonical JSON uses UTF-8, Unicode NFC, lexicographically sorted object keys, schema-declared ordered arrays, schema-declared sort keys for set-like arrays, integers only, no NaN/infinity, and no insignificant whitespace. Hash input excludes wall time, host, PID, environment, absolute path, transport retry metadata, and mutable aliases. Equal-order constraints without an explicit tie-break key reject.

### 6.2 Input manifest and VAE consumption

`StaticCompositionInputManifestV1` requires:

```text
schema_id, manifest_id, version
content_derivative_job_ref
harness_definition_ref, harness_execution_binding_ref
source_package_refs[], source_authority_refs[]
visual_activation_handoff_ref
visual_semantic_pack_ref, visual_narrative_program_ref
composition_intent_refs[], feature_contract_refs[]
approved_final_script_ref, activation_transfer_contract_ref
primitive_coalition_ref, archetype_coalition_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
category_id, profile_id, output_profile_ref
transformation_contract_ref
visual_asset_bindings[]
parent_derivative_refs[], parent_lock_evidence_refs[]
wrong_reading_lock_refs[], evaluation_profile_ref
compatibility_profile_ref, required_capabilities[]
```

Each `VisualAssetBindingV1` contains exact Visual Asset Demand, VAE Asset Result, VAE Production Acceptance, asset artifact, image-conditioned geometry pack, requested/realized geometry comparison, tolerance consumption, inherited locks, delivery profile, and Pipeline Consumption Acknowledgement refs. The acknowledgement is created only after exact result validation and cannot be inferred from VAE acceptance.

Parent derivative and parent lock evidence arrays are both required for derivatives and both empty at the root. Validator computes transitive ancestor locks. Same lock ID with narrower scope, weaker enforcement, reduced evidence, or missing descendant application is `STATIC_LOCK_INHERITANCE_WEAKENED`.

### 6.3 `StaticCompositionIRV1`

```text
schema_id, composition_ir_id, version, content_sha256
input_manifest_ref, canvas_spec
functional_regions[], layers[], reading_order[]
hierarchy_edges[], spatial_relationships[]
reserved_regions[], protected_regions[], negative_space_constraints[]
text_layers[], asset_bindings[], annotation_intents[]
composition_intent_refs[], feature_contract_refs[]
transformation_contract_ref, provenance_bindings[]
wrong_reading_lock_refs[], evaluation_obligations[]
compilation_policy_ref, coverage_receipt_ref
predecessor_ir_ref?, claim_ceiling
```

`CanvasSpecV1` requires integer width/height, pixel-density rational, physical-size policy, colorspace/ICC artifact ref, alpha policy, background policy, output profile and safe-area refs. Width/height are not parsed from a string.

`FunctionalRegionV1` requires region ID, normalized requested geometry, syntactic function enum, attention function enum, semantic job ref, WHY ref, sequence role, hierarchy rank, reading-order memberships, hard/soft strength, allowed variation ref, tolerance policy ref, protected/reserved relations, applicable Feature Contract refs, T/V refs, lock refs, and source owner. Function enums are registry/version pinned; unknown values reject.

`CompositionLayerV1` requires layer ID, one type (`ASSET`, `TEXT`, `VECTOR`, `SHAPE`, `ANNOTATION`, `MASK`, `BACKGROUND`, `DIAGNOSTIC`), parent layer, z-order, region ref, source/artifact ref where applicable, transform, crop/clip/mask refs, opacity fixed-point, blend-mode enum, visibility, role/function refs, provenance, Feature refs, and locks. Cycles, duplicate IDs/z-tie ambiguity, missing parents, or a layer pointing outside its region policy reject.

`ReadingOrderEntryV1` contains path ID, ordinal, layer/region target, transition relation, semantic reason ref, required/optional state, and evaluation obligation. Reading order is not inferred from z-order or coordinates. `HierarchyEdgeV1` is typed (`PARENT`, `DOMINATES`, `SUPPORTS`, `CONTRASTS`, `ANNOTATES`, `EVIDENCES`) and acyclic for structural edge types.

`TextLayerV1` requires exact approved text bytes/hash, language/script/direction, source/transformation provenance ref, semantic job, region, font configuration ref, wrap/hyphenation/truncation policy refs, alignment, max lines, accessibility label ref, annotation target ranges, Feature refs and locks. Truncation is forbidden unless the exact upstream Transformation Contract authorizes it and disclosure remains correct.

Positive example: a headline region retains AIR's `PRIMARY_RECOGNITION_CARRIER`, WHY ref and left-to-right reading path while executable geometry is solved inside allowed variation. Negative example: `{bbox:[.1,.1,.8,.2], label:"headline"}` lacks function, WHY, ownership, tolerance, lineage, Feature and lock refs and rejects.

### 6.4 Typography measurement contracts

`FinalFontConfigurationV1` requires font artifact/hash, collection face index, variation axes as sorted typed tags/fixed values, OpenType feature set, language/script/direction, size in micropoints, line height rational, letter/word spacing in micropixels, hinting/raster policy, fallback policy, colorspace/density profile, and license/evidence ref when governed. Fallback is `FORBIDDEN` unless a pinned policy provides an exact ordered, hash-pinned set.

`TextMeasurementRequestV1` requires text layer/ref/hash, final font configuration ref, maximum width/height in micropixels, wrap/hyphenation/line-break policies, measurement adapter binding, and canonical request hash.

`TextMeasurementResultV1` requires request ref/hash; adapter ID/version/binary hash; font config hash; grapheme count; ordered line records; logical and ink bounds; baseline/ascender/descender/leading; total measured width/height; overflow axes and exact first overflowing grapheme; missing-glyph records; and environment manifest ref. Each line records Unicode scalar and grapheme ranges, exact substring hash, advance, logical/ink boxes, baseline, and break reason. Indices declare coordinate system and cannot mix byte/codepoint/grapheme offsets.

A `PRETEXT` capability declaration means the adapter conforms to this contract and passes compatibility evidence. It does not assert facts about unavailable external source bytes. Result mismatch, float-only output, missing font hash, fallback substitution, or measurement under nonfinal font conditions rejects.

### 6.5 Geometry constraints and solution

`GeometryConstraintV1` contains constraint ID, type, subject refs, object refs, hard/soft, priority class, semantic/function/WHY refs, source owner, allowed variation/tolerance, exact predicate/operator, fixed-point parameters, conflict group, tie-break key, Feature refs, locks, and evidence obligations. Types include `INSIDE`, `OUTSIDE`, `NO_OVERLAP`, `MIN_GAP`, `ALIGN`, `ANCHOR`, `ASPECT`, `SIZE_RANGE`, `READING_SEQUENCE`, `VISIBILITY`, `SAFE_CROP`, `PROTECTED_REGION`, `RESERVED_REGION`, `NEGATIVE_SPACE`, `DEPTH_ORDER`, and `TEXT_FIT`.

`SolvedCompositionPlanV1` contains IR and measurement refs, solver binding/policy/hash, ordered constraints, selected variant, all candidates where governed, `ConstraintResolution` for every constraint, final layer/region geometry, final text line placements, cue envelopes, objective facts, conflict sets, deterministic proof ref, and content hash. It does not contain an opaque score map. Each objective/result dimension is a typed record with profile source and evidence.

`ConstraintResolutionV1` decision is `SATISFIED_UNCHANGED`, `SATISFIED_MOVED_WITHIN_TOLERANCE`, `SATISFIED_SCALED_WITHIN_TOLERANCE`, `SATISFIED_WRAPPED`, `OMITTED_BY_APPLICABILITY_RULE`, or `BLOCKED`. Rewriting text, changing semantic role, weakening a lock, or moving outside tolerance is never a solver resolution.

### 6.6 Annotation contracts

`RoughAnnotationCueV1` requires cue ID, target layer/region and exact text grapheme range when applicable, cue type (`UNDERLINE`, `HIGHLIGHT`, `BOX`, `CIRCLE`, `STRIKE_THROUGH`, `CROSSED_OFF`, `BRACKET`, `ARROW`, `CONNECTOR`), semantic job ref, WHY ref, static/reveal mode, rational start/duration for timed previews, z-order, collision envelope, style registry ref, color, stroke width, padding, bracket side where applicable, deterministic path policy, seed value only when policy requires it, exact generated path ref/hash after compilation, required/optional applicability, Feature refs and locks.

`AnnotationPathCompilationReceiptV1` pins cue, target geometry/text measurement, compiler/version/hash, canonical seed derivation policy, exact vector path bytes/hash, collision findings and outcome. A seed alone is not path evidence. Annotation cannot be accepted when target text changed after measurement.

### 6.7 Render program, worker, and artifacts

`StaticRenderProgramV1` pins input manifest, Composition IR, measurement set, solved plan/selected variant, annotation cue/path set, every font/asset/mask/profile artifact, renderer binding, output slots, evaluation profile, locks, compatibility receipt, compilation command/receipt and predecessor. It is sealed by content hash.

`SkiaRuntimeBindingV1` contains worker protocol, adapter/runtime/binary/container IDs/versions/hashes, supported contract features, colorspace/font/image/annotation capabilities, deterministic claim enum, environment manifest, input/output schema hashes, execution limits, trust/signing state and compatibility receipt. The exact Skia embodiment is an infrastructure choice under the pinned registry, not semantic authority.

`StaticRenderAttemptV1` contains program, attempt ordinal, idempotency key, authorized worker, sealed request artifact/hash, expected output slots and dispatch receipt. `StaticArtifactManifestV1` contains attempt/program hashes; actual `ArtifactRef`s; media types; dimensions; colorspace; alpha; per-output role/profile; nonblank and decode facts; font/asset/cue coverage; renderer output receipt; and logs/metrics refs. Synthetic references, claimed hashes without bytes, or machine-absolute paths reject.

### 6.8 Reparse, evaluation, and decisions

`StaticReparseReceiptV1` records artifact/program refs; observed text hashes; observed regions/layers/hierarchy/reading path; collisions; protected/reserved/negative-space facts; asset/identity placement; annotation realization; output profile; differences from plan/intent; parser/version/hash; and evidence refs.

`StaticEvaluationReceiptV1` pins candidate, deterministic validators, independent evaluator/profile/model/runtime, per-dimension inputs/results/evidence, conflicts, missing evidence, and claim ceiling. Dimensions include exact text/source fidelity, semantic hierarchy, attention/reading path, BBOX function/WHY realization, Composition Intent, Feature Contracts, T/V effects where applicable, Visual DNA/identity, negative space/depth, annotation semantic job, locks, category/profile fit, and technical artifact integrity. Thresholds reside only in the pinned profile.

`NOT_APPLICABLE` is a typed result with rule/evidence; missing evidence is `NOT_EVALUATED_MISSING_REQUIRED_EVIDENCE`, never pass, zero, or N/A.

`StaticOperatorDecisionV1` pins artifact/reparse/evaluation hashes, attributable actor/authority, decision (`ACCEPT`, `REJECT`, `CONTEST`, `REQUEST_REVISION`), reasons/corrections, HumanResolutionEpisode ref, and expected version. Acceptance applies only to exact bytes and does not imply publication, certification, production eligibility, or later derivative acceptance.

### 6.9 Commands, events, and queries

| Command | Result |
|---|---|
| `AdmitStaticComposition` | Input manifest/admission receipt or typed denial |
| `AcknowledgeVaeAssetConsumption` | Exact consumption acknowledgement or conflict |
| `CompileStaticCompositionIr` | IR plus total field-coverage receipt |
| `MeasureStaticText` | Measurement set or typed font/text/adapter failure |
| `SolveStaticGeometry` | Solved plan/variants or minimal conflict set |
| `SelectSolvedStaticVariant` | Immutable selection receipt |
| `CompileRoughAnnotationPaths` | Cue/path artifacts and receipt |
| `CompileStaticRenderProgram` | Sealed program and compatibility receipt |
| `AuthorizeStaticRender` | Atomic attempt/outbox or denial |
| `IngestStaticArtifacts` | Actual content-addressed artifact set or stale/mismatch evidence |
| `ReparseStaticArtifacts` | Observed composition receipt |
| `EvaluateStaticArtifacts` | Deterministic and independent evaluation receipt |
| `RecordStaticOperatorDecision` | Exact decision/HumanResolution relation |
| `InvalidateStaticDependency` | Selective invalidation projection |
| `CancelStaticCommand` | Append-only cancellation and optional worker-cancel outbox |

Every mutating command includes command ID, idempotency scope/key, actor/authority, expected aggregate version, compatibility profile, canonical payload hash, causation/correlation IDs, and evidence-only issued time. Events include `StaticInputsAdmitted`, `VaeAssetConsumptionAcknowledged`, `StaticCompositionIrCompiled`, `StaticTextMeasured`, `StaticGeometrySolved`, `StaticVariantSelected`, `StaticAnnotationPathsCompiled`, `StaticRenderProgramCompiled`, `StaticRenderAuthorized`, `StaticRenderStarted`, `StaticArtifactsIngested`, `StaticRenderResultLate`, `StaticArtifactsReparsed`, `StaticArtifactsEvaluated`, `StaticOperatorDecisionRecorded`, `StaticRevisionRequested`, `StaticCompositionAccepted`, `StaticCompositionRejected`, `StaticCompositionCancelled`, `StaticCompositionSuperseded`, `StaticCompositionInvalidated`, and `StaticCompositionRevoked`.

Version-addressed queries are `GetStaticCase`, `GetStaticCompositionIr`, `GetTextMeasurementSet`, `GetSolvedCompositionPlan`, `GetStaticRenderProgram`, `GetStaticArtifactManifest`, `GetStaticReparseReceipt`, `GetStaticEvaluation`, `GetStaticDecision`, `GetStaticDependencyGraph`, and `GetStaticReplayBundle`. Exact historical queries never redirect to current.

### 6.10 Repository, compatibility, and migration invariants

One transaction stores aggregate/version, canonical bytes, command/idempotency, events/hash chain, receipts, dependencies/invalidation projection, outbox and current alias. IR without compilation/coverage receipt, measurement without exact request/font, plan without per-constraint resolutions, render program without selected plan, artifact manifest without actual bytes, evaluation without artifact/reparse, decision without evaluation, or outbox without committed attempt is corruption and cannot advance.

Compatibility is semantic feature negotiation, not parsing. Adapters emit field-by-field `AdapterCoverageReceipt`; required semantics cannot go to generic notes. Unknown required region functions, Features, locks, cues, profiles or extensions reject. Migration creates a new immutable version and receipt with source/target schemas, migrator hash, every field disposition, source/target hashes and validation. It never guesses function/WHY, source text, font, hierarchy, reading order, Composition Intent, Feature, profile, tolerance or locks. Required missing meaning yields `MIGRATION_BLOCKED_MISSING_SEMANTICS`; historical bytes remain intact.

## 7. Implementation stages and exact target paths

These are future paths only. This Prompt creates none.

```text
05_ATOMIC_HARNESS_PIPELINE/
  src/atomic_harness_pipeline/static_runtime/
    domain/{models,enums,invariants,events,failures}.py
    application/{commands,handlers,queries,ports,invalidation,replay}.py
    composition/{admission,coverage,ir_compiler,vae_geometry}.py
    typography/{contracts,pretext_adapter,measurement_validation}.py
    geometry/{constraints,solver,conflicts,determinism}.py
    annotation/{contracts,path_compiler,validation}.py
    rendering/{program,skia_worker,artifact_ingestion}.py
    evaluation/{reparse,deterministic,coordinator,decision}.py
    infrastructure/{persistence,outbox,object_store,delegation_adapter}.py
    api/{schemas,routes}.py
  tests/
    unit/static_runtime/
    contract/static_runtime/
    integration/static_runtime/
    replay/static_runtime/
    portability/static_runtime/
    architecture/static_runtime/
    fixtures/static_runtime/
```

| Stage/task | Exact future paths | FR/Story and evidence |
|---|---|---|
| 1. Closed domain primitives/IR | `domain/*`, `composition/ir_compiler.py`, unit/schema tests | FR-049/050, ST-05.01; schema, ownership and canonical hash |
| 2. Admission/AIR/VAE/lock coverage | `composition/admission.py`, `coverage.py`, `vae_geometry.py`, contract tests | FR-049/050, ST-05.01; total-coverage, consumption, lock receipts |
| 3. Final-font measurement | `typography/*`, unit/contract fixtures | FR-051; exact line/grapheme/bounds/overflow evidence |
| 4. Deterministic solver | `geometry/*`, property/integration tests | FR-052; collision, reading order, tolerance, determinism evidence |
| 5. Annotation compilation | `annotation/*`, unit/golden/negative fixtures | FR-053; cue/path hash and semantic-job evidence |
| 6. Skia program/worker/artifacts | `rendering/*`, infrastructure adapters, integration/portability tests | FR-054; sealed request and real artifact hashes |
| 7. Reparse/evaluation/decision | `evaluation/*`, integration/evaluation fixtures | All FRs; independent evidence and HumanResolution |
| 8. Persistence/replay/API | `application/*`, `infrastructure/*`, `api/*`, replay/architecture tests | ST-05.01; atomicity, recovery, exact history and boundary proof |

Import law: domain imports only standard library and approved shared primitives; application depends on domain/ports; composition/typography/geometry/annotation/rendering/evaluation depend inward; infrastructure alone imports storage, worker/provider or Delegation clients; API maps transport to commands and owns no decisions. Pipeline consumes externally owned versioned schemas/types and never forks AIR, Builder, VAE or Delegation authority locally. Architecture tests protect import/owner behavior rather than exact source strings.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Trigger | Owner/next action | Retry |
|---|---|---|---|
| `STATIC_INPUT_REF_UNRESOLVED` | Missing/hash-mismatched/stale exact ref | Supplying owner corrects ref | No |
| `STATIC_HARNESS_OR_PROFILE_INELIGIBLE` | Category/profile/capability not authorized | Builder/Pipeline registry | No |
| `STATIC_SEMANTIC_LINEAGE_INCOMPLETE` | AIR intent/narrative/Feature/transfer/DNA absent | AIR | No |
| `STATIC_VAE_RESULT_UNACCEPTED` | Asset result lacks exact VAE production acceptance | VAE | Wait/correct |
| `STATIC_VAE_RESULT_STALE` | Demand/result/version superseded or invalidated | VAE/Pipeline | No |
| `STATIC_GEOMETRY_AUTHORITY_CONFLICT` | Realized geometry exceeds upstream tolerance or changes function | AIR/VAE/upstream demand owner | No; amendment needed |
| `STATIC_LOCK_INHERITANCE_WEAKENED` | Child omits/weakens ancestor lock | Request producer | No |
| `STATIC_BBOX_FUNCTION_MISSING` | Geometry or function/WHY incomplete | AIR/Pipeline compiler input | No |
| `STATIC_TEXT_SOURCE_OR_TRANSFORM_INVALID` | Text bytes/provenance/Transformation Contract mismatch | Source/AIR owner | No |
| `STATIC_FONT_ARTIFACT_UNRESOLVED` | Font/hash/face/axes/features unavailable | Pipeline assets/operator | No |
| `STATIC_TEXT_MEASUREMENT_FAILED` | Adapter mismatch, missing glyph, invalid metrics | Pipeline typography adapter | Bounded same-input retry only for transport |
| `STATIC_TEXT_OVERFLOW_UNRESOLVED` | Final text cannot fit allowed constraints | AIR/operator amendment route | No automatic rewrite |
| `STATIC_CONSTRAINT_SET_UNSATISFIABLE` | Hard constraints conflict | Named source owners | No; return minimal conflict set |
| `STATIC_READING_ORDER_VIOLATION` | Solved order differs from governed path | Pipeline solver | No |
| `STATIC_ANNOTATION_UNGROUNDED` | Cue lacks semantic job/target/WHY | AIR/Pipeline input | No |
| `STATIC_ANNOTATION_COLLISION` | Cue covers protected evidence/text | Pipeline solver/annotation | Recompile affected cue |
| `STATIC_RENDERER_INCOMPATIBLE` | Worker lacks required schema/capability/profile | Pipeline operations | Alternate authorized binding |
| `STATIC_RENDER_DISPATCH_FAILED` | Outbox/transport/worker failure | Pipeline/Delegation | Bounded idempotent retry |
| `STATIC_ARTIFACT_BYTES_MISSING` | URI/hash claim without stored bytes | Worker/Pipeline | No acceptance |
| `STATIC_ARTIFACT_MISMATCH` | Count/type/dimensions/profile/hash/attempt differs | Worker adapter | New attempt if authorized |
| `STATIC_RENDER_RESULT_LATE` | Callback targets cancelled/stale version | Pipeline evidence store | Never canonicalize |
| `STATIC_REPARSE_CONFORMANCE_FAILED` | Artifact differs from plan/intent | Pipeline correction route | Repair/new version |
| `STATIC_EVALUATION_EVIDENCE_MISSING` | Required dimension absent | Evaluator/Pipeline | Retry evaluation only |
| `STATIC_EVALUATION_CONFLICT` | Mechanical and independent findings conflict | Operator/Studio | No automatic approval |
| `STATIC_IDEMPOTENCY_COLLISION` | Same key, changed canonical request | Caller/security | No |
| `STATIC_CONCURRENCY_CONFLICT` | Stale expected version | Caller | Reload/reissue |
| `STATIC_STORAGE_ATOMICITY_FAILURE` | Any success transaction participant fails | Pipeline operations | Full safe retry |
| `STATIC_DEPENDENCY_INVALIDATED` | Upstream dependency changed/revoked | Owning correction route | Recompute descendants only |
| `STATIC_REPLAY_ARTIFACT_MISSING` | Historical byte unavailable | Pipeline operations incident | No substitution |

### 8.2 Retry, rollback, cancellation, and partial result law

Transport retry may reuse an immutable request/attempt and idempotency key. Quality repair, changed inputs/font/solver/renderer/evaluator, or any semantic correction creates a new version/attempt. A transaction failure leaves no success-visible subset; staged orphan bytes remain unreachable until garbage collection. Failure receipts use a separate explicit failure transaction and cannot resemble success.

Partial multi-output renders may be stored as attempt evidence but are not a complete artifact set unless the exact output profile authorizes partial delivery and enumerates missing slots/restrictions. Partial delivery never waives required text, lock, protected-region, evaluation or disclosure evidence. Cancellation/supersession/invalidation/revocation are append-only; historical bytes are not deleted.

### 8.3 Selective invalidation and historical replay

Dependency edges cover source/text/Transformation Contract; AIR narrative/intent/Features/T-V/locks; Harness/profile; VAE demand/result/geometry; font/measurement adapter/result; constraint/solver; annotation/style/path; renderer/runtime/environment; artifact/reparse/evaluator/decision; and downstream acknowledgements. Traversal is exact and cycle-checked.

A changed font invalidates measurements and dependent layout/render descendants, not AIR intent. A changed VAE mask invalidates bound geometry and dependent layers, not unrelated text. A changed AIR reading path invalidates relevant IR/solve/render/evaluation. A revoked lock or source permission invalidates every descendant use. New current versions do not rewrite historical accepted attempts.

Offline replay resolves exact content-addressed bytes and events without current aliases, environment discovery, network, or new model calls. It proves decision history and evidence. A new renderer invocation is a new attempt and may only claim byte identity after explicit environment proof.

### 8.4 Observability and operations

Metrics cover admission denials by type, unacknowledged VAE assets, field coverage, measurement latency/failures/missing glyphs/overflow, solver conflicts/iterations with bounded limits, annotation failures, outbox lag, attempts/retries/late callbacks, artifact decode/hash failures, reparse deltas, evaluation completeness/conflicts, operator latency, invalidation fanout, replay completeness and repository invariant violations.

Logs/traces use case/program/attempt/command/correlation IDs and digests. They exclude raw private source text/assets, font/license secrets, credentials, machine paths and unredacted worker payloads. Alerts fire for missing artifact bytes, orphan state/receipt, outbox gap, stale callback, nonportable path, unauthorized geometry change, weakened lock, preview/final divergence and historical-byte loss.

Operational status separately reports specification, implementation, adapter availability, renderer connectivity, deterministic claim level, evaluation, operator acceptance, production authorization, publication and certification. No state implies another.

### 8.5 Security and portability

Technical security enforces authenticated actors, least privilege, immutable/signed/hash-pinned messages where governed, secret isolation, encryption, content hash verification, replay protection, sandboxed rendering/media/font parsing, resource limits and worker result authentication. Operator source authority and product sovereignty remain governing; this spec adds no generic creative-safety/content-rights approval authority.

Archive and path handling rejects absolute/drive/UNC paths, parent traversal, alternate data streams, devices, normalized/case-fold collisions, symlink/reparse escape and decompression bombs. Materialization remains inside an isolated job root. Manifests store relative logical paths or governed object IDs and content hashes, never host-specific roots.

## 9. Behavior-specific acceptance criteria

Each criterion is for later independent audit/implementation evidence, not acceptance in this prompt.

### AC-STA-001 — renderer-neutral IR completeness

**Given** an admitted static job, **when** IR compiles, **then** canvas, layers, assets, exact text, functional BBOXes, hierarchy, reading order, annotations, provenance and Transformation Contract are all typed and hash-pinned. Failure: a provider prompt substitutes for IR. Evidence: schema/coverage receipt. Layer: contract. Trace: FR-049, ST-05.01.

### AC-STA-002 — AIR ownership preserved

**Given** AIR Visual Narrative/Composition Intent/Features, **when** Pipeline compiles syntax, **then** every semantic field remains an exact AIR ref and no execution object rewrites meaning. Failure: solver changes primary hierarchy to fit. Evidence: before/after ownership map. Layer: architecture/integration. Trace: FR-049, ST-05.01.

### AC-STA-003 — BBOX plus function and WHY

**Given** any requested region, **when** accepted into IR, **then** normalized geometry, syntactic/attention function, semantic job and WHY ref are present. Failure: coordinates-only rectangle. Evidence: negative schema fixture. Layer: contract. Trace: FR-050, ST-05.01.

### AC-STA-004 — no inferred reading order

**Given** AIR reading path, **when** IR compiles, **then** exact ordered entries and reasons persist independently of z-order/coordinates. Failure: renderer sorts top-to-bottom. Evidence: order fixture. Layer: unit/contract. Trace: FR-049/050.

### AC-STA-005 — VAE role remains unchanged

**Given** accepted image-conditioned geometry, **when** Pipeline binds it, **then** requested versus realized geometry and tolerance are recorded without changing requested function. Failure: VAE recommendation moves witness image into decorative role. Evidence: geometry comparison/consumption receipt. Layer: cross-product integration. Trace: FR-050.

### AC-STA-006 — production acceptance is not consumption

**Given** VAE production acceptance, **when** Pipeline uses an asset, **then** a distinct exact consumption acknowledgement is required. Failure: acceptance automatically marks consumed. Evidence: lifecycle fixture. Layer: integration. Trace: FR-049/050.

### AC-STA-007 — exact final-font input

**Given** a text layer, **when** measurement runs, **then** exact text, font bytes/hash, face/axes/features, size/spacing/line policy/density and adapter binding are pinned. Failure: font family name only. Evidence: measurement request. Layer: contract. Trace: FR-051.

### AC-STA-008 — exact line-range evidence

**Given** final text/font conditions, **when** adapter returns, **then** grapheme/line ranges, substring hashes, widths, heights, baselines, logical/ink bounds and overflow evidence are exact. Failure: character-count width estimate. Evidence: measurement result/golden fixture. Layer: adapter contract. Trace: FR-051.

### AC-STA-009 — font fallback denial

**Given** a missing glyph/font, **when** fallback is unpinned or forbidden, **then** measurement/render blocks. Failure: machine font silently substituted. Evidence: clean-machine negative fixture. Layer: portability. Trace: FR-051.

### AC-STA-010 — overflow does not rewrite source

**Given** text overflow, **when** no upstream transformation authorizes editing, **then** the case returns `STATIC_TEXT_OVERFLOW_UNRESOLVED`. Failure: quote shortened automatically. Evidence: denial and unchanged source hash. Layer: integration. Trace: FR-051, ST-05.01 CBAR.

### AC-STA-011 — deterministic constraint resolution

**Given** identical immutable IR/measurements/profile, **when** solving runs in fresh processes with shuffled inputs/environment, **then** plan bytes/hash match. Failure: first dictionary entry wins. Evidence: cross-process property suite. Layer: determinism. Trace: FR-052.

### AC-STA-012 — protected regions outrank polish

**Given** face/hand/evidence/protected regions, **when** a locally attractive placement collides, **then** it is moved within tolerance or blocked before rendering. Failure: text overlays a participant face. Evidence: conflict/resolution receipt. Layer: solver integration. Trace: FR-052, ST-05.01 CBAR.

### AC-STA-013 — every collision is explained

**Given** a solver action, **when** plan emits, **then** every move/scale/wrap/omit/block has constraint, owner, before/after geometry and reason evidence. Failure: silent shrink. Evidence: complete resolution matrix. Layer: contract/integration. Trace: FR-052.

### AC-STA-014 — outside-tolerance conflict routes upstream

**Given** no solution within allowed variation, **when** solving ends, **then** a minimal conflict set and amendment route are returned without mutating intent. Failure: subject silently relocated. Evidence: typed conflict. Layer: integration. Trace: FR-050/052.

### AC-STA-015 — annotation is semantically grounded

**Given** an annotation request, **when** cue compiles, **then** target, semantic job, WHY, timing, path policy, style, Feature refs and locks are present. Failure: random underline for visual energy. Evidence: cue schema/negative fixture. Layer: contract. Trace: FR-053.

### AC-STA-016 — annotation path is deterministic

**Given** identical cue/target/style/policy, **when** path compiles twice, **then** exact vector path bytes/hash match; a seed alone is insufficient. Failure: process random changes underline. Evidence: path determinism suite. Layer: unit/property. Trace: FR-053.

### AC-STA-017 — annotation cannot cover evidence

**Given** cue envelope collides with protected evidence or changes reading order, **when** validation runs, **then** it blocks or uses governed optional omission. Failure: circle obscures quote attribution. Evidence: collision fixture. Layer: integration. Trace: FR-053, ST-05.01.

### AC-STA-018 — real Skia artifacts required

**Given** authorized render, **when** completion is claimed, **then** actual decodable bytes, recomputed hashes, dimensions, colorspace, roles and attempt identity exist. Failure: `skia://output/1` string with no bytes. Evidence: artifact manifest/object-store proof. Layer: worker integration. Trace: FR-054.

### AC-STA-019 — no browser screenshot fallback

**Given** Skia worker unavailable, **when** render is requested, **then** typed failure is returned and no browser screenshot is accepted as production artifact. Evidence: negative worker fixture. Layer: integration. Trace: FR-054.

### AC-STA-020 — sealed preview/final lineage

**Given** preview and final outputs, **when** compared, **then** each pins the intended selected plan/program/assets/fonts/cues/runtime and divergence is explicit. Failure: operator reviews one plan and final uses another. Evidence: program/artifact hash matrix. Layer: integration. Trace: FR-054.

### AC-STA-021 — wrong-reading locks are monotonic

**Given** a crop/size/static derivative with parent locks, **when** compiled, **then** every ancestor lock remains equal/stronger with portable evidence. Failure: crop drops identity-context lock. Evidence: inheritance validator. Layer: contract/property. Trace: FR-049/050, ST-05.01.

### AC-STA-022 — reparse checks pixels against intent

**Given** actual artifacts, **when** reparsed, **then** observed text, hierarchy, BBOX relations, reading path, collisions, cue realization, Features and locks compare to exact plan/AIR intent. Failure: correct manifest but reversed eye path. Evidence: reparse receipt. Layer: evaluation integration. Trace: all FRs.

### AC-STA-023 — no producer self-acceptance

**Given** compiler/solver/renderer output, **when** judgment is required, **then** a pinned independent evaluator and attributable operator decision are separate. Failure: renderer returns `approved=true`. Evidence: actor/receipt boundary test. Layer: architecture/security. Trace: ST-05.01.

### AC-STA-024 — atomic commit and no orphan records

**Given** injected failure at any repository write, **when** command runs, **then** no success-visible subset remains; bidirectional invariant scan finds no orphan artifact/receipt/command/event/outbox/dependency. Evidence: fault-injection suite. Layer: persistence. Trace: ST-05.01.

### AC-STA-025 — idempotency, concurrency, and late results

**Given** repeated identical command, changed-payload collision, stale expected version, cancellation race or late callback, **when** handled, **then** original response, typed collision/conflict, and noncanonical late evidence follow exact law with no duplicate dispatch. Evidence: concurrency suite. Layer: integration. Trace: ST-05.01.

### AC-STA-026 — selective invalidation

**Given** a changed text, font, mask, asset, cue, AIR intent, lock, renderer or evaluator, **when** invalidation runs, **then** only exact descendants stale and unrelated accepted work/history remains. Evidence: graph fanout tests. Layer: integration/replay. Trace: ST-05.01 selective recovery.

### AC-STA-027 — portable historical reproduction

**Given** invalidated/superseded accepted output, **when** offline replay is requested on another root, **then** exact evidence resolves without absolute paths/current aliases/network and does not mislabel a rerender as historical bytes. Evidence: clean extracted-layout replay. Layer: portability/replay. Trace: ST-05.01.

### AC-STA-028 — status claims remain separated

**Given** a written spec, available adapter, real artifact or accepted static result, **when** status projects, **then** build, production, publication, category certification and Format 02 remain separately false/unproven. Evidence: status projection test. Layer: governance. Trace: all FRs.

## 10. Testing and completion evidence

### 10.1 Exact future test anchors

| Path | Required cases |
|---|---|
| `tests/unit/static_runtime/test_composition_ir.py` | Closed fields, functional BBOX/WHY, hierarchy, reading order, cycles, canonical bytes |
| `tests/contract/static_runtime/test_air_visual_handoff.py` | Total AIR intent/Feature/T-V/lock preservation and owner boundaries |
| `tests/contract/static_runtime/test_vae_geometry_consumption.py` | Demand/result/acceptance/geometry/tolerance and separate acknowledgement |
| `tests/unit/static_runtime/test_text_measurement_contract.py` | Grapheme ranges, exact font config, missing glyph, overflow, direction, no unpinned fallback |
| `tests/contract/static_runtime/test_pretext_adapter.py` | Request/result/hash compatibility and final-font proof |
| `tests/unit/static_runtime/test_geometry_solver.py` | Constraint priorities, tie-breakers, minimal conflicts, every resolution, fixed point |
| `tests/unit/static_runtime/test_annotation_paths.py` | Typed targets/jobs/styles/timing/path hashes/collisions |
| `tests/contract/static_runtime/test_skia_worker.py` | Sealed request, capabilities, authenticated actual bytes, mismatch/late results |
| `tests/integration/static_runtime/test_static_reference_slice.py` | admit -> IR -> measure -> solve -> cue -> render -> reparse -> evaluate -> HumanResolution |
| `tests/integration/static_runtime/test_atomicity_concurrency.py` | fault points, optimistic concurrency, idempotency, cancellation, outbox |
| `tests/replay/static_runtime/test_selective_invalidation.py` | dependency-specific fanout and unrelated history preservation |
| `tests/replay/static_runtime/test_offline_historical_reproduction.py` | exact historical bundle without current aliases/network |
| `tests/portability/static_runtime/test_deterministic_fresh_context.py` | time/random/hash seed/locale/environment/cwd/order/path variation |
| `tests/portability/static_runtime/test_archive_and_path_safety.py` | traversal, drive/UNC, symlink/reparse, collision, bomb, no absolute path leakage |
| `tests/architecture/static_runtime/test_import_and_ownership_boundaries.py` | inward imports; no local AIR/Builder/VAE schema fork; no provider authority |

### 10.2 Fixture matrix

Positive fixtures cover: quote-led single image, SuperVisual, carousel slide and diagnostic plate; multilingual/directional text; multiple exact fonts/axes; protected face/hand/evidence zones; negative space; optional and required annotations; crop/size derivative with inherited locks; VAE geometry within tolerance; independent evaluation and HumanResolution.

Negative/adversarial fixtures cover: coordinates without function/WHY; flattened Composition Intent; missing Feature; ambiguous order; stale VAE result; production acceptance inferred as consumption; out-of-tolerance role change; missing parent lock; paraphrased quote; baked text; machine-font fallback; missing glyph; unresolved overflow; solver order dependence; protected-region collision; ungrounded annotation; seed without path; Skia URI without bytes; output mismatch; browser fallback; preview/final drift; missing evaluator dimension; producer self-approval; invalid N/A; absolute path; partial commit; orphan receipt; duplicate dispatch; concurrency race; late result; invalidation overreach; lossy migration; and unauthorized build/production/certification claim.

### 10.3 Determinism, portability, and performance evidence

Canonical compile/measure/solve/path/program/replay runs at least twice in fresh processes with varied current time, timezone, locale, random state, hash seed, mapping insertion, filesystem traversal, working directory and irrelevant environment. Exact deterministic objects must have byte-identical hashes. Worker output receives only the deterministic claim its pinned environment proves.

Artifact scans reject Windows drives/UNC, POSIX home/temp/workspace roots, usernames, hostnames, PIDs, unresolved environment expressions and timestamps used as semantic identity. Resource/latency/memory budgets and maximum solver/adapter/render work come from pinned profiles; this spec invents no thresholds. Budget exhaustion yields a typed incomplete/blocked result, never relaxed constraints.

### 10.4 Reference-slice evidence

The mandatory reference slice starts with one exact source-grounded `ContentDerivativeJob` and AIR Visual Activation Handoff containing Visual Narrative Program, semantic Composition Intent, functional BBOX/WHY, Feature Contracts, approved exact text, Visual DNA and locks. It binds one exact VAE production-accepted asset and separately acknowledges consumption; compiles Composition IR; measures exact text with an exact font; solves geometry; compiles an annotation; renders actual hash-addressed Skia artifacts; reparses; independently evaluates; records HumanResolution; selectively invalidates one text/font dependency; and reproduces both old and new evidence offline.

### 10.5 Later completion evidence and Build Receipt definition

A future implementation claim requires:

1. exact implemented-file/hash manifest and architecture boundary report;
2. FR-049..054/ST-05.01/AC/test trace matrix;
3. closed schema/generated-type/compatibility validation;
4. two fresh-process complete regressions and source compilation;
5. AIR field-coverage and authority-boundary receipts;
6. VAE geometry and separate consumption lifecycle evidence;
7. font/measurement adapter compatibility, line metrics and overflow evidence;
8. solver determinism, collision, reading-order and conflict evidence;
9. annotation cue/path determinism and protected-region evidence;
10. real Skia worker artifact bytes/hash/portability evidence;
11. reparse, independent evaluation and HumanResolution evidence;
12. atomicity, idempotency, concurrency, cancellation, invalidation and offline replay evidence;
13. security/archive/path/resource evidence;
14. no-orphan repository invariant report; and
15. independent audit, revision if required, re-audit, attributable ratification/acceptance and bounded Development Capsule at their later governed stages.

A later `StaticRuntimeBuildReceiptV1` would pin implementation commit/tree, source/dependency/toolchain/environment hashes, test/evidence refs, migrations, known limitations, authority/ratification/adoption receipts, claim ceiling and signer. This document does not issue it.

### 10.6 Current completion state

```yaml
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
implementation_created: false
canonical_schema_created: false
shared_release_created: false
development_capsule_created: false
production_authority: false
publication_authority: false
certification_claim: false
```

The next permitted action is independent audit under Prompt 04 by a different agent. A changed TS-AHP-003 or TS-AIR-017 hash reopens the six recorded revision-impact sections. Nothing here authorizes code, external source adoption, VAE Stage 5, Format 02, build, production, publication, or certification.
