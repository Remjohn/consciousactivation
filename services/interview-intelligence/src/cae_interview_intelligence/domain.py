"""
domain.py
---------
Canonical domain contracts for the Interview Semantic Program (CAE-M04).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QuestionStage(str, Enum):
    ORIENTATION = "ORIENTATION"
    TENSION_PROBE = "TENSION_PROBE"
    CRUCIBLE_EXPOSURE = "CRUCIBLE_EXPOSURE"
    RESOLUTION_SYNTHESIS = "RESOLUTION_SYNTHESIS"


class DesiredEvidenceClass(str, Enum):
    CRUCIBLE_MOMENT = "CRUCIBLE_MOMENT"
    CONTRARIAN_DECISION = "CONTRARIAN_DECISION"
    COST_PAID_RECEIPT = "COST_PAID_RECEIPT"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"


class InterviewQuestion(BaseModel):
    """An individual elicitation prompt within the interview progression."""
    question_id: str = Field(default_factory=lambda: f"QST-{uuid.uuid4().hex[:8]}")
    stage: QuestionStage = Field(...)
    prompt_text: str = Field(..., min_length=15, description="The human-facing open-ended elicitation prompt")
    expected_evidence_class: DesiredEvidenceClass = Field(...)
    forbidden_presumptions: List[str] = Field(default_factory=list, description="Presumptions forbidden from being leadingly stated")


class AdaptiveFollowUpPolicy(BaseModel):
    """Rules for dynamically pivoting or probing based on guest conversational cues."""
    on_intellectualization: str = Field(
        default="Request specific episodic scene, sensory detail, or chronological moment.",
        description="Strategy when guest retreats into abstract theory",
    )
    on_vagueness: str = Field(
        default="Request specific numbers, named entities, or exact costs paid.",
        description="Strategy when guest uses generic corporate speak",
    )
    on_defensiveness: str = Field(
        default="Acknowledge emotional friction, mirror stance, and shift to systemic frame.",
        description="Strategy when guest hardens defenses",
    )
    max_adaptive_probes_per_stage: int = Field(default=2, ge=1, le=5)


class MatrixOfEdgingConfig(BaseModel):
    """Governs psychological pressure, vulnerability target, and safety ceilings."""
    target_vulnerability_depth: float = Field(0.75, ge=0.0, le=1.0)
    pressure_gradient: str = Field("PROGRESSIVE_EXPONENTIAL", description="Pacing model for intellectual pressure")
    forbidden_territories: List[str] = Field(default_factory=list, description="Explicit boundaries off-limits for elicitation")
    safety_ceiling_threshold: float = Field(0.90, ge=0.5, le=1.0, description="Max allowable pressure before auto-pivot")


class InterviewBrief(BaseModel):
    """
    The canonical interview semantic program contract.
    The system structures the collision field; the guest provides the authentic lived evidence.
    """
    brief_id: str = Field(default_factory=lambda: f"BRF-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(..., description="Tenant isolation identifier")
    hypothesis_ref: str = Field(..., description="Linked CollisionHypothesis ID")
    guest_id: str = Field(..., description="Target guest identifier")
    audience_id: str = Field(..., description="Target audience cohort identifier")
    
    target_activation_state: str = Field(..., min_length=5, description="Target cognitive/affective shift to elicit")
    context_premise: str = Field(..., min_length=20, description="Mutual factual reality and framing")
    collision_anchor_thesis: str = Field(..., min_length=15, description="The underlying tension thesis being tested")
    
    question_progression: List[InterviewQuestion] = Field(..., min_length=4, description="At least 4 staged questions")
    follow_up_policy: AdaptiveFollowUpPolicy = Field(default_factory=AdaptiveFollowUpPolicy)
    edging_config: MatrixOfEdgingConfig = Field(default_factory=MatrixOfEdgingConfig)
    stopping_conditions: List[str] = Field(
        default_factory=lambda: [
            "EVIDENCE_SATURATED",
            "SAFETY_CEILING_REACHED",
            "CRUCIBLE_MOMENT_AUTHENTICATED",
            "MAX_TURNS_EXCEEDED",
        ]
    )
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InterviewTurnResponse(BaseModel):
    """A recorded response turn from the live interview session."""
    turn_id: str = Field(default_factory=lambda: f"TRN-{uuid.uuid4().hex[:8]}")
    question_id: str = Field(...)
    stage: QuestionStage = Field(...)
    transcript_text: str = Field(..., min_length=10)
    
    specificity_score: float = Field(..., ge=0.0, le=1.0, description="Presence of concrete facts, names, dates, metrics")
    authenticity_score: float = Field(..., ge=0.0, le=1.0, description="Presence of autobiographical vulnerability vs PR script")
    contains_lived_evidence: bool = Field(...)
    is_generic_slop: bool = Field(False)


class InterviewSessionResult(BaseModel):
    """Aggregated outcome of an executed interview session."""
    session_id: str = Field(default_factory=lambda: f"SES-{uuid.uuid4().hex[:12]}")
    brief_id: str = Field(...)
    workspace_id: str = Field(...)
    guest_id: str = Field(...)
    turns: List[InterviewTurnResponse] = Field(default_factory=list)
    
    is_authenticated: bool = Field(True, description="Presence of verified human guest signatures")
    execution_status: str = Field("COMPLETED", description="COMPLETED, INCOMPLETE, QUARANTINED")
    extracted_crucible_evidence: List[str] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
