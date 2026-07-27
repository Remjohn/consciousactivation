---
tech_spec_id: "TS-CMF-009"
title: "Recording Setup and Source Artifact Gate"
story_id: "2.2"
story_title: "Recording Setup and Source Artifact Gate"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-2-2-recording-setup-and-source-artifact-gate.md"
fr_ids:
  - "FR-CMF-02.02"
  - "FR-CMF-02.04"
pipeline_stage: "1 / 5"
entry_object: "recording setup"
exit_object: "SourceArtifactManifest"
validation_contract: "source quality and provenance"
required_receipt: "source intake receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / object storage / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-009: Recording Setup and Source Artifact Gate

**Status:** Ready for Development  
**Story:** `2.2 - Recording Setup and Source Artifact Gate`  
**Implementation Boundary:** Recording configuration, source artifact manifest, source quality gate, provenance storage, source intake receipt, and Complete Expression Session pre-start status.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for interview-first capture, source truth, and voice/audio quality risks. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-02.02 and FR-CMF-02.04 source authority. |
| `docs/architecture.md` | Architecture source for source artifacts, object storage paths, immutable source uploads, and complete expression session workflow. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1 and Stage 5 trace for consent/source intake and recording. |
| `docs/migration/legacy-inventory.md` | Legacy audio engine and source-separation references as read-only migration context. |
| `docs/stories/story-2-2-recording-setup-and-source-artifact-gate.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-008-versioned-consent-records.md` | Consent dependency. |

## 2. Overview

### Problem Statement

The entire CMF chain depends on source artifacts that can be trusted. If the master recording is missing, a compressed platform file is silently promoted, or upload provenance is ambiguous, downstream extraction, Voice-DNA Boost eligibility, transcript alignment, render lineage, approval, and memory become unstable.

### Solution

Implement a recording setup and source artifact gate before a Complete Expression Session starts. Operators must declare expected master source, backup route, platform source, upload method, safety expectations, and quality requirements. Accepted source artifacts are immutable and stored with content hash, source hash, brand ID, session ID, retention policy, provenance, and URI. Missing or poor-quality source blocks session start unless an explicit approved exception receipt exists.

### Scope

In scope:

- `RecordingConfiguration`, `RecordingArtifact`, `SourceArtifact`, `SourceArtifactManifest`, `SourceQualityReport`, and `SourceIntakeReceipt`.
- Pre-start source validation for Complete Expression Session.
- Object storage path policy for `brands/{brand_id}/source/`.
- Quality failure categories and recovery actions.
- Explicit exception receipts when production proceeds without the expected master source.

Out of scope:

- Live recording tool implementation.
- Transcript provider implementation.
- Audio restoration execution. This spec only classifies source quality for later workflows.
- Timeline editing.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-02.02 | Operators configure and confirm recording setup, source, upload, safety, and quality before session start. | `RecordingConfiguration`, `SourceQualityReport`, Complete Expression Session pre-start validation, and source intake receipt. |
| FR-CMF-02.04 | System preserves source artifacts, transcript revisions, timestamps, claim references, and file provenance. | `SourceArtifactManifest`, object storage hashes, immutable URI, provenance fields, and downstream source refs. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace, commercial, consent, and source intake`; `5 - Complete Expression Session` |
| Entry Object | Recording setup |
| Exit Object | `SourceArtifactManifest` |
| Allowed Actors / Services | Operator, SourceIngestionWorkflow, ConsentPolicyService, object storage service |
| Validation Contract | Source quality, master/backup expectations, provenance, consent compatibility, retention policy |
| Required Receipt | Source intake receipt |
| Forbidden Shortcut | Promoting compressed meeting-platform file as canonical master without review, mutable source artifact, missing content/source hash |

### Legacy Intelligence Mapping

Legacy audio engine references are used for source separation and audio quality expectations, especially preserving the difference between interviewer voice and guest performance. They are not imported directly. Source artifact contracts are Python/Pydantic first, and object storage is governed by brand-scoped immutable paths.

Target modules:

- `ccp_studio.contracts.source`
- `ccp_studio.contracts.recording`
- `ccp_studio.services.source_ingestion`
- `ccp_studio.services.source_quality`
- `ccp_studio.repositories.source_artifacts`
- `ccp_studio.workflows.source_ingestion`
- `ccp_studio.api.v1.source`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `RecordingConfiguration` | Expected master, backup, platform, upload route, safety, and quality requirements. |
| `RecordingArtifact` | Uploaded or referenced raw source file with provenance. |
| `SourceArtifact` | Accepted immutable source artifact with hashes and retention policy. |
| `SourceArtifactManifest` | Session-level source truth manifest for downstream workflows. |
| `SourceQualityReport` | Quality status, failure category, thresholds, and recovery action. |
| `SourceIntakeReceipt` | Receipt proving source gate outcome. |

## 4. Implementation Plan

### Workstream A: Contracts

Define recording, source artifact, source manifest, quality report, and source receipt contracts.

### Workstream B: Object Storage

Store accepted source artifacts under `brands/{brand_id}/source/{session_id}/...` with content hash, source hash, immutable URI, and retention policy.

### Workstream C: Source Quality Gate

Implement quality validation for missing master source, compressed platform source, unsafe upload type, missing backup, low audio/video quality, unknown provenance, and hash mismatch.

### Workstream D: Complete Expression Session Pre-Start

Block session start until consent and source requirements pass, or an approved exception receipt exists.

### Workstream E: Recovery Actions

Return exact failure categories and recommended recovery actions to Operator surfaces.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SourceArtifactKind(str, Enum):
    master_recording = "master_recording"
    backup_recording = "backup_recording"
    platform_recording = "platform_recording"
    uploaded_reference = "uploaded_reference"


class SourceQualityStatus(str, Enum):
    accepted = "accepted"
    blocked = "blocked"
    exception_required = "exception_required"
    review_required = "review_required"


class RecordingConfiguration(BaseModel):
    schema_version: Literal["cmf.recording_configuration.v1"]
    recording_configuration_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    expected_master_source: str
    backup_route: str
    platform_source: str | None = None
    upload_method: str
    quality_requirements: list[str]
    created_at: datetime


class SourceArtifact(BaseModel):
    schema_version: Literal["cmf.source_artifact.v1"]
    source_artifact_id: UUID
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    kind: SourceArtifactKind
    content_hash: str
    source_hash: str
    retention_policy_id: UUID
    provenance: str
    immutable_uri: str
    accepted_at: datetime | None = None


class SourceQualityReport(BaseModel):
    schema_version: Literal["cmf.source_quality_report.v1"]
    source_quality_report_id: UUID
    source_artifact_id: UUID
    status: SourceQualityStatus
    failure_category: str | None = None
    recovery_action: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `SubmitRecordingConfigurationCommand`, `UploadSourceArtifactCommand`, `EvaluateSourceQualityCommand`, `AcceptSourceArtifactCommand`, `ApproveSourceExceptionCommand`, `StartCompleteExpressionSessionCommand` |
| Events | `RecordingConfigurationSubmitted`, `SourceArtifactUploaded`, `SourceQualityEvaluated`, `SourceArtifactAccepted`, `SourceExceptionApproved`, `SourceArtifactManifestCreated` |
| Workflows | `SourceIngestionWorkflow`, Complete Expression Session pre-start workflow |
| Receipts | `SourceIntakeReceipt`, `SourceExceptionReceipt`, `AuditReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy audio/source modules become quality heuristics and fixtures. If a migrated source file lacks content hash, source hash, brand ID, session ID, or provenance, it cannot become canonical until repaired.

