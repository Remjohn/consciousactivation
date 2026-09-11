---
type: technical_specification
spec_id: TS-INT-002
title: Word/Speaker Alignment and Packed Phrase Transcript
version: 2.1.0-candidate
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Interview Expression
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED
output_path_class: DIRECT_PRODUCT_SPEC_PATH
date: '2026-07-22'
controlling_frs: [FR-124, FR-128]
controlling_stories: [ST-01.03, ST-02.01]
upstream_drafts:
  - spec_id: TS-INT-001
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: ca13c9fdcc3b840533de2a955a5388497a434a0b7f94950978012536fd4301e8
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-INT-002 — Word/Speaker Alignment and Packed Phrase Transcript

This specification defines the deterministic technical-evidence surface on which later Reaction Receipts and Expression Moments may cite exact words, speakers, audio events, and source time. It does **not** define Reaction Receipt semantics; `TS-INT-006` owns that separate contract. This document is `WRITTEN_PENDING_AUDIT`, the authority remains `CANDIDATE_NOT_CURRENT`, specification work is authorized, build authority is false, and no Development Capsule, implementation, production claim, or certification is issued.

## 1. Files and authorities read

| Class | Exact path | SHA-256 | State and fact used |
|---|---|---|---|
| V2.1 Constitution candidate | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate pending ratification; planned, observed, inferred, confirmed, rejected, and superseded evidence must not collapse. |
| Interview Expression amendment | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/amendments/INTERVIEW_EXPRESSION_PRD_V2_1_AMENDMENT.md` | `7afd45aaaeff5c1c0b7a82b7df113499873d045e03af0cf91ae9ad4cd1d1d074` | Interview Expression records transcript, word/phrase timing, speakers, audio events, and reaction evidence without taking AIR derivative-semantic ownership. |
| Controlling PRD | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/PRD_COMBINED.md` | `387568731acfe57f022a2fadcd2acfc73baf1287b8a5a1e1d3ed78675ccb067d` | FR-124 requires bounded word/speaker/time alignment; FR-128 requires deterministic packed phrases with raw-word backreferences. |
| Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-01.03 and ST-02.01 require imported-source truth, drift denial, phrase-context fidelity, replay, and selective recovery. |
| Assignment brief | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/spec_assignments/TS-INT-002.md` | `cbe6f5fc5c93064e0b78ab9ac9313f7b17b672934e0bd11dd98a69749adbb2e4` | Assignment-only donor; current Program Control path and V3.3 structure control. |
| Interview-first doctrine | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Source timestamps and transcript segments are required for grounded extraction; anchors and source expression cannot be reconstructed from normalized prose. |
| Studio interview evidence | `THE_CMF_STUDIO(2)/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | `6534c0be726ea542e0a9821edf93c99493ebc8d957e76e80cb1799c6c8de95fd` | Historical/adaptation evidence for immutable transcript revisions, timestamp integrity, receipts, and source lineage; Studio does not own canonical alignment. |
| Pinned upstream draft | `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md` | `ca13c9fdcc3b840533de2a955a5388497a434a0b7f94950978012536fd4301e8` | `WRITTEN_PENDING_AUDIT`; supplies source-root, media timebase, transcript-input, component-slot, package-version, command, atomicity, and invalidation interfaces. |
| Writer skill | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Exactly one ten-section spec; no writer self-audit or acceptance. |
| Recovery packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-INT-002-RECOVERY`; exact direct-product output path. |
| Wave lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_05_DISPATCH_LOCK.yaml` | `e135a1ddce50c52c3a03901cde6feb257c8cf73dc9f81eb02df2484d2a7ad2bf` | Freezes TS-INT-001 at the hash above. |
| Authorization and ceiling | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml`; `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25`; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Specification lifecycle allowed; build/Capsule/production/certification forbidden; ceiling pending ratification. |
| Ownership matrices | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml`; `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39`; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Interview Expression owns source resolution, Reaction evidence, Expression Moments, and the source package; downstream products consume refs without reinterpretation. |
| Queue, FR, path, and source ledgers | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv`; `CANONICAL_FR_LEDGER.csv`; `FR_OWNER_STORY_SPEC_TRACEABILITY.csv`; `PATH_OWNERSHIP_REGISTRY.yaml`; `SOURCE_DISPOSITION_LEDGER.yaml`; `SOURCE_GAP_NOTICE.yaml` | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c`; `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b`; `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6`; `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7`; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3`; `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Exactly two FRs/two Stories; exact path reserved; no blocking required-source gap. |

The dependency-stage ledger (`4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8`) classifies `SDE-026` as a `WRITE_INTERFACE_DEPENDENCY`; acceptance and build do not block WRITE. TS-INT-001 is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Its hash change reopens sections 3, 5, 6, 8, 9, and 10.

