import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from ccp_studio.repositories.supervisual_runtime import InMemorySuperVisualRuntimeRepository
from ccp_studio.services.supervisual_runtime_service import SuperVisualRuntimeService
from ccp_studio.api.v1.supervisual_runtime import create_supervisual_runtime_router


def _client():
    app = fastapi.FastAPI()
    service = SuperVisualRuntimeService(InMemorySuperVisualRuntimeRepository())
    app.include_router(create_supervisual_runtime_router(service))
    return TestClient(app)


def _create_project(client):
    response = client.post("/api/v1/supervisual/projects", json={
        "brand_id": "brand_1",
        "brand_context_version_id": "bcv_1",
        "title": "Runtime API Project",
        "source_context_refs": ["source_1"],
        "default_frame_profile": "1:1_SOFT_ROUNDED_EDITORIAL",
        "create_initial_variant": True,
    })
    assert response.status_code == 200, response.text
    return response.json()


def test_create_project_endpoint():
    client = _client()
    project = _create_project(client)
    assert project["brand_context_version_id"] == "bcv_1"
    assert project["current_variant_id"]


def test_list_projects_endpoint():
    client = _client()
    _create_project(client)
    response = client.get("/api/v1/supervisual/projects")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_project_detail_endpoint():
    client = _client()
    project = _create_project(client)
    response = client.get(f"/api/v1/supervisual/projects/{project['supervisual_project_id']}")
    assert response.status_code == 200
    assert response.json()["project"]["supervisual_project_id"] == project["supervisual_project_id"]


def test_create_variant_endpoint():
    client = _client()
    project = _create_project(client)
    response = client.post(f"/api/v1/supervisual/projects/{project['supervisual_project_id']}/variants", json={"variant_label": "Variant B"})
    assert response.status_code == 200
    assert response.json()["variant_label"] == "Variant B"


def test_start_build_run_and_run_step_endpoint_creates_event():
    client = _client()
    project = _create_project(client)
    variant_id = project["current_variant_id"]
    run_response = client.post(f"/api/v1/supervisual/variants/{variant_id}/build-runs", json={"requested_steps": ["context_hydrate"]})
    assert run_response.status_code == 200
    build_run_id = run_response.json()["supervisual_build_run_id"]
    step_response = client.post(f"/api/v1/supervisual/build-runs/{build_run_id}/steps/context_hydrate/run", json={})
    assert step_response.status_code == 200
    events_response = client.get(f"/api/v1/supervisual/variants/{variant_id}/events")
    assert any(event["event_type"] == "step.completed" for event in events_response.json())


def test_lock_composition_endpoint_requires_valid_state():
    client = _client()
    project = _create_project(client)
    variant_id = project["current_variant_id"]
    response = client.post(f"/api/v1/supervisual/variants/{variant_id}/composition/lock", json={
        "composition_decision_receipt_id": "composition_1",
        "idempotency_key": "lock_1",
    })
    assert response.status_code == 400


def test_approve_endpoint_requires_eval_pass():
    client = _client()
    project = _create_project(client)
    variant_id = project["current_variant_id"]
    response = client.post(f"/api/v1/supervisual/variants/{variant_id}/approve", json={
        "approval_receipt_id": "approval_1",
        "idempotency_key": "approve_1",
    })
    assert response.status_code == 400


def test_export_endpoint_requires_approval():
    client = _client()
    project = _create_project(client)
    variant_id = project["current_variant_id"]
    response = client.post(f"/api/v1/supervisual/variants/{variant_id}/export", json={
        "export_pack_id": "export_1",
        "idempotency_key": "export_1",
    })
    assert response.status_code == 400
