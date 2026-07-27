from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
import hashlib
import base64

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def svg_to_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


class TemplateFormat(str, Enum):
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"
    FORMAT02_SCENE = "format02_scene"


class TemplateApprovalStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


class PreviewStatus(str, Enum):
    COMPILED = "compiled"
    BLOCKED = "blocked"


class PreviewRenderMode(str, Enum):
    STATIC_SVG = "static_svg"
    THUMBNAIL_ONLY = "thumbnail_only"


class FrameProfile(str, Enum):
    ONE_ONE_SOFT_ROUNDED = "1:1_SOFT_ROUNDED_EDITORIAL"
    FOUR_FIVE_CAROUSEL = "4:5_CAROUSEL_SLIDE"
    NINE_SIXTEEN_PAPERCUT = "9:16_PAPERCUT_EXPLAINER"


class TemplateSlotRole(str, Enum):
    SOURCE_TRUTH = "source_truth"
    HERO_OBJECT = "hero_object"
    POWER_PHRASE = "power_phrase"
    BRAND_MARK = "brand_mark"
    NEGATIVE_SPACE = "negative_space"
    CAROUSEL_THESIS = "carousel_thesis"
    CLOSURE_CONTRACT = "closure_contract"
    SLIDE_SEQUENCE = "slide_sequence"
    CONCEPT_STATEMENT = "concept_statement"
    HEADLINE_TEXT = "headline_text"
    AVATAR_ACTION = "avatar_action"
    AUDIENCE_PROXY = "audience_proxy"
    SFL_FUNCTION = "sfl_function"


class TemplateSlot(BaseModel):
    slot_id: str = Field(default_factory=lambda: new_id("slot"))
    slot_key: str
    role: TemplateSlotRole
    label: str
    required: bool = True
    description: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.slot_key:
            raise ValueError("TemplateSlot requires slot_key")
        if not self.label:
            raise ValueError("TemplateSlot requires label")


class TemplateSlotMap(BaseModel):
    template_slot_map_id: str = Field(default_factory=lambda: new_id("slot_map"))
    template_id: str
    template_format: TemplateFormat
    frame_profile: FrameProfile
    slots: list[TemplateSlot]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.template_id:
            raise ValueError("TemplateSlotMap requires template_id")
        if not self.slots:
            raise ValueError("TemplateSlotMap requires slots")
        keys = [slot.slot_key for slot in self.slots]
        if len(keys) != len(set(keys)):
            raise ValueError("TemplateSlotMap cannot contain duplicate slot keys")


class TemplateSamplePayload(BaseModel):
    template_sample_payload_id: str = Field(default_factory=lambda: new_id("sample_payload"))
    template_format: TemplateFormat
    values: dict[str, Any]
    source: str = "fixture"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.values:
            raise ValueError("TemplateSamplePayload requires values")

    def assert_satisfies(self, slot_map: TemplateSlotMap) -> None:
        missing = [slot.slot_key for slot in slot_map.slots if slot.required and slot.slot_key not in self.values]
        if missing:
            raise ValueError(f"Sample payload missing required slots: {missing}")
        if self.template_format != slot_map.template_format:
            raise ValueError("Sample payload format does not match slot map format")


class TemplatePreviewRequest(BaseModel):
    template_preview_request_id: str = Field(default_factory=lambda: new_id("preview_req"))
    template_id: str
    template_format: TemplateFormat
    slot_map: TemplateSlotMap
    sample_payload: TemplateSamplePayload
    preview_mode: PreviewRenderMode = PreviewRenderMode.STATIC_SVG
    provider_calls_allowed: bool = False
    renderer_calls_allowed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_allowed or self.renderer_calls_allowed:
            raise ValueError("Template preview V1 cannot call providers or renderers")
        if self.template_format != self.slot_map.template_format:
            raise ValueError("Preview request format must match slot map")
        self.sample_payload.assert_satisfies(self.slot_map)


