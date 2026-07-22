# Render Runtime Gate

Real local rendering requires:

```text
execution_mode = real_local
runtime_capability_tested = true
local_worker_lease_id present
allow_subprocess_execution = true
```

Without those conditions, service methods must not shell out.
