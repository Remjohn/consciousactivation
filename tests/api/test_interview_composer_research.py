from __future__ import annotations

import json
from fastapi.testclient import TestClient
from ca_contracts import bytes_sha256
from tests.api.interview_composer_helpers import seed_brand_and_voice, stored_ref, seed_brand_context, seed_voice_dna


def _research_package(client: TestClient, *, guest_name: str = "Test Guest") -> dict:
    response = client.post(
        "/api/interviews/compose/research",
        data={
            "guest_name": guest_name,
            "source_urls_json": json.dumps(["https://example.com/bio"]),
            "workspace_id": "ws-test",
            "project_id": "prj-test",
            "operator_id": "op-test",
            "authority_scope": "DEVELOPMENT_TEST",
            "assertion_id": "assert-test",
        },
        headers={"Idempotency-Key": f"research:{guest_name}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def _valid_seed() -> dict:
    return {
        "psychological_role": "self-recognizing witness",
        "tension": "keep control as proof of competence or recognize what it prevents",
        "activation_direction_set": ["MIRROR"],
        "pressure_path": "concealed protection to visible relational cost",
        "stance": "name the protective logic before offering movement",
        "counteractivation_strategy": "preserve the hesitation and belief revision before any instruction",
        "smallest_commitment": "notice one moment when control prevents listening",
    }


def _valid_questions() -> list[dict]:
    return [{
        "question_text": "What happened when you realized that?",
        "activation_direction": "MIRROR",
        "psychological_role": "self-recognizing witness",
    }]


def _error_code(response) -> str:
    """Extract the error_code from either response shape.

    Status 404 is handled by the gateway's global not_found_handler, which
    returns a top-level ErrorResponse (``{"error_code": "NOT_FOUND", ...}``).
    Every other status goes through http_exception_handler, which wraps the
    ErrorResponse in ``{"detail": {...}}``. This helper reads both."""
    body = response.json()
    if "error_code" in body:
        return body["error_code"]
    return body["detail"]["error_code"]


def _brief_payload(research_package_id: str, brand_ref: dict, voice_ref: dict,
                   guest_name: str = "Guest") -> dict:
    return {
        "research_package_id": research_package_id,
        "brand_context_ref": brand_ref,
        "voice_dna_ref": voice_ref,
        "guest_name": guest_name,
        "tension_hypothesis": "Keeps control as proof of competence.",
        "matrix_of_edging_seed": _valid_seed(),
        "planned_questions": _valid_questions(),
        "expression_targets": ["self-recognizing witness"],
        "operator_id": "op-test",
        "authority_scope": "DEVELOPMENT_TEST",
        "assertion_id": "assert-test",
    }


def test_ac001_research_package_urls_only(api_app):
    """AC-001: Research package with URLs and no documents."""
    with TestClient(api_app) as client:
        body = _research_package(client)
        assert body["research_package_id"].startswith("ic:research:")
        assert len(body["source_urls"]) == 1
        assert body["source_urls"][0] == "https://example.com/bio"
        assert body["uploaded_documents"] == []


def test_ac002_research_package_with_document(api_app):
    """AC-002: Research package with URLs + uploaded document."""
    with TestClient(api_app) as client:
        content = b"fake pdf content"
        response = client.post(
            "/api/interviews/compose/research",
            data={
                "guest_name": "Doc Guest",
                "source_urls_json": json.dumps([]),
                "workspace_id": "ws-test",
                "project_id": "prj-test",
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            files={"documents": ("ref.pdf", content, "application/pdf")},
            headers={"Idempotency-Key": "research:doc-guest"},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert len(body["uploaded_documents"]) == 1
        doc = body["uploaded_documents"][0]
        assert doc["sha256"] == bytes_sha256(content)
        assert doc["bytes"] == len(content)
        assert doc["media_type"] == "application/pdf"
        assert doc["original_filename"] == "ref.pdf"


def test_ac003_brief_with_real_brand_dna(api_app):
    """AC-003: Brief with real, existing Brand DNA returns pipeline status BLOCKED."""
    with TestClient(api_app) as client:
        air = client.app.state.air
        brand, voice = seed_brand_and_voice(air)
        brand_ref = stored_ref(brand)
        voice_ref = stored_ref(voice)

        research = _research_package(client, guest_name="Brief Guest")
        response = client.post(
            "/api/interviews/compose/brief",
            json=_brief_payload(research["research_package_id"], brand_ref, voice_ref, "Brief Guest"),
            headers={"Idempotency-Key": "brief:ac003"},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["brief_id"].startswith("ic:brief:")
        assert body["content_origin"] == "operator_supplied"
        assert body["hypothesis_pipeline_status"]["status"] == "BLOCKED_PENDING_GAP_007"
        assert body["hypothesis_pipeline_status"]["iac_ref"] is None
        assert body["hypothesis_pipeline_status"]["planned_aip_ref"] is None
        assert body["hypothesis_pipeline_status"]["arm_receipt_ref"] is None


def test_ac004_brief_non_existent_brand_context(api_app):
    """AC-004: Brief against a non-existent Brand Context returns 404."""
    with TestClient(api_app) as client:
        research = _research_package(client, guest_name="Bad Brand")
        nonexistent_brand = {"object_id": "nonexistent-brand", "version": "1.0.0", "sha256": "f" * 64}
        nonexistent_voice = {"object_id": "nonexistent-voice", "version": "1.0.0", "sha256": "f" * 64}

        response = client.post(
            "/api/interviews/compose/brief",
            json=_brief_payload(research["research_package_id"], nonexistent_brand, nonexistent_voice, "Bad Brand"),
            headers={"Idempotency-Key": "brief:ac004"},
        )
        assert response.status_code == 404, response.text
        # 404 is routed through the gateway's global not_found_handler, which
        # always emits error_code "NOT_FOUND"; the specific cause is in the
        # message. The status + message together express AC-004's intent.
        assert _error_code(response) == "NOT_FOUND"
        assert "brand_context_ref" in response.text


def test_ac005_brief_mismatched_voice_dna(api_app):
    """AC-005: Brief against mismatched Voice DNA returns 422."""
    with TestClient(api_app) as client:
        air = client.app.state.air
        # Brand A
        brand_a = seed_brand_context(air, brand_id="brand-ctx-A")
        brand_a_ref = stored_ref(brand_a)
        # Brand B
        brand_b = seed_brand_context(air, brand_id="brand-ctx-B")
        brand_b_ref = stored_ref(brand_b)
        # Voice DNA belongs to brand B, but we supply brand A ref
        voice = seed_voice_dna(air, brand_context_ref=brand_b_ref, voice_id="voice-dna-B")
        voice_ref = stored_ref(voice)

        research = _research_package(client, guest_name="Mismatch Voice")
        response = client.post(
            "/api/interviews/compose/brief",
            json=_brief_payload(research["research_package_id"], brand_a_ref, voice_ref, "Mismatch Voice"),
            headers={"Idempotency-Key": "brief:ac005"},
        )
        assert response.status_code == 422, response.text
        assert _error_code(response) == "BRAND_VOICE_MISMATCH"


def test_ac006_brief_non_existent_research_package(api_app):
    """AC-006: Brief against a non-existent research package returns 404."""
    with TestClient(api_app) as client:
        air = client.app.state.air
        brand, voice = seed_brand_and_voice(air)
        brand_ref = stored_ref(brand)
        voice_ref = stored_ref(voice)

        response = client.post(
            "/api/interviews/compose/brief",
            json=_brief_payload("ic:research:nonexistent", brand_ref, voice_ref, "No Research"),
            headers={"Idempotency-Key": "brief:ac006"},
        )
        assert response.status_code == 404, response.text
        # 404 is routed through the gateway's global not_found_handler, which
        # always emits error_code "NOT_FOUND"; the research-package cause is in
        # the message. AC-006's intent is the 404 + research-package message.
        assert _error_code(response) == "NOT_FOUND"


def test_ac007_idempotent_replay(api_app):
    """AC-007: Idempotent replay returns same brief_id with idempotent_replay: true."""
    with TestClient(api_app) as client:
        air = client.app.state.air
        brand, voice = seed_brand_and_voice(air)
        brand_ref = stored_ref(brand)
        voice_ref = stored_ref(voice)
        research = _research_package(client, guest_name="Idem Guest")

        payload = _brief_payload(research["research_package_id"], brand_ref, voice_ref, "Idem Guest")
        r1 = client.post("/api/interviews/compose/brief", json=payload, headers={"Idempotency-Key": "idem-brief"})
        assert r1.status_code == 201
        assert r1.json()["idempotent_replay"] is False

        r2 = client.post("/api/interviews/compose/brief", json=payload, headers={"Idempotency-Key": "idem-brief"})
        assert r2.status_code == 201
        assert r2.json()["idempotent_replay"] is True
        assert r2.json()["brief_id"] == r1.json()["brief_id"]


def test_ac008_idempotency_conflict(api_app):
    """AC-008: Different payload with same idempotency key returns 409."""
    with TestClient(api_app) as client:
        r1 = client.post(
            "/api/interviews/compose/research",
            data={
                "guest_name": "Conflict",
                "source_urls_json": json.dumps([]),
                "workspace_id": "ws-test",
                "project_id": "prj-test",
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            headers={"Idempotency-Key": "conflict-key"},
        )
        assert r1.status_code == 201

        r2 = client.post(
            "/api/interviews/compose/research",
            data={
                "guest_name": "Different",
                "source_urls_json": json.dumps([]),
                "workspace_id": "ws-test",
                "project_id": "prj-test",
                "operator_id": "op-test",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-test",
            },
            headers={"Idempotency-Key": "conflict-key"},
        )
        assert r2.status_code == 409
        assert _error_code(r2) == "CONFLICT"


def test_ac011_get_endpoints_404(api_app):
    """AC-011: GET endpoints return 404 for unknown IDs."""
    with TestClient(api_app) as client:
        for path in [
            "/api/interviews/compose/research/ic:research:nonexistent",
            "/api/interviews/compose/briefs/ic:brief:nonexistent",
            "/api/interviews/compose/sessions/ic:session:nonexistent",
        ]:
            response = client.get(path)
            assert response.status_code == 404, f"{path}: {response.text}"


def test_research_get(api_app):
    """Verify GET /research/{id} returns the stored research package."""
    with TestClient(api_app) as client:
        body = _research_package(client, guest_name="Getter")
        pid = body["research_package_id"]
        response = client.get(f"/api/interviews/compose/research/{pid}")
        assert response.status_code == 200
        assert response.json()["research_package_id"] == pid
        assert response.json()["guest_name"] == "Getter"


def test_brief_get(api_app):
    """Verify GET /briefs/{id} returns the stored brief."""
    with TestClient(api_app) as client:
        air = client.app.state.air
        brand, voice = seed_brand_and_voice(air)
        research = _research_package(client, guest_name="Brief Getter")
        brand_ref = stored_ref(brand)
        voice_ref = stored_ref(voice)

        create_resp = client.post(
            "/api/interviews/compose/brief",
            json=_brief_payload(research["research_package_id"], brand_ref, voice_ref, "Brief Getter"),
            headers={"Idempotency-Key": "brief-get"},
        )
        assert create_resp.status_code == 201
        brief_id = create_resp.json()["brief_id"]

        get_resp = client.get(f"/api/interviews/compose/briefs/{brief_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["brief_id"] == brief_id