from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.format_intelligence import EngineAdapterPayload, FormatId


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class BridgeStatus(str, Enum):
    CREATED = "created"
    MAPPED = "mapped"
    COMPILED = "compiled"
    AUTHORIZED = "authorized"
    ADAPTED = "adapted"
    FAILED = "failed"


class NarrativePacketKind(str, Enum):
    FORMAT01 = "format01_story_extraction_packet"
    FORMAT02 = "format02_explainer_extraction_packet"
    FORMAT03 = "format03_reaction_extraction_packet"
    FORMAT04 = "format04_conscious_reaction_extraction_packet"
    SUPERVISUAL = "supervisual_extraction_packet"
    CAROUSEL = "carousel_extraction_packet"
    VIDEO = "video_extraction_packet"
    MEME = "meme_visual_extraction_packet"
    POLL = "poll_visual_extraction_packet"
    REACTION_SEED = "reaction_seed_packet"


class NarrativePacketBridgeRef(BaseModel):
    narrative_packet_bridge_ref_id: str = Field(default_factory=lambda: new_id("narr_packet_ref"))
    packet_kind: NarrativePacketKind
    packet_id: str
    target_format: FormatId
    source_span_refs: list[str]
    sub_format_hint: str | None = None
    extraction_payload: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.packet_id:
            raise ValueError("packet_id is required")
        if not self.source_span_refs:
            raise ValueError("NarrativePacketBridgeRef requires source_span_refs")


class NarrativeToFormatBridgeRequest(BaseModel):
    narrative_to_format_bridge_request_id: str = Field(default_factory=lambda: new_id("bridge_req"))
    brand_id: str
    brand_context_version_id: str
    source_extraction_run_id: str | None = None
    archetype_program_id: str | None = None
    primitive_coalition_candidate_id: str | None = None
    delivery_recipe_program_id: str | None = None
    packet_refs: list[NarrativePacketBridgeRef]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.packet_refs:
            raise ValueError("Bridge request requires packet_refs")


class FormatProgramCompileReceipt(BaseModel):
    format_program_compile_receipt_id: str = Field(default_factory=lambda: new_id("format_compile_receipt"))
    packet_id: str
    target_format: FormatId
    generic_extraction_packet_id: str
    format_program_id: str
    commander_verdict_id: str | None = None
    engine_adapter_payload_id: str | None = None
    status: BridgeStatus
    created_at: str = Field(default_factory=_now_iso)


class NarrativeToFormatBridgeReceipt(BaseModel):
    narrative_to_format_bridge_receipt_id: str = Field(default_factory=lambda: new_id("bridge_receipt"))
    request_id: str
    compile_receipts: list[FormatProgramCompileReceipt]
    engine_adapter_payloads: list[EngineAdapterPayload] = Field(default_factory=list)
    status: BridgeStatus
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.status not in {BridgeStatus.FAILED, BridgeStatus.COMPILED}:
            raise ValueError("Bridge blockers require failed/compiled status")
