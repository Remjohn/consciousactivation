import pytest

try:
    import fastapi
    from fastapi.testclient import TestClient
except Exception:
    fastapi = None
    TestClient = None

from ccp_studio.api.v1.video_timeline_workbench import create_video_timeline_workbench_router
from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.services.video_timeline_workbench_service import VideoTimelineWorkbenchService


def _client():
    if fastapi is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")
    app = fastapi.FastAPI()
    service = VideoTimelineWorkbenchService()
    app.include_router(create_video_timeline_workbench_router(service))
    return TestClient(app), service


def test_proxy_render_service_creates_leases_and_completes_local_worker_job():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")

    response = service.create_proxy_render(read_model.program_id)
    state = response.render_job_state

    assert state.program_id == read_model.program_id
    assert state.timeline_program_id == read_model.timeline_program_id
    assert state.job_type == RenderJobType.PROXY_VIDEO_RENDER.value
    assert state.job_status == "completed"
    assert state.worker_id == "video_workbench_fake_worker"
    assert state.lease_id
    assert state.result_id
    assert {"created", "queued", "leased", "heartbeat", "completed"}.issubset(set(state.lifecycle_events))


def test_proxy_render_service_returns_output_preview_url_and_safe_execution_flags():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")

    response = service.create_proxy_render(read_model.program_id)

    assert response.output_preview_url.startswith(("fake://", "dry-run://"))
    assert response.output_uri == response.output_preview_url
    assert response.render_job_state.output_uri == response.output_preview_url
    assert response.provider_calls_executed is False
    assert response.render_job_state.provider_calls_executed is False
    assert response.render_job_state.external_runtime_calls_executed is False
    assert response.remotion_called is False
    assert response.ffmpeg_called is False


def test_proxy_render_service_attaches_passing_synthetic_render_qa():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")

    response = service.create_proxy_render(read_model.program_id)
    qa = response.render_qa

    assert qa.render_qa_report_id
    assert qa.pass_status == "pass"
    assert qa.blockers == []
    assert qa.ffprobe_status == "pass"
    assert qa.frame_sampling_status == "pass"
    assert qa.audio_level_status == "pass"
    assert qa.duration_tolerance_status == "pass"
    assert qa.duration_ms == read_model.duration_ms
    assert qa.width == 1080
    assert qa.height == 1920
    assert qa.fps == read_model.fps


def test_proxy_render_updates_current_workbench_read_model_state():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    response = service.create_proxy_render(read_model.program_id)

    updated = service.get_workbench(read_model.program_id)
    assert updated.output_preview_url == response.output_preview_url
    assert updated.proxy_render_ref == response.output_preview_url
    assert updated.last_render_job_state.render_job_id == response.render_job_state.render_job_id
    assert updated.last_render_qa.render_qa_report_id == response.render_qa.render_qa_report_id
    assert updated.render_summaries[0].render_type == "proxy"
    assert updated.render_summaries[0].output_uri == response.output_preview_url


def test_proxy_render_does_not_trigger_final_render_or_real_runtime_calls():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    response = service.create_proxy_render(read_model.program_id)

    assert response.render_job_state.job_type == "proxy_video_render"
    assert response.render_job_state.dry_run is True
    assert response.render_job_state.fake_result is True
    assert response.render_job_state.external_runtime_calls_executed is False
    assert response.render_job_state.provider_calls_executed is False


def test_proxy_render_endpoint_returns_render_job_state_output_preview_and_qa():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()

    response = client.post(f"/api/v1/video-edit-programs/{read_model['program_id']}/proxy-renders", json={})
    assert response.status_code == 200, response.text
    payload = response.json()

    assert payload["timeline_program_id"] == read_model["timeline_program_id"]
    assert payload["render_job_state"]["job_type"] == "proxy_video_render"
    assert payload["render_job_state"]["job_status"] == "completed"
    assert payload["output_preview_url"].startswith(("fake://", "dry-run://"))
    assert payload["render_qa"]["pass_status"] == "pass"
    assert payload["source_mode"] in {"backend", "dry_run", "fake"}


def test_render_job_state_endpoint_returns_stored_state():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()
    render_response = client.post(f"/api/v1/video-edit-programs/{read_model['program_id']}/proxy-renders", json={}).json()

    state_response = client.get(
        f"/api/v1/video-edit-programs/{read_model['program_id']}/render-jobs/{render_response['render_job_state']['render_job_id']}"
    )
    assert state_response.status_code == 200, state_response.text
    state = state_response.json()
    assert state["render_job_id"] == render_response["render_job_state"]["render_job_id"]
    assert state["timeline_program_id"] == read_model["timeline_program_id"]
    assert state["external_runtime_calls_executed"] is False
