"""
errors.py
---------
Structured error taxonomy for Production Semantic Program (CAE-M11).
"""

class ProductionProgramError(Exception):
    """Base exception for all production program compiler failures."""
    pass


class EvidenceQuoteMismatchError(ProductionProgramError):
    """Raised when a scene's spoken text does not match the registered upstream evidence checksum."""
    pass


class UnapprovedAssetInsertionError(ProductionProgramError):
    """Raised when an unapproved media asset is injected into a scene progression."""
    pass


class StoryArcGeometryMutationError(ProductionProgramError):
    """Raised when downstream compilation attempts to alter the approved structural story arc."""
    pass


class TimingDiscontinuityError(ProductionProgramError):
    """Raised when scene start and end times have gaps, overlaps, or negative durations."""
    pass
