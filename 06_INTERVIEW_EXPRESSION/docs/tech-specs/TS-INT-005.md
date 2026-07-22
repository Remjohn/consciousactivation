# TS-INT-005 — Expression Ingredient Inventory and Asset Package Spec

```yaml
spec_id: TS-INT-005
title: Expression Ingredient Inventory and Asset Package Spec
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Interview Expression
writing_wave: 8
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs:
  - FR-132
controlling_stories:
  - ST-02.04
upstream_drafts:
  - spec_id: TS-INT-004
    path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-004.md
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This candidate specification is authorized for technical writing and later independent review only. It creates no implementation, build, schema-release, contract-release, production, publication, certification, or Development Capsule authority. Interview Expression owns the approved human-source evidence and the compilation, approval, versioning, and handoff of the Expression Ingredient Inventory and Asset Package Spec. Activative Intelligence Runtime (AIR) owns downstream Primitive, archetype, brand, Voice DNA, Visual DNA, role-tension, Matrix, Edge Product, Final Script, Activation Transfer, and production-program meaning. An Asset Package Spec exposes source-backed ingredients, constraints, and possibilities; it does not decide the semantic program or authorize production.

## 1. Files and authorities read

### 1.1 Writer, dispatch, and claim-ceiling inputs

All digests are SHA-256 over the exact bytes read.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current one-spec writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_08_DISPATCH_LOCK.yaml` | 898 | `3d0b252c245e2f671b9b319afeb09893b4d89995ae506aa02b9097abf8a13797` | Wave 8 path and upstream lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact `CA-P03-WRITE-TS-INT-005-RECOVERY` packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate authority and acceptance ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-work-only authorization |

No `AGENTS.md` governs `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-005.md`. The recovery packet classifies the target as `DIRECT_PRODUCT_SPEC_PATH` and grants this writer only the exact specification path plus the five Program Control writer receipts.

### 1.2 Current constitutional and candidate ownership inputs

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current authority for source truth, human reaction, Expression Moments, lineage, wrong-reading constraints, and product sovereignty |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product boundary ledger |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate unique semantic-object ownership |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | 1,621 | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Intended Interview Expression root; implementation remains unauthorized |

The candidate ownership package remains `CANDIDATE_NOT_CURRENT`. It is admitted under the Prompt 02C specification-work authorization and cannot be cited as ratified current authority.

### 1.3 Reconciliation, requirements, Story, and assignment

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Canonical ID, title, owner, path, gate, and candidate disposition |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Exact `FR-132` requirement and evidence |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact FR/Story/owner/spec/source/claim trace |
| AHP bundle `prd/features/F22-activative-tags-expression-moments-keyframes-and-asset-package-spec.md` | 17,347 | `d93b5c4fb09d6ba3f35cf84a2206b1100fa457abf94acd384ca703dc4ca5cd6e` | `FR-132` context and downstream handoff boundary |
| AHP bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553 | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | `ST-02.04`, CBAR law, invalid path, recovery, and evidence obligations |
| AHP bundle `planning/spec_assignments/TS-INT-005.md` | 2,834 | `917811269b31bc640eb73d0bc0a8e65540761c8a76aba23d29778db161d74023` | Assignment brief only; not a full specification or write grant |
| AHP bundle `governance/CURRENT_WRITING_PROFILE.md` | 11,536 | `ba88c5572ae3f7571daac9991a0d325a20f491cb9c0ea7c3816deb3ff3d32956` | Source-first, CBAR, ownership, `NOT_APPLICABLE`, and claim-ceiling law |
| AHP bundle `sources/EXACT_SOURCE_REUSE_CROSSWALK.csv` | 21,449 | `c8c97f5d2003d070180a7061484609b2f9c8ef990efa116914f05b4e400e7820` | Brownfield reuse requires bounded review and explicit disposition |

`FR-132` requires approved quotes, evidence, Expression Moments, keyframes, voice/audio references, visual references, tags, archetype opportunities, restrictions, and lineage to be compiled into a package that downstream Atomic Harnesses consume without rediscovering the source. `ST-02.04` requires an exact source-backed ingredient package, rejects a quote without exact words and source time, and requires reconstruction of inputs, decisions, state transitions, handoff, selective recovery, and historical evidence.

### 1.4 Exact non-accepted upstream draft

