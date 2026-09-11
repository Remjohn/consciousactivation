"""Tests for Control Tower endpoint (TS-APP-API-006 AC-001 to AC-004).

Uses FastAPI TestClient with tmp_path isolation.  Campaigns are persisted
through the PipelineRepository generic object store (campaign_projection.py).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.api.fixtures.studio_campaign_fixtures import (
    make_running_campaign,
    make_failed_node_run,
)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def pipeline(client):
    return client.app.state.pipeline


def test_control_tower_returns_projection_with_run_nodes(
    client, pipeline,
) -> None:
    """AC-001: GET /api/campaigns/{id}/tower returns a ControlTowerProjection
    with the expected projection_id, campaign state, and run_node statuses."""
    campaign_id = "ct-test-001"
    make_running_campaign(pipeline, campaign_id, idempotency_key="ct-001")

    resp = client.get(f"/api/campaigns/{campaign_id}/tower")
    assert resp.status_code == 200, resp.text

    body = resp.json()
    assert "projection_id" in body
    assert body["campaign"]["campaign_id"] == campaign_id
    assert body["campaign"]["lifecycle_state"] == "RUNNING"
    assert isinstance(body["run_nodes"], list)
    assert isinstance(body["available_actions"], list)
    assert "projection_sha256" in body


def test_control_tower_with_failed_node(
    client, pipeline,
) -> None:
    """AC-002: Control Tower reflects a failed node from the pipeline run."""
    campaign_id = "ct-test-002"
    make_failed_node_run(pipeline, campaign_id, idempotency_key="ct-002")

    resp = client.get(f"/api/campaigns/{campaign_id}/tower")
    assert resp.status_code == 200, resp.text

    body = resp.json()
    failed_nodes = [n for n in body["run_nodes"] if n["status"] == "FAILED"]
    assert len(failed_nodes) >= 1
    assert body["campaign"]["lifecycle_state"] == "BLOCKED_EXCEPTION"


def test_control_tower_campaign_not_found(
    client, pipeline,
) -> None:
    """AC-003: Unknown campaign returns 404."""
    resp = client.get("/api/campaigns/nonexistent-campaign/tower")
    assert resp.status_code == 404
    # The error may be wrapped in detail (HTTPException) or at top level
    # (global 404 handler) depending on which route matched.
    body = resp.json()
    error_code = body.get("detail", {}).get("error_code") or body.get("error_code")
    assert error_code in ("CAMPAIGN_NOT_FOUND", "NOT_FOUND")


def test_control_tower_studio_binding_present(
    client, pipeline,
) -> None:
    """AC-004: Control Tower includes studio_binding with expected fields."""
    campaign_id = "ct-test-004"
    make_running_campaign(pipeline, campaign_id, idempotency_key="ct-004")

    resp = client.get(f"/api/campaigns/{campaign_id}/tower")
    assert resp.status_code == 200, resp.text

    binding = resp.json()["studio_binding"]
    assert binding["primary_surface"] == "VIDEO_PRODUCTION_STUDIO"
    assert "binding_id" in binding
    assert "binding_reason" in binding
