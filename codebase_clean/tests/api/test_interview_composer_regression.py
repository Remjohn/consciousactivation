from __future__ import annotations

import json
from fastapi.testclient import TestClient
from tests.api.interview_composer_helpers import seed_brand_and_voice, stored_ref


def _research_package(client: TestClient, *, guest_name: str = "Test Guest") -> dict:
    import json as _json
    response = client.post(
        "/api/interviews/compose/research",
        data={
            "guest_name": guest_name,
            "source_urls_json": _json.dumps(["https://example.com/bio"]),
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


def _make_brief(client: TestClient, *, guest_name: str = "Session Guest") -> dict:
    air = client.app.state.air
    brand, voice = seed_brand_and_voice(air)
    brand_ref = stored_ref(brand)
    voice_ref = stored_ref(voice)
    research = _research_package(client, guest_name=guest_name)
    response = client.post(
        "/api/interviews/compose/brief",
        json={
            "research_package_id": research["research_package_id"],
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
        },
        headers={"Idempotency-Key": f"brief:{guest_name}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_ac013_composer_output_honestly_rejected_by_brief_led(api_app, fixtures_dir):
    """AC-013: A Brief's planning_lineage_template with null refs is correctly
    rejected by POST /brief-led.  This asserts the current, honest boundary
    -- not a defect to fix.  A future GAP-007-resolving spec will have a
    concrete, already-red test to turn green."""
    with TestClient(api_app) as client:
        brief = _make_brief(client, guest_name="Regression Guest")
        template = brief["planning_lineage_template"]

        # Assemble into a planning_lineage with state forced to PRESENT_VERIFIED.
        # The null values for planned_aip_ref / iac_ref / arm_receipt_ref should
        # cause validate_planning_lineage() to reject via exact_keys/require_ref.
        lineage = {
            "state": "PRESENT_VERIFIED",
            "brief_ref": template["brief_ref"],
            "planned_aip_ref": template["planned_aip_ref"],
            "iac_ref": template["iac_ref"],
            "arm_receipt_ref": template["arm_receipt_ref"],
            "planned_object_digests": template["planned_object_digests"],
        }

        with open(fixtures_dir / "synthetic_interview.mp4", "rb") as video, \
             open(fixtures_dir / "sample_transcript.srt", "rb") as transcript:
            response = client.post(
                "/api/interviews/brief-led",
                files={
                    "video": ("interview.mp4", video, "video/mp4"),
                    "transcript": ("t.srt", transcript, "text/plain"),
                },
                data={
                    "workspace_id": "ws-regression",
                    "project_id": "prj-regression",
                    "operator_id": "op-test",
                    "authority_scope": "DEVELOPMENT_TEST",
                    "assertion_id": "assert-test",
                    "transcript_format": "SRT",
                    "speaker_id": "guest",
                    "planning_lineage_json": json.dumps(lineage),
                },
            )

        # The request must fail -- exact_keys/require_ref in
        # validate_planning_lineage() reject the None values.
        assert response.status_code == 422, response.text
        body = response.json()
        # The error comes through http_exception_handler (422), so it's
        # nested under "detail".
        assert body["detail"]["error_code"] == "VALIDATION_FAILED"
