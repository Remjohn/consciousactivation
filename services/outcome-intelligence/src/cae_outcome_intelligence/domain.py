"""
domain.py
---------
Canonical domain models for Outcome Measurement, Evaluation Receipts & Selective Learning (CAE-M12).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OutcomeDomain(str, Enum):
    SEMANTIC = "SEMANTIC"
    PERCEPTUAL = "PERCEPTUAL"
    DISTRIBUTION = "DISTRIBUTION"
    COMMERCIAL = "COMMERCIAL"
    OPERATOR_TASTE = "OPERATOR_TASTE"


class FailureMode(str, Enum):
    NONE = "NONE"
    SEMANTIC_FAILURE = "SEMANTIC_FAILURE"
    PERCEPTUAL_FAILURE = "PERCEPTUAL_FAILURE"
    DISTRIBUTION_FAILURE = "DISTRIBUTION_FAILURE"
    GROUNDING_FAILURE = "GROUNDING_FAILURE"


class ObservedOutcome(BaseModel):
    """Empirical observation of a published program's real-world performance."""
    outcome_id: str = Field(default_factory=lambda: f"OUT-{uuid.uuid4().hex[:12]}")
    program_id: str = Field(...)
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    domain: OutcomeDomain = Field(...)
    metrics: Dict[str, float] = Field(default_factory=dict)
    failure_mode: FailureMode = Field(default=FailureMode.NONE)
    is_grounded: bool = Field(default=True)
    misleading_context: bool = Field(default=False)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None


class EvaluationReceipt(BaseModel):
    """Auditable receipt capturing delta between predicted and observed performance."""
    receipt_id: str = Field(default_factory=lambda: f"EVR-{uuid.uuid4().hex[:12]}")
    outcome_id: str = Field(...)
    program_id: str = Field(...)
    candidate_id: str = Field(...)
    predicted_composite_score: float = Field(..., ge=0.0, le=1.0)
    observed_normalized_score: float = Field(..., ge=0.0, le=1.0)
    score_delta: float = Field(...)
    evaluator_scores: Dict[str, float] = Field(default_factory=dict)
    disagreement_spread: float = Field(default=0.0, ge=0.0, le=1.0)
    failure_mode: FailureMode = Field(default=FailureMode.NONE)
    is_grounded: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LearningProposal(BaseModel):
    """Advisory learning recommendation generated from recurring empirical evidence."""
    proposal_id: str = Field(default_factory=lambda: f"LPR-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    pattern_summary: str = Field(..., min_length=10)
    proposal_type: str = Field(..., min_length=3)  # e.g. "EVALUATOR_CALIBRATION", "BENCHMARK_UPDATE"
    suggested_modifications: Dict[str, Any] = Field(default_factory=dict)
    recurrence_count: int = Field(..., ge=1)
    evidence_receipt_ids: List[str] = Field(..., min_length=1)
    requires_operator_ratification: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PerformanceMemory(BaseModel):
    """Scoped workspace memory store tracking outcomes, receipts, and learning proposals."""
    workspace_id: str = Field(...)
    outcomes: List[ObservedOutcome] = Field(default_factory=list)
    receipts: List[EvaluationReceipt] = Field(default_factory=list)
    proposals: List[LearningProposal] = Field(default_factory=list)
