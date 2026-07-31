from __future__ import annotations


class InterviewComposerError(RuntimeError):
    code = "IC_ERROR"

    def __init__(self, message: str, *, context: dict[str, object] | None = None):
        super().__init__(message)
        self.context = context or {}


class ValidationError(InterviewComposerError):
    code = "IC_VALIDATION_FAILED"


class ConflictError(InterviewComposerError):
    code = "IC_CONFLICT"


class NotFoundError(InterviewComposerError):
    code = "IC_NOT_FOUND"


class CrossReferenceError(InterviewComposerError):
    """Raised when a caller-supplied AIR ref (brand/voice) does not resolve,
    resolves to the wrong object type, or fails the brand/voice ownership
    check. Distinct from NotFoundError because the failing reference lives
    in a different repository than the one this module owns."""
    code = "IC_CROSS_REFERENCE_FAILED"
