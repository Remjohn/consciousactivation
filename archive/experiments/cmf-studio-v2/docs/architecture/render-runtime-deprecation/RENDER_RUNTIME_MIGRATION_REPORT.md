# Render Runtime Migration Report

## Canonical Direction

Legacy Python/C++ Skia sidecars are deprecated in favor of:

Remotion Node.js + `@remotion/skia`

The canonical execution path is:

1. Video Editing Engine or template/still-visual compiler emits typed render payloads.
2. Capability Preflight confirms local render readiness when real execution is requested.
3. Local Render Worker owns queue, lease, heartbeat, and result lifecycle.
4. Remotion/FFmpeg adapter compiles command plans and stays dry-run unless real-local gates pass.
5. Render QA V1 validates observations before review, approval, export, or publishing.

## Legacy Paths To Migrate

| Legacy surface | Current status | Replacement target | Delete now? |
|---|---|---|---|
| `HeadlessFrameRenderRequest` / `HeadlessFrameRenderReceipt` | Test-covered legacy queue contract | `RenderJob` with `template_preview_render`, `thumbnail_render`, or `avatar_state_preview_render` | No |
| `AvatarExportWorkerJob` / `AvatarExportReceipt` | Test-covered legacy worker contract | `RenderJob` with `avatar_state_preview_render` plus Avatar Asset Production manifests | No |
| `SkiaRenderBinding` / `SkiaRenderReceipt` | Test-covered legacy binding/receipt | `RemotionRenderJob`, `FFmpegFinishJob`, `RenderQACompositeReport` | No |
| `SingleImageSkiaScene` | Test-covered still visual read model | Template Preview / Atlas and Remotion Skia payload read models | No |
| `skia_render_job:*` refs | Test-covered pointer refs | `RenderJob.render_job_id` and artifact refs | No |
| `cmf_skia_renderer` final authority | Test-covered provider plan authority | Remotion Node.js + `@remotion/skia` runtime authority behind gates | No |
| Old spec path `src/ccp/sidecars/skia-renderer/` | Not present as executable code | No action except deprecation docs | No |

## Required Replacement Tests Before Deletion

Do not delete legacy contracts until these pass:

1. Single-image SuperVisual output can be represented as Template Preview / Atlas plus Remotion Skia payload without `SingleImageSkiaScene`.
2. Carousel preview/export can compile continuous slide previews without `skia_render_job_refs`.
3. Avatar preview/export can route through Local Render Worker fake/dry-run jobs without `AvatarExportWorkerJob`.
4. Headless frame preview routes through `RenderJob` lifecycle and Render QA receipts.
5. `tests/cmf_studio/test_batch2_asset_program_compilers.py` has explicit replacement coverage or is migrated.
6. `tests/cmf_studio/test_batch3_production_orchestration_and_still_visuals.py` no longer requires `skia-renderer` as selected provider authority.

## Migration Steps

1. Add replacement read models for still visual and carousel preview output using Template Preview / Atlas.
2. Add Local Render Worker job mapping for still visual and carousel preview render jobs.
3. Map legacy `render://skia/...` refs to workspace `ArtifactRef` pointers.
4. Bridge legacy `SkiaRenderReceipt` assertions to Render QA V1 receipts.
5. Update provider menu and style route tests to prefer Remotion Skia authority.
6. Keep fixture fallback and old read models until all replacement tests pass.
7. Only then remove deprecated classes and old registry requirements in a separate deletion prompt.

## Guardrails

- No provider calls.
- No renderer calls.
- No subprocess calls.
- No Remotion/FFmpeg/ffprobe calls during tests.
- No deletion in this audit.
- No blind `git clean`.

## Next Recommended Prompt

Create a replacement parity prompt for still visual and carousel preview runtime mapping:

`PROMPT_08_STILL_VISUAL_CAROUSEL_REPLACE_LEGACY_SKIA_RUNTIME_WITH_REMOTION_SKIA_PARITY`

That prompt should be implementation work. This prompt remains an audit/deprecation marker pass.
