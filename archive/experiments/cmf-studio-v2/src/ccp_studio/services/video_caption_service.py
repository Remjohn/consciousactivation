from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import CaptionCue, CaptionTrack


class VideoCaptionService:
    def compile_caption_track(self, cues: list[CaptionCue], *, collision_with_face: bool = False, collision_with_proof_object: bool = False) -> CaptionTrack:
        return CaptionTrack(cues=cues, collision_with_face=collision_with_face, collision_with_proof_object=collision_with_proof_object)
