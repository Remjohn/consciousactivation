import pytest

from ccp_studio.contracts.capability_preflight import (
    CapabilityKind,
    CapabilityState,
    PipelineId,
    PreflightPassStatus,
    ProviderAvailabilityReport,
    ProviderName,
    ProviderRole,
    RuntimeAvailabilityReport,
    RuntimeName,
    SetupOffer,
    ToolSupportEnvelope,
)
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService
from ccp_studio.services.provider_menu_service import ProviderMenuService
from ccp_studio.services.runtime_availability_service import RuntimeAvailabilityService
from ccp_studio.services.tool_support_registry_service import ToolSupportRegistryService


def test_tool_support_envelope_rejects_available_without_configured():
    with pytest.raises(Exception):
        ToolSupportEnvelope(
            capability_id="runtime:render:remotion",
            kind=CapabilityKind.RUNTIME,
            display_name="Remotion",
            configured=False,
            available=True,
        )


def test_tool_support_envelope_does_not_execute_providers_or_runtimes():
    with pytest.raises(Exception):
        ToolSupportEnvelope(
            capability_id="provider:image:ideogram",
            kind=CapabilityKind.PROVIDER,
            display_name="Ideogram",
            configured=True,
            available=True,
            provider_calls_executed=True,
        )


def test_provider_availability_rejects_missing_secrets_when_available():
    with pytest.raises(Exception):
        ProviderAvailabilityReport(
            provider_name=ProviderName.IDEOGRAM,
            provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR,
            capability_id="provider:image:ideogram",
            configured=True,
            available=True,
            missing_secrets=["IDEOGRAM_API_KEY"],
        )


def test_provider_menu_counts_configured_missing_degraded_and_estimates_cost():
    service = ProviderMenuService()
    reports = [
        service.compile_provider_report(
            provider_name=ProviderName.IDEOGRAM,
            provider_role=ProviderRole.COMPOSITION_PLATE_GENERATOR,
            capability_id="provider:image:ideogram",
            configured=True,
            available=True,
            min_cost_usd=0.1,
            max_cost_usd=0.2,
            sample_required=True,
            sample_approved=True,
        ),
        service.compile_provider_report(
            provider_name=ProviderName.FLUX,
            provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
            capability_id="provider:image:flux",
            configured=False,
            available=False,
            missing_secrets=["BFL_API_KEY"],
            min_cost_usd=0.1,
            max_cost_usd=0.3,
        ),
    ]
    menu = service.compile_menu(reports)
    assert menu.configured_count == 1
    assert menu.available_count == 1
    assert menu.missing_count == 1
    assert menu.estimated_cost_max_usd == pytest.approx(0.5)


def test_sample_first_policy_blocks_batch_until_sample_approved():
    menu = ProviderMenuService().compile_default_provider_menu(
        ideogram_configured=True,
        ideogram_available=True,
        flux_configured=True,
        flux_available=True,
        sample_approved=False,
        batch_requested=True,
    )
    assert menu.blocked_count == 2
    assert menu.sample_required
    assert not menu.sample_approved


def test_runtime_availability_rejects_available_without_configured():
    with pytest.raises(Exception):
        RuntimeAvailabilityReport(
            runtime_name=RuntimeName.REMOTION,
            capability_id="runtime:render:remotion",
            configured=False,
            available=True,
        )


def test_runtime_availability_service_reports_missing_remotion_and_ffmpeg():
    reports = RuntimeAvailabilityService().compile_default_runtime_reports(
        remotion_configured=False,
        remotion_available=False,
        ffmpeg_configured=False,
        ffmpeg_available=False,
    )
    by_cap = {report.capability_id: report for report in reports}
    assert by_cap["runtime:render:remotion"].status == CapabilityState.MISSING
    assert by_cap["runtime:finish:ffmpeg"].status == CapabilityState.MISSING
    assert by_cap["runtime:python"].status == CapabilityState.AVAILABLE


def test_setup_offer_requires_steps():
    with pytest.raises(Exception):
        SetupOffer(capability_id="provider:image:ideogram", title="Configure", steps=[])


def test_tool_support_registry_returns_requirements_for_avatar_64_state_generation():
    required = ToolSupportRegistryService().required_capabilities_for_pipeline(PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION)
    assert "provider:image:ideogram" in required
    assert "provider:image:flux" in required
    assert "tool:storage:artifact_store" in required


def test_preflight_blocks_avatar_library_generation_when_providers_missing():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION,
        ideogram_configured=False,
        flux_configured=False,
        artifact_store_configured=True,
        artifact_store_available=True,
    )
    assert report.pipeline_status.pass_status == PreflightPassStatus.BLOCKED
    assert "provider:image:ideogram" in report.pipeline_status.missing_required_capability_ids
    assert "provider:image:flux" in report.pipeline_status.missing_required_capability_ids
    assert report.missing_blockers


def test_preflight_passes_for_format02_golden_path_fake_runtime():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
        artifact_store_configured=True,
        artifact_store_available=True,
    )
    assert report.pipeline_status.pass_status in {PreflightPassStatus.PASS, PreflightPassStatus.DEGRADED}
    assert "runtime:python" in report.pipeline_status.available_required_capability_ids
    assert not report.provider_calls_executed
    assert not report.runtime_calls_executed


def test_preflight_blocks_real_video_render_without_local_worker_and_runtimes():
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


def test_preflight_blocks_provider_batch_until_sample_approved_even_if_configured():
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


def test_preflight_passes_provider_batch_when_sample_approved():
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
    assert report.provider_menu_summary.sample_approved


def test_preflight_degraded_when_optional_runtime_missing():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
        artifact_store_configured=True,
        artifact_store_available=True,
        remotion_configured=False,
        ffmpeg_configured=False,
    )
    assert report.pipeline_status.pass_status == PreflightPassStatus.DEGRADED
    assert "runtime:render:remotion" in report.pipeline_status.optional_missing_capability_ids


def test_preflight_report_total_cost_matches_provider_menu():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
        ideogram_configured=True,
        ideogram_available=True,
        flux_configured=True,
        flux_available=True,
        artifact_store_configured=True,
        artifact_store_available=True,
        sample_approved=True,
    )
    assert report.total_estimated_cost.max_usd == report.provider_menu_summary.estimated_cost_max_usd
    assert report.total_estimated_cost.min_usd == report.provider_menu_summary.estimated_cost_min_usd
