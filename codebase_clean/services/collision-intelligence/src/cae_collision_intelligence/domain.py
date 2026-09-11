"""
domain.py
---------
Canonical domain models for Collision Hypothesis & Multi-World Intersection (CAE-M03).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CollisionRelationType(str, Enum):
    ANALOGY = "ANALOGY"
    INVERSION = "INVERSION"
    PARADOX = "PARADOX"
    SYSTEMS_LENS = "SYSTEMS_LENS"
    COUNTER_POSITION = "COUNTER_POSITION"


class ObliqueLens(BaseModel):
    """An external cross-domain mental model or structural invariant used as a thinking lens."""
    lens_id: str = Field(default_factory=lambda: f"LENS-{uuid.uuid4().hex[:8]}")
    domain_name: str = Field(..., description="Source field, e.g. Evolutionary Biology, Thermodynamics, Jazz Improvisation")
    source_reference: str = Field(..., description="Book title, paper citation, or canonical framework")
    invariant_principle: str = Field(..., min_length=10, description="The abstract structural rule or mechanism")


class NoveltyClicheAssessment(BaseModel):
    """Evaluates the semantic distance vs overused trope risk of a hypothesis."""
    semantic_distance_score: float = Field(..., ge=0.0, le=1.0, description="Distance from common discourse baselines")
    cliche_risk_score: float = Field(..., ge=0.0, le=1.0, description="Presence of generic viral buzzwords/tropes")
    trope_penalty: float = Field(0.0, ge=0.0, le=1.0, description="Penalty applied if trope patterns detected")
    is_cliche_quarantined: bool = Field(False, description="Flag indicating if hypothesis is blocked due to excessive cliché")


class FalsificationCondition(BaseModel):
    """Explicit conditions under which the hypothesis is disproven or invalidated."""
    refuting_observation: str = Field(..., min_length=10, description="What real-world evidence would prove this thesis false")
    disconfirming_testimony: str = Field(..., min_length=10, description="What guest lived experience would refute this claim")
    boundary_limitation: str = Field(..., min_length=10, description="Where this hypothesis ceases to hold true")


class HeritageCMFEval(BaseModel):
    """Descriptive / advisory viral trinity scoring from OLD CMF heritage."""
    surprise_score: float = Field(..., ge=0.0, le=1.0, description="Pattern interrupt & expectation violation")
    emotion_score: float = Field(..., ge=0.0, le=1.0, description="Somatic & affective resonance")
    specificity_score: float = Field(..., ge=0.0, le=1.0, description="Concrete detail & un-fakable lived proof")
    ai_slop_risk: float = Field(..., ge=0.0, le=1.0, description="Risk of sounding like generic AI-generated copy")
    composite_viral_potential: float = Field(..., ge=0.0, le=1.0, description="Non-compensable advisory score")


class CollisionHypothesis(BaseModel):
    """
    The canonical, typed hypothesis entity created by the 4-world collision:
    World Signal (M01) x Audience Psyche (M02) x Guest Authority (M02) x Oblique Lens (M03).
    """
    hypothesis_id: str = Field(default_factory=lambda: f"HYP-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(..., description="Tenant isolation anchor")
    title: str = Field(..., min_length=5, description="Concise editorial hypothesis thesis")
    relation_type: CollisionRelationType = Field(...)
    
    # 4-World Anchors
    audience_id: str = Field(..., description="Target Audience identifier")
    audience_tension_ref: str = Field(..., description="Active audience tension label / relation ID")
    guest_id: str = Field(..., description="Guest identifier")
    guest_lived_proof_citation: str = Field(..., min_length=10, description="Verifiable biographical proof backing authority")
    research_signal_id: str = Field(..., description="Verified ResearchSignal ID from M01")
    sda_invariant: str = Field("SDA-INV-001_ACTIVE_TENSION", description="Structural Dynamics of Activation invariant")
    oblique_lens: Optional[ObliqueLens] = None
    
    # Bridge & Evidence
    bridge_statement: str = Field(..., min_length=20, description="Explicit logical/semantic argument joining all 4 worlds")
    evidence_references: List[str] = Field(..., min_length=1, description="Citations to verified world signal, survey, or interview turns")
    
    # Quality & Falsification Standards
    novelty_assessment: NoveltyClicheAssessment = Field(...)
    falsification_condition: FalsificationCondition = Field(...)
    heritage_eval: HeritageCMFEval = Field(...)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
