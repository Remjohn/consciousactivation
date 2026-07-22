---
document_type: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-VID-001
title: Existing VideoEditProgram Adoption and Canonical Source Media Intake
product: Atomic Harness Pipeline
version: 2.1.0-candidate
issued_on: '2026-07-22'
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 12
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs: [FR-067, FR-068]
controlling_stories: [ST-04.01]
upstream_draft_dependencies:
  - {edge_id: SDE-046, spec_id: TS-AHP-003, quality_state: WRITTEN_PENDING_AUDIT, sha256: 072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-047, spec_id: TS-INT-002, quality_state: WRITTEN_PENDING_AUDIT, sha256: 1aff9aca4776d0dbb8254882814b6277303258924990a0f75640798768f4123d, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-048, spec_id: TS-INT-003, quality_state: WRITTEN_PENDING_AUDIT, sha256: d6075ebbc317a2e9f363bebfedda78dcf7d8d31dc1377dbc15b212f7800bd1d6, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-049, spec_id: TS-AIR-015, quality_state: WRITTEN_PENDING_AUDIT, sha256: 58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-VID-001 — Existing VideoEditProgram Adoption and Canonical Source Media Intake

This candidate specifies contracts only. It authorizes no code, schema release, Development Capsule, renderer/provider call, production artifact, product adoption, certification, or `ACCEPTED_FOR_BUILD` claim.

## 1. Files and authorities read

### 1.1 Frozen Wave 12 inputs

| Upstream draft | State and SHA-256 | Interface admitted for writing | Revision impact if audit changes the hash |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-003.md` | `WRITTEN_PENDING_AUDIT`; `072041914b836be5a45e80ee87102cc490f0927a946633e78806bee63e3578ed` | Immutable derivative job, source-use grant, exact source/semantic/Harness binding, category/profile, evaluation and wrong-reading constraints. | Reopen sections 3, 5, 6, 8, 9 and 10. |
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-002.md` | `WRITTEN_PENDING_AUDIT`; `1aff9aca4776d0dbb8254882814b6277303258924990a0f75640798768f4123d` | Exact rational source time, aligned words/speakers/events, packed phrases, limitations, immutable correction and selective invalidation. | Reopen sections 3, 5, 6, 8, 9 and 10. |
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-003.md` | `WRITTEN_PENDING_AUDIT`; `d6075ebbc317a2e9f363bebfedda78dcf7d8d31dc1377dbc15b212f7800bd1d6` | Exact stream/frame addressing, shot/transition map, keyframes, visual references, source authority and variable-frame-rate handling. | Reopen sections 3, 5, 6, 8, 9 and 10. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-015.md` | `WRITTEN_PENDING_AUDIT`; `58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8` | AIR-owned approved Final Script, semantic production package, Activation Transfer Contract, role/tension, Primitive/archetype, Brand/Voice/Visual DNA and lock lineage. | Reopen sections 3, 5, 6, 8, 9 and 10. |

Every row is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. None is ratified authority. Current Constitution V1.1 and current product authorities prevail; Prompt 02C permits candidate-specification work only.

### 1.2 Current authority, requirements and writing controls

| Source | State / SHA-256 | Class | Specific fact used |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest current authority | Pipeline executes a Harness and preserves Activative/source authority; an editor or renderer cannot become meaning authority. |
| AHP `prd/PRD_COMBINED.md` | `1.2.0-draft`; `387568731acfe57f022a2fadcd2acfc73baf1287b8a5a1e1d3ed78675ccb067d` | candidate product PRD | Original interview footage is the A-roll spine; composition and approved meaning precede editing; the PRD grants no implementation/production authority. |
| F12 `Source-First Short-Form Video Editing and Adopted Timeline Runtime` | candidate; `ae65689ae06ccf8b01dbba407ab093fd77cf01a74637f0ba0f7c16c053ae1a01` | controlling feature | FR-067 adopts one canonical temporal program; FR-068 registers exact interview media without mutating originals. |
| AHP `EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | controlling Story | ST-04.01 requires reconstructable timeline/source intake and rejects irreconcilable transcript/source identity. |
| `planning/spec_assignments/TS-VID-001.md` | assignment only; `ec216646fb5f382134c96605820d2f0a7ef580088144131c8887efb3eccede40` | scope evidence | Names predecessor files; its old `04_ATOMIC_HARNESS_PIPELINE` target is superseded by the frozen Program Control path. |
| Program Control cross-product and semantic ownership matrices | candidate; `cd92d291...` / `232a9153...` | ownership | Interview Expression owns live source evidence; AIR owns semantic program meaning; Pipeline owns temporal execution state/program; Studio is projection; renderers are embodiments. |
| `SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | write gate | Writing is allowed; build, production and certification remain false. |

### 1.3 Required current and predecessor evidence

| Source ID / path | SHA-256 | Current disposition | Actual evidence used |
|---|---|---|---|
| `SRC-CUR-007` — `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py` | `cef3bf6673bde2ec501c01099f0efee12b7ad47cb8379c68a58b074a13c35512` | required current implementation | Short-form edited video requires ordered time state, edited transitions, reading order and Activative sequence; category identity, rich lineage and repair units remain explicit. |
| `SRC-LEG-006` — `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/video_editing_engine.py` | `38edbceab7152ae1d09d131936bc1625ced13d384932f333acca4425954d4bd7` | required unique predecessor | Useful track/layer/scene/caption/audio/timeline vocabulary, but random IDs, clock defaults, open maps/`Any`, free string refs, mutable models, fake receipt flags and historical formats are not canonical. |
| `SRC-LEG-007` — `.../services/video_editing_engine_service.py` | `3d13c36601d1719b5b6c826ae43e9e24a71a77e61f92137396cad60649472e05` | required unique predecessor | Thin orchestration mutates timeline objects and upserts current state without command/receipt/version/atomicity guarantees. |
| `SRC-LEG-008` — `.../services/video_timeline_service.py` | `ad3350e56122474d063f6e5bbebee44a57d298ca14f615ba7b9c3d031637a012` | required unique predecessor | Constructs layers/tracks/scene timing/timeline but lacks exact source, semantic, Harness and replay lineage. |
| `SRC-LEG-009` — `.../services/video_audio_service.py` | `27b20631cfdc261dd99d748a172ddf44ce638fa30af816d12ed123b09602faa6` | required unique predecessor | Provides audio-plan vocabulary with embedded ungovened defaults; later audio specs must own actual policy. |
| `SRC-LEG-010` — `.../services/video_caption_service.py` | `894a20db54aedc80a5cf691f4edff6560a2148a0206095c37364e04a4801094a` | required unique predecessor | Provides caption-track construction and collision flags but no word/source lineage or immutable receipt. |
| `SRC-LEG-011` — `.../services/video_media_probe_service.py` | `10ef27499d7bc52995de2670d7c63e8d563efe37bf402d8b29a1f4b89357c1cc` | required unique predecessor | The “probe” echoes caller metadata; it does not execute or verify ffprobe, bytes, streams or identity. |
| `SRC-LEG-012` — `.../services/video_source_asset_service.py` | `40ef7cdde27586686901c08e2e917c7284d211b936959c73c57125e08455857c` | required unique predecessor | `asset_hashes` incorrectly copies `source_ref`; source bytes are not actually hashed or reconciled. |
| `test_video_editing_engine_v1.py` | `ad33f9106a1da01c404b5e7dc617a0b14cd5d53e96ec18fe805a46dadf3933b4` | predecessor test evidence | Tests useful local constraints but use `file://`, arbitrary refs/hashes, fake renders and active historical Format 02, so they are migration fixtures, not current acceptance evidence. |
| `SRC-AM-001` Studio Architecture Amendment V2.1 archive | `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | required authority input | Format 02 is deferred; Studio supervises via typed commands and cannot hold hidden canonical timeline state. |
| `SRC-INT-001` Interview-first doctrine | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | required unique evidence | Human expression and original media remain the source; downstream systems multiply rather than replace them. |
| `SRC-INT-002` and `SRC-INT-003` current-ledger doctrine evidence | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | required unique evidence | Exact Expression Moment/capture and frame/route lineage remain source-grounded; the current ledger explicitly resolves both source records to these verified bytes. |

`SRC-AM-002` and external references `SRC-EXT-017`, `018`, `019`, `020`, and `023` are `DEFERRED_REFERENCE`. No algorithm, threshold, provider capability, license conclusion, performance claim or factual statement in this spec is attributed to them. Their absence is nonblocking under the current Source Disposition Ledger and gap registry.

The output is a `DIRECT_PRODUCT_SPEC_PATH`. No applicable `AGENTS.md` exists in the target or its ancestors.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure without this specification

The predecessor can assemble a plausible timeline, but it cannot prove what bytes were edited, whether caller-supplied probe values are true, whether transcript and source duration/timebase agree, whether a layer came from approved source or generated evidence, or whether reload reconstructs the same program. Random IDs, current-time defaults, mutable in-memory upserts, arbitrary `file://` URIs, open dictionaries and hidden browser state can yield a polished edit whose source, semantic function and receipt cannot be reproduced.

A greenfield replacement would create a second timeline truth and lose proven predecessor vocabulary. A direct fork would preserve unsafe identity, weak source registration, active historical Format 02 assumptions and ownership confusion. A governed adoption is required.

### 2.2 User and system outcome

A video operator opens one exact source-backed derivative job and obtains:

1. an immutable `SourceMediaTechnicalRegistration` proving each admitted original artifact, stream, rational timebase, duration, alignment, shot map and keyframe binding without changing the original bytes; and
2. one canonical `VideoEditProgram` whose every timeline element resolves to an exact source interval, approved derivative, or typed unmaterialized generated slot and whose byte-identical state can be reconstructed after reload.

The UI, OTIO view, renderer props, worker workspace and cached proxy are projections of the program, never independent timeline authorities.

### 2.3 Bounded solution

This specification:

- adopts the predecessor timeline vocabulary into one strict immutable `VideoEditProgram`;
- validates exact source-package and derivative-job identity before media access;
- streams and hashes source bytes, records portable locators, and probes technical media through a pinned deterministic binding;
- reconciles streams with TS-INT-002 word/phrase timing and TS-INT-003 frame/shot/keyframe indexes using exact rational time;
- compiles complete source-to-output mappings, tracks, elements, constraints, runtime/evaluation refs and lineage;
- persists program, registration, receipts, events, dependencies and idempotency atomically;
- supports correction, supersession, selective invalidation and historical replay without mutating predecessors.

### 2.4 In scope

- FR-067, FR-068 and ST-04.01 only.
- Canonical source technical registration and validation, not source capture/approval.
- Canonical temporal program identity, source/output time mapping, track/element skeleton and lineage.
- Migration from exact predecessor contracts as lossless-or-blocked evidence.
- Source alignment/visual-index reconciliation and typed blockers.
- Projection boundaries for Studio/UI, OTIO and future render adapters.
- Exact proposed implementation/test paths and completion evidence.

### 2.5 Out of scope and non-goals

- Selecting source spans or compiling word-safe A-roll edits (TS-VID-002 scope).
- Captions/audio/support layers, runtime embodiment selection, FFmpeg execution/export or final evaluation (later video specs).
- Creating or correcting transcripts, words, speakers, shots, keyframes, Reaction Receipts or Expression Moments.
- Compiling AIR meaning, Final Script, Primitive/archetype, Composition Intent or Activation Transfer semantics.
- Changing a Builder Harness, derivative-job source grant, VAE demand or source authorization.
- Activating historical Format 02, selecting Remotion/HyperFrames/FFmpeg, making license claims, calling providers or rendering media.
- Treating a local test, dry run, probe command, synthetic URI or UI reload as production evidence.

## 3. Governing decisions and constraints

### 3.1 Authority stage and product sovereignty

Constitution V1.1 is current. V2.1 ownership, the AHP V1.2 PRD, F12, Stories and upstream specs remain `CANDIDATE_NOT_CURRENT`. Specification work is authorized; build is false; the maximum later pre-ratification state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

Interview Expression owns original source truth, authorization, source package, transcript alignment, shot/transition decisions, keyframes and visual references. AIR owns semantic production meaning, Final Script, role/tension, Matrix/Edge, Primitive/archetype coalition, Brand/Voice/Visual DNA and transfer law. Builder owns Harness/category requirements. Pipeline owns the read-only technical-registration decision and canonical temporal execution program. Studio projects it; renderers embody it. `Activative Contract Compiler != Activative Intelligence Runtime`, and neither is this runtime.

### 3.2 One timeline truth

`VideoEditProgram` is the sole canonical temporal editing state. The following are noncanonical projections:

- browser/editor component state;
- OTIO interchange/audit timelines;
- Remotion/renderer input props;
- FFmpeg command graphs;
- worker workspaces, proxies and cache manifests;
- Studio view models and drag/drop state.

A projection carries exact program version/hash and transformation profile. Any edit returns a typed command that creates a new program version. It never writes a hidden “current” timeline or becomes authoritative when the program is unavailable.

### 3.3 Original media and A-roll spine

Original talking-head media remains immutable and is the primary A-roll source for source-led short video. Registration never transcodes, normalizes, strips metadata, rewrites a container, modifies timestamps or substitutes a visually equivalent file. Derived/proxy media receives a separate artifact identity and parent lineage. The initial program must contain a `PRIMARY_A_ROLL_SPINE` track requirement; this spec does not choose its clips.

### 3.4 Composition and meaning precede editing

A program is compilable only from an admitted TS-AHP-003 job and exact AIR semantic package/approved Final Script/Activation Transfer Contract. Timeline elements reference the already-approved function and transformation rule. Pipeline cannot decide a new source meaning, rewrite a quote, choose a new archetype/Primitive, flatten a psychological role/tension, or replace Composition Intent with editor convenience.

### 3.5 Source fidelity and lineage

Every source-bearing element has:

- exact source package/media/version/hash;
- exact rational source interval and timebase;
- applicable word/phrase, speaker, audio-event, shot/frame/keyframe and visual-reference refs;
- source-use grant and restrictions;
- semantic/sequence function and transfer-rule refs;
- transformation class and evidence;
- exact output interval and mapping.

Generic notes, filenames, UI clip IDs, generated summaries or “latest” queries cannot substitute. Unknown/missing/mismatched refs block before program identity is assigned.

### 3.6 Rational time and variable-frame-rate law

Canonical time is integer ticks plus positive rational timebase. Float seconds and nominal FPS are display/diagnostic only. Source video frames use TS-INT-003 presentation ordinal, timestamp, duration and decoded-pixel digest; source words use TS-INT-002 exact intervals. Conversions record integer numerator/denominator and profile-owned rounding. A mapping may not shrink evidence through rounding.

### 3.7 Technical registration is not source ownership

`SourceMediaTechnicalRegistration` is a Pipeline-owned validation projection. It proves the exact bytes/stream metadata consumed by a job and binds them to IE-owned records. It is not a second Canonical Interview Source Package, transcript, shot map or approval. Registration acceptance does not authorize editing, rendering, publication or production.

### 3.8 Determinism, portability and no guessed values

Canonical identity excludes current time, random state, environment, machine path, hostname, locale, timezone, map insertion order, filesystem traversal, worker scheduling and tool output order. Commands provide IDs and evidence timestamps; timestamps are excluded from semantic hashes. Portable refs are repository-relative logical or content-addressed URIs. Drive paths, UNC, traversal, symlinks, environment expansion and mutable `file://` paths fail.

Probe/alignment tolerances, accepted codecs, stream-count rules and conversion rounding are owned by immutable profiles. This spec invents no threshold. Unknown codecs/profiles/enum values fail or produce typed unsupported status; they are never coerced.

### 3.9 `NOT_APPLICABLE`, category/profile and Format 02

Conditional fields use `ApplicabilityDecision` with rule/evidence/owner/reason. Null, omission or a bare `NOT_APPLICABLE` string cannot hide required source, A-roll, alignment, visual-index, evaluation or lineage evidence. Category/profile identity is exact and does not inherit certification. Format 02 remains deferred and cannot enter an eligible program merely because the predecessor enum contains it.

### 3.10 Immutability, atomicity and segregation

Source bytes and accepted program versions never mutate. Each command atomically commits artifacts, receipt, event, dependency edges, idempotency result, command record and outbox intent. A source or program artifact without its receipt, or a success receipt without its artifact, is corruption. Producing technical metadata does not self-approve unresolved alignment/quality judgment.

## 4. Current brownfield architecture

The target Pipeline repository has no implementation, tests or released schemas. Its only current artifacts are candidate Tech Specs. Therefore all code paths below are future proposals.

| Brownfield component | Actual behavior | Disposition | Migration constraint |
|---|---|---|---|
| `VideoTimelineProgram` and track/layer types in `video_editing_engine.py` | Models project/variant/frame profile, tracks, layers, scenes, caption/audio refs and render projections. Uses mutable Pydantic models, default random IDs/times, strings/open dictionaries and no canonical hash. | `ADAPT` | Preserve useful vocabulary only. Replace identity, refs, time, ownership, lifecycle, serialization and lineage. Do not copy historical format authority. |
| `VideoSourceMedia` / `VideoSourceAssetSet` | Caller supplies URI, duration, dimensions/FPS; “asset_hashes” can be arbitrary. | `REPLACE` | Source package and streamed-byte digest are mandatory; portable refs only; exact streams/timebases replace integer FPS as truth. |
| `VideoMediaProbeService.probe` | Echoes fields from the caller object and returns PASS. | `REPLACE` | Future adapter must execute a pinned probe binding, validate result against exact bytes and independently derive the receipt. |
| `VideoSourceAssetService.compile_source_asset_set` | Copies `source_ref` into an `asset_hashes` map. | `REPLACE` | Cryptographic hashes must be calculated from bytes or verified content-addressed storage; a ref is never a digest. |
| `VideoTimelineService` | Thin constructors; verifies positive duration/sorted nonoverlapping scenes indirectly via models. | `ADAPT` | Rebuild around strict immutable program, exact source/output mapping, dependency closure and atomic receipt. |
| `VideoEditingEngineService` / in-memory repository | Creates random projects/variants, mutates and upserts timeline state, locks by field assignment. | `REPLACE` | Use commands, compare-and-swap versions and append-only commit; lock is a successor decision, not mutation. |
| `VideoAudioService` / `VideoCaptionService` | Produces typed local plans with embedded defaults and shallow collision checks. | `ADAPT_LATER` | Preserve as migration vocabulary for later specs; do not let defaults define current policy or source words. |
| `test_video_editing_engine_v1.py` | Proves some local validation and a fake full path; treats Format 02 as active and accepts arbitrary refs/file URI/fake hashes. | `ARCHIVE_AS_MIGRATION_FIXTURE` | Re-express useful negative cases; no current production/readiness claim. |
| TS-INT-002/003 and TS-AHP-003/AIR-015 drafts | Provide current candidate typed interfaces absent from the predecessor. | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Pin exact hashes; change during audit reopens six dependency-sensitive sections. |

No predecessor object is accepted as current authority merely because tests pass.

## 5. Proposed architecture and workflows

### 5.1 Components and responsibility boundaries

| Component | Owns | Must not own |
|---|---|---|
| `SourceMediaIntakeService` | Orchestration of exact source technical registration. | Source approval, capture or semantic interpretation. |
| `PortableSourceArtifactReader` | Bounded streaming access to exact artifact bytes by authorized portable ref. | Arbitrary local-path access or content mutation. |
| `SourceHashVerifier` | Byte count/SHA-256 and manifest equality. | Trusting a filename/ref as a digest. |
| `MediaProbePort` | Exact pinned technical probe execution and raw result artifact. | Automatic PASS or semantic/media-quality approval. |
| `MediaProbeNormalizer` | Closed canonical stream/container projection under a profile. | Guessing unknown codec/timebase/rotation values. |
| `TranscriptMediaReconciler` | TS-INT-002 word/phrase/speaker/event bounds and source identity reconciliation. | Correcting or inventing words/speakers. |
| `VisualStructureReconciler` | TS-INT-003 stream/frame/shot/keyframe/source digest reconciliation. | Assigning semantic importance or editing shot decisions. |
| `SourceMediaRegistrationRepository` | Atomic immutable registration/receipt/dependency storage. | Storing original media as a competing source root. |
| `VideoEditProgramCompiler` | One canonical temporal program from admitted job/Harness/AIR/source registration. | Selecting meaning/source spans or executing renderers. |
| `TimelineProjectionService` | Exact read projections and projection-diff validation. | Hidden canonical UI/OTIO/renderer state. |
| `VideoProgramRepository` | Exact-version append, CAS, idempotency, replay and dependency traversal. | In-place update or “latest” substitution. |

### 5.2 Workflow A — admit the source package and job

1. `RegisterSourceMediaCommand` supplies exact derivative-job, source package/version/hash, source-use grant, media-entry refs, package approval/hand-off refs, TS-INT-002 alignment/phrase refs, TS-INT-003 visual-index refs, authority/profile snapshots, actor/delegation, idempotency key and expected registration head.
2. Verify the TS-AHP-003 job is current, category/profile compatible, `ADMITTED_NOT_EXECUTION_AUTHORIZED`, and permits technical source intake. Job admission does not authorize external editing/rendering.
3. Verify IE package/component ownership, approval/current lifecycle, media manifest, use restrictions and exact dependency closure. No “latest package” resolution occurs.
4. Freeze an immutable `SourceMediaIntakeManifest` before reading bytes. A shared identity or authority failure blocks the registration; individual optional streams may be evidence-bearing N/A only when the profile allows it.

### 5.3 Workflow B — hash and probe immutable media

1. Reader resolves each portable/content-addressed artifact under source-grant scope. It rejects absolute/traversal/symlink/device/environment paths and enforces bounded bytes.
2. Hash bytes during one read; compare byte length/media type/SHA-256 to the package manifest. The original stream is read-only. Any mismatch quarantines operational bytes and emits no successful registration.
3. Invoke a pinned `MediaProbeBinding` with exact executable/container identity, version/hash, argument profile and sandbox. A command string or exit code alone is not proof.
4. Persist the raw probe result as evidence, then parse it with a closed `MediaProbeNormalizationProfile`. Unknown fields may remain in raw evidence but cannot silently enter canonical state.
5. Validate container/stream IDs, codecs, disposition, start/duration ticks, rational timebases, presentation order metadata, video dimensions/sample-aspect/rotation, audio channels/sample rate and source duration according to the profile. No bare float seconds enter canonical models.
6. Emit `SourceHashLedger`, `MediaProbeReceipt` and candidate `SourceMediaTechnicalRegistration`.

### 5.4 Workflow C — reconcile transcript and visual structure

1. For TS-INT-002, prove alignment source root/media/transcript refs match the registered package/artifact; every eligible word/phrase/audio event interval is within the declared stream bounds under exact rational conversion. Preserve unknown/overlap speaker and limitations.
2. Duration/alignment tolerances are profile-owned. Identity/timebase/bounds contradictions are hard failures. Quality uncertainty remains typed and cannot be averaged into PASS.
3. For TS-INT-003, prove frame-address index, stream index, presentation ordinals/timestamps, decoded-pixel/source digest, shot map, keyframe set and visual references bind the same exact registered stream.
4. Variable-frame-rate media is reconciled by presentation coordinates, not nominal FPS. Missing exact frame identity or visually similar re-encode fails.
5. Emit `TranscriptMediaReconciliationReceipt`, `VisualStructureReconciliationReceipt` and a complete registration. Commit registration and all receipts/edges/events atomically.

### 5.5 Workflow D — compile the canonical `VideoEditProgram`

1. `CompileVideoEditProgramCommand` references one exact admitted derivative job, Harness/binding, source registration, AIR Semantic Production Package, approved Final Script, Activation Transfer Contract, category/profile, composition program and program policy.
2. Verify all refs, owners, hashes, lifecycle states and claim ceilings. Composition and semantic state are inputs, not editable timeline fields.
3. Create required track declarations, including `PRIMARY_A_ROLL_SPINE`, and typed timeline elements. At this stage elements may reference an exact source clip, an approved derivative, or a typed generated slot requirement.
4. Validate each element against source-use grant, source registration, AIR function/transfer rules, Harness/category profile and wrong-reading restrictions.
5. Compile a complete `SourceToOutputTimeMap`; track-local output overlaps/gaps, global duration, ordering and transformation legality are profile-governed and explicitly receipted.
6. Generated slots remain `UNMATERIALIZED` and make execution eligibility false until a later authorized spec binds an exact approved artifact. A placeholder URI cannot satisfy a slot.
7. Canonically serialize, hash and atomically persist program, compilation receipt, command, event, edges, idempotency and outbox. No renderer side effect occurs.

### 5.6 Workflow E — project, command, reload and prove reconstruction

1. Query exact program version/hash and derive Studio, OTIO or renderer-neutral views through a version/hash-pinned projection profile.
2. Every projection includes `source_program_ref` and `projection_hash`; it cannot be persisted as a second current program.
3. A UI edit emits a typed command naming target element/ref, requested change, expected program version/hash, operator authority and reason. It does not patch program bytes.
4. The compiler creates a successor program or typed denial and records the affected dependency set. Human resolutions are separately governed; this spec does not create a `HumanResolutionEpisode` schema.
5. Reload begins from exact canonical bytes and rebuilds projections. Byte/hash or semantic divergence is a blocking failure, not a cosmetic warning.

### 5.7 Idempotency, concurrency, cancellation, late results and replay

- Command identity covers type, canonical payload, actor/delegation scope, exact aggregate/version, authority/profile snapshots and dependency hashes.
- Same key/same request returns the original receipt. Same key/different bytes fails. Compare-and-swap permits one current successor per expected head.
- Cancellation before commit produces a cancellation receipt and no current registration/program. If commit wins, cancellation is a successor command and cannot erase success.
- Late probe/worker results after cancellation/supersession are quarantined evidence and cannot bind automatically.
- Replay uses exact historical source bytes, package/components, bindings, profiles, commands and decisions. Missing bytes fail explicitly; latest/current substitution is forbidden.

### 5.8 States and events

```text
Source registration:
REQUESTED -> INPUTS_VERIFIED -> BYTES_VERIFIED -> PROBED -> ALIGNMENT_RECONCILED
          -> VISUAL_STRUCTURE_RECONCILED -> REGISTERED
          -> BLOCKED | CANCELLED | SUPERSEDED | INVALIDATED | REVOKED

VideoEditProgram:
REQUESTED -> DEPENDENCIES_VERIFIED -> COMPILED -> VALIDATED -> PROJECTABLE
          -> UNMATERIALIZED_SLOTS_PENDING | READY_FOR_LATER_EXECUTION_ADMISSION
          -> BLOCKED | CANCELLED | SUPERSEDED | INVALIDATED | REVOKED
```

Events: `SourceMediaRegistrationRequested`, `SourceMediaBytesVerified`, `MediaProbeCompleted`, `TranscriptMediaReconciled`, `VisualStructureReconciled`, `SourceMediaRegistered`, `SourceMediaRegistrationBlocked`, `VideoEditProgramCompilationRequested`, `VideoEditProgramCompiled`, `VideoEditProgramBlocked`, `TimelineProjectionCreated`, `VideoEditProgramSuperseded`, `VideoEditProgramInvalidated`, `VideoEditProgramRevoked`, `VideoEditCommandCancelled`, and `VideoEditHistoricalReplayVerified`.

## 6. Data models, contracts, schemas, and APIs

All models are immutable, strict and closed (`additionalProperties: false`). No `Any`, untyped maps, placeholder fields, implicit defaults, mutable lists/dicts, random IDs or current-time factories are allowed.

### 6.1 Common types, time and serialization

`ImmutableRef` requires object/schema/version/hash/owner/lifecycle/authority. `PortableArtifactRef` requires logical/content-addressed URI, bytes, SHA-256, media type and authority/restriction refs.

```text
RationalTimebase { numerator: PositiveInt, denominator: PositiveInt }
MediaTime { media_ref: ImmutableRef, stream_id: NonEmptyText, ticks: Integer, timebase: RationalTimebase }
MediaInterval { start: MediaTime, end_exclusive: MediaTime }
OutputTime { ticks: NonNegativeInt, timebase: RationalTimebase }
OutputInterval { start: OutputTime, end_exclusive: OutputTime }
```

Interval ends exceed starts; source interval endpoints share exact media/stream/timebase; output endpoints share program timebase. Conversion uses overflow-checked integer arithmetic and a pinned rounding rule.

Canonical JSON is UTF-8 with NFC strings, lexicographic keys, exact integers, no NaN/Infinity and one terminal newline. Set-semantic arrays sort by canonical ID; track, element, mapping and lineage order are explicit. `content_sha256` excludes itself, evidence timestamps and operational staging data.

### 6.2 `SourceMediaIntakeManifest`

Schema `ca.pipeline.source-media-intake-manifest/2.1.0-candidate`:

```text
manifest_id, version
derivative_job_ref, source_use_grant_ref
source_package_ref, package_approval_receipt_ref
source_media_entry_refs: nonempty ordered ImmutableRef[]
transcript_alignment_ref, packed_phrase_transcript_ref
source_visual_structure_index_ref
source_authority_declaration_ref, effective_restriction_refs
media_probe_binding_ref, normalization_profile_ref
transcript_reconciliation_profile_ref, visual_reconciliation_profile_ref
authority_snapshot_ref, command_ref
canonical_hash
```

The exact refs must form one source root and organization/brand scope. A package handoff/acknowledgement does not substitute for approval/current eligibility.

### 6.3 Hash ledger and technical media models

`SourceHashLedgerEntry` includes source media ref, portable artifact ref, expected/observed bytes and SHA-256, read profile, verification result, mismatch reason and receipt ref. It never stores a local staging path.

`MediaContainerTechnicalRecord` contains container format/profile, byte size, duration/start in governed rational clock, raw probe evidence ref and ordered stream refs. `MediaStreamTechnicalRecord` contains stream ID/index/type, codec/profile/pixel/sample format, rational timebase, start/duration ticks, disposition, video dimensions/sample aspect/rotation or audio sample rate/channel layout, nominal-rate observation and limitations. Fields not applicable use evidence-bearing decisions.

`MediaProbeReceipt` requires input artifact/hash, exact probe executable/binding/profile, command manifest hash, exit/process evidence, raw result artifact/hash, normalization/validation results, expected-versus-observed facts, result `PASS | BLOCKED | UNSUPPORTED | FAILED`, limitations and canonical hash. `PASS` requires actual verified output, not a command string or return code.

### 6.4 `SourceMediaTechnicalRegistration`

Schema `ca.pipeline.source-media-technical-registration/2.1.0-candidate`:

```text
registration_id, version, lifecycle_state
intake_manifest_ref
source_package_ref, source_media_entry_refs
source_hash_ledger_ref
container_record_refs, stream_record_refs
primary_video_stream_ref, primary_audio_stream_ref_or_not_applicable
transcript_alignment_ref, packed_phrase_transcript_ref
transcript_media_reconciliation_receipt_ref
frame_address_index_ref, shot_map_ref, keyframe_set_ref, visual_reference_index_ref
visual_structure_reconciliation_receipt_ref
source_use_grant_ref, effective_restriction_refs
original_bytes_immutable: true
limitations, maximum_claim
production_eligible: false, certified: false
supersedes_ref, dependency_refs, canonical_hash
```

The object owner is Pipeline for the registration decision; every referenced source value remains IE-owned. It cannot contain corrected transcript/shot/keyframe data or a replacement source artifact.

### 6.5 Reconciliation receipts

`TranscriptMediaReconciliationReceipt` records exact registration/media/alignment/phrase refs; source-root equality; rational timebase conversion profile; word/phrase/audio-event bounds; speaker/limitation preservation; duration/profile results; blocked ranges; result; owner; evidence; and hash.

`VisualStructureReconciliationReceipt` records registration/media/stream/frame-index/shot/keyframe/visual-ref refs; source/stream/digest equality; presentation-frame coverage; variable-frame-rate handling; keyframe source equality; uncertainty/limitations; result; evidence; and hash.

Neither receipt creates Interview Expression evidence. A profile-governed quality limitation can be carried forward; source identity/timebase/bounds contradiction blocks.

### 6.6 `VideoEditProgram`

Schema `ca.pipeline.video-edit-program/2.1.0-candidate`:

```text
program_id, version, lifecycle_state
derivative_job_ref, batch_program_ref
harness_definition_ref, harness_execution_binding_ref
source_media_registration_refs: nonempty ordered ImmutableRef[]
semantic_production_package_ref, approved_final_script_ref
activation_transfer_contract_ref, composition_program_ref
category_profile_ref, platform_profile_ref
program_timebase: RationalTimebase, duration_ticks: PositiveInt
tracks: nonempty ordered VideoTrack[]
source_to_output_map: ordered TimeMappingEntry[]
runtime_requirement_refs, evaluation_requirement_refs
review_policy_ref, wrong_reading_lock_refs, source_restriction_refs
projection_profile_refs, dependency_refs
limitations, maximum_claim
execution_eligible: false
production_eligible: false, certified: false
supersedes_ref, canonical_hash
```

At least one track has role `PRIMARY_A_ROLL_SPINE`. `duration_ticks` equals the governed program end. Every element is included in dependency closure and time mapping where applicable. A program with unmaterialized generated slots remains valid as a planning artifact but is not execution eligible.

### 6.7 Tracks, elements and source-to-output mapping

`VideoTrack`:

```text
track_id
role: PRIMARY_A_ROLL_SPINE | SOURCE_AUDIO | SUPPORTING_VISUAL | CAPTION |
      EDITORIAL_TEXT | PROOF | ANIMATION_SLOT | AUDIO_SUPPORT | OTHER_PROFILED
z_order: integer
mix_or_composition_policy_ref
elements: ordered TimelineElement[]
```

`TimelineElement` is a closed tagged union:

- `SourceClipElement`: exact source registration/media/interval, TS-INT-002 word/phrase/speaker/event refs, TS-INT-003 shot/frame/keyframe/visual refs, source-use grant, AIR function/transfer rule, output interval, transformation class and restrictions;
- `ApprovedDerivativeElement`: exact immutable artifact/result/acceptance/lineage refs, parent source/semantic refs, output interval and declared function;
- `GeneratedSlotElement`: slot requirement ID, owner product, required input/output contract, capability/implementation eligibility refs, expected function, constraints and state `UNMATERIALIZED | MATERIALIZED_PENDING_VALIDATION | BOUND_APPROVED_ARTIFACT`;
- `EvidenceBearingGapElement`: exact output interval, governed reason/rule/evidence and blocking state where a deliberate pause/negative-space interval is authorized.

`TimeMappingEntry` contains element ref, source intervals (empty only for approved non-source element or governed gap), output interval, mapping kind `IDENTITY | CUT | REORDER | HOLD | RATE_TRANSFORM | APPROVED_DERIVATIVE | GENERATED_SLOT | GAP`, transformation-rule ref, exact rate ratio when applicable, continuity refs and evidence. No element can masquerade as source speech without exact source spans.

### 6.8 Commands, receipts, events, repository and APIs

Commands:

```text
RegisterSourceMedia
VerifySourceMediaBytes
RecordMediaProbeEvidence
ReconcileTranscriptMedia
ReconcileVisualStructure
CompleteSourceMediaRegistration
CompileVideoEditProgram
ValidateVideoEditProgram
ProjectVideoEditProgram
RequestVideoEditProgramCorrection
SupersedeVideoEditProgram
RevokeSourceMediaRegistration
InvalidateVideoProgramDescendants
CancelVideoProgramCommand
ReplayVideoProgramDecision
```

Each command uses ID/idempotency key, canonical request hash, actor/delegation, organization/brand, exact aggregate/version, causation/correlation, authority/profile snapshots and cancellation ref. Callers cannot set acceptance, lifecycle, eligibility or certification.

Repositories expose exact-version `get`, compare-and-swap append, atomic commit bundle, command/receipt/event/idempotency lookup, dependency traversal and historical replay. Mutable upsert/overwrite is prohibited.

Future APIs:

```text
POST /v2/pipeline/video/source-media:register
POST /v2/pipeline/video/source-media/{id}/versions/{version}:reconcile
POST /v2/pipeline/video/edit-programs:compile
POST /v2/pipeline/video/edit-programs/{id}/versions/{version}:project
POST /v2/pipeline/video/edit-programs/{id}/versions/{version}:supersede
GET  /v2/pipeline/video/source-media/{id}/versions/{version}
GET  /v2/pipeline/video/edit-programs/{id}/versions/{version}
GET  /v2/pipeline/video/edit-programs/{id}/versions/{version}/lineage
```

HTTP success is not approval. Responses return exact artifact/receipt/hash/state and claim ceiling.

### 6.9 Compatibility, migration and negative examples

Compatibility is semantic. Adapters preserve all source, timebase, stream, alignment, shot/keyframe, semantic, Harness, category/profile, restriction, lock, evaluation and lifecycle fields. Parse-only acceptance is failure.

Migration from predecessor records creates new immutable objects plus field-by-field receipt. It blocks when original bytes/hash, source package, exact stream/timebase, span lineage, artifact ownership, track role, element function, restrictions or lifecycle cannot be recovered. Random IDs are retained only as historical aliases; new IDs derive from governed input. Float milliseconds/nominal FPS are evidence, never enough when exact source coordinates are ambiguous. Format 02 records are historical/deferred and do not become active programs.

Invalid examples:

```yaml
# Invalid: source ref is falsely treated as a digest.
asset_hashes: {source_1: source-video-1}
```

```yaml
# Invalid: machine-local mutable locator.
uri: file:///D:/captures/interview.mp4
```

```yaml
# Invalid: hidden UI state is the timeline truth.
program_ref: null
browser_timeline: {...}
```

```yaml
# Invalid: nominal FPS and float seconds replace exact time.
fps: 29.97
start_seconds: 4.2
```

```yaml
# Invalid: Pipeline reconstructs AIR meaning.
archetype: myth_debunk
final_script: "generated from transcript"
```

```yaml
# Invalid: fake/local evidence implies readiness.
probe_status: PASS
production_eligible: true
```

## 7. Implementation stages and exact target paths

These are future paths only. This prompt creates none of them.

### 7.1 Stage 0 — contracts and profile locks

- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/contracts/source_media.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/contracts/video_edit_program.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/contracts/time_mapping.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/contracts/receipts.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/profiles/media_probe.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/video/profiles/reconciliation.py`

Gate: authority ratification/adoption as required, independently accepted upstream specs, schema decisions and Development Capsule. No schema/release bytes now.

### 7.2 Stage 1 — source intake domain and ports

- `src/ca_pipeline/video/domain/source_media_registration.py`
- `src/ca_pipeline/video/domain/media_technical_record.py`
- `src/ca_pipeline/video/ports/source_artifact_reader.py`
- `src/ca_pipeline/video/ports/media_probe.py`
- `src/ca_pipeline/video/application/register_source_media.py`

Maps FR-068/ST-04.01 primary and denial cases. Gate: byte/hash/path/probe/timebase strict tests.

### 7.3 Stage 2 — Interview component reconciliation

- `src/ca_pipeline/video/adapters/interview_transcript_alignment.py`
- `src/ca_pipeline/video/adapters/interview_visual_structure.py`
- `src/ca_pipeline/video/application/reconcile_source_components.py`

Maps FR-068 evidence/replay. Gate: exact TS-INT-002/003 contract, VFR, bounds, limitations and source-authority tests.

### 7.4 Stage 3 — canonical program domain and compiler

- `src/ca_pipeline/video/domain/video_edit_program.py`
- `src/ca_pipeline/video/domain/timeline_element.py`
- `src/ca_pipeline/video/domain/time_mapping.py`
- `src/ca_pipeline/video/application/compile_video_edit_program.py`

Maps FR-067/ST-04.01. Gate: every element resolves; A-roll spine declared; no hidden timeline truth; deterministic round trip.

### 7.5 Stage 4 — durable repository and lifecycle

- `src/ca_pipeline/video/persistence/source_media_repository.py`
- `src/ca_pipeline/video/persistence/video_edit_program_repository.py`
- `src/ca_pipeline/video/persistence/video_dependency_graph.py`
- `src/ca_pipeline/video/persistence/video_outbox.py`

Gate: atomic fault injection, CAS, idempotency, cancellation, invalidation and clean-process replay.

### 7.6 Stage 5 — projection and predecessor migration

- `src/ca_pipeline/video/projections/video_edit_program_projection.py`
- `src/ca_pipeline/video/migrations/studio_video_editing_v1.py`
- `src/ca_pipeline/video/migrations/studio_video_editing_v1_mapping.yaml`

Gate: field-level lossless-or-blocked migration and UI/OTIO projection round trip. Historical Format 02 remains deferred.

### 7.7 Future test paths

- `tests/unit/video/test_source_media_registration.py`
- `tests/unit/video/test_media_time.py`
- `tests/unit/video/test_video_edit_program.py`
- `tests/contract/video/test_interview_alignment_adapter.py`
- `tests/contract/video/test_interview_visual_index_adapter.py`
- `tests/contract/video/test_air_semantic_package_boundary.py`
- `tests/integration/video/test_source_media_intake.py`
- `tests/integration/video/test_video_edit_program_round_trip.py`
- `tests/integration/video/test_video_program_atomicity.py`
- `tests/migration/video/test_studio_v1_timeline_migration.py`
- `tests/architecture/test_video_product_boundaries.py`
- `tests/replay/video/test_video_program_historical_reproduction.py`

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Trigger / owner | Effect and next admissible action |
|---|---|---|
| `VID_SOURCE_PACKAGE_INELIGIBLE` | IE package not approved/current or wrong source scope | Block intake; IE/source owner supplies an eligible version. |
| `VID_SOURCE_ARTIFACT_MISSING` | Exact original bytes unavailable | Block; no reconstruction from proxy/filename. |
| `VID_SOURCE_HASH_MISMATCH` | Observed bytes/hash differ from package manifest | Quarantine operational copy; obtain exact owner bytes. |
| `VID_SOURCE_PATH_UNSAFE` | Absolute/traversal/symlink/device/environment locator | Deny before read/materialization. |
| `VID_PROBE_BINDING_UNAVAILABLE` | Exact executable/profile unavailable | Block registration; no caller-metadata fallback. |
| `VID_PROBE_OUTPUT_INVALID` | Process/raw output missing, altered or unparsable | Fail with raw evidence; retry only if binding policy permits. |
| `VID_STREAM_TIMEBASE_INVALID` | Zero/invalid/overflowing rational timebase | Block affected media registration. |
| `VID_TRANSCRIPT_SOURCE_MISMATCH` | TS-INT-002 source/media/transcript does not match | Block; IE corrects via successor. |
| `VID_TRANSCRIPT_MEDIA_ALIGNMENT_BLOCKED` | Word/phrase/event range irreconcilable | No edit program accepted; emit exact blocked ranges/profile. |
| `VID_VISUAL_INDEX_SOURCE_MISMATCH` | TS-INT-003 source/stream/frame digest mismatch | Block; no visually-similar substitution. |
| `VID_FRAME_ADDRESS_AMBIGUOUS` | Exact presentation frame cannot be resolved | Block affected visual lineage. |
| `VID_DERIVATIVE_JOB_INELIGIBLE` | TS-AHP-003 job stale/blocked/incompatible | Block program compilation. |
| `VID_SEMANTIC_LINEAGE_INCOMPLETE` | AIR Final Script/transfer/role/coalition refs missing | Block; AIR supplies successor; Pipeline does not rebuild. |
| `VID_TIMELINE_ELEMENT_UNRESOLVED` | Element is not source, approved derivative or typed slot | Reject program. |
| `VID_TIME_MAPPING_INVALID` | Mapping out of bounds, ambiguous, illegal or inconsistent | Reject exact element/program per profile. |
| `VID_HIDDEN_TIMELINE_STATE` | Projection cannot reconstruct exact program | Quarantine projection; canonical program remains unchanged. |
| `VID_NOT_APPLICABLE_UNEVIDENCED` | N/A lacks profile/rule/evidence | Reject before identity. |
| `VID_FORMAT02_DEFERRED` | Historical Format 02 enters active program | Block until later governed activation gates. |
| `VID_IDEMPOTENCY_CONFLICT` | Same key/different request bytes | Reject without mutation. |
| `VID_VERSION_CONFLICT` | Expected registration/program head stale | Commit nothing; return current exact ref. |
| `VID_ATOMIC_COMMIT_FAILED` | Any bundled persistence step fails | Roll back all visibility. |
| `VID_LATE_RESULT` | Probe/worker response after cancel/supersede | Quarantine as operational evidence only. |
| `VID_REPLAY_DEPENDENCY_UNAVAILABLE` | Exact historical source/profile/binding missing | Fail replay; never use latest. |
| `VID_REPLAY_DIVERGENCE` | Frozen replay produces different canonical bytes | Quarantine implementation and report expected/observed digest. |
| `VID_AUTHORIZATION_CEILING_EXCEEDED` | Build/production/certification inferred | Deny and identify required gate. |

Failures include code, stage, owner, command/correlation, expected/observed refs/digests, profile/binding, affected ranges/elements, retryability, evidence and next admissible action. Source text/frames and secrets do not enter logs.

### 8.2 Retry versus quality correction

Transient content-store/process/transaction failure may retry only with identical command, idempotency key, bytes and binding where the policy declares equivalence. Alignment, probe, mapping or projection-quality repair uses a new command and immutable successor; it is never a hidden retry. Source or AIR semantic correction belongs to the owning product.

### 8.3 Atomic rollback, cancellation and partial results

Registration/program commits are all-or-nothing. Staged bytes and raw probe evidence remain noncanonical until referenced by a committed receipt. A profile may return a typed partial technical result with explicit blockers, but it cannot be `REGISTERED` or feed program compilation. Cancellation and commit race by transaction order; post-commit cancellation becomes a successor lifecycle action.

### 8.4 Migration and backward compatibility

The predecessor adapter pins exact source byte hash and adapter version. It emits mapping for every field, identifies dropped/derived/blocked fields, preserves historical aliases and never changes old bytes. Missing source hash/package/timebase/lineage/authority blocks. Deprecated program/profile versions remain readable for pinned historical jobs; deprecation does not rewrite them. Compatibility adapters cannot drop restrictions, locks or uncertainties.

### 8.5 Selective invalidation and recovery

Dependency impact classes include `SOURCE_BYTES`, `SOURCE_TECHNICAL_METADATA`, `TRANSCRIPT_ALIGNMENT`, `VISUAL_STRUCTURE`, `SEMANTIC_PROGRAM`, `HARNESS_OR_CATEGORY`, `TIMELINE_ELEMENT`, `PROJECTION_ONLY` and `OPERATIONAL_ONLY`. Source byte change invalidates registration/program descendants. Word timing changes invalidate only elements/mappings that cite affected words/spans. Shot/keyframe correction invalidates affected visual refs/elements. Projection-only changes do not invalidate canonical program. Historical artifacts remain reproducible and current revoked media becomes nonconsumable.

Recovery rebuilds projections/indexes from canonical log, reconciles outbox/idempotency, verifies artifacts and stops at first divergence. No recovery mutates source/program bytes or chooses “close enough” media.

### 8.6 Observability, security and degraded behavior

Signals include source byte/hash verification; probe binding/result; stream/timebase/duration facts; transcript/visual reconciliation counts and reason codes; unresolved limitations; program/element/mapping counts; hidden-state denial; idempotency/CAS/rollback; invalidation fan-out; replay digest; and path/security denials. Logs use refs/digests, not raw transcript, frames, identity/voice payload, local paths or secrets.

Security is operational: least-privilege source grants, sandboxed bounded probes, immutable executable/profile identity, path traversal/device/symlink denial, size/resource limits and source-authority retention/training enforcement. It does not introduce generic creative/content-rights approval authority. When a required probe or exact source is unavailable, the system blocks; caller metadata is not a degraded truth source.

## 9. Behavior-specific acceptance criteria

### AC-01 — FR-068 / ST-04.01 primary source registration

Given an accepted exact interview source package with original video/audio, TS-INT-002 alignment and TS-INT-003 visual index, when intake runs, then byte hashes, streams, timebases, duration, words/phrases, shots/frames/keyframes and restrictions reconcile into one immutable registration. Failure example: `source_ref` copied as a hash. Evidence: hash ledger, probe and reconciliation receipts. Test: integration/contract.

### AC-02 — FR-068 immutable originals

Given source media registration and any probe/reconciliation outcome, original bytes remain byte-identical and no canonical path references a staging/transcoded file. Failure: probe rewrites container metadata. Evidence: before/after SHA-256 and access log. Test: integration/security.

### AC-03 — FR-068 transcript/source denial

Given transcript alignment with wrong media identity, invalid timebase or out-of-bounds duration, admission emits `VID_TRANSCRIPT_SOURCE_MISMATCH` or `VID_TRANSCRIPT_MEDIA_ALIGNMENT_BLOCKED` and no edit program is accepted. Evidence: blocker and empty commit projection. Test: adversarial integration.

### AC-04 — FR-068 variable-frame-rate fidelity

Given variable-frame-rate media, keyframes and shots resolve by presentation ordinal/timestamp/pixel digest rather than nominal FPS and reproduce in a fresh process. Failure: frame selected by `round(seconds * fps)`. Evidence: visual reconciliation receipt/hash. Test: property/integration.

### AC-05 — FR-067 canonical program adoption

Given one eligible derivative job, registration, Harness, AIR semantic package and composition, compilation emits one `VideoEditProgram` with A-roll spine, exact tracks/elements/time map/evaluation/locks/lineage. Failure: a browser-only timeline exists without program bytes. Evidence: canonical program/receipt. Test: contract/integration.

### AC-06 — FR-067 every element resolves

Every program element is exact source, approved derivative, typed generated slot or governed gap. An arbitrary URI/free-form overlay/unknown slot fails `VID_TIMELINE_ELEMENT_UNRESOLVED`. Evidence: element resolution matrix. Test: unit/contract.

### AC-07 — FR-067 source-to-output reconstruction

Given canonical program bytes, reload reconstructs identical tracks, elements, intervals and source-output map and produces the same SHA-256 across fresh processes. Failure: insertion order or UI state changes bytes. Evidence: round-trip/replay comparison. Test: determinism/replay.

### AC-08 — ST-04.01 CBAR A-roll spine

Given a source-led short program, `PRIMARY_A_ROLL_SPINE` is present and bound to original talking-head registration; supporting projections cannot silently replace it. Failure: generated B-roll becomes the only primary track. Evidence: category/Harness validation receipt. Test: contract/architecture.

### AC-09 — AIR meaning remains AIR-owned

Given missing role/tension, Final Script, Primitive/archetype or transfer refs, Pipeline blocks rather than inferring them from transcript/timeline. Evidence: `VID_SEMANTIC_LINEAGE_INCOMPLETE`. Test: architecture/adversarial.

### AC-10 — IE evidence remains IE-owned

Pipeline validates exact words, speakers, shots and keyframes but cannot correct or promote them. A local “speaker=guest” or “important frame” inference fails. Evidence: immutable upstream hash and no IE write port. Test: architecture/contract.

### AC-11 — projection is not authority

Given a Studio/OTIO/renderer projection edit, only a typed command against expected program version may create a successor. Reloading projection without canonical program fails `VID_HIDDEN_TIMELINE_STATE`. Evidence: projection source ref/diff/command receipt. Test: integration/architecture.

### AC-12 — unsafe path and false probe denial

Absolute, UNC, traversal, symlink/device or environment path is rejected. A zero-exit probe without declared result bytes/normalized validation cannot PASS. Evidence: security/probe failure receipt. Test: security/integration.

### AC-13 — evidence-bearing applicability

Absent audio/geometry/optional stream is N/A only with exact rule/evidence/inspected scope. Bare null/N/A fails. Evidence: applicability decision. Test: schema/property.

### AC-14 — generated slot is not a result

An unmaterialized generated slot keeps `execution_eligible=false`; a placeholder/fake URI cannot satisfy it. Evidence: program eligibility result. Test: contract/integration.

### AC-15 — atomicity, idempotency and concurrency

Injected failure at each commit boundary leaves no orphan artifact/receipt/current head; same key/same bytes returns original receipt; same key/different bytes and stale expected version fail. Evidence: fault matrix. Test: repository integration.

### AC-16 — selective invalidation

Correcting one word time invalidates only mappings/elements that cite it; an unrelated keyframe leaves source-only elements current; source byte revocation blocks all current descendants while history remains queryable. Evidence: impact graph and replay. Test: integration.

### AC-17 — lossless-or-blocked predecessor migration

Legacy timeline migrates only when exact source bytes/package/timebase/lineage/roles/functions can be proven. Random IDs and float times become historical evidence, never current truth. Evidence: field mapping/loss receipt. Test: migration.

### AC-18 — Format 02 and certification truth

Historical Format 02 enums/tests do not create an active route. Registration/program/probe/test PASS leaves production/certification false. Evidence: category/status gate. Test: governance/contract.

### AC-19 — cancellation, late results and replay

Cancellation-before-commit produces no current object; late probe result cannot bind; historical replay uses exact old source/profile/binding or fails explicitly. Evidence: ordering/replay receipts. Test: integration/replay.

### AC-20 — candidate-authority ceiling

All output preserves `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, specification work authorized, build false and later ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Evidence: writer/completion receipt. Test: governance.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

- strict model/unknown-field/enum/reference validation;
- rational conversion, overflow, half-open intervals, VFR coordinate and rounding containment;
- canonical bytes across map/order/environment/locale/timezone/hash-seed variation;
- source hash ledger compares actual bytes;
- stream/word/phrase/shot/frame/keyframe bounds and identity;
- complete element resolution and time-map integrity;
- evidence-bearing N/A and restriction/lock monotonicity;
- immutable original source and false production/certification flags.

### 10.2 Contract and architecture tests

- exact TS-AHP-003 derivative-job/source-grant/Harness adapter;
- TS-INT-002 alignment/phrase/limitation adapter preserves all fields or blocks;
- TS-INT-003 VFR/frame/shot/keyframe/visual-ref adapter preserves all fields or blocks;
- TS-AIR-015 semantic/Final Script/transfer/lock adapter preserves all fields or blocks;
- no imports/ports that create IE or AIR meaning, modify Builder Harness, or implement VAE production;
- Studio/OTIO/renderer projections cannot persist canonical timeline state;
- all draft dependencies retain pinned hashes and `DRAFT_DEPENDENCY_NOT_ACCEPTED`.

### 10.3 Integration and adversarial tests

Golden imported-interview slice: exact package bytes, one primary video/audio stream, TS-INT-002 aligned words/phrases/speakers/events, TS-INT-003 VFR frame/shot/keyframe index, eligible TS-AHP-003 job and AIR package compile one source registration and one planning-state `VideoEditProgram`. Reload produces identical bytes.

Adversarial corpus covers altered media bytes, spoofed ref-as-hash, unsafe path, missing probe output, unknown codec/profile, invalid rational timebase, transcript duration/source mismatch, frame pixel mismatch, UI-only edit, arbitrary timeline URI, unresolved generated slot, missing AIR meaning, wrong source grant, revoked source, active Format 02 attempt and fake production claim.

### 10.4 Atomicity, cancellation, recovery and replay

Fault-inject artifact/receipt/event/dependency/idempotency/outbox commits for registration and program. Race duplicate commands and cancellation. Quarantine late results. Rebuild projections from canonical log in fresh processes. Verify historical bytes after supersession/revocation and explicit failure when an exact dependency is missing.

### 10.5 Migration tests

Use exact predecessor fixtures to prove:

- useful track/layer/scene vocabulary maps explicitly;
- random IDs/timestamps/open maps/file URIs/arbitrary hashes are never accepted silently;
- float millisecond/FPS records require exact corroborating source evidence;
- hidden/mutable upsert state blocks migration;
- historical Format 02 remains deferred;
- migration produces a new object and field-level receipt without modifying source files.

### 10.6 Determinism, portability, security and performance evidence

Run clean processes under varied `TZ`, locale, hash seed, working/temp directories, environment order and file discovery order. Compare all canonical hashes and search artifacts for drive/UNC/home/temp/environment leakage. Performance evidence reports byte streaming, probe duration/resource bounds, reconciliation counts and program size as measurements; no invented SLO passes. Security evidence proves sandboxing, least privilege, source-authority restrictions, redaction and no training/retention outside declared scope.

### 10.7 Exact future evidence artifacts

A later authorized build must produce source registration schemas and validators; probe binding/normalization profiles; canonical fixtures; migration mapping; hash/probe/alignment/visual reconciliation receipts; program/round-trip receipts; atomicity/replay/invalidation matrices; architecture boundary report; clean-room manifest; full regression; independent audit/revision/re-audit; ratification/adoption receipt; bounded Development Capsule and Build Receipt. None is issued here.

### 10.8 Traceability and writing-stage state

| Requirement / Story | Design coverage | Evidence ceiling |
|---|---|---|
| FR-067 / ST-04.01 | Sections 3.2–3.6, 5.5–5.7, 6.6–6.9, 8 and AC-05–11/14–20 | Canonical program, mapping, migration, reload, replay and denial evidence only after later build. |
| FR-068 / ST-04.01 | Sections 3.3/3.6–3.8, 5.2–5.4, 6.2–6.5, 8 and AC-01–04/10/12/13/15–20 | Hash ledger, probe, alignment, visual reconciliation and immutable-source evidence only after later build. |

The writer performed no audit, revision, acceptance, implementation, schema publication, contract release, build, capsule, production action or certification. This spec ends `WRITTEN_PENDING_AUDIT`; all four upstreams remain `DRAFT_DEPENDENCY_NOT_ACCEPTED`. The next action is independent audit by a different agent.
