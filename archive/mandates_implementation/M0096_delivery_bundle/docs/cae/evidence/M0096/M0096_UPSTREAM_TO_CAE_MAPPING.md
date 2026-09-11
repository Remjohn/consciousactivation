# CAE-M0096 — Upstream → CAE Mapping

**Evidence class:** `REGISTRY_SOURCE` + `DOCUMENT`  
**Date:** 2026-09-11  
**Purpose:** record the exact external source surface inspected for the bounded partner-ready vertical slice without importing external semantic authority into CAE.

## Upstream source

- Repository: https://github.com/0xsline/OpenChatCut
- Current upstream `main` commit observed 2026-09-11: `607e0fcc2b755a92a659deb54305ba8164930ae3`
- Current package version observed in upstream package metadata: `0.2.14`
- License: `AGPL-3.0-or-later`
- Local vendored package metadata: `engines/video/openchatcut/upstream/package.json`
- Local vendored source is **not** asserted to be byte-identical to upstream commit `607e0fcc...`; the supplied repository has no `.git` metadata, so its local revision cannot be provenance-linked to that commit.

## Exact files inspected and treatment

| Upstream file | Local CAE file inspected | Local SHA-256 | Adopted behavior | Explicitly excluded |
|---|---|---|---|---|
| `src/agent/tools/edit-item-visual.ts` | `engines/video/openchatcut/upstream/src/agent/tools/edit-item-visual.ts` | `69d6ab0b1050fb142ceb837b5c4c8ebcda88bec5e5d3fb45b2e37c2e051b1d44` | Deterministic numeric parsing, clamping and visual transform/crop execution vocabulary | Semantic intent, asset identity, provenance, operator promotion, CAE state mutation |
| `src/editor/visualFrameGeometry.ts` | `engines/video/openchatcut/upstream/src/editor/visualFrameGeometry.ts` | `d64f5ea9f3bb7941fdb447f85a42584d4bef87fb25a610b9a235bbcf03fb76e5` | Deterministic rendered/visible frame geometry and bounded corner-radius computation | CAE geometry authority, semantic meaning, source evidence, acceptance |
| `src/components/timeline/track-mute-visual.verify.ts` | `engines/video/openchatcut/upstream/src/components/timeline/track-mute-visual.verify.ts` | `7b554faf011204fe422553101c6cc1d6024e7586578ea707b8b564c6b1c751ef` | Executable visual verification pattern for downstream runtime UI behavior | CAE release gates, operator authority, evidence lineage |

## CAE authority and execution boundary

The canonical CAE path already present in the supplied snapshot is:

`Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`

The downstream runtime is reached through the existing M0065/M0067 boundary. OpenChatCut remains a replaceable execution/runtime surface. The CAE path retains ownership of semantic meaning, contracts, state, provenance, validation and promotion.

No external repository implementation was copied or edited as part of M0096. No second visual, retrieval, storyboard, transformation, Design System, or semantic-program authority is introduced.

## Source and evidence limitations

1. The exact supplied archive has no `.git` metadata. Local upstream source cannot be assigned a truthful local commit SHA.
2. Native OpenChatCut runtime is not reachable at the configured endpoint (`http://localhost:5199/api/external-mcp/mcp`) in this environment.
3. No real governed source media artifact is supplied through `CAE_M067_SOURCE_MEDIA`.
4. The snapshot contains synthetic/corrupt MP4 fixtures only; they are not promoted as production evidence.
5. Because the native runtime and real source media are unavailable, this mapping establishes source inspection and boundary intent only; it is not a native-render fidelity or partner-readiness certificate.
