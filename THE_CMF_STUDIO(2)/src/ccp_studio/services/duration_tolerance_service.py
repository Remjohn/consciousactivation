from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import DurationToleranceReceipt


class DurationToleranceService:
    def compile_receipt(
        self,
        *,
        expected_duration_ms: int,
        actual_duration_ms: int,
        tolerance_ms: int = 500,
    ) -> DurationToleranceReceipt:
        return DurationToleranceReceipt(
            expected_duration_ms=expected_duration_ms,
            actual_duration_ms=actual_duration_ms,
            tolerance_ms=tolerance_ms,
        )
