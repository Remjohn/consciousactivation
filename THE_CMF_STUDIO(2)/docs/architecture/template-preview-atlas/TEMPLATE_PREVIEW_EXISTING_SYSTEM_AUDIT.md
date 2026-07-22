# Template Preview Existing System Audit

Branch: `feat/template-preview-atlas-v1`

Baseline before bundle apply:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result: `775 passed, 10 skipped`.

## Existing Template-Related Contract Files Found

- `src/ccp_studio/contracts/composition_runtime.py`
  - Existing composition template concepts include `SceneTemplateBinding`, `CompositionTemplateLayer`, `CompositionTemplateJson`, `CompositionTemplateApprovalReceipt`, `CompositionTemplateFamily`, and `OpenSourceTemplateConversion`.
  - Existing templates are tied to composition runtime, approval, conversion, and renderer props, not deterministic atlas preview read models.
- `src/ccp_studio/contracts/composition_intelligence.py`
  - Existing composition concepts include `CompositionTemplate` and `SceneTemplate`.
  - These model composition decisions and scene templates, not visual template atlas cards.
- `src/ccp_studio/contracts/reaction_editing.py`
  - Existing live reaction template routing contracts include `ReactionEditingTemplate`, `TemplateMotionGrammar`, `ReactionTemplateRoute`, and `ReactionTemplateRouteReceipt`.
- `src/ccp_studio/contracts/comfy_template_migration.py`
  - Existing ComfyUI migration contracts include template hashing and migration receipts.
- `src/ccp_studio/contracts/gates.py`
  - Existing provider template approval/hash gate exists for imported provider templates.
- `src/ccp_studio/contracts/carousel_engine.py`
  - Includes `CarouselPreviewPack`, carousel composition/template-related objects, and sequence gates.
- `src/ccp_studio/contracts/project_workspace_artifact_store.py`
  - Includes `ArtifactCategory.TEMPLATE` and template library folder conventions.
- `src/ccp_studio/contracts/capability_preflight.py`
  - Includes `PipelineId.TEMPLATE_PREVIEW`.

## Existing SuperVisual Template Files Found

- No dedicated `SuperVisualTemplate` or `TemplatePreview` contract was found.
- SuperVisual runtime files exist:
  - `src/ccp_studio/contracts/supervisual_runtime.py`
  - `src/ccp_studio/services/supervisual_runtime_service.py`
  - `operator-web/src/screens/SuperVisualStudio.jsx`
  - `operator-web/src/components/supervisual/*`
- Existing SuperVisual frontend code has canvas preview concepts via `SuperVisualCanvasPreview`, but it consumes runtime snapshots, not template atlas preview results.

## Existing Carousel Template Files Found

- Carousel engine contracts and registries exist:
  - `src/ccp_studio/contracts/carousel_engine.py`
  - `src/ccp_studio/services/carousel_engine_service.py`
  - `registries/canonical/carousel/composition_templates.v1.json`
  - `registries/canonical/skills/engines/carousel/`
- No dedicated Carousel Template Atlas preview module was found.

## Existing Format 02 Scene/Template Files Found

- Format 02 composition contracts and services exist:
  - `src/ccp_studio/contracts/format02_composition_intelligence.py`
  - `src/ccp_studio/services/format02_composition_service.py`
  - `registries/canonical/format02_composition/format02_composition_templates.v1.json`
- Existing Format 02 systems enforce concept, motion, avatar/proxy/object, and cognitive-load gates.
- No deterministic Format 02 scene template preview read model was found.

## Existing Preview/Thumbnail/Read-Model Files Found

- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` contains preview-like timeline fixture data.
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx` renders frontend proxy preview layouts.
- `src/ccp_studio/contracts/asset_program_compilers.py` includes preview and carousel atlas output concepts.
- `src/ccp_studio/contracts/deterministic_rendering.py` and `src/ccp_studio/services/deterministic_rendering_service.py` provide deterministic render contracts, but this bundle must not call renderers.
- No existing `preview_svg`, `thumbnail_uri`, `sample_payload`, or `TemplatePreviewResult` contract was found in source.

## Existing Operator-Web Template/Preview UI Files Found

- No dedicated Template Atlas / Template Preview screen was found in `operator-web/src/screens`.
- Existing CSS contains template and preview classes in `operator-web/src/styles.css`, plus timeline and SuperVisual preview styling.
- The operator-web navigation audit identified Template Atlas / Preview as missing and recommended adding backend read models before UI.

## Naming Conflicts

- `template` is already used by composition runtime, reaction editing, ComfyUI migration, provider template gates, and UI CSS.
- The requested target module name `template_preview_atlas` is new and avoids overwriting existing template owners.
- Bundle package `__init__.py` files are not copied over existing package init files.

## Additive Applicability

This bundle can be applied additively:

- All requested target files/directories were missing before copy.
- Existing composition, SuperVisual, Carousel, and Format 02 systems remain untouched.
- The new module should operate as deterministic preview/read-model infrastructure, not as a replacement for runtime template, provider, or render systems.

## Files Requiring Merge Instead Of Copy

None. All requested target files were absent before integration. Existing `src/ccp_studio/contracts/__init__.py`, `src/ccp_studio/services/__init__.py`, and `src/ccp_studio/repositories/__init__.py` were inspected and left unchanged.
