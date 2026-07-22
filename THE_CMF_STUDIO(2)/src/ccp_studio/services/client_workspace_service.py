from __future__ import annotations

from pathlib import Path

from ccp_studio.contracts.project_workspace_artifact_store import (
    ClientWorkspace,
    PassStatus,
    WorkspaceMaterializationReceipt,
    WorkspacePathPolicy,
)
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository
from ccp_studio.services.workspace_path_service import WorkspacePathService


class ClientWorkspaceService:
    def __init__(
        self,
        repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None,
        path_service: WorkspacePathService | None = None,
    ):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()
        self.paths = path_service or WorkspacePathService()

    def create_workspace(
        self,
        *,
        client_id: str,
        client_slug: str,
        brand_id: str,
        brand_context_version_id: str,
        workspace_root: str = "client_workspaces",
    ) -> ClientWorkspace:
        workspace = ClientWorkspace(
            client_id=client_id,
            client_slug=client_slug,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            workspace_root=workspace_root,
        )
        folder_map = self.paths.compile_workspace_folder_map(workspace)
        self.repository.upsert("workspaces", workspace.client_workspace_id, workspace)
        self.repository.upsert("folder_maps", folder_map.workspace_folder_map_id, folder_map)
        return workspace

    def materialize_workspace(
        self,
        workspace: ClientWorkspace,
        *,
        base_dir: str | Path = ".",
        policy: WorkspacePathPolicy | None = None,
    ) -> WorkspaceMaterializationReceipt:
        policy = policy or WorkspacePathPolicy(workspace_root=workspace.workspace_root)
        folder_map = self.paths.compile_workspace_folder_map(workspace)
        created = []
        existing = []
        blockers = []
        base_dir = Path(base_dir)
        for rel in folder_map.all_paths():
            try:
                path = base_dir / rel
                if path.exists():
                    existing.append(rel)
                else:
                    path.mkdir(parents=True, exist_ok=True)
                    created.append(rel)
            except Exception as exc:
                blockers.append(f"{rel}: {exc}")
        receipt = WorkspaceMaterializationReceipt(
            client_workspace_id=workspace.client_workspace_id,
            created_paths=created,
            existing_paths=existing,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
        self.repository.upsert("materialization_receipts", receipt.workspace_materialization_receipt_id, receipt)
        return receipt
