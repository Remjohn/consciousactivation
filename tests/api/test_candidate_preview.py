from __future__ import annotations

from tests.api.fixtures.studio_campaign_fixtures import make_running_campaign

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(api_app):
    with TestClient(api_app) as test_client:
        yield test_client


@pytest.fixture()
def pipeline(client):
    return client.app.state.pipeline


OPERATOR = {
    "actor_id": "operator:test",
    "actor_type": "human",
    "product_id": "conscious-activations-studio",
    "workflow_role": "operator",
}


def _candidate(cid: str, rank: int, *, fit: int = 9500, rights: str = "CLEARED") -> dict:
    return {
        "candidate_id": cid,
        "media_type": "VIDEO_CLIP",
        "preview_uri": f"https://media.test/{cid}.mp4",
        "transcript_context": "Operational turning point in context.",
        "source_ref": {"object_id": f"asset:{cid}", "version": "7", "sha256": "a" * 64},
        "source_range_ms": [1000, 5000],
        "duration_ms": 4000,
        "rights_state": rights,
        "confidence_bps": 9500,
        "semantic_fit_bps": fit,
        "quality_bps": 9000,
        "ranking": rank,
        "eligible": True,
        "eligibility_reasons": [],
        "provenance": {"candidate_id": cid, "scene_id": "SCN-1", "source_version": "7", "source_sha256": "a" * 64},
        "source_quality_state": "HIGH",
    }


def _campaign_with_timeline(pipeline, campaign_id: str):
    state = make_running_campaign(pipeline, campaign_id, idempotency_key=campaign_id)
    state["video_edit_program"] = {
        "width": 1920,
        "height": 1080,
        "fps_numerator": 30,
        "fps_denominator": 1,
        "duration_frames": 300,
        "items": [{
            "item_id": "node-1",
            "source_ref": {"object_id": "asset:old", "version": "1", "sha256": "b" * 64},
            "start_frame": 0,
            "end_frame": 120,
            "editable_operations": ["SUBSTITUTE_ASSET"],
        }],
        "tracks": [],
    }
    state["version"] = int(state.get("version", 1)) + 1
    from api.services.campaign_projection import save_campaign_state
    return save_campaign_state(pipeline, campaign_id, state, idempotency_key=f"{campaign_id}:timeline", expected_revision=1)


def test_candidate_preview_session_navigation_rejection_and_auto_accept(client, pipeline):
    campaign_id = "m0087-api-flow"
    _campaign_with_timeline(pipeline, campaign_id)
    body = {
        "workspace_id": "workspace:test",
        "request_ref": {"object_id": "req:1", "version": "1", "sha256": "c" * 64},
        "target_ref": {"object_id": "asset:old", "version": "1", "sha256": "b" * 64},
        "target_node_id": "node-1",
        "candidates": [_candidate("AST-1", 1), _candidate("AST-2", 2)],
    }
    created = client.post(f"/api/visual-studio/campaigns/{campaign_id}/candidate-sessions", json=body)
    assert created.status_code == 200, created.text
    session = created.json()["session"]
    session_id = session["session_id"]
    assert created.json()["current_candidate"]["candidate_id"] == "AST-1"

    moved = client.post(f"/api/visual-studio/candidate-sessions/{session_id}/navigate", json={"direction": "NEXT", "expected_version": session["version"]})
    assert moved.status_code == 200, moved.text
    assert moved.json()["current_candidate"]["candidate_id"] == "AST-2"

    accepted = client.post(f"/api/visual-studio/candidate-sessions/{session_id}/decisions", json={
        "candidate_id": "AST-2", "decision": "AUTO_ACCEPT", "expected_version": moved.json()["session"]["version"]
    })
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["decision_receipt"]["auto_selection_policy"] == "visual-candidate-auto-accept-v1"
    assert accepted.json()["decision_receipt"]["revision_ref"]["object_id"] == f"studio-campaign-state:{campaign_id}"

    promoted = client.post(f"/api/visual-studio/candidate-sessions/{session_id}/promote", json={
        "expected_version": accepted.json()["session"]["version"], "operator_actor": OPERATOR
    })
    assert promoted.status_code == 200, promoted.text
    assert promoted.json()["session"]["status"] == "PROMOTED"
    assert promoted.json()["campaign"]["version"] == 3


def test_candidate_preview_blocks_good_looking_wrong_auto_accept(client, pipeline):
    campaign_id = "m0087-api-block"
    _campaign_with_timeline(pipeline, campaign_id)
    body = {
        "workspace_id": "workspace:test",
        "request_ref": {"object_id": "req:2", "version": "1", "sha256": "c" * 64},
        "target_ref": {"object_id": "asset:old", "version": "1", "sha256": "b" * 64},
        "target_node_id": "node-1",
        "candidates": [_candidate("AST-WRONG", 1, fit=6200)],
    }
    created = client.post(f"/api/visual-studio/campaigns/{campaign_id}/candidate-sessions", json=body)
    assert created.status_code == 200, created.text
    session = created.json()["session"]
    blocked = client.post(f"/api/visual-studio/candidate-sessions/{session['session_id']}/decisions", json={
        "candidate_id": "AST-WRONG", "decision": "AUTO_ACCEPT", "expected_version": session["version"]
    })
    assert blocked.status_code == 422
    assert blocked.json()["detail"]["error_code"] == "AUTO_ACCEPT_BLOCKED"


def test_candidate_preview_reject_requires_operator_and_preserves_lineage(client, pipeline):
    campaign_id = "m0087-api-reject"
    _campaign_with_timeline(pipeline, campaign_id)
    body = {
        "workspace_id": "workspace:test",
        "request_ref": {"object_id": "req:3", "version": "1", "sha256": "c" * 64},
        "target_ref": {"object_id": "asset:old", "version": "1", "sha256": "b" * 64},
        "target_node_id": "node-1",
        "candidates": [_candidate("AST-REJECT", 1)],
    }
    created = client.post(f"/api/visual-studio/campaigns/{campaign_id}/candidate-sessions", json=body)
    session = created.json()["session"]
    blocked = client.post(f"/api/visual-studio/candidate-sessions/{session['session_id']}/decisions", json={
        "candidate_id": "AST-REJECT", "decision": "REJECT", "expected_version": session["version"], "operator_actor": {"actor_type": "model"}, "rationale": "wrong"
    })
    assert blocked.status_code == 422
    rejected = client.post(f"/api/visual-studio/candidate-sessions/{session['session_id']}/decisions", json={
        "candidate_id": "AST-REJECT", "decision": "REJECT", "expected_version": session["version"], "operator_actor": OPERATOR, "rationale": "Wrong semantic reading."
    })
    assert rejected.status_code == 200, rejected.text
    assert "AST-REJECT" in rejected.json()["session"]["rejected_candidate_ids"]
    assert rejected.json()["decision_receipt"]["rejected_candidates"][0]["candidate_id"] == "AST-REJECT"
