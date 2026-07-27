from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.format_intelligence import EngineTarget, FormatId, PassStatus, StyleRoute


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class AdapterInputStatus(str):
    pass


class SuperVisualBuilderFormatAdapterInput(BaseModel):
    supervisual_builder_format_adapter_input_id: str = Field(default_factory=lambda: new_id("sv_format_input"))
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
    commander_verdict_id: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("SuperVisual adapter input requires source_span_refs")
        if self.engine_target != EngineTarget.SUPERVISUAL_ENGINE:
            raise ValueError("SuperVisual adapter input requires SUPERVISUAL_ENGINE target")


class CarouselEngineFormatAdapterInput(BaseModel):
    carousel_engine_format_adapter_input_id: str = Field(default_factory=lambda: new_id("carousel_format_input"))
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
    engine_target: EngineTarget = EngineTarget.CAROUSEL_ENGINE
    commander_verdict_id: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("Carousel adapter input requires source_span_refs")
        if not self.closure_contract_ref:
            raise ValueError("Carousel adapter input requires closure_contract_ref")
        indexes = [int(step.get("step_index", 0)) for step in self.sequence_steps]
        if indexes != list(range(1, len(indexes) + 1)):
            raise ValueError("Carousel adapter input requires continuous sequence step indexes")
        if self.engine_target != EngineTarget.CAROUSEL_ENGINE:
            raise ValueError("Carousel adapter input requires CAROUSEL_ENGINE target")


class FormatAdapterReceipt(BaseModel):
    format_adapter_receipt_id: str = Field(default_factory=lambda: new_id("format_adapter_receipt"))
    format_program_id: str
    adapter_input_id: str
    engine_target: EngineTarget
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)
