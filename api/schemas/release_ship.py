"""
api/schemas/release_ship.py
---------------------------
FastAPI Pydantic schemas for Release / Ship / Outcome Runtime endpoints (M45).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreateReleaseSessionInput(BaseModel):
    candidate_id: str = Field(..., description="ID of the candidate to release")
    workspace_id: str = Field(..., description="Target tenant workspace ID")
    actor_id: str = Field(..., description="Actor initializing the session")
    artifact_ref: Dict[str, Any] = Field(..., description="Reference to the candidate artifact")


class VerifyFinalQAInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    actor_id: str = Field(..., description="Actor performing QA verification (ANALYST)")
    actor_lane: str = Field(default="ANALYST", description="Authority lane")
    semantic_qa_result: Dict[str, Any] = Field(..., description="Semantic QA evaluation result")
    render_qa_result: Dict[str, Any] = Field(..., description="Render QA evaluation result")
    evidence_segment: Dict[str, Any] = Field(..., description="Evidence segment with quote_text")
    wrong_reading_locks: List[str] = Field(..., description="Lexicographical wrong-reading locks")
    is_synthetic: bool = Field(default=False, description="Synthetic marker")


class AuthorizeReleaseInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    operator_id: str = Field(..., description="Human operator ID (COMMANDER)")
    actor_lane: str = Field(default="COMMANDER", description="Authority lane")
    decision: str = Field(default="APPROVED", description="Operator decision (APPROVED/REJECTED)")
    target_channels: List[str] = Field(..., min_length=1, description="Target distribution channels")
    rationale: str = Field(..., min_length=5, description="Operator decision rationale")
    release_manifest_sha256: Optional[str] = None


class ExecuteShipInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    actor_id: str = Field(..., description="Actor executing shipment (COMPOSER)")
    actor_lane: str = Field(default="COMPOSER", description="Authority lane")
    target_channel: str = Field(..., description="Target distribution channel")
    delivery_endpoint: str = Field(..., description="Target delivery endpoint URL/path")
    simulate_channel_failure: bool = Field(default=False, description="Simulate channel failure")


class CaptureOutcomeInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    actor_id: str = Field(..., description="Actor capturing outcome (HUNTER)")
    actor_lane: str = Field(default="HUNTER", description="Authority lane")
    domain: str = Field(default="PERCEPTUAL", description="Outcome domain (SEMANTIC, PERCEPTUAL, DISTRIBUTION, COMMERCIAL)")
    metrics: Dict[str, float] = Field(..., description="Empirical performance metrics")
    predicted_composite_score: float = Field(..., ge=0.0, le=1.0)
    observed_normalized_score: float = Field(..., ge=0.0, le=1.0)
    evaluator_scores: Optional[Dict[str, float]] = None
    is_grounded: bool = Field(default=True)
    misleading_context: bool = Field(default=False)
    failure_mode: str = Field(default="NONE")
    notes: Optional[str] = None


class ProposeLearningInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    actor_id: str = Field(..., description="Actor proposing learning (ANALYST)")
    actor_lane: str = Field(default="ANALYST", description="Authority lane")
    min_recurrence: int = Field(default=2, ge=1)


class RatifyProposalInput(BaseModel):
    aggregate_id: str = Field(..., description="ID of the program aggregate")
    operator_id: str = Field(..., description="Operator ratifying proposal (COMMANDER)")
    actor_lane: str = Field(default="COMMANDER", description="Authority lane")
    proposal_id: str = Field(...)
    decision: str = Field(default="RATIFIED")


class ReleaseSessionResponse(BaseModel):
    aggregate_id: str
    program_id: str
    workspace_id: str
    current_state: str
    state_data: Dict[str, Any]
