from __future__ import annotations

from collections import Counter
from pathlib import PurePosixPath

from ccp_studio.contracts.client_workspace_reference_ui import (
    BrandContextVersionCreateRequest,
    BrandContextVersionReadModel,
    ClientWorkspaceCreateRequest,
    ClientWorkspaceReadModel,
    ReferenceApprovalState,
    ReferenceAssetReadModel,
    ReferenceAssetRegisterRequest,
    ReferenceAssetUpdateRequest,
    ReferenceLibraryReadModel,
    ReferenceRightsStatus,
)
from ccp_studio.contracts.project_workspace_artifact_store import (
    ArtifactCategory,
    ArtifactStorageState,
    ClientWorkspace,
    WorkspaceFolderMap,
    validate_relative_path,
)
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository
from ccp_studio.services.artifact_store_service import ArtifactStoreService
from ccp_studio.services.client_workspace_service import ClientWorkspaceService
from ccp_studio.services.workspace_path_service import WorkspacePathService


def _dump_model(model):
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


class ClientWorkspaceReferenceService:
    def __init__(
        self,
        *,
        repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None,
        workspace_service: ClientWorkspaceService | None = None,
        artifact_store: ArtifactStoreService | None = None,
        path_service: WorkspacePathService | None = None,
    ):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()
        self.path_service = path_service or WorkspacePathService()
        self.workspace_service = workspace_service or ClientWorkspaceService(
            repository=self.repository,
            path_service=self.path_service,
        )
        self.artifact_store = artifact_store or ArtifactStoreService(repository=self.repository)
        self._workspace_metadata: dict[str, dict[str, str | None]] = {}
        self._brand_context_versions: dict[str, BrandContextVersionReadModel] = {}
        self._reference_metadata: dict[str, dict[str, object]] = {}
        self._reference_order_by_workspace: dict[str, list[str]] = {}

    @property
    def provider_calls_executed(self) -> bool:
        return False

    @property
    def generation_triggered(self) -> bool:
        return False

    def create_workspace(self, request: ClientWorkspaceCreateRequest) -> ClientWorkspaceReadModel:
        workspace = self.workspace_service.create_workspace(
            client_id=request.client_id,
            client_slug=request.client_slug,
            brand_id=request.brand_id,
            brand_context_version_id=request.brand_context_version_id,
        )
        self._workspace_metadata[workspace.client_workspace_id] = {
            "display_name": request.display_name,
            "notes": request.notes,
        }
        return self._workspace_read_model(workspace)

    def list_workspaces(self) -> list[ClientWorkspaceReadModel]:
        return [self._workspace_read_model(workspace) for workspace in self.repository.workspaces.values()]

    def get_workspace(self, client_workspace_id: str) -> ClientWorkspaceReadModel:
        return self._workspace_read_model(self._workspace(client_workspace_id))

    def create_brand_context_version(
        self,
        request: BrandContextVersionCreateRequest,
    ) -> BrandContextVersionReadModel:
        workspace = self._workspace(request.client_workspace_id)
        if request.brand_id != workspace.brand_id:
            raise ValueError("brand_id must match the client workspace brand_id")
        version = BrandContextVersionReadModel(
            brand_context_version_id=request.brand_context_version_id,
            brand_id=request.brand_id,
            client_workspace_id=request.client_workspace_id,
            context_label=request.context_label,
            source_note=request.source_note,
        )
        self._brand_context_versions[version.brand_context_version_id] = version
        return version

    def register_reference(self, request: ReferenceAssetRegisterRequest) -> ReferenceAssetReadModel:
        workspace = self._workspace(request.client_workspace_id)
        relative_path = request.relative_path or self._default_reference_path(workspace, request)
        validate_relative_path(relative_path, "reference relative_path")
        artifact = self.artifact_store.register_artifact(
            workspace=workspace,
            category=request.category,
            relative_path=relative_path,
            run_id=request.run_id,
            content_type=request.content_type,
            sha256=request.sha256,
            storage_state=request.storage_state,
            tags=request.tags,
            source_refs=request.source_refs,
        )
        artifact.size_bytes = request.size_bytes
        self.repository.upsert("artifact_refs", artifact.artifact_ref_id, artifact)
        self._reference_metadata[artifact.artifact_ref_id] = {
            "rights_status": request.rights_status,
            "approval_state": request.approval_state,
            "notes": request.notes,
        }
        self._reference_order_by_workspace.setdefault(workspace.client_workspace_id, []).append(artifact.artifact_ref_id)
        return ReferenceAssetReadModel.from_artifact(
            artifact,
            rights_status=request.rights_status,
            approval_state=request.approval_state,
            notes=request.notes,
        )

    def update_reference(self, artifact_ref_id: str, request: ReferenceAssetUpdateRequest) -> ReferenceAssetReadModel:
        artifact = self.repository.get("artifact_refs", artifact_ref_id)
        metadata = self._reference_metadata.setdefault(
            artifact_ref_id,
            {
                "rights_status": ReferenceRightsStatus.UNKNOWN,
                "approval_state": ReferenceApprovalState.PENDING,
                "notes": None,
            },
        )
        if request.tags is not None:
            artifact.tags = list(request.tags)
            self.repository.upsert("artifact_refs", artifact.artifact_ref_id, artifact)
        if request.rights_status is not None:
            metadata["rights_status"] = request.rights_status
        if request.approval_state is not None:
            metadata["approval_state"] = request.approval_state
        if request.notes is not None:
            metadata["notes"] = request.notes
        return ReferenceAssetReadModel.from_artifact(
            artifact,
            rights_status=metadata["rights_status"],
            approval_state=metadata["approval_state"],
            notes=metadata.get("notes"),
        )

    def list_references(self, client_workspace_id: str) -> ReferenceLibraryReadModel:
        self._workspace(client_workspace_id)
        artifact_ids = self._reference_order_by_workspace.get(client_workspace_id, [])
        references = [
            self._reference_read_model(artifact_id)
            for artifact_id in artifact_ids
            if artifact_id in self.repository.artifact_refs
        ]
        approval_counts = Counter(reference.approval_state.value for reference in references)
        rights_counts = Counter(reference.rights_status.value for reference in references)
        return ReferenceLibraryReadModel(
            client_workspace_id=client_workspace_id,
            references=references,
            counts_by_approval_state=dict(approval_counts),
            counts_by_rights_status=dict(rights_counts),
        )

    def _workspace(self, client_workspace_id: str) -> ClientWorkspace:
        return self.repository.get("workspaces", client_workspace_id)

    def _workspace_read_model(self, workspace: ClientWorkspace) -> ClientWorkspaceReadModel:
        folder_map = self.path_service.compile_workspace_folder_map(workspace)
        metadata = self._workspace_metadata.get(workspace.client_workspace_id, {})
        return ClientWorkspaceReadModel(
            client_workspace_id=workspace.client_workspace_id,
            client_id=workspace.client_id,
            client_slug=workspace.client_slug,
            brand_id=workspace.brand_id,
            brand_context_version_id=workspace.brand_context_version_id,
            workspace_relative_path=workspace.workspace_relative_path or f"{workspace.workspace_root}/{workspace.client_slug}",
            status=workspace.status,
            folder_map=self._folder_map_dict(folder_map),
            display_name=metadata.get("display_name"),
            notes=metadata.get("notes"),
            created_at=workspace.created_at,
        )

    def _reference_read_model(self, artifact_ref_id: str) -> ReferenceAssetReadModel:
        artifact = self.repository.get("artifact_refs", artifact_ref_id)
        metadata = self._reference_metadata.get(
            artifact_ref_id,
            {
                "rights_status": ReferenceRightsStatus.UNKNOWN,
                "approval_state": ReferenceApprovalState.PENDING,
                "notes": None,
            },
        )
        return ReferenceAssetReadModel.from_artifact(
            artifact,
            rights_status=metadata["rights_status"],
            approval_state=metadata["approval_state"],
            notes=metadata.get("notes"),
        )

    def _folder_map_dict(self, folder_map: WorkspaceFolderMap) -> dict[str, str]:
        data = _dump_model(folder_map)
        return {
            key: value
            for key, value in data.items()
            if key != "workspace_folder_map_id" and isinstance(value, str)
        }

    def _default_reference_path(self, workspace: ClientWorkspace, request: ReferenceAssetRegisterRequest) -> str:
        filename = PurePosixPath(request.filename.replace("\\", "/")).name
        if request.run_id:
            if request.storage_state == ArtifactStorageState.MATERIALIZED and not request.sha256:
                raise ValueError("Materialized reference requires sha256")
            return f"{workspace.workspace_relative_path}/runs/{request.run_id}/assets/references/{filename}"
        category_dir = "references"
        if request.category not in {ArtifactCategory.REFERENCE, ArtifactCategory.BRAND}:
            category_dir = f"references/{request.category.value}"
        return f"{workspace.workspace_relative_path}/{category_dir}/{filename}"

