---
document_type: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-VID-002
title: Talking-Head A-Roll Selection, Word-Boundary EDL, and Output-Time Mapping
product: Atomic Harness Pipeline
version: 2.1.0-candidate
issued_on: '2026-07-22'
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 13
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs: [FR-069, FR-139, FR-140, FR-141]
controlling_stories: [ST-04.02]
upstream_draft_dependencies:
  - {edge_id: SDE-062, spec_id: TS-VID-001, quality_state: WRITTEN_PENDING_AUDIT, sha256: cfa33fdc9fcfc0a98c1b73f9ef6ed970b906774f5f87deb33fbde8fd385c2cd8, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-063, spec_id: TS-INT-004, quality_state: WRITTEN_PENDING_AUDIT, sha256: e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-VID-002 - Talking-Head A-Roll Selection, Word-Boundary EDL, and Output-Time Mapping

This candidate specifies contracts only. It authorizes no code, schema or contract release, Development Capsule, provider call, render, publication, product adoption, certification, or `ACCEPTED_FOR_BUILD` claim.

## 1. Files and authorities read

### 1.1 Frozen Wave 13 inputs

| Upstream draft | State and SHA-256 | Interface admitted for writing | Required revision impact if its hash changes |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-VID-001.md` | `WRITTEN_PENDING_AUDIT`; `cfa33fdc9fcfc0a98c1b73f9ef6ed970b906774f5f87deb33fbde8fd385c2cd8` | The immutable source registration, rational time types, source/output mapping vocabulary, `PRIMARY_A_ROLL_SPINE`, and sole canonical `VideoEditProgram`. | Reopen sections 3, 5, 6, 8, 9 and 10; rebind every affected interface and rerun downstream impact review. |
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-004.md` | `WRITTEN_PENDING_AUDIT`; `e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a` | The IE-owned approved `ExpressionMoment`, exact boundary/source spans, phrase/word/speaker/audio/visual evidence, approval receipt, route constraints and lifecycle. | Reopen sections 3, 5, 6, 8, 9 and 10; invalidate derived eligibility sets, candidate portfolios, decisions and EDLs that bind the old hash. |

Both inputs are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their exact hashes are writing inputs, not evidence that either draft is ratified, audited, accepted, build-ready or adopted. Constitution V1.1 and other current authorities prevail. Prompt 02C authorizes candidate-specification work only.

### 1.2 Current authority, requirements and writing controls

| Source | State / SHA-256 | Class | Fact used by this specification |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest current authority | Pipeline executes an already-authorized Harness and preserves human reaction, source and Activative lineage; editing cannot become semantic authority. |
| AHP `prd/PRD_COMBINED.md` | `1.2.0-draft`; `387568731acfe57f022a2fadcd2acfc73baf1287b8a5a1e1d3ed78675ccb067d` | candidate product PRD | Original talking-head expression remains the source-led short's A-roll spine; source meaning and approved composition precede execution. |
| F12 `Source-First Short-Form Video Editing and Adopted Timeline Runtime` | candidate; `ae65689ae06ccf8b01dbba407ab093fd77cf01a74637f0ba0f7c16c053ae1a01` | controlling feature | FR-069 requires word/audio-event-safe source intervals, declared function, and deterministic source-to-output time. |
| F24 `Talking-Head A-Roll Short-Video Production` | candidate; `5aab16f89bda9f3838168733c774e3cff61abae09557edca637de8402c5cb741` | controlling feature | FR-139 through FR-141 require a source-backed A-roll spine, bounded span-selection portfolio, exact word/silence boundaries and production-aware cut evidence. |
| AHP `EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | controlling Story | ST-04.02 requires a truthful word-safe talking-head spine and rejects generated paraphrase labeled interview-derived. |
| `planning/spec_assignments/TS-VID-002.md` | assignment only; `7b96faa1e62c2d9141b2e9b12027f35698850ec7c4e6977051b81d88979e9840` | scope evidence | Names the candidate-selection, EDL, source/output mapping and predecessor scope; its old target path is not path authority. |
| Program Control cross-product and semantic ownership matrices | candidate; `cd92d291...` / `232a9153...` | ownership evidence | IE owns live-source and Expression Moment evidence; AIR owns semantic-program meaning; Pipeline owns temporal execution; Studio projects; workers/renderers execute. |
| `SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | write gate | Writing and later technical review are permitted; build, production and certification remain false. |

### 1.3 Required source and predecessor evidence

| Source ID / path | SHA-256 | Disposition | Evidence used |
|---|---|---|---|
| `SRC-INT-001` - interview-first doctrine | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE` | Original human expression and source media remain the grounding evidence; a derivative multiplies rather than replaces them. |
| `SRC-LEG-006` - `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/video_editing_engine.py` | `38edbceab7152ae1d09d131936bc1625ced13d384932f333acca4425954d4bd7` | `REQUIRED_UNIQUE_EVIDENCE` | Supplies useful A-roll, source, track, layer, timing and caption vocabulary, but uses random/current-time defaults, millisecond integers, open maps and weak refs that cannot be canonical. |
| `SRC-LEG-007` - `THE_CMF_STUDIO(2)/src/ccp_studio/services/video_editing_engine_service.py` | `3d13c36601d1719b5b6c826ae43e9e24a71a77e61f92137396cad60649472e05` | `REQUIRED_UNIQUE_EVIDENCE` | Shows a thin mutable in-memory orchestration pattern without atomic state/receipt/event closure. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_video_editing_engine_v1.py` | `ad33f9106a1da01c404b5e7dc617a0b14cd5d53e96ec18fe805a46dadf3933b4` | relevant predecessor test evidence | Exercises a local A-roll timeline vocabulary but does not prove exact word cuts, quote integrity, source/output mapping, deterministic identity or durable replay. |

`SRC-AM-002` and `SRC-EXT-017`, `SRC-EXT-018`, `SRC-EXT-019`, `SRC-EXT-020`, `SRC-EXT-023`, and `SRC-EXT-024` are `DEFERRED_REFERENCE`. This specification attributes no algorithm, threshold, performance, licensing, provider or product claim to those unavailable or reference-only sources. Their absence is nonblocking under the current Source Disposition Ledger.

The target is a `DIRECT_PRODUCT_SPEC_PATH`. The recovery packet records no applicable `AGENTS.md` in the target or its ancestors and grants explicit Prompt 02/02C specification-path authority.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure without this specification

A timeline system can place source media on an A-roll track and still create a false interview-derived short. A selector can favor a catchy phrase while dropping its premise, remove hesitation or reaction evidence, cut through a spoken word, reorder statements without disclosing the change, synthesize a cleaner paraphrase, or assign output positions that cannot be recomputed from source intervals. A technically valid clip list then appears authoritative although neither the exact IE approval nor the AIR-owned semantic purpose licensed the resulting reading.

The predecessor makes the risk worse: caller-created IDs, millisecond offsets, arbitrary source refs, mutable upserts and open dictionaries allow a selection, timeline and receipt to drift independently. A reload can retain a timeline without the evidence that justified it, or retain a receipt while the chosen clip set has changed.

### 2.2 User and system outcome

Given one exact approved IE `ExpressionMoment`, its current approval and source scope, an exact source registration and `VideoEditProgram`, and immutable AIR/Harness constraints, the operator receives:

1. an inspectable portfolio of source-only A-roll sequence candidates;
2. deterministic eligibility and boundary evidence for every proposed interval;
3. an independently selected candidate rather than a selector self-approval;
4. an immutable word/audio-boundary EDL whose source and output times recompute exactly; and
5. a new `VideoEditProgram` version containing the `PRIMARY_A_ROLL_SPINE`, with complete dependency, decision, invalidation and replay receipts.

The original source, IE meaning and approval remain visible. A polished or short candidate is not accepted merely because it fits duration.

### 2.3 Bounded solution

This specification defines an `ARollSelectionCase` that:

- admits exact, hash-pinned IE, AIR, Harness and `VideoEditProgram` inputs;
- compiles an eligibility corpus without inventing words, boundaries or authority;
- requests a bounded candidate portfolio from a declared selector implementation;
- performs deterministic source, context, boundary, duration and lineage validation;
- requires an independent evaluation and authorized selection decision;
- compiles a rational-time `ARollEditDecisionList` and exact `SourceToOutputTimeMap`;
- commits the EDL, decision, receipts, dependency edges and a successor `VideoEditProgram` atomically;
- invalidates only affected descendants when source, approval, semantic or program inputs change; and
- reproduces historical accepted states from immutable bytes and events.

### 2.4 In scope

- FR-069, FR-139, FR-140, FR-141 and ST-04.02 only.
- Selection among already-authorized source intervals for an interview-derived, source-led short.
- Exact context windows, must-preserve/exclude rules, reaction/tail treatment and source-order declarations.
- Word, permitted silence and audio-event boundary validation.
- Candidate portfolio, evaluation, operator decision, EDL and output-time-map contracts.
- Compilation into the TS-VID-001 `PRIMARY_A_ROLL_SPINE` as a new immutable program version.
- Deterministic identity, idempotency, optimistic concurrency, atomic persistence, selective invalidation and replay.
- Lossless-or-blocked migration of applicable predecessor evidence.
- Exact future implementation and test locations.

### 2.5 Out of scope and non-goals

- Creating, correcting, approving or reinterpreting source packages, transcripts, speakers, Expression Moments, Reaction Receipts or source authority.
- Compiling Primitive/archetype, role/tension, Matrix, Final Script, Activation Transfer, Visual DNA or other AIR-owned meaning.
- Selecting captions, B-roll, SuperVisuals, animations, music, sound design, transitions, render engines or provider workflows.
- Final video rendering, mouth-discontinuity certification, caption rendering, publication or production acceptance.
- Replacing `VideoEditProgram` with an EDL, OTIO document, UI state or renderer timeline.
- Generating, cloning, redubbing or paraphrasing speech and labeling it interview-derived.
- Inventing boundary tolerances, target-duration thresholds, ranking weights, model capability claims or evaluator certification.
- Activating Format 02 or inferring certification from the Release 1 reference path.

## 3. Governing decisions and constraints

### 3.1 Authority stage and ownership

Constitution V1.1 is current. Candidate V2.1 authority, the AHP PRD, features, Story and upstream specs remain `CANDIDATE_NOT_CURRENT`. Specification work is authorized; build authority is false; the maximum later state before required ratification is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

Ownership is non-transferable:

- Interview Expression owns source-package identity, exact words/speakers/audio and visual evidence, Expression Moment boundary/meaning, Reaction Receipt evidence, approval, source scope and correction.
- AIR owns Activative purpose, Primitive/archetype coalition, role/tension, Matrix, Final Script, Activation Transfer and other semantic-program meaning.
- Builder/Harness authority declares category, duration/profile, sequence role, approved semantic dependencies and constraints.
- Pipeline owns the bounded technical selection case, candidate evaluation orchestration, EDL, source/output time mapping and `VideoEditProgram` version.
- Studio may project and request typed corrections. It does not own hidden timeline or semantic state.
- Renderers and workers execute a pinned program. VAE visual-production authority does not authorize A-roll source rewriting.
- Delegation transports immutable messages and receipts; it does not select or reinterpret content.

`Activative Contract Compiler != Activative Intelligence Runtime`, and neither is the A-roll selector.

### 3.2 The approved source remains the A-roll spine

An interview-derived source-led short MUST contain a non-empty `PRIMARY_A_ROLL_SPINE` made only from the exact approved original source media and permitted immutable derivatives that preserve source identity. Generated or reconstructed talking-head footage, synthetic voice, dubbed language, avatar speech, reenactment or paraphrase MUST NOT satisfy the A-roll requirement.

Supporting visual or audio layers may later cover portions of the output only under separately authorized functions. They do not erase the A-roll spine, its source/output map or its auditability. `NOT_APPLICABLE` is forbidden for the A-roll spine in this category.

### 3.3 No semantic reconstruction during selection

The selector receives immutable semantic and source constraints. It may rank permitted source sequences against declared goals, but MUST NOT:

- author or clean up a quote;
- infer omitted premise as if present;
- convert a model summary into spoken evidence;
- change an Expression Moment boundary or approval;
- create a new Activative Call, role, tension, Matrix reading or transfer;
- treat duration fit, predicted engagement or edit smoothness as authority to change meaning;
- guess a missing source kind, speaker, word boundary, reaction meaning or source scope.

When the requested duration cannot preserve the licensed reading, the outcome is `TARGET_DURATION_INFEASIBLE`, not a shorter false edit.

### 3.4 One temporal truth and one EDL role

TS-VID-001 `VideoEditProgram` remains the sole canonical temporal program. `ARollEditDecisionList` is an immutable decision artifact that compiles a new A-roll-spine version into that program. It MUST NOT become a second mutable timeline, renderer contract, editor-session document or hidden current state.

Every EDL identifies the predecessor program version/hash and the successor program version/hash. Reapplying an identical accepted EDL to the same predecessor is idempotent. Applying it to a different current version fails optimistic concurrency; it never rebases silently.

### 3.5 Exact source boundaries

Canonical time uses the TS-VID-001 integer-ticks-plus-positive-rational-timebase representation. Float seconds, nominal FPS and UI pixel locations are diagnostics only.

A cut boundary is permitted only when it resolves to one of:

- a validated word start or word end owned by IE;
- an explicitly permitted silence interval;
- an explicitly permitted non-speech audio-event boundary; or
- the exact approved source-span boundary when the approval proves that boundary safe.

The boundary record includes the exact word/event/span reference, time, source timebase, declared padding, alignment limitation and evidence hash. A UI snap, waveform pixel, subtitle cue edge or model-predicted timestamp is insufficient. A boundary with unresolved overlap, diarization conflict or timing limitation blocks selection unless the IE-owned evidence explicitly permits it.

### 3.6 Context, reactions and order

Each eligible span declares how it preserves the approved Expression Moment's premise/cause, core, turn/landing and reaction tail. `must_preserve` and `must_exclude` sets are hard constraints. Hesitations, laughter, breath, sigh, silence, speaker handoff and reaction tails remain eligible evidence; they are not noise by default.

Removing a reaction or tail requires an explicit, source-authorized decision and a reason compatible with the Expression Moment approval. A semantic reaction cannot be removed solely by a generic silence-removal, pace, cleanup or duration rule.

Source order is the default. Any reorder MUST identify every moved span, old and new ordinal, governing semantic/sequence constraint, continuity risk and authorizing decision. Hidden reorder is invalid.

### 3.7 Independent selection and no self-approval

The candidate generator and acceptance evaluator are distinct declared roles. A model or heuristic may propose candidates, reasons and scores; those values are untrusted proposals. Deterministic validators verify hard constraints, and an independent evaluator or authorized human chooses or rejects the portfolio. The same invocation identity MUST NOT both generate and issue the final selection decision.

Capability presence is not certification. A local successful candidate generation, synthetic test or evaluator declaration does not prove production evaluator certification.

### 3.8 Determinism, portability and claim ceiling

Canonical identities and rankings MUST NOT depend on current time, random state, dictionary insertion order, filesystem traversal order, locale, hostname, drive letter, absolute path, environment variable, process scheduling or provider response order. If a stochastic selector is admitted, it MUST receive an explicit seed and frozen model/profile/version; candidate identity still derives from normalized candidate content, not invocation order.

All canonical maps serialize with ordered keys and ordered collections under a versioned canonicalization profile. Portable logical/content-addressed refs replace local paths. Evidence timestamps and diagnostic host data are excluded from semantic hashes.

This draft cannot claim adoption, implementation, production eligibility, certification or build readiness.

## 4. Current brownfield architecture

### 4.1 Reusable predecessor concepts

The predecessor `video_editing_engine.py` usefully distinguishes source media, A-roll tracks, primary-source layers, scene timing, captions, audio and a timeline program. Its service demonstrates one orchestration façade, and its test suite demonstrates local construction and negative validation patterns. These concepts may guide names and adapter boundaries.

### 4.2 Brownfield gaps against the governing invariants

The predecessor cannot be adopted directly because it:

- assigns random identifiers and current-time defaults;
- represents canonical time as unqualified integer milliseconds;
- accepts arbitrary string source refs and caller-supplied hashes;
- uses open dictionaries and `Any` where closed contracts are required;
- permits mutable object updates and current-state upserts without aggregate/version preconditions;
- has no exact Expression Moment approval, word/phrase/speaker/audio-event or AIR semantic binding;
- has no candidate portfolio, independent selection decision or word-boundary receipt;
- cannot prove a complete deterministic source/output mapping;
- stores timeline state without a corresponding atomic command/event/receipt closure;
- lacks selective descendant invalidation and historical replay guarantees; and
- tests synthetic `file://` media, fake renders and active historical Format 02 assumptions that cannot establish current production trust.

### 4.3 Brownfield disposition

| Component | Disposition | Rule |
|---|---|---|
| Track/layer/source/timeline vocabulary | `ADAPT` | Map only through typed, exact, immutable TS-VID-001 contracts. |
| `VideoTimelineProgram` as mutable current record | `SUPERSEDE` | `VideoEditProgram` remains sole immutable temporal truth. |
| Random IDs and clock-derived identity | `REJECT` | Caller-supplied command IDs and canonical content hashes only. |
| Integer-ms interval inputs | `MIGRATE_LOSSLESS_OR_BLOCK` | Convert only with declared timebase and exact divisibility/proof. |
| Open dict/`Any` metadata | `MIGRATE_TYPED_OR_BLOCK` | No unknown semantic fields are flattened into notes. |
| In-memory upsert/lock behavior | `ARCHIVE_AS_PREDECESSOR_EVIDENCE` | It is not a persistence or replay implementation. |
| Existing tests | `RETAIN_AS_MIGRATION_FIXTURES` | Add current invariant tests; do not count fake renders as acceptance. |

No predecessor object is current authority. Migration creates new immutable artifacts and never edits historical bytes.

## 5. Proposed architecture and workflows

### 5.1 Components and boundaries

| Component | Responsibility | Explicitly forbidden |
|---|---|---|
| `ARollSelectionCommandService` | Validate command identity, authority, exact aggregate version and input hashes; orchestrate the state machine. | Selecting meaning or mutating source/AIR/Harness inputs. |
| `ExpressionMomentSelectionAdapter` | Resolve exact TS-INT-004 moment, approval, boundary, Reaction Receipt and source evidence by version/hash. | Querying `latest`, correcting boundaries or manufacturing missing refs. |
| `VideoEditProgramAdapter` | Resolve source registration, timebase and predecessor `VideoEditProgram`; compile typed A-roll elements into a successor. | Maintaining an independent timeline. |
| `ARollEligibilityCompiler` | Produce the finite authorized interval and constraint set. | Inferring classification, thresholds or approval. |
| `ARollCandidateGenerator` | Propose a bounded, deterministically ordered portfolio under a frozen selector profile. | Accepting its own output or inventing words. |
| `WordAudioBoundaryValidator` | Verify exact cut points, padding, protected words, silence/audio events and limitations. | Using subtitle/display positions as canonical evidence. |
| `ARollContextValidator` | Check premise/core/turn/tail, speaker, quote reconstruction, source order and must-preserve/exclude constraints. | Reinterpreting the Expression Moment. |
| `ARollSelectionEvaluator` | Independently evaluate hard constraints and declared ranking evidence. | Claiming evaluator certification or changing constraints. |
| `ARollDecisionService` | Apply an authorized human/system decision to one validated candidate. | Silent auto-approval or selection by generator invocation. |
| `ARollEDLCompiler` | Compile exact EDL entries and source/output map from the selected candidate. | Rounding canonical time or creating output-only clips. |
| `ARollProgramCommitService` | Atomically persist aggregate, artifacts, receipts, events, dependencies and successor program. | Partial writes, overwrite or hidden rebase. |
| `ARollSelectionRepository` | Optimistic concurrency, idempotency, historical reads and dependency traversal. | Mutable singleton defaults or current-only history. |
| `ARollInvalidationProjector` | Project typed upstream changes to exact descendants. | Deleting history or invalidating unrelated jobs. |

### 5.2 Aggregate state machine

The immutable `ARollSelectionCase` follows:

`OPEN -> EVIDENCE_FROZEN -> ELIGIBILITY_COMPILED -> CANDIDATES_PROPOSED -> VALIDATED -> SELECTED -> EDL_COMPILED -> PROGRAM_SUPERSEDED`

Terminal or side states are `BLOCKED`, `CANCELLED`, `SUPERSEDED` and `INVALIDATED`. A blocked case may continue only through a new typed command whose expected version matches and whose evidence resolves the recorded blocker. A correction creates a successor; it never mutates a terminal historical version.

Allowed transitions and required artifacts are:

| Transition | Required input | Required artifact/receipt |
|---|---|---|
| open | exact command, job, source registration and predecessor program | `ARollSelectionOpenedReceipt` |
| freeze evidence | exact IE moment/approval and AIR/Harness refs | `SelectionEvidenceSnapshot` and dependency edges |
| compile eligibility | source boundary/context rules | `ARollEligibilitySet` and denial ledger |
| propose | frozen selector profile and eligibility hash | `ARollCandidatePortfolio` and generation receipt |
| validate | exact portfolio and profiles | deterministic validation receipts plus independent evaluation request/result |
| select | validated candidate and authorized actor | `ARollSelectionDecision` |
| compile EDL | decision and exact predecessor program | `ARollEditDecisionList`, boundary ledger and source/output map |
| supersede program | EDL and expected program version | new `VideoEditProgram`, atomic commit receipt and supersession edge |

### 5.3 End-to-end happy path

1. The caller submits `OpenARollSelectionCase` with command/idempotency keys; expected absent case; exact derivative job, source registration and predecessor `VideoEditProgram` versions/hashes; exact IE moment/approval versions/hashes; and exact AIR/Harness constraint refs.
2. The command service verifies every hash and authority scope, ensures the moment is approved and route-eligible for this derivative, and rejects stale, revoked, invalidated or superseded inputs.
3. The evidence adapter freezes the exact premise/cause, core, optional turn/landing and reaction-tail spans; words, phrases, speakers, audio events and visual references; source-use limitations; and approval constraints.
4. The eligibility compiler intersects the approved source scope with source registration and job constraints. It emits explicit eligible, required and excluded intervals. It never expands outside approval.
5. The generator proposes a finite portfolio. Each candidate is an ordered list of exact source intervals with purpose, context coverage, source-order relation, target-duration delta and generation evidence. Unsupported text is impossible because proposed quote text must reconstruct from referenced words.
6. Deterministic validators verify source identity, boundary class, context, speaker, quote reconstruction, reaction/tail decisions, source order, duration arithmetic, semantic refs and portability. Invalid candidates remain auditable but cannot be selected.
7. An independent evaluator examines validated candidates and records findings without changing them. An authorized actor issues `SelectARollCandidate` or rejects all candidates with typed reasons.
8. The EDL compiler assigns contiguous output intervals from exact source durations, compiles one mapping segment per A-roll interval, records cut-in/cut-out evidence and emits caption/audio handoff requirements. It performs no rendering.
9. The program adapter compiles a successor `VideoEditProgram` with one non-empty `PRIMARY_A_ROLL_SPINE`. EDL and program hashes cross-bind.
10. One atomic commit writes case version, EDL, map, decision, validations, command record, domain events, dependency edges, program successor and commit receipt. Only then is the new aggregate version visible.

### 5.4 Candidate-generation and ranking law

The generator profile declares implementation ID/version/hash, deterministic/stochastic mode, explicit seed when applicable, maximum candidate count, feature contract and supported requirement set. A candidate is rejected before ranking when any hard constraint fails. Ranking applies only among valid candidates.

The profile may expose named signals such as duration fit, sequence coverage, source continuity or expression completeness, but their definitions and weights are immutable profile data. This spec sets no universal weights or thresholds. Missing required profile features produce `SELECTOR_PROFILE_UNSUPPORTED`.

The portfolio canonical order is `(hard_constraint_status, declared_rank_tuple, candidate_content_hash)`. Provider return order is never canonical. Equal ranks resolve by content hash, not arrival order.

### 5.5 Boundary and output-time compilation

For every selected segment, the compiler:

1. resolves the requested source start/end to exact IE evidence;
2. verifies half-open interval ordering and source timebase;
3. verifies cut-in and cut-out boundary decisions;
4. applies only declared padding bounded by source authorization and neighboring protected intervals;
5. computes duration as exact rational subtraction;
6. assigns the next output start from the prior output end;
7. records any declared transition overlap/gap as a separate typed mapping rule rather than hiding it in arithmetic;
8. verifies the union of mapped A-roll output intervals exactly equals the declared A-roll-spine coverage; and
9. produces forward and reverse lookup indexes that return exact refs or an explicit unmapped interval.

Spoken A-roll is 1:1 time by default. Any speed change, time warp, reverse, interpolation or voice timing alteration is unsupported here and must be blocked unless a later ratified contract supplies explicit source/semantic authority and mapping rules.

### 5.6 Correction, invalidation and replay workflow

An upstream event identifies exact old/new versions and changed evidence paths. The invalidation projector traverses persisted dependency edges:

- changed word/phrase timing invalidates boundary decisions, affected candidates, EDL entries, mapping segments and successor program elements;
- changed Expression Moment boundary/approval invalidates every eligibility/candidate/decision derived from it;
- revoked source scope invalidates all dependent selection/program versions from current consumption while preserving history;
- changed AIR/Harness semantic or sequence constraint invalidates candidates whose stated functions bind the changed ref;
- changed unrelated keyframe or source interval does not invalidate a selection with no dependency edge to it;
- a changed upstream draft hash requires the section-level specification impact review declared in section 1 before later lifecycle advancement.

Replay loads immutable artifacts/events by exact identity, verifies hashes and reducers, and reconstructs the selected historical state without resolving aliases or current inputs. Re-evaluation is a new command and new artifact; it never overwrites historical evidence.

## 6. Data models, contracts, schemas, and APIs

All records are closed, versioned and immutable. Unknown enum values or fields fail the supported contract unless an explicit compatibility profile says otherwise. `NonEmptyString`, `Sha256`, `ArtifactRef`, `VersionRef`, `CommandId`, `IdempotencyKey`, `ActorRef`, `AuthorityRef`, `RationalTime` and `TimeInterval` reuse exact Program Control/TS-VID-001 value-object semantics.

### 6.1 `ARollSelectionCase`

```text
ARollSelectionCase {
  case_id: ARollSelectionCaseId
  aggregate_version: PositiveInteger
  state: ARollSelectionState
  derivative_job_ref: VersionedArtifactRef
  source_registration_ref: VersionedArtifactRef
  predecessor_video_edit_program_ref: VersionedArtifactRef
  expression_moment_ref: VersionedArtifactRef
  expression_moment_approval_ref: VersionedArtifactRef
  air_semantic_program_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  harness_constraint_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  evidence_snapshot_ref?: VersionedArtifactRef
  eligibility_set_ref?: VersionedArtifactRef
  candidate_portfolio_ref?: VersionedArtifactRef
  validation_receipt_refs: OrderedSet<VersionedArtifactRef>
  selection_decision_ref?: VersionedArtifactRef
  a_roll_edl_ref?: VersionedArtifactRef
  successor_video_edit_program_ref?: VersionedArtifactRef
  blocker_refs: OrderedSet<VersionedArtifactRef>
  dependency_edge_refs: OrderedSet<DependencyEdgeRef>
  predecessor_case_ref?: VersionedArtifactRef
  semantic_hash: Sha256
}
```

Only fields valid for the current state may be populated. Required fields cannot be replaced with an empty list, null, free-text note or `NOT_APPLICABLE` unless a field's contract expressly permits evidenced non-applicability.

### 6.2 `SelectionEvidenceSnapshot`

```text
SelectionEvidenceSnapshot {
  snapshot_id: ContentDerivedId
  source_package_ref: VersionedArtifactRef
  source_media_ref: VersionedArtifactRef
  source_media_digest: Sha256
  source_registration_ref: VersionedArtifactRef
  expression_moment_ref: VersionedArtifactRef
  expression_moment_boundary_ref: VersionedArtifactRef
  approval_receipt_ref: VersionedArtifactRef
  source_authority_scope_ref: VersionedArtifactRef
  premise_or_cause_span_refs: OrderedSet<ExpressionSourceSpanRef>
  core_span_refs: NonEmptyOrderedSet<ExpressionSourceSpanRef>
  turn_or_landing_span_refs: OrderedSet<ExpressionSourceSpanRef>
  reaction_tail_span_refs: OrderedSet<ExpressionSourceSpanRef>
  phrase_refs: NonEmptyOrderedSet<PhraseRef>
  word_refs: NonEmptyOrderedSet<WordRef>
  speaker_assertion_refs: NonEmptyOrderedSet<SpeakerAssertionRef>
  audio_event_refs: OrderedSet<AudioEventRef>
  visual_evidence_refs: OrderedSet<VisualEvidenceRef>
  reaction_receipt_refs: OrderedSet<VersionedArtifactRef>
  route_constraints: OrderedSet<TypedConstraint>
  source_limitations: OrderedSet<TypedLimitation>
  air_function_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  activation_transfer_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  harness_constraints: NonEmptyOrderedSet<TypedConstraint>
  exact_text_reconstruction_hash: Sha256
  input_manifest_hash: Sha256
  semantic_hash: Sha256
}
```

Interview-derived source kind requires the non-empty Reaction Receipt and Expression Moment provenance already governed by the shared contract. This adapter validates their presence and exact identity; it does not create a local source-kind field or reconstruct missing provenance.

### 6.3 `ARollEligibilitySet`

```text
ARollEligibilitySet {
  eligibility_set_id: ContentDerivedId
  evidence_snapshot_ref: VersionedArtifactRef
  source_timebase: PositiveRational
  eligible_spans: NonEmptyOrderedSet<ARollEligibleSpan>
  must_preserve_refs: NonEmptyOrderedSet<SourceEvidenceRef>
  must_exclude_refs: OrderedSet<SourceEvidenceRef>
  protected_boundary_refs: OrderedSet<SourceEvidenceRef>
  permitted_boundary_classes: NonEmptyOrderedSet<BoundaryClass>
  source_order_policy: PRESERVE | EXPLICIT_AUTHORIZED_REORDER
  target_duration_constraint: TypedConstraint
  selector_requirement_set: NonEmptyOrderedSet<FeatureRequirement>
  denial_ledger: OrderedSet<EligibilityDenial>
  profile_ref: VersionedArtifactRef
  semantic_hash: Sha256
}

ARollEligibleSpan {
  eligible_span_id: ContentDerivedId
  source_interval: TimeInterval
  expression_source_span_refs: NonEmptyOrderedSet<ExpressionSourceSpanRef>
  phrase_refs: NonEmptyOrderedSet<PhraseRef>
  word_refs: NonEmptyOrderedSet<WordRef>
  speaker_assertion_refs: NonEmptyOrderedSet<SpeakerAssertionRef>
  audio_event_refs: OrderedSet<AudioEventRef>
  visual_evidence_refs: OrderedSet<VisualEvidenceRef>
  expression_role: PREMISE_OR_CAUSE | CORE | TURN_OR_LANDING | REACTION_TAIL
  semantic_function_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  allowed_padding_before: TimeInterval
  allowed_padding_after: TimeInterval
  source_authority_scope_ref: VersionedArtifactRef
  limitations: OrderedSet<TypedLimitation>
  semantic_hash: Sha256
}
```

`allowed_padding_*` is an authorized interval, not a guessed duration. Empty eligibility is a typed blocker, not an empty successful portfolio.

### 6.4 Candidate portfolio and independent evaluation

```text
ARollCandidatePortfolio {
  portfolio_id: ContentDerivedId
  case_ref: VersionedArtifactRef
  eligibility_set_ref: VersionedArtifactRef
  selector_profile_ref: VersionedArtifactRef
  selector_implementation_digest: Sha256
  deterministic_mode: Boolean
  explicit_seed?: Integer
  candidates: NonEmptyOrderedSet<ARollSequenceCandidate>
  canonical_order_rule: NonEmptyString
  generation_receipt_ref: VersionedArtifactRef
  semantic_hash: Sha256
}

ARollSequenceCandidate {
  candidate_id: ContentDerivedId
  segments: NonEmptyOrderedSet<ARollCandidateSegment>
  reconstructed_verbatim_text: NonEmptyString
  reconstructed_text_hash: Sha256
  source_order_changes: OrderedSet<SourceOrderChange>
  expression_role_coverage: NonEmptyOrderedSet<ExpressionRoleCoverage>
  reaction_tail_decisions: OrderedSet<ReactionTailDecision>
  exact_source_duration: RationalDuration
  exact_output_duration_preview: RationalDuration
  target_duration_delta: RationalDuration
  semantic_function_coverage: NonEmptyOrderedSet<VersionedArtifactRef>
  declared_rank_signals: OrderedMap<SignalId, CanonicalScalar>
  generation_reason_refs: NonEmptyOrderedSet<EvidenceRef>
  limitation_refs: OrderedSet<TypedLimitation>
  semantic_hash: Sha256
}

ARollSelectionEvaluationReceipt {
  receipt_id: ContentDerivedId
  portfolio_ref: VersionedArtifactRef
  candidate_ref: VersionedArtifactRef
  evaluator_identity: EvaluatorIdentity
  evaluator_profile_ref: VersionedArtifactRef
  generator_identity: GeneratorIdentity
  independence_result: PASS | FAIL
  source_identity_result: PASS | FAIL
  verbatim_reconstruction_result: PASS | FAIL
  source_authority_result: PASS | FAIL
  expression_context_result: PASS | FAIL
  semantic_alignment_result: PASS | FAIL
  word_audio_boundary_result: PASS | FAIL
  reaction_tail_result: PASS | FAIL
  source_order_result: PASS | FAIL
  duration_arithmetic_result: PASS | FAIL
  a_roll_spine_result: PASS | FAIL
  visible_discontinuity_risk: NOT_EVALUATED_UNTIL_RENDER | EVIDENCE_REQUIRED
  findings: OrderedSet<TypedFinding>
  pass_status: PASS | FAIL
  evaluated_artifact_hash: Sha256
  semantic_hash: Sha256
}
```

The `visible_discontinuity_risk` field cannot report rendered pass in this pre-render stage. FR-141's visible-mouth continuity requirement remains a mandatory downstream render-evaluation gate. Mechanical boundary validity does not satisfy it.

### 6.5 Boundary decisions

```text
WordAudioBoundaryDecision {
  decision_id: ContentDerivedId
  source_media_ref: VersionedArtifactRef
  boundary_time: RationalTime
  boundary_side: CUT_IN | CUT_OUT
  boundary_class: WORD_START | WORD_END | PERMITTED_SILENCE | PERMITTED_AUDIO_EVENT | APPROVED_SPAN_EDGE
  word_ref?: WordRef
  audio_event_ref?: AudioEventRef
  expression_source_span_ref: ExpressionSourceSpanRef
  requested_padding: RationalDuration
  applied_padding: RationalDuration
  protected_word_refs: OrderedSet<WordRef>
  alignment_evidence_refs: NonEmptyOrderedSet<EvidenceRef>
  limitation_refs: OrderedSet<TypedLimitation>
  profile_ref: VersionedArtifactRef
  result: PASS | FAIL
  reason_codes: OrderedSet<BoundaryReasonCode>
  semantic_hash: Sha256
}
```

Presence rules are closed: `WORD_START`/`WORD_END` require exactly one `word_ref`; `PERMITTED_AUDIO_EVENT` requires exactly one `audio_event_ref`; other classes forbid those refs unless the profile explicitly requires corroboration. Padding cannot cross the approved source scope, a protected word or an excluded interval.

### 6.6 Selection decision

```text
ARollSelectionDecision {
  decision_id: ContentDerivedId
  case_ref: VersionedArtifactRef
  portfolio_ref: VersionedArtifactRef
  selected_candidate_ref?: VersionedArtifactRef
  disposition: SELECTED | REJECT_ALL | HUMAN_RESOLUTION_REQUIRED
  decision_actor_ref: ActorRef
  decision_authority_ref: AuthorityRef
  generator_identity: GeneratorIdentity
  evaluator_identity: EvaluatorIdentity
  independence_assertion: PASS
  evaluation_receipt_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  reason_codes: NonEmptyOrderedSet<SelectionReasonCode>
  human_resolution_ref?: VersionedArtifactRef
  evidence_manifest_hash: Sha256
  semantic_hash: Sha256
}
```

`SELECTED` requires one candidate and all hard-constraint receipts passing. `REJECT_ALL` forbids a candidate. `HUMAN_RESOLUTION_REQUIRED` requires the governed request and cannot compile an EDL. Actor authorization is checked against the frozen job/approval scope.

### 6.7 `ARollEditDecisionList`

```text
ARollEditDecisionList {
  edl_id: ContentDerivedId
  case_ref: VersionedArtifactRef
  decision_ref: VersionedArtifactRef
  selected_candidate_ref: VersionedArtifactRef
  predecessor_video_edit_program_ref: VersionedArtifactRef
  source_registration_ref: VersionedArtifactRef
  source_timebase: PositiveRational
  output_timebase: PositiveRational
  entries: NonEmptyOrderedSet<ARollEDLEntry>
  source_output_time_map_ref: VersionedArtifactRef
  audio_boundary_plan_ref: VersionedArtifactRef
  caption_mapping_requirement_ref: VersionedArtifactRef
  exact_output_duration: RationalDuration
  a_roll_coverage: TimeIntervalSet
  source_order_change_refs: OrderedSet<SourceOrderChangeRef>
  validation_receipt_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  semantic_hash: Sha256
}

ARollEDLEntry {
  entry_id: ContentDerivedId
  ordinal: NonNegativeInteger
  source_package_ref: VersionedArtifactRef
  source_media_ref: VersionedArtifactRef
  source_stream_ref: VersionedArtifactRef
  source_interval: TimeInterval
  output_interval: TimeInterval
  expression_moment_ref: VersionedArtifactRef
  expression_boundary_ref: VersionedArtifactRef
  approval_receipt_ref: VersionedArtifactRef
  phrase_refs: NonEmptyOrderedSet<PhraseRef>
  word_refs: NonEmptyOrderedSet<WordRef>
  speaker_assertion_refs: NonEmptyOrderedSet<SpeakerAssertionRef>
  audio_event_refs: OrderedSet<AudioEventRef>
  visual_evidence_refs: OrderedSet<VisualEvidenceRef>
  semantic_function_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  activation_transfer_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  expression_role: PREMISE_OR_CAUSE | CORE | TURN_OR_LANDING | REACTION_TAIL
  cut_in_decision_ref: VersionedArtifactRef
  cut_out_decision_ref: VersionedArtifactRef
  padding_before: RationalDuration
  padding_after: RationalDuration
  source_order_ordinal: NonNegativeInteger
  output_order_ordinal: NonNegativeInteger
  transition_class: HARD_CUT | DECLARED_AUDIO_CROSSFADE | DECLARED_VISUAL_TRANSITION_SLOT
  cut_reason_codes: NonEmptyOrderedSet<CutReasonCode>
  limitations: OrderedSet<TypedLimitation>
  semantic_hash: Sha256
}
```

`transition_class` declares a handoff requirement only. It does not select a renderer transition or prove visible continuity. No entry may contain generated spoken content.

### 6.8 Exact source/output mapping

The EDL reuses and specializes the TS-VID-001 mapping contract:

```text
SourceToOutputTimeMapSegment {
  mapping_segment_id: ContentDerivedId
  edl_entry_ref: VersionedArtifactRef
  source_media_ref: VersionedArtifactRef
  source_interval: TimeInterval
  output_interval: TimeInterval
  rate: ExactRatio  // MUST equal 1/1 in this specification
  mapping_class: DIRECT_A_ROLL_SOURCE
  forward_transform: ExactAffineTransform
  reverse_transform: ExactAffineTransform
  source_word_refs: NonEmptyOrderedSet<WordRef>
  boundary_decision_refs: ExactlyTwo<VersionedArtifactRef>
  semantic_hash: Sha256
}

SourceToOutputTimeMap {
  map_id: ContentDerivedId
  edl_ref: VersionedArtifactRef
  predecessor_program_ref: VersionedArtifactRef
  segments: NonEmptyOrderedSet<SourceToOutputTimeMapSegment>
  declared_unmapped_output_intervals: OrderedSet<TypedUnmappedInterval>
  exact_a_roll_output_duration: RationalDuration
  continuity_receipt_ref: VersionedArtifactRef
  semantic_hash: Sha256
}
```

For every mapped time, forward then reverse conversion MUST return the original rational time. Adjacent mapped entries may meet exactly. Gaps and overlaps are forbidden unless represented by a typed, profile-authorized transition interval whose source and output behavior is explicit. No rounding residual may accumulate silently.

### 6.9 Commands, events and receipts

Commands are closed tagged unions:

- `OpenARollSelectionCase`
- `FreezeARollSelectionEvidence`
- `CompileARollEligibility`
- `GenerateARollCandidatePortfolio`
- `ValidateARollCandidatePortfolio`
- `SelectARollCandidate`
- `RejectARollCandidatePortfolio`
- `CompileARollEDL`
- `CommitARollVideoEditProgram`
- `InvalidateARollSelectionCase`
- `CancelARollSelectionCase`
- `SupersedeARollSelectionCase`

Every command contains `command_id`, `idempotency_key`, `actor_ref`, `authority_ref`, `aggregate_id`, `expected_aggregate_version`, exact input refs/hashes, profile refs and canonical payload hash. Operational timestamps may be receipt metadata but do not affect semantic identity.

Events mirror successful transitions and contain event ID, aggregate/version, command ref, before/after semantic hashes and artifact refs. Receipts bind command, input manifest, output manifest, actor/authority decision, profile versions, result, blockers and aggregate version. A denial produces a durable command record and denial receipt without committing success artifacts.

### 6.10 Repository atomicity and idempotency

```text
commit_transition(
  command,
  expected_aggregate_version,
  new_aggregate,
  artifacts,
  receipts,
  events,
  dependency_edges,
  idempotency_record,
  optional_successor_video_edit_program
) -> AtomicCommitReceipt
```

The repository MUST make all items visible together or none. State without receipt/event/dependencies, receipt without state/artifact, or successor program without EDL is corruption. On restart, an identical idempotency key plus identical canonical command hash returns the exact prior result. The same key with different bytes fails `IDEMPOTENCY_KEY_REUSE`. Competing expected versions yield exactly one success and one `OPTIMISTIC_CONCURRENCY_CONFLICT`.

### 6.11 API projection

Application/API adapters expose versioned commands and exact reads only:

- `POST /v2.1/a-roll-selection-cases`
- `POST /v2.1/a-roll-selection-cases/{id}/evidence:freeze`
- `POST /v2.1/a-roll-selection-cases/{id}/eligibility:compile`
- `POST /v2.1/a-roll-selection-cases/{id}/candidates:generate`
- `POST /v2.1/a-roll-selection-cases/{id}/candidates:validate`
- `POST /v2.1/a-roll-selection-cases/{id}/decision:select`
- `POST /v2.1/a-roll-selection-cases/{id}/edl:compile`
- `POST /v2.1/a-roll-selection-cases/{id}/program:commit`
- `GET /v2.1/a-roll-selection-cases/{id}/versions/{version}`
- `GET /v2.1/a-roll-edls/{id}/versions/{version}`
- `GET /v2.1/source-output-maps/{id}/versions/{version}`

Every write requires expected version and idempotency key. No endpoint accepts `latest` as an authority-bearing input. API response timestamps, links and pagination tokens are projections and excluded from semantic hashes.

## 7. Implementation stages and exact target paths

These are future build locations only. Their listing does not authorize creation during this writing factory.

### 7.1 Stage A - closed domain contracts

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/a_roll_selection.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/a_roll_edl.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/a_roll_boundaries.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/source_output_time_map.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/a_roll_events.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/a_roll_failures.py`

Exit evidence: closed-enum/presence/property tests, canonical-serialization fixtures and no import from adapters, services, repositories or frameworks.

### 7.2 Stage B - admitted upstream adapters

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/interview_expression_moment.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/video_edit_program.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/air_semantic_program.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/harness_video_constraints.py`

Exit evidence: exact version/hash reads, no `latest`, ownership-negative tests, and typed denial for missing/ambiguous/stale inputs.

### 7.3 Stage C - eligibility, generation and validation

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_eligibility_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_candidate_generator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/word_audio_boundary_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_context_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/a_roll_selection_evaluator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_decision_service.py`

Exit evidence: bounded portfolio, deterministic ordering, independent decision, exact quote reconstruction, reaction-tail and context denial tests.

### 7.4 Stage D - EDL, mapping and program compilation

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_edl_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/source_output_time_map_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_program_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_selection_command_service.py`

Exit evidence: exact rational duration/map properties, complete `PRIMARY_A_ROLL_SPINE`, predecessor/successor cross-binding and no secondary timeline.

### 7.5 Stage E - persistence, invalidation and replay

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/repositories/a_roll_selection_repository.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_program_commit_service.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_invalidation_projector.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/services/a_roll_replay_service.py`

Exit evidence: crash-point atomicity, optimistic concurrency, idempotency, exact descendant invalidation, historical reconstruction and state/receipt/artifact/event cardinality tests.

### 7.6 Stage F - APIs and projections

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/api/a_roll_selection_commands.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/api/a_roll_selection_queries.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/projections/a_roll_inspection_projection.py`

Exit evidence: strict request schemas, portable responses, command-only correction, no hidden editor state and no authority escalation.

### 7.7 Exact test locations

- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/domain/test_a_roll_selection_contracts.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_a_roll_eligibility_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_word_audio_boundary_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_a_roll_context_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_a_roll_candidate_generator.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_a_roll_edl_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/unit/services/test_source_output_time_map_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_a_roll_atomic_commit.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_a_roll_invalidation_and_replay.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/contract/test_interview_expression_a_roll_adapter.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/contract/test_video_edit_program_a_roll_adapter.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/architecture/test_a_roll_import_boundaries.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/fixtures/a_roll_selection/`

Exact-source architecture tests should assert import direction and ownership boundaries, not duplicate entire source files or formatting-sensitive bodies.

### 7.8 Build sequencing and claim limit

Implementation sequencing is domain -> adapters -> validators/generator/evaluator -> EDL/program compiler -> persistence/replay -> API. No stage begins from this document alone. A separately authorized capsule must state ratification/adoption state, exact accepted spec hash, tests, paths and claim ceiling. Until then all paths remain proposed.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failure taxonomy

| Code | Meaning | Required response |
|---|---|---|
| `SOURCE_REGISTRATION_STALE` | Source registration version/hash differs. | Block; request exact current input. |
| `VIDEO_EDIT_PROGRAM_STALE` | Predecessor program is not exact expected version/hash. | Fail concurrency; never rebase. |
| `EXPRESSION_MOMENT_NOT_APPROVED` | Moment approval absent, rejected, revoked or invalidated. | Block selection. |
| `EXPRESSION_MOMENT_BOUNDARY_INCOMPLETE` | Required core/context/source evidence is missing. | Block; return IE-owned evidence refs. |
| `SOURCE_AUTHORITY_DENIED` | Requested interval/function exceeds approval/source scope. | Deny; do not trim or guess. |
| `INTERVIEW_PROVENANCE_MISSING` | Reaction Receipt or Expression Moment provenance required by interview source is absent. | Reject before eligibility. |
| `UNSUPPORTED_PARAPHRASE_AS_SOURCE` | Proposed spoken text does not reconstruct from exact words. | Reject candidate and record evidence. |
| `GENERATED_A_ROLL_FORBIDDEN` | Candidate uses generated/reconstructed speech as the source spine. | Reject case output. |
| `WORD_BOUNDARY_INVALID` | Cut crosses a protected word or lacks exact word evidence. | Reject candidate segment. |
| `AUDIO_BOUNDARY_INVALID` | Silence/event boundary is unpermitted or ambiguous. | Reject candidate segment. |
| `PADDING_EXCEEDS_AUTHORITY` | Applied padding crosses approved scope/protected evidence. | Reject; do not clamp silently. |
| `REACTION_TAIL_REMOVAL_UNAUTHORIZED` | Semantically relevant tail/reaction removed without evidence. | Reject candidate. |
| `CONTEXT_MEANING_CHANGED` | Candidate omits/reorders evidence so approved reading no longer holds. | Reject candidate; HumanResolution if unresolved. |
| `SOURCE_ORDER_CHANGE_UNDECLARED` | Output order differs without explicit record/authority. | Reject candidate. |
| `TARGET_DURATION_INFEASIBLE` | No valid sequence meets duration without violating hard constraints. | Reject all; preserve truthful source. |
| `SELECTOR_PROFILE_UNSUPPORTED` | Required selector feature/profile is unavailable. | Block; never downgrade requirements. |
| `GENERATOR_EVALUATOR_NOT_INDEPENDENT` | Same invocation controls proposal and decision. | Reject decision. |
| `SOURCE_OUTPUT_MAP_DISCONTINUITY` | Unexplained gap/overlap, rate, rounding or inverse failure. | Reject EDL. |
| `A_ROLL_SPINE_MISSING` | Successor program lacks non-empty primary spine. | Reject commit. |
| `SEMANTIC_AUTHORITY_MUTATION` | Pipeline output changes IE/AIR/Harness-owned meaning. | Reject and raise ownership violation. |
| `IDEMPOTENCY_KEY_REUSE` | Same key, different command bytes. | Return conflict and original record ref. |
| `OPTIMISTIC_CONCURRENCY_CONFLICT` | Expected aggregate/program version differs. | No commit; return exact observed version. |
| `ATOMIC_COMMIT_FAILED` | Any aggregate/artifact/receipt/event/dependency/program write fails. | Roll back all visibility; retain operational diagnostics only. |
| `HISTORICAL_REPLAY_MISMATCH` | Recomputed hash differs from stored historical state. | Quarantine read, raise integrity incident. |

Failures retain exact stage, command, aggregate/version, input refs/hashes, profile, typed reasons and safe retry disposition. User-facing text is a projection; codes and context are canonical.

### 8.2 `NOT_APPLICABLE` law

`NOT_APPLICABLE` is a typed evidence-bearing result, never a blank or shortcut. It requires `field_or_requirement`, `reason_code`, `evidence_refs`, `authority_ref`, `profile_ref` and evaluator identity.

It is forbidden for: interview source kind; Expression Moment/approval; core span; A-roll spine; source media; word/phrase/speaker refs for spoken spans; source/output map; semantic function; command/idempotency; and validation receipts.

It may be valid for: turn/landing span when the approved moment has none; reaction tail when IE evidence proves none exists; an audio event at a word boundary; source reorder when order is preserved; or HumanResolution when no conflict occurred. Optionality does not permit omission of the applicability decision when the profile requires it.

### 8.3 Migration

Migration is a new command producing new immutable artifacts and a `LegacyARollMigrationReceipt`. It records source digest, predecessor contract/service version, field-by-field mapping, time conversion, unresolved fields and output hashes.

- Integer milliseconds convert only through an explicit 1/1000 timebase and exact source registration compatibility.
- Arbitrary source IDs must resolve to exact source-package/media/version/hash; unresolved refs block.
- Existing A-roll layers without word/phrase/speaker/boundary evidence are not inferred; they remain historical-only or blocked for re-approval.
- Open dictionaries must map to governed fields; unknown semantic values are not flattened into notes.
- Random IDs and timestamps are preserved as legacy metadata but excluded from new semantic identity.
- A historical locked timeline is not treated as an approved Expression Moment, selection decision or current `VideoEditProgram`.
- No migration guesses source kind, interview provenance, reaction meaning, approval, cut boundary, semantic function or AIR lineage.

### 8.4 Rollback and recovery

Before an atomic commit becomes visible, any failure leaves the prior aggregate and `VideoEditProgram` current. After commit, rollback is a compensating command that creates a new program version referencing a prior valid EDL; it never deletes the failed or superseded version.

Crash recovery scans durable command/idempotency and commit markers. A prepared-but-uncommitted batch is invisible and safely retried. A committed marker with missing members is corruption, not a partial success. Repository repair requires a separately governed recovery operation and receipt.

Cancelled, invalidated, revoked and superseded artifacts remain retrievable by exact historical identity. They are barred from current consumption but remain reproducible.

### 8.5 Observability without identity leakage

Structured telemetry includes operation/stage, aggregate/version, command ref, profile refs, counts, rational durations, failure code, dependency refs and semantic hashes. It MUST NOT include raw interview text, unrestricted source paths, credentials, access tokens, full media bytes, unapproved personal data or machine-absolute paths.

Metrics may count candidate denials, boundary failures, infeasible duration, concurrency conflict, idempotent replay and invalidation fan-out. Thresholds and alert policy are operational configuration, not invented by this spec. Logs are not canonical receipts.

## 9. Behavior-specific acceptance criteria

Each criterion requires the stated observable evidence. A prose assertion or passing predecessor test is insufficient.

1. **FR-069 exact selection:** Given an approved moment, every selected EDL entry resolves to exact source media, interval, phrase/word/speaker evidence, declared expression/Activative function and exact output interval. Evidence: EDL, map, boundary and semantic-lineage receipts.
2. **FR-069 primary example:** An approved Expression Moment with exact word boundaries compiles to an EDL whose output duration and every output start/end recompute byte-identically. Evidence: golden fixture plus property test.
3. **FR-069 adversarial boundary:** A cut through a protected word is rejected before EDL identity is assigned. Evidence: `WORD_BOUNDARY_INVALID` denial and unchanged repository snapshot.
4. **FR-139 source spine:** Every interview-derived short successor program contains a non-empty `PRIMARY_A_ROLL_SPINE` backed by exact original source. Evidence: program/EDL cross-validation.
5. **FR-139 generated paraphrase denial:** Generated talking-head or paraphrased audio labeled interview-derived cannot satisfy A-roll. Evidence: `GENERATED_A_ROLL_FORBIDDEN` or `UNSUPPORTED_PARAPHRASE_AS_SOURCE` test.
6. **FR-140 bounded portfolio:** The selector emits no more than the frozen profile permits, all candidates use only eligible spans, and canonical ordering is stable under provider return-order permutation. Evidence: portfolio/generator/property tests.
7. **FR-140 context fidelity:** A shorter candidate that changes the approved premise/core/turn reading fails even when it fits duration. Evidence: context validator/evaluator denial.
8. **FR-140 no quote synthesis:** Candidate text reconstructs exactly from referenced words in output order. Evidence: reconstruction hash and mutation test.
9. **FR-140 reaction evidence:** Laughter, hesitation, sigh or reaction tail cannot be removed by a generic cleanup rule. Evidence: preservation test and authorized-removal counterexample.
10. **FR-141 permitted boundaries:** Word, silence and audio-event cut classes enforce their closed presence and evidence rules. Evidence: table-driven positive/negative tests.
11. **FR-141 visible continuity ceiling:** Mechanical word/audio validation records rendered mouth-discontinuity evaluation as pending and cannot claim rendered acceptance. Evidence: state/receipt schema test.
12. **Output-time exactness:** Forward/reverse mapping round-trips exact rational times; no hidden gap, overlap or rounding drift exists. Evidence: property and long-sequence tests.
13. **Source-order truth:** Reorder without explicit moved-span evidence and authority fails; authorized reorder remains inspectable. Evidence: paired tests and EDL source/output ordinals.
14. **IE ownership:** Pipeline cannot change the Expression Moment, boundary, approval, Reaction Receipt, source kind or source authority. Evidence: adapter/command ownership-negative tests.
15. **AIR ownership:** Pipeline cannot create or mutate Primitive/archetype, role/tension, Matrix, Final Script, Activative Call or Activation Transfer meaning. Evidence: closed adapter and semantic-mutation tests.
16. **One temporal truth:** EDL compilation creates a successor TS-VID-001 program and cannot create an independently current timeline. Evidence: repository and architecture tests.
17. **Independent decision:** Generator and evaluator/decision invocation identities must be distinct; candidate scores cannot self-accept. Evidence: independence denial test.
18. **Stale input denial:** A changed source registration, moment approval or program version prevents commit. Evidence: exact stale-version tests.
19. **Idempotency:** Identical command/key returns exact prior output hashes; same key/different payload fails. Evidence: restart-backed idempotency tests.
20. **Optimistic concurrency:** Two commands against one version produce one complete success and one typed conflict. Evidence: interleaving test.
21. **Atomicity:** At every injected persistence failure, aggregate, EDL, map, receipts, events, dependencies and successor program are all visible or all absent. Evidence: crash-point matrix.
22. **Selective invalidation:** Word/moment/approval/semantic changes invalidate exact dependent descendants; unrelated source evidence stays current. Evidence: dependency-graph tests.
23. **Historical reproduction:** A superseded or invalidated version reloads by exact identity and recomputes stored hashes without current aliases. Evidence: cold-start replay test.
24. **Portability:** Canonical output contains no absolute path, hostname, environment expansion, locale-sensitive number or current-time/random identity. Evidence: cross-root/process determinism scan.
25. **`NOT_APPLICABLE`:** Required A-roll/source/word/map/lineage fields reject N/A; valid optional cases require evidence. Evidence: table-driven presence tests.
26. **Migration losslessness:** A complete predecessor fixture migrates with exact mapping; missing source/word/approval evidence blocks instead of being guessed. Evidence: paired migration fixtures.
27. **Status ceiling:** Written and test artifacts retain candidate/non-build state and cannot emit acceptance, capsule, production or certification claims. Evidence: metadata/claim scan.

## 10. Testing and completion evidence

### 10.1 Test strategy

Unit tests cover closed models, presence rules, canonical serialization, eligibility intersections, quote reconstruction, boundary decisions, context, ranking, rational duration and mapping. Property tests generate varied rational timebases, segment counts, source orders and map round trips without using wall-clock or random implicit state.

Contract tests run against exact frozen TS-VID-001 and TS-INT-004 fixtures. They prove exact version/hash binding, ownership denials, upstream invalidation and the `DRAFT_DEPENDENCY_NOT_ACCEPTED` revision-impact path.

Integration tests use a durable repository adapter and fault injection. They test atomic transitions, restart idempotency, optimistic concurrency, descendant invalidation, cancellation/supersession and cold historical replay. Architecture tests assert domain import direction and prevent Pipeline from importing product internals or defining IE/AIR semantic fields locally.

Rendered visual continuity is not fabricated in this scope. A future rendered-evaluation integration must consume this spec's pending evidence and prove mouth/cut continuity before production acceptance.

### 10.2 Mandatory fixture matrix

At minimum:

- approved single-speaker moment with premise, core, landing and reaction tail;
- approved moment with no tail and evidenced `NOT_APPLICABLE`;
- protected-word cut;
- permitted silence boundary;
- ambiguous audio event;
- phrase text altered by one token;
- candidate that fits duration by deleting necessary premise;
- candidate that removes laughter as generic silence;
- explicit authorized reorder and hidden reorder;
- source registration/moment approval/program stale versions;
- generated paraphrase presented as A-roll;
- unsupported selector feature/profile;
- same generator/evaluator identity;
- exact mapping across unlike rational source/output timebases;
- long sequence that exposes rounding accumulation;
- persistence failure at every atomic member;
- idempotent replay after process restart;
- selective invalidation from word, approval and semantic refs;
- lossless predecessor migration and blocked ambiguous migration;
- same canonical inputs under different roots, locales, environments and dictionary construction orders.

### 10.3 Determinism proof

Run the complete canonical fixture corpus in at least two fresh processes and two distinct workspace roots. Freeze all command IDs, evidence times, profiles, selector implementation hashes and explicit seeds. Compare byte-for-byte:

- evidence snapshot;
- eligibility set and denial ledger;
- candidate portfolio and canonical order;
- validation/evaluation receipts;
- selection decision;
- EDL and boundary ledger;
- source/output map;
- successor `VideoEditProgram`;
- event stream, dependency edges and commit receipt.

Search outputs for absolute drive/UNC paths, hostnames, environment values, nondeterministic timestamps and unstable ordering. Any difference is a failure, not an accepted diagnostic variation.

### 10.4 Traceability and negative-authority proof

The completion evidence must map FR-069/139/140/141 and ST-04.02 to tests, symbols, fixtures and exact artifact hashes. It must include negative proofs that:

- the Pipeline did not alter IE source/evidence/approval;
- the Pipeline did not compile AIR meaning;
- the selector did not approve itself;
- the EDL did not become a second temporal truth;
- supporting layers did not replace the A-roll spine;
- mechanical validation did not claim rendered continuity;
- no candidate/build/production/certification state was escalated.

### 10.5 Completion evidence required by a future authorized build

A future build may claim implementation coverage only after providing:

- source and test file manifest with SHA-256;
- canonical model/command/event/receipt schema evidence;
- full unit, property, contract, integration and architecture results;
- atomicity fault-injection matrix;
- two-process/two-root determinism comparison;
- idempotency/concurrency/replay/invalidation reports;
- predecessor migration disposition and fixtures;
- FR/Story/symbol/test traceability;
- independent audit and any revision/re-audit receipts;
- ratification/adoption evidence required for any later build acceptance;
- explicit `production_eligibility: false` and `certification: false` unless separately governed evidence changes those states.

### 10.6 Current writing-factory completion state

This document finishes only as `WRITTEN_PENDING_AUDIT`. Candidate authority is `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; the later pre-ratification ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. The next permitted lifecycle action is independent audit by a different agent under Prompt 04. No writer self-audit, revision, acceptance, implementation, capsule, contract release or product authorization occurred.
