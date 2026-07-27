# CCP Template Preview / Template Atlas V1 Integration Bundle

This bundle makes SuperVisual, Carousel, and Format 02 templates visually inspectable.

## Purpose

JSON-only templates are not operationally useful. Operators need visual thumbnails, slot labels, sample payloads, and preview read models before templates are approved into production registries.

This bundle adds:

```text
TemplateAtlas
TemplatePreviewRequest
TemplatePreviewResult
TemplateSlotMap
TemplateSamplePayload
SuperVisualTemplatePreview
CarouselTemplatePreview
Format02SceneTemplatePreview
TemplateApprovalReceipt
TemplateVersion
```

## Scope

V1 produces deterministic SVG preview read models only.

It does not:

```text
call providers
call Remotion
call FFmpeg
render real media
create UI routes
write files to workspace
approve templates automatically
```

## Apply after

Recommended:

```text
Project Workspace + Artifact Store V1
Composition Intelligence Core + Format 02 Pack V1
SuperVisual / Carousel foundations
Video Editing Engine V1
```

## What this bundle adds

```text
docs/architecture/template-preview-atlas/
fixtures/template_preview/
registries/canonical/template_preview_atlas/
src/ccp_studio/contracts/template_preview_atlas.py
src/ccp_studio/repositories/template_preview_atlas.py
src/ccp_studio/services/template_atlas_service.py
src/ccp_studio/services/template_preview_service.py
src/ccp_studio/services/supervisual_template_preview_service.py
src/ccp_studio/services/carousel_template_preview_service.py
src/ccp_studio/services/format02_template_preview_service.py
tests/cmf_studio/test_template_preview_atlas_v1.py
```

## Hard laws

```text
Template preview cannot call providers.
Template preview cannot call renderers.
Template preview must emit a visual SVG and thumbnail URI.
Template preview request must include a sample payload.
Sample payload must satisfy required template slots.
Template approval cannot pass with blockers.
Template version requires a stable template hash.
Carousel preview requires continuous slide indexes.
Format 02 preview must preserve cognitive-load defaults visually.
SuperVisual preview must preserve one source truth / one hero object logic.
```
