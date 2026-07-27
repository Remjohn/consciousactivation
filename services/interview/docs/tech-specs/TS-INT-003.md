# TS-INT-003 — Shot Boundary, Transition, Keyframe, and Visual Reference Index

```yaml
spec_id: TS-INT-003
title: Shot Boundary, Transition, Keyframe, and Visual Reference Index
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Interview Expression
writing_wave: 5
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs: [FR-129]
controlling_stories: [ST-02.02]
upstream_draft:
  spec_id: TS-INT-001
  path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md
  quality_state: WRITTEN_PENDING_AUDIT
  sha256: ca13c9fdcc3b840533de2a955a5388497a434a0b7f94950978012536fd4301e8
  label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This candidate specification is authorized for writing and later independent technical review only. It is not current product authority, a canonical schema release, an implementation authorization, build readiness, product certification, or production authority. It defines the visual-evidence input to later Expression Moment derivation; it does not discover, approve, rank, or route Expression Moments.

## 1. Files and authorities read

### 1.1 Workflow, authority, and dispatch inputs

The writer read the following exact bytes. All hashes are SHA-256.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current V3.3 writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_05_DISPATCH_LOCK.yaml` | 1,205 | `e135a1ddce50c52c3a03901cde6feb257c8cf73dc9f81eb02df2484d2a7ad2bf` | Wave 5 output and upstream lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact one-spec recovery packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate-authority state and claim ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-work-only authorization |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current constitutional authority |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product authority boundaries |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate semantic-object ownership |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | 1,621 | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Reserved Interview Expression product-root intent; no build authority |

No `AGENTS.md` applies to `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-003.md`. The recovery packet classifies the exact target as `DIRECT_PRODUCT_SPEC_PATH` and permits no second spec or product file.

### 1.2 Reconciliation, requirement, Story, and source controls

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Canonical ID, title, owner, and output path |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | `FR-129` ownership and behavior |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | `FR-129` → `ST-02.02` → `TS-INT-003` trace |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | 134,201 | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Current source classification |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_GAP_NOTICE.yaml` | 17,743 | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Deferred external-source handling |
| AHP `governance/CURRENT_WRITING_PROFILE.md` | 11,536 | `ba88c5572ae3f7571daac9991a0d325a20f491cb9c0ea7c3816deb3ff3d32956` | Candidate source-first, CBAR, ownership, and evidence laws |
| AHP `prd/features/F22-activative-tags-expression-moments-keyframes-and-asset-package-spec.md` | 17,347 | `d93b5c4fb09d6ba3f35cf84a2206b1100fa457abf94acd384ca703dc4ca5cd6e` | Controlling `FR-129` |
| AHP `planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553 | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | Controlling `ST-02.02` and CBAR conditions |
| AHP `planning/spec_assignments/TS-INT-003.md` | 2,606 | `515298c9f8819ebc2cc25542c2a3c5810209b24babe428fe4315a977085ffa6b` | Bounded assignment; assignment target path superseded by canonical ledger path |
| AHP `sources/EXACT_SOURCE_REUSE_CROSSWALK.csv` | 21,449 | `c8c97f5d2003d070180a7061484609b2f9c8ef990efa116914f05b4e400e7820` | Source reuse/disposition check; no unlisted code adoption |

The controlling requirement is `FR-129`: detect existing shot boundaries and transitions, sample representative and expression-relevant keyframes, record camera/framing changes, and expose visual references without treating shot changes as semantic importance. The controlling Story is `ST-02.02`: provide inspectable source shots, transitions, and keyframes while preserving the rule that visual change does not itself become content meaning.

### 1.3 Upstream draft and admitted evidence

| File or source | Bytes | SHA-256 | State and treatment |
|---|---:|---|---|
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md` | 71,751 | `ca13c9fdcc3b840533de2a955a5388497a434a0b7f94950978012536fd4301e8` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` |
| AIR bundle `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; interview/source doctrine |
| `THE_CMF_STUDIO(2)/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | 131,456 | `6534c0be726ea542e0a9821edf93c99493ebc8d957e76e80cb1799c6c8de95fd` | Hash-locked brownfield product evidence; `ADAPT`, not current authority |

`TS-INT-001` supplies the draft aggregate interface: exact source-media identity, portable artifact refs, rational timebase, immutable package versions, component slots, `SHOT_MAP`, `KEYFRAME_SET`, and `VISUAL_REFERENCE_SET` component kinds, binding through `BindSourcePackageComponent`, atomic receipts, and selective invalidation. These interface assumptions are not represented as accepted authority.

If the exact `TS-INT-001` hash changes, this specification MUST reopen its governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence.

### 1.4 Deferred references

`SRC-EXT-017` (`github://browser-use/video-use`) and `SRC-EXT-020` (`github://UVA-Computer-Vision-Lab/OmniShotCut`) are `DEFERRED_REFERENCE`: exact bytes are unavailable, no unique active requirement depends solely on them, and the current source ledger says to retain them in the research backlog without attributed claims. They do not block writing. This specification attributes no algorithm, benchmark, interface, dependency, license, or behavior to either unavailable source.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

An admitted interview video is not yet an inspectable visual evidence surface. Downstream moment hunters, edit planners, Carousel/visual programs, identity-sensitive derivatives, evaluators, and human reviewers need to locate exact source frames and avoid source transitions. A weak implementation commonly commits one or more correctness failures:

- uses nominal frames-per-second arithmetic on variable-frame-rate media and points to the wrong source image;
- calls every detector peak a shot boundary and hides missed-transition uncertainty;
- chooses a visually different frame and labels it emotionally or semantically important;
- emits thumbnails without source-media hash, stream, presentation timestamp, decode profile, or pixel digest;
- overwrites a shot map after one correction, making historical derivatives irreproducible;
- changes a detector or selection profile and silently retargets active consumers;
- stores local absolute paths, random IDs, current time, or nondeterministic traversal order in canonical output;
- treats face/subject geometry as identity or psychological meaning; or
- writes technical visual observations into generic notes that lose provenance, method, uncertainty, and applicability.

These failures can push unsupported or context-stripped visual evidence into later Expression Moment derivation and every derivative format.

### 2.2 User and system outcome

A visual analyst or downstream service can request an exact source frame, inspect why it was selected, see the shot and transition context around it, understand detector uncertainty, and verify every byte against the admitted source package. Correcting one boundary or keyframe creates a new immutable visual index and invalidates only consumers that depended on the changed evidence.

### 2.3 Bounded solution

Interview Expression SHALL own a versioned `SourceVisualStructureIndex` composed of:

- an exact source-stream timeline and frame-address index;
- a complete, gap-free `ShotMap` over the analyzed video stream;
- explicit `TransitionObservation` and boundary-decision records;
- a `KeyframeSet` whose selection reasons are technical or evidence-candidate reasons, never semantic approval;
- a `VisualReferenceIndex` containing exact frame refs, quality observations, and optional face/subject geometry with provenance and uncertainty; and
- one immutable `VisualStructureAnalysisReceipt` linking command, profiles, workers/tools, source package, outputs, validation, and package-component binding.

The output binds to the exact `TS-INT-001` package through the `SHOT_MAP`, `KEYFRAME_SET`, and `VISUAL_REFERENCE_SET` component slots by creating a successor package version.

### 2.4 In scope

- Technical video-stream admission checks specific to visual analysis.
- Exact rational source-time and presentation-order frame addressing.
- Boundary proposals, transition observations, review/validation, and complete shot segmentation.
- Representative, transition-context, quality-diagnostic, identity-geometry, and expression-signal-candidate keyframes.
- Exact frame artifact materialization, portable locators, and frame/pixel hashes.
- Camera/framing-change observations and optional face/subject geometry as technical evidence.
- Versioned analysis and validation profiles without invented thresholds.
- Commands, events, state, receipts, canonical serialization, idempotency, optimistic concurrency, atomic commit, replay, cancellation, correction, supersession, and selective invalidation.
- Typed handoff to the source-package aggregate and read-only consumption by later Interview Expression and Pipeline work.
- Migration rules for hash-locked legacy shot/keyframe evidence.

### 2.5 Out of scope and non-goals

