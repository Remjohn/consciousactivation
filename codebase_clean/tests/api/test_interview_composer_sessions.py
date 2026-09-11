from __future__ import annotations

import json
from fastapi.testclient import TestClient
from tests.api.interview_composer_helpers import seed_brand_and_voice, stored_ref
from tests.api.test_interview_composer_research import (
    _brief_payload, _research_package, _valid_questions, _valid_seed, _error_code,
)


def _make_brief(client: TestClient, *, guest_name: str = "Session Guest") -> dict:
    """Create a research package + brief and return the brief JSON."""
    air = client.app.state.air
    brand, voice = seed_brand_and_voice(air)
    brand_ref = stored_ref(brand)
    voice_ref = stored_ref(voice)
    research = _research_package(client, guest_name=guest_name)
    response = client.post(
        "/api/interviews/compose/brief",
        json=_brief_payload(research["research_package_id"], brand_ref, voice_ref, guest_name),
        headers={"Idempotency-Key": f"brief:{guest_name}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_ac009_session_creation_reuses_real_air_data(api_app):
    """AC-009: Session creation reuses real AIR data (compile_relationship_program)."""
    with TestClient(api_app) as client:
        brief = _make_brief(client, guest_name="Session Guest")
        response = client.post(
            "/api/interviews/compose/sessions",
            json={
                "brief_id": brief["brief_id"],
                "recording_date": "2026-08-15",
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            headers={"Idempotency-Key": "session:ac009"},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["session_id"].startswith("ic:session:")
        assert body["stage"] == "ENGAGED"
        assert body["recording_date"] == "2026-08-15"

        # The relationship_state_ref / progression_ref must resolve to real,
        # stored AIR objects.
        air = client.app.state.air
        state_ref = body["relationship_state_ref"]
        program_ref = body["progression_ref"]
        state = air.repository.get_object(state_ref["object_id"])
        assert state.object_type == "relationship_activation_state"
        program = air.repository.get_object(program_ref["object_id"])
        assert program.object_type == "reelcast_progression_program"


def test_ac010_session_non_existent_brief(api_app):
    """AC-010: Session against a non-existent brief returns 404."""
    with TestClient(api_app) as client:
        response = client.post(
            "/api/interviews/compose/sessions",
            json={
                "brief_id": "ic:brief:nonexistent",
                "recording_date": None,
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            headers={"Idempotency-Key": "session:ac010"},
        )
        assert response.status_code == 404, response.text
        assert _error_code(response) == "NOT_FOUND"


def test_session_get(api_app):
    """Verify GET /sessions/{id} returns the stored session."""
    with TestClient(api_app) as client:
        brief = _make_brief(client, guest_name="Get Session")
        create = client.post(
            "/api/interviews/compose/sessions",
            json={
                "brief_id": brief["brief_id"],
                "recording_date": None,
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            headers={"Idempotency-Key": "session:get"},
        )
        assert create.status_code == 201
        session_id = create.json()["session_id"]

        get = client.get(f"/api/interviews/compose/sessions/{session_id}")
        assert get.status_code == 200
        assert get.json()["session_id"] == session_id
        assert get.json()["stage"] == "ENGAGED"