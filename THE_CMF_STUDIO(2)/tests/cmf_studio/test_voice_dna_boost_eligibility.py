from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.audio import AudioSourceType
from ccp_studio.contracts.commands import ActorContext, ActorType
from ccp_studio.contracts.consent import ConsentScope
from ccp_studio.contracts.voice import (
    VoiceBridgeClaimCategory,
    VoiceEligibilityStatus,
    new_repair_hierarchy_proof,
)
from ccp_studio.dspy_programs.anti_draft_calibration_program import AntiDraftCalibrationProgram
from ccp_studio.providers.moss_tts import MossTtsAdapter
from ccp_studio.services.audio_classification import AudioClassificationError, AudioClassificationService
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.consent_guard import ConsentGuardService, register_consent_guard
from ccp_studio.services.consent_service import ConsentService
from ccp_studio.services.voice_boost_eligibility import VoiceBoostEligibilityService


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


def _actor():
    return ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["owner"])


def _proof(**overrides):
    values = {
        "recut_checked": True,
        "verbatim_fragment_search_checked": True,
        "prior_approved_quote_checked": True,
        "human_pickup_request_checked": True,
        "evidence_refs": ["hierarchy:recut", "hierarchy:fragment", "hierarchy:quote", "hierarchy:pickup"],
    }
    values.update(overrides)
    return new_repair_hierarchy_proof(**values)


def _fixture(scope=None):
    consent = ConsentService()
    guard = ConsentGuardService(consent)
    bus = create_in_memory_command_bus()
    register_consent_guard(bus, guard)
    org_id = uuid4()
    brand_id = uuid4()
    guest_id = uuid4()
    actor = _actor()
    bus.brands.add_scope(org_id, brand_id)
    consent.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=scope or _scope(),
        actor_id=actor.actor_id,
        evidence_refs=["consent:synthetic_voice"],
    )
    service = VoiceBoostEligibilityService(guard)
    return service, consent, guard, org_id, brand_id, guest_id


def _evaluate(service, org_id, brand_id, guest_id, **overrides):
    values = {
        "organization_id": org_id,
        "brand_id": brand_id,
        "guest_or_client_id": guest_id,
        "render_output_id": uuid4(),
        "final_video_duration_seconds": 60.0,
        "requested_duration_seconds": 4.0,
        "repair_hierarchy": _proof(),
        "visual_covering_provided": True,
        "visual_covering_ref": "broll:paper-cut:bridge-cover",
        "claim_categories": [VoiceBridgeClaimCategory.bridge_context],
        "evaluation_receipt_ids": [uuid4()],
        "source_evidence_refs": ["source:quote:001"],
    }
    values.update(overrides)
    return service.evaluate(**values)


def test_repair_hierarchy_must_be_exhausted_before_voice_boost():
    service, _consent, _guard, org_id, brand_id, guest_id = _fixture()

    report = _evaluate(
        service,
        org_id,
        brand_id,
        guest_id,
        repair_hierarchy=_proof(verbatim_fragment_search_checked=False),
    )

    assert report.status == VoiceEligibilityStatus.blocked
    assert "VOICE_REPAIR_HIERARCHY_INCOMPLETE" in report.blocker_codes
    assert next(iter(service.repository.eligibility_receipts.values())).decision_code == "VOICE_BOOST_BLOCKED"


