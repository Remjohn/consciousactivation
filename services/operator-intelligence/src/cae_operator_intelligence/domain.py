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


class OperatorDecisionReceipt(BaseModel):
    """Immutable record of an operator decision, emitting training signals for ML taste calibration."""
    receipt_id: str = Field(default_factory=lambda: f"RCP-{uuid.uuid4().hex[:12]}")
    operator_id: str = Field(..., min_length=3)
    candidate_id: str = Field(...)
    action_type: OperatorActionType = Field(...)
    rationale: str = Field(..., min_length=5)
    taste_delta: Optional[str] = Field(None, description="Comparative delta between model score and operator taste")
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
    evidence_links: List[Dict[str, Any]] = Field(..., min_length=1)
    
    approved_by: str = Field(..., min_length=3)
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = Field(None)


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


class OperatorSelectionSession(BaseModel):
    """Active operator curation session tracking all decisions, receipts, and approved candidates."""
    session_id: str = Field(default_factory=lambda: f"OPS-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    operator_id: str = Field(..., min_length=3)
    receipts: List[OperatorDecisionReceipt] = Field(default_factory=list)
    approved_snapshots: List[SelectedCandidateSnapshot] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
