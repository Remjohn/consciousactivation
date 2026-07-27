---
tech_spec_id: "TS-CMF-030"
title: "Source Ingestion, Transcript Alignment, and Provenance"
story_id: "6.2"
story_title: "Source Ingestion, Transcript Alignment, and Provenance"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-2-source-ingestion-transcript-alignment-and-provenance.md"
fr_ids:
  - "FR-CMF-06.02"
pipeline_stage: "5"
entry_object: "recordings/transcripts"
exit_object: "aligned source/transcript artifacts"
validation_contract: "source integrity and transcript alignment"
required_receipt: "ingestion receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / object storage / transcript provider adapters"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-030: Source Ingestion, Transcript Alignment, and Provenance

**Status:** Ready for Development  
**Story:** `6.2 - Source Ingestion, Transcript Alignment, and Provenance`  
**Implementation Boundary:** Recording artifact ingestion, immutable object storage, transcript revision alignment, source voice/interviewer voice distinction, upload provenance, and ingestion receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-2-source-ingestion-transcript-alignment-and-provenance.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.02 authority and source artifact lineage rules. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Recording source doctrine and remote/in-person recording configuration. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Source lineage and dual extraction doctrine. |
| `docs/architecture.md` | Source artifacts, transcript revisions, provider capability, and append-only rules. |
| `docs/cmf-studio-pipeline-map.md` | Stage 5 capture and transcript alignment sub-workflow. |
| `docs/migration/legacy-inventory.md` | Legacy audio engine, Demucs separation reference, source doctrine, and receipt chain. |
| `docs/stories/story-6-2-source-ingestion-transcript-alignment-and-provenance.md` | Handoff metadata and pipeline trace. |

## 2. Overview

Implement source ingestion as the immutable bridge between the human session and downstream extraction. Every master recording, backup recording, audio track, transcript revision, timestamp map, and upload route must have a source hash, storage URI, provenance, brand/session scope, retention policy, and ingestion receipt.

Transcript revisions are append-only. Alignment chooses a selected transcript revision for extraction without mutating previous revisions. Source corruption is terminal for that artifact and requires re-upload.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.02 | Ingest, preserve, align, and version master recordings, backup recordings, audio tracks, transcripts, timestamps, and upload provenance. | RecordingArtifact, TranscriptRevision, TranscriptAlignmentMap, voice role classification, source integrity checks, and ingestion receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 5 - Complete Expression Session |
| Entry Object | recordings/transcripts |
| Exit Object | aligned source/transcript artifacts |
| Validation Contract | source integrity and transcript alignment |
| Required Receipt | ingestion receipt |

### Legacy Intelligence Mapping

- Legacy audio engine and Demucs references inform voice separation fixtures.
- V9.1 source doctrine treats phone recording as master source when configured and meeting-platform capture as backup unless explicitly changed.
- Source artifacts and transcript revisions are greenfield immutable records.

## 4. Implementation Plan

1. Add contracts for `RecordingArtifact`, `TranscriptRevision`, `TranscriptAlignmentMap`, `VoiceRoleSegment`, and `IngestionReceipt`.
2. Store artifacts in object storage under immutable source/transcript namespaces with hashes.
3. Add transcript provider capability contract and adapter interface.
4. Implement alignment from transcript segments to source artifact timestamp ranges.
5. Classify source voice and interviewer voice where audio separation/classification is available.
6. Block extraction when selected transcript revision is missing, unaligned, or tied to corrupted source.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class RecordingArtifactType(str, Enum):
    MASTER_VIDEO = "master_video"
    BACKUP_VIDEO = "backup_video"
    MASTER_AUDIO = "master_audio"
    SEPARATED_GUEST_AUDIO = "separated_guest_audio"
    SEPARATED_INTERVIEWER_AUDIO = "separated_interviewer_audio"


class RecordingArtifact(BaseModel):
    recording_artifact_id: str
    expression_session_id: str
    brand_id: str
    artifact_type: RecordingArtifactType
    source_label: str
    object_uri: str
    content_hash: str
    upload_route: str
    retention_policy_id: str
    duration_ms: int | None = None
    corrupted: bool = False
    created_at: datetime


