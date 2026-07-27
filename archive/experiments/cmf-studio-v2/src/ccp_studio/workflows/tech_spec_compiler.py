"""TechSpecCompilerWorkflow for TS-CMF-003."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    AgentHandoffPacket,
    OrchestrationRun,
    StageExecutionPlan,
    StageExecutionReceipt,
    StageRunStatus,
    ValidationContract,
    new_stage_execution_receipt,
)
from ccp_studio.contracts.spec_governance import (
    SpecAuditReceipt,
    SpecAuditStatus,
    TechSpecSourcePacket,
    TechSpecWorkflow,
)
from ccp_studio.services.orchestration import OrchestrationService
from ccp_studio.services.spec_governance import SpecGovernanceService


@dataclass
class GovernedTechSpecWorkflow:
    tech_spec_workflow: TechSpecWorkflow
    source_packet: TechSpecSourcePacket
    orchestration_run: OrchestrationRun
    stage_plan: StageExecutionPlan
    validation_contract: ValidationContract
    handoff_packet: AgentHandoffPacket


@dataclass
class TechSpecCompilerWorkflow:
    spec_governance_service: SpecGovernanceService
    orchestration_service: OrchestrationService

    def open(
        self,
        *,
        spec_id: str,
        story_path: str,
        actor_id: UUID,
        feature_sources: list[str] | None = None,
    ) -> GovernedTechSpecWorkflow:
        tech_spec_workflow = self.spec_governance_service.open_workflow_from_story(
            spec_id=spec_id,
            story_path=story_path,
            actor_id=actor_id,
        )
        source_packet = self.spec_governance_service.resolve_source_packet(
            workflow_id=tech_spec_workflow.workflow_id,
            feature_sources=feature_sources,
        )
        orchestration_run = self.orchestration_service.open_or_resume_run(
            organization_id=actor_id,
            brand_id=actor_id,
            actor_id=actor_id,
            active_object=ActiveObjectRef(
                object_type="tech_spec_workflow",
                object_id=tech_spec_workflow.workflow_id,
            ),
            requested_outcome="produce spec audit receipt",
        )
        stage_plan = self.orchestration_service.create_stage_execution_plan(
            orchestration_run_id=orchestration_run.orchestration_run_id,
            pipeline_stage="spec-governance overlay",
            expected_exit_object_type="SpecAuditReceipt",
            allowed_actor_or_service="TechSpecCompilerWorkflow",
            required_inputs=[
                "approved story",
                "source packet",
                "files-read receipt",
                "FR trace",
                "pipeline trace",
                "CBAR check",
            ],
            allowed_actions=[
                "record_files_read",
                "compile_requirement_trace",
                "compile_pipeline_stage_trace",
                "run_cbar_check",
                "write_spec_audit_receipt",
            ],
            blocked_actions=[
                "skip_stage",
                "direct_canonical_mutation",
                "self_approve",
                "publish_public",
                "neo4j_authorize_transition",
            ],
            downstream_proof_obligation="spec_audit_receipt with source, trace, and CBAR evidence",
        )
        validation_contract = self.orchestration_service.record_validation_contract(
            stage_execution_plan_id=stage_plan.stage_execution_plan_id,
            success_criteria=[
                "all required files read",
                "FR trace recorded",
                "pipeline stage trace recorded",
                "CBAR check recorded",
                "greenfield alignment lint passed",
            ],
            failure_criteria=[
                "missing required source",
                "missing trace",
                "old-stack assumption",
                "legacy runtime import",
            ],
            required_receipt_types=["spec_audit_receipt"],
            required_evidence_refs=[
                "files_read_receipt",
                "requirement_trace",
                "pipeline_stage_trace",
                "cbar_check",
            ],
        )
        handoff_packet = self.orchestration_service.create_agent_handoff_packet(
            orchestration_run_id=orchestration_run.orchestration_run_id,
            stage_execution_plan_id=stage_plan.stage_execution_plan_id,
            recipient_type="workflow",
            recipient_name="TechSpecCompilerWorkflow",
            source_evidence_refs=[ref.path for ref in source_packet.required_sources],
            upstream_receipt_ids=[],
        )
        return GovernedTechSpecWorkflow(
            tech_spec_workflow=tech_spec_workflow,
            source_packet=source_packet,
            orchestration_run=orchestration_run,
            stage_plan=stage_plan,
            validation_contract=validation_contract,
            handoff_packet=handoff_packet,
        )

    def close_with_audit_receipt(
        self,
        *,
        governed_workflow: GovernedTechSpecWorkflow,
        audit_receipt: SpecAuditReceipt,
    ) -> StageExecutionReceipt:
        status = (
            StageRunStatus.succeeded
            if audit_receipt.status == SpecAuditStatus.accepted
            else StageRunStatus.blocked
        )
        receipt = new_stage_execution_receipt(
            orchestration_run_id=governed_workflow.orchestration_run.orchestration_run_id,
            stage_execution_plan_id=governed_workflow.stage_plan.stage_execution_plan_id,
            receipt_type="spec_audit_receipt",
            status=status,
            decision=audit_receipt.status.value,
            evidence_refs=[
                "files_read_receipt",
                "requirement_trace",
                "pipeline_stage_trace",
                "cbar_check",
                f"spec_audit_receipt:{audit_receipt.spec_audit_receipt_id}",
            ],
            correlation_id=governed_workflow.orchestration_run.correlation_id,
        )
        return self.orchestration_service.close_stage_execution(receipt)
