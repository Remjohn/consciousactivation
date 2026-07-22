# Local Render Worker V1

## Definition

Local Render Worker V1 registers a local machine as a render worker and manages render job queue lifecycle.

It supports:

```text
worker registration
capability declaration
job creation
job queue
job lease
heartbeat
fake execution
result recording
health receipts
```

V1 does not call Remotion, FFmpeg, or providers.
