# Lane C — Static Composition Runtime Activation

## Exclusive target paths

```text
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_composition_runtime/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_static_skia_runtime/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_pretext_adapter/**
04_ATOMIC_HARNESS_PIPELINE/packages/cmf_annotation_runtime/**
04_ATOMIC_HARNESS_PIPELINE/tests/static/**
```

## Predecessor source

```text
THE_CMF_STUDIO(2).zip/
  src/ccp_studio/contracts/composition_runtime.py
  src/ccp_studio/services/composition_runtime_service.py
  src/ccp_studio/contracts/asset_program_compilers.py
  src/ccp_studio/services/asset_program_compiler_service.py
  src/ccp_studio/services/carousel_engine_service.py
  src/ccp_studio/services/carousel_render_service.py
  src/ccp_studio/services/supervisual_runtime_service.py
  src/ccp_studio/services/supervisual_project_service.py
  docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md
  docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md
  docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md
  docs/tech-specs/TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md
```

## Deliver

- Typed static Composition IR.
- Real PRETEXT measurement adapter with pinned fonts.
- Geometrics/layout and collision validation.
- Typed Rough Annotation Cue representation.
- Skia realization of text, images, geometry, annotation cues, masks, and export.
- Real PNG/JPEG/PDF outputs.
- One Carousel family and one SuperVisual family running end to end.
- Visual Syntax measurement/reparse receipts.
