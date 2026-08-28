"""
test_segmentation_adversarial_cases.py
--------------------------------------
Adversarial tests for mid-thought cuts, shifted timecodes, duplicate segments, and tampered transcript text.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "segmentation-intelligence" / "src"))

import pytest

from cae_segmentation_intelligence.domain import (
    EvidenceSegment,
    SemanticBoundaryType,
    TranscriptSegmentationResult,
    TranscriptSourceRef,
)
from cae_segmentation_intelligence.errors import (
    DuplicateSegmentError,
    NarrativeTruncationError,
    ProvenanceTamperError,
    TimecodeDiscontinuityError,
)
from cae_segmentation_intelligence.segmenter import SemanticEvidenceSegmenter
from cae_segmentation_intelligence.verifier import EvidenceSegmentVerifier


def test_dangling_mid_thought_truncation_rejection():
    # Attempting to slice a segment that ends on a dangling conjunction "and then"
    source_ref = TranscriptSourceRef(
        source_uri="s3://conscious-media/raw/session_999.mp4",
        media_sha256="c" * 64,
        transcript_sha256="d" * 64,
        total_duration_ms=10000,
        session_id="SES-999",
    )

    raw_turns = [
        {
            "speaker": "Guest",
            "start_time_ms": 0,
            "end_time_ms": 5000,
            "text": "We walked into the boardroom and then",  # Dangling!
            "boundary_type": SemanticBoundaryType.THOUGHT_COMPLETION,
        }
    ]

    with pytest.raises(NarrativeTruncationError, match="Narrative truncation detected"):
        SemanticEvidenceSegmenter.segment_turns(
            workspace_id="ws-client-99",
            session_id="SES-999",
            source_ref=source_ref,
            raw_turns=raw_turns,
        )


def test_timecode_discontinuity_rejection():
    # Segment 2 starts at 3000ms while Segment 1 ends at 5000ms (overlap / backwards skip)
    source_ref = TranscriptSourceRef(
        source_uri="s3://conscious-media/raw/session_999.mp4",
        media_sha256="c" * 64,
        transcript_sha256="d" * 64,
        total_duration_ms=10000,
        session_id="SES-999",
    )

    raw_turns = [
        {
            "speaker": "Guest",
            "start_time_ms": 0,
            "end_time_ms": 5000,
            "text": "First complete sentence here.",
            "boundary_type": SemanticBoundaryType.THOUGHT_COMPLETION,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 3000,  # Overlap!
            "end_time_ms": 8000,
            "text": "Second complete sentence here.",
            "boundary_type": SemanticBoundaryType.THOUGHT_COMPLETION,
        },
    ]

    with pytest.raises(TimecodeDiscontinuityError, match="Non-monotonic timecode"):
        SemanticEvidenceSegmenter.segment_turns(
            workspace_id="ws-client-99",
            session_id="SES-999",
            source_ref=source_ref,
            raw_turns=raw_turns,
        )


def test_tampered_transcript_text_rejection():
    text = "Exact verbatim quote from guest."
    correct_hash = EvidenceSegment.compute_text_hash(text)
    tampered_hash = "0" * 64

    seg = EvidenceSegment(
        workspace_id="ws-client-99",
        session_id="SES-001",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=5000,
        verbatim_text=text,
        boundary_type=SemanticBoundaryType.THOUGHT_COMPLETION,
        text_sha256=tampered_hash,  # Tampered!
    )

    with pytest.raises(ProvenanceTamperError, match="text hash mismatch"):
        EvidenceSegmentVerifier.verify_segment(seg)


def test_duplicate_segment_id_rejection():
    text = "Valid verbatim sentence."
    seg1 = EvidenceSegment(
        segment_id="SEG-DUPLICATE-ID",
        workspace_id="ws-client-99",
        session_id="SES-001",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=5000,
        verbatim_text=text,
        boundary_type=SemanticBoundaryType.THOUGHT_COMPLETION,
        text_sha256=EvidenceSegment.compute_text_hash(text),
    )

    seg2 = EvidenceSegment(
        segment_id="SEG-DUPLICATE-ID",  # Duplicate!
        workspace_id="ws-client-99",
        session_id="SES-001",
        speaker="Guest",
        start_time_ms=6000,
        end_time_ms=10000,
        verbatim_text=text,
        boundary_type=SemanticBoundaryType.THOUGHT_COMPLETION,
        text_sha256=EvidenceSegment.compute_text_hash(text),
    )

    source_ref = TranscriptSourceRef(
        source_uri="s3://uri",
        media_sha256="c" * 64,
        transcript_sha256="d" * 64,
        total_duration_ms=10000,
        session_id="SES-001",
    )

    result = TranscriptSegmentationResult(
        workspace_id="ws-client-99",
        source_ref=source_ref,
        segments=[seg1, seg2],
        total_segment_count=2,
        total_word_count=6,
        is_lossless=True,
    )

    with pytest.raises(DuplicateSegmentError, match="Duplicate segment ID detected"):
        EvidenceSegmentVerifier.verify_segmentation_result(result, f"{text} {text}")
