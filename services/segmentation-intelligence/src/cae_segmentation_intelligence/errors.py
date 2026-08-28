"""
errors.py
---------
Structured error taxonomy for Evidence Segmentation (CAE-M05).
"""

class SegmentationIntelligenceError(Exception):
    """Base exception for all segmentation intelligence failures."""
    pass


class NarrativeTruncationError(SegmentationIntelligenceError):
    """Raised when fixed-window or mechanical chunking truncates a sentence or narrative beat mid-thought."""
    pass


class DuplicateSegmentError(SegmentationIntelligenceError):
    """Raised when duplicate segment IDs or overlapping verbatim text fragments are generated."""
    pass


class TimecodeDiscontinuityError(SegmentationIntelligenceError):
    """Raised when start/end timecodes are inverted, negative, or non-monotonic across sequential segments."""
    pass


class ProvenanceTamperError(SegmentationIntelligenceError):
    """Raised when segment verbatim text fails SHA-256 integrity verification against source transcript."""
    pass


class PrematureAnnotationError(SegmentationIntelligenceError):
    """Raised when word-by-word captioning or candidate scoring is prematurely attempted on full transcripts."""
    pass
