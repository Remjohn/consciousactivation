import pytest

try:
    import fastapi
    from fastapi.testclient import TestClient
except Exception:
    fastapi = None
    TestClient = None

from ccp_studio.api.v1.pipeline_run_monitor import create_pipeline_run_monitor_router
from ccp_studio.contracts.pipeline_run_monitor import PipelineRunMonitorReadModel
from ccp_studio.services.pipeline_run_monitor_service import PipelineRunMonitorService


def _client():
    if fastapi is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")
    app = fastapi.FastAPI()
    service = PipelineRunMonitorService()
    app.include_router(create_pipeline_run_monitor_router(service))
    return TestClient(app), service


def _demo_monitor(service: PipelineRunMonitorService | None = None) -> PipelineRunMonitorReadModel:
    service = service or PipelineRunMonitorService()
    runs = service.list_runs()
    assert runs
    return service.get_run_monitor(runs[0].pipeline_run_id)


def test_list_runs_returns_run_status_read_models():
    service = PipelineRunMonitorService()
    runs = service.list_runs()
    assert runs
    run = runs[0]
    assert run.pipeline_run_id
    assert run.recipe_id == "format02_golden_path"
    assert run.brand_context_version_id == "bcv_health_myth_demo_v1"
    assert run.orchestration_run_id == "orch_format02_pipeline_monitor_demo"
    assert run.source_mode in {"backend", "fixture", "synthetic"}


def test_get_run_monitor_returns_receipts_artifacts_blockers_and_approvals():
    monitor = _demo_monitor()
    assert monitor.run_status.pipeline_run_id
    assert monitor.stage_receipts
    assert monitor.artifacts
    assert monitor.blockers
    assert monitor.approvals
    assert monitor.scene_output_links
    assert monitor.summary


def test_stage_receipt_pass_fail_state_is_preserved():
    monitor = _demo_monitor()
    receipt_by_step = {receipt.step_id: receipt for receipt in monitor.stage_receipts}
    assert receipt_by_step["source_intake"].pass_status == "pass"
    assert receipt_by_step["provider_samples"].pass_status == "fail"
    assert receipt_by_step["provider_samples"].receipt_id


def test_blockers_are_surfaced():
    monitor = _demo_monitor()
    assert monitor.blockers[0].code == "approval_gate_not_approved"
    assert monitor.blockers[0].severity == "blocking"
    assert monitor.blockers[0].step_id == "provider_samples"


def test_pending_approvals_are_surfaced():
    monitor = _demo_monitor()
    approval_by_gate = {approval.gate_id: approval for approval in monitor.approvals}
    assert approval_by_gate["provider_sample_first"].status == "pending"
    assert approval_by_gate["provider_sample_first"].required_sample_types == [
        "scene_sample",
        "face_plate_sample",
        "template_preview_sample",
    ]
    assert "face_plate_sample" in approval_by_gate["provider_sample_first"].pending_reason


def test_artifacts_are_pointer_refs_without_raw_bytes():
    monitor = _demo_monitor()
    assert monitor.artifacts
    assert all(artifact.storage_state == "pointer_only" for artifact in monitor.artifacts)
    assert all(artifact.raw_bytes_included is False for artifact in monitor.artifacts)
    assert all(artifact.uri for artifact in monitor.artifacts)


def test_scene_output_links_include_template_preview_when_template_artifact_exists():
    monitor = _demo_monitor()
    scene_link = monitor.scene_output_links[0]
    assert scene_link.template_preview_url == "/template-preview/format02_scene_01"
    assert scene_link.status == "preview_available"


def test_scene_output_links_include_video_preview_when_timeline_artifact_exists():
    monitor = _demo_monitor()
    scene_link = monitor.scene_output_links[0]
    assert scene_link.video_preview_url == "/timeline?program_id=timeline_health_myth_demo"


def test_golden_path_detail_read_model_uses_format02_recipe():
    service = PipelineRunMonitorService()
    monitor = _demo_monitor(service)
    detail = service.get_golden_path_detail(monitor.run_status.golden_path_run_id)
    assert detail.recipe_id == "format02_golden_path"
    assert detail.golden_path_run_id == "golden_path_health_myth_demo"
    assert detail.pipeline_run_id == monitor.run_status.pipeline_run_id
    assert detail.composition_scene_outputs
    assert detail.timeline_outputs


def test_golden_path_detail_preserves_brand_context_version_id():
    service = PipelineRunMonitorService()
    monitor = _demo_monitor(service)
    detail = service.get_golden_path_detail(monitor.run_status.golden_path_run_id)
    assert detail.brand_context_version_id == "bcv_health_myth_demo_v1"


def test_monitor_does_not_call_providers_renderers_or_workers():
    monitor = _demo_monitor()
    assert monitor.provider_calls_executed is False
    assert monitor.renderer_calls_executed is False
    assert monitor.local_worker_jobs_executed is False


def test_golden_path_detail_does_not_execute_runtime_systems():
    service = PipelineRunMonitorService()
    monitor = _demo_monitor(service)
    detail = service.get_golden_path_detail(monitor.run_status.golden_path_run_id)
    assert detail.provider_calls_executed is False
    assert detail.renderer_calls_executed is False
    assert detail.local_worker_jobs_executed is False


def test_http_routes_list_get_monitor_scene_outputs_and_golden_path_detail():
    client, _service = _client()
    list_response = client.get("/api/v1/pipeline-runs")
    assert list_response.status_code == 200, list_response.text
    runs = list_response.json()
    assert runs

    pipeline_run_id = runs[0]["pipeline_run_id"]
    monitor_response = client.get(f"/api/v1/pipeline-runs/{pipeline_run_id}")
    assert monitor_response.status_code == 200, monitor_response.text
    monitor = monitor_response.json()
    assert monitor["run_status"]["pipeline_run_id"] == pipeline_run_id
    assert monitor["stage_receipts"]
    assert monitor["artifacts"]

    scene_response = client.get(f"/api/v1/pipeline-runs/{pipeline_run_id}/scene-outputs")
    assert scene_response.status_code == 200, scene_response.text
    assert scene_response.json()[0]["template_preview_url"]

    golden_path_run_id = monitor["run_status"]["golden_path_run_id"]
    detail_response = client.get(f"/api/v1/golden-path-runs/{golden_path_run_id}")
    assert detail_response.status_code == 200, detail_response.text
    detail = detail_response.json()
    assert detail["recipe_id"] == "format02_golden_path"
    assert detail["brand_context_version_id"] == "bcv_health_myth_demo_v1"
