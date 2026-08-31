"""
domain.py
---------
Canonical domain models for Operator Editorial Selection & Decision Receipts (CAE-M09).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OperatorActionType(str, Enum):
    SELECT = "SELECT"
    REJECT = "REJECT"
    MERGE = "MERGE"
    MODIFY = "MODIFY"
    PRIORITIZE = "PRIORITIZE"
    DEFER = "DEFER"
    REQUEST_ALTERNATIVES = "REQUEST_ALTERNATIVES"
    LOCK = "LOCK"
    COMPARE = "COMPARE"
    REGENERATE = "REGENERATE"


class OperatorDecisionReceipt(BaseModel):
    """Immutable record of an operator decision, emitting training signals for ML taste calibration."""
    receipt_id: str = Field(default_factory=lambda: f"RCP-{uuid.uuid4().hex[:12]}")
    operator_id: str = Field(..., min_length=3)
    candidate_id: str = Field(...)
    action_type: OperatorActionType = Field(...)
    rationale: str = Field(..., min_length=5)
    taste_delta: Optional[str] = Field(None, description="Comparative delta between model score and operator taste")
    predecessor_candidate_id: Optional[str] = Field(None, description="Lineage back to predecessor candidate if regenerated")
    version: int = Field(default=1, ge=1)
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Constraints applied during action (e.g. regeneration parameters)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SelectedCandidateSnapshot(BaseModel):
    """Immutable snapshot of an operator-approved candidate promoted to production workflows."""
    snapshot_id: str = Field(default_factory=lambda: f"SNP-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    title: str = Field(..., min_length=3)
    hook_statement: str = Field(..., min_length=5)
    priority_rank: int = Field(default=5, ge=1, le=10)
    version: int = Field(default=1, ge=1)
    predecessor_candidate_id: Optional[str] = Field(None)
    status: str = Field(default="SELECTED_FOR_PRODUCTION")
    evidence_links: List[Dict[str, Any]] = Field(..., min_length=1)
    
    approved_by: str = Field(..., min_length=3)
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = Field(None)


class CandidateLockRecord(BaseModel):
    """Immutable record of a candidate locked by an operator against automated mutations or pruning."""
    lock_id: str = Field(default_factory=lambda: f"LCK-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    locked_by: str = Field(..., min_length=3)
    rationale: str = Field(..., min_length=5)
    locked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CandidateComparisonItem(BaseModel):
    """Individual candidate evaluation metrics and attributes within a comparative matrix."""
    candidate_id: str = Field(...)
    title: str = Field(...)
    hook_statement: str = Field(...)
    candidate_type: str = Field(...)
    cmf_composite_score: float = Field(..., ge=0.0, le=1.0)
    cmf_score_bps: int = Field(..., ge=0, le=10000)
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    evidence_segment_ids: List[str] = Field(default_factory=list)
    is_selected: bool = Field(default=False)
    is_locked: bool = Field(default=False)


class CandidateComparisonMatrix(BaseModel):
    """Structured side-by-side comparison across multiple candidates for operator decision-making."""
    matrix_id: str = Field(default_factory=lambda: f"CCM-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    operator_id: str = Field(..., min_length=3)
    candidates: List[CandidateComparisonItem] = Field(..., min_length=2)
    score_deltas: Dict[str, float] = Field(default_factory=dict)
    evidence_overlap: Dict[str, List[str]] = Field(default_factory=dict)
    trade_off_notes: Optional[str] = Field(None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConstrainedRegenerationSpec(BaseModel):
    """Specification guiding constrained candidate regeneration while preserving underlying evidence."""
    predecessor_candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    operator_id: str = Field(..., min_length=3)
    guidance: str = Field(..., min_length=5)
    target_hook_emphasis: Optional[str] = Field(None)
    tone_refinement: Optional[str] = Field(None)
    target_duration_seconds: Optional[int] = Field(None, ge=10, le=300)
    preserve_evidence_segment_ids: List[str] = Field(default_factory=list)
    forbidden_angles: List[str] = Field(default_factory=list)


class CandidateEditorialBoardView(BaseModel):
    """Enriched presentation view exposing multi-dimensional context for operator taste decisions."""
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    title: str = Field(...)
    hook_statement: str = Field(...)
    candidate_type: str = Field(...)
    story_arc: Optional[str] = Field(None)
    tension_ref: Optional[str] = Field(None)
    cmf_composite_score: float = Field(..., ge=0.0, le=1.0)
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    cluster_theme: Optional[str] = Field(None)
    visual_opportunity_notes: Optional[str] = Field(None)
    is_selected: bool = Field(default=False)
    is_locked: bool = Field(default=False)


class OperatorSelectionSession(BaseModel):
    """Active operator curation session tracking all decisions, receipts, and approved candidates."""
    session_id: str = Field(default_factory=lambda: f"OPS-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    operator_id: str = Field(..., min_length=3)
    receipts: List[OperatorDecisionReceipt] = Field(default_factory=list)
    approved_snapshots: List[SelectedCandidateSnapshot] = Field(default_factory=list)
    locked_candidates: List[CandidateLockRecord] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
