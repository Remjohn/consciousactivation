"""Operational readiness contracts for TS-CMF-061."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ReadinessCheckType(str, Enum):
    restore_drill = "restore_drill"
    provider_outage = "provider_outage"
    gpu_worker_shutdown = "gpu_worker_shutdown"
    memory_rebuild = "memory_rebuild"
    projection_rebuild = "projection_rebuild"
    complete_brand_cycle = "complete_brand_cycle"


class ReadinessOverallStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    blocked = "blocked"


class ReadinessCheckResult(BaseModel):
    check_type: ReadinessCheckType
    passed: bool
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    required_fixes: list[str] = Field(default_factory=list)
    observed_counts: dict[str, int | float] = Field(default_factory=dict)


class RestoreDrillReport(BaseModel):
    schema_version: Literal["cmf.restore_drill_report.v1"]
    restore_drill_report_id: UUID
    canonical_state_verified: bool
    object_storage_verified: bool
    receipts_verified: bool
    projection_rebuild_verified: bool
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class ProviderOutageSimulation(BaseModel):
    schema_version: Literal["cmf.provider_outage_simulation.v1"]
    provider_outage_simulation_id: UUID
    failed_provider_job_id: UUID
    recovery_receipt_id: UUID
    duplicate_block_receipt_id: UUID
    preserved_artifact_refs: list[str] = Field(default_factory=list)
    requeued_work_refs: list[str] = Field(default_factory=list)
    duplicate_side_effect_blocked: bool
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class GpuWorkerShutdownCheck(BaseModel):
    schema_version: Literal["cmf.gpu_worker_shutdown_check.v1"]
    gpu_worker_shutdown_check_id: UUID
    gpu_worker_job_id: UUID
    gpu_cost_report_id: UUID
    shutdown_status: str
    final_cost_amount: float
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class MemoryRebuildCheck(BaseModel):
    schema_version: Literal["cmf.memory_rebuild_check.v1"]
    memory_rebuild_check_id: UUID
    active_memory_event_ids: list[UUID] = Field(default_factory=list)
    expired_memory_event_ids: list[UUID] = Field(default_factory=list)
    reversed_memory_event_ids: list[UUID] = Field(default_factory=list)
    quarantined_memory_event_ids: list[UUID] = Field(default_factory=list)
    replay_preserved_governance_state: bool
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class ProjectionRebuildCheck(BaseModel):
    schema_version: Literal["cmf.projection_rebuild_check.v1"]
    projection_rebuild_check_id: UUID
    projection_receipt_id: UUID
    node_count: int
    relationship_count: int
    health_status: str
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class CompleteBrandCycleCheck(BaseModel):
    schema_version: Literal["cmf.complete_brand_cycle_check.v1"]
    complete_brand_cycle_check_id: UUID
    completed_stage_refs: list[str] = Field(default_factory=list)
    operations_board_state_id: UUID
    projection_health: str
    manual_database_edits_detected: bool
    command_count: int
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class ReadinessCheckRun(BaseModel):
    schema_version: Literal["cmf.readiness_check_run.v1"]
    readiness_run_id: UUID
    organization_id: UUID
    brand_id: UUID
    triggered_by_user_id: UUID
    fixture_pack_id: str = Field(min_length=1)
    results: list[ReadinessCheckResult] = Field(default_factory=list)
    overall_status: ReadinessOverallStatus
    manual_database_edits_detected: bool = False
    source_spine_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class ReadinessReceipt(BaseModel):
    schema_version: Literal["cmf.readiness_receipt.v1"]
    receipt_id: UUID
    readiness_run_id: UUID
    fixture_pack_id: str = Field(min_length=1)
    canonical_state_verified: bool
    object_storage_verified: bool
    receipts_verified: bool
    projection_rebuild_verified: bool
    manual_database_edits_detected: bool
    passed_check_count: int
    failed_check_count: int
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class OperationalReadinessReport(BaseModel):
    schema_version: Literal["cmf.operational_readiness_report.v1"]
    readiness_report_id: UUID
    run: ReadinessCheckRun
    receipt: ReadinessReceipt
    detailed_reports: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime


class OperationalReadinessDomainEvent(BaseModel):
    schema_version: Literal["cmf.operational_readiness_domain_event.v1"]
    readiness_event_id: UUID
    event_type: str = Field(min_length=1)
    readiness_run_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def readiness_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_readiness_receipt(
    *,
    run: ReadinessCheckRun,
    canonical_state_verified: bool,
    object_storage_verified: bool,
    receipts_verified: bool,
    projection_rebuild_verified: bool,
) -> ReadinessReceipt:
    evidence_refs = sorted({ref for result in run.results for ref in result.evidence_refs})
    blocker_codes = sorted({code for result in run.results for code in result.blocker_codes})
    passed_count = sum(result.passed for result in run.results)
    failed_count = len(run.results) - passed_count
    payload = {
        "readiness_run_id": run.readiness_run_id,
        "fixture_pack_id": run.fixture_pack_id,
        "canonical_state_verified": canonical_state_verified,
        "object_storage_verified": object_storage_verified,
        "receipts_verified": receipts_verified,
        "projection_rebuild_verified": projection_rebuild_verified,
        "manual_database_edits_detected": run.manual_database_edits_detected,
        "passed_check_count": passed_count,
        "failed_check_count": failed_count,
        "blocker_codes": blocker_codes,
        "evidence_refs": evidence_refs,
    }
    return ReadinessReceipt(
        schema_version="cmf.readiness_receipt.v1",
        receipt_id=uuid4(),
        readiness_run_id=run.readiness_run_id,
        fixture_pack_id=run.fixture_pack_id,
        canonical_state_verified=canonical_state_verified,
        object_storage_verified=object_storage_verified,
        receipts_verified=receipts_verified,
        projection_rebuild_verified=projection_rebuild_verified,
        manual_database_edits_detected=run.manual_database_edits_detected,
        passed_check_count=passed_count,
        failed_check_count=failed_count,
        blocker_codes=blocker_codes,
        evidence_refs=evidence_refs,
        receipt_hash=readiness_hash(payload),
        written_at=utc_now(),
    )
