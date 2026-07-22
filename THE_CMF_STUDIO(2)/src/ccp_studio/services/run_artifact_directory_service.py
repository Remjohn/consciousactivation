from __future__ import annotations

from pathlib import Path

from ccp_studio.contracts.project_workspace_artifact_store import (
    ClientWorkspace,
    PassStatus,
    RunArtifactDirectory,
    WorkspaceMaterializationReceipt,
)
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository
from ccp_studio.services.workspace_path_service import WorkspacePathService


class RunArtifactDirectoryService:
    def __init__(
        self,
        repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None,
        path_service: WorkspacePathService | None = None,
    ):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()
        self.paths = path_service or WorkspacePathService()

    def compile_run_directory(self, workspace: ClientWorkspace, run_id: str) -> RunArtifactDirectory:
        directory = self.paths.compile_run_directory(workspace, run_id)
        self.repository.upsert("run_directories", directory.run_artifact_directory_id, directory)
        return directory

    def materialize_run_directory(self, directory: RunArtifactDirectory, *, base_dir: str | Path = ".") -> WorkspaceMaterializationReceipt:
        created = []
        existing = []
        blockers = []
        base_dir = Path(base_dir)
        for rel in directory.all_paths():
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
            client_workspace_id=directory.client_workspace_id,
            created_paths=created,
            existing_paths=existing,
            pass_status=PassStatus.FAIL if blockers else PassStatus.PASS,
            blockers=blockers,
        )
        self.repository.upsert("materialization_receipts", receipt.workspace_materialization_receipt_id, receipt)
        return receipt
