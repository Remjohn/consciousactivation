"""SuperVisual grammar contracts for TS-CMF-134."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.asset_program_compilers import PrimitiveTriadContract, compiler_hash
from ccp_studio.contracts.orchestration import utc_now


SuperVisualSubtype = Literal["SPV-CON", "SPV-SYM", "SPV-PRM"]


class SuperVisualGrammarRecord(BaseModel):
    schema_version: Literal["cmf.supervisual_grammar_record.v1"] = "cmf.supervisual_grammar_record.v1"
    supervisual_grammar_record_id: UUID = Field(default_factory=uuid4)
    grammar_code: str = Field(min_length=1)
    subtype: SuperVisualSubtype
    display_name: str = Field(min_length=1)
    composition_purpose: str = Field(min_length=1)
    required_zones: list[str] = Field(min_length=1)
    required_contrast_axes: list[str] = Field(default_factory=list)
    symbol_explanation_required: bool = False
    authority_evidence_required: bool = False
    skia_scene_obligations: list[str] = Field(min_length=1)
    primitive_triads: list[PrimitiveTriadContract] = Field(min_length=3)

    @model_validator(mode="after")
    def _subtype_obligations(self) -> "SuperVisualGrammarRecord":
        if self.subtype == "SPV-CON" and not self.required_contrast_axes:
            raise ValueError("conceptual contrast SuperVisuals require contrast axes")
        if self.subtype == "SPV-SYM" and not self.symbol_explanation_required:
            raise ValueError("symbolic SuperVisuals must require symbol explanation")
        if self.subtype == "SPV-PRM" and not self.authority_evidence_required:
            raise ValueError("proof/authority SuperVisuals must require authority evidence")
        return self


class SuperVisualFeelMatrixEntry(BaseModel):
    schema_version: Literal["cmf.supervisual_feel_matrix_entry.v1"] = "cmf.supervisual_feel_matrix_entry.v1"
    subtype: SuperVisualSubtype
    required_feel: str = Field(min_length=1)
    must_avoid: list[str] = Field(min_length=1)
    minimum_primitive_score: float = Field(ge=0, le=1)


class SuperVisualGrammarRouteRequest(BaseModel):
    schema_version: Literal["cmf.supervisual_grammar_route_request.v1"] = "cmf.supervisual_grammar_route_request.v1"
    supervisual_grammar_route_request_id: UUID = Field(default_factory=uuid4)
    program_ref: str = Field(min_length=1)
    brand_context_ref: str = Field(min_length=1)
    archetype_ref: str = Field(min_length=1)
    target_subtype_hint: SuperVisualSubtype | None = None
    platform: Literal["instagram", "linkedin", "youtube_shorts", "x"]
    source_evidence_refs: list[str] = Field(min_length=1)


class SuperVisualGrammarRouteDecision(BaseModel):
    schema_version: Literal["cmf.supervisual_grammar_route_decision.v1"] = "cmf.supervisual_grammar_route_decision.v1"
    supervisual_grammar_route_decision_id: UUID = Field(default_factory=uuid4)
    route_request_id: UUID
    selected_grammar_code: str = Field(min_length=1)
    selected_subtype: SuperVisualSubtype
    primitive_coverage_ids: list[str] = Field(min_length=3)
    feel_matrix_ref: str = Field(min_length=1)
    skia_scene_obligation_refs: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualPrimitiveCoverageReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_primitive_coverage_receipt.v1"] = "cmf.supervisual_primitive_coverage_receipt.v1"
    supervisual_primitive_coverage_receipt_id: UUID = Field(default_factory=uuid4)
    route_decision_id: UUID
    primitive_score: float = Field(ge=0, le=1)
    role_coverage: dict[str, bool] = Field(default_factory=dict)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


def supervisual_hash(parts: object) -> str:
    return compiler_hash(parts)
