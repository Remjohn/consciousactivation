---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F12
title: "Source-First Short-Form Video Editing and Adopted Timeline Runtime"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-067–FR-072"
---

# F12 — Source-First Short-Form Video Editing and Adopted Timeline Runtime

## 1. Product claim and user outcome

**User outcome:** Interview-derived shorts preserve talking-head A-roll as the base timeline and automate word-safe, source-grounded editing through a canonical VideoEditProgram.

Adopt predecessor edit/timeline contracts, bind source spans, support layers, and temporal embodiments, and keep the UI as a projection and command surface. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

The owning product is the Atomic Harness Pipeline unless an FR explicitly assigns Interview Expression, VAE, Delegation, Studio, Program Control, or an external runtime.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Original talking-head footage remains the A-roll spine.
- No second timeline truth exists.
- Every cut and layer preserves source/function lineage.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-CUR-007` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py | Category-native runtime plan requirements, evaluation dimensions and repair units. |
| `SRC-LEG-006` | `FORK` | src/ccp_studio/contracts/video_editing_engine.py | Reuse timeline, tracks, captions, transitions, audio and export contracts. |
| `SRC-LEG-007` | `FORK_ADAPT` | src/ccp_studio/services/video_editing_engine_service.py | Bind to current Timeline IR and format-native runtime plans. |
| `SRC-LEG-008` | `FORK` | src/ccp_studio/services/video_timeline_service.py | Deterministic timeline construction. |
| `SRC-LEG-009` | `FORK` | src/ccp_studio/services/video_audio_service.py | Audio plan and mix metadata. |
| `SRC-LEG-010` | `FORK` | src/ccp_studio/services/video_caption_service.py | Caption planning contract; renderer-specific realization stays in adapters. |
| `SRC-LEG-011` | `FORK` | src/ccp_studio/services/video_media_probe_service.py | Media inspection via ffprobe. |
| `SRC-LEG-012` | `FORK_ADAPT` | src/ccp_studio/services/video_source_asset_service.py | Source media registry and lineage. |
| `SRC-AM-001` | `AMENDMENT_INPUT` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-EXT-017` | `REFERENCE` | github://browser-use/video-use | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-EXT-018` | `REFERENCE_LICENSE_REVIEW` | github://remotion-dev/remotion | React/frame source-of-truth rendering, Player, batch rendering, and editor integration. |
| `SRC-EXT-019` | `REFERENCE` | github://heygen-com/hyperframes | Deterministic HTML/CSS/GSAP motion blocks, skills, registry, Studio, and Player. |
| `SRC-INT-001` | `ADAPT` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-INT-002` | `ADAPT` | THE_CMF_STUDIO(2).zip::CCP V9 Interview-First Expression Engine.md | Expression capture, source truth, archetype routing, and interview-first doctrine. |
| `SRC-INT-003` | `ADAPT` | THE_CMF_STUDIO(2).zip::CCP V9.1 Expression Capture & Archetype Routing Update.md | Expression Moment and archetype-routing refinements. |
| `SRC-AM-002` | `AMENDMENT_INPUT` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-EXT-020` | `REFERENCE` | github://UVA-Computer-Vision-Lab/OmniShotCut | Shot-boundary and transition classification. |
| `SRC-EXT-023` | `REFERENCE` | github://SamurAIGPT/AI-Youtube-Shorts-Generator | Long-video chunking with overlap, deduplication, caching, structured JSON, and vertical crop patterns. |

## 5. Workflow integration

Validated upstream state → feature behavior → typed output and receipt → downstream handoff → evaluation, invalidation, and replay.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-067 — Adopt the existing VideoEditProgram and timeline contracts

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** The Pipeline shall adopt and normalize the predecessor CMF edit-decision and timeline contracts as the canonical temporal editing program, extending them for current source lineage, Activative sequence, Transformation Contracts, runtime bindings, evaluation, and selective repair rather than creating a second timeline model.

**Trigger and preconditions:** An edited-video Atomic Harness reaches temporal planning with an accepted Canonical Interview Source Package and source-backed sequence purpose.

**Required output or state transition:** A versioned VideoEditProgram containing source spans, output-time mapping, tracks, captions, audio, visual treatments, runtime bindings, evaluation requirements, and exact lineage.

**Authority and invariants:**
- No second timeline truth is introduced.
- The UI remains a projection and command surface.
- Source meaning and approved span lineage cannot be changed by renderer adapters.

**Acceptance scenarios**