- Discovering, scoring, approving, rejecting, or routing Anchor Hits or Expression Moments. That later semantic/evidence workflow consumes this index; a boundary or keyframe never creates a moment.
- Compiling Activative Intelligence, Context Premise, Resonance, Matrix of Edging, Primitive coalitions, archetypes, role-tension, Activative Call, Reaction Receipt meaning, Activation Contract, Final Script, Visual Semantic Pack, Visual Narrative Program, or Feature Contracts. AIR owns semantic compilation.
- Transcript, word/phrase alignment, speaker map, or audio-event contracts; `TS-INT-002` owns those components.
- Reaction Receipt or Expression Moment component semantics; `TS-INT-006` and `TS-INT-004` own them.
- Selecting A-roll, edit decisions, crop/reframe commands, derivative composition, visual production, or production evaluation.
- Naming an implementation library, model, provider, codec stack, confidence threshold, benchmark target, worker capacity, or service-level objective without separately governed evidence.
- Granting publication, identity, voice, model-training, creative-safety, content-rights, implementation, certification, or production authority.
- Creating code, tests, schemas, generated types, release bytes, or Development Capsules during this writing task.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty and ownership

1. Interview Expression owns source visual analysis, boundary decisions, technical keyframe selection, visual reference evidence, and the immutable visual index.
2. The Canonical Interview Source Package remains the aggregate root. `TS-INT-003` creates component artifacts and requests their exact binding; it does not create a second source package or mutate a prior package version.
3. AIR owns semantic and psychological meaning. A frame may be an `EXPRESSION_SIGNAL_CANDIDATE` based on declared visible evidence, but Interview Expression cannot call it a valid Expression Moment or Activative role.
4. Later Interview Expression hunters may consume the index to propose source-backed spans. Hunters propose; they do not approve. An independent/authorized validation path governs promotion.
5. Pipeline consumes exact accepted component refs and may execute/replay declared nodes. Builder declares dependencies. Neither rebuilds source meaning or rewrites index evidence.
6. VAE owns visual production realization, not source-frame truth. Studio projects index state and emits typed review/correction commands, not canonical writes. Delegation transports immutable messages and receipts, not meaning.
7. `Activative Contract Compiler != Activative Intelligence Runtime`; a visual-index compiler cannot absorb AIR authority.

### 3.2 Visual change is not semantic importance

A shot boundary, transition, camera move, crop change, face appearance, gesture peak, blur change, luminance change, or detector score is technical evidence. It MUST NOT automatically:

- create or approve an Expression Moment;
- become an observed Activative tag;
- rank a quote or route;
- assert a Primitive, archetype, Matrix edge, role-tension, or psychological state;
- confer source authority or participant approval; or
- authorize a derivative.

The visual index may carry a keyframe selection reason `EXPRESSION_SIGNAL_CANDIDATE` only when it also carries exact observable features, method/profile provenance, uncertainty, and the label `NON_SEMANTIC_PROPOSAL`. Later owners decide semantic applicability.

### 3.3 Source and time fidelity

- Every analysis is pinned to one `CanonicalInterviewSourcePackageVersion`, one admitted video artifact digest, one stream identity, and one technical admission/probe record.
- Presentation time uses rational ticks from the exact stream timebase. Floating seconds are display-only and never canonical.
- Variable frame rate is first-class. A frame is addressed by stream, presentation ordinal, presentation timestamp, duration, and exact decoded-pixel digest; nominal FPS cannot be the sole locator.
- Shot intervals use half-open presentation ranges `[start, end_exclusive)` and cover every admitted presentation frame exactly once. They neither overlap nor leave gaps.
- Transition intervals may span frames on both sides of a boundary but MUST identify their exact presentation range and adjacent shots.
- Every materialized keyframe resolves to an exact source frame and source-media hash. A visually similar re-encode is a different artifact unless a governed equivalence profile proves compatibility.

### 3.4 Profiles, thresholds, and uncertainty

`ShotDetectionProfile`, `TransitionClassificationProfile`, `KeyframeSelectionProfile`, `VisualObservationProfile`, `DecodeProfile`, and `ValidationProfile` are immutable, versioned inputs. They own any thresholds, sampling windows, model/tool refs, numerical tolerances, and fallback rules. This specification does not invent values.

Outputs expose:

- raw or normalized detector observations where governed;
- method/profile and implementation binding;
- confidence or uncertainty with declared scale semantics;
- validation verdict and reviewer/evaluator provenance;
- known blind-spot and missed-transition risk codes; and
- degraded-mode or unsupported-media status.

Parsing a detector result without enforcing its profile, source lineage, and validation state is non-conformant.

### 3.5 Determinism, canonicalization, and portability

- Canonical records use governed UTF-8 JSON, sorted map keys, stable enum spellings, integer/rational time, and semantically ordered arrays.
- Canonical identity MUST NOT depend on current time, random state, dictionary insertion order, filesystem traversal order, machine path, hostname, username, locale, timezone, environment, thread scheduling, or device enumeration.
- Authority-supplied command time and worker facts may be recorded, but nonsemantic operational facts are excluded from content identity.
- Artifact refs use content digest, bytes, media type, and portable logical URI. Drive-qualified paths, UNC paths, traversal, unexpanded environment syntax, and local temporary paths are rejected.
- The same source bytes, profiles, implementation binding, and canonical command MUST yield the same accepted index bytes. A proposal runtime that cannot meet canonical determinism may submit proposals, but a deterministic reference validation must produce the accepted identity.

### 3.6 Immutability, replay, and concurrency

- Source visual indexes, component records, profiles, decisions, reviews, artifacts, and receipts are immutable.
- Corrections create successor versions and explicit supersession edges.
- Command records, events, artifacts/refs, receipts, dependency edges, idempotency result, package-binding request, and outbox intent commit atomically.
- A duplicate idempotency key with identical command bytes returns the original result. Reuse with different bytes fails.
- Commands that alter a current analysis require exact expected index version/digest and current source-package version/digest.
- Replay uses the exact historical profiles, implementation bindings, source artifact, and decisions. It never substitutes current profiles or latest package versions.

### 3.7 Applicability and `NOT_APPLICABLE`

For a technically admitted interview video, `SHOT_MAP` and `KEYFRAME_SET` are required before derivative publication under the profile defined by `TS-INT-001`. An empty nonzero-duration video cannot pass admission. A shot contains at least one presentation frame and requires at least one representative keyframe unless a profile produces an explicit blocking failure.

Face/subject geometry is optional because a source can contain inserts, empty frames, or non-face imagery. Its absence MUST be represented as evidence-bearing `NOT_APPLICABLE` with profile, reason, inspected range, and evidence—not null or a permissive default. `VISUAL_REFERENCE_SET` remains required and can reference non-face visual evidence.

### 3.8 Source authority and restricted evidence

The analysis service enforces the source-package `OperatorSourceAuthorityDeclaration`, including restrictions on identity/voice use, publication, derivative routes, model training, retention, and restricted evidence. It records enforcement but does not create a new legal or creative approval authority. A prohibited model-training scope cannot be bypassed by a detector profile that requests learning or retention.

## 4. Current brownfield architecture

### 4.1 Current Interview Expression root

The Program Control root registry reserved `06_INTERVIEW_EXPRESSION` without source-tree or implementation authority. At writing time the root contains candidate Tech Specs and no governed visual-analysis implementation. There is no current package, service, repository, adapter, test, worker, or accepted schema to reuse at the target product path.

Disposition: `ACTIVATE_AFTER_SEPARATE_AUTHORIZATION`, not greenfield invention by this prompt. Exact future paths are reserved in section 7 only.

### 4.2 `TS-INT-001` draft aggregate interface

`TS-INT-001` defines source media, rational timebase, portable artifact refs, immutable component slots, and package binding. Its `SHOT_MAP`, `KEYFRAME_SET`, and `VISUAL_REFERENCE_SET` slots are the sole aggregate attachment points for this work.

Disposition: `ADAPT_DRAFT_INTERFACE`. This spec pins the exact hash and makes no acceptance claim. If audit changes the slot model, package states, binding command, timebase, or portability rules, the six recorded downstream sections reopen.

### 4.3 Interview-first doctrine and Studio predecessor