| Draft | Bytes | SHA-256 | Exact interface consumed |
|---|---:|---|---|
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-004.md` | 99,774 | `e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a` | `WRITTEN_PENDING_AUDIT`; approved Expression Moments, tag assertions, Anchor Hit evidence, source-boundary evidence, negative evidence, AIR handoff separation, and selective invalidation |

This input is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Its exact hash and state are frozen by `WAVE_08_DISPATCH_LOCK.yaml`. A change to it reopens this specification's governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence. No text in this specification represents the draft as ratified, adopted, or accepted for build.

### 1.5 Required source evidence and dispositions

| Source | Bytes | SHA-256 | Current disposition and bound use |
|---|---:|---|---|
| AIR bundle `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; source-first interview expression, extraction before derivative work, and Asset Package predecessor |
| AIR bundle `sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | `REQUIRED_UNIQUE_EVIDENCE`; Complete Expression Session, route/package predecessor, source sufficiency, and gap preservation |
| `THE_CMF_STUDIO(2)/CCP V9.1 Expression Capture & Archetype Routing Update.md` (`SRC-INT-003`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | `REQUIRED_UNIQUE_EVIDENCE`; second registered occurrence with byte-identical content, retained as a provenance alias |

`SRC-AM-002` is `DEFERRED_REFERENCE`. Its named production-activation archive is unavailable at an active workspace path, it is not unique authority for `FR-132`, and this specification attributes no claim to it. `SOURCE_GAP_NOTICE.yaml` (17,743 bytes; `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886`) preserves the non-blocking gap. The current `SOURCE_DISPOSITION_LEDGER.yaml` is 134,201 bytes with digest `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3`.

### 1.6 Canonical-object and brownfield evidence

| File | Bytes | SHA-256 | Observed disposition |
|---|---:|---|---|
| AIR predecessor `sources/ai_v2_predecessor/06_CANONICAL_OBJECT_MODEL.md` | 1,483 | `18a6ffc82f8d980ee72ba05f99cff6eb8aea22aa0a2ed16f245cf2d51935872a` | `ADAPT`; names `ExpressionIngredientInventory` in the source-resolution plane and requires ID, version, hash, lifecycle, producer, authority, provenance, supersession, and invalidation |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/asset_program_compilers.py` | 28,865 | `b8f018ae42956618e2466465faeb33912824e005c5c7878fb266d7c985638ca3` | `ADAPT`; useful ingredient and relation vocabulary, but current shape flattens evidence and lacks approval/version law |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/asset_program_compiler_service.py` | 44,636 | `b4726def1d6917ab2dfc399972d89418e9ae2bcfc4f72bfe5d7612dd312f48fc` | `REPLACE_FOR_IE_AUTHORITY`; deterministic hashing is useful, but keyword-like coverage and automatic sequence assignment cannot establish source truth or AIR meaning |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/asset_package.py` | 6,358 | `b0d53412515a1d51842b621115a318552a6a8c2f45e29f75d2a6049a3a54b5d0` | `ADAPT`; package, item, gap, receipt, approval, and handoff vocabulary; fixed commercial counts are not current semantic law |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/asset_package_service.py` | 17,280 | `3625cd8386cc8b4114d26cf35ab24f97c790aea27e42855560cce37965556f84` | `ADAPT`; source-gap behavior and approval-before-handoff are useful; route-fit threshold, fixed counts, wall time, random IDs, and in-place replacement are noncanonical |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/asset_package.py` | 1,620 | `d41a6f54ae2e070acea09be3dade5d5ceed28eee4c1f349d29957e3d0eb77e7d` | `REPLACE`; independent in-memory dictionaries do not prove atomic artifacts, receipts, commands, versions, or dependencies |
| `THE_CMF_STUDIO(2)/src/ccp_studio/workflows/complete_expression_session.py` | 7,756 | `dc1588dc02daef62c9676a238d2e564b3ece31545af19f191b554022a4bb0484` | `ADAPT`; stage ordering evidence, not present authority |
| `THE_CMF_STUDIO(2)/src/ccp_studio/api/v1/asset_packages.py` | 2,216 | `e184f0248a65b7194828758cb21da19da52eda8e6cc1a09dea42e17e22ab7398` | `REPLACE`; command-oriented boundary must preserve version/hash/idempotency/authority context |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_guest_asset_pack_spec_generation.py` | 8,956 | `6a05d7c54272168dd0586af03a450298d58fb011ebd87c88d46b8da83e7fedf8` | `ADAPT`; source gaps, route lineage, approval, and handoff tests are useful; fixed offer/count claims are historical |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_complete_editing_session_creation_from_approved_source.py` | 10,898 | `767e09f3bdb2bda1e14436bdacc3f9d3151db602df7da3282607b25d6d1e2ab4` | `ADAPT`; approved source and locked-context handoff evidence, with current object and authority corrections |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_archetype_and_asset_derivative_routing.py` | 8,980 | `04d2dec22580098e6979e316b14b4490b761cd7f072a8da99cfb59d0c6ab0b15` | `ARCHIVE_AS_HEURISTIC`; preserves reject-instead-of-fabricate and lineage lessons, but repository-local archetype routing cannot own AIR semantic selection |

The intended `06_INTERVIEW_EXPRESSION` root currently contains specification artifacts, not a product implementation to modify. This writing pass creates no code, schema, validator, fixture, migration, release, test, or capsule.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

An approved Expression Moment is still too coarse for a downstream Harness to consume safely. A Harness may need an exact quote span, a wider context span, a clean or source-faithful audio interval, one or more admissible keyframes, visual continuity references, associated tag assertions, reaction evidence, restrictions, exclusions, and the evidence that connects them. If each derivative team rediscovers those elements, the source is repeatedly reinterpreted and the system can silently change the speaker, cut away a qualification, separate a reaction from its cause, choose a visually striking but misleading frame, present an inferred tag as observed fact, or turn a repository-local route suggestion into authoritative archetype meaning.

A weak package implementation can also:

- admit a quote without exact words, speaker, rational source time, and transcript revision;
- copy free-form `source_evidence_refs` while losing the typed evidence graph;
- declare a target derivative simply because a historical pack expected a fixed count;
- fill a missing item with generated content instead of recording a source gap;
- treat `archetype_opportunity` as an approved AIR archetype or Primitive decision;
- let a Hunter, router, model score, or package compiler approve its own proposal;
- mix selectable ingredients with rejected, superseded, revoked, or borderline evidence;
- call package approval production acceptance, consumption authorization, or certification;
- allow a downstream consumer to use “latest” instead of a pinned immutable package version;
- mutate a package after handoff, leaving its receipt and content hash inconsistent;
- lose the dependency edge from a derivative to the exact source package, Moment, frame, audio, and restriction versions;
- invalidate all historical packages when only one source span changes, or fail to invalidate affected descendants at all; or
- let Interview Expression compile AIR-owned semantic meaning or VAE-owned production choices.

These failures make downstream output unreproducible and can convert a human source into invented meaning while receipts still appear complete.

### 2.2 User and system outcome

An authorized Interview Expression operator can compile one immutable, reviewable package from approved source evidence. A downstream Builder/Harness can select only eligible ingredients and reconstruct their exact words, source time, speaker, audiovisual references, governing Expression Moment, tag provenance, restrictions, lineage, and package decision without reopening the original session. The downstream system acknowledges exactly which package version it consumed. Missing support becomes an explicit gap, not fabricated source. AIR receives evidence and possibilities while retaining exclusive authority to compile semantic meaning.

### 2.3 Bounded solution

Interview Expression SHALL provide two related immutable aggregates:

1. `ExpressionIngredientInventoryVersion`, the typed set of selectable source ingredients, explicit exclusions, typed evidence relations, gaps, restrictions, and completeness results derived from approved source objects; and
2. `AssetPackageSpecVersion`, a consumer-targeted projection that selects inventory entries and declares allowed uses, required upstream semantic dependencies, forbidden interpretations, applicability, and exact handoff rules without choosing final semantic or production programs.

Compilation SHALL be command-based, idempotent, optimistic-concurrency protected, source-snapshot pinned, canonically serialized, hashed, atomically persisted with command/event/decision receipts, and independently approved. Approval SHALL freeze a version. Any correction produces a new immutable version with explicit supersession and selective invalidation. Consumer acknowledgement SHALL never mutate or reinterpret the package.

### 2.4 In scope

- Typed ingredients for quotes, context passages, stories, claims, frameworks, reactions, audio selections, voice references, keyframes, visual references, visual seeds, and governed semantic-opportunity references.
- Exact evidence from approved Expression Moments and their source dependencies.
- Tag, Anchor Hit, Reaction Receipt, transcript/phrase/audio, shot/keyframe, source-package, consent/authority, and restriction references without ownership transfer.
- Ingredient relation graph: supports, contradicts, qualifies, precedes, follows, causes, reacts_to, frames, visually_depicts, visually_contrasts, same_source_continuity, requires_context, and mutually_exclusive.
- Package completeness, source sufficiency, eligibility, restriction propagation, exclusion, and evidence-bearing `NOT_APPLICABLE`.
- Typed archetype/Primitive/format/route opportunities that remain non-authoritative until compiled or adopted by their owning product.
- Draft, evaluated, review-required, approved, rejected, superseded, revoked, and invalidated package lifecycles.
- Approval authority, amendment authority, consumer acknowledgement, and the separation from production acceptance.
- Deterministic identity, hashing, atomic commit, idempotency, optimistic concurrency, replay, cancellation, correction, selective invalidation, and historical reproduction.
- Portability and redaction-safe projection without machine-specific absolute paths.
- Handoffs to Builder/Harness, AIR, Pipeline, Studio, VAE, and Delegation through their existing ownership boundaries.

### 2.5 Out of scope and non-goals

- Discovering, evaluating, approving, correcting, or owning Expression Moments and tag evidence (`TS-INT-004`).
- Transcription, diarization, phrase packing, audio-event discovery, shot detection, keyframe selection, visual-index creation, or Reaction Receipt compilation.
- AIR-owned Primitive/archetype/brand/Voice DNA/Visual DNA/role-tension/Matrix/Edge Product/Final Script/Activation Transfer/production-program compilation.
- Builder/Harness semantic intent, sequence role, asset role, Composition Intent, Visual Asset Demand, Feature Contract, or wrong-reading-lock authorship.
- Pipeline execution, scheduling, retrieval policy, evaluation policy, or worker routing.
- VAE Visual Production Plan, model/workflow/LoRA/conditioning choice, candidate generation, production evaluation, targeted repair, production acceptance, or delivery.
- Studio canonical mutation; Studio may project state and issue typed correction commands only.
- Delegation contract ownership, compatibility negotiation, transport, or shared failure-semantics release design.
- Fixed Guest Asset Pack counts, prices, offers, unsupported deliverable families, Format 02 activation, format certification, VAE Stage 5, or production authorization.
- Generic creative-safety/content-rights approval authority. Source authority, provenance, lineage, explicit operator approvals, and product sovereignty remain the governing controls; technical security remains operational.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty and object ownership

1. Interview Expression owns the source-facing `ExpressionIngredientInventoryVersion`, `AssetPackageSpecVersion`, package review/approval decisions, completeness results, gaps, exclusions, handoff receipts, and correction/supersession lifecycle.
2. `TS-INT-004` owns the source-backed Expression Moment, tag assertions, Anchor Hit evidence, negative evidence, and its approval lifecycle. This specification may only reference exact immutable versions and cannot promote or repair them.
3. The products that own transcript, audio, visual-index, keyframe, Reaction Receipt, and source-package records keep ownership. The package stores immutable refs, hashes, bounded excerpts where authorized, and verification facts; it does not fork those objects.
4. AIR exclusively owns semantic compilation. A package may carry `SemanticOpportunityRef` entries issued by AIR or explicitly labeled `NON_AUTHORITATIVE_CANDIDATE`, but Interview Expression cannot create an approved Primitive, archetype coalition, role-tension program, Matrix, Edge Product, Final Script, Activation Contract, Activation Transfer, Visual Semantic Pack, Visual Narrative Program, or Feature Contract.
5. Builder/Harness owns downstream semantic intent, source classification constraints, sequence role, asset role, Composition Intent, identity/continuity requirements, wrong-reading locks, Visual Asset Demand authority, and amendment authorization. It consumes package evidence rather than rediscovering it.
6. Pipeline consumes, validates, retrieves, executes, evaluates, and invalidates under pinned inputs. It does not rebuild package or AIR meaning.
7. VAE owns production realization after a valid Visual Asset Demand; package references do not authorize VAE to mutate upstream source or semantic authority.
8. Studio owns projection and typed correction workflows. Delegation owns transport and authority enforcement. Neither becomes package or semantic authority.

### 3.2 Inventory and package are distinct

The inventory is the complete governed set of eligible source ingredients and explicit noneligible evidence for one source snapshot. The package is a bounded consumer projection over that inventory. Therefore:

- one approved inventory may support multiple package specs for different consumers;
- a package item must reference an inventory item version, never copy free-form content without lineage;
- an inventory does not declare final derivative composition, ordering, meaning, or production route;
- a package may narrow eligibility or add stricter restrictions, but may not weaken source restrictions;
- package approval does not promote excluded inventory entries; and
- package completeness is evaluated against a declared package request, not historical fixed quotas.

### 3.3 Source truth is mandatory and typed

Every selectable ingredient SHALL bind:

- one source package/version/hash;
- one current approved Expression Moment/version/hash;
- the relevant exact source evidence: phrase/span, speaker, rational time interval, transcript revision, audio interval, frame/shot/keyframe, visual reference, Reaction Receipt, or other typed record;
- the authority and approval receipt that makes the ingredient eligible;
- all applicable restrictions and limitations; and
- a deterministic evidence-closure result.

A quote ingredient is invalid without exact words, speaker identity, rational start/end source time, transcript revision, and Expression Moment boundary. A keyframe ingredient is invalid without source artifact identity, frame index or rational presentation time, shot/index version, crop/transform metadata when applicable, and a statement of whether it is source-faithful or derivative. A voice/audio ingredient is invalid without source artifact/version, channel or track, rational interval, speaker binding, and permitted-use restriction. Generic notes never satisfy typed lineage.

### 3.4 Approval and proposal boundaries

Hunters, extractors, routers, and model-backed compilers may propose ingredients and gaps. They SHALL NOT approve their own proposals. The approving role SHALL be attributable, authorized for the source/brand/organization scope, and independent of the proposal decision when policy requires. Model confidence, route-fit score, keyword presence, historical template membership, and completeness score are evidence only. No numeric threshold invented by this spec grants truth or certification.

Package approval means: the package accurately represents the pinned source snapshot and is eligible for the declared downstream consumers under stated restrictions. It does not mean:

- AIR has accepted a semantic interpretation;
- Builder has declared a harness dependency;
- Pipeline has accepted execution;
- VAE has accepted production;
- a downstream consumer has acknowledged consumption;
- a format is certified;
- an asset is production accepted; or
- production/publication is authorized.

### 3.5 Semantic opportunities cannot become hidden authority

`archetype_opportunities` in `FR-132` SHALL be represented as typed `SemanticOpportunityRef` records with:

- `opportunity_kind`;
- owning authority (`AIR` or another named owner);
- exact referenced registry/object/version/hash when already governed;
- proposal provenance when not yet governed;
- `authority_state` (`AUTHORITATIVE_REFERENCE`, `NON_AUTHORITATIVE_CANDIDATE`, or `NOT_APPLICABLE`);
- supporting and contradicting ingredient refs;
- declared limitations; and
- downstream action (`CONSUME_REFERENCE`, `REQUEST_AIR_COMPILATION`, or `NO_ACTION`).

Interview Expression may say that evidence could support a future semantic route. It cannot say that the source *is* a Primitive, archetype, Matrix position, or Edge Product unless that statement is an exact reference to an AIR-owned approved version. Historical Studio archetype routes are predecessor heuristics and SHALL NOT be promoted into current AIR authority.

### 3.6 Restrictions, wrong-reading risks, and inheritance

The package SHALL preserve all source restrictions, approval scopes, consent constraints, identity constraints, epistemic limits, quote-context requirements, continuity constraints, and wrong-reading risks. A package or consumer may add stricter restrictions. It may not remove or weaken an inherited restriction.

When a Builder later creates a generative, composited, restyled, or semantically transformative Visual Asset Demand, Builder remains responsible for authoritative wrong-reading locks. The package supplies source-derived wrong-reading risks and restriction evidence; it does not author the final Visual Asset Demand. Deterministic/nonsemantic derivatives must preserve all inherited restrictions and must expose parent evidence. Relaxation requires a new authorized upstream source or demand version as applicable.

### 3.7 `NOT_APPLICABLE` is evidence-bearing

An optional ingredient class or package request dimension MAY be `NOT_APPLICABLE` only when the completeness result identifies:

- the exact rule/profile version evaluated;
- why the dimension does not apply to this source or consumer;
- the evidence refs supporting that decision;
- the deciding actor or deterministic rule;
- the decision receipt and timestamp as metadata; and
- whether a source or request change reopens applicability.

Missing evidence, evaluator failure, unsupported input, uncertainty, unavailable source bytes, or an inconvenient gap SHALL NOT be encoded as `NOT_APPLICABLE`.

### 3.8 Determinism, canonicalization, and portability

Canonical object identity and content hashes SHALL depend only on normalized semantic content and pinned input identities. They SHALL NOT depend on current time, random UUID generation, dictionary insertion order, filesystem traversal order, absolute machine paths, locale, process environment, host name, temporary directory, database row order, or model sampling state.

Normative rules:

- UTF-8; Unicode normalization form NFC; LF line endings for canonical text;
- JSON object keys sorted by Unicode code point after normalization;
- arrays sorted only when the contract declares them set-like; sequence-bearing arrays preserve explicit order with stable ordinal fields;
- timestamps excluded from content-derived IDs and retained as receipt metadata;
- time intervals represented as reduced rational values in the source timebase, not binary floats;
- hashes represented as lowercase hexadecimal SHA-256 with an algorithm field;
- repository-relative logical artifact locators, content-addressed URIs, or governed object refs only; no absolute paths;
- explicit `null`, absent, empty, and `NOT_APPLICABLE` semantics; and
- stable deterministic IDs formed from object type, governing scope, parent/version inputs, and canonical payload hash.

### 3.9 Immutability, versioning, and claim ceiling

An approved inventory or package version is immutable. Any content change creates a new version with a new content hash and explicit predecessor relation. Metadata-only receipt annotations that do not change semantic content SHALL be stored separately and cannot rewrite the artifact bytes.

All candidate-authority-controlled objects and this specification remain `CANDIDATE_NOT_CURRENT`. Specification work is authorized, implementation/build is not. Before ratification, the maximum later quality state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; `ACCEPTED_FOR_BUILD` and Development Capsules are prohibited.

## 4. Current brownfield architecture

### 4.1 Target product state

`06_INTERVIEW_EXPRESSION` currently has no authorized implementation tree for this capability. It contains candidate specifications. There is therefore no current Interview Expression package service, repository, schema, API, migration, or test suite to preserve. Section 7 names future paths only; it does not create or authorize them.

### 4.2 AIR predecessor object model

The AIR predecessor canonical-object document places `ExpressionIngredientInventory` in the source-resolution plane and requires stable ID, version, hash, lifecycle, producer, authority, provenance, supersession, and invalidation relationships. This is directionally compatible with `FR-132`. It does not define the full package contents, approval boundary, exact source evidence, failure semantics, or current ownership split and is therefore adapted rather than copied.

### 4.3 Studio expression-inventory predecessor

The Studio predecessor defines:

- `ExpressionIngredient` with a type, free-form source evidence refs, optional transcript span, and guest truth claim;
- `ExpressionRelationEdge` with five relation types;
- `ExpressionIngredientInventory` with ingredients, relation edges, blockers, and deterministic input hash; and
- a compiler that blocks only when a source-evidence list is empty.

Useful retained concepts are typed ingredients, relation edges, a blocker set, and deterministic hashing. The current canonical design must replace:

- free-form refs with typed version/hash evidence;
- unversioned inventory identity with immutable versioned identity;
- a single empty-list test with evidence closure and eligibility evaluation;
- caller-supplied `guest_truth_claim` with source-backed quote/claim objects and operator approval;
- automatic sequence slot and target compiler selection with owner-specific downstream compilation; and
- repository-local “approved” decisions with attributable product authority.

### 4.4 Studio Asset Package predecessor

The Studio predecessor provides useful concepts: package items, explicit package gaps, reaction seeds, package receipt, approval state, approval-before-editing handoff, source route lineage, and reject-instead-of-fabricate behavior. Its fixed trial pack counts, offer/pricing fields, route-fit threshold, registry-owned archetype routing, wall-clock identity, random UUIDs, mutable `put_spec` replacement, and independent in-memory dictionaries are not current law.

In particular, `TARGET_TRIAL_GUEST_PACK_COUNTS` is historical product behavior, not a current requirement of `FR-132`. This specification neither preserves nor rejects those counts for a future commercial product; it simply does not make them canonical. Any future count belongs in a separately governed package request/profile owned by the appropriate product and must not convert a source gap into fabricated material.

### 4.5 Brownfield test lessons

The predecessor tests establish several valuable behavioral intentions:

- unsupported source creates a gap rather than a fabricated item;
- ready items retain Moment, route, registry, evaluation, and source lineage;
- package approval precedes downstream editing-session request preparation;
- a route lacking source support is rejected;
- historical package and downstream session references can be queried; and
- command execution writes a receipt/event.

They do not prove current authority, atomic persistence, deterministic identity, version pinning, semantic-owner boundaries, source-restriction inheritance, selective invalidation, or historical reproduction. Those become explicit here.

### 4.6 Reuse boundary

No brownfield bytes are copied into a current implementation by this spec. Future implementation MAY adapt vocabulary and test scenarios only after independent audit and authorized build work. Any adapter from historical `cmf.expression_ingredient_inventory.v1` or `cmf.asset_package_spec.v1` must be explicit, lossless for required semantics, and blocked when source classification, source time, approval, restriction, or version identity cannot be recovered without guessing.

## 5. Proposed architecture and workflows

### 5.1 Components and ports

The future product boundary SHALL contain these logical components:

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `SourceSnapshotResolver` | Resolve exact current/pinned source package, Moment, transcript/audio/visual/Reaction evidence and hashes | Query “latest” after the command snapshot is frozen; reconstruct missing meaning |
| `IngredientCandidateCompiler` | Propose typed candidates and relation edges from admitted evidence | Approve candidates; compile AIR meaning |
| `IngredientEvidenceValidator` | Verify referential closure, exact source time, speaker/frame/audio identity, restrictions, and admissibility | Repair upstream source objects |
| `InventoryCompletenessEvaluator` | Evaluate request/profile applicability, eligible coverage, gaps, exclusions, and `NOT_APPLICABLE` evidence | Invent thresholds, fabricate missing ingredients, declare certification |
| `InventoryReviewService` | Record review-required, approval, rejection, correction, supersession, and revocation decisions | Self-approve model proposals |
| `AssetPackageCompiler` | Project approved inventory entries into a consumer-scoped package request | Decide final semantic sequence, composition, Visual Asset Demand, or production route |
| `PackageApprovalService` | Approve immutable package accuracy and declared eligibility | Grant downstream consumption or production acceptance |
| `PackageHandoffService` | Emit exact package manifest and handoff receipt; capture downstream acknowledgement separately | Mutate package after handoff |
| `PackageDependencyGraph` | Record inputs/descendants, impact classes, supersession, invalidation, and replay closure | Cascade invalidation without typed reasons |
| `PackageUnitOfWork` | Atomically commit aggregate, decision, receipt, command record, event, outbox, and dependencies | Store artifacts or receipts independently |
| `CanonicalSerializer` | Normalize and hash portable bytes | Include current time, absolute paths, random state, or environment in semantic hash |

Required external ports are read-only source evidence, authority policy, actor/organization/brand scope, durable aggregate/event/receipt storage, idempotency store, dependency graph, outbox, clock for receipt metadata only, and an optional deterministic evaluator registry. AIR, Builder, Pipeline, Studio, VAE, and Delegation adapters are outbound handoff consumers, not internal semantic authorities.

### 5.2 Compile an inventory candidate

`CompileExpressionIngredientInventory` SHALL include:

- command ID and idempotency key;
- organization, brand, source session, and source package scopes;
- expected aggregate version when the aggregate exists;
- exact Expression Moment version refs;
- exact evidence snapshot manifest/hash;
- inventory request/profile ID/version/hash;
- requested ingredient classes and consumer intents;
- actor identity, roles, and delegated authority refs;
- cancellation token/ref; and
- optional prior inventory version to amend.

The service SHALL:

1. authorize the actor and scope;
2. resolve every input by exact version/hash;
3. reject superseded, revoked, invalidated, or unapproved required Moment versions unless a historical replay command explicitly pins them;
4. build candidates without changing upstream bytes;
5. validate exact evidence closure and inherited restrictions;
6. compute relation edges only from typed evidence or attributable proposals;
7. classify each candidate as `ELIGIBLE`, `REVIEW_REQUIRED`, `EXCLUDED`, or `BLOCKED` with typed reasons;
8. compute completeness, gaps, exclusions, and `NOT_APPLICABLE` decisions;
9. canonically serialize and derive ID/version/hash;
10. atomically store inventory candidate, decision receipt, command record, event, dependency edges, and outbox entry; and
11. return the exact stored version/hash and receipt.

Compilation may finish `REVIEW_REQUIRED` or `BLOCKED_WITH_GAPS`; those are valid truthful outcomes. It SHALL NOT silently return a smaller “complete” inventory.

### 5.3 Review and approve inventory entries

Review SHALL operate on a pinned inventory candidate and expected version. The reviewer can:

- approve eligible candidate entries;
- reject an entry with typed rationale;
- mark it borderline/review-required;
- request upstream evidence correction;
- split an entry while preserving parent evidence;
- merge entries while retaining all parent evidence and ordering;
- narrow an allowed-use scope;
- add stricter restrictions;
- confirm a proposal-only semantic opportunity remains non-authoritative; or
- mark an optional class `NOT_APPLICABLE` with evidence.

Review cannot edit the source quote, source time, speaker, source frame, Reaction Receipt, approved Moment, or AIR-owned semantic ref. A requested correction creates a typed upstream correction request and leaves the package blocked or review-required. Approval creates a new immutable `APPROVED` inventory version and approval receipt. The proposal version remains reproducible.

### 5.4 Compile a consumer-scoped Asset Package Spec

`CompileAssetPackageSpec` SHALL pin:

- one approved inventory version/hash;
- a package request/profile ID/version/hash;
- intended consumer product and bounded use;
- requested ingredient roles/classes;
- required/optional applicability rules;
- any exact downstream semantic dependency declarations supplied by their owner;
- additional restrictions, never weaker ones;
- portability/redaction projection policy; and
- expected package aggregate version.

The compiler SHALL select only eligible approved entries, preserve all inherited evidence/restrictions, record excluded candidates and gaps by reference, and emit `PackageSlot` records. A slot means “this source ingredient may be considered for this declared use”; it is not a final semantic role, sequence slot, composition decision, format route, or production job. If the request needs a semantic choice not already supplied by AIR or Builder, the slot SHALL carry `OWNER_DECISION_REQUIRED` and the package cannot claim that dimension complete.

### 5.5 Evaluate package completeness and source sufficiency

Completeness SHALL be rule-based under a pinned profile. Each requirement produces one of:

- `SATISFIED` with exact ingredient/evidence refs;
- `NOT_APPLICABLE` with evidence and rule;
- `SOURCE_GAP` with missing source condition;
- `OWNER_DECISION_REQUIRED` with owning product;
- `REVIEW_REQUIRED` with unresolved evidence conflict;
- `UPSTREAM_INVALID` with invalid/superseded dependency; or
- `EVALUATOR_UNAVAILABLE` with no false pass.

The aggregate readiness is derived without invented numeric thresholds:

- `READY_FOR_IE_APPROVAL` only when all required dimensions are `SATISFIED` or valid `NOT_APPLICABLE`;
- `SOURCE_GAPS_RECORDED` when missing source prevents one or more requested items;
- `OWNER_DECISION_PENDING` when AIR/Builder or another owner must decide meaning;
- `REVIEW_REQUIRED` for resolvable evidence conflict; and
- `BLOCKED` for invalid authority, provenance, version, restriction, or dependency state.

### 5.6 Approve and hand off a package

Approval SHALL verify:

- package bytes/hash match the reviewed candidate;
- all required inputs are exact and current for the command snapshot;
- all selectable entries are approved and eligible;
- all restrictions and source limitations are inherited;
- all required gaps/owner decisions are resolved or explicitly outside the package's declared applicability;
- the actor has package-approval authority; and
- the approval is not self-approval where segregation policy applies.

The approval transaction creates an immutable approved version, package approval receipt, event, command record, dependency edges, and outbox entry atomically.

`PublishAssetPackageHandoff` creates a portable manifest containing exact object refs, versions, hashes, source-relative/content-addressed locators, schema/profile identifiers, restrictions, gap/exclusion summaries, compatibility declarations, and the package approval receipt. It does not copy mutable “latest” objects. `AcknowledgeAssetPackageConsumption` records the consumer, package version/hash, consumer purpose, accepted/rejected result, and reason. Acknowledgement is a separate receipt and does not change package approval or duplicate source evaluation.

### 5.7 Downstream ownership handoffs

| Consumer | Receives | May do | Must not do |
|---|---|---|---|
| AIR | Approved source ingredients, evidence graph, source limitations, non-authoritative opportunity candidates | Compile owned semantic objects and emit their own versions/receipts | Treat IE candidate opportunities as approved AIR meaning; mutate IE evidence |
| Builder/Harness | Package slots, source class/evidence, exact restrictions, semantic refs after owner approval | Declare dependencies and compile target semantic intent/sequence/asset/composition authority | Rediscover source, alter quote/context, implement VAE production choices |
| Pipeline | Exact package and downstream contract refs | Validate, retrieve, execute, evaluate, and invalidate | Rebuild semantic meaning or weaken constraints |
| Studio | Read model and correction-command affordances | Project state; request typed correction; capture HumanResolution | Directly rewrite package or source truth |
| VAE | Only the package refs embedded in a valid upstream Visual Asset Demand | Use them as immutable evidence while realizing visuals | Treat package approval as production acceptance or change upstream semantics |
| Delegation | Validated envelope and immutable refs | Transport, negotiate compatibility, route, and receipt | Become creative/source authority or alter package bytes |

### 5.8 Correction, amendment, supersession, and selective invalidation

Corrections SHALL never mutate approved bytes. An authorized correction command references the affected inventory/package version, exact evidence change, reason, actor, and expected version. It creates a new candidate version. Approval creates a successor and marks the predecessor `SUPERSEDED` for current consumption while retaining historical replay.

Dependency edges SHALL carry an impact class:

- `CONTENT_IDENTITY`: any change necessarily invalidates the descendant;
- `BOUNDARY_OR_TIMING`: invalidate only descendants using the changed span/frame/audio region;
- `AUTHORITY_OR_RESTRICTION`: invalidate descendants whose use is no longer authorized;
- `SEMANTIC_OPPORTUNITY`: notify/re-evaluate only descendants that consumed the changed opportunity ref;
- `PRESENTATION_ONLY`: no semantic invalidation unless a consumer declared it identity-bearing; and
- `METADATA_ONLY`: no content invalidation.

Invalidation SHALL traverse exact dependency edges from the changed version and affect only descendants whose recorded impact rule matches. Historical artifacts stay readable with their original dependency closure and invalidation receipt. A revoked source authorization blocks new consumption and marks affected current descendants unusable; it does not erase evidence needed for audit.

### 5.9 State machines

Inventory lifecycle:

```text
PROPOSED -> EVIDENCE_VALIDATING -> REVIEW_REQUIRED -> APPROVED
                  |                     |              |
                  +-> BLOCKED_WITH_GAPS +-> REJECTED   +-> SUPERSEDED
                                                        +-> REVOKED
                                                        +-> INVALIDATED
