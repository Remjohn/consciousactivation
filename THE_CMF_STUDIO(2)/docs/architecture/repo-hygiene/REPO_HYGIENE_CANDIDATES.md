# Repo Hygiene Candidates

## 1. Git Status Before Cleanup

Branch before cleanup work: `chore/repo-hygiene-baseline`

Pre-existing dirty state unrelated to this hygiene pass:

- Deleted tracked root archive: `THE_CMF_STUDIO_CONVERGED_WORKING_COPY.zip`
- Deleted tracked `operator-web/.npm-cache/_logs/*.log` files
- Deleted tracked `operator-web/dist/assets/index-C0oq3ruo.css`
- Deleted tracked `operator-web/dist/assets/index-CZf6317K.js`
- Modified tracked `operator-web/dist/index.html`
- Modified tracked `src/ccp_studio/contracts/__pycache__/visual_preproduction.cpython-312.pyc`
- Untracked `operator-web` build/cache files
- Untracked SuperVisual API/UI files that are outside this cleanup scope
- Untracked `storage/`
- Untracked root integration bundle artifacts and generated Python cache directories

## 2. Baseline Test Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result before cleanup:

```text
718 passed, 4 skipped
```

## 3. Candidate Directories To Delete

Safe deletion candidates:

- `.tmp/`
- All discovered `__pycache__/` directories
- All discovered `.pytest_cache/` directories
- All discovered `.mypy_cache/` directories, if any
- All discovered `.ruff_cache/` directories, if any

These are generated temporary/cache artifacts only. Product code, docs, registries, tests, and operator web source files are not deletion candidates.

## 4. Candidate Files To Delete

Safe root-level integrated bundle zip files:

- `CCP_ASSET_INTELLIGENCE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_AVATAR_PERFORMANCE_LAYER_V1_INTEGRATION_BUNDLE.zip`
- `CCP_CAROUSEL_ENGINE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_INTEGRATION_BUNDLE.zip`
- `CCP_FORMAT_ENGINE_DRAFT_WIRING_V1_2_INTEGRATION_BUNDLE.zip`
- `CCP_FORMAT_INTELLIGENCE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_NARRATIVE_TO_FORMAT_BRIDGE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_STYLE_ROUTE_CAC_GMG_PAPER_CUT_V1_INTEGRATION_BUNDLE.zip`
- `CCP_SUPERVISUAL_CAROUSEL_FORMAT_ADAPTERS_V1_1_INTEGRATION_BUNDLE.zip`
- `CCP_SUPERVISUAL_REAL_PROVIDER_ADAPTERS_V1_INTEGRATION_BUNDLE.zip`
- `CCP_SUPERVISUAL_RUNTIME_API_PERSISTENCE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_SUPERVISUAL_STUDIO_BACKEND_UI_INTEGRATION_V1_BUNDLE.zip`
- `CCP_VIDEO_EDITING_ENGINE_V1_INTEGRATION_BUNDLE.zip`
- `CCP_VISUAL_PREPRODUCTION_V1_INTEGRATION_BUNDLE.zip`

Safe root-level apply notes:

- `APPLY_ASSET_INTELLIGENCE_V1_PATCH.md`
- `APPLY_AVATAR_PERFORMANCE_LAYER_V1_PATCH.md`
- `APPLY_CAROUSEL_ENGINE_V1_PATCH.md`
- `APPLY_COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_PATCH.md`
- `APPLY_FORMAT_ENGINE_DRAFT_WIRING_V1_2_PATCH.md`
- `APPLY_FORMAT_INTELLIGENCE_V1_PATCH.md`
- `APPLY_NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_PATCH.md`
- `APPLY_NARRATIVE_TO_FORMAT_BRIDGE_V1_PATCH.md`
- `APPLY_STYLE_ROUTE_CAC_GMG_PAPER_CUT_V1_PATCH.md`
- `APPLY_SUPERVISUAL_CAROUSEL_FORMAT_ADAPTERS_V1_1_PATCH.md`
- `APPLY_SUPERVISUAL_REAL_PROVIDER_ADAPTERS_V1_PATCH.md`
- `APPLY_SUPERVISUAL_RUNTIME_API_PERSISTENCE_V1_PATCH.md`
- `APPLY_VIDEO_EDITING_ENGINE_V1_PATCH.md`
- `APPLY_VISUAL_PREPRODUCTION_V1_PATCH.md`

