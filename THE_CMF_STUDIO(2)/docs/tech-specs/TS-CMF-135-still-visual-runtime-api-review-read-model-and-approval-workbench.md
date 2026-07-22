---
tech_spec_id: "TS-CMF-135"
title: "Still Visual Runtime API, Review Read Model, and Approval Workbench"
story_id: "14.3"
story_title: "Still Visual Runtime API and Approval Workbench"
epic_id: 14
epic_title: "Still Visual Composition Architecture"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-14.07"
  - "FR-CMF-14.08"
  - "FR-CMF-14.09"
pipeline_stage: "still visual review, approval, revision, and export"
entry_object: "StillVisualReviewCommand"
exit_object: "StillVisualApprovalReceipt"
validation_contract: "API route, review read model, Telegram review card, primitive blockers, revision command, waiver policy, export readiness"
required_receipt: "StillVisualApprovalReceipt"
runtime_target: "FastAPI / Python / Pydantic v2 / review workflow / approval gate / Telegram review / PWA workbench"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-135: Still Visual Runtime API, Review Read Model, and Approval Workbench

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory tech spec structure. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | CBAR mandates for blocker handling, rejection, and routing. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact, earned escalation, and review rules. |
| `THE CMF STUDIO/docs/audits/CMF_STILL_VISUAL_COMPOSITION_ARCHITECTURE_AUDIT_2026-06-25.md` | Audit finding that still visual assets need stage-review visibility, not hidden renderer artifacts. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | Parent UI architecture for operator-facing PWA. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-075-operator-composition-and-template-approval-workbench.md` | Composition approval workbench precedent. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Eval and approval workbench dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md` | Still image eval and review dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` | Canonical stage artifact review and approval policy. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md` | Parent still visual program manifest. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-134-supervisual-visual-grammar-atlas-router-and-primitive-feel-matrix.md` | SuperVisual route/read-model evidence dependency. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | Requirement that operator can reconstruct why a composition looks the way it does. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_08_Evals_and_Primitives.md` | Eval receipt and approval blocker requirements. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/compositions.py` | Existing composition API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/renders.py` | Existing render API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/review.py` | Existing review API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/review_state.py` | Existing review state API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/review_decisions.py` | Existing review decision API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/telegram_review.py` | Existing Telegram review API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/provider_jobs.py` | Existing provider job API precedent. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/approval_gate.py` | Existing approval gate API precedent. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Review state service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_decision_service.py` | Review decision service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/telegram_review_service.py` | Telegram review service owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Approval blocker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Eval receipt owner. |

## 2. Overview

Still visual composition needs an operator-readable runtime surface. Without it, the system can generate files but cannot prove why a carousel slide, SuperVisual, poll, meme, quote, or reaction still should be trusted. This spec defines the API, read model, approval flow, revision command, waiver boundary, Telegram review card, and PWA workbench requirements for `StillVisualCompositionProgram`.

The workbench must show the image preview and the reasoning behind it: guest workspace, content asset code, Brand Context version, source evidence, route decision, atlas or grammar binding, provider jobs, layer manifest, primitive coverage, doctrine evals, render hash, review blockers, and export readiness. Operators must be able to approve, reject, revise, waive eligible warnings, or request regeneration from structured commands. They must not approve a composition by visual taste alone.