The assignment’s external repositories `SRC-EXT-017`, `SRC-EXT-020`, and `SRC-EXT-023` are current `OPTIONAL_REFERENCE`/`DEFERRED_REFERENCE` research-backlog inputs and were not used for factual claims. `SRC-AM-002` is `DEFERRED_REFERENCE`. No unavailable source was reconstructed.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

ASR text alone is not source evidence. If words drift from media time, speakers are swapped, overlap is flattened, hesitations disappear, or phrase packing changes with traversal order, every later Reaction Receipt, Expression Moment, quote, cut, tag, and learning artifact can cite the wrong human or wrong moment. An imported interview is especially vulnerable because absent Brief history may be fabricated to explain the text.

The operator outcome is one immutable, portable alignment component and one deterministic packed phrase transcript that preserve exact source-word identity, speaker identity or explicit ambiguity, rational media time, meaningful audio events, confidence/limitations, and selective invalidation edges. Language-reasoning consumers get compact phrases by default and may retrieve raw words or visual evidence only for the current bounded decision.

### Bounded solution

Implement a deterministic compiler that validates media/time bases, normalizes ASR tokens without changing source truth, aligns speakers and audio events, emits typed low-confidence regions and blockers, packs words into reproducible phrases under one pinned policy, and binds the component into a successor TS-INT-001 package version atomically. It supplies exact evidence refs to TS-INT-006 and TS-INT-004; it does not decide reaction meaning or Expression Moment eligibility.

### In scope

- FR-124 and FR-128; ST-01.03 and ST-02.01;
- word-level tokens, rational time conversion, speaker map, overlap, audio-event map, alignment confidence/limitations, phrase packing, raw-word backreferences, hashes, receipts, correction, supersession, selective invalidation, and historical replay;
- brief-led and imported interviews with explicit planning-lineage distinction;
- deterministic serialization, idempotency, optimistic concurrency, atomic component/package binding, and portable artifact refs;
- bounded retrieval of phrases, raw words, and evidence for later Reaction Receipt/Expression Moment decisions.

### Out of scope and non-goals

- defining Reaction Receipt semantics (`TS-INT-006`), Expression Moment semantics (`TS-INT-004`), shot/keyframe analysis (`TS-INT-003`), AIR semantic programs, derivative scripts, composition, rendering, VAE production, or publishing;
- inventing a Brief, planned tag, speaker identity, missing word, hesitation, audio event, reaction, or approval;
- editing media or “cleaning” speech so the source record no longer matches it;
- external repository adoption, provider selection, model certification, Format 02, VAE Stage 5, code, release bytes, or build authority.

## 3. Governing decisions and constraints

1. **Ownership.** Interview Expression owns source alignment, speaker/time evidence, audio events, phrase packing, corrections, and binding receipts. The operator/source authority owns source-use declarations. TS-INT-006 owns Reaction Receipt semantics; TS-INT-004 owns Expression Moment semantics; AIR owns semantic activation programs; Pipeline consumes eligible source refs.
2. **Raw evidence authority.** Primary media bytes plus the admitted raw ASR/word artifact are canonical for timing/source reconstruction. A packed phrase is a derived reasoning surface, never a replacement lineage root.
3. **No fabricated history.** Imported admission carries TS-INT-001 `AbsentPlanningLineage`; no aligner or phrase compiler may synthesize planned anchors, calls, tags, Matrix use, or Brief history.
4. **Integer/rational time.** Canonical time is non-negative integer source ticks against a positive rational time base. Floating-point seconds are display-only and forbidden in canonical objects or hashes.
5. **Explicit uncertainty.** Low-confidence words, speaker ambiguity, overlap, inaudibility, truncation, and alignment gaps remain typed evidence. Confidence cannot be rounded into certainty.
6. **Meaning-preserving packing.** Packing may normalize display whitespace and governed punctuation only. It must preserve source tokens, word order, meaningful fillers, hesitation, breath/silence/laughter/self-correction markers, speaker changes, and raw-word backreferences.
7. **Determinism.** Same accepted inputs, policy, implementation binding, and declared locale produce byte-identical component, phrase pack, receipt, and hashes independent of current time, randomness, environment, machine paths, map insertion, or filesystem traversal.
8. **No hidden repair.** Alignment correction is a new command and immutable successor. Model-based proposals remain inferred until accepted by deterministic evidence or attributable operator resolution.
9. **No self-acceptance.** Deterministic validation is required; sampling/quality evaluation is independently receipted. A producer cannot approve its own uncertain speaker or drift decision.
10. **Source privacy and portability.** Canonical artifacts contain portable refs/hashes, not absolute paths, local cache roots, credentials, or raw restricted transcript text in logs.

