# M0093 External Upstream -> CAE Mapping

## Open Carrusel

| Evidence class | Exact upstream source | Pinned source | License | Adopted behavior | Explicitly excluded |
|---|---|---|---|---|---|
| REGISTRY_SOURCE | `src/types/carousel.ts` | `https://github.com/Hainrixz/open-carrusel/tree/8ba717ba4d59c8a9a5f64d278f6e83cbea34efde` (current `main` at audited commit) | MIT | `AspectRatio` values `1:1`, `4:5`, `9:16`; carousel/slide data shape; slide ordering; `MAX_SLIDES=20`; `DIMENSIONS` 1080x1080 / 1080x1350 / 1080x1920 | Open Carrusel storage, agent/chat behavior, UI/editor state, model policy, mutation semantics |
| REGISTRY_SOURCE | `src/lib/slide-html.ts` | same commit `8ba717ba4d59c8a9a5f64d278f6e83cbea34efde` | MIT | `wrapSlideHtml(slideHtml, aspectRatio, options?)` full-HTML slide wrapper and exact dimension contract | External wrapper as authority; external persistence/export pipeline |

CAE implementation uses the observed data shape only as a downstream handoff projection. No Open Carrusel state is written and `native_reachability_proven=False` is explicit.

## Slidev

| Evidence class | Exact upstream source | Pinned source | License | Adopted behavior | Explicitly excluded |
|---|---|---|---|---|---|
| REGISTRY_SOURCE | `docs/guide/syntax.md` | tag `v52.19.1` (`dbc307b` release commit as displayed by GitHub) | MIT | `slides.md` Markdown entrypoint; `---` slide separators; frontmatter | Slidev as semantic/storyboard authority; Slidev-generated content as CAE evidence |
| REGISTRY_SOURCE | `docs/guide/animations.md` | tag `v52.19.1` (`dbc307b`) | MIT | native `v-click` build-step marker, including absolute numeric step form | Slidev timing/animation policy beyond the CAE presentation expression |

The adapter emits `slides.md` and marks `native_reachability_proven=False`; installation/build/browser fidelity remains operator/runtime responsibility.

## reveal.js

| Evidence class | Exact upstream source | Pinned source | License | Adopted behavior | Explicitly excluded |
|---|---|---|---|---|---|
| REGISTRY_SOURCE | `index.html` | tag `6.0.1` (`52c6c8b` release commit as displayed by GitHub) | MIT | canonical scaffold: reset/reveal/theme CSS, `.reveal > .slides`, `dist/reveal.js`, `Reveal.initialize({hash:true})` | reveal.js as semantic/storyboard authority; runtime state as CAE state |
| REGISTRY_SOURCE | release documentation for fragments / fragment attributes | tag `6.0.1` | MIT | `.fragment` plus `data-fragment-index` for deterministic build ordering | runtime-driven semantic reordering or creative mutation |

The adapter emits `index.html` and marks `native_reachability_proven=False`; no reveal runtime is installed or invoked by this mandate.

## CAE authority boundary

The canonical CAE source remains the M0079 storyboard session/revision layer and M0080 `CarouselStoryboardProgram` / `PresentationStoryboardProgram`. Runtime adapters re-run the canonical compiler, verify validation and compile-receipt lineage, and compare the full canonical expression before projection. Runtime syntax cannot change semantic purpose, evidence refs, provenance, or promotion state.
