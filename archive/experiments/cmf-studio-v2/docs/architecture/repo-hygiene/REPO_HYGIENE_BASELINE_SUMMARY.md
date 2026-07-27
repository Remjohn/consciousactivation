# Repo Hygiene Baseline Summary

## Branch

`chore/repo-hygiene-baseline`

## Baseline Before Cleanup

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result: `718 passed, 4 skipped`

## Final Verification After Cleanup

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result: `718 passed, 4 skipped`

## Directories Deleted

- Root `.tmp/`
- Generated `__pycache__/` directories under the repository
- Generated `.pytest_cache/` directories under the repository
- Generated `.mypy_cache/` directories, where present
- Generated `.ruff_cache/` directories, where present

## Files Deleted

The cleanup removed only root-level integration artifacts that were already represented in canonical docs, source, registries, or tests:

- Integrated `CCP_*_INTEGRATION_BUNDLE.zip` / `*_INTEGRATION_BUNDLE.zip` archives for Asset Intelligence, Visual Preproduction, Style Route, SuperVisual runtime/UI/provider adapters, Carousel, Narrative Story Doctor, Format Intelligence, Narrative-to-Format bridge, Format Engine Draft Wiring, Composition Intelligence, Avatar Performance, and Video Editing Engine.
- Root `APPLY_*_PATCH.md` files for the same integrated bundles.
- Root `*_LOCAL_VERIFICATION.json` files for the same integrated bundles.
- Root `*_BUNDLE_MANIFEST.json` files for the same integrated bundles.
- Tracked Python bytecode artifacts inside `__pycache__/` directories.

The exact candidate list is recorded in `docs/architecture/repo-hygiene/REPO_HYGIENE_CANDIDATES.md`.

## Files Skipped As Uncertain

- `CCP_CONTRACT_CONVERGENCE_REGISTRY_CONSOLIDATION_PATCH.zip`
- `CCP_SKILL_ARCHITECTURE_SUPERVISUAL_BUILDER_V1_PATCH.zip`
- `CCP_STUDIO_MASTER_ONTOLOGY_GLOSSARY_V1_BUNDLE.zip`
- `CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/`
- `CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/`
- `CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/`
- `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/`
- `CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/`
- `scratch_append.py`
- `storage/`
- Existing dirty `operator-web/` build/cache changes
- Existing dirty `THE_CMF_STUDIO_CONVERGED_WORKING_COPY.zip`

## Protected Paths Not Touched

No product code, tests, registries, specs, PRDs, or operator UI source files were intentionally changed by this hygiene pass.

Generated cache directories were removed where found, including under protected source/test areas, because cache deletion was explicitly allowed by the hygiene prompt.

## Pre-Existing Dirty Files Not Related To Cleanup

The repo had unrelated dirty state before this pass. These items were not staged for the hygiene commit:

- `operator-web/.npm-cache/_logs/*`
- `operator-web/dist/*`
- `operator-web/dist/index.html`
- `THE_CMF_STUDIO_CONVERGED_WORKING_COPY.zip`
- `storage/`
- `scratch_append.py`

## Remaining Root-Level Artifacts Kept

Uncertain source/reference bundles and unzipped reference folders were intentionally kept because the cleanup prompt said to skip anything doubtful. They should be reviewed in a separate artifact-retention pass before deletion.

## Next Recommended Step

Integrate Format 02 Golden Path Orchestrator V1 on top of this stabilized baseline.
