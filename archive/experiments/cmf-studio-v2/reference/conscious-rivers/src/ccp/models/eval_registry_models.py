"""
src/ccp/models/eval_registry_models.py
======================================
Pydantic v2 model definitions for FR-ERA3-35A Eval Registry and Scoring Taxonomy.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class MetricScale(str, Enum):
    """Irreducible format definitions for raw sensor or NLP model outputs."""
    PROBABILITY = "probability"  # 0.0 - 1.0
    PERCENTAGE = "percentage"    # 0.0 - 100.0
    DECIBELS = "decibels"        # Sound pressure level limits
    WORDS_PER_MINUTE = "wpm"     # Temporal speed measurement
    COUNT = "count"              # Natural integers


class VisibleFamilyKey(str, Enum):
    """The seven immutable score cards shown to the coach."""
    HUMANITY = "Humanity"
    PRESENCE = "Presence"
    TRUST = "Trust"
    MEMORABILITY = "Memorability"
    RESONANCE = "Resonance"
    SIGNAL = "Signal"
    AI_SLOP_RISK = "AI Slop Risk"


class HiddenClusterKey(str, Enum):
    """Support metric groups that govern weight calculations without public visibility."""
    STRUCTURE = "Structure"
    ACTIONABILITY = "Actionability"
    VISUAL_PROOF = "Visual Proof"
    CAPTION_ALIGNMENT = "Caption Alignment"
    TEMPORAL_CRAFT = "Temporal Craft"


class EvalDefinition(BaseModel):
    """Defines a single internal metric's constraints, sources, and conversion metadata."""
    metric_id: str = Field(..., pattern=r"^MET-[A-Z0-9_]{3,12}$")
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10)
    scale: MetricScale = Field(...)
    default_weight: float = Field(..., ge=0.0, le=1.0)
    is_active: bool = Field(default=True)

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, v: str) -> str:
        if not v.startswith("MET-"):
            raise ValueError("metric_id must begin with prefix 'MET-'")
        return v


class EvalCluster(BaseModel):
    """A logical grouping of internal metrics that maps to a visible score family."""
    cluster_id: str = Field(..., pattern=r"^CLU-[A-Z0-9_]{3,12}$")
    name: str = Field(..., min_length=3)
    target_family: VisibleFamilyKey = Field(...)
    metrics: List[EvalDefinition] = Field(..., min_length=1)
    cluster_description: str = Field(..., min_length=15)

    @model_validator(mode="after")
    def verify_metric_weights(self) -> EvalCluster:
        total_weight = sum(m.default_weight for m in self.metrics)
        if not (0.95 <= total_weight <= 1.05):
            raise ValueError(f"Sum of metric weights in cluster {self.cluster_id} must approximate 1.0 (got {total_weight})")
        return self


class VisibleScoreFamily(BaseModel):
    """Metadata and bounds configuration for the seven main public score cards."""
    family_key: VisibleFamilyKey = Field(...)
    primary_question: str = Field(..., min_length=10)
    base_color_hex: str = Field(..., pattern=r"^#[A-Fa-f0-9]{6}$")
    is_penalty_indicator: bool = Field(default=False)


class HiddenSupportCluster(BaseModel):
    """Metadata configurations for internal weighting adjustments."""
    cluster_key: HiddenClusterKey = Field(...)
    description: str = Field(..., min_length=10)
    influence_mappings: Dict[VisibleFamilyKey, float] = Field(...)

    @field_validator("influence_mappings")
    @classmethod
    def validate_influences(cls, v: Dict[VisibleFamilyKey, float]) -> Dict[VisibleFamilyKey, float]:
        for k, weight in v.items():
            if not (0.0 <= weight <= 1.0):
                raise ValueError(f"Influence weight for {k} must lie between 0.0 and 1.0")
        return v


class EvalMeasurement(BaseModel):
    """A single captured metric execution with its source raw value and its normalized equivalent."""
    metric_id: str = Field(...)
    raw_value: float = Field(...)
    normalized_score: int = Field(..., ge=0, le=99)
    captured_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class EvalPenaltyRule(BaseModel):
    """Configures overall score cap limits based on severe failures or high slop signals."""
    rule_id: str = Field(...)
    trigger_metric: VisibleFamilyKey = Field(...)
    threshold_value: int = Field(..., ge=0, le=99)
    cap_limit: int = Field(..., ge=0, le=99)
    penalty_multiplier: float = Field(default=1.0, ge=0.0, le=1.0)
    description: str = Field(...)


class EvalScoreProjection(BaseModel):
    """The computed outcome package consisting of all evaluated states and the immutable QA signature."""
    measurements: List[EvalMeasurement] = Field(...)
    visible_scores: Dict[VisibleFamilyKey, int] = Field(...)
    overall_score: int = Field(..., ge=0, le=99)
    is_internally_approved: bool = Field(default=False)
    qa_signature: Optional[str] = Field(None, description="Cryptographic or UUID signature indicating operator verification approval")

    @model_validator(mode="after")
    def verify_all_visible_families_present(self) -> EvalScoreProjection:
        for family in VisibleFamilyKey:
            if family not in self.visible_scores:
                raise ValueError(f"Missing required visible score family evaluation for {family.value}")
        return self