TS-INT-001 remains `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Its component-slot names, media manifest, transcript-input, package state, atomicity, and invalidation interfaces are used only at the pinned hash. Revision-impact sections are `governing_decisions`, `proposed_architecture_and_workflows`, `data_models_contracts_schemas_and_apis`, `failure_migration_rollback_recovery_observability`, `acceptance_criteria`, and `testing_and_completion_evidence`.

The claim ceiling is `WRITTEN_PENDING_AUDIT`, with later maximum `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Passing synthetic alignment tests would not prove real-world speaker accuracy, downstream expression quality, production readiness, or certification.

## 4. Current brownfield architecture

The intended `06_INTERVIEW_EXPRESSION` product root currently contains specifications only; there is no `src/`, tests, schema release, or active alignment service. Future paths below are proposals pending ratification, independent acceptance, and a Development Capsule.

| Evidence | Current behavior | Disposition | Constraint |
|---|---|---|---|
| TS-INT-001 source-package draft | Defines `SourceMediaEntry` rational timebase/duration ticks, `TranscriptInput`, component slots for alignment/word/phrase/speaker/time/audio evidence, immutable package versions, and selective invalidation. | `REUSE` as pinned draft interface | No local component-slot fork; package binding uses successor versions only. |
| AHP assignment TS-INT-002 | Names packed phrase transcript and useful external research topics. | `ADAPT` | It is not a full spec or path authority; optional external sources cannot supply unverified claims. |
| Studio interview PRD | Requires transcript revisions, timestamp integrity, source lineage, alignment receipts, and reconstructable decisions. | `REUSE_AS_EVIDENCE` | Studio projection/control does not become canonical alignment owner. |
| Interview-first doctrine | Preserves transcript segments, timestamps, anchors, and source-grounded extraction. | `REUSE_AS_EVIDENCE` | Do not turn anchor phrases or planned intent into observed source evidence. |
| External reference identifiers | No exact bytes are locked in the current repository. | `DEFER` | Research backlog only; implementation cannot claim copied behavior, license, or performance. |

No current code behavior, provider capability, alignment tolerance, or performance benchmark is inferred from these documents.

## 5. Proposed architecture and workflows

### Components

1. `TranscriptAlignmentApplicationService` validates commands, resolves TS-INT-001 source/package versions, orchestrates ports, and commits one immutable result.
2. `MediaTimebaseValidator` proves duration/time-base compatibility and exact tick↔microsecond conversion bounds.
3. `WordAlignmentCompiler` converts provider/raw tokens into canonical `AlignedWord` records without losing raw refs.
4. `SpeakerMapCompiler` maps diarization labels to source participant refs where supported; unresolved identities remain explicit.
5. `AudioEventCompiler` records silence, breath, laughter, interruption, overlap, self-correction, non-speech, and unknown events with exact spans and evidence.
6. `AlignmentQualityGate` computes deterministic coverage/drift/bounds/ordering checks and typed blocked regions under a pinned profile.
7. `PackedPhraseCompiler` groups words deterministically under a versioned `PhrasePackingPolicy`.
8. `AlignmentEvaluationPort` runs independent review/calibration for uncertain regions; it cannot rewrite canonical words.
9. `TranscriptAlignmentRepository` atomically stores components, edges, command/idempotency records, events, receipts, and TS-INT-001 successor-package binding.
10. `TranscriptEvidenceQueryPort` returns bounded phrase records and, only when requested, exact raw words/audio/visual evidence refs.

### Workflow A — validate source media and transcript input

1. Accept `CompileTranscriptAlignmentCommand` with exact package/media/transcript refs, policy/binding refs, idempotency key, expected package version/hash, actor/authority, and requested source language.
2. Confirm the transcript belongs to the same source root and the source-authority scope permits processing. Preserve `BRIEF_LED` or `IMPORTED`; never synthesize missing planning.
3. Validate every media duration and rational time base. Convert time only with exact integer arithmetic and a declared rounding policy (`FLOOR_START`, `CEIL_END`) so spans never shrink source evidence.
4. Reject negative/out-of-bounds/non-monotonic time, zero denominators, missing source refs, or provider tokens without a deterministic stable order.

### Workflow B — compile words, speakers, and audio events