```

Package lifecycle:

```text
DRAFT -> EVALUATED -> READY_FOR_IE_APPROVAL -> APPROVED -> HANDED_OFF
  |          |                  |                  |          |
  |          +-> SOURCE_GAPS_RECORDED              |          +-> ACKNOWLEDGED
  |          +-> OWNER_DECISION_PENDING             |          +-> CONSUMER_REJECTED
  |          +-> REVIEW_REQUIRED                    +-> SUPERSEDED / REVOKED / INVALIDATED
  +-> CANCELLED
```

`HANDED_OFF` and `ACKNOWLEDGED` do not imply production acceptance. A package can remain approved while one consumer rejects it for an incompatible profile. Consumer rejection creates a new receipt, not a package mutation.

### 5.10 Atomicity, idempotency, concurrency, replay, and cancellation

Every mutating command SHALL run in one unit of work. Commit succeeds only if the aggregate/version, command record, decision/approval receipt, event, dependency edges, idempotency result, and outbox entry all persist. Any failure rolls back all of them. State without a receipt and a receipt without its artifact are corruption conditions.

An idempotency key is scoped by organization, brand, command type, aggregate, and actor/delegation. Replay with the same key and same canonical request hash returns the original result. The same key with different bytes fails `IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST`. Expected-version mismatch fails before semantic work commits. Concurrent approvals cannot both succeed.

Cancellation before commit produces a cancellation receipt and no artifact transition. Cancellation after commit cannot erase success; it becomes a new supersession/revocation request. Historical replay uses exact versions/hashes and a recorded evaluator/model/profile identity. If required bytes are unavailable, replay fails explicitly; it never substitutes a newer object.

## 6. Data models, contracts, schemas, and APIs

The models below are implementation requirements for a future authorized build. They do not publish canonical schema bytes in this writing pass.

### 6.1 Common value objects and enumerations

Every top-level artifact SHALL contain:

| Field | Required meaning |
|---|---|
| `object_id` | Stable content-derived logical identity |
| `version` | Positive immutable version within the logical identity |
| `schema_id` / `schema_version` | Exact governed contract identity |
| `content_hash` | SHA-256 of canonical semantic payload |
| `authority_owner` | Product that owns the artifact meaning |
| `organization_id`, `brand_id` | Explicit tenant/brand scope where applicable |
| `source_snapshot_hash` | Digest of exact admitted upstream identities |
| `producer` | Service/program identity and version |
| `lifecycle_state` | Typed state from the appropriate state machine |
| `predecessor_ref` | Prior version when amended/superseded |
| `supersession_refs`, `invalidation_refs` | Explicit lifecycle relations |
| `created_by_receipt_ref` | Attributable creation decision |

Normative enums:

```text
IngredientKind =
  EXACT_QUOTE | CONTEXT_PASSAGE | STORY | SOURCE_CLAIM | FRAMEWORK_EXPRESSION |
  REACTION_EXCERPT | AUDIO_SELECTION | VOICE_REFERENCE | KEYFRAME |
  VISUAL_REFERENCE | VISUAL_SEED | SEMANTIC_OPPORTUNITY_REFERENCE

