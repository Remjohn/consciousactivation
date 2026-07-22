# Operator Web Fixture Dependency Audit

Fixture mode should remain available as offline fallback. No fixtures were removed or changed in this audit.

## Fixture And Static Data Sources

| Fixture/Data File | Screens Using It | Data Shape | Backend Fallback Exists? | Demo/Offline Role | Expected Backend Endpoint | Related Backend Contract/Service | Recommendation |
|---|---|---|---:|---|---|---|---|
| `operator-web/src/data.js` | `ControlTower`, `GuestWorkspace`, `InterviewBrief`, `PipelineView`, `CompositionStudio`, `ReviewWorkbench`, `AgentFactory`, `EvalsView`, shell nav | `navItems`, `guests`, `pipelineStages`, `compositionTemplates`, `stillVisualMockupBoards`, `assets`, `agents`, `evalReceipts`, `contentFormats`, `interviewBrief` | partial via command submit only | Primary shell demo data and offline state | Mixed: `/api/v1/operator-ui/shell`, `/control-tower`, `/content-formats`, `/agent-factory/{brand_workspace_id}`, plus operations, orchestration, review, evaluations, workspace/artifact endpoints | `operator_ui.py`, `operations.py`, `orchestration.py`, `review_state.py`, `evaluations.py`, `project_workspace_artifact_store.py` | Keep as offline fallback. Incrementally replace each screen with read models rather than deleting the file. |
| `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` | `VideoTimelineWorkbench.jsx` through `operator-web/src/api/videoTimeline.js` and `TimelineWorkbenchProvider.jsx` | `cmf.video_timeline_workbench_state.v1`: workbench ids, program id, frame/timing data, lanes, segments, transcript markers, render refs, blocker codes, valid commands | yes | Default fixture mode unless `VITE_CMF_TIMELINE_FIXTURE_MODE=false` | `GET /api/v1/video-edit-programs/current/timeline-workbench`, edit, proxy render, and OTIO endpoints | `VideoTimelineWorkbenchReadModel`, `VideoTimelineWorkbenchService` | Keep as fallback. Backend path appears ready but the frontend defaults to fixture mode. |

## Notable Fixture Behavior

- Timeline fixture mode is enabled by default through `VITE_CMF_TIMELINE_FIXTURE_MODE !== "false"`.
- Timeline API calls fall back to fixture responses on non-OK responses or network errors.
- Operator command submission falls back to `runtime_mode: "offline-ui-ledger"` if `/api/v1/operator-ui/commands` or `/commands/submit` fails.
- SuperVisual Studio does not have an explicit fixture fallback in the audited active client/hook path.

## Fixture-Only Screens

| Screen | Fixture/Data Source | Backend Candidate | Missing Work |
|---|---|---|---|
| Pipeline | `pipelineStages` in `data.js` | `/api/v1/orchestration/prepare-stage`, production orchestration routes, Golden Path spine mapping | Pipeline run read model and frontend API client. |
| Composition | `compositionTemplates`, `stillVisualMockupBoards`, `assets` in `data.js` | `/api/v1/composition-runtime/*`, `/api/v1/compositions/*` | Composition workbench read model and API client. |
| Review | `evalReceipts`, `assets` in `data.js` | `/api/v1/review-states`, `/api/v1/review-decisions`, `/api/v1/evaluations` | Review packet/read model API and frontend wiring. |
| Agents | `agents` in `data.js` | `/api/v1/operator-ui/agent-factory/{brand_workspace_id}`, `/api/v1/agent-factory/*` | Agent factory read model client. |
| Evals | `evalReceipts` in `data.js` | `/api/v1/evaluations/receipts/{id}/review` | Evaluation receipt list/read model API. |
| Guests / Workspace | `guests` in `data.js` | Workspace/artifact services; no route found | Client workspace endpoints and artifact browser read model. |
| Interview Brief | `interviewBrief` in `data.js` | Narrative Story Doctor services; no UI route found | Brief/extraction read model and API. |
