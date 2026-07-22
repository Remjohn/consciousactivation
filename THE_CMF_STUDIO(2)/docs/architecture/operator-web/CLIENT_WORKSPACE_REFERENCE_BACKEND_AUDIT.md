# Client Workspace Reference Backend Audit

Branch: `feat/client-workspace-reference-ui`

## Existing Route Files

Relevant existing API route files:

- `src/ccp_studio/api/v1/operator_ui.py`
- `src/ccp_studio/api/v1/video_timeline_workbench.py`
- `src/ccp_studio/api/v1/supervisual_runtime.py`
- `src/ccp_studio/api/v1/source.py`
- `src/ccp_studio/api/v1/source_provenance.py`
- `src/ccp_studio/api/v1/brands.py`
- `src/ccp_studio/api/v1/provider_jobs.py`
- `src/ccp_studio/api/v1/renders.py`

No dedicated client workspace/reference route existed before this prompt.

## Existing Route Mounting Pattern

The repo does not currently expose a central FastAPI app bootstrap in `src/ccp_studio`. Most route modules define a module-level `router`, and newer workbench modules expose router factories for tests and dependency injection.

Recommended additive route location:

- `src/ccp_studio/api/v1/client_workspace_reference.py`

## Existing Client / Workspace Endpoints

No existing HTTP endpoints were found for:

- create client workspace
- list client workspaces
- get client workspace
- create brand context version for workspace
- register reference metadata
- list reference library
- update reference metadata

## Existing Artifact / Reference Services

Project Workspace + Artifact Store V1 exists and is the required backend substrate:

- `src/ccp_studio/contracts/project_workspace_artifact_store.py`
- `src/ccp_studio/repositories/project_workspace_artifact_store.py`
- `src/ccp_studio/services/client_workspace_service.py`
- `src/ccp_studio/services/workspace_path_service.py`
- `src/ccp_studio/services/run_artifact_directory_service.py`
- `src/ccp_studio/services/artifact_store_service.py`
- `src/ccp_studio/services/artifact_manifest_service.py`
- `src/ccp_studio/services/artifact_lineage_service.py`

Useful existing laws already enforced by these contracts:

- `client_slug` must be path-safe.
- `workspace_relative_path` must be relative and cannot traverse.
- `ArtifactRef.relative_path` must be relative and cannot traverse.
- `ArtifactRef` with `storage_state=materialized` requires `sha256`.

## Existing Upload Handling Conventions

No safe general binary upload convention was found for this operator-web surface. This prompt therefore implements register-only reference endpoints and defers binary upload.

## Existing Test Client Pattern

Existing workbench tests directly mount route factories when FastAPI is available. This prompt follows that pattern while keeping service tests as the stable path when optional FastAPI dependencies are not installed.

## Missing Backend Endpoints

Added additively:

- `POST /api/v1/client-workspaces`
- `GET /api/v1/client-workspaces`
- `GET /api/v1/client-workspaces/{client_workspace_id}`
- `POST /api/v1/client-workspaces/{client_workspace_id}/brand-context-versions`
- `POST /api/v1/client-workspaces/{client_workspace_id}/references/register`
- `GET /api/v1/client-workspaces/{client_workspace_id}/references`
- `PATCH /api/v1/client-workspaces/{client_workspace_id}/references/{artifact_ref_id}`

Deferred:

- `POST /api/v1/client-workspaces/{client_workspace_id}/references/upload`

Binary upload should only be added after the repo has a safe upload/storage convention that computes `sha256` server-side and materializes files under the configured workspace root.

