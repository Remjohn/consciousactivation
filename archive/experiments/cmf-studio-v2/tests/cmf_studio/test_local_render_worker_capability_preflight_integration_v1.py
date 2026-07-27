from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService


def test_local_worker_fake_capability_is_registered_without_real_runtime():
    worker = LocalRenderWorkerService().register_worker(
        worker_id="worker_preflight_demo",
        machine_id="machine_preflight_demo",
        display_name="Preflight Demo Worker",
    )

    fake_capability = worker.capabilities[0]
    assert fake_capability.capability_id == "runtime:python_fake"
    assert fake_capability.available
    assert RenderJobType.PROXY_VIDEO_RENDER in fake_capability.supports_job_types


def test_video_real_render_preflight_still_blocks_without_remotion_and_ffmpeg():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.VIDEO_REAL_RENDER,
        remotion_configured=False,
        ffmpeg_configured=False,
        local_worker_configured=True,
        local_worker_available=True,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert "runtime:render:remotion" in report.pipeline_status.missing_required_capability_ids
    assert "runtime:finish:ffmpeg" in report.pipeline_status.missing_required_capability_ids
    assert "runtime:worker:local_render_worker" not in report.pipeline_status.missing_required_capability_ids
    assert report.runtime_calls_executed is False


def test_video_real_render_preflight_passes_only_when_runtime_requirements_are_available():
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
    assert report.pipeline_status.missing_required_capability_ids == []
    assert report.runtime_calls_executed is False
