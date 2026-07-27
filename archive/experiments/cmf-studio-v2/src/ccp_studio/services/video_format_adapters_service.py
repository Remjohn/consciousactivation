from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import VideoFormatId, VideoFormatProgramRef


class VideoFormatAdaptersService:
    def attach_format_program(self, *, format_program_id: str, format_id: VideoFormatId, source_span_refs: list[str]) -> VideoFormatProgramRef:
        return VideoFormatProgramRef(format_program_id=format_program_id, format_id=format_id, source_span_refs=source_span_refs)
