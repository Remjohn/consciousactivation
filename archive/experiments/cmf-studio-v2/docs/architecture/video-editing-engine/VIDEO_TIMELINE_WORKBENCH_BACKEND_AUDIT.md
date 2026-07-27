# Video Timeline Workbench Backend Audit

## Backend Route Files Found

- Existing route files live under `src/ccp_studio/api/v1/`.
- Routes are exposed as module-level `router` objects or through factory helpers, then tests mount them with `FastAPI().include_router(...)`.
- Existing examples inspected:
  - `src/ccp_studio/api/v1/orchestration.py`
  - `src/ccp_studio/api/v1/supervisual_runtime.py`

## API Router Mounting Pattern

- The repo does not expose a single central app registration file in the inspected API package.
- API tests commonly create a local FastAPI app and include the target router.
- The new workbench router follows this pattern with `create_video_timeline_workbench_router(service)` and a module-level `router` when FastAPI imports cleanly.

## Existing Video Endpoints

- No existing `video-edit-programs` route module was present under `src/ccp_studio/api/v1/`.
- Tech specs reference `/api/v1/video-edit-programs/...`, and the operator-web client already calls that prefix.

## Existing Read Models

- No `VideoTimelineWorkbenchReadModel` contract existed before this integration.
- Video Editing Engine V1 already provides the backend source objects needed for a read model:
  - `VideoTimelineProgram`
  - `VideoTrackProgram`
  - `VideoLayerProgram`
  - `VideoSceneTimingPlan`
  - `ProxyRenderReceipt`
  - `OTIOAuditTimeline`
  - `VideoEvaluationReceipt`
  - `OperatorVideoRevisionCommand`

## Existing Service Dependencies

- `src/ccp_studio/services/video_editing_engine_service.py`
- `src/ccp_studio/services/video_render_contract_service.py`
- `src/ccp_studio/services/video_revision_service.py`
- `src/ccp_studio/services/video_export_service.py`
- Golden Path files are present:
  - `src/ccp_studio/contracts/golden_path_orchestrator.py`
  - `src/ccp_studio/services/format02_golden_path_orchestrator_service.py`
  - `fixtures/golden_path/`

## Endpoint Gaps

- Missing before this integration:
  - current timeline workbench read model endpoint
  - timeline edit proposal endpoint
  - timeline edit submission endpoint
  - fake proxy render endpoint
  - OTIO audit export endpoint

## Recommended Additive Route Location

- `src/ccp_studio/api/v1/video_timeline_workbench.py`

This keeps the existing API file-per-domain pattern and avoids creating a second app or second video engine.
