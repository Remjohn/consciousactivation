"""
cae_candidate_intelligence
--------------------------
The Editorial Candidate Formation and Narrative Architecture package for CAE.
"""

from .domain import (
    CandidateType,
    NarrativeCompleteness,
    ProductionStatus,
    HeritageCMFScore,
    CandidateEvidenceLink,
    ContentCandidate,
)
from .errors import (
    CandidateIntelligenceError,
    UngroundedCandidateError,
    NarrativeIncompletenessError,
    MissingStoryTurnError,
    PrematureProductionApprovalError,
)
from .composer import EditorialCandidateComposer
from .verifier import ContentCandidateVerifier

__all__ = [
    "CandidateType",
    "NarrativeCompleteness",
    "ProductionStatus",
    "HeritageCMFScore",
    "CandidateEvidenceLink",
    "ContentCandidate",
    "CandidateIntelligenceError",
    "UngroundedCandidateError",
    "NarrativeIncompletenessError",
    "MissingStoryTurnError",
    "PrematureProductionApprovalError",
    "EditorialCandidateComposer",
    "ContentCandidateVerifier",
]
