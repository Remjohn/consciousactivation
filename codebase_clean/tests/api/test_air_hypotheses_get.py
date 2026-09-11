from __future__ import annotations

from fastapi.testclient import TestClient

from tests.api.fixtures.air_portfolio_fixture import build_portfolio_fixture
from tests.api.fixtures.air_script_fixture import build_script_fixture


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def test_ac001_get_portfolio_returns_populated_candidates_and_404_for_unknown(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac001")

        response = client.get(f"/api/air/hypotheses/{fx['portfolio_id']}")
        assert response.status_code == 200
        body = response.json()
        assert body["portfolio_state"] == "OPEN"
        assert len(body["candidates"]) == 3
        for candidate in body["candidates"]:
            assert candidate["psychological_role"]
            assert candidate["tension"]
            assert candidate["diversity_signature"]["axes"]
            assert candidate["diversity_signature"]["proof_sha256"]

        missing = client.get("/api/air/hypotheses/does-not-exist")
        assert missing.status_code == 404
        # NOTE: this app's global 404 handler (api/errors.py::not_found_handler,
        # registered by status code in api/main.py) overrides every 404 body
        # with a generic error_code -- it does not preserve the route's own
        # PORTFOLIO_NOT_FOUND detail. See tests/api/test_health.py's own
        # test_unknown_service_returns_404 for the same, pre-existing behavior.
        assert missing.json()["error_code"] == "NOT_FOUND"


def test_ac002_get_portfolio_wrong_object_type_returns_404_not_500(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        script_fx = build_script_fixture(air, prefix="ac002")

        # script_fx['script_id'] resolves to a final_script_package, not a
        # activation_hypothesis_portfolio -- must be 404, not 500/400.
        response = client.get(f"/api/air/hypotheses/{script_fx['script_id']}")
        assert response.status_code == 404
        assert response.json()["error_code"] == "NOT_FOUND"
