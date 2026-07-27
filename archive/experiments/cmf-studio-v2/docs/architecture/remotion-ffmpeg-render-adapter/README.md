# Real Remotion + FFmpeg Render Adapter V1.1

## Definition

This layer connects the Video Editing Engine and Local Render Worker to a gated real-local render path.

It creates:

```text
RemotionRenderJob
FFmpegFinishJob
Render QA receipts
```

and service methods for dry-run command planning and future real-local execution.

Tests remain dry-run only.
