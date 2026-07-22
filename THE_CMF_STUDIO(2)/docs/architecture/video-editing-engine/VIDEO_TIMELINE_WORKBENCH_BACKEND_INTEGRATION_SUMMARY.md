# Video Timeline Workbench Backend Integration Summary

## Branch

`feat/video-timeline-workbench-backend-v1`

## Frontend Files Inspected

- `operator-web/src/screens/VideoTimelineWorkbench.jsx`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- `operator-web/src/components/timeline/`
- `operator-web/src/state/timelineDraftReducer.js`
- `operator-web/package.json`

## Endpoints Expected By Frontend

- `GET /api/v1/video-edit-programs/current/timeline-workbench`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/propose`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/submit`
- `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- `POST /api/v1/video-edit-programs/{program_id}/otio-exports`

## Backend API Files Inspected

- `src/ccp_studio/api/v1/orchestration.py`
- `src/ccp_studio/api/v1/supervisual_runtime.py`
- `tests/cmf_studio/test_supervisual_runtime_api_v1.py`
- `tests/cmf_studio/test_orchestration_records.py`

## Routes Added

- `src/ccp_studio/api/v1/video_timeline_workbench.py`

Added:
- `GET /api/v1/video-edit-programs/current/timeline-workbench`
- `GET /api/v1/video-edit-programs/{program_id}/timeline-workbench`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/propose`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/submit`
- `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- `POST /api/v1/video-edit-programs/{program_id}/otio-exports`

## Contracts / Read Models Added

- `src/ccp_studio/contracts/video_timeline_workbench.py`

Includes:
- `VideoTimelineWorkbenchReadModel`
- `VideoTimelineWorkbenchProgramSummary`
- `VideoTimelineWorkbenchScene`
- `VideoTimelineWorkbenchTrack`
- `VideoTimelineWorkbenchLayer`
- `VideoTimelineWorkbenchCaptionCue`
- `VideoTimelineWorkbenchSoundCue`
- `VideoTimelineWorkbenchRenderSummary`
- `VideoTimelineWorkbenchEvalSummary`
- `VideoTimelineEditProposal`
- `VideoTimelineEditSubmission`
- `VideoTimelineEditReceipt`
- `ProxyRenderRequest`
- `ProxyRenderResponse`
- `OTIOExportRequest`
- `OTIOExportResponse`

## Services Added

- `src/ccp_studio/services/video_timeline_workbench_service.py`

The service builds backend/demo read models from `VideoTimelineProgram`, translates Video Engine tracks/layers into UI lanes/segments, compiles typed revision commands, returns fake proxy render receipts, and returns OTIO audit timelines.

## Tests Added

- `tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`

## Test Results

- Baseline before changes:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `724 passed, 4 skipped`
- Targeted backend:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`
  - Result: `6 passed, 6 skipped`
- Full CMF:
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `730 passed, 10 skipped`
- Frontend build:
  - `npm --prefix operator-web run build`
  - Result: passed. PowerShell emitted an npm prefix permission warning before Vite completed successfully.

## Fixture Fallback Status

Fixture fallback is preserved. When `VITE_CMF_TIMELINE_FIXTURE_MODE` is not `false`, the UI remains fixture-driven. When fixture mode is disabled and the backend is unavailable, the client returns the existing fixture with `source_mode="fixture"`.

## Source Modes

- `backend`: read model built from an existing `VideoTimelineProgram`
- `demo`: deterministic backend-generated Video Editing Engine V1 timeline
- `fixture`: operator-web fixture fallback

## Safety Confirmations

- No real providers are called.
- No real Remotion calls are made.
- No FFmpeg calls are made.
- Proxy render responses use fake `ProxyRenderReceipt` objects.
- OTIO export responses use `OTIOAuditTimeline` read-model data and do not write files.
- Timeline edit endpoints compile typed revision commands and fake revision receipts rather than mutating arbitrary JSON.

## Known Limitations

- In-memory/demo timeline state only.
- No database persistence.
- FastAPI route tests skipped in this local environment because importing FastAPI fails on missing `annotated_doc`; service-level backend behavior is covered.
- No real render worker.
- No real Remotion or FFmpeg calls.
- No real OTIO file is written.
- Frontend fixture fallback remains available in offline mode.
- Golden Path-backed persistent state can be added when the runtime stores timeline objects.

## Next Recommended Step

Add a persistent Video Timeline Workbench runtime store or wire the Golden Path run output into the workbench service so `source_mode="backend"` can load previously compiled timeline programs instead of generating deterministic demo state.