IngredientEligibility = ELIGIBLE | REVIEW_REQUIRED | EXCLUDED | BLOCKED

EvidenceRole =
  PRIMARY_SOURCE | CONTEXT | QUALIFICATION | CONTRADICTION | REACTION |
  AUDIO_SUPPORT | VISUAL_SUPPORT | AUTHORITY | APPROVAL | RESTRICTION | LIMITATION

RelationKind =
  SUPPORTS | CONTRADICTS | QUALIFIES | PRECEDES | FOLLOWS | CAUSES | REACTS_TO |
  FRAMES | VISUALLY_DEPICTS | VISUALLY_CONTRASTS | SAME_SOURCE_CONTINUITY |
  REQUIRES_CONTEXT | MUTUALLY_EXCLUSIVE

ApplicabilityDecision = SATISFIED | NOT_APPLICABLE | SOURCE_GAP |
  OWNER_DECISION_REQUIRED | REVIEW_REQUIRED | UPSTREAM_INVALID | EVALUATOR_UNAVAILABLE

SemanticOpportunityAuthority =
  AUTHORITATIVE_REFERENCE | NON_AUTHORITATIVE_CANDIDATE | NOT_APPLICABLE

PackageLifecycleState =
  DRAFT | EVALUATED | SOURCE_GAPS_RECORDED | OWNER_DECISION_PENDING |
  REVIEW_REQUIRED | READY_FOR_IE_APPROVAL | APPROVED | HANDED_OFF |
  ACKNOWLEDGED | CONSUMER_REJECTED | CANCELLED | SUPERSEDED | REVOKED | INVALIDATED
```

IDs and hashes SHALL be references, not opaque free-form strings where a governed object exists. `NOT_APPLICABLE` SHALL be a decision record, not an enum value placed in an arbitrary nullable field.

### 6.2 `EvidencePointer`

```yaml
EvidencePointer:
  evidence_pointer_id: content-derived-id
  evidence_kind: TRANSCRIPT_SPAN | PHRASE | AUDIO_INTERVAL | SHOT | FRAME | KEYFRAME |
    VISUAL_REFERENCE | EXPRESSION_MOMENT | TAG_ASSERTION | ANCHOR_HIT |
    REACTION_RECEIPT | SOURCE_PACKAGE | APPROVAL_RECEIPT | AUTHORITY_RECORD |
    RESTRICTION_RECORD | OTHER_GOVERNED_OBJECT
  object_ref:
    object_id: string
    version: integer
    content_hash: sha256
    schema_id: string
    schema_version: string
    authority_owner: string
  role: EvidenceRole
  source_artifact_ref: optional exact object ref
  source_time:
    start_numerator: integer
    end_numerator: integer
    timebase_denominator: positive integer
  speaker_ref: optional exact identity ref
  channel_ref: optional string
  frame_index: optional nonnegative integer
  transform_ref: optional exact transform/crop ref
  bounded_excerpt: optional authorized source-faithful text
  source_faithful: boolean
  limitations: [string]
  restriction_refs: [exact object ref]
```

Validation law:

- `start < end`, after rational normalization, for non-point intervals;
- source time must be in the referenced artifact timebase and inside the governing Expression Moment boundary;
- quotes require transcript/phrase evidence, exact speaker, exact words, and source time;
- audio requires source artifact, track/channel, interval, and speaker binding;
- keyframes require source artifact, shot/index version, frame or rational time, and transform identity;
- a derived image can be a visual reference only if its derivation and parent source are explicit;
- an excerpt cannot be normalized into different words; display normalization metadata is separate;
- every restriction ref must resolve, or the ingredient is blocked; and
- no absolute local path may appear in a canonical pointer.

### 6.3 `ExpressionIngredientCandidate` and `ExpressionIngredientVersion`

```yaml
ExpressionIngredientCandidate:
  candidate_id: content-derived-id
  kind: IngredientKind
  governing_expression_moment_ref: exact approved version/hash
  primary_evidence: [EvidencePointer]
  contextual_evidence: [EvidencePointer]
  contradicting_evidence: [EvidencePointer]
  tag_assertion_refs: [exact refs]
  anchor_hit_refs: [exact refs]
  reaction_receipt_refs: [exact refs]
  source_package_ref: exact ref
  source_kind: interview_expression
  proposed_display_value: optional source-faithful projection
  proposed_by:
    actor_or_program_ref: string
    program_version: optional string
    proposal_receipt_ref: exact ref
  epistemic_state: PROPOSED
  declared_limitations: [string]
  inherited_restriction_refs: [exact refs]
  source_wrong_reading_risks: [typed risk]
  candidate_semantic_opportunity_refs: [SemanticOpportunityRef]
```

```yaml
ExpressionIngredientVersion:
  ingredient_id: stable content-derived-id
  version: integer
  content_hash: sha256
  kind: IngredientKind
  governing_expression_moment_ref: exact approved version/hash
  evidence_graph_ref: exact graph/version/hash
  approved_display_projection: optional source-faithful projection
  eligibility: IngredientEligibility
  eligibility_reason_codes: [typed code]
  applicable_use_classes: [typed use]
  prohibited_use_classes: [typed use]
  inherited_restriction_refs: [exact refs]
  added_restriction_refs: [exact refs]
  source_wrong_reading_risks: [typed risk]
  semantic_opportunity_refs: [SemanticOpportunityRef]
  decision_receipt_ref: exact ref
  lifecycle_state: APPROVED | REJECTED | SUPERSEDED | REVOKED | INVALIDATED
  predecessor_ref: optional exact ingredient version
  supersession_refs: [exact refs]
  invalidation_refs: [exact refs]
