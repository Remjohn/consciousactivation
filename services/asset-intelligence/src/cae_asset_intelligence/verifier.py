"""
verifier.py
-----------
Verification logic for media asset byte integrity, rights evidence, and catalog coherence (CAE-M10).
"""

from __future__ import annotations

import hashlib
from typing import Optional

from .domain import AssetAnnotation, AssetCatalog, RightsStatus
from .errors import (
    AssetByteHashMismatchError,
    MissingRightsEvidenceError,
)


class AssetIntelligenceVerifier:
    """Enforces cryptographic checksum integrity and rights validation."""

    @classmethod
    def verify_media_bytes(cls, asset: AssetAnnotation, media_bytes: bytes) -> bool:
        """Calculates sha256 checksum of raw media bytes and compares against registered hash."""
        computed_hash = hashlib.sha256(media_bytes).hexdigest()
        if computed_hash != asset.source_sha256:
            raise AssetByteHashMismatchError(
                f"Asset '{asset.asset_id}' hash mismatch! Computed {computed_hash} != registered {asset.source_sha256}."
            )
        return True

    @classmethod
    def verify_catalog(cls, catalog: AssetCatalog) -> bool:
        """Validates all assets in a catalog for rights compliance and candidate lineage."""
        for asset in catalog.assets:
            if asset.candidate_id != catalog.candidate_id:
                raise ValueError(
                    f"Asset '{asset.asset_id}' belongs to candidate '{asset.candidate_id}', not catalog candidate '{catalog.candidate_id}'."
                )
            if asset.rights.status == RightsStatus.UNKNOWN_UNLICENSED:
                raise MissingRightsEvidenceError(
                    f"Asset '{asset.asset_id}' has UNKNOWN_UNLICENSED rights status and cannot be verified for production."
                )
        return True
