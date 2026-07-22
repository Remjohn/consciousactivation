# CCP Project Workspace + Artifact Store V1 Integration Bundle

This bundle adds deterministic client workspace folders and artifact reference contracts.

## Purpose

Create a stable local/client artifact model before UI, provider runtime, and local render worker work expands.

## Folder convention

```text
client_workspaces/<client_slug>/
  brand/
  references/
  libraries/
    avatar/
    real_life_cutouts/
    templates/
  runs/
    <run_id>/
      artifacts/
      receipts/
      assets/
        references/
        ideogram_plates/
        flux_edits/
        avatar/
        cutouts/
        audio/
      timeline/
      renders/
      exports/
```

## Why now

The upcoming UI, provider runtime, 64-state avatar generation, template preview, and local render worker will become messy without deterministic workspace paths, artifact refs, manifests, lineage, and receipts.

## Apply after

Recommended:

```text
Capability Preflight + Provider Menu V1
Format 02 Golden Path Orchestrator V1
Video Editing Engine V1
Avatar Performance Layer V1
```

## Do not

```text
Do not move existing client files automatically.
Do not delete existing artifacts.
Do not write outside configured workspace root.
Do not allow path traversal.
Do not treat artifact refs as raw file contents.
Do not call providers.
Do not render.
Do not add UI/API endpoints in this bundle.
```

## What this bundle adds

```text
ClientWorkspace
WorkspacePathPolicy
ArtifactRef
ArtifactVersion
ArtifactManifest
ArtifactLineage
ArtifactReceipt
RunArtifactDirectory

client_workspace_service.py
workspace_path_service.py
run_artifact_directory_service.py
artifact_store_service.py
artifact_manifest_service.py
artifact_lineage_service.py
```

## Milestones

### Milestone 1 — Docs, registries, contracts

Copy/add:

```text
docs/architecture/project-workspace-artifact-store/
registries/canonical/project_workspace/
src/ccp_studio/contracts/project_workspace_artifact_store.py
PROJECT_WORKSPACE_ARTIFACT_STORE_V1_BUNDLE_MANIFEST.json
PROJECT_WORKSPACE_ARTIFACT_STORE_V1_LOCAL_VERIFICATION.json
APPLY_PROJECT_WORKSPACE_ARTIFACT_STORE_V1_PATCH.md
```

Commit:

```bash
git add .
git commit -m "feat(workspace): add project workspace and artifact contracts"
```

### Milestone 2 — Repository, services, skills

Copy/add:

```text
src/ccp_studio/repositories/project_workspace_artifact_store.py
src/ccp_studio/services/workspace_path_service.py
src/ccp_studio/services/client_workspace_service.py
src/ccp_studio/services/run_artifact_directory_service.py
src/ccp_studio/services/artifact_store_service.py
src/ccp_studio/services/artifact_manifest_service.py
src/ccp_studio/services/artifact_lineage_service.py
registries/canonical/skills/shared/project_workspace/
```

Commit:

```bash
git add .
git commit -m "feat(workspace): add artifact store services"
```

### Milestone 3 — Tests

Copy/add:

```text
tests/cmf_studio/test_project_workspace_artifact_store_v1.py
```

Run:

```bash
PYTHONPATH=src python -m compileall -q src
PYTHONPATH=src python -m pytest -q tests/cmf_studio
```

Commit:

```bash
git add .
git commit -m "test(workspace): verify deterministic artifact store"
```

## V1 limitations

```text
local filesystem model only
no database persistence
no object storage integration
no UI/API endpoints
no provider calls
no render execution
no automatic migration of old artifacts
```
