"""
segmenter.py
------------
Semantic Evidence Segmenter converting transcript streams into lossless EvidenceSegments.
"""

from __future__ import annotations

from typing import List, Optional

from .domain import (
    EvidenceSegment,
    SegmentContextDependency,
    SemanticBoundaryType,
    TranscriptSegmentationResult,
    TranscriptSourceRef,
)
from .errors import (
    NarrativeTruncationError,
    TimecodeDiscontinuityError,
)


class SemanticEvidenceSegmenter:
    """Segments continuous interview dialogue into complete, typed EvidenceSegments."""

    DANGLING_CONJUNCTIONS = {"and", "but", "or", "because", "so", "then", "which", "that", "although"}

    @classmethod
    def assert_thought_completion(cls, text: str) -> None:
        """Check that a segment does not end on a dangling mid-sentence conjunction."""
        cleaned = text.strip().rstrip(".!?,")
        tokens = cleaned.split()
        if tokens:
            last_token = tokens[-1].lower()
            if last_token in cls.DANGLING_CONJUNCTIONS:
                raise NarrativeTruncationError(
                    f"Narrative truncation detected: Segment text ends on dangling conjunction '{last_token}'. "
                    f"Segments must terminate at complete thought boundaries."
                )

    @classmethod
    def segment_turns(
        cls,
        *,
        workspace_id: str,
        session_id: str,
        source_ref: TranscriptSourceRef,
        raw_turns: List[dict],
    ) -> TranscriptSegmentationResult:
        """
        Convert raw timed speech turns into canonical EvidenceSegments.
        Each entry in raw_turns:
          { 'speaker': str, 'start_time_ms': int, 'end_time_ms': int, 'text': str, 'boundary_type': SemanticBoundaryType, 'has_context_dep': bool }
        """
        segments: List[EvidenceSegment] = []
        last_end_time = -1
        total_words = 0

        for idx, turn in enumerate(raw_turns):
            start = turn["start_time_ms"]
            end = turn["end_time_ms"]
            text = turn["text"].strip()
            speaker = turn["speaker"]
            b_type = turn.get("boundary_type", SemanticBoundaryType.THOUGHT_COMPLETION)
            has_dep = turn.get("has_context_dep", False)

            # Monotonic timecode check
            if start < 0 or end <= start:
                raise TimecodeDiscontinuityError(
                    f"Invalid timecodes on turn {idx}: start={start}ms, end={end}ms. End must be strictly greater than start."
                )
            if start < last_end_time:
                raise TimecodeDiscontinuityError(
                    f"Non-monotonic timecode on turn {idx}: start {start}ms overlaps previous segment ending at {last_end_time}ms."
                )

            # Thought completion check
            cls.assert_thought_completion(text)

            text_hash = EvidenceSegment.compute_text_hash(text)
            ctx_dep = SegmentContextDependency(
                has_antecedent_dependency=has_dep,
                preceding_context_summary=turn.get("context_summary"),
                required_antecedent_turn_id=turn.get("antecedent_turn_id"),
            )

            seg = EvidenceSegment(
                workspace_id=workspace_id,
                session_id=session_id,
                speaker=speaker,
                start_time_ms=start,
                end_time_ms=end,
                verbatim_text=text,
                boundary_type=b_type,
                text_sha256=text_hash,
                context_dependency=ctx_dep,
            )
            segments.append(seg)
            last_end_time = end
            total_words += len(text.split())

        return TranscriptSegmentationResult(
            workspace_id=workspace_id,
            source_ref=source_ref,
            segments=segments,
            total_segment_count=len(segments),
            total_word_count=total_words,
            is_lossless=True,
        )
