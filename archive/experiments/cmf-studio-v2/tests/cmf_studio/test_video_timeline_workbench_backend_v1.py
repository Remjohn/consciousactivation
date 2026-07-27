import pytest

try:
    import fastapi
    from fastapi.testclient import TestClient
except Exception:
    fastapi = None
    TestClient = None

from ccp_studio.api.v1.video_timeline_workbench import create_video_timeline_workbench_router
from ccp_studio.contracts.video_timeline_workbench import VideoTimelineWorkbenchReadModel
from ccp_studio.services.video_timeline_workbench_service import VideoTimelineWorkbenchService


def _client():
    if fastapi is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")
    app = fastapi.FastAPI()
    service = VideoTimelineWorkbenchService()
    app.include_router(create_video_timeline_workbench_router(service))
    return TestClient(app), service


def test_get_current_timeline_workbench_returns_read_model():
    client, _service = _client()
    response = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU")
    assert response.status_code == 200, response.text
    read_model = response.json()
    assert read_model["schema_version"] == "cmf.video_timeline_workbench_state.v1"
    assert read_model["program_id"]
    assert read_model["timeline_program_id"]
    assert read_model["frame_profile"] == "9:16_PAPERCUT_EXPLAINER"
    assert read_model["duration_ms"] > 0
    assert read_model["scenes"]
    assert read_model["tracks"]
    assert read_model["lanes"]
    assert read_model["source_mode"] in {"backend", "demo", "fixture"}


def test_read_model_preserves_brand_context_and_source_span_refs():
    service = VideoTimelineWorkbenchService()
    timeline = service.build_demo_format02_timeline(format_slot="SV-EDU")
    read_model = service.build_from_timeline(timeline, source_mode="backend", format_slot="SV-EDU")
    assert isinstance(read_model, VideoTimelineWorkbenchReadModel)
    assert read_model.brand_context_version_id == "bcv_health_demo_v1"
    assert read_model.source_span_refs == ["span_health_myth_1"]
    assert read_model.program_summary.source_span_refs == ["span_health_myth_1"]


def test_service_current_workbench_returns_demo_read_model():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-RRC")
    assert read_model.program_id
    assert read_model.timeline_program_id
    assert read_model.frame_profile == "9:16_CONSCIOUS_REACTION"
    assert read_model.duration_ms > 0
    assert read_model.scenes
    assert read_model.tracks
    assert read_model.source_mode == "demo"


def test_service_timeline_edit_propose_returns_typed_proposal():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    proposal = service.propose_timeline_edit(
        read_model.program_id,
        {
            "program_id": read_model.program_id,
            "target_segment_id": read_model.selected_segment_id,
            "edit_type": "request_repair",
            "expected_object_version": read_model.object_version,
            "payload": {"target": "timeline_integrity_review"},
        },
    )
    assert proposal.status == "proposed"
    assert proposal.typed_revision_command_id


def test_service_timeline_edit_submit_returns_typed_revision_receipt():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    receipt = service.submit_timeline_edit(
        read_model.program_id,
        {
            "command_id": "cmd_service_test_1",
            "draft_id": "draft_service_test_1",
            "program_id": read_model.program_id,
            "brand_workspace_id": read_model.brand_workspace_id,
            "guest_id": read_model.guest_id,
            "target_segment_id": read_model.selected_segment_id,
            "edit_type": "request_repair",
            "expected_object_version": read_model.object_version,
            "expected_renderer_props_hash": read_model.renderer_props_hash,
            "expected_scope_ref": f"{read_model.brand_workspace_id}:{read_model.guest_id}",
            "payload": {"target": "caption_review"},
            "submitted_by_operator_id": "operator_test",
        },
    )
    assert receipt.status == "receipted"
    assert receipt.command_id == "cmd_service_test_1"
    assert receipt.typed_revision_command_id
    assert receipt.revision_receipt_id
    assert receipt.applied is True


def test_service_proxy_render_returns_fake_receipt_hash_and_uri():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    receipt = service.create_proxy_render(read_model.program_id)
    assert receipt.fake_render is True
    assert receipt.output_uri.startswith(("fake://", "dry-run://"))
    assert receipt.output_sha256
    assert receipt.provider_calls_executed is False
    assert receipt.remotion_called is False
    assert receipt.ffmpeg_called is False
    assert receipt.timeline_program_id == read_model.timeline_program_id
    assert receipt.render_job_state.job_type == "proxy_video_render"
    assert receipt.render_job_state.job_status == "completed"
    assert receipt.render_qa.pass_status == "pass"


