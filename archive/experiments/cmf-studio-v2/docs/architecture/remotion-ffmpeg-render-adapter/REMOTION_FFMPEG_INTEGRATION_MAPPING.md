# Remotion + FFmpeg Integration Mapping

This branch adds the gated adapter layer for Remotion Node.js + `@remotion/skia`, FFmpeg finishing, ffprobe-style validation, deterministic frame/audio/duration checks, and render QA reporting.

V1.1 does not turn on real rendering by default. Tests and normal service usage remain dry-run unless a later worker-controlled path satisfies every real-local gate.

## 1. Video Editing Engine

Recommended call sites:

- `VideoTimelineProgram` and `RemotionInputProps` can compile into `RemotionRenderJob`.
- `FinalRenderContract` and `FFmpegFinishPlan` can compile into `FFmpegFinishJob`.
- `ProxyRenderContract` can continue producing fake receipts until the runtime gate passes.
- `FinalRenderContract` can continue producing fake receipts until the runtime gate passes.

Real execution should not be called directly from `VideoRenderContractService`. That service remains the compiler for video contracts and fake receipts. This adapter is the later runtime boundary.

## 2. Local Render Worker

Real local execution requires a local worker lease.

Required Remotion capability:

```text
runtime:render:remotion
```

Required FFmpeg capability:

```text
runtime:finish:ffmpeg
```

The adapter's dry-run path does not require a worker lease. The real-local path must require:

- `execution_mode=real_local`
- `runtime_capability_tested=True`
- `local_worker_lease_id`
- `allow_subprocess_execution=True`

Worker-controlled execution should own any future subprocess call. Arbitrary service calls should not bypass the worker.

## 3. Capability Preflight

Before real local render, `CapabilityPreflightService.run_preflight(...)` should be called with:

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.VIDEO_REAL_RENDER,
    remotion_configured=True,
    remotion_available=True,
    ffmpeg_configured=True,
    ffmpeg_available=True,
    local_worker_configured=True,
    local_worker_available=True,
)
```

If any required runtime is missing, degraded, or unavailable, real render remains blocked.

No secrets are required for local Remotion/FFmpeg render, and preflight must not infer or print secrets.

## 4. Project Workspace / Artifact Store

Future materialized outputs should use workspace-relative paths:

```text
client_workspaces/<client_slug>/runs/<run_id>/renders/
client_workspaces/<client_slug>/runs/<run_id>/exports/
client_workspaces/<client_slug>/runs/<run_id>/receipts/
```

Recommended future artifact refs:

- Remotion intermediate output -> `ArtifactCategory.RENDER`
- FFmpeg final output -> `ArtifactCategory.EXPORT`
- FFprobe/frame/audio/duration receipts -> `ArtifactCategory.RECEIPT`
- Render QA report -> `ArtifactCategory.RECEIPT`

This branch does not materialize artifacts by default.

## 5. Complete Editing Session

`CompleteEditingSessionRenderStateWrapper` preserves the source and production spine required by render:

- `complete_editing_session_ref`
- `brand_context_version_id`
- `research_snapshot_refs`
- `asset_manifest_refs`
- `scene_spec_refs`
- `composition_job_refs`
- `provider_job_receipt_refs`
- `evaluation_receipt_refs`

The render adapter must not collapse this into loose render props.

## 6. Avatar Asset Production

`AvatarRemotionLayerPayload` can later contribute to the avatar layer in `SevenLayerCompositionPayload`.

The adapter does not create avatar identity, face plates, body layers, action timelines, or rig exports. It only consumes approved layer payload references.

## 7. Template Preview / Atlas

Template Preview V1 already emits deterministic SVG preview read models and thumbnail URIs. That path remains valid.

A later template preview render can create a Remotion dry-run or real-local job only after:

- the template sample payload passes slot validation;
- `PipelineId.TEMPLATE_PREVIEW` preflight passes;
- a local worker lease exists for real execution.

## 8. Render QA

`RenderQAReport` aggregates:

- `FFprobeValidationReceipt`
- `FrameSamplingReceipt`
- `AudioLevelAnalysisReceipt`
- `DurationToleranceReceipt`

Any failed receipt contributes blockers to the report. A blocked report should prevent final approval, export, and publishing until repaired or explicitly waived by a future approval workflow.

## 9. Motion And Memetic Sound

`MotionVocabularyPolicyReceipt` blocks banned cues such as:

- `ai_liquid_morph`
- `object_warp`
- `unmotivated_shake`

`MemeticSoundCueModerationReceipt` enforces:

- Format 04: at least 10 seconds between cues
- Formats 01, 02, and 03: at least 30 seconds between cues

These policies must be checked before compiling a render job.

## 10. Non-goals In This Branch

- No UI/API endpoints.
- No package installation.
- No Remotion project generation.
- No FFmpeg binary discovery.
- No ffprobe subprocess validation.
- No real video file writing.
- No provider calls.
- No direct bypass around Local Render Worker or Capability Preflight.
