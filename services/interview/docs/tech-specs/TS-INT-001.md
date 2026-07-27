# TS-INT-001 — Canonical Interview Source Package and Dual Admission

```yaml
spec_id: TS-INT-001
title: Canonical Interview Source Package and Dual Admission
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Interview Expression
writing_wave: 4
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs:
  - AIR-FR-067
  - AIR-FR-068
  - AIR-FR-069
  - AIR-FR-070
  - AIR-FR-071
  - AIR-FR-072
  - FR-121
  - FR-122
  - FR-123
  - FR-125
  - FR-126
controlling_stories:
  - AIR-ST-12.01
  - AIR-ST-12.02
  - AIR-ST-12.03
  - ST-01.02
  - ST-01.03
  - ST-01.04
upstream_draft:
  spec_id: TS-AIR-008
  path: 04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-008.md
  quality_state: WRITTEN_PENDING_AUDIT
  sha256: e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0
  label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This specification is authorized for technical writing and later independent technical review only. Candidate V2.1 authority is not current authority. Nothing in this document authorizes implementation, build, product adoption, production use, certification, a Development Capsule, or a shared-contract release.

## 1. Files and authorities read

### 1.1 Governing and workflow records

The writer used the following exact records. Hashes are SHA-256 over the bytes read.

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | V3.3 writer law and ten-section structure |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_04_DISPATCH_LOCK.yaml` | 671 | `bf0ed7cf77ae548fd7262e030ee8bc4e9f28f501db28d2a06ca7bd10a62be442` | Wave, one-spec scope, and output lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact recovery packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate-authority state and claim ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-writing-only authorization |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | 134,201 | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Current source classification |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current constitutional authority |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate cross-product authority boundary |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate semantic-object ownership |

No `AGENTS.md` governs the assigned `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md` path. The recovery packet classifies it as `DIRECT_PRODUCT_SPEC_PATH`.

### 1.2 Exact upstream writing input

| File | Bytes | SHA-256 | State and treatment |
|---|---:|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-008.md` | 78,755 | `e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` |

`TS-AIR-008` supplies draft interface assumptions for the `PlannedActivativeIntelligencePack`, `InterviewAssetContract`, arming receipt, source-kind vocabulary, lineage references, planned route hypotheses, wrong-reading locks, authority-first state transitions, canonical serialization, idempotency, concurrency, replay, and selective invalidation. Those assumptions are consumed as hash-pinned draft context. They are not represented here as ratified or accepted authority.

If that exact upstream hash changes, the downstream revision-impact review MUST reopen: governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure, migration, rollback, recovery, and observability; acceptance criteria; and testing and completion evidence.

### 1.3 Requirement, assignment, evidence, and brownfield sources

| File or package member | Bytes | SHA-256 | Disposition in this specification |
|---|---:|---|---|
| AIR F12 source-package feature | 40,421 | `09f9e76096c1616125f637e2cf831fbaad0e7ef6f32e3ca972ddeef767078024` | Controlling candidate requirements `AIR-FR-067`–`AIR-FR-072` |
| Interview Expression integration amendment | 1,131 | `7afd45aaaeff5c1c0b7a82b7df113499873d045e03af0cf91ae9ad4cd1d1d074` | Candidate ownership and integration boundary |
| AHP F21 source-package feature | 18,058 | `3ec22bdc21a2fb99de44e64637ca9da52d50db5739a241b5a557733063a58d21` | Controlling candidate requirements `FR-121`–`FR-126` |
| `TS-INT-001` assignment | 3,670 | `843360ccf5d9acb1296e385885c3aa52f19270dce310b0ad44e8d429b42ce4c1` | Bounded assignment |
| Donor `TS-AIR-012-canonical-interview-source-package-and-dual-admission.md` | 27,865 | `9ab5eca69c1ffc84ff54b61c211dbfb6163bae5ed20057deefb70ec38edfd6d6` | `ADAPT`; not accepted as current architecture |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/IMPORTED_INTERVIEW_REFERENCE_SLICE_CONTRACT.yaml` | 3,115 | `3e0e0cf0c3fbcd65b93895cf8363f5c5422fa7cbe170ed06eb4114d153d2e21e` | Frozen imported-source workflow slice |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_GAP_NOTICE.yaml` | 17,743 | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Enforces no attribution to deferred unavailable sources |
| `05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS/README.md` candidate root note | 575 | `58f438c433f56a22582a5a89b05f50f5e293fe393a6b5ef36edde4bd92756b47` | Product-root intent only; no implementation claim |
| `05_FUTURE_PRODUCTS/INTERVIEW_EXPRESSION_HARNESS/CURRENT_DECISIONS.md` | 432 | `232f9ddd1372546df5ed80d6155f53d329f629cd01bf4b1ba2a603d243edf188` | Historical/brownfield context; conflicting ownership language not adopted |
| `AI2-SOURCE` contract evidence | 383 | `568fd028786e3ad87b1e65f0ee0f49dcc45b2745261e8003f3b75104f5544bd1` | Required unique evidence; source handoff compatibility |
| Candidate interview-source-package schema | 3,583 | `86b10803fdf60c6438b7d2780baba1d1d33271fb93d721bd0171dbec9717208f` | `ADAPT`; weak null/default behavior is not canonicalized |
| Candidate Reaction Receipt schema | 5,467 | `f59a1b22020d37a9e27b172cf5066d2149a39233b4cf909f17933e7db0127a0f` | Required unique evidence; later component owner remains `TS-INT-006` |
| Candidate Expression Moment schema | 3,453 | `1c870906d4b1a4facbebb8ecd3a379717e2902aac6e6095e243c0424c0fc1728` | Required unique evidence; later component owner remains `TS-INT-004` |
| `CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Required unique source/reaction doctrine evidence |
| `CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Required unique expression-capture evidence; AIR keeps archetype meaning |
| `PRM-VOC-009 Sensory Scene Anchoring` | 7,583 | `90405cef54e303ca87c2f274e6ac6a39b77cf261b86166a385e2ffb6420d5b80` | Primitive evidence; consumed by reference, not redefined |
| `PRM-VSG-003 Intent Governs Style` | 5,071 | `2be2e140588e23e43b4461c9443884b09401f6541ea29bdbae8e945e4672e30c` | Primitive evidence; preserves semantic-over-style authority |
| `EXP-FBK-001 RIM Feedback Discipline` | 6,981 | `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Feedback evidence; not promoted into source authority |
| `CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | 13,678 | `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | Required authority package; Studio projects/corrects but does not own source truth |
| Studio `expression_session.py` | 5,923 | `afce01302bb59f8b85b49bc12ea000ec74de8cd2f020707df6c6dd18e7ae316a` | `ADAPT` brownfield domain evidence |
| Studio expression-session repository | 1,441 | `3fac9930a8ba9f41be8768b03f1a06a76f75eb4d0d02027ae421cf673e9f27b5` | `ADAPT`; mutable overwrite is insufficient |
| Studio expression-session service | 24,790 | `bde10d6cd18e37cb4c8bd347654a65cec4f47eaf91f8d96f93ef1bf09b6d745b` | `ADAPT`; workflow ownership must move to Interview Expression |
| Studio expression workflow | 7,756 | `dc1588dc02daef62c9676a238d2e564b3ece31545af19f191b554022a4bb0484` | `ADAPT`; projections/corrections remain Studio-owned |
| Studio creation test | 10,256 | `0f0d04640e1c91f8f295aaed270fb014574dff455efe04a1de599bf20a3e3668` | Reusable behavioral evidence, not proof of this future contract |
| Studio moment-boundary test | 10,108 | `1d0ee6fac2dc0f18d87330993daa459d6fc5c67828713b3277c8e732ee5f9412` | Reusable invariant evidence |
| Studio PRD | 131,456 | `6534c0be726ea542e0a9821edf93c99493ebc8d957e76e80cb1799c6c8de95fd` | Brownfield context subordinate to current/candidate Program Control authority |
| Builder actor contracts | 18,625 | `9dc8aaf8aa2085aff66adda56faf891fc260287e04e0ca0c35681934126e4399` | Current integration evidence; Builder declares dependencies, not source meaning |