def test_service_otio_export_returns_audit_read_model():
    service = VideoTimelineWorkbenchService()
    read_model = service.get_current_workbench(format="SV-EDU")
    otio = service.export_otio(read_model.program_id)
    assert otio.timeline_program_id == read_model.timeline_program_id
    assert otio.otio_audit_timeline_id
    assert otio.tracks_summary
    assert otio.external_media_refs
    assert otio.file_written is False
    assert otio.provider_calls_executed is False
    assert otio.remotion_called is False
    assert otio.ffmpeg_called is False


def test_timeline_edit_propose_returns_typed_proposal():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()
    segment_id = read_model["selected_segment_id"]
    response = client.post(
        f"/api/v1/video-edit-programs/{read_model['program_id']}/timeline-edits/propose",
        json={
            "program_id": read_model["program_id"],
            "target_segment_id": segment_id,
            "edit_type": "request_repair",
            "expected_object_version": read_model["object_version"],
            "payload": {"target": "timeline_integrity_review"},
        },
    )
    assert response.status_code == 200, response.text
    proposal = response.json()
    assert proposal["status"] == "proposed"
    assert proposal["typed_revision_command_id"]
    assert proposal["target_segment_id"] == segment_id


def test_timeline_edit_submit_returns_typed_revision_receipt():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()
    response = client.post(
        f"/api/v1/video-edit-programs/{read_model['program_id']}/timeline-edits/submit",
        json={
            "command_id": "cmd_test_1",
            "draft_id": "draft_test_1",
            "program_id": read_model["program_id"],
            "brand_workspace_id": read_model["brand_workspace_id"],
            "guest_id": read_model["guest_id"],
            "target_segment_id": read_model["selected_segment_id"],
            "edit_type": "request_repair",
            "expected_object_version": read_model["object_version"],
            "expected_renderer_props_hash": read_model["renderer_props_hash"],
            "expected_scope_ref": f"{read_model['brand_workspace_id']}:{read_model['guest_id']}",
            "payload": {"target": "caption_review"},
            "submitted_by_operator_id": "operator_test",
        },
    )
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["status"] == "receipted"
    assert receipt["command_id"] == "cmd_test_1"
    assert receipt["typed_revision_command_id"]
    assert receipt["revision_receipt_id"]
    assert receipt["applied"] is True


def test_proxy_render_endpoint_returns_fake_proxy_receipt_hash_and_uri():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()
    response = client.post(f"/api/v1/video-edit-programs/{read_model['program_id']}/proxy-renders", json={})
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["fake_render"] is True
    assert receipt["output_uri"].startswith(("fake://", "dry-run://"))
    assert receipt["output_sha256"]
    assert receipt["provider_calls_executed"] is False
    assert receipt["remotion_called"] is False
    assert receipt["ffmpeg_called"] is False
    assert receipt["timeline_program_id"] == read_model["timeline_program_id"]
    assert receipt["render_job_state"]["job_type"] == "proxy_video_render"
    assert receipt["render_job_state"]["job_status"] == "completed"
    assert receipt["output_preview_url"] == receipt["output_uri"]
    assert receipt["render_qa"]["pass_status"] == "pass"


def test_otio_export_endpoint_returns_audit_timeline_read_model():
    client, _service = _client()
    read_model = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-EDU").json()
    response = client.post(f"/api/v1/video-edit-programs/{read_model['program_id']}/otio-exports", json={})
    assert response.status_code == 200, response.text
    otio = response.json()
    assert otio["timeline_program_id"] == read_model["timeline_program_id"]
    assert otio["otio_audit_timeline_id"]
    assert otio["tracks_summary"]
    assert otio["external_media_refs"]
    assert otio["otio_manifest_ref"].startswith("otio://audit/")
    assert otio["file_written"] is False
    assert otio["provider_calls_executed"] is False
    assert otio["remotion_called"] is False
    assert otio["ffmpeg_called"] is False


def test_backend_route_can_fetch_specific_program_workbench():
    client, _service = _client()
    current = client.get("/api/v1/video-edit-programs/current/timeline-workbench?format=SV-RRC").json()
    response = client.get(f"/api/v1/video-edit-programs/{current['program_id']}/timeline-workbench")
    assert response.status_code == 200, response.text
    assert response.json()["program_id"] == current["program_id"]
