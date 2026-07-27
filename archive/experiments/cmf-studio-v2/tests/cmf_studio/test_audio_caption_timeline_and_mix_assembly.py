from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_voice_dna_boost_eligibility import _evaluate as _voice_evaluate  # noqa: E402
from test_voice_dna_boost_eligibility import _fixture as _voice_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.sonic_timeline import SonicAudioComponentRole  # noqa: E402
from ccp_studio.contracts.voice import VoiceBridgeClaimCategory  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.sonic_timeline_service import (  # noqa: E402
    SonicTimelineError,
    SonicTimelineService,
    register_sonic_timeline_command_handlers,
)
from ccp_studio.workflows.render_workflow import RenderWorkflow  # noqa: E402


def _audio_components():
    return [
        {
            "role": SonicAudioComponentRole.source_guest.value,
            "source_ref": "source_artifact:guest:truth-moment",
            "start_ms": 0,
            "end_ms": 2800,
        },
        {
            "role": SonicAudioComponentRole.interviewer.value,
            "source_ref": "source_artifact:interviewer:prompt",
            "start_ms": 2800,
            "end_ms": 3500,
        },
        {
            "role": SonicAudioComponentRole.restored_source.value,
            "source_ref": "restored_source:lavasr:breath-cleanup",
            "provider_receipt_id": str(uuid4()),
            "start_ms": 3500,
            "end_ms": 4300,
        },
        {
            "role": SonicAudioComponentRole.synthetic_bridge.value,
            "source_ref": "synthetic_bridge:moss_tts:approved-connector",
            "provider_receipt_id": str(uuid4()),
            "start_ms": 4300,
            "end_ms": 5200,
        },
        {
            "role": SonicAudioComponentRole.sfx.value,
            "source_ref": "sfx:paper-cut-soft-rise",
            "start_ms": 0,
            "end_ms": 1400,
            "gain_db": -12.0,
        },
        {
            "role": SonicAudioComponentRole.music.value,
            "source_ref": "music:licensed-bed:steady",
            "start_ms": 0,
            "end_ms": 8000,
            "gain_db": -18.0,
        },
        {
            "role": SonicAudioComponentRole.final_mix.value,
            "source_ref": "final_mix:render-output-main",
            "start_ms": 0,
            "end_ms": 8000,
        },
    ]


def _caption_segments():
    return [
        {
            "text": "This is the moment where the guest names the real edge.",
            "start_ms": 500,
            "end_ms": 2500,
            "source_start_ms": 0,
            "source_end_ms": 3000,
            "text_source_ref": "source_expression_moment:anchor-hit-001",
            "style_tags": ["negative_space_safe", "speaker_emphasis"],
        }
    ]


def _timeline_segments(audio, captions):
    return [
        {
            "track": "audio",
            "source_ref": f"audio_mix_manifest:{audio.audio_mix_manifest_id}",
            "component_refs": [item.component_id for item in audio.components],
            "start_ms": 0,
            "end_ms": 8000,
        },
        {
            "track": "caption",
            "source_ref": f"caption_manifest:{captions.caption_manifest_id}",
            "component_refs": [],
            "start_ms": 500,
            "end_ms": 2500,
        },
    ]


def _ducking_rules(audio):
    drivers = [
        item.component_id
        for item in audio.components
        if item.role
        in {
            SonicAudioComponentRole.source_guest,
            SonicAudioComponentRole.interviewer,
            SonicAudioComponentRole.restored_source,
            SonicAudioComponentRole.synthetic_bridge,
        }
    ]
    ducked = [item.component_id for item in audio.components if item.role == SonicAudioComponentRole.music]
    return [
        {
            "ducking_rule_id": "legacy-audio-engine:voice-over-music-duck",
            "driver_component_ids": drivers,
            "ducked_component_ids": ducked,
            "affected_window_ms": (0, 5200),
            "gain_reduction_db": -9.0,
            "reason": "Legacy audio engine fixture keeps voice intelligible over the music bed.",
        }
    ]


def _voice_report(render_output_id, blocked=False):
    service, _consent, _guard, org_id, brand_id, guest_id = _voice_fixture()
    claim_categories = (
        [VoiceBridgeClaimCategory.primary_claim]
        if blocked
        else [VoiceBridgeClaimCategory.bridge_context]
    )
    return _voice_evaluate(
        service,
        org_id,
        brand_id,
        guest_id,
        render_output_id=render_output_id,
        final_video_duration_seconds=60.0,
        requested_duration_seconds=1.0,
        claim_categories=claim_categories,
        source_evidence_refs=["source:quote:001", "visual_cover:paper-cut-bridge"],
    )


