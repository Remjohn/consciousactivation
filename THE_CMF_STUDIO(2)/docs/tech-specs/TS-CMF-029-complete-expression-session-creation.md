---
tech_spec_id: "TS-CMF-029"
title: "Complete Expression Session Creation"
story_id: "6.1"
story_title: "Complete Expression Session Creation"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-1-complete-expression-session-creation.md"
fr_ids:
  - "FR-CMF-06.01"
pipeline_stage: "5"
entry_object: "approved contracts and setup"
exit_object: "CompleteExpressionSession"
validation_contract: "consent and recording readiness"
required_receipt: "session start receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-029: Complete Expression Session Creation

**Status:** Ready for Development  
**Story:** `6.1 - Complete Expression Session Creation`  
**Implementation Boundary:** Complete Expression Session creation, recording configuration binding, consent/readiness gate, session status machine, workflow start, and session start receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-1-complete-expression-session-creation.md` | Story source, acceptance criteria, and trace metadata. |
| `docs/epics.md` | Epic 6 dependency order and FR coverage. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.01 authority and dual-layer extraction constraints. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Complete Expression Session and trial pack doctrine. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Complete Expression Session V2 schema, recording configuration, source doctrine, and quality gate. |
| `docs/architecture.md` | `CompleteExpressionSessionWorkflow`, core objects, and stage 5 contract. |
| `docs/cmf-studio-pipeline-map.md` | Stage 5 sub-workflow and source capture lineage. |
| `docs/migration/legacy-inventory.md` | V9.1, receipt chain, source doctrine, and legacy audio references. |

## 2. Overview

Implement `CompleteExpressionSession` as the upstream wrapper for the human expression event. It is not a render job and not a Complete Editing Session. It binds approved Interview Asset Contracts, consent state, recording configuration, source requirements, pre-session quality gate, brand scope, guest/client, Operator, and workflow status before capture begins.

Session start must fail closed if consent, recording configuration, approved deck, or brand scope is incomplete. A successful start writes `CompleteExpressionSessionStarted` and a session start receipt that downstream ingestion, extraction, routing, and package planning must reference.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.01 | Operators can create and manage Complete Expression Sessions with recording configuration, source artifacts, transcript revisions, interview contracts, quality gates, consent state, and session status. | Session schema, status machine, create/start commands, consent/readiness gate, and start receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 5 - Complete Expression Session |
| Entry Object | approved contracts and setup |
| Exit Object | `CompleteExpressionSession` |
| Validation Contract | consent and recording readiness |
| Required Receipt | session start receipt |

### Legacy Intelligence Mapping

- V9.1 defines every interview as a Complete Expression Session and every question as an Interview Asset Contract.
- Legacy recording and audio doctrine informs source setup but production state is greenfield Pydantic/SQLAlchemy.
- Receipt chain discipline requires every start/pause/fail status transition to be auditable.

## 4. Implementation Plan

1. Add contracts for `CompleteExpressionSession`, `RecordingConfigurationRef`, `SessionQualityGateRef`, and `SessionStartReceipt`.
2. Add SQLAlchemy tables for expression sessions, session contracts, status events, and receipt references.
3. Implement Command Bus handlers for create, start, pause, fail, resume, and close commands.
4. Validate brand scope, consent compatibility, approved Interview Deck, recording configuration, and pre-session quality gate before start.
5. Start `CompleteExpressionSessionWorkflow` only after receipt persistence succeeds.
6. Expose `/api/v1/expression-sessions` endpoints for create/query/status transitions.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ExpressionSessionStatus(str, Enum):
    DRAFT = "draft"
    READY_FOR_RECORDING = "ready_for_recording"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    INGESTION_PENDING = "ingestion_pending"
    EXTRACTION_PENDING = "extraction_pending"
    CLOSED = "closed"
    FAILED = "failed"


class RecordingConfigurationRef(BaseModel):
    recording_configuration_id: str
    session_mode: str
    master_recording_source: str
    backup_recording_source: str | None = None
    orientation: str
    quality_gate_required: bool = True


class CompleteExpressionSession(BaseModel):
    expression_session_id: str
    brand_id: str
    guest_id: str
    operator_id: str
    conversation_language: str
    system_label_language: str = "en"
    interview_deck_id: str
    interview_asset_contract_ids: list[str] = Field(min_length=1)
    consent_record_version_id: str
    recording_configuration: RecordingConfigurationRef
    pre_session_quality_gate_id: str
    status: ExpressionSessionStatus
    created_at: datetime
    started_at: datetime | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateCompleteExpressionSessionCommand`, `ValidateExpressionSessionReadinessCommand`, `StartCompleteExpressionSessionCommand`, `PauseCompleteExpressionSessionCommand`, `FailCompleteExpressionSessionCommand`, `CloseCompleteExpressionSessionCommand` |
