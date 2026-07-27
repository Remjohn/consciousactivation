"""Frame profiles for delivery and source-only media.

16:9 is explicitly source-only for the current short-form production system.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class FrameProfileCode(str, Enum):
    vertical_full = "9:16_FULL_VERTICAL"
    vertical_split_reaction = "9:16_SPLIT_REACTION"
    vertical_papercut_explainer = "9:16_PAPERCUT_EXPLAINER"
    square_soft_rounded_editorial = "1:1_SOFT_ROUNDED_EDITORIAL"
    square_proof_card = "1:1_PROOF_CARD"
    square_cinematic_card = "1:1_CINEMATIC_CARD"
    feed_poster = "4:5_FEED_POSTER"
    carousel_slide = "4:5_CAROUSEL_SLIDE"
    source_interview_16_9 = "16:9_SOURCE_INTERVIEW"
    source_broll_reference_16_9 = "16:9_SOURCE_BROLL_REFERENCE"
    raw_archive_16_9 = "16:9_RAW_ARCHIVE"


class FrameDeliveryMode(str, Enum):
    delivery = "delivery"
    source_only = "source_only"
    intermediate = "intermediate"


class FrameProfileKind(str, Enum):
    source = "source"
    delivery = "delivery"
    intermediate = "intermediate"


class InnerFrameSpec(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    corner_radius: int = Field(default=0, ge=0)
    shadow_blur: int = Field(default=0, ge=0)
    shadow_opacity: float = Field(default=0.0, ge=0, le=1)
    shadow_offset_y: int = 0


class CaptionPolicy(BaseModel):
    placement: str = Field(min_length=1)
    max_lines: int = Field(default=3, ge=0)
    tone: str = Field(default="platform_native")


class MotionPolicy(BaseModel):
    camera_motion: str = Field(default="hold")
    max_motion_intensity: Literal["none", "low", "medium_low", "medium", "high"] = "medium"
    no_chaotic_overlays: bool = True


class FrameProfile(BaseModel):
    schema_version: Literal["cmf.frame_profile.v1"] = "cmf.frame_profile.v1"
    frame_profile_id: UUID = Field(default_factory=uuid4)
    code: FrameProfileCode
    display_name: str = Field(min_length=1)
    delivery_mode: FrameDeliveryMode
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    inner_frame: InnerFrameSpec | None = None
    caption_policy: CaptionPolicy
    motion_policy: MotionPolicy = Field(default_factory=MotionPolicy)
    compatible_output_classes: list[str] = Field(default_factory=list)
    invariants: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def source_profiles_are_not_delivery(self):
        if self.code.value.startswith("16:9") and self.delivery_mode == FrameDeliveryMode.delivery:
            raise ValueError("16:9 profiles are source-only or intermediate, not short-form delivery")
        if "SOFT_ROUNDED" in self.code.value and (self.inner_frame is None or self.inner_frame.corner_radius <= 0):
            raise ValueError("soft-rounded profiles require an inner_frame with positive corner_radius")
        return self


DEFAULT_FRAME_PROFILES: list[FrameProfile] = [
    FrameProfile(
        code=FrameProfileCode.vertical_full,
        display_name="Full Vertical Social Video",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1920,
        caption_policy=CaptionPolicy(placement="lower_safe_zone", max_lines=3, tone="mobile_direct"),
        compatible_output_classes=["video", "paper_cut_explainer", "talking_head"],
        invariants=["primary short-form vertical delivery profile"],
    ),
    FrameProfile(
        code=FrameProfileCode.vertical_split_reaction,
        display_name="Vertical Split Reaction",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1920,
        caption_policy=CaptionPolicy(placement="between_ui_and_reaction_or_lower", max_lines=3, tone="reaction_native"),
        compatible_output_classes=["reaction_video", "poll", "ranking", "debate"],
    ),
    FrameProfile(
        code=FrameProfileCode.vertical_papercut_explainer,
        display_name="9:16 PaperCut Explainer",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1920,
        caption_policy=CaptionPolicy(placement="lower_teaching_safe_zone", max_lines=3, tone="educational"),
        motion_policy=MotionPolicy(camera_motion="layered_paper_parallax", max_motion_intensity="medium_low", no_chaotic_overlays=True),
        compatible_output_classes=["paper_cut_explainer", "animated_avatar", "educational_video"],
    ),
    FrameProfile(
        code=FrameProfileCode.square_soft_rounded_editorial,
        display_name="Square Soft-Rounded Editorial Card",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1080,
        inner_frame=InnerFrameSpec(x=54, y=54, width=972, height=972, corner_radius=44, shadow_blur=24, shadow_opacity=0.18, shadow_offset_y=10),
        caption_policy=CaptionPolicy(placement="inside_bottom_or_below_card", max_lines=3, tone="premium_editorial"),
        motion_policy=MotionPolicy(camera_motion="slow_push_or_hold", max_motion_intensity="medium_low", no_chaotic_overlays=True),
        compatible_output_classes=["cinematic_card", "proof_card", "quote_card", "premium_short"],
    ),
    FrameProfile(
        code=FrameProfileCode.square_proof_card,
        display_name="Square Proof Card",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1080,
        inner_frame=InnerFrameSpec(x=44, y=44, width=992, height=992, corner_radius=18, shadow_blur=18, shadow_opacity=0.16, shadow_offset_y=8),
        caption_policy=CaptionPolicy(placement="proof_card_integrated", max_lines=2, tone="proof"),
        motion_policy=MotionPolicy(camera_motion="hold", max_motion_intensity="low", no_chaotic_overlays=True),
        compatible_output_classes=["proof_card", "quote_card", "documentary_social_card"],
    ),
    FrameProfile(
        code=FrameProfileCode.feed_poster,
        display_name="4:5 Feed Poster",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1350,
        caption_policy=CaptionPolicy(placement="poster_integrated", max_lines=0, tone="poster"),
        compatible_output_classes=["supervisual", "single_image", "feed_post"],
    ),
    FrameProfile(
        code=FrameProfileCode.carousel_slide,
        display_name="4:5 Carousel Slide",
        delivery_mode=FrameDeliveryMode.delivery,
        width=1080,
        height=1350,
        caption_policy=CaptionPolicy(placement="slide_integrated", max_lines=0, tone="carousel"),
        compatible_output_classes=["carousel_slide"],
    ),
    FrameProfile(
        code=FrameProfileCode.source_interview_16_9,
        display_name="16:9 Source Interview",
        delivery_mode=FrameDeliveryMode.source_only,
        width=1920,
        height=1080,
        caption_policy=CaptionPolicy(placement="none", max_lines=0, tone="source"),
        compatible_output_classes=["source_media"],
        invariants=["source-only; must be recomposed before short-form delivery"],
    ),
]