`SRC-EXT-017` and `SRC-EXT-023` are `DEFERRED_REFERENCE` and unavailable. No factual claim in this specification is attributed to them. `SRC-AM-002` is also deferred reference-only. `SRC-SOURCE-FIRST-001` is superseded and appears only as historical context. None is required unique evidence for writing this specification.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

The program needs one immutable source-of-record for an interview expression before downstream AIR semantic compilation, short-form or visual program generation, evaluation, correction, HumanResolution, or replay. Current and donor artifacts contain useful parts but do not establish a single governed aggregate with all of the following at once:

1. two truthful admission modes—Brief-led and imported—without inventing missing planning history;
2. exact media, transcript, speaker, timing, audio-event, shot, keyframe, visual-reference, reaction, and expression evidence identities;
3. explicit operator-declared source authority, route scope, retention, revocation, identity/voice-use, and model-training conditions without creating a new generic creative-safety or legal-approval authority;
4. epistemic state and provenance for every planned, observed, inferred, confirmed, rejected, or superseded assertion;
5. additive immutable correction and selective invalidation behavior;
6. a publication boundary that prevents an admitted but incomplete interview from masquerading as derivative-ready `interview_expression` evidence; and
7. portable serialization and replay independent of process time, random identifiers, machine paths, mutable repository state, or traversal order.

Without this aggregate, a consumer can flatten planned intent and observed evidence into generic notes, infer a Brief for an imported interview, lose exact media spans, treat operator declarations as outside metadata, publish a source with no Reaction Receipt or Expression Moment, or overwrite history during correction.

### 2.2 User outcome

An operator can admit either a planned live interview or an existing imported interview, see precisely which planning objects existed, preserve exact source and reaction evidence, and publish only a complete immutable package version. A downstream product can reproduce exactly what was admitted, distinguish planned from observed meaning, validate source-kind and provenance, and refuse stale, revoked, ambiguous, or incomplete versions without reconstructing missing semantics.

### 2.3 Solution

Interview Expression SHALL own an immutable `CanonicalInterviewSourcePackage` aggregate. The aggregate is created through one of two typed admission commands:

- `AdmitBriefLedInterviewSource`, which consumes hash-pinned AIR-owned planned objects and records them as pre-existing planning lineage; or
- `AdmitImportedInterviewSource`, which records explicit `ABSENT_NOT_CREATED` planning lineage and forbids synthesis of a Brief, Planned AIP, IAC, Matrix, anchors, planned calls, or planned routes.

Admission creates a source-root version, not automatic derivative eligibility. Later Interview Expression components bind technical alignment, keyframes, Reaction Receipts, Expression Moments, and their receipts by creating successor package versions. Only a version satisfying its publication profile can become `PUBLISHED_FOR_DERIVATIVES`.

### 2.4 In scope

- Aggregate identity, immutable versioning, canonical serialization, digesting, and portable references.
- Brief-led and imported admission invariants.
- Exact source-media and transcript-input capture.
- Exact references and typed slots for alignment, speaker, audio-event, shot, keyframe, visual, reaction, and expression components.
- Source-kind validation and `interview_expression` publication provenance.
- Planned-versus-observed epistemic state.
- Operator-supplied source-authority declaration and route-scope enforcement.
- Commands, authority envelopes, state transitions, events, receipts, idempotency, concurrency, replay, selective invalidation, revocation, supersession, rollback, and observability.
- Integration boundaries with AIR, Pipeline, Builder, VAE, Studio, Delegation, and Independent Evaluation.
- Migration disposition for current donor schemas and Studio brownfield.

### 2.5 Out of scope

- Compiling Primitive, archetype, brand, Voice DNA, Visual DNA, Matrix of Edging, role-tension, transfer, Final Script, or Visual Narrative meaning; AIR owns that work.
- Defining the full transcript/alignment engine (`TS-INT-002`), keyframe engine (`TS-INT-003`), Expression Moment contract (`TS-INT-004`), Reaction Receipt contract (`TS-INT-006`), or downstream ingredient packaging.
- Generating visual candidates, selecting models/LoRAs/conditioning, production evaluation, repair, or production acceptance; VAE owns those actions.
- Pipeline execution logic, Builder implementation, Delegation transport behavior, Studio UI behavior, HumanResolution policy, or evaluator certification.
- Granting legal rights, creative-safety approval, content-rights approval, production authority, publication authority outside the recorded operator declaration, or model-training permission beyond enforcing the supplied declaration.
- Creating canonical schemas, generated types, validators, code, tests, releases, or Development Capsules in this writing stage.

## 3. Governing decisions and constraints

### 3.1 Authority and ownership

1. The Activative System Constitution V1.1 remains current highest authority. V2.1 candidate authorities are `CANDIDATE_NOT_CURRENT` but are explicitly authorized for specification work.
2. Interview Expression owns live source admission, media/transcript evidence, observed human reaction evidence, Reaction Receipts, Expression Moments, the package aggregate, and publication of a source-evidence package.
3. AIR owns the semantic meaning and compilation of the Planned Activative Intelligence Pack, Interview Asset Contract, Primitive/archetype/brand/Voice DNA/Visual DNA, Context Premise, Resonance, Matrix, Activative Calls, Observed AIP, Activation Contract, Final Script, transfer, and semantic/visual programs.
4. A Brief-led package references AIR-owned planned objects by exact immutable ref. Interview Expression MUST NOT revise their meaning.
5. An imported package MUST NOT imply that planned objects existed. AIR may later compile semantic meaning from admitted evidence, but the source package preserves the original planning absence.
6. Builder may declare dependency and demand requirements. Pipeline may consume, validate, retrieve, execute, evaluate, and invalidate exact package versions. Neither owns or rebuilds Interview Expression source truth.
7. VAE realizes immutable visual demands and MUST NOT mutate this source package. Delegation validates and transports immutable references and shared failures; it does not become semantic or creative authority.
8. Studio may project, inspect, request correction, and carry HumanResolution actions. A correction accepted by Interview Expression creates a new package version; Studio does not overwrite canonical source truth.
9. Independent Evaluation may issue evaluation receipts. It does not alter source facts or confer source authority.
10. `Activative Contract Compiler != Activative Intelligence Runtime`. A compiler or pipeline stage cannot absorb AIR semantic ownership.

### 3.2 Operator-supplied source authority

The package records an attributable, versioned `OperatorSourceAuthorityDeclaration`. The system validates its structure and enforces its declared constraints. It does not adjudicate whether the operator legally owns material, create a generic rights authority, or invent approval status. Technical security controls remain operational controls rather than semantic approval.

The declaration MUST separately state:

- declaring actor and accountable operator authority;
- source ownership/authorization assertion and evidence refs where supplied;
- participant authorization refs or explicit absence status;
- permitted derivative formats, categories, routes, and publication scope;
- identity and voice use constraints;
- model-training eligibility as `ALLOWED`, `PROHIBITED`, or evidence-bearing `NOT_APPLICABLE` where policy permits;
- retention policy, restricted-evidence handling, expiry, and revocation terms;
- geographic/channel limitations if supplied; and
- effective version and supersession history.

