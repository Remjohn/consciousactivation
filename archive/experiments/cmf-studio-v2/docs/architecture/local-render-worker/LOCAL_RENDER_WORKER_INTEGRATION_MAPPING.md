# Local Render Worker Integration Mapping

Local Render Worker V1 is a fake deterministic worker lifecycle layer. It registers local workers, declares tested capabilities, creates jobs, queues them, leases them, records heartbeats, emits fake results, and evaluates health.

It does not execute Remotion, FFmpeg, providers, subprocesses, or shell commands.

## 1. Video Editing Engine

Recommended future call sites:

```text
ProxyRenderContract
-> RenderJob(job_type=proxy_video_render)
-> LocalRenderWorker queue / lease / fake result
```

```text
FinalRenderContract
-> RenderJob(job_type=final_video_render, payload.final_timeline_locked=True)
-> LocalRenderWorker queue / lease / fake result
```

Rules:

- Final video render jobs must include `payload.final_timeline_locked=True`.
- V1 worker results remain fake and deterministic.
- Existing `VideoRenderContractService.execute_proxy_render_fake(...)` and `execute_final_render_fake(...)` stay as Video Editing Engine fake receipt paths.
- Local Render Worker adds the worker lifecycle seam around future execution, not a replacement for video contracts.

## 2. Template Preview / Atlas

Recommended future call site:

```text
TemplatePreviewResult
-> RenderJob(job_type=template_preview_render)
```

Current Template Preview V1 already emits deterministic SVG/read-model previews and does not require worker execution. Real preview rendering should go through Local Render Worker after Remotion/local runtime adapters are integrated and preflighted.

## 3. Avatar Asset Production

Recommended future call site:

```text
AvatarRemotionLayerPayload
-> RenderJob(job_type=avatar_state_preview_render)
```

V1 must not call Remotion. The worker can fake-preview avatar state payloads only.

## 4. Project Workspace / Artifact Store

Recommended future storage:

```text
client_workspaces/<client_slug>/runs/<run_id>/renders/
client_workspaces/<client_slug>/runs/<run_id>/receipts/
```

Mapping:

- `RenderJobResult.output_uri` can later be registered as an `ArtifactRef`.
- Worker logs/results can later be stored under run `renders/` and `receipts/`.
- V1 tests register fake worker result read models as workspace render artifacts.

## 5. Capability Preflight

Recommended future connection:

```text
CapabilityPreflightService.run_preflight(
  pipeline_id=PipelineId.VIDEO_REAL_RENDER,
  remotion_configured=...,
  remotion_available=...,
  ffmpeg_configured=...,
  ffmpeg_available=...,
  local_worker_configured=...,
  local_worker_available=...
)
```

Rules:

- LocalRenderWorker health/capabilities should later feed `PipelineId.VIDEO_REAL_RENDER`.
- Remotion and FFmpeg real availability must be preflighted before any real runtime execution.
- V1 local fake worker capability does not satisfy real Remotion/FFmpeg execution by itself.

## 6. Operator Web

Future Render Worker dashboard can show:

- workers
- capabilities
- queue
- leases
- heartbeats
- fake/real result status
- health receipts

This integration does not add UI or API routes.

## 7. Remotion / FFmpeg V1.1

Real execution belongs in a future adapter bundle:

```text
CCP_REMOTION_FFMPEG_RENDER_ADAPTER_V1_1_INTEGRATION_BUNDLE
```

That adapter should consume Local Render Worker jobs only after:

- Capability Preflight passes.
- Worker capabilities are explicitly enabled and tested.
- Required runtime versions and paths are validated.
- Operator approval is recorded for real execution where needed.

Local Render Worker V1 remains fake-only.
