from ccp_studio.contracts.render_qa import PassStatus
from ccp_studio.services.audio_level_analysis_service import AudioLevelAnalysisService
from ccp_studio.services.duration_tolerance_service import DurationToleranceService
from ccp_studio.services.ffprobe_validation_service import FFprobeValidationService
from ccp_studio.services.frame_sampling_service import FrameSamplingService
from ccp_studio.services.render_qa_adapter_bridge_service import RenderQAAdapterBridgeService
from ccp_studio.services.render_qa_service import RenderQAService


def test_adapter_receipts_bridge_to_render_qa_without_runtime_calls():
    file_ref = "workspace://renders/proxy.mp4"
    adapter_report = RenderQAService().compile_report(
        file_ref=file_ref,
        ffprobe_validation=FFprobeValidationService().validate_from_metadata(
            file_ref=file_ref,
            metadata={
                "duration_ms": 24000,
                "width": 1080,
                "height": 1920,
                "fps": 30,
                "video_codec": "h264",
                "audio_codec": "aac",
            },
        ),
        frame_sampling=FrameSamplingService().compile_receipt(
            file_ref=file_ref,
            sampled_frame_count=8,
            expected_scene_count=8,
        ),
        audio_level_analysis=AudioLevelAnalysisService().compile_receipt(
            file_ref=file_ref,
            integrated_lufs=-14,
            true_peak_db=-1.5,
        ),
        duration_tolerance=DurationToleranceService().compile_receipt(
            expected_duration_ms=24000,
            actual_duration_ms=24000,
        ),
    )
    promise = RenderQAService().promise_profile(
        delivery_id="delivery_proxy",
        expected_width=1080,
        expected_height=1920,
        expected_duration_ms=24000,
    )
    bridge = RenderQAAdapterBridgeService()
    report = bridge.composite_from_adapter_report(adapter_report=adapter_report, promise_profile=promise)
    assert report.pass_status == PassStatus.PASS
    assert bridge.external_tool_calls_executed is False
    assert bridge.provider_calls_executed is False
    assert bridge.local_worker_jobs_executed is False


def test_adapter_duration_mismatch_fails_delivery_promise():
    file_ref = "workspace://renders/final.mp4"
    adapter_report = RenderQAService().compile_report(
        file_ref=file_ref,
        ffprobe_validation=FFprobeValidationService().validate_from_metadata(
            file_ref=file_ref,
            metadata={
                "duration_ms": 26000,
                "width": 1080,
                "height": 1920,
                "fps": 30,
                "video_codec": "h264",
                "audio_codec": "aac",
            },
        ),
        frame_sampling=FrameSamplingService().compile_receipt(
            file_ref=file_ref,
            sampled_frame_count=8,
            expected_scene_count=8,
        ),
        audio_level_analysis=AudioLevelAnalysisService().compile_receipt(
            file_ref=file_ref,
            integrated_lufs=-14,
            true_peak_db=-1.5,
        ),
        duration_tolerance=DurationToleranceService().compile_receipt(
            expected_duration_ms=24000,
            actual_duration_ms=26000,
            tolerance_ms=500,
        ),
    )
    promise = RenderQAService().promise_profile(
        delivery_id="delivery_final",
        expected_width=1080,
        expected_height=1920,
        expected_duration_ms=24000,
    )
    report = RenderQAAdapterBridgeService().composite_from_adapter_report(
        adapter_report=adapter_report,
        promise_profile=promise,
    )
    codes = {blocker.code for blocker in report.blockers}
    assert report.pass_status == PassStatus.FAIL
    assert "delivery_duration_out_of_tolerance" in codes
