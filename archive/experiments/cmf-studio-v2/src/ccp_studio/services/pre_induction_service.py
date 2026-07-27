"""Interviewer pre-induction service for TS-CMF-026."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.context import ContextArtifactKind, ContextOutputStatus
from ccp_studio.contracts.matrix import MatrixBriefStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import (
    InductionRiskLevel,
    LiveInterviewModeBinding,
    OperatorEdit,
    PreInductionPlan,
    PreInductionPlanStatus,
    PreInductionReceipt,
    new_pre_induction_receipt,
)
from ccp_studio.dspy_programs.pre_induction_compiler import PreInductionEvaluator, PreInductionPlanCompiler
from ccp_studio.repositories.pre_induction import InMemoryPreInductionRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.matrix_service import MatrixService


class PreInductionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class PreInductionService:
    context_service: ContextCompilationService
    matrix_service: MatrixService
    repository: InMemoryPreInductionRepository = field(default_factory=InMemoryPreInductionRepository)
    compiler: PreInductionPlanCompiler = field(default_factory=PreInductionPlanCompiler)
    evaluator: PreInductionEvaluator = field(default_factory=PreInductionEvaluator)

    def compile_pre_induction_plan(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_id: UUID | None,
        operator_id: UUID,
        context_premise_id: UUID,
        matrix_brief_id: UUID,
        resonance_context_id: UUID | None,
        compiled_by_actor_id: UUID,
    ) -> PreInductionPlan:
        premise = self.context_service.repository.context_premises.get(context_premise_id)
        if premise is None:
            raise PreInductionServiceError("CONTEXT_PREMISE_REQUIRED", "Context Premise is required.")
        if premise.organization_id != organization_id or premise.brand_id != brand_id:
            raise PreInductionServiceError("BRAND_SCOPE_VIOLATION", "Context Premise is outside active brand scope.")
        if premise.status != ContextOutputStatus.approved:
            raise PreInductionServiceError("CONTEXT_PREMISE_APPROVAL_REQUIRED", "Context Premise must be approved.")
        matrix = self.matrix_service.repository.briefs.get(matrix_brief_id)
        if matrix is None:
            raise PreInductionServiceError("MATRIX_BRIEF_REQUIRED", "Matrix brief is required.")
        if matrix.organization_id != organization_id or matrix.brand_id != brand_id:
            raise PreInductionServiceError("BRAND_SCOPE_VIOLATION", "Matrix brief is outside active brand scope.")
        if matrix.status != MatrixBriefStatus.approved:
            raise PreInductionServiceError("MATRIX_BRIEF_APPROVAL_REQUIRED", "Matrix brief must be approved.")
        resonance = None
        if resonance_context_id is not None:
            resonance = self.context_service.repository.resonance_contexts.get(resonance_context_id)
            if resonance is None:
                raise PreInductionServiceError("RESONANCE_CONTEXT_REQUIRED", "Interviewer Resonance Context is required.")
            if resonance.organization_id != organization_id or resonance.brand_id != brand_id:
                raise PreInductionServiceError("BRAND_SCOPE_VIOLATION", "Resonance context is outside active brand scope.")
        plan = self.compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            operator_id=operator_id,
            context_premise=premise,
            resonance_context=resonance,
            matrix_brief=matrix,
        )
        self.repository.put_plan(plan)
        self._write_receipt(plan, "PRE_INDUCTION_PLAN_COMPILED", compiled_by_actor_id)
        return plan

    def evaluate_pre_induction_plan(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        evaluator_actor_id: UUID,
    ) -> PreInductionReceipt:
        plan = self._plan_for_brand(organization_id, brand_id, pre_induction_plan_id)
        updated_questions = []
        for question in plan.planned_questions:
            centroid, manipulation = self.evaluator.evaluate_question(question)
            updated_questions.append(
                question.model_copy(update={"centroid_risk": centroid, "manipulation_risk": manipulation})
            )
        has_block = any(item.manipulation_risk == InductionRiskLevel.blocked for item in updated_questions)
        status = PreInductionPlanStatus.blocked if has_block else PreInductionPlanStatus.evaluated
        updated = plan.model_copy(
            update={
                "planned_questions": updated_questions,
                "status": status,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_plan(updated)
        return self._write_receipt(
            updated,
            "PRE_INDUCTION_PLAN_BLOCKED" if has_block else "PRE_INDUCTION_PLAN_EVALUATED",
            evaluator_actor_id,
        )

    def edit_pre_induction_question(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        question_id: UUID,
        revised_question: str,
        evidence_ids: list[UUID],
        rationale: str,
        edited_by_actor_id: UUID,
    ) -> OperatorEdit:
        plan = self._plan_for_brand(organization_id, brand_id, pre_induction_plan_id)
        if plan.status == PreInductionPlanStatus.approved:
            raise PreInductionServiceError("PRE_INDUCTION_PLAN_IMMUTABLE", "Approved pre-induction plans are read-only.")
        if not evidence_ids:
            raise PreInductionServiceError("INDUCTION_EDIT_EVIDENCE_REQUIRED", "Operator edits must preserve evidence links.")
        questions = list(plan.planned_questions)
        for index, question in enumerate(questions):
            if question.question_id == question_id:
                edit = OperatorEdit(
                    schema_version="cmf.operator_edit.v1",
                    operator_edit_id=uuid4(),
                    pre_induction_plan_id=pre_induction_plan_id,
                    question_id=question_id,
                    previous_question=question.natural_question,
                    revised_question=revised_question,
                    evidence_ids=evidence_ids,
                    rationale=rationale,
                    edited_by_actor_id=edited_by_actor_id,
                    edited_at=utc_now(),
                )
                centroid, manipulation = self.evaluator.evaluate_question(
                    question.model_copy(update={"natural_question": revised_question, "evidence_ids": evidence_ids})
                )
                questions[index] = question.model_copy(
                    update={
                        "natural_question": revised_question,
                        "evidence_ids": evidence_ids,
                        "centroid_risk": centroid,
                        "manipulation_risk": manipulation,
                    }
                )
                self.repository.put_edit(edit)
                updated = plan.model_copy(
                    update={
                        "planned_questions": questions,
                        "operator_edit_ids": [*plan.operator_edit_ids, edit.operator_edit_id],
                        "status": PreInductionPlanStatus.draft,
                        "updated_at": utc_now(),
                    }
                )
                self.repository.put_plan(updated)
                self._write_receipt(updated, "PRE_INDUCTION_QUESTION_EDITED", edited_by_actor_id)
                return edit
        raise PreInductionServiceError("PRE_INDUCTION_QUESTION_REQUIRED", "Question is required.")

    def block_manipulative_prompt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        question_id: UUID,
        reviewer_actor_id: UUID,
        reason: str,
    ) -> PreInductionPlan:
        plan = self._plan_for_brand(organization_id, brand_id, pre_induction_plan_id)
        questions = [
            question.model_copy(update={"manipulation_risk": InductionRiskLevel.blocked})
            if question.question_id == question_id
            else question
            for question in plan.planned_questions
        ]
        blocked = plan.model_copy(
            update={"planned_questions": questions, "status": PreInductionPlanStatus.blocked, "updated_at": utc_now()}
        )
        self.repository.put_plan(blocked)
        self._write_receipt(blocked, f"MANIPULATIVE_PROMPT_BLOCKED:{reason}", reviewer_actor_id)
        return blocked

    def approve_pre_induction_plan(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        reviewer_actor_id: UUID,
    ) -> PreInductionPlan:
        plan = self._plan_for_brand(organization_id, brand_id, pre_induction_plan_id)
        if plan.status != PreInductionPlanStatus.evaluated:
            raise PreInductionServiceError("PRE_INDUCTION_EVALUATION_REQUIRED", "Plan must be evaluated before approval.")
        if any(question.manipulation_risk == InductionRiskLevel.blocked for question in plan.planned_questions):
            raise PreInductionServiceError("MANIPULATION_GATE_BLOCKED", "Manipulative prompt must be rewritten before approval.")
        binding = LiveInterviewModeBinding(
            schema_version="cmf.live_interview_mode_binding.v1",
            live_interview_mode_binding_id=uuid4(),
            pre_induction_plan_id=pre_induction_plan_id,
            organization_id=organization_id,
            brand_id=brand_id,
            read_only=True,
            operator_judgment_required=True,
            bound_at=utc_now(),
        )
        self.repository.put_binding(binding)
        approved = plan.model_copy(
            update={
                "status": PreInductionPlanStatus.approved,
                "approved_at": utc_now(),
                "live_interview_mode_binding_id": binding.live_interview_mode_binding_id,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_plan(approved)
        self._write_receipt(approved, "PRE_INDUCTION_PLAN_APPROVED", reviewer_actor_id)
        return approved

    def get_live_interview_mode_binding(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
    ) -> LiveInterviewModeBinding:
        plan = self._plan_for_brand(organization_id, brand_id, pre_induction_plan_id)
        if plan.status != PreInductionPlanStatus.approved or plan.live_interview_mode_binding_id is None:
            raise PreInductionServiceError("PRE_INDUCTION_PLAN_NOT_APPROVED", "Approved plan is required for live mode.")
        return self.repository.bindings[plan.live_interview_mode_binding_id]

    def _plan_for_brand(self, organization_id: UUID, brand_id: UUID, pre_induction_plan_id: UUID) -> PreInductionPlan:
        plan = self.repository.plans.get(pre_induction_plan_id)
        if plan is None:
            raise PreInductionServiceError("PRE_INDUCTION_PLAN_REQUIRED", "Pre-induction plan is required.")
        if plan.organization_id != organization_id or plan.brand_id != brand_id:
            raise PreInductionServiceError("BRAND_SCOPE_VIOLATION", "Pre-induction plan is outside active brand scope.")
        return plan

    def _write_receipt(self, plan: PreInductionPlan, decision_code: str, actor_id: UUID) -> PreInductionReceipt:
        receipt = new_pre_induction_receipt(
            organization_id=plan.organization_id,
            brand_id=plan.brand_id,
            pre_induction_plan_id=plan.pre_induction_plan_id,
            context_premise_id=plan.context_premise_id,
            matrix_brief_id=plan.matrix_brief_id,
            risk_scores=self.evaluator.risk_scores(plan),
            edit_trail_ids=plan.operator_edit_ids,
            approval_state=plan.status.value,
            live_interview_mode_binding_id=plan.live_interview_mode_binding_id,
            decision_code=decision_code,
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)


@dataclass
class PreInductionCommandHandler:
    command_type: str
    service: PreInductionService
    aggregate_type: str = "pre_induction"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompilePreInductionPlanCommand":
            return self.service.compile_pre_induction_plan(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_id=UUID(payload["guest_id"]) if payload.get("guest_id") else None,
                operator_id=UUID(payload["operator_id"]),
                context_premise_id=UUID(payload["context_premise_id"]),
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                resonance_context_id=UUID(payload["resonance_context_id"]) if payload.get("resonance_context_id") else None,
                compiled_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "EvaluatePreInductionPlanCommand":
            return self.service.evaluate_pre_induction_plan(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                evaluator_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "EditPreInductionQuestionCommand":
            return self.service.edit_pre_induction_question(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                question_id=UUID(payload["question_id"]),
                revised_question=payload["revised_question"],
                evidence_ids=[UUID(item) for item in payload["evidence_ids"]],
                rationale=payload["rationale"],
                edited_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockManipulativePromptCommand":
            return self.service.block_manipulative_prompt(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                question_id=UUID(payload["question_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
            ).model_dump(mode="json")
        if self.command_type == "ApprovePreInductionPlanCommand":
            return self.service.approve_pre_induction_plan(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise PreInductionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("pre_induction_plan_id") or payload.get("matrix_brief_id") or payload.get("context_premise_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_pre_induction_command_handlers(bus: CommandBus, service: PreInductionService) -> None:
    for command_type in [
        "CompilePreInductionPlanCommand",
        "EvaluatePreInductionPlanCommand",
        "EditPreInductionQuestionCommand",
        "BlockManipulativePromptCommand",
        "ApprovePreInductionPlanCommand",
    ]:
        bus.register_handler(PreInductionCommandHandler(command_type=command_type, service=service))
