# SuperVisual Runtime Persistence Plan

## V1 repository implementations

```text
InMemorySuperVisualRuntimeRepository
JsonFileSuperVisualRuntimeRepository
```

## JSON storage path

```text
storage/supervisual_runtime/
  projects/
  variants/
  snapshots/
  build_runs/
  step_runs/
  events/
  commands/
```

## Future DB tables

```text
supervisual_projects
supervisual_variants
supervisual_snapshots
supervisual_build_runs
supervisual_step_runs
supervisual_events
supervisual_commands
supervisual_artifact_links
supervisual_exports
supervisual_approvals
```

V1 stores references to large/binary artifacts instead of embedding them in project JSON.
