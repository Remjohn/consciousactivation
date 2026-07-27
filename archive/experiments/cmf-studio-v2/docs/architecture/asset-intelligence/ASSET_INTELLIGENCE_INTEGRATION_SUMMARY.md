# Asset Intelligence V1 Integration Summary

## Files added

- `src/ccp_studio/contracts/asset_intelligence.py`
- `src/ccp_studio/repositories/asset_intelligence.py`
- `src/ccp_studio/services/asset_intelligence_service.py`
- `src/ccp_studio/services/asset_intelligence_adapters.py`
- `registries/canonical/asset_intelligence/`
- `registries/canonical/skills/shared/asset_intelligence/`
- `docs/architecture/asset-intelligence/`
- `tests/cmf_studio/test_asset_intelligence_v1.py`
- `APPLY_ASSET_INTELLIGENCE_V1_PATCH.md`
- `ASSET_INTELLIGENCE_V1_BUNDLE_MANIFEST.json`

## Existing systems preserved

Asset Intelligence V1 was integrated as a shared ingredient and asset layer above the existing systems. It does not replace or delete:

- `src/ccp_studio/contracts/creative_libraries.py`
- `src/ccp_studio/services/creative_library_service.py`
- `src/ccp_studio/contracts/visual_research.py`
- `src/ccp_studio/services/visual_research_service.py`
- `src/ccp_studio/contracts/asset_package.py`
- `src/ccp_studio/services/asset_package_service.py`
- `src/ccp_studio/contracts/acting_library.py`
- `src/ccp_studio/services/acting_library_service.py`

The V1 adapters are additive and convert micro-semiotic anchors, visual research candidates, and provider output receipts into Asset Intelligence records, ingredients, and variants without creating a disconnected second asset library.

## Tests added

- `tests/cmf_studio/test_asset_intelligence_v1.py`

The tests cover brand scoping, hash requirements, rights and direct-use gates, reference-only use, blocked asset retrieval exclusion, adapter behavior, brand context retrieval, candidate scoring, reference board gaps, usage receipts, fatigue, winner promotion thresholds, and SuperVisual reference-board retrieval.

## Test result

Final V1 verification command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Latest passing result before this summary:

```text
540 passed, 3 skipped
```

## Known limitations

- The repository is in-memory for V1 and is storage-ready but not yet backed by durable persistence.
- SuperVisual production still needs an explicit service integration pass before replacing internal or fixture reference-board logic.
- Carousel and Video integrations are intentionally not wired in this branch.
- Real provider execution is intentionally not wired here; generated provider outputs should later enter Asset Intelligence as variants after provider adapter gates pass.

## Next integration steps

The next SuperVisual integration should replace fake internal reference-board logic with:

- `AssetIntelligenceService.retrieve_candidates(...)`
- `AssetIntelligenceService.build_reference_board(...)`
- `AssetIntelligenceService.record_usage(...)`

If Visual Preproduction V1, Style Route V1, or Provider Adapter V1 are integrated after or alongside this branch, rerun their tests because they conceptually depend on Asset Intelligence as the shared ingredient layer.

Recommended sequence from this point:

1. Keep Visual Preproduction V1 and Style Route V1 green against this branch.
2. Integrate Provider Adapter V1 with fake provider default only.
3. Wire `SuperVisualBuilderService` or its equivalent SuperVisual/still-visual builder facade to Asset Intelligence first, then Visual Preproduction, then Style Route, then Provider Materialization.