```

`approved_display_projection` is a display convenience only. The evidence pointers are canonical truth. For an exact quote, display text SHALL byte-equivalently represent the approved normalized source words under the declared transcript normalization policy. For a story, claim, or framework expression, any summary SHALL be labeled as a non-source paraphrase and cannot substitute for exact supporting spans.

### 6.4 Ingredient-specific requirements

| Kind | Additional mandatory evidence | Invalid conditions |
|---|---|---|
| `EXACT_QUOTE` | Exact phrase/span, speaker, source time, transcript revision, Moment boundary, context/qualification span when required | Missing exact words/time/speaker; quote crosses excluded span; qualifier omitted |
| `CONTEXT_PASSAGE` | Ordered spans and continuity relation | Unordered excerpts; discontinuity hidden |
| `STORY` | Source-backed constituent spans, order, premise/turn/release evidence, declared gaps | Generated bridge represented as source; timeline reordered without explicit projection |
| `SOURCE_CLAIM` | Exact claim span, speaker, epistemic qualifier, supporting/contradicting context | Paraphrase presented as exact quote; uncertainty removed |
| `FRAMEWORK_EXPRESSION` | Exact named/structured framework evidence and limitations | AIR semantic model inferred without owner decision |
| `REACTION_EXCERPT` | Reaction Receipt and exact cause/outcome/observation refs | Reaction separated from causal source or exceeds receipt maximum claim |
| `AUDIO_SELECTION` | Source recording/version, track/channel, interval, speaker, quality/limitations | Rendered mix substituted for source without lineage |
| `VOICE_REFERENCE` | Source audio, speaker identity, consent/allowed-use scope, quality caveats | Implied synthesis/training permission; unknown identity or rights scope |
| `KEYFRAME` | Shot/index version, frame/time, source artifact, crop/transform, technical quality | Visual salience treated as semantic truth; machine path stored |
| `VISUAL_REFERENCE` | Source or derivative lineage, frame/asset hash, declared use, identity/continuity limits | Derivative parent missing; visual changes source meaning |
| `VISUAL_SEED` | Source-backed visual cue and exact evidence; non-authoritative label | Production prompt or composition decision authored by IE |
| `SEMANTIC_OPPORTUNITY_REFERENCE` | `SemanticOpportunityRef` and evidence graph | Repository-local suggestion presented as approved AIR meaning |

### 6.5 `SemanticOpportunityRef`

```yaml
SemanticOpportunityRef:
  opportunity_ref_id: content-derived-id
  opportunity_kind: PRIMITIVE | ARCHETYPE | ROLE_TENSION | MATRIX_POSITION |
    EDGE_PRODUCT | ACTIVATIVE_CALL | FORMAT | ASSET_FAMILY | OTHER_OWNER_OBJECT
  authority_state: AUTHORITATIVE_REFERENCE | NON_AUTHORITATIVE_CANDIDATE | NOT_APPLICABLE
  authority_owner: AIR | BUILDER | OTHER_NAMED_OWNER
  governed_object_ref: optional exact version/hash
  proposed_label: optional string
  proposal_provenance_refs: [exact refs]
  supporting_ingredient_refs: [exact refs]
  contradicting_ingredient_refs: [exact refs]
  limitation_codes: [typed code]
  downstream_action: CONSUME_REFERENCE | REQUEST_OWNER_COMPILATION | NO_ACTION
```

Rules:

- `AUTHORITATIVE_REFERENCE` requires a resolvable object version/hash owned by the named authority;
- `NON_AUTHORITATIVE_CANDIDATE` must have proposal provenance and `REQUEST_OWNER_COMPILATION` or `NO_ACTION`;
- a candidate cannot be used as a final sequence, composition, or Visual Asset Demand decision;
- `NOT_APPLICABLE` requires an applicability decision receipt; and
- package approval does not change `authority_state`.

### 6.6 `ExpressionEvidenceGraph` and relation edges

```yaml
ExpressionEvidenceGraph:
  evidence_graph_id: content-derived-id
  version: integer
  content_hash: sha256
  node_refs: [exact ingredient/evidence/object refs]
  edges:
    - edge_id: content-derived-id
      source_ref: exact ref
      target_ref: exact ref
      relation_kind: RelationKind
      ordinal: optional integer
      evidence_refs: [exact refs]
      proposed_by_ref: exact actor/program ref
      decision_state: PROPOSED | APPROVED | REJECTED | SUPERSEDED
      decision_receipt_ref: optional exact ref
  graph_validation_receipt_ref: exact ref
```

Graph validation SHALL reject dangling refs, cross-tenant refs, cycles in relation kinds declared acyclic (`PRECEDES`, `FOLLOWS`, `CAUSES` where a cycle is semantically invalid), contradictory order without a review decision, and relation edges with no evidence. A graph may preserve conflicting claims; the conflict must be explicit through `CONTRADICTS` and cannot be normalized away.

### 6.7 `ExpressionIngredientInventoryVersion`

```yaml
ExpressionIngredientInventoryVersion:
  inventory_id: stable content-derived-id
  version: integer
  content_hash: sha256
  schema_id: conscious-activations.interview-expression.expression-ingredient-inventory
  schema_version: candidate-v2.1
  organization_id: string
  brand_id: string
  source_session_ref: exact ref
  source_package_ref: exact ref
  source_kind: interview_expression
  source_snapshot_hash: sha256
  inventory_profile_ref: exact version/hash
  approved_ingredient_refs: [exact refs]
  review_required_candidate_refs: [exact refs]
  excluded_candidate_refs: [exact refs]
  evidence_graph_ref: exact version/hash
  completeness_result_ref: exact version/hash
  gap_refs: [exact refs]
  semantic_opportunity_refs: [exact refs]
  effective_restriction_refs: [exact refs]
  lifecycle_state: PROPOSED | REVIEW_REQUIRED | APPROVED | REJECTED |
    SUPERSEDED | REVOKED | INVALIDATED
  approval_receipt_ref: optional exact ref
  predecessor_ref: optional exact inventory ref
  dependency_manifest_ref: exact ref
```

The inventory SHALL include at least one eligible ingredient or a truthful `BLOCKED_WITH_GAPS` result. It cannot be approved if a required evidence pointer fails resolution, if an ingredient cites a non-approved current Moment, if restrictions are unresolved, or if the evidence graph is inconsistent. Excluded and review-required entries stay outside `approved_ingredient_refs` but remain historically reachable.

### 6.8 Package request, slots, gaps, and completeness

```yaml
AssetPackageRequest:
  package_request_id: content-derived-id
  request_version: integer
  content_hash: sha256
  requesting_product: AIR | BUILDER | PIPELINE | STUDIO | OTHER_GOVERNED_CONSUMER
  purpose_code: typed string
  inventory_ref: exact approved version/hash
  package_profile_ref: exact version/hash
  requested_slots:
    - slot_request_id: stable string
      ingredient_kinds: [IngredientKind]
      cardinality:
        minimum: nonnegative integer
        maximum: optional nonnegative integer
      applicability_rule_refs: [exact refs]
      required_use_classes: [typed use]
      optional: boolean
  supplied_owner_decision_refs: [exact refs]
  additional_restriction_refs: [exact refs]
  portability_profile_ref: exact version/hash
```

```yaml
PackageSlot:
  slot_id: content-derived-id
  slot_request_id: string
  ingredient_ref: exact approved version/hash
  intended_consumer_use: typed use
  evidence_graph_ref: exact version/hash
  inherited_restriction_refs: [exact refs]
  added_restriction_refs: [exact refs]
  source_wrong_reading_risk_refs: [exact refs]
  semantic_owner_decision_refs: [exact refs]
  eligibility_state: ELIGIBLE | OWNER_DECISION_REQUIRED | REVIEW_REQUIRED | BLOCKED
  eligibility_receipt_ref: exact ref
```

```yaml
PackageGap:
  gap_id: content-derived-id
  slot_request_id: string
  gap_kind: SOURCE_EVIDENCE_MISSING | APPROVAL_MISSING | RESTRICTION_UNRESOLVED |
    OWNER_DECISION_MISSING | COMPATIBILITY_UNSUPPORTED | EVALUATOR_UNAVAILABLE
  missing_condition: typed condition
  attempted_ingredient_refs: [exact refs]
  evidence_refs: [exact refs]
  owner: named product or actor role
  resolution_criteria: [typed criterion]
  lifecycle_state: OPEN | RESOLVED | SUPERSEDED
```

```yaml
PackageCompletenessResult:
  result_id: content-derived-id
  package_request_ref: exact ref
  inventory_ref: exact ref
  profile_ref: exact ref
  requirement_results:
    - requirement_id: string
      decision: ApplicabilityDecision
      ingredient_refs: [exact refs]
      gap_refs: [exact refs]
      evidence_refs: [exact refs]
      rule_ref: exact version/hash
      owner_decision_ref: optional exact ref
  aggregate_state: READY_FOR_IE_APPROVAL | SOURCE_GAPS_RECORDED |
    OWNER_DECISION_PENDING | REVIEW_REQUIRED | BLOCKED
  evaluator_identity: deterministic rule/program/version
  canonical_input_hash: sha256
```

Cardinality is evaluated only when the active request/profile declares it. A shortfall becomes a `PackageGap`; the compiler never duplicates an ingredient or generates a replacement to meet a count.

### 6.9 `AssetPackageSpecVersion`, manifest, and receipts

```yaml
AssetPackageSpecVersion:
  asset_package_spec_id: stable content-derived-id
  version: integer
  content_hash: sha256
  schema_id: conscious-activations.interview-expression.asset-package-spec
  schema_version: candidate-v2.1
  organization_id: string
  brand_id: string
  source_kind: interview_expression
  inventory_ref: exact approved version/hash
  package_request_ref: exact version/hash
  package_profile_ref: exact version/hash
  intended_consumer: named product
  purpose_code: typed string
  slots: [PackageSlot]
  gap_refs: [exact refs]
  exclusion_summary_refs: [exact refs]
  semantic_opportunity_refs: [exact refs]
  effective_restriction_refs: [exact refs]
  source_wrong_reading_risk_refs: [exact refs]
  completeness_result_ref: exact ref
  portability_profile_ref: exact ref
  compatibility_declarations: [typed declaration]
  lifecycle_state: PackageLifecycleState
  approval_receipt_ref: optional exact ref
  predecessor_ref: optional exact package ref
  dependency_manifest_ref: exact ref
