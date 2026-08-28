"""
cae_segmentation_intelligence
-----------------------------
The Evidence Segmentation and Semantic Boundary Preservation package for CAE.
"""

from .domain import (
    SemanticBoundaryType,
    TranscriptSourceRef,
    SegmentContextDependency,
    EvidenceSegment,
    TranscriptSegmentationResult,
)
from .errors import (
    SegmentationIntelligenceError,
    NarrativeTruncationError,
    DuplicateSegmentError,
    TimecodeDiscontinuityError,
    ProvenanceTamperError,
    PrematureAnnotationError,
)
from .segmenter import SemanticEvidenceSegmenter
from .verifier import EvidenceSegmentVerifier

__all__ = [
    "SemanticBoundaryType",
    "TranscriptSourceRef",
    "SegmentContextDependency",
    "EvidenceSegment",
    "TranscriptSegmentationResult",
    "SegmentationIntelligenceError",
    "NarrativeTruncationError",
    "DuplicateSegmentError",
    "TimecodeDiscontinuityError",
    "ProvenanceTamperError",
    "PrematureAnnotationError",
    "SemanticEvidenceSegmenter",
    "EvidenceSegmentVerifier",
]
