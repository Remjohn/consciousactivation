# Video Workbench Local Render UI Audit

Branch: `feat/video-workbench-local-render-worker`

## Existing VideoTimelineWorkbench component

- `operator-web/src/screens/VideoTimelineWorkbench.jsx`
- Existing route owner in `operator-web/src/App.jsx`
- The implementation uses the existing `TimelineWorkbenchProvider` and panel components. No duplicate screen is needed.

## API client file

- `operator-web/src/api/videoTimeline.js`
- Existing client functions before this prompt:
  - `fetchVideoTimelineWorkbench({ formatSlot })`
  - `proposeTimelineEdit({ draft })`
  - `submitTimelineEditCommand({ command })`
  - `requestProxyRerender({ programId })`
  - `requestOtioExport({ programId })`

## Fixture fallback file

- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- Fixture mode remains available.
- Backend failures still fall back to fixture data in the API client.

## Existing proxy render button/action

- `operator-web/src/components/timeline/TimelineInspector.jsx`
  - Existing `Rerender proxy` button calls `rerenderProxy`.
- `operator-web/src/components/timeline/TimelineCommandDrawer.jsx`
  - Existing command drawer also exposes proxy rerender through provider actions.

## Existing render state UI

- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
  - Before this prompt it showed proxy status and renderer references.
- `operator-web/src/components/timeline/TimelineInspector.jsx`
  - Before this prompt it exposed the rerender action but did not show the worker lease or QA state.

## Existing output preview UI

- `ProxyPreviewPanel.jsx` already had a proxy preview area.
- It now has an output preview URL field populated from backend local render worker/dry-run results.

## Existing QA/eval receipt UI

- The workbench already displayed evaluation summary data from the timeline read model.
- It did not have a dedicated proxy render QA section.
- This prompt adds a compact render QA section to the existing proxy panel and inspector.

## Existing endpoint names

- `GET /api/v1/video-edit-programs/current/timeline-workbench`
- `GET /api/v1/video-edit-programs/{program_id}/timeline-workbench`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/propose`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/submit`
- `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- `POST /api/v1/video-edit-programs/{program_id}/otio-exports`

## Gaps filled

- Proxy render action now sends a typed payload to the backend proxy render endpoint.
- Backend response fields are stored in workbench state:
  - `last_render_job_state`
  - `last_render_qa`
  - `output_preview_url`
  - updated proxy render summary
- The existing UI now shows:
  - render job status
  - worker ID
  - lease ID
  - output preview URL
  - render QA statuses and blockers

## Confirmation

No duplicate Video Timeline Workbench screen was created. This prompt extends the existing screen and existing fixture fallback path.
