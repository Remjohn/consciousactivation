# M0093 Baseline / Limitations Receipt

## Baseline import blocker

Evidence class: `TEST`

Standard collection was attempted from the uploaded repository root with:

```text
python -m pytest -q tests/cae/test_m0080_storyboard_program_contracts.py tests/cae/test_m0079_storyboard_session_revision.py
```

Observed result during brownfield audit: test collection stopped with `ModuleNotFoundError: No module named 'psycopg'` from the package import chain.

A second isolated import probe showed an additional unavailable package dependency, `cmf_pipeline`, in unrelated `ca_runtime` package initialization. Application code was not changed to work around either dependency.

## Focused test bootstrap limitation

Evidence class: `OPERATOR_DECISION_REQUIRED`

The M0093 focused suite uses a test-only namespace bootstrap at `/mnt/data/m0093_test_bootstrap/sitecustomize.py` so the canonical M0079/M0080 modules can be imported without executing unrelated package initialization. This is test plumbing outside the repository change boundary; it is not production-runtime evidence.

The adapter code itself does not vendor, stub, or change CAE dependencies.

## External runtime fidelity

Evidence class: `OPERATOR_DECISION_REQUIRED`

The snapshot contains Node.js and npm but no native `slidev`, `pnpm`, or Open Carrusel installation. Native Slidev/reveal.js/Open Carrusel preview/export was not executed. All produced artifacts therefore carry `native_reachability_proven=False`.

A real preview inspection is still required for final perceptual acceptance, including evidence-lineage review and confirmation that format transformation does not create gratuitous attention or alter intended meaning.

## Git identity

Evidence class: `OPERATOR_DECISION_REQUIRED`

The uploaded repository snapshot contains no `.git` directory or history. `git rev-parse HEAD` fails with `fatal: not a git repository`. No synthetic Git commit was created. The operator must apply/commit the six repository changes in the tracked CAE worktree and record the real commit SHA.

## Tooling

Evidence class: `OPERATOR_DECISION_REQUIRED`

`ruff` is not installed in the supplied environment, so no ruff result is claimed.
