"""Causal admission boundary for pipeline stage ordering (INV-CAUSAL-001)."""

from .causal_admission import (
    AncestorBinding,
    CausalAdmissionDecision,
    CausalAdmissionError,
    CausalAdmissionService,
    RequiredAncestor,
)

__all__ = [
    "AncestorBinding",
    "CausalAdmissionDecision",
    "CausalAdmissionError",
    "CausalAdmissionService",
    "RequiredAncestor",
]
