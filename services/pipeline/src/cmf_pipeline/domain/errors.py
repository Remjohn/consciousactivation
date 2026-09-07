from __future__ import annotations


class PipelineError(RuntimeError):
    """Base error for deterministic Pipeline development behavior."""


class PipelineValidationError(ValueError):
    pass


class PipelineSourceIntegrityError(PipelineValidationError):
    """Raised when physical source bytes no longer match their sovereign digest."""


class PipelineSourceLineageError(PipelineValidationError):
    """Raised when a source reference cannot prove its immutable registration lineage."""


class PipelineAuthorityError(PipelineError):
    pass


class PipelineConflict(PipelineError):
    pass


class PipelineNotFound(PipelineError):
    pass


class PipelineLifecycleError(PipelineError):
    pass


class PipelineBudgetError(PipelineError):
    pass
