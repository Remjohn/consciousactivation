"""Operations Board read model service for TS-CMF-059."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.approval_gate import ApprovalGateDecision
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.comfy_gpu_worker import GpuWorkerStatus
from ccp_studio.contracts.operations_board import (
    BlockerSummary,
    CostSnapshot,
    IncidentSummary,
    OperationsActionDecision,
    OperationsBoardState,
    OperationsDomainEvent,
    OperationsReceipt,
    ProviderStatusSnapshot,
    QueueSnapshot,
    RecoveryRecommendation,
    WorkerStatusSnapshot,
    new_operations_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import ProviderJobStatus
from ccp_studio.contracts.provider_recovery import OperationalIncident, RecoveryActionType
from ccp_studio.repositories.approval_gate import InMemoryApprovalGateRepository
from ccp_studio.repositories.comfy_gpu_worker import InMemoryComfyGpuWorkerRepository
from ccp_studio.repositories.memory_governance import InMemoryMemoryGovernanceRepository
from ccp_studio.repositories.operations_board import InMemoryOperationsBoardRepository
from ccp_studio.repositories.projection import InMemoryProjectionRepository
from ccp_studio.repositories.provider_jobs import InMemoryProviderOperationsRepository
from ccp_studio.repositories.provider_recovery import InMemoryProviderRecoveryRepository
from ccp_studio.repositories.publishing import InMemoryPublishingRepository
from ccp_studio.services.command_bus import CommandBus


OPERATIONS_ROLES = {"owner", "admin", "operator", "production_steward"}


class OperationsBoardError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class OperationsBoardService:
    provider_repository: InMemoryProviderOperationsRepository | None = None
    gpu_worker_repository: InMemoryComfyGpuWorkerRepository | None = None
    recovery_repository: InMemoryProviderRecoveryRepository | None = None
    approval_gate_repository: InMemoryApprovalGateRepository | None = None
    publishing_repository: InMemoryPublishingRepository | None = None
    memory_governance_repository: InMemoryMemoryGovernanceRepository | None = None
    projection_repository: InMemoryProjectionRepository | None = None
    repository: InMemoryOperationsBoardRepository = field(default_factory=InMemoryOperationsBoardRepository)

    def build_operations_board_state(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID | None = None,
        include_resolved: bool = True,
        idempotency_key: str | None = None,
    ) -> OperationsBoardState:
        if idempotency_key:
            prior = self.repository.state_for_idempotency(idempotency_key)
            if prior:
                return prior
        blockers = [
            *self._approval_blockers(organization_id, brand_id),
            *self._publishing_blockers(organization_id, brand_id),
            *self._memory_blockers(),
            *self._projection_blockers(),
            *self.repository.manual_blockers,
        ]
        incidents = self._incidents(include_resolved=include_resolved)
        recommendations = [
            *self._recommendations_from_incidents(incidents),
            *self._recommendations_from_blockers(blockers),
            *self.repository.manual_recommendations,
        ]
        state = OperationsBoardState(
            schema_version="cmf.operations_board_state.v1",
            board_state_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            queues=self._queues(),
            workers=self._workers(),
            blockers=blockers,
            provider_statuses=self._provider_statuses(),
            incident_ids=[incident.incident_id for incident in incidents],
            incidents=incidents,
            workflow_checkpoint_refs=self._workflow_checkpoint_refs(),
            cost_snapshot=self._cost_snapshot(),
            projection_health=self.projection_repository.health.status.value if self.projection_repository else "unknown",
            recovery_recommendations=recommendations,
            generated_at=utc_now(),
        )
        self.repository.put_state(state, idempotency_key=idempotency_key)
        receipt = self.record_operations_receipt(state)
        self._event("OperationsBoardStateBuilt", state, {"operations_receipt_id": str(receipt.operations_receipt_id)})
        return state

    def refresh_operations_board(self, **kwargs: Any) -> OperationsBoardState:
        state = self.build_operations_board_state(**kwargs)
        self._event("OperationsBoardRefreshed", state, {"board_state_id": str(state.board_state_id)})
        return state

    def link_blocker_to_object(
        self,
        *,
        blocker_type: str,
        blocker_code: str,
        object_ref: str,
        receipt_id: str,
        required_action: str,
        allowed_command_type: str,
    ) -> BlockerSummary:
        blocker = self.repository.add_blocker(
            BlockerSummary(
                blocker_type=blocker_type,  # type: ignore[arg-type]
                blocker_code=blocker_code,
                object_ref=object_ref,
                receipt_id=receipt_id,
                required_action=required_action,
                allowed_command_type=allowed_command_type,
            )
        )
        self.repository.append_event(
            OperationsDomainEvent(
                schema_version="cmf.operations_domain_event.v1",
                operations_event_id=uuid4(),
                event_type="BlockerLinkedToObject",
                payload=blocker.model_dump(mode="json"),
                created_at=utc_now(),
            )
        )
        return blocker

    def recommend_recovery_action(
        self,
        *,
        object_ref: str,
        recommended_command_type: str,
        reason: str,
        receipt_refs: list[str] | None = None,
    ) -> RecoveryRecommendation:
        recommendation = self.repository.add_recommendation(
            RecoveryRecommendation(
                recommendation_id=uuid4(),
                object_ref=object_ref,
                recommended_command_type=recommended_command_type,
                reason=reason,
                receipt_refs=receipt_refs or [],
                manual_database_edit_allowed=False,
            )
        )
        self.repository.append_event(
            OperationsDomainEvent(
                schema_version="cmf.operations_domain_event.v1",
                operations_event_id=uuid4(),
                event_type="RecoveryActionRecommended",
                payload=recommendation.model_dump(mode="json"),
                created_at=utc_now(),
            )
        )
        return recommendation

    def record_operations_receipt(self, state: OperationsBoardState) -> OperationsReceipt:
        receipt = self.repository.put_receipt(
            new_operations_receipt(
                state=state,
                source_query_snapshot={
                    "queue_count": len(state.queues),
                    "worker_count": len(state.workers),
                    "provider_status_count": len(state.provider_statuses),
                    "blocker_count": len(state.blockers),
                    "incident_count": len(state.incidents),
                },
            )
        )
        self._event("OperationsReceiptRecorded", state, {"operations_receipt_id": str(receipt.operations_receipt_id)})
        return receipt

    def operations_action_boundary(
        self,
        *,
        requested_action: str,
        allowed_command_type: str,
        manual_database_edit_requested: bool,
    ) -> OperationsActionDecision:
        return OperationsActionDecision(
            schema_version="cmf.operations_action_decision.v1",
            requested_action=requested_action,
            allowed_command_type=allowed_command_type,
            manual_database_edit_allowed=False,
            reason="Operations Board actions must route through typed backend commands."
            if manual_database_edit_requested
            else "Typed command route accepted.",
        )

    def overlay_board_state(self, **kwargs: Any) -> OperationsBoardState:
        return self.build_operations_board_state(**kwargs)

    def _queues(self) -> list[QueueSnapshot]:
        queues: list[QueueSnapshot] = []
        if self.provider_repository:
            jobs = list(self.provider_repository.jobs.values())
            queues.append(
                QueueSnapshot(
                    queue_name="provider_jobs",
                    depth=sum(job.status in {ProviderJobStatus.requested, ProviderJobStatus.submitted, ProviderJobStatus.running} for job in jobs),
                    active_count=sum(job.status in {ProviderJobStatus.submitted, ProviderJobStatus.running} for job in jobs),
                    failed_count=sum(job.status == ProviderJobStatus.failed for job in jobs),
                )
            )
        if self.gpu_worker_repository:
            jobs = list(self.gpu_worker_repository.jobs.values())
            queues.append(
                QueueSnapshot(
                    queue_name="gpu_workers",
                    depth=sum(job.status in {GpuWorkerStatus.queued, GpuWorkerStatus.starting, GpuWorkerStatus.running, GpuWorkerStatus.draining} for job in jobs),
                    active_count=sum(job.status in {GpuWorkerStatus.running, GpuWorkerStatus.draining} for job in jobs),
                    failed_count=sum(job.status == GpuWorkerStatus.failed for job in jobs),
                )
            )
        return queues

    def _workers(self) -> list[WorkerStatusSnapshot]:
        if not self.gpu_worker_repository:
            return []
        workers: list[WorkerStatusSnapshot] = []
        for job in self.gpu_worker_repository.jobs.values():
            cost = sum(report.cost_amount for report in self.gpu_worker_repository.cost_reports.values() if report.gpu_worker_job_id == job.gpu_worker_job_id)
            status = {
                GpuWorkerStatus.running: "running",
                GpuWorkerStatus.draining: "draining",
                GpuWorkerStatus.failed: "failed",
                GpuWorkerStatus.shutdown: "offline",
            }.get(job.status, "idle")
            workers.append(
                WorkerStatusSnapshot(
                    worker_id=str(job.gpu_worker_job_id),
                    worker_type="comfyui_docker",
                    status=status,  # type: ignore[arg-type]
                    gpu_tier=job.gpu_tier.value,
                    active_job_ids=[str(job.provider_job_id)] if status in {"running", "draining"} else [],
                    current_cost_estimate_usd=cost or None,
                    shutdown_status="draining_until_queue_empty" if status == "draining" else ("shutdown_complete" if status == "offline" else None),
                )
            )
        return workers

    def _provider_statuses(self) -> list[ProviderStatusSnapshot]:
        if not self.provider_repository:
            return []
        by_provider: dict[str, list[Any]] = {}
        for job in self.provider_repository.jobs.values():
            by_provider.setdefault(job.provider_name, []).append(job)
        statuses: list[ProviderStatusSnapshot] = []
        for provider_name, jobs in by_provider.items():
            failed = [job for job in jobs if job.status == ProviderJobStatus.failed]
            affected = failed or [job for job in jobs if job.status in {ProviderJobStatus.running, ProviderJobStatus.submitted}]
            completed_artifacts = [
                artifact
                for receipt in self.provider_repository.receipts.values()
                for artifact in receipt.output_artifact_hashes
                if receipt.provider_job_id in {job.provider_job_id for job in affected}
            ]
            cost = sum((receipt.cost_amount or 0) for receipt in self.provider_repository.receipts.values() if receipt.provider_name == provider_name)
            blocker_codes = [receipt.failure_code for receipt in self.provider_repository.receipts.values() if receipt.provider_name == provider_name and receipt.failure_code]
            statuses.append(
                ProviderStatusSnapshot(
                    provider_name=provider_name,
                    status="outage" if failed else ("degraded" if affected else "healthy"),
                    affected_job_ids=[str(job.provider_job_id) for job in affected],
                    completed_artifact_hashes=completed_artifacts,
                    safe_retry_available=bool(failed),
                    cost_estimate_usd=cost,
                    blocker_codes=blocker_codes,
                    recommended_action="RetryProviderJobCommand" if failed else None,
                )
            )
        return statuses

    def _approval_blockers(self, organization_id: UUID, brand_id: UUID | None) -> list[BlockerSummary]:
        if not self.approval_gate_repository:
            return []
        blockers: list[BlockerSummary] = []
        for receipt in self.approval_gate_repository.receipts.values():
            if receipt.organization_id != organization_id or (brand_id and receipt.brand_id != brand_id):
                continue
            for code in receipt.blocker_codes:
                blockers.append(
                    BlockerSummary(
                        blocker_type="approval",
                        blocker_code=code,
                        object_ref=f"{receipt.object_type}:{receipt.object_id}",
                        receipt_id=str(receipt.approval_blocker_receipt_id),
                        required_action="resolve_approval_blocker",
                        allowed_command_type="ApproveMemoryAdmissionCommand" if code.startswith("MEMORY") else "ResolveApprovalBlockerCommand",
                    )
                )
        return blockers

    def _publishing_blockers(self, organization_id: UUID, brand_id: UUID | None) -> list[BlockerSummary]:
        if not self.publishing_repository:
            return []
        blockers: list[BlockerSummary] = []
        for receipt in self.publishing_repository.receipts.values():
            if receipt.organization_id != organization_id or (brand_id and receipt.brand_id != brand_id):
                continue
            for code in receipt.blocker_codes:
                blockers.append(
                    BlockerSummary(
                        blocker_type="publishing",
                        blocker_code=code,
                        object_ref=f"approved_asset:{receipt.approved_asset_id}",
                        receipt_id=str(receipt.publishing_receipt_id),
                        required_action="repair_publishing_intent",
                        allowed_command_type="DraftPublishingIntentCommand",
                    )
                )
        return blockers

    def _memory_blockers(self) -> list[BlockerSummary]:
        if not self.memory_governance_repository:
            return []
        blockers: list[BlockerSummary] = []
        for receipt in self.memory_governance_repository.receipts.values():
            if receipt.resulting_status.value in {"quarantined", "reversed", "expired", "corrected"}:
                blockers.append(
                    BlockerSummary(
                        blocker_type="memory",
                        blocker_code=f"memory_{receipt.resulting_status.value}",
                        object_ref=f"memory_event:{receipt.memory_event_id}",
                        receipt_id=str(receipt.memory_governance_receipt_id),
                        required_action="review_memory_governance",
                        allowed_command_type="ValidateMemoryUsageCommand",
                    )
                )
        return blockers

    def _projection_blockers(self) -> list[BlockerSummary]:
        if not self.projection_repository:
            return []
        health = self.projection_repository.health
        if health.status.value == "healthy":
            return []
        return [
            BlockerSummary(
                blocker_type="projection",
                blocker_code=f"projection_{health.status.value}",
                object_ref="neo4j_relationship_projection",
                receipt_id=str(health.last_checkpoint_id or "projection:no_checkpoint"),
                required_action="rebuild_or_retry_projection",
                allowed_command_type="RebuildNeo4jProjectionCommand",
            )
        ]

    def _incidents(self, *, include_resolved: bool) -> list[IncidentSummary]:
        if not self.recovery_repository:
            return []
        incidents: list[IncidentSummary] = []
        for incident in self.recovery_repository.incidents.values():
            if incident.resolved and not include_resolved:
                continue
            action_ids = [
                str(action.provider_recovery_action_id)
                for action in self.recovery_repository.actions.values()
                if action.provider_job_id == incident.provider_job_id
            ]
            receipt_ids = [
                str(receipt.recovery_receipt_id)
                for receipt in self.recovery_repository.receipts.values()
                if receipt.provider_job_id == incident.provider_job_id
            ]
            incidents.append(
                IncidentSummary(
                    incident_id=str(incident.operational_incident_id),
                    provider_job_id=str(incident.provider_job_id),
                    severity=incident.severity,
                    summary=incident.summary,
                    resolved=incident.resolved,
                    recovery_action_ids=action_ids,
                    receipt_ids=receipt_ids,
                )
            )
        return incidents

    def _workflow_checkpoint_refs(self) -> list[str]:
        if not self.recovery_repository:
            return []
        return [
            f"provider_job_checkpoint:{checkpoint.provider_job_checkpoint_id}:{checkpoint.work_id}:{'complete' if checkpoint.completed else 'pending'}"
            for checkpoint in self.recovery_repository.checkpoints.values()
        ]

    def _cost_snapshot(self) -> CostSnapshot:
        provider_cost = sum((receipt.cost_amount or 0) for receipt in self.provider_repository.receipts.values()) if self.provider_repository else 0
        gpu_cost = sum(report.cost_amount for report in self.gpu_worker_repository.cost_reports.values()) if self.gpu_worker_repository else 0
        recovery_risk = sum(risk.risk_detected * 1.0 for risk in self.recovery_repository.duplicate_cost_risks.values()) if self.recovery_repository else 0
        return CostSnapshot(
            total_cost_usd=provider_cost + gpu_cost + recovery_risk,
            provider_cost_usd=provider_cost,
            gpu_cost_usd=gpu_cost,
            recovery_risk_usd=recovery_risk,
        )

    @staticmethod
    def _recommendations_from_incidents(incidents: list[IncidentSummary]) -> list[RecoveryRecommendation]:
        recommendations: list[RecoveryRecommendation] = []
        for incident in incidents:
            if incident.resolved:
                continue
            recommendations.append(
                RecoveryRecommendation(
                    recommendation_id=uuid4(),
                    object_ref=f"provider_job:{incident.provider_job_id}",
                    recommended_command_type="RetryProviderJobCommand",
                    reason=f"incident:{incident.summary}",
                    receipt_refs=incident.receipt_ids,
                    manual_database_edit_allowed=False,
                )
            )
        return recommendations

    @staticmethod
    def _recommendations_from_blockers(blockers: list[BlockerSummary]) -> list[RecoveryRecommendation]:
        return [
            RecoveryRecommendation(
                recommendation_id=uuid4(),
                object_ref=blocker.object_ref,
                recommended_command_type=blocker.allowed_command_type,
                reason=f"blocker:{blocker.blocker_code}",
                receipt_refs=[blocker.receipt_id],
                manual_database_edit_allowed=False,
            )
            for blocker in blockers
        ]

    def _event(self, event_type: str, state: OperationsBoardState, payload: dict[str, Any]) -> OperationsDomainEvent:
        return self.repository.append_event(
            OperationsDomainEvent(
                schema_version="cmf.operations_domain_event.v1",
                operations_event_id=uuid4(),
                event_type=event_type,
                board_state_id=state.board_state_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class OperationsBoardCommandHandler:
    command_type: str
    service: OperationsBoardService
    aggregate_type: str = "operations"
    allowed_roles: set[str] = field(default_factory=lambda: OPERATIONS_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {"BuildOperationsBoardStateCommand", "RefreshOperationsBoardCommand"}:
            state = self.service.build_operations_board_state(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id if payload.get("brand_scoped", True) else None,
                include_resolved=bool(payload.get("include_resolved", True)),
                idempotency_key=envelope.idempotency_key,
            )
            return state.model_dump(mode="json")
        if self.command_type == "LinkBlockerToObjectCommand":
            return self.service.link_blocker_to_object(**payload).model_dump(mode="json")
        if self.command_type == "RecommendRecoveryActionCommand":
            return self.service.recommend_recovery_action(**payload).model_dump(mode="json")
        if self.command_type == "RecordOperationsReceiptCommand":
            state = self.service.repository.board_states.get(UUID(payload["board_state_id"]))
            if state is None:
                raise OperationsBoardError("OPERATIONS_BOARD_STATE_REQUIRED", "Operations board state is required.")
            return self.service.record_operations_receipt(state).model_dump(mode="json")
        raise OperationsBoardError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        if payload.get("board_state_id"):
            return UUID(payload["board_state_id"])
        return envelope.brand_id


def register_operations_board_command_handlers(bus: CommandBus, service: OperationsBoardService) -> None:
    for command_type in [
        "BuildOperationsBoardStateCommand",
        "RefreshOperationsBoardCommand",
        "LinkBlockerToObjectCommand",
        "RecommendRecoveryActionCommand",
        "RecordOperationsReceiptCommand",
    ]:
        bus.register_handler(OperationsBoardCommandHandler(command_type=command_type, service=service))
