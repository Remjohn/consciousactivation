from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    AudioLevelAnalysisReceipt as AdapterAudioLevelAnalysisReceipt,
    DurationToleranceReceipt as AdapterDurationToleranceReceipt,
    FFprobeValidationReceipt as AdapterFFprobeValidationReceipt,
    FrameSamplingReceipt as AdapterFrameSamplingReceipt,
    RenderQAReport as AdapterRenderQAReport,
)
from ccp_studio.contracts.render_qa import (
    AudioLevelAnalysisReceipt,
    CaptionBurnCheckReceipt,
    CharacterQAReport,
    DeliveryPromiseValidationReceipt,
    FFprobeValidationReceipt,
    FrameSamplingReceipt,
    MotionDowngradeBlocker,
    ObservedMotionLevel,
    RenderedAssetEvaluationReceipt,
    RenderQAPromiseProfile,
    RenderQACompositeReport,
    VisualRegressionScreenshotReceipt,
)


class RenderQAAdapterBridgeService:
    """Map dry-run/adapter observations into canonical Render QA V1 receipts.

    This bridge only translates already-supplied observations. It never calls
    ffprobe, FFmpeg, Remotion, providers, subprocesses, or Local Render Worker.
    """

    external_tool_calls_executed = False
    provider_calls_executed = False
    local_worker_jobs_executed = False

    def ffprobe_from_adapter(
        self,
        receipt: AdapterFFprobeValidationReceipt,
        *,
        playable: bool = True,
        has_video_stream: bool = True,
        expected_width: int | None = None,
        expected_height: int | None = None,
    ) -> FFprobeValidationReceipt:
        return FFprobeValidationReceipt(
            file_ref=receipt.file_ref,
            playable=playable,
            duration_ms=receipt.duration_ms,
            width=receipt.width,
            height=receipt.height,
            fps=receipt.fps,
            video_codec=receipt.video_codec,
            audio_codec=receipt.audio_codec,
            has_video_stream=has_video_stream,
            has_audio_stream=receipt.audio_codec is not None,
            expected_width=expected_width,
            expected_height=expected_height,
        )

    def frame_sampling_from_adapter(self, receipt: AdapterFrameSamplingReceipt) -> FrameSamplingReceipt:
        return FrameSamplingReceipt(
            file_ref=receipt.file_ref,
            sampled_frame_count=receipt.sampled_frame_count,
            expected_scene_count=receipt.expected_scene_count,
            black_frame_count=receipt.black_frame_count,
            broken_text_detected=receipt.broken_text_detected,
            visual_artifact_detected=False,
        )

    def audio_from_adapter(self, receipt: AdapterAudioLevelAnalysisReceipt) -> AudioLevelAnalysisReceipt:
        return AudioLevelAnalysisReceipt(
            file_ref=receipt.file_ref,
            integrated_lufs=receipt.integrated_lufs,
            true_peak_db=receipt.true_peak_db,
            target_lufs=receipt.target_lufs,
            tolerance_lufs=receipt.tolerance_lufs,
            max_true_peak_db=receipt.max_true_peak_db,
        )

    def delivery_from_adapter_duration(
        self,
        *,
        file_ref: str,
        promise_profile: RenderQAPromiseProfile,
        duration_tolerance: AdapterDurationToleranceReceipt,
        actual_width: int,
        actual_height: int,
        captions_pass: bool = True,
        motion_pass: bool = True,
        negative_space_ratio: float = 0.35,
        identity_consistency: float = 0.95,
        composition_quality: float = 0.90,
        style_consistency: float = 0.90,
        emotional_accuracy: float = 0.85,
        platform_fit: float = 0.88,
        hook_strength: float = 0.82,
        shareability: float = 0.75,
        routeability: float = 0.90,
    ) -> DeliveryPromiseValidationReceipt:
        return DeliveryPromiseValidationReceipt(
            file_ref=file_ref,
            promise_profile=promise_profile,
            actual_width=actual_width,
            actual_height=actual_height,
            actual_duration_ms=duration_tolerance.actual_duration_ms,
            captions_pass=captions_pass,
            motion_pass=motion_pass,
            negative_space_ratio=negative_space_ratio,
            identity_consistency=identity_consistency,
            composition_quality=composition_quality,
            style_consistency=style_consistency,
            emotional_accuracy=emotional_accuracy,
            platform_fit=platform_fit,
            hook_strength=hook_strength,
            shareability=shareability,
            routeability=routeability,
        )

    def composite_from_adapter_report(
        self,
        *,
        adapter_report: AdapterRenderQAReport,
        promise_profile: RenderQAPromiseProfile,
        captions_pass: bool = True,
        screenshot_refs: list[str] | None = None,
        baseline_refs: list[str] | None = None,
        character_qa: CharacterQAReport | None = None,
        rendered_asset_evaluation: RenderedAssetEvaluationReceipt | None = None,
        observed_motion_level: ObservedMotionLevel = ObservedMotionLevel.STANDARD,
    ) -> RenderQACompositeReport:
        ffprobe = self.ffprobe_from_adapter(
            adapter_report.ffprobe_validation,
            expected_width=promise_profile.expected_width,
            expected_height=promise_profile.expected_height,
        )
        frame_sampling = self.frame_sampling_from_adapter(adapter_report.frame_sampling)
        audio = self.audio_from_adapter(adapter_report.audio_level_analysis)
        captions = CaptionBurnCheckReceipt(
            file_ref=adapter_report.file_ref,
            captions_required=promise_profile.captions_required,
            captions_detected=captions_pass,
            burned_caption_detected=captions_pass,
        )
        visual = VisualRegressionScreenshotReceipt(
            file_ref=adapter_report.file_ref,
            screenshot_refs=screenshot_refs or ["adapter://synthetic-frame-sample"],
            baseline_refs=baseline_refs or ["adapter://synthetic-baseline"],
            observed_max_drift=0.0,
        )
        motion = MotionDowngradeBlocker(
            file_ref=adapter_report.file_ref,
            promised_motion_level=promise_profile.promised_motion_level,
            observed_motion_level=observed_motion_level,
            motion_required=promise_profile.motion_required,
        )
        delivery = self.delivery_from_adapter_duration(
            file_ref=adapter_report.file_ref,
            promise_profile=promise_profile,
            duration_tolerance=adapter_report.duration_tolerance,
            actual_width=adapter_report.ffprobe_validation.width,
            actual_height=adapter_report.ffprobe_validation.height,
            captions_pass=captions.pass_status != "fail",
            motion_pass=motion.pass_status != "fail",
        )
        return RenderQACompositeReport(
            file_ref=adapter_report.file_ref,
            ffprobe_validation=ffprobe,
            frame_sampling=frame_sampling,
            audio_level_analysis=audio,
            caption_burn_check=captions,
            visual_regression=visual,
            character_qa=character_qa,
            motion_downgrade=motion,
            delivery_promise=delivery,
            rendered_asset_evaluation=rendered_asset_evaluation,
        )
