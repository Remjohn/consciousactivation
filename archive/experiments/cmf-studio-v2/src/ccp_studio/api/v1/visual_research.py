"""FastAPI adapter for TS-CMF-049 visual asset research."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.visual_research import (
    AssetResearchReceipt,
    LicensingDecision,
    VisualCandidate,
    VisualResearchQuery,
)
from ccp_studio.services.visual_research_service import VisualResearchService


router = APIRouter(prefix="/api/v1/visual-research", tags=["visual-research"])
_visual_research_service: VisualResearchService | None = None


class CreateVisualResearchQueryRequest(BaseModel):
    scene_spec_id: UUID
    asset_roll_role: str
    emotional_state: str
    symbolic_role: str
    contradiction_value: str | None = None
    brand_alignment_constraints: list[str]
    source_constraints: list[str]
    licensing_requirements: list[str]
    query_terms: list[str]
    actor_id: UUID
    known_person_name: str | None = None


class RecordLicensingDecisionRequest(BaseModel):
    visual_research_query_id: UUID
    source_url_or_ref: str
    license_tier: str
    provenance_summary: str
    actor_id: UUID
    direct_use_requested: bool = True
    attribution_required: bool = False
    evidence_refs: list[str] = Field(default_factory=list)


class ScoreVisualCandidateRequest(BaseModel):
    visual_research_query_id: UUID
    source_url_or_ref: str
    candidate_uri: str | None = None
    provenance_summary: str
    licensing_decision_id: UUID
    provider_route: str
    score_fields: dict[str, float | str]
    actor_id: UUID
    superseded_legacy_logic_refs: list[str] = Field(default_factory=list)


class RunAssetResearchRequest(BaseModel):
    visual_research_query_id: UUID
    candidates: list[dict[str, Any]]
    actor_id: UUID
    downstream_render_route: str


def set_visual_research_service(service: VisualResearchService) -> None:
    global _visual_research_service
    _visual_research_service = service


def get_visual_research_service() -> VisualResearchService:
    if _visual_research_service is None:
        raise RuntimeError("VisualResearchService must be configured by the application.")
    return _visual_research_service


@router.post("/queries", response_model=VisualResearchQuery)
def create_visual_research_query(
    request: CreateVisualResearchQueryRequest,
    service: VisualResearchService = Depends(get_visual_research_service),
) -> VisualResearchQuery:
    return service.create_visual_research_query(**request.model_dump())


@router.post("/licenses", response_model=LicensingDecision)
def record_licensing_decision(
    request: RecordLicensingDecisionRequest,
    service: VisualResearchService = Depends(get_visual_research_service),
) -> LicensingDecision:
    return service.record_licensing_decision(**request.model_dump())


@router.post("/candidates", response_model=VisualCandidate)
def score_visual_candidate(
    request: ScoreVisualCandidateRequest,
    service: VisualResearchService = Depends(get_visual_research_service),
) -> VisualCandidate:
    return service.score_visual_candidate(**request.model_dump())


@router.post("/runs", response_model=AssetResearchReceipt)
def run_asset_research(
    request: RunAssetResearchRequest,
    service: VisualResearchService = Depends(get_visual_research_service),
) -> AssetResearchReceipt:
    return service.run_asset_research(**request.model_dump())
