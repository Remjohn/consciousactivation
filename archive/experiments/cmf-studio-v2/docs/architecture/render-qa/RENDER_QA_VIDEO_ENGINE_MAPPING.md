# Render QA Video Engine Mapping

## 1. Video Render Output Contract Names

Video Editing Engine V1 provides:

- `ProxyRenderContract`
- `ProxyRenderReceipt`
- `FinalRenderContract`
- `FinalRenderReceipt`
- `FFmpegFinishPlan`
- `VideoEvaluationReceipt`
- `RemotionInputProps`
- `OTIOAuditTimeline`

## 2. Existing Evaluation Receipt Names

Existing evaluation systems include:

- `VideoEvaluationReceipt`
- `TimelineIntegrityReceipt`
- `CaptionReadabilityReceipt`
- `AudioQualityReceipt`
- `MotionDoctrineReceipt`
- `EvaluationReceipt`
- `EvaluationReviewReadModel`

## 3. Mapping to RenderQAPromiseProfile

Recommended mapping:

- `FinalRenderContract.output_profile` -> delivery id / export profile
- `FinalRenderContract.timeline_program_id` -> render source ref
- `RemotionInputProps.timeline_program_id` -> source timeline ref
- `FFmpegFinishPlan` -> expected codec/finish assumptions
- Video frame profile -> expected width/height
- Timeline duration -> expected duration
- Caption policy -> `captions_required`
- Motion doctrine -> `promised_motion_level`

## 4. Mapping to RenderedAssetEvaluationReceipt

Rendered-asset V9.1 metrics should be populated from evaluation observations:

- identity consistency
- composition quality
- style consistency
- emotional accuracy
- platform fit
- negative space compliance
- hook strength
- shareability
- routeability

## 5. RenderQACompositeReport Gates

Render QA should gate:

- proxy review
- final approval
- export
- publishing

Blocking Render QA failures should stop export/publishing and create operator-visible blockers.

## Deferred Bridge

`video_render_qa_bridge_service.py` was not added in this integration because the Video Editing Engine has multiple render contract/read-model variants and this prompt does not require changing engine semantics. The safe bridge point should be added when a persisted render output/read-model source is selected.

## Safety Confirmation

This mapping does not execute renders, providers, ffprobe, FFmpeg, Remotion, subprocesses, or Local Render Worker jobs.