1. Stable-sort raw tokens by `(start_tick, end_tick, provider_segment_ordinal, provider_token_ordinal, raw_token_sha256)`; duplicated ordinals or unresolved collisions block.
2. Emit one immutable `AlignedWord` per admitted token. Preserve raw text, governed display text, source span, confidence micros, language, and flags. No filler or hesitation is dropped.
3. Resolve speaker labels using diarization evidence and participant mapping. A word may carry one resolved speaker, one explicit `UNKNOWN`, or a typed overlap set; silent majority-vote attribution is forbidden.
4. Align audio events independently. Event ranges may overlap words and must remain retrievable by phrase/source span.
5. Build low-confidence regions from exact word/speaker/time/event limitations; do not conceal them in an average score.

### Workflow C — validate alignment

1. Run bounds, source-root, monotonicity, gap/overlap, speaker coverage, raw-token coverage, event coverage, duration reconciliation, and reversible-conversion checks.
2. Apply the pinned `AlignmentAcceptanceProfile`; the profile owns tolerances and sampling requirements. This spec invents no thresholds.
3. Hard failures block affected ranges or the whole component according to the profile. Independent evaluation may resolve a sampled uncertainty only by an immutable resolution receipt.
4. Emit `TranscriptAlignmentComponent` plus `AlignmentValidationReceipt` in `ACCEPTED`, `PARTIAL_BLOCKED`, or `REJECTED` state.

### Workflow D — pack phrases deterministically

1. Accept only an accepted/partially accepted alignment and exclude blocked word ranges from eligibility while preserving them in history.
2. Traverse canonical word order once. Phrase boundaries are introduced by versioned policy on speaker change, explicit terminal punctuation, audio-event boundary, declared maximum gap/duration/token count, source segment boundary, language change, or operator-confirmed boundary.
3. A boundary never discards a word. Fillers/events declared editorially meaningful stay in phrase text/event refs; any display normalization produces a typed transformation record.
4. Emit `PackedPhrase` records with exact ordered word refs, start/end ticks, speaker state, event refs, tag refs by epistemic state, display text, verbatim reconstruction hash, and limitations.
5. Verify that concatenated phrase word refs cover every eligible word exactly once in original order. Emit `PackedPhraseTranscript` and `PhrasePackingReceipt`.

### Workflow E — bind, query, correct, invalidate, and replay

1. Atomically store alignment, phrase pack, receipts, dependency edges, command/event/idempotency records, and a TS-INT-001 successor package binding the `TRANSCRIPT_ALIGNMENT`, `WORD_TIMING`, `PHRASE_TIMING`, `SPEAKER_MAP`, `TIME_ALIGNMENT`, and `AUDIO_EVENT_MAP` slots.
2. Query consumers request phrase windows by exact source interval, speaker, or phrase refs. Raw words and audio/visual evidence are loaded only when the decision contract requires them.
3. A correction command names affected word/speaker/boundary refs and produces successor components/package. Typed dependency traversal invalidates only phrases, Reaction Receipts, Expression Moments, and derivatives that cite changed spans.
4. Historical replay uses exact old media/transcript/policy/binding refs and reproduces old hashes. Current aliases are forbidden.

### Atomicity, idempotency, concurrency, and cancellation

One transaction contains all component artifacts, receipts, edges, events, command record, idempotency record, and successor package binding. Partial visibility is corruption. Identical key/input hash returns the original receipt; same key/different input fails. Stale expected package version/hash commits nothing. Cancellation that wins before commit records a cancellation receipt; late provider/evaluator results remain late evidence and cannot bind automatically.

## 6. Data models, contracts, schemas, and APIs

All records are immutable, reject unknown fields, use nonempty normalized strings, closed enums/tagged unions, integer ticks/micros, and portable immutable refs. No `Any`, open dictionary, floating-point canonical field, implicit current time, random ID, or mutable default is allowed.

### Time and source primitives

```text
RationalTimebase { numerator: PositiveInt, denominator: PositiveInt }
SourceTime { media_ref: ImmutableRef, ticks: NonNegativeInt, timebase: RationalTimebase }
SourceInterval { media_ref: ImmutableRef, start_ticks: NonNegativeInt, end_ticks: PositiveInt, timebase: RationalTimebase }
```

`end_ticks > start_ticks`; both ends are within the TS-INT-001 `SourceMediaEntry.duration_ticks`. Cross-timebase comparison uses exact rational multiplication with overflow-checked integers. Canonical conversion to microseconds records numerator/denominator and start/end rounding modes.

### `AlignedWord` — `ca.interview.aligned-word/2.1.0-candidate`

