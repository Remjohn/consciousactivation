# Baseline Verification

Date: 2026-06-30 12:34:18 +02:00

Branch: `feat/ontology-contract-convergence`

Baseline policy: the current dirty worktree was explicitly accepted by Emilio as the baseline for ontology and contract convergence integration. No cleanup, reset, stash, or revert was performed before running verification.

## Commands

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
```

Result: passed.

```powershell
$env:PYTHONPATH="src"
python -m pytest -q tests/cmf_studio
```

Result: passed.

## Test Output Summary

```text
476 passed, 2 skipped in 9.64s
```

Pytest emitted a `pytest_asyncio` deprecation warning about unset `asyncio_default_fixture_loop_scope`. This was a warning only and did not fail baseline verification.

## Baseline Gate Decision

The accepted current worktree compiles and the CMF Studio test suite passes before ontology convergence changes. Proceed with ontology documentation integration, canonical contract kernel, convergence services, canonical registries, path freeze, and convergence tests.
