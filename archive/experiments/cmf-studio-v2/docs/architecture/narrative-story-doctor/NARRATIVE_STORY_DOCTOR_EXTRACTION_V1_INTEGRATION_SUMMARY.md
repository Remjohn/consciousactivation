# Narrative Story Doctor + Extraction V1 Integration Summary

## Summary

Narrative Story Doctor + Content Extraction Intelligence V1 was integrated as an additive shared compiler layer under `src/ccp_studio`. It runs conceptually before SuperVisual, Carousel, Format Intelligence, and Video Editing Engine execution.

The layer encodes these core production laws:

- The Interview Brief is a prior, not evidence.
- Expected ingredients cannot become extracted facts without source spans.
- Verbatim spans preserve source text.
- Engine packets require source references.
- Archetype fit is resolved before format expression.
- Primitive coalition candidates are compiled before engine packets.
- Component engines consume extraction packets; they do not invent doctrine.

## Files Added

Architecture docs:

- `docs/architecture/narrative-story-doctor/README.md`
- `docs/architecture/narrative-story-doctor/OBJECT_MODEL.md`
- `docs/architecture/narrative-story-doctor/INTERVIEW_BRIEF_REVERSE_COMPILER.md`
- `docs/architecture/narrative-story-doctor/18_LAYER_MAPPING.md`
- `docs/architecture/narrative-story-doctor/FORMAT_AND_ENGINE_MAPPING.md`
- `docs/architecture/narrative-story-doctor/SERVICE_PLAN.md`
- `docs/architecture/narrative-story-doctor/IMPLEMENTATION_ORDER.md`
- `docs/architecture/narrative-story-doctor/TEST_PLAN.md`
- `docs/architecture/narrative-story-doctor/LEGACY_CMF_HUNTER_MAPPING.md`
- `docs/architecture/narrative-story-doctor/NARRATIVE_STORY_DOCTOR_EXTRACTION_V1_INTEGRATION_SUMMARY.md`

Contracts:

- `src/ccp_studio/contracts/narrative_story_doctor.py`
- `src/ccp_studio/contracts/content_extraction_intelligence.py`

Repository and services:

- `src/ccp_studio/repositories/narrative_story_doctor.py`
- `src/ccp_studio/services/narrative_story_doctor_service.py`
- `src/ccp_studio/services/content_subsystem_compiler_service.py`
- `src/ccp_studio/services/archetype_subsystem_compiler_service.py`
- `src/ccp_studio/services/primitive_coalition_compiler_service.py`
- `src/ccp_studio/services/format_expression_compiler_service.py`
- `src/ccp_studio/services/engine_packet_compiler_service.py`
- `src/ccp_studio/services/interview_brief_binding_service.py`
- `src/ccp_studio/services/extraction_commander_service.py`

Registries and skills:

- `registries/canonical/narrative_story_doctor/`
- `registries/canonical/skills/shared/narrative_story_doctor/`

Tests and bundle metadata:

- `tests/cmf_studio/test_narrative_story_doctor_v1.py`
- `APPLY_NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_PATCH.md`
- `NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_BUNDLE_MANIFEST.json`
- `NARRATIVE_STORY_DOCTOR_EXTRACTION_INTELLIGENCE_V1_LOCAL_VERIFICATION.json`

## Files Modified

No existing production source files were modified. The generated `CarouselSlideSeed.copy` field was cleaned up during integration by naming the field `slide_copy` in the new contract and service call sites.

## Tests Added

- `tests/cmf_studio/test_narrative_story_doctor_v1.py`

The test file verifies:

- brand context requirement;
- Interview Brief question contract compilation;
- expected ingredient graph compilation;
- brief bias without invented evidence;
- raw transcript lower confidence;
- cluster verbatim span preservation;
- archetype, primitive coalition, and format packet requirements;
- SuperVisual, Carousel, Video, Format 01-04, Meme, Poll, and Reaction Seed packets;
- question coverage with hits, misses, and unexpected wins;
- commander rejection of paraphrased quotes;
- Guest Asset Pack candidate counts when enforcement is enabled.

## Verification Result

Command:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result after integration:

```text
607 passed, 4 skipped
```

## Legacy CMF Hunter Preservation Status

The exact old `cmf/hunters`, `cmf/analysts`, `cmf/composers`, and `cmf/commanders` folders are not live at the CMF Studio project root. The integration therefore preserves:

- the current `src/ccp_studio` extraction stack;
- the reference CMF assembler material under `reference/conscious-rivers/src/ccp/harness/cmf/assembler/`;
- the canonical ontology roles for Visual Researcher, Storyboard Composer, Storyboard Commander, CAC Composer, and GMG Composer;
- the visual-preproduction shared skill pack.

No legacy extraction or reference code was deleted or rewritten.

## Namespace Choice

The new layer was added under `src/ccp_studio` because:

- Contract Convergence already freezes canonical paths in `src/ccp_studio`;
- recent SuperVisual, Carousel, Provider, Asset Intelligence, Visual Preproduction, and Style Route systems live in `src/ccp_studio`;
- the live repo does not currently expose a production `src/ccp` namespace;
- legacy `src/ccp` materials are present as reference assets, not live runtime modules.

Future adapter work should wrap reference/current legacy behavior into `ccp_studio` services rather than moving canonical contracts.

## Known Limitations

- Deterministic heuristic scaffold only.
- No real DSPy programs are wired.
- No UI.
- No API runtime endpoints.
- No database persistence.
- No real transcript diarization or WhisperX integration.
- No direct SuperVisual, Carousel, Video, or Format Intelligence service wiring.
- Old CMF hunters are mapped but not yet wrapped.
- No real Complete Expression Session store integration yet.

## Next Recommended Work

1. Build the legacy CMF Hunter adapter layer around current extraction services and reference beat-cluster logic.
2. Wire Narrative Story Doctor outputs into `SuperVisualBuilderService`.
3. Wire Narrative Story Doctor outputs into `CarouselEngineService`.
4. Build Format Intelligence V1 using Narrative Story Doctor outputs.
5. Build Video Editing Engine V1 consuming Format Intelligence and Story Doctor packets.
