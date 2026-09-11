# SuperVisual composition/editor surface

`SuperVisualEditor` is a bounded editor/projection facade. Semantic meaning, canonical state, source retrieval, provenance, and release remain upstream CAE authorities.

Production construction is `SuperVisualEditor.from_cae()`, which binds the surface to the existing CAE `BBox`/`GeometryValidator`, `PretextEngine`, and `SkiaStaticRenderer` implementations. The module does not vendor or duplicate upstream Pretext, Rough Notation, or Skia source.

`prepare_annotation()` emits a typed Rough Notation proposal with animation disabled by default. It does not persist or promote the change. `prepare_revision()` requires a human operator actor and produces deterministic revision identity. Geometry edits are review drafts only.

The web component `apps/web/src/components/visual-studio/SuperVisualPrimitiveStack.tsx` exposes the same four distinct primitive responsibilities on the existing Visual Asset Studio surface.
