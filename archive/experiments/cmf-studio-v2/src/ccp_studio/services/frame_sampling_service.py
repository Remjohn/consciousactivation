from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import FrameSamplingReceipt


class FrameSamplingService:
    def compile_receipt(
        self,
        *,
        file_ref: str,
        sampled_frame_count: int,
        expected_scene_count: int,
        black_frame_count: int = 0,
        broken_text_detected: bool = False,
        character_drift_detected: bool = False,
    ) -> FrameSamplingReceipt:
        return FrameSamplingReceipt(
            file_ref=file_ref,
            sampled_frame_count=sampled_frame_count,
            expected_scene_count=expected_scene_count,
            black_frame_count=black_frame_count,
            broken_text_detected=broken_text_detected,
            character_drift_detected=character_drift_detected,
        )
