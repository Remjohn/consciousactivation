class InterviewExpressionError(RuntimeError):
    code = "INT_ERROR"

    def __init__(self, message: str, *, context: dict[str, object] | None = None):
        super().__init__(message)
        self.context = context or {}


class ValidationError(InterviewExpressionError):
    code = "INT_VALIDATION_FAILED"


class ConflictError(InterviewExpressionError):
    code = "INT_CONFLICT"


class NotFoundError(InterviewExpressionError):
    code = "INT_NOT_FOUND"


class AuthorityError(InterviewExpressionError):
    code = "INT_AUTHORITY_DENIED"


class StateError(InterviewExpressionError):
    code = "INT_STATE_INVALID"


class EvidenceGapError(InterviewExpressionError):
    code = "INT_EVIDENCE_GAP"
