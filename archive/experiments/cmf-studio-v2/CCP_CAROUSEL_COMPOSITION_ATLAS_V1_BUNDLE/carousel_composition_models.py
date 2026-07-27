from __future__ import annotations

from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class CompositionFamily(str, Enum):
    HOOK_COVER = "hook_cover"
    NARRATIVE_EMOTION = "narrative_emotion"
    FRAMEWORK_EDUCATION = "framework_education"
    COMPARISON_JUXTAPOSITION = "comparison_juxtaposition"
    IDENTITY_BRAND = "identity_brand"
    CTA_CLOSING = "cta_closing"


class LayoutZone(BaseModel):
    id: str
    kind: str
    rect: tuple[float, float, float, float]
    required: bool = True
    align: str | None = None

    @field_validator("rect")
    @classmethod
    def rect_inside_canvas(cls, value: tuple[float, float, float, float]):
        x, y, width, height = value
        if min(value) < 0 or width <= 0 or height <= 0:
            raise ValueError("Rectangle values must be non-negative and dimensions positive")
        if x + width > 1.0001 or y + height > 1.0001:
            raise ValueError("Rectangle exceeds normalized canvas")
        return value


class TextBudget(BaseModel):
    headline_words: tuple[int, int]
    headline_lines: tuple[int, int]
    body_words: tuple[int, int]
    bullets: tuple[int, int] | None = None


class ToolRouting(BaseModel):
    ideogram_4: dict
    qwen_image_layered: dict
    sam3: dict
    rough_notation: dict
    skia: list[str]


class CanonicalCompositionSpec(BaseModel):
    composition_id: str
    name: str
    family: CompositionFamily
    summary: str
    semantic_roles: list[str]
    recommended_slide_positions: list[int]
    supported_aspect_ratios: list[Literal["1:1", "4:5", "3:4"]]
    attention_path: str
    zones: list[LayoutZone]
    text_budget: TextBudget
    visual_mode: str
    tool_routing: ToolRouting
    micro_semiotic_anchor_slots: list[str]
    source_references: list[str]
    avoid: list[str]


class SlideIntent(BaseModel):
    slide_index: int = Field(ge=1)
    semantic_role: str
    message: str
    evidence_ids: list[str] = Field(default_factory=list)
    visual_metaphor: str | None = None
    emotion: str | None = None
    desired_composition_family: CompositionFamily | None = None
    required_micro_semiotic_anchor_ids: list[str] = Field(default_factory=list)
    max_copy_words: int = Field(ge=1, le=140)


class AnnotationSpec(BaseModel):
    target_zone_id: str
    type: Literal["underline", "box", "circle", "highlight", "strike-through", "crossed-off", "brackets", "arrow"]
    semantic_reason: Literal["contrast", "emphasis", "rejection", "connection", "proof", "action"]
    color_token: str
    stroke_width: float = Field(gt=0, le=12)
    animation_order: int | None = None


class CarouselRenderContract(BaseModel):
    carousel_id: str
    brand_id: str
    brand_context_version_id: str
    registry_version: str
    canvas_width: int
    canvas_height: int
    composition_id: str
    slide_intent: SlideIntent
    resolved_copy: dict[str, str | list[str]]
    asset_bindings: dict[str, str]
    annotations: list[AnnotationSpec] = Field(default_factory=list)
    render_seed: int
    source_provenance: list[str]


class CarouselSequenceSpec(BaseModel):
    sequence_id: str
    name: str
    slide_count: int = Field(ge=2, le=20)
    slides: list[SlideIntent]
    continuity_tokens: dict[str, str | int | float | list[str]]
    diversity_constraints: dict[str, int | float | list[str]]
