"""
domain.py
---------
Canonical domain contracts for Evidence Segmentation (CAE-M05).
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SemanticBoundaryType(str, Enum):
    THOUGHT_COMPLETION = "THOUGHT_COMPLETION"
    STORY_TURN = "STORY_TURN"
    MECHANISM_TRANSITION = "MECHANISM_TRANSITION"
    CONTRADICTION = "CONTRADICTION"
    REVEAL = "REVEAL"
    EMOTIONAL_SHIFT = "EMOTIONAL_SHIFT"


class TranscriptSourceRef(BaseModel):
    """Immutable provenance reference linking segments back to source media & transcript."""
    source_uri: str = Field(..., description="Canonical path or URI of source audio/video transcript")
    media_sha256: str = Field(..., min_length=64, max_length=64, description="SHA-256 of media file")
    transcript_sha256: str = Field(..., min_length=64, max_length=64, description="SHA-256 of raw text transcript")
    total_duration_ms: int = Field(..., gt=0, description="Total media duration in milliseconds")
    session_id: str = Field(..., description="Linked InterviewSession ID")


class SegmentContextDependency(BaseModel):
    """Captures conversational context needed to resolve indexical references."""
    has_antecedent_dependency: bool = Field(False)
    preceding_context_summary: Optional[str] = Field(None, description="Brief note on antecedent referent")
    required_antecedent_turn_id: Optional[str] = Field(None, description="ID of preceding turn")


class EvidenceSegment(BaseModel):
    """
    The canonical, lossless excerpt entity derived from an interview transcript.
    Preserves exact verbatim speech, millisecond boundaries, and semantic categorization.
    """
    segment_id: str = Field(default_factory=lambda: f"SEG-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(..., description="Tenant isolation anchor")
    session_id: str = Field(..., description="Linked InterviewSession ID")
    speaker: str = Field(..., min_length=2, description="Speaker name or tag, e.g. 'Guest', 'Host'")
    
    start_time_ms: int = Field(..., ge=0, description="Start offset in milliseconds")
    end_time_ms: int = Field(..., gt=0, description="End offset in milliseconds")
    verbatim_text: str = Field(..., min_length=5, description="Exact un-rewritten speech transcript")
    
    boundary_type: SemanticBoundaryType = Field(...)
    text_sha256: str = Field(..., min_length=64, max_length=64)
    context_dependency: SegmentContextDependency = Field(default_factory=SegmentContextDependency)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def compute_text_hash(cls, text: str) -> str:
        """Compute standard SHA-256 hash of verbatim segment text."""
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


class TranscriptSegmentationResult(BaseModel):
    """The complete, lossless collection of EvidenceSegments for an interview session."""
    result_id: str = Field(default_factory=lambda: f"SGR-{uuid.uuid4().hex[:12]}")
    workspace_id: str = Field(...)
    source_ref: TranscriptSourceRef = Field(...)
    segments: List[EvidenceSegment] = Field(..., min_length=1)
    
    total_segment_count: int = Field(...)
    total_word_count: int = Field(...)
    is_lossless: bool = Field(True, description="True if verbatim text concatenation matches source hash")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