This spec also prevents a product gap: still visual composition APIs cannot be scattered across carousel, single-image, renderer, provider, and review routes with no unified object. The API in this spec treats the still visual program as the public unit. Existing lower-level APIs remain useful internally, but the operator, package compiler, and Telegram review flow should interact with a single coherent endpoint family.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-135-001 | `StillVisualRuntimeAPI` | FastAPI route family for create, retrieve, route, materialize, render, evaluate, review, approve, reject, revise, waive, and export. |
| DEP-CMF-135-002 | `StillVisualReviewReadModel` | Operator-readable projection of source, route, preview, layers, provider jobs, evals, blockers, and approval state. |
| DEP-CMF-135-003 | `StillVisualReviewCommand` | Structured approve/reject/waive/revise command with actor, reason, selected blockers, and repair instruction. |
| DEP-CMF-135-004 | `StillVisualApprovalReceipt` | Immutable approval receipt for final export and package handoff. |
| DEP-CMF-135-005 | `TelegramStillVisualReviewCard` | Compact review payload for mobile approval, rejection, or revision request. |
| DEP-CMF-135-006 | `StillVisualRevisionCommand` | Structured command that targets route, text, layer, provider, primitive, render, or export repairs. |
| DEP-CMF-135-007 | `StillVisualExportReadiness` | Computed state showing whether all receipts required for export and package inclusion exist. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/api/v1/still_visuals.py` | New API router implementing routes in Section 4. |
| `src/ccp_studio/contracts/still_visuals.py` | Extend TS-CMF-133 contracts with review/read-model command objects. |
| `src/ccp_studio/services/still_visual_program_service.py` | Provide program state, read-model composition, revision, approval, and export operations. |
| `src/ccp_studio/services/review_state_service.py` | Store and retrieve still visual review state. |
| `src/ccp_studio/services/review_decision_service.py` | Persist review decisions and reviewer findings. |
| `src/ccp_studio/services/telegram_review_service.py` | Generate still visual Telegram review cards. |
| `src/ccp_studio/services/approval_gate_service.py` | Compute blockers and approval eligibility. |
| `src/ccp_studio/services/evaluation_receipt_service.py` | Attach eval summaries to the read model. |
| `src/ccp_studio/api/v1/router.py` | Register `still_visuals` route family. |

### ADR-05 Primitive Implementation

The review read model must surface primitive coverage in a way the operator can understand:

1. Which primitive role is satisfied.
2. Which exact primitive or registry item was used.
3. Which source evidence supports it.
4. Which layer, text zone, visual grammar, or scene object expresses it.
5. Whether the primitive passed, warned, or blocked approval.

The UI must not hide primitive failures behind generic red status icons. Every primitive failure requires a human-readable explanation and a repair path.

### CBAR Mandate Enforcement

| CBAR Mandate | API/Workbench Requirement |
|---|---|
| Intelligence-Gated Intercept Rule | API rejects creation and approval if source evidence or Brand Context is missing. |
| Cinematic Meaning Rule | Read model shows the meaning function and route justification before preview approval. |
| Inline Routing SLA | Route endpoint returns selected route, alternates, and blockers without requiring render. |
| Frictionless Block Rule | Workbench exposes blockers with repair commands and target stage. |
| Actionable Rejection Rule | Reject and revise commands require structured reason and must generate next action. |
| Verifiable Artifact Rule | Approval receipt includes source, route, render, eval, review, and export evidence. |
| Earned Escalation | Waivers are allowed only for declared warning-level blockers, never for source truth, primitive minimum, consent, guest scope, or deterministic render failures. |

### Technical Decisions

1. The still visual API is program-centered, not renderer-centered.
2. The review read model is a projection and must not become the source of truth.
3. Approval commands must write receipts; direct status mutation is prohibited.
4. Telegram review is a compressed surface, not a replacement for the complete read model.
5. Revision commands must target structured stage repairs instead of free-form "make it better" prompts.
6. Export is blocked until approval receipt exists.

## 4. Implementation Plan

### Step 1 - Add API Routes

Create `src/ccp_studio/api/v1/still_visuals.py`:

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/api/v1/still-visuals/programs` | Create `StillVisualCompositionProgram`. |
| `GET` | `/api/v1/still-visuals/programs/{program_id}` | Retrieve canonical program state. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/route` | Resolve family route and atlas/grammar binding. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/materialize` | Execute provider materialization plan. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/render` | Compile and render deterministic Skia scene. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/evaluate` | Run primitive, doctrine, visual grammar, source truth, and platform evals. |
| `GET` | `/api/v1/still-visuals/programs/{program_id}/review` | Retrieve `StillVisualReviewReadModel`. |
| `GET` | `/api/v1/still-visuals/programs/{program_id}/telegram-review` | Retrieve `TelegramStillVisualReviewCard`. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/approve` | Approve eligible program and emit receipt. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/reject` | Reject with structured reason and blockers. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/revise` | Create revision command for route, provider, layer, text, primitive, render, or export stage. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/waive` | Waive eligible warning only. |
| `POST` | `/api/v1/still-visuals/programs/{program_id}/export` | Export approved assets and package handoff manifest. |

### Step 2 - Build Review Read Model

`StillVisualProgramService.get_review_read_model(program_id)` must assemble:

