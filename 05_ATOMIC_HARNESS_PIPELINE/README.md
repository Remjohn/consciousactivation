# Atomic Harness Pipeline

The Phase 3 Atomic Harness Pipeline is a deterministic, development-only execution control plane. It consumes approved Builder and Activative Intelligence objects, binds exact implementations, compiles Workflow Nodes, persists execution state, and preserves replayable evidence without acquiring upstream semantic authority.

## Core commands

```bash
python -m cmf_pipeline bootstrap --json
python -m cmf_pipeline health --json
python -m cmf_pipeline status --json
python -m cmf_pipeline load-development-candidates --json
python -m cmf_pipeline demo --json
python -m cmf_pipeline export-schemas ./phase3-schemas --json
python -m cmf_pipeline inspect-run <run-id> --json
python -m cmf_pipeline replay-run <run-id> --json
```

## Execution laws

- Program Control is canonical for program status and authority.
- AIR semantic dependencies are referenced and validated, never recompiled.
- Bindings are exact and ambiguity fails closed.
- Workflow scheduling is deterministic.
- Commands are idempotent and events/checkpoints are append-only.
- Cancellation quarantines late results.
- Invalidation is descendant-only and historical bytes remain replayable.
- Synthetic adapters are never real artifacts or provider evidence.

## Validate

```bash
python ../../scripts/phase3/validate_phase3.py
```

Authority remains candidate. Production authorization and certification remain false.
