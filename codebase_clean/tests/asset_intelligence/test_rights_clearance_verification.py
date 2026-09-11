"""
test_rights_clearance_verification.py
-------------------------------------
Tests rights metadata validation and ensures unverified assets cannot be marked CLEARED without proof.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "asset-intelligence" / "src"))

import pytest

from cae_asset_intelligence.annotator import AssetAnnotator
from cae_asset_intelligence.domain import (
    EditorialInsertRole,
    MediaType,
    RightsMetadata,
    RightsStatus,
    SourceType,
)
from cae_asset_intelligence.errors import MissingRightsEvidenceError


def test_unverified_cleared_rights_rejection():
    # Attempting to mark rights CLEARED with no proof URL and no license ID
    invalid_rights = RightsMetadata(
        status=RightsStatus.CLEARED,
        license_id=None,
        proof_url=None,  # VIOLATION!
    )

    with pytest.raises(MissingRightsEvidenceError, match="must provide a valid license_id or proof_url"):
        AssetAnnotator.annotate_insert(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            source_type=SourceType.MOVIE,
            media_type=MediaType.VIDEO_CLIP,
            start_time=10.0,
            end_time=14.0,
            contextual_caption="A movie moment illustrating dramatic realization and suspense.",
            semantic_role="DRAMATIC_SUSPENSE",
            insert_role=EditorialInsertRole.EMOTIONAL_AMPLIFICATION,
            source_sha256="c" * 64,
            rights=invalid_rights,
        )
