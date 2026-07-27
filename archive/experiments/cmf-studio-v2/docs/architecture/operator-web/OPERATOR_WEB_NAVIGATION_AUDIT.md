# Operator Web Navigation Audit

Branch: `audit/operator-web-nav-read-models`

Audit scope: `operator-web/src/App.jsx`, `operator-web/src/data.js`, `operator-web/src/screens/`, `operator-web/src/components/`, `operator-web/src/api/`, `operator-web/src/fixtures/`, `operator-web/src/hooks/`, `operator-web/src/lib/`.

## Routing Model

The current operator web shell does not use a URL router. Navigation is driven by `activeView` state in `operator-web/src/App.jsx`. Sidebar items are defined in `operator-web/src/data.js` as `navItems`; selecting an item changes `activeView`.

| Nav Id | Label | Component File | Reachable In Sidebar? | Backend Call? | Fixture/Data Source | Notes |
|---|---|---|---:|---:|---|---|
| `control` | Control Tower | `operator-web/src/App.jsx` inline `ControlTower` | yes | command submission only | `operator-web/src/data.js` | Static operational overview with command receipts captured through `operatorRuntime.js` when commands are triggered. |
| `ops` | Operations | `operator-web/src/screens/OperationsCommandCenter.jsx` | yes | command submission only | props from `App.jsx` state and `data.js` | Full screen exists. It is not wired to `/api/v1/operations` yet. |
| `guests` | Guests | `operator-web/src/App.jsx` inline `GuestWorkspace` | yes | command submission only | `operator-web/src/data.js` | Client/workspace style UI exists as guest workspace, not the newer artifact store read model. |
| `brief` | Interview Brief | `operator-web/src/App.jsx` inline `InterviewBrief` | yes | command submission only | `operator-web/src/data.js` | Uses static brief state and command receipts. No Narrative Story Doctor API client. |
| `pipeline` | Pipeline | `operator-web/src/App.jsx` inline `PipelineView` | yes | no | `operator-web/src/data.js` | Pipeline monitor is fixture-only. Backend orchestration routes exist but are not wired. |
| `composition` | Composition | `operator-web/src/App.jsx` inline `CompositionStudio` | yes | no | `operator-web/src/data.js` | Composition studio is fixture-only. Backend composition routes exist but are not wired. |
| `supervisual` | SuperVisual | `operator-web/src/screens/SuperVisualStudio.jsx` | yes | yes | backend only | Uses hooks and `operator-web/src/api/supervisualRuntime.js`. No fixture fallback found. |
| `timeline` | Timeline | `operator-web/src/screens/VideoTimelineWorkbench.jsx` | yes | yes, when fixture mode disabled | `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` | Backend client exists with default fixture fallback. |
| `review` | Review | `operator-web/src/App.jsx` inline `ReviewWorkbench` | yes | no | `operator-web/src/data.js` | Review backend routes exist but are not wired. |
| `agents` | Agents | `operator-web/src/App.jsx` inline `AgentFactory` | yes | no | `operator-web/src/data.js` | Backend agent factory routes exist but frontend uses fixture data. |
| `evals` | Evals | `operator-web/src/App.jsx` inline `EvalsView` | yes | no | `operator-web/src/data.js` | Backend evaluations routes exist but are not wired. |

## Requested Screen Coverage

| Requested Area | Current Finding | Route/Path | Component | Status |
|---|---|---|---|---|
| Client / Workspace | Guest workspace exists; artifact workspace UI does not. | `activeView=guests` | inline `GuestWorkspace` | partial |
| Reference Library / Reference Manager | No dedicated screen found. Some asset/reference concepts appear in data and SuperVisual inspector components. | none | none | missing |
| Pipeline View / Pipeline Run Monitor | Screen exists. | `activeView=pipeline` | inline `PipelineView` | fixture-only |
| Control Tower / Operations Command Center | Both exist. | `activeView=control`, `activeView=ops` | inline `ControlTower`, `OperationsCommandCenter.jsx` | partial |
| Composition Studio | Screen exists. | `activeView=composition` | inline `CompositionStudio` | fixture-only |
| SuperVisual Studio | Screen exists and calls backend runtime API. | `activeView=supervisual` | `SuperVisualStudio.jsx` | partial |
| Carousel Studio | No dedicated screen found. | none | none | missing |
| Video Timeline Workbench | Screen exists with backend client and fixture fallback. | `activeView=timeline` | `VideoTimelineWorkbench.jsx` | partial |
| Review Workbench | Screen exists. | `activeView=review` | inline `ReviewWorkbench` | fixture-only |
| Avatar Library / Avatar Builder | No dedicated screen found. Acting library backend exists. | none | none | backend-only |
| Template Atlas / Template Preview | No dedicated screen found. | none | none | missing |
| Capability / Provider / Render Readiness | No dedicated screen found. Provider/readiness backend contracts exist. | none | none | backend-only |
| Artifact / Workspace File Browser | No dedicated screen found. Workspace/artifact contracts and services exist. | none | none | backend-only |
| Golden Path / Demo Run View | No dedicated screen or frontend API found. Golden Path backend service exists. | none | none | backend-only |
| Evals / Receipts View | Evals screen exists but uses fixture data. | `activeView=evals` | inline `EvalsView` | fixture-only |

## Reachability Notes

- All `navItems` in `operator-web/src/data.js` are visible in the shell sidebar and render through `activeView`.
- No browser path mapping was found; deep linking is not currently represented in the frontend shell.
- SuperVisual and Timeline are the only audited UI areas with domain-specific frontend API clients.
- Operator command capture is shared across multiple shell screens through `operator-web/src/api/operatorRuntime.js`, with an offline UI ledger fallback.