Silence is never interpreted as permission. Missing required declaration fields block admission or publication according to policy; adapters cannot default them to permissive values.

### 3.3 Source-kind rule

`source_kind` is mandatory at admission and uses the governed exact vocabulary:

`interview_expression`, `public_comment`, `direct_message_reply`, `authored_source`, `live_premise`, `research_synthesis`, `operator_supplied`, `legacy_migrated`.

Unknown values are rejected. Ambiguous values are not guessed. Migration does not invent a classification. This specification’s derivative-publication profile is `interview_expression`. Non-interview kinds may be retained in the common envelope only when a later owning profile explicitly permits them.

For an `interview_expression` package to be published for derivatives, it MUST contain at least one non-empty Reaction Receipt reference and at least one non-empty Expression Moment reference. An admitted live source with no qualifying moment remains valid source history but is not derivative-eligible. This preserves the truth that an interview may not yield an Expression Moment without fabricating one.

For non-interview source kinds, interview provenance is optional but MUST validate when supplied. This specification does not certify those profiles.

### 3.4 Planned, observed, and inferred meaning

Every tag or semantic assertion reference carries one epistemic state: `PLANNED`, `OBSERVED`, `INFERRED`, `OPERATOR_CONFIRMED`, `REJECTED`, or `SUPERSEDED`. The record also carries an asserting owner, attributable actor or system, evidence source, exact span or component ref, lifecycle state, and supersession ref when applicable.

- Planned assertions come from exact AIR-owned objects; Interview Expression cannot promote them to observed.
- Observed assertions require source evidence.
- Inferred assertions remain visibly inferred until an authorized owner confirms or rejects them.
- Operator confirmation does not erase original provenance.
- Rejection and supersession are additive lifecycle facts, never destructive mutation.

### 3.5 Immutability, portability, and determinism

- Every aggregate version and receipt is immutable and content-addressed.
- IDs are deterministic from governed namespace plus canonical input or are supplied by an authorized command; implementation MUST NOT use random state for canonical identity.
- Canonical bytes use governed UTF-8 JSON, sorted map keys, stable array ordering where order is semantic, explicit time units, normalized enums, and no floating-point timestamps.
- Recorded time is command context supplied by the authority envelope and is excluded from content identity unless the contract explicitly declares it semantic.
- Portable logical locators and hashes are canonical. Absolute machine paths, temporary directories, hostnames, environment variables, or filesystem traversal order are forbidden from canonical bytes.
- A duplicate idempotency key with identical canonical command bytes returns the recorded result. The same key with different bytes fails.
- Optimistic concurrency uses the exact expected package version and digest.
- State, artifacts, events, receipts, command records, and dependency edges commit atomically.

### 3.6 `NOT_APPLICABLE`

`NOT_APPLICABLE` is a typed, evidence-bearing state, not a null, empty array, placeholder, or free text. It includes the governed policy condition, decision actor, evidence ref, and decision time. It is permitted only where the publication profile states that a component is inapplicable.

For the `interview_expression` derivative-publication profile, source media, source authority, source kind, transcript/alignment evidence, speaker/time evidence, Reaction Receipt references, and Expression Moment references are required and cannot be `NOT_APPLICABLE`. Planned object refs are not applicable only for imported admission and are represented together as `ABSENT_NOT_CREATED`, not as independent accidental nulls.

### 3.7 Wrong-reading locks and route hypotheses

For Brief-led admission, exact planned wrong-reading locks and T/V or other planned route hypotheses are referenced from the armed AIR package. They remain `PLANNED_UNCONFIRMED`. Interview Expression preserves them and records evidence; it does not reinterpret, relax, or silently confirm them.

For imported admission, Interview Expression MUST NOT manufacture planned locks or route hypotheses. Evidence-derived risks may be recorded as observations for AIR to compile later. A downstream derivative inherits applicable upstream locks through the separately governed demand and derivative-lock contracts; this source package never weakens inherited locks.

## 4. Current brownfield architecture

### 4.1 Donor specification and candidate schema

The donor `TS-AIR-012` and candidate source-package schema establish useful concepts: dual admission, package identity, media and transcript references, provenance, and immutability intent. They are not adopted byte-for-byte. The current schema permits weak defaults, nullable planned fields, and shapes that can flatten absence, pending work, and not-applicable conditions into the same representation. It also does not establish the complete aggregate commit boundary required here.

Disposition: `ADAPT`. The implementation SHALL migrate semantic values only through explicit typed conversions. No current schema is modified by this writing task.

### 4.2 Studio expression-session implementation

Studio brownfield contains reusable behaviors: explicit session states and events, receipt-like records, source ranges, quality gating, and immutable/superseded handling for approved moments. It also exposes incompatibilities with the target contract:

- random UUID and current-time generation can affect replay identity;
- a mutable overwrite repository cannot reproduce every historical version;
- separate stores risk package state without corresponding artifacts or receipts;
- broad untyped payloads can flatten provenance;
- Studio currently appears to own workflow steps that candidate ownership assigns to Interview Expression; and
- older stage labels do not establish current V2.1 authorization.

Disposition: `ADAPT_BEHAVIOR_NOT_AUTHORITY`. Studio remains a projection/correction client. Existing sessions are historical inputs to migration, not canonical package versions merely because they exist.

### 4.3 Existing source and reaction doctrine

Interview-first and expression-capture doctrine supplies required unique evidence about capturing human reaction and preserving source spans. It does not transfer AIR’s archetype or semantic compilation ownership to Interview Expression. Primitive and feedback sources remain referenced upstream evidence; this specification does not rewrite them.

### 4.4 Brownfield gaps to close

An implementation conforming to this specification needs:

1. an event-sourced immutable package repository with an atomic commit unit;
2. typed dual-admission records;
3. a typed component-slot model distinguishing pending, bound, and governed not-applicable;
4. deterministic canonical serialization and portable locator validation;
5. a package state machine with separate archive acceptance and derivative publication;
6. explicit command, authority, replay, invalidation, and revocation receipts;
7. dependency edges to every exact upstream and component version;
8. selective descendant invalidation rather than global destruction;
9. an outbox or equivalent atomic publication boundary; and
10. migrations that refuse ambiguous source kind, planning history, missing authority, or unrecoverable hashes.

### 4.5 Dependency boundary with later Interview Expression specs

This specification owns the aggregate, component slots, admission, versioning, and publication gates. It does not circularly depend on later component specs to define the aggregate root.

- `TS-INT-002` owns transcript, word/phrase timing, speaker map, time alignment, and audio-event component contracts.
- `TS-INT-003` owns shot map, keyframe, and visual-reference component contracts.
- `TS-INT-006` owns Reaction Receipt component semantics.
- `TS-INT-004` owns Expression Moment and expression-tag component semantics.

Until those component contracts are available, an admitted package carries `PENDING_REQUIRED_COMPONENT` slots. Binding a component creates a new immutable successor package version. Publication is blocked until all profile-required slots are bound and valid.

## 5. Proposed architecture and workflows

### 5.1 Component model

The bounded context contains:

- `SourceAdmissionPolicy`: selects required fields and components by admission mode and source-kind profile.
- `CanonicalInterviewSourcePackage`: immutable aggregate version and dependency root.
- `SourcePackageCommandService`: authenticates authority, validates command identity, applies the aggregate state machine, and commits atomically.
- `SourceComponentRegistryPort`: resolves exact component refs and validates owner, version, digest, lifecycle, and compatibility without copying their meaning.
- `SourcePackageRepositoryPort`: atomically stores commands, versions, events, receipts, dependency edges, and outbox records.
- `SourcePackageQueryPort`: reads a requested historical version without projecting it as current.
- `PublicationEligibilityEvaluator`: computes a deterministic eligibility result from declared profile rules and exact component refs.
- `SelectiveInvalidationProjector`: marks affected descendants stale while retaining all historical bytes.
- `OperatorAuthorityPolicyPort`: validates structure and scope of operator declarations without becoming a rights adjudicator.

