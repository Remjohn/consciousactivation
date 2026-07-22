# Lane B — Temporal Editing Runtime Activation

## Exclusive target paths

```text
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_video_editing_runtime/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_remotion_adapter/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_hyperframes_adapter/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_ffmpeg_adapter/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_render_qa/**
04_ATOMIC_HARNESS_PIPELINE/tests/temporal/**
```

## Reuse these exact predecessor paths

```text
THE_CMF_STUDIO(2).zip/
  src/ccp_studio/contracts/video_editing_engine.py
  src/ccp_studio/services/video_editing_engine_service.py
  src/ccp_studio/services/video_timeline_service.py
  src/ccp_studio/contracts/video_timeline_workbench.py
  src/ccp_studio/services/video_timeline_workbench_service.py
  src/ccp_studio/contracts/sonic_timeline.py
  src/ccp_studio/services/sonic_timeline_service.py
  src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py
  src/ccp_studio/services/remotion_render_adapter_service.py
  src/ccp_studio/services/ffmpeg_finish_adapter_service.py
  src/ccp_studio/services/remotion_ffmpeg_render_orchestrator_service.py
  docs/architecture/remotion-ffmpeg-render-adapter/**
  registries/canonical/remotion_ffmpeg_render_adapter/**
```

## Deliver

- Preserve existing edit-decision and timeline contracts.
- Adapter from accepted edit decisions to Remotion props and components.
- FFmpeg probe/trim/cut/concat/audio/subtitle/color/mux/encode execution.
- HyperFrames project/compiler adapter for its native motion families.
- Runtime preflight and explicit blocker behavior.
- Real file outputs and hashes.
- Post-render ffprobe, frame sampling, audio, caption, duration, and runtime-swap checks.
- Existing timeline workbench compatibility.

## Prohibited

- New timeline engine.
- New timeline UI.
- Silent runtime swaps.
- Replacing a motion-led promise with Ken Burns or concat fallback without an explicit new decision.