1. Program identity and content asset code.
2. Guest workspace and Brand Context version.
3. Preview image and export variants.
4. Source evidence summaries.
5. Route decision and alternates.
6. Atlas or SuperVisual grammar binding.
7. Provider jobs and responsibility boundaries.
8. Layer/mask/typography manifest.
9. Primitive and doctrine eval status.
10. Render hash and replay command.
11. Blockers and repair commands.
12. Approval eligibility and waiver rules.

### Step 3 - Integrate Workbench UI

The PWA should render:

| Panel | Required Content |
|---|---|
| Preview | Final preview, platform variants, zoom, safe-area overlay. |
| Source | Quote, transcript moment, research/context premise, Brand Context refs. |
| Route | Format family, selected grammar, candidate scores, rejected alternatives. |
| Layers | Layer tree, mask refs, text zones, annotation zones, brand lockups. |
| Primitives | Meaning, delivery, format/material coverage and failed roles. |
| Provider Jobs | Ideogram/Qwen/SAM3/Skia job refs and responsibility boundaries. |
| Blockers | Actionable blockers, severity, repair command, waiver eligibility. |
| Approval | Approve, reject, revise, waive, export readiness. |

The UI must avoid in-app explanatory essays. It should show operational evidence and controls, not marketing copy.

### Step 4 - Add Telegram Review Card

Telegram cards must include:

1. Thumbnail preview.
2. Guest name and asset code.
3. Format code and route.
4. Top source line.
5. Primitive status summary.
6. Blocking issues count.
7. Buttons for approve, reject, revise, and open full workbench.

Telegram approval is only allowed when no hard blockers exist and the card includes all required receipt refs. If a hard blocker exists, Telegram may only reject or request revision.

### Step 5 - Add Revision Commands

Revision commands must target one of:

| Revision Target | Examples |
|---|---|
| `route` | Reroute from generic single image to `SPV-CON`; reroute quote card to carousel. |
| `source` | Request stronger quote evidence or context premise. |
| `text` | Reduce headline, fix quote accuracy, change CTA. |
| `layer` | Replace cutout, refine mask, adjust object hierarchy. |
| `provider` | Regenerate plate, rerun Qwen layered extraction, repair Flux layer. |
| `primitive` | Add missing delivery-shape or format-material primitive evidence. |
| `render` | Recompile Skia scene, fix safe area, repair typography overflow. |
| `export` | Add missing platform variant or thumbnail. |

### Step 6 - Add Waiver Policy

Hard blockers cannot be waived:

1. Missing guest workspace.
2. Missing Brand Context.
3. Missing source evidence.
4. Consent or source truth failure.
5. Primitive minimum failure.
6. Provider responsibility violation.
7. Deterministic render failure.
8. Export hash mismatch.

Warning-level blockers may be waived only with actor, reason, scope, expiration, and audit receipt.

## 5. Primary Output Schema

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

ReviewDecision = Literal["approve", "reject", "revise", "waive"]
RevisionTarget = Literal["route", "source", "text", "layer", "provider", "primitive", "render", "export"]

class StillVisualEvidenceSummary(BaseModel):
    evidence_ref: str
    evidence_type: Literal["interview_quote", "transcript", "brand_context", "context_premise", "research", "operator_note", "sequence_program"]
    display_summary: str
    source_hash: str | None = None
    timestamp_ref: str | None = None

class PrimitiveReviewStatus(BaseModel):
    role: Literal["meaning_transform", "delivery_shape", "format_material"]
    primitive_ref: str
    status: Literal["passed", "warning", "blocked"]
    evidence_refs: list[str]
    expressed_by_refs: list[str]
    explanation: str
    repair_command_ref: str | None = None

class StillVisualReviewBlocker(BaseModel):
    blocker_code: str
    severity: Literal["info", "warning", "hard_blocker"]
    stage: str
    message: str
    evidence_refs: list[str] = Field(default_factory=list)
    failed_contract_ref: str | None = None
    repair_command_ref: str | None = None
    waiver_allowed: bool = False

