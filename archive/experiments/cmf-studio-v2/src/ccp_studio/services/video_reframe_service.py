from __future__ import annotations

from ccp_studio.contracts.video_editing_engine import (
    FaceSafeZoneReceipt,
    PassStatus,
    SquareSoftCardPlan,
    TalkingHeadTrackingPlan,
    VerticalReframePlan,
    VideoFrameProfile,
)


class VideoReframeService:
    def compile_vertical_reframe(self, source_media_id: str, target_frame_profile: VideoFrameProfile) -> VerticalReframePlan:
        return VerticalReframePlan(source_media_id=source_media_id, target_frame_profile=target_frame_profile)

    def compile_square_soft_card(self, source_media_id: str) -> SquareSoftCardPlan:
        return SquareSoftCardPlan(source_media_id=source_media_id)

    def evaluate_face_safe_zone(self, *, eyes_cropped: bool = False, mouth_cropped: bool = False) -> FaceSafeZoneReceipt:
        return FaceSafeZoneReceipt(pass_status=PassStatus.FAIL if eyes_cropped or mouth_cropped else PassStatus.PASS, eyes_cropped=eyes_cropped, mouth_cropped=mouth_cropped)