| Field | Type | Validation / owner |
|---|---|---|
| `word_id` | deterministic ID | Interview Expression; derived from source root, transcript, ordinal, interval, and raw hash. |
| `source_root_ref` | `ImmutableRef` | TS-INT-001 exact root. |
| `transcript_input_ref` | `ImmutableRef` | TS-INT-001 exact input. |
| `raw_token_ref` | `ImmutableRef` | ASR/source owner; mandatory and unique. |
| `provider_segment_ordinal` / `provider_token_ordinal` | non-negative integers | Establish stable raw order. |
| `raw_text` | `NonEmptyText` | Verbatim token evidence. |
| `display_text` | `NonEmptyText` | Governed normalization only; transformation ref required if different. |
| `interval` | `SourceInterval` | Exact source time. |
| `speaker` | `ResolvedSpeaker | UnknownSpeaker | OverlappingSpeakers` | No guessed identity. |
| `language` | `LanguageAssertion` | Value, provenance, epistemic state. |
| `confidence_micros` | integer `0..1_000_000` | Provider/deterministic evidence; not acceptance. |
| `flags` | canonical set of `FILLER | HESITATION | SELF_CORRECTION | TRUNCATED | INAUDIOBLE | OVERLAP | PUNCTUATION_ONLY | LOW_CONFIDENCE` | Closed set. |
| `audio_event_refs` | ordered tuple of `ImmutableRef` | Events intersecting the interval. |
| `supersedes_ref` | `ImmutableRef?` | Required for correction. |

`ResolvedSpeaker` has `participant_ref`, `diarization_label`, `mapping_evidence_refs`, and `confidence_micros`. `UnknownSpeaker` has label/evidence/limitation code. `OverlappingSpeakers` has two or more ordered speaker assertions and overlap evidence.

### Speaker, event, limitation, and alignment models

`SpeakerMap` contains source root, diarization-track ref, canonical speaker assertions, participant mapping evidence, unresolved labels, overlap policy ref, evaluation receipt, and hash. `AudioEvent` contains event ID, closed kind (`SILENCE`, `BREATH`, `LAUGHTER`, `SIGH`, `INTERRUPTION`, `OVERLAP`, `SELF_CORRECTION`, `NON_SPEECH`, `UNKNOWN`), interval, evidence refs, confidence micros, and epistemic state.

`AlignmentLimitation` contains code, exact affected interval/word refs, severity (`INFO | BLOCK_RANGE | BLOCK_COMPONENT`), evidence refs, responsible owner, and next admissible action. Generic notes cannot substitute.

`TranscriptAlignmentComponent` — `ca.interview.transcript-alignment/2.1.0-candidate` — contains:

- `component_version`, `source_root_ref`, `package_ref`, `media_manifest_ref`, `transcript_input_ref`;
- `word_refs` in canonical order, `speaker_map_ref`, `audio_event_refs`, and `limitation_refs`;
- `time_conversion_profile_ref`, `alignment_acceptance_profile_ref`, `compiler_binding_ref`;
- raw-token count, eligible-word count, blocked-word count, coverage micros, and duration reconciliation evidence;
- `validation_receipt_ref`, state `COMPILED | PARTIAL_BLOCKED | ACCEPTED | REJECTED | SUPERSEDED | INVALIDATED`, `supersedes_ref?`, and `content_sha256`.

`ACCEPTED` requires every mandatory hard gate pass. `PARTIAL_BLOCKED` exposes only eligible ranges and cannot masquerade as global acceptance.

### Packed phrase contracts

`PhrasePackingPolicy` is immutable and declares boundary causes, terminal punctuation set, gap/duration/token limits as exact integers, language handling, speaker-change rule, event-preservation rule, display-normalization profile, and policy version/hash.

`PackedPhrase` contains `phrase_id`, `source_root_ref`, `alignment_ref`, contiguous ordered `word_refs`, `interval`, `speaker_state`, `raw_reconstruction_sha256`, `display_text`, `display_transformation_refs`, `audio_event_refs`, `tag_assertion_refs`, `limitation_refs`, `boundary_before`, and `boundary_after`. Tag refs retain `PLANNED | OBSERVED | INFERRED | OPERATOR_CONFIRMED | REJECTED | SUPERSEDED`; phrase packing never promotes a tag.

`PackedPhraseTranscript` — `ca.interview.packed-phrase-transcript/2.1.0-candidate` — contains component version, source/package/alignment/policy refs, canonical phrase refs, eligible/blocked word counts, compression ratio as integer numerator/denominator, complete coverage proof hash, retrieval-index ref, validation receipt, lifecycle, supersedes ref, and content hash.

### Receipts, commands, events, and repository

`AlignmentValidationReceipt` includes exact input/output refs, policy/binding refs, hard-gate results, blocked regions, deterministic metrics, independent-review ref if applicable, actor/authority, command, dependency edges, result code, and hash. `PhrasePackingReceipt` includes alignment/policy refs, word/phrase counts, exact coverage/order proof, transformation inventory, limitations, and result. Neither is a Reaction Receipt.

