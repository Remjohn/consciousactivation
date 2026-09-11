"""Tests for the Timeline endpoint (TS-APP-API-006 AC-005, AC-006).

Uses the shared ``client`` fixture and ``make_running_campaign`` helper.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.api.fixtures.studio_campaign_fixtures import make_running_campaign


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


def test_timeline_returns_projection(
    client, pipeline,
) -> None:
    """AC-005: GET /api/campaigns/{id}/timeline returns a TimelineProjection."""
    campaign_id = "tl-test-001"
    make_running_campaign(pipeline, campaign_id, idempotency_key="tl-001")

    resp = client.get(f"/api/campaigns/{campaign_id}/timeline")
    assert resp.status_code == 200, resp.text

    body = resp.json()
    assert "projection_id" in body
    assert body["state"] == "READ_ONLY_CANONICAL_PROGRAM_PROJECTION"
    assert body["width"] == 1920
    assert body["height"] == 1080
    assert isinstance(body["tracks"], list)
    assert isinstance(body["items"], list)


def test_timeline_nonexistent_campaign(
    client, pipeline,
) -> None:
    """AC-006: Returns 404 for unknown campaign."""
    resp = client.get("/api/campaigns/nonexistent-campaign/timeline")
    assert resp.status_code == 404
