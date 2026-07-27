# Pipeline Run Monitor Backend Audit

Branch: `feat/operator-pipeline-run-monitor-ui`

## Existing Route Files

- `src/ccp_studio/api/v1/video_timeline_workbench.py`
- `src/ccp_studio/api/v1/client_workspace_reference.py`
- `src/ccp_studio/api/v1/orchestration.py`
- `src/ccp_studio/api/v1/operator_ui.py`
- Added: `src/ccp_studio/api/v1/pipeline_run_monitor.py`

## Existing Route Mounting Pattern

Recent feature routes use optional FastAPI imports and route factory functions:

- `create_video_timeline_workbench_router(...)`
- `create_client_workspace_reference_router(...)`

No central FastAPI application mount file was found in `src/ccp_studio`. The new monitor route follows the route-factory convention and is tested by mounting the router into a local FastAPI app.

## Existing Pipeline/Orchestration Read Models

- `src/ccp_studio/contracts/studio_pipeline_recipe_harness.py`
  - `PipelineRecipe`
  - `PipelineRun`
  - `PipelineStepRun`
  - `PipelineStepReceipt`
  - `PipelineArtifactRef`
  - `PipelineApprovalGate`
  - `PipelineRunBlocker`
  - `PipelineRunSummary`
- `src/ccp_studio/contracts/orchestration.py`
  - Existing orchestration spine contract.
- Added: `src/ccp_studio/contracts/pipeline_run_monitor.py`
  - Operator-facing read models only.

## Existing Golden Path Repositories/Services

- `src/ccp_studio/contracts/golden_path_orchestrator.py`
- `src/ccp_studio/services/format02_golden_path_orchestrator_service.py`
- `src/ccp_studio/repositories/golden_path_orchestrator.py`
- `src/ccp_studio/services/format02_golden_path_recipe_adapter_service.py`

The monitor does not rerun Golden Path. It reads/projects monitor state and provides deterministic synthetic fallback when repository state is not available.

## Existing Pipeline Recipe Harness Repositories/Services

- `src/ccp_studio/repositories/studio_pipeline_recipe_harness.py`
- `src/ccp_studio/services/pipeline_recipe_catalog_service.py`
- `src/ccp_studio/services/pipeline_run_service.py`
- `src/ccp_studio/services/pipeline_run_summary_service.py`
- `src/ccp_studio/services/pipeline_orchestration_spine_adapter_service.py`

## Existing Test Client Pattern

Backend route tests mount feature route factories into a local `fastapi.FastAPI()` test app. This prompt follows the same pattern in `tests/cmf_studio/test_pipeline_run_monitor_backend_v1.py`.

## Missing Endpoints Filled

- `GET /api/v1/pipeline-runs`
- `GET /api/v1/pipeline-runs/{pipeline_run_id}`
- `GET /api/v1/pipeline-runs/{pipeline_run_id}/scene-outputs`
- `GET /api/v1/golden-path-runs/{golden_path_run_id}`

## Recommended Additive Route Location

`src/ccp_studio/api/v1/pipeline_run_monitor.py`

This route file is additive and does not replace orchestration, Golden Path, or recipe harness route/service code.
