from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService


def test_format02_provider_scene_batch_blocks_missing_ideogram_and_flux():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=False,
        flux_configured=False,
        artifact_store_configured=True,
        artifact_store_available=True,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert "provider:image:ideogram" in report.pipeline_status.missing_required_capability_ids
    assert "provider:image:flux" in report.pipeline_status.missing_required_capability_ids
    assert report.provider_calls_executed is False


def test_format02_provider_scene_batch_blocks_batch_before_sample_approval():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=True,
        ideogram_available=True,
        flux_configured=True,
        flux_available=True,
        artifact_store_configured=True,
        artifact_store_available=True,
        batch_requested=True,
        sample_approved=False,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert report.pipeline_status.batch_blocked
    assert any(blocker.capability_id == "sample_approval" for blocker in report.missing_blockers)
    assert report.provider_calls_executed is False


def test_format02_provider_scene_batch_passes_after_sample_approval():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=True,
        ideogram_available=True,
        flux_configured=True,
        flux_available=True,
        artifact_store_configured=True,
        artifact_store_available=True,
        batch_requested=True,
        sample_approved=True,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.PASS
    assert report.provider_menu_summary.available_count == 2
    assert report.provider_calls_executed is False
