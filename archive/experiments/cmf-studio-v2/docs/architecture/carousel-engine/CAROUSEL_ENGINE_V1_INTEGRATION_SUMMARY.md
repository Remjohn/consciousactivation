# Carousel Engine V1 Integration Summary

## Files Added

- `src/ccp_studio/contracts/carousel_engine.py`
- `src/ccp_studio/repositories/carousel_engine.py`
- `src/ccp_studio/services/carousel_engine_service.py`
- `src/ccp_studio/services/carousel_render_service.py`
- `src/ccp_studio/services/carousel_eval_service.py`
- `tests/cmf_studio/test_carousel_engine_v1.py`
- `registries/canonical/carousel/`
- `registries/canonical/skills/engines/carousel/`
- `docs/architecture/carousel-engine/`
- `APPLY_CAROUSEL_ENGINE_V1_PATCH.md`
- `CAROUSEL_ENGINE_V1_BUNDLE_MANIFEST.json`
- `CAROUSEL_ENGINE_V1_LOCAL_VERIFICATION.json`

## Files Modified

- `src/ccp_studio/contracts/carousel_engine.py`
  - Added `CarouselVariantComparisonReport` to complete the requested V1 object model.
- `src/ccp_studio/repositories/carousel_engine.py`
  - Added a dedicated `variant_comparison_reports` in-memory store.
- `src/ccp_studio/services/carousel_engine_service.py`
  - Added `validate_narrative_arc(...)`, `audit_sequence_composition(...)`, and `compare_variants(...)`.
- `tests/cmf_studio/test_carousel_engine_v1.py`
  - Added coverage for narrative validation, composition audit, and variant comparison.

## Tests Added

- `tests/cmf_studio/test_carousel_engine_v1.py`

The test suite verifies the V1 hard gates:

- `brand_context_version_id` is required.
- Factual claims require source refs or approved strategy refs.
- Slide indexes must be continuous from 1.
- Repeated slide roles require `repeat_reason`.
- Copy budgets are enforced.
- Blocked assets cannot be allocated.
- Unknown-rights assets cannot be direct-use.
- Visual system lock is required before slide composition.
- Route averaging is rejected.
- Composition lock is required before provider blueprint compilation.
- Provider blueprints require source refs, style route, frame profile, and composition role.
- Render batch contracts require asset hashes.
- 16:9 delivery frame profiles are rejected.
- Unsupported claims and mobile readability failures block approval.
- Revision feedback compiles into typed commands.
- Export pack compilation requires approved status.
- Fake end-to-end Carousel build path works.

## Test Result

Final verification command:

```powershell
$env:PYTHONPATH="src"; python -m compileall -q src; python -m pytest -q tests/cmf_studio
```

Result:

```text
584 passed, 4 skipped
```

## Known Limitations

- V1 repository is in-memory only.
- V1 render service is fake and deterministic.
- No Carousel Runtime API was added in this branch.
- No Carousel Builder UI was added in this branch.
- No real provider execution was added in this branch.
- Asset Intelligence integration is scaffolded through contracts and requirements, but not deeply wired into retrieval yet.
- Visual Preproduction integration is scaffolded through skill manifests, but not deeply wired into packet generation yet.
- Style Route integration is scaffolded through policy contracts, but not deeply wired into `StyleRouteEngineService` yet.
- Provider Adapter integration is represented by provider blueprint contracts, but materialization remains fake/no-provider in this branch.
- Publishing handoff is not wired yet.

## Shared Systems Not Yet Deeply Wired

- `AssetIntelligenceService`
- `VisualPreproductionService`
- `StyleRouteEngineService`
- `SuperVisualProviderMaterializationService`
- Eval/review persistence
- Publishing/runtime handoff

## Next Recommended Integration Steps

1. Wire `CarouselEngineService` to `VisualPreproductionService`.
2. Wire `CarouselEngineService` to `AssetIntelligenceService`.
3. Wire `CarouselEngineService` to `StyleRouteEngineService`.
4. Add Carousel Runtime API + Persistence.
5. Build Carousel Builder UI.
6. Add real provider materialization only after the fake path remains stable.
