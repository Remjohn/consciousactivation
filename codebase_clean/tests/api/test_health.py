from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app

    with TestClient(app) as c:
        yield c


def test_all_services_healthy(client):
    """AC-002."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert set(data["services"].keys()) == {"pipeline", "air", "vae", "interview", "builder"}
    for name, item in data["services"].items():
        assert item["integrity"] == "ok", f"{name} not healthy: {item}"


def test_per_service_health(client):
    """AC-003 (valid name)."""
    response = client.get("/api/health/pipeline")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "pipeline"
    assert data["integrity"] == "ok"


def test_unknown_service_returns_404(client):
    """AC-003 (invalid name)."""
    response = client.get("/api/health/unknown")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "NOT_FOUND"


def test_degraded_on_service_failure(client, tmp_path):
    """AC-004.

    "Deliberately set to an unwritable location" is simulated by pointing the
    pipeline repository's database path at a location where an *intermediate
    path segment is a regular file*, not a directory permissions bit. A plain
    chmod 000 does not reliably fail here because test suites (and this
    container) commonly run as root, which ignores Unix permission bits;
    trying to create a directory or file underneath an existing plain file
    fails regardless of uid.
    """
    blocked_file = tmp_path / "not_a_directory"
    blocked_file.write_text("blocking pipeline.db from being created underneath this")
    client.app.state.pipeline.repository.path = blocked_file / "pipeline.db"

    response = client.get("/api/health")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert data["services"]["pipeline"]["integrity"] == "error"
    for name in ("air", "vae", "interview", "builder"):
        assert data["services"][name]["integrity"] == "ok", (
            f"{name} should be unaffected by the pipeline failure: {data['services'][name]}"
        )


def test_cors_headers(client):
    """AC-005.

    Starlette's CORSMiddleware only emits preflight headers when both `Origin`
    and `Access-Control-Request-Method` are present on an OPTIONS request --
    without the latter it is treated as a normal (non-preflight) request.
    """
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_error_response_shape(client):
    """Validates ErrorResponse schema on 404."""
    response = client.get("/api/health/unknown")
    assert response.status_code == 404
    data = response.json()
    assert set(data.keys()) == {"error_code", "message", "service", "timestamp"}
    assert data["error_code"] == "NOT_FOUND"
    assert isinstance(data["message"], str) and data["message"]
    assert data["service"] == "unknown"
    assert isinstance(data["timestamp"], str) and data["timestamp"]
