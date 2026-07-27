from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.acting_library import (  # noqa: E402
    ActingReferenceStatus,
    acting_state_matrix,
)
from ccp_studio.contracts.brand_genesis import (  # noqa: E402
    BrandSourceInput,
    NegativeSpaceInput,
    VisualConstitutionInput,
    VoiceDnaReference,
    VoiceDnaReferenceKind,
)
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.source import SourceArtifactKind  # noqa: E402
from ccp_studio.services.acting_library_service import ActingLibraryService, ActingLibraryServiceError  # noqa: E402
from ccp_studio.services.brand_genesis_service import BrandGenesisService  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.source_ingestion import SourceIngestionService  # noqa: E402


def _consent_scope():
    return ConsentScope(
        recording_allowed=True,
        source_storage_allowed=True,
        likeness_use_allowed=True,
        derivative_generation_allowed=True,
        provider_processing_allowed=True,
        synthetic_voice_eligible=True,
        reuse_allowed=True,
        retention_allowed=True,
        publication_allowed=False,
    )


def _brand_genesis_ready_for_acting():
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
        scope=_consent_scope(),
        actor_id=actor_id,
        evidence_refs=["signed likeness consent"],
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
        provenance="client photo upload",
    )
    report = source.evaluate_quality(session_id=source_session_id, artifact=artifact)
    accepted = source.accept_source_artifact(artifact=artifact, report=report)
    brand_genesis = BrandGenesisService(consent.repository, source.repository)
    session = brand_genesis.create_session(
        organization_id=org_id,
        brand_id=brand_id,
        brand_notes="Interview-first coaching brand with credible warmth.",
        audience_summary="Introverted founders who need sharper public expression.",
        offer_summary="Interview-led production of thought leadership assets.",
        forbidden_tone=["hype", "guru certainty"],
        visual_preferences=["editorial paper-cut", "realistic identity source"],
        voice_dna_references=[
            VoiceDnaReference(
                schema_version="cmf.voice_dna_reference.v1",
                voice_dna_reference_id=uuid4(),
                reference_kind=VoiceDnaReferenceKind.migrated_registry_entry,
                label="Brand voice calibration",
                approved=True,
                migration_ledger_entry_id=uuid4(),
                registry_entry_id=uuid4(),
                evidence_refs=["legacy voice dna"],
            )
        ],
        source_inputs=[
            BrandSourceInput(
                schema_version="cmf.brand_source_input.v1",
                source_artifact_ids=[accepted.source_artifact_id],
                consent_record_version_id=version.consent_record_version_id,
                source_quality_receipt_ids=[report.source_quality_report_id],
            )
        ],
        visual_constitution_input=VisualConstitutionInput(
            schema_version="cmf.visual_constitution_input.v1",
            visual_preferences=["editorial paper-cut"],
            paper_cut_direction="2.5D papercut avatar with realistic acting references first",
            composition_preferences=["caption-safe negative space"],
            style_constraints=["avoid glossy stock realism"],
        ),
        negative_space_input=NegativeSpaceInput(
            schema_version="cmf.negative_space_input.v1",
            forbidden_tone=["hype"],
            forbidden_visual_motifs=["generic neon AI"],
            avoided_claims=["guaranteed virality"],
            style_boundaries=["no parody without explicit approval"],
        ),
        created_by_actor_id=actor_id,
    )
    brand_genesis.start_workflow(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
        actor_id=actor_id,
    )
    acting = ActingLibraryService(brand_genesis.repository)
    return acting, org_id, brand_id, session, accepted


def _generated_grid():
    acting, org_id, brand_id, session, accepted = _brand_genesis_ready_for_acting()
    version = acting.generate_reference_grid(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session.brand_genesis_session_id,
        source_artifact_ids=[accepted.source_artifact_id],
        provider_name="GPT Image 2",
    )
    return acting, org_id, brand_id, session, accepted, version


def _evaluate_and_approve_all(acting, org_id, brand_id, version):
    for reference_id in version.acting_reference_ids:
        acting.evaluate_reference(
            organization_id=org_id,
            brand_id=brand_id,
            acting_reference_id=reference_id,
            likeness_score=0.95,
            gesture_clarity_score=0.94,
            hand_quality_score=0.93,
            paper_texture_score=0.92,
            style_adherence_score=0.91,
            negative_space_score=0.9,
            production_usability_score=0.96,
        )
        acting.approve_reference(
            organization_id=org_id,
            brand_id=brand_id,
            acting_reference_id=reference_id,
        )


def test_64_state_grid_records_emotional_gesture_sources_provider_receipts_and_review_state():
    acting, org_id, brand_id, _session, accepted, version = _generated_grid()
    references = [acting.repository.references[item] for item in version.acting_reference_ids]

    assert len(version.acting_reference_ids) == 64
    assert len(acting_state_matrix()) == 64
    assert len(acting.repository.provider_receipts) == 64
    assert {(ref.state_cell.matrix_row, ref.state_cell.matrix_column) for ref in references} == {
        (row, column) for row in range(1, 9) for column in range(1, 9)
    }
    first = references[0]
    assert first.organization_id == org_id
    assert first.brand_id == brand_id
    assert accepted.source_artifact_id in first.source_artifact_ids
    assert first.provider_receipt_id in acting.repository.provider_receipts
    assert first.status == ActingReferenceStatus.generated
    assert first.artifact_uri.startswith(f"brands/{brand_id}/brand-genesis/")


