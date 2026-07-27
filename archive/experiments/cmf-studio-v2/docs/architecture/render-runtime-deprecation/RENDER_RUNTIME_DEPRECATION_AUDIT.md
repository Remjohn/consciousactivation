# Render Runtime Deprecation Audit

Branch: `audit/render-runtime-deprecation`

Prompt: `PROMPT_07_RENDER_RUNTIME_DEPRECATION_AUDIT`

## Purpose

Audit legacy render paths before cleanup. The current strategic runtime target is Remotion Node.js + `@remotion/skia`, gated through Local Render Worker, Capability Preflight, Remotion/FFmpeg adapter contracts, and Render QA receipts.

This audit does not delete legacy code. It marks deprecated paths and records the migration sequence required before removal.

## Baseline

- Baseline command: `PYTHONPATH=src python -m compileall -q src; PYTHONPATH=src python -m pytest -q tests/cmf_studio`
- Baseline result before audit edits: `970 passed, 14 skipped`
- Existing unrelated dirty files were left untouched.

## Search Scope

Searched:

- `src/`
- `tests/`
- `docs/`
- `registries/`
- `operator-web/`

Primary search terms:

- `skia`
- `sidecar`
- `render_queue`
- `RenderQueue`
- `HeadlessFrameRender`
- `AvatarExportWorkerJob`
- `skia_render_job`
- `cmf_skia_renderer`
- `subprocess`
- `Popen`
- `shell=True`
- `os.system`
- `@remotion/skia`
- `LocalRenderWorker`
- `RenderJobQueue`

## Findings

### Python/C++ Skia sidecar files

No executable sidecar directory was found at the old spec path `src/ccp/sidecars/skia-renderer/`.

No active Python source import was found for:

- `import skia`
- `from skia`
- `skia-python`
- `cppyy`
- `ctypes` / `cffi` sidecar bindings
- direct `Popen` / `shell=True` Skia execution

The old sidecar appears to survive as contracts, docs, registry requirements, and test-backed read models rather than an executable sidecar.

### Legacy Skia-era contracts and queues still present

The following are still used by tests and existing service methods:

- `HeadlessFrameRenderRequest`
- `HeadlessFrameRenderReceipt`
- `AvatarExportWorkerJob`
- `AvatarExportReceipt`
- `SkiaRenderBinding`
- `SkiaRenderReceipt`
- `SingleImageSkiaScene`
- `CarouselBuilderProgram.skia_render_job_refs`
- `SingleImageProviderJobPlan.final_authority = "cmf_skia_renderer"`

Primary owner files:

- `src/ccp_studio/contracts/asset_program_compilers.py`
- `src/ccp_studio/services/asset_program_compiler_service.py`
- `src/ccp_studio/repositories/asset_program_compilers.py`
- `src/ccp_studio/api/v1/asset_program_compilers.py`
- `src/ccp_studio/services/production_orchestration_service.py`
- `src/ccp_studio/services/still_visual_program_service.py`
- `src/ccp_studio/services/supervisual_project_service.py`
- `src/ccp_studio/contracts/provider_adapters.py`
- `src/ccp_studio/contracts/style_route_runtime.py`

### Current replacement path

The replacement path is present and should remain canonical for new render runtime work:

- `src/ccp_studio/contracts/local_render_worker.py`
- `src/ccp_studio/services/render_job_queue_service.py`
- `src/ccp_studio/services/local_render_worker_orchestrator_service.py`
- `src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py`
- `src/ccp_studio/services/remotion_render_adapter_service.py`
- `src/ccp_studio/services/ffmpeg_finish_adapter_service.py`
- `src/ccp_studio/services/render_command_safety_service.py`
- `src/ccp_studio/contracts/render_qa.py`
- `src/ccp_studio/services/render_qa_service.py`

This path preserves the gated execution laws:

- Real Remotion/FFmpeg execution is not default.
- Real local execution requires tested runtime capability, worker lease, and explicit subprocess allowance.
- Render QA receipts gate review/approval/export/publishing.

## Deprecation Markers Added

Non-behavioral markers were added to `src/ccp_studio/contracts/asset_program_compilers.py`:

- Module-level `LEGACY_SKIA_RUNTIME_DEPRECATION_NOTE`
- Class docstrings for legacy queue/Skia contracts
- Inline comments on `skia_render_job_refs`
- Inline comments on `cmf_skia_renderer` authority

No fields, validators, route behavior, or service behavior were changed.

## Still Used

The deprecated contracts are still covered by tests:

- `tests/cmf_studio/test_batch2_asset_program_compilers.py`
- `tests/cmf_studio/test_batch3_production_orchestration_and_still_visuals.py`

Therefore deletion is not safe yet.

## Not Deprecated

These are current systems, not legacy cleanup targets:

- Local Render Worker V1
- Remotion + FFmpeg Render Adapter V1.1
- Video Timeline Workbench local worker wiring
- Render QA V1

## Decision

Mark the legacy Skia-era contracts as deprecated, preserve tests, and defer deletion until replacement parity exists.
