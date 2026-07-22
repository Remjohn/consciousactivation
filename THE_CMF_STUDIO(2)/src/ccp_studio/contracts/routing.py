"""Archetype and asset derivative routing contracts for TS-CMF-033."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class RouteDecision(str, Enum):
    accepted = "accepted"
    rejected_source_unsupported = "rejected_source_unsupported"
    rejected_unsupported_format = "rejected_unsupported_format"
    review_required = "review_required"


class RouteRegistryType(str, Enum):
    core_content_archetype = "core_content_archetype"
    asset_derivative = "asset_derivative"
    meme_mechanism = "meme_mechanism"
    reaction_archetype = "reaction_archetype"
    cmf_render_mode = "cmf_render_mode"


class RegistryRouteRefs(BaseModel):
    schema_version: Literal["cmf.registry_route_refs.v1"]
    core_content_archetype_ref: str = Field(min_length=1)
    asset_derivative_ref: str | None = None
    meme_mechanism_ref: str | None = None
    reaction_archetype_ref: str | None = None
    cmf_render_mode_ref: str = Field(min_length=1)
    registry_bundle_version: str = Field(min_length=1)

    def all_refs(self) -> list[str]:
        return [
            item
            for item in [
                self.core_content_archetype_ref,
                self.asset_derivative_ref,
                self.meme_mechanism_ref,
                self.reaction_archetype_ref,
                self.cmf_render_mode_ref,
            ]
            if item
        ]


class RouteSelectionCandidate(BaseModel):
    schema_version: Literal["cmf.route_selection_candidate.v1"]
    route_selection_candidate_id: UUID
    expression_moment_id: UUID
    requested_format: str | None = None
    route_refs: RegistryRouteRefs
    source_support_evidence: list[str] = Field(min_length=1)
    route_rationale: str = Field(min_length=1)
    route_fit_score: float = Field(ge=0, le=1)
    failure_alternatives: list[str] = Field(default_factory=list)


class ArchetypeRoute(BaseModel):
    schema_version: Literal["cmf.archetype_route.v1"]
    archetype_route_id: UUID
    expression_moment_id: UUID
    route_refs: RegistryRouteRefs
    source_support_evidence: list[str] = Field(min_length=1)
    route_rationale: str = Field(min_length=1)
    route_fit_score: float = Field(ge=0, le=1)
    failure_alternatives: list[str] = Field(default_factory=list)
    decision: RouteDecision
    created_at: datetime


class UnsupportedFormatRejection(BaseModel):
    schema_version: Literal["cmf.unsupported_format_rejection.v1"]
    unsupported_format_rejection_id: UUID
    expression_moment_id: UUID
    requested_format: str = Field(min_length=1)
    decision: RouteDecision
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    rejected_at: datetime


class AssetRouteReceipt(BaseModel):
    schema_version: Literal["cmf.asset_route_receipt.v1"]
    asset_route_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_moment_id: UUID
    requested_format: str | None = None
    accepted_route_ids: list[UUID] = Field(default_factory=list)
    rejected_route_ids: list[UUID] = Field(default_factory=list)
    unsupported_format_rejection_ids: list[UUID] = Field(default_factory=list)
    registry_bundle_version: str = Field(min_length=1)
    registry_entry_refs: list[str] = Field(default_factory=list)
    source_support_evidence: list[str] = Field(default_factory=list)
    route_rationale: str = Field(min_length=1)
    route_fit_score: float = Field(ge=0, le=1)
    failure_alternatives: list[str] = Field(default_factory=list)
    evaluator_summary: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    package_planning_refs: list[str] = Field(default_factory=list)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def registry_bundle_version_for(refs: list[str]) -> str:
    payload = json.dumps(sorted(refs), sort_keys=True)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"cmf-routing-bundle:{digest}"


def new_archetype_route(
    *,
    expression_moment_id: UUID,
    route_refs: RegistryRouteRefs,
    source_support_evidence: list[str],
    route_rationale: str,
    route_fit_score: float,
    failure_alternatives: list[str],
    decision: RouteDecision,
) -> ArchetypeRoute:
    return ArchetypeRoute(
        schema_version="cmf.archetype_route.v1",
        archetype_route_id=uuid4(),
        expression_moment_id=expression_moment_id,
        route_refs=route_refs,
        source_support_evidence=source_support_evidence,
        route_rationale=route_rationale,
        route_fit_score=route_fit_score,
        failure_alternatives=failure_alternatives,
        decision=decision,
        created_at=utc_now(),
    )


def new_unsupported_format_rejection(
    *,
    expression_moment_id: UUID,
    requested_format: str,
    reason: str,
    evidence_refs: list[str],
) -> UnsupportedFormatRejection:
    return UnsupportedFormatRejection(
        schema_version="cmf.unsupported_format_rejection.v1",
        unsupported_format_rejection_id=uuid4(),
        expression_moment_id=expression_moment_id,
        requested_format=requested_format,
        decision=RouteDecision.rejected_unsupported_format,
        reason=reason,
        evidence_refs=evidence_refs,
        rejected_at=utc_now(),
    )


def new_asset_route_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_moment_id: UUID,
    registry_bundle_version: str,
    route_rationale: str,
    route_fit_score: float,
    evaluator_summary: str,
    decision_code: str,
    requested_format: str | None = None,
    accepted_route_ids: list[UUID] | None = None,
    rejected_route_ids: list[UUID] | None = None,
    unsupported_format_rejection_ids: list[UUID] | None = None,
    registry_entry_refs: list[str] | None = None,
    source_support_evidence: list[str] | None = None,
    failure_alternatives: list[str] | None = None,
    package_planning_refs: list[str] | None = None,
    reviewer_actor_id: UUID | None = None,
) -> AssetRouteReceipt:
    return AssetRouteReceipt(
        schema_version="cmf.asset_route_receipt.v1",
        asset_route_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_moment_id=expression_moment_id,
        requested_format=requested_format,
        accepted_route_ids=accepted_route_ids or [],
        rejected_route_ids=rejected_route_ids or [],
        unsupported_format_rejection_ids=unsupported_format_rejection_ids or [],
        registry_bundle_version=registry_bundle_version,
        registry_entry_refs=registry_entry_refs or [],
        source_support_evidence=source_support_evidence or [],
        route_rationale=route_rationale,
        route_fit_score=route_fit_score,
        failure_alternatives=failure_alternatives or [],
        evaluator_summary=evaluator_summary,
        decision_code=decision_code,
        package_planning_refs=package_planning_refs or [],
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
