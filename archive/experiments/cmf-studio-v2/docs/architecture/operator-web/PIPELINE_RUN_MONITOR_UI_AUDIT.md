# Pipeline Run Monitor UI Audit

Branch: `feat/operator-pipeline-run-monitor-ui`

## Existing Pipeline View Files

- `operator-web/src/App.jsx`
  - Contains the existing `PipelineView` function.
  - Route/view id: `pipeline`.
  - Visible in sidebar through `operator-web/src/data.js` nav item `{ id: "pipeline", code: "PLN" }`.
  - Before this wiring, it rendered the static factory map from `pipelineStages`.

## Existing Operations Command Center Files

- `operator-web/src/screens/OperationsCommandCenter.jsx`
  - Existing Operations Command Center view.
  - Route/view id: `ops`.
  - Already receives `onView` from `App.jsx`, so it can link operators back to the Pipeline view without creating a new screen.

## Existing Control Tower Run/Status Files

- `operator-web/src/App.jsx`
  - Control Tower remains separate and was not modified for this prompt.
  - Existing status objects come from browser-session runtime state and `operator-web/src/data.js`.

## Existing API Clients

- `operator-web/src/api/operatorRuntime.js`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/api/clientWorkspaceReferences.js`
- Added: `operator-web/src/api/pipelineRunMonitor.js`

The new client follows the existing fallback pattern: backend first, fixture fallback on network failure or explicit fixture mode.

## Existing Fixture Files

- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- `operator-web/src/fixtures/clientWorkspaceReferences.fixture.js`
- Added: `operator-web/src/fixtures/pipelineRunMonitor.fixture.js`

No fixture files were removed.

## Existing Route Names

The app uses internal view ids rather than a full frontend router:

- `ops` for Operations Command Center
- `pipeline` for Pipeline View
- `timeline` for Video Timeline Workbench

No existing Template Atlas route was found in operator-web. Template preview links are returned as deterministic placeholder URLs.

## Existing Stage/Receipt/Artifact UI

- Pipeline stage cards existed in `PipelineView`.
- Command and render receipts existed in `OperationsCommandCenter`.
- There was no pipeline run detail UI for stage receipts, pipeline artifacts, blockers, or approvals.

## Existing Approval/Blocker UI

- Review and timeline surfaces showed review/command state.
- Pipeline View did not expose approval gates or blockers before this prompt.

## Existing Template Preview Links

- No dedicated Template Preview / Atlas operator-web route was found.
- The monitor read model returns deterministic `/template-preview/{id}` links and marks the data as synthetic/fixture when not backend-backed.

## Existing Video Timeline Workbench Links

- Video Timeline Workbench exists as internal view id `timeline`.
- The monitor returns deterministic video preview links as `/timeline?program_id={timeline_program_id}`.

## Missing UI Pieces Filled

- Pipeline run list.
- Pipeline run detail panel.
- Stage receipt table.
- Artifact pointer panel.
- Blocker panel.
- Pending approval panel.
- Golden Path detail panel inside the existing Pipeline View.
- Compact Pipeline Runs widget in the existing Operations Command Center.

## Duplicate-Risk Areas

- Pipeline View and Operations Command Center already existed.
- Recommended approach was followed: extend existing screens, do not create duplicate screens.

## Recommended Approach

Extend the existing Pipeline View and Operations Command Center with backend read models and fixture fallback. Add a dedicated frontend API client and same-shaped fixture, but do not create a new route tree or duplicate product surface.
