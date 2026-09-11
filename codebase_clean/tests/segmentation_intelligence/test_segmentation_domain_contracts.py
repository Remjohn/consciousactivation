"""
test_segmentation_domain_contracts.py
-------------------------------------
Validates EvidenceSegment serialization, hash generation, and schema integrity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "segmentation-intelligence" / "src"))

from cae_segmentation_intelligence.domain import (
    EvidenceSegment,
    SemanticBoundaryType,
)
from cae_segmentation_intelligence.verifier import EvidenceSegmentVerifier


def test_evidence_segment_creation_and_hash_verification():
    text = "We realized that the metric was optimizing for short-term vanity rather than actual patient recovery."
    text_hash = EvidenceSegment.compute_text_hash(text)

    seg = EvidenceSegment(
        workspace_id="ws-client-99",
        session_id="SES-001",
        speaker="Dr. Thorne",
        start_time_ms=12000,
        end_time_ms=18500,
        verbatim_text=text,
        boundary_type=SemanticBoundaryType.REVEAL,
        text_sha256=text_hash,
    )

    assert seg.segment_id.startswith("SEG-")
    assert seg.boundary_type == SemanticBoundaryType.REVEAL
    assert EvidenceSegmentVerifier.verify_segment(seg) is True
