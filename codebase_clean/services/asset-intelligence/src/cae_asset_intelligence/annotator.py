"""
annotator.py
------------
Annotator for reusable production assets and E/D-roll inserts (CAE-M10).
"""

from __future__ import annotations

import re
from typing import Optional

from .domain import (
    AssetAnnotation,
    AssetCatalog,
    EditorialInsertRole,
    MediaType,
    RightsMetadata,
    RightsStatus,
    SourceType,
)
from .errors import (
    DurationConstraintViolationError,
    GenericCaptionRejectedError,
    MissingRightsEvidenceError,
)


class AssetAnnotator:
    """Builds deep AssetAnnotation objects for approved candidates with strict quality gates."""

    GENERIC_PATTERNS = [
        r"^a person (talking|speaking|smiling)$",
        r"^a man (talking|sitting)$",
        r"^a woman (talking|sitting)$",
        r"^a video clip$",
        r"^b-roll footage$",
        r"^stock footage$",
    ]

    @classmethod
    def annotate_insert(
        cls,
        *,
        candidate_id: str,
        workspace_id: str,
        source_type: SourceType,
        media_type: MediaType,
        start_time: float,
        end_time: float,
        contextual_caption: str,
        semantic_role: str,
        insert_role: EditorialInsertRole,
        source_sha256: str,
        rights: RightsMetadata,
        allow_extended_duration: bool = False,
    ) -> AssetAnnotation:
        """Annotates an E/D-roll insert asset with duration and contextual quality validation."""
        duration = round(end_time - start_time, 2)
        if duration <= 0:
            raise ValueError(f"end_time ({end_time}) must be strictly greater than start_time ({start_time}).")

        # 1. Duration Constraint Gate (3.0s - 6.0s preference for inserts)
        if not allow_extended_duration and (duration < 2.0 or duration > 8.0):
            raise DurationConstraintViolationError(
                f"Insert duration {duration}s violates preference (expected 3.0s - 6.0s, tolerance [2.0s, 8.0s])."
            )

        # 2. Generic Caption Rejection Gate
        normalized_caption = contextual_caption.strip().lower()
        for pattern in cls.GENERIC_PATTERNS:
            if re.match(pattern, normalized_caption):
                raise GenericCaptionRejectedError(
                    f"Caption '{contextual_caption}' is too shallow/generic. Must provide semantic narrative context."
                )

        # 3. Rights Clearance Evidence Gate
        if rights.status == RightsStatus.CLEARED and not rights.proof_url and not rights.license_id:
            raise MissingRightsEvidenceError(
                "Assets marked CLEARED must provide a valid license_id or proof_url documentation."
            )

        return AssetAnnotation(
            candidate_id=candidate_id,
            workspace_id=workspace_id,
            source_type=source_type,
            media_type=media_type,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            contextual_caption=contextual_caption,
            semantic_role=semantic_role,
            insert_role=insert_role,
            source_sha256=source_sha256,
            rights=rights,
        )
