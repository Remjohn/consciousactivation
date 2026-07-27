"""In-memory orchestration repositories for TS-CMF-002."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.orchestration import (
    AgentHandoffPacket,
    FailureReceipt,
    FrictionReceipt,
    HumanHandoffRequest,
    OrchestrationRun,
    QuarantineReceipt,
    StageExecutionPlan,
    StageExecutionReceipt,
    StageRunStatus,
    ValidationContract,
)
from ccp_studio.contracts.skills import SkillInvocationRecord


TERMINAL_STATUSES = {
    StageRunStatus.succeeded,
    StageRunStatus.failed,
    StageRunStatus.quarantined,
    StageRunStatus.compensated,
}


@dataclass
class InMemoryOrchestrationRepository:
    runs: dict[UUID, OrchestrationRun] = field(default_factory=dict)
    plans: dict[UUID, StageExecutionPlan] = field(default_factory=dict)
    validation_contracts: dict[UUID, ValidationContract] = field(default_factory=dict)
    validation_by_plan: dict[UUID, UUID] = field(default_factory=dict)
    handoff_packets: dict[UUID, AgentHandoffPacket] = field(default_factory=dict)
    skill_invocations: dict[UUID, SkillInvocationRecord] = field(default_factory=dict)
    stage_receipts: dict[UUID, StageExecutionReceipt] = field(default_factory=dict)
    failure_receipts: dict[UUID, FailureReceipt] = field(default_factory=dict)
    friction_receipts: dict[UUID, FrictionReceipt] = field(default_factory=dict)
    human_handoffs: dict[UUID, HumanHandoffRequest] = field(default_factory=dict)
    quarantine_receipts: dict[UUID, QuarantineReceipt] = field(default_factory=dict)

    def save_run(self, run: OrchestrationRun) -> OrchestrationRun:
        self.runs[run.orchestration_run_id] = run
        return run

    def get_run(self, orchestration_run_id: UUID) -> OrchestrationRun | None:
        return self.runs.get(orchestration_run_id)

    def find_open_run(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: str,
        object_id: UUID,
        requested_outcome: str,
    ) -> OrchestrationRun | None:
        for run in self.runs.values():
            if run.status in TERMINAL_STATUSES:
                continue
            if (
                run.organization_id == organization_id
                and run.brand_id == brand_id
                and run.active_object.object_type == object_type
                and run.active_object.object_id == object_id
                and run.requested_outcome == requested_outcome
            ):
                return run
        return None

    def save_plan(self, plan: StageExecutionPlan) -> StageExecutionPlan:
        self.plans[plan.stage_execution_plan_id] = plan
        return plan

    def get_plan(self, stage_execution_plan_id: UUID) -> StageExecutionPlan | None:
        return self.plans.get(stage_execution_plan_id)

    def latest_plan_for_run(self, orchestration_run_id: UUID) -> StageExecutionPlan | None:
        matching = [
            plan
            for plan in self.plans.values()
            if plan.orchestration_run_id == orchestration_run_id
        ]
        if not matching:
            return None
        return max(matching, key=lambda item: item.created_at)

    def save_validation_contract(self, contract: ValidationContract) -> ValidationContract:
        self.validation_contracts[contract.validation_contract_id] = contract
        self.validation_by_plan[contract.stage_execution_plan_id] = contract.validation_contract_id
        return contract

    def get_validation_for_plan(self, stage_execution_plan_id: UUID) -> ValidationContract | None:
        contract_id = self.validation_by_plan.get(stage_execution_plan_id)
        if contract_id is None:
            return None
        return self.validation_contracts.get(contract_id)

    def save_handoff_packet(self, packet: AgentHandoffPacket) -> AgentHandoffPacket:
        self.handoff_packets[packet.handoff_packet_id] = packet
        return packet

    def save_skill_invocation(self, record: SkillInvocationRecord) -> SkillInvocationRecord:
        self.skill_invocations[record.skill_invocation_id] = record
        return record

    def save_stage_receipt(self, receipt: StageExecutionReceipt) -> StageExecutionReceipt:
        self.stage_receipts[receipt.receipt_id] = receipt
        return receipt

    def save_failure_receipt(self, receipt: FailureReceipt) -> FailureReceipt:
        self.failure_receipts[receipt.receipt_id] = receipt
        return receipt

    def save_friction_receipt(self, receipt: FrictionReceipt) -> FrictionReceipt:
        self.friction_receipts[receipt.receipt_id] = receipt
        return receipt

    def save_human_handoff(self, request: HumanHandoffRequest) -> HumanHandoffRequest:
        self.human_handoffs[request.handoff_request_id] = request
        return request

    def save_quarantine_receipt(self, receipt: QuarantineReceipt) -> QuarantineReceipt:
        self.quarantine_receipts[receipt.receipt_id] = receipt
        return receipt
