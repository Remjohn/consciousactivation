from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.brand_genesis import (  # noqa: E402
    BrandGenesisSessionStatus,
    BrandSourceInput,
    NegativeSpaceInput,
    VisualConstitutionInput,
    VoiceDnaReference,
    VoiceDnaReferenceKind,
)
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.source import SourceArtifactKind  # noqa: E402
from ccp_studio.services.brand_genesis_service import BrandGenesisService, BrandGenesisServiceError  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.source_ingestion import SourceIngestionService  # noqa: E402


def _scope(**overrides):
    defaults = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": True,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": False,
    }
    defaults.update(overrides)
    return ConsentScope(**defaults)


def _source_and_consent(consent_scope=None):
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    guest_id = uuid4()
    source_session_id = uuid4()
    consent = ConsentService()
    source = SourceIngestionService()
    version = consent.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=consent_scope or _scope(),
        actor_id=actor_id,
        evidence_refs=["signed likeness release", "brand genesis consent"],
    )
    source.submit_recording_configuration(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=source_session_id,
        expected_master_source="source photo set",
        backup_route="operator upload",
        platform_source=None,
        upload_method="brand_genesis_upload",
        file_safety_expectations=["no unconsented likeness reuse"],
        quality_requirements=["face visibility", "angle diversity", "identity stability"],
    )
    artifact = source.create_source_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=source_session_id,
        kind=SourceArtifactKind.uploaded_reference,
        filename="front-facing-neutral.png",
        content_hash="sha256-front-facing-neutral",
        source_hash="sha256-source-photo-set",
        retention_policy_id=uuid4(),
        provenance="client-uploaded photo",
    )
    report = source.evaluate_quality(session_id=source_session_id, artifact=artifact)
    accepted = source.accept_source_artifact(artifact=artifact, report=report)
    service = BrandGenesisService(consent.repository, source.repository)
    return service, org_id, brand_id, actor_id, version, accepted, report


def _voice_reference(kind=VoiceDnaReferenceKind.migrated_registry_entry, approved=True):
    return VoiceDnaReference(
        schema_version="cmf.voice_dna_reference.v1",
        voice_dna_reference_id=uuid4(),
        reference_kind=kind,
        label="Claude Voice DNA calibration",
        approved=approved,
        migration_ledger_entry_id=uuid4(),
        registry_entry_id=uuid4() if kind == VoiceDnaReferenceKind.migrated_registry_entry else None,
        evidence_refs=["legacy-inventory:voice_dna_models.py"],
    )


def _valid_intake(version, accepted, report, **overrides):
    intake = {
        "brand_notes": "Interview-first coaching brand with warm authority and precise insight.",
        "audience_summary": "Introverted founders who need sharper thought leadership without scripted performance.",
        "offer_summary": "Interview-led content pack that turns real speech into usable assets.",
        "forbidden_tone": ["hype", "guru certainty"],
        "visual_preferences": ["editorial paper-cut", "clean hierarchy"],
        "voice_dna_references": [_voice_reference()],
        "source_inputs": [
            BrandSourceInput(
                schema_version="cmf.brand_source_input.v1",
                source_artifact_ids=[accepted.source_artifact_id],
                consent_record_version_id=version.consent_record_version_id,
                source_quality_receipt_ids=[report.source_quality_report_id],
                source_notes="front-facing neutral source photo",
            )
        ],
        "visual_constitution_input": VisualConstitutionInput(
            schema_version="cmf.visual_constitution_input.v1",
            visual_preferences=["editorial paper-cut", "subtle dimensionality"],
            paper_cut_direction="2.5D papercut avatar with restrained motion potential",
            composition_preferences=["clear subject hierarchy", "caption-safe negative space"],
            style_constraints=["avoid glossy stock-photo realism"],
        ),
        "negative_space_input": NegativeSpaceInput(
            schema_version="cmf.negative_space_input.v1",
            forbidden_tone=["hype", "guru certainty"],
            forbidden_visual_motifs=["wealth flex", "generic neon AI"],
            avoided_claims=["guaranteed virality"],
            style_boundaries=["no parody unless explicitly consented"],
        ),
    }
    intake.update(overrides)
    return intake


