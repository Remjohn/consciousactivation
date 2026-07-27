# Audio and Render

V1 compiles:

```text
VoicePresencePlan
PausePreservationPlan
SoundCueTimeline
MemeticCueLedger
AudioMixPlan
LoudnessFinishPlan
RemotionInputProps
OTIOAuditTimeline
ProxyRenderContract
FinalRenderContract
FFmpegFinishPlan
```

V1 does not call Remotion or FFmpeg. It emits fake render receipts with deterministic hashes.
