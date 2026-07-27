from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    AudioLevelAnalysisReceipt as AdapterAudioLevelAnalysisReceipt,
    DurationToleranceReceipt,
    FFprobeValidationReceipt as AdapterFFprobeValidationReceipt,
    FrameSamplingReceipt as AdapterFrameSamplingReceipt,
    RenderQAReport,
)
from ccp_studio.contracts.render_qa import (
    AudioLevelAnalysisReceipt,
    CaptionBurnCheckReceipt,
    CharacterQAReport,
    DeliveryPromiseValidationReceipt,
    FFprobeValidationReceipt,
    FrameSamplingReceipt,
    MotionDowngradeBlocker,
    RenderedAssetEvaluationReceipt,
    RenderQAPromiseProfile,
    RenderQACompositeReport,
    VisualRegressionScreenshotReceipt,
)


class RenderQAService:
    def compile_report(
        self,
        *,
        file_ref: str,
        ffprobe_validation: AdapterFFprobeValidationReceipt,
        frame_sampling: AdapterFrameSamplingReceipt,
        audio_level_analysis: AdapterAudioLevelAnalysisReceipt,
        duration_tolerance: DurationToleranceReceipt,
    ) -> RenderQAReport:
        return RenderQAReport(
            file_ref=file_ref,
            ffprobe_validation=ffprobe_validation,
            frame_sampling=frame_sampling,
            audio_level_analysis=audio_level_analysis,
            duration_tolerance=duration_tolerance,
        )

    def ffprobe(self, **kwargs) -> FFprobeValidationReceipt:
        return FFprobeValidationReceipt(**kwargs)

    def frame_sampling(self, **kwargs) -> FrameSamplingReceipt:
        return FrameSamplingReceipt(**kwargs)

    def audio(self, **kwargs) -> AudioLevelAnalysisReceipt:
        return AudioLevelAnalysisReceipt(**kwargs)

    def captions(self, **kwargs) -> CaptionBurnCheckReceipt:
        return CaptionBurnCheckReceipt(**kwargs)

    def visual_regression(self, **kwargs) -> VisualRegressionScreenshotReceipt:
        return VisualRegressionScreenshotReceipt(**kwargs)

    def character(self, **kwargs) -> CharacterQAReport:
        return CharacterQAReport(**kwargs)

    def motion(self, **kwargs) -> MotionDowngradeBlocker:
        return MotionDowngradeBlocker(**kwargs)

    def promise_profile(self, **kwargs) -> RenderQAPromiseProfile:
        return RenderQAPromiseProfile(**kwargs)

    def delivery(self, **kwargs) -> DeliveryPromiseValidationReceipt:
        return DeliveryPromiseValidationReceipt(**kwargs)

    def evaluation(self, **kwargs) -> RenderedAssetEvaluationReceipt:
        return RenderedAssetEvaluationReceipt(**kwargs)

    def composite(self, **kwargs) -> RenderQACompositeReport:
        return RenderQACompositeReport(**kwargs)