The hash-locked interview doctrine and Studio PRD establish source-first expression capture and Complete Expression Session concepts. They are evidence rather than current Interview Expression implementation authority. No exact Studio source/test path was identified by the assignment or source crosswalk as a current shot-map/keyframe implementation to transplant.

Disposition: `ADAPT_BEHAVIOR_NOT_AUTHORITY`. Preserve exact source and expression context, but do not transfer Studio’s canonical ownership or historical lifecycle labels.

### 4.4 External references

The assignment mentions `SRC-EXT-017` and `SRC-EXT-020`, but current Program Control classifies both as unavailable `DEFERRED_REFERENCE`. No code, API, benchmark, threshold, license conclusion, or architecture is imported from them.

Disposition: `DEFER`. A later research lane may hash-lock and disposition exact bytes. Such research may propose an implementation binding but cannot change this contract or ownership without governed revision.

### 4.5 Brownfield and migration constraints

Any legacy shot/keyframe evidence may be migrated only when it supplies:

- exact source-media digest and bytes;
- stream identity and rational timebase;
- unambiguous presentation-frame mapping;
- boundary/transition ranges and method provenance;
- exact frame or materialized-image digests;
- selection reasons and lifecycle state; and
- source authority compatible with the intended use.

A float timestamp, thumbnail filename, scene number, or local file path alone is insufficient. Ambiguous evidence is preserved historically and migration is blocked rather than guessed.

## 5. Proposed architecture and workflows

### 5.1 Components

1. **VisualAnalysisAdmissionService** — resolves the exact source-package and media refs, validates technical/source-authority prerequisites, and freezes a command input manifest.
2. **MediaProbePort** — returns deterministic stream metadata, timebase, presentation ordering, duration, and decode compatibility under an immutable binding.
3. **FrameAddressIndexBuilder** — creates the complete source presentation-frame index and exact pixel/artifact identities.
4. **ShotBoundaryProposalPort** — produces technical boundary/transition observations under a pinned profile; it has no semantic authority.
5. **ShotMapValidator** — reconciles proposals/reviews into a complete nonoverlapping shot partition and exposes uncertainty.
6. **KeyframeSelector** — selects required representative and evidence-candidate frames under a pinned profile and bounded reasons.
7. **VisualObservationPort** — records framing, camera, image quality, and optional face/subject geometry with profile provenance.
8. **KeyframeMaterializerPort** — emits portable content-addressed frame artifacts from exact source coordinates.
9. **SourceVisualIndexService** — orchestrates commands, state transitions, corrections, and atomic persistence.
10. **SourceVisualIndexRepositoryPort** — stores command records, events, versions, decisions, receipts, dependencies, idempotency, invalidation, and outbox in one transaction.
11. **SourcePackageBindingPort** — invokes the exact aggregate binding interface and records the resulting successor package ref.
12. **VisualIndexQueryPort** — returns exact versions, frame refs, shots, transitions, keyframes, visual observations, and descendant dependencies.

### 5.2 Analysis workflow

1. `RequestSourceVisualAnalysis` identifies the exact source-package version, admitted video artifact, stream, profiles, implementation bindings, authority, idempotency key, and expected current index state.
2. Admission verifies source bytes, media digest, source authority, technical admission, stream existence, and compatibility. It writes an immutable input manifest.
3. The media probe produces exact stream/timebase/presentation metadata. The frame index enumerates presentation frames deterministically and records source coordinate plus decoded-pixel digest.
4. The boundary port emits `ShotBoundaryProposal` and `TransitionObservation` records. Proposals cannot enter the accepted shot map directly.
5. Deterministic validation checks profile conformance, range bounds, chronological order, duplicate/conflicting proposals, and coverage. The configured review path resolves borderline or conflicting observations without semantic labeling.
6. The validator compiles a complete `ShotMap`: every presentation frame belongs to exactly one shot; every adjacent pair is connected by an accepted boundary decision; transition ranges remain explicit.
7. The keyframe selector emits one or more frame selections per shot, plus transition-context, quality-diagnostic, geometry-reference, or expression-signal-candidate selections where supported. It cannot emit `EXPRESSION_MOMENT` or `SEMANTIC_IMPORTANCE` as a reason.
8. The materializer resolves each exact frame and stores portable frame artifacts with byte and pixel digests. Materialization that lands on a different frame fails.
9. Visual observations are attached to exact frames/ranges. Optional face/subject geometry uses normalized rational coordinates and retains method uncertainty; it does not assert identity.
10. Validation compiles immutable `ShotMap`, `KeyframeSet`, and `VisualReferenceIndex` components plus one analysis receipt.
11. The repository atomically commits the visual-index version, command, events, decisions, component refs, receipt, dependency edges, idempotency result, and outbox intent.
12. `BindVisualStructureComponents` requests binding to the exact current source package. Successful binding returns a successor package ref. Component publication and package binding are distinguishable receipts.

### 5.3 Review workflow

Review is profile-driven, sampled or exhaustive as governed. A `ReviewShotBoundaryProposal` command records one of:

- `CONFIRM_BOUNDARY`
- `REJECT_BOUNDARY`
- `RECLASSIFY_TRANSITION`
- `ADJUST_RANGE`
- `MARK_BORDERLINE`
- `ESCALATE_UNRESOLVED`

The review record contains exact before/after frames, adjacent context, reason code, actor/evaluator, evidence refs, and profile. Review may confirm technical visual structure. It cannot assert that the content is meaningful, true, activating, archetypal, or production-ready.

Unresolved conflicts place the analysis in `REVIEW_REQUIRED`; they are not silently resolved using the highest detector score.

### 5.4 Keyframe selection workflow

Selection reasons are closed enums:

- `SHOT_REPRESENTATIVE`
- `TRANSITION_CONTEXT_BEFORE`
- `TRANSITION_CONTEXT_AFTER`
- `EXPRESSION_SIGNAL_CANDIDATE`
- `IDENTITY_GEOMETRY_REFERENCE`
- `QUALITY_DIAGNOSTIC`

Each selection records the profile rule, candidate set, reason evidence, rejected alternatives when required, and uncertainty. `EXPRESSION_SIGNAL_CANDIDATE` means only that a declared observable visual signal may help a later evidence workflow. The output carries `NON_SEMANTIC_PROPOSAL=true` and cannot satisfy the Reaction Receipt or Expression Moment provenance gate by itself.

### 5.5 Correction and selective invalidation

`CorrectShotBoundary`, `CorrectTransitionObservation`, `ReplaceKeyframeSelection`, and `CorrectVisualObservation` create successor artifacts and a successor index. They do not patch prior bytes.

Invalidation scope is field-dependent:

- source-media or stream identity change invalidates the entire frame address index and all descendants;
- decode-profile change invalidates frame/pixel identities and all shot/keyframe/visual descendants;
- boundary correction invalidates adjacent shot records, selections derived from those shots, and consumers of affected ranges;
- transition reclassification invalidates consumers that use that transition class/range but not unrelated shots;
- keyframe-selection-profile change invalidates the keyframe set and consumers of changed selections, not the shot map when boundaries are unchanged;
- visual-observation correction invalidates the exact visual refs and their consumers, not unrelated frame or shot records; and
- source-authority revocation invalidates only newly prohibited scopes while retaining historical evidence.

All invalidation records identify the changed exact ref, changed fields, affected descendants, unaffected proof, authority, reason, and replacement where available.

### 5.6 Cancellation, late results, and partial work

Cancellation records an immutable request. Workers check the cancellation token before expensive stages and before commit. A late worker result after cancellation is stored only as quarantined operational evidence when policy permits; it cannot become an accepted index or package component.

No partial shot map, incomplete frame index, missing keyframe artifact, or unresolved boundary set is published as `VALIDATED`. Intermediate artifacts may be retained in a quarantined run scope with explicit noncanonical status and retention policy.

### 5.7 State machine

`SourceVisualAnalysis` states:

`REQUESTED` → `TECHNICALLY_ADMITTED` → `FRAME_INDEXED` → `BOUNDARIES_PROPOSED` → (`REVIEW_REQUIRED` ↔ `BOUNDARIES_PROPOSED`) → `SHOT_MAP_VALIDATED` → `KEYFRAMES_SELECTED` → `ARTIFACTS_MATERIALIZED` → `VISUAL_INDEX_VALIDATED` → `BOUND_TO_SOURCE_PACKAGE`.

