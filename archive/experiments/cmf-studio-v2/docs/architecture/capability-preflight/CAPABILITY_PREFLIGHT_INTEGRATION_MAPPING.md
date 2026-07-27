# Capability Preflight Integration Mapping

## Purpose

Capability Preflight runs before real provider execution, local render work, Remotion, FFmpeg, and avatar-library production jobs. It is a visibility and gating layer, not a provider adapter, render worker, or orchestration harness.

## Existing Upstream Systems

- Golden Path Orchestrator:
  - `src/ccp_studio/contracts/golden_path_orchestrator.py`
  - `src/ccp_studio/services/format02_golden_path_orchestrator_service.py`
- Video Editing Engine:
  - `src/ccp_studio/contracts/video_editing_engine.py`
  - `src/ccp_studio/services/video_editing_engine_service.py`
  - `src/ccp_studio/services/video_render_contract_service.py`
- Provider adapters and orchestration:
  - `src/ccp_studio/contracts/provider_adapters.py`
  - `src/ccp_studio/providers/`
  - `src/ccp_studio/services/provider_orchestration_service.py`
  - `src/ccp_studio/services/supervisual_provider_materialization_service.py`
- Style Route provider blueprint compiler:
  - `src/ccp_studio/contracts/style_route_runtime.py`
  - `src/ccp_studio/services/style_route_engine_service.py`

## Recommended Call Sites

### Before Format 02 Provider Scene Batch

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.FORMAT02_PROVIDER_SCENE_BATCH,
    ideogram_configured=...,
    ideogram_available=...,
    flux_configured=...,
    flux_available=...,
    sample_approved=...,
    batch_requested=True,
)
```

This must run before Ideogram composition plates or Flux reference edits. Missing Ideogram/Flux, missing artifact storage, or missing sample approval blocks the batch.

### Before Avatar 64-State Generation

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION,
    ideogram_configured=...,
    ideogram_available=...,
    flux_configured=...,
    flux_available=...,
    sample_approved=...,
    batch_requested=True,
)
```

This must run before any real avatar face/body plate generation. It must never create avatar assets itself.

### Before Real Video Render

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.VIDEO_REAL_RENDER,
    remotion_configured=...,
    remotion_available=...,
    ffmpeg_configured=...,
    ffmpeg_available=...,
    local_worker_configured=...,
    local_worker_available=...,
)
```

This must run before any real Remotion, FFmpeg, or local worker execution. V1 only checks caller-supplied configuration and availability state.

### Before Template Preview

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.TEMPLATE_PREVIEW,
    remotion_configured=...,
    remotion_available=...,
)
```

This gates preview capability visibility without invoking Remotion.

### Before Fake Format 02 Golden Path

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.FORMAT02_GOLDEN_PATH,
)
```

The fake golden path requires Python and artifact storage. Missing optional real render tools may degrade the report but should not block the fake export path.

## Integration Rule

Preflight reports can be attached to orchestration metadata, Golden Path receipts, Video Editing Engine run metadata, or provider batch command context later. V1 does not wire enforcement into those runtimes because no shared preflight hook exists yet.

## Deferred Runtime Wiring

- Add a common pre-execution hook for real provider/materialization requests.
- Add a common pre-render hook before real Remotion/FFmpeg execution.
- Store `CapabilityPreflightReport` refs on future provider batch and render commands.
- Surface provider menu and setup offers in operator UI after backend persistence/API is defined.

## Non-Goals In This Branch

- No provider calls.
- No runtime calls.
- No Remotion or FFmpeg shelling.
- No API/UI endpoints.
- No secret probing or inferred credential state.
