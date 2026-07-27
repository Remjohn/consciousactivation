"""Operational readiness repository for TS-CMF-061."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.operational_readiness import (
    CompleteBrandCycleCheck,
    GpuWorkerShutdownCheck,
    MemoryRebuildCheck,
    OperationalReadinessDomainEvent,
    OperationalReadinessReport,
    ProjectionRebuildCheck,
    ProviderOutageSimulation,
    ReadinessCheckRun,
    ReadinessReceipt,
    RestoreDrillReport,
)


@dataclass
class InMemoryOperationalReadinessRepository:
    runs: dict[UUID, ReadinessCheckRun] = field(default_factory=dict)
    reports: dict[UUID, OperationalReadinessReport] = field(default_factory=dict)
    receipts: dict[UUID, ReadinessReceipt] = field(default_factory=dict)
    restore_drills: dict[UUID, RestoreDrillReport] = field(default_factory=dict)
    provider_outages: dict[UUID, ProviderOutageSimulation] = field(default_factory=dict)
    gpu_shutdown_checks: dict[UUID, GpuWorkerShutdownCheck] = field(default_factory=dict)
    memory_rebuild_checks: dict[UUID, MemoryRebuildCheck] = field(default_factory=dict)
    projection_rebuild_checks: dict[UUID, ProjectionRebuildCheck] = field(default_factory=dict)
    complete_brand_cycle_checks: dict[UUID, CompleteBrandCycleCheck] = field(default_factory=dict)
    events: list[OperationalReadinessDomainEvent] = field(default_factory=list)
    idempotency_index: dict[tuple[UUID, UUID, str], UUID] = field(default_factory=dict)

    def put_run(self, run: ReadinessCheckRun, *, idempotency_key: str | None = None) -> ReadinessCheckRun:
        self.runs[run.readiness_run_id] = run
        if idempotency_key:
            self.idempotency_index[(run.organization_id, run.brand_id, idempotency_key)] = run.readiness_run_id
        return run

    def run_for_idempotency(self, organization_id: UUID, brand_id: UUID, idempotency_key: str) -> ReadinessCheckRun | None:
        run_id = self.idempotency_index.get((organization_id, brand_id, idempotency_key))
        return self.runs.get(run_id) if run_id else None

    def put_report(self, report: OperationalReadinessReport) -> OperationalReadinessReport:
        self.reports[report.readiness_report_id] = report
        return report

    def put_receipt(self, receipt: ReadinessReceipt) -> ReadinessReceipt:
        self.receipts[receipt.receipt_id] = receipt
        return receipt

    def put_restore_drill(self, report: RestoreDrillReport) -> RestoreDrillReport:
        self.restore_drills[report.restore_drill_report_id] = report
        return report

    def put_provider_outage(self, report: ProviderOutageSimulation) -> ProviderOutageSimulation:
        self.provider_outages[report.provider_outage_simulation_id] = report
        return report

    def put_gpu_shutdown_check(self, report: GpuWorkerShutdownCheck) -> GpuWorkerShutdownCheck:
        self.gpu_shutdown_checks[report.gpu_worker_shutdown_check_id] = report
        return report

    def put_memory_rebuild_check(self, report: MemoryRebuildCheck) -> MemoryRebuildCheck:
        self.memory_rebuild_checks[report.memory_rebuild_check_id] = report
        return report

    def put_projection_rebuild_check(self, report: ProjectionRebuildCheck) -> ProjectionRebuildCheck:
        self.projection_rebuild_checks[report.projection_rebuild_check_id] = report
        return report

    def put_complete_brand_cycle_check(self, report: CompleteBrandCycleCheck) -> CompleteBrandCycleCheck:
        self.complete_brand_cycle_checks[report.complete_brand_cycle_check_id] = report
        return report

    def append_event(self, event: OperationalReadinessDomainEvent) -> OperationalReadinessDomainEvent:
        self.events.append(event)
        return event
