---
tech_spec_id: "TS-CMF-051"
title: "Evidence-Rich Review Surface"
story_id: "9.2"
story_title: "Evidence-Rich Review Surface"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-2-evidence-rich-review-surface.md"
fr_ids:
  - "FR-CMF-09.02"
pipeline_stage: "13"
entry_object: "asset under review"
exit_object: "evidence-rich review state"
validation_contract: "consent/source/eval completeness"
required_receipt: "review state receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / generated TypeScript / PWA / Telegram deep links"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-051: Evidence-Rich Review Surface

**Status:** Ready for Development  
**Story:** `9.2 - Evidence-Rich Review Surface`  
**Implementation Boundary:** ReviewEvidenceState, PWA render review read model, evaluation receipt viewer, consent/source compatibility flags, revision history, brand boundary enforcement, and Telegram-to-PWA deep links.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-2-evidence-rich-review-surface.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.02 authority and evidence list. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Human approval and review safety doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Common review fields, source reference, and PWA/Telegram parity. |
| `docs/architecture.md` | Review service, evaluation receipts, approval events, and PWA/Telegram surfaces. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13 review trace and Telegram handoff context. |
| `docs/migration/legacy-inventory.md` | Brand Genesis review surfaces, CBAR, and receipt-chain references. |

## 2. Overview

The review surface is not a gallery preview. It is the evidence cockpit for human approval. It must expose preview, source quote, transcript segment, timestamps, archetype route, Brand Context Version, selected assets, render output, evaluations, revisions, and current consent state.

The PWA owns the full evidence view. Telegram may link to or summarize this view, but complex cases must deep-link to PWA. All review state is read from backend contracts and cannot cross organization or brand boundaries.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.02 | Operators can review source quote, transcript segment, archetype route, Brand Context Version, selected assets, render output, evaluation receipt, revision history, and consent state. | Review read model, evidence panels, evaluation failure expansion, consent compatibility flag, revision history, and deep-link routing. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 13 - Evaluation, review, revision, approval |
| Entry Object | asset under review |
| Exit Object | evidence-rich review state |
| Validation Contract | consent/source/eval completeness |
| Required Receipt | review state receipt |

### Legacy Intelligence Mapping

- V9.1 Evaluation Receipt doctrine becomes expandable receipt panels with exact evidence.
- Brand Genesis review surfaces inform the brand-context and identity lineage display.
- Active primitive families FBK, SAF, and PER shape feedback clarity, safety visibility, and review pacing.

## 4. Implementation Plan

1. Define `ReviewEvidenceState`, `EvidencePanel`, `EvaluationFailureView`, `RevisionHistoryItem`, `ConsentCompatibilitySnapshot`, and `ReviewStateReceipt`.
2. Implement `ReviewReadModelService` that joins render output, source quote, transcript segment, route, Brand Context Version, selected assets, evaluation receipts, revisions, and consent state.
3. Enforce organization and brand boundary filters at query and command levels.
4. Add evaluation failure expansion with exact evidence and repair recommendation.
5. Add Telegram complexity routing to PWA review deep links.
6. Write review state receipt whenever an evidence-rich review state is generated for decisioning.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class EvidencePanelType(str, Enum):
    PREVIEW = "preview"
    SOURCE_QUOTE = "source_quote"
    TRANSCRIPT = "transcript"
    ARCHETYPE_ROUTE = "archetype_route"
    BRAND_CONTEXT = "brand_context"
    SELECTED_ASSETS = "selected_assets"
    RENDER_OUTPUT = "render_output"
    EVALUATION = "evaluation"
    REVISION_HISTORY = "revision_history"
    CONSENT_STATE = "consent_state"


class EvidencePanel(BaseModel):
    panel_type: EvidencePanelType
    object_refs: list[str]
    summary: str
    completeness: Literal["complete", "missing", "conflicting"]
    blocker_codes: list[str]


class EvaluationFailureView(BaseModel):
    evaluation_receipt_id: str
    category: str
    failure_code: str
    evidence_refs: list[str]
    repair_recommendation: str


