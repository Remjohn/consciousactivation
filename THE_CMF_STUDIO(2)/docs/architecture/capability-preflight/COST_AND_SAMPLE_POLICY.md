# Cost and Sample Policy

High-cost or batch flows require a sample-first approval gate.

Examples:

```text
avatar_64_state_library_generation
format02_provider_scene_batch
carousel_batch_generation
supervisual_batch_generation
```

If `sample_required=True` and `sample_approved=False`, the preflight should mark batch execution as blocked.