Terminal or side states are `BLOCKED_CONSTRAINT_CONFLICT`, `FAILED`, `CANCELLED`, `SUPERSEDED`, and `INVALIDATED`.

Only typed commands with actor authority, expected state/version, and receipts cause transitions. A worker callback, file appearance, or model response never changes canonical state by itself.

### 5.8 Handoffs

- `TS-INT-001` receives the three immutable component refs and returns a successor source-package version.
- Later Expression Moment derivation consumes exact keyframe/visual refs as evidence alongside transcript, audio, Reaction Receipts, context, and other governed inputs. It may ignore visual-change proposals and must independently validate source meaning.
- Pipeline and derivative products consume exact published package/component versions; they cannot query “latest” during an active job.
- Studio reads projections and submits typed review/correction commands.
- Delegation transports exact refs, versions, hashes, compatibility profiles, and receipts when the boundary is cross-product.

## 6. Data models, contracts, schemas, and APIs

The following are normative logical contracts. They do not create canonical schema bytes in this writing stage.

### 6.1 Identity and time values

```text
RationalTimebase {
  numerator: positive integer
  denominator: positive integer
}

FrameCoordinate {
  source_media_ref: ImmutableRef
  stream_index: non-negative integer
  presentation_ordinal: non-negative integer
  presentation_timestamp_ticks: signed integer
  duration_ticks: positive integer
  timebase: RationalTimebase
  decode_ordinal: optional non-negative integer
  packet_digest: optional sha256
  decoded_pixel_digest: sha256
}

FrameRange {
  start: FrameCoordinate
  end_exclusive_presentation_ordinal: positive integer
  start_time_ticks: signed integer
  end_time_ticks_exclusive: signed integer
  timebase: RationalTimebase
}
```

The same stream/timebase/source digest is required throughout a range. Display seconds are derived and excluded from canonical identity. A coordinate without a decoded-pixel digest may exist only as a nonaccepted proposal.

### 6.2 Frozen input manifest

```text
VisualAnalysisInputManifest {
  manifest_id: deterministic identifier
  source_package_ref: ImmutableRef
  source_media_ref: PortableArtifactRef
  source_authority_declaration_ref: ImmutableRef
  stream_index: non-negative integer
  technical_admission_receipt_ref: ImmutableRef
  media_probe_binding_ref: ImmutableRef
  decode_profile_ref: ImmutableRef
  shot_detection_profile_ref: ImmutableRef
  transition_profile_ref: ImmutableRef
  keyframe_selection_profile_ref: ImmutableRef
  visual_observation_profile_ref: ImmutableRef
  validation_profile_ref: ImmutableRef
  worker_binding_refs: canonical ordered ImmutableRef[]
  command_ref: ImmutableRef
  manifest_sha256: sha256 of canonical fields excluding itself
}
```

Every profile and implementation binding declares owner, version, digest, compatibility, dependency/license disposition where applicable, determinism class, tool/model requirement, source-authority use, and lifecycle state.

### 6.3 Frame address index

```text
FrameAddressIndex {
  index_id: deterministic identifier
  version: positive integer
  input_manifest_ref: ImmutableRef
  source_media_ref: ImmutableRef
  stream_index: non-negative integer
  timebase: RationalTimebase
  presentation_frames: non-empty ordered FrameCoordinate[]
  stream_duration_ticks: positive integer
  pixel_canonicalization_profile_ref: ImmutableRef
  index_sha256: sha256
}
```

Presentation ordinals are contiguous and unique. Timestamps are nondecreasing; duplicate timestamps, when permitted by the media profile, remain distinct by ordinal and digest. A gap or duplicate ordinal fails validation.

### 6.4 Boundary and transition records

```text
ShotBoundaryProposal {
  proposal_id: deterministic identifier
  left_frame_ref: ImmutableRef
  right_frame_ref: ImmutableRef
  transition_range: optional FrameRange
  proposed_transition_type: HARD_CUT | DISSOLVE | FADE_IN | FADE_OUT | WIPE | OCCLUSION | CAMERA_START_STOP | OTHER_PROFILED | UNKNOWN
  detector_observations: non-empty typed DetectorObservation[]
  detection_profile_ref: ImmutableRef
  implementation_binding_ref: ImmutableRef
  confidence: optional GovernedScore
  uncertainty_codes: governed non-empty set when unresolved
  proposal_state: PROPOSED | BORDERLINE | REJECTED_BY_VALIDATION
  semantic_importance_asserted: false
}

ShotBoundaryDecision {
  decision_id: deterministic identifier
  proposal_ref: ImmutableRef
  verdict: CONFIRMED | REJECTED | RECLASSIFIED | RANGE_ADJUSTED | UNRESOLVED
  decided_transition_type: optional governed transition type
  decided_transition_range: optional FrameRange
  actor_or_evaluator_ref: ImmutableRef
  validation_profile_ref: ImmutableRef
  evidence_refs: non-empty ImmutableRef[]
  reason_codes: non-empty governed set
  supersedes: optional ImmutableRef
}

TransitionObservation {
  transition_id: deterministic identifier
  type: governed transition type
  frame_range: FrameRange
  preceding_shot_id: deterministic identifier
  following_shot_id: deterministic identifier
  decision_ref: ImmutableRef
  uncertainty_codes: governed set
}
```

`GovernedScore` includes value, scale ID, calibration/profile ref, and interpretation. A bare float is forbidden.

### 6.5 Shot map

```text
ShotRecord {
  shot_id: deterministic identifier
  presentation_range: FrameRange
  preceding_boundary_ref: optional ImmutableRef
  following_boundary_ref: optional ImmutableRef
  transition_in_ref: optional ImmutableRef
  transition_out_ref: optional ImmutableRef
  camera_framing_observation_refs: canonical ordered ImmutableRef[]
  uncertainty_codes: governed set
}

ShotMap {
  shot_map_id: deterministic identifier
  version: positive integer
  input_manifest_ref: ImmutableRef
  frame_address_index_ref: ImmutableRef
  shots: non-empty presentation-ordered ShotRecord[]
  boundary_decision_refs: presentation-ordered ImmutableRef[]
  transition_refs: presentation-ordered ImmutableRef[]
  validation_receipt_ref: ImmutableRef
  supersedes: optional ImmutableRef
  shot_map_sha256: sha256
}
```

The first shot begins at the first presentation frame; the last ends at the end-exclusive ordinal after the last frame. Adjacent shots meet at one boundary. Accepted shots do not overlap or leave gaps.

### 6.6 Keyframe records

```text
KeyframeArtifactRef {
  logical_uri: portable relative or content URI
  bytes: positive integer
  media_type: governed image media type
  artifact_sha256: sha256
  decoded_pixel_sha256: sha256
  width: positive integer
  height: positive integer
  color_profile_ref: ImmutableRef
}

KeyframeSelection {
  keyframe_id: deterministic identifier
  shot_ref: ImmutableRef
  source_frame: FrameCoordinate
  artifact_ref: KeyframeArtifactRef
  reason: SHOT_REPRESENTATIVE | TRANSITION_CONTEXT_BEFORE | TRANSITION_CONTEXT_AFTER | EXPRESSION_SIGNAL_CANDIDATE | IDENTITY_GEOMETRY_REFERENCE | QUALITY_DIAGNOSTIC
  rule_ref: ImmutableRef
  candidate_set_ref: ImmutableRef
  evidence_refs: canonical ordered ImmutableRef[]
  uncertainty_codes: governed set
  non_semantic_proposal: true
  lifecycle_state: SELECTED | REJECTED | SUPERSEDED | INVALIDATED
}

KeyframeSet {
  keyframe_set_id: deterministic identifier
  version: positive integer
  input_manifest_ref: ImmutableRef
  shot_map_ref: ImmutableRef
  selections: canonical ordered KeyframeSelection[]
  selection_profile_ref: ImmutableRef
  validation_receipt_ref: ImmutableRef
  supersedes: optional ImmutableRef
  keyframe_set_sha256: sha256
}
```

