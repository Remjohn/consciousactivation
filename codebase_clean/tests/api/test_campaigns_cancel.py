"""Integration tests for POST /api/campaigns/{id}/cancel
— AC-013 (cancel LAUNCHED), AC-014 (cancel twice), AC-015 (stale version)."""

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
def launched_campaign(client, fixtures_dir):
    """Create a campaign at LAUNCHED, version 1."""
    pkg = _import_source_package(client, fixtures_dir)
    hr = _build_harness(client)
    body = _minimal_create_body(pkg, hr)
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# AC-013 — Cancel transitions LAUNCHED → CANCELLED
# ---------------------------------------------------------------------------

def test_cancel_launched_campaign(client, launched_campaign):
    cid = launched_campaign["state"]["campaign_id"]
    resp = client.post(
        f"/api/campaigns/{cid}/cancel",
        json={"expected_version": 1, "reason": "no longer needed"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["state"]["lifecycle_state"] == "CANCELLED"
    assert body["state"]["version"] == 2


# ---------------------------------------------------------------------------
# AC-014 — Cancel twice is rejected
# ---------------------------------------------------------------------------

def test_cancel_already_cancelled_rejected(client, launched_campaign):
    cid = launched_campaign["state"]["campaign_id"]
    # First cancel — succeeds
    r1 = client.post(
        f"/api/campaigns/{cid}/cancel",
        json={"expected_version": 1, "reason": "first cancel"},
    )
    assert r1.status_code == 200

    # Second cancel — rejected (CANCELLED cannot transition)
    r2 = client.post(
        f"/api/campaigns/{cid}/cancel",
        json={"expected_version": 2, "reason": "second cancel"},
    )
    assert r2.status_code == 409
    assert r2.json()["detail"]["error_code"] == "CAMPAIGN_TRANSITION_DENIED"


# ---------------------------------------------------------------------------
# AC-015 — Stale version on cancel is rejected
# ---------------------------------------------------------------------------

def test_cancel_stale_version_conflict(client, launched_campaign):
    cid = launched_campaign["state"]["campaign_id"]
    # Try to cancel with version=1 but we send version=99 (stale)
    resp = client.post(
        f"/api/campaigns/{cid}/cancel",
        json={"expected_version": 99, "reason": "stale"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["error_code"] == "CONFLICT"


# ---------------------------------------------------------------------------
# Additional cancel tests
# ---------------------------------------------------------------------------

def test_cancel_unknown_campaign_404(client):
    resp = client.post(
        "/api/campaigns/does-not-exist/cancel",
        json={"expected_version": 1, "reason": "test"},
    )
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "NOT_FOUND"


def test_cancel_returns_full_detail(client, launched_campaign):
    """Cancel response includes full CampaignDetailResponse."""
    cid = launched_campaign["state"]["campaign_id"]
    resp = client.post(
        f"/api/campaigns/{cid}/cancel",
        json={"expected_version": 1, "reason": "test"},
    )
    body = resp.json()
    assert "order" in body
    assert "state" in body
    assert "source_derivative_eligible" in body
    assert body["pipeline_ingestion_status"] == "NOT_YET_TRIGGERED"
