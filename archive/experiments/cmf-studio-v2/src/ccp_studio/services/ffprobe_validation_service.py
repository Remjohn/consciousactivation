from __future__ import annotations

from ccp_studio.contracts.remotion_ffmpeg_render_adapter import FFprobeValidationReceipt


class FFprobeValidationService:
    def validate_from_metadata(self, *, file_ref: str, metadata: dict) -> FFprobeValidationReceipt:
        return FFprobeValidationReceipt(
            file_ref=file_ref,
            duration_ms=int(metadata["duration_ms"]),
            width=int(metadata["width"]),
            height=int(metadata["height"]),
            fps=float(metadata["fps"]),
            video_codec=str(metadata["video_codec"]),
            audio_codec=metadata.get("audio_codec"),
        )
