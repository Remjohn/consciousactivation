from __future__ import annotations

from ._support import composer_app, ref, valid_seed, valid_question
from conscious_activations_interview_composer.errors import NotFoundError


def _create_research_package(app, pid="r1"):
    result = app.research.create_package(
        {
            "workspace_id": "ws-1", "project_id": "prj-1",
            "guest_name": "Guest", "source_urls": [],
            "uploaded_documents": [],
            "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        },
        idempotency_key=pid,
    )
    return result["object"]


def test_create_brief_success(tmp_path):
    app = composer_app(tmp_path)
    research = _create_research_package(app)
    research_ref = {"object_id": research["object_id"], "version": research["version"], "sha256": research["sha256"]}

    result = app.briefs.create_brief(
        {
            "research_package_ref": research_ref,
            "brand_context_ref": ref("brand-ctx-1"),
            "voice_dna_ref": ref("voice-dna-1"),
            "guest_name": "Guest",
            "tension_hypothesis": "Keeps control as proof of competence.",
            "matrix_of_edging_seed": valid_seed(),
            "planned_questions": [valid_question()],
            "expression_targets": ["self-recognizing witness"],
            "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        },
        idempotency_key="brief-1",
    )
    payload = result["object"]["payload"]
    assert payload["brief_id"].startswith("ic:brief:")
    assert payload["content_origin"] == "operator_supplied"
    assert payload["hypothesis_pipeline_status"]["status"] == "BLOCKED_PENDING_GAP_007"
    assert payload["hypothesis_pipeline_status"]["iac_ref"] is None
    assert payload["hypothesis_pipeline_status"]["planned_aip_ref"] is None
    assert payload["hypothesis_pipeline_status"]["arm_receipt_ref"] is None


def test_create_brief_research_not_found(tmp_path):
    app = composer_app(tmp_path)
    missing_ref = ref("ic:research:nonexistent")
    try:
        app.briefs.create_brief(
            {
                "research_package_ref": missing_ref,
                "brand_context_ref": ref("brand-ctx-1"),
                "voice_dna_ref": ref("voice-dna-1"),
                "guest_name": "Guest",
                "tension_hypothesis": "Hypothesis.",
                "matrix_of_edging_seed": valid_seed(),
                "planned_questions": [valid_question()],
                "expression_targets": [],
                "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
            },
            idempotency_key="brief-fail",
        )
        assert False, "expected NotFoundError"
    except NotFoundError as e:
        assert "no guest_research_package" in str(e)


def test_create_brief_adds_edge(tmp_path):
    app = composer_app(tmp_path)
    research = _create_research_package(app)
    research_ref = {"object_id": research["object_id"], "version": research["version"], "sha256": research["sha256"]}

    result = app.briefs.create_brief(
        {
            "research_package_ref": research_ref,
            "brand_context_ref": ref("brand-ctx-1"),
            "voice_dna_ref": ref("voice-dna-1"),
            "guest_name": "Guest",
            "tension_hypothesis": "Hypothesis.",
            "matrix_of_edging_seed": valid_seed(),
            "planned_questions": [valid_question()],
            "expression_targets": [],
            "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        },
        idempotency_key="brief-edge",
    )
    brief_id = result["object"]["payload"]["brief_id"]
    # Check edge was created - descendant should include the research package
    descendants = app.repository.list_objects()
    assert any(d["object_id"] == research["object_id"] for d in descendants)


def test_get_brief(tmp_path):
    app = composer_app(tmp_path)
    research = _create_research_package(app)
    research_ref = {"object_id": research["object_id"], "version": research["version"], "sha256": research["sha256"]}

    result = app.briefs.create_brief(
        {
            "research_package_ref": research_ref,
            "brand_context_ref": ref("brand-ctx-1"),
            "voice_dna_ref": ref("voice-dna-1"),
            "guest_name": "Guest",
            "tension_hypothesis": "Hypothesis.",
            "matrix_of_edging_seed": valid_seed(),
            "planned_questions": [valid_question()],
            "expression_targets": [],
            "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        },
        idempotency_key="brief-get",
    )
    brief_id = result["object"]["object_id"]
    stored = app.repository.get_object(brief_id)
    assert stored["payload"]["tension_hypothesis"] == "Hypothesis."
    assert stored["payload"]["content_origin"] == "operator_supplied"


def test_create_brief_idempotent(tmp_path):
    app = composer_app(tmp_path)
    research = _create_research_package(app)
    research_ref = {"object_id": research["object_id"], "version": research["version"], "sha256": research["sha256"]}
    cmd = {
        "research_package_ref": research_ref,
        "brand_context_ref": ref("brand-ctx-1"),
        "voice_dna_ref": ref("voice-dna-1"),
        "guest_name": "Guest",
        "tension_hypothesis": "Hypothesis.",
        "matrix_of_edging_seed": valid_seed(),
        "planned_questions": [valid_question()],
        "expression_targets": [],
        "composer_authority": {"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
    }
    r1 = app.briefs.create_brief(cmd, idempotency_key="idem-brief")
    r2 = app.briefs.create_brief(cmd, idempotency_key="idem-brief")
    assert r2["idempotent_replay"] is True
    assert r2["object"]["object_id"] == r1["object"]["object_id"]