```

`AssetPackageManifest` SHALL contain only repository-relative logical names or content-addressed locators, exact bytes/hashes/media metadata where material is distributed, and the dependency closure required for reconstruction. It SHALL distinguish embedded bytes from referenced bytes and redacted from unavailable bytes. A manifest with an absolute path, unresolved local drive, home directory, temporary directory, or environment-dependent locator fails portability.

Required receipts:

- `InventoryCompilationReceipt` — exact inputs, candidate outputs, blockers, command/idempotency, deterministic hash;
- `IngredientDecisionReceipt` — actor, authority, proposed and decided entry refs, rationale/evidence, segregation result;
- `InventoryApprovalReceipt` — approved version/hash and evidence closure;
- `PackageCompilationReceipt` — request/inventory/profile inputs, slots/gaps/completeness, deterministic hash;
- `PackageApprovalReceipt` — attributable approval and restrictions;
- `PackageHandoffReceipt` — exact distributed manifest/hash, target consumer, transport projection, no consumption claim;
- `PackageConsumptionAcknowledgement` — consumer and exact accepted/rejected package version/hash; and
- `PackageInvalidationReceipt` — upstream change, dependency traversal, affected/unaffected descendants, and reason.

Receipts are immutable and refer to artifact versions. They SHALL NOT embed mutable “current” snapshots as proof.

### 6.10 Commands, events, repository, and API boundary

Required commands:

```text
CompileExpressionIngredientInventory
EvaluateExpressionIngredientInventory
DecideExpressionIngredientCandidates
ApproveExpressionIngredientInventory
RejectExpressionIngredientInventory
CompileAssetPackageSpec
EvaluateAssetPackageCompleteness
ApproveAssetPackageSpec
RejectAssetPackageSpec
PublishAssetPackageHandoff
AcknowledgeAssetPackageConsumption
RequestAssetPackageCorrection
SupersedeAssetPackageSpec
RevokeAssetPackageSpec
InvalidateAssetPackageDescendants
ReplayAssetPackageDecision
CancelAssetPackageCommand
```

Each command envelope SHALL include command ID, idempotency key, canonical request hash, actor/delegation context, organization and brand scope, aggregate ref/expected version, causation/correlation refs, policy/profile versions, and cancellation ref. Command handlers SHALL not accept unscoped actor IDs or caller-supplied approval fields.

Required events:

```text
ExpressionInventoryCompiled
ExpressionIngredientDecided
ExpressionInventoryApproved
ExpressionInventoryRejected
AssetPackageCompiled
AssetPackageCompletenessEvaluated
AssetPackageApproved
AssetPackageRejected
AssetPackageHandoffPublished
AssetPackageConsumptionAcknowledged
AssetPackageConsumptionRejected
AssetPackageCorrectionRequested
AssetPackageSuperseded
AssetPackageRevoked
AssetPackageInvalidated
AssetPackageReplayCompleted
AssetPackageCommandCancelled
```

The repository interface SHALL expose exact-version `get`, compare-and-swap append, receipt/event/command lookup, dependency traversal, historical reconstruction, and idempotency lookup. It SHALL NOT expose a mutable `put_spec` overwrite as the canonical write primitive. “Get current” MAY exist for operator projection but cannot be used to reconstruct or execute a pinned handoff.

Future APIs SHOULD be command endpoints plus exact-version queries, for example:

```text
POST /v2/interview-expression/inventories:compile
POST /v2/interview-expression/inventories/{id}/versions/{version}:approve
POST /v2/interview-expression/asset-packages:compile
POST /v2/interview-expression/asset-packages/{id}/versions/{version}:approve
POST /v2/interview-expression/asset-packages/{id}/versions/{version}:handoff
POST /v2/interview-expression/asset-packages/{id}/versions/{version}:acknowledge
GET  /v2/interview-expression/asset-packages/{id}/versions/{version}
GET  /v2/interview-expression/asset-packages/{id}/versions/{version}/manifest
GET  /v2/interview-expression/asset-packages/{id}/versions/{version}/lineage
```

Status codes and typed error bodies SHALL preserve semantic failure context. A request returning `202` or `200` is not evidence of package approval unless the response contains the exact approval receipt and artifact version/hash.

### 6.11 Canonical serialization and hash projection

The semantic hash projection SHALL include all fields that affect source identity, meaning, eligibility, restrictions, applicability, evidence, owner decision, relation order, and consumer use. It SHALL exclude operational metadata such as database key, wall-clock persistence time, retry count, process ID, host, absolute path, and trace sampling details.

For an inventory:

```text
inventory_content_hash = SHA256(
  canonical_json({
    schema_identity,
    scope,
    exact_source_snapshot,
    profile_ref,
    sorted_approved_ingredient_refs,
    sorted_review_required_refs,
    sorted_excluded_refs,
    evidence_graph_ref,
    completeness_result_ref,
    sorted_gap_refs,
    sorted_semantic_opportunity_refs,
    sorted_effective_restrictions
  })
)
```

For a package, slots preserve `slot_request_id` then explicit ordinal; references within a set-like field sort by `(object_type, object_id, version, hash)`. Two implementations supplied the same semantic inputs SHALL produce byte-identical canonical projections, hashes, and content-derived IDs.

### 6.12 Compatibility, adapters, and invalid examples

Compatibility is semantic, not parse-only. A consumer SHALL negotiate and pin support for:

- schema and package profile identity/version;
- required Ingredient kinds and Evidence roles;
- rational-time and exact-version refs;
- source-kind `interview_expression`;
- restriction inheritance and wrong-reading-risk preservation;
- semantic opportunity authority states;
- `NOT_APPLICABLE`, gap, exclusion, supersession, invalidation, and acknowledgement semantics;
- portability manifest version; and
- receipt and replay features.

An adapter may rename or reshape fields only when every required meaning survives. It cannot flatten typed evidence to notes, convert a missing decision to `NOT_APPLICABLE`, downgrade a restriction, guess source kind/classification, replace exact version/hash with latest, turn a candidate opportunity authoritative, or interpret parse success as behavioral compatibility.

Invalid examples include:

```yaml
# Invalid: no exact time, speaker, transcript revision, Moment, or approval.
kind: EXACT_QUOTE
text: "I finally saw it differently."
source_evidence_refs: ["interview-1"]
```

```yaml
# Invalid: IE creates AIR semantic authority.
archetype_opportunity:
  label: Transformation Story
  authority_state: AUTHORITATIVE_REFERENCE
  authority_owner: INTERVIEW_EXPRESSION
```

```yaml
# Invalid: missing evidence hidden as applicability.
keyframe_requirement:
  decision: NOT_APPLICABLE
  evidence_refs: []
