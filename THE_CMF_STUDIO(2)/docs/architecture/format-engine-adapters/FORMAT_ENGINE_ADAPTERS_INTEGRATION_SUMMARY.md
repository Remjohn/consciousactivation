# Format Engine Adapters Integration Summary

## Scope

This integration connects the new compiler chain without rewriting the component engines:

```text
Narrative Story Doctor / Content Extraction Intelligence
-> Format Intelligence
-> SuperVisual / Carousel adapter inputs
```

The Narrative-to-Format bridge compiles authorized format programs from typed narrative extraction packets. The SuperVisual and Carousel adapters then convert authorized format programs into engine-ready input contracts. No UI, API endpoint, provider call, render call, or direct component-engine execution is introduced in this branch.

## Files Added

- `docs/architecture/narrative-format-bridge/`
- `docs/architecture/format-engine-adapters/`
- `registries/canonical/narrative_format_bridge/`
- `registries/canonical/format_engine_adapters/`
- `registries/canonical/skills/shared/narrative_format_bridge/`
- `registries/canonical/skills/shared/format_engine_adapters/`
- `src/ccp_studio/contracts/narrative_format_bridge.py`
- `src/ccp_studio/contracts/supervisual_carousel_format_adapters.py`
- `src/ccp_studio/services/narrative_to_format_bridge_service.py`
- `src/ccp_studio/services/supervisual_format_program_adapter_service.py`
- `src/ccp_studio/services/carousel_format_program_adapter_service.py`
- `tests/cmf_studio/test_narrative_to_format_bridge_v1.py`
- `tests/cmf_studio/test_supervisual_carousel_format_adapters_v1_1.py`

## Tests Added

- Narrative packet to Format Intelligence bridge coverage for Format 01, Format 02, Format 03, Format 04, SuperVisual, Carousel, Meme, Poll, and Reaction Seed packets.
- Bridge failure coverage when source references are missing.
- SuperVisual adapter authorization coverage.
- Carousel adapter authorization coverage.

## Final Test Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result at integration time:

```text
643 passed, 4 skipped
```

## Existing-File Adjustments

The real repository already uses `CarouselSlideSeed.slide_copy` instead of the bundle's older `copy` field. The bridge test was updated to use the canonical `slide_copy` field. The production contract was not loosened.

The requested `SuperVisualBuilderService` exact path was not present in the current repository state. The current SuperVisual foundation exists through runtime, project, and provider-materialization services. This branch does not call those services; it only creates adapter input contracts for a later wiring step.

## Confirmed Boundaries

- Bridge consumes Narrative Story Doctor packets, not raw transcripts.
- Bridge emits `GenericExtractionPacketRef` and delegates format compilation to `FormatIntelligenceService`.
- Bridge can emit `EngineAdapterPayload`, but does not call SuperVisual, Carousel, video, provider, API, or render services.
- SuperVisual and Carousel adapters require authorized format programs.
- Adapters preserve `brand_context_version_id` and `source_span_refs`.
- Adapters preserve composition grammar, layer stack, style route policy, frame profile, render requirement, and eval gates.
- Adapters do not call providers, renderers, UI, API, SuperVisual engines, or Carousel engines.

## Known Limitations

- Adapters produce engine-ready input objects but do not call engines.
- No UI/API integration is included.
- No provider calls or render calls are included.
- No direct `SuperVisualBuilderService` wiring is included.
- No direct `CarouselEngineService` wiring is included.
- No video engine wiring is included.

## Next Wiring Work

1. Add an optional SuperVisual builder/runtime method such as `build_from_format_adapter_input(...)`.
2. Add an optional Carousel engine method such as `create_variant_from_format_adapter_input(...)`.
3. Add integration tests proving Narrative packet -> Format program -> Adapter input -> SuperVisual draft state.
4. Add integration tests proving Narrative packet -> Format program -> Adapter input -> Carousel draft state.
5. Keep provider execution and render execution out of these bridge tests.
