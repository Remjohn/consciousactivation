import pytest

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    AudioLevelAnalysisReceipt,
    CompleteEditingSessionRenderStateWrapper,
    DurationToleranceReceipt,
    FFmpegFinishJob,
    FFmpegFinishResult,
    FFprobeValidationReceipt,
    FrameSamplingReceipt,
    MemeticSoundCueModerationReceipt,
    MotionCueName,
    MotionVocabularyPolicyReceipt,
    PassStatus,
    RemotionRenderJob,
    RemotionRenderResult,
    RenderExecutionMode,
    RenderJobStatus,
    RenderLayerName,
    SevenLayerCompositionPayload,
    VideoFormatId,
)
from ccp_studio.services.audio_level_analysis_service import AudioLevelAnalysisService
from ccp_studio.services.duration_tolerance_service import DurationToleranceService
from ccp_studio.services.ffmpeg_finish_adapter_service import FFmpegFinishAdapterService
from ccp_studio.services.ffprobe_validation_service import FFprobeValidationService
from ccp_studio.services.frame_sampling_service import FrameSamplingService
from ccp_studio.services.render_qa_service import RenderQAService
from ccp_studio.services.remotion_ffmpeg_render_orchestrator_service import RemotionFFmpegRenderOrchestratorService
from ccp_studio.services.remotion_render_adapter_service import RemotionRenderAdapterService


def _wrapper():
    return CompleteEditingSessionRenderStateWrapper(
        complete_editing_session_ref="ces_1",
        brand_context_version_id="bcv_1",
        research_snapshot_refs=["research_1"],
        asset_manifest_refs=["asset_manifest_1"],
        scene_spec_refs=["scene_1"],
        composition_job_refs=["composition_1"],
        provider_job_receipt_refs=["provider_receipt_1"],
        evaluation_receipt_refs=["eval_1"],
    )


def _seven_layers():
    return SevenLayerCompositionPayload(
        layer_refs={
            RenderLayerName.BACKGROUND: ["background_layer"],
            RenderLayerName.PROOF_OBJECT: ["proof_layer"],
            RenderLayerName.REAL_LIFE_CUTOUT: ["cutout_layer"],
            RenderLayerName.AVATAR: ["avatar_layer"],
            RenderLayerName.TEXT: ["text_layer"],
            RenderLayerName.ANNOTATION: ["annotation_layer"],
            RenderLayerName.FOREGROUND_FX: ["fx_layer"],
        }
    )


def _motion_ok():
    return MotionVocabularyPolicyReceipt(
        requested_motion_cues=[MotionCueName.PAPER_SLIDE_IN, MotionCueName.AVATAR_GESTURE]
    )


def _sound_ok():
    return MemeticSoundCueModerationReceipt(
        format_id=VideoFormatId.FORMAT_02,
        cue_times_ms=[0, 31000],
    )


def _remotion_job(**overrides):
    data = dict(
        timeline_program_id="timeline_1",
        composition_id="Format02SceneComposition",
        entry_point="remotion/index.ts",
        output_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        input_props_ref="client_workspaces/demo/runs/run_1/timeline/props.json",
        complete_editing_session_state=_wrapper(),
        seven_layer_payload=_seven_layers(),
        motion_vocabulary_receipt=_motion_ok(),
        memetic_sound_receipt=_sound_ok(),
        duration_in_frames=720,
    )
    data.update(overrides)
    return RemotionRenderJob(**data)


def _ffmpeg_job(**overrides):
    data = dict(
        input_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        output_path="client_workspaces/demo/runs/run_1/exports/final.mp4",
    )
    data.update(overrides)
    return FFmpegFinishJob(**data)


def test_complete_editing_session_wrapper_requires_state_refs():
    with pytest.raises(Exception):
        CompleteEditingSessionRenderStateWrapper(
            complete_editing_session_ref="ces_1",
            brand_context_version_id="bcv_1",
            asset_manifest_refs=[],
            scene_spec_refs=["scene"],
            composition_job_refs=["composition"],
        )


