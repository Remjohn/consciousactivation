from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def api_app(tmp_path, monkeypatch):
    """Point the gateway at an isolated CA_DATA_ROOT for this test only."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    # api.main is imported lazily so the env vars above are set before
    # api.config.load_config() runs at lifespan startup.
    from api.main import app

    return app


def test_lifespan_initialises_all_services(api_app):
    """AC-001: server starts cleanly and every service initialises."""
    with TestClient(api_app) as client:
        response = client.get("/api/health")
        assert response.status_code in (200, 503), (
            f"server should start and answer, got connection-level failure instead: {response.status_code}"
        )


def test_app_state_has_all_service_objects(api_app):
    with TestClient(api_app) as client:
        assert client.app.state.pipeline is not None
        assert client.app.state.air is not None
        assert client.app.state.vae is not None
        assert client.app.state.interview is not None
        assert client.app.state.builder is not None
        assert client.app.state.builder_repository is not None


def test_service_databases_created_under_data_root(api_app, tmp_path):
    with TestClient(api_app):
        state_dir = tmp_path / "state"
        assert (state_dir / "pipeline.db").exists()
        assert (state_dir / "air.db").exists()
        assert (state_dir / "vae.db").exists()
        assert (state_dir / "interview.db").exists()
        assert (state_dir / "builder.db").exists()
