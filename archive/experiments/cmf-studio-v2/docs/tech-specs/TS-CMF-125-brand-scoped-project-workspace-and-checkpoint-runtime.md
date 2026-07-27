---
tech_spec_id: "TS-CMF-125"
title: "Brand-Scoped Project Workspace and Checkpoint Runtime"
story_id: "13.6"
story_title: "Brand-Scoped Project Workspace and Checkpoint Runtime"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.06"
pipeline_stage: "workspace, artifacts, checkpointing, and recovery"
entry_object: "ProductionWorkspaceCreateCommand"
exit_object: "WorkspaceCheckpointReceipt"
validation_contract: "tenant isolation, brand scope, guest/source/session binding, artifact classes, checkpoint state, receipt chain"
required_receipt: "WorkspaceCheckpointReceipt"
runtime_target: "Python / Pydantic v2 / workspace service / object storage / workflow recovery / Operations Board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-125: Brand-Scoped Project Workspace and Checkpoint Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 mandates for recovery, routing, and rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact mandate. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.06. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md` | Existing orchestration record dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Brand workspace lifecycle dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-007-pwa-and-telegram-state-parity.md` | UI state parity precedent. |
| `THE CMF STUDIO/src/ccp_studio/services/workspace_service.py` | Existing workspace owner. |
| `THE CMF STUDIO/src/ccp_studio/services/workflow_recovery_service.py` | Existing recovery and resume owner. |
| `THE CMF STUDIO/src/ccp_studio/services/orchestration.py` | Existing run owner. |
| `THE CMF STUDIO/src/ccp_studio/repositories/brand_workspaces.py` | Brand workspace persistence. |
| `THE CMF STUDIO/src/ccp_studio/repositories/workflow_recovery.py` | Recovery persistence. |
| `OpenMontage docs/ARCHITECTURE.md` | Reference pattern for project folder structure and checkpoints. |

## 2. Overview

CMF needs a project workspace and checkpoint runtime that gives operators the practical resumability of OpenMontage without adopting loose local folders as production truth. Every production run must have a deterministic brand-scoped workspace rooted in organization, brand, guest, source artifact, session, asset package, pipeline run, and manifest snapshot IDs.

The workspace separates canonical JSON artifacts, source media, provider raw outputs, generated assets, audio, subtitles, render manifests, QA reports, final deliverables, and quarantine evidence. Checkpoints persist each stage state as `pending`, `in_progress`, `awaiting_human`, `completed`, `failed`, `quarantined`, or `superseded`, with object hashes and receipt refs.

