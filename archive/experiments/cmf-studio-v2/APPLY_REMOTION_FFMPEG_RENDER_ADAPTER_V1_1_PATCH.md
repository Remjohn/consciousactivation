# CCP Real Remotion + FFmpeg Render Adapter V1.1 Integration Bundle

This bundle adds the gated real-local rendering adapter layer that comes after Local Render Worker V1.

## Purpose

Replace purely fake render receipts with a safe local rendering path for:

```text
Remotion Node.js + @remotion/skia composition render
FFmpeg finishing
ffprobe validation
frame sampling receipt
audio level analysis receipt
duration tolerance receipt
render QA report
```

## Critical spec anchor

Downstream visual composition should use:

```text
Remotion Node.js + @remotion/skia
```

The generation payload should preserve:

```text
Complete Editing Session state wrapper
research snapshot refs
asset state refs
scene spec refs
composition job refs
provider job receipt refs
evaluation receipt refs
```

The render payload must preserve:

```text
seven-layer composition model
allowed/banned motion vocabulary
memetic sound cue moderation law
source fidelity / render QA receipts
```

## Important

This bundle includes real-local execution service methods, but they are gated.

Tests use dry-run execution only and must not require Remotion or FFmpeg to be installed.

Real subprocess execution is allowed only when:

```text
execution_mode = real_local
runtime_capability_tested = true
local_worker_lease_id is present
allow_subprocess_execution = true
```

## Do not

```text
Do not call providers.
Do not call Remotion during tests.
Do not call FFmpeg during tests.
Do not call ffprobe during tests.
Do not shell out unless explicitly enabled.
Do not render real media by default.
Do not bypass Local Render Worker V1.
Do not bypass Capability Preflight.
Do not accept banned motion cues.
Do not allow memetic cue spacing violations.
Do not write outside workspace-safe relative output paths.
```

## Contracts

```text
RemotionRenderJob
RemotionRenderResult
FFmpegFinishJob
FFmpegFinishResult
FFprobeValidationReceipt
FrameSamplingReceipt
AudioLevelAnalysisReceipt
DurationToleranceReceipt
RenderQAReport
```

Additional support contracts:

```text
CompleteEditingSessionRenderStateWrapper
SevenLayerCompositionPayload
MotionVocabularyPolicyReceipt
MemeticSoundCueModerationReceipt
RenderRuntimeGateReceipt
RenderCommandPlan
```

## Services

```text
remotion_render_adapter_service.py
ffmpeg_finish_adapter_service.py
ffprobe_validation_service.py
frame_sampling_service.py
audio_level_analysis_service.py
duration_tolerance_service.py
render_qa_service.py
render_command_safety_service.py
remotion_ffmpeg_render_orchestrator_service.py
```

## V1.1 limitations

```text
real execution is gated and disabled in tests
no UI/API endpoints
no distributed worker process
no package installation
no Remotion project generation
no FFmpeg binary discovery
no actual frame extraction unless future runner enables it
```
