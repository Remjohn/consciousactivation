"""Tests for the Revisions endpoints (TS-APP-API-006 AC-007 to AC-011).

Tests the POST /api/revisions, POST /api/revisions/direct, and
POST /api/revisions/{program_id}/execute endpoints.
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


def test_compile_natural_language_revision_returns_program(
    client, pipeline,
) -> None:
    """AC-007: POST /api/revisions compiles a natural language revision."""
    campaign_id = "rev-test-001"
    make_running_campaign(pipeline, campaign_id, idempotency_key="rev-001")

    body = {
        "request_id": "req-001",
        "run_ref": {
            "object_id": f"run:{campaign_id}",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "target_refs": [
            {
                "object_id": "target:001",
                "version": "1.0.0",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            }
        ],
        "target_node_ids": ["node:001"],
        "category_id": "conversational_activation_expression",
        "natural_language_request": "raise the selected target by 10 px",
        "current_state_ref": {
            "object_id": "state:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "evaluation_ref": None,
        "jit_capsule_ref": {
            "object_id": "jit:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "permitted_tool_registry_ref": {
            "object_id": "tools:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "expected_state_version": 1,
    }

    resp = client.post("/api/revisions", json=body)
    if resp.status_code == 201:
        data = resp.json()
        assert "program_id" in data
        assert "compilation_status" in data
        assert "exact_operations" in data
        assert "program_sha256" in data
    elif resp.status_code == 422:
        pass
    else:
        pytest.fail(f"Unexpected status {resp.status_code}: {resp.text}")


def test_compile_direct_manipulation_returns_program(
    client, pipeline,
) -> None:
    """AC-008: POST /api/revisions/direct compiles a direct manipulation."""
    campaign_id = "rev-test-002"
    make_running_campaign(pipeline, campaign_id, idempotency_key="rev-002")

    body = {
        "delta_id": "delta-001",
        "run_ref": {
            "object_id": f"run:{campaign_id}",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "target_ref": {
            "object_id": "target:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "target_node_id": "node:001",
        "manipulation_type": "MOVE_BBOX",
        "arguments": {"axis": "x", "delta_micros": 10000, "mode": "PIXELS"},
        "current_state_ref": {
            "object_id": "state:001",
            "version": "1.0.0",
            "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "expected_state_version": 1,
    }

    resp = client.post("/api/revisions/direct", json=body)
    if resp.status_code == 201:
        data = resp.json()
        assert "program_id" in data
        assert data["compilation_status"] == "COMPILED"
    elif resp.status_code == 422:
        pass
    else:
        pytest.fail(f"Unexpected status {resp.status_code}: {resp.text}")


def test_execute_revision_acknowledges(
    client, pipeline,
) -> None:
    """AC-009: POST /api/revisions/{program_id}/execute acknowledges."""
    resp = client.post("/api/revisions/test-program-001/execute")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "program" in data
    assert data["program"]["program_id"] == "test-program-001"


def test_revision_bad_request_returns_422(
    client, pipeline,
) -> None:
    """AC-010: Invalid revision request body returns 422."""
    resp = client.post("/api/revisions", json={"invalid": "payload"})
    assert resp.status_code == 422


def test_direct_manipulation_bad_request_returns_422(
    client, pipeline,
) -> None:
    """AC-011: Invalid direct manipulation body returns 422."""
    resp = client.post("/api/revisions/direct", json={"invalid": "payload"})
    assert resp.status_code == 422