class TemplatePreviewResult(BaseModel):
    template_preview_result_id: str = Field(default_factory=lambda: new_id("preview_result"))
    template_id: str
    template_format: TemplateFormat
    frame_profile: FrameProfile
    slot_labels: dict[str, str]
    sample_values: dict[str, Any]
    preview_svg: str
    thumbnail_uri: str
    status: PreviewStatus = PreviewStatus.COMPILED
    blockers: list[str] = Field(default_factory=list)
    provider_calls_executed: bool = False
    renderer_calls_executed: bool = False
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.status == PreviewStatus.COMPILED:
            raise ValueError("Compiled preview cannot have blockers")
        if not self.preview_svg.strip().startswith("<svg"):
            raise ValueError("TemplatePreviewResult requires SVG preview")
        if not self.thumbnail_uri.startswith("data:image/svg+xml;base64,"):
            raise ValueError("TemplatePreviewResult requires SVG data URI thumbnail")
        if self.provider_calls_executed or self.renderer_calls_executed:
            raise ValueError("Template preview result must not execute providers or renderers")


class SuperVisualTemplatePreview(TemplatePreviewResult):
    single_source_truth: str
    hero_object_label: str
    power_phrase: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.template_format != TemplateFormat.SUPERVISUAL:
            raise ValueError("SuperVisualTemplatePreview requires template_format=supervisual")
        if not self.single_source_truth:
            raise ValueError("SuperVisual preview requires one source truth")


class CarouselSlidePreview(BaseModel):
    slide_index: int = Field(ge=1)
    role: str
    headline: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.role or not self.headline:
            raise ValueError("CarouselSlidePreview requires role and headline")


class CarouselTemplatePreview(TemplatePreviewResult):
    carousel_thesis: str
    closure_contract: str
    slides: list[CarouselSlidePreview]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.template_format != TemplateFormat.CAROUSEL:
            raise ValueError("CarouselTemplatePreview requires template_format=carousel")
        if not self.slides:
            raise ValueError("Carousel preview requires slides")
        indexes = [slide.slide_index for slide in self.slides]
        if indexes != list(range(1, len(indexes) + 1)):
            raise ValueError("Carousel slide indexes must be continuous")


class Format02SceneTemplatePreview(TemplatePreviewResult):
    concept_statement: str
    headline_text: str
    avatar_action: str
    hero_object: str
    audience_proxy: str
    sfl_function: str
    max_visible_words: int = 14

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.template_format != TemplateFormat.FORMAT02_SCENE:
            raise ValueError("Format02SceneTemplatePreview requires template_format=format02_scene")
        if len(self.headline_text.split()) > self.max_visible_words:
            raise ValueError("Format 02 preview headline exceeds visible word budget")
        if not self.sfl_function:
            raise ValueError("Format 02 preview requires SFL function")


class TemplateVersion(BaseModel):
    template_version_id: str = Field(default_factory=lambda: new_id("template_version"))
    template_id: str
    version: int = Field(ge=1)
    template_format: TemplateFormat
    slot_map: TemplateSlotMap
    template_hash: str
    preview_result_id: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.template_hash:
            raise ValueError("TemplateVersion requires template_hash")
        if self.slot_map.template_format != self.template_format:
            raise ValueError("TemplateVersion format must match slot map")


class TemplateApprovalReceipt(BaseModel):
    template_approval_receipt_id: str = Field(default_factory=lambda: new_id("template_approval"))
    template_id: str
    template_version_id: str
    approval_status: TemplateApprovalStatus
    approved_by: str | None = None
    blockers: list[str] = Field(default_factory=list)
    notes: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.approval_status == TemplateApprovalStatus.APPROVED:
            raise ValueError("Template cannot be approved with blockers")
        if self.approval_status == TemplateApprovalStatus.APPROVED and not self.approved_by:
            raise ValueError("Approved template requires approved_by")


class TemplateAtlas(BaseModel):
    template_atlas_id: str = Field(default_factory=lambda: new_id("template_atlas"))
    atlas_name: str
    template_versions: list[TemplateVersion] = Field(default_factory=list)
    preview_results: list[TemplatePreviewResult] = Field(default_factory=list)
    approval_receipts: list[TemplateApprovalReceipt] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.atlas_name:
            raise ValueError("TemplateAtlas requires atlas_name")
        version_ids = [version.template_version_id for version in self.template_versions]
        if len(version_ids) != len(set(version_ids)):
            raise ValueError("TemplateAtlas cannot contain duplicate template versions")
