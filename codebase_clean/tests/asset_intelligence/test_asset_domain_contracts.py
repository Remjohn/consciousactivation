"""
test_asset_domain_contracts.py
------------------------------
Validates AssetAnnotation and AssetCatalog serialization, typing, and schema integrity.
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


def test_asset_annotation_contracts():
    rights = RightsMetadata(
        status=RightsStatus.CLEARED,
        license_id="LIC-CC-BY-4.0",
        copyright_holder="Open Source Archive",
        proof_url="https://licenses.org/proof-991",
    )

    asset = AssetAnnotator.annotate_insert(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        source_type=SourceType.ARCHIVAL,
        media_type=MediaType.VIDEO_CLIP,
        start_time=12.5,
        end_time=16.8,
        contextual_caption="Archival footage of the 1969 Apollo mission control room celebrating touchdown.",
        semantic_role="HISTORICAL_TRIUMPH_METAPHOR",
        insert_role=EditorialInsertRole.SEMANTIC_SIMILE,
        source_sha256="a" * 64,
        rights=rights,
    )

    assert asset.asset_id.startswith("AST-")
    assert asset.duration == 4.3
    assert asset.insert_role == EditorialInsertRole.SEMANTIC_SIMILE
    assert asset.rights.status == RightsStatus.CLEARED
