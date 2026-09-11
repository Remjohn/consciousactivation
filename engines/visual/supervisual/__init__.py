"""Governed SuperVisual editor surface over CAE's canonical primitive roles.

This package is an editor/projection layer only. It does not own semantic meaning,
canonical campaign state, source retrieval, or release authority.
"""

from .editor import (
    AnnotationProposal,
    EditorRevision,
    PrimitiveRole,
    SuperVisualEditor,
    SuperVisualProjection,
)

__all__ = [
    "AnnotationProposal",
    "EditorRevision",
    "PrimitiveRole",
    "SuperVisualEditor",
    "SuperVisualProjection",
]
