"""
cae_world_intelligence
----------------------
The World Intelligence and Research Signal Ingestion package for CAE.
"""

from .domain import (
    ResearchSignal,
    ProvenanceRecord,
    SourceMultiplicity,
    RawObservation,
)
from .verifier import ResearchSignalVerifier
from .normalization import SignalNormalizer
from .errors import (
    WorldIntelligenceError,
    ProvenanceError,
    StaleObservationError,
    DuplicateSourceInflationError,
    EvidenceError,
    TaxonomyError,
)

__all__ = [
    "ResearchSignal",
    "ProvenanceRecord",
    "SourceMultiplicity",
    "RawObservation",
    "ResearchSignalVerifier",
    "SignalNormalizer",
    "WorldIntelligenceError",
    "ProvenanceError",
    "StaleObservationError",
    "DuplicateSourceInflationError",
    "EvidenceError",
    "TaxonomyError",
]
