from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_complete_expression_session_creation import _approved_deck_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.source_provenance import (  # noqa: E402
    RecordingArtifactType,
    TranscriptSegment,
    TranscriptSource,
    VoiceRole,
    hash_content,
)
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.source_provenance_service import (  # noqa: E402
    SourceProvenanceService,
    SourceProvenanceServiceError,
    register_source_provenance_command_handlers,
)
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _started_source_service():
    session_service, org_id, brand_id, actor_id, _guest_id, _consent, _deck, session = _approved_deck_fixture()
    session_service.start_session(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    source_service = SourceProvenanceService(session_service)
    return source_service, session_service, org_id, brand_id, actor_id, session


def _segments(source_artifact_id=None):
    return [
        TranscriptSegment(
            schema_version="cmf.transcript_segment.v1",
            segment_id=uuid4(),
            speaker_role=VoiceRole.guest,
            text="The camera was not the problem; exposure was.",
            start_ms=0,
            end_ms=4100,
            confidence=0.94,
            source_artifact_id=source_artifact_id,
        ),
        TranscriptSegment(
            schema_version="cmf.transcript_segment.v1",
            segment_id=uuid4(),
            speaker_role=VoiceRole.interviewer,
            text="Where did that pressure first become real?",
            start_ms=4100,
            end_ms=6900,
            confidence=0.91,
            source_artifact_id=source_artifact_id,
        ),
    ]


def _artifact(service, org_id, brand_id, actor_id, session):
    return service.ingest_recording_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        artifact_type=RecordingArtifactType.master_audio,
        source_label="phone master",
        filename="master.wav",
        content="source audio bytes",
        upload_route="operator_upload",
        retention_policy_id=uuid4(),
        expected_content_hash=hash_content("source audio bytes"),
        duration_ms=6900,
        actor_id=actor_id,
    )


def test_artifact_records_hash_source_type_upload_route_retention_brand_session_and_uri():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()

    artifact = _artifact(service, org_id, brand_id, actor_id, session)

    assert artifact.organization_id == org_id
    assert artifact.brand_id == brand_id
    assert artifact.expression_session_id == session.expression_session_id
    assert artifact.artifact_type == RecordingArtifactType.master_audio
    assert artifact.content_hash == hash_content("source audio bytes")
    assert artifact.source_hash == artifact.content_hash
    assert artifact.upload_route == "operator_upload"
    assert artifact.retention_policy_id
    assert artifact.object_uri.startswith(f"brands/{brand_id}/source/{session.expression_session_id}/")


def test_transcript_revisions_are_append_only_and_timestamp_aligned():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()
    artifact = _artifact(service, org_id, brand_id, actor_id, session)
    revision1 = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.provider_generated,
        provider_name="fixture-transcriber",
        provider_receipt_id=uuid4(),
        actor_id=actor_id,
    )
    revision2 = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.reviewer_revision,
        supersedes_revision_id=revision1.transcript_revision_id,
        actor_id=actor_id,
    )
    alignment = service.align_transcript_to_source(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision2.transcript_revision_id,
        actor_id=actor_id,
    )

    assert revision1.revision_number == 1
    assert revision2.revision_number == 2
    assert revision2.supersedes_revision_id == revision1.transcript_revision_id
    assert alignment.segment_alignments[0].source_start_ms == revision2.segments[0].start_ms
    with pytest.raises(ValueError):
        service.repository.put_transcript_revision(revision1.model_copy(update={"revision_number": 99}))


def test_extraction_references_selected_revision_instead_of_mutating_prior_revision():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()
    artifact = _artifact(service, org_id, brand_id, actor_id, session)
    revision1 = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.provider_generated,
        actor_id=actor_id,
    )
    revision2 = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.operator_upload,
        supersedes_revision_id=revision1.transcript_revision_id,
        actor_id=actor_id,
    )
    service.align_transcript_to_source(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision2.transcript_revision_id,
        actor_id=actor_id,
    )
    receipt = service.select_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision2.transcript_revision_id,
        actor_id=actor_id,
    )
    selected = service.selected_transcript_for_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
    )

    assert receipt.selected_transcript_revision_id == revision2.transcript_revision_id
    assert selected.transcript_revision_id == revision2.transcript_revision_id
    assert service.repository.transcript_revisions[revision1.transcript_revision_id].selected_for_extraction is False


def test_guest_and_interviewer_voice_segments_are_distinct_when_classification_exists():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()
    artifact = _artifact(service, org_id, brand_id, actor_id, session)
    revision = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.provider_generated,
        actor_id=actor_id,
    )
    service.align_transcript_to_source(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision.transcript_revision_id,
        actor_id=actor_id,
    )
    roles = {item.speaker_role for item in service.repository.voice_role_segments.values()}

    assert VoiceRole.guest in roles
    assert VoiceRole.interviewer in roles


def test_corruption_creates_terminal_reupload_requirement_and_blocks_extraction():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()
    artifact = _artifact(service, org_id, brand_id, actor_id, session)
    revision = service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.provider_generated,
        actor_id=actor_id,
    )
    service.align_transcript_to_source(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision.transcript_revision_id,
        actor_id=actor_id,
    )
    service.select_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision.transcript_revision_id,
        actor_id=actor_id,
    )

    receipt = service.mark_source_artifact_corrupted(
        organization_id=org_id,
        brand_id=brand_id,
        recording_artifact_id=artifact.recording_artifact_id,
        reason="demux_hash_mismatch",
        actor_id=actor_id,
    )

    assert receipt.terminal_failure is True
    assert receipt.decision_code == "SOURCE_ARTIFACT_CORRUPTED"
    with pytest.raises(SourceProvenanceServiceError) as exc:
        service.selected_transcript_for_extraction(
            organization_id=org_id,
            brand_id=brand_id,
            expression_session_id=session.expression_session_id,
        )
    assert exc.value.code == "SOURCE_ARTIFACT_CORRUPTED"


def test_workflow_stage5_ingest_and_align_returns_alignment_map():
    service, session_service, org_id, brand_id, actor_id, session = _started_source_service()
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=service,
    )

    alignment = workflow.stage5_ingest_and_align(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
        filename="master.wav",
        content="source audio bytes",
        retention_policy_id=uuid4(),
        segments=_segments(),
    )

    assert alignment.segment_alignments
    assert alignment.alignment_map_hash


def test_source_provenance_command_bus_emits_ingestion_event():
    service, _session_service, org_id, brand_id, actor_id, session = _started_source_service()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_source_provenance_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="IngestRecordingArtifactCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "expression_session_id": str(session.expression_session_id),
            "artifact_type": "master_audio",
            "source_label": "phone master",
            "filename": "master.wav",
            "content": "source audio bytes",
            "upload_route": "operator_upload",
            "retention_policy_id": str(uuid4()),
            "expected_content_hash": hash_content("source audio bytes"),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["schema_version"] == "cmf.ingested_recording_artifact.v1"
    assert bus.event_outbox.events[-1].event_type == "IngestRecordingArtifactCommand.succeeded"
