# Test Plan

Tests verify:

```text
worker registration requires IDs
capability availability requires enabled+tested
job type supported
provider/runtime calls blocked
final render requires final_timeline_locked
queue lease requires healthy worker
lease worker must complete result
heartbeat rejects offline active jobs
fake result emits hash
health fails missing capabilities/stale heartbeat/offline worker
```
