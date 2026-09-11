"""
domain.py
---------
Canonical domain models for Production Semantic Program & Handoff Receipts (CAE-M11).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, model_validator


class SceneRole(str, Enum):
    HOOK_INTERRUPT = "HOOK_INTERRUPT"
    NARRATIVE_SETUP = "NARRATIVE_SETUP"
    TENSION_EXPOSURE = "TENSION_EXPOSURE"
    EVIDENCE_CLIMAX = "EVIDENCE_CLIMAX"
    INSIGHT_RESOLUTION = "INSIGHT_RESOLUTION"
    CLOSING_CALL_TO_AWARENESS = "CLOSING_CALL_TO_AWARENESS"


class SFLModulationProfile(BaseModel):
    """Systemic Functional Linguistics register modulation for visual & kinetic pacing."""
    pacing_multiplier: float = Field(default=1.0, ge=0.5, le=2.0)
    kinetic_typography: bool = Field(default=True)
    pause_duration_seconds: float = Field(default=0.0, ge=0.0, le=5.0)
    color_grade_tone: str = Field(default="NEUTRAL_HIGH_CONTRAST")


class VisualAudioSpecs(BaseModel):
    """Target visual framing and audio mixing constraints."""
    aspect_ratio: str = Field(default="9:16")
    subtitle_font: str = Field(default="Inter Bold")
    background_music_ducking: float = Field(default=0.25, ge=0.0, le=1.0)
    transition_style: str = Field(default="HARD_CUT")


class AssetDemandSpec(BaseModel):
    """Declarative physical-media requirement emitted by a semantic scene.

    This is a requirement, not a selected asset. Runtime consumers may validate
    a candidate asset against these constraints but may not infer a new semantic
    obligation from the asset itself.
    """
    demand_key: str = Field(..., min_length=1)
    media_type: Literal["VIDEO_CLIP", "AUDIO_BITE", "STILL_IMAGE", "MOTION_GRAPHIC"]
    source_type: Literal[
        "REAL_WORLD",
        "PREVIOUS_INTERVIEW",
        "ARCHIVAL",
        "MOVIE",
        "SOCIAL_MEDIA",
        "CULTURAL",
    ]
    insert_role: str = Field(..., min_length=3)
    semantic_role: str = Field(..., min_length=3)
    semantic_obligation: str = Field(..., min_length=10)
    min_duration_seconds: float = Field(..., gt=0.0)
    max_duration_seconds: float = Field(..., gt=0.0)
    preferred_duration_seconds: Optional[float] = Field(None, gt=0.0)
    rights_statuses: List[str] = Field(..., min_length=1)
    allowed_territories: List[str] = Field(default_factory=lambda: ["GLOBAL"], min_length=1)
    license_required: bool = False
    evidence_ref: str = Field(..., min_length=1)
    evidence_sha256: str = Field(..., min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_duration_constraints(self) -> "AssetDemandSpec":
        if self.min_duration_seconds > self.max_duration_seconds:
            raise ValueError("min_duration_seconds cannot exceed max_duration_seconds")
        if self.preferred_duration_seconds is not None and not (
            self.min_duration_seconds
            <= self.preferred_duration_seconds
            <= self.max_duration_seconds
        ):
            raise ValueError("preferred_duration_seconds must be inside the duration range")
        return self

    @property
    def duration_is_valid(self) -> bool:
        return True


class SemanticSceneSpec(BaseModel):
    """Atomic scene blueprint binding spoken evidence, E/D-roll inserts, and SFL styling."""
    scene_index: int = Field(..., ge=1)
    scene_role: SceneRole = Field(...)
    segment_id: str = Field(...)
    spoken_text: str = Field(..., min_length=5)
    text_sha256: str = Field(..., min_length=64, max_length=64)
    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., ge=0.0)
    duration: float = Field(..., ge=0.0)
    asset_inserts: List[Dict[str, Any]] = Field(default_factory=list)
    asset_demands: List[AssetDemandSpec] = Field(default_factory=list)
    sfl_profile: SFLModulationProfile = Field(default_factory=SFLModulationProfile)


class SemanticProgram(BaseModel):
    """Complete, typed semantic program compiled for downstream CMF video realization."""
    program_id: str = Field(default_factory=lambda: f"PRG-{uuid.uuid4().hex[:12]}")
    program_version: str = Field(default="1.0.0")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    storyboard_id: Optional[str] = None
    title: str = Field(..., min_length=3)
    semantic_intent: str = Field(..., min_length=10)
    story_arc: str = Field(...)
    scenes: List[SemanticSceneSpec] = Field(..., min_length=1)
    total_duration: float = Field(..., ge=1.0)
    visual_audio_specs: VisualAudioSpecs = Field(default_factory=VisualAudioSpecs)
    wrong_reading_locks: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CompositionHandoffReceipt(BaseModel):
    """Auditable cryptographic receipt verifying compiler handoff to downstream renderers."""
    receipt_id: str = Field(default_factory=lambda: f"PRG-RCP-{uuid.uuid4().hex[:12]}")
    program_id: str = Field(...)
    candidate_id: str = Field(...)
    storyboard_id: Optional[str] = None
    compiler_version: str = Field(default="1.0.0")
    evidence_sha256_list: List[str] = Field(..., min_length=1)
    asset_id_list: List[str] = Field(default_factory=list)
    wrong_reading_locks: List[str] = Field(default_factory=list)
    receipt_sha256: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
