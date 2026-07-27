---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F26
title: "Operator Revision Compiler and Human Resolution Programming Material"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-151–FR-156"
---

# F26 — Operator Revision Compiler and Human Resolution Programming Material

## 1. Product claim and user outcome

**User outcome:** Natural-language and direct-manipulation corrections become minimal typed changes, selective reruns, and reusable evidence.

Compile operator intent into bounded tool programs, validate authority/minimality, evaluate results, and capture every meaningful decision. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

Studio captures intent; Pipeline validates and executes; Knowledge/Model systems consume eligible episodes.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- No direct UI mutation bypasses the command path.
- Prior accepted state remains until replacement passes.
- Learning is scoped and offline-promoted.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-AM-001` | `AMENDMENT_INPUT` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-AM-002` | `AMENDMENT_INPUT` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-EXT-021` | `REFERENCE_LICENSE_REVIEW` | github://openvideodev/video-editor | Multi-track timeline, drag/split/trim/snapping, interactive canvas, client-side preview/export patterns. |
| `SRC-EXT-022` | `REFERENCE_LICENSE_REVIEW` | github://lineCode/ai-video-editor | AI Copilot controlling scripts, visuals, and timeline; UI pattern only. |
| `SRC-CUR-010` | `REFERENCE` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py | Execution-free Workflow Node, edge, authority and validation contracts. |
| `SRC-CUR-019` | `REFERENCE` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md | Typed visual repair and bounded reruns. |
| `SRC-EXT-017` | `REFERENCE` | github://browser-use/video-use | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-CUR-020` | `REFERENCE` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md | CMF-OKF, Steering Recipes, hybrid retrieval and Minimum Complete Context. |

## 5. Workflow integration

Operator language or direct manipulation → ChangeRequestProgram → authority/minimality validation → selective rerun → evaluation → commit/reject → HumanResolutionEpisode.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-151 — Compile natural-language operator revisions into typed change programs

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** A Revision Compiler Programmed Model or eligible general fallback shall translate an authorized operator request, current state, target objects, Harness, JIT context, allowed tool registry, and evaluation into the smallest typed ChangeRequestProgram or an explicit clarification/escalation.

**Trigger and preconditions:** An operator submits a revision in a category Studio or review queue.

**Required output or state transition:** A structured interpretation, exact operations, preconditions, invariants, affected nodes, validation plan, confidence, and escalation state.

**Authority and invariants:**
- The compiler proposes commands; deterministic authority validation decides admission.
- Unclear requests may ask one targeted question.
- No unrestricted tool access.

**Acceptance scenarios**

- **Primary success:** Given 'let the reaction breathe half a second longer and lower the caption,' when context is sufficient, then the compiler emits exact temporal and layout operations with affected nodes.
- **Adversarial or denial case:** Given 'make it better' with multiple plausible meanings, when confidence is insufficient, then it requests clarification rather than guessing.
- **Evidence required:** Tool-call schema tests, human request benchmark, argument accuracy, over-edit rate, and interpretation receipt.

**Governing decisions:** D047, D049  
**Exact source references:** SRC-AM-001, SRC-AM-002


### FR-152 — Convert direct manipulation into the same typed command path

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Dragging, trimming, splitting, resizing, cropping, reordering, selecting a candidate, or changing a parameter in the Studio shall produce the same canonical ChangeRequestProgram and validation path as an equivalent language request.

**Trigger and preconditions:** An operator performs a direct manipulation and attempts to commit it.

**Required output or state transition:** A typed command/delta linked to before-state, target, user authority, and preview.

**Authority and invariants:**
- The UI cannot mutate accepted state directly.
- Undo and replay are command-based.
- Equivalent actions have equivalent evidence.

**Acceptance scenarios**

- **Primary success:** Given a twelve-frame clip move, when committed, then the canonical program changes through a validated move operation and the same episode schema used for text revisions.
- **Adversarial or denial case:** Given an unsupported canvas drag outside permitted geometry tolerance, when committed, then the command is rejected or converted into an amendment proposal.
- **Evidence required:** UI-to-command round-trip tests, undo/replay, before/after hashes, and HumanResolutionEpisode.

**Governing decisions:** D047, D049  
**Exact source references:** SRC-AM-001, SRC-EXT-021, SRC-EXT-022


### FR-153 — Validate revision authority, scope, and minimality before execution

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Every ChangeRequestProgram shall pass schema, current-state identity, authority, tool grant, Transformation Contract, source truth, geometry/timing, budget, and minimal-change validation before preview or execution.