class StillVisualReviewReadModel(BaseModel):
    read_model_id: str
    program_id: str
    content_asset_code: str
    guest_workspace_id: str
    brand_context_version: str
    current_stage: str
    format_code: str
    resolved_family: str
    resolved_subtype: str
    preview_asset_ref: str | None = None
    export_variant_refs: list[str] = Field(default_factory=list)
    source_summaries: list[StillVisualEvidenceSummary]
    route_decision_ref: str
    route_summary: str
    atlas_or_grammar_refs: list[str]
    provider_job_refs: list[str]
    layer_manifest_ref: str | None = None
    primitive_statuses: list[PrimitiveReviewStatus]
    doctrine_eval_refs: list[str]
    render_hash: str | None = None
    replay_command_ref: str | None = None
    blockers: list[StillVisualReviewBlocker]
    approval_eligible: bool
    export_ready: bool
    updated_at: datetime

class StillVisualReviewCommand(BaseModel):
    command_id: str
    program_id: str
    decision: ReviewDecision
    actor_id: str
    actor_role: Literal["operator", "creative_director", "admin", "system"]
    reason: str
    blocker_codes: list[str] = Field(default_factory=list)
    waiver_scope: str | None = None
    created_at: datetime

class StillVisualRevisionCommand(BaseModel):
    revision_command_id: str
    program_id: str
    actor_id: str
    target: RevisionTarget
    reason: str
    instruction: str
    source_refs_to_preserve: list[str]
    blocker_codes_to_repair: list[str] = Field(default_factory=list)
    created_at: datetime

class StillVisualApprovalReceipt(BaseModel):
    receipt_id: str
    program_id: str
    content_asset_code: str
    actor_id: str
    approved_at: datetime
    review_decision_ref: str
    approval_gate_receipt_ref: str
    primitive_eval_refs: list[str]
    doctrine_eval_refs: list[str]
    source_evidence_refs: list[str]
    render_hash: str
    export_manifest_ref: str
    waiver_refs: list[str] = Field(default_factory=list)

class TelegramStillVisualReviewCard(BaseModel):
    card_id: str
    program_id: str
    content_asset_code: str
    guest_display_name: str
    format_code: str
    route_summary: str
    thumbnail_asset_ref: str
    source_line: str
    primitive_status_summary: str
    hard_blocker_count: int
    warning_count: int
    approval_eligible: bool
    workbench_url: str
    action_tokens: dict[str, str]
    created_at: datetime
