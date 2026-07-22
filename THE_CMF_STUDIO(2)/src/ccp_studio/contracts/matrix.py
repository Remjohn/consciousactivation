"""Matrix of Edging contracts for TS-CMF-025."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class MatrixPass(str, Enum):
    research = "research"
    provocation = "provocation"
    authentication = "authentication"
    primitive = "primitive"
    coalition = "coalition"
    edge = "edge"
    routing = "routing"
    benchmark = "benchmark"


class MatrixBriefStatus(str, Enum):
    draft = "draft"
    evaluation_failed = "evaluation_failed"
    evaluated = "evaluated"
    approved = "approved"
    rejected = "rejected"
    superseded = "superseded"


class PrimitiveCandidateStatus(str, Enum):
    native = "native"
    latent = "latent"
    jit_completable = "jit_completable"
    unsupported = "unsupported"
    unresolved_registry_ref = "unresolved_registry_ref"


class MatrixPassOutput(BaseModel):
    schema_version: Literal["cmf.matrix_pass_output.v1"]
    pass_name: MatrixPass
    summary: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(default_factory=list)


class BroadPrimarySignal(BaseModel):
    schema_version: Literal["cmf.broad_primary_signal.v1"]
    broad_primary_signal_id: UUID
    statement: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(min_length=1)
    magnitude_score: float = Field(ge=0, le=1)


class TensionSite(BaseModel):
    schema_version: Literal["cmf.tension_site.v1"]
    tension_site_id: UUID
    statement: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(default_factory=list)
    collision_type: str = Field(min_length=1)
    magnitude_score: float = Field(ge=0, le=1)
    speculative: bool = False
    can_anchor_question: bool = True


class PrimitiveCandidatePacket(BaseModel):
    schema_version: Literal["cmf.primitive_candidate_packet.v1"]
    primitive_candidate_id: UUID
    primitive_family: str = Field(min_length=1)
    primitive_ref: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(default_factory=list)
    status: PrimitiveCandidateStatus
    survival_rationale: str = Field(min_length=1)
    weakness: str | None = None


class CoalitionSignature(BaseModel):
    schema_version: Literal["cmf.coalition_signature.v1"]
    coalition_signature_id: UUID
    primitive_candidate_ids: list[UUID] = Field(min_length=2)
    family_ratios: dict[str, float] = Field(default_factory=dict)
    interaction_rationale: str = Field(min_length=1)
    route_implications: list[str] = Field(min_length=1)


class EdgeProduct(BaseModel):
    schema_version: Literal["cmf.edge_product.v1"]
    edge_product_id: UUID
    name: str = Field(min_length=1)
    tension_site_ids: list[UUID] = Field(min_length=1)
    coalition_signature_id: UUID
    anti_centroid_pressure: str = Field(min_length=1)
    expected_expression_state: list[str] = Field(min_length=1)
    route_implications: list[str] = Field(min_length=1)


class MatrixFailurePoint(BaseModel):
    schema_version: Literal["cmf.matrix_failure_point.v1"]
    failure_point_id: UUID
    statement: str = Field(min_length=1)
    avoidance_guidance: str = Field(min_length=1)
    severity: str = Field(default="medium")


class MatrixEvaluationScores(BaseModel):
    schema_version: Literal["cmf.matrix_evaluation_scores.v1"]
    pass_completeness_score: float = Field(ge=0, le=1)
    saturation_score: float = Field(ge=0, le=1)
    collision_strength_score: float = Field(ge=0, le=1)
    specificity_score: float = Field(ge=0, le=1)
    anti_centroid_risk_score: float = Field(ge=0, le=1)
    routeability_score: float = Field(ge=0, le=1)


class MatrixOfEdgingBrief(BaseModel):
    schema_version: Literal["cmf.matrix_of_edging_brief.v1"]
    matrix_brief_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    guest_dossier_id: UUID
    audience_reality_brief_id: UUID
    context_premise_id: UUID
    trigger_map_id: UUID | None = None
    version: int = 1
    status: MatrixBriefStatus
    pass_outputs: list[MatrixPassOutput] = Field(min_length=8)
    broad_primary_signals: list[BroadPrimarySignal] = Field(min_length=1)
    tension_sites: list[TensionSite] = Field(min_length=1)
    primitive_candidates: list[PrimitiveCandidatePacket] = Field(min_length=1)
    coalition_signatures: list[CoalitionSignature] = Field(min_length=1)
    edge_products: list[EdgeProduct] = Field(min_length=1)
    likely_failure_points: list[MatrixFailurePoint] = Field(min_length=1)
    route_implications: list[str] = Field(min_length=1)
    input_context_hash: str = Field(min_length=1)
    created_by_actor_id: UUID
    approved_by_actor_id: UUID | None = None
    created_at: datetime
    updated_at: datetime


class MatrixReceipt(BaseModel):
    schema_version: Literal["cmf.matrix_receipt.v1"]
    matrix_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    matrix_brief_id: UUID
    input_context_ids: dict[str, UUID]
    pass_names: list[MatrixPass] = Field(min_length=8)
    evaluator_scores: MatrixEvaluationScores | None = None
    failure_points: list[str] = Field(default_factory=list)
    reviewer_state: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


class MatrixSaturationPacket(BaseModel):
    schema_version: Literal["cmf.matrix_saturation_packet.v1"]
    organization_id: UUID
    brand_id: UUID
    matrix_brief_id: UUID
    primitive_candidate_ids: list[UUID] = Field(min_length=1)
    coalition_signature_ids: list[UUID] = Field(min_length=1)
    edge_product_ids: list[UUID] = Field(min_length=1)
    route_implications: list[str] = Field(min_length=1)


def matrix_context_hash(*, input_ids: dict[str, UUID], route_seed: str | None = None) -> str:
    payload = {
        "input_ids": {key: str(value) for key, value in sorted(input_ids.items())},
        "route_seed": route_seed or "",
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def new_pass_output(*, pass_name: MatrixPass, summary: str, evidence_ids: list[UUID]) -> MatrixPassOutput:
    return MatrixPassOutput(
        schema_version="cmf.matrix_pass_output.v1",
        pass_name=pass_name,
        summary=summary,
        evidence_ids=evidence_ids,
    )


def new_matrix_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    matrix_brief_id: UUID,
    input_context_ids: dict[str, UUID],
    pass_names: list[MatrixPass],
    evaluator_scores: MatrixEvaluationScores | None,
    failure_points: list[str],
    reviewer_state: str,
    decision_code: str,
    reviewer_actor_id: UUID | None = None,
) -> MatrixReceipt:
    return MatrixReceipt(
        schema_version="cmf.matrix_receipt.v1",
        matrix_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        matrix_brief_id=matrix_brief_id,
        input_context_ids=input_context_ids,
        pass_names=pass_names,
        evaluator_scores=evaluator_scores,
        failure_points=failure_points,
        reviewer_state=reviewer_state,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