```

```yaml
# Invalid: nonportable and mutable dependency.
visual_reference_path: D:\\captures\\guest\\frame-441.png
expression_moment_ref: latest
```

```yaml
# Invalid: historical fixed count causes fabrication.
requested_short_videos: 4
available_source_moments: 1
compiler_action: duplicate_and_rewrite_to_fill
```

## 7. Implementation stages and exact target paths

These stages and paths are a future build plan only. They are not created by this prompt and are not authorized until ratification/adoption and a governed Development Capsule permit build.

### 7.1 Stage 0 — contract and profile lock

Future authorized work SHALL first create or adopt:

- governed schema IDs/versions for inventory, ingredient, evidence graph, package, completeness, gaps, manifests, and receipts;
- package request/profile and portability-profile registries;
- role/authority policy and segregation-of-duty rules;
- compatibility declaration and feature negotiation;
- canonical serialization/hash rules; and
- migration/adaptation disposition for Studio predecessors.

No stage may publish shared contract release bytes unless separately authorized.

### 7.2 Stage 1 — immutable domain models

Proposed future paths under the Interview Expression product root:

```text
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/models.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/evidence.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/relations.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/completeness.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/canonicalization.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/errors.py
```

Models SHALL be immutable value objects with validation at construction, no mutable defaults, no implicit current time, and no random identity in semantic constructors.

### 7.3 Stage 2 — application services and ports

```text
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/commands.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/events.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/ports.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/inventory_service.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/package_service.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/review_service.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/handoff_service.py
06_INTERVIEW_EXPRESSION/src/interview_expression/asset_packages/invalidation_service.py
```

Services SHALL depend inward on domain/ports. They cannot import Studio, VAE, Builder, Pipeline, or Delegation implementation modules.

### 7.4 Stage 3 — durable persistence and atomic command handling

```text
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_repository.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_unit_of_work.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_event_store.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_dependency_graph.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_idempotency_store.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/persistence/asset_package_outbox.py
```

Transaction/invariant tests SHALL prove no partial state, receipt, event, command, dependency, idempotency, or outbox storage.

### 7.5 Stage 4 — source and consumer adapters

```text
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/source/expression_moment_reader.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/source/transcript_audio_reader.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/source/visual_index_reader.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/source/reaction_receipt_reader.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/source/source_package_reader.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/outbound/air_evidence_handoff.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/outbound/builder_package_handoff.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/outbound/studio_projection.py
06_INTERVIEW_EXPRESSION/src/interview_expression/adapters/outbound/delegation_projection.py
```

Adapters SHALL translate without redefining owners. No adapter may import a consumer's local canonical schema as an IE fork. Any VAE interaction must remain downstream of a valid Builder/AIR-owned demand, not a direct package-to-production shortcut.

### 7.6 Stage 5 — API, projections, and operator review

```text
06_INTERVIEW_EXPRESSION/src/interview_expression/api/v2/asset_packages.py
06_INTERVIEW_EXPRESSION/src/interview_expression/projections/asset_package_read_model.py
06_INTERVIEW_EXPRESSION/src/interview_expression/projections/asset_package_lineage.py
06_INTERVIEW_EXPRESSION/src/interview_expression/projections/asset_package_review.py
```

The UI/projection SHALL show source evidence, restrictions, eligibility, gaps, exclusions, owner-decision state, content hash, version, approval, handoff, and invalidation. It must not offer direct editing of upstream evidence or semantic-owner decisions. All corrections are commands.

### 7.7 Stage 6 — migrations and fixtures

```text
06_INTERVIEW_EXPRESSION/migrations/asset_packages/
06_INTERVIEW_EXPRESSION/fixtures/asset_packages/
06_INTERVIEW_EXPRESSION/docs/migrations/asset-package-predecessor-crosswalk.md
```

Migration SHALL create new immutable artifacts and explicit receipts. Historical Studio objects that lack exact source time, speaker, transcript revision, Moment approval, evidence graph, restriction closure, or content hash SHALL be blocked or imported as `HISTORICAL_REFERENCE_ONLY`; no adapter may guess missing data. Original bytes/hashes remain linked.

### 7.8 Stage 7 — exact future test paths

```text
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_evidence_pointer_validation.py
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_ingredient_eligibility.py
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_evidence_graph.py
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_completeness_and_not_applicable.py
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_canonical_serialization.py
06_INTERVIEW_EXPRESSION/tests/unit/asset_packages/test_semantic_opportunity_authority.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_inventory_atomic_commit.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_package_approval_handoff.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_idempotency_and_concurrency.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_selective_invalidation.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_historical_reproduction.py
06_INTERVIEW_EXPRESSION/tests/integration/asset_packages/test_portable_manifest.py
06_INTERVIEW_EXPRESSION/tests/contract/test_air_evidence_handoff.py
06_INTERVIEW_EXPRESSION/tests/contract/test_builder_package_handoff.py
06_INTERVIEW_EXPRESSION/tests/contract/test_delegation_projection.py
06_INTERVIEW_EXPRESSION/tests/architecture/test_asset_package_import_boundaries.py
```

### 7.9 Stage gates

| Gate | Evidence | Claim ceiling |
|---|---|---|
| Contract lock | Ratified/adopted authority, exact schemas/profiles, owner review | Ready for authorized implementation planning only |
| Domain | Unit/property tests and canonical vectors | No integration or production claim |
| Persistence | Atomicity, idempotency, concurrency, replay tests | Local implementation evidence only |
| Adapters | Contract fixtures and owner acceptance receipts | Contract-compatible, not production accepted |
| End-to-end | Imported-interview reference slice through package handoff and replay | Synthetic/limited proof only as separately authorized |
| Production | Trust, operations, compute, recovery, evaluator, security, and product authorization | Separately governed; not granted here |

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Condition | Retry class | Required context |
|---|---|---|---|
| `PACKAGE_SOURCE_REF_MISSING` | Required exact upstream ref absent | Repair input | object kind/id/version/hash |
| `PACKAGE_SOURCE_HASH_MISMATCH` | Observed bytes differ from pinned hash | Nonretryable until corrected | expected/observed hash and source |
| `PACKAGE_SOURCE_VERSION_STALE` | Current command attempts stale/superseded dependency | Repair or explicit historical replay | requested/current refs |
| `PACKAGE_EXPRESSION_MOMENT_NOT_APPROVED` | Ingredient cites non-approved Moment | Repair upstream | Moment and lifecycle refs |
| `PACKAGE_QUOTE_EXACT_SOURCE_REQUIRED` | Quote lacks exact words/speaker/time/revision | Repair evidence | missing fields and candidate |
| `PACKAGE_AUDIO_LINEAGE_REQUIRED` | Audio/voice ref lacks artifact/track/time/speaker/use | Repair evidence | missing closure |
| `PACKAGE_VISUAL_LINEAGE_REQUIRED` | Frame/keyframe/visual ref lacks source/index/transform | Repair evidence | missing closure |
| `PACKAGE_EVIDENCE_GRAPH_INVALID` | Dangling/invalid/unsupported relation | Repair graph | node/edge and reason |
| `PACKAGE_RESTRICTION_UNRESOLVED` | Required restriction cannot resolve or is weakened | Nonretryable until owner correction | inherited/effective refs |
| `PACKAGE_SEMANTIC_AUTHORITY_VIOLATION` | IE or adapter claims owner-external meaning | Nonretryable | field, claimed owner, canonical owner |
| `PACKAGE_SOURCE_GAP` | Requested source ingredient does not exist | New source or request amendment | slot and missing condition |
| `PACKAGE_OWNER_DECISION_REQUIRED` | AIR/Builder/other owner decision absent | Await owner | owner and decision type |
| `PACKAGE_NOT_APPLICABLE_EVIDENCE_REQUIRED` | N/A lacks rule/evidence/decision | Repair decision | requirement/profile refs |
| `PACKAGE_SELF_APPROVAL_FORBIDDEN` | Proposer and approver violate policy | New authorized reviewer | actors and policy |
| `PACKAGE_EXPECTED_VERSION_CONFLICT` | Optimistic-concurrency mismatch | Refresh and reissue | expected/observed version |
| `PACKAGE_IDEMPOTENCY_CONFLICT` | Same key with different request bytes | Nonretryable | key and both hashes |
| `PACKAGE_ATOMIC_COMMIT_FAILED` | Any aggregate/receipt/event/dependency/outbox write fails | Safe retry after rollback | transaction/ref states |
| `PACKAGE_CONSUMER_PROFILE_UNSUPPORTED` | Required semantic feature not negotiated | New compatibility decision | required/observed features |
| `PACKAGE_ABSOLUTE_PATH_FORBIDDEN` | Manifest contains machine path | Repair projection | offending locator |
| `PACKAGE_MIGRATION_WOULD_GUESS` | Legacy conversion lacks required meaning | Block migration | missing fields and source bytes |
| `PACKAGE_REPLAY_INPUT_UNAVAILABLE` | Exact historical bytes/profile absent | Nonretryable unless restored | missing identities |
| `PACKAGE_COMMAND_CANCELLED` | Cancellation accepted before commit | Final for command | command/cancellation refs |

Every failure receipt SHALL include command ID, correlation/causation, actor/scope, aggregate/version, canonical request hash, exact failed dependency refs, typed code, retry classification, safe operator action, and whether any transaction committed. Logs without a durable failure receipt are insufficient.

### 8.2 Retry versus semantic repair

Infrastructure failures may be retried with the same idempotency key after confirmed rollback. Semantic failures require corrected evidence, owner decision, authority, restriction, profile, or a new command. A retry SHALL not silently switch to a newer source version. Evaluator unavailability produces `EVALUATOR_UNAVAILABLE`, not pass, N/A, or a guessed result.

### 8.3 Atomic rollback and partial results

The unit of work SHALL treat aggregate version, receipts, event stream, command result, dependency graph, idempotency record, and outbox as one commit. If any write fails:

- no lifecycle transition is visible;
- no success receipt/event/idempotency result remains;
- no handoff message is publishable;
- temporary staged bytes are unreachable and garbage-collectable; and
- a durable failure receipt is written only through a separate explicitly designed failure transaction that cannot be mistaken for success.

A partial compilation result MAY be persisted as an explicit candidate with gaps only if that is the intended semantic outcome and all its artifacts/receipts commit atomically. It is not an infrastructure partial commit.

### 8.4 Cancellation and post-completion action

Cancellation checks occur before source resolution, after expensive deterministic evaluation boundaries, and immediately before commit. A cancelled command cannot create an approved artifact. Once commit succeeds, cancellation cannot reverse history; the caller must issue supersession, revocation, or invalidation as authorized. Late cancellation and late evidence are ordered by committed event sequence and expected version, not wall-clock arrival alone.

### 8.5 Migration and compatibility

Historical `cmf.expression_ingredient_inventory.v1` and `cmf.asset_package_spec.v1` records require a source-by-source migration receipt. Migration SHALL:

1. hash-lock original bytes;
2. map each field to the new semantic field or record an explicit gap;
3. preserve original IDs as historical aliases, never current canonical identities;
4. resolve exact source objects without guessing;
5. inherit all known restrictions;
6. mark fixed count/offer/pricing fields as historical profile metadata, not canonical package truth;
7. represent repository-local archetype routes as `NON_AUTHORITATIVE_CANDIDATE` unless an exact AIR ref exists;
8. create a new immutable target artifact and migration receipt; and
9. block current consumption until required evidence/approval closes.

Parsing a legacy record is not compatibility. An adapter that accepts bytes but does not enforce evidence closure, restrictions, authority states, lifecycle, and invalidation is incompatible.

### 8.6 Selective invalidation

On an upstream change, the invalidation service SHALL:

1. verify the upstream correction/supersession/revocation receipt;
2. locate descendants by exact version/hash edge;
3. evaluate each edge's impact class and consumed subrange/ref;
4. mark only affected current descendants invalid or review-required;
5. leave unaffected siblings active and record why;
6. emit per-descendant and traversal-summary receipts; and
7. preserve historical artifact bytes and dependency closures.

Examples:

- a transcript correction outside a quote and outside its required context does not invalidate that quote;
- a speaker correction for a used quote invalidates the ingredient and all packages selecting it;
- a keyframe crop correction invalidates packages using that crop, not audio-only packages;
- a revoked source authorization invalidates all descendants using the prohibited scope;
- a revised non-authoritative archetype opportunity reopens only consumers that cited it; and
- a metadata-only display label change does not invalidate semantic content.

### 8.7 Replay and historical reproduction

Historical reconstruction SHALL load the exact command envelope, authority/policy/profile versions, upstream object versions/hashes, evaluator/program versions, canonicalization version, aggregate events, decisions, and receipts. It SHALL reproduce:

- canonical inventory/package semantic bytes and hash;
- lifecycle transition sequence;
- eligible/excluded/gap/completeness decisions;
- handoff manifest and consumer acknowledgement; and
- later supersession/invalidation overlay without rewriting original state.

Replay time is isolated from receipt recorded time. External source bytes must be content-addressed or restored from the governed archive. If a stochastic program proposed candidates, its frozen proposal bytes/receipt are replay inputs; canonical truth is not regenerated from a new model call.

### 8.8 Recovery and degraded behavior

Safe degraded behaviors:

- source resolver unavailable: fail before artifact transition;
- optional consumer adapter unavailable: keep approved package, mark handoff pending, no false acknowledgement;
- deterministic evaluator unavailable: record evaluator unavailable, block required completeness;
- outbox delivery interrupted after commit: retry delivery using the committed outbox/idempotency record;
- dependency projection lag: block current consumption if correctness depends on it, while exact-version reads remain available; and
- Studio projection unavailable: canonical package remains unchanged; operator UI reports projection lag.

Unsafe fallbacks are latest-version substitution, free-form notes, guessed source classification, relaxed restrictions, local archetype inference, generated gap filling, or approval based only on compiler success.

### 8.9 Observability, privacy, and technical security

Metrics SHALL distinguish compilation attempts, evidence-closure failures, source gaps, owner decisions, review outcomes, approvals, handoffs, consumer acknowledgements/rejections, invalidations, replay results, conflicts, rollbacks, and adapter incompatibility. Traces SHALL carry correlation/causation and object/version/hash identifiers but SHALL NOT log unrestricted transcript, voice, video, consent details, or private source excerpts.

Operational security includes tenant/brand scoping, least-privilege command roles, signed/delegated actor context where governed, encryption in transit/at rest, redaction-safe logs, content-addressed integrity, and audit retention. These controls do not create generic creative/content-rights approval authority. Source use is controlled by explicit source authority/restriction records and attributable operator decisions.

## 9. Behavior-specific acceptance criteria

### AC-01 — Exact writer and upstream lock

The implementation evidence cites the exact `TS-INT-004` version/hash admitted by this specification. A changed draft triggers the six declared revision-impact sections and cannot be silently substituted.

### AC-02 — Exact quote evidence

Given a proposed quote without exact words, speaker, rational source time, transcript revision, approved Expression Moment, or approval evidence, compilation returns `PACKAGE_QUOTE_EXACT_SOURCE_REQUIRED`, stores no eligible ingredient, and records which fields are missing.

### AC-03 — Qualification and context preservation

Given a quote whose meaning changes when a neighboring qualification is omitted, the evidence validator requires the context/qualification span or excludes the quote. The package cannot present the truncated text as source truth.

### AC-04 — Audio and voice-reference limits

Given audio with missing track/channel, source artifact hash, interval, speaker identity, or permitted-use restriction, the audio/voice ingredient is blocked. A voice reference never implies synthesis, cloning, training, or production permission.

### AC-05 — Keyframe and visual lineage

Given a keyframe, the package preserves source artifact/version/hash, shot/index version, frame index or rational time, crop/transform, technical limitations, and source-faithful/derived status. A machine path or untraced derivative is rejected.

### AC-06 — Approved Moment is mandatory

Only current approved Expression Moment versions are selectable for new current packages. Proposed, borderline, rejected, superseded, revoked, or invalidated Moments remain historical evidence and cannot silently enter the eligible inventory.

### AC-07 — Tag and Reaction ownership

The package references exact tag and Reaction Receipt objects without changing their provenance, outcome, maximum claim, cause, or reaction tail. Parsing those refs without enforcing their states is rejected.

### AC-08 — Candidate archetype remains non-authoritative

Given a repository-local route suggestion with no AIR object ref, the package records `NON_AUTHORITATIVE_CANDIDATE` and `REQUEST_OWNER_COMPILATION` or `NO_ACTION`. Neither inventory nor package approval converts it to `AUTHORITATIVE_REFERENCE`.

### AC-09 — Exact AIR reference remains AIR-owned

Given a valid AIR-owned semantic object ref, the package may preserve it by exact version/hash and owner. Interview Expression cannot amend it, and a changed AIR ref produces a new package version or owner-decision state.

### AC-10 — Source gap, not fabrication

Given a package request for an ingredient unsupported by the source, compilation records `PackageGap(SOURCE_EVIDENCE_MISSING)` and an incomplete aggregate state. It does not generate, duplicate, rewrite, or infer an ingredient to meet requested cardinality.

### AC-11 — Historical fixed counts are not current law

Absent a current governed package request/profile declaring cardinality, no historical Guest Asset Pack count influences completeness. When cardinality is governed, it is evaluated as a request rule and any shortfall is a gap.

### AC-12 — Evidence-bearing `NOT_APPLICABLE`

An N/A decision includes exact profile/rule, evidence, deciding actor/program, receipt, and reopen condition. Missing evidence, unsupported input, or evaluator failure cannot become N/A.

### AC-13 — Restriction monotonicity

Every package slot contains the union of inherited source restrictions and any stricter package restrictions. A command or adapter that removes or weakens one fails `PACKAGE_RESTRICTION_UNRESOLVED` or the corresponding authority failure.

### AC-14 — Wrong-reading risks cross the boundary

Source-derived wrong-reading risks and continuity constraints survive into every selecting package slot and handoff. Builder remains responsible for authoritative downstream wrong-reading locks and cannot claim IE package evidence is already a Visual Asset Demand.

### AC-15 — Independent approval

A proposer or model cannot approve its own inventory/package when segregation policy requires independence. Approval records attributable actor, scope, authority, evidence, exact bytes/hash, and decision rationale.

### AC-16 — Inventory and package approval remain distinct

Approving an inventory does not approve any package. Approving a package does not acknowledge consumer use, grant AIR adoption, authorize Builder/Harness execution, accept VAE production, or certify a format.

### AC-17 — Immutable version and stale concurrency

After approval, a content change creates a new version/hash. Two commands with the same expected version cannot both commit; the loser receives `PACKAGE_EXPECTED_VERSION_CONFLICT` with no partial artifacts.

### AC-18 — Idempotent replay

Repeating the same command with identical idempotency scope and canonical request bytes returns the original artifact and receipts without duplicate events or versions. Reusing the key with changed bytes fails explicitly.

### AC-19 — Atomic commit and rollback

Injected failures at each persistence step prove that artifact, command, decision/approval receipt, event, dependencies, idempotency result, and outbox either all commit or all roll back. No state-only or receipt-only success is observable.

### AC-20 — Portable handoff

The handoff manifest contains no absolute path, host, home directory, temp directory, environment value, or traversal-order artifact. Extraction on a clean layout validates all distributed bytes and exact hashes.

### AC-21 — Consumer acknowledgement is separate

A consumer accepts or rejects one exact package version/hash with a reason. The acknowledgement does not mutate the package and does not duplicate source or visual-production evaluation.

### AC-22 — Selective invalidation

Correcting one source span invalidates only ingredients and packages whose dependency edges consume that span or required context. Unaffected siblings remain active with recorded evidence. All historical versions remain reproducible.

### AC-23 — Revocation and post-completion invalidation

Revoked source authority blocks new consumption and invalidates affected current descendants while retaining audit evidence. Previously handed-off assets/results remain historically reconstructable but cannot be presented as currently authorized.

### AC-24 — Migration never guesses

Legacy objects missing source kind, exact source time, speaker, approval, restrictions, or version/hash are blocked or marked historical-reference-only. Migration creates a new immutable artifact/receipt and never edits predecessor bytes.

### AC-25 — Semantic compatibility, not parse-only

A consumer that parses the document but ignores evidence closure, authority state, restriction inheritance, invalidation, or source-kind semantics is rejected as incompatible.

### AC-26 — Owner boundaries hold end to end

AIR compiles semantic meaning; Builder declares dependencies and target authority; Pipeline executes; VAE realizes; Studio projects/corrects; Delegation transports. No package command invokes or internalizes another product's owned decision.

### AC-27 — Historical reproduction

Replaying a historical package with exact frozen inputs reproduces canonical bytes/hash, decisions, receipts, manifest, and handoff identity even after successors or invalidations exist. Missing exact bytes yields an explicit failure, not current-version substitution.

### AC-28 — Claim ceiling remains false for build and production

All completion evidence reports `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, `build_authority: false`, and the pre-ratification ceiling. No test pass or package approval changes product implementation/production authorization.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

