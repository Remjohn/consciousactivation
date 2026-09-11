from __future__ import annotations
from fastapi.testclient import TestClient


def _post_import(client, fixtures_dir, *, video_name="synthetic_interview.mp4",
                  transcript_name="sample_transcript.srt", transcript_content_type="text/plain",
                  workspace_id="ws-1", project_id="prj-1", transcript_format="SRT",
                  speaker_id="guest", idempotency_key=None):
    headers = {"Idempotency-Key": idempotency_key} if idempotency_key else {}
    with open(fixtures_dir / video_name, "rb") as video, open(fixtures_dir / transcript_name, "rb") as transcript:
        data = {
            "workspace_id": workspace_id, "project_id": project_id, "operator_id": "op-1",
            "authority_scope": "DEVELOPMENT_TEST", "assertion_id": "assert-1",
            "transcript_format": transcript_format,
        }
        if speaker_id is not None:
            data["speaker_id"] = speaker_id
        return client.post(
            "/api/interviews/import",
            files={
                "video": (video_name, video, "video/mp4"),
                "transcript": (transcript_name, transcript, transcript_content_type),
            },
            data=data,
            headers=headers,
        )


def test_real_mp4_and_srt_import_succeeds(api_app, fixtures_dir):
    """AC-001: a real, ffprobe-readable mp4 plus a real SRT transcript is
    admitted end to end -- 201, all three refs present, lifecycle advances
    past ADMITTED."""
    with TestClient(api_app) as client:
        response = _post_import(client, fixtures_dir)
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["admission_mode"] == "IMPORTED"
        assert body["lifecycle_state"] == "COMPONENTS_IN_PROGRESS"
        assert body["transcript_alignment_ref"]["object_id"]
        assert body["packed_phrase_transcript_ref"]["object_id"]
        assert body["visual_structure_index_ref"]["object_id"]
        assert body["word_count"] > 0
        assert body["phrase_count"] > 0
        assert body["shot_count"] == 1
        assert body["idempotent_replay"] is False


def test_imported_admission_preserves_absent_lineage(api_app, fixtures_dir):
    """AC-002: /import never fabricates planning history -- planning_lineage
    is always exactly {"state": "ABSENT_NOT_CREATED"}."""
    with TestClient(api_app) as client:
        response = _post_import(client, fixtures_dir, workspace_id="ws-2", project_id="prj-2")
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["planning_lineage"] == {"state": "ABSENT_NOT_CREATED"}

        status = client.get(f"/api/interviews/{body['package_id']}/status")
        assert status.status_code == 200
        assert status.json()["planning_lineage"] == {"state": "ABSENT_NOT_CREATED"}


def test_srt_words_are_inferred_not_observed(api_app, fixtures_dir):
    """AC-005: SRT has no per-word confidence signal, so every word the
    even-split ingester produces must be epistemic_state INFERRED, never
    OBSERVED. Evidence is a direct repository read of the stored
    transcript_alignment payload, as the spec's AC-005 evidence line requires."""
    with TestClient(api_app) as client:
        response = _post_import(client, fixtures_dir, workspace_id="ws-5", project_id="prj-5")
        assert response.status_code == 201, response.text
        alignment_ref = response.json()["transcript_alignment_ref"]

        alignment = client.app.state.interview.repository.get_object(alignment_ref["object_id"])
        words = alignment["payload"]["words"]
        assert words, "expected at least one word in the alignment"
        assert all(w["epistemic_state"] == "INFERRED" for w in words)


def test_pre_aligned_json_epistemic_state_passthrough(api_app, fixtures_dir):
    """AC-006: a PRE_ALIGNED_JSON transcript where every word is declared
    OBSERVED must come through unchanged -- the API must not overwrite the
    caller's declared epistemic_state."""
    with TestClient(api_app) as client:
        response = _post_import(
            client, fixtures_dir, workspace_id="ws-6", project_id="prj-6",
            transcript_name="sample_pre_aligned.json", transcript_content_type="application/json",
            transcript_format="PRE_ALIGNED_JSON", speaker_id=None,
        )
        assert response.status_code == 201, response.text
        alignment_ref = response.json()["transcript_alignment_ref"]

        alignment = client.app.state.interview.repository.get_object(alignment_ref["object_id"])
        words = alignment["payload"]["words"]
        assert words, "expected at least one word in the alignment"
        assert all(w["epistemic_state"] == "OBSERVED" for w in words)


def test_untimed_transcript_rejected(api_app, fixtures_dir):
    """AC-007: a plain .txt transcript with no timing information, submitted
    as transcript_format=SRT, must be rejected with 422
    UNSUPPORTED_TRANSCRIPT_FORMAT, and no package may be created."""
    with TestClient(api_app) as client:
        response = _post_import(
            client, fixtures_dir, workspace_id="ws-7", project_id="prj-7",
            transcript_name="untimed.txt", transcript_content_type="text/plain",
            transcript_format="SRT",
        )
        assert response.status_code == 422, response.text
        err = response.json().get("detail", response.json())
        assert err["error_code"] == "UNSUPPORTED_TRANSCRIPT_FORMAT"
        assert client.app.state.interview.repository.list_objects("canonical_interview_source_package") == []


def test_corrupt_media_rejected_before_admit(api_app, fixtures_dir):
    """AC-008: a zero-byte "video" file must be rejected with 422
    MEDIA_PROBE_FAILED before any repository write occurs."""
    with TestClient(api_app) as client:
        response = _post_import(
            client, fixtures_dir, workspace_id="ws-8", project_id="prj-8", video_name="corrupt.mp4",
        )
        assert response.status_code == 422, response.text
        err = response.json().get("detail", response.json())
        assert err["error_code"] == "MEDIA_PROBE_FAILED"
        assert client.app.state.interview.repository.list_objects("canonical_interview_source_package") == []


def test_identical_retry_is_idempotent(api_app, fixtures_dir):
    """AC-011: resending the exact same multipart request returns the same
    package_id with idempotent_replay: true, and the repository still
    contains exactly one canonical_interview_source_package object."""
    with TestClient(api_app) as client:
        first = _post_import(client, fixtures_dir, workspace_id="ws-11", project_id="prj-11")
        assert first.status_code == 201, first.text
        second = _post_import(client, fixtures_dir, workspace_id="ws-11", project_id="prj-11")
        assert second.status_code == 201, second.text

        assert first.json()["package_id"] == second.json()["package_id"]
        assert second.json()["idempotent_replay"] is True
        objects = client.app.state.interview.repository.list_objects("canonical_interview_source_package")
        assert len(objects) == 1


def test_default_visual_index_is_single_shot(api_app, fixtures_dir):
    """AC-012: with no caller-supplied shot/keyframe data, the visual index
    defaults to exactly one shot spanning the full media duration, no
    keyframes, technical_only, and creates_expression_moments: false."""
    with TestClient(api_app) as client:
        response = _post_import(client, fixtures_dir, workspace_id="ws-12", project_id="prj-12")
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["shot_count"] == 1
        assert body["keyframe_count"] == 0

        visual = client.app.state.interview.repository.get_object(body["visual_structure_index_ref"]["object_id"])
        payload = visual["payload"]
        assert len(payload["shots"]) == 1
        assert payload["shots"][0]["start_ms"] == 0
        assert payload["shots"][0]["end_ms"] == payload["duration_ms"]
        assert payload["keyframes"] == []
        assert payload["technical_only"] is True
        assert payload["creates_expression_moments"] is False