def test_valid_brand_genesis_intake_records_source_voice_visual_negative_space_and_start_receipt():
    service, org_id, brand_id, actor_id, version, accepted, report = _source_and_consent()
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        created_by_actor_id=actor_id,
        **_valid_intake(version, accepted, report),
    )

    run = service.start_workflow(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
        actor_id=actor_id,
    )
    receipt = service.repository.latest_start_receipt(session.brand_genesis_session_id)
    stored = service.get_session(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
    )

    assert stored.status == BrandGenesisSessionStatus.running
    assert stored.brand_notes.startswith("Interview-first")
    assert stored.voice_dna_references[0].registry_entry_id is not None
    assert stored.visual_constitution_input.paper_cut_direction.startswith("2.5D")
    assert "guru certainty" in stored.negative_space_input.forbidden_tone
    assert stored.storage_prefix.startswith(f"brands/{brand_id}/brand-genesis/")
    assert receipt is not None
    assert receipt.genesis_start_receipt_id == run.start_receipt_id
    assert receipt.decision_code == "BRAND_GENESIS_WORKFLOW_STARTED"
    assert accepted.source_artifact_id in receipt.source_artifact_ids
    assert version.consent_record_version_id in receipt.consent_record_version_ids


def test_source_media_without_consent_scope_blocks_brand_genesis_start():
    service, org_id, brand_id, actor_id, version, accepted, report = _source_and_consent(
        _scope(likeness_use_allowed=False)
    )
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        created_by_actor_id=actor_id,
        **_valid_intake(version, accepted, report),
    )

    with pytest.raises(BrandGenesisServiceError) as exc:
        service.start_workflow(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session.brand_genesis_session_id,
            actor_id=actor_id,
        )

    assert exc.value.code == "CONSENT_SCOPE_BLOCKED"
    assert service.repository.get_session(session.brand_genesis_session_id).status == BrandGenesisSessionStatus.blocked


def test_incomplete_intake_returns_missing_evidence_without_fabricated_brand_constitution():
    service, org_id, brand_id, actor_id, version, accepted, report = _source_and_consent()
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        created_by_actor_id=actor_id,
        **_valid_intake(
            version,
            accepted,
            report,
            brand_notes="",
            voice_dna_references=[],
            visual_constitution_input=None,
        ),
    )

    missing = service.validate_intake(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
    )

    assert missing.fabricated_defaults_used is False
    assert "brand_notes" in missing.missing_fields
    assert "voice_dna_references" in missing.missing_fields
    assert "visual_constitution_input" in missing.missing_fields
    with pytest.raises(BrandGenesisServiceError) as exc:
        service.start_workflow(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session.brand_genesis_session_id,
            actor_id=actor_id,
        )
    assert exc.value.code == "BRAND_GENESIS_INTAKE_INCOMPLETE"


def test_brand_genesis_session_cannot_be_queried_or_reused_across_brand_boundaries():
    service, org_id, brand_id, actor_id, version, accepted, report = _source_and_consent()
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        created_by_actor_id=actor_id,
        **_valid_intake(version, accepted, report),
    )

    with pytest.raises(BrandGenesisServiceError) as exc:
        service.get_session(
            organization_id=org_id,
            brand_id=uuid4(),
            brand_genesis_session_id=session.brand_genesis_session_id,
        )

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_raw_legacy_voice_dna_reference_must_be_migrated_before_activation():
    service, org_id, brand_id, actor_id, version, accepted, report = _source_and_consent()
    session = service.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        created_by_actor_id=actor_id,
        **_valid_intake(
            version,
            accepted,
            report,
            voice_dna_references=[
                _voice_reference(kind=VoiceDnaReferenceKind.raw_legacy_reference, approved=True)
            ],
        ),
    )
    missing = service.validate_intake(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
    )

    assert "VOICE_DNA_REFERENCE_NOT_MIGRATED" in missing.blocker_codes
    with pytest.raises(BrandGenesisServiceError) as exc:
        service.start_workflow(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session.brand_genesis_session_id,
            actor_id=actor_id,
        )
    assert exc.value.code == "VOICE_DNA_REFERENCE_NOT_MIGRATED"