Safe root-level local verification files:

- `AVATAR_PERFORMANCE_LAYER_V1_LOCAL_VERIFICATION.json`
- `CAROUSEL_ENGINE_V1_LOCAL_VERIFICATION.json`
- `COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_LOCAL_VERIFICATION.json`
- `FORMAT_ENGINE_DRAFT_WIRING_V1_2_LOCAL_VERIFICATION.json`
- `FORMAT_INTELLIGENCE_V1_LOCAL_VERIFICATION.json`
- `NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_LOCAL_VERIFICATION.json`
- `NARRATIVE_TO_FORMAT_BRIDGE_V1_LOCAL_VERIFICATION.json`
- `SUPERVISUAL_CAROUSEL_FORMAT_ADAPTERS_V1_1_LOCAL_VERIFICATION.json`
- `VIDEO_EDITING_ENGINE_V1_LOCAL_VERIFICATION.json`

Safe root-level bundle manifest files:

- `ASSET_INTELLIGENCE_V1_BUNDLE_MANIFEST.json`
- `AVATAR_PERFORMANCE_LAYER_V1_BUNDLE_MANIFEST.json`
- `CAROUSEL_ENGINE_V1_BUNDLE_MANIFEST.json`
- `COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_BUNDLE_MANIFEST.json`
- `FORMAT_ENGINE_DRAFT_WIRING_V1_2_BUNDLE_MANIFEST.json`
- `FORMAT_INTELLIGENCE_V1_BUNDLE_MANIFEST.json`
- `NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_BUNDLE_MANIFEST.json`
- `NARRATIVE_TO_FORMAT_BRIDGE_V1_BUNDLE_MANIFEST.json`
- `STYLE_ROUTE_CAC_GMG_PAPER_CUT_V1_BUNDLE_MANIFEST.json`
- `SUPERVISUAL_CAROUSEL_FORMAT_ADAPTERS_V1_1_BUNDLE_MANIFEST.json`
- `SUPERVISUAL_REAL_PROVIDER_ADAPTERS_V1_BUNDLE_MANIFEST.json`
- `SUPERVISUAL_RUNTIME_API_PERSISTENCE_V1_BUNDLE_MANIFEST.json`
- `VIDEO_EDITING_ENGINE_V1_BUNDLE_MANIFEST.json`
- `VISUAL_PREPRODUCTION_V1_BUNDLE_MANIFEST.json`

## 5. Protected Files Explicitly Not Touched

- `src/` product source, except generated `__pycache__/` directories
- `tests/` test source, except generated `__pycache__/` directories
- `registries/`
- `docs/`
- `docs/architecture/`, except adding this hygiene report
- `docs/prd/`
- `docs/tech-specs/`
- `docs/stories/`
- `operator-web/`
- `apps/`
- `packages/`
- `scripts/`
- `pyproject.toml`
- `package.json`
- `pnpm-lock.yaml`
- README files
- root PRD/spec/reference markdown files

## 6. Uncertain Files Skipped

Skipped because they may be source/reference artifacts or were not in the explicit deletion allowlist:

- `CCP_CONTRACT_CONVERGENCE_REGISTRY_CONSOLIDATION_PATCH.zip`
- `CCP_SKILL_ARCHITECTURE_SUPERVISUAL_BUILDER_V1_PATCH.zip`
- `CCP_STUDIO_MASTER_ONTOLOGY_GLOSSARY_V1_BUNDLE.zip`
- Root unzipped reference/source bundle directories such as `CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/`
- Root unzipped reference/source bundle directories such as `CCP_CAROUSEL_COMPOSITION_ATLAS_V1_BUNDLE/`
- Root unzipped reference/source bundle directories such as `CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/`
- Root unzipped reference/source bundle directories such as `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/`
- Root `CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/`
- `storage/`
- `scratch_append.py`
- Existing dirty `operator-web/` artifacts
- Existing dirty `THE_CMF_STUDIO_CONVERGED_WORKING_COPY.zip` deletion

