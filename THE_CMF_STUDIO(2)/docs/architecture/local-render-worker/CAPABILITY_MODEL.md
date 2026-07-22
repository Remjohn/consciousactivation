# Capability Model

A worker capability is available only when:

```text
enabled = true
tested = true
status = available
```

Examples:

```text
runtime:render:remotion
runtime:finish:ffmpeg
runtime:qa:ffprobe
render:template_preview
render:proxy_video
render:final_video
```

V1 stores capability declarations only. It does not test local binaries by shelling out.