class ReviewEvidenceState(BaseModel):
    schema_version: Literal["cmf.review_evidence_state.v1"]
    review_state_id: str
    object_type: str
    object_id: str
    organization_id: str
    brand_id: str
    panels: list[EvidencePanel]
    evaluation_failures: list[EvaluationFailureView]
    consent_compatible: bool
    telegram_complexity: Literal["quick_allowed", "pwa_required"]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BuildReviewEvidenceStateCommand`, `ExpandEvaluationFailureCommand`, `ValidateReviewEvidenceCompletenessCommand`, `CreatePwaReviewDeepLinkCommand`, `RecordReviewStateReceiptCommand` |
| Events | `ReviewEvidenceStateBuilt`, `EvaluationFailureExpanded`, `ReviewEvidenceCompletenessValidated`, `PwaReviewDeepLinkCreated`, `ReviewStateReceiptRecorded` |
| Workflow | `ReviewWorkflow.stage13_build_evidence_state` |
| Receipt | `ReviewStateReceipt` with object refs, panel completeness, consent compatibility, evaluation failure IDs, revision history hash, and surface route |

## 7. Backward Compatibility and Migration Fallback

Legacy review surfaces are used as layout and evidence-depth references only. They cannot become canonical state. If a legacy surface had hidden or local-only decision flags, those flags must be converted into backend Pydantic state or discarded.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Review speed vs. evidence depth | PWA carries full evidence; Telegram quick review is allowed only when complexity permits. | Telegram route returns `pwa_required` for complex or conflicting evidence. |
| Beautiful preview vs. source truth | Preview cannot hide source, consent, route, and evaluation evidence. | ReviewStateReceipt records panel completeness. |
| Cross-brand convenience vs. tenancy safety | Review queries are brand-scoped and organization-scoped. | Tests prove no cross-brand evidence leakage. |

## 9. Tasks

- Add review evidence contracts.
- Implement review read model service.
- Add evidence panel completeness policy.
- Add evaluation failure expansion endpoint.
- Add consent compatibility snapshot.
- Add PWA review deep-link generator.
- Add generated TypeScript consumer contracts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Review page shows preview, quote, transcript, timestamps, route, brand context, assets, render, evaluations, revisions, and consent. | Reviewer sees only a final video preview. |
| AC2 | Expanded failure shows exact evidence and repair recommendation. | Failure expands to a generic "quality low" message. |
| AC3 | Revision history exposes prior versions and reasons. | Prior rejection reason is hidden after a new render. |
| AC4 | Changed consent is flagged during review. | Asset remains approval-ready after consent revocation. |
| AC5 | Complex Telegram review deep-links to PWA. | Telegram allows approval from a short preview despite conflicting evidence. |

## 11. Dependencies

- TS-CMF-007 PWA and Telegram state parity.
- TS-CMF-012 consent and source review surface.
- TS-CMF-021 Brand Context locking.
- TS-CMF-040 revision and reconstruction audit.
- TS-CMF-050 evaluation receipt generation.

## 12. Testing Strategy


Unit tests:

- Unit tests for panel completeness and consent compatibility.
- Integration tests for review read model joins.
- Authorization tests for brand and organization boundaries.
- UI contract tests for generated TypeScript models.
- Telegram deep-link tests for complexity routing.

Integration tests:

- Workflow test from `asset under review` to `evidence-rich review state` through pipeline stage `13`.
- Command Bus test proving `review state receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for review state builds, missing panels, conflict flags, failure expansions, and PWA deep links.
- Logs include review state ID, object ID, organization ID, brand ID, panel completeness, and consent compatibility.
- Recovery rebuilds review state from canonical objects.
- Rollback invalidates cached review states when upstream render, consent, evaluation, or revision objects change.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-051 |
| Story | 9.2 |
| Requirement Trace | FR-CMF-09.02 |
| Pipeline Trace | Stage 13, asset under review to evidence-rich review state |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No preview-only approval, no cross-brand evidence leak, no Telegram shortcut for complex evidence |
