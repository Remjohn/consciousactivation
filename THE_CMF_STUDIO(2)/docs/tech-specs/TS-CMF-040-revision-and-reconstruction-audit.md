---
tech_spec_id: "TS-CMF-040"
title: "Revision and Reconstruction Audit"
story_id: "7.5"
story_title: "Revision and Reconstruction Audit"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-5-revision-and-reconstruction-audit.md"
fr_ids:
  - "FR-CMF-07.07"
  - "FR-CMF-07.08"
pipeline_stage: "9 / 12 / 13"
entry_object: "revision request"
exit_object: "revision chain and audit view"
validation_contract: "lineage preservation"
required_receipt: "revision receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / PWA review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-040: Revision and Reconstruction Audit

**Status:** Ready for Development  
**Story:** `7.5 - Revision and Reconstruction Audit`  
**Implementation Boundary:** Revision commands, revision chain, lineage-preserving validation, reconstruction audit view, approval version binding, and revision receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-5-revision-and-reconstruction-audit.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.07 and FR-CMF-07.08 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Governed reproducibility and audit validation. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative State transitions and reproducibility doctrine. |
| `docs/architecture.md` | Stage 13 evaluation/review/revision and reconstructability requirements. |
| `docs/cmf-studio-pipeline-map.md` | Pi render example and approval/revision boundaries. |
| `docs/migration/legacy-inventory.md` | Receipt chain, CMF manifest lineage, CBAR, and failure corpus. |

## 2. Overview

Implement revision history that never loses source lineage, composition lineage, provider receipts, evaluation history, version history, or approval history. Revisions create new version records and receipts. They do not mutate final-looking artifacts in place.

The reconstruction audit view answers why a scene looks the way it does by resolving source expression, Interview Asset Contract, route, Brand Context Version, SceneSpec, CompositionJob, provider jobs, render manifests, evaluation receipts, revisions, and approvals.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.07 | Operators can request revisions without losing source lineage, composition lineage, provider receipts, evaluation history, version history, or approval history. | Revision command, version chain, lineage validator, and revision receipt. |
| FR-CMF-07.08 | Reconstruct why a scene looks the way it does from source expression, route, brand context, composition JSON, provider jobs, render manifests, and human approvals. | Reconstruction graph, audit view, lineage resolver, and approval binding. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 9 / 12 / 13 - Editing, assembly, evaluation/review |
| Entry Object | revision request |
| Exit Object | revision chain and audit view |
| Validation Contract | lineage preservation |
| Required Receipt | revision receipt |

### Legacy Intelligence Mapping

- CMF beat-fingerprint/manifest lineage informs reconstruction fields.
- CBAR requires every revision to preserve the reason, failure, and proof trail.
- Receipt chain prevents final media URL from replacing process lineage.

## 4. Implementation Plan

1. Add contracts for `RevisionRequest`, `RevisionDelta`, `RevisionChain`, `ReconstructionAuditView`, and `RevisionReceipt`.
2. Implement revision commands for SceneSpec, CompositionJob usage state, manifests, render outputs, evaluation receipts, and approval events.
3. Validate that revision deltas preserve source, route, Brand Context, composition, provider, render, evaluation, and approval references.
4. Bind final approval to exact final version and prior revision chain.
5. Expose reconstruction audit endpoint and PWA view.
6. Block revisions that drop lineage or cross brand context without approved fork.

## 5. Primary Output Schema

```python
from datetime import datetime
from pydantic import BaseModel, Field


class RevisionDelta(BaseModel):
    field_path: str
    previous_value_hash: str
    new_value_hash: str
    reason: str


class RevisionRequest(BaseModel):
    revision_request_id: str
    complete_editing_session_id: str
    requested_by_user_id: str
    reason: str
    target_object_type: str
    target_object_id: str
    deltas: list[RevisionDelta] = Field(min_length=1)
    prior_version_id: str
    created_at: datetime


class ReconstructionAuditView(BaseModel):
    complete_editing_session_id: str
    source_expression_moment_id: str
    asset_route_receipt_id: str
    brand_context_version_id: str
    scene_spec_versions: list[str]
    composition_job_ids: list[str]
    provider_job_ids: list[str]
    render_manifest_ids: list[str]
    evaluation_receipt_ids: list[str]
    approval_event_ids: list[str]
    revision_receipt_ids: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RequestSceneRevisionCommand`, `ValidateRevisionLineageCommand`, `ApplyRevisionCommand`, `ApproveFinalVersionCommand`, `BuildReconstructionAuditViewCommand`, `BlockLineageDroppingRevisionCommand` |
| Events | `RevisionRequested`, `RevisionLineageValidated`, `RevisionApplied`, `LineageDroppingRevisionBlocked`, `FinalVersionApproved`, `ReconstructionAuditViewBuilt` |
| Workflow | `ReviewWorkflow.stage13_revision_and_reconstruction` |
| Receipt | `RevisionReceipt` with prior version, new version, deltas, lineage refs, evaluator state, actor, and approval binding |

## 7. Backward Compatibility and Migration Fallback

Legacy beat-fingerprint and manifest concepts become lineage references and fixtures. A revision imported from legacy terminology must map to typed target object, delta, and receipt fields before persistence.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast revision vs. auditability | Every revision is versioned with deltas and receipt. | Final approval references final version and chain. |
| Visual repair vs. source truth | Lineage validator blocks source/route/context drops. | Reconstruction view still resolves original source. |
| Provider complexity vs. explainability | Audit view resolves provider jobs, manifests, evals, approvals. | Reviewer can inspect why scene looks as it does. |

## 9. Tasks

- Add revision and audit contracts.
- Implement revision command handlers.
- Add lineage preservation validator.
- Add reconstruction resolver and API.
- Add approval binding to final version.
- Add tests for multi-revision chain and blocked lineage drops.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Revision records reason, changed fields, prior version, actor, lineage, provider receipts, evaluation. | Revision overwrites SceneSpec silently. |
| AC2 | Audit traces all revisions to source/route/brand/provider/eval/human decision. | Final output hides prior provider job. |
| AC3 | Dropping source lineage is blocked. | Revision replaces scene source with unrelated quote. |
| AC4 | Approval references final version and prior chain. | Approval points to stale render. |
| AC5 | Reconstruction resolves source, route, brand context, composition JSON, provider jobs, manifests, approvals. | Audit view shows only media URL. |

## 11. Dependencies

- TS-CMF-036 through TS-CMF-039.
- TS-CMF-032 Expression Moment review.
- TS-CMF-038 CompositionJob lineage.
- Evaluation and approval specs from Epic 9 when generated.

## 12. Testing Strategy


Unit tests:

- Unit tests for revision delta schema and hash requirements.
- Command tests for valid/invalid revisions.
- Lineage blocker tests.
- Audit resolver tests over three revision versions.
- Approval binding tests to final version.

Integration tests:

- Workflow test from `revision request` to `revision chain and audit view` through pipeline stage `9 / 12 / 13`.
- Command Bus test proving `revision receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for revision count, blocked lineage drops, audit view usage, approval version mismatches, and reconstruction failures.
- Logs include revision receipt ID, target object, prior/new version, session ID, and actor.
- Recovery: create superseding revision that restores lineage or corrects invalid target.
- Rollback: mark revision superseded and rebuild audit view while preserving full chain.

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
| Tech Spec ID | TS-CMF-040 |
| Story | 7.5 |
| Requirement Trace | FR-CMF-07.07, FR-CMF-07.08 |
| Pipeline Trace | Stages 9 / 12 / 13, revision request to revision chain/audit view |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No final-URL-only audit, no lineage-dropping revision, no in-place mutation |