def test_seven_layer_payload_requires_exact_layers():
    with pytest.raises(Exception):
        SevenLayerCompositionPayload(layer_refs={RenderLayerName.BACKGROUND: ["bg"]})


def test_motion_vocabulary_blocks_banned_cues():
    receipt = MotionVocabularyPolicyReceipt(requested_motion_cues=[MotionCueName.AI_LIQUID_MORPH])
    assert receipt.pass_status == PassStatus.FAIL
    assert "banned_motion_cues_requested" in receipt.blockers


def test_memetic_sound_spacing_format02_is_30_seconds():
    receipt = MemeticSoundCueModerationReceipt(format_id=VideoFormatId.FORMAT_02, cue_times_ms=[0, 10000])
    assert receipt.pass_status == PassStatus.FAIL


def test_memetic_sound_spacing_format04_is_10_seconds():
    receipt = MemeticSoundCueModerationReceipt(format_id=VideoFormatId.FORMAT_04, cue_times_ms=[0, 10000])
    assert receipt.pass_status == PassStatus.PASS


def test_remotion_job_blocks_provider_calls():
    with pytest.raises(Exception):
        _remotion_job(provider_calls_allowed=True)


def test_remotion_job_rejects_unsafe_paths():
    with pytest.raises(Exception):
        _remotion_job(output_path="../escape.mp4")


def test_remotion_real_local_requires_tested_capability_and_worker_lease():
    with pytest.raises(Exception):
        _remotion_job(execution_mode=RenderExecutionMode.REAL_LOCAL, runtime_capability_tested=False)


def test_remotion_dry_run_emits_hash_and_no_runtime_call():
    job = _remotion_job()
    result = RemotionRenderAdapterService().execute_dry_run(job)
    assert result.status == RenderJobStatus.SUCCEEDED
    assert result.output_sha256
    assert result.output_uri.startswith("dry-run://")
    assert not result.external_runtime_calls_executed


def test_remotion_real_local_execution_blocked_without_explicit_allow():
    job = _remotion_job(
        execution_mode=RenderExecutionMode.REAL_LOCAL,
        runtime_capability_tested=True,
        local_worker_lease_id="lease_1",
        allow_subprocess_execution=False,
    )
    plan = RemotionRenderAdapterService().compile_command_plan(job)
    assert plan.safe_for_execution is False


def test_ffmpeg_job_blocks_provider_calls_and_unsafe_path():
    with pytest.raises(Exception):
        _ffmpeg_job(provider_calls_allowed=True)
    with pytest.raises(Exception):
        _ffmpeg_job(output_path="../final.mp4")


def test_ffmpeg_real_local_requires_tested_capability_and_worker_lease():
    with pytest.raises(Exception):
        _ffmpeg_job(execution_mode=RenderExecutionMode.REAL_LOCAL, runtime_capability_tested=False)


def test_ffmpeg_dry_run_emits_hash_and_no_runtime_call():
    job = _ffmpeg_job()
    result = FFmpegFinishAdapterService().execute_dry_run(job)
    assert result.status == RenderJobStatus.SUCCEEDED
    assert result.output_sha256
    assert result.output_uri.startswith("dry-run://")
    assert not result.external_runtime_calls_executed


def test_dry_run_results_reject_external_runtime_flag():
    with pytest.raises(Exception):
        RemotionRenderResult(
            remotion_render_job_id="job",
            status=RenderJobStatus.SUCCEEDED,
            output_uri="dry-run://x.mp4",
            output_sha256="hash",
            dry_run=True,
            external_runtime_calls_executed=True,
        )
    with pytest.raises(Exception):
        FFmpegFinishResult(
            ffmpeg_finish_job_id="job",
            status=RenderJobStatus.SUCCEEDED,
            output_uri="dry-run://x.mp4",
            output_sha256="hash",
            dry_run=True,
            external_runtime_calls_executed=True,
        )


