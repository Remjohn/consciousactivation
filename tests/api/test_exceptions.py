"""Tests for the Exceptions endpoints (TS-APP-API-006 AC-012, AC-013).

Tests GET /api/campaigns/{id}/exceptions and
POST /api/campaigns/{id}/exceptions/resolve.
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


def test_list_exceptions_returns_list(
    client, pipeline,
) -> None:
    """AC-012: GET /api/campaigns/{id}/exceptions returns a list."""
    campaign_id = "exc-test-001"
    make_running_campaign(pipeline, campaign_id, idempotency_key="exc-001")

    resp = client.get(f"/api/campaigns/{campaign_id}/exceptions")
    assert resp.status_code == 200, resp.text
    assert isinstance(resp.json(), list)


def test_resolve_exception_returns_response(
    client, pipeline,
) -> None:
    """AC-013: POST /api/campaigns/{id}/exceptions/resolve returns response."""
    campaign_id = "exc-test-002"
    make_running_campaign(pipeline, campaign_id, idempotency_key="exc-002")

    body = {
        "package_id": "exception:001",
        "decision": "APPROVE",
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "campaign_ref": {
            "object_id": campaign_id,
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
    }

    resp = client.post(
        f"/api/campaigns/{campaign_id}/exceptions/resolve",
        json=body,
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "campaign" in data
    assert data["exception_resolved"] is True
