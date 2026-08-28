"""
cae_asset_intelligence
----------------------
The Multimodal Asset Intelligence and E/D-Roll package for CAE.
"""

from .domain import (
    SourceType,
    MediaType,
    EditorialInsertRole,
    RightsStatus,
    RightsMetadata,
    AssetAnnotation,
    AssetCatalog,
)
from .errors import (
    AssetIntelligenceError,
    AssetByteHashMismatchError,
    MissingRightsEvidenceError,
    InsertRoleContextMismatchError,
    GenericCaptionRejectedError,
    DurationConstraintViolationError,
)
from .annotator import AssetAnnotator
from .verifier import AssetIntelligenceVerifier

__all__ = [
    "SourceType",
    "MediaType",
    "EditorialInsertRole",
    "RightsStatus",
    "RightsMetadata",
    "AssetAnnotation",
    "AssetCatalog",
    "AssetIntelligenceError",
    "AssetByteHashMismatchError",
    "MissingRightsEvidenceError",
    "InsertRoleContextMismatchError",
    "GenericCaptionRejectedError",
    "DurationConstraintViolationError",
    "AssetAnnotator",
    "AssetIntelligenceVerifier",
]
