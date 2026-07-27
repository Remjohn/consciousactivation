# Pipeline Run Monitor UI Integration Summary

## Branch

`feat/operator-pipeline-run-monitor-ui`

## Existing Pipeline View Files Inspected

- `operator-web/src/App.jsx`
- `operator-web/src/data.js`

## Existing Operations Command Center Files Inspected

- `operator-web/src/screens/OperationsCommandCenter.jsx`

## Backend Routes Added/Reused

Added:

- `GET /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs/{pipeline_run_id}`
- `GET /api/v1/pipeline-runs/{pipeline_run_id}/scene-outputs`
- `GET /api/v1/golden-path-runs/{golden_path_run_id}`

Route file:

- `src/ccp_studio/api/v1/pipeline_run_monitor.py`

The route follows the existing route-factory test pattern. No central FastAPI app mount file was found.

## Backend Services Added/Reused

Added:

- `src/ccp_studio/services/pipeline_run_monitor_service.py`

Reused:

- `PipelineRecipeCatalogService`
- `PipelineRunService`
- `PipelineRunSummaryService`
- `PipelineArtifactRefService`
- Existing Studio Pipeline Recipe Harness contracts
- Existing Format 02 Golden Path identifiers/read-model concepts

## Frontend Files Modified

- `operator-web/src/App.jsx`
- `operator-web/src/screens/OperationsCommandCenter.jsx`
- `operator-web/src/styles.css`

Added:

- `operator-web/src/api/pipelineRunMonitor.js`
- `operator-web/src/fixtures/pipelineRunMonitor.fixture.js`

## Fixture Fallback Status

Preserved and extended.

The Pipeline Run Monitor API client uses backend responses when available and falls back to a same-shaped fixture when the backend is unavailable or `VITE_CMF_PIPELINE_MONITOR_FIXTURE_MODE=true`.

## Read Models Added/Reused

Added:

- `PipelineRunStatusReadModel`
- `PipelineStageReceiptReadModel`
- `PipelineArtifactReadModel`
- `PipelineApprovalReadModel`
- `PipelineBlockerReadModel`
- `PipelineSceneOutputLinkReadModel`
- `PipelineRunMonitorReadModel`
- `GoldenPathRunDetailReadModel`

Read model file:

- `src/ccp_studio/contracts/pipeline_run_monitor.py`

## Golden Path Detail Route/Page

Added as a detail panel inside the existing Pipeline View, not as a duplicate screen.

Backend detail endpoint:

- `GET /api/v1/golden-path-runs/{golden_path_run_id}`

## Scene Output Link Behavior

Scene output links are deterministic and safe:

- Template preview: `/template-preview/format02_scene_01`
- Video preview: `/timeline?program_id=timeline_health_myth_demo`

When the corresponding artifact is missing, the UI shows the pointer and marks preview unavailable rather than exposing local filesystem paths.

## Template Preview Link Behavior

No dedicated Template Atlas operator-web route was found. Template preview links are included as stable placeholders and documented as synthetic/fixture when not backend-backed.

## Video Preview Link Behavior

The Video Timeline Workbench exists as the `timeline` view. The read model carries `/timeline?program_id=timeline_health_myth_demo`, and the existing Pipeline View UI opens the `timeline` workbench view for the video preview action.

## Tests Run

Backend targeted:

- `PYTHONPATH=src python -m compileall -q src`
- `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_pipeline_run_monitor_backend_v1.py`
- Result: `12 passed, 1 skipped`

Related backend:

- `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_studio_pipeline_recipe_harness_v1.py tests/cmf_studio/test_format02_golden_path_orchestrator_v1.py tests/cmf_studio/test_pipeline_run_monitor_backend_v1.py`
- Result: `36 passed, 1 skipped`

Full backend:

- `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
- Result: `955 passed, 14 skipped`

Frontend:

- `npm --prefix operator-web run build -- --outDir ../.tmp/operator-web-pipeline-monitor-build-2`
- Result: Vite build passed. PowerShell emitted an existing npm profile access warning before the build.

`operator-web/package.json` exposes `dev`, `build`, and `preview`; no `test` or `lint` scripts are available.

## Confirmation No Providers Were Called

Confirmed. The monitor service is read-model only and sets `provider_calls_executed=false`.

## Confirmation No Renderers Were Called

Confirmed. The monitor service is read-model only and sets `renderer_calls_executed=false`.

## Confirmation No Local Render Worker Jobs Were Executed

Confirmed. The monitor service does not import or call Local Render Worker services and sets `local_worker_jobs_executed=false`.

## Known Limitations

- Read-model/UI only.
- No live websocket updates.
- No pipeline execution.
- No provider execution.
- No renderer execution.
- No Local Render Worker execution.
- Fixture fallback remains.
- Template preview route is represented by deterministic placeholder links until Template Atlas UI routing exists.
- Backend route factory is added, but no central FastAPI mount file was found.
- Synthetic monitor state is used when no persisted PipelineRun/GoldenPathRun repository state is available.

## Next Recommended Step

Provider Sample Approval UI or Operator Render Worker Dashboard, depending on roadmap priority.
