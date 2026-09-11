"""
domain.py
---------
Canonical domain models for Editorial Candidate Formation (CAE-M07).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CandidateType(str, Enum):
    QUOTE_CANDIDATE = "QUOTE_CANDIDATE"
    BEAT_CANDIDATE = "BEAT_CANDIDATE"
    STORY_CANDIDATE = "STORY_CANDIDATE"
    MECHANISM_CANDIDATE = "MECHANISM_CANDIDATE"
    CONTRADICTION_CANDIDATE = "CONTRADICTION_CANDIDATE"
    TRANSFORMATION_CANDIDATE = "TRANSFORMATION_CANDIDATE"
    REACTION_CANDIDATE = "REACTION_CANDIDATE"
    HYBRID_CANDIDATE = "HYBRID_CANDIDATE"


class NarrativeCompleteness(str, Enum):
    COMPLETE = "COMPLETE"
    INTENTIONALLY_OPEN_ENDED = "INTENTIONALLY_OPEN_ENDED"
    INCOMPLETE = "INCOMPLETE"


class ProductionStatus(str, Enum):
    DRAFT_CANDIDATE = "DRAFT_CANDIDATE"
    PENDING_OPERATOR_REVIEW = "PENDING_OPERATOR_REVIEW"
    REJECTED = "REJECTED"
    APPROVED_FOR_PRODUCTION = "APPROVED_FOR_PRODUCTION"


class HeritageCMFScore(BaseModel):
    """OLD CMF multi-axis diagnostic scoring framework."""
    emotional_resonance: float = Field(..., ge=0.0, le=1.0)
    cognitive_novelty: float = Field(..., ge=0.0, le=1.0)
    authority_evidence: float = Field(..., ge=0.0, le=1.0)
    narrative_velocity: float = Field(..., ge=0.0, le=1.0)
    composite_score: float = Field(..., ge=0.0, le=1.0)

    @classmethod
    def calculate(
        cls,
        *,
        emotional_resonance: float,
        cognitive_novelty: float,
        authority_evidence: float,
        narrative_velocity: float,
    ) -> HeritageCMFScore:
        composite = (
            0.30 * emotional_resonance
            + 0.30 * cognitive_novelty
            + 0.25 * authority_evidence
            + 0.15 * narrative_velocity
        )
        return cls(
            emotional_resonance=emotional_resonance,
            cognitive_novelty=cognitive_novelty,
            authority_evidence=authority_evidence,
            narrative_velocity=narrative_velocity,
            composite_score=round(composite, 4),
        )


class CandidateEvidenceLink(BaseModel):
    """Direct verifiable provenance linkage to an upstream EvidenceSegment and SemanticAnnotation."""
    segment_id: str = Field(...)
    annotation_id: str = Field(...)
    speaker: str = Field(...)
    start_time_ms: int = Field(..., ge=0)
    end_time_ms: int = Field(..., gt=0)
    verbatim_text: str = Field(..., min_length=5)
    text_sha256: str = Field(..., min_length=64, max_length=64)


class ContentCandidate(BaseModel):
    """
    The canonical candidate editorial unit synthesizing grounded evidence into a structured narrative candidate.
    """
    candidate_id: str = Field(default_factory=lambda: f"CND-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    candidate_type: CandidateType = Field(...)
    title: str = Field(..., min_length=3, max_length=120)
    hook_statement: str = Field(..., min_length=5)
    narrative_completeness: NarrativeCompleteness = Field(...)
    
    story_arc: Optional[str] = Field(None, description="e.g. 'THE_WITNESS', 'CRUCIBLE_AND_REBIRTH'")
    tension_ref: Optional[str] = Field(None, description="Linked audience tension ID (e.g. AET-*)")
    invariant_ref: Optional[str] = Field(None, description="Linked SDA invariant ID (e.g. SDA-INV-*)")
    archetypal_container: Optional[str] = Field(None, description="e.g. 'THE_SAGE', 'THE_REBEL'")
    
    evidence_links: List[CandidateEvidenceLink] = Field(..., min_length=1)
    cmf_score: HeritageCMFScore = Field(...)
    
    production_status: ProductionStatus = Field(default=ProductionStatus.DRAFT_CANDIDATE)
    standalone_context_notes: Optional[str] = Field(None, description="Explanatory notes needed for standalone extraction")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