- **Primary success:** Given a valid interview source package and Harness sequence, when the temporal program is compiled, then every program element resolves to an existing source, approved derivative, or typed generated slot and can be reconstructed after reload.
- **Adversarial or denial case:** Given an implementation that stores hidden timeline state only inside a browser component, when the project is reopened, then admission fails because the canonical program cannot be reproduced.
- **Evidence required:** Canonical serialized program, migration mapping from predecessor contracts, schema validation, round-trip test, and source-lineage receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035, D043, D049, D053  
**Exact source references:** SRC-CUR-007, SRC-LEG-006, SRC-LEG-007, SRC-LEG-008, SRC-LEG-009, SRC-LEG-010, SRC-LEG-011, SRC-LEG-012, SRC-AM-001, SRC-EXT-017, SRC-EXT-018, SRC-EXT-019


### FR-068 — Register canonical interview source media

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** The temporal runtime shall ingest source media only through an accepted Canonical Interview Source Package, verify immutable file identities and technical metadata, and expose source-time ranges without mutating the originals.

**Trigger and preconditions:** A source package is admitted for a short-video job.

**Required output or state transition:** Source asset records, ffprobe metadata, time bases, audio streams, shot map, transcript alignment, keyframe references, and immutable source hashes.

**Authority and invariants:**
- Original source bytes remain untouched.
- All derivative timestamps use declared source time bases.
- Missing or unverifiable source files block execution.

**Acceptance scenarios**

- **Primary success:** Given an uploaded interview and transcript, when intake completes, then the runtime can resolve every transcript word and candidate span to the exact source file and time range.
- **Adversarial or denial case:** Given a transcript whose duration or source identity cannot be reconciled with the video, when admission runs, then no edit decision is accepted and a typed alignment blocker is issued.
- **Evidence required:** Media probe receipt, hash ledger, transcript alignment report, shot/keyframe index, and source-package acceptance receipt.

**Governing decisions:** D023, D027, D043, D044, D054  
**Exact source references:** SRC-INT-001, SRC-INT-002, SRC-INT-003, SRC-AM-002, SRC-EXT-017, SRC-EXT-020, SRC-EXT-023


### FR-069 — Compile source-backed A-roll edit decisions

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** Every selected A-roll span, cut, hold, reorder, reaction extension, and transition shall preserve exact source-time lineage, land on valid word or audio-event boundaries where required, declare its narrative or Activative function, and map deterministically into output time.

**Trigger and preconditions:** A short-video Harness has an approved source expression sequence and target duration.

**Required output or state transition:** A-roll EDL entries with source ID, source start/end, output start/end, transcript phrase/word refs, speaker, beat/archetype role, cut padding, and reason.

**Authority and invariants:**
- No cut occurs inside a protected word.
- Reactions, laughter, sighs, and expression tails are not removed without an explicit decision.
- Source order changes remain inspectable.

**Acceptance scenarios**

- **Primary success:** Given an approved Expression Moment, when the A-roll compiler creates a short, then the result begins and ends on permitted source boundaries and the output duration is recomputable from the EDL.
- **Adversarial or denial case:** Given a proposed cut through a word or an unsupported paraphrase represented as source speech, when validation runs, then the EDL is rejected before rendering.
- **Evidence required:** Word-boundary validation, source/output time map, EDL hash, phrase references, and cut-purpose receipt.

**Governing decisions:** D023, D027, D043, D044, D052, D053  
**Exact source references:** SRC-AM-002, SRC-EXT-017, SRC-EXT-020, SRC-EXT-023, SRC-EXT-024, SRC-LEG-006, SRC-LEG-007


### FR-070 — Compile captions, audio, evidence, and motion support around A-roll

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** The edit program shall compile exact captions, audio treatment, color, reframing, B-roll, evidence inserts, keyframe freezes, designed overlays, annotation cues, and bounded animation slots as supporting layers around the talking-head A-roll spine.

**Trigger and preconditions:** The A-roll EDL is accepted and the Harness declares supporting visual or audio functions.

**Required output or state transition:** Typed track/layer records, caption plan, audio mix plan, B-roll/evidence slots, motion-block requests, composition constraints, and child-runtime bindings.

**Authority and invariants:**
- Supporting layers cannot contradict or replace source truth.
- Captions preserve verbatim source words unless explicitly marked as editorial text.
- Every insert has a declared function and lineage.

**Acceptance scenarios**

- **Primary success:** Given a claim with supporting evidence, when a proof card is inserted, then it is timed to the source statement, cites its evidence object, respects face/caption safe regions, and returns to A-roll without losing source continuity.
- **Adversarial or denial case:** Given an attractive generated overlay with no declared function or evidence, when program validation runs, then it is excluded from the accepted edit program.
- **Evidence required:** Track manifest, caption word map, audio plan, motion-slot receipts, B-roll/evidence lineage, and composition preview.

**Governing decisions:** D023, D027, D043, D044, D053  
**Exact source references:** SRC-EXT-017, SRC-EXT-018, SRC-EXT-019, SRC-EXT-021, SRC-EXT-022, SRC-LEG-008, SRC-LEG-009, SRC-LEG-010


### FR-071 — Bind temporal embodiments explicitly

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** Remotion, HyperFrames, FFmpeg, Stretchy/Spine, or another approved temporal embodiment shall be selected through an immutable compatibility and authority decision; child renderers may realize bounded slots but may not silently replace the master edit program or each other.

**Trigger and preconditions:** A validated VideoEditProgram requires one or more renderer capabilities.

**Required output or state transition:** A runtime binding manifest identifying master compositor, child slots, versions, dependencies, fallback policy, and expected artifacts.

**Authority and invariants:**
- No silent renderer substitution.
- Renderer selection does not change semantic or composition authority.
- License and capability eligibility precede execution.

**Acceptance scenarios**

- **Primary success:** Given a Remotion master timeline and a HyperFrames motion slot, when rendering starts, then both exact bindings are recorded and the HyperFrames output is consumed only at its declared slot.
- **Adversarial or denial case:** Given an unavailable Remotion binding, when the fallback is not explicitly authorized, then the system blocks rather than switching to a different compositor.
- **Evidence required:** Binding decision, compatibility report, runtime health check, license disposition, and resolved execution fingerprint.

**Governing decisions:** D023, D027, D049, D053  
**Exact source references:** SRC-EXT-018, SRC-EXT-019, SRC-EXT-025, SRC-LEG-013, SRC-LEG-014, SRC-LEG-015


### FR-072 — Enforce FFmpeg production-correctness rules

**Lifecycle:** `AMENDED_V1_1`  
**Normative requirement:** FFmpeg shall be a first-class media engine for probe, lossless extraction where eligible, trim, concat, audio fades, retime, filters, grade, mix, subtitle composition, mux, encode, and delivery validation under versioned production-correctness rules.

**Trigger and preconditions:** The accepted VideoEditProgram requires source extraction, media transformation, finishing, or export.

**Required output or state transition:** Intermediate media segments, final encoded files, command manifests, technical QA, and process receipts.

**Authority and invariants:**
- Cut boundaries receive declared audio treatment.
- Subtitle timing uses output-time mapping.
- No successful result is inferred from a command string or synthetic URI.

**Acceptance scenarios**

- **Primary success:** Given a multi-segment A-roll EDL, when FFmpeg finishing executes, then the output has no audible boundary pops, captions align after concat, and ffprobe matches the expected duration, codec, dimensions, and streams.
- **Adversarial or denial case:** Given a render command that exits without producing the declared file or whose probe differs from the plan, when validation runs, then the job fails and no production artifact is promoted.
- **Evidence required:** Executed command receipt, binary/version identity, output hash, ffprobe report, boundary checks, and caption/audio validation.

**Governing decisions:** D023, D027, D053  
**Exact source references:** SRC-EXT-017, SRC-EXT-018, SRC-LEG-011, SRC-LEG-012


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes source/time maps, EDL validation, round-trip/reload tests, runtime bindings, FFmpeg correctness, and rendered boundary evaluation. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

## 9. Risks, mitigations, and stop conditions

| Risk | Concrete consequence | Mitigation |
|---|---|---|
| Authority drift | A predecessor, external project, UI, model, or renderer is treated as current product authority. | Require exact source disposition, current authority validation, and product-boundary tests. |
| False completion | A synthetic URI, dry-run, unverified command, or model self-report is promoted as a real result. | Require actual files, hashes, independent validation, and artifact-class labels. |
| Over-broad automation | A model or agent gains tools, context, or authority beyond the current node. | Use JIT context, node-local tool grants, sandboxes, and explicit escalation. |
| Hidden mutation | Accepted meaning, source, program, or human preference changes without a versioned record. | Use immutable versions, typed commands, receipts, and selective invalidation. |

**Stop conditions**

- The behavior would create a second semantic or canonical state owner.
- A required source, authority, contract, primitive coalition, archetype, Final Script, runtime, evaluator, or human decision is unavailable or unverified.
- The implementation would treat migration evidence or an external project as current authority.
- The change would imply real output, production readiness, or certification beyond available evidence.

## 10. Planning and implementation handoff

This module is implementation-ready only after its FRs have one primary vertical Story owner, its Stories pass CBAR hardening, its candidate Tech Specs identify exact existing code and target paths, and Program Control issues a bounded Development Capsule. Until then, this module is a product-authority draft.

*This feature module belongs to the Conscious Activations Atomic Harness Pipeline PRD V1.1 source-first reconciliation package.*
