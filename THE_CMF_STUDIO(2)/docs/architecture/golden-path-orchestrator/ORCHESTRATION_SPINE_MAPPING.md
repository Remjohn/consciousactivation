# Orchestration Spine Mapping

This bundle is not a second harness.

When integrated into the real repo, map:

```text
GoldenPathRun
→ OrchestrationRun

GoldenPathStageResult
→ StageExecutionReceipt

Golden path stage gates
→ ValidationContract

GoldenPathReceipt
→ run summary receipt
```

The golden path is a pipeline recipe running on the existing orchestration spine.