| Events | `CompleteExpressionSessionCreated`, `ExpressionSessionReadinessValidated`, `CompleteExpressionSessionStarted`, `CompleteExpressionSessionPaused`, `CompleteExpressionSessionFailed`, `CompleteExpressionSessionClosed` |
| Workflow | `CompleteExpressionSessionWorkflow.stage5_start_session` |
| Receipt | `SessionStartReceipt` with brand, guest, consent version, deck ID, contract IDs, recording config, quality gate, and command ID |

## 7. Backward Compatibility and Migration Fallback

Legacy V9.1 schema fields guide the greenfield object shape. Direct imports from old code are forbidden. If a migrated recording protocol is incomplete, the session remains draft and cannot start.

If consent or recording readiness is blocked, the workflow writes a blocked receipt and returns actionable missing fields rather than starting a partially governed session.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast capture vs. governed source truth | Start requires consent, approved deck, recording config, and quality gate. | Ingestion records session start receipt ID. |
| Human interview vs. media job | Session object captures expression event only; editing sessions are downstream. | Complete Editing Session requires approved moment plus route receipt. |
| Brand context switching vs. source privacy | Query and mutation scope by active brand. | Cross-brand session lookup is rejected. |

## 9. Tasks

- Add contracts and persistence models.
- Implement command handlers and status transition guard.
- Add readiness validator.
- Add workflow start activity and receipt writer.
- Add PWA/Telegram read models for session state.
- Add tests for consent/readiness/brand scope blocks.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Session binds brand, guest, consent, config, contracts, and status. | Session created without approved deck. |
| AC2 | Incomplete consent/setup blocks start. | Workflow starts with missing consent version. |
| AC3 | Brand scope filters session queries. | Active Brand B can see Brand A sessions. |
| AC4 | Start writes event and receipt. | Session status changes with no receipt. |
| AC5 | Pause/fail transitions use explicit statuses. | Session status is overwritten by free text. |

## 11. Dependencies

- TS-CMF-001 Command Bus.
- TS-CMF-002 stage execution records.
- TS-CMF-008 consent records.
- TS-CMF-009 recording setup/source artifact gate.
- TS-CMF-027 Interview Asset Contract and quality gate.

## 12. Testing Strategy


Unit tests:

- Unit tests for session schema and status transitions.
- Command tests for create/start/pause/fail/close.
- Permission tests for brand-scoped query and mutation.
- Workflow tests proving no workflow starts without receipt.
- Contract tests ensuring deck/contract IDs are approved and belong to active brand.

Integration tests:

- Workflow test from `approved contracts and setup` to `CompleteExpressionSession` through pipeline stage `5`.
- Command Bus test proving `session start receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Log command ID, session ID, brand ID, consent version, recording config, and status transition.
- Metrics for readiness failures, session starts, failed sessions, and blocked cross-brand access.
- Recovery: failed session can be superseded by a new session referencing the same approved deck if consent remains valid.
- Rollback: invalid start is corrected by failing the session and creating a superseding session; receipts remain immutable.

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
| Tech Spec ID | TS-CMF-029 |
| Story | 6.1 |
| Requirement Trace | FR-CMF-06.01 |
| Pipeline Trace | Stage 5, approved contracts/setup to CompleteExpressionSession |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No clip-only workflow, no session without consent, no legacy runtime coupling |

