# M0086 — Evidence Receipt

## Mandate
`M0086 — Asset Research Session and PlayPhrase-Like Temporal Retrieval`

## Evidence classes
- `DOCUMENT`: mandatory CAE constitutional, PRD, M65–M72, Asset Intelligence, and Visual Production authority materials were inspected in the uploaded repository. The constitution and M72 require reuse of canonical authorities; the Media Intelligence brief defines Evidence Retrieval as search → locate → resolve → contextualize → verify → promote; the Visual Asset Editor update defines Asset Research Session as retrieval → candidates → preview → inspect → accept/reject → promote.
- `REGISTRY_SOURCE`: current CAE upstream files and external PlayPhrase source inspected at pinned references recorded in `M0086_UPSTREAM_REFERENCE.md`.
- `EXECUTABLE`: M0086 source module and package exports compile and execute against current Asset Intelligence objects.
- `TEST`: focused M0086 plus M063 retrieval regression suite passed.
- `OPERATOR_DECISION_REQUIRED`: actual media playback, perceptual relevance, source-quality assessment, legal resolution for review-required rights, and promotion into canonical Storyboard/VAE state remain operator/integration responsibilities.

## Commands and observed results

1. Python syntax:
```text
python -m py_compile services/asset-intelligence/src/cae_asset_intelligence/research_session.py services/asset-intelligence/src/cae_asset_intelligence/__init__.py
```
Observed: `PASS`.

2. Focused M0086 + existing retrieval regression:
```text
python -m pytest tests/asset_intelligence/test_asset_research_session_m0086.py tests/asset_intelligence/test_cinematic_retrieval_m063.py -q
```
Observed: `21 passed in 0.20s`.

3. Diff hygiene:
```text
git diff --check
```
Observed: `PASS` before final commit.

4. Import smoke:
```text
python -c "import sys; sys.path.insert(0, 'services/asset-intelligence/src'); from cae_asset_intelligence import AssetResearchSession, PlayPhraseTemporalAdapter; print('import-ok')"
```
Observed: `import-ok`.

## Proof coverage
- Happy path: exact transcript phrase → timestamped candidate → playable preview reference.
- Context proof: surrounding transcript/range is preserved without erasing the exact phrase match range.
- Good-looking-but-wrong counterexample: semantically close pressure scene is excluded by the requested `WORLD_BUILDING` insert-role constraint.
- Rights negative: `UNKNOWN_UNLICENSED` phrase hit is excluded.
- Stale negative: semantic request with mismatched expected index hash is `BLOCKED` with no candidates.
- Preview negative: missing media URI prevents selection.
- Immutability: selection and promotion are projections; canonical asset state is not mutated.
- Rejection: rejected candidates are preserved and cannot later be selected from that session.
- Deterministic replay: repeated identical requests produce identical session/candidate/selection identifiers.
- Authority separation: phrase adapter searches only governed `SceneRecord.transcript` data and does not rank, promote, or mutate canonical state.

## Non-claims
- No native browser/MPV playback was proven.
- No real external media source was used for evidence.
- No production Storyboard/VAE promotion was performed.
- No deterministic automatic acceptance policy was introduced; all selection in this slice is explicit operator selection.
- The archive baseline had no usable Git history; the implementation commit below is a local evidence commit derived from an immutable archive-baseline commit.
