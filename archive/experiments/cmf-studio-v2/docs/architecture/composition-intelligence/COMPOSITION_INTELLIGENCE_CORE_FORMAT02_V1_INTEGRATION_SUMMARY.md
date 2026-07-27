# Composition Intelligence Core + Format 02 V1 Integration Summary

## Branch

`feat/composition-intelligence-core-format02-v1`

## Scope

This integration adds the Composition Intelligence layer that runs after Format Intelligence and before Visual Preproduction, Asset Intelligence, Style Route, provider planning, Avatar Performance, and Video Editing.

```text
Narrative Story Doctor / Extraction Intelligence
-> Format Intelligence
-> Composition Intelligence
-> Visual Preproduction / Asset Intelligence / Style Route / Provider Planning
-> Avatar Performance Layer
-> Video Editing Engine
-> Render / Eval / Publishing
```

Composition Intelligence owns locked spatial meaning: cognitive load, attention path, safe zones, text placement, avatar placement, audience proxy placement, real-life cutout placement, layer plan, and provider edit boundaries.

## Files Added

- `docs/architecture/composition-intelligence/`
- `registries/canonical/composition_intelligence/`
- `registries/canonical/format02_composition/`
- `registries/canonical/skills/shared/composition_intelligence/`
- `registries/canonical/skills/shared/format02_composition/`
- `src/ccp_studio/contracts/composition_intelligence.py`
- `src/ccp_studio/contracts/format02_composition_intelligence.py`
- `src/ccp_studio/services/composition_intelligence_service.py`
- `src/ccp_studio/services/composition_template_service.py`
- `src/ccp_studio/services/cognitive_load_gate_service.py`
- `src/ccp_studio/services/attention_path_service.py`
- `src/ccp_studio/services/text_placement_service.py`
- `src/ccp_studio/services/real_life_cutout_composition_service.py`
- `src/ccp_studio/services/provider_composition_plate_service.py`
- `src/ccp_studio/services/reference_edit_contract_service.py`
- `src/ccp_studio/services/format02_composition_service.py`
- `src/ccp_studio/services/composition_commander_service.py`
- `src/ccp_studio/services/format02_format_program_to_composition_adapter_service.py`
- `tests/cmf_studio/test_composition_intelligence_core_format02_v1.py`
- `COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_BUNDLE_MANIFEST.json`
- `COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_LOCAL_VERIFICATION.json`
- `APPLY_COMPOSITION_INTELLIGENCE_CORE_AND_FORMAT02_PACK_V1_PATCH.md`

## Files Modified

- `src/ccp_studio/services/format02_composition_service.py`
- `tests/cmf_studio/test_composition_intelligence_core_format02_v1.py`

## Tests Added

- Composition context brand-context/source-span gates.
- Text placement visible-word gate.
- Avatar action concept-service gate.
- Audience proxy SFL gate.
- Real-life cutout role/source gate.
- Provider edit-boundary drift gates.
- Cognitive-load overload gate.
- Format 02 one-concept and one-primary-action gates.
- Format 02 clean scene compilation.
- Composition lock / commander authorization.
- Ideogram composition-plate contract.
- Flux reference-edit contract.
- Optional Format 02 Format Intelligence program to composition adapter.

## Final Test Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result at integration time:

```text
668 passed, 4 skipped
```

## Existing Systems Inspected

The repo already contains related but separate systems:

- `src/ccp_studio/contracts/composition_runtime.py`
- `src/ccp_studio/services/composition_runtime_service.py`
- `src/ccp_studio/contracts/composition.py`
- `src/ccp_studio/services/composition_service.py`
- `src/ccp_studio/contracts/carousel_engine.py`
- `src/ccp_studio/contracts/visual_preproduction.py`
- `src/ccp_studio/contracts/format_intelligence.py`
- `src/ccp_studio/contracts/style_route_runtime.py`
- `docs/architecture/visual-preproduction/`
- `docs/architecture/format-intelligence/`
- `docs/architecture/format-engine-adapters/`

No naming conflict required overwriting these systems. This bundle adds `composition_intelligence` and `format02_composition_intelligence` as the pre-video composition layer. The existing runtime, Ideogram composition lineage, Carousel composition, and Visual Preproduction systems remain intact.

## Optional Format Intelligence Adapter

Added:

```text
src/ccp_studio/services/format02_format_program_to_composition_adapter_service.py
```

It maps:

```text
Format02AvatarPaperCutExplainerProgram
-> Format02CompositionService.compile_scene_program(...)
```

The adapter extracts stable fields only:

- `brand_id`
- `brand_context_version_id`
- `source_span_refs`
- `format_intelligence_program_id`
- `teachable_mechanism_ref`
- `concept_node_refs`
- `diagram_sequence_ref`
- `avatar_clip_requirements`

It produces a deterministic, low-load `Format02SceneProgram` and stops before provider jobs or rendering.

## Confirmed Boundaries

- Cognitive-load gates run.
- One-concept and one-primary-action gates run.
- Provider edit boundaries forbid text, layout, avatar, and claim drift.
- Ideogram is represented only as a composition-plate contract.
- Flux is represented only as a reference-edit contract.
- No real provider calls are made.
- No Ideogram API calls are made.
- No Flux API calls are made.
- No rendering is added.
- No UI/API endpoints are added.
- No Avatar Performance runtime is added.
- No Video Editing Engine is added.

## Known Limitations

- Deterministic scaffold only.
- No real provider calls.
- No real Ideogram or Flux integration.
- No render calls.
- No UI/API.
- No real Visual Preproduction wiring.
- No real Asset Intelligence wiring.
- No Avatar Performance runtime.
- No Video Editing Engine.

## Next Recommended Work

1. Build Avatar Performance Layer V1.
2. Add `Format02SceneProgram -> AvatarPerformancePlan` adapter.
3. Add `Format02SceneProgram -> Visual Research / Asset Intelligence` requirement adapter.
4. Add `ProviderCompositionPlateContract` and `ReferenceEditContract` to provider job adapters.
5. Then build Video Editing Engine V1 that consumes locked `CompositionSceneProgram`, `AvatarPerformancePlan`, provider/layer outputs, and timeline constraints.
