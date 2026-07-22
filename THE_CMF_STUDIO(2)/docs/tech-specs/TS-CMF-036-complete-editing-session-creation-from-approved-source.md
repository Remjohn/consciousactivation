---
tech_spec_id: "TS-CMF-036"
title: "Complete Editing Session Creation From Approved Source"
story_id: "7.1"
story_title: "Complete Editing Session Creation From Approved Source"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-1-complete-editing-session-creation-from-approved-source.md"
fr_ids:
  - "FR-CMF-07.01"
pipeline_stage: "9"
entry_object: "approved moment, route, brand context"
exit_object: "CompleteEditingSession"
validation_contract: "source approval and brand lock"
required_receipt: "editing session receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-036: Complete Editing Session Creation From Approved Source

**Status:** Ready for Development  
**Story:** `7.1 - Complete Editing Session Creation From Approved Source`  
**Implementation Boundary:** Complete Editing Session creation, approved source/route validation, locked Brand Context Version binding, workflow start, and editing session receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-1-complete-editing-session-creation-from-approved-source.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.01 authority and scene lineage requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Complete Editing Session lineage doctrine. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Complete Editing Session container and creative harness doctrine. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Context Version and downstream editing-session boundary. |
| `docs/architecture.md` | Stage 9 workflow, core objects, lock rule, and reproducibility contract. |
| `docs/cmf-studio-pipeline-map.md` | Complete Editing Session sub-workflow and Pi orchestration example. |
| `docs/migration/legacy-inventory.md` | Creative Pipeline, CMF engine refs, receipt chain, and scene intelligence sources. |

## 2. Overview

Implement `CompleteEditingSession` as the production container for one source-backed asset route. Creation is allowed only from an approved Expression Moment, an accepted route receipt, an Asset Package item when applicable, and a locked Brand Context Version. Editing cannot begin from an unsupported source, stale/unlocked brand context, or route that has not passed registry validation.

The session must preserve source expression, route, brand context, actor, status, and production readiness. It becomes the boundary that SceneSpec, CompositionJob, provider jobs, render contracts, evaluation receipts, revisions, approvals, and publishing lineage attach to.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.01 | Create Complete Editing Sessions from approved Expression Moments, route decisions, asset package items, and locked Brand Context Versions. | Creation command, source/route/brand lock validation, session schema, workflow start, and receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 9 - Complete Editing Session |
| Entry Object | approved moment, route, brand context |
| Exit Object | `CompleteEditingSession` |
| Validation Contract | source approval and brand lock |
| Required Receipt | editing session receipt |

### Legacy Intelligence Mapping

- Creative Pipeline V2 says no creative workflow is production-ready unless it runs inside a Complete Editing Session.
- Brand Genesis V3 requires every asset route to become a Complete Editing Session.
- Legacy CMF orchestration is retained as lineage and contracts, not legacy runtime couplings.

## 4. Implementation Plan

1. Add `CompleteEditingSession`, `EditingSessionSourceBinding`, `EditingSessionRouteBinding`, and `EditingSessionReceipt` contracts.
2. Add persistence for complete editing sessions, source bindings, route bindings, brand context bindings, and status events.
3. Implement `CreateCompleteEditingSessionCommand` with source approval, route receipt, asset package, brand lock, and brand scope checks.
4. Start `CompleteEditingSessionWorkflow` only after receipt persistence.
5. Expose `/api/v1/editing-sessions` query and create endpoints.
6. Surface source, route, locked Brand Context Version, and readiness in PWA/Telegram review read models.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class CompleteEditingSessionStatus(str, Enum):
    CREATED = "created"
    SCENE_SPEC_PENDING = "scene_spec_pending"
    COMPOSITION_PENDING = "composition_pending"
    RENDER_PENDING = "render_pending"
    EVALUATION_PENDING = "evaluation_pending"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class CompleteEditingSession(BaseModel):
    complete_editing_session_id: str
    brand_id: str
    source_expression_session_id: str
    source_expression_moment_id: str
    asset_route_receipt_id: str
    asset_package_item_id: str | None = None
    brand_context_version_id: str
    brand_context_version_hash: str
    registry_bundle_version: str
    created_by_user_id: str
    status: CompleteEditingSessionStatus
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateCompleteEditingSessionCommand`, `ValidateEditingSessionSourceCommand`, `ValidateLockedBrandContextForEditingCommand`, `StartCompleteEditingSessionWorkflowCommand`, `BlockEditingSessionCreationCommand` |
| Events | `CompleteEditingSessionCreated`, `EditingSessionSourceValidated`, `EditingSessionBrandContextValidated`, `CompleteEditingSessionWorkflowStarted`, `CompleteEditingSessionCreationBlocked` |
| Workflow | `CompleteEditingSessionWorkflow.stage9_create_session` |
| Receipt | `EditingSessionReceipt` with source moment ID, route receipt ID, package item ID, Brand Context Version ID/hash, registry bundle, actor, and command ID |

## 7. Backward Compatibility and Migration Fallback

Legacy CMF session concepts inform the object shape but do not become production state. If a legacy workflow references an unapproved asset, route, or brand layer, the create command fails and writes a blocked receipt.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Production speed vs. source truth | Creation requires approved Expression Moment and accepted route receipt. | SceneSpec stores session source binding. |
| Creative flexibility vs. brand lock | Brand Context Version must be locked and hashed. | Render contracts carry the same version/hash. |
| Asset package pressure vs. unsupported material | Package item is optional, but route/source approval is not. | Editing session receipt contains route and source lineage. |

## 9. Tasks

- Add contracts and persistence.
- Implement create/validate/start commands.
- Add route/source/brand lock guards.
- Add API read/write models.
- Add workflow start activity.
- Add tests for blocked and successful creation paths.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Session binds source, route, package item, locked brand context, actor, brand, status. | Session lacks Brand Context Version hash. |
| AC2 | Missing moment approval fails. | Candidate moment starts editing. |
| AC3 | Unlocked or stale brand context fails. | Draft Brand Context assets are selected. |
| AC4 | Creation writes event and receipt. | Session appears without receipt. |
| AC5 | Query displays source, route, brand context, readiness. | Review surface only shows output target. |

## 11. Dependencies

- TS-CMF-021 Brand Context locking/forking.
- TS-CMF-022 production gate to locked Brand Context.
- TS-CMF-032 approved Expression Moments.
- TS-CMF-033 route receipts.
- TS-CMF-034 package specs.

## 12. Testing Strategy


Unit tests:

- Unit tests for session schema and status.
- Command tests for approved and blocked creation.
- Brand context lock/hash validation tests.
- Route receipt and package item lineage tests.
- Workflow tests proving no SceneSpec compilation starts without editing receipt.

Integration tests:

- Workflow test from `approved moment, route, brand context` to `CompleteEditingSession` through pipeline stage `9`.
- Command Bus test proving `editing session receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for creation success, source approval failures, brand lock failures, stale context blocks, and workflow starts.
- Logs include command ID, session ID, source moment, route receipt, brand context hash, and actor.
- Recovery: create a new session from corrected source/route/context.
- Rollback: mark erroneous session rejected and preserve receipt lineage.

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
| Tech Spec ID | TS-CMF-036 |
| Story | 7.1 |
| Requirement Trace | FR-CMF-07.01 |
| Pipeline Trace | Stage 9, approved moment/route/brand context to CompleteEditingSession |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No unsupported editing start, no unlocked Brand Context use, no final-URL-only lineage |

