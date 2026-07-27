# Video Workbench Local Render Worker Integration Summary

## Branch

`feat/video-workbench-local-render-worker`

## Existing VideoTimelineWorkbench files inspected

- `operator-web/src/screens/VideoTimelineWorkbench.jsx`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx`
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
- `operator-web/src/components/timeline/TimelineInspector.jsx`
- `operator-web/src/components/timeline/TimelineCommandDrawer.jsx`
- `operator-web/src/styles/timeline.css`

## Backend routes inspected

- `src/ccp_studio/api/v1/video_timeline_workbench.py`
- Existing route reused:
  - `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- Route added:
  - `GET /api/v1/video-edit-programs/{program_id}/render-jobs/{render_job_id}`

## Files added

- `docs/architecture/video-editing-engine/VIDEO_WORKBENCH_LOCAL_RENDER_UI_AUDIT.md`
- `docs/architecture/video-editing-engine/VIDEO_WORKBENCH_LOCAL_RENDER_BACKEND_AUDIT.md`
- `docs/architecture/video-editing-engine/VIDEO_WORKBENCH_LOCAL_RENDER_WORKER_INTEGRATION_SUMMARY.md`
- `tests/cmf_studio/test_video_workbench_local_render_worker_v1.py`

## Files modified

- `src/ccp_studio/contracts/video_timeline_workbench.py`
- `src/ccp_studio/services/video_timeline_workbench_service.py`
- `src/ccp_studio/api/v1/video_timeline_workbench.py`
- `tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx`
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
- `operator-web/src/components/timeline/TimelineInspector.jsx`
- `operator-web/src/styles/timeline.css`

## Proxy render endpoint behavior

`POST /api/v1/video-edit-programs/{program_id}/proxy-renders` now returns the existing proxy render receipt data plus:

- `timeline_program_id`
- `render_job_state`
- `output_preview_url`
- `render_qa`
- `source_mode`

The endpoint remains additive and keeps the existing workbench route prefix.

## Render job lifecycle behavior

The workbench service now:

1. Resolves the current `VideoTimelineProgram`.
2. Registers a deterministic fake local worker.
3. Creates a `RenderJob` with `job_type=proxy_video_render`.
4. Enqueues the job.
5. Leases it to the worker.
6. Records heartbeat.
7. Completes a fake result.
8. Compiles a Remotion dry-run job when the V1.1 adapter is available.
9. Returns a render job state read model.

No final render path is triggered by the proxy render action.

## Output preview URL behavior

The output preview URL is sourced from the dry-run Remotion result when available, otherwise from the Local Render Worker fake result or Video Editing Engine fake proxy receipt. The contract only accepts V1-safe preview schemes:

- `dry-run://`
- `fake://`
- `proxy://`

## Render QA receipt behavior

The service compiles deterministic synthetic QA receipts for the dry-run/fake result:

- `FFprobeValidationReceipt`
- `FrameSamplingReceipt`
- `AudioLevelAnalysisReceipt`
- `DurationToleranceReceipt`
- `RenderQAReport`

The UI shows QA pass status, blockers, and ffprobe/frame/audio/duration statuses.

## Fixture fallback status

Fixture fallback is preserved. The frontend API client now attempts the backend by default, but still returns fixture data if:

- explicit fixture mode is enabled with `VITE_CMF_TIMELINE_FIXTURE_MODE=true`
- the backend request fails
- the backend returns a non-OK response

## Source modes supported

- `backend`
- `dry_run`
- `fake`
- `fixture`

## Tests run

- Baseline before changes:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `876 passed, 10 skipped`
- Targeted workbench/local render tests:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_video_workbench_local_render_worker_v1.py tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`
  - Result: `11 passed, 8 skipped`
- Related backend tests:
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_local_render_worker_v1.py tests/cmf_studio/test_remotion_ffmpeg_render_adapter_v1_1.py tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`
  - Result: `45 passed, 6 skipped`
- Full backend suite:
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `881 passed, 12 skipped`
- Frontend build check:
  - `npm --prefix operator-web run build -- --outDir ../.tmp/operator-web-build-check --emptyOutDir`
  - Result: Vite build passed. PowerShell emitted an npm wrapper access warning before Vite ran, but the command exited successfully.

## Confirmations

- No providers were called.
- No real Remotion was called.
- No real FFmpeg was called.
- No ffprobe subprocess was called.
- No subprocess runtime calls were added by default.
- The proxy render path uses Local Render Worker job lifecycle.
- Fixture fallback remains available.
- No duplicate Video Timeline Workbench screen was created.
- Final render gates were not weakened.

## Known limitations

- Proxy render remains fake/dry-run unless real runtime gates are explicitly enabled later.
- No real Remotion render by default.
- No real FFmpeg finish by default.
- No persistent render queue beyond current in-memory services.
- No artifact file materialization was added.
- Fixture fallback remains for offline/frontend demo mode.
- Render job polling is available through the backend route, but the current UI only needs the synchronous proxy render response.

## Next recommended step

Provider Runtime Ideogram/Flux V1, Operator Render Worker Dashboard, or a real render-gated execution prompt after the local environment is configured.
