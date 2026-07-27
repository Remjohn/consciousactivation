# Video Workbench Local Render Backend Audit

Branch: `feat/video-workbench-local-render-worker`

## Existing route files

- `src/ccp_studio/api/v1/video_timeline_workbench.py`
- Route factory: `create_video_timeline_workbench_router`
- Mounted by the repo's existing API v1 router pattern.

## Existing proxy render endpoint

- Existing endpoint:
  - `POST /api/v1/video-edit-programs/{program_id}/proxy-renders`
- Before this prompt it returned a Video Editing Engine fake proxy render receipt.
- This prompt keeps the endpoint and extends the response additively with local render worker state and render QA.

## Existing timeline workbench service

- `src/ccp_studio/services/video_timeline_workbench_service.py`
- Existing service responsibilities:
  - build deterministic Format 02 demo timeline read models
  - propose and submit typed timeline edits
  - compile fake proxy render receipts
  - compile OTIO audit responses

## Existing Local Render Worker services

- `src/ccp_studio/contracts/local_render_worker.py`
- `src/ccp_studio/services/local_render_worker_service.py`
- `src/ccp_studio/services/render_job_queue_service.py`
- `src/ccp_studio/services/render_job_lease_service.py`
- `src/ccp_studio/services/render_job_heartbeat_service.py`
- `src/ccp_studio/services/render_job_result_service.py`
- `src/ccp_studio/services/render_worker_health_service.py`
- `src/ccp_studio/services/local_render_worker_orchestrator_service.py`

## Existing Remotion/FFmpeg adapter services

- `src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py`
- `src/ccp_studio/services/remotion_render_adapter_service.py`
- `src/ccp_studio/services/ffmpeg_finish_adapter_service.py`
- `src/ccp_studio/services/render_qa_service.py`
- The workbench uses only the dry-run Remotion adapter path. It does not invoke real Remotion, FFmpeg, ffprobe, or subprocess execution.

## Existing Render QA services

- `src/ccp_studio/services/ffprobe_validation_service.py`
- `src/ccp_studio/services/frame_sampling_service.py`
- `src/ccp_studio/services/audio_level_analysis_service.py`
- `src/ccp_studio/services/duration_tolerance_service.py`
- `src/ccp_studio/services/render_qa_service.py`

## Backend changes required

- Add workbench render read models to `video_timeline_workbench.py`.
- Extend `VideoTimelineWorkbenchService.create_proxy_render` to:
  - create a `proxy_video_render` Local Render Worker job
  - enqueue it
  - lease it to a healthy fake worker
  - record heartbeat
  - complete a fake result
  - compile a Remotion dry-run job when the adapter is available
  - compile synthetic Render QA receipts
  - return output preview URL, render job state, and QA read model
- Add a read endpoint for stored render job state:
  - `GET /api/v1/video-edit-programs/{program_id}/render-jobs/{render_job_id}`

## Missing read model fields before this prompt

- `last_render_job_state`
- `last_render_qa`
- `output_preview_url`
- `render_job_state` on proxy render response
- `render_qa` on proxy render response

## Safety notes

- Provider calls remain forbidden.
- External runtime calls remain false for dry-run/fake responses.
- Real local execution remains gated by the Remotion/FFmpeg adapter and Local Render Worker layers.
- The final render path is not touched.