```

## 6. Backward Compatibility Fallback

Existing review APIs may continue to serve generic composition reviews, but still visual production must use the new program-centered routes for approval and export. Compatibility rules:

| Existing Path | Compatibility Rule |
|---|---|
| `/api/v1/review` | May store generic review findings, but still visual approval must reference `program_id`. |
| `/api/v1/review_state` | May remain the underlying state service. Still visual read model must project from it. |
| `/api/v1/telegram_review` | May remain the transport service. Still visual cards must use `TelegramStillVisualReviewCard`. |
| Direct renderer export | Blocked unless approval receipt already exists. |
| Existing carousel preview UI | May link into new workbench by `program_id`. |
| Existing single-image preview UI | May link into new workbench by `program_id`. |

## 7. Tasks

1. Create `src/ccp_studio/api/v1/still_visuals.py`.
2. Register API router in the application route registry.
3. Extend `src/ccp_studio/contracts/still_visuals.py` with review command/read-model schemas.
4. Implement `StillVisualProgramService.get_review_read_model`.
5. Implement approve, reject, revise, waive, and export commands.
6. Integrate approval gate blocker computation.
7. Integrate review state and review decision services.
8. Integrate Telegram still visual card generation.
9. Add PWA workbench route for still visual program review.
10. Add UI panels listed in Section 4.
11. Add route and API tests for every endpoint.
12. Add e2e tests for approve, reject, revise, waiver, export, and Telegram review paths.

## 8. Acceptance Criteria

### AC135-01: API Is Program-Centered

Given a still visual asset, when an operator opens it, then the API must retrieve by `program_id` and show program state, not only a raw image URL.

### AC135-02: Review Read Model Is Complete

Given a rendered still visual, when `/review` is requested, then the read model must include source summaries, route summary, atlas/grammar refs, provider job refs, layer manifest, primitive statuses, blockers, render hash, approval eligibility, and export readiness.

### AC135-03: Approval Blocks Hard Failures

Given a hard blocker exists, when `/approve` is called, then the API must reject with `STILL_VISUAL_APPROVAL_HARD_BLOCKED` and include blocker codes.

### AC135-04: Revision Is Structured

Given a rejected program, when `/revise` is called, then the command must include a target, reason, instruction, preserved source refs, and blockers to repair. Free-form revision without target must fail with `STILL_VISUAL_REVISION_TARGET_MISSING`.

### AC135-05: Waiver Cannot Override Doctrine-Critical Failures

Given a primitive minimum, source truth, consent, guest scope, provider responsibility, or deterministic render blocker, when `/waive` is called, then the API must reject with `STILL_VISUAL_WAIVER_NOT_ALLOWED`.

### AC135-06: Telegram Card Cannot Hide Blockers

Given a program with hard blockers, when the Telegram card is generated, then the card must show blocker count and disable approve action.

### AC135-07: Export Requires Approval Receipt

Given a rendered but unapproved program, when `/export` is called, then the API must reject with `STILL_VISUAL_APPROVAL_RECEIPT_MISSING`.

### AC135-08: Read Model Explains Primitive Failure

Given a primitive failure, when the workbench loads, then the read model must show role, primitive ref, evidence refs, expressed-by refs, explanation, and repair command.

### AC135-09: Preview Is Not Source Of Truth

Given an operator approves a preview image, when the receipt is stored, then approval must reference render hash, Skia scene, source evidence, route, evals, and export manifest. The preview URL alone is insufficient.

### AC135-10: PWA Workbench Shows Export Readiness

Given all required receipts exist, when the operator opens the workbench, then export readiness must show true and include target platform variants.

## 9. Dependencies

| Dependency | Type | Status |
|---|---|---|
| TS-CMF-070 | Tech spec | Required for PWA architecture |
| TS-CMF-075 | Tech spec | Required for composition approval workbench |
| TS-CMF-092 | Tech spec | Required for eval fixtures and approval workbench |
| TS-CMF-105 | Tech spec | Required for single-image eval/review runtime |
| TS-CMF-132 | Tech spec | Required for canonical stage approval |
| TS-CMF-133 | Tech spec | Required parent manifest |
| TS-CMF-134 | Tech spec | Required for SuperVisual read-model evidence |
| `review_state_service.py` | Existing service | Required |
| `review_decision_service.py` | Existing service | Required |
| `telegram_review_service.py` | Existing service | Required |
| `approval_gate_service.py` | Existing service | Required |
| `evaluation_receipt_service.py` | Existing service | Required |

## 10. Testing Strategy

### API Tests

1. `POST /programs` creates a program and returns `program_id`.
2. `GET /programs/{id}` returns canonical state.
3. `POST /route` returns route and atlas/grammar binding.
4. `POST /materialize` rejects if route is not locked.
5. `POST /render` rejects if provider materialization is incomplete.
6. `POST /evaluate` writes primitive and doctrine eval refs.
7. `GET /review` returns complete read model.
8. `POST /approve` rejects hard blockers and succeeds only when eligible.
9. `POST /reject` writes review decision and repair path.
10. `POST /revise` writes structured revision command.
11. `POST /waive` rejects hard blockers and stores warning waiver.
12. `POST /export` rejects missing approval and succeeds with receipt.

### UI Tests

1. Workbench renders preview, source, route, layers, primitives, provider jobs, blockers, and approval panels.
2. Long quote text does not overflow source panel.
3. Primitive failure panel shows repair command.
4. Hard blockers disable approve button.
5. Warning waiver requires reason.
6. Export button appears only after approval.

### Telegram Tests

1. Telegram card shows thumbnail, asset code, guest, route, source line, primitive summary, and blocker count.
2. Approve action disabled when hard blocker count is greater than zero.
3. Revise action creates structured revision command.
4. Open workbench action includes secure program review URL.

### End-To-End Tests

Run one valid path and three invalid paths:

| Fixture | Expected Result |
|---|---|
| `supervisual_valid_approval_flow.json` | route, materialize, render, evaluate, review, approve, export. |
| `carousel_missing_primitive_flow.json` | approval blocked. |
| `quote_missing_source_flow.json` | creation or evaluation blocked. |
| `meme_warning_waiver_flow.json` | warning waiver allowed, hard blockers still blocked. |

### Audit Tests

For each approval receipt, assert that it links to source evidence, route decision, primitive evals, doctrine evals, render hash, review decision, approval gate receipt, and export manifest.
