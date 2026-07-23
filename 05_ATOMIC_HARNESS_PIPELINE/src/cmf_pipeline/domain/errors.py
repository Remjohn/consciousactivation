from __future__ import annotations


class PipelineError(RuntimeError):
    """Base error for deterministic Pipeline development behavior."""


class PipelineValidationError(ValueError):
    pass


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
