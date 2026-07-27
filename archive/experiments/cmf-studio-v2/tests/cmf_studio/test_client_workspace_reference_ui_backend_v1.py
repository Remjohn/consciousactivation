import pytest

try:
    import fastapi
    from fastapi.testclient import TestClient
except Exception:
    fastapi = None
    TestClient = None

from ccp_studio.api.v1.client_workspace_reference import create_client_workspace_reference_router
from ccp_studio.contracts.client_workspace_reference_ui import (
    ClientWorkspaceCreateRequest,
    ReferenceApprovalState,
    ReferenceAssetRegisterRequest,
    ReferenceAssetUpdateRequest,
    ReferenceRightsStatus,
)
from ccp_studio.contracts.project_workspace_artifact_store import ArtifactStorageState
from ccp_studio.services.client_workspace_reference_service import ClientWorkspaceReferenceService


def _workspace_request(**overrides):
    data = {
        "client_id": "client_health_myth",
        "client_slug": "health_myth_client",
        "brand_id": "brand_health_myth",
        "brand_context_version_id": "bcv_health_myth_v1",
        "display_name": "Health Myth Client",
    }
    data.update(overrides)
    return ClientWorkspaceCreateRequest(**data)


def _reference_request(client_workspace_id: str, **overrides):
    data = {
        "client_workspace_id": client_workspace_id,
        "filename": "morning-routine.jpg",
        "content_type": "image/jpeg",
        "category": "reference",
        "tags": ["guest_asset_pack", "source_truth"],
        "source_refs": ["interview:00:01:00"],
        "rights_status": "client_provided",
        "approval_state": "pending",
        "notes": "Operator registered reference.",
    }
    data.update(overrides)
    return ReferenceAssetRegisterRequest(**data)


def _service_with_workspace():
    service = ClientWorkspaceReferenceService()
    workspace = service.create_workspace(_workspace_request())
    return service, workspace


def _client():
    if fastapi is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")
    app = fastapi.FastAPI()
    service = ClientWorkspaceReferenceService()
    app.include_router(create_client_workspace_reference_router(service))
    return TestClient(app), service


def test_create_workspace_requires_brand_context_version_id():
    with pytest.raises(ValueError):
        ClientWorkspaceCreateRequest(
            client_id="client_1",
            client_slug="client_one",
            brand_id="brand_1",
            brand_context_version_id="",
        )


def test_unsafe_client_slug_is_rejected():
    with pytest.raises(ValueError):
        ClientWorkspaceCreateRequest(
            client_id="client_1",
            client_slug="../client_one",
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
        )


def test_create_workspace_returns_folder_map():
    service = ClientWorkspaceReferenceService()
    workspace = service.create_workspace(_workspace_request())
    assert workspace.client_workspace_id
    assert workspace.brand_context_version_id == "bcv_health_myth_v1"
    assert workspace.folder_map["root"] == "client_workspaces/health_myth_client"
    assert workspace.folder_map["references"] == "client_workspaces/health_myth_client/references"


def test_register_reference_creates_artifact_ref_backed_read_model():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    assert reference.artifact_ref_id in service.repository.artifact_refs
    assert reference.client_workspace_id == workspace.client_workspace_id
    assert reference.relative_path.endswith("/references/morning-routine.jpg")
    assert reference.uri.startswith("workspace://health_myth_client/")
    assert reference.provider_calls_executed is False
    assert reference.generation_triggered is False


def test_reference_rights_status_is_explicit():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(
        _reference_request(workspace.client_workspace_id, rights_status=ReferenceRightsStatus.OWNED)
    )
    assert reference.rights_status == ReferenceRightsStatus.OWNED


def test_reference_approval_state_is_explicit():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(
        _reference_request(workspace.client_workspace_id, approval_state=ReferenceApprovalState.NEEDS_REVIEW)
    )
    assert reference.approval_state == ReferenceApprovalState.NEEDS_REVIEW


def test_materialized_reference_requires_sha256():
    service, workspace = _service_with_workspace()
    with pytest.raises(ValueError):
        service.register_reference(
            _reference_request(
                workspace.client_workspace_id,
                storage_state=ArtifactStorageState.MATERIALIZED,
                sha256=None,
            )
        )


def test_update_reference_tags_works():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    updated = service.update_reference(
        reference.artifact_ref_id,
        ReferenceAssetUpdateRequest(tags=["approved_source", "face_reference"]),
    )
    assert updated.tags == ["approved_source", "face_reference"]


