from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.source import SourceArtifactKind, SourceQualityStatus
from ccp_studio.services.source_ingestion import SourceIngestionError, SourceIngestionService


def _source_fixture():
    service = SourceIngestionService()
    org_id = uuid4()
    brand_id = uuid4()
    session_id = uuid4()
    retention_policy_id = uuid4()
    config = service.submit_recording_configuration(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        expected_master_source="local wav master",
        backup_route="secondary recorder",
        platform_source="zoom",
        upload_method="operator_upload",
        file_safety_expectations=["no platform compression as canonical"],
        quality_requirements=["master wav", "guest/interviewer separation", "timestamp alignment"],
    )
    return service, org_id, brand_id, session_id, retention_policy_id, config


def test_recording_setup_records_master_backup_platform_upload_safety_and_quality():
    _service, org_id, brand_id, session_id, _retention_policy_id, config = _source_fixture()

    assert config.organization_id == org_id
    assert config.brand_id == brand_id
    assert config.session_id == session_id
    assert config.expected_master_source == "local wav master"
    assert config.backup_route == "secondary recorder"
    assert config.platform_source == "zoom"
    assert config.upload_method == "operator_upload"
    assert "no platform compression as canonical" in config.file_safety_expectations
    assert "guest/interviewer separation" in config.quality_requirements


def test_missing_master_source_blocks_session_start_with_recovery_action():
    service, _org_id, _brand_id, session_id, _retention_policy_id, _config = _source_fixture()

    report = service.evaluate_quality(session_id=session_id, artifact=None)

    assert report.status == SourceQualityStatus.blocked
    assert report.failure_category == "MASTER_SOURCE_REQUIRED"
    assert report.recovery_action == "upload master recording"


def test_compressed_platform_source_requires_review_before_canonical_acceptance():
    service, org_id, brand_id, session_id, retention_policy_id, _config = _source_fixture()
    artifact = service.create_source_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        kind=SourceArtifactKind.platform_recording,
        filename="zoom.mp4",
        content_hash="sha256-platform",
        source_hash="sha256-platform-source",
        retention_policy_id=retention_policy_id,
        provenance="zoom export",
    )

    report = service.evaluate_quality(session_id=session_id, artifact=artifact)

    assert report.status == SourceQualityStatus.review_required
    assert report.failure_category == "CANONICAL_SOURCE_REVIEW_REQUIRED"
    with pytest.raises(SourceIngestionError) as exc:
        service.accept_source_artifact(artifact=artifact, report=report)
    assert exc.value.code == "CANONICAL_SOURCE_REVIEW_REQUIRED"


def test_accepted_source_stores_hashes_brand_session_retention_provenance_and_immutable_uri():
    service, org_id, brand_id, session_id, retention_policy_id, _config = _source_fixture()
    artifact = service.create_source_artifact(
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
    report = service.evaluate_quality(session_id=session_id, artifact=artifact)

    accepted = service.accept_source_artifact(artifact=artifact, report=report)

    assert accepted.accepted_at is not None
    assert accepted.content_hash == "sha256-master"
    assert accepted.source_hash == "sha256-source"
    assert accepted.retention_policy_id == retention_policy_id
    assert accepted.immutable_uri.startswith(f"brands/{brand_id}/source/{session_id}/sha256-master/")
    assert len(service.repository.receipts) == 1
    with pytest.raises(ValueError):
        service.repository.put_artifact(accepted.model_copy(update={"source_hash": "changed"}))


def test_manifest_creation_requires_accepted_source_and_consent_compatibility():
    service, org_id, brand_id, session_id, retention_policy_id, _config = _source_fixture()
    artifact = service.create_source_artifact(
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
    report = service.evaluate_quality(session_id=session_id, artifact=artifact)
    accepted = service.accept_source_artifact(artifact=artifact, report=report)

    with pytest.raises(SourceIngestionError) as exc:
        service.create_manifest_for_session(
            organization_id=org_id,
            brand_id=brand_id,
            session_id=session_id,
            consent_compatible=False,
        )
    assert exc.value.code == "CONSENT_RECORD_REQUIRED"

    manifest = service.create_manifest_for_session(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
    )

    assert accepted.source_artifact_id in manifest.source_artifact_ids
    assert len(service.repository.manifests) == 1
    assert any(receipt.decision_code == "SOURCE_ARTIFACT_MANIFEST_CREATED" for receipt in service.repository.receipts.values())


def test_quality_failure_shows_exact_category_and_recovery_action():
    service, org_id, brand_id, session_id, retention_policy_id, _config = _source_fixture()
    artifact = service.create_source_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        kind=SourceArtifactKind.master_recording,
        filename="master.wav",
        content_hash="mismatch",
        source_hash="sha256-source",
        retention_policy_id=retention_policy_id,
        provenance="local recorder",
    )

    report = service.evaluate_quality(session_id=session_id, artifact=artifact)

    assert report.status == SourceQualityStatus.blocked
    assert report.failure_category == "SOURCE_HASH_MISMATCH"
    assert report.recovery_action == "re-upload source artifact"
