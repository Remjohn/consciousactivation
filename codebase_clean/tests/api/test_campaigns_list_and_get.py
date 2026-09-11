"""Integration tests for GET /api/campaigns and GET /api/campaigns/{id}
— AC-011 (list/filter) and AC-012 (detail 404)."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from tests.api.test_campaigns_create import (
    _build_harness,
    _import_source_package,
    _minimal_create_body,
)

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def campaign1(client, fixtures_dir):
    """Create one campaign in workspace:acme-coach."""
    pkg = _import_source_package(client, fixtures_dir)
    hr = _build_harness(client)
    body = _minimal_create_body(pkg, hr, workspace_id="workspace:acme-coach", project_id="project:q3")
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.fixture()
def campaign2(client, fixtures_dir):
    """Create a second campaign in a different workspace."""
    pkg = _import_source_package(client, fixtures_dir)
    hr = _build_harness(client)
    body = _minimal_create_body(pkg, hr, workspace_id="workspace:other", project_id="project:other")
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# AC-011 — List and filter
# ---------------------------------------------------------------------------

class TestListCampaigns:
    def test_list_all_returns_all(self, client, campaign1, campaign2):
        resp = client.get("/api/campaigns")
        assert resp.status_code == 200
        ids = [c["campaign_id"] for c in resp.json()]
        assert campaign1["state"]["campaign_id"] in ids
        assert campaign2["state"]["campaign_id"] in ids

    def test_filter_by_workspace(self, client, campaign1, campaign2):
        resp = client.get("/api/campaigns?workspace_id=workspace:acme-coach")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 1
        assert body[0]["campaign_id"] == campaign1["state"]["campaign_id"]

    def test_filter_by_project(self, client, campaign1):
        resp = client.get("/api/campaigns?project_id=project:q3")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_filter_by_lifecycle_state(self, client, campaign1):
        resp = client.get("/api/campaigns?lifecycle_state=LAUNCHED")
        assert resp.status_code == 200
        assert all(c["lifecycle_state"] == "LAUNCHED" for c in resp.json())

    def test_empty_filter_returns_empty(self, client):
        resp = client.get("/api/campaigns?workspace_id=workspace:nonexistent")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_summaries(self, client, campaign1):
        resp = client.get("/api/campaigns")
        item = resp.json()[0]
        # CampaignSummary fields, not the full detail
        assert "order" not in item
        assert "state" not in item
        assert "campaign_id" in item
        assert "lifecycle_state" in item
        assert "output_target_count" in item


# ---------------------------------------------------------------------------
# AC-012 — Detail for unknown campaign
# ---------------------------------------------------------------------------

class TestGetCampaign:
    def test_get_unknown_campaign_404(self, client):
        resp = client.get("/api/campaigns/does-not-exist")
        assert resp.status_code == 404
        assert resp.json()["error_code"] == "NOT_FOUND"

    def test_get_known_campaign(self, client, campaign1):
        cid = campaign1["state"]["campaign_id"]
        resp = client.get(f"/api/campaigns/{cid}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["state"]["campaign_id"] == cid
        assert "order" in body
        assert "source_derivative_eligible" in body
        assert body["pipeline_ingestion_status"] == "NOT_YET_TRIGGERED"
