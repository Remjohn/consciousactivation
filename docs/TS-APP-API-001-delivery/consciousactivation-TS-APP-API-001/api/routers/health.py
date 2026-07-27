from __future__ import annotations

import sqlite3
from contextlib import closing
from importlib import metadata as importlib_metadata
from typing import Any, Callable

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ca_contracts import utc_now_rfc3339

router = APIRouter()

VALID_SERVICES = {"pipeline", "air", "vae", "interview", "builder"}


class ServiceHealthItem(BaseModel):
    service: str
    product_id: str
    product_version: str
    authority_state: str
    database_path: str
    integrity: str
    command_count: int
    event_count: int
    receipt_count: int
    production_authorized: bool
    certified: bool
    claim_ceiling: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    gateway_version: str
    ca_data_root: str
    services: dict[str, dict]


# ---------------------------------------------------------------------------
# Per-service status collection.
#
# TS-APP-API-001 Section 7 Stage 2 specifies a single generic accessor:
#   raw = getattr(app_state, service_name).status()
#
# Reading the real service packages shows that assumption only holds for two
# of the five services. This is not a stylistic deviation -- calling it the
# way the spec literally describes makes AC-002 permanently fail (interview
# and builder always come back integrity: "error", degrading the whole
# response to 503) because those two objects don't expose what the spec
# assumes:
#
#   pipeline    -> PipelineApplication.status()                          OK, matches ServiceHealthItem
#   air         -> AirApplication.status()                               OK, matches ServiceHealthItem
#   vae         -> VAEApplication.status()                                exists, but its dict never
#                                                                          contains product_id/product_version/
#                                                                          authority_state/command_count/receipt_count
#   interview   -> InterviewExpressionApplication has NO .status()       must call .repository.health() instead
#   builder     -> BuilderProductizationService has NO .status()/.health() must be assembled from its repository's
#                                                                          verify_integrity() + raw table counts
#
# None of the fallbacks below modify the underlying service packages --
# they only read attributes/methods that already exist, from this new
# gateway module, keeping AC-007 (no modification to existing packages) intact.
# ---------------------------------------------------------------------------

_REQUIRED_DEFAULTS: dict[str, Any] = {
    "product_id": "unknown",
    "product_version": "unknown",
    "authority_state": "unknown",
    "database_path": "",
    "command_count": 0,
    "event_count": 0,
    "receipt_count": 0,
    "production_authorized": False,
    "certified": False,
    "claim_ceiling": "UNSPECIFIED",
}


def _package_version(distribution_name: str, fallback: str) -> str:
    try:
        return importlib_metadata.version(distribution_name)
    except importlib_metadata.PackageNotFoundError:
        return fallback


def _vae_status(app_state) -> dict[str, Any]:
    # VAEApplication.status() == {**VAERepository.health(), "lifecycle_state": ...,
    # "delegation_release": ..., "capability_count": ..., ...}. That inner health()
    # dict only carries database_path / integrity / object_count / job_count /
    # worker_count / event_count -- it never carries product_id, product_version,
    # authority_state, command_count, or receipt_count. VAE has no notion of a
    # "command" or "receipt" the way the ca_runtime-backed services do, so those
    # two counts are reported as 0 rather than invented.
    raw = app_state.vae.status()
    return {
        "product_id": "cmf-visual-asset-editor",
        "product_version": _package_version("cmf-visual-asset-editor", "0.8.0.dev1"),
        "authority_state": raw.get("lifecycle_state", "unknown"),
        "command_count": 0,
        "receipt_count": 0,
        **raw,  # raw's own integrity / database_path / event_count win when present
    }


def _interview_status(app_state) -> dict[str, Any]:
    # InterviewExpressionApplication has no .status(); its repository does have
    # .health(), and (unlike VAE's) that health dict is already built from
    # ca_runtime's ProductHealth.to_dict(), so it carries every field
    # ServiceHealthItem needs.
    return app_state.interview.repository.health()


def _builder_status(app_state) -> dict[str, Any]:
    # BuilderProductizationService exposes neither .status() nor .health().
    # The gateway lifespan keeps a direct handle on its SQLiteProductizationRepository
    # (app.state.builder_repository) specifically so this adapter can assemble a
    # status snapshot from what *does* exist: verify_integrity() and the two
    # durability tables it manages. Builder has no separate "event" concept, and
    # every committed command produces exactly one receipt, so command_count and
    # receipt_count are reported as the same number and event_count as 0.
    repo = app_state.builder_repository
    issues = repo.verify_integrity()
    integrity = "ok" if not issues else "error"
    receipt_count = 0
    try:
        with closing(sqlite3.connect(str(repo.database_path))) as connection:
            receipt_count = int(
                connection.execute("SELECT COUNT(*) FROM durable_command_receipts").fetchone()[0]
            )
    except sqlite3.Error:
        integrity = "error"
    return {
        "product_id": "atomic-harness-builder",
        "product_version": getattr(
            __import__("cmf_builder"), "__version__", "unknown"
        ),
        "authority_state": "bounded_local_release_candidate",
        "database_path": str(repo.database_path),
        "integrity": integrity,
        "command_count": receipt_count,
        "event_count": 0,
        "receipt_count": receipt_count,
        "production_authorized": False,
        "certified": False,
        "claim_ceiling": "ATOMIC_HARNESS_BUILDER_BOUNDED_LOCAL_RELEASE_CANDIDATE_EVIDENCE",
        "integrity_issues": list(issues),
    }


_STATUS_COLLECTORS: dict[str, Callable[[Any], dict[str, Any]]] = {
    "pipeline": lambda state: state.pipeline.status(),
    "air": lambda state: state.air.status(),
    "vae": _vae_status,
    "interview": _interview_status,
    "builder": _builder_status,
}


def _collect_service_status(app_state, service_name: str) -> dict:
    try:
        raw = _STATUS_COLLECTORS[service_name](app_state)
        normalized = {**_REQUIRED_DEFAULTS, **raw}
        normalized["service"] = service_name
        normalized.setdefault("integrity", "ok")
        return normalized
    except Exception as exc:
        return {
            "service": service_name,
            "integrity": "error",
            "error": str(exc),
            **_REQUIRED_DEFAULTS,
            "production_authorized": False,
            "certified": False,
        }


@router.get("/health", response_model=HealthResponse)
def get_health(request: Request):
    config = request.app.state.config
    statuses = {
        name: _collect_service_status(request.app.state, name)
        for name in VALID_SERVICES
    }
    overall = "ok" if all(s.get("integrity") == "ok" for s in statuses.values()) else "degraded"
    response = HealthResponse(
        status=overall,
        timestamp=utc_now_rfc3339(),
        gateway_version=config.gateway_version,
        ca_data_root=str(config.ca_data_root),
        services=statuses,
    )
    status_code = 200 if overall == "ok" else 503
    return JSONResponse(content=response.model_dump(), status_code=status_code)


@router.get("/health/{service}")
def get_service_health(service: str, request: Request):
    if service not in VALID_SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown service: '{service}'. Valid values: {', '.join(sorted(VALID_SERVICES))}",
        )
    status = _collect_service_status(request.app.state, service)
    status_code = 200 if status.get("integrity") == "ok" else 503
    return JSONResponse(content=status, status_code=status_code)
