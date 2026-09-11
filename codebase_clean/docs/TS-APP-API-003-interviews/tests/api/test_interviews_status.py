from __future__ import annotations
from fastapi.testclient import TestClient


def _post_import(client, fixtures_dir, *, workspace_id, project_id):
    with open(fixtures_dir / "synthetic_interview.mp4", "rb") as video, \
         open(fixtures_dir / "sample_transcript.srt", "rb") as transcript:
        return client.post(
            "/api/interviews/import",
            files={"video": ("interview.mp4", video, "video/mp4"), "transcript": ("t.srt", transcript, "text/plain")},
            data={
                "workspace_id": workspace_id, "project_id": project_id, "operator_id": "op-1",
                "authority_scope": "DEVELOPMENT_TEST", "assertion_id": "assert-1",
                "transcript_format": "SRT", "speaker_id": "guest",
            },
        )


def test_unknown_package_returns_404(api_app, fixtures_dir):
    """AC-009: GET status for a package_id that was never admitted returns
    404 NOT_FOUND."""
    with TestClient(api_app) as client:
        response = client.get("/api/interviews/ie:source-package:0000000000000000000000000000000000000000000000000000000000000000/status")
        assert response.status_code == 404, response.text
        assert response.json()["error_code"] == "NOT_FOUND"


def test_status_reflects_bound_components(api_app, fixtures_dir):
    """AC-010: after a real /import, GET status reflects the actual bound
    component slots -- the three components /import binds show BOUND with a
    ref, and a component /import never touches (expression_moments) still
    shows PENDING_REQUIRED_COMPONENT."""
    with TestClient(api_app) as client:
        imported = _post_import(client, fixtures_dir, workspace_id="ws-10", project_id="prj-10")
        assert imported.status_code == 201, imported.text
        package_id = imported.json()["package_id"]

        response = client.get(f"/api/interviews/{package_id}/status")
        assert response.status_code == 200, response.text
        body = response.json()
        components = body["components"]
        for name in ("transcript_alignment", "packed_phrase_transcript", "visual_structure_index"):
            assert components[name]["state"] == "BOUND", components[name]
            assert components[name]["ref"]["object_id"]
        assert components["expression_moments"]["state"] == "PENDING_REQUIRED_COMPONENT"
        assert body["derivative_eligible"] is False
        assert len(body["media_assets"]) == 1
