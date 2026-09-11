# AGENT_HANDOFF — M0086 Asset Research Session and PlayPhrase-Like Temporal Retrieval

## Status
`EXECUTED — OPERATOR REVIEW REQUIRED`

No self-promotion performed.

## Decision implemented
Added a first-class `AssetResearchSession` as a downstream operator projection over existing CAE Asset Intelligence. Phrase retrieval is a deterministic temporal adapter over governed transcript cues. Semantic/cinematic retrieval delegates to the existing `SemanticCinematicRetriever`. Selection produces an immutable receipt and promotion produces a typed request without mutating canonical Storyboard/VAE state.

## Brownfield findings
- Existing `SceneRecord` already owns media identity, source version/hash, temporal bounds, transcript evidence, candidate identity, semantic role, insert role and rights state.
- Existing `SemanticCinematicRetriever` already enforces workspace, candidate, role, rights and index constraints before ranking and emits its own retrieval receipt.
- Existing retrieval therefore remains the authority. M0086 adds only the operator session/projection layer and the PlayPhrase-like temporal adapter.
- No `AssetResearchSession` existed in the inspected CAE tree.
- No new canonical database/state model was required.

## Changed/new repository paths
1. `services/asset-intelligence/src/cae_asset_intelligence/research_session.py` — new M0086 session contract, temporal adapter, selection/promotion projections, deterministic identifiers.
2. `services/asset-intelligence/src/cae_asset_intelligence/__init__.py` — exports the new M0086 contracts.
3. `tests/asset_intelligence/test_asset_research_session_m0086.py` — focused functional and adversarial coverage.
4. `services/asset-intelligence/M0086_UPSTREAM_REFERENCE.md` — CAE and PlayPhrase upstream mapping, source commits, license observation, adopted/excluded behavior.
5. `services/asset-intelligence/M0086_EVIDENCE_RECEIPT.md` — evidence classes, commands, observed results, limitations.
6. `services/asset-intelligence/AGENT_HANDOFF.md` — this handoff.

No files outside the M0086 allowed boundary were changed.

## Contract behavior
- `AssetResearchRequest` supports phrase and semantic/cinematic modes, candidate/role filters, rights policy, confidence, expected index hash and bounded temporal context.
- `AssetResearchCandidate` carries source identity, exact/context/selected ranges, transcript context, semantic/insert roles, confidence, rights, playable preview reference and provenance.
- `AssetResearchSession` is immutable. `reject()` returns a new session and deterministic receipt id; rejected candidates remain recorded.
- `select()` requires an available source URI and resolved rights; it returns a `CandidateSelectionReceipt` carrying the FR-VAE-017 selection fields and explicitly records `canonical_asset_mutation=NOT_PERFORMED`.
- `request_promotion()` requires operator identity plus Storyboard element/revision references and a selection receipt reference. It returns a typed downstream request and does not perform promotion itself.
- No auto-accept policy is introduced.

## External/source reference
CAE repository: `https://github.com/Remjohn/consciousactivation`
Reference commit: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`
Exact CAE paths: `services/asset-intelligence/src/cae_asset_intelligence/retrieval.py`, `corpus.py`, `domain.py`.

PlayPhrase repository: `https://github.com/kelciour/playphrase`
Reference commit: `129a948f02d124a2a8269a71685fce5ad2703f49`
Exact path: `playphrase.py`.

PlayPhrase is an archived public repository; no visible root `LICENSE` file was established during inspection. No PlayPhrase code was copied.

## Exact commands / results
- `python -m py_compile services/asset-intelligence/src/cae_asset_intelligence/research_session.py services/asset-intelligence/src/cae_asset_intelligence/__init__.py` → `PASS`.
- `python -c "import sys; sys.path.insert(0, 'services/asset-intelligence/src'); from cae_asset_intelligence import AssetResearchSession, PlayPhraseTemporalAdapter; print('import-ok')"` → `import-ok`.
- `python -m pytest tests/asset_intelligence/test_asset_research_session_m0086.py tests/asset_intelligence/test_cinematic_retrieval_m063.py -q` → `21 passed in 0.20s`.
- `git diff --check` → `PASS` before the implementation commit.

## Verification boundaries / limitations
`TEST`: the suite proves deterministic contract behavior against synthetic governed `SceneRecord` fixtures; it does not prove native browser/media-player playback, real external-media availability, perceptual semantic correctness, legal clearance beyond recorded rights metadata, or production promotion.

`OPERATOR_DECISION_REQUIRED`: inspect a real playable candidate in the eventual Visual Asset Studio integration, verify source lineage and rights state, and confirm that any downstream runtime remains subordinate to CAE authority and independently replaceable.

## Git identity
Archive baseline commit: `4a1e61ab0d642b7771c9e785e8b91a7638b3d2c3`
M0086 implementation commit: `372c297db62882cb939e0a09fef730a43813e4fa`
Current CAE upstream reference: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`

The archive was supplied without a `.git` directory, so the baseline is an explicit local immutable archive commit, not an upstream history claim. Final handoff documentation is committed separately after the implementation commit so the implementation SHA is stable and self-verifiable.

## Rollback / recovery
Revert only the M0086 implementation commit identified above. Preserve the archive baseline, evidence receipt, upstream reference, and rejected-candidate records. No database migration was introduced.

## Operator decision requested
Select exactly one:

`APPROVE`

`APPROVE-WITH-LIMITATIONS`

`REJECT`

For approval, verify the real media preview, source lineage, rights/provenance, semantic/editorial fitness, and downstream authority boundary in the integrating Studio/runtime surface.