**Trigger and preconditions:** A compiled or manually constructed change program is submitted.

**Required output or state transition:** An admitted dry-run/preview plan or typed denial with exact cause and next action.

**Authority and invariants:**
- Valid existing relationships are preserved.
- Out-of-scope meaning changes require the owning authority.
- Stale-state commands cannot commit.

**Acceptance scenarios**

- **Primary success:** Given a caption shift within safe bounds, when validated, then it may preview without invalidating A-roll selection.
- **Adversarial or denial case:** Given a stale command targeting a superseded composition version, when validation runs, then it is denied.
- **Evidence required:** Schema/authority tests, stale-state race tests, minimal-diff analysis, and admission receipt.

**Governing decisions:** D047, D049  
**Exact source references:** SRC-CUR-010, SRC-AM-001


### FR-154 — Rerun only affected work and independently evaluate the result

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** An accepted revision shall invalidate only directly changed objects and dependent nodes, reuse unaffected checkpoints and assets, render an appropriate preview, run required deterministic and independent evaluations, and either commit, reject, or escalate.

**Trigger and preconditions:** Revision validation succeeds.

**Required output or state transition:** A selective rerun plan, new artifacts, evaluation, commit/reject state, and dependency updates.

**Authority and invariants:**
- No full-batch rerun without dependency evidence.
- Rejected preview leaves prior accepted state intact.
- Repair limits prevent loops.

**Acceptance scenarios**

- **Primary success:** Given a SuperVisual text-size change, when executed, then only text layout, render, and dependent evaluation rerun.
- **Adversarial or denial case:** Given a local edit that causes a new wrong-reading failure, when evaluated, then it is rejected and the prior accepted version remains current.
- **Evidence required:** Checkpoint reuse report, invalidation graph, render diffs, evaluation, and state transaction receipt.

**Governing decisions:** D047, D049  
**Exact source references:** SRC-CUR-019, SRC-AM-001, SRC-EXT-017


### FR-155 — Emit a HumanResolutionEpisode for every meaningful human decision

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Every approval, rejection, candidate selection, revision, manual change, tool override, escalation resolution, taste explanation, and publication decision shall emit an immutable HumanResolutionEpisode linked to the exact before/after state, operations, evidence, authority, and applicability scope.

**Trigger and preconditions:** An authorized human decision commits.

**Required output or state transition:** A complete HumanResolutionEpisode and automatic retrieval/programming-material disposition.

**Authority and invariants:**
- No meaningful decision is stored only as UI telemetry.
- Scope defaults to narrow.
- Human rationale may remain optional but absence is explicit.

**Acceptance scenarios**

- **Primary success:** Given an operator rejects candidate A and selects B because A feels too polished, when committed, then the pair and reason are captured as scoped preference evidence.
- **Adversarial or denial case:** Given an anonymous button click with no run or authority context, when persistence runs, then it cannot become a resolution episode.
- **Evidence required:** Episode completeness validation, exact change/tool links, scope tests, and indexing receipt.

**Governing decisions:** D047  
**Exact source references:** SRC-AM-001


### FR-156 — Use human-resolution evidence for governed retrieval and Programmed Model improvement

**Lifecycle:** `NEW_V1_1`  
**Normative requirement:** Eligible HumanResolutionEpisodes shall become immediately retrievable precedents and may later produce supervised examples, preference pairs, hard negatives, repair trajectories, Steering Recipe evidence, or model-training candidates through offline operator-authorized dataset, shadow, evaluation, and promotion gates.

**Trigger and preconditions:** A HumanResolutionEpisode closes and attribution completes.

**Required output or state transition:** Retrieval index entry, candidate learning dispositions, and later promotion artifacts where authorized.

**Authority and invariants:**
- Immediate retrieval does not mean universal applicability.
- Training eligibility follows operator-declared source authority.
- No live weight mutation.

**Acceptance scenarios**

- **Primary success:** Given repeated accepted video corrections in one profile, when a future Revision Compiler is evaluated, then held-out episodes can test whether it predicts the same minimal operations.
- **Adversarial or denial case:** Given one idiosyncratic workspace preference, when global recipe promotion is requested, then evidence scope blocks it.
- **Evidence required:** Indexing tests, dataset eligibility, shadow replay, claim benchmark, and promotion receipt.

**Governing decisions:** D047  
**Exact source references:** SRC-AM-001, SRC-CUR-020


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes revision benchmark, UI-command round-trip, validation, selective rerun, HumanResolutionEpisode, and shadow/promotion. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

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