def test_failed_reference_blocks_approval_and_can_be_repaired_rejected_or_replaced():
    acting, org_id, brand_id, _session, _accepted, version = _generated_grid()
    reference_id = version.acting_reference_ids[0]
    acting.evaluate_reference(
        organization_id=org_id,
        brand_id=brand_id,
        acting_reference_id=reference_id,
        likeness_score=0.95,
        gesture_clarity_score=0.87,
        hand_quality_score=0.25,
        paper_texture_score=0.91,
        style_adherence_score=0.9,
        negative_space_score=0.88,
        production_usability_score=0.4,
        failure_notes=["broken hero-frame hands"],
    )

    with pytest.raises(ActingLibraryServiceError) as exc:
        acting.approve_reference(organization_id=org_id, brand_id=brand_id, acting_reference_id=reference_id)
    assert exc.value.code == "ACTING_REFERENCE_EVALUATION_FAILED"

    repair = acting.request_repair(
        organization_id=org_id,
        brand_id=brand_id,
        acting_reference_id=reference_id,
        instructions="repair hands and preserve likeness",
    )
    assert repair.status == ActingReferenceStatus.repair_requested
    replacement = acting.replace_reference(
        organization_id=org_id,
        brand_id=brand_id,
        acting_reference_id=reference_id,
        provider_name="GPT Image 2",
    )
    assert replacement.replaces_reference_id == reference_id
    rejected = acting.reject_reference(
        organization_id=org_id,
        brand_id=brand_id,
        acting_reference_id=replacement.acting_reference_id,
        reason="identity drift after repair",
    )
    assert rejected.status == ActingReferenceStatus.rejected


def test_approved_references_lock_into_immutable_acting_library_version():
    acting, org_id, brand_id, _session, _accepted, version = _generated_grid()
    _evaluate_and_approve_all(acting, org_id, brand_id, version)

    locked = acting.lock_library_version(
        organization_id=org_id,
        brand_id=brand_id,
        acting_library_version_id=version.acting_library_version_id,
    )
    first_reference_id = locked.acting_reference_ids[0]
    selectable = acting.assert_reference_selectable_for_scenespec(
        organization_id=org_id,
        brand_id=brand_id,
        acting_library_version_id=locked.acting_library_version_id,
        acting_reference_id=first_reference_id,
    )

    assert locked.locked is True
    assert locked.version_hash != "draft"
    assert selectable.status == ActingReferenceStatus.locked
    with pytest.raises(ActingLibraryServiceError) as exc:
        acting.evaluate_reference(
            organization_id=org_id,
            brand_id=brand_id,
            acting_reference_id=first_reference_id,
            likeness_score=0.1,
            gesture_clarity_score=0.1,
            hand_quality_score=0.1,
            paper_texture_score=0.1,
            style_adherence_score=0.1,
            negative_space_score=0.1,
            production_usability_score=0.1,
        )
    assert exc.value.code == "ACTING_LIBRARY_VERSION_IMMUTABLE"
    assert acting.repository.versions[locked.acting_library_version_id].version_hash == locked.version_hash


def test_unapproved_reference_blocks_scenespec_selection_and_library_lock():
    acting, org_id, brand_id, _session, _accepted, version = _generated_grid()
    reference_id = version.acting_reference_ids[0]

    with pytest.raises(ActingLibraryServiceError) as lock_exc:
        acting.lock_library_version(
            organization_id=org_id,
            brand_id=brand_id,
            acting_library_version_id=version.acting_library_version_id,
        )
    assert lock_exc.value.code == "ACTING_REFERENCE_NOT_APPROVED"

    with pytest.raises(ActingLibraryServiceError) as select_exc:
        acting.assert_reference_selectable_for_scenespec(
            organization_id=org_id,
            brand_id=brand_id,
            acting_library_version_id=version.acting_library_version_id,
            acting_reference_id=reference_id,
        )
    assert select_exc.value.code == "ACTING_LIBRARY_VERSION_NOT_LOCKED"


def test_provider_output_cannot_skip_evaluation_or_receipt_before_approval():
    acting, org_id, brand_id, _session, _accepted, version = _generated_grid()
    reference_id = version.acting_reference_ids[0]
    reference = acting.repository.references[reference_id]

    with pytest.raises(ActingLibraryServiceError) as eval_exc:
        acting.approve_reference(organization_id=org_id, brand_id=brand_id, acting_reference_id=reference_id)
    assert eval_exc.value.code == "EVALUATION_RECEIPT_REQUIRED"

    acting.evaluate_reference(
        organization_id=org_id,
        brand_id=brand_id,
        acting_reference_id=reference_id,
        likeness_score=0.95,
        gesture_clarity_score=0.94,
        hand_quality_score=0.93,
        paper_texture_score=0.92,
        style_adherence_score=0.91,
        negative_space_score=0.9,
        production_usability_score=0.96,
    )
    del acting.repository.provider_receipts[reference.provider_receipt_id]
    with pytest.raises(ActingLibraryServiceError) as provider_exc:
        acting.approve_reference(organization_id=org_id, brand_id=brand_id, acting_reference_id=reference_id)
    assert provider_exc.value.code == "PROVIDER_RECEIPT_REQUIRED"


def test_cross_brand_reference_selection_fails():
    acting, org_id, brand_id, _session, _accepted, version = _generated_grid()
    reference_id = version.acting_reference_ids[0]

    with pytest.raises(ActingLibraryServiceError) as exc:
        acting.assert_reference_selectable_for_scenespec(
            organization_id=org_id,
            brand_id=uuid4(),
            acting_library_version_id=version.acting_library_version_id,
            acting_reference_id=reference_id,
        )

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"