Every shot requires at least one current `SHOT_REPRESENTATIVE`. Other reasons are optional and profile-governed. Two selection reasons may reference the same exact frame but remain separate reason records or a governed canonical reason set; the representation must be declared by the profile and deterministic.

### 6.7 Visual observations and references

```text
NormalizedRationalBox {
  x_num: non-negative integer
  y_num: non-negative integer
  width_num: positive integer
  height_num: positive integer
  denominator: positive integer
}

VisualObservation {
  observation_id: deterministic identifier
  source_frame_or_range_ref: ImmutableRef
  kind: CAMERA_CHANGE | FRAMING | IMAGE_QUALITY | FACE_GEOMETRY | SUBJECT_GEOMETRY | OCCLUSION | OTHER_PROFILED
  value: typed union owned by observation kind
  method_profile_ref: ImmutableRef
  implementation_binding_ref: ImmutableRef
  confidence: optional GovernedScore
  uncertainty_codes: governed set
  epistemic_state: OBSERVED | INFERRED
  identity_asserted: false
  semantic_importance_asserted: false
  applicability: APPLICABLE | EvidenceBearingNotApplicable
}

VisualReference {
  visual_reference_id: deterministic identifier
  source_frame_ref: ImmutableRef
  keyframe_ref: optional ImmutableRef
  observation_refs: canonical ordered ImmutableRef[]
  source_authority_scope_ref: ImmutableRef
  permitted_use_scopes: canonical governed set
  restrictions: typed non-permissive constraints
}

VisualReferenceIndex {
  visual_reference_index_id: deterministic identifier
  version: positive integer
  input_manifest_ref: ImmutableRef
  shot_map_ref: ImmutableRef
  keyframe_set_ref: ImmutableRef
  visual_references: canonical ordered VisualReference[]
  validation_receipt_ref: ImmutableRef
  supersedes: optional ImmutableRef
  index_sha256: sha256
}
```

Geometry is a technical observation, not recognized identity. Missing geometry is evidence-bearing `NOT_APPLICABLE`, including inspected range and reason such as `NO_DETECTABLE_SUBJECT`, `PROFILE_UNSUPPORTED`, or `RESTRICTED_BY_SOURCE_AUTHORITY`.

### 6.8 Aggregate component and receipt

```text
SourceVisualStructureIndex {
  visual_index_id: deterministic identifier
  version: positive integer
  source_package_ref: ImmutableRef
  input_manifest_ref: ImmutableRef
  frame_address_index_ref: ImmutableRef
  shot_map_ref: ImmutableRef
  keyframe_set_ref: ImmutableRef
  visual_reference_index_ref: ImmutableRef
  lifecycle_state: governed analysis state
  dependency_edges: canonical ordered DependencyEdge[]
  source_package_binding_ref: optional ImmutableRef
  supersedes: optional ImmutableRef
  index_sha256: sha256
}

VisualStructureAnalysisReceipt {
  receipt_id: deterministic identifier
  command_ref: ImmutableRef
  actor_authority_ref: ImmutableRef
  input_manifest_ref: ImmutableRef
  prior_index_ref: optional ImmutableRef
  resulting_index_ref: optional ImmutableRef
  output_component_refs: canonical ordered ImmutableRef[]
  validation_and_review_refs: canonical ordered ImmutableRef[]
  package_binding_request_ref: optional ImmutableRef
  resulting_source_package_ref: optional ImmutableRef
  events: canonical ordered ImmutableRef[]
  invalidated_descendants: canonical ordered ImmutableRef[]
  failure: optional TypedFailure
  replay_equivalence_digest: optional sha256
}
```

Success requires artifacts and receipt in the same atomic commit. A binding receipt without the three exact component artifacts, or components without a command/receipt, is invalid.

### 6.9 Commands, events, and APIs

Normative commands:

- `RequestSourceVisualAnalysis`
- `RecordShotBoundaryProposals`
- `ReviewShotBoundaryProposal`
- `ValidateShotMap`
- `SelectSourceKeyframes`
- `MaterializeSourceKeyframes`
- `RecordVisualObservations`
- `ValidateSourceVisualIndex`
- `BindVisualStructureComponents`
- `CorrectShotBoundary`
- `CorrectTransitionObservation`
- `ReplaceKeyframeSelection`
- `CorrectVisualObservation`
- `CancelSourceVisualAnalysis`
- `SupersedeSourceVisualIndex`
- `InvalidateVisualIndexDescendants`

All commands use the `TS-INT-001` authority/idempotency/concurrency envelope by exact adopted interface or a reconciled successor. Generic patch commands are prohibited.

Normative events mirror accepted state transitions: `SourceVisualAnalysisRequested`, `SourceVisualAnalysisAdmitted`, `FrameAddressIndexBuilt`, `ShotBoundariesProposed`, `ShotBoundaryReviewed`, `ShotMapValidated`, `KeyframesSelected`, `KeyframeArtifactsMaterialized`, `VisualObservationsRecorded`, `SourceVisualIndexValidated`, `VisualStructureComponentsBound`, `VisualIndexCorrected`, `VisualIndexSuperseded`, `VisualIndexDescendantsInvalidated`, and `SourceVisualAnalysisCancelled`.

Logical query APIs:

- `get_visual_index(index_id, version, sha256)`
- `get_frame(source_media_ref, stream_index, presentation_ordinal, pixel_sha256)`
- `get_shot(shot_map_ref, shot_id)`
- `find_shot_at_time(shot_map_ref, ticks, timebase)`
- `list_transitions(shot_map_ref, frame_range, cursor)`
- `list_keyframes(keyframe_set_ref, shot_id, reason, cursor)`
- `get_visual_reference(visual_reference_index_ref, visual_reference_id)`
- `list_index_descendants(exact_ref, edge_type, cursor)`
- `verify_visual_index_replay(index_ref)`

Exact-version/hash requests never fall back to latest.

### 6.10 Compatibility and negative examples

Compatibility is semantic, not “JSON parses.” A consumer declares required profile/features: rational time, frame pixel digest, transition range, keyframe reason, source-authority scope, and invalidation support. An adapter cannot drop any required field.

Invalid examples:

- `{ "time_seconds": 12.4, "image": "C:\\temp\\frame.jpg" }` — no rational source coordinate, digest, portability, or lineage.
- `{ "boundary": 120, "importance": "high" }` — presentation unit unspecified and forbidden semantic inference.
- `{ "face_box": null }` — ambiguity between not run, not found, restricted, failed, and not applicable.
- `{ "confidence": 0.9 }` — no scale, calibration, profile, or interpretation.
- a keyframe ref whose image hash resolves but whose source-media hash or presentation frame differs — fails lineage validation.

## 7. Implementation stages and exact target paths

These are future paths for a separately authorized build. This writing task creates none of them.

### 7.1 Stage A — Domain and canonical values

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/frame_coordinate.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/visual_analysis_profiles.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/shot_map.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/keyframe_set.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/visual_reference_index.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/source_visual_structure_index.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/domain/visual_analysis_failures.py`

Implement immutable rational time, presentation-frame identity, component records, state machine, profile refs, typed applicability, canonical ordering, and content identities. Maps and sets use explicit canonical sort keys.

### 7.2 Stage B — Ports and persistence

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/media_probe.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/frame_decoder.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/shot_boundary_proposer.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/keyframe_materializer.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/visual_observer.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/source_package_binding.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/ports/source_visual_index_repository.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/repositories/event_sourced_source_visual_index_repository.py`

The repository implements one atomic transaction across state, artifacts/refs, command, event, receipt, dependency, idempotency, invalidation, and outbox records. An in-memory implementation used for tests must enforce identical atomicity and historical-version behavior.

### 7.3 Stage C — Application services

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/visual_analysis_admission_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/frame_address_index_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/shot_map_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/keyframe_selection_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/visual_reference_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/visual_index_binding_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/visual_index_invalidation_service.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/services/visual_index_replay_service.py`

Services orchestrate typed ports and domain commands. They do not embed AIR semantic compilation, edit planning, VAE production, Studio UI, or Delegation routing.

### 7.4 Stage D — Adapters and profile registry

Proposed paths:

- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/source_package_visual_component_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/studio_visual_review_projection.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/pipeline_visual_index_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/adapters/delegation_visual_index_adapter.py`
- `06_INTERVIEW_EXPRESSION/src/conscious_activations_interview_expression/registries/visual_analysis_profile_registry.py`

