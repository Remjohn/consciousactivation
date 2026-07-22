from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover
    APIRouter = None  # type: ignore
    HTTPException = Exception  # type: ignore

from ccp_studio.contracts.client_workspace_reference_ui import (
    BrandContextVersionCreateRequest,
    ClientWorkspaceCreateRequest,
    ReferenceAssetRegisterRequest,
    ReferenceAssetUpdateRequest,
)
from ccp_studio.services.client_workspace_reference_service import ClientWorkspaceReferenceService


def _copy_model(model, **updates):
    return model.model_copy(update=updates) if hasattr(model, "model_copy") else model.copy(update=updates)


def create_client_workspace_reference_router(service: ClientWorkspaceReferenceService | None = None):
    if APIRouter is None:
        raise RuntimeError("FastAPI is required to create the Client Workspace Reference router")

    workspace_references = service or ClientWorkspaceReferenceService()
    router = APIRouter(prefix="/api/v1/client-workspaces", tags=["client-workspace-references"])

    def handle(fn):
        try:
            return fn()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @router.post("")
    def create_workspace(request: ClientWorkspaceCreateRequest):
        return handle(lambda: workspace_references.create_workspace(request))

    @router.get("")
    def list_workspaces():
        return handle(workspace_references.list_workspaces)

    @router.get("/{client_workspace_id}")
    def get_workspace(client_workspace_id: str):
        return handle(lambda: workspace_references.get_workspace(client_workspace_id))

    @router.post("/{client_workspace_id}/brand-context-versions")
    def create_brand_context_version(client_workspace_id: str, request: BrandContextVersionCreateRequest):
        request = _copy_model(request, client_workspace_id=client_workspace_id)
        return handle(lambda: workspace_references.create_brand_context_version(request))

    @router.post("/{client_workspace_id}/references/register")
    def register_reference(client_workspace_id: str, request: ReferenceAssetRegisterRequest):
        request = _copy_model(request, client_workspace_id=client_workspace_id)
        return handle(lambda: workspace_references.register_reference(request))

    @router.get("/{client_workspace_id}/references")
    def list_references(client_workspace_id: str):
        return handle(lambda: workspace_references.list_references(client_workspace_id))

    @router.patch("/{client_workspace_id}/references/{artifact_ref_id}")
    def update_reference(client_workspace_id: str, artifact_ref_id: str, request: ReferenceAssetUpdateRequest):
        def update():
            reference = workspace_references.update_reference(artifact_ref_id, request)
            if reference.client_workspace_id != client_workspace_id:
                raise ValueError("artifact_ref_id does not belong to this client workspace")
            return reference

        return handle(update)

    return router


router = create_client_workspace_reference_router() if APIRouter is not None else None

