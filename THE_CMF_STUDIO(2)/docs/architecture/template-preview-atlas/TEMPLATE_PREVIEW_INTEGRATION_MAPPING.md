# Template Preview Integration Mapping

Template Preview / Template Atlas V1 adds deterministic SVG preview read models. It does not replace runtime engines, provider jobs, renderer contracts, or operator-web screens.

## Project Workspace / Artifact Store

Future call sites:

- `TemplatePreviewResult.preview_svg` can later be registered as `ArtifactRef` with `ArtifactCategory.TEMPLATE`.
- `TemplatePreviewResult.thumbnail_uri` can later be stored under:

```text
client_workspaces/<client_slug>/libraries/templates/
```

- Template approval receipts can later be stored under either:

```text
client_workspaces/<client_slug>/runs/<run_id>/receipts/
client_workspaces/<client_slug>/libraries/templates/
```

V1 integration status:

- No file materialization is performed by default.
- Optional tests register preview SVG text as an artifact ref and compile a manifest without writing media bytes.

## SuperVisual

Future call sites:

- `SuperVisualTemplatePreview` should populate Template Atlas cards for SuperVisual templates.
- SuperVisual template slot maps should align with SuperVisual runtime concepts such as source truth, hero object, power phrase, brand mark, negative space, snapshot preview refs, and display payloads.

Rules:

- Do not replace `SuperVisualRuntimeService`.
- Do not bypass runtime state transitions.
- Do not treat template previews as rendered SuperVisual outputs.
- Do not call providers or renderers from preview compilation.

## Carousel

Future call sites:

- `CarouselTemplatePreview` should populate sequence/slide template atlas cards.
- Carousel slide indexes must be continuous and compatible with Carousel Engine sequence assumptions.

Rules:

- Do not replace `CarouselEngineService`.
- Do not export unapproved carousel variants from preview results.
- Do not call provider materialization or fake render batch services from preview compilation.

## Format 02

Future call sites:

- `Format02SceneTemplatePreview` should support avatar/object/proxy scene layout preview.
- It should preserve:
  - one concept
  - visible word budget
  - avatar action slot
  - hero object slot
  - audience proxy slot
  - SFL function

Rules:

- Preview compilation should remain upstream of any Video Editing Engine timeline decisions.
- Providers may later execute locked composition contracts, but Template Preview V1 only emits SVG read models.

## Capability Preflight

Template Preview V1 requires no provider or runtime capabilities.

Later, if a real preview renderer is added, call preflight first:

```python
CapabilityPreflightService().run_preflight(
    pipeline_id=PipelineId.TEMPLATE_PREVIEW,
    remotion_configured=...,
    local_worker_configured=...,
)
```

V1 does not call preflight because it does not request provider/runtime execution.

## Operator-Web

Future Template Atlas UI should consume `TemplatePreviewResult` and show:

- visual thumbnail
- preview SVG
- slot labels
- sample payload
- JSON inspector
- template version
- approval status
- blockers

Rules:

- Do not build UI in this integration.
- Preserve existing operator-web screens and fixture fallback.
- Template Atlas should not duplicate SuperVisual Studio, Carousel Studio, or Composition Studio.