Fallback behavior:

- Missing master source returns `MASTER_SOURCE_REQUIRED`.
- Compressed platform source without review returns `CANONICAL_SOURCE_REVIEW_REQUIRED`.
- Hash mismatch returns `SOURCE_HASH_MISMATCH`.
- Missing retention policy returns `RETENTION_POLICY_REQUIRED`.
- Missing consent returns `CONSENT_RECORD_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Operators need to start sessions quickly; downstream truth requires source files to be explicit, hashed, and provenance-backed. |
| UX / Ops Failure Scenario | Extraction relies on a low-quality meeting export that was never meant to be canonical, making quote timing and voice repair unreliable. |
| Resolution Demand | Source truth takes precedence. Session start is blocked unless source expectations pass or an exception receipt is explicitly approved. |
| Downstream Proof | Tests must prove missing master source blocks start, accepted artifacts are immutable, hashes are stored, and quality failures show recovery actions. |

## 9. Tasks

- Define recording and source contracts.
- Add source artifact and manifest migrations.
- Implement source ingestion workflow.
- Implement source quality evaluator.
- Integrate session pre-start gate.
- Implement object storage path and hash policy.
- Add failure categories and recovery actions.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Recording setup records expected master, backup route, platform source, upload method, safety, and quality requirements. | Session starts with no declared master recording. |
| AC2 | Missing master source blocks session or requires explicit approved exception receipt. | Operator begins session with only a compressed call export. |
| AC3 | Compressed platform file cannot become canonical without review when master is required. | Platform file is marked as master automatically. |
| AC4 | Accepted source stores content hash, source hash, brand ID, session ID, retention policy, provenance, and immutable URI. | Source artifact lacks source hash. |
| AC5 | Quality failure shows exact category and recovery action. | UI says "upload failed" without source truth reason. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-004 Workspace lifecycle
- TS-CMF-008 Consent records
- Complete Expression Session workflow from later specs

External:

- FastAPI
- Pydantic v2
- Object storage
- PostgreSQL

## 12. Testing Strategy

Unit tests:

- Recording configuration validation.
- Source artifact hash requirements.
- Quality report categories.
- Source manifest schema.

Integration tests:

- Submit setup, upload master, accept source, create manifest.
- Missing master blocks session start.
- Platform-only source requires review.
- Accepted artifact is immutable.

Safety tests:

- Object storage path must include brand ID and session ID.
- Source artifact cannot be modified after accepted.
- Session cannot start without consent compatibility.

## 13. Observability, Recovery, and Rollback

- Logs include `source_artifact_id`, `session_id`, `brand_id`, `content_hash`, `source_hash`, and quality status.
- Metrics track source blocks, exception receipts, quality categories, and successful manifests.
- Recovery can re-evaluate source quality from immutable files.
- Rollback marks artifact superseded by a new artifact; it does not mutate accepted source.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-02.02, FR-CMF-02.04 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Audio/source references mapped to quality heuristics and fixtures |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python source gate; Pi cannot start session without receipt |
| TypeScript Boundary | Surfaces display generated source status only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

