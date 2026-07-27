"""Source provenance repositories for TS-CMF-030."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.source_provenance import (
    IngestedRecordingArtifact,
    IngestionReceipt,
    TranscriptAlignmentMap,
    TranscriptRevision,
    VoiceRoleSegment,
)


@dataclass
class InMemorySourceProvenanceRepository:
    recording_artifacts: dict[UUID, IngestedRecordingArtifact] = field(default_factory=dict)
    transcript_revisions: dict[UUID, TranscriptRevision] = field(default_factory=dict)
    alignment_maps: dict[UUID, TranscriptAlignmentMap] = field(default_factory=dict)
    voice_role_segments: dict[UUID, VoiceRoleSegment] = field(default_factory=dict)
    receipts: dict[UUID, IngestionReceipt] = field(default_factory=dict)
    selected_revision_by_session: dict[UUID, UUID] = field(default_factory=dict)

    def put_recording_artifact(self, artifact: IngestedRecordingArtifact) -> IngestedRecordingArtifact:
        existing = self.recording_artifacts.get(artifact.recording_artifact_id)
        if existing is not None and existing.corrupted and existing != artifact:
            raise ValueError("corrupted source artifact is terminal and immutable")
        self.recording_artifacts[artifact.recording_artifact_id] = artifact
        return artifact

    def put_transcript_revision(self, revision: TranscriptRevision) -> TranscriptRevision:
        existing = self.transcript_revisions.get(revision.transcript_revision_id)
        if existing is not None and existing != revision:
            raise ValueError("transcript revisions are append-only")
        self.transcript_revisions[revision.transcript_revision_id] = revision
        return revision

    def put_alignment_map(self, alignment_map: TranscriptAlignmentMap) -> TranscriptAlignmentMap:
        self.alignment_maps[alignment_map.alignment_map_id] = alignment_map
        return alignment_map

    def put_voice_role_segment(self, segment: VoiceRoleSegment) -> VoiceRoleSegment:
        self.voice_role_segments[segment.voice_role_segment_id] = segment
        return segment

    def put_receipt(self, receipt: IngestionReceipt) -> IngestionReceipt:
        self.receipts[receipt.ingestion_receipt_id] = receipt
        return receipt

    def artifacts_for_session(self, expression_session_id: UUID) -> list[IngestedRecordingArtifact]:
        return [
            item
            for item in self.recording_artifacts.values()
            if item.expression_session_id == expression_session_id
        ]

    def transcript_revisions_for_session(self, expression_session_id: UUID) -> list[TranscriptRevision]:
        return [
            item
            for item in self.transcript_revisions.values()
            if item.expression_session_id == expression_session_id
        ]

    def alignment_for_revision(self, transcript_revision_id: UUID) -> TranscriptAlignmentMap | None:
        return next(
            (
                item
                for item in self.alignment_maps.values()
                if item.transcript_revision_id == transcript_revision_id
            ),
            None,
        )
