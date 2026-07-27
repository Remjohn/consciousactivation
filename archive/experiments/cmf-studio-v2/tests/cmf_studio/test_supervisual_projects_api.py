from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional adapter dependency
    FastAPI = None
    TestClient = None

from ccp_studio.services.supervisual_project_service import SuperVisualProjectService, SuperVisualProjectServiceError  # noqa: E402

if FastAPI is not None and TestClient is not None:
    from ccp_studio.api.v1.supervisual import router, set_supervisual_project_service  # noqa: E402
else:
    router = None
    set_supervisual_project_service = None


def _payload(frame_profile_code: str = "1:1_SOFT_ROUNDED_EDITORIAL") -> dict:
    return {
        "project_name": "Claude Ntahuga Proof SuperVisual",
        "workspace_id": str(uuid4()),
        "brand_context_version_ref": "brand_context:claude:v1",
        "source_evidence_refs": ["transcript:claude:moment-001", "interview_brief:claude:v1"],
        "context_type": "interview_brief_and_transcript",
        "interview_brief_ref": "interview_brief:claude:v1",
        "transcript_ref": "transcript:claude:v1",
        "context_payload": {
            "primary_claim": "The silence of a friend can become a survival question.",
            "proof_detail": "Claude describes the precise moment friendship became suspicion.",
        },
        "frame_profile_code": frame_profile_code,
        "style_route_code": "GMG_EXPERT_05_EDITORIAL_SCRIBE",
    }


def _service_project(service: SuperVisualProjectService, frame_profile_code: str = "1:1_SOFT_ROUNDED_EDITORIAL"):
    return service.create_project(**_payload(frame_profile_code=frame_profile_code))


def test_supervisual_project_build_approval_export_acceptance_path():
    service = SuperVisualProjectService()
    project = _service_project(service)

    variant = service.build_project(project_id=project.supervisual_project_id)
    approval = service.approve_project(project_id=project.supervisual_project_id, operator_id=uuid4())
    export = service.export_project(project_id=project.supervisual_project_id)
    timeline = service.get_timeline(project_id=project.supervisual_project_id)

    assert project.supervisual_project_id in service.repository.projects
    assert variant.supervisual_variant_id in service.repository.variants
    assert variant.context.brand_context_version_ref == "brand_context:claude:v1"
    assert len(variant.primitive_binding.primitive_refs) == 3
    assert variant.frame_profile.code.value == "1:1_SOFT_ROUNDED_EDITORIAL"
    assert variant.style_route.route_code == "GMG_EXPERT_05_EDITORIAL_SCRIBE"
    assert variant.composition_receipt.composition_json["style_route_code"] == "GMG_EXPERT_05_EDITORIAL_SCRIBE"
    assert {layer.layer_id for layer in variant.layer_plan.layers} >= {"headline", "proof-detail", "source-anchor"}
    assert {receipt.provider_code for receipt in variant.provider_receipts} == {"ideogram_4", "qwen_layered", "sam3", "skia_renderer"}
    assert variant.render_contract.deterministic_replay_required is True
    assert variant.eval_receipt.decision == "approved"
    assert approval.decision == "approved"
    assert export.stored is True
    assert export.artifact_ref.startswith("artifact://supervisual/")
    assert timeline.active_variant_id == variant.supervisual_variant_id
    assert "export_created" in {event.event_kind for event in timeline.events}


def test_supervisual_rejects_16_9_delivery_frame():
    service = SuperVisualProjectService()
    project = _service_project(service, frame_profile_code="16:9_SOURCE_INTERVIEW")

    with pytest.raises(SuperVisualProjectServiceError) as exc:
        service.build_project(project_id=project.supervisual_project_id)

    assert exc.value.code == "SUPERVISUAL_FRAME_PROFILE_REJECTED"
    assert "16:9" in exc.value.message


