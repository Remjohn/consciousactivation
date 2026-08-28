"""
test_semantic_boundary_segmentation.py
--------------------------------------
Tests segmentation across all 6 canonical semantic boundary types.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "segmentation-intelligence" / "src"))

from cae_segmentation_intelligence.domain import (
    SemanticBoundaryType,
    TranscriptSourceRef,
)
from cae_segmentation_intelligence.segmenter import SemanticEvidenceSegmenter


def test_multi_boundary_segmentation():
    raw_text = (
        "In 2021 we launched the new surgical workflow. "
        "And then three months later, the first major system failure occurred. "
        "The reason this happened was that the communication handoff had no verification step. "
        "Everyone assumed the senior nurse signed off, but the records were completely blank. "
        "What I never told the board was that we almost lost two patients that night. "
        "After that moment, I could never look at our safety metrics the same way again."
    )

    source_ref = TranscriptSourceRef(
        source_uri="s3://conscious-media/raw/session_001.mp4",
        media_sha256="a" * 64,
        transcript_sha256=hashlib.sha256(raw_text.encode("utf-8")).hexdigest(),
        total_duration_ms=60000,
        session_id="SES-001",
    )

    raw_turns = [
        {
            "speaker": "Guest",
            "start_time_ms": 0,
            "end_time_ms": 8000,
            "text": "In 2021 we launched the new surgical workflow.",
            "boundary_type": SemanticBoundaryType.ORIENTATION if hasattr(SemanticBoundaryType, 'ORIENTATION') else SemanticBoundaryType.THOUGHT_COMPLETION,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 8500,
            "end_time_ms": 17000,
            "text": "And then three months later, the first major system failure occurred.",
            "boundary_type": SemanticBoundaryType.STORY_TURN,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 17500,
            "end_time_ms": 28000,
            "text": "The reason this happened was that the communication handoff had no verification step.",
            "boundary_type": SemanticBoundaryType.MECHANISM_TRANSITION,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 28500,
            "end_time_ms": 38000,
            "text": "Everyone assumed the senior nurse signed off, but the records were completely blank.",
            "boundary_type": SemanticBoundaryType.CONTRADICTION,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 38500,
            "end_time_ms": 49000,
            "text": "What I never told the board was that we almost lost two patients that night.",
            "boundary_type": SemanticBoundaryType.REVEAL,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 49500,
            "end_time_ms": 60000,
            "text": "After that moment, I could never look at our safety metrics the same way again.",
            "boundary_type": SemanticBoundaryType.EMOTIONAL_SHIFT,
        },
    ]

    res = SemanticEvidenceSegmenter.segment_turns(
        workspace_id="ws-client-99",
        session_id="SES-001",
        source_ref=source_ref,
        raw_turns=raw_turns,
    )

    assert res.total_segment_count == 6
    assert res.segments[1].boundary_type == SemanticBoundaryType.STORY_TURN
    assert res.segments[2].boundary_type == SemanticBoundaryType.MECHANISM_TRANSITION
    assert res.segments[3].boundary_type == SemanticBoundaryType.CONTRADICTION
    assert res.segments[4].boundary_type == SemanticBoundaryType.REVEAL
    assert res.segments[5].boundary_type == SemanticBoundaryType.EMOTIONAL_SHIFT
