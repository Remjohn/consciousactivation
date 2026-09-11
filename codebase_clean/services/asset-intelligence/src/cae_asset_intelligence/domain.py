"""
domain.py
---------
Canonical domain models for Multimodal Asset Intelligence and E/D-Roll (CAE-M10).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    REAL_WORLD = "REAL_WORLD"
    PREVIOUS_INTERVIEW = "PREVIOUS_INTERVIEW"
    ARCHIVAL = "ARCHIVAL"
    MOVIE = "MOVIE"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    CULTURAL = "CULTURAL"


class MediaType(str, Enum):
    VIDEO_CLIP = "VIDEO_CLIP"
    AUDIO_BITE = "AUDIO_BITE"
    STILL_IMAGE = "STILL_IMAGE"
    MOTION_GRAPHIC = "MOTION_GRAPHIC"


class EditorialInsertRole(str, Enum):
    SEMANTIC_SIMILE = "SEMANTIC_SIMILE"
    PATTERN_MATCH = "PATTERN_MATCH"
    PATTERN_INTERRUPT = "PATTERN_INTERRUPT"
    COMEDIC_PUNCTUATION = "COMEDIC_PUNCTUATION"
    FORESHADOWING = "FORESHADOWING"
    CONTRAST = "CONTRAST"
    CULTURAL_RECOGNITION = "CULTURAL_RECOGNITION"
    EMOTIONAL_AMPLIFICATION = "EMOTIONAL_AMPLIFICATION"
    WORLD_BUILDING = "WORLD_BUILDING"


class RightsStatus(str, Enum):
    CLEARED = "CLEARED"
    FAIR_USE_LEGAL_REVIEW_REQUIRED = "FAIR_USE_LEGAL_REVIEW_REQUIRED"
    RESTRICTED = "RESTRICTED"
    UNKNOWN_UNLICENSED = "UNKNOWN_UNLICENSED"


class RightsMetadata(BaseModel):
    """Legal rights and clearance verification for a production media asset."""
    status: RightsStatus = Field(...)
    license_id: Optional[str] = Field(None)
    copyright_holder: Optional[str] = Field(None)
    proof_url: Optional[str] = Field(None)
    allowed_territories: List[str] = Field(default_factory=lambda: ["GLOBAL"])
    notes: Optional[str] = Field(None)


class AssetAnnotation(BaseModel):
    """Deep annotation of a selected reusable media asset for production insertion."""
    asset_id: str = Field(default_factory=lambda: f"AST-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    source_type: SourceType = Field(...)
    media_type: MediaType = Field(...)
    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., ge=0.0)
    duration: float = Field(..., ge=0.0)
    contextual_caption: str = Field(..., min_length=15, description="Contextual semantic description")
    semantic_role: str = Field(..., min_length=3)
    insert_role: EditorialInsertRole = Field(...)
    source_sha256: str = Field(..., min_length=64, max_length=64)
    rights: RightsMetadata = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AssetCatalog(BaseModel):
    """Collection of verified media assets curated for an approved candidate."""
    catalog_id: str = Field(default_factory=lambda: f"CAT-{uuid.uuid4().hex[:12]}")
    candidate_id: str = Field(...)
    workspace_id: str = Field(...)
    assets: List[AssetAnnotation] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