### 5.2 Brief-led admission workflow

1. The operator submits `AdmitBriefLedInterviewSource` with an authority envelope, idempotency key, canonical source media inputs, transcript input if present, `source_kind=interview_expression`, an `OperatorSourceAuthorityDeclaration`, and exact refs to the AIR Brief, Planned AIP, applicable IACs, arm receipt, planned Context/Matrix/anchors/calls/tags, locks, and route hypotheses.
2. The service verifies current actor authority for source admission and checks that the referenced arm receipt binds the exact planned hashes. It does not reinterpret the planned content.
3. It validates media bytes and declared metadata, computes exact hashes, converts physical input paths to portable logical locators, and rejects absolute-path leakage.
4. It constructs `planning_lineage=PRESENT`. Each planned ref remains AIR-owned and carries its lifecycle-at-use.
5. It creates required component slots. Components already provided and verified become `BOUND`; later components become `PENDING_REQUIRED_COMPONENT` with their owning spec.
6. It records planned assertions as `PLANNED`; no value is marked observed merely because the session was armed.
7. It atomically commits the command record, source-root package version, admission event, dependency edges, receipt, and outbox intent.
8. The package enters `ADMITTED_SOURCE_ROOT` or `ALIGNMENT_PENDING`. It is not derivative-eligible.

If the live interview never produces a qualifying reaction or Expression Moment, the source remains historically reproducible and may reach `SOURCE_ARCHIVE_ACCEPTED`, but it MUST NOT reach `DERIVATIVE_ELIGIBLE` or `PUBLISHED_FOR_DERIVATIVES` under the `interview_expression` profile.

### 5.3 Imported admission workflow

1. The operator submits `AdmitImportedInterviewSource` with exact media, transcript input if available, source kind, operator authority declaration, provenance, and an explicit planning-absence attestation.
2. The command MUST list all absent planning object kinds relevant to the profile and state why they were not created. The accepted state is `ABSENT_NOT_CREATED`, never `UNKNOWN`, `EMPTY`, or a synthesized placeholder.
3. The service rejects supplied refs that pretend an imported source was Brief-led. If authentic prior planning objects exist, the operator must use the Brief-led mode or a separately governed reconciliation path.
4. The service verifies media bytes, portable locators, source authority, and provenance, then creates pending technical/evidence component slots.
5. It atomically commits the immutable source-root version and receipt.
6. `TS-INT-002` and `TS-INT-003` components may later bind alignment and visual evidence. Reaction and Expression Moment components may bind only with their owning receipts.
7. AIR may later compile semantic programs from published evidence; this does not retroactively create pre-interview planning history.

### 5.4 Component binding and correction

`BindSourcePackageComponent` receives a current package ref, expected version/digest, component kind, exact component ref, owner, compatibility profile, evidence receipt, and idempotency key.

The service:

1. resolves the component by hash;
2. verifies the component owner and allowed lifecycle state;
3. verifies that all referenced source spans belong to the same source-root lineage;
4. checks no existing immutable component is being overwritten;
5. creates a successor package version with the slot changed from pending to bound or from an older bound ref to a corrected successor ref;
6. records a dependency edge and component-bound event;
7. computes selective invalidation for descendants of the superseded component or package version; and
8. commits the new version, receipt, invalidation records, and outbox atomically.

Corrections never mutate an earlier version. A corrected transcript span, speaker assignment, keyframe, reaction, Expression Moment, source declaration, or tag assertion produces a new component and new package version. Unaffected descendants remain valid when dependency proofs show that they do not depend on the changed component.

### 5.5 Archive acceptance and derivative publication

`AcceptSourceArchive` and `PublishSourcePackageForDerivatives` are separate commands.

Archive acceptance verifies that the source itself is reproducible, authority is recorded, required original bytes are hash-locked, and the package can be inspected historically. It does not assert that the source produced an Activative result.

Derivative publication additionally verifies:

- source kind and publication profile are exact and supported;
- no required slot is pending or not applicable;
- every ref resolves to an immutable non-stale component;
- at least one non-empty Reaction Receipt ref and one non-empty Expression Moment ref exist for `interview_expression`;
- source authority and route scope permit the requested derivative profile;
- participant/identity/voice/model-training constraints are enforced as declared;
- planned refs, if present, remain the exact armed versions;
- imported planning lineage remains absent rather than reconstructed;
- tag provenance and epistemic states are complete;
- no package, component, authority declaration, or dependency is revoked, cancelled, superseded for current use, or invalidated; and
- the current expected package version/digest matches.

Successful publication emits an immutable publication receipt. It does not constitute AIR semantic acceptance, VAE production acceptance, downstream consumption acknowledgement, certification, or production authorization.

### 5.6 Consumption and acknowledgement

A consumer requests an exact published version and records an acknowledgement with consumer, purpose, compatibility profile, input digest, and dependency pin. Acknowledgement proves receipt and pinning; it does not duplicate source evaluation, semantic compilation, visual evaluation, or production acceptance.

Active downstream work remains pinned to the version accepted at its own boundary. A later package version does not silently retarget it. If a dependency is invalidated, the descendant becomes stale according to the recorded edge and cannot be newly consumed, while its historical execution remains reproducible.

### 5.7 Revocation, cancellation, and supersession

- `CancelSourceAdmission` applies before publication and creates a terminal successor state while preserving earlier events.
- `RevokeSourceAuthority` creates a new authority-declaration version and invalidates newly prohibited uses. It never deletes historical evidence.
- `SupersedeSourcePackage` links an exact replacement package version and blocks new use of the superseded current version.
- `InvalidateSourcePackageDescendants` records reason, authority, scope, and exact affected descendants.
- Post-completion invalidation marks results non-consumable for new work but preserves the exact package, result, receipts, evaluator context, and dependency graph needed for reproduction.

### 5.8 State machine

Allowed package states are:

`ADMITTED_SOURCE_ROOT`, `ALIGNMENT_PENDING`, `EVIDENCE_PENDING`, `SOURCE_ARCHIVE_ACCEPTED`, `DERIVATIVE_ELIGIBLE`, `PUBLISHED_FOR_DERIVATIVES`, `BLOCKED_CONSTRAINT_CONFLICT`, `CANCELLED`, `SUPERSEDED`, and `REVOKED`.

Key transition rules:

- admission enters `ADMITTED_SOURCE_ROOT` or `ALIGNMENT_PENDING`;
- required technical components pending leads to `ALIGNMENT_PENDING`;
- alignment complete but reaction/expression evidence missing leads to `EVIDENCE_PENDING`;
- archive criteria may lead to `SOURCE_ARCHIVE_ACCEPTED` independently of derivative eligibility;
- deterministic eligibility evaluation creates a successor in `DERIVATIVE_ELIGIBLE`;
- authorized publication creates `PUBLISHED_FOR_DERIVATIVES`;
- a constraint conflict creates `BLOCKED_CONSTRAINT_CONFLICT`, never partial publication;
- correction supersedes the prior current version but retains it for history;
- cancellation and revocation are explicit events and do not delete bytes.

No state transition is inferred from the mere presence of a field. Every transition requires a command, authority decision, expected version, deterministic policy result, and receipt.

## 6. Data models, contracts, schemas, and APIs

