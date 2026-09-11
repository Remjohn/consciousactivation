"""
test_lossless_transcript_integrity_and_provenance.py
----------------------------------------------------
Tests that segmented transcript chunks reconstruct 100% of the raw source text with SHA-256 verification.
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
from cae_segmentation_intelligence.verifier import EvidenceSegmentVerifier


def test_lossless_transcript_reconstruction():
    t1 = "When I first stepped into the founder role, I believed leadership was about having all the right answers."
    t2 = "Three years of scaling through market downturns completely shattered that illusion."
    t3 = "Real leadership is creating an environment where truth travels faster than fear."

    raw_source = f"{t1} {t2} {t3}"
    source_hash = hashlib.sha256(raw_source.encode("utf-8")).hexdigest()

    source_ref = TranscriptSourceRef(
        source_uri="s3://conscious-media/raw/session_002.mp4",
        media_sha256="b" * 64,
        transcript_sha256=source_hash,
        total_duration_ms=45000,
        session_id="SES-002",
    )

    raw_turns = [
        {
            "speaker": "Guest",
            "start_time_ms": 0,
            "end_time_ms": 14000,
            "text": t1,
            "boundary_type": SemanticBoundaryType.THOUGHT_COMPLETION,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 14500,
            "end_time_ms": 28000,
            "text": t2,
            "boundary_type": SemanticBoundaryType.STORY_TURN,
        },
        {
            "speaker": "Guest",
            "start_time_ms": 28500,
            "end_time_ms": 45000,
            "text": t3,
            "boundary_type": SemanticBoundaryType.REVEAL,
        },
    ]

    result = SemanticEvidenceSegmenter.segment_turns(
        workspace_id="ws-client-99",
        session_id="SES-002",
        source_ref=source_ref,
        raw_turns=raw_turns,
    )

    assert EvidenceSegmentVerifier.verify_segmentation_result(result, raw_source) is True
