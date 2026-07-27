# Queue and Leases

The worker lifecycle:

```text
RenderJob created
→ queued
→ leased to healthy worker
→ heartbeat updates worker status
→ fake result recorded
→ job completed
```

A lease must belong to the worker that completes the job.
