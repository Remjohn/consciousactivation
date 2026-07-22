from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import TextRevealTrack


class VideoTextRevealService:
    def compile_text_reveal_track(self, reveal_refs: list[str]) -> TextRevealTrack:
        return TextRevealTrack(reveal_refs=reveal_refs, reveal_order=reveal_refs)
