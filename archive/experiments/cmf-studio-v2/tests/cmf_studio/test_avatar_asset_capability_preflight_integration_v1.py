from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.services.avatar_asset_production_service import AvatarAssetProductionService
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService


def test_avatar_asset_manifest_stack_compiles_without_runtime_preflight():
    spec = AvatarAssetProductionService().create_character_spec(
        avatar_id="coach_avatar_v1",
        brand_id="brand_avatar_demo",
        brand_context_version_id="bcv_avatar_demo_v1",
    )
    stack = AvatarAssetProductionService().compile_default_asset_stack(spec)

    assert "No Stretchy Studio runtime call executed" in stack["stretchy_studio_import_manifest"].notes
    assert stack["action_timeline"].lip_sync_enabled is False


def test_avatar_64_state_generation_blocks_missing_ideogram_and_flux():
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
    assert report.provider_calls_executed is False
    assert report.runtime_calls_executed is False


def test_avatar_64_state_generation_sample_first_gate_blocks_batch():
    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION,
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
    assert report.runtime_calls_executed is False