Unlike OpenMontage's gitignored local project folder convention, CMF persists durable workspace metadata in Postgres/repositories and object storage, while local working directories are temporary execution caches. Operators should never confuse one guest or brand with another, and workflow recovery must never rerun paid provider work unless retry policy and budget governance approve it.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-125-001 | `ProductionWorkspace` | Brand-scoped workspace record with org, brand, guest, source, session, package, pipeline run, and manifest refs. |
| DEP-CMF-125-002 | `WorkspaceArtifactSlot` | Typed artifact lane for canonical JSON, source media, provider raw output, generated assets, audio, subtitles, QA, renders, and deliverables. |
| DEP-CMF-125-003 | `WorkspaceCheckpoint` | Stage checkpoint with status, artifact hashes, receipt refs, retry policy, and resume cursor. |
| DEP-CMF-125-004 | `WorkspaceResumeDecision` | Decision object proving whether a stage can resume, rerun, quarantine, or require human approval. |
| DEP-CMF-125-005 | `WorkspaceCheckpointReceipt` | Receipt proving checkpoint mutation and artifact hash state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/workspace_lifecycle.py` | Add production workspace, artifact slot, checkpoint, resume decision, and receipt contracts. |
| `src/ccp_studio/services/workspace_service.py` | Create deterministic workspace records and object-storage paths. |
| `src/ccp_studio/services/workflow_recovery_service.py` | Resolve latest valid checkpoint and replay/resume decisions. |
| `src/ccp_studio/services/orchestration.py` | Bind pipeline runs to workspace ID and checkpoint state. |
| `src/ccp_studio/repositories/brand_workspaces.py` | Persist workspace metadata and brand/guest scope. |
| `src/ccp_studio/repositories/workflow_recovery.py` | Persist checkpoints, retry state, quarantine state, and resume decisions. |
| `src/ccp_studio/api/v1/workflow_recovery.py` | Add workspace checkpoint and resume endpoints. |
| `POST /api/v1/workflow-recovery/workspaces`, `POST /api/v1/workflow-recovery/workspaces/{workspace_id}/checkpoints`, `POST /api/v1/workflow-recovery/workspaces/{workspace_id}/resume`, `GET /api/v1/workflow-recovery/workspaces/{workspace_id}` | Exact API routes for workspace creation, checkpointing, resume, and inspection. |
| Postgres tables: `brand_project_workspaces`, `workspace_checkpoints`, `workspace_artifact_slots`, `workflow_resume_decisions`, `workspace_quarantine_events` | Durable storage for brand-scoped workspaces, artifacts, checkpoints, and recovery decisions. |
| `src/ccp_studio/services/operations_board_service.py` | Surface workspace stage status, blockers, and artifact links. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-SOC-001` | Verifiable Artifact | Every checkpoint and artifact slot is hash-backed and receipt-linked. |
| `EXP-FBK-001` | Actionable Rejection | Failed checkpoints state exact artifact, stage, and repair action. |
| `EXP-PRG-001` | Inline Routing SLA | Resume uses the active workspace and latest valid checkpoint. |
| `EXP-FRC-006` | Frictionless Block | Recovery blocks unsafe reruns but gives clear resume/quarantine/repair route. |
| `EXP-PER-003` | Intelligence-Gated Intercept | Workspace scope must include brand, guest, source, and session context. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M01: Intelligence-Gated Intercept Rule | Phase 4 Story 1.1 | `EXP-PER-003` | Workspace creation requires org, brand, guest/source/session, and pipeline run scope. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Stage resume resolves latest checkpoint and manifest stage. |
| Phase4-M04: Frictionless Block Rule | Phase 4 Story 4.1 | `EXP-FRC-006` | Unsafe rerun, cross-brand access, or missing artifact hash returns a repair route. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Failed checkpoints include exact stage, artifact, receipt, and next command. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Checkpoint receipt preserves artifact hashes and state transition. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Durable state lives in repositories/object storage, not local folders. | Avoids hidden state and cross-brand confusion. |
| Workspace path is deterministic but collision-safe. | Makes artifact retrieval predictable while preserving tenant isolation. |
| Provider raw output and final deliverable slots are separate. | Keeps provenance distinct from approved output. |
| Resume decisions are explicit. | Prevents accidental paid reruns and unsafe partial recovery. |

## 4. Implementation Plan

1. Extend workspace contracts with production workspace, artifact slots, checkpoints, resume decisions, and receipts.
2. Implement deterministic workspace key generation from org, brand, guest/source, session, package, pipeline run, and manifest snapshot IDs.
3. Add artifact slot taxonomy and object-storage path rules.
4. Add checkpoint mutation functions for stage start, artifact write, awaiting human, complete, fail, quarantine, supersede, and resume.
5. Integrate checkpoint creation with orchestration run stage transitions.
6. Add resume decision logic that checks artifact hashes, receipts, retry policy, provider cost, and approval requirements.
7. Add Operations Board workspace status read model.
8. Add API endpoints for workspace inspection, checkpoint mutation, and resume decision.
9. Add tests for cross-brand isolation, checkpoint replay, paid rerun prevention, quarantine, and artifact hash validation.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field