The following are normative logical shapes. They are not schema-release bytes and do not authorize creating or modifying canonical schemas in this prompt.

### 6.1 Common values

```text
ImmutableRef {
  object_type: governed non-empty identifier
  object_id: governed non-empty identifier
  version: positive integer or governed semantic version
  sha256: lowercase 64-hex digest
  owner: governed product identifier
  lifecycle_state_at_use: governed enum
  compatibility_profile_id: optional governed identifier
}

PortableArtifactRef {
  logical_uri: relative or governed content URI
  sha256: lowercase 64-hex digest
  bytes: non-negative integer
  media_type: governed MIME value
  container_profile: optional governed identifier
}
```

`logical_uri` MUST reject drive-qualified paths, UNC paths, leading `/`, `..` traversal, environment substitutions, and host-local temp locations. Consumers resolve it through an injected content store; the canonical package never stores a host path.

### 6.2 Admission record

```text
SourceAdmissionRecord {
  admission_id: deterministic identifier
  admission_mode: BRIEF_LED | IMPORTED
  source_kind: governed source-kind enum
  source_root_id: deterministic identifier
  media_manifest: SourceMediaManifest
  transcript_input: TranscriptInput
  planning_lineage: PresentPlanningLineage | AbsentPlanningLineage
  source_authority: OperatorSourceAuthorityDeclarationRef
  provenance: non-empty ProvenanceAssertion[]
  admitted_by: ActorAuthorityRef
  command_id: deterministic identifier
  command_record_ref: ImmutableRef
}
```

`PresentPlanningLineage` requires exact AIR-owned refs for the Brief, Planned AIP, applicable IACs, and arm receipt. Context Premise, Resonance, Matrix, anchors, calls, tags, locks, and routes are recorded as exact refs when applicable under the armed plan. A package MUST NOT copy them into editable Interview Expression fields.

`AbsentPlanningLineage` requires:

```text
AbsentPlanningLineage {
  state: ABSENT_NOT_CREATED
  absent_object_types: non-empty governed object-type set
  reason_code: SOURCE_PREEXISTED_PROGRAM | EXTERNAL_IMPORT | LEGACY_CAPTURE | OTHER_ATTESTED
  operator_attestation: ImmutableRef
  evidence_refs: ImmutableRef[]
}
```

The absent-object set is canonical-sorted and MUST include every required planning object kind that did not exist. Missing information is not represented as `ABSENT_NOT_CREATED`; ambiguity blocks admission.

### 6.3 Media manifest and transcript input

```text
SourceMediaEntry {
  role: PRIMARY_VIDEO | PRIMARY_AUDIO | AUXILIARY_AUDIO | AUXILIARY_VIDEO | SOURCE_DOCUMENT
  artifact: PortableArtifactRef
  original_filename_evidence: optional string excluded from canonical identity
  duration_ticks: non-negative integer
  timebase_numerator: positive integer
  timebase_denominator: positive integer
  channels: optional positive integer
  width: optional positive integer
  height: optional positive integer
  ingest_provenance_ref: ImmutableRef
}

SourceMediaManifest {
  entries: non-empty canonical ordered SourceMediaEntry[]
  manifest_sha256: digest of canonical entries
}

TranscriptInput {
  state: PROVIDED_UNALIGNED | PROVIDED_ALIGNED_COMPONENT | PENDING_TRANSCRIPTION
  artifact_ref: optional PortableArtifactRef
  aligned_component_ref: optional ImmutableRef
  language_declaration: governed value with provenance
}
```

Mutually exclusive fields are rejected. Transcript input is not equivalent to an accepted alignment component.

### 6.4 Operator source-authority declaration

```text
OperatorSourceAuthorityDeclaration {
  declaration_id: deterministic identifier
  version: positive integer
  declared_by: ActorAuthorityRef
  source_authority_assertion: governed enum plus evidence refs
  participant_authorization_refs: ImmutableRef[] | EvidenceBearingNotApplicable
  permitted_derivative_formats: canonical governed identifier set
  permitted_categories: canonical governed identifier set
  permitted_routes: canonical governed identifier set
  publication_scope: governed scope set
  identity_use: ALLOWED_WITH_CONSTRAINTS | PROHIBITED | NOT_APPLICABLE_WITH_EVIDENCE
  voice_use: ALLOWED_WITH_CONSTRAINTS | PROHIBITED | NOT_APPLICABLE_WITH_EVIDENCE
  model_training_eligibility: ALLOWED | PROHIBITED | NOT_APPLICABLE_WITH_EVIDENCE
  retention_policy_ref: ImmutableRef
  restricted_evidence_policy_ref: optional ImmutableRef
  effective_at: authority-supplied timestamp
  expires_at: optional authority-supplied timestamp
  revocation_policy_ref: ImmutableRef
  limitations: structured non-permissive constraints
  supersedes: optional ImmutableRef
}
```

An adapter MUST NOT translate missing scope into `all`, missing eligibility into `ALLOWED`, or missing participant evidence into approval.

### 6.5 Component slot

```text
ComponentSlot =
  BoundComponent {
    state: BOUND
    component_kind: governed enum
    component_ref: ImmutableRef
    binding_receipt_ref: ImmutableRef
  }
| PendingRequiredComponent {
    state: PENDING_REQUIRED_COMPONENT
    component_kind: governed enum
    owning_spec_id: governed identifier
    reason_code: governed enum
  }
| EvidenceBearingNotApplicable {
    state: NOT_APPLICABLE
    component_kind: governed enum
    policy_ref: ImmutableRef
    decision_actor: ActorAuthorityRef
    evidence_refs: non-empty ImmutableRef[]
  }
```

Governed component kinds include `TRANSCRIPT_ALIGNMENT`, `WORD_TIMING`, `PHRASE_TIMING`, `SPEAKER_MAP`, `TIME_ALIGNMENT`, `AUDIO_EVENT_MAP`, `SHOT_MAP`, `KEYFRAME_SET`, `VISUAL_REFERENCE_SET`, `REACTION_RECEIPT_SET`, `EXPRESSION_MOMENT_SET`, and `EXPRESSION_TAG_ASSERTION_SET`.

A slot cannot change in place. A component correction binds a successor ref on a successor package version.

### 6.6 Tag assertion ref

```text
TagAssertionRef {
  tag_id: governed identifier
  tag_version: governed version
  epistemic_state: PLANNED | OBSERVED | INFERRED | OPERATOR_CONFIRMED | REJECTED | SUPERSEDED
  semantic_owner: governed product identifier
  asserted_by: ActorOrSystemRef
  source_component_ref: ImmutableRef
  source_span_ref: optional ImmutableRef
  evidence_refs: ImmutableRef[]
  lifecycle_state: governed enum
  supersedes: optional ImmutableRef
}
```

Generic note fields cannot substitute for this record. An adapter that cannot preserve all required fields fails closed.

### 6.7 Package version

```text
CanonicalInterviewSourcePackageVersion {
  package_id: deterministic identifier
  version: positive integer
  previous_version_ref: optional ImmutableRef
  root_admission_ref: ImmutableRef
  admission_mode: BRIEF_LED | IMPORTED
  source_kind: governed source-kind enum
  media_manifest_ref: ImmutableRef
  transcript_input_ref: ImmutableRef
  planning_lineage: PresentPlanningLineage | AbsentPlanningLineage
  source_authority_declaration_ref: ImmutableRef
  component_slots: canonical map<ComponentKind, ComponentSlot>
  tag_assertion_refs: canonical ordered ImmutableRef[]
  planned_wrong_reading_lock_refs: canonical ordered ImmutableRef[]
  planned_route_hypothesis_refs: canonical ordered ImmutableRef[]
  dependency_edges: canonical ordered DependencyEdge[]
  lifecycle_state: PackageState
  compatibility_profile_id: governed identifier
  publication_profile_id: governed identifier
  created_by_command_ref: ImmutableRef
  package_sha256: digest of canonical content excluding itself
}
```