def _assembled(service: SonicTimelineService):
    render_output_id = uuid4()
    actor_id = uuid4()
    audio = service.compile_audio_mix_manifest(
        render_output_id=render_output_id,
        components=_audio_components(),
        actor_id=actor_id,
    )
    captions = service.compile_caption_manifest(
        render_output_id=render_output_id,
        platform_variant="reels_9x16",
        caption_segments=_caption_segments(),
        style_constraints={"max_chars_per_segment": 80, "safe_area": "caption_safe_negative_space"},
        actor_id=actor_id,
    )
    timeline = service.compile_timeline_manifest(
        render_output_id=render_output_id,
        duration_ms=8000,
        segments=_timeline_segments(audio, captions),
        actor_id=actor_id,
    )
    ducking = service.evaluate_audio_ducking(
        audio_mix_manifest_id=audio.audio_mix_manifest_id,
        ducking_rules=_ducking_rules(audio),
        actor_id=actor_id,
    )
    voice = service.validate_voice_bridge_policy(
        audio_mix_manifest_id=audio.audio_mix_manifest_id,
        voice_boost_report=_voice_report(render_output_id),
        actor_id=actor_id,
    )
    receipt = service.write_sonic_timeline_receipt(
        render_output_id=render_output_id,
        audio_mix_manifest_id=audio.audio_mix_manifest_id,
        caption_manifest_id=captions.caption_manifest_id,
        timeline_manifest_id=timeline.timeline_manifest_id,
        ducking_decision_ids=[item.ducking_decision_id for item in ducking],
        voice_bridge_policy_validation_id=voice.voice_bridge_policy_validation_id,
        actor_id=actor_id,
    )
    return render_output_id, actor_id, audio, captions, timeline, ducking, voice, receipt


def test_audio_mix_manifest_classifies_all_legacy_audio_roles_and_final_mix():
    service = SonicTimelineService()

    manifest = service.compile_audio_mix_manifest(
        render_output_id=uuid4(),
        components=_audio_components(),
        actor_id=uuid4(),
    )

    assert {item.role for item in manifest.components} == set(SonicAudioComponentRole)
    assert all(item.content_hash for item in manifest.components)
    assert any(item.role == SonicAudioComponentRole.final_mix for item in manifest.components)

    bad_components = _audio_components()
    bad_components[0] = bad_components[0] | {"source_ref": "synthetic_bridge:hidden-source"}
    with pytest.raises(SonicTimelineError) as exc:
        service.compile_audio_mix_manifest(
            render_output_id=uuid4(),
            components=bad_components,
            actor_id=uuid4(),
        )
    assert exc.value.code == "AUDIO_SOURCE_ROLE_CONFLICT"


def test_caption_manifest_stores_timing_text_source_style_and_platform_constraints():
    service = SonicTimelineService()

    manifest = service.compile_caption_manifest(
        render_output_id=uuid4(),
        platform_variant="linkedin_4x5",
        caption_segments=_caption_segments(),
        style_constraints={"max_chars_per_segment": 80, "font_role": "deterministic_text_layer"},
        actor_id=uuid4(),
    )

    assert manifest.platform_variant == "linkedin_4x5"
    assert manifest.text_source_refs == ["source_expression_moment:anchor-hit-001"]
    assert manifest.style_constraints["font_role"] == "deterministic_text_layer"
    assert manifest.caption_segments[0].start_ms == 500

    with pytest.raises(SonicTimelineError) as exc:
        service.compile_caption_manifest(
            render_output_id=uuid4(),
            platform_variant="reels_9x16",
            caption_segments=[
                _caption_segments()[0]
                | {"start_ms": 100, "end_ms": 400, "source_start_ms": 500, "source_end_ms": 900}
            ],
            style_constraints={"max_chars_per_segment": 80},
            actor_id=uuid4(),
        )
    assert exc.value.code == "CAPTION_SOURCE_TIMING_CONFLICT"


