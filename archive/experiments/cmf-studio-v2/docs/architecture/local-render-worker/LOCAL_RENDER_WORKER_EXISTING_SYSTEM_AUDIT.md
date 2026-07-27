# Local Render Worker Existing System Audit

Branch: `feat/local-render-worker-v1`

Baseline before bundle integration:

- `PYTHONPATH=src python -m compileall -q src`: passed
- `PYTHONPATH=src python -m pytest -q tests/cmf_studio`: passed, `828 passed, 10 skipped`

## 1. Existing Render Worker Files Found

No existing `LocalRenderWorker` contract or service was found.

Related worker systems already present:

- `src/ccp_studio/contracts/comfy_gpu_worker.py`
- `src/ccp_studio/services/comfy_gpu_worker_service.py`
- `tests/cmf_studio/test_self_hosted_comfyui_docker_gpu_worker.py`

The Comfy GPU worker is a provider/cloud GPU worker path tied to ComfyUI workflow assets and provider operations. The Local Render Worker V1 bundle should not replace it.

## 2. Existing Render Job / Queue Files Found

Existing queue/job concepts appear in:

- `src/ccp_studio/contracts/comfy_gpu_worker.py`
- `src/ccp_studio/services/comfy_gpu_worker_service.py`
- `src/ccp_studio/workflows/provider_job_workflow.py`
- operations board services/tests that display queues and workers
- provider job retry/resume/cancel tests

No existing local render queue, lease, heartbeat, or health model was found with the exact V1 target names.

## 3. Existing Remotion / FFmpeg References Found

Remotion and FFmpeg are already represented in contracts, docs, registries, and tests:

- Video Editing Engine contracts include `RemotionInputProps`, `ProxyRenderContract`, `FinalRenderContract`, fake proxy/final receipts, and `FFmpegFinishPlan`.
- Capability Preflight includes runtime requirements for `runtime:render:remotion`, `runtime:finish:ffmpeg`, and `runtime:worker:local_render_worker`.
- Deterministic renderer contracts mention Remotion and Motion Canvas as deterministic renderer routes.
- Operator-web fixtures and copy mention Remotion/FFmpeg as planned render engines.

This branch must not introduce real Remotion, FFmpeg, ffprobe, subprocess, or shell execution.

## 4. Existing Video Editing Engine Render Contract Files Found

Relevant files:

- `src/ccp_studio/contracts/video_editing_engine.py`
- `src/ccp_studio/services/video_render_contract_service.py`
- `src/ccp_studio/services/video_editing_engine_service.py`
- `registries/canonical/skills/engines/video/30_video.proxy_render_contract.compile.skill.yaml`
- `registries/canonical/skills/engines/video/31_video.proxy_render.execute_fake.skill.yaml`
- `registries/canonical/skills/engines/video/35_video.final_render_contract.compile.skill.yaml`
- `registries/canonical/skills/engines/video/37_video.final_render.execute_fake.skill.yaml`

The existing Video Editing Engine owns timeline render contracts and fake render receipts. Local Render Worker V1 should provide worker registration, queue, lease, heartbeat, result, and health receipts around future execution, not replace Video Editing Engine contracts.

## 5. Existing Operator-Web Render UI Files Found

Render-adjacent UI references exist in:

- `operator-web/src/App.jsx`
- `operator-web/src/data.js`
- `operator-web/src/api/videoTimeline.js`
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
- `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx`
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`

No dedicated render worker dashboard was found. This integration must not add UI/API routes.

## 6. Existing Queue / Lease / Heartbeat Systems Found

Queue concepts exist for provider jobs, operations board state, and Comfy GPU workers. Exact local render worker lease and heartbeat contracts were not found.

Related files:

- `src/ccp_studio/services/comfy_gpu_worker_service.py`
- `tests/cmf_studio/test_operations_board.py`
- `tests/cmf_studio/test_provider_job_retry_resume_cancel_and_compensation.py`
- `tests/cmf_studio/test_workflow_recovery_actions.py`

The Local Render Worker bundle can be applied additively as its own fake local queue/lease/heartbeat layer.

## 7. Existing Subprocess / Shell Render Paths Found

Searches found historical docs/tests using words like shell/subprocess, but no local render worker code path that shells out to Remotion or FFmpeg. Deterministic render and video render services currently compile/read models and fake receipts in Python.

This integration must keep that boundary: no subprocess calls, no runtime probing, no local command execution.

## 8. Naming Conflicts

Potential overlap:

- `RenderReceipt` exists in deterministic rendering contracts.
- `ProxyRenderReceipt` and `FinalRenderReceipt` exist in Video Editing Engine contracts.
- `GpuWorkerJob` and `GpuWorkerReceipt` exist in Comfy GPU worker contracts.
- Capability Preflight already references `runtime:worker:local_render_worker`.

Resolution:

- Add `local_render_worker.py` as a new local worker lifecycle contract surface.
- Do not modify existing Video Editing Engine, deterministic rendering, or Comfy GPU worker contracts.
- Preserve Capability Preflight as the future gate for real local render worker availability.

## 9. Additive Application Decision

The bundle can be applied additively. It should introduce:

- `src/ccp_studio/contracts/local_render_worker.py`
- `src/ccp_studio/repositories/local_render_worker.py`
- local render worker services under `src/ccp_studio/services/`
- `registries/canonical/local_render_worker/`
- `registries/canonical/skills/shared/local_render_worker/`
- V1 tests under `tests/cmf_studio/`

No existing render, video, capability, workspace, or operator-web file needs to be overwritten for V1.

## 10. Files That Require Merge Instead of Copy

No target file was found that requires merge before bundle application. If the unzipped bundle contains package `__init__.py` files or broad exports, those should not be copied unless tests prove an additive export is required.
