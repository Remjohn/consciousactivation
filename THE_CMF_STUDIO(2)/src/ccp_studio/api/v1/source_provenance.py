"""FastAPI adapter for TS-CMF-030 source provenance."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.source_provenance import (
    IngestedRecordingArtifact,
    IngestionReceipt,
    RecordingArtifactType,
    TranscriptAlignmentMap,
    TranscriptRevision,
    TranscriptSegment,
    TranscriptSource,
)
from ccp_studio.services.source_provenance_service import SourceProvenanceService


router = APIRouter(prefix="/api/v1/source-provenance", tags=["source-provenance"])
_source_provenance_service: SourceProvenanceService | None = None


class IngestRecordingArtifactRequest(BaseModel):
    artifact_type: RecordingArtifactType
    source_label: str
    filename: str
    content: str
    upload_route: str = "operator_upload"
    retention_policy_id: UUID
    source_hash: str | None = None
    expected_content_hash: str | None = None
    duration_ms: int | None = None
    actor_id: UUID


class TranscriptRevisionRequest(BaseModel):
    source_artifact_ids: list[UUID]
    segments: list[TranscriptSegment]
    transcript_source: TranscriptSource = TranscriptSource.provider_generated
    provider_name: str | None = None
    provider_receipt_id: UUID | None = None
    supersedes_revision_id: UUID | None = None
    actor_id: UUID


def set_source_provenance_service(service: SourceProvenanceService) -> None:
    global _source_provenance_service
    _source_provenance_service = service


def get_source_provenance_service() -> SourceProvenanceService:
    if _source_provenance_service is None:
        raise RuntimeError("SourceProvenanceService must be configured by the application.")
    return _source_provenance_service


@router.post("/brands/{brand_id}/sessions/{expression_session_id}/recordings", response_model=IngestedRecordingArtifact)
def ingest_recording_artifact(
    brand_id: UUID,
    organization_id: UUID,
    expression_session_id: UUID,
    request: IngestRecordingArtifactRequest,
    service: SourceProvenanceService = Depends(get_source_provenance_service),
) -> IngestedRecordingArtifact:
    return service.ingest_recording_artifact(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        artifact_type=request.artifact_type,
        source_label=request.source_label,
        filename=request.filename,
        content=request.content,
        upload_route=request.upload_route,
        retention_policy_id=request.retention_policy_id,
        source_hash=request.source_hash,
        expected_content_hash=request.expected_content_hash,
        duration_ms=request.duration_ms,
        actor_id=request.actor_id,
    )


@router.post("/brands/{brand_id}/sessions/{expression_session_id}/transcripts", response_model=TranscriptRevision)
def create_transcript_revision(
    brand_id: UUID,
    organization_id: UUID,
    expression_session_id: UUID,
    request: TranscriptRevisionRequest,
    service: SourceProvenanceService = Depends(get_source_provenance_service),
) -> TranscriptRevision:
    return service.generate_transcript_revision(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        source_artifact_ids=request.source_artifact_ids,
        segments=request.segments,
        transcript_source=request.transcript_source,
        provider_name=request.provider_name,
        provider_receipt_id=request.provider_receipt_id,
        supersedes_revision_id=request.supersedes_revision_id,
        actor_id=request.actor_id,
    )


@router.post("/brands/{brand_id}/transcripts/{transcript_revision_id}/align", response_model=TranscriptAlignmentMap)
def align_transcript(
    brand_id: UUID,
    organization_id: UUID,
    transcript_revision_id: UUID,
    actor_id: UUID,
    service: SourceProvenanceService = Depends(get_source_provenance_service),
) -> TranscriptAlignmentMap:
    return service.align_transcript_to_source(
        organization_id=organization_id,
        brand_id=brand_id,
        transcript_revision_id=transcript_revision_id,
        actor_id=actor_id,
    )


@router.post("/brands/{brand_id}/transcripts/{transcript_revision_id}/select", response_model=IngestionReceipt)
def select_transcript(
    brand_id: UUID,
    organization_id: UUID,
    transcript_revision_id: UUID,
    actor_id: UUID,
    service: SourceProvenanceService = Depends(get_source_provenance_service),
) -> IngestionReceipt:
    return service.select_transcript_revision(
        organization_id=organization_id,
        brand_id=brand_id,
        transcript_revision_id=transcript_revision_id,
        actor_id=actor_id,
    )
