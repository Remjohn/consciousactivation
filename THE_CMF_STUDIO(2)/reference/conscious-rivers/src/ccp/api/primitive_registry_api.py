"""
Primitive registry API endpoints for FR-ERA3-06.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from src.ccp.models.primitive_registry_models import (
    CacheHealthStatus,
    ExperiencePrimitiveRecord,
    MeaningPrimitiveRecord,
    PrimitiveFamilyQueryResponse,
    PrimitiveInvalidationRequest,
    PrimitiveInvalidationResponse,
    PrimitivePlane,
    PrimitivePlaneQueryResponse,
    PrimitiveQueryRequest,
    PrimitiveQueryResponse,
)
from src.ccp.services.primitive_registry_service import (
    PrimitiveRegistryQueryService,
    get_primitive_registry_service,
)

router = APIRouter()


def _service_dependency() -> PrimitiveRegistryQueryService:
    service = get_primitive_registry_service()
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Primitive registry service is not initialized",
        )
    return service


def _verify_internal_api_key(request: Request, x_internal_api_key: str = Header(default="")) -> bool:
    configured = os.getenv("INTERNAL_API_KEY", "")
    if not configured:
        return True
    return bool(x_internal_api_key) and x_internal_api_key == configured


@router.get("/primitives/experience/{primitive_id}", response_model=ExperiencePrimitiveRecord)
async def get_experience_primitive(
    primitive_id: str,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    record = service.query_by_id(primitive_id, PrimitivePlane.EXPERIENCE)
    if not isinstance(record, ExperiencePrimitiveRecord):
        raise HTTPException(status_code=404, detail=f"Experience primitive not found: {primitive_id}")
    return record


@router.get("/primitives/meaning/{primitive_id}", response_model=MeaningPrimitiveRecord)
async def get_meaning_primitive(
    primitive_id: str,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    record = service.query_by_id(primitive_id, PrimitivePlane.MEANING)
    if not isinstance(record, MeaningPrimitiveRecord):
        raise HTTPException(status_code=404, detail=f"Meaning primitive not found: {primitive_id}")
    return record


@router.post("/primitives/query", response_model=PrimitiveQueryResponse)
async def query_primitives(
    payload: PrimitiveQueryRequest,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    return service.query_batch(payload)


@router.get("/primitives/family/{family_code}", response_model=PrimitiveFamilyQueryResponse)
async def get_primitives_by_family(
    family_code: str,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    return service.query_by_family(family_code)


@router.get("/primitives/plane/{plane}", response_model=PrimitivePlaneQueryResponse)
async def get_primitives_by_plane(
    plane: PrimitivePlane,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    return service.query_by_plane(plane)


@router.get("/primitives/health", response_model=CacheHealthStatus)
async def primitive_registry_health(
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
):
    return service.health()


@router.post("/primitives/invalidate", response_model=PrimitiveInvalidationResponse)
async def invalidate_primitive(
    payload: PrimitiveInvalidationRequest,
    request: Request,
    service: PrimitiveRegistryQueryService = Depends(_service_dependency),
    x_internal_api_key: str = Header(default=""),
):
    if not _verify_internal_api_key(request, x_internal_api_key=x_internal_api_key):
        raise HTTPException(status_code=403, detail="Invalid internal API key")
    return service.invalidate_primitive(payload.primitive_id)
