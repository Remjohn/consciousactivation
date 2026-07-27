from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ca_contracts import utc_now_rfc3339


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    service: str | None = None
    timestamp: str


def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    # Section 6's documented example response includes "service": "unknown" for
    # GET /api/health/{service} 404s. The literal Stage 1 handler code never set
    # it (always None). Path params are available on `request` regardless of
    # which route raised the 404, so this recovers the documented behaviour for
    # routes that have a `{service}` path parameter without hardcoding anything.
    service = request.path_params.get("service")
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error_code="NOT_FOUND",
            message=str(exc),
            service=service,
            timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )


def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )
