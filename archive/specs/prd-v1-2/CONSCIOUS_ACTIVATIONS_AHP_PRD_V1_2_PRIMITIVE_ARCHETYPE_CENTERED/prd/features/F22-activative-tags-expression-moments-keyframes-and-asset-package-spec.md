---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F22
title: "Activative Tags, Expression Moments, Keyframes, and Asset Package Spec"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-127–FR-132"
---

# F22 — Activative Tags, Expression Moments, Keyframes, and Asset Package Spec

## 1. Product claim and user outcome

**User outcome:** The source becomes a compact, inspectable inventory of approved expression material, visual references, and routeable ingredients.

Separate tag provenance, pack transcript context, map shots/keyframes, govern Moment discovery, retain negatives, and compile downstream handoff. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

Interview Expression owns discovery and approval; Pipeline consumes the Asset Package Spec.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Hunters propose but do not approve.
- Every quote and moment has exact source context.
- Rejected evidence remains excluded but learnable within source authority.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-INT-002` | `ADAPT` | THE_CMF_STUDIO(2).zip::CCP V9 Interview-First Expression Engine.md | Expression capture, source truth, archetype routing, and interview-first doctrine. |
| `SRC-INT-003` | `ADAPT` | THE_CMF_STUDIO(2).zip::CCP V9.1 Expression Capture & Archetype Routing Update.md | Expression Moment and archetype-routing refinements. |
| `SRC-AM-002` | `AMENDMENT_INPUT` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-EXT-017` | `REFERENCE` | github://browser-use/video-use | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-EXT-023` | `REFERENCE` | github://SamurAIGPT/AI-Youtube-Shorts-Generator | Long-video chunking with overlap, deduplication, caching, structured JSON, and vertical crop patterns. |
| `SRC-INT-001` | `ADAPT` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-EXT-020` | `REFERENCE` | github://UVA-Computer-Vision-Lab/OmniShotCut | Shot-boundary and transition classification. |
| `SRC-AM-001` | `AMENDMENT_INPUT` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |

## 5. Workflow integration

Accepted source package → tag/phrase/shot/keyframe analysis → Hunter proposals → Analyst validation → approval/rejection → Expression Ingredient Inventory and Asset Package Spec.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-127 — Separate planned, observed, inferred, confirmed, rejected, and superseded tags

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Every source and routing tag shall declare its provenance state, evidence, confidence, authority, applicability, and lifecycle so an intended interview topic cannot be confused with an observed Expression Moment or an operator-confirmed route.

**Trigger and preconditions:** A Brief, transcript analysis, source observation, operator decision, or supersession produces a tag.

**Required output or state transition:** Typed tag records and relationships to source spans, evidence, Brief items, archetypes, and downstream jobs.

**Authority and invariants:**
- Tag states never collapse silently.
- Inference cannot outrank confirmed evidence.
- Rejected tags remain available as negative evidence.

**Acceptance scenarios**

- **Primary success:** Given a planned 'authority conflict' tag and an observed unrelated answer, when routing runs, then only observed/confirmed tags influence the job unless the operator resolves the gap.
- **Adversarial or denial case:** Given an inferred tag with no supporting source span, when it is proposed for a quote card, then eligibility fails.
- **Evidence required:** Tag-state registry tests, provenance graph, evidence links, and exclusion receipt.

**Governing decisions:** D045  
**Exact source references:** SRC-INT-002, SRC-INT-003, SRC-AM-002


### FR-128 — Use the packed phrase-level transcript as the primary language reasoning surface

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** The Pipeline shall compile a compact, speaker-aware, time-annotated phrase transcript from cached word-level data and use it as the default text reasoning surface, loading raw words or visual composites only when the current decision requires them.

**Trigger and preconditions:** Transcript alignment is accepted.

**Required output or state transition:** A versioned phrase pack with source IDs, start/end times, speaker, words, audio events, tags, and links to source evidence.

**Authority and invariants:**
- Raw word data remains canonical for timing.
- Compression cannot remove editorially meaningful fillers or events without declaration.
- Phrase packing is deterministic.

**Acceptance scenarios**

- **Primary success:** Given a one-hour interview, when a Moment Hunter runs, then it receives the compact phrase pack plus only the relevant raw words and visual evidence.
- **Adversarial or denial case:** Given phrase packing that normalizes away a hesitation used as an expression signal, when validation compares it with raw ASR, then the pack is rejected.
- **Evidence required:** Phrase-pack hash, compression coverage, source-word backreferences, and retrieval/context-size benchmark.

**Governing decisions:** D041, D053  
**Exact source references:** SRC-EXT-017, SRC-EXT-023, SRC-INT-001


### FR-129 — Build source shot maps, transitions, keyframes, and visual references

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** The source-package compiler shall detect existing shot boundaries and transitions, sample representative and expression-relevant keyframes, record camera/framing changes, and expose visual references without treating shot changes as semantic importance.

**Trigger and preconditions:** Video source media passes technical admission.

**Required output or state transition:** A shot map, transition labels, keyframe set, visual-quality notes, face/subject geometry where available, and source-time references.

**Authority and invariants:**
- Shot detection does not create Expression Moments.
- Keyframes remain linked to exact source frames.
- Model uncertainty and missed-transition risk are visible.

**Acceptance scenarios**

- **Primary success:** Given an already edited interview, when shot analysis runs, then downstream edit planning can avoid cutting across source dissolves and can retrieve representative frames.
- **Adversarial or denial case:** Given a detected shot boundary, when no meaningful expression or quote exists, then it is not automatically routed as content.
- **Evidence required:** Detection benchmark, frame hashes, source-time validation, and sampled human review.

**Governing decisions:** D041, D044, D053  
**Exact source references:** SRC-EXT-020, SRC-EXT-017, SRC-INT-001


### FR-130 — Discover and approve Anchor Hits and Expression Moments

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** A bounded Expression Moment Hunter may propose source-backed spans using transcript, audio events, keyframes, Brief context, tags, and evidence; an Analyst validates truth and completeness, and only the authorized approval path may promote an Expression Moment.

**Trigger and preconditions:** An accepted source package is ready for expression discovery.

**Required output or state transition:** Candidate Anchor Hits and Expression Moments with source spans, quotes, speakers, evidence, expression qualities, archetype opportunities, confidence, and verdicts.

**Authority and invariants:**
- The Hunter cannot approve, route, or invent unsupported quotes.
- Expression meaning remains source-backed.
- Rejected candidates remain historical.

**Acceptance scenarios**

- **Primary success:** Given a charged answer with a complete premise and reaction tail, when proposed and validated, then it may become an approved Expression Moment with exact source lineage.
- **Adversarial or denial case:** Given a catchy partial quote that reverses the speaker's meaning outside context, when the Analyst checks it, then promotion is denied.
- **Evidence required:** Candidate portfolio, source-context review, Analyst report, approval receipt, and false-positive/false-negative benchmark.

**Governing decisions:** D041, D045, D052  
**Exact source references:** SRC-INT-001, SRC-INT-002, SRC-INT-003, SRC-AM-002


### FR-131 — Preserve rejected and borderline expression evidence

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Rejected, incomplete, invalid, low-confidence, or borderline Anchor Hit and Expression Moment candidates shall be stored with reasons, responsible failure layer, and future admissibility conditions rather than discarded.

**Trigger and preconditions:** Expression candidate evaluation returns other than accepted.

**Required output or state transition:** A rejected/borderline evidence record linked to source spans, verdict dimensions, reviewer, and possible repair or re-evaluation condition.

**Authority and invariants:**
- Rejected evidence cannot enter production routing.
- Negative examples remain source authority-scoped.
- A later superseding decision is additive.

**Acceptance scenarios**

- **Primary success:** Given a powerful quote with insufficient operator source authorization for publication, when evaluated, then it remains a restricted candidate and cannot enter a content job.
- **Adversarial or denial case:** Given a rejected candidate, when retrieval searches for production-ready moments, then it is excluded but may appear as required negative evidence.
- **Evidence required:** Lifecycle and retrieval tests, rejection reasons, source authority scope, and supersession history.

**Governing decisions:** D045, D047  
**Exact source references:** SRC-INT-001, SRC-AM-001


### FR-132 — Compile an Expression Ingredient Inventory and Asset Package Spec

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Interview Expression shall compile approved quotes, evidence, Expression Moments, keyframes, voice/audio references, visual references, tags, archetype opportunities, restrictions, and lineage into an Asset Package Spec that downstream Atomic Harnesses can consume without rediscovering the source.

**Trigger and preconditions:** Expression discovery and source validation reach an approved handoff state.

**Required output or state transition:** A versioned Expression Ingredient Inventory and Asset Package Spec linked to the Canonical Interview Source Package.

**Authority and invariants:**
- The package exposes possibilities, not final derivative meaning.
- Each ingredient carries source and authority.
- Unavailable or restricted ingredients remain explicit.

**Acceptance scenarios**

- **Primary success:** Given an approved session, when the package is compiled, then a short-video and Carousel Harness can select ingredients with no loss of source-time or evidence lineage.
- **Adversarial or denial case:** Given a quote without exact words or source time, when the package is validated, then it is rejected.
- **Evidence required:** Schema validation, completeness report, ingredient/source graph, restrictions, and handoff receipt.

**Governing decisions:** D041, D044, D046  
**Exact source references:** SRC-INT-001, SRC-INT-002, SRC-INT-003, SRC-AM-002


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes tag-state tests, phrase pack, shot/keyframe map, Moment benchmark, Analyst approval, and Asset Package completeness. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

## 9. Risks, mitigations, and stop conditions

| Risk | Concrete consequence | Mitigation |
|---|---|---|
| Authority drift | A predecessor, external project, UI, model, or renderer is treated as current product authority. | Require exact source disposition, current authority validation, and product-boundary tests. |
| False completion | A synthetic URI, dry-run, unverified command, or model self-report is promoted as a real result. | Require actual files, hashes, independent validation, and artifact-class labels. |
| Over-broad automation | A model or agent gains tools, context, or authority beyond the current node. | Use JIT context, node-local tool grants, sandboxes, and explicit escalation. |
| Hidden mutation | Accepted meaning, source, program, or human preference changes without a versioned record. | Use immutable versions, typed commands, receipts, and selective invalidation. |
| Source truth loss | A derived artifact, route, quote, or cut weakens or changes the participant's actual expression. | Require exact source context, quote/voice labels, independent semantic review, and downstream lineage. |

**Stop conditions**

- The behavior would create a second semantic or canonical state owner.
- A required source, authority, contract, primitive coalition, archetype, Final Script, runtime, evaluator, or human decision is unavailable or unverified.
- The implementation would treat migration evidence or an external project as current authority.
- The change would imply real output, production readiness, or certification beyond available evidence.

## 10. Planning and implementation handoff

This module is implementation-ready only after its FRs have one primary vertical Story owner, its Stories pass CBAR hardening, its candidate Tech Specs identify exact existing code and target paths, and Program Control issues a bounded Development Capsule. Until then, this module is a product-authority draft.

*This feature module belongs to the Conscious Activations Atomic Harness Pipeline PRD V1.1 source-first reconciliation package.*
