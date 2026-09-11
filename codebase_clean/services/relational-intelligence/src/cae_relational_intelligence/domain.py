"""
domain.py
---------
Canonical domain contracts for Audience x Guest State Synthesis (CAE-M02).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MoralFoundationAxis(str, Enum):
    CARE_HARM = "CARE_HARM"
    FAIRNESS_CHEATING = "FAIRNESS_CHEATING"
    LOYALTY_BETRAYAL = "LOYALTY_BETRAYAL"
    AUTHORITY_SUBVERSION = "AUTHORITY_SUBVERSION"
    SANCTITY_DEGRADATION = "SANCTITY_DEGRADATION"
    LIBERTY_OPPRESSION = "LIBERTY_OPPRESSION"


class CopingPotentialType(str, Enum):
    PROBLEM_FOCUSED = "PROBLEM_FOCUSED"
    EMOTION_FOCUSED = "EMOTION_FOCUSED"
    HELPLESSNESS = "HELPLESSNESS"
    AVOIDANCE = "AVOIDANCE"


class AgencyAttributionType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    SYSTEMIC = "SYSTEMIC"
    FATE = "FATE"


class TemporalPositionType(str, Enum):
    PAST_TRAUMA = "PAST_TRAUMA"
    PRESENT_ACUTE_STRUGGLE = "PRESENT_ACUTE_STRUGGLE"
    FUTURE_ANTICIPATED_CRISIS = "FUTURE_ANTICIPATED_CRISIS"
    TRANSCENDED_RESOLUTION = "TRANSCENDED_RESOLUTION"


class FourAxisEvidence(BaseModel):
    """Explicit multi-axis evidence preventing single-score flat collapse."""
    moral_foundation: MoralFoundationAxis
    moral_foundation_notes: str = Field(..., min_length=5)
    
    coping_potential: CopingPotentialType
    coping_potential_notes: str = Field(..., min_length=5)
    
    agency_attribution: AgencyAttributionType
    agency_attribution_notes: str = Field(..., min_length=5)
    
    temporal_position: TemporalPositionType
    temporal_position_notes: str = Field(..., min_length=5)
    
    axis_alignment_scores: Dict[str, float] = Field(
        ...,
        description="Individual alignment score [0.0 - 1.0] per axis",
    )


class AudienceProfile(BaseModel):
    """Persistent schema and existential invariants for a defined audience cohort."""
    workspace_id: str = Field(..., description="Tenant isolation identifier")
    audience_id: str = Field(default_factory=lambda: f"AUD-{uuid.uuid4().hex[:12]}")
    persona_name: str = Field(..., min_length=2)
    existential_invariants: List[str] = Field(default_factory=list, description="Core worldview axioms")
    core_wounds: List[str] = Field(default_factory=list, description="Foundational emotional wounds")
    default_schemas: List[str] = Field(default_factory=list, description="Habitual cognitive framing models")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AudienceTemporalState(BaseModel):
    """Dynamic, time-bounded emotional, semantic, and capacity state of the audience."""
    state_id: str = Field(default_factory=lambda: f"AST-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(..., description="Tenant isolation identifier")
    audience_id: str = Field(...)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    affective_state: str = Field(..., min_length=2, description="Current mood / emotional climate (e.g. Anxiety, Cynicism, Awe)")
    semantic_frame: str = Field(..., min_length=2, description="Dominant language & metaphoric framing")
    media_motive: str = Field(..., min_length=2, description="Active gratification sought (e.g. Validation, Escape, Guidance)")
    capacity_level: str = Field("MODERATE", description="Cognitive and emotional bandwidth (LOW, MODERATE, HIGH)")
    active_tensions: List[str] = Field(default_factory=list, description="Unresolved psychological friction points")
    evidence_refs: List[str] = Field(default_factory=list, description="Citations to underlying community signals or chats")


class GuestProfile(BaseModel):
    """Persistent profile and lived proof authority of an interview guest."""
    workspace_id: str = Field(..., description="Tenant isolation identifier")
    guest_id: str = Field(default_factory=lambda: f"GST-{uuid.uuid4().hex[:12]}")
    full_name: str = Field(..., min_length=2)
    email: Optional[str] = None
    emotional_dna_baseline: Dict[str, Any] = Field(default_factory=dict)
    lived_proof_milestones: List[str] = Field(default_factory=list, description="Real biographical events and crucible moments")
    forbidden_territories: List[str] = Field(default_factory=list, description="Stances or topics explicitly off-limits")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GuestActivationState(BaseModel):
    """Dynamic activation snapshot of the guest's current readiness and vulnerability."""
    state_id: str = Field(default_factory=lambda: f"GAS-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(..., description="Tenant isolation identifier")
    guest_id: str = Field(...)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    current_arousal: float = Field(..., ge=0.0, le=1.0, description="Physiological / emotional activation level")
    active_vulnerability_vectors: List[str] = Field(default_factory=list, description="Areas of open emotional exposure")
    defended_stances: List[str] = Field(default_factory=list, description="Defended semantic intellectualizations")
    epistemic_readiness: str = Field("RECEPTIVE", description="Readiness for challenging inquiry (DEFENDED, CAUTIOUS, RECEPTIVE, INTEGRATIVE)")
    evidence_refs: List[str] = Field(default_factory=list, description="Citations to pre-interview turns or notes")


class GuestExperiencedTension(BaseModel):
    """Relation linking Guest to a lived existential or ethical tension."""
    relation_id: str = Field(default_factory=lambda: f"REL-GET-{uuid.uuid4().hex[:12]}")
    workspace_id: str
    guest_id: str
    tension_label: str = Field(..., min_length=3)
    moral_foundation: MoralFoundationAxis
    coping_type: CopingPotentialType
    lived_proof_citation: str = Field(..., min_length=10)
    was_resolved: bool = Field(False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GuestResolvedTension(GuestExperiencedTension):
    """Relation specifically denoting a tension the Guest successfully navigated and resolved."""
    resolution_pathway: str = Field(..., min_length=10)
    transcended_insight: str = Field(..., min_length=10)
    was_resolved: bool = Field(True)


class AudienceExperiencesTension(BaseModel):
    """Relation linking Audience to an active existential or ethical tension."""
    relation_id: str = Field(default_factory=lambda: f"REL-AET-{uuid.uuid4().hex[:12]}")
    workspace_id: str
    audience_id: str
    tension_label: str = Field(..., min_length=3)
    moral_foundation: MoralFoundationAxis
    current_coping: CopingPotentialType
    urgency_score: float = Field(..., ge=0.0, le=1.0)
    evidence_citation: str = Field(..., min_length=10)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GuestAudienceCongruence(BaseModel):
    """
    The synthesized relational bridge between Audience and Guest.
    Carries the full 4-axis evidence breakdown and workspace lineage.
    """
    congruence_id: str = Field(default_factory=lambda: f"CONG-{uuid.uuid4().hex[:12]}")
    workspace_id: str
    guest_id: str
    guest_state_id: str
    audience_id: str
    audience_state_id: str
    shared_tension_theme: str = Field(..., min_length=3)
    
    four_axis_evidence: FourAxisEvidence = Field(...)
    composite_congruence_score: float = Field(..., ge=0.0, le=1.0)
    
    is_valid_bridge: bool = Field(True)
    synthesized_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
