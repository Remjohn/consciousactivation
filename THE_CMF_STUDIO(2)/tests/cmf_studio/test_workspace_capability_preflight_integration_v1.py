from ccp_studio.contracts.capability_preflight import PipelineId, PreflightPassStatus
from ccp_studio.contracts.project_workspace_artifact_store import PassStatus
from ccp_studio.services.capability_preflight_service import CapabilityPreflightService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService


def test_materialized_workspace_satisfies_capability_preflight_artifact_store(tmp_path):
    workspace_service = ClientWorkspaceService()
    workspace = workspace_service.create_workspace(
        client_id="client_1",
        client_slug="client-one",
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    materialization = workspace_service.materialize_workspace(workspace, base_dir=tmp_path)

    report = CapabilityPreflightService().run_preflight(
        pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
        artifact_store_configured=materialization.pass_status == PassStatus.PASS,
        artifact_store_available=(tmp_path / workspace.workspace_relative_path).exists(),
    )

    assert report.pipeline_status.pass_status in {PreflightPassStatus.PASS, PreflightPassStatus.DEGRADED}
    assert "tool:storage:artifact_store" not in report.pipeline_status.missing_required_capability_ids
    assert not any(blocker.capability_id == "tool:storage:artifact_store" for blocker in report.missing_blockers)
    assert not report.provider_calls_executed
    assert not report.runtime_calls_executed
