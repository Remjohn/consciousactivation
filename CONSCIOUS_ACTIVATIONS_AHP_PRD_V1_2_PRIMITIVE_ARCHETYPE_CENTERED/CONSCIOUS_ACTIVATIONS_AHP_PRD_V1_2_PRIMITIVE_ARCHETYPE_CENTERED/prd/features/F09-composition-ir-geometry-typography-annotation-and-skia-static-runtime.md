---
type: prd_feature_module
product: Conscious Activations Atomic Harness Pipeline
prd_id: CA-AHP-PRD-V1.2
feature_id: F09
title: "Composition IR, Geometry, Typography, Annotation, and Skia Static Runtime"
version: 1.2.0-draft
status: DRAFT_FOR_HUMAN_RATIFICATION
functional_requirements: "FR-049–FR-054"
---

# F09 — Composition IR, Geometry, Typography, Annotation, and Skia Static Runtime

## 1. Product claim and user outcome

**User outcome:** Static visual production uses typed geometry, measured text, and deterministic rendering rather than prompt-only layout.

Compile renderer-neutral composition intent into measurable BBOX, typography, annotation, and Skia artifacts with exact source and transformation lineage. This feature exists to convert doctrine and source evidence into behavior that can be implemented, tested, denied, replayed, and audited. It does not grant implementation, provider, model-training, publication, production, or certification authority by itself.

## 2. Product boundary and ownership

The owning product is the Atomic Harness Pipeline unless an FR explicitly assigns Interview Expression, VAE, Delegation, Studio, Program Control, or an external runtime.

The feature must preserve the current product topology. Builder supplies the immutable Atomic Harness; Pipeline executes its declared nodes; Interview Expression owns source expression preparation and approval; VAE owns visual production; Delegation owns cross-product envelopes; Studio projects state and emits typed operator commands; Program Control owns cross-product authority and release truth. External renderers and models are embodiments, not sources of meaning.

## 3. Canonical objects and state

**Cross-cutting Activative law:** Content activates when it gives the viewer a psychological role inside a tension. Content-bearing work inherits the approved archetype coalition, Primitive Coalition Contract, Final Script, Source Fidelity, Negative Space, Edge Integrity / Anti-Centroid, and Brand/Voice/Visual context when applicable.

The feature consumes current, versioned upstream records and emits typed outputs that remain linked to the active Harness, source package where applicable, Workflow Node, JIT Capsule, execution binding, evaluator, and receipt. Canonical records use stable serialization and immutable identities. A UI projection, model response, provider job, renderer workspace, or local cache cannot become accepted product state until its contract and authority gates pass.

Core invariants for this feature are:

- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

## 4. Brownfield and external capability treatment

The implementation begins from exact current and predecessor evidence. The table below identifies the most relevant source records. `REUSE` or `ADAPT` permits bounded implementation reuse after namespace, authority, license, dependency, and behavior review; it never imports historical product meaning automatically.

| Source | Disposition | Exact path or reference | Role |
|---|---|---|---|
| `SRC-CUR-014` | `REFERENCE` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md | Composition intent, feasibility, geometry and composition-context evaluation. |
| `SRC-LEG-004` | `FORK` | src/ccp_studio/contracts/composition_runtime.py | Reuse Composition IR primitives, BBOX, layers and scene relationships under current taxonomy. |
| `SRC-LEG-005` | `FORK_ADAPT` | src/ccp_studio/services/composition_runtime_service.py | Retain deterministic geometry; replace placeholder visual providers and old authority assumptions. |
| `SRC-LEG-028` | `FORK_ADAPT` | src/ccp_studio/contracts/asset_program_compilers.py | Retain typed PRETEXT/SAM3/Rough/Skia bindings; replace placeholders. |
| `SRC-LEG-029` | `FORK_ADAPT` | src/ccp_studio/services/asset_program_compiler_service.py | Compile current transformation contracts into runtime-neutral plans. |
| `SRC-LEG-033` | `RETAIN_EVIDENCE` | docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md | Existing execution-spine audit. |
| `SRC-LEG-036` | `RETAIN_AND_ADAPT` | docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md | Static visual runtime specification. |
| `SRC-EXT-008` | `REFERENCE` | https://github.com/chenglou/pretext | Deterministic multiline text measurement and layout. |
| `SRC-EXT-009` | `REFERENCE` | https://roughnotation.com/ | Typed hand-drawn annotation cue implementation reference. |
| `SRC-EXT-015` | `REFERENCE` | https://api.skia.org/ | 2D static graphics reference embodiment. |

## 5. Workflow integration

