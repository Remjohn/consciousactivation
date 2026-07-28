from __future__ import annotations

from fastapi.testclient import TestClient

from tests.api.fixtures.air_script_fixture import build_script_fixture


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def test_ac009_approve_then_get_shows_approved_but_batch_refs_still_incomplete(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac009")

        approve = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert approve.status_code == 200
        assert approve.json()["decision"] == "APPROVE"

        followup = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert followup.status_code == 200
        body = followup.json()
        assert body["operator_approved"] is True
        assert body["composition_eligible"] is True
        # Proves approval alone is honestly insufficient for a batch-ready
        # ref set (Source gap notice B) -- a transfer contract is separate.
        assert body["batch_compilation_refs"] == {"reason": "NO_TRANSFER_CONTRACT_YET"}


def test_ac010_approving_an_already_approved_script_returns_409(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac010")

        first = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert first.status_code == 200

        second = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert second.status_code == 409
        assert second.json()["detail"]["error_code"] == "ALREADY_APPROVED"
