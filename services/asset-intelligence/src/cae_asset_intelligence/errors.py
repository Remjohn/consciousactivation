"""
errors.py
---------
Structured error taxonomy for Asset Intelligence (CAE-M10).
"""

class AssetIntelligenceError(Exception):
    """Base exception for all asset intelligence failures."""
    pass


class AssetByteHashMismatchError(AssetIntelligenceError):
    """Raised when the calculated hash of an asset does not match its registered sha256 checksum."""
    pass


class MissingRightsEvidenceError(AssetIntelligenceError):
    """Raised when an asset claims CLEARED status without valid license or proof documentation."""
    pass


class InsertRoleContextMismatchError(AssetIntelligenceError):
    """Raised when an editorial insert role does not fit the narrative context."""
    pass


class GenericCaptionRejectedError(AssetIntelligenceError):
    """Raised when an asset caption is shallow/literal (e.g. 'man talking') rather than contextually semantic."""
    pass


class DurationConstraintViolationError(AssetIntelligenceError):
    """Raised when an insert asset violates duration bounds (preferred 3.0s - 6.0s)."""
    pass
