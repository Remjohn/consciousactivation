from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import VideoMediaProbeReceipt, VideoSourceMedia


class VideoMediaProbeService:
    def probe(self, media: VideoSourceMedia) -> VideoMediaProbeReceipt:
        return VideoMediaProbeReceipt(
            source_media_id=media.source_media_id,
            duration_ms=media.duration_ms,
            width=media.width,
            height=media.height,
            fps=media.fps,
        )
