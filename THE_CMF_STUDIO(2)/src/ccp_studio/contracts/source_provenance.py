"""Source ingestion, transcript alignment, and provenance contracts for TS-CMF-030."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from ccp_studio.contracts.orchestration import utc_now


class RecordingArtifactType(str, Enum):
    master_video = "master_video"
    backup_video = "backup_video"
    master_audio = "master_audio"
    separated_guest_audio = "separated_guest_audio"
    separated_interviewer_audio = "separated_interviewer_audio"


class TranscriptSource(str, Enum):
    provider_generated = "provider_generated"
    operator_upload = "operator_upload"
    reviewer_revision = "reviewer_revision"


class VoiceRole(str, Enum):
    guest = "guest"
    interviewer = "interviewer"
    unknown_or_mixed = "unknown_or_mixed"


class IngestedRecordingArtifact(BaseModel):
    schema_version: Literal["cmf.ingested_recording_artifact.v1"]
    recording_artifact_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    artifact_type: RecordingArtifactType
    source_label: str = Field(min_length=1)
    object_uri: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    upload_route: str = Field(min_length=1)
    retention_policy_id: UUID
    duration_ms: int | None = Field(default=None, ge=1)
    corrupted: bool = False
    corruption_reason: str | None = None
    created_at: datetime


class TranscriptSegment(BaseModel):
    schema_version: Literal["cmf.transcript_segment.v1"]
    segment_id: UUID
    speaker_role: VoiceRole
    text: str = Field(min_length=1)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    confidence: float = Field(ge=0, le=1)
    source_artifact_id: UUID | None = None

    @field_validator("end_ms")
    @classmethod
    def end_after_start(cls, value: int, info):
        start = info.data.get("start_ms")
        if start is not None and value <= start:
            raise ValueError("end_ms must be greater than start_ms")
        return value


class TranscriptRevision(BaseModel):
    schema_version: Literal["cmf.transcript_revision.v1"]
    transcript_revision_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    selected_for_extraction: bool = False
    source_artifact_ids: list[UUID] = Field(min_length=1)
    segments: list[TranscriptSegment] = Field(min_length=1)
    revision_number: int = Field(ge=1)
    transcript_source: TranscriptSource
    provider_name: str | None = None
    provider_receipt_id: UUID | None = None
    supersedes_revision_id: UUID | None = None
    created_at: datetime


class TranscriptSegmentAlignment(BaseModel):
    schema_version: Literal["cmf.transcript_segment_alignment.v1"]
    segment_id: UUID
    source_artifact_id: UUID
    source_start_ms: int = Field(ge=0)
    source_end_ms: int = Field(ge=0)
    alignment_confidence: float = Field(ge=0, le=1)


class TranscriptAlignmentMap(BaseModel):
    schema_version: Literal["cmf.transcript_alignment_map.v1"]
    alignment_map_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    transcript_revision_id: UUID
    source_artifact_ids: list[UUID] = Field(min_length=1)
    segment_alignments: list[TranscriptSegmentAlignment] = Field(min_length=1)
    alignment_map_hash: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    selected_for_extraction: bool = False
    created_at: datetime


class VoiceRoleSegment(BaseModel):
    schema_version: Literal["cmf.voice_role_segment.v1"]
    voice_role_segment_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    transcript_revision_id: UUID
    segment_id: UUID
    speaker_role: VoiceRole
    confidence: float = Field(ge=0, le=1)
    classification_source: str = Field(min_length=1)
    source_artifact_id: UUID | None = None


class IngestionReceipt(BaseModel):
    schema_version: Literal["cmf.ingestion_receipt.v1"]
    ingestion_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    recording_artifact_ids: list[UUID] = Field(default_factory=list)
    artifact_hashes: dict[UUID, str] = Field(default_factory=dict)
    transcript_revision_ids: list[UUID] = Field(default_factory=list)
    alignment_map_id: UUID | None = None
    alignment_map_hash: str | None = None
    provider_receipt_ids: list[UUID] = Field(default_factory=list)
    selected_transcript_revision_id: UUID | None = None
    corruption_status: str = "clean"
    terminal_failure: bool = False
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def object_uri_for_source(*, brand_id: UUID, session_id: UUID, content_hash: str, filename: str) -> str:
    safe_name = filename.replace("..", "").replace("\\", "_").replace("/", "_")
    return f"brands/{brand_id}/source/{session_id}/{content_hash}/{safe_name}"


def object_uri_for_transcript(*, brand_id: UUID, session_id: UUID, revision_number: int) -> str:
    return f"brands/{brand_id}/transcripts/{session_id}/revision-{revision_number}.json"


def hash_content(content: str | bytes) -> str:
    raw = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(raw).hexdigest()


def alignment_hash(alignments: list[TranscriptSegmentAlignment]) -> str:
    payload = [item.model_dump(mode="json") for item in alignments]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def new_ingestion_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_session_id: UUID,
    decision_code: str,
    recording_artifact_ids: list[UUID] | None = None,
    artifact_hashes: dict[UUID, str] | None = None,
    transcript_revision_ids: list[UUID] | None = None,
    alignment_map_id: UUID | None = None,
    alignment_map_hash: str | None = None,
    provider_receipt_ids: list[UUID] | None = None,
    selected_transcript_revision_id: UUID | None = None,
    corruption_status: str = "clean",
    terminal_failure: bool = False,
    reviewer_actor_id: UUID | None = None,
) -> IngestionReceipt:
    return IngestionReceipt(
        schema_version="cmf.ingestion_receipt.v1",
        ingestion_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        recording_artifact_ids=recording_artifact_ids or [],
        artifact_hashes=artifact_hashes or {},
        transcript_revision_ids=transcript_revision_ids or [],
        alignment_map_id=alignment_map_id,
        alignment_map_hash=alignment_map_hash,
        provider_receipt_ids=provider_receipt_ids or [],
        selected_transcript_revision_id=selected_transcript_revision_id,
        corruption_status=corruption_status,
        terminal_failure=terminal_failure,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