Brief-led mode requires planned lock and route references when present in the armed plan. Imported mode forbids fabricated planned refs. An empty list is valid only when the exact upstream plan proves none were defined; absence of proof blocks publication.

### 6.8 Commands

Commands use a common envelope:

```text
CommandEnvelope {
  command_id: deterministic identifier
  idempotency_key: non-empty string
  actor_authority_ref: ImmutableRef
  expected_package_version: optional positive integer
  expected_package_sha256: optional digest
  requested_at: authority-supplied timestamp
  correlation_id: non-empty identifier
  causation_id: optional identifier
  payload_sha256: digest of canonical payload
}
```

Normative commands:

- `AdmitBriefLedInterviewSource`
- `AdmitImportedInterviewSource`
- `BindSourcePackageComponent`
- `RecordTagAssertion`
- `AcceptSourceArchive`
- `EvaluateDerivativeEligibility`
- `PublishSourcePackageForDerivatives`
- `AcknowledgeSourcePackageConsumption`
- `CorrectSourcePackageComponent`
- `SupersedeSourcePackage`
- `InvalidateSourcePackageDescendants`
- `CancelSourceAdmission`
- `RevokeSourceAuthority`

No command accepts a generic patch document. Every mutation intent is typed, authority-scoped, and additive.

### 6.9 Events and receipts

Normative events include `BriefLedSourceAdmitted`, `ImportedSourceAdmitted`, `SourceComponentBound`, `TagAssertionRecorded`, `SourceArchiveAccepted`, `DerivativeEligibilityEvaluated`, `SourcePackagePublished`, `SourcePackageConsumptionAcknowledged`, `SourcePackageCorrected`, `SourcePackageSuperseded`, `SourcePackageDescendantsInvalidated`, `SourceAdmissionCancelled`, and `SourceAuthorityRevoked`.

Every command result receipt contains:

- command and idempotency identity;
- actor authority and decision;
- prior and resulting package refs;
- exact artifact/component/dependency refs read;
- policy and compatibility profile versions;
- canonical result digest;
- event and outbox refs;
- affected descendant refs for invalidation;
- failure code and context if rejected; and
- replay equivalence proof fields.

Receipt creation is part of the same atomic commit as the resulting package version. No package state exists without its command/event/receipt, and no success receipt exists without the corresponding artifact.

### 6.10 Query APIs

The logical API exposes:

- `get_package(package_id, version, sha256) -> exact historical version`
- `get_current_package(package_id) -> current ref plus lifecycle state`
- `get_admission(admission_id) -> exact admission record`
- `list_package_versions(package_id, cursor) -> ordered immutable refs`
- `resolve_component(package_ref, component_kind) -> slot and exact component ref`
- `evaluate_publication(package_ref, profile_id) -> deterministic eligibility report`
- `list_descendants(ref, edge_type, cursor) -> exact dependency refs`
- `verify_replay(package_ref) -> replay-equivalence receipt`

Current queries never substitute for exact-version queries. A request for an unknown or mismatched hash fails rather than returning the latest version.

## 7. Implementation stages and exact target paths

This section is a future implementation plan, not implementation authorization. Paths are reserved under the intended Interview Expression product root; no listed file is created by this writing task.

### 7.1 Stage A — Domain values and aggregate

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/source_package.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/source_admission.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/source_authority.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/source_components.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/tag_assertion_ref.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/package_state.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/failures.py`

Implement immutable values, canonical normalization, dual-admission union, component-slot union, lifecycle transitions, and authority-preserving invariants. Domain constructors receive deterministic IDs and command time; they do not read the clock, environment, random state, or filesystem.

### 7.2 Stage B — Ports and atomic persistence

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/source_package_repository.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/source_component_registry.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/operator_authority_policy.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/content_store.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/repositories/event_sourced_source_package_repository.py`

Define one transaction boundary over command records, events, package versions, receipts, dependencies, idempotency records, invalidation records, and outbox messages. The port MUST expose compare-and-swap on expected version/digest. A reference implementation may be in memory for tests but must enforce the identical atomicity and historical-read contract.

### 7.3 Stage C — Application services

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/admission_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/component_binding_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/publication_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/invalidation_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/replay_service.py`

Services orchestrate ports and domain commands. They do not embed AIR semantic compilation, VAE production policy, Studio UI policy, Delegation routing, or evaluator certification.

### 7.4 Stage D — Adapters

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/air_planned_interview_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/imported_source_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/pipeline_source_package_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/studio_projection_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/delegation_envelope_adapter.py`

Adapters preserve every required field, owner, version, digest, epistemic state, lifecycle state, lock, route, authority constraint, and dependency edge. Parsing without enforcement is non-conformant. An adapter that cannot preserve a required value returns a typed incompatibility failure; it may not flatten the value into notes.

### 7.5 Stage E — Candidate contracts and migrations

Potential future paths, subject to separate canonical-schema authority:

- `06_INTERVIEW_EXPRESSION/contracts/schemas/canonical-interview-source-package.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/source-admission-command.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/source-package-receipt.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/migrations/source-package-v1-to-v2.yaml`

No schema is created now. A later authorized contract-writing step MUST reconcile these shapes with the accepted `TS-INT-002`, `TS-INT-003`, `TS-INT-004`, and `TS-INT-006` interfaces before release bytes are produced.

### 7.6 Stage F — Tests and fixtures

Proposed paths:

- `06_INTERVIEW_EXPRESSION/tests/unit/test_dual_admission.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_source_kind_and_provenance.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_component_slots.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_package_state_machine.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_canonical_serialization.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_operator_source_authority.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_atomic_commit_and_rollback.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_replay_and_idempotency.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_selective_invalidation.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_portable_package_export.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/test_air_planned_interview_mapping.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/test_pipeline_consumption_mapping.py`

### 7.7 Dependency sequencing

This spec can be implemented only after its authority/adoption and build gates are separately satisfied. Component integration waits for accepted component interfaces, but the aggregate root and pending-slot model prevent a writing-time cycle.

Implementation sequencing after authorization:

1. domain and canonical serialization;
2. ports and atomic repository;
3. admission services;
4. component binding and publication eligibility;
5. adapters against accepted upstream/component contracts;
6. migration tooling;
7. complete unit, integration, contract, replay, portability, and fault-injection evidence.

No downstream consumer may assume this written draft is a released interface.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

Failures use stable codes with command ID, correlation ID, actor, package ref, expected/observed version, dependency refs, policy version, and retryability. Minimum codes:

