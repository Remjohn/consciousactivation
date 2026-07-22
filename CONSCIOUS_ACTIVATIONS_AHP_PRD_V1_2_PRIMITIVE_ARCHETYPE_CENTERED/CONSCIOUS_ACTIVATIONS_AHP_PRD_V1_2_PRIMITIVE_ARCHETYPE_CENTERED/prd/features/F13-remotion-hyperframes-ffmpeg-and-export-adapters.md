---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F13
title: "Remotion, HyperFrames, FFmpeg, and Export Adapters"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-073–FR-078"
---

# F13 — Remotion, HyperFrames, FFmpeg, and Export Adapters

## 1. Product claim and user outcome

**User outcome:** Temporal programs are realized by category-appropriate engines with common receipts and no semantic authority leakage.

Compile approved renderer-neutral programs into exact runtime workspaces, outputs, QA, and delivery packages. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

The owning product is the Atomic Harness Pipeline unless an FR explicitly assigns Interview Expression, VAE, Delegation, Studio, Program Control, or an external runtime.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-LEG-013` | `FORK` | src/ccp_studio/contracts/deterministic_rendering.py | Renderer-neutral render requests/results. |
| `SRC-LEG-014` | `FORK_ADAPT` | src/ccp_studio/services/deterministic_rendering_service.py | Separate technical rendering from semantic acceptance. |
| `SRC-LEG-015` | `FORK_SPLIT` | src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py | Split combined adapter into independent runtime packages. |
| `SRC-LEG-016` | `FORK_ADAPT` | src/ccp_studio/services/remotion_render_adapter_service.py | Activate against a verified Remotion composer project. |
| `SRC-LEG-017` | `FORK_ACTIVATE` | src/ccp_studio/services/ffmpeg_finish_adapter_service.py | First-class media editing and post-production. |
| `SRC-LEG-018` | `REPLACE_WITH_PIPELINE_BINDING` | src/ccp_studio/services/remotion_ffmpeg_render_orchestrator_service.py | The Pipeline binding, not legacy orchestration, chooses an authorized runtime. |
| `SRC-EXT-007` | `REFERENCE` | https://github.com/calesthio/OpenMontage | Agentic production/editing reference; AGPL review required before code reuse. |
| `SRC-EXT-012` | `REFERENCE` | https://www.remotion.dev/ | React-based programmatic temporal composition reference. |
| `SRC-EXT-013` | `REFERENCE` | https://hyperframes.video/docs | HTML/CSS/GSAP deterministic temporal composition reference. |
| `SRC-EXT-014` | `REFERENCE` | https://www.ffmpeg.org/documentation.html | Media processing, editing, finishing and technical inspection. |

## 5. Workflow integration

Validated upstream state → feature behavior → typed output and receipt → downstream handoff → evaluation, invalidation, and replay.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-073 — Activate Remotion adapter

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The adapter shall render verified React/frame compositions, reusable scene components, data motion, captions and presenter paths.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Activate Remotion adapter` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the adapter shall render verified React/frame compositions, reusable scene components, data motion, captions and presenter paths and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


### FR-074 — Implement HyperFrames adapter

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The adapter shall compile HTML/CSS/GSAP workspaces, run lint/validate/render and support kinetic typography, motion graphics, website-to-video and SVG animation.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Implement HyperFrames adapter` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the adapter shall compile HTML/CSS/GSAP workspaces, run lint/validate/render and support kinetic typography, motion graphics, website-to-video and SVG animation and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


### FR-075 — Enforce runtime selection lineage

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The final receipt shall prove the runtime used matches the authorized binding or an explicit superseding decision.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Enforce runtime selection lineage` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the final receipt shall prove the runtime used matches the authorized binding or an explicit superseding decision and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


### FR-076 — Translate from renderer-neutral plans

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Renderer adapters shall consume typed Composition/Timeline plans instead of reading Skills or inventing visual strategy.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Translate from renderer-neutral plans` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then renderer adapters shall consume typed Composition/Timeline plans instead of reading Skills or inventing visual strategy and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


### FR-077 — Perform technical post-render validation

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Rendered outputs shall pass ffprobe, frame sampling, audio checks, transcript/caption checks and delivery-profile validation.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Perform technical post-render validation` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then rendered outputs shall pass ffprobe, frame sampling, audio checks, transcript/caption checks and delivery-profile validation and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


### FR-078 — Package final delivery artifacts

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Export shall emit artifact hashes, codec/container profile, manifests, previews, logs and technical QA receipts.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Package final delivery artifacts` within feature F13.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- Adapters do not read complete doctrine or choose strategy.
- No silent runtime substitution.
- Actual output and process are verified.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then export shall emit artifact hashes, codec/container profile, manifests, previews, logs and technical QA receipts and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D035  
**Exact source references:** SRC-LEG-013, SRC-LEG-014, SRC-LEG-015, SRC-LEG-016, SRC-LEG-017, SRC-LEG-018, SRC-EXT-007, SRC-EXT-012, SRC-EXT-013, SRC-EXT-014


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes runtime integration tests, version/fingerprint receipts, real renders, ffprobe/frame/audio/caption QA, and export manifests. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

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