def test_ducking_math_and_affected_segments_are_recorded():
    service = SonicTimelineService()
    audio = service.compile_audio_mix_manifest(
        render_output_id=uuid4(),
        components=_audio_components(),
        actor_id=uuid4(),
    )

    decisions = service.evaluate_audio_ducking(
        audio_mix_manifest_id=audio.audio_mix_manifest_id,
        ducking_rules=_ducking_rules(audio),
        actor_id=uuid4(),
    )

    decision = decisions[0]
    assert decision.gain_reduction_db == -9.0
    assert decision.affected_window_ms == (0, 5200)
    assert len(decision.driver_component_ids) == 4
    assert len(decision.ducked_component_ids) == 1
    assert decision.decision_hash


def test_synthetic_bridge_voice_requires_voice_dna_boost_policy_validation():
    service = SonicTimelineService()
    render_output_id = uuid4()
    audio = service.compile_audio_mix_manifest(
        render_output_id=render_output_id,
        components=_audio_components(),
        actor_id=uuid4(),
    )

    with pytest.raises(SonicTimelineError) as missing:
        service.validate_voice_bridge_policy(audio_mix_manifest_id=audio.audio_mix_manifest_id, actor_id=uuid4())
    assert missing.value.code == "VOICE_BRIDGE_POLICY_REPORT_REQUIRED"

    with pytest.raises(SonicTimelineError) as blocked:
        service.validate_voice_bridge_policy(
            audio_mix_manifest_id=audio.audio_mix_manifest_id,
            voice_boost_report=_voice_report(render_output_id, blocked=True),
            actor_id=uuid4(),
        )
    assert blocked.value.code == "VOICE_BRIDGE_POLICY_BLOCKED"
    assert list(service.repository.voice_policy_validations.values())[-1].passed is False

    validation = service.validate_voice_bridge_policy(
        audio_mix_manifest_id=audio.audio_mix_manifest_id,
        voice_boost_report=_voice_report(render_output_id),
        actor_id=uuid4(),
    )
    assert validation.passed is True
    assert validation.synthetic_component_ids


def test_sonic_timeline_receipt_links_hashes_final_mix_and_review_lineage():
    service = SonicTimelineService()

    _render_output_id, _actor_id, audio, captions, timeline, ducking, voice, receipt = _assembled(service)
    review = service.build_review_read_model(receipt.sonic_timeline_receipt_id)

    assert receipt.audio_mix_hash == audio.mix_hash
    assert receipt.caption_hash == captions.manifest_hash
    assert receipt.timeline_hash == timeline.timeline_hash
    assert receipt.ducking_decision_ids == [item.ducking_decision_id for item in ducking]
    assert receipt.voice_bridge_policy_validation_id == voice.voice_bridge_policy_validation_id
    assert receipt.final_mix_ref == "final_mix:render-output-main"
    assert {item["role"] for item in review.audio_lineage} == {role.value for role in SonicAudioComponentRole}
    assert review.caption_lineage[0]["text_source_ref"] == "source_expression_moment:anchor-hit-001"
    assert review.mix_lineage["final_mix_ref"] == receipt.final_mix_ref


def test_render_workflow_stage12_audio_caption_timeline_assembly():
    service = SonicTimelineService()
    render_output_id = uuid4()
    actor_id = uuid4()
    workflow = RenderWorkflow(assembly_planner=None, sonic_timeline_service=service)

    receipt = workflow.stage12_audio_caption_timeline_assembly(
        render_output_id=render_output_id,
        audio_components=_audio_components(),
        caption_segments=_caption_segments(),
        duration_ms=8000,
        actor_id=actor_id,
        platform_variant="reels_9x16",
        style_constraints={"max_chars_per_segment": 80},
        voice_boost_report=_voice_report(render_output_id),
    )

    assert receipt.decision_code == "SONIC_TIMELINE_VALIDATED"
    assert receipt.sonic_timeline_receipt_id in service.repository.receipts


def test_sonic_timeline_command_bus_writes_receipt_event():
    service = SonicTimelineService()
    render_output_id, actor_id, audio, captions, timeline, ducking, voice, _receipt = _assembled(service)
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    register_sonic_timeline_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="WriteSonicTimelineReceiptCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "render_output_id": str(render_output_id),
            "audio_mix_manifest_id": str(audio.audio_mix_manifest_id),
            "caption_manifest_id": str(captions.caption_manifest_id),
            "timeline_manifest_id": str(timeline.timeline_manifest_id),
            "ducking_decision_ids": [str(item.ducking_decision_id) for item in ducking],
            "voice_bridge_policy_validation_id": str(voice.voice_bridge_policy_validation_id),
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["sonic_timeline_receipt_id"]
    assert bus.event_outbox.events[-1].event_type == "WriteSonicTimelineReceiptCommand.succeeded"
