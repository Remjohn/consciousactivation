"""
test_edroll_insert_roles.py
---------------------------
Tests annotation across all 9 canonical E/D-roll insert roles.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "asset-intelligence" / "src"))

from cae_asset_intelligence.annotator import AssetAnnotator
from cae_asset_intelligence.domain import (
    EditorialInsertRole,
    MediaType,
    RightsMetadata,
    RightsStatus,
    SourceType,
)


def test_all_nine_insert_roles():
    rights = RightsMetadata(
        status=RightsStatus.CLEARED,
        license_id="LIC-INTERNAL-001",
        proof_url="https://internal.vault/proof/1",
    )

    roles = [
        EditorialInsertRole.SEMANTIC_SIMILE,
        EditorialInsertRole.PATTERN_MATCH,
        EditorialInsertRole.PATTERN_INTERRUPT,
        EditorialInsertRole.COMEDIC_PUNCTUATION,
        EditorialInsertRole.FORESHADOWING,
        EditorialInsertRole.CONTRAST,
        EditorialInsertRole.CULTURAL_RECOGNITION,
        EditorialInsertRole.EMOTIONAL_AMPLIFICATION,
        EditorialInsertRole.WORLD_BUILDING,
    ]

    for role in roles:
        asset = AssetAnnotator.annotate_insert(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            source_type=SourceType.REAL_WORLD,
            media_type=MediaType.VIDEO_CLIP,
            start_time=0.0,
            end_time=4.5,
            contextual_caption=f"Contextual illustration demonstrating {role.value} for candidate story arc.",
            semantic_role="NARRATIVE_ENHANCEMENT",
            insert_role=role,
            source_sha256="b" * 64,
            rights=rights,
        )
        assert asset.insert_role == role
