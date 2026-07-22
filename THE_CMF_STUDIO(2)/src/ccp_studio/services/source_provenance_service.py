"""Source ingestion, transcript alignment, and provenance service for TS-CMF-030."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.expression_session import ExpressionSessionStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.source_provenance import (
    IngestedRecordingArtifact,
    IngestionReceipt,
    RecordingArtifactType,
    TranscriptAlignmentMap,
    TranscriptRevision,
    TranscriptSegment,
    TranscriptSegmentAlignment,
    TranscriptSource,
    VoiceRole,
    VoiceRoleSegment,
    alignment_hash,
    hash_content,
    new_ingestion_receipt,
    object_uri_for_source,
)
from ccp_studio.repositories.source_provenance import InMemorySourceProvenanceRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.expression_session_service import CompleteExpressionSessionService


class SourceProvenanceServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class SourceProvenanceService:
    expression_session_service: CompleteExpressionSessionService
    repository: InMemorySourceProvenanceRepository = field(default_factory=InMemorySourceProvenanceRepository)

    def ingest_recording_artifact(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        artifact_type: RecordingArtifactType,
        source_label: str,
        filename: str,
        content: str | bytes,
        upload_route: str,
        retention_policy_id: UUID,
        actor_id: UUID,
        source_hash: str | None = None,
        expected_content_hash: str | None = None,
        duration_ms: int | None = None,
    ) -> IngestedRecordingArtifact:
        self._session_ready_for_ingestion(organization_id, brand_id, expression_session_id)
        content_hash = hash_content(content)
        if expected_content_hash is not None and expected_content_hash != content_hash:
            receipt = new_ingestion_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                decision_code="SOURCE_HASH_MISMATCH",
                corruption_status="hash_mismatch",
                terminal_failure=True,
                reviewer_actor_id=actor_id,
            )
            self.repository.put_receipt(receipt)
            raise SourceProvenanceServiceError("SOURCE_HASH_MISMATCH", "Uploaded source content does not match expected hash.")
        artifact = IngestedRecordingArtifact(
            schema_version="cmf.ingested_recording_artifact.v1",
            recording_artifact_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            artifact_type=artifact_type,
            source_label=source_label,
            object_uri=object_uri_for_source(
                brand_id=brand_id,
                session_id=expression_session_id,
                content_hash=content_hash,
                filename=filename,
            ),
            content_hash=content_hash,
            source_hash=source_hash or content_hash,
            upload_route=upload_route,
            retention_policy_id=retention_policy_id,
            duration_ms=duration_ms,
            created_at=utc_now(),
        )
        self.repository.put_recording_artifact(artifact)
        self.repository.put_receipt(
            new_ingestion_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                recording_artifact_ids=[artifact.recording_artifact_id],
                artifact_hashes={artifact.recording_artifact_id: artifact.content_hash},
                decision_code="RECORDING_ARTIFACT_INGESTED",
                reviewer_actor_id=actor_id,
            )
        )
        return artifact

    def generate_transcript_revision(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        source_artifact_ids: list[UUID],
        segments: list[TranscriptSegment],
        transcript_source: TranscriptSource,
        actor_id: UUID,
        provider_name: str | None = None,
        provider_receipt_id: UUID | None = None,
        supersedes_revision_id: UUID | None = None,
    ) -> TranscriptRevision:
        self._session_ready_for_ingestion(organization_id, brand_id, expression_session_id)
        self._require_clean_artifacts(organization_id, brand_id, expression_session_id, source_artifact_ids)
        revision_number = len(self.repository.transcript_revisions_for_session(expression_session_id)) + 1
        revision = TranscriptRevision(
            schema_version="cmf.transcript_revision.v1",
            transcript_revision_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            source_artifact_ids=source_artifact_ids,
            segments=segments,
            revision_number=revision_number,
            transcript_source=transcript_source,
            provider_name=provider_name,
            provider_receipt_id=provider_receipt_id,
            supersedes_revision_id=supersedes_revision_id,
            created_at=utc_now(),
        )
        self.repository.put_transcript_revision(revision)
        self.repository.put_receipt(
            new_ingestion_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                transcript_revision_ids=[revision.transcript_revision_id],
                provider_receipt_ids=[provider_receipt_id] if provider_receipt_id else [],
                decision_code="TRANSCRIPT_REVISION_CREATED",
                reviewer_actor_id=actor_id,
            )
        )
        return revision

    def align_transcript_to_source(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        transcript_revision_id: UUID,
        actor_id: UUID,
    ) -> TranscriptAlignmentMap:
        revision = self._revision_for_brand(organization_id, brand_id, transcript_revision_id)
        artifacts = self._require_clean_artifacts(
            organization_id,
            brand_id,
            revision.expression_session_id,
            revision.source_artifact_ids,
        )
        alignments = [
            TranscriptSegmentAlignment(
                schema_version="cmf.transcript_segment_alignment.v1",
                segment_id=segment.segment_id,
                source_artifact_id=segment.source_artifact_id or artifacts[0].recording_artifact_id,
                source_start_ms=segment.start_ms,
                source_end_ms=segment.end_ms,
                alignment_confidence=segment.confidence,
            )
            for segment in revision.segments
        ]
        amap_hash = alignment_hash(alignments)
        alignment_map = TranscriptAlignmentMap(
            schema_version="cmf.transcript_alignment_map.v1",
            alignment_map_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=revision.expression_session_id,
            transcript_revision_id=revision.transcript_revision_id,
            source_artifact_ids=revision.source_artifact_ids,
            segment_alignments=alignments,
            alignment_map_hash=amap_hash,
            confidence=min(item.alignment_confidence for item in alignments),
            created_at=utc_now(),
        )
        self.repository.put_alignment_map(alignment_map)
        for segment in revision.segments:
            self.repository.put_voice_role_segment(
                VoiceRoleSegment(
                    schema_version="cmf.voice_role_segment.v1",
                    voice_role_segment_id=uuid4(),
                    organization_id=organization_id,
                    brand_id=brand_id,
                    expression_session_id=revision.expression_session_id,
                    transcript_revision_id=revision.transcript_revision_id,
                    segment_id=segment.segment_id,
                    speaker_role=segment.speaker_role,
                    confidence=segment.confidence,
                    classification_source="transcript_provider" if segment.speaker_role != VoiceRole.unknown_or_mixed else "fallback_unknown",
                    source_artifact_id=segment.source_artifact_id or artifacts[0].recording_artifact_id,
                )
            )
        self.repository.put_receipt(
            new_ingestion_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=revision.expression_session_id,
                transcript_revision_ids=[revision.transcript_revision_id],
                alignment_map_id=alignment_map.alignment_map_id,
                alignment_map_hash=alignment_map.alignment_map_hash,
                provider_receipt_ids=[revision.provider_receipt_id] if revision.provider_receipt_id else [],
                decision_code="TRANSCRIPT_ALIGNED",
                reviewer_actor_id=actor_id,
            )
        )
        return alignment_map

    def select_transcript_revision(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        transcript_revision_id: UUID,
        actor_id: UUID,
    ) -> IngestionReceipt:
        revision = self._revision_for_brand(organization_id, brand_id, transcript_revision_id)
        alignment_map = self.repository.alignment_for_revision(transcript_revision_id)
        if alignment_map is None:
            raise SourceProvenanceServiceError("TRANSCRIPT_ALIGNMENT_REQUIRED", "Transcript must be aligned before extraction selection.")
        self._require_clean_artifacts(organization_id, brand_id, revision.expression_session_id, revision.source_artifact_ids)
        self.repository.selected_revision_by_session[revision.expression_session_id] = transcript_revision_id
        selected_map = alignment_map.model_copy(update={"selected_for_extraction": True})
        self.repository.put_alignment_map(selected_map)
        receipt = new_ingestion_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=revision.expression_session_id,
            transcript_revision_ids=[transcript_revision_id],
            alignment_map_id=selected_map.alignment_map_id,
            alignment_map_hash=selected_map.alignment_map_hash,
            selected_transcript_revision_id=transcript_revision_id,
            decision_code="TRANSCRIPT_REVISION_SELECTED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def selected_transcript_for_extraction(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
    ) -> TranscriptRevision:
        self._session_ready_for_ingestion(organization_id, brand_id, expression_session_id)
        selected_id = self.repository.selected_revision_by_session.get(expression_session_id)
        if selected_id is None:
            raise SourceProvenanceServiceError("SELECTED_TRANSCRIPT_REQUIRED", "Extraction requires an explicitly selected transcript revision.")
        revision = self._revision_for_brand(organization_id, brand_id, selected_id)
        if self.repository.alignment_for_revision(selected_id) is None:
            raise SourceProvenanceServiceError("TRANSCRIPT_ALIGNMENT_REQUIRED", "Selected transcript is not aligned.")
        self._require_clean_artifacts(organization_id, brand_id, expression_session_id, revision.source_artifact_ids)
        return revision

    def mark_source_artifact_corrupted(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        recording_artifact_id: UUID,
        reason: str,
        actor_id: UUID,
    ) -> IngestionReceipt:
        artifact = self._artifact_for_brand(organization_id, brand_id, recording_artifact_id)
        corrupted = artifact.model_copy(update={"corrupted": True, "corruption_reason": reason})
        self.repository.recording_artifacts[recording_artifact_id] = corrupted
        receipt = new_ingestion_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=artifact.expression_session_id,
            recording_artifact_ids=[recording_artifact_id],
            artifact_hashes={recording_artifact_id: artifact.content_hash},
            corruption_status=reason,
            terminal_failure=True,
            decision_code="SOURCE_ARTIFACT_CORRUPTED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def _session_ready_for_ingestion(self, organization_id: UUID, brand_id: UUID, expression_session_id: UUID):
        session = self.expression_session_service.get_session(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
        )
        if session.status not in {
            ExpressionSessionStatus.in_progress,
            ExpressionSessionStatus.paused,
            ExpressionSessionStatus.closed,
        }:
            raise SourceProvenanceServiceError("EXPRESSION_SESSION_CAPTURE_REQUIRED", "Session capture must be started before source ingestion.")
        return session

    def _artifact_for_brand(self, organization_id: UUID, brand_id: UUID, recording_artifact_id: UUID) -> IngestedRecordingArtifact:
        artifact = self.repository.recording_artifacts.get(recording_artifact_id)
        if artifact is None:
            raise SourceProvenanceServiceError("RECORDING_ARTIFACT_REQUIRED", "Recording artifact is required.")
        if artifact.organization_id != organization_id or artifact.brand_id != brand_id:
            raise SourceProvenanceServiceError("BRAND_SCOPE_VIOLATION", "Recording artifact is outside active brand scope.")
        return artifact

    def _require_clean_artifacts(
        self,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        artifact_ids: list[UUID],
    ) -> list[IngestedRecordingArtifact]:
        artifacts = [self._artifact_for_brand(organization_id, brand_id, item) for item in artifact_ids]
        if any(item.expression_session_id != expression_session_id for item in artifacts):
            raise SourceProvenanceServiceError("SESSION_SCOPE_VIOLATION", "Source artifact belongs to a different session.")
        corrupted = [item for item in artifacts if item.corrupted]
        if corrupted:
            raise SourceProvenanceServiceError("SOURCE_ARTIFACT_CORRUPTED", "Corrupted source requires re-upload before extraction.")
        return artifacts

    def _revision_for_brand(self, organization_id: UUID, brand_id: UUID, transcript_revision_id: UUID) -> TranscriptRevision:
        revision = self.repository.transcript_revisions.get(transcript_revision_id)
        if revision is None:
            raise SourceProvenanceServiceError("TRANSCRIPT_REVISION_REQUIRED", "Transcript revision is required.")
        if revision.organization_id != organization_id or revision.brand_id != brand_id:
            raise SourceProvenanceServiceError("BRAND_SCOPE_VIOLATION", "Transcript revision is outside active brand scope.")
        return revision


@dataclass
class SourceProvenanceCommandHandler:
    command_type: str
    service: SourceProvenanceService
    aggregate_type: str = "source_provenance"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "IngestRecordingArtifactCommand":
            return self.service.ingest_recording_artifact(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                artifact_type=RecordingArtifactType(payload["artifact_type"]),
                source_label=payload["source_label"],
                filename=payload["filename"],
                content=payload["content"],
                upload_route=payload["upload_route"],
                retention_policy_id=UUID(payload["retention_policy_id"]),
                source_hash=payload.get("source_hash"),
                expected_content_hash=payload.get("expected_content_hash"),
                duration_ms=payload.get("duration_ms"),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type in {"GenerateTranscriptRevisionCommand", "UploadTranscriptRevisionCommand"}:
            return self.service.generate_transcript_revision(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                source_artifact_ids=[UUID(item) for item in payload["source_artifact_ids"]],
                segments=[TranscriptSegment.model_validate(item) for item in payload["segments"]],
                transcript_source=TranscriptSource(payload.get("transcript_source", "provider_generated")),
                provider_name=payload.get("provider_name"),
                provider_receipt_id=UUID(payload["provider_receipt_id"]) if payload.get("provider_receipt_id") else None,
                supersedes_revision_id=UUID(payload["supersedes_revision_id"]) if payload.get("supersedes_revision_id") else None,
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "AlignTranscriptToSourceCommand":
            return self.service.align_transcript_to_source(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                transcript_revision_id=UUID(payload["transcript_revision_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "SelectTranscriptRevisionCommand":
            return self.service.select_transcript_revision(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                transcript_revision_id=UUID(payload["transcript_revision_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "MarkSourceArtifactCorruptedCommand":
            return self.service.mark_source_artifact_corrupted(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                recording_artifact_id=UUID(payload["recording_artifact_id"]),
                reason=payload["reason"],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise SourceProvenanceServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("expression_session_id") or payload.get("transcript_revision_id") or payload.get("recording_artifact_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_source_provenance_command_handlers(bus: CommandBus, service: SourceProvenanceService) -> None:
    for command_type in [
        "IngestRecordingArtifactCommand",
        "GenerateTranscriptRevisionCommand",
        "UploadTranscriptRevisionCommand",
        "AlignTranscriptToSourceCommand",
        "SelectTranscriptRevisionCommand",
        "MarkSourceArtifactCorruptedCommand",
    ]:
        bus.register_handler(SourceProvenanceCommandHandler(command_type=command_type, service=service))
