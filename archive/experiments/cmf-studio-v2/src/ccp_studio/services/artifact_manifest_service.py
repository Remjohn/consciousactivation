from __future__ import annotations

from ccp_studio.contracts.project_workspace_artifact_store import ArtifactManifest, ArtifactRef, ArtifactVersion
from ccp_studio.repositories.project_workspace_artifact_store import InMemoryProjectWorkspaceArtifactStoreRepository


class ArtifactManifestService:
    def __init__(self, repository: InMemoryProjectWorkspaceArtifactStoreRepository | None = None):
        self.repository = repository or InMemoryProjectWorkspaceArtifactStoreRepository()

    def compile_manifest(
        self,
        *,
        client_workspace_id: str,
        manifest_name: str,
        artifact_refs: list[ArtifactRef],
        version_refs: list[ArtifactVersion] | None = None,
        run_id: str | None = None,
    ) -> ArtifactManifest:
        manifest = ArtifactManifest(
            client_workspace_id=client_workspace_id,
            run_id=run_id,
            manifest_name=manifest_name,
            artifact_refs=artifact_refs,
            version_refs=version_refs or [],
        )
        self.repository.upsert("manifests", manifest.artifact_manifest_id, manifest)
        return manifest