- `INT_SOURCE_KIND_MISSING`
- `INT_SOURCE_KIND_UNKNOWN`
- `INT_SOURCE_KIND_AMBIGUOUS`
- `INT_PLANNING_LINEAGE_CONTRADICTORY`
- `INT_IMPORTED_PLANNING_HISTORY_INVENTED`
- `INT_BRIEF_LED_REQUIRED_REF_MISSING`
- `INT_ARMED_PLAN_HASH_MISMATCH`
- `INT_SOURCE_AUTHORITY_MISSING`
- `INT_SOURCE_AUTHORITY_SCOPE_DENIED`
- `INT_PARTICIPANT_EVIDENCE_REQUIRED`
- `INT_MEDIA_HASH_MISMATCH`
- `INT_NONPORTABLE_ARTIFACT_LOCATOR`
- `INT_COMPONENT_OWNER_MISMATCH`
- `INT_COMPONENT_HASH_MISMATCH`
- `INT_COMPONENT_SOURCE_LINEAGE_MISMATCH`
- `INT_REQUIRED_COMPONENT_PENDING`
- `INT_NOT_APPLICABLE_FORBIDDEN`
- `INT_INTERVIEW_REACTION_RECEIPT_REQUIRED`
- `INT_INTERVIEW_EXPRESSION_MOMENT_REQUIRED`
- `INT_TAG_PROVENANCE_INCOMPLETE`
- `INT_STALE_PACKAGE_VERSION`
- `INT_OPTIMISTIC_CONCURRENCY_CONFLICT`
- `INT_IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD`
- `INT_DEPENDENCY_REVOKED`
- `INT_CONSTRAINT_CONFLICT`
- `INT_ATOMIC_COMMIT_FAILED`
- `INT_REPLAY_DIVERGENCE`
- `INT_MIGRATION_AMBIGUOUS`
- `INT_MIGRATION_LOSSY`

No failure is converted to a successful partial package. The failure receipt may be stored atomically with the rejected command record but MUST NOT imply creation of a package version.

### 8.2 Atomic rollback

The transaction rolls back if any package artifact, event, receipt, dependency edge, idempotency record, invalidation record, or outbox intent fails to persist. Retrying the same command after an unknown outcome uses the idempotency record to return the committed result or safely rerun when no commit exists.

There is no compensating delete of canonical history. If an external content-store object was staged before transaction commit, it remains unreferenced and is cleaned only by a separate garbage-collection policy that proves no canonical ref points to it.

### 8.3 Replay and historical reproduction

Replay reads exact command records and governed policy/compatibility versions in event order. It MUST reproduce identical canonical package bytes and digest in a fresh process with a clean repository projection. Replay cannot call the current clock, generate a UUID, enumerate directories without sorting, depend on environment variables, or resolve an absolute machine path.

Historical queries remain possible after cancellation, supersession, invalidation, or revocation. A historical record is returned with its lifecycle and non-consumability state; it is never silently upgraded to the replacement version.

### 8.4 Selective invalidation

Each dependency edge identifies upstream ref, downstream ref, edge type, fields consumed, and invalidation policy. A correction computes descendants from the changed exact ref. It invalidates only descendants whose consumed fields intersect the change scope, while preserving unaffected results.

Examples:

- a corrected speaker span invalidates Expression Moments and downstream programs using that span, not unrelated moments;
- a source-authority revocation scoped to model training blocks training descendants without falsely invalidating an allowed archival projection;
- a corrected planned AIR ref reopens Brief-led package eligibility and descendants that consumed that planned field;
- a new package version does not invalidate an active historical delegation pinned to an unchanged prior version unless an explicit revocation/invalidation rule applies.

### 8.5 Migration

Migration creates new immutable artifacts; it never overwrites donor files or current package history.

The migrator MUST:

1. hash-lock the source artifact and record its schema/profile;
2. determine source kind from explicit evidence or stop with `INT_MIGRATION_AMBIGUOUS`;
3. distinguish authentic planned refs from absent planning history;
4. convert null/default fields into a valid typed state only with evidence;
5. preserve every source ref, span, owner, epistemic state, lifecycle, lock, route, authority constraint, and supersession link;
6. reject absolute-path-only evidence until bytes are imported into a portable content store;
7. emit a field-by-field migration receipt and losslessness proof; and
8. leave the original artifact unchanged and historically addressable.

If a required value cannot be recovered, migration is explicitly blocked. It cannot invent source classification, participant approval, planned intent, Reaction Receipts, Expression Moments, or hashes.

### 8.6 Recovery

Recovery uses the canonical event log plus content-addressed artifacts. Projections are disposable. After a crash, the service reconciles outbox entries against committed transaction IDs, republishes only unacknowledged events, and verifies package/event/receipt linkage before becoming writable.

A quarantined state is required when digest verification or replay diverges. Operators receive the exact first divergent event and expected/observed hashes. Quarantine never substitutes a newer package or suppresses history.

### 8.7 Observability

Metrics and structured logs MAY expose identifiers and state but MUST avoid raw transcript text, restricted evidence, voice data, participant PII, or media bytes. Required signals include:

- admission attempts/success/failure by mode and failure code;
- package state transition counts;
- pending component age by kind;
- publication eligibility failures by rule;
- optimistic concurrency and idempotency conflicts;
- replay and digest divergence;
- invalidation fan-out and processing latency;
- outbox lag and recovery count; and
- attempted nonportable locator or permissive-default violations.

Every log includes correlation ID, command ID, package ID/version, and policy/profile versions. Security/audit access to restricted evidence is itself recorded through an operational access-control layer.

## 9. Behavior-specific acceptance criteria

The following criteria are prerequisites for later independent acceptance. They are not asserted as passed by this writer.

1. A valid Brief-led command with exact AIR Brief, Planned AIP, IAC, arm receipt, source media, authority declaration, and provenance creates one immutable source-root package and one linked success receipt.
2. A Brief-led command with any planned-object digest differing from the arm receipt fails `INT_ARMED_PLAN_HASH_MISMATCH` and creates no package version.
3. A valid imported command creates `planning_lineage.state=ABSENT_NOT_CREATED` and does not synthesize a Brief, Planned AIP, IAC, Matrix, anchor, call, lock, route, or tag.
4. An imported command with ambiguous planning history fails rather than choosing an admission mode.
5. Missing, unknown, or ambiguous source kind fails with its typed code; no migration or adapter guesses it.
6. Every admitted media artifact is addressed by exact digest, bytes, media type, and portable logical URI. Absolute, UNC, traversal, environment-derived, or temporary paths are rejected.
7. `PENDING_REQUIRED_COMPONENT`, `BOUND`, and evidence-bearing `NOT_APPLICABLE` remain distinguishable through serialization, adapters, replay, and queries.
8. A required `interview_expression` component cannot be marked `NOT_APPLICABLE`.
9. A source with no qualifying human reaction or Expression Moment can be archive-accepted when reproducible, but cannot become derivative-eligible or published.
10. Publication of `interview_expression` fails unless at least one non-empty Reaction Receipt ref and at least one non-empty Expression Moment ref resolve and validate.
11. Non-interview source kinds do not require interview provenance unless supplied; supplied refs are fully validated.
12. Planned, observed, inferred, operator-confirmed, rejected, and superseded assertions retain distinct epistemic states, source spans, owners, actors, evidence, and lifecycle.
13. Interview Expression cannot alter AIR-owned semantic content; it can only preserve exact refs and record source/reaction evidence.
14. An adapter that cannot preserve a required lineage field, owner, lock, route, authority constraint, or epistemic state fails closed instead of flattening it into generic notes.
15. Operator source-authority constraints are enforced exactly; missing values never default to permission, certification, or approval.
16. Binding or correcting a component creates a successor package version and leaves the prior version byte-readable.
17. Correction records exact changed fields and invalidates only dependent descendants. Unaffected descendants remain usable when proven independent.
18. Expected-version or digest mismatch produces an optimistic concurrency failure without partial state.
19. An identical idempotent retry returns the original package and receipt refs; a changed payload under the same key fails.
20. Fault injection at every persistence boundary proves no package without a receipt, no receipt without its package, no missing command record, no missing dependency edge, and no outbox message for a rolled-back command.
21. Replay in a fresh process produces the exact package bytes and digest without current time, random state, insertion order, traversal order, environment, or machine path.
22. Cancellation, supersession, invalidation, and revocation preserve historical package, event, receipt, and dependency bytes while blocking prohibited new consumption.
23. Downstream acknowledgement records exact consumption but does not become source acceptance, semantic acceptance, visual production acceptance, certification, or production authorization.
24. Brief-led planned wrong-reading locks and route hypotheses remain exact `PLANNED_UNCONFIRMED` refs until their owning authority changes state. Imported admission does not invent them.
25. Migration from each supported donor shape emits a new artifact and losslessness receipt; ambiguity or information loss blocks migration.
26. Package publication and query behavior are compatible with a content-addressed clean extracted layout and contain no absolute source-machine path.
27. All events, commands, receipts, package versions, component refs, and invalidations use one traceable correlation/causation chain.
28. The implementation contains no AIR semantic compiler, VAE production planner, Studio canonical workflow owner, Delegation creative authority, or generic rights/safety approval authority.
29. All 11 controlling FRs and six controlling Stories are traceable to executable tests and completion evidence.
30. Product eligibility, certification, build authorization, and production authorization remain false unless later distinct governed receipts change them.