Commands are `CompileTranscriptAlignment`, `ValidateTranscriptAlignment`, `PackPhraseTranscript`, `BindTranscriptComponents`, `CorrectWordTiming`, `CorrectSpeakerAssignment`, `CorrectPhraseBoundary`, `SupersedeTranscriptComponents`, `InvalidateTranscriptDescendants`, `CancelTranscriptCompilation`, and `ReplayTranscriptComponents`. Each uses command ID, idempotency key, actor/authority, exact expected package version/hash, input/policy/binding refs, and authority-supplied request time.

Repository interface:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_word_range(alignment_ref, interval) -> tuple[AlignedWord, ...]
load_phrase_window(pack_ref, phrase_refs, evidence_level) -> PhraseEvidenceWindow
commit(bundle: TranscriptComponentCommitBundle, expected_package_ref) -> ComponentBindingReceipt
lookup_idempotency(source_root_id, command_kind, key) -> IdempotencyRecord | null
list_descendants(root_refs, edge_types) -> tuple[ImmutableRef, ...]
replay(source_root_id, through_package_version) -> ReplayResult
```

`PhraseEvidenceWindow.evidence_level` is `PHRASES_ONLY | PHRASES_AND_RAW_WORDS | FULL_SOURCE_EVIDENCE`; the caller’s contract must authorize the latter two.

### Canonical serialization, hashing, and examples

Canonical JSON is UTF-8, normalized, lexicographically keyed, integers only, with arrays ordered by explicit semantic order. Set-like values are canonical-sorted. IDs/hashes exclude absolute paths, environment, process, clock, random state, cache layout, and provider response order. `content_sha256` hashes the payload excluding itself.

Positive phrase example:

```yaml
phrase_id: phr_000042
word_refs: [word_00102, word_00103, word_00104]
interval: {media_ref: primary-audio, start_ticks: 48120, end_ticks: 53640, timebase: {numerator: 1, denominator: 48000}}
speaker_state: {kind: RESOLVED, participant_ref: guest-julie}
display_text: "I… I chose to leave."
audio_event_refs: [event_hesitation_17]
boundary_before: SPEAKER_CHANGE
boundary_after: TERMINAL_PUNCTUATION
```

Negative example: a phrase claiming `guest-julie`, starting before zero, omitting two eligible raw-word refs, or normalizing away the hesitation is rejected; no speaker or missing token is inferred.

Adapters must preserve source root, raw token refs/order, rational time, speaker ambiguity, events, limitations, epistemic states, and hashes. Parsing while dropping hesitation or enforcing no bounds is incompatible.

## 7. Implementation stages and exact target paths

These are future targets only.

| Stage | Exact future path | FR / Story | Evidence |
|---|---|---|---|
| Capsule/source lock | `06_INTERVIEW_EXPRESSION/development-capsules/TS-INT-002/SOURCE_LOCK.yaml` | all | Only after ratification, acceptance, and Capsule authorization. |
| Domain models | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/domain/transcript_alignment.py` | 124, 128 | Strict types, schemas, canonical examples. |
| Contracts | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/contracts/transcript_alignment.py` | 124, 128 | Commands/events/receipts/query types. |
| Time and alignment compiler | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/transcript_alignment_service.py` | 124 / 01.03 | Exact rational time, word/speaker/event compilation and validation. |
| Phrase compiler | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/packed_phrase_compiler.py` | 128 / 02.01 | Deterministic boundaries, coverage, transformations, tags. |
| Policies | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/policies/alignment_acceptance_policy.py`; `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/policies/phrase_packing_policy.py` | both | Versioned gates/limits; no hard-coded hidden thresholds. |
| Repository | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/repositories/transcript_component_repository.py` | both | Atomic artifact/receipt/package/edge/command/idempotency commit. |
| TS-INT-001 adapter | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/source_package_transcript_adapter.py` | both | Exact component slots and successor package binding. |
| Migration | `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/migrations/transcript_alignment_v1_to_v2_1.py` | both | New immutable artifacts; no guessed speaker/time/history. |
| Contract/unit/integration tests | `06_INTERVIEW_EXPRESSION/tests/contracts/test_transcript_alignment_contracts.py`; `06_INTERVIEW_EXPRESSION/tests/unit/test_timebase_and_phrase_packing.py`; `06_INTERVIEW_EXPRESSION/tests/integration/test_word_speaker_alignment_and_phrase_pack.py` | both Stories | Positive/adversarial/replay/selective recovery. |
| Architecture/reproduction tests | `06_INTERVIEW_EXPRESSION/tests/architecture/test_transcript_product_boundaries.py`; `06_INTERVIEW_EXPRESSION/tests/reproducibility/test_transcript_fresh_process.py` | all | No TS-INT-006 semantic ownership; byte-identical fresh processes. |

