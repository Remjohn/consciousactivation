# M0086 — Upstream/reference extraction record

## Status
`REGISTRY_SOURCE` / `DOCUMENT` — behavior reference only; no upstream code copied.

## CAE upstream reference
Repository: `https://github.com/Remjohn/consciousactivation`
Reference commit: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`
Exact inspected paths:
- `services/asset-intelligence/src/cae_asset_intelligence/retrieval.py`
- `services/asset-intelligence/src/cae_asset_intelligence/corpus.py`
- `services/asset-intelligence/src/cae_asset_intelligence/domain.py`

Adopted behavior:
- `SemanticCinematicRetriever` remains the canonical CAE semantic/cinematic retrieval authority.
- `SceneRecord` / `TranscriptCue` remain the governed source/time/provenance objects.
- `RightsPolicy` remains the retrieval rights filter.
- `RetrievalReceipt` remains the authoritative retrieval receipt; `AssetResearchSession` is a downstream operator projection.

Excluded:
- No second semantic index.
- No replacement for `AuthorityFirstRetrievalService`.
- No mutation of `SceneRecord`, `AssetAnnotation`, or canonical Storyboard/VAE state.
- No provider-specific or external playback runtime was installed.

## External behavioral reference: PlayPhrase
Repository: `https://github.com/kelciour/playphrase`
Reference branch: `master`
Reference commit used for source inspection: `129a948f02d124a2a8269a71685fce5ad2703f49`
Exact inspected path:
- `playphrase.py`

License status: **not established**. The public repository is archived and its visible root file list did not expose a `LICENSE` file; M0086 therefore copies no code and makes no license compatibility claim.

Adopted behavior:
- Search transcript/subtitle text for a requested phrase.
- Resolve the match to a source time interval.
- Keep a surrounding temporal context window.
- Present multiple clips as rapidly inspectable candidates.

Excluded:
- Shelling to `grep`/`ripgrep`.
- Direct `mpv` process/pipe control.
- Direct `ffmpeg` fragment export.
- External media-directory discovery and sidecar subtitle generation.
- Randomization, CLI behavior, or provider-specific assumptions.

CAE mapping:

| PlayPhrase behavior | CAE M0086 | Authority outcome |
|---|---|---|
| Phrase text search | `PlayPhraseTemporalAdapter.find` | Adapter only; `SceneRecord.transcript` is source |
| Timestamp match | `match_range` / `selected_range` | CAE `SourceTimeRange` |
| Clip padding/context | `context_range` | Bounded by governed scene interval |
| Playable media | `PlayablePreviewRef` | URI resolver only; no playback authority |
| Next/previous candidate inspection | ordered `session.candidates` | Presentation concern; no new authority |
| Player/export runtime | excluded | Downstream integration responsibility |
