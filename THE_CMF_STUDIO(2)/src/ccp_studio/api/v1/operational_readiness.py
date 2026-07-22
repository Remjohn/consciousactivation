"""FastAPI adapter for TS-CMF-061 operational readiness."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.operational_readiness import (
    CompleteBrandCycleCheck,
    GpuWorkerShutdownCheck,
    MemoryRebuildCheck,
    OperationalReadinessReport,
    ProjectionRebuildCheck,
    ProviderOutageSimulation,
    ReadinessReceipt,
    RestoreDrillReport,
)
from ccp_studio.services.operational_readiness_service import OperationalReadinessService


router = APIRouter(prefix="/api/v1/operations/readiness", tags=["operational-readiness"])
_operational_readiness_service: OperationalReadinessService | None = None


class RunOperationalReadinessSuiteRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    triggered_by_user_id: UUID
    role_ids: list[str] = Field(default_factory=list)
    fixture_pack_id: str = "cmf.full-brand-cycle.fixture.v1"
    manual_database_edits_detected: bool = False
    idempotency_key: str | None = None


class RunReadinessCheckRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    triggered_by_user_id: UUID
    fixture_pack_id: str = "cmf.readiness.fixture.v1"
    manual_database_edits_detected: bool = False


class RecordReadinessReceiptRequest(BaseModel):
    readiness_run_id: UUID


def set_operational_readiness_service(service: OperationalReadinessService) -> None:
    global _operational_readiness_service
    _operational_readiness_service = service


def get_operational_readiness_service() -> OperationalReadinessService:
    if _operational_readiness_service is None:
        raise RuntimeError("OperationalReadinessService must be configured by the application.")
    return _operational_readiness_service


@router.post("/suite", response_model=OperationalReadinessReport)
def run_operational_readiness_suite(
    request: RunOperationalReadinessSuiteRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> OperationalReadinessReport:
    return service.run_operational_readiness_suite(**request.model_dump())


@router.post("/restore-drill", response_model=RestoreDrillReport)
def run_restore_drill(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> RestoreDrillReport:
    data = request.model_dump(exclude={"manual_database_edits_detected"})
    return service.run_restore_drill(**data)


@router.post("/provider-outage", response_model=ProviderOutageSimulation)
def simulate_provider_outage(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> ProviderOutageSimulation:
    data = request.model_dump(exclude={"manual_database_edits_detected"})
    return service.simulate_provider_outage(**data)


@router.post("/gpu-worker-shutdown", response_model=GpuWorkerShutdownCheck)
def run_gpu_worker_shutdown_check(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> GpuWorkerShutdownCheck:
    data = request.model_dump(exclude={"manual_database_edits_detected"})
    return service.run_gpu_worker_shutdown_check(**data)


@router.post("/memory-rebuild", response_model=MemoryRebuildCheck)
def run_memory_rebuild_check(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> MemoryRebuildCheck:
    data = request.model_dump(exclude={"manual_database_edits_detected"})
    return service.run_memory_rebuild_check(**data)


@router.post("/projection-rebuild", response_model=ProjectionRebuildCheck)
def run_projection_rebuild_check(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> ProjectionRebuildCheck:
    data = request.model_dump(include={"organization_id", "brand_id", "fixture_pack_id"})
    return service.run_projection_rebuild_check(**data)


@router.post("/complete-brand-cycle", response_model=CompleteBrandCycleCheck)
def run_complete_brand_cycle_check(
    request: RunReadinessCheckRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> CompleteBrandCycleCheck:
    return service.run_complete_brand_cycle_check(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        manual_database_edits_detected=request.manual_database_edits_detected,
    )


@router.post("/receipts", response_model=ReadinessReceipt)
def record_readiness_receipt(
    request: RecordReadinessReceiptRequest,
    service: OperationalReadinessService = Depends(get_operational_readiness_service),
) -> ReadinessReceipt:
    return service.record_readiness_receipt(request.readiness_run_id)
