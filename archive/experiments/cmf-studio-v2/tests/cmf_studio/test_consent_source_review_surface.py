from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.audio import AudioSourceType
from ccp_studio.contracts.consent import ConsentScope
from ccp_studio.contracts.review_evidence import ApprovalBlockerCode, new_source_reference
from ccp_studio.contracts.source import SourceArtifactKind
from ccp_studio.services.audio_classification import AudioClassificationService
from ccp_studio.services.consent_service import ConsentService
from ccp_studio.services.review_evidence_service import ReviewEvidenceError, ReviewEvidenceService
from ccp_studio.services.source_ingestion import SourceIngestionService


def _scope(**overrides):
    values = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": True,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": True,
    }
    values.update(overrides)
    return ConsentScope(**values)


def _source_fixture():
    source_service = SourceIngestionService()
    org_id = uuid4()
    brand_id = uuid4()
    session_id = uuid4()
    retention_policy_id = uuid4()
    source_service.submit_recording_configuration(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        expected_master_source="local wav master",
        backup_route="secondary recorder",
        platform_source=None,
        upload_method="operator_upload",
        file_safety_expectations=["hash required"],
        quality_requirements=["master wav"],
    )
    artifact = source_service.create_source_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        kind=SourceArtifactKind.master_recording,
        filename="master.wav",
        content_hash="sha256-master",
        source_hash="sha256-source",
        retention_policy_id=retention_policy_id,
        provenance="local recorder",
    )
    report = source_service.evaluate_quality(session_id=session_id, artifact=artifact)
    artifact = source_service.accept_source_artifact(artifact=artifact, report=report)
    return source_service, org_id, brand_id, artifact


def _review_fixture():
    source_service, org_id, brand_id, artifact = _source_fixture()
    consent_service = ConsentService()
    guest_id = uuid4()
    actor_id = uuid4()
    consent_service.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(),
        actor_id=actor_id,
        evidence_refs=["consent:review"],
    )
    review_service = ReviewEvidenceService(
        consent_repository=consent_service.repository,
        source_repository=source_service.repository,
    )
    transcript = review_service.append_transcript_revision(
        source_artifact_id=artifact.source_artifact_id,
        revision_number=1,
        transcript_hash="transcript-hash-v1",
        source_hash=artifact.source_hash,
        text_ref="transcripts/session/v1.json",
    )
    audio = AudioClassificationService()
    segment = audio.classify_segment(
        source_type=AudioSourceType.source_voice,
        start_seconds=10.0,
        end_seconds=16.0,
        source_ref=str(artifact.source_artifact_id),
    )
    audio_manifest = audio.create_manifest(render_output_id=uuid4(), segments=[segment])
    source_reference = new_source_reference(
        source_artifact_id=artifact.source_artifact_id,
        transcript_revision_id=transcript.transcript_revision_id,
        start_seconds=10.0,
        end_seconds=16.0,
        claim_ref="claim:core:001",
    )
    return review_service, org_id, brand_id, guest_id, artifact, transcript, audio_manifest, source_reference


def _clean_view(review_service, org_id, brand_id, guest_id, source_reference, audio_manifest, **overrides):
    values = {
        "organization_id": org_id,
        "brand_id": brand_id,
        "guest_or_client_id": guest_id,
        "object_type": "render_output",
        "object_id": uuid4(),
        "source_references": [source_reference],
        "evaluation_receipt_ids": [uuid4()],
        "audio_mix_manifest_id": audio_manifest.audio_mix_manifest_id,
        "file_provenance_refs": ["source:sha256-master", "render:sha256-output"],
    }
    values.update(overrides)
    return review_service.generate_evidence_view(**values)


def test_review_surface_shows_consent_source_transcript_timestamps_claim_voice_and_provenance():
    review_service, org_id, brand_id, guest_id, artifact, transcript, audio_manifest, source_reference = _review_fixture()

    view = _clean_view(review_service, org_id, brand_id, guest_id, source_reference, audio_manifest)

    assert view.consent_record_version_id is not None
    assert view.source_references[0].source_artifact_id == artifact.source_artifact_id
    assert view.source_references[0].start_seconds == 10.0
    assert view.source_references[0].claim_ref == "claim:core:001"
    assert transcript.transcript_revision_id in view.transcript_revision_ids
    assert view.transcript_revisions[0].transcript_hash == "transcript-hash-v1"
    assert view.audio_mix_manifest_id == audio_manifest.audio_mix_manifest_id
    assert "source:sha256-master" in view.file_provenance_refs
    assert view.blockers == []


