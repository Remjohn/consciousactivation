from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import (
    FFmpegFinishJob,
    RemotionRenderJob,
)
from ccp_studio.services.remotion_render_adapter_service import RemotionRenderAdapterService
from ccp_studio.services.ffmpeg_finish_adapter_service import FFmpegFinishAdapterService


class RemotionFFmpegRenderOrchestratorService:
    def __init__(
        self,
        remotion_service: RemotionRenderAdapterService | None = None,
        ffmpeg_service: FFmpegFinishAdapterService | None = None,
    ):
        self.remotion = remotion_service or RemotionRenderAdapterService()
        self.ffmpeg = ffmpeg_service or FFmpegFinishAdapterService()

    def execute_dry_run_pipeline(self, *, remotion_job: RemotionRenderJob, ffmpeg_job: FFmpegFinishJob):
        remotion_result = self.remotion.execute_dry_run(remotion_job)
        ffmpeg_result = self.ffmpeg.execute_dry_run(ffmpeg_job)
        return {
            "remotion_result": remotion_result,
            "ffmpeg_result": ffmpeg_result,
        }
