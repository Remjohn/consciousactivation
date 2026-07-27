from __future__ import annotations

from pathlib import Path

from ccp_studio.contracts.project_workspace_artifact_store import (
    ClientWorkspace,
    RunArtifactDirectory,
    WorkspaceFolderMap,
    WorkspacePathPolicy,
    path_is_relative_to,
)


class WorkspacePathService:
    def compile_workspace_folder_map(self, workspace: ClientWorkspace) -> WorkspaceFolderMap:
        root = workspace.workspace_relative_path
        return WorkspaceFolderMap(
            client_workspace_id=workspace.client_workspace_id,
            root=root,
            brand=f"{root}/brand",
            references=f"{root}/references",
            libraries=f"{root}/libraries",
            avatar_library=f"{root}/libraries/avatar",
            real_life_cutouts_library=f"{root}/libraries/real_life_cutouts",
            templates_library=f"{root}/libraries/templates",
            runs=f"{root}/runs",
        )

    def compile_run_directory(self, workspace: ClientWorkspace, run_id: str) -> RunArtifactDirectory:
        return RunArtifactDirectory(
            client_workspace_id=workspace.client_workspace_id,
            client_slug=workspace.client_slug,
            run_id=run_id,
            workspace_root=workspace.workspace_root,
        )

    def assert_under_workspace_root(self, policy: WorkspacePathPolicy, relative_path: str) -> None:
        root = Path(policy.workspace_root).resolve()
        candidate = (Path(policy.workspace_root) / Path(relative_path)).resolve()
        if not path_is_relative_to(candidate, root):
            raise ValueError("Path escapes workspace root")
