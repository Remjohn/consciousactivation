"""Stage-bound orchestration service for TS-CMF-002."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import ActorContext, CommandResult, new_command_envelope
from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
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
    new_agent_handoff_packet,
    new_orchestration_run,
    new_stage_execution_plan,
    new_validation_contract,
    utc_now,
)
from ccp_studio.contracts.skills import SkillInvocationRecord, new_skill_invocation_record
from ccp_studio.repositories.orchestration import InMemoryOrchestrationRepository
from ccp_studio.services.command_bus import CommandBus


FORBIDDEN_ACTION_CODES = {
    "skip_stage": "PIPELINE_STAGE_MISMATCH",
    "direct_canonical_mutation": "DIRECT_CANONICAL_MUTATION_FORBIDDEN",
    "self_approve": "SELF_APPROVAL_FORBIDDEN",
    "approve_own_output": "SELF_APPROVAL_FORBIDDEN",
    "publish_public": "PUBLICATION_APPROVAL_REQUIRED",
    "neo4j_authorize_transition": "PROJECTION_NOT_CANONICAL",
}


class OrchestrationValidationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class OrchestrationService:
    repository: InMemoryOrchestrationRepository = field(
        default_factory=InMemoryOrchestrationRepository
    )

    def open_or_resume_run(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        active_object: ActiveObjectRef,
        requested_outcome: str,
    ) -> OrchestrationRun:
        existing = self.repository.find_open_run(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=active_object.object_type,
            object_id=active_object.object_id,
            requested_outcome=requested_outcome,
        )
        if existing is not None:
            return existing

        run = new_orchestration_run(
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            active_object=active_object,
            requested_outcome=requested_outcome,
        )
        return self.repository.save_run(run)

    def create_stage_execution_plan(
        self,
        *,
        orchestration_run_id: UUID,
        pipeline_stage: str,
        expected_exit_object_type: str,
        allowed_actor_or_service: str,
        required_inputs: list[str],
        allowed_actions: list[str],
        blocked_actions: list[str],
        downstream_proof_obligation: str,
    ) -> StageExecutionPlan:
        run = self._require_run(orchestration_run_id)
        plan = new_stage_execution_plan(
            orchestration_run_id=run.orchestration_run_id,
            pipeline_stage=pipeline_stage,
            entry_object=run.active_object,
            expected_exit_object_type=expected_exit_object_type,
            allowed_actor_or_service=allowed_actor_or_service,
            required_inputs=required_inputs,
            allowed_actions=allowed_actions,
            blocked_actions=blocked_actions,
            downstream_proof_obligation=downstream_proof_obligation,
        )
        run.status = StageRunStatus.planned
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_plan(plan)

    def record_validation_contract(
        self,
        *,
        stage_execution_plan_id: UUID,
        success_criteria: list[str],
        failure_criteria: list[str],
        required_receipt_types: list[str],
        thresholds: dict[str, float] | None = None,
        forbidden_skips: list[str] | None = None,
        required_evidence_refs: list[str] | None = None,
    ) -> ValidationContract:
        self._require_plan(stage_execution_plan_id)
        contract = new_validation_contract(
            stage_execution_plan_id=stage_execution_plan_id,
            success_criteria=success_criteria,
            failure_criteria=failure_criteria,
            thresholds=thresholds,
            forbidden_skips=forbidden_skips,
            required_evidence_refs=required_evidence_refs,
            required_receipt_types=required_receipt_types,
        )
        return self.repository.save_validation_contract(contract)

    def create_agent_handoff_packet(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        recipient_type: str,
        recipient_name: str,
        source_evidence_refs: list[str],
        upstream_receipt_ids: list[UUID],
        allowed_actions: list[str] | None = None,
    ) -> AgentHandoffPacket:
        run = self._require_run(orchestration_run_id)
        plan = self._require_plan(stage_execution_plan_id)
        if plan.orchestration_run_id != run.orchestration_run_id:
            raise OrchestrationValidationError(
                "RUN_PLAN_MISMATCH",
                "StageExecutionPlan does not belong to OrchestrationRun.",
            )
        contract = self._require_validation_contract(stage_execution_plan_id)
        requested_actions = allowed_actions or plan.allowed_actions
        for action in requested_actions:
            self.guard_action(plan, action, recipient_name)

        packet = new_agent_handoff_packet(
            orchestration_run_id=run.orchestration_run_id,
            stage_execution_plan_id=plan.stage_execution_plan_id,
            recipient_type=recipient_type,
            recipient_name=recipient_name,
            active_object=run.active_object,
            source_evidence_refs=source_evidence_refs,
            upstream_receipt_ids=upstream_receipt_ids,
            allowed_actions=requested_actions,
            blocked_actions=plan.blocked_actions,
            required_downstream_receipt=contract.required_receipt_types[0],
        )
        run.status = StageRunStatus.executing
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_handoff_packet(packet)

    def record_skill_invocation(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        skill_key: str,
        registry_snapshot_id: UUID,
        compiler_fingerprint: str,
        source_context_refs: list[str],
        contrastive_prompt_layer_refs: list[str],
        critic_result_ref: str,
        synthesis_result_ref: str,
        eval_state: str,
    ) -> SkillInvocationRecord:
        self._require_run(orchestration_run_id)
        self._require_plan(stage_execution_plan_id)
        self._require_validation_contract(stage_execution_plan_id)
        record = new_skill_invocation_record(
            orchestration_run_id=orchestration_run_id,
            stage_execution_plan_id=stage_execution_plan_id,
            skill_key=skill_key,
            registry_snapshot_id=registry_snapshot_id,
            compiler_fingerprint=compiler_fingerprint,
            source_context_refs=source_context_refs,
            contrastive_prompt_layer_refs=contrastive_prompt_layer_refs,
            critic_result_ref=critic_result_ref,
            synthesis_result_ref=synthesis_result_ref,
            eval_state=eval_state,
        )
        return self.repository.save_skill_invocation(record)

    def close_stage_execution(self, receipt: StageExecutionReceipt) -> StageExecutionReceipt:
        run = self._require_run(receipt.orchestration_run_id)
        plan = self._require_plan(receipt.stage_execution_plan_id)
        if plan.orchestration_run_id != run.orchestration_run_id:
            raise OrchestrationValidationError(
                "RUN_PLAN_MISMATCH",
                "StageExecutionReceipt does not match OrchestrationRun.",
            )
        contract = self._require_validation_contract(plan.stage_execution_plan_id)
        self._validate_receipt_against_contract(receipt, contract)

        run.status = receipt.status
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_stage_receipt(receipt)

    def submit_stage_command(
        self,
        *,
        command_bus: CommandBus,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        command_type: str,
        actor: ActorContext,
        payload: dict,
        idempotency_key: str | None = None,
    ) -> CommandResult:
        run = self._require_run(orchestration_run_id)
        plan = self._require_plan(stage_execution_plan_id)
        self._require_validation_contract(stage_execution_plan_id)
        payload_with_context = {
            **payload,
            "orchestration_run_id": str(run.orchestration_run_id),
            "stage_execution_plan_id": str(plan.stage_execution_plan_id),
            "pipeline_stage": plan.pipeline_stage,
        }
        envelope = new_command_envelope(
            command_type=command_type,
            organization_id=run.organization_id,
            brand_id=run.brand_id,
            actor=actor,
            payload=payload_with_context,
            source_surface="orchestration",
            idempotency_key=idempotency_key,
        )
        return command_bus.submit(envelope)

    def record_failure_receipt(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        failed_gate: str,
        root_cause: str,
        retry_policy: str,
        next_action: str,
        evidence_refs: list[str] | None = None,
        quarantine_status: str = "not_quarantined",
    ) -> FailureReceipt:
        run = self._require_run(orchestration_run_id)
        self._require_plan(stage_execution_plan_id)
        receipt = FailureReceipt(
            schema_version="cmf.failure_receipt.v1",
            receipt_id=uuid4(),
            orchestration_run_id=orchestration_run_id,
            stage_execution_plan_id=stage_execution_plan_id,
            failed_gate=failed_gate,
            root_cause=root_cause,
            retry_policy=retry_policy,
            quarantine_status=quarantine_status,
            next_action=next_action,
            evidence_refs=evidence_refs or [],
            created_at=utc_now(),
        )
        run.status = (
            StageRunStatus.quarantined
            if quarantine_status == "quarantined"
            else StageRunStatus.failed
        )
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_failure_receipt(receipt)

    def record_friction_receipt(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        friction_type: str,
        description: str,
        severity: str = "medium",
        evidence_refs: list[str] | None = None,
    ) -> FrictionReceipt:
        self._require_run(orchestration_run_id)
        self._require_plan(stage_execution_plan_id)
        receipt = FrictionReceipt(
            schema_version="cmf.friction_receipt.v1",
            receipt_id=uuid4(),
            orchestration_run_id=orchestration_run_id,
            stage_execution_plan_id=stage_execution_plan_id,
            friction_type=friction_type,
            description=description,
            severity=severity,
            evidence_refs=evidence_refs or [],
            created_at=utc_now(),
        )
        return self.repository.save_friction_receipt(receipt)

    def request_human_handoff(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        reason: str,
        required_decision: str,
        allowed_responses: list[str],
        evidence_refs: list[str] | None = None,
    ) -> HumanHandoffRequest:
        run = self._require_run(orchestration_run_id)
        self._require_plan(stage_execution_plan_id)
        request = HumanHandoffRequest(
            schema_version="cmf.human_handoff_request.v1",
            handoff_request_id=uuid4(),
            orchestration_run_id=orchestration_run_id,
            stage_execution_plan_id=stage_execution_plan_id,
            reason=reason,
            required_decision=required_decision,
            allowed_responses=allowed_responses,
            evidence_refs=evidence_refs or [],
            requested_at=utc_now(),
        )
        run.status = StageRunStatus.waiting_for_human
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_human_handoff(request)

    def record_quarantine_receipt(
        self,
        *,
        orchestration_run_id: UUID,
        stage_execution_plan_id: UUID,
        quarantine_reason: str,
        recovery_action: str,
        blocked_output_refs: list[str] | None = None,
    ) -> QuarantineReceipt:
        run = self._require_run(orchestration_run_id)
        self._require_plan(stage_execution_plan_id)
        receipt = QuarantineReceipt(
            schema_version="cmf.quarantine_receipt.v1",
            receipt_id=uuid4(),
            orchestration_run_id=orchestration_run_id,
            stage_execution_plan_id=stage_execution_plan_id,
            quarantine_reason=quarantine_reason,
            blocked_output_refs=blocked_output_refs or [],
            recovery_action=recovery_action,
            created_at=utc_now(),
        )
        run.status = StageRunStatus.quarantined
        run.updated_at = utc_now()
        self.repository.save_run(run)
        return self.repository.save_quarantine_receipt(receipt)

    def guard_action(
        self,
        plan: StageExecutionPlan,
        requested_action: str,
        actor_or_service: str,
    ) -> None:
        if requested_action in plan.blocked_actions:
            raise OrchestrationValidationError(
                FORBIDDEN_ACTION_CODES.get(requested_action, "BLOCKED_ACTION_FOR_STAGE"),
                f"{requested_action} is blocked for {plan.pipeline_stage}.",
            )
        if requested_action not in plan.allowed_actions:
            raise OrchestrationValidationError(
                "ACTION_NOT_ALLOWED",
                f"{requested_action} is not listed in StageExecutionPlan.allowed_actions.",
            )
        if (
            actor_or_service.lower() in {"pi", "pi orchestrator", "orchestrator"}
            and requested_action in {"approve", "self_approve", "approve_own_output"}
        ):
            raise OrchestrationValidationError(
                "SELF_APPROVAL_FORBIDDEN",
                "Pi may orchestrate review but cannot approve its own output.",
            )

    def _validate_receipt_against_contract(
        self,
        receipt: StageExecutionReceipt,
        contract: ValidationContract,
    ) -> None:
        if receipt.receipt_type not in contract.required_receipt_types:
            raise OrchestrationValidationError(
                "REQUIRED_RECEIPT_MISSING",
                f"{receipt.receipt_type} does not satisfy required receipt types.",
            )
        missing_refs = sorted(set(contract.required_evidence_refs) - set(receipt.evidence_refs))
        if missing_refs:
            raise OrchestrationValidationError(
                "REQUIRED_EVIDENCE_MISSING",
                f"Stage receipt is missing evidence refs: {', '.join(missing_refs)}.",
            )

    def _require_run(self, orchestration_run_id: UUID) -> OrchestrationRun:
        run = self.repository.get_run(orchestration_run_id)
        if run is None:
            raise OrchestrationValidationError("ORCHESTRATION_RUN_NOT_FOUND", "Run not found.")
        return run

    def _require_plan(self, stage_execution_plan_id: UUID) -> StageExecutionPlan:
        plan = self.repository.get_plan(stage_execution_plan_id)
        if plan is None:
            raise OrchestrationValidationError("STAGE_EXECUTION_PLAN_NOT_FOUND", "Plan not found.")
        return plan

    def _require_validation_contract(self, stage_execution_plan_id: UUID) -> ValidationContract:
        contract = self.repository.get_validation_for_plan(stage_execution_plan_id)
        if contract is None:
            raise OrchestrationValidationError(
                "VALIDATION_CONTRACT_REQUIRED",
                "ValidationContract must exist before execution.",
            )
        return contract
