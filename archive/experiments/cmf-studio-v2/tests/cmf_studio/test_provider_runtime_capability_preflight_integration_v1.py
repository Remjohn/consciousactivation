from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.contracts.provider_runtime import ProviderJobKind, ProviderName
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService
from ccp_studio.services.ideogram_provider_runtime_service import IdeogramProviderRuntimeService
from ccp_studio.services.provider_job_service import ProviderJobService


def test_ideogram_scene_sample_job_remains_fake_after_preflight_context():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=True,
        ideogram_available=True,
        flux_configured=True,
        flux_available=True,
        artifact_store_configured=True,
        artifact_store_available=True,
        batch_requested=False,
    )
    profile, job = IdeogramProviderRuntimeService().compile_scene_sample_job(
        {"composition_prompt": "paper cut scene plate"},
        ["format02_scene_1"],
    )
    output, receipt = ProviderJobService().fake_execute(job)

    assert report.provider_calls_executed is False
    assert profile.provider_name == ProviderName.IDEOGRAM
    assert job.job_kind == ProviderJobKind.SCENE_SAMPLE
    assert output.provider_calls_executed is False
    assert receipt.provider_calls_executed is False
    assert receipt.fake_execution is True


def test_provider_runtime_batch_remains_blocked_when_preflight_missing_ideogram_flux():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=False,
        flux_configured=False,
        artifact_store_configured=True,
        artifact_store_available=True,
        batch_requested=True,
        sample_approved=True,
    )

    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert "provider:image:ideogram" in report.pipeline_status.missing_required_capability_ids
    assert "provider:image:flux" in report.pipeline_status.missing_required_capability_ids
    assert report.provider_calls_executed is False
