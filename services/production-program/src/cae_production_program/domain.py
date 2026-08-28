"""
domain.py
---------
Canonical domain models for Production Semantic Program & Handoff Receipts (CAE-M11).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


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
    sfl_profile: SFLModulationProfile = Field(default_factory=SFLModulationProfile)


class SemanticProgram(BaseModel):
    """Complete, typed semantic program compiled for downstream CMF video realization."""
    program_id: str = Field(default_factory=lambda: f"PRG-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    title: str = Field(..., min_length=3)
    semantic_intent: str = Field(..., min_length=10)
    story_arc: str = Field(...)
    scenes: List[SemanticSceneSpec] = Field(..., min_length=1)
    total_duration: float = Field(..., ge=1.0)
    visual_audio_specs: VisualAudioSpecs = Field(default_factory=VisualAudioSpecs)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CompositionHandoffReceipt(BaseModel):
    """Auditable cryptographic receipt verifying compiler handoff to downstream renderers."""
    receipt_id: str = Field(default_factory=lambda: f"PRG-RCP-{uuid.uuid4().hex[:12]}")
    program_id: str = Field(...)
    candidate_id: str = Field(...)
    compiler_version: str = Field(default="1.0.0")
    evidence_sha256_list: List[str] = Field(..., min_length=1)
    asset_id_list: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
