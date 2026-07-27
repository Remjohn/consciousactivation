# CCP Local Render Worker V1 Integration Bundle

This bundle introduces the Local Render Worker V1.

## Purpose

Register a local machine as a render worker and manage deterministic render job lifecycle contracts.

V1 supports job registration, queueing, leasing, heartbeat, fake execution, result recording, and worker health receipts.

## Supported job types

```text
template_preview_render
avatar_state_preview_render
proxy_video_render
final_video_render
thumbnail_render
carousel_preview_render
supervisual_preview_render
```

## Important

V1 does not call Remotion or FFmpeg.

Real runtime execution should only be added later after explicit capability preflight, worker capability testing, and dedicated Remotion/FFmpeg adapter integration.

## Apply after

Recommended:

```text
Project Workspace + Artifact Store V1
Capability Preflight + Provider Menu V1
Video Editing Engine V1
Template Preview / Atlas V1
Avatar Asset Production + Rig Export V1
```

## Do not

```text
Do not call Remotion.
Do not call FFmpeg.
Do not shell out to subprocess runtimes.
Do not render real media.
Do not call providers.
Do not add UI/API endpoints.
Do not bypass capability testing.
Do not let a worker claim a capability as available unless enabled and tested.
Do not lease jobs to offline/unhealthy workers.
Do not mark final video render complete without final_timeline_locked=True in payload.
```

## What this bundle adds

```text
LocalRenderWorker
LocalRenderWorkerCapability
RenderJob
RenderJobQueue
RenderJobLease
RenderJobHeartbeat
RenderJobResult
RenderWorkerHealthReceipt
```

Services:

```text
local_render_worker_service.py
render_job_queue_service.py
render_job_lease_service.py
render_job_heartbeat_service.py
render_job_result_service.py
render_worker_health_service.py
```

## Hard laws

```text
Worker ID and machine ID are required.
Worker capabilities must be explicitly enabled and tested to be available.
Render jobs require supported job type.
Render jobs must not allow providers.
V1 render jobs must not allow external runtime calls.
Final video render jobs require final_timeline_locked=True.
A job cannot be leased to an offline/unhealthy worker.
A lease must belong to the worker that completes the job.
Heartbeat cannot report active jobs for an offline worker.
Render result cannot mark provider/runtime calls executed in V1.
Health receipt fails if required capabilities are missing, worker is offline, or stale heartbeat is detected.
```

## Milestones

### Milestone 1 — Docs, registries, contracts

```bash
git add docs/architecture/local-render-worker registries/canonical/local_render_worker src/ccp_studio/contracts/local_render_worker.py
git commit -m "feat(render-worker): add local worker contracts and registries"
```

### Milestone 2 — Repository, services, skills

```bash
git add src/ccp_studio/repositories/local_render_worker.py src/ccp_studio/services/*render_worker* src/ccp_studio/services/render_job_* registries/canonical/skills/shared/local_render_worker
git commit -m "feat(render-worker): add queue lease heartbeat and fake result services"
```

### Milestone 3 — Tests

```bash
PYTHONPATH=src python -m compileall -q src
PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_local_render_worker_v1.py
git add tests/cmf_studio/test_local_render_worker_v1.py
git commit -m "test(render-worker): verify local worker gates"
```

## V1 limitations

```text
fake execution only
no real Remotion adapter
no real FFmpeg adapter
no subprocess execution
no API endpoints
no UI
no persistent database
no distributed queue backend
```