class TranscriptSegment(BaseModel):
    segment_id: str
    speaker_role: str
    text: str
    start_ms: int
    end_ms: int
    confidence: float = Field(ge=0, le=1)


class TranscriptRevision(BaseModel):
    transcript_revision_id: str
    expression_session_id: str
    selected_for_extraction: bool = False
    source_artifact_ids: list[str]
    segments: list[TranscriptSegment]
    revision_number: int
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `IngestRecordingArtifactCommand`, `GenerateTranscriptRevisionCommand`, `UploadTranscriptRevisionCommand`, `AlignTranscriptToSourceCommand`, `SelectTranscriptRevisionCommand`, `MarkSourceArtifactCorruptedCommand` |
| Events | `RecordingArtifactIngested`, `TranscriptRevisionCreated`, `TranscriptAligned`, `TranscriptRevisionSelected`, `SourceArtifactCorrupted`, `IngestionReceiptWritten` |
| Workflow | `CompleteExpressionSessionWorkflow.stage5_ingest_and_align` |
| Receipt | `IngestionReceipt` with artifact hashes, transcript revision IDs, alignment map hash, provider receipt IDs, and corruption status |

## 7. Backward Compatibility and Migration Fallback

Legacy audio/math behavior can be ported into new Python modules and fixtures. No old local-shell audio scripts are production dependencies. If voice separation is unavailable, store speaker role as `unknown_or_mixed` and require reviewer attention before extraction uses speaker-specific claims.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Convenient upload vs. source fidelity | Immutable hash and upload provenance required for every artifact. | Expression Moment candidates cite artifact ID and hash. |
| Transcript revision speed vs. auditability | Revisions are append-only and selected explicitly. | Extraction receipt names selected transcript revision. |
| Mixed audio vs. guest source truth | Voice role classification is explicit and confidence-scored. | Voice-specific extraction cannot use unclassified segments as certainty. |

## 9. Tasks

- Add source/transcript contracts and tables.
- Implement object storage hash verification.
- Implement transcript adapter and alignment service.
- Add corruption terminal failure handling.
- Add extraction blocker for missing selected transcript revision.
- Add voice role classification fields and fixtures.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Artifact records hash, source type, upload route, retention, brand, session, URI. | Source file saved with no hash. |
| AC2 | Transcript revisions are append-only and timestamp aligned. | Prior transcript revision is mutated in place. |
| AC3 | Extraction references selected revision. | Candidate uses a stale transcript revision silently. |
| AC4 | Guest/interviewer voices are distinct when classification exists. | Interviewer sentence becomes guest quote. |
| AC5 | Corruption creates terminal re-upload requirement. | Corrupted file proceeds to extraction. |

## 11. Dependencies

- TS-CMF-009 source artifact gate.
- TS-CMF-029 Complete Expression Session creation.
- TS-CMF-011 voice/audio classification where applicable.
- TS-CMF-002 stage records.
- Provider capability contract from architecture.

## 12. Testing Strategy


Unit tests:

- Unit tests for artifact hashing, transcript revision immutability, and timestamp ranges.
- Integration tests for transcript provider adapter and alignment map.
- Corruption tests requiring terminal re-upload.
- Security tests for cross-brand artifact access.
- Audio fixture tests for guest/interviewer classification fallback.

Integration tests:

- Workflow test from `recordings/transcripts` to `aligned source/transcript artifacts` through pipeline stage `5`.
- Command Bus test proving `ingestion receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for upload failures, hash mismatches, alignment confidence, transcript provider errors, and corrupted artifacts.
- Logs include artifact ID, transcript revision ID, provider receipt, and alignment map hash.
- Recovery: re-upload creates a new artifact and ingestion receipt.
- Rollback: select an earlier transcript revision through explicit command; prior revisions remain immutable.

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
| Tech Spec ID | TS-CMF-030 |
| Story | 6.2 |
| Requirement Trace | FR-CMF-06.02 |
| Pipeline Trace | Stage 5, recordings/transcripts to aligned artifacts |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No mutable transcript revisions, no hidden source mutation, no legacy runtime coupling |