def test_eligible_bridge_receipt_proves_consent_evidence_visual_covering_cap_hierarchy_and_claims():
    service, _consent, _guard, org_id, brand_id, guest_id = _fixture()
    provider_receipt = MossTtsAdapter().synthesize_bridge(
        text="That is the bridge into the next idea.",
        voice_profile_ref="voice-dna:approved:1",
    )

    report = _evaluate(service, org_id, brand_id, guest_id)
    bridge = service.create_bridge_manifest(
        report=report,
        provider_receipt=provider_receipt,
        synthetic_audio_uri=provider_receipt.artifact_uri,
        visual_covering_ref="broll:paper-cut:bridge-cover",
        claim_categories=[VoiceBridgeClaimCategory.bridge_context],
    )
    receipt = next(iter(service.repository.eligibility_receipts.values()))

    assert report.status == VoiceEligibilityStatus.eligible
    assert report.max_duration_seconds == 7.0
    assert report.visual_covering_provided is True
    assert report.claim_restriction_passed is True
    assert report.repair_hierarchy.exhausted is True
    assert receipt.consent_record_version_id == report.consent_record_version_id
    assert "source:quote:001" in receipt.evidence_refs
    assert bridge.duration_cap_compliant is True


def test_audio_manifest_distinguishes_all_audio_source_types():
    audio = AudioClassificationService()
    render_output_id = uuid4()
    segments = [
        audio.classify_segment(source_type=source_type, start_seconds=index, end_seconds=index + 0.5, source_ref=f"audio:{source_type.value}")
        for index, source_type in enumerate(AudioSourceType)
    ]

    manifest = audio.create_manifest(render_output_id=render_output_id, segments=segments)

    assert {segment.source_type for segment in manifest.segments} == set(AudioSourceType)
    assert any(segment.source_type == AudioSourceType.synthetic_bridge_voice for segment in manifest.segments)


def test_primary_claim_or_sensitive_assertion_is_rejected():
    service, _consent, _guard, org_id, brand_id, guest_id = _fixture()

    report = _evaluate(
        service,
        org_id,
        brand_id,
        guest_id,
        claim_categories=[VoiceBridgeClaimCategory.primary_claim],
    )

    assert report.status == VoiceEligibilityStatus.blocked
    assert report.claim_restriction_passed is False
    assert "VOICE_BRIDGE_CLAIM_RESTRICTED" in report.blocker_codes


def test_failed_voice_dna_evaluation_blocks_review_approval():
    service, _consent, _guard, org_id, brand_id, guest_id = _fixture()
    calibration = AntiDraftCalibrationProgram().evaluate(
        render_output_id=uuid4(),
        semantic_continuity_score=0.92,
        voice_continuity_score=0.42,
        anti_draft_score=0.91,
        evidence_refs=["voice-continuity:failed"],
    )

    report = _evaluate(
        service,
        org_id,
        brand_id,
        guest_id,
        render_output_id=calibration.render_output_id,
        calibration_report=calibration,
    )

    assert "VOICE_DNA_EVALUATION_FAILED" in report.blocker_codes
    assert service.can_approve_voice_bridge(report) is False


def test_synthetic_bridge_requires_explicit_synthetic_voice_consent():
    service, _consent, guard, org_id, brand_id, guest_id = _fixture(
        _scope(synthetic_voice_eligible=False)
    )

    report = _evaluate(service, org_id, brand_id, guest_id)
    blocker_receipt = next(iter(guard.repository.blocker_receipts.values()))

    assert report.status == VoiceEligibilityStatus.blocked
    assert "SYNTHETIC_VOICE_CONSENT_REQUIRED" in report.blocker_codes
    assert blocker_receipt.decision_code == "SYNTHETIC_VOICE_CONSENT_REQUIRED"


def test_moss_tts_adapter_returns_provider_receipt_without_approval_state():
    receipt = MossTtsAdapter().synthesize_bridge(
        text="Small bridge.",
        voice_profile_ref="voice-dna:approved:1",
    )

    assert receipt.provider_name == "moss_tts"
    assert receipt.operation == "synthesize_voice_bridge"
    assert not hasattr(receipt, "approval_state")


def test_audio_classification_required_before_publishing():
    audio = AudioClassificationService()

    with pytest.raises(AudioClassificationError) as exc:
        audio.require_manifest_before_publishing(render_output_id=uuid4())

    assert exc.value.code == "AUDIO_CLASSIFICATION_REQUIRED"