## 8. Failure, migration, rollback, recovery, and observability

| Code | Trigger | Behavior |
|---|---|---|
| `INT_TA_REQUIRED_SOURCE_MISSING` | Required media/transcript/source authority absent. | Block; reconstruct nothing. |
| `INT_TA_UPSTREAM_DRAFT_DRIFT` | TS-INT-001 hash differs. | Block and reopen six revision-impact sections. |
| `INT_TA_TIMEBASE_INVALID` | Zero/negative denominator, overflow, or irreconcilable timebase. | Reject component. |
| `INT_TA_SOURCE_BOUNDS_VIOLATION` | Word/event/phrase exceeds media duration. | Block exact range or component per profile. |
| `INT_TA_RAW_ORDER_AMBIGUOUS` | Duplicate/unresolvable provider ordinals. | Reject deterministic compilation. |
| `INT_TA_SPEAKER_UNRESOLVED` | Required speaker cannot be supported. | Preserve unknown/block range; never guess. |
| `INT_TA_DIARIZATION_CONFLICT` | Speaker mapping conflicts with evidence. | Emit limitation and independent-review request. |
| `INT_TA_DRIFT_EXCEEDED` | Alignment drift exceeds pinned tolerance. | Block affected ranges before downstream extraction. |
| `INT_TA_WORD_COVERAGE_GAP` | Eligible raw token missing/duplicated in words or phrases. | Reject pack. |
| `INT_TA_MEANINGFUL_EVENT_DROPPED` | Filler/hesitation/event removed without declared transformation. | Reject pack. |
| `INT_TA_TAG_STATE_FLATTENED` | Packed phrase promotes or collapses tag epistemic state. | Reject. |
| `INT_TA_IDEMPOTENCY_CONFLICT` | Same key/different canonical input. | Reject; preserve original receipt. |
| `INT_TA_VERSION_CONFLICT` | Expected package ref is stale. | Commit nothing; return current ref. |
| `INT_TA_ATOMIC_COMMIT_FAILED` | Any artifact/receipt/edge/package write fails. | Roll back all visibility. |
| `INT_TA_LATE_RESULT` | Result arrives after cancel/supersede. | Store late evidence only. |
| `INT_TA_REPLAY_DIVERGENCE` | Same frozen inputs produce different bytes. | Fail evidence gate; preserve diagnostics. |

Transient retries reuse the same command/idempotency identity. Quality correction creates a new command and successor; it is never a retry.

Migration ingests legacy words/segments only when raw source, time base, source root, stable ordering, and speaker evidence are preserved. Floating seconds are converted with a pinned rational/rounding policy and original value evidence. Missing source kind, time base, speaker uncertainty, word order, or planning-history truth blocks migration. Deprecated artifacts remain historical and readable.

Corrections invalidate only descendants whose dependency edges intersect changed word, speaker, event, or phrase refs. Historical packages/Reaction Receipts/Expression Moments remain reproducible even when no longer current. Rollback changes the active compiler/policy binding for new work; it never mutates artifacts from the failed binding.

Structured logs contain refs/hashes/counts/reason codes, not unrestricted transcript text, voice/identity payloads, or local paths. Metrics cover bounds/drift/coverage/speaker ambiguity/event preservation, blocked ranges, correction frequency, phrase compression, raw-word retrieval, idempotency/concurrency, atomic rollback, invalidation fan-out, late results, and replay divergence. Operational telemetry is not semantic authority.

## 9. Behavior-specific acceptance criteria

