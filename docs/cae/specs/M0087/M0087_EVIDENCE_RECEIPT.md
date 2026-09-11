# CAE-M0087 — Evidence Receipt

## Scope
Playable candidate previews and governed selection over the existing M0086/Asset Intelligence retrieval projection.

## Authority mapping
- Candidate cards are supplied by governed retrieval; M0087 does not retrieve or synthesize candidates.
- Source object/version/SHA, temporal interval, rights, ranking, confidence, semantic fit, quality, provenance, and real preview URI are preserved.
- `visual-candidate-auto-accept-v1` requires eligibility, confidence >= 9000 bps, semantic fit >= 9000 bps, CLEARED rights, complete provenance including scene id, and quality >= 8000 bps.
- Human ACCEPT/REJECT requires an operator; REJECT requires rationale.
- Candidate decisions create immutable content-addressed receipts and preserve rejected-candidate lineage.
- Promotion uses the existing `SUBSTITUTE_ASSET` native edit path and cannot mutate canonical state outside that path.
- Navigation wraps deterministically and is guarded by optimistic session versions.
- The UI remains fail-closed when no real playable preview URI is supplied.

## Implemented paths
- `services/asset-intelligence/src/cae_asset_intelligence/candidate_preview.py`
- `api/routers/candidate_preview.py`
- `apps/web/src/api/candidatePreview.ts`
- `apps/web/src/components/visual-studio/CandidatePreviewPanel.tsx`
- Existing Visual Asset Studio embedding and API registration
- Focused unit/API tests

## Verification
- `python -m pytest -q tests/asset_intelligence/test_m0087_candidate_preview.py tests/api/test_visual_studio_pure.py tests/asset_intelligence/test_cinematic_retrieval_m063.py tests/production_program/test_m0064_asset_selection_binding_lineage.py` — **PASS (35/35)**.
- `python -m pytest -q tests/api/test_candidate_preview.py` — **PASS (3/3)**.
- Combined M0085–M0087/M0089 regression — **PASS (72/72)**.
- `node --test services/studio/tests/*.test.mjs` — **PASS (20/20)**.
- Python compile checks — **PASS**.
- `git diff --check` — **PASS**.

## Integration repairs
- Added `services/asset-intelligence/src` to the repository pytest path so the API can import the local package without inventing a duplicate package.
- Added the missing API `pipeline` fixture and corrected the fixture’s campaign version progression to match `save_campaign_state`’s next-version contract.
- Adapted repository reads to the active `PipelineRepository.get_object` row shape while retaining store-object response handling.
- Kept the established API structured-error envelope.

## Limitations
The full web typecheck still reports unrelated pre-existing errors in other app areas; no new M0087-specific errors were observed. Actual media playback, perceptual semantic fitness, rights clearance beyond supplied metadata, and final promotion judgment remain operator responsibilities.
