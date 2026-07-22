# Format Engine Draft Wiring V1.2 Integration Summary

## Scope

This integration adds the draft-state seam after the Format Engine Adapters:

```text
SuperVisualBuilderFormatAdapterInput -> SuperVisualDraftState
CarouselEngineFormatAdapterInput -> CarouselDraftVariantState
```

The draft state is explicitly not final engine state. It preserves the compiler output so later Visual Preproduction, Asset Intelligence, Style Route, render, approval, and export systems can operate from typed state instead of loose payloads.

## Files Added

- `docs/architecture/format-engine-adapters/FORMAT_ENGINE_DRAFT_WIRING_V1_2.md`
- `docs/architecture/format-engine-adapters/SUPERVISUAL_CAROUSEL_DRAFT_WIRING_NEXT.md`
- `docs/architecture/format-engine-adapters/FORMAT_ENGINE_DRAFT_WIRING_V1_2_INTEGRATION_SUMMARY.md`
- `registries/canonical/format_engine_adapters/draft_wiring_targets.v1.json`
- `registries/canonical/skills/shared/format_engine_draft_wiring/`
- `src/ccp_studio/contracts/format_engine_draft_wiring.py`
- `src/ccp_studio/services/supervisual_format_draft_wiring_service.py`
- `src/ccp_studio/services/carousel_format_draft_wiring_service.py`
- `src/ccp_studio/services/format_engine_draft_wiring_service.py`
- `tests/cmf_studio/test_format_engine_draft_wiring_v1_2.py`
- `APPLY_FORMAT_ENGINE_DRAFT_WIRING_V1_2_PATCH.md`
- `FORMAT_ENGINE_DRAFT_WIRING_V1_2_BUNDLE_MANIFEST.json`
- `FORMAT_ENGINE_DRAFT_WIRING_V1_2_LOCAL_VERIFICATION.json`

## Files Modified

- `src/ccp_studio/services/carousel_engine_service.py`
- `tests/cmf_studio/test_format_engine_draft_wiring_v1_2.py`

## Tests Added

- SuperVisual adapter input builds `SuperVisualDraftState`.
- Carousel adapter input creates `CarouselDraftVariantState`.
- Generic draft wiring service routes both adapter input types.
- Missing SuperVisual source refs are rejected.
- Non-continuous Carousel sequence steps are rejected.
- Existing `CarouselEngineService` optional draft entrypoint delegates to `CarouselFormatDraftWiringService`.

## Final Test Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result at integration time:

```text
649 passed, 4 skipped
```

## Engine Service Availability

- `src/ccp_studio/services/supervisual_builder_service.py`: not present in this repository state.
- `src/ccp_studio/services/carousel_engine_service.py`: present.

Because `SuperVisualBuilderService` is not present, this branch does not create a fake replacement. The standalone `SuperVisualFormatDraftWiringService` is the canonical SuperVisual draft seam until the real builder service exists.

Because `CarouselEngineService` is present, this branch adds one optional method:

```python
create_variant_from_format_adapter_input(adapter_input)
```

The method delegates to `CarouselFormatDraftWiringService` and stops at `CarouselDraftVariantState`.

## Confirmed Boundaries

- Draft state is not final state.
- `brand_context_version_id` is preserved.
- `source_span_refs` are preserved.
- SuperVisual draft state requires `EngineTarget.SUPERVISUAL_ENGINE`.
- Carousel draft variant state requires `EngineTarget.CAROUSEL_ENGINE`.
- Carousel draft variant state requires `closure_contract_ref`.
- Carousel sequence step indexes must be continuous.
- Provider calls are not executed.
- Rendering is not executed.
- No UI/API endpoints are added.
- No final approval/export state is created.

## Known Limitations

- Draft state only.
- No provider calls.
- No rendering.
- No UI/API.
- No final approval/export.
- No deeper Visual Preproduction, Asset Intelligence, or Style Route execution in this branch.
- SuperVisual has only the standalone draft wiring seam because the exact builder service file is absent.

## Next Recommended Work

1. `SuperVisualDraftState` -> Visual Preproduction packet.
2. `SuperVisualDraftState` -> Asset Intelligence reference board.
3. `SuperVisualDraftState` -> Style Route policy execution.
4. `CarouselDraftVariantState` -> Carousel sequence strategy / slide role plan.
5. `CarouselDraftVariantState` -> Carousel visual system seed.
6. Define 2D Character Animation / Avatar Performance Layer before implementing the Format 02 video path.
7. Plan Video Editing Engine implementation only after the visual and carousel draft seams prove stable.