def test_ffprobe_validation_from_metadata_passes():
    receipt = FFprobeValidationService().validate_from_metadata(
        file_ref="final.mp4",
        metadata={"duration_ms": 24000, "width": 1080, "height": 1920, "fps": 30, "video_codec": "h264", "audio_codec": "aac"},
    )
    assert receipt.pass_status == PassStatus.PASS


def test_frame_sampling_fails_insufficient_samples():
    receipt = FrameSamplingService().compile_receipt(
        file_ref="final.mp4",
        sampled_frame_count=2,
        expected_scene_count=8,
    )
    assert receipt.pass_status == PassStatus.FAIL
    assert "insufficient_frame_samples" in receipt.blockers


def test_audio_level_analysis_fails_loudness_out_of_tolerance():
    receipt = AudioLevelAnalysisService().compile_receipt(
        file_ref="final.mp4",
        integrated_lufs=-24,
        true_peak_db=-2,
    )
    assert receipt.pass_status == PassStatus.FAIL
    assert "integrated_lufs_out_of_tolerance" in receipt.blockers


def test_duration_tolerance_fails_out_of_range():
    receipt = DurationToleranceService().compile_receipt(
        expected_duration_ms=24000,
        actual_duration_ms=26000,
        tolerance_ms=500,
    )
    assert receipt.pass_status == PassStatus.FAIL
    assert "duration_out_of_tolerance" in receipt.blockers


def test_render_qa_report_passes_when_all_receipts_pass():
    ffprobe = FFprobeValidationService().validate_from_metadata(
        file_ref="final.mp4",
        metadata={"duration_ms": 24000, "width": 1080, "height": 1920, "fps": 30, "video_codec": "h264", "audio_codec": "aac"},
    )
    frame = FrameSamplingService().compile_receipt(file_ref="final.mp4", sampled_frame_count=8, expected_scene_count=8)
    audio = AudioLevelAnalysisService().compile_receipt(file_ref="final.mp4", integrated_lufs=-14, true_peak_db=-1.5)
    duration = DurationToleranceService().compile_receipt(expected_duration_ms=24000, actual_duration_ms=24100)
    report = RenderQAService().compile_report(
        file_ref="final.mp4",
        ffprobe_validation=ffprobe,
        frame_sampling=frame,
        audio_level_analysis=audio,
        duration_tolerance=duration,
    )
    assert report.pass_status == PassStatus.PASS
    assert not report.blockers


def test_render_qa_report_fails_when_receipt_fails():
    ffprobe = FFprobeValidationReceipt(
        file_ref="final.mp4",
        duration_ms=24000,
        width=1080,
        height=1920,
        fps=30,
        video_codec="h264",
    )
    frame = FrameSamplingReceipt(file_ref="final.mp4", sampled_frame_count=1, expected_scene_count=8)
    audio = AudioLevelAnalysisReceipt(file_ref="final.mp4", integrated_lufs=-14, true_peak_db=-1.5)
    duration = DurationToleranceReceipt(expected_duration_ms=24000, actual_duration_ms=24000)
    report = RenderQAService().compile_report(
        file_ref="final.mp4",
        ffprobe_validation=ffprobe,
        frame_sampling=frame,
        audio_level_analysis=audio,
        duration_tolerance=duration,
    )
    assert report.pass_status == PassStatus.FAIL
    assert "insufficient_frame_samples" in report.blockers


def test_dry_run_orchestrator_compiles_remotion_and_ffmpeg_results():
    result = RemotionFFmpegRenderOrchestratorService().execute_dry_run_pipeline(
        remotion_job=_remotion_job(),
        ffmpeg_job=_ffmpeg_job(),
    )
    assert result["remotion_result"].output_sha256
    assert result["ffmpeg_result"].output_sha256
    assert result["remotion_result"].dry_run
    assert result["ffmpeg_result"].dry_run
