from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    CompleteEditingSessionRenderStateWrapper,
    FFmpegFinishJob,
    MemeticSoundCueModerationReceipt,
    MotionCueName,
    MotionVocabularyPolicyReceipt,
    RemotionRenderJob,
    RenderLayerName,
    SevenLayerCompositionPayload,
    VideoFormatId,
)
from ccp_studio.contracts.video_editing_engine import FinalRenderContract, RemotionInputProps
from ccp_studio.services.audio_level_analysis_service import AudioLevelAnalysisService
from ccp_studio.services.duration_tolerance_service import DurationToleranceService
from ccp_studio.services.ffmpeg_finish_adapter_service import FFmpegFinishAdapterService
from ccp_studio.services.ffprobe_validation_service import FFprobeValidationService
from ccp_studio.services.frame_sampling_service import FrameSamplingService
from ccp_studio.services.render_qa_service import RenderQAService
from ccp_studio.services.remotion_ffmpeg_render_orchestrator_service import RemotionFFmpegRenderOrchestratorService
from ccp_studio.services.remotion_render_adapter_service import RemotionRenderAdapterService


def test_video_engine_props_can_map_to_dry_run_remotion_ffmpeg_and_render_qa():
    remotion_props = RemotionInputProps(
        timeline_program_id="timeline_video_engine_mapping",
        input_props={"timeline_program_id": "timeline_video_engine_mapping"},
    )
    final_contract = FinalRenderContract(
        timeline_program_id="timeline_video_engine_mapping",
        timeline_locked=True,
        asset_hashes={"asset_manifest_video_engine_mapping": "hash_123"},
    )
    wrapper = CompleteEditingSessionRenderStateWrapper(
        complete_editing_session_ref="ces_video_engine_mapping",
        brand_context_version_id="bcv_video_engine_mapping",
        research_snapshot_refs=["research_snapshot_video_engine_mapping"],
        asset_manifest_refs=["asset_manifest_video_engine_mapping"],
        scene_spec_refs=["scene_spec_video_engine_mapping"],
        composition_job_refs=["composition_job_video_engine_mapping"],
        provider_job_receipt_refs=["provider_receipt_video_engine_mapping"],
        evaluation_receipt_refs=["eval_receipt_video_engine_mapping"],
    )
    seven_layers = SevenLayerCompositionPayload(
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

    remotion_job = RemotionRenderJob(
        timeline_program_id=remotion_props.timeline_program_id,
        composition_id="Format02SceneComposition",
        entry_point="remotion/index.ts",
        output_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        input_props_ref=remotion_props.remotion_input_props_id,
        complete_editing_session_state=wrapper,
        seven_layer_payload=seven_layers,
        motion_vocabulary_receipt=MotionVocabularyPolicyReceipt(
            requested_motion_cues=[MotionCueName.PAPER_SLIDE_IN, MotionCueName.AVATAR_GESTURE]
        ),
        memetic_sound_receipt=MemeticSoundCueModerationReceipt(
            format_id=VideoFormatId.FORMAT_02,
            cue_times_ms=[0, 31000],
        ),
        duration_in_frames=720,
    )
    ffmpeg_job = FFmpegFinishJob(
        input_path="client_workspaces/demo/runs/run_1/renders/proxy.mp4",
        output_path="client_workspaces/demo/runs/run_1/exports/final.mp4",
    )

    dry_run = RemotionFFmpegRenderOrchestratorService(
        remotion_service=RemotionRenderAdapterService(),
        ffmpeg_service=FFmpegFinishAdapterService(),
    ).execute_dry_run_pipeline(remotion_job=remotion_job, ffmpeg_job=ffmpeg_job)

    ffprobe = FFprobeValidationService().validate_from_metadata(
        file_ref=final_contract.final_render_contract_id,
        metadata={
            "duration_ms": 24000,
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "video_codec": "h264",
            "audio_codec": "aac",
        },
    )
    frame = FrameSamplingService().compile_receipt(
        file_ref=final_contract.final_render_contract_id,
        sampled_frame_count=8,
        expected_scene_count=8,
    )
    audio = AudioLevelAnalysisService().compile_receipt(
        file_ref=final_contract.final_render_contract_id,
        integrated_lufs=-14,
        true_peak_db=-1.5,
    )
    duration = DurationToleranceService().compile_receipt(
        expected_duration_ms=24000,
        actual_duration_ms=24100,
    )
    qa_report = RenderQAService().compile_report(
        file_ref=final_contract.final_render_contract_id,
        ffprobe_validation=ffprobe,
        frame_sampling=frame,
        audio_level_analysis=audio,
        duration_tolerance=duration,
    )

    assert dry_run["remotion_result"].dry_run is True
    assert dry_run["ffmpeg_result"].dry_run is True
    assert dry_run["remotion_result"].external_runtime_calls_executed is False
    assert dry_run["ffmpeg_result"].external_runtime_calls_executed is False
    assert qa_report.pass_status.value == "pass"
