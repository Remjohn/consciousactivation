# Tool Support Envelope

Every required capability should be represented as a `ToolSupportEnvelope`.

Capabilities include:

```text
provider:image:ideogram
provider:image:flux
runtime:render:remotion
runtime:finish:ffmpeg
runtime:worker:local_render_worker
tool:qa:ffprobe
tool:storage:artifact_store
```

A capability can be:

```text
available
configured
missing
degraded
blocked
```