def test_supervisual_fake_provider_output_is_deterministic_for_same_input():
    service = SuperVisualProjectService()
    project = _service_project(service)
    first = service.build_project(project_id=project.supervisual_project_id)

    project_after_build = service.get_project(project_id=project.supervisual_project_id)
    frame_profile = first.frame_profile
    style_route = first.style_route
    expected = service._fake_provider_receipt(
        provider_code="qwen_layered",
        project=project_after_build,
        frame_profile=frame_profile,
        style_route=style_route,
        revision_number=0,
        revision_instruction=None,
    )
    actual = next(receipt for receipt in first.provider_receipts if receipt.provider_code == "qwen_layered")

    assert actual.request_hash == expected.request_hash
    assert actual.output_ref == expected.output_ref


def test_supervisual_approval_blocks_when_eval_fails_and_export_requires_approval():
    service = SuperVisualProjectService()
    project = _service_project(service)
    variant = service.build_project(project_id=project.supervisual_project_id, source_truth_score=0.51)
    approval = service.approve_project(project_id=project.supervisual_project_id, operator_id=uuid4())

    with pytest.raises(SuperVisualProjectServiceError) as exc:
        service.export_project(project_id=project.supervisual_project_id)

    assert variant.eval_receipt.decision == "blocked"
    assert "SOURCE_TRUTH_SCORE_BELOW_THRESHOLD" in variant.eval_receipt.blocker_codes
    assert approval.decision == "blocked"
    assert "SOURCE_TRUTH_SCORE_BELOW_THRESHOLD" in approval.blocker_codes
    assert exc.value.code == "SUPERVISUAL_APPROVAL_REQUIRED"


def test_supervisual_operator_can_reject_variant_before_export():
    service = SuperVisualProjectService()
    project = _service_project(service)
    variant = service.build_project(project_id=project.supervisual_project_id)
    rejection = service.reject_project(
        project_id=project.supervisual_project_id,
        operator_id=uuid4(),
        reason="The visual family is right, but the proof detail needs a cleaner source quote.",
    )

    with pytest.raises(SuperVisualProjectServiceError):
        service.export_project(project_id=project.supervisual_project_id)

    assert rejection.decision == "blocked"
    assert rejection.variant_id == variant.supervisual_variant_id
    assert "SUPERVISUAL_OPERATOR_REJECTED" in rejection.blocker_codes


def test_supervisual_fastapi_project_endpoints():
    if FastAPI is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")
    service = SuperVisualProjectService()
    assert set_supervisual_project_service is not None
    assert router is not None
    set_supervisual_project_service(service)
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    created = client.post("/api/v1/supervisual/projects", json=_payload()).json()
    project_id = created["supervisual_project_id"]
    build = client.post(f"/api/v1/supervisual/projects/{project_id}/build", json={}).json()
    rejected_project = client.post("/api/v1/supervisual/projects", json=_payload()).json()
    rejected_build = client.post(f"/api/v1/supervisual/projects/{rejected_project['supervisual_project_id']}/build", json={}).json()
    rejection = client.post(
        f"/api/v1/supervisual/projects/{rejected_project['supervisual_project_id']}/reject",
        json={"operator_id": str(uuid4()), "reason": "Operator rejected this proof layout."},
    ).json()
    approval = client.post(f"/api/v1/supervisual/projects/{project_id}/approve", json={"operator_id": str(uuid4())}).json()
    export = client.post(f"/api/v1/supervisual/projects/{project_id}/export", json={}).json()
    timeline = client.get(f"/api/v1/supervisual/projects/{project_id}/timeline").json()

    assert build["frame_profile"]["code"] == "1:1_SOFT_ROUNDED_EDITORIAL"
    assert build["eval_receipt"]["decision"] == "approved"
    assert rejection["decision"] == "blocked"
    assert rejection["variant_id"] == rejected_build["supervisual_variant_id"]
    assert approval["decision"] == "approved"
    assert export["artifact_ref"].startswith("artifact://supervisual/")
    assert timeline["active_variant_id"] == build["supervisual_variant_id"]

    rejected = client.post(
        "/api/v1/supervisual/projects",
        json=_payload(frame_profile_code="16:9_SOURCE_INTERVIEW"),
    ).json()
    rejected_response = client.post(f"/api/v1/supervisual/projects/{rejected['supervisual_project_id']}/build", json={})
    assert rejected_response.status_code == 400
    assert rejected_response.json()["detail"]["code"] == "SUPERVISUAL_FRAME_PROFILE_REJECTED"
