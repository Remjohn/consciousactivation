from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import AudioLevelAnalysisReceipt


class AudioLevelAnalysisService:
    def compile_receipt(
        self,
        *,
        file_ref: str,
        integrated_lufs: float,
        true_peak_db: float,
    ) -> AudioLevelAnalysisReceipt:
        return AudioLevelAnalysisReceipt(
            file_ref=file_ref,
            integrated_lufs=integrated_lufs,
            true_peak_db=true_peak_db,
        )
