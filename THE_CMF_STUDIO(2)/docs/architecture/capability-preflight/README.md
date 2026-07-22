# Capability Preflight + Provider Menu V1

## Definition

Capability Preflight V1 is the operational gate that runs before real generation, rendering, or batch jobs.

It answers:

```text
Can this pipeline run?
Which providers are configured?
Which runtimes are available?
Which tools are missing?
What will it probably cost?
Is this blocked, degraded, or ready?
Is sample approval required before batch?
```

V1 is deterministic and config-driven. It does not call providers or runtimes.
