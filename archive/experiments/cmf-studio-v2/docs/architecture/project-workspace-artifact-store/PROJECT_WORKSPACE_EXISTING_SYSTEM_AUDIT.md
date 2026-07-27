# Project Workspace Existing System Audit

Branch: `feat/project-workspace-artifact-store-v1`

## 1. Existing Workspace/Client Files Found

- `src/ccp_studio/contracts/workspace_lifecycle.py` defines organization and brand workspace lifecycle objects such as `BrandWorkspace`, `WorkspaceReceipt`, and `WorkspaceInspectionSnapshot`.
- `src/ccp_studio/services/workspace_service.py` owns brand workspace lifecycle commands, active brand context switching, workspace inspection, and brand-scoped object listing.
- `src/ccp_studio/repositories/brand_workspaces.py` stores brand workspace lifecycle records in memory.
- `src/ccp_studio/domain/policies/workspace_lifecycle_policy.py` enforces workspace lifecycle permissions and status transitions.
- `tests/cmf_studio/test_workspace_lifecycle.py` verifies existing brand workspace lifecycle behavior, including object storage path guard behavior.
- `operator-web/src/App.jsx` contains existing workspace UI copy for guest/brand workspace surfaces.

## 2. Existing Artifact/Storage Files Found

- `src/ccp_studio/repositories/source_artifacts.py` stores source artifact manifests, quality reports, and source intake receipts.
- `src/ccp_studio/providers/provider_storage.py` stores provider output bytes under `storage/provider_outputs`, writes metadata JSON, and computes sha256 hashes.
- `src/ccp_studio/contracts/asset_intelligence.py`, `asset_package.py`, `visual_research.py`, and related services model creative assets and rights/provenance, but they do not define deterministic client workspace folders.
- `src/ccp_studio/contracts/video_editing_engine.py` and `src/ccp_studio/services/video_render_contract_service.py` use render/export receipts and hashes for video outputs.
- `src/ccp_studio/contracts/video_timeline_workbench.py` contains backend read models for timeline render summaries and output sha256 values.

## 3. Existing Source Artifact Manifest Files Found

- `src/ccp_studio/contracts/source.py` defines `SourceArtifact`, `SourceArtifactManifest`, and source intake contracts.
- `src/ccp_studio/services/source_ingestion.py` and `src/ccp_studio/workflows/source_ingestion.py` are existing source ingestion paths.
- `src/ccp_studio/contracts/source_provenance.py` and `src/ccp_studio/services/source_provenance_service.py` preserve source provenance and consent/review evidence.
- `tests/cmf_studio/test_source_artifact_gate.py` and `tests/cmf_studio/test_source_ingestion_transcript_alignment_and_provenance.py` verify source artifact and provenance behavior.

## 4. Existing Render/Export Artifact Files Found

- `src/ccp_studio/contracts/deterministic_rendering.py`, `services/deterministic_rendering_service.py`, and `api/v1/renders.py` support deterministic render contracts and receipts.
- `src/ccp_studio/contracts/video_editing_engine.py`, `services/video_render_contract_service.py`, and `services/video_export_service.py` define fake proxy/final render receipts, OTIO audit timelines, and export packs.
- `src/ccp_studio/services/carousel_render_service.py` provides deterministic carousel render receipts.
- `src/ccp_studio/services/avatar_render_payload_service.py` compiles avatar render payloads but does not execute final render.

## 5. Existing UI References To Workspace/Artifacts

- `operator-web/src/App.jsx` includes guest workspace and brand workspace UI sections.
- `operator-web/src/api/videoTimeline.js` calls proxy-render and OTIO-export backend endpoints.
- `operator-web/src/types/supervisualRuntime.js` references materialized asset statuses.
- Existing UI code is not modified by this bundle.

## 6. Naming Conflicts

- Existing `WorkspaceStatus` appears in `workspace_lifecycle.py`; the bundle introduces a project-workspace-specific `WorkspaceStatus` in a new module. This is acceptable because imports remain explicit.
- Existing source artifact manifests are source-ingestion specific; the new `ArtifactManifest` is broader and remains in `project_workspace_artifact_store.py`.
- Existing provider storage writes files and hashes provider outputs; the new artifact store records deterministic workspace artifact refs and versions. It does not replace provider storage in this branch.

## 7. Additive Application Assessment

The bundle can be applied additively. The target namespace is currently absent:

- `docs/architecture/project-workspace-artifact-store/`
- `registries/canonical/project_workspace/`
- `src/ccp_studio/contracts/project_workspace_artifact_store.py`
- `src/ccp_studio/repositories/project_workspace_artifact_store.py`
- `src/ccp_studio/services/*artifact*` files from this bundle

Existing brand workspace lifecycle, source artifacts, provider storage, and render/export systems are preserved.

## 8. Files Requiring Merge Instead Of Copy

No existing target implementation files require merge. The bundle includes package `__init__.py` files and pycache from local verification; those are not copied. The integration copies only the explicit contract, repository, services, docs, registries, skills, and tests requested by the prompt.
