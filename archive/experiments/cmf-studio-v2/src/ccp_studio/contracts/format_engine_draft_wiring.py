from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.format_intelligence import EngineTarget, PassStatus
from ccp_studio.contracts.supervisual_carousel_format_adapters import (
    CarouselEngineFormatAdapterInput,
    SuperVisualBuilderFormatAdapterInput,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class DraftWiringStatus(str, Enum):
    DRAFT_READY = "draft_ready"
    BLOCKED = "blocked"


class SuperVisualDraftState(BaseModel):
    supervisual_draft_state_id: str = Field(default_factory=lambda: new_id("sv_draft"))
    brand_id: str
    brand_context_version_id: str
    format_program_id: str
    source_extraction_packet_id: str
    source_span_refs: list[str]
    single_source_truth_ref: str
    visual_hook_ref: str
    edge_product_ref: str
    composition_grammar: dict[str, Any]
    layer_stack: dict[str, Any]
    style_routes_allowed: list[str]
    style_routes_forbidden: list[str] = Field(default_factory=list)
    negative_space_policy: str
    frame_profile: str
    eval_gates: list[str]
    render_requirement: dict[str, Any]
    engine_target: EngineTarget = EngineTarget.SUPERVISUAL_ENGINE
    status: DraftWiringStatus = DraftWiringStatus.DRAFT_READY
    provider_calls_executed: bool = False
    render_executed: bool = False
    next_recommended_step: str = "visual_preproduction_from_supervisual_format_draft"
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.source_span_refs:
            raise ValueError("SuperVisualDraftState requires source_span_refs")
        if self.engine_target != EngineTarget.SUPERVISUAL_ENGINE:
            raise ValueError("SuperVisualDraftState requires SUPERVISUAL_ENGINE")
        if self.provider_calls_executed or self.render_executed:
            raise ValueError("Draft wiring must not execute providers or render")


class CarouselDraftVariantState(BaseModel):
    carousel_draft_variant_state_id: str = Field(default_factory=lambda: new_id("carousel_draft"))
    brand_id: str
    brand_context_version_id: str
    format_program_id: str
    source_extraction_packet_id: str
    source_span_refs: list[str]
    carousel_thesis_ref: str
    sequence_steps: list[dict[str, Any]]
    closure_contract_ref: str
    composition_grammar: dict[str, Any]
    layer_stack: dict[str, Any]
    style_routes_allowed: list[str]
    style_routes_forbidden: list[str] = Field(default_factory=list)
    frame_profile: str
    eval_gates: list[str]
    render_requirement: dict[str, Any]
    slide_count_hint: int
    engine_target: EngineTarget = EngineTarget.CAROUSEL_ENGINE
    status: DraftWiringStatus = DraftWiringStatus.DRAFT_READY
    provider_calls_executed: bool = False
    render_executed: bool = False
    next_recommended_step: str = "carousel_sequence_planning_from_format_draft"
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.source_span_refs:
            raise ValueError("CarouselDraftVariantState requires source_span_refs")
        if not self.closure_contract_ref:
            raise ValueError("CarouselDraftVariantState requires closure_contract_ref")
        if self.engine_target != EngineTarget.CAROUSEL_ENGINE:
            raise ValueError("CarouselDraftVariantState requires CAROUSEL_ENGINE")
        indexes = [int(step.get("step_index", 0)) for step in self.sequence_steps]
        if indexes != list(range(1, len(indexes) + 1)):
            raise ValueError("CarouselDraftVariantState requires continuous sequence step indexes")
        if self.provider_calls_executed or self.render_executed:
            raise ValueError("Draft wiring must not execute providers or render")


class FormatEngineDraftWiringReceipt(BaseModel):
    format_engine_draft_wiring_receipt_id: str = Field(default_factory=lambda: new_id("draft_wiring_receipt"))
    adapter_input_id: str
    draft_state_id: str
    engine_target: EngineTarget
    pass_status: PassStatus = PassStatus.PASS
    provider_calls_executed: bool = False
    render_executed: bool = False
    blockers: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed or self.render_executed:
            raise ValueError("Draft wiring receipt cannot indicate provider/render execution")
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("Receipt with blockers cannot pass")


class FormatEngineDraftWiringBatchResult(BaseModel):
    format_engine_draft_wiring_batch_result_id: str = Field(default_factory=lambda: new_id("draft_batch"))
    supervisual_drafts: list[SuperVisualDraftState] = Field(default_factory=list)
    carousel_drafts: list[CarouselDraftVariantState] = Field(default_factory=list)
    receipts: list[FormatEngineDraftWiringReceipt] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)
