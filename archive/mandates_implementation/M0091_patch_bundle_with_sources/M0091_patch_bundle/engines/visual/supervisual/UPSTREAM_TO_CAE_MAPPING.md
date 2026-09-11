# M0091 — Upstream → CAE mapping

Classification: `REGISTRY_SOURCE` / `DOCUMENT` unless a row explicitly says otherwise.

| Source | Current reference observed | License | Adopted behavior | Excluded |
|---|---|---|---|---|
| `chenglou/pretext` | `src/layout.ts` — `prepare`, `prepareWithSegments`, `layoutWithLines` | MIT | Pre-layout measurement, width-independent preparation, explicit line materialization | DOM/runtime ownership, semantic authority, browser-accuracy claims not re-proven locally |
| `rough-stuff/rough-notation` | `src/rough-notation.ts`; public `annotate()` / annotation-group API documented in `README.md` | MIT | Typed annotation primitive vocabulary; proposal-only CAE mapping; animation disabled in deterministic proposal defaults | Rough Notation state, page semantics, source/evidence ownership |
| `google/skia` | `include/core/SkCanvas.h`, `SkSurface.h`, `SkPaint.h` | BSD-3-Clause | Rendering substrate boundary; CAE display-list/projection remains authoritative | Full Skia source import, platform/runtime claims, semantic meaning |
| CAE BBOX | `services/pipeline/src/cmf_pipeline/composition/geometry.py` — `BBox`, `GeometryValidator` | CAE | Normalized geometry, bounds validation, collision validation | A competing geometry authority |

## Current external evidence

- Pretext current main was observed at web-visible commit `ac49b09` on 2026-09-11; GitHub did not expose the full SHA in the accessible page, so this is **not promoted to an exact 40-character pin**.
- Rough Notation current `master` history is old/stable through the accessible GitHub history; exact current tip SHA was not exposed. The public repository is MIT and documents the supported annotation types and `annotate()` API.
- Skia current `main` exposes web-visible commit `b5465d7` dated 2026-08-26 in the accessible history; exact full SHA was not exposed by the page.

No upstream source code is copied into CAE by this mandate. These sources are behavioral references only.
