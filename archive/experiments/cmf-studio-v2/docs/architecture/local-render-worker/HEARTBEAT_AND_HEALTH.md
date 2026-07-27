# Heartbeat and Health

Heartbeats report:

```text
worker_id
status
active_job_ids
observed capability IDs
disk/free memory hints
```

Health receipts fail if:

```text
worker is offline
required capabilities are missing
heartbeat is stale
active jobs are reported by offline worker
```