No provider-specific adapter is named until exact implementation evidence, dependency/license review, deterministic behavior, and authority are approved. Deferred external references cannot be used as implied dependencies.

### 7.5 Stage E — Candidate contracts and migration

Potential future paths, requiring separate schema authority:

- `06_INTERVIEW_EXPRESSION/contracts/schemas/source-visual-structure-index.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/shot-map.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/keyframe-set.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/visual-reference-index.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/visual-structure-analysis-receipt.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/migrations/legacy-shot-keyframe-to-source-visual-index.yaml`

No schema or migration is created now. Contract release requires accepted `TS-INT-001` compatibility and reconciliation with later downstream specs.

### 7.6 Stage F — Tests

Proposed paths:

- `06_INTERVIEW_EXPRESSION/tests/unit/test_frame_coordinate.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_shot_map_partition.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_transition_observation.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_keyframe_selection.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_visual_observation_applicability.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_visual_change_not_semantic_importance.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_visual_analysis_atomic_commit.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_visual_index_replay_and_idempotency.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_visual_index_selective_invalidation.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_visual_component_package_binding.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/test_ts_int_001_visual_component_mapping.py`
- `06_INTERVIEW_EXPRESSION/tests/architecture/test_visual_analysis_authority_boundaries.py`
- `06_INTERVIEW_EXPRESSION/tests/migration/test_legacy_shot_keyframe_migration.py`
- `06_INTERVIEW_EXPRESSION/tests/portability/test_visual_index_clean_room_export.py`

### 7.7 FR/Story implementation mapping

| Stage | `FR-129` / `ST-02.02` outcome | Required later evidence |
|---|---|---|
| A | Exact frame, boundary, shot, transition, keyframe, and visual-reference semantics | Domain/property tests and canonical vectors |
| B | Reproducible decode/proposal/materialization and atomic history | Port contract and fault-injection results |
| C | Complete workflow, review, binding, correction, and replay | Integration receipts and state-transition evidence |
| D | Source-package and consumer mapping without authority drift | Field-preservation and architecture-boundary matrix |
| E | Portable, compatible immutable contract and lossless migration | Schema/migration validation after authorization |
| F | Positive, adversarial, recovery, and clean-room proof | Full governed test manifest |

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

Minimum failure codes:

- `INT_VIS_SOURCE_PACKAGE_NOT_ELIGIBLE`
- `INT_VIS_SOURCE_MEDIA_HASH_MISMATCH`
- `INT_VIS_STREAM_NOT_FOUND`
- `INT_VIS_STREAM_TIMEBASE_INVALID`
- `INT_VIS_FRAME_INDEX_NONCONTIGUOUS`
- `INT_VIS_FRAME_PIXEL_HASH_MISMATCH`
- `INT_VIS_DECODE_PROFILE_UNSUPPORTED`
- `INT_VIS_NONDETERMINISTIC_REFERENCE_RESULT`
- `INT_VIS_PROFILE_MISSING_OR_STALE`
- `INT_VIS_BOUNDARY_OUT_OF_RANGE`
- `INT_VIS_BOUNDARY_CONFLICT`
- `INT_VIS_TRANSITION_RANGE_INVALID`
- `INT_VIS_SHOT_MAP_GAP`
- `INT_VIS_SHOT_MAP_OVERLAP`
- `INT_VIS_BOUNDARY_REVIEW_REQUIRED`
- `INT_VIS_SHOT_REPRESENTATIVE_MISSING`
- `INT_VIS_KEYFRAME_SOURCE_MISMATCH`
- `INT_VIS_KEYFRAME_REASON_FORBIDDEN`
- `INT_VIS_SEMANTIC_IMPORTANCE_ASSERTION_FORBIDDEN`
- `INT_VIS_GEOMETRY_APPLICABILITY_AMBIGUOUS`
- `INT_VIS_SOURCE_AUTHORITY_SCOPE_DENIED`
- `INT_VIS_NONPORTABLE_ARTIFACT_LOCATOR`
- `INT_VIS_STALE_INDEX_VERSION`
- `INT_VIS_SOURCE_PACKAGE_DRIFT`
- `INT_VIS_IDEMPOTENCY_CONFLICT`
- `INT_VIS_ATOMIC_COMMIT_FAILED`
- `INT_VIS_LATE_RESULT_AFTER_CANCELLATION`
- `INT_VIS_REPLAY_DIVERGENCE`
- `INT_VIS_MIGRATION_AMBIGUOUS`
- `INT_VIS_MIGRATION_LOSSY`

Each failure includes command/correlation ID, source package/media/index refs, expected and observed versions/digests, profile/binding refs, stage, retryability, responsible layer, and next admissible action. A detector quality failure is not mislabeled as a storage retry, and a storage retry does not change detector/profile inputs.

### 8.2 Retry versus bounded quality repair

- Transient content-store or transaction failures may retry with the same canonical command and idempotency key.
- Decode, detector, transition, or materialization failures retry only when the exact binding declares deterministic retry equivalence.
- Quality repair uses a new authorized command, new profile/binding or review input, and a successor run; it never changes inputs under an existing command ID.
- Unresolved semantic significance is not “repaired” in this component. It remains outside scope.

### 8.3 Atomic rollback and compensation

If any canonical record, artifact ref, event, receipt, dependency, idempotency result, invalidation, package-binding request, or outbox intent fails, the transaction produces no successful visual-index version. Staged unreferenced frame artifacts are cleaned only by a governed garbage collector that proves no canonical ref uses them.

If component artifacts commit but source-package binding later fails due to a concurrency conflict, the components remain immutable unpublished outputs with a typed binding-failure receipt. A new binding command may target the verified current package after compatibility review; it cannot silently retarget.

### 8.4 Cancellation races and late results

A cancellation request and a commit use optimistic ordering. If commit wins, cancellation creates a successor cancelled/nonconsumable state where allowed. If cancellation wins, late worker results are quarantined and never published. The receipt states the ordering decision and exact transaction IDs.

### 8.5 Migration and backward compatibility

Migration creates new immutable artifacts and a field-by-field receipt. It never mutates legacy thumbnails, EDLs, shot lists, or source packages.

Migration is blocked when:

- source bytes or digest are unavailable;
- frame times cannot be mapped exactly to a rational admitted stream;
- only nominal FPS or float seconds exist and exact frames are ambiguous;
- image bytes cannot be traced to a source frame;
- transition class/range provenance is missing where required;
- selection reasons or lifecycle are ambiguous;
- local paths are the only artifact identity; or
- source authority does not permit the target use.

Deprecated profile versions remain readable for historical replay. Active accepted work stays pinned to the profile negotiated at acceptance. Deprecation does not corrupt historical analysis, but a revoked profile may block new work.

### 8.6 Replay and historical reproduction

Replay starts with a clean projection and exact source bytes, profiles, bindings, commands, decisions, and events. It MUST reconstruct identical canonical records and component digests. Operational timestamps or worker IDs may differ only when explicitly excluded from canonical identity and retained in separate run metadata.

Historical source visual indexes remain queryable after correction, supersession, invalidation, cancellation, or source-authority revocation, with their exact nonconsumable state. Query APIs never replace a requested historical ref with current.

### 8.7 Selective invalidation and recovery

The invalidation projector records changed fields and traverses typed dependency edges. It can resume idempotently from a checkpoint. A failed projector does not mark invalidation complete; new consumption checks both artifact lifecycle and pending invalidation state.

Recovery rebuilds query projections from the canonical log, reconciles outbox records, verifies artifact hashes, and quarantines the service on the first replay divergence. Quarantine reports the exact expected/observed digest and prior valid event; it never selects a “close enough” frame.

### 8.8 Observability and security

Required structured signals:

- admission and technical-probe results by failure code;
- frame-index coverage and duplicate/gap counts;
- boundary proposal, confirmed, rejected, borderline, and unresolved counts;
- transition classes and uncertainty codes by profile;
- shots and keyframes per source duration, reported as measurements rather than invented pass thresholds;
- materialization hash mismatches;
- sampled review decisions and disagreement;
- semantic-importance assertion denials;
- optimistic concurrency and idempotency conflicts;
- invalidation fan-out, lag, and recovery;
- replay divergence; and
- nonportable locator attempts.

