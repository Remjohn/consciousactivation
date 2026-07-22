# CCP Render QA V1 Integration Bundle

Purpose: validate rendered assets before approval/export/publishing.

Contracts:
- FFprobeValidationReceipt
- FrameSamplingReceipt
- AudioLevelAnalysisReceipt
- CaptionBurnCheckReceipt
- VisualRegressionScreenshotReceipt
- CharacterQAReport
- MotionDowngradeBlocker
- DeliveryPromiseValidationReceipt

Support:
- RenderQABlocker
- RenderQAPromiseProfile
- RenderedAssetEvaluationReceipt
- RenderQACompositeReport

V1 is receipt-first and deterministic. It does not call ffprobe, ffmpeg, Remotion, providers, subprocesses, or local workers. Future adapters/workers may populate these receipts from real observations.

Hard laws:
- unplayable renders fail
- duration/dimension/audio/caption/frame/visual-regression failures block
- character identity drift blocks
- silent motion downgrade blocks unless explicitly operator-approved as warning
- V9.1 rendered-asset metrics are validated: identity consistency, composition quality, style consistency, emotional accuracy, platform fit, negative space compliance, hook strength, shareability, routeability
