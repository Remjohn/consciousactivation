"""
domain.py
---------
Canonical domain models for Semantic Attribution & Evidence Classification (CAE-M06).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SemanticRole(str, Enum):
    QUOTE = "QUOTE"
    BEAT = "BEAT"
    STORY = "STORY"
    MECHANISM = "MECHANISM"
    CLAIM = "CLAIM"
    PROOF = "PROOF"
    CONTRADICTION = "CONTRADICTION"
    REVEAL = "REVEAL"
    REFLECTION = "REFLECTION"
    QUESTION = "QUESTION"
    POSITION = "POSITION"
    OBSERVATION = "OBSERVATION"


class EvidenceEpistemicStatus(str, Enum):
    FIRST_PARTY_FACT = "FIRST_PARTY_FACT"
    LIVED_EXPERIENCE = "LIVED_EXPERIENCE"
    SPECULATIVE_INFERENCE = "SPECULATIVE_INFERENCE"
    SECOND_PARTY_HEARSAY = "SECOND_PARTY_HEARSAY"
    ABSTRACT_OPINION = "ABSTRACT_OPINION"


class EmotionalRegister(str, Enum):
    VULNERABILITY = "VULNERABILITY"
    CONVICTION = "CONVICTION"
    FRUSTRATION = "FRUSTRATION"
    CLARITY = "CLARITY"
    RESOLVE = "RESOLVE"
    NEUTRAL = "NEUTRAL"


class StoryArcGeometry(str, Enum):
    THE_WITNESS = "THE_WITNESS"
    CRUCIBLE_AND_REBIRTH = "CRUCIBLE_AND_REBIRTH"
    DAVID_VS_GOLIATH = "DAVID_VS_GOLIATH"
    SYSTEMS_AWAKENING = "SYSTEMS_AWAKENING"
    NONE = "NONE"


class ObservableEvidence(BaseModel):
    """Immutable observable facts directly extracted from the EvidenceSegment."""
    segment_id: str = Field(...)
    workspace_id: str = Field(...)
    session_id: str = Field(...)
    speaker: str = Field(...)
    start_time_ms: int = Field(..., ge=0)
    end_time_ms: int = Field(..., gt=0)
    verbatim_text: str = Field(..., min_length=5)
    text_sha256: str = Field(..., min_length=64, max_length=64)


class SemanticInference(BaseModel):
    """Model-derived or verified editorial attributions attached to the observable evidence."""
    semantic_role: SemanticRole = Field(...)
    epistemic_status: EvidenceEpistemicStatus = Field(...)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    
    tension_ref: Optional[str] = Field(None, description="Linked audience tension ID (e.g. AET-*)")
    invariant_ref: Optional[str] = Field(None, description="Linked SDA invariant ID (e.g. SDA-INV-*)")
    emotional_register: EmotionalRegister = Field(default=EmotionalRegister.NEUTRAL)
    story_arc_geometry: StoryArcGeometry = Field(default=StoryArcGeometry.NONE)
    
    is_eligible_for_candidate_formation: bool = Field(True)
    is_publishable: bool = Field(False, description="Strictly false in M06. Publishability is deferred.")


class SemanticAnnotation(BaseModel):
    """
    Composite entity binding observable transcript evidence with typed semantic inference.
    Maintains strict cryptographic and logical partition between fact and interpretation.
    """
    annotation_id: str = Field(default_factory=lambda: f"ANN-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    observable_evidence: ObservableEvidence = Field(...)
    semantic_inference: SemanticInference = Field(...)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidenceClassification(BaseModel):
    """Summary classification record used downstream by Candidate Formation (CAE-M07)."""
    classification_id: str = Field(default_factory=lambda: f"ECL-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    segment_id: str = Field(...)
    annotation_id: str = Field(...)
    primary_role: SemanticRole = Field(...)
    epistemic_tier: EvidenceEpistemicStatus = Field(...)
    is_candidate_eligible: bool = Field(...)
