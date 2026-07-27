# Operator Web Navigation And Read Model Audit Summary

## Branch

`audit/operator-web-nav-read-models`

## Baseline Backend Test Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result before audit docs: `775 passed, 10 skipped in 18.13s`.

## Frontend Scripts Available

From `operator-web/package.json`:

- `dev`: `vite --host 127.0.0.1`
- `build`: `vite build`
- `preview`: `vite preview --host 127.0.0.1`

Unavailable:

- `test`
- `lint`
- `typecheck`

No frontend test/lint command was run because the scripts do not exist. `build` was not run because this is a docs-only audit and the prompt asked to inspect scripts and run non-mutating checks only if available.

## Screens Found

- Control Tower
- Operations
- Guests / Guest Workspace
- Interview Brief
- Pipeline
- Composition
- SuperVisual Studio
- Video Timeline Workbench
- Review Workbench
- Agents
- Evals

## Screens Missing

- Dedicated Reference Library / Reference Manager
- Carousel Studio
- Avatar Library / Avatar Builder
- Template Atlas / Template Preview
- Capability / Provider / Render readiness screen
- Artifact / Workspace file browser
- Golden Path / Demo Run view
- Local Render Worker / Render Queue
- Provider Jobs dashboard
- Publishing / Publer dashboard

## Fixture-Only Screens

- Pipeline
- Composition
- Review
- Agents
- Evals
- Guests / Workspace
- Interview Brief

Video Timeline Workbench has fixture fallback and defaults to fixture mode unless `VITE_CMF_TIMELINE_FIXTURE_MODE=false`.

## Backend Routes Found

UI-relevant route families found:

- `/api/v1/operator-ui`
- `/api/v1/video-edit-programs`
- `/api/v1/supervisual`
- `/api/v1/operations`
- `/api/v1/orchestration`
- `/api/v1/composition-runtime`
- `/api/v1/compositions`
- `/api/v1/review-states`
- `/api/v1/review-decisions`
- `/api/v1/evaluations`
- `/api/v1/provider-jobs`
- `/api/v1/renders`
- `/api/v1/acting-library`
- `/api/v1/publishing-intents`
- `/api/v1/source`
- `/api/v1/source-provenance`

No central FastAPI app/router mount file was found under `src`, so each route is recorded as "router exists; app mount not found."

## Backend Routes Missing

Missing screen-shaped backend endpoint groups:

- Client workspace / artifact browser routes
- Reference library/upload routes
- Pipeline run list/detail routes
- Golden Path run/get/read model routes
- Capability Preflight / Provider Menu routes
- Template Atlas routes
- Avatar Library Builder routes
- Carousel runtime/read model routes
- Review packet routes matching the current Review Workbench
- Render worker dashboard routes
- Provider job sample approval/batch dashboard routes

## Read Models Found

- `OperatorShellState`
- `WorkspaceControlTowerState`
- `ContentAssetFormatRegistryState`
- `AgentFactoryState`
- `VideoTimelineWorkbenchReadModel`
- `VideoTimelineEditReceipt`
- `ProxyRenderResponse`
- `OTIOExportResponse`
- `SuperVisualProjectDetailResponse`
- `SuperVisualVariantDetailResponse`
- `SuperVisualSnapshot`
- `SuperVisualEvent`
- `ReviewReadModel`
- `ReviewEvidenceState`
- `EvaluationReviewReadModel`
- `OperationsBoardState`
- `GoldenPathRun`
- `CapabilityPreflightReport`
- `ProviderMenuSummary`
- `ClientWorkspace`
- `ArtifactManifest`
- `ProviderJob`
- `ProviderReceipt`
- `PublishingIntent`

## Read Models Missing

- Workspace/artifact browser UI read model
- Reference library UI read model
- Pipeline run monitor read model
- Golden Path run UI read model
- Capability/Provider readiness UI read model route
- Template Atlas read model
- Avatar 64-state grid UI read model
- Carousel Studio UI read model
- Provider job sample approval read model
- Local render worker dashboard read model

## Duplicate-Risk Areas

- Control Tower / Operations
- Pipeline Monitor / Golden Path visibility
- Composition Studio
- SuperVisual Studio
- Video Timeline Workbench
- Review Workbench
- Agents / Agent Factory
- Evals / Receipts
- Client Workspace / Guests

Untracked duplicate-risk files were observed in the dirty worktree:

- `operator-web/src/api/supervisuals.js`
- `operator-web/src/components/supervisual/SuperVisualPanels.jsx`
- `src/ccp_studio/api/v1/supervisual.py`
- `src/ccp_studio/contracts/supervisual_projects.py`
- `src/ccp_studio/repositories/supervisual_projects.py`
- `src/ccp_studio/services/supervisual_project_service.py`
- `tests/cmf_studio/test_supervisual_projects_api.py`

These were not modified or staged by this audit.

## Audit Documents

- `docs/architecture/operator-web/OPERATOR_WEB_NAVIGATION_AUDIT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_FIXTURE_DEPENDENCY_AUDIT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_FRONTEND_API_AUDIT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_BACKEND_ROUTE_AUDIT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_BACKEND_READ_MODEL_AUDIT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_UI_WIRING_MATRIX.md`
- `docs/architecture/operator-web/OPERATOR_WEB_DUPLICATE_RISK_REPORT.md`
- `docs/architecture/operator-web/OPERATOR_WEB_MISSING_BACKEND_ENDPOINTS.md`
- `docs/architecture/operator-web/OPERATOR_WEB_UI_PRIORITY_PLAN.md`

## Recommended Next Prompts/Bundles

1. `PROMPT_02_CONNECT_VIDEO_TIMELINE_WORKBENCH_BACKEND` if app mounting/runtime rollout is not complete.
2. `PROMPT_CONNECT_PIPELINE_AND_GOLDEN_PATH_RUN_MONITOR_V1`.
3. Client Workspace / Artifact Browser read-model and UI wiring.
4. Capability Preflight / Provider Menu API and UI wiring.
5. Reference Library upload/register/approve UI.

## Implementation Statement

No implementation changes were made beyond documentation/audit files.