Future unit/property evidence SHALL cover:

- every Ingredient kind's required evidence matrix;
- rational source-time normalization, boundary containment, and invalid intervals;
- quote exactness, speaker binding, qualification/context preservation, and transcript revision pinning;
- audio/voice identity, permitted-use scope, and no implied synthesis permission;
- keyframe/visual source identity, frame/time, crop/transform, derived-parent lineage, and nonsemantic status;
- tag, Anchor Hit, Reaction Receipt, Expression Moment, and source-package state enforcement;
- evidence-graph dangling refs, relation constraints, cycles, contradictions, and stable ordering;
- semantic-opportunity authority states and owner action;
- restriction union/monotonicity and wrong-reading-risk preservation;
- completeness outcomes and evidence-bearing N/A;
- gap creation without duplicate/generated source;
- canonical serialization across dictionary orders, filesystem orders, locales, time zones, environment variables, and processes;
- stable content-derived IDs/hashes with clock/random differences; and
- mutable-default/shared-state resistance.

Property tests SHALL generate semantically equivalent payload permutations and assert identical canonical bytes/hash, plus minimally different authority/restriction/evidence payloads and assert different hashes.

### 10.2 Integration tests

Future integration evidence SHALL prove:

1. approved Moment/source package through inventory candidate, review, approved inventory, package compile, completeness, approval, handoff, and consumer acknowledgement;
2. quote without exact words/time rejects before eligibility;
3. unsupported requested slot creates a durable source gap and no fabricated item;
4. package with unresolved AIR semantic decision remains `OWNER_DECISION_PENDING` while unrelated package requests remain writable;
5. independent reviewer policy blocks self-approval;
6. optimistic concurrency permits one winning transition;
7. idempotent duplicate returns original result and conflicting duplicate fails;
8. failures injected at every unit-of-work write roll back all success state;
9. outbox retry publishes exactly once semantically;
10. consumer rejection does not alter IE approval;
11. correction produces immutable successor and selective descendant invalidation;
12. historical replay reproduces pre-correction bytes and overlays later invalidation;
13. portable manifest validates in a clean extracted layout; and
14. legacy adapter blocks missing semantics rather than guessing.

### 10.3 Contract tests

AIR contract tests SHALL show that IE supplies evidence and candidate opportunities while AIR alone creates owned semantic objects. Builder contract tests SHALL show exact package pinning, restriction inheritance, and no source rediscovery. Delegation tests SHALL show immutable transport, authority context, compatibility negotiation, replay/idempotency semantics, and no creative mutation. Studio tests SHALL show read projection and typed correction commands only. Any future VAE test SHALL begin from an authorized upstream demand and prove package approval is not production acceptance.

### 10.4 Architecture tests

Architecture tests SHOULD protect semantic boundaries, not brittle exact source text. They SHALL assert:

- domain modules do not import API, persistence, Studio, AIR, Builder, Pipeline, VAE, or Delegation implementations;
- source adapters are read-only from the IE package domain's perspective;
- only review/approval services can emit approval decisions;
- no package module defines AIR-owned semantic object constructors;
- no package module defines VAE production plans or Builder Visual Asset Demands;
- canonicalization code has no clock/random/environment/path dependency;
- persistence writes flow through the unit of work; and
- API/projection layers cannot call repository mutation outside command handlers.

Tests SHALL prefer import-graph, interface, AST, and behavior assertions over exact duplicate lists of implementation source lines.

### 10.5 Determinism and portability matrix

The same frozen fixture SHALL run at least twice in fresh processes and across supported operating systems/layouts with varied:

- current time and time zone;
- random seed;
- dictionary construction order;
- filesystem enumeration order;
- workspace absolute path;
- process environment;
- locale and Unicode input representation; and
- database insertion/row order.

Expected canonical inventory/package bytes, content-derived IDs, hashes, decisions, and manifests SHALL be identical. Receipt metadata timestamps may differ only when receipts are newly produced; a replay of frozen receipt bytes SHALL reproduce the original recorded values.

### 10.6 Security and misuse tests

Tests SHALL reject cross-tenant/brand refs, actor scope escalation, forged approval refs, weakened restrictions, path traversal, absolute paths, unsupported manifest members, hash mismatch, oversized/unbounded excerpt projection, unauthorized voice-use claims, stale versions, and a consumer attempting to alter IE/AIR/Builder/VAE ownership. Logs and traces SHALL be checked for leaked transcript, audio, private path, or sensitive authority detail.

### 10.7 Golden imported-interview reference slice

The governed reference slice SHALL freeze:

1. one exact imported source package and source kind `interview_expression`;
2. exact transcript/phrase/audio/visual/Reaction evidence;
3. approved Expression Moments from `TS-INT-004`;
4. an inventory with an exact quote, context, audio/voice ref, keyframe/visual ref, tags, restrictions, and at least one non-authoritative semantic opportunity;
5. one explicit source gap or evidence-bearing N/A;
6. an approved inventory and consumer-scoped Asset Package Spec;
7. an AIR owner-decision boundary rather than IE-created semantics;
8. Builder/Harness consumption by exact version/hash without source rediscovery;
9. downstream Format 07 short, SuperVisual, and animation-scene package references only when their own specs/owners authorize them;
10. evaluation, operator correction, HumanResolution, selective invalidation, and replay; and
11. evidence that package approval, consumption acknowledgement, production acceptance, certification, and publication authorization remain distinct.

This spec defines only the inventory/package segment. Passing this slice cannot certify any format or authorize VAE Stage 5 or production.

### 10.8 Completion evidence required from a future build

A future completion receipt SHALL contain:

- exact authority, specification, schema/profile, source, and code hashes;
- FR-132 / ST-02.04 traceability;
- files-read and source-disposition receipts;
- unit, property, integration, contract, architecture, security, determinism, portability, migration, rollback, replay, and reference-slice results;
- exact pass/fail/skip counts with skip rationale;
- command/artifact/receipt/dependency atomicity proof;
- no-absolute-path scan;
- clean extracted-layout validation;
- no owner-boundary violations;
- known limitations and open productization concerns;
- candidate authority and adoption state;
- implementation/build/production/certification claim ceiling; and
- an independent audit reference.

### 10.9 Specification traceability matrix

| Requirement | Governing design | Primary acceptance evidence |
|---|---|---|
| Approved quotes/evidence/Moments/keyframes/audio/visual/tags | Sections 3.3, 6.2–6.4, 6.7 | AC-02–AC-07 |
| Archetype opportunities without ownership theft | Sections 3.5, 6.5 | AC-08, AC-09, AC-26 |
| Restrictions and lineage | Sections 3.6, 6.2, 6.7–6.9 | AC-13, AC-14, AC-20 |
| Downstream use without source rediscovery | Sections 5.6–5.7, 6.9 | AC-20, AC-21, AC-26 |
| Invalid quote rejection | Sections 3.3, 6.4, 8.1 | AC-02, AC-03 |
| No fabricated missing source | Sections 5.5, 6.8 | AC-10, AC-11 |
| Exact replay, decisions, state, and handoff | Sections 5.10, 8.7 | AC-18, AC-19, AC-27 |
| Selective recovery and historical integrity | Sections 5.8, 8.6–8.7 | AC-22, AC-23, AC-27 |
| AIR/Builder/Pipeline/VAE/Studio/Delegation boundaries | Sections 3.1, 5.7 | AC-16, AC-26 |
| Pending-ratification claim ceiling | Sections 3.9, 7.9 | AC-28 |

### 10.10 Writing-stage completion state

This document finishes exactly as:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
self_audited: false
self_accepted: false
development_capsule_issued: false
implementation_created: false
schema_or_release_bytes_created: false
```

Independent audit, revision, re-audit, adoption/ratification, build authorization, and any Development Capsule remain later governed steps.