def test_update_reference_rights_status_works():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    updated = service.update_reference(
        reference.artifact_ref_id,
        ReferenceAssetUpdateRequest(rights_status=ReferenceRightsStatus.LICENSED),
    )
    assert updated.rights_status == ReferenceRightsStatus.LICENSED


def test_update_reference_approval_state_works():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    updated = service.update_reference(
        reference.artifact_ref_id,
        ReferenceAssetUpdateRequest(approval_state=ReferenceApprovalState.APPROVED),
    )
    assert updated.approval_state == ReferenceApprovalState.APPROVED


def test_list_references_returns_counts_by_approval_state():
    service, workspace = _service_with_workspace()
    service.register_reference(_reference_request(workspace.client_workspace_id, approval_state="pending"))
    service.register_reference(
        _reference_request(
            workspace.client_workspace_id,
            filename="hero-cutout.png",
            approval_state="approved",
            rights_status="owned",
        )
    )
    library = service.list_references(workspace.client_workspace_id)
    assert library.counts_by_approval_state["pending"] == 1
    assert library.counts_by_approval_state["approved"] == 1
    assert library.counts_by_rights_status["client_provided"] == 1
    assert library.counts_by_rights_status["owned"] == 1


def test_path_traversal_in_relative_path_is_rejected():
    service, workspace = _service_with_workspace()
    with pytest.raises(ValueError):
        service.register_reference(
            _reference_request(
                workspace.client_workspace_id,
                relative_path="../escape.jpg",
            )
        )


def test_register_reference_does_not_call_providers():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    assert service.provider_calls_executed is False
    assert reference.provider_calls_executed is False


def test_register_reference_does_not_trigger_generation():
    service, workspace = _service_with_workspace()
    reference = service.register_reference(_reference_request(workspace.client_workspace_id))
    assert service.generation_triggered is False
    assert reference.generation_triggered is False


def test_http_routes_create_register_list_and_update_reference():
    client, _service = _client()
    workspace_response = client.post(
        "/api/v1/client-workspaces",
        json={
            "client_id": "client_health_myth",
            "client_slug": "health_myth_client",
            "brand_id": "brand_health_myth",
            "brand_context_version_id": "bcv_health_myth_v1",
            "display_name": "Health Myth Client",
        },
    )
    assert workspace_response.status_code == 200, workspace_response.text
    workspace = workspace_response.json()

    brand_context_response = client.post(
        f"/api/v1/client-workspaces/{workspace['client_workspace_id']}/brand-context-versions",
        json={
            "client_workspace_id": workspace["client_workspace_id"],
            "brand_id": "brand_health_myth",
            "brand_context_version_id": "bcv_health_myth_v2",
            "context_label": "Interview intake refresh",
            "source_note": "Operator confirmed source packet.",
        },
    )
    assert brand_context_response.status_code == 200, brand_context_response.text

    reference_response = client.post(
        f"/api/v1/client-workspaces/{workspace['client_workspace_id']}/references/register",
        json={
            "client_workspace_id": workspace["client_workspace_id"],
            "filename": "guest-portrait.jpg",
            "content_type": "image/jpeg",
            "category": "reference",
            "tags": ["portrait", "client_uploaded"],
            "source_refs": ["guest_asset_pack:portrait"],
            "rights_status": "client_provided",
            "approval_state": "needs_review",
            "notes": "Uploaded outside this register-only route.",
        },
    )
    assert reference_response.status_code == 200, reference_response.text
    reference = reference_response.json()
    assert reference["artifact_ref_id"]
    assert reference["rights_status"] == "client_provided"
    assert reference["approval_state"] == "needs_review"

    update_response = client.patch(
        f"/api/v1/client-workspaces/{workspace['client_workspace_id']}/references/{reference['artifact_ref_id']}",
        json={
            "tags": ["portrait", "approved_source"],
            "rights_status": "owned",
            "approval_state": "approved",
            "notes": "Approved by operator.",
        },
    )
    assert update_response.status_code == 200, update_response.text
    updated = update_response.json()
    assert updated["rights_status"] == "owned"
    assert updated["approval_state"] == "approved"
    assert updated["tags"] == ["portrait", "approved_source"]

    library_response = client.get(f"/api/v1/client-workspaces/{workspace['client_workspace_id']}/references")
    assert library_response.status_code == 200, library_response.text
    library = library_response.json()
    assert library["counts_by_approval_state"]["approved"] == 1
    assert library["counts_by_rights_status"]["owned"] == 1