def test_claim_without_source_reference_blocks_approval_until_repaired_or_removed():
    review_service, org_id, brand_id, guest_id, _artifact, _transcript, audio_manifest, _source_reference = _review_fixture()

    view = _clean_view(
        review_service,
        org_id,
        brand_id,
        guest_id,
        source_reference=None,
        audio_manifest=audio_manifest,
        source_references=[],
    )

    assert any(blocker.blocker_code == ApprovalBlockerCode.missing_source_reference for blocker in view.blockers)
    with pytest.raises(ReviewEvidenceError) as exc:
        review_service.approve_with_evidence(
            approval_evidence_view_id=view.approval_evidence_view_id,
            approved_by_actor_id=uuid4(),
        )
    assert exc.value.code == "MISSING_SOURCE_REFERENCE"


def test_multiple_source_revisions_display_append_only_transcript_revisions_and_hashes():
    review_service, org_id, brand_id, guest_id, artifact, transcript, audio_manifest, source_reference = _review_fixture()
    second = review_service.append_transcript_revision(
        source_artifact_id=artifact.source_artifact_id,
        revision_number=2,
        transcript_hash="transcript-hash-v2",
        source_hash=artifact.source_hash,
        text_ref="transcripts/session/v2.json",
    )

    view = _clean_view(review_service, org_id, brand_id, guest_id, source_reference, audio_manifest)

    assert [item.revision_number for item in view.transcript_revisions] == [1, 2]
    assert [item.transcript_hash for item in view.transcript_revisions] == [
        transcript.transcript_hash,
        second.transcript_hash,
    ]
    with pytest.raises(ValueError):
        review_service.repository.append_transcript_revision(transcript)


def test_approval_event_and_review_receipt_include_consent_and_source_references():
    review_service, org_id, brand_id, guest_id, _artifact, _transcript, audio_manifest, source_reference = _review_fixture()
    view = _clean_view(review_service, org_id, brand_id, guest_id, source_reference, audio_manifest)

    event = review_service.approve_with_evidence(
        approval_evidence_view_id=view.approval_evidence_view_id,
        approved_by_actor_id=uuid4(),
    )
    receipt = next(iter(review_service.repository.receipts.values()))

    assert event.consent_record_version_id == view.consent_record_version_id
    assert source_reference.source_reference_id in event.source_reference_ids
    assert event.review_evidence_receipt_id == receipt.review_evidence_receipt_id
    assert str(source_reference.source_reference_id) in event.audit_evidence_refs
    assert str(view.consent_record_version_id) in receipt.evidence_refs


def test_complex_telegram_review_deep_links_to_pwa():
    review_service, org_id, brand_id, guest_id, _artifact, _transcript, audio_manifest, source_reference = _review_fixture()
    view = _clean_view(
        review_service,
        org_id,
        brand_id,
        guest_id,
        source_reference,
        audio_manifest,
        telegram_complexity_score=5,
    )

    deep_link = review_service.telegram_deep_link_for_review(view)

    assert any(blocker.blocker_code == ApprovalBlockerCode.pwa_review_required for blocker in view.blockers)
    assert deep_link is not None
    assert deep_link.target_surface == "pwa"
    assert deep_link.required_reason == "PWA_REVIEW_REQUIRED"


def test_approval_command_cannot_bypass_review_evidence_receipt():
    review_service, org_id, brand_id, guest_id, _artifact, _transcript, audio_manifest, source_reference = _review_fixture()
    view = _clean_view(review_service, org_id, brand_id, guest_id, source_reference, audio_manifest)
    review_service.repository.receipts.clear()

    with pytest.raises(ReviewEvidenceError) as exc:
        review_service.approve_with_evidence(
            approval_evidence_view_id=view.approval_evidence_view_id,
            approved_by_actor_id=uuid4(),
        )

    assert exc.value.code == "REVIEW_EVIDENCE_RECEIPT_REQUIRED"


def test_review_read_model_never_returns_cross_brand_source_artifacts():
    review_service, org_id, brand_id, guest_id, _artifact, _transcript, audio_manifest, _source_reference = _review_fixture()
    other_artifact = next(iter(_source_fixture()[0].repository.artifacts.values()))
    cross_brand_ref = new_source_reference(
        source_artifact_id=other_artifact.source_artifact_id,
        start_seconds=0.0,
        end_seconds=1.0,
        claim_ref="claim:cross-brand",
    )

    view = _clean_view(
        review_service,
        org_id,
        brand_id,
        guest_id,
        cross_brand_ref,
        audio_manifest,
    )

    assert view.source_references == []
    assert any(blocker.blocker_code == ApprovalBlockerCode.missing_source_reference for blocker in view.blockers)
