# Atomic Harness Pipeline

Phase 1 product shell only. Harness intake, scheduling, replay, and selective rerun begin in Phase 3.

## Phase 1 commands

```bash
python -m cmf_pipeline status --json
python -m cmf_pipeline init-db --json
python -m cmf_pipeline bootstrap --json
python -m cmf_pipeline health --json
```

Authority remains candidate and explicit. Development is authorized for the bounded
Phase 1 foundation; production and certification remain false.
