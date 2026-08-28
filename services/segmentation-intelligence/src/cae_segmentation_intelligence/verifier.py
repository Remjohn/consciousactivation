"""
verifier.py
-----------
Verification and gating logic for Evidence Segments and full transcript reconstructions (CAE-M05).
"""

from __future__ import annotations

import hashlib
from typing import List

from .domain import (
    EvidenceSegment,
    TranscriptSegmentationResult,
)
from .errors import (
    DuplicateSegmentError,
    NarrativeTruncationError,
    ProvenanceTamperError,
    TimecodeDiscontinuityError,
)


class EvidenceSegmentVerifier:
    """Enforces lossless reconstruction, timecode monotonicity, and cryptographic integrity on segments."""

    @classmethod
    def verify_segment(cls, segment: EvidenceSegment) -> bool:
        """Verify an individual EvidenceSegment's internal integrity."""
        # Timecode validity
        if segment.start_time_ms < 0 or segment.end_time_ms <= segment.start_time_ms:
            raise TimecodeDiscontinuityError(
                f"Segment '{segment.segment_id}' has invalid time range: {segment.start_time_ms}ms to {segment.end_time_ms}ms."
            )

        # Hash integrity
        expected_hash = EvidenceSegment.compute_text_hash(segment.verbatim_text)
        if segment.text_sha256 != expected_hash:
            raise ProvenanceTamperError(
                f"Segment '{segment.segment_id}' text hash mismatch: expected {expected_hash}, got {segment.text_sha256}."
            )

        return True

    @classmethod
    def verify_segmentation_result(cls, result: TranscriptSegmentationResult, raw_source_text: str) -> bool:
        """
        Validates an entire TranscriptSegmentationResult against the raw source transcript.
        Enforces lossless concatenation, unique segment IDs, and monotonic timecodes.
        """
        seen_ids = set()
        last_end_time = -1
        reconstructed_tokens: List[str] = []

        for seg in result.segments:
            # 1. Uniqueness check
            if seg.segment_id in seen_ids:
                raise DuplicateSegmentError(f"Duplicate segment ID detected: {seg.segment_id}")
            seen_ids.add(seg.segment_id)

            # 2. Individual segment check
            cls.verify_segment(seg)

            # 3. Monotonic timecodes
            if seg.start_time_ms < last_end_time:
                raise TimecodeDiscontinuityError(
                    f"Timecode discontinuity: Segment '{seg.segment_id}' start ({seg.start_time_ms}ms) "
                    f"overlaps previous segment end ({last_end_time}ms)."
                )
            last_end_time = seg.end_time_ms

            reconstructed_tokens.append(seg.verbatim_text.strip())

        # 4. Lossless text concatenation verification
        concatenated_text = " ".join(reconstructed_tokens)
        source_tokens = " ".join(raw_source_text.strip().split())

        concatenated_hash = hashlib.sha256(concatenated_text.encode("utf-8")).hexdigest()
        source_hash = hashlib.sha256(source_tokens.encode("utf-8")).hexdigest()

        if concatenated_hash != source_hash:
            raise ProvenanceTamperError(
                f"Lossless transcript verification failed! Reconstructed text hash ({concatenated_hash}) "
                f"does not match source transcript hash ({source_hash})."
            )

        return True
