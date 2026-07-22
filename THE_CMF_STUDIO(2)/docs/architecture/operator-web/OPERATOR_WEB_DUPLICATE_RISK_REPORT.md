# Operator Web Duplicate Risk Report

The repo already contains several screens that should be extended rather than duplicated.

## Duplicate-Risk Areas

| Area | Existing Files | Existing Screen Purpose | Missing Pieces | Recommended Approach |
|---|---|---|---|---|
| Control Tower / Operations | `operator-web/src/App.jsx`, `operator-web/src/screens/OperationsCommandCenter.jsx`, `operator-web/src/data.js` | Operator command center, active guest status, command receipt ledger, operational controls | Backend read model connection to `OperatorUiService` / `OperationsBoardService`; router mount verification | Extend existing Control Tower and Operations screens. Add backend endpoint/client wiring; keep offline `data.js` fallback. Do not build a new command center. |
| Pipeline Monitor / Golden Path Visibility | `operator-web/src/App.jsx` inline `PipelineView`, `operator-web/src/data.js` | Shows production pipeline stages from static data | Pipeline run list, Golden Path run state, stage receipts, gate actions | Extend `PipelineView` or split an internal tab in the existing route. Add orchestration/Golden Path read model first. |
| Composition Studio | `operator-web/src/App.jsx` inline `CompositionStudio`, `operator-web/src/data.js` | Shows composition templates, mockup boards, assets | Backend composition scene/read model, cognitive load/lock state, provider boundary visibility | Extend existing Composition screen. Do not create a parallel composition app. |
| SuperVisual Studio | `operator-web/src/screens/SuperVisualStudio.jsx`, `operator-web/src/components/supervisual/*`, `operator-web/src/api/supervisualRuntime.js`, hooks | Backend-connected SuperVisual operator UI | Router mount verification, optional fallback behavior, duplicate untracked client cleanup | Continue extending this screen. Do not use untracked `api/supervisuals.js` as a new path until reviewed. |
| Video Timeline Workbench | `operator-web/src/screens/VideoTimelineWorkbench.jsx`, `operator-web/src/components/timeline/*`, `operator-web/src/api/videoTimeline.js`, `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` | Timeline editor/workbench with fixture fallback and backend client | Router mount verification, backend source mode rollout, persistence | Extend existing workbench. Do not build another timeline UI. |
| Review Workbench | `operator-web/src/App.jsx` inline `ReviewWorkbench`, `operator-web/src/data.js` | Review/evidence style view from static eval/assets | Review packet API, review decision client, evaluation read model | Extend existing Review screen; add backend read model and action clients. |
| Agents / Agent Factory | `operator-web/src/App.jsx` inline `AgentFactory`, `operator-web/src/data.js` | Agent overview from static data | API client to `operator-ui/agent-factory` or `agent-factory` routes | Extend existing Agents screen. |
| Evals / Receipts | `operator-web/src/App.jsx` inline `EvalsView`, `operator-web/src/data.js` | Eval receipt list from static data | Evaluation receipt list/review endpoint wiring | Extend existing Evals screen. |
| Client Workspace | `operator-web/src/App.jsx` inline `GuestWorkspace`, `operator-web/src/data.js` | Guest/client workspace summary | Artifact store visibility, workspace materialization, reference list | Product decision needed: extend Guests into Workspace or add a subview, but avoid a separate disconnected workspace shell. |

## Specific Duplicate-Risk Files

- `operator-web/src/api/supervisuals.js` is untracked and overlaps with `operator-web/src/api/supervisualRuntime.js`.
- `src/ccp_studio/api/v1/supervisual.py` is untracked and overlaps the `/api/v1/supervisual` prefix used by committed `supervisual_runtime.py`.
- `operator-web/src/components/supervisual/SuperVisualPanels.jsx` is untracked while committed SuperVisual components already exist in `operator-web/src/components/supervisual/`.

These files may represent useful work from another branch, but they should be reviewed before any new UI bundle relies on them.

## Do-Not-Build-New-Screen Recommendations

- Do not build a new Video Timeline Workbench.
- Do not build a new SuperVisual Studio.
- Do not build a new Control Tower or Operations command center.
- Do not build a new Composition Studio without first deciding whether the existing inline screen should become the canonical composition route.
- Do not delete fixtures; keep them as offline/demo fallback.