1. **FR-124 / ST-01.03 — exact multi-speaker alignment.** Given admitted multi-speaker media and raw ASR, when alignment completes, every eligible word has one exact source interval and resolved/unknown/overlap speaker state within media bounds. Assigning an unknown word to the nearest speaker fails. Evidence: component, bounds/diarization receipt, sample review. Layer: contract/integration.
2. **FR-124 / ST-01.03 — drift denial.** Given a range beyond the profile’s drift tolerance, when downstream extraction requests it, the range is blocked or corrected first. Allowing it because global average confidence passes fails. Evidence: range blocker and unchanged package eligibility. Layer: integration.
3. **FR-124 / ST-01.03 — imported-source truth.** Given an imported interview without a Brief, when alignment binds, `AbsentPlanningLineage` remains intact and no planned anchor/tag/Matrix ref is created. Inferring a historical plan fails. Evidence: before/after package diff. Layer: cross-spec contract.
4. **FR-124 / ST-01.03 — timebase reproducibility.** Given video/audio with different rational time bases, two fresh processes produce identical tick conversions and spans. Floating-seconds rounding drift fails. Evidence: byte/hash comparison. Layer: unit/reproducibility.
5. **FR-128 / ST-02.01 — deterministic phrase pack.** Given accepted words and one policy, phrase IDs/order/text/intervals/backrefs/hash are byte-identical across input map/traversal order changes. Nondeterministic boundary order fails. Evidence: phrase-pack hashes. Layer: unit/reproducibility.
6. **FR-128 / ST-02.01 — complete word coverage.** Every eligible word appears exactly once and in order; blocked words remain explicitly excluded with limitations. Dropped/duplicated words fail. Evidence: coverage proof. Layer: contract.
7. **FR-128 / ST-02.01 — hesitation preservation.** Given a hesitation used by later reaction/expression analysis, packing retains its word/event refs and readable marker. Normalizing it away fails. Evidence: raw-to-phrase diff and transformation inventory. Layer: adversarial integration.
8. **FR-128 / ST-02.01 — epistemic tag separation.** Given a planned tag and unrelated observed answer, phrases retain distinct tag states; default routing exposes observed/confirmed only unless an operator resolution authorizes otherwise. Promoting planned to observed fails. Evidence: tag refs/query result. Layer: contract/integration.
9. **Reaction Receipt boundary.** Given TS-INT-006 cites a hesitation or state-change span, the cited phrase resolves to exact raw words, speaker, event, and time. This spec does not assert reaction meaning. A phrase pack emitting its own Reaction Receipt fails architecture. Evidence: dependency contract test. Layer: architecture/integration.
10. **Selective correction.** Given one speaker assignment is corrected, only intersecting phrases and semantic descendants become stale; unrelated phrases and historical receipts remain valid/replayable. Global package deletion fails. Evidence: invalidation graph/replay. Layer: integration.
11. **Atomicity/idempotency/concurrency.** Same command/key returns original receipt; same key/different input fails; stale expected package commits nothing; injected mid-commit failure leaves no orphan component/receipt/package binding. Evidence: fault log. Layer: repository integration.
12. **Portability and claim ceiling.** Canonical artifacts contain no absolute machine path/environment/current-time/random fields, and even complete synthetic tests leave production eligibility/certification false. A local PASS represented as real-world accuracy or build approval fails. Evidence: artifact scan/completion receipt. Layer: clean-environment/governance.

## 10. Testing and completion evidence

Exact future suites:

- `tests/contracts/test_transcript_alignment_contracts.py`: unknown fields, rational time, closed enums, speaker unions, bounds, receipt/tag states, positive/negative examples.
- `tests/unit/test_timebase_and_phrase_packing.py`: overflow-safe conversion, stable ordering, all boundary causes, fillers/events, canonical hashes, property tests.
- `tests/integration/test_word_speaker_alignment_and_phrase_pack.py`: both Stories, imported history, TS-INT-001 binding, TS-INT-006/004 evidence handoff, corrections.
- `tests/integration/test_transcript_repository_atomicity.py`: command/artifact/receipt/edge/package parity, idempotency, concurrency, cancellation, fault injection.
- `tests/migrations/test_transcript_alignment_v1_to_v2_1.py`: lossless mappings and exact blockers for missing evidence.
- `tests/architecture/test_transcript_product_boundaries.py`: Interview Expression ownership, no AIR/Pipeline/Studio/VAE semantic mutation, no TS-INT-006 contract duplication.
- `tests/reproducibility/test_transcript_fresh_process.py`: two fresh processes, locale/timezone/environment/map/filesystem perturbation, exact byte/hash equality.
- `tests/security/test_transcript_evidence_redaction.py`: logs/metrics contain refs and hashes rather than restricted text/PII/secrets.

Fixtures cover mono/stereo and distinct time bases; multi-speaker turns; overlap; unknown speaker; empty/partial transcript; out-of-bounds/negative/non-monotonic words; drift; duplicated ordinals; filler, hesitation, breath, laughter, interruption, silence, self-correction; multilingual transitions; punctuation/no punctuation; very long gaps; blocked regions; planned/observed/inferred/confirmed/rejected/superseded tags; imported missing Brief; corrections; stale package; cancellation/late result; legacy float timestamps; absolute paths; and downstream citation/replay.

A later authorized implementation requires a ratified/accepted spec hash in a Development Capsule, schema and fixture hashes, benchmark data with declared tolerance profiles, independent diarization/alignment review evidence, phrase coverage/compression/context-size evidence, atomicity/selective-invalidation/historical-replay proof, fresh-environment reproduction, portability scan, and a Build Receipt whose claim ceiling remains evidence-specific. This writer issues none of those artifacts. The next permitted step is independent audit by a different agent.
