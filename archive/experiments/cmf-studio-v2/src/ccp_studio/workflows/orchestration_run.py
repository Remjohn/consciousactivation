"""Durable-workflow-shaped orchestration helper for TS-CMF-002.

The production deployment can back this with Temporal, Prefect, or another
durable runtime. This local workflow object keeps the same orchestration steps
explicit for tests and early integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    AgentHandoffPacket,
    OrchestrationRun,
    StageExecutionPlan,
    ValidationContract,
)
from ccp_studio.services.orchestration import OrchestrationService


@dataclass
class PreparedStage:
    run: OrchestrationRun
    plan: StageExecutionPlan
    validation_contract: ValidationContract
    handoff_packet: AgentHandoffPacket


@dataclass
class OrchestrationRunWorkflow:
    orchestration_service: OrchestrationService

    def prepare_stage(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        active_object: ActiveObjectRef,
        requested_outcome: str,
        pipeline_stage: str,
        expected_exit_object_type: str,
        allowed_actor_or_service: str,
        required_inputs: list[str],
        allowed_actions: list[str],
        blocked_actions: list[str],
        downstream_proof_obligation: str,
        success_criteria: list[str],
        failure_criteria: list[str],
        required_receipt_types: list[str],
        required_evidence_refs: list[str],
        source_evidence_refs: list[str],
        upstream_receipt_ids: list[UUID],
    ) -> PreparedStage:
        run = self.orchestration_service.open_or_resume_run(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            active_object=active_object,
            requested_outcome=requested_outcome,
        )
        plan = self.orchestration_service.create_stage_execution_plan(
            orchestration_run_id=run.orchestration_run_id,
            pipeline_stage=pipeline_stage,
            expected_exit_object_type=expected_exit_object_type,
            allowed_actor_or_service=allowed_actor_or_service,
            required_inputs=required_inputs,
            allowed_actions=allowed_actions,
            blocked_actions=blocked_actions,
            downstream_proof_obligation=downstream_proof_obligation,
        )
        contract = self.orchestration_service.record_validation_contract(
            stage_execution_plan_id=plan.stage_execution_plan_id,
            success_criteria=success_criteria,
            failure_criteria=failure_criteria,
            required_receipt_types=required_receipt_types,
            required_evidence_refs=required_evidence_refs,
        )
        packet = self.orchestration_service.create_agent_handoff_packet(
            orchestration_run_id=run.orchestration_run_id,
            stage_execution_plan_id=plan.stage_execution_plan_id,
            recipient_type="agent",
            recipient_name=allowed_actor_or_service,
            source_evidence_refs=source_evidence_refs,
            upstream_receipt_ids=upstream_receipt_ids,
        )
        return PreparedStage(
            run=run,
            plan=plan,
            validation_contract=contract,
            handoff_packet=packet,
        )
