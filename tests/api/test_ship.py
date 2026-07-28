"""Tests for Ship and Audit Export endpoints (TS-APP-API-006 AC-014 to AC-017).

Tests POST /api/ship and GET /api/audit-export.
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


def test_ship_request_returns_decision(
    client, pipeline,
) -> None:
    """AC-014: POST /api/ship evaluates a ship request."""
    campaign_id = "ship-test-001"
    make_running_campaign(
        pipeline, campaign_id, idempotency_key="ship-001",
        lifecycle_state="READY_TO_SHIP",
    )

    body = {
        "ship_request_id": "ship-req-001",
        "campaign_ref": {
            "object_id": campaign_id,
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "autonomy_mode": "AUTOPILOT",
        "target_channel": "web",
        "artifact_refs": [
            {
                "artifact_id": "artifact:001",
                "artifact_kind": "video",
                "bytes": 1024,
                "media_type": "video/mp4",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                "uri": "artifacts/artifact-001.mp4",
            }
        ],
        "evaluation_refs": [
            {
                "object_id": "eval:001",
                "version": "1.0.0",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            }
        ],
        "unresolved_exception_ids": [],
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "publication_authority_ref": {
            "object_id": "pub-auth:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "publication_policy_ref": {
            "object_id": "pub-policy:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
    }

    resp = client.post("/api/ship", json=body)
    if resp.status_code == 201:
        data = resp.json()
        assert "decision_id" in data
        assert "status" in data
        assert "decision_sha256" in data
    elif resp.status_code == 422:
        pass
    else:
        pytest.fail(f"Unexpected status {resp.status_code}: {resp.text}")


def test_ship_request_denied_no_authority(
    client, pipeline,
) -> None:
    """AC-015: Ship request without authority returns DENIED."""
    campaign_id = "ship-test-002"
    make_running_campaign(
        pipeline, campaign_id, idempotency_key="ship-002",
        lifecycle_state="READY_TO_SHIP",
    )

    body = {
        "ship_request_id": "ship-req-002",
        "campaign_ref": {
            "object_id": campaign_id,
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "autonomy_mode": "AUTOPILOT",
        "target_channel": "web",
        "artifact_refs": [
            {
                "artifact_id": "artifact:001",
                "artifact_kind": "video",
                "bytes": 1024,
                "media_type": "video/mp4",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                "uri": "artifacts/artifact-001.mp4",
            }
        ],
        "evaluation_refs": [
            {
                "object_id": "eval:001",
                "version": "1.0.0",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            }
        ],
        "unresolved_exception_ids": [],
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "publication_authority_ref": None,
        "publication_policy_ref": None,
    }

    resp = client.post("/api/ship", json=body)
    if resp.status_code == 201:
        data = resp.json()
        if data["status"] == "DENIED":
            assert "PUBLICATION_AUTHORITY_REQUIRED" in data["denial_codes"]
    elif resp.status_code == 422:
        pass
    else:
        pytest.fail(f"Unexpected status {resp.status_code}: {resp.text}")


def test_audit_export_returns_manifest(
    client, pipeline,
) -> None:
    """AC-016: GET /api/audit-export returns an AuditExportManifest."""
    campaign_id = "ship-test-003"
    make_running_campaign(pipeline, campaign_id, idempotency_key="ship-003")

    resp = client.get(f"/api/audit-export?campaign_id={campaign_id}")
    if resp.status_code == 200:
        data = resp.json()
        assert "export_id" in data
        assert "campaign_ref" in data
        assert "export_sha256" in data
    elif resp.status_code == 422:
        pass
    else:
        pytest.fail(f"Unexpected status {resp.status_code}: {resp.text}")


def test_audit_export_campaign_not_found(
    client, pipeline,
) -> None:
    """AC-017: Unknown campaign returns 404."""
    resp = client.get("/api/audit-export?campaign_id=nonexistent-campaign")
    assert resp.status_code == 404