Validated upstream state → feature behavior → typed output and receipt → downstream handoff → evaluation, invalidation, and replay.

Every handoff is typed. A downstream node begins only after the producer output passes the declared contract and evidence gates. Failures are attributed to source, knowledge, retrieval, Skill, recipe, Programmed Model, tool, runtime, product, evaluator, or human-policy layers before repair or escalation.

## 6. Functional Requirements

### FR-049 — Define renderer-neutral Composition IR

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Composition IR shall represent canvas, layers, assets, text, BBOXes, hierarchy, reading order, annotations, provenance and Transformation Contract.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Define renderer-neutral Composition IR` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then composition IR shall represent canvas, layers, assets, text, BBOXes, hierarchy, reading order, annotations, provenance and Transformation Contract and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


### FR-050 — Carry BBOX plus function

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Every requested region shall carry normalized geometry and its declared syntactic/attention function.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Carry BBOX plus function` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then every requested region shall carry normalized geometry and its declared syntactic/attention function and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


### FR-051 — Activate PRETEXT measurement

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** A pinned PRETEXT adapter shall produce exact text line ranges, widths, heights and overflow evidence for the final font configuration.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Activate PRETEXT measurement` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then a pinned PRETEXT adapter shall produce exact text line ranges, widths, heights and overflow evidence for the final font configuration and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


### FR-052 — Run deterministic layout solving

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Geometrics shall resolve placement, collisions, text reservations, reserved regions and tolerances before rendering.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Run deterministic layout solving` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then geometrics shall resolve placement, collisions, text reservations, reserved regions and tolerances before rendering and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


### FR-053 — Compile typed Rough Annotation Cues

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** Rough Notation behavior shall be represented as renderer-neutral deterministic cues with target, semantic job, timing, seed/path and style.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Compile typed Rough Annotation Cues` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then rough Notation behavior shall be represented as renderer-neutral deterministic cues with target, semantic job, timing, seed/path and style and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


### FR-054 — Render actual Skia artifacts

**Lifecycle:** `PRESERVED_AND_DEEPENED`  
**Normative requirement:** The Skia runtime shall render Carousels, SuperVisuals, previews and diagnostic plates to hash-addressed artifacts rather than synthetic references.

**Trigger and preconditions:** When a validated run, planning action, or operator request requires `Render actual Skia artifacts` within feature F09.

**Required output or state transition:** A versioned, inspectable result or governed record that satisfies this requirement and can be consumed by the declared downstream owner.

**Authority and invariants:**
- BBOX includes function, not coordinates alone.
- Text is measured with final font conditions.
- Real files and hashes replace synthetic references.

**Acceptance scenarios**

- **Primary success:** Given current authority, valid inputs, and an eligible execution binding, when this behavior runs, then the Skia runtime shall render Carousels, SuperVisuals, previews and diagnostic plates to hash-addressed artifacts rather than synthetic references and the downstream consumer receives a contract-valid result.
- **Adversarial or denial case:** Given stale, ineligible, ambiguous, out-of-scope, or unverifiable inputs, when this behavior is requested, then no unauthorized side effect occurs and a typed blocker names the cause, owner, and next admissible action.
- **Evidence required:** schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse, linked to an immutable requirement receipt.

**Governing decisions:** D023, D027, D028, D029, D030, D039  
**Exact source references:** SRC-CUR-014, SRC-LEG-004, SRC-LEG-005, SRC-LEG-028, SRC-LEG-029, SRC-LEG-033, SRC-LEG-036, SRC-EXT-008, SRC-EXT-009, SRC-EXT-015


## 7. Execution, model, tool, and human responsibilities

Deterministic services own mechanically decidable facts. Programmed Models or bounded Agent Programs may propose or compile behavior only within their evidence-backed claim and node-local tool grants. Independent evaluators inspect judgment dimensions. Humans own new meaning, identity interpretation, unresolved taste, operator source authority, promotion, and publication authority where assigned. The producing model or runtime cannot accept its own output.

When the feature uses a Hunter, Analyst, Composer, or Commander role, the role is an explicit workflow responsibility. It may be implemented by code, a small model, a larger model, or a human. The role name never hides the actual actor or expand its authority.

## 8. Validation and quality gates

Validation must prove both the intended result and the process that produced it. The minimum feature evidence includes schema tests, PRETEXT measurements, collision/reading-order validation, render hashes, and visual reparse. Mechanical tests run before expensive model or visual evaluation. Judgment evaluators are calibrated to the exact category and context. Every denial names the cause, owner, and next admissible action. Every accepted mutation emits an immutable receipt and updates only dependent state.

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
