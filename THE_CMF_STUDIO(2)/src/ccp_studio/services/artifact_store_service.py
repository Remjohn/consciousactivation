from __future__ import annotations

from pathlib import Path

from ccp_studio.contracts.project_workspace_artifact_store import (
    ArtifactCategory,
    ArtifactRef,
    ArtifactStorageState,
    ArtifactVersion,
    ClientWorkspace,
    RunArtifactDirectory,
    sha256_text,
)
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository


class ArtifactStoreService:
    def __init__(self, repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()

    def register_artifact(
        self,
        *,
        workspace: ClientWorkspace,
        category: ArtifactCategory,
        relative_path: str,
        artifact_id: str | None = None,
        run_id: str | None = None,
        content_type: str | None = None,
        sha256: str | None = None,
        storage_state: ArtifactStorageState = ArtifactStorageState.REGISTERED,
        tags: list[str] | None = None,
        source_refs: list[str] | None = None,
    ) -> ArtifactRef:
        artifact = ArtifactRef(
            artifact_id=artifact_id or Path(relative_path).stem.replace(".", "_").replace("-", "_"),
            client_workspace_id=workspace.client_workspace_id,
            client_slug=workspace.client_slug,
            run_id=run_id,
            category=category,
            relative_path=relative_path,
            content_type=content_type,
            sha256=sha256,
            storage_state=storage_state,
            tags=tags or [],
            source_refs=source_refs or [],
        )
        self.repository.upsert("artifact_refs", artifact.artifact_ref_id, artifact)
        return artifact

    def register_text_artifact(
        self,
        *,
        workspace: ClientWorkspace,
        category: ArtifactCategory,
        relative_path: str,
        text: str,
        run_id: str | None = None,
        content_type: str = "text/plain",
    ) -> tuple[ArtifactRef, ArtifactVersion]:
        digest = sha256_text(text)
        artifact = self.register_artifact(
            workspace=workspace,
            category=category,
            relative_path=relative_path,
            run_id=run_id,
            content_type=content_type,
            sha256=digest,
            storage_state=ArtifactStorageState.MATERIALIZED,
        )
        version = ArtifactVersion(
            artifact_ref_id=artifact.artifact_ref_id,
            version=1,
            sha256=digest,
            relative_path=relative_path,
        )
        self.repository.upsert("artifact_versions", version.artifact_version_id, version)
        return artifact, version

    def register_run_output(
        self,
        *,
        workspace: ClientWorkspace,
        run_directory: RunArtifactDirectory,
        category: ArtifactCategory,
        filename: str,
        text: str,
        subdir: str = "artifacts",
    ) -> tuple[ArtifactRef, ArtifactVersion]:
        relative_path = f"{run_directory.run_root}/{subdir}/{filename}"
        return self.register_text_artifact(
            workspace=workspace,
            category=category,
            relative_path=relative_path,
            text=text,
            run_id=run_directory.run_id,
        )