Logs use IDs/digests and do not expose restricted media, raw frames, faces, transcripts, participant data, or operator declarations. Artifact access is mediated by operational security controls and recorded. Telemetry cannot be reused for model training when the source declaration prohibits it.

## 9. Behavior-specific acceptance criteria

These are requirements for later independent acceptance, not claims made by this writer.

### AC-01 — Complete source shot map

- **Governing requirement:** `FR-129`; `ST-02.02` primary journey.
- **Given** an exact technically admitted edited interview stream with a pinned timebase, source hash, profiles, and authority,
- **When** visual structure analysis completes,
- **Then** every presentation frame belongs to exactly one ordered shot, accepted transitions have exact ranges, and downstream edit planning can resolve both sides of every boundary.
- **Failure example:** a dissolve range is omitted and two frames are in no shot.
- **Evidence/test layer:** shot-map partition property tests, integration receipt, and source-time validation report.

### AC-02 — Visual change cannot become semantic importance

- **Governing requirement:** `FR-129`; `ST-02.02` adversarial and CBAR criteria.
- **Given** a confirmed hard cut with no approved quote, reaction, or meaningful expression evidence,
- **When** the index is validated and queried,
- **Then** the cut is available as technical evidence but creates no Expression Moment, observed Activative tag, semantic ranking, or route.
- **Failure example:** a detector score is copied into `moment_importance=high`.
- **Evidence/test layer:** unit denial test and architecture authority-boundary test.

### AC-03 — Exact frame lineage

- **Governing requirement:** `FR-129`; `ST-02.02` evidence/replay criterion.
- **Given** a selected keyframe,
- **When** a consumer resolves it,
- **Then** the source-package/media hash, stream, presentation ordinal/timestamp, timebase, decoded-pixel digest, artifact digest, and selection reason all verify.
- **Failure example:** the thumbnail exists but points to the adjacent frame after variable-frame-rate conversion.
- **Evidence/test layer:** contract test, frame-hash fixture, and clean-room materialization proof.

### AC-04 — Variable frame rate and presentation order

- **Governing requirement:** `FR-129`; `ST-02.02` evidence/replay criterion.
- **Given** a video whose presentation timing cannot be represented by one constant frame rate,
- **When** the frame index is built,
- **Then** rational presentation coordinates address every frame without relying on nominal FPS.
- **Failure example:** `round(seconds * fps)` returns a different frame than the recorded PTS.
- **Evidence/test layer:** VFR contract fixture and frame-coordinate property tests.

### AC-05 — Boundary uncertainty remains visible

- **Governing requirement:** `FR-129`; `ST-02.02` primary journey.
- **Given** conflicting or borderline transition observations,
- **When** validation cannot resolve them under the pinned profile,
- **Then** the analysis enters `REVIEW_REQUIRED` with uncertainty and evidence; it does not select the highest score silently.
- **Failure example:** overlapping dissolve and hard-cut proposals are auto-accepted with no decision record.
- **Evidence/test layer:** boundary-conflict unit test and review workflow integration test.

### AC-06 — Representative keyframe coverage

- **Governing requirement:** `FR-129`; `ST-02.02` primary journey.
- **Given** a validated nonempty shot map,
- **When** keyframe selection succeeds,
- **Then** every shot has at least one current `SHOT_REPRESENTATIVE` linked to an exact source frame.
- **Failure example:** a short shot is omitted because a sampler interval skipped it.
- **Evidence/test layer:** keyframe coverage property test and completion report.

### AC-07 — Expression-signal candidate stays nonsemantic

- **Governing requirement:** `FR-129`; `ST-02.02` CBAR criterion.
- **Given** a frame selected for a declared visible expression signal,
- **When** it is emitted,
- **Then** it is labeled `EXPRESSION_SIGNAL_CANDIDATE`, `NON_SEMANTIC_PROPOSAL=true`, with observable evidence, method, and uncertainty, and it cannot satisfy Reaction Receipt or Expression Moment provenance alone.
- **Failure example:** a facial geometry delta is called “audience resistance” without reaction/context evidence.
- **Evidence/test layer:** semantic-boundary contract test and downstream denial fixture.

### AC-08 — Geometry applicability is explicit

- **Governing requirement:** `FR-129`; `ST-02.02` invalid-input criterion.
- **Given** a shot with no detectable face or subject under the exact profile,
- **When** visual references compile,
- **Then** geometry is evidence-bearing `NOT_APPLICABLE` with inspected range and reason while the visual reference remains valid where otherwise eligible.
- **Failure example:** `face_box=null` leaves consumers unable to distinguish not-run from not-found.
- **Evidence/test layer:** applicability union test and schema/contract test.

### AC-09 — Source-authority restrictions are enforced

- **Governing requirement:** `FR-129`; source-first product boundary.
- **Given** a source declaration prohibiting model training or restricting identity-frame export,
- **When** a profile or consumer requests the prohibited use,
- **Then** the request fails with `INT_VIS_SOURCE_AUTHORITY_SCOPE_DENIED` and no prohibited artifact/outbox record is produced.
- **Failure example:** keyframe thumbnails are sent to a learning store because a profile defaulted training eligibility to allowed.
- **Evidence/test layer:** authority-policy integration and negative data-egress test.

### AC-10 — Deterministic fresh-context reproduction

- **Governing requirement:** `FR-129`; `ST-02.02` evidence/replay criterion.
- **Given** identical exact source bytes, profiles, implementation bindings, commands, and decisions in two fresh processes with different environment, timezone, temp root, and traversal order,
- **When** both analyses complete,
- **Then** canonical frame index, shot map, keyframe set, visual reference index, and aggregate digests match exactly.
- **Failure example:** keyframe ordering changes with directory enumeration.
- **Evidence/test layer:** clean-process determinism harness and hash matrix.

### AC-11 — Idempotency and optimistic concurrency

- **Governing requirement:** `FR-129`; `ST-02.02` selective recovery.
- **Given** an accepted command,
- **When** the identical command retries under the same idempotency key,
- **Then** the original refs/receipt return; a different payload under that key or stale expected version fails without mutation.
- **Failure example:** two corrections both overwrite version 3 and issue conflicting version 4 receipts.
- **Evidence/test layer:** repository concurrency integration test.

### AC-12 — Atomic commit and rollback

- **Governing requirement:** `FR-129`; `ST-02.02` evidence/replay criterion.
- **Given** fault injection at any canonical persistence boundary,
- **When** commit fails,
- **Then** there is no accepted index without its components/receipt, no success receipt without artifacts, no missing command/dependency, and no published outbox for rolled-back state.
- **Failure example:** a `KEYFRAME_SET` binding receipt exists while the image artifact write failed.
- **Evidence/test layer:** exhaustive atomic fault-injection matrix.

### AC-13 — Selective boundary correction

- **Governing requirement:** `FR-129`; `ST-02.02` selective recovery.
- **Given** a correction to one boundary between shots 4 and 5 and unrelated accepted shots,
- **When** the successor index is committed,
- **Then** adjacent shot/keyframe and dependent consumer refs are invalidated while unrelated shot/keyframe refs remain valid with proof.
- **Failure example:** the whole source campaign is invalidated although no other consumer used the corrected range.
- **Evidence/test layer:** dependency-graph selective-invalidation integration test.

### AC-14 — Cancellation race and late result

- **Governing requirement:** `FR-129`; `ST-02.02` selective recovery.
- **Given** cancellation races a worker result,
- **When** cancellation commits first,
- **Then** the late result is quarantined/noncanonical and cannot bind to the source package.
- **Failure example:** a callback publishes keyframes after the cancellation receipt.
- **Evidence/test layer:** deterministic race fixture and outbox assertion.

### AC-15 — Lossless-or-blocked migration

- **Governing requirement:** `FR-129`; `ST-02.02` evidence/replay criterion.
- **Given** a legacy thumbnail with only a float timestamp and local path,
- **When** migration cannot prove an exact frame/source digest,
- **Then** it fails `INT_VIS_MIGRATION_AMBIGUOUS`, preserves the legacy artifact, and invents no coordinate.
- **Failure example:** migration rounds 12.4 seconds to frame 372 and claims exact lineage.
- **Evidence/test layer:** migration negative fixture and immutable donor hash check.