class WorkspaceArtifactSlot(BaseModel):
    schema_version: Literal["cmf.workspace_artifact_slot.v1"]
    slot_id: str
    artifact_class: Literal[
        "canonical_json", "source_media", "provider_raw_output",
        "generated_asset", "audio", "subtitles", "render_manifest",
        "qa_report", "final_deliverable", "quarantine_evidence"
    ]
    object_uri: str
    sha256: str
    receipt_refs: list[str] = Field(default_factory=list)


class WorkspaceCheckpoint(BaseModel):
    schema_version: Literal["cmf.workspace_checkpoint.v1"]
    checkpoint_id: str
    workspace_id: str
    pipeline_run_id: str
    manifest_snapshot_id: str
    stage_id: str
    status: Literal["pending", "in_progress", "awaiting_human", "completed", "failed", "quarantined", "superseded"]
    artifact_slots: list[WorkspaceArtifactSlot] = Field(default_factory=list)
    retry_policy_ref: str | None = None
    receipt_refs: list[str] = Field(default_factory=list)


class WorkspaceCheckpointReceipt(BaseModel):
    schema_version: Literal["cmf.workspace_checkpoint_receipt.v1"]
    receipt_id: str
    checkpoint_id: str
    previous_status: str | None
    new_status: str
    artifact_hashes: dict[str, str]
    mutation_reason: str
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing brand workspace lifecycle behavior remains valid. Legacy runs without production workspaces can be read as historical records, but new production runs must create a production workspace before provider work, source processing, render jobs, QA, or final approval.

If workspace creation fails, orchestration blocks before expensive or irreversible work starts. If checkpoint lookup fails during resume, the workflow must not rerun provider jobs by default; it returns a recovery blocker requiring operator decision.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T125-01 | Contracts | Add production workspace, artifact slot, checkpoint, resume decision, receipt. |
| T125-02 | Services | Implement deterministic workspace creation and artifact slot assignment. |
| T125-03 | Recovery | Add resume/rerun/quarantine decision logic. |
| T125-04 | Orchestration | Bind stage transitions to checkpoints. |
| T125-05 | API | Add workspace inspect, checkpoint mutate, and resume endpoints. |
| T125-06 | Operations Board | Add workspace and checkpoint read model. |
| T125-07 | Tests | Add isolation, replay, rerun prevention, quarantine, and hash tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC125-01 | Production workspace is scoped to org, brand, guest/source, session, package, pipeline run, and manifest snapshot. | Two guests share the same render workspace. | Phase4-M01; scope isolation test. |
| AC125-02 | Every checkpoint mutation writes receipt with artifact hashes. | Stage marks completed with no artifact hash or receipt. | Phase5-M01; checkpoint receipt test. |
| AC125-03 | Resume uses latest valid checkpoint and blocks unsafe paid reruns. | Failed image job reruns automatically without budget approval. | Phase4-M04; resume policy test. |
| AC125-04 | Artifact slots separate raw provider outputs from approved deliverables. | Raw ComfyUI output appears as final deliverable. | Phase4-M05; artifact class test. |
| AC125-05 | Cross-brand access is blocked. | Operator in Brand A opens Brand B workspace link. | Phase4-M01; access boundary test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-002` | Orchestration records | Stage records feed checkpoints. |
| `TS-CMF-004` | Brand workspace lifecycle | Production workspace extends brand workspace scope. |
| `TS-CMF-121` | Manifest registry | Workspace stages reference manifest snapshots. |
| `workspace_service.py` | Existing service | Extend. |
| `workflow_recovery_service.py` | Existing service | Extend. |
| `operations_board_service.py` | Existing service | Surface status. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Workspace, artifact slot, checkpoint, resume decision, and receipt validate. |
| Isolation tests | Cross-brand, cross-guest, and cross-session artifact access is blocked. |
| Checkpoint tests | Stage status transitions write receipts and preserve artifact hashes. |
| Resume tests | Latest valid checkpoint is selected; unsafe reruns block. |
| Quarantine tests | Failed or suspect artifacts move to quarantine and cannot be final deliverables. |
| Read-model tests | Operations Board receives workspace state, blockers, and artifact links. |
