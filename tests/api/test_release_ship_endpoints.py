"""
test_release_ship_endpoints.py
------------------------------
Integration tests for Release / Ship / Outcome REST API endpoints.
"""

import hashlib
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def authentic_evidence() -> dict:
    quote = "Direct evidence of authentic production value."
    quote_sha = hashlib.sha256(quote.encode("utf-8")).hexdigest()
    return {
        "segment_id": "seg-001",
        "quote_text": quote,
        "evidence_quote_sha256": quote_sha,
        "speaker": "Speaker 1",
        "is_synthetic": False,
    }


def test_release_api_status(client: TestClient):
    """GET /api/release/status returns READY and state machine details."""
    resp = client.get("/api/release/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "READY"
    assert data["state_machine"] == "RELEASE_SHIP_OUTCOME_STATE_MACHINE_V1"


def test_release_api_e2e_flow(client: TestClient, workspace_id: str, authentic_evidence: dict):
    """Full E2E API flow: create session -> QA verify -> authorize -> ship -> capture outcome -> propose learning."""
    # 1. Create Session
    create_resp = client.post(
        "/api/release/sessions/create",
        json={
            "candidate_id": "cand-api-001",
            "workspace_id": workspace_id,
            "actor_id": "operator:lead",
            "artifact_ref": {"artifact_id": "art-001", "sha256": "a" * 64},
        },
    )
    assert create_resp.status_code == 201
    agg_data = create_resp.json()
    agg_id = agg_data["aggregate_id"]
    assert agg_data["current_state"] == "INITIAL"

    # 2. Verify Final QA (ANALYST)
    qa_resp = client.post(
        "/api/release/qa/verify",
        json={
            "aggregate_id": agg_id,
            "actor_id": "analyst:qa",
            "actor_lane": "ANALYST",
            "semantic_qa_result": {"passed": True, "fidelity": 0.99},
            "render_qa_result": {"passed": True, "format": "mp4"},
            "evidence_segment": authentic_evidence,
            "wrong_reading_locks": ["LOCK_1", "LOCK_2"],
            "is_synthetic": False,
        },
    )
    assert qa_resp.status_code == 200
    assert qa_resp.json()["status"] == "QA_VERIFIED"

    # 3. Authorize Release (COMMANDER)
    auth_resp = client.post(
        "/api/release/authorize",
        json={
            "aggregate_id": agg_id,
            "operator_id": "commander:lead",
            "actor_lane": "COMMANDER",
            "decision": "APPROVED",
            "target_channels": ["web"],
            "rationale": "Clearance granted.",
        },
    )
    assert auth_resp.status_code == 200
    assert auth_resp.json()["status"] == "RELEASE_AUTHORIZED"

    # 4. Execute Ship (COMPOSER)
    ship_resp = client.post(
        "/api/release/ship",
        json={
            "aggregate_id": agg_id,
            "actor_id": "composer:dispatcher",
            "actor_lane": "COMPOSER",
            "target_channel": "web",
            "delivery_endpoint": "https://cdn.example.com/asset.mp4",
        },
    )
    assert ship_resp.status_code == 200
    assert ship_resp.json()["status"] == "SHIPPED"

    # 5. Capture Outcome (HUNTER)
    outcome_resp = client.post(
        "/api/release/outcomes/capture",
        json={
            "aggregate_id": agg_id,
            "actor_id": "hunter:telemetry",
            "actor_lane": "HUNTER",
            "domain": "PERCEPTUAL",
            "metrics": {"views": 1200.0, "completion_rate": 0.8},
            "predicted_composite_score": 0.85,
            "observed_normalized_score": 0.88,
            "is_grounded": True,
            "misleading_context": False,
        },
    )
    assert outcome_resp.status_code == 200
    assert outcome_resp.json()["status"] == "OUTCOME_CAPTURED"

    # 6. Propose Learning (ANALYST)
    prop_resp = client.post(
        "/api/release/learning/propose",
        json={
            "aggregate_id": agg_id,
            "actor_id": "analyst:calibration",
            "actor_lane": "ANALYST",
            "min_recurrence": 1,
        },
    )
    assert prop_resp.status_code == 200
    assert prop_resp.json()["status"] == "LEARNING_PROPOSED"


def test_release_api_synthetic_blocked(client: TestClient, workspace_id: str, authentic_evidence: dict):
    """POST /api/release/qa/verify blocks synthetic candidate with 400 Bad Request."""
    create_resp = client.post(
        "/api/release/sessions/create",
        json={
            "candidate_id": "cand-syn-002",
            "workspace_id": workspace_id,
            "actor_id": "operator:lead",
            "artifact_ref": {"artifact_id": "art-002"},
        },
    )
    agg_id = create_resp.json()["aggregate_id"]

    qa_resp = client.post(
        "/api/release/qa/verify",
        json={
            "aggregate_id": agg_id,
            "actor_id": "analyst:qa",
            "actor_lane": "ANALYST",
            "semantic_qa_result": {"passed": True},
            "render_qa_result": {"passed": True},
            "evidence_segment": authentic_evidence,
            "wrong_reading_locks": ["LOCK_1"],
            "is_synthetic": True,
        },
    )
    assert qa_resp.status_code == 400
    assert "Synthetic production blocked" in qa_resp.json()["detail"]


def test_release_api_failed_ship_502(client: TestClient, workspace_id: str, authentic_evidence: dict):
    """POST /api/release/ship with simulated channel failure returns 502 Bad Gateway."""
    create_resp = client.post(
        "/api/release/sessions/create",
        json={
            "candidate_id": "cand-fail-002",
            "workspace_id": workspace_id,
            "actor_id": "operator:lead",
            "artifact_ref": {"artifact_id": "art-002"},
        },
    )
    agg_id = create_resp.json()["aggregate_id"]

    client.post(
        "/api/release/qa/verify",
        json={
            "aggregate_id": agg_id,
            "actor_id": "analyst:qa",
            "actor_lane": "ANALYST",
            "semantic_qa_result": {"passed": True},
            "render_qa_result": {"passed": True},
            "evidence_segment": authentic_evidence,
            "wrong_reading_locks": ["LOCK_1"],
        },
    )
    client.post(
        "/api/release/authorize",
        json={
            "aggregate_id": agg_id,
            "operator_id": "commander:lead",
            "actor_lane": "COMMANDER",
            "decision": "APPROVED",
            "target_channels": ["web"],
            "rationale": "Approved.",
        },
    )

    ship_resp = client.post(
        "/api/release/ship",
        json={
            "aggregate_id": agg_id,
            "actor_id": "composer:dispatcher",
            "actor_lane": "COMPOSER",
            "target_channel": "web",
            "delivery_endpoint": "https://cdn.example.com/asset.mp4",
            "simulate_channel_failure": True,
        },
    )
    assert ship_resp.status_code == 502
    assert "Shipment execution failed" in ship_resp.json()["detail"]