### AC-16 — Portable clean-room consumption

- **Governing requirement:** `FR-129`; `ST-02.02` downstream journey.
- **Given** an exported validated index and content-addressed artifacts,
- **When** loaded under a different root in a clean environment,
- **Then** every ref resolves without source-machine paths and all hashes verify.
- **Failure example:** `C:\Users\...\frame.png` appears in a canonical record.
- **Evidence/test layer:** clean-room export/import test and absolute-path scan.

### AC-17 — Package component binding

- **Governing requirement:** `FR-129`; `ST-02.02` downstream journey; draft `TS-INT-001` interface.
- **Given** validated `SHOT_MAP`, `KEYFRAME_SET`, and `VISUAL_REFERENCE_SET` component refs and the exact current package version,
- **When** binding succeeds,
- **Then** `TS-INT-001` returns one immutable successor package version and linked receipt without altering prior versions.
- **Failure example:** only the keyframe slot is updated before a transaction failure, leaving a partially bound package.
- **Evidence/test layer:** package-binding contract and atomic integration tests.

### AC-18 — No claim inflation

- **Governing requirement:** candidate-authority and Story claim ceiling.
- **Given** passing schema, test, or benchmark evidence,
- **When** status is reported,
- **Then** the maximum writer state remains `WRITTEN_PENDING_AUDIT`, authority remains `CANDIDATE_NOT_CURRENT`, and implementation/build/certification/production remain false.
- **Failure example:** detector benchmark success is reported as production certification or Expression Moment approval.
- **Evidence/test layer:** receipt/status-policy validation.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

Required exact future tests:

- `tests/unit/test_frame_coordinate.py::test_vfr_coordinate_round_trip_is_exact`
- `tests/unit/test_frame_coordinate.py::test_nominal_fps_is_not_an_exact_locator`
- `tests/unit/test_shot_map_partition.py::test_every_presentation_frame_is_covered_once`
- `tests/unit/test_shot_map_partition.py::test_gap_overlap_and_out_of_order_boundaries_fail`
- `tests/unit/test_transition_observation.py::test_transition_range_links_adjacent_shots`
- `tests/unit/test_transition_observation.py::test_bare_confidence_float_is_rejected`
- `tests/unit/test_keyframe_selection.py::test_every_shot_has_representative`
- `tests/unit/test_keyframe_selection.py::test_selection_reasons_are_closed_and_nonsemantic`
- `tests/unit/test_visual_observation_applicability.py::test_geometry_not_applicable_requires_evidence`
- `tests/unit/test_visual_change_not_semantic_importance.py::test_boundary_cannot_create_moment_or_route`

Property tests vary frame counts, rational timebases, duplicate timestamps, transition spans, shot partitions, canonical insertion order, and correction ranges.

### 10.2 Contract and schema tests

- Validate every logical type’s required fields, unions, enums, owners, refs, digest format, range invariants, and no permissive defaults.
- Use canonical positive/negative vectors for `FrameCoordinate`, boundary decision, shot map, keyframe set, visual observation, visual reference index, aggregate, command, event, and receipt.
- Verify the `TS-INT-001` mapping preserves exact refs, owner, version, digest, lifecycle, compatibility, package version, and binding receipt.
- Reject parsing-only adapters that ignore profile enforcement, source authority, or nonsemantic labels.

### 10.3 Integration and architecture tests

- Run complete analysis from exact admitted video through component binding with a deterministic test binding.
- Fault-inject every persistence boundary and assert atomic rollback.
- Exercise idempotent retry after acknowledgement loss and concurrent correction conflicts.
- Assert that Interview Expression source modules do not import AIR semantic compiler, Pipeline executor, VAE production, Studio repository, or Delegation implementation modules.
- Assert that Studio integration is projection/command-only and that later moment derivation consumes refs without write access to visual-index history.
- Assert no command or record exposes `semantic_importance`, `approved_expression_moment`, or equivalent authority.

### 10.4 Detection, transition, and keyframe evidence

A future build must supply governed fixture media and exact expected outputs for:

- single-shot constant-frame-rate source;
- variable-frame-rate source;
- already-edited hard cuts;
- dissolve, fade, and profile-supported transition examples;
- rapid camera/framing changes with no semantic importance;
- short shots that interval sampling could miss;
- repeated or visually similar frames;
- corrupt/truncated media;
- no-face/non-subject inserts;
- restricted identity-frame export; and
- ambiguous/borderline boundaries requiring review.

Evidence includes input/source hashes, profile/binding hashes, complete detection output, accepted/rejected decision records, frame hashes, source-time validation, and sampled human review. No threshold or benchmark pass line is invented here; it must come from a governed profile/decision.

### 10.5 Determinism, replay, cancellation, and recovery

- Run canonical analysis twice in fresh processes with different hash seed, locale, timezone, environment, working directory, temp directory, and input discovery order.
- Rebuild projections from events and compare every canonical byte/hash.
- Verify historical query after correction, supersession, invalidation, cancellation, and source-authority revocation.
- Exercise cancellation before admission, during proposal, during materialization, before commit, and after commit.
- Crash between commit and outbox acknowledgement, recover, and prove one logical publication.
- Corrupt one artifact and prove quarantine identifies the first exact mismatch.

### 10.6 Migration and clean-environment tests

- Hash donor fixtures before and after migration to prove no mutation.
- Prove exact mappings where source media, stream/timebase, frame coordinates, digests, reasons, and authority are complete.
- Prove blocked migration for float-only timestamps, local-path-only images, unknown source bytes, missing method provenance, or ambiguous lifecycle.
- Export into a clean extracted layout and verify all logical URIs, artifact hashes, and query behavior.
- Scan canonical outputs for drive letters, UNC prefixes, checkout roots, usernames, temp directories, environment values, and traversal sequences.

### 10.7 Security, privacy, performance, and operational evidence

- Verify denied source-authority scopes produce no artifacts, outbox entries, telemetry payloads, or learning-store writes.
- Verify restricted frames and participant data never enter logs/metrics.
- Verify malformed media, excessive dimensions/duration, resource exhaustion, and decoder timeout produce typed bounded failures under separately governed resource policies.
- Measure probe, frame indexing, proposal, validation, keyframe materialization, exact query, replay, and invalidation fan-out on governed fixture classes. Report measurements and variance; do not claim an ungoverned SLO.
- Record dependency/license/binary provenance for every future implementation binding before adoption.

### 10.8 Reference-slice and downstream evidence

The imported-interview reference slice must prove:

1. an imported source remains truthful about absent planning history;
2. the exact video/source package produces a reproducible visual index;
3. shot/keyframe evidence is available to later moment derivation but creates no semantic meaning;
4. corrected visual evidence selectively invalidates only dependent later moments/programs/derivatives; and
5. Format 07, SuperVisual, animation, evaluation, Studio correction, HumanResolution, and replay consumers retain exact source refs without inheriting Format 02 certification.

### 10.9 Required later completion artifacts

A separately authorized build requires:

- source/build/file manifest with exact hashes;
- profile and implementation-binding registry snapshot;
- unit/property/contract/integration/architecture/migration/portability/security results;
- detection benchmark and sampled review evidence;
- frame/source-time hash matrix;
- atomic fault-injection matrix;
- deterministic fresh-context reproduction receipt;
- selective-invalidation graph and recovery receipt;
- package-component mapping receipt;
- clean-room export and absolute-path scan;
- dependency/license disposition;
- independent audit, bounded revision where required, independent re-audit, and attributable acceptance; and
- explicit non-production/non-certification status until later authority proves otherwise.

### 10.10 Draft dependency and lifecycle handoff

This specification consumed `TS-INT-001` at SHA-256 `ca13c9fdcc3b840533de2a955a5388497a434a0b7f94950978012536fd4301e8`, quality state `WRITTEN_PENDING_AUDIT`, labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. A changed upstream hash reopens the six downstream revision-impact sections before re-audit.

The next lifecycle action is independent audit by an agent that did not write this specification. The writer has not audited, revised, accepted, implemented, built, released, certified, or issued a Development Capsule.
