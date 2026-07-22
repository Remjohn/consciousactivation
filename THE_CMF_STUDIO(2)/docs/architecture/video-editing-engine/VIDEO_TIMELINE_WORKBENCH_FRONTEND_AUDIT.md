# Video Timeline Workbench Frontend Audit

## Frontend Files Found

- `operator-web/src/screens/VideoTimelineWorkbench.jsx`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx`
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
- `operator-web/src/components/timeline/TranscriptBeatPanel.jsx`
- `operator-web/src/components/timeline/TimelineRuler.jsx`
- `operator-web/src/components/timeline/TrackLaneStack.jsx`
- `operator-web/src/components/timeline/TimelineTrackLane.jsx`
- `operator-web/src/components/timeline/TimelineSegment.jsx`
- `operator-web/src/components/timeline/TimelineInspector.jsx`
- `operator-web/src/components/timeline/TimelineCommandDrawer.jsx`
- `operator-web/src/state/timelineDraftReducer.js`
- `operator-web/src/styles/timeline.css`

## Existing Fixtures

- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- Fixture mode is controlled by `VITE_CMF_TIMELINE_FIXTURE_MODE`.
- Existing default behavior is fixture-first unless `VITE_CMF_TIMELINE_FIXTURE_MODE=false`.

## API Client Files

- `operator-web/src/api/videoTimeline.js`

## Frontend-Expected Endpoints

- `GET /api/v1/video-edit-programs/current/timeline-workbench?format={formatSlot}`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/propose`
- `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/submit`
- `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- `POST /api/v1/video-edit-programs/{program_id}/otio-exports`

## Request Payload Shapes

- Timeline edit proposal uses `cmf.timeline_edit_draft.v1` fields:
  `draft_id`, `program_id`, `target_segment_id`, `edit_type`, `proposed_time_range`, `payload`, `expected_object_version`, and `blocker_codes`.
- Timeline edit submit uses `cmf.timeline_edit_command.v1` fields:
  `command_id`, `draft_id`, `program_id`, `brand_workspace_id`, `guest_id`, `target_segment_id`, `edit_type`, `expected_object_version`, `expected_renderer_props_hash`, `expected_scope_ref`, `payload`, and `submitted_by_operator_id`.
- Proxy render and OTIO export currently submit empty POST bodies from the UI.

## Response / Read Model Shape

The UI expects `cmf.video_timeline_workbench_state.v1` compatible data with:

- scope fields: `program_id`, `brand_workspace_id`, `guest_id`, `guest_name`, `asset_code`
- timing fields: `fps`, `duration_frames`, `duration_ms`, `object_version`
- render fields: `proxy_render_ref`, `renderer_props_manifest_ref`, `renderer_props_hash`, `playback_proxy_status`
- source fields: `beat_map_ref`, `otio_manifest_ref`
- workbench fields: `format_slot`, `format_meta`, `lanes`, `markers`, `selected_segment_id`, `hard_blocker_codes`, `next_valid_commands`
- lane segments with `segment_id`, `lane_id`, `segment_type`, `label`, `time_range`, `source_refs`, `primitive_refs`, `receipt_refs`, `blocker_codes`, `locked`, and `note`

## Fixture Fallback

Fixture fallback existed as explicit fixture mode. This integration preserves that and adds a backend-failure fallback when fixture mode is disabled, returning the existing fixture with `source_mode="fixture"`.

## Mismatches / Uncertainties

- The frontend default `formatSlot` is `SV-RRC`, while the new backend can also synthesize demo read models for `SV-CSC`, `SV-EDU`, and `SV-FRB`.
- The frontend has no test or lint script in `operator-web/package.json`; only `dev`, `build`, and `preview` are available.
- The UI still applies accepted edit receipts locally after submit. The backend now returns typed revision receipts, but canonical refresh-on-receipt should be tightened in a later live runtime pass.
