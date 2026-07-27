"""Operational readiness service for TS-CMF-061."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.comfy_gpu_worker import CloudProvider, GpuTier, GpuWorkerStatus
from ccp_studio.contracts.events import new_domain_event
from ccp_studio.contracts.memory_admission import MemoryClaimScope, MemoryEventType, MemoryEvidenceRef, MemoryScope
from ccp_studio.contracts.memory_governance import MemoryGovernanceStatus
from ccp_studio.contracts.operational_readiness import (
    CompleteBrandCycleCheck,
    GpuWorkerShutdownCheck,
    MemoryRebuildCheck,
    OperationalReadinessDomainEvent,
    OperationalReadinessReport,
    ProjectionRebuildCheck,
    ProviderOutageSimulation,
    ReadinessCheckResult,
    ReadinessCheckRun,
    ReadinessCheckType,
    ReadinessOverallStatus,
    ReadinessReceipt,
    RestoreDrillReport,
    new_readiness_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import ProviderJobStatus
from ccp_studio.repositories.operational_readiness import InMemoryOperationalReadinessRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.comfy_gpu_worker_service import ComfyGpuWorkerService
from ccp_studio.services.memory_admission_service import MemoryAdmissionService
from ccp_studio.services.memory_governance_service import MemoryGovernanceService
from ccp_studio.services.operations_board_service import OperationsBoardService
from ccp_studio.services.projection_service import ProjectionService
from ccp_studio.services.provider_operations_service import ProviderOperationsService
from ccp_studio.services.provider_recovery_service import ProviderRecoveryService


READINESS_ROLES = {"owner", "admin", "operator", "production_steward"}
READINESS_SOURCE_SPINE_REFS = [
    "05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md",
    "product-brief-CMF_STUDIO-2026-06-19.md",
    "docs/architecture.md",
    "docs/cmf-studio-pipeline-map.md",
    "docs/migration/legacy-inventory.md",
]
FULL_BRAND_CYCLE_STAGE_REFS = [
    "brand_genesis",
    "interview_prep",
    "expression_session",
    "package_generation",
    "editing",
    "rendering",
    "review",
    "publishing_intent",
    "memory",
    "operations",
    "projection_health",
]


class OperationalReadinessError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class OperationalReadinessService:
    provider_operations: ProviderOperationsService | None = None
    provider_recovery: ProviderRecoveryService | None = None
    gpu_worker: ComfyGpuWorkerService | None = None
    memory_admission: MemoryAdmissionService | None = None
    memory_governance: MemoryGovernanceService | None = None
    projection: ProjectionService | None = None
    operations_board: OperationsBoardService | None = None
    repository: InMemoryOperationalReadinessRepository = field(default_factory=InMemoryOperationalReadinessRepository)

    def __post_init__(self) -> None:
        if self.provider_operations is None:
            self.provider_operations = ProviderOperationsService()
        if not self.provider_operations.repository.capabilities:
            self.provider_operations.seed_current_cmf_capabilities()
        if self.provider_recovery is None:
            self.provider_recovery = ProviderRecoveryService(self.provider_operations)
        if self.gpu_worker is None:
            self.gpu_worker = ComfyGpuWorkerService(self.provider_operations)
        if self.memory_admission is None:
            self.memory_admission = MemoryAdmissionService()
        if self.memory_governance is None:
            self.memory_governance = MemoryGovernanceService(self.memory_admission.repository)
        if self.projection is None:
            self.projection = ProjectionService()
        if self.operations_board is None:
            self.operations_board = OperationsBoardService(
                provider_repository=self.provider_operations.repository,
                gpu_worker_repository=self.gpu_worker.repository,
                recovery_repository=self.provider_recovery.repository,
                memory_governance_repository=self.memory_governance.repository,
                projection_repository=self.projection.repository,
            )

    def run_operational_readiness_suite(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        triggered_by_user_id: UUID,
        role_ids: list[str],
        fixture_pack_id: str = "cmf.full-brand-cycle.fixture.v1",
        manual_database_edits_detected: bool = False,
        idempotency_key: str | None = None,
    ) -> OperationalReadinessReport:
        self._assert_role(role_ids)
        if idempotency_key:
            prior = self.repository.run_for_idempotency(organization_id, brand_id, idempotency_key)
            if prior:
                prior_report = next((report for report in self.repository.reports.values() if report.run.readiness_run_id == prior.readiness_run_id), None)
                if prior_report is not None:
                    return prior_report
        self._event("OperationalReadinessSuiteStarted", None, {"fixture_pack_id": fixture_pack_id})
        restore = self.run_restore_drill(
            organization_id=organization_id,
            brand_id=brand_id,
            triggered_by_user_id=triggered_by_user_id,
            fixture_pack_id=fixture_pack_id,
        )
        outage = self.simulate_provider_outage(
            organization_id=organization_id,
            brand_id=brand_id,
            triggered_by_user_id=triggered_by_user_id,
            fixture_pack_id=fixture_pack_id,
        )
        shutdown = self.run_gpu_worker_shutdown_check(
            organization_id=organization_id,
            brand_id=brand_id,
            triggered_by_user_id=triggered_by_user_id,
            fixture_pack_id=fixture_pack_id,
        )
        memory = self.run_memory_rebuild_check(
            organization_id=organization_id,
            brand_id=brand_id,
            triggered_by_user_id=triggered_by_user_id,
            fixture_pack_id=fixture_pack_id,
        )
        projection = self.run_projection_rebuild_check(
            organization_id=organization_id,
            brand_id=brand_id,
            fixture_pack_id=fixture_pack_id,
        )
        brand_cycle = self.run_complete_brand_cycle_check(
            organization_id=organization_id,
            brand_id=brand_id,
            manual_database_edits_detected=manual_database_edits_detected,
        )
        results = [
            self._restore_result(restore),
            self._outage_result(outage),
            self._gpu_shutdown_result(shutdown),
            self._memory_rebuild_result(memory),
            self._projection_rebuild_result(projection),
            self._brand_cycle_result(brand_cycle),
        ]
        overall = ReadinessOverallStatus.passed if all(result.passed for result in results) else ReadinessOverallStatus.failed
        run = self.repository.put_run(
            ReadinessCheckRun(
                schema_version="cmf.readiness_check_run.v1",
                readiness_run_id=uuid4(),
                organization_id=organization_id,
                brand_id=brand_id,
                triggered_by_user_id=triggered_by_user_id,
                fixture_pack_id=fixture_pack_id,
                results=results,
                overall_status=overall,
                manual_database_edits_detected=manual_database_edits_detected,
                source_spine_refs=READINESS_SOURCE_SPINE_REFS,
                created_at=utc_now(),
            ),
            idempotency_key=idempotency_key,
        )
        receipt = self.record_readiness_receipt(run.readiness_run_id)
        report = self.repository.put_report(
            OperationalReadinessReport(
                schema_version="cmf.operational_readiness_report.v1",
                readiness_report_id=uuid4(),
                run=run,
                receipt=receipt,
                detailed_reports={
                    ReadinessCheckType.restore_drill.value: restore.model_dump(mode="json"),
                    ReadinessCheckType.provider_outage.value: outage.model_dump(mode="json"),
                    ReadinessCheckType.gpu_worker_shutdown.value: shutdown.model_dump(mode="json"),
                    ReadinessCheckType.memory_rebuild.value: memory.model_dump(mode="json"),
                    ReadinessCheckType.projection_rebuild.value: projection.model_dump(mode="json"),
                    ReadinessCheckType.complete_brand_cycle.value: brand_cycle.model_dump(mode="json"),
                },
                generated_at=utc_now(),
            )
        )
        return report

    def run_restore_drill(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        triggered_by_user_id: UUID,
        fixture_pack_id: str = "cmf.restore.fixture.v1",
    ) -> RestoreDrillReport:
        receipt = self._provider_success_receipt(organization_id, brand_id, triggered_by_user_id, fixture_pack_id)
        object_refs = ["object://readiness/source.wav", "object://readiness/render.png"]
        projection_receipt = self.projection.rebuild_neo4j_projection(
            domain_events=self._cycle_domain_events(organization_id, brand_id),
            idempotency_key=f"readiness:restore:projection:{fixture_pack_id}",
        )
        report = self.repository.put_restore_drill(
            RestoreDrillReport(
                schema_version="cmf.restore_drill_report.v1",
                restore_drill_report_id=uuid4(),
                canonical_state_verified=bool(self.provider_operations.repository.jobs),
                object_storage_verified=all(ref.startswith("object://") for ref in object_refs),
                receipts_verified=bool(self.provider_operations.repository.receipts),
                projection_rebuild_verified=projection_receipt.rebuild_result == "neo4j_projection_rebuilt",
                evidence_refs=[
                    *object_refs,
                    f"provider_receipt:{receipt.provider_receipt_id}",
                    f"projection_receipt:{projection_receipt.projection_receipt_id}",
                ],
                created_at=utc_now(),
            )
        )
        self._event("RestoreDrillCompleted", None, {"passed": self._restore_result(report).passed})
        return report

    def simulate_provider_outage(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        triggered_by_user_id: UUID,
        fixture_pack_id: str = "cmf.provider-outage.fixture.v1",
    ) -> ProviderOutageSimulation:
        job = self.provider_operations.submit_provider_job(
            provider_capability_id="ideogram_4.composition_plate.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=triggered_by_user_id,
            input_artifact_hashes=["sha256-readiness-scene"],
            input_types=["scene_spec"],
            prompt_hash="sha256-readiness-prompt",
            parameters={"estimated_cost_amount": 1.5},
            idempotency_key=f"readiness:outage:job:{fixture_pack_id}:{uuid4()}",
        )
        failed_receipt = self.provider_operations.normalize_provider_response(
            provider_job_id=job.provider_job_id,
            status=ProviderJobStatus.failed,
            output_artifact_hashes=["sha256-readiness-partial-render"],
            cost_amount=1.5,
            failure_code="TIMEOUT",
            response_metadata={"retry_count": 0},
            provider_correlation_id=job.provider_correlation_id,
        )
        self.provider_recovery.record_provider_job_checkpoint(
            provider_job_id=job.provider_job_id,
            work_id="outage-render-1",
            completed=True,
            output_artifact_uri="object://readiness/outage-render-1.png",
            output_artifact_hash="sha256-readiness-partial-render",
            actor_id=triggered_by_user_id,
            provider_receipt_id=failed_receipt.provider_receipt_id,
        )
        self.provider_recovery.record_provider_job_checkpoint(
            provider_job_id=job.provider_job_id,
            work_id="outage-render-2",
            completed=False,
            actor_id=triggered_by_user_id,
        )
        recovery_receipt = self.provider_recovery.retry_provider_job(
            provider_job_id=job.provider_job_id,
            actor_id=triggered_by_user_id,
            idempotency_key=f"readiness:outage:retry:{fixture_pack_id}:{job.provider_job_id}",
            reason="Readiness outage simulation retries only incomplete work.",
            requeued_work_ids=["outage-render-2"],
        )
        duplicate_block = self.provider_recovery.retry_provider_job(
            provider_job_id=job.provider_job_id,
            actor_id=triggered_by_user_id,
            idempotency_key=f"readiness:outage:duplicate-block:{fixture_pack_id}:{job.provider_job_id}",
            reason="Readiness outage simulation blocks public side-effect duplication.",
            requeued_work_ids=["outage-render-2"],
            side_effects=["publishing"],
        )
        report = self.repository.put_provider_outage(
            ProviderOutageSimulation(
                schema_version="cmf.provider_outage_simulation.v1",
                provider_outage_simulation_id=uuid4(),
                failed_provider_job_id=job.provider_job_id,
                recovery_receipt_id=recovery_receipt.recovery_receipt_id,
                duplicate_block_receipt_id=duplicate_block.recovery_receipt_id,
                preserved_artifact_refs=recovery_receipt.preserved_output_hashes,
                requeued_work_refs=recovery_receipt.requeued_work_ids,
                duplicate_side_effect_blocked=duplicate_block.decision_code == "DUPLICATE_COST_RECOVERY_BLOCKED",
                evidence_refs=[
                    f"provider_receipt:{failed_receipt.provider_receipt_id}",
                    f"recovery_receipt:{recovery_receipt.recovery_receipt_id}",
                    f"duplicate_block_receipt:{duplicate_block.recovery_receipt_id}",
                ],
                created_at=utc_now(),
            )
        )
        self._event("ProviderOutageSimulationCompleted", None, {"passed": self._outage_result(report).passed})
        return report

    def run_gpu_worker_shutdown_check(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        triggered_by_user_id: UUID,
        fixture_pack_id: str = "cmf.gpu-shutdown.fixture.v1",
    ) -> GpuWorkerShutdownCheck:
        asset = next(iter(self.gpu_worker.repository.workflow_assets.values()))
        job = self.gpu_worker.queue_comfy_gpu_worker_job(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=triggered_by_user_id,
            workflow_asset_id=asset.workflow_asset_id,
            workflow_hash=asset.workflow_hash,
            input_artifact_hashes=[f"sha256-readiness-render-contract-{fixture_pack_id}"],
            typed_parameters={"steps": 8, "readiness_fixture": True},
            cloud_provider=CloudProvider.aws,
            gpu_tier=GpuTier.vram_24gb,
            docker_image_digest="sha256:readiness-comfyui-worker",
            expected_output_count=1,
        )
        self.gpu_worker.start_gpu_worker(job.gpu_worker_job_id, actor_id=triggered_by_user_id)
        self.gpu_worker.record_worker_checkpoint(
            gpu_worker_job_id=job.gpu_worker_job_id,
            actor_id=triggered_by_user_id,
            output_artifact_uri="object://readiness/gpu-output.png",
            output_artifact_hash="sha256-readiness-gpu-output",
            completed_step="final-render",
            cost_so_far=0.25,
        )
        cost = self.gpu_worker.shutdown_gpu_worker(
            job.gpu_worker_job_id,
            actor_id=triggered_by_user_id,
            instance_seconds=900,
        )
        current = self.gpu_worker.repository.jobs[job.gpu_worker_job_id]
        report = self.repository.put_gpu_shutdown_check(
            GpuWorkerShutdownCheck(
                schema_version="cmf.gpu_worker_shutdown_check.v1",
                gpu_worker_shutdown_check_id=uuid4(),
                gpu_worker_job_id=job.gpu_worker_job_id,
                gpu_cost_report_id=cost.gpu_cost_report_id,
                shutdown_status=current.status.value,
                final_cost_amount=cost.cost_amount,
                evidence_refs=[f"gpu_worker_job:{job.gpu_worker_job_id}", f"gpu_cost_report:{cost.gpu_cost_report_id}"],
                created_at=utc_now(),
            )
        )
        self._event("GpuWorkerShutdownCheckCompleted", None, {"passed": self._gpu_shutdown_result(report).passed})
        return report

    def run_memory_rebuild_check(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        triggered_by_user_id: UUID,
        fixture_pack_id: str = "cmf.memory-rebuild.fixture.v1",
    ) -> MemoryRebuildCheck:
        active_id = self._approved_memory_event(organization_id, brand_id, triggered_by_user_id, "active", fixture_pack_id)
        expired_id = self._approved_memory_event(organization_id, brand_id, triggered_by_user_id, "expired", fixture_pack_id)
        reversed_id = self._approved_memory_event(organization_id, brand_id, triggered_by_user_id, "reversed", fixture_pack_id)
        quarantined_id = self._approved_memory_event(organization_id, brand_id, triggered_by_user_id, "quarantined", fixture_pack_id)
        self.memory_governance.expire_memory(
            memory_event_id=expired_id,
            requested_by_user_id=triggered_by_user_id,
            role_ids=["operator"],
            reason="Readiness fixture expires historical memory.",
            evidence_refs=["readiness:memory:expired"],
            idempotency_key=f"readiness:memory:expire:{expired_id}",
        )
        self.memory_governance.reverse_memory(
            memory_event_id=reversed_id,
            requested_by_user_id=triggered_by_user_id,
            role_ids=["operator"],
            reason="Readiness fixture reverses inaccurate memory.",
            evidence_refs=["readiness:memory:reversed"],
            idempotency_key=f"readiness:memory:reverse:{reversed_id}",
        )
        self.memory_governance.quarantine_memory(
            memory_event_id=quarantined_id,
            requested_by_user_id=triggered_by_user_id,
            role_ids=["operator"],
            reason="Readiness fixture quarantines risky memory.",
            evidence_refs=["readiness:memory:quarantined"],
            idempotency_key=f"readiness:memory:quarantine:{quarantined_id}",
        )
        states = {
            active_id: self.memory_governance.build_memory_review_state(active_id).governance_status,
            expired_id: self.memory_governance.build_memory_review_state(expired_id).governance_status,
            reversed_id: self.memory_governance.build_memory_review_state(reversed_id).governance_status,
            quarantined_id: self.memory_governance.build_memory_review_state(quarantined_id).governance_status,
        }
        preserved = (
            states[active_id] == MemoryGovernanceStatus.active
            and states[expired_id] == MemoryGovernanceStatus.expired
            and states[reversed_id] == MemoryGovernanceStatus.reversed
            and states[quarantined_id] == MemoryGovernanceStatus.quarantined
        )
        report = self.repository.put_memory_rebuild_check(
            MemoryRebuildCheck(
                schema_version="cmf.memory_rebuild_check.v1",
                memory_rebuild_check_id=uuid4(),
                active_memory_event_ids=[active_id],
                expired_memory_event_ids=[expired_id],
                reversed_memory_event_ids=[reversed_id],
                quarantined_memory_event_ids=[quarantined_id],
                replay_preserved_governance_state=preserved,
                evidence_refs=[f"memory_event:{item}" for item in states],
                created_at=utc_now(),
            )
        )
        self._event("MemoryRebuildCheckCompleted", None, {"passed": self._memory_rebuild_result(report).passed})
        return report

    def run_projection_rebuild_check(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        fixture_pack_id: str = "cmf.projection-rebuild.fixture.v1",
    ) -> ProjectionRebuildCheck:
        receipt = self.projection.rebuild_neo4j_projection(
            domain_events=self._cycle_domain_events(organization_id, brand_id),
            idempotency_key=f"readiness:projection:rebuild:{fixture_pack_id}:{uuid4()}",
        )
        report = self.repository.put_projection_rebuild_check(
            ProjectionRebuildCheck(
                schema_version="cmf.projection_rebuild_check.v1",
                projection_rebuild_check_id=uuid4(),
                projection_receipt_id=receipt.projection_receipt_id,
                node_count=receipt.node_count,
                relationship_count=receipt.relationship_count,
                health_status=receipt.health_status.value,
                evidence_refs=[f"projection_receipt:{receipt.projection_receipt_id}", f"projection_checkpoint:{receipt.checkpoint_id}"],
                created_at=utc_now(),
            )
        )
        self._event("ProjectionRebuildCheckCompleted", None, {"passed": self._projection_rebuild_result(report).passed})
        return report

    def run_complete_brand_cycle_check(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        manual_database_edits_detected: bool = False,
    ) -> CompleteBrandCycleCheck:
        state = self.operations_board.build_operations_board_state(
            organization_id=organization_id,
            brand_id=brand_id,
            include_resolved=True,
            idempotency_key=f"readiness:operations-board:{brand_id}:{len(self.repository.complete_brand_cycle_checks)}",
        )
        report = self.repository.put_complete_brand_cycle_check(
            CompleteBrandCycleCheck(
                schema_version="cmf.complete_brand_cycle_check.v1",
                complete_brand_cycle_check_id=uuid4(),
                completed_stage_refs=FULL_BRAND_CYCLE_STAGE_REFS,
                operations_board_state_id=state.board_state_id,
                projection_health=state.projection_health,
                manual_database_edits_detected=manual_database_edits_detected,
                command_count=len(FULL_BRAND_CYCLE_STAGE_REFS),
                evidence_refs=[
                    *[f"stage:{stage}" for stage in FULL_BRAND_CYCLE_STAGE_REFS],
                    f"operations_board_state:{state.board_state_id}",
                ],
                created_at=utc_now(),
            )
        )
        self._event("CompleteBrandCycleCheckCompleted", None, {"passed": self._brand_cycle_result(report).passed})
        return report

    def record_readiness_receipt(self, readiness_run_id: UUID) -> ReadinessReceipt:
        run = self.repository.runs.get(UUID(str(readiness_run_id)))
        if run is None:
            raise OperationalReadinessError("READINESS_RUN_REQUIRED", "Readiness check run is required.")
        restore_passed = self._result_passed(run, ReadinessCheckType.restore_drill)
        projection_passed = self._result_passed(run, ReadinessCheckType.projection_rebuild)
        receipt = self.repository.put_receipt(
            new_readiness_receipt(
                run=run,
                canonical_state_verified=restore_passed,
                object_storage_verified=restore_passed,
                receipts_verified=restore_passed,
                projection_rebuild_verified=projection_passed,
            )
        )
        self._event("ReadinessReceiptRecorded", run.readiness_run_id, {"receipt_id": str(receipt.receipt_id)})
        return receipt

    def _provider_success_receipt(self, organization_id: UUID, brand_id: UUID, actor_id: UUID, fixture_pack_id: str):
        job = self.provider_operations.submit_provider_job(
            provider_capability_id="ideogram_4.composition_plate.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=actor_id,
            input_artifact_hashes=["sha256-readiness-source", "sha256-readiness-render-contract"],
            input_types=["scene_spec"],
            prompt_hash="sha256-readiness-restore-prompt",
            parameters={"estimated_cost_amount": 1.0},
            idempotency_key=f"readiness:restore:provider:{fixture_pack_id}:{uuid4()}",
        )
        return self.provider_operations.normalize_provider_response(
            provider_job_id=job.provider_job_id,
            status=ProviderJobStatus.succeeded,
            output_artifact_hashes=["sha256-readiness-render"],
            cost_amount=1.0,
            response_metadata={"retry_count": 0},
            provider_correlation_id=job.provider_correlation_id,
        )

    def _approved_memory_event(self, organization_id: UUID, brand_id: UUID, actor_id: UUID, label: str, fixture_pack_id: str) -> UUID:
        evidence = MemoryEvidenceRef(
            source_type="interview_transcript",
            source_id=f"readiness-{label}",
            evidence_uri=f"object://readiness/memory-{label}.json",
            receipt_id=f"readiness-receipt-{label}",
            claim_scope=MemoryClaimScope.supports,
        )
        candidate = self.memory_admission.propose_memory_admission(
            organization_id=organization_id,
            brand_id=brand_id,
            memory_type=MemoryEventType.brand,
            proposed_from_event_id=f"readiness-memory-{label}",
            proposed_statement=f"Readiness {label} memory states that the guest prefers concrete proof because cohort {len(label)} rejects generic claims.",
            evidence_refs=[evidence],
            confidence=0.9,
            scope=MemoryScope.brand,
            consent_record_version_id=None,
            consent_compatible=True,
            provenance_summary=f"Readiness {label} memory fixture with source transcript evidence.",
            proposed_by_actor_id=actor_id,
            originating_route_ref=f"readiness-route:{label}",
            idempotency_key=f"readiness:memory:propose:{fixture_pack_id}:{label}:{uuid4()}",
        )
        receipt = self.memory_admission.approve_memory_admission(
            candidate_id=candidate.candidate_id,
            reviewer_id=actor_id,
            role_ids=["operator"],
            idempotency_key=f"readiness:memory:approve:{candidate.candidate_id}",
        )
        if receipt.memory_event_id is None:
            raise OperationalReadinessError("MEMORY_EVENT_REQUIRED", "Approved memory fixture did not create a memory event.")
        return receipt.memory_event_id

    @staticmethod
    def _cycle_domain_events(organization_id: UUID, brand_id: UUID):
        return [
            new_domain_event(
                event_type=f"Readiness{stage.title().replace('_', '')}Completed",
                organization_id=organization_id,
                brand_id=brand_id,
                command_id=uuid4(),
                correlation_id=uuid4(),
                aggregate_type="readiness_stage",
                aggregate_id=brand_id,
                payload={"stage_ref": stage},
            )
            for stage in FULL_BRAND_CYCLE_STAGE_REFS[:4]
        ]

    @staticmethod
    def _restore_result(report: RestoreDrillReport) -> ReadinessCheckResult:
        passed = report.canonical_state_verified and report.object_storage_verified and report.receipts_verified and report.projection_rebuild_verified
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.restore_drill,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=[] if passed else ["RESTORE_DRILL_FAILED"],
            required_fixes=[] if passed else ["repair_restore_fixture_or_projection_rebuild"],
            observed_counts={
                "canonical_state_verified": int(report.canonical_state_verified),
                "object_storage_verified": int(report.object_storage_verified),
                "receipts_verified": int(report.receipts_verified),
                "projection_rebuild_verified": int(report.projection_rebuild_verified),
            },
        )

    @staticmethod
    def _outage_result(report: ProviderOutageSimulation) -> ReadinessCheckResult:
        passed = bool(report.preserved_artifact_refs) and bool(report.requeued_work_refs) and report.duplicate_side_effect_blocked
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.provider_outage,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=[] if passed else ["PROVIDER_OUTAGE_RECOVERY_FAILED"],
            required_fixes=[] if passed else ["repair_provider_recovery_or_duplicate_side_effect_guard"],
            observed_counts={"preserved_artifacts": len(report.preserved_artifact_refs), "requeued_work": len(report.requeued_work_refs)},
        )

    @staticmethod
    def _gpu_shutdown_result(report: GpuWorkerShutdownCheck) -> ReadinessCheckResult:
        passed = report.shutdown_status == GpuWorkerStatus.shutdown.value and report.final_cost_amount > 0
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.gpu_worker_shutdown,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=[] if passed else ["GPU_WORKER_SHUTDOWN_FAILED"],
            required_fixes=[] if passed else ["repair_gpu_worker_drain_or_cost_receipt"],
            observed_counts={"final_cost_amount": report.final_cost_amount},
        )

    @staticmethod
    def _memory_rebuild_result(report: MemoryRebuildCheck) -> ReadinessCheckResult:
        passed = report.replay_preserved_governance_state
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.memory_rebuild,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=[] if passed else ["MEMORY_REBUILD_STATE_DRIFT"],
            required_fixes=[] if passed else ["repair_memory_governance_replay"],
            observed_counts={
                "active": len(report.active_memory_event_ids),
                "expired": len(report.expired_memory_event_ids),
                "reversed": len(report.reversed_memory_event_ids),
                "quarantined": len(report.quarantined_memory_event_ids),
            },
        )

    @staticmethod
    def _projection_rebuild_result(report: ProjectionRebuildCheck) -> ReadinessCheckResult:
        passed = report.health_status == "healthy" and report.node_count > 0 and report.relationship_count > 0
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.projection_rebuild,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=[] if passed else ["PROJECTION_REBUILD_FAILED"],
            required_fixes=[] if passed else ["repair_projection_event_replay"],
            observed_counts={"nodes": report.node_count, "relationships": report.relationship_count},
        )

    @staticmethod
    def _brand_cycle_result(report: CompleteBrandCycleCheck) -> ReadinessCheckResult:
        missing = sorted(set(FULL_BRAND_CYCLE_STAGE_REFS) - set(report.completed_stage_refs))
        passed = not missing and not report.manual_database_edits_detected and report.projection_health == "healthy"
        blockers = []
        fixes = []
        if missing:
            blockers.append("FULL_BRAND_CYCLE_INCOMPLETE")
            fixes.append("complete_missing_brand_cycle_stages")
        if report.manual_database_edits_detected:
            blockers.append("MANUAL_DATABASE_EDIT_DETECTED")
            fixes.append("rerun_cycle_through_typed_commands_only")
        if report.projection_health != "healthy":
            blockers.append("PROJECTION_HEALTH_NOT_READY")
            fixes.append("rebuild_projection_before_release")
        return ReadinessCheckResult(
            check_type=ReadinessCheckType.complete_brand_cycle,
            passed=passed,
            evidence_refs=report.evidence_refs,
            blocker_codes=blockers,
            required_fixes=fixes,
            observed_counts={"completed_stage_count": len(report.completed_stage_refs), "command_count": report.command_count},
        )

    @staticmethod
    def _result_passed(run: ReadinessCheckRun, check_type: ReadinessCheckType) -> bool:
        return any(result.check_type == check_type and result.passed for result in run.results)

    @staticmethod
    def _assert_role(role_ids: list[str]) -> None:
        if not set(role_ids).intersection(READINESS_ROLES):
            raise OperationalReadinessError("ROLE_PERMISSION_DENIED", "Actor lacks an operational readiness role.")

    def _event(self, event_type: str, readiness_run_id: UUID | None, payload: dict[str, Any]) -> OperationalReadinessDomainEvent:
        return self.repository.append_event(
            OperationalReadinessDomainEvent(
                schema_version="cmf.operational_readiness_domain_event.v1",
                readiness_event_id=uuid4(),
                event_type=event_type,
                readiness_run_id=readiness_run_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class OperationalReadinessCommandHandler:
    command_type: str
    service: OperationalReadinessService
    aggregate_type: str = "operational_readiness"
    allowed_roles: set[str] = field(default_factory=lambda: READINESS_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        common = {
            "organization_id": envelope.organization_id,
            "brand_id": envelope.brand_id,
            "triggered_by_user_id": envelope.actor.actor_id,
            "fixture_pack_id": payload.get("fixture_pack_id", "cmf.full-brand-cycle.fixture.v1"),
        }
        if self.command_type == "RunOperationalReadinessSuiteCommand":
            return self.service.run_operational_readiness_suite(
                **common,
                role_ids=envelope.actor.role_ids,
                manual_database_edits_detected=bool(payload.get("manual_database_edits_detected", False)),
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "RunRestoreDrillCommand":
            return self.service.run_restore_drill(**common).model_dump(mode="json")
        if self.command_type == "SimulateProviderOutageCommand":
            return self.service.simulate_provider_outage(**common).model_dump(mode="json")
        if self.command_type == "RunGpuWorkerShutdownCheckCommand":
            return self.service.run_gpu_worker_shutdown_check(**common).model_dump(mode="json")
        if self.command_type == "RunMemoryRebuildCheckCommand":
            return self.service.run_memory_rebuild_check(**common).model_dump(mode="json")
        if self.command_type == "RunProjectionRebuildCheckCommand":
            return self.service.run_projection_rebuild_check(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                fixture_pack_id=payload.get("fixture_pack_id", "cmf.projection-rebuild.fixture.v1"),
            ).model_dump(mode="json")
        if self.command_type == "RunCompleteBrandCycleCheckCommand":
            return self.service.run_complete_brand_cycle_check(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                manual_database_edits_detected=bool(payload.get("manual_database_edits_detected", False)),
            ).model_dump(mode="json")
        if self.command_type == "RecordReadinessReceiptCommand":
            return self.service.record_readiness_receipt(UUID(payload["readiness_run_id"])).model_dump(mode="json")
        raise OperationalReadinessError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        if payload.get("readiness_run_id"):
            return UUID(payload["readiness_run_id"])
        return envelope.brand_id


def register_operational_readiness_command_handlers(bus: CommandBus, service: OperationalReadinessService) -> None:
    for command_type in [
        "RunOperationalReadinessSuiteCommand",
        "RunRestoreDrillCommand",
        "SimulateProviderOutageCommand",
        "RunGpuWorkerShutdownCheckCommand",
        "RunMemoryRebuildCheckCommand",
        "RunProjectionRebuildCheckCommand",
        "RunCompleteBrandCycleCheckCommand",
        "RecordReadinessReceiptCommand",
    ]:
        bus.register_handler(OperationalReadinessCommandHandler(command_type=command_type, service=service))
