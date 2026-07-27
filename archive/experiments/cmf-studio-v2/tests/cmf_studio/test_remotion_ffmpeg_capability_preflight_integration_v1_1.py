from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService


def test_remotion_ffmpeg_real_render_preflight_blocks_missing_runtime_stack():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.VIDEO_REAL_RENDER,
        remotion_configured=False,
        ffmpeg_configured=False,
        local_worker_configured=False,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert "runtime:render:remotion" in report.pipeline_status.missing_required_capability_ids
    assert "runtime:finish:ffmpeg" in report.pipeline_status.missing_required_capability_ids
    assert "runtime:worker:local_render_worker" in report.pipeline_status.missing_required_capability_ids
    assert report.provider_calls_executed is False
    assert report.runtime_calls_executed is False


def test_remotion_ffmpeg_real_render_preflight_passes_only_with_required_runtime_stack():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.VIDEO_REAL_RENDER,
        remotion_configured=True,
        remotion_available=True,
        ffmpeg_configured=True,
        ffmpeg_available=True,
        local_worker_configured=True,
        local_worker_available=True,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.PASS
    assert set(report.pipeline_status.available_required_capability_ids) == {
        "runtime:render:remotion",
        "runtime:finish:ffmpeg",
        "runtime:worker:local_render_worker",
    }
    assert report.provider_calls_executed is False
    assert report.runtime_calls_executed is False
