"""SVRE/Aurore visual asset research contracts for TS-CMF-049."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class CandidateUseMode(str, Enum):
    direct_use = "direct_use"
    composition_reference_only = "composition_reference_only"
    blocked = "blocked"


class LicenseTier(str, Enum):
    owned = "owned"
    public_domain = "public_domain"
    royalty_free = "royalty_free"
    editorial_review = "editorial_review"
    unknown = "unknown"
    restricted = "restricted"


class VisualResearchQuery(BaseModel):
    schema_version: Literal["cmf.visual_research_query.v1"]
    visual_research_query_id: UUID
    scene_spec_id: UUID
    asset_roll_role: str = Field(min_length=1)
    emotional_state: str = Field(min_length=1)
    symbolic_role: str = Field(min_length=1)
    contradiction_value: str | None = None
    brand_alignment_constraints: list[str] = Field(min_length=1)
    source_constraints: list[str] = Field(min_length=1)
    licensing_requirements: list[str] = Field(min_length=1)
    query_terms: list[str] = Field(min_length=1)
    known_person_name: str | None = None
    legacy_adapter_route: str = Field(min_length=1)
    created_at: datetime


class LicensingDecision(BaseModel):
    schema_version: Literal["cmf.licensing_decision.v1"]
    licensing_decision_id: UUID
    visual_research_query_id: UUID
    source_url_or_ref: str = Field(min_length=1)
    license_tier: LicenseTier
    direct_use_allowed: bool
    composition_reference_allowed: bool
    attribution_required: bool
    provenance_ready: bool
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    decided_at: datetime

    @model_validator(mode="after")
    def direct_use_requires_provenance(self):
        if self.direct_use_allowed and not self.provenance_ready:
            raise ValueError("direct use requires provenance")
        return self


class VisualCandidateScore(BaseModel):
    schema_version: Literal["cmf.visual_candidate_score.v1"]
    score_id: UUID
    visual_research_query_id: UUID
    emotional_mode_match: float = Field(ge=0, le=1)
    tribal_cultural_proximity: float = Field(ge=0, le=1)
    symbolic_role_fit: float = Field(ge=0, le=1)
    visual_congruence: float = Field(ge=0, le=1)
    authenticity: float = Field(ge=0, le=1)
    source_quality: float = Field(ge=0, le=1)
    brand_alignment: float = Field(ge=0, le=1)
    known_person_validity: float | None = Field(default=None, ge=0, le=1)
    source_win_rate: float = Field(ge=0, le=1)
    total_score: float = Field(ge=0, le=1)
    scoring_rationale: str = Field(min_length=1)
    created_at: datetime


class VisualCandidate(BaseModel):
    schema_version: Literal["cmf.visual_candidate.v1"]
    visual_candidate_id: UUID
    visual_research_query_id: UUID
    source_url_or_ref: str = Field(min_length=1)
    candidate_uri: str | None = None
    provenance_summary: str = Field(min_length=1)
    use_mode: CandidateUseMode
    license_decision_id: UUID
    score_id: UUID
    provider_route: str = Field(min_length=1)
    superseded_legacy_logic_refs: list[str] = Field(default_factory=list)
    selected: bool = False
    created_at: datetime


class AssetResearchManifest(BaseModel):
    schema_version: Literal["cmf.asset_research_manifest.v1"]
    asset_research_manifest_id: UUID
    visual_research_query_id: UUID
    scene_spec_id: UUID
    asset_roll_role: str = Field(min_length=1)
    selected_candidate_id: UUID
    alternative_candidate_ids: list[UUID] = Field(default_factory=list)
    rejected_candidate_reasons: dict[str, str] = Field(default_factory=dict)
    selected_use_mode: CandidateUseMode
    downstream_render_route: str = Field(min_length=1)
    scoring_receipt_refs: list[UUID] = Field(default_factory=list)
    license_decision_refs: list[UUID] = Field(default_factory=list)
    manifest_hash: str = Field(min_length=1)
    written_at: datetime


class ImageResolutionMap(BaseModel):
    schema_version: Literal["cmf.image_resolution_map.v1"]
    image_resolution_map_id: UUID
    asset_research_manifest_id: UUID
    selected_candidate_id: UUID
    selected_use_mode: CandidateUseMode
    source_url_or_ref: str = Field(min_length=1)
    direct_use_asset_uri: str | None = None
    composition_reference_uri: str | None = None
    downstream_render_route: str = Field(min_length=1)
    provider_route: str = Field(min_length=1)
    resolution_steps: list[str] = Field(min_length=1)
    map_hash: str = Field(min_length=1)
    created_at: datetime


class AssetResearchReceipt(BaseModel):
    schema_version: Literal["cmf.asset_research_receipt.v1"]
    asset_research_receipt_id: UUID
    visual_research_query_id: UUID
    candidate_ids: list[UUID] = Field(min_length=1)
    score_ids: list[UUID] = Field(min_length=1)
    license_decision_ids: list[UUID] = Field(min_length=1)
    selected_candidate_id: UUID
    rejected_candidate_reasons: dict[str, str] = Field(default_factory=dict)
    asset_research_manifest_id: UUID
    image_resolution_map_id: UUID
    legacy_adapter_route: str = Field(min_length=1)
    provider_routes: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


def visual_research_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_asset_research_receipt(
    *,
    query: VisualResearchQuery,
    candidates: list[VisualCandidate],
    scores: list[VisualCandidateScore],
    licenses: list[LicensingDecision],
    manifest: AssetResearchManifest,
    image_map: ImageResolutionMap,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    command_id: UUID | None = None,
) -> AssetResearchReceipt:
    payload = {
        "query": query.visual_research_query_id,
        "candidate_ids": [item.visual_candidate_id for item in candidates],
        "score_ids": [item.score_id for item in scores],
        "license_decision_ids": [item.licensing_decision_id for item in licenses],
        "manifest": manifest.asset_research_manifest_id,
        "image_map": image_map.image_resolution_map_id,
        "decision_code": decision_code,
    }
    return AssetResearchReceipt(
        schema_version="cmf.asset_research_receipt.v1",
        asset_research_receipt_id=uuid4(),
        visual_research_query_id=query.visual_research_query_id,
        candidate_ids=[item.visual_candidate_id for item in candidates],
        score_ids=[item.score_id for item in scores],
        license_decision_ids=[item.licensing_decision_id for item in licenses],
        selected_candidate_id=manifest.selected_candidate_id,
        rejected_candidate_reasons=manifest.rejected_candidate_reasons,
        asset_research_manifest_id=manifest.asset_research_manifest_id,
        image_resolution_map_id=image_map.image_resolution_map_id,
        legacy_adapter_route=query.legacy_adapter_route,
        provider_routes=sorted({item.provider_route for item in candidates}),
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        receipt_hash=visual_research_hash(payload),
        written_at=utc_now(),
    )
