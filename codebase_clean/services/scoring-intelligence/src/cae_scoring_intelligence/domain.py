"""
domain.py
---------
Canonical domain models for Candidate Scoring, Clustering & Editorial Board (CAE-M08).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GateStatus(str, Enum):
    PASSED = "PASSED"
    FAILED_AUTHENTICITY = "FAILED_AUTHENTICITY"
    FAILED_EVIDENCE = "FAILED_EVIDENCE"
    FAILED_COMPLETENESS = "FAILED_COMPLETENESS"


class DimensionScores(BaseModel):
    """8 separable evaluation dimensions scored in range [0.0, 1.0]."""
    semantic_strength: float = Field(..., ge=0.0, le=1.0)
    guest_authenticity: float = Field(..., ge=0.0, le=1.0)
    audience_relevance: float = Field(..., ge=0.0, le=1.0)
    novelty: float = Field(..., ge=0.0, le=1.0)
    narrative_utility: float = Field(..., ge=0.0, le=1.0)
    visual_opportunity: float = Field(..., ge=0.0, le=1.0)
    editorial_completeness: float = Field(..., ge=0.0, le=1.0)
    distribution_potential: float = Field(..., ge=0.0, le=1.0)
    
    weighted_composite_score: float = Field(..., ge=0.0, le=1.0)

    @classmethod
    def calculate_composite(
        cls,
        *,
        semantic_strength: float,
        guest_authenticity: float,
        audience_relevance: float,
        novelty: float,
        narrative_utility: float,
        visual_opportunity: float,
        editorial_completeness: float,
        distribution_potential: float,
    ) -> DimensionScores:
        composite = (
            0.15 * semantic_strength
            + 0.20 * guest_authenticity
            + 0.15 * audience_relevance
            + 0.15 * novelty
            + 0.10 * narrative_utility
            + 0.10 * visual_opportunity
            + 0.05 * editorial_completeness
            + 0.10 * distribution_potential
        )
        return cls(
            semantic_strength=semantic_strength,
            guest_authenticity=guest_authenticity,
            audience_relevance=audience_relevance,
            novelty=novelty,
            narrative_utility=narrative_utility,
            visual_opportunity=visual_opportunity,
            editorial_completeness=editorial_completeness,
            distribution_potential=distribution_potential,
            weighted_composite_score=round(composite, 4),
        )


class EvaluatorProvenance(BaseModel):
    """Audit lineage for evaluation algorithms."""
    evaluator_id: str = Field(...)
    evaluator_version: str = Field(...)
    scored_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str = Field(..., min_length=5)


class CandidateEvaluationProfile(BaseModel):
    """Complete evaluation profile for a single ContentCandidate."""
    profile_id: str = Field(default_factory=lambda: f"EVP-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    scores: DimensionScores = Field(...)
    gate_status: GateStatus = Field(...)
    is_eligible_for_board: bool = Field(...)
    provenance: EvaluatorProvenance = Field(...)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClusterGroup(BaseModel):
    """Semantic cluster revealing thematic coverage and redundancy across candidates."""
    cluster_id: str = Field(default_factory=lambda: f"CLS-{uuid.uuid4().hex[:8]}")
    theme: str = Field(..., min_length=3)
    candidate_ids: List[str] = Field(..., min_length=1)
    redundancy_index: float = Field(..., ge=0.0, le=1.0, description="0.0 = diverse, 1.0 = highly redundant")
    coverage_domain: str = Field(...)


class EditorialBoard(BaseModel):
    """
    Transparent portfolio representing evaluated candidates and their cluster structure.
    Does NOT declare production approval; prepares structured portfolio for Operator selection.
    """
    board_id: str = Field(default_factory=lambda: f"BRD-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    evaluated_candidates: List[CandidateEvaluationProfile] = Field(default_factory=list)
    clusters: List[ClusterGroup] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
