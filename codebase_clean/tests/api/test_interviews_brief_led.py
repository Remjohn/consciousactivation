from __future__ import annotations
import json
from fastapi.testclient import TestClient

# NOTE: validate_planning_lineage() for PRESENT_VERIFIED only checks internal
# consistency (planned_object_digests must match each ref's own sha256) -- it
# does not dereference brief_ref/planned_aip_ref/iac_ref/arm_receipt_ref
# against the repository. tests/phase4/test_ts_int_001_source_package.py's
# own test_valid_brief_led_admission_preserves_exact_plan_refs and
# test_brief_led_hash_mismatch_fails both hand-craft these refs the same way
# rather than storing real objects first; this file follows that same
# established pattern for consistency.
_BRIEF_REF = {"object_id": "brief-1", "version": "1.0.0", "sha256": "b" * 64}
_PLANNED_AIP_REF = {"object_id": "aip-1", "version": "1.0.0", "sha256": "c" * 64}
_IAC_REF = {"object_id": "iac-1", "version": "1.0.0", "sha256": "d" * 64}
_ARM_RECEIPT_REF = {"object_id": "arm-1", "version": "1.0.0", "sha256": "e" * 64}


def _valid_planning_lineage() -> dict:
    return {
        "state": "PRESENT_VERIFIED",
        "brief_ref": _BRIEF_REF, "planned_aip_ref": _PLANNED_AIP_REF,
        "iac_ref": _IAC_REF, "arm_receipt_ref": _ARM_RECEIPT_REF,
        "planned_object_digests": {
            "brief": _BRIEF_REF["sha256"], "planned_aip": _PLANNED_AIP_REF["sha256"], "iac": _IAC_REF["sha256"],
        },
    }


def _post_brief_led(client, fixtures_dir, *, planning_lineage: dict, workspace_id="ws-3", project_id="prj-3"):
    with open(fixtures_dir / "synthetic_interview.mp4", "rb") as video, \
         open(fixtures_dir / "sample_transcript.srt", "rb") as transcript:
        return client.post(
            "/api/interviews/brief-led",
            files={"video": ("interview.mp4", video, "video/mp4"), "transcript": ("t.srt", transcript, "text/plain")},
            data={
                "workspace_id": workspace_id, "project_id": project_id, "operator_id": "op-1",
                "authority_scope": "DEVELOPMENT_TEST", "assertion_id": "assert-1",
                "transcript_format": "SRT", "speaker_id": "guest",
                "planning_lineage_json": json.dumps(planning_lineage),
            },
        )


def test_valid_brief_led_admission_succeeds(api_app, fixtures_dir):
    """AC-003: brief-led admission with a correctly-digested planning lineage
    succeeds and the lineage is preserved exactly as supplied."""
    with TestClient(api_app) as client:
        lineage = _valid_planning_lineage()
        response = _post_brief_led(client, fixtures_dir, planning_lineage=lineage)
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["admission_mode"] == "BRIEF_LED"
        assert body["planning_lineage"] == lineage


def test_digest_mismatch_rejected(api_app, fixtures_dir):
    """AC-004: a planned_object_digests entry that doesn't match its ref's
    own sha256 (INT_ARMED_PLAN_HASH_MISMATCH) is rejected 422
    VALIDATION_FAILED before any component work, and no package is created."""
    with TestClient(api_app) as client:
        lineage = _valid_planning_lineage()
        lineage["planned_object_digests"]["brief"] = "f" * 64  # no longer matches brief_ref's sha256
        response = _post_brief_led(client, fixtures_dir, planning_lineage=lineage, workspace_id="ws-4", project_id="prj-4")
        assert response.status_code == 422, response.text
        body = response.json().get("detail", response.json())
        assert body["error_code"] == "VALIDATION_FAILED"
        assert "INT_ARMED_PLAN_HASH_MISMATCH" in body["message"]
        assert client.app.state.interview.repository.list_objects("canonical_interview_source_package") == []
