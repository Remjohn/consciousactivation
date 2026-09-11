"""
test_asset_adversarial_cases.py
-------------------------------
Adversarial tests for byte hash mismatches, generic captions, and duration constraint violations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "asset-intelligence" / "src"))

import pytest

from cae_asset_intelligence.annotator import AssetAnnotator
from cae_asset_intelligence.domain import (
    AssetCatalog,
    EditorialInsertRole,
    MediaType,
    RightsMetadata,
    RightsStatus,
    SourceType,
)
from cae_asset_intelligence.errors import (
    AssetByteHashMismatchError,
    DurationConstraintViolationError,
    GenericCaptionRejectedError,
    MissingRightsEvidenceError,
)
from cae_asset_intelligence.verifier import AssetIntelligenceVerifier


def test_byte_hash_mismatch_rejection():
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-1", proof_url="https://proof")

    asset = AssetAnnotator.annotate_insert(
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        source_type=SourceType.REAL_WORLD,
        media_type=MediaType.VIDEO_CLIP,
        start_time=0.0,
        end_time=4.0,
        contextual_caption="Authentic field recording of engineering test bench under stress.",
        semantic_role="ENGINEERING_PROOF",
        insert_role=EditorialInsertRole.PATTERN_MATCH,
        source_sha256="d" * 64,
        rights=rights,
    )

    tampered_bytes = b"tampered media file contents that don't match dddd... hash"

    with pytest.raises(AssetByteHashMismatchError, match="hash mismatch"):
        AssetIntelligenceVerifier.verify_media_bytes(asset, tampered_bytes)


def test_generic_caption_rejection():
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-1", proof_url="https://proof")

    with pytest.raises(GenericCaptionRejectedError, match="too shallow/generic"):
        AssetAnnotator.annotate_insert(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            source_type=SourceType.REAL_WORLD,
            media_type=MediaType.VIDEO_CLIP,
            start_time=0.0,
            end_time=4.0,
            contextual_caption="a person talking",  # VIOLATION: generic shallow caption
            semantic_role="TEST",
            insert_role=EditorialInsertRole.SEMANTIC_SIMILE,
            source_sha256="e" * 64,
            rights=rights,
        )


def test_insert_duration_violation():
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-1", proof_url="https://proof")

    with pytest.raises(DurationConstraintViolationError, match="violates preference"):
        AssetAnnotator.annotate_insert(
            candidate_id="CND-001",
            workspace_id="ws-client-99",
            source_type=SourceType.REAL_WORLD,
            media_type=MediaType.VIDEO_CLIP,
            start_time=0.0,
            end_time=15.0,  # VIOLATION: 15 seconds insert duration!
            contextual_caption="Detailed footage of an assembly line running at full capacity.",
            semantic_role="PRODUCTION_SCALE",
            insert_role=EditorialInsertRole.WORLD_BUILDING,
            source_sha256="f" * 64,
            rights=rights,
            allow_extended_duration=False,
        )
