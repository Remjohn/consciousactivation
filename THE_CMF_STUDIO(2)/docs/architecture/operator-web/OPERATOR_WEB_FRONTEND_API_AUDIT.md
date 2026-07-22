# Operator Web Frontend API Audit

## API Base Helpers

| File | Purpose | Base URL Behavior | Notes |
|---|---|---|---|
| `operator-web/src/lib/apiClient.js` | JSON fetch helper for newer runtime clients | `VITE_API_BASE_URL`, stripped trailing slash | Throws `ApiError` on non-OK responses. Used by `supervisualRuntime.js`. |
| `operator-web/src/api/operatorRuntime.js` | Operator command and lightweight connectivity client | `VITE_CMF_API_BASE_URL` or empty string | Has offline ledger fallback for command submission. |
| `operator-web/src/api/videoTimeline.js` | Video Timeline Workbench client | relative paths, no base helper | Fixture mode defaults on unless `VITE_CMF_TIMELINE_FIXTURE_MODE=false`. |

## Frontend API Calls

| Function | Method | Endpoint | Request Shape | Response/Read Model Shape | Caller | Fallback/Error Behavior | Backend Route Status |
|---|---|---|---|---|---|---|---|
| `testOperatorApi` | GET | `/api/v1/operator-ui/content-formats` | none | `ContentAssetFormatRegistryState` summarized into connected/offline status | `App.jsx` command/status flow | Returns `{state:"offline"}` on failure | router exists in `operator_ui.py`; app mount not found |
| `submitOperatorUiCommand` | POST | `/api/v1/operator-ui/commands` | command envelope fields: requested user/role, organization, workspace, guest, active object, command type/payload, source route | `UiCommandEnvelope` | `App.jsx` commands from multiple screens | falls back to local receipt | router exists; app mount not found |
| `submitOperatorUiCommand` | POST | `/api/v1/operator-ui/commands/submit` | `{ envelope, blockers, content_asset_code, object_version_current }` | `UiActionReceipt` normalized into UI receipt | `App.jsx` commands from multiple screens | falls back to local receipt | router exists; app mount not found |
| `fetchVideoTimelineWorkbench` | GET | `/api/v1/video-edit-programs/current/timeline-workbench?format={formatSlot}` | query `format` | `VideoTimelineWorkbenchReadModel` or fixture state | `TimelineWorkbenchProvider.jsx` | returns fixture if fixture mode, fetch fails, or response non-OK | router exists; app mount not found |
| `proposeTimelineEdit` | POST | `/api/v1/video-edit-programs/{program_id}/timeline-edits/propose` | draft object from timeline reducer | proposal result/read receipt | `TimelineWorkbenchProvider.jsx` | local fixture draft on failure | router exists; app mount not found |
| `submitTimelineEditCommand` | POST | `/api/v1/video-edit-programs/{program_id}/timeline-edits/submit` | command with `program_id`, `command_id`, `payload`, expected version | `VideoTimelineEditReceipt` or fixture receipt | `TimelineWorkbenchProvider.jsx` | local receipt on failure | router exists; app mount not found |
| `requestProxyRerender` | POST | `/api/v1/video-edit-programs/{program_id}/proxy-renders` | no body in current frontend | `ProxyRenderResponse` or fixture receipt | `TimelineWorkbenchProvider.jsx` | local queued receipt on failure | router exists; app mount not found |
| `requestOtioExport` | POST | `/api/v1/video-edit-programs/{program_id}/otio-exports` | no body in current frontend | `OTIOExportResponse` or fixture receipt | `TimelineWorkbenchProvider.jsx` | local coverage-ready receipt on failure | router exists; app mount not found |
| `listSuperVisualProjects` | GET | `/api/v1/supervisual/projects` | none | list of `SuperVisualProject` | SuperVisual hooks/screen | `ApiError` normalized in hooks; no fixture fallback | router exists; app mount not found |
| `createSuperVisualProject` | POST | `/api/v1/supervisual/projects` | project payload plus `actor_id`, `idempotency_key` | `SuperVisualProjectDetailResponse`/project detail | SuperVisual hooks/screen | error normalized; no fixture fallback | router exists; app mount not found |
| `getSuperVisualProject` | GET | `/api/v1/supervisual/projects/{project_id}` | none | `SuperVisualProjectDetailResponse` | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `updateSuperVisualProject` | PATCH | `/api/v1/supervisual/projects/{project_id}` | update payload plus command metadata | project detail | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `createSuperVisualVariant` | POST | `/api/v1/supervisual/projects/{project_id}/variants` | variant payload plus command metadata | `SuperVisualVariantDetailResponse` | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `getSuperVisualVariant` | GET | `/api/v1/supervisual/variants/{variant_id}` | none | `SuperVisualVariantDetailResponse` | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `cloneSuperVisualVariant` | POST | `/api/v1/supervisual/variants/{variant_id}/clone` | clone payload plus command metadata | variant detail | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `getSuperVisualSnapshot` | GET | `/api/v1/supervisual/variants/{variant_id}/snapshot` | none | `SuperVisualSnapshot` | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `getSuperVisualEvents` | GET | `/api/v1/supervisual/variants/{variant_id}/events` | none | list of `SuperVisualEvent` | SuperVisual hooks/screen | error normalized | router exists; app mount not found |
| `startSuperVisualBuildRun` | POST | `/api/v1/supervisual/variants/{variant_id}/build-runs` | command metadata payload | `SuperVisualBuildRun` | SuperVisual actions hook | error normalized | router exists; app mount not found |
| `getSuperVisualBuildRun` | GET | `/api/v1/supervisual/build-runs/{build_run_id}` | none | `SuperVisualBuildRun` | SuperVisual actions hook | error normalized | router exists; app mount not found |
| `runSuperVisualStep` | POST | `/api/v1/supervisual/build-runs/{build_run_id}/steps/{step_name}/run` | command metadata payload | step/run detail | SuperVisual actions hook | error normalized | router exists; app mount not found |
| `lockSuperVisualComposition` and other write actions | POST | `/api/v1/supervisual/variants/{variant_id}/composition/*`, `/provider-blueprints`, `/materialize`, `/render-contract`, `/render`, `/evaluate`, `/revisions`, `/approve`, `/export` | typed payloads plus `actor_id` and `idempotency_key` | runtime variant/snapshot/event updates | SuperVisual actions hook | error normalized | router exists; app mount not found |

## Untracked/Duplicate-Risk Client

`operator-web/src/api/supervisuals.js` exists in the worktree as untracked code. It targets older project-style endpoints such as `/api/v1/supervisual/projects/{project_id}/build`, `/revise`, `/approve`, `/reject`, `/export`, and `/timeline`. It is not the active SuperVisual Studio client found in `SuperVisualStudio.jsx`/hooks. Treat it as duplicate-risk until reviewed; do not build new UI on top of it without resolving ownership.

## Missing Frontend API Clients

No dedicated frontend API clients were found for:

- Client workspace / artifact store
- Reference library / uploads
- Carousel Engine
- Composition Intelligence workbench
- Golden Path run visibility
- Capability Preflight / Provider Menu
- Avatar library builder
- Template Atlas / preview
- Provider job sample approval
- Local render worker / render queue
- Publishing / Publer