## 10. Testing and completion evidence

### 10.1 Required test suites

**Domain property tests**

- Generate valid and invalid dual-admission combinations and prove their union is exhaustive and exclusive.
- Prove immutable version monotonicity and prior-byte preservation.
- Prove component-slot transitions reject overwrite and invalid `NOT_APPLICABLE`.
- Prove tag epistemic state and provenance survive canonical round trips.
- Prove state-machine transitions are closed over the governed transition table.

**Determinism tests**

- Serialize logically identical maps with varied insertion order and receive identical bytes.
- Run in fresh processes with different locale, timezone, environment, temp root, hash seed, and working directory and receive identical digests.
- Shuffle filesystem discovery input and prove canonical sorting or fail if traversal order reaches identity.
- Freeze authority-supplied command time and prove no system clock read affects bytes.
- Reject random canonical IDs and absolute path leakage.

**Admission contract tests**

- Exercise complete Brief-led and imported fixtures.
- Exercise absent-versus-unknown planning lineage.
- Verify exact `TS-AIR-008` mapping for planned refs, arming receipt, locks, routes, and source-kind assumptions after that spec is accepted/adopted.
- Verify imported admission cannot accept fake planned refs.
- Verify source-authority declarations fail closed for missing scope.

**Component and publication tests**

- Bind each component kind with correct and incorrect owner/hash/source lineage.
- Prove archive acceptance differs from derivative publication.
- Prove `interview_expression` needs both Reaction Receipt and Expression Moment refs.
- Prove a no-moment interview remains valid archival history without fabricated evidence.
- Prove non-interview optional provenance validates when present.

**Repository and fault-injection tests**

- Fail before and after each artifact, event, receipt, dependency, idempotency, invalidation, and outbox write.
- Verify rollback leaves no inconsistent subset.
- Verify replay after commit-acknowledgement loss returns the original result.
- Verify expected-version conflicts under concurrent commands.
- Verify historical reads after correction, invalidation, supersession, cancellation, and revocation.

**Selective invalidation tests**

- Build dependency graphs with shared and independent descendants.
- Change one transcript span, one speaker mapping, one keyframe, one source-authority scope, and one planned ref separately.
- Verify only field-dependent descendants become stale and all invalidation receipts list exact causes.

**Portability and security tests**

- Export and import a package into a clean extracted layout on a different root.
- Scan canonical artifacts and receipts for drive letters, UNC prefixes, source checkout paths, temporary paths, usernames, and environment values.
- Fuzz archive names and logical locators for traversal, symlink escape, case collision, duplicate member, decompression-bomb, and hash-confusion behavior.
- Verify logs and metrics do not expose restricted transcript/media or participant data.

**Migration tests**

- Migrate every declared donor schema/profile through exact fixtures.
- Verify field-by-field equivalence and explicit blocked results for missing source kind, missing bytes, ambiguous planning history, unprovable authority, or lossy provenance.
- Verify migration produces new immutable artifacts and leaves donors unchanged.

### 10.2 Required fixtures

Minimum fixtures include:

1. complete Brief-led package with multiple IACs, planned locks, route hypotheses, reaction evidence, and Expression Moments;
2. Brief-led interview with no qualifying reaction/moment;
3. imported video plus transcript with explicit absent planning history;
4. imported video without transcript, remaining alignment-pending;
5. ambiguous source-kind migration blocked;
6. corrupted media digest;
7. absolute and traversing artifact locators;
8. stale component and package versions;
9. correction with one affected and one unaffected descendant;
10. revocation scoped to publication, identity use, voice use, and model training;
11. idempotent retry after unknown commit outcome; and
12. clean-room replay/export fixture.

Fixture expectations are exact digests and typed outcomes, not merely schema parsing.

### 10.3 Completion evidence required from a future build

A later authorized build cannot claim completion without:

- source and build manifests with exact hashes;
- unit, property, integration, contract, migration, fault-injection, replay, portability, security, and performance results;
- command/event/receipt/artifact atomicity matrix;
- deterministic fresh-process reproduction report;
- selective-invalidation graph evidence;
- absolute-path scan;
- clean extracted-layout validation;
- adapter field-preservation matrix;
- migration losslessness or blocked-fixture evidence;
- product-owner adoption and candidate-authority ratification as required for build acceptance;
- independent audit, bounded revision where needed, independent re-audit, and an attributable acceptance receipt; and
- explicit statements that certification and production eligibility remain false unless separately proven and authorized.

### 10.4 Performance evidence

Performance targets are not invented in this draft. A future implementation SHALL measure canonical serialization, admission, component binding, publication evaluation, exact-version query, replay, and invalidation fan-out on governed fixture sizes. Any service-level objective requires an attributable product decision. Correctness, authority, provenance, and atomicity cannot be relaxed to meet an ungoverned threshold.

### 10.5 Traceability summary

| Requirement | Primary behavior | Primary sections |
|---|---|---|
| `AIR-FR-067` | Brief-led package binds planned objects and observed evidence without collapsing ownership | 3, 5, 6, 9, 10 |
| `AIR-FR-068` | Imported package records planning absence without fabrication | 3, 5, 6, 9, 10 |
| `AIR-FR-069` | Exact hashes/versions for source, transcript, timing, speakers, audio, shots, keyframes, and visual refs | 5, 6, 8, 9, 10 |
| `AIR-FR-070` | Tag provenance and epistemic state | 3, 6, 9, 10 |
| `AIR-FR-071` | Additive correction versions and selective descendants | 5, 6, 8, 9, 10 |
| `AIR-FR-072` | Operator source authority and route scope without new creative-policy authority | 3, 5, 6, 8, 9 |
| `FR-121` | Immutable package binds all accepted evidence and provenance for derivatives | 2, 5, 6, 9, 10 |
| `FR-122` | Brief-led admission preserves planned separately from observed; no fabricated moment | 3, 5, 6, 9, 10 |
| `FR-123` | Imported admission does not pretend planning artifacts existed | 3, 5, 6, 8, 9 |
| `FR-125` | Versioned operator-declared source authority and usage constraints | 3, 5, 6, 8, 9 |
| `FR-126` | Corrections create immutable versions and selective invalidation | 5, 6, 8, 9, 10 |

### 10.6 Draft dependency impact and lifecycle handoff

This specification consumed `TS-AIR-008` at SHA-256 `e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0`, state `WRITTEN_PENDING_AUDIT`, label `DRAFT_DEPENDENCY_NOT_ACCEPTED`. If that draft changes, the recorded downstream revision-impact sections MUST reopen before this spec can proceed through re-audit.

The next lifecycle action is independent audit by an agent that did not write this specification. The writer has not audited, revised, accepted, implemented, built, released, or issued a Development Capsule for this document.
