"""Interview Asset Contract service for TS-CMF-027."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.interview_contracts import (
    ContractCompilationReceipt,
    ContractInductionContext,
    DeckSessionBinding,
    InterviewContractStatus,
    InterviewDeck,
    new_contract_compilation_receipt,
)
from ccp_studio.contracts.matrix import MatrixBriefStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import PreInductionPlanStatus
from ccp_studio.dspy_programs.interview_contract_compiler import (
    InterviewAssetContractCompiler,
    InterviewPlanQualityGate,
)
from ccp_studio.repositories.interview_contracts import InMemoryInterviewContractRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService


class InterviewContractServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class InterviewContractService:
    pre_induction_service: PreInductionService
    matrix_service: MatrixService
    repository: InMemoryInterviewContractRepository = field(default_factory=InMemoryInterviewContractRepository)
    compiler: InterviewAssetContractCompiler = field(default_factory=InterviewAssetContractCompiler)
    quality_gate: InterviewPlanQualityGate = field(default_factory=InterviewPlanQualityGate)

    def compile_interview_deck(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        matrix_brief_id: UUID,
        compiled_by_actor_id: UUID,
        force_confusion: bool = False,
        force_generic: bool = False,
    ) -> InterviewDeck:
        plan = self.pre_induction_service.repository.plans.get(pre_induction_plan_id)
        if plan is None:
            raise InterviewContractServiceError("PRE_INDUCTION_PLAN_REQUIRED", "Approved pre-induction plan is required.")
        if plan.organization_id != organization_id or plan.brand_id != brand_id:
            raise InterviewContractServiceError("BRAND_SCOPE_VIOLATION", "Pre-induction plan is outside active brand scope.")
        if plan.status != PreInductionPlanStatus.approved:
            raise InterviewContractServiceError("PRE_INDUCTION_PLAN_APPROVAL_REQUIRED", "Pre-induction plan must be approved.")
        matrix = self.matrix_service.repository.briefs.get(matrix_brief_id)
        if matrix is None:
            raise InterviewContractServiceError("MATRIX_BRIEF_REQUIRED", "Approved Matrix brief is required.")
        if matrix.organization_id != organization_id or matrix.brand_id != brand_id:
            raise InterviewContractServiceError("BRAND_SCOPE_VIOLATION", "Matrix brief is outside active brand scope.")
        if matrix.status != MatrixBriefStatus.approved:
            raise InterviewContractServiceError("MATRIX_BRIEF_APPROVAL_REQUIRED", "Matrix brief must be approved.")
        contracts = self.compiler.compile_contracts(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=plan.guest_id,
            pre_induction_plan=plan,
            matrix_brief=matrix,
            force_confusion=force_confusion,
            force_generic=force_generic,
        )
        for contract in contracts:
            self.repository.put_contract(contract)
        deck = self.compiler.compile_deck(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=plan.guest_id,
            pre_induction_plan=plan,
            matrix_brief=matrix,
            contracts=contracts,
        )
        self.repository.put_deck(deck)
        self.repository.put_receipt(
            new_contract_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                interview_deck_id=deck.interview_deck_id,
                contract_ids=deck.contract_ids,
                input_artifact_ids={
                    "pre_induction_plan_id": pre_induction_plan_id,
                    "matrix_brief_id": matrix_brief_id,
                },
                registry_versions=self._registry_versions(),
                route_targets=[contract.route_target for contract in contracts],
                evaluation_scores=None,
                failure_reasons=[],
                approval_state=deck.status.value,
                decision_code="INTERVIEW_DECK_COMPILED",
                reviewer_actor_id=compiled_by_actor_id,
            )
        )
        return deck

    def evaluate_interview_plan(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        interview_deck_id: UUID,
        evaluator_actor_id: UUID,
    ) -> ContractCompilationReceipt:
        deck = self._deck_for_brand(organization_id, brand_id, interview_deck_id)
        contracts = [self.repository.contracts[contract_id] for contract_id in deck.contract_ids]
        scores, failures, passed = self.quality_gate.evaluate(contracts)
        status = InterviewContractStatus.evaluated if passed else InterviewContractStatus.rejected
        for contract in contracts:
            self.repository.put_contract(contract.model_copy(update={"status": status, "updated_at": utc_now()}))
        deck = deck.model_copy(update={"status": status, "updated_at": utc_now()})
        self.repository.put_deck(deck)
        receipt = new_contract_compilation_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            interview_deck_id=interview_deck_id,
            contract_ids=deck.contract_ids,
            input_artifact_ids={
                "pre_induction_plan_id": deck.pre_induction_plan_id,
                "matrix_brief_id": deck.matrix_brief_id,
            },
            registry_versions=self._registry_versions(),
            route_targets=[contract.route_target for contract in contracts],
            evaluation_scores=scores,
            failure_reasons=failures,
            approval_state=deck.status.value,
            decision_code="INTERVIEW_PLAN_EVALUATION_PASSED" if passed else "INTERVIEW_PLAN_EVALUATION_FAILED",
            reviewer_actor_id=evaluator_actor_id,
        )
        receipt = self.repository.put_receipt(receipt)
        self.repository.put_deck(deck.model_copy(update={"evaluation_receipt_id": receipt.contract_compilation_receipt_id}))
        return receipt

    def reject_expression_archetype_confusion(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        interview_deck_id: UUID,
        reviewer_actor_id: UUID,
        correction_note: str,
    ) -> InterviewDeck:
        deck = self._deck_for_brand(organization_id, brand_id, interview_deck_id)
        rejected = deck.model_copy(update={"status": InterviewContractStatus.rejected, "updated_at": utc_now()})
        self.repository.put_deck(rejected)
        self.repository.put_receipt(
            new_contract_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                interview_deck_id=interview_deck_id,
                contract_ids=deck.contract_ids,
                input_artifact_ids={"pre_induction_plan_id": deck.pre_induction_plan_id, "matrix_brief_id": deck.matrix_brief_id},
                registry_versions=self._registry_versions(),
                route_targets=[self.repository.contracts[item].route_target for item in deck.contract_ids],
                evaluation_scores=None,
                failure_reasons=["EXPRESSION_ARCHETYPE_CONFUSION", correction_note],
                approval_state="rejected",
                decision_code="EXPRESSION_ARCHETYPE_CONFUSION_REJECTED",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return rejected

    def approve_interview_deck(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        interview_deck_id: UUID,
        reviewer_actor_id: UUID,
    ) -> InterviewDeck:
        deck = self._deck_for_brand(organization_id, brand_id, interview_deck_id)
        if deck.status != InterviewContractStatus.evaluated:
            raise InterviewContractServiceError("INTERVIEW_PLAN_EVALUATION_REQUIRED", "Deck must pass evaluation before approval.")
        approved = deck.model_copy(update={"status": InterviewContractStatus.approved, "approved_for_session": True, "updated_at": utc_now()})
        self.repository.put_deck(approved)
        for contract_id in deck.contract_ids:
            contract = self.repository.contracts[contract_id]
            self.repository.put_contract(contract.model_copy(update={"status": InterviewContractStatus.approved, "updated_at": utc_now()}))
        self.repository.put_receipt(
            new_contract_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                interview_deck_id=interview_deck_id,
                contract_ids=deck.contract_ids,
                input_artifact_ids={"pre_induction_plan_id": deck.pre_induction_plan_id, "matrix_brief_id": deck.matrix_brief_id},
                registry_versions=self._registry_versions(),
                route_targets=[self.repository.contracts[item].route_target for item in deck.contract_ids],
                evaluation_scores=self._latest_scores(interview_deck_id),
                failure_reasons=[],
                approval_state="approved",
                decision_code="INTERVIEW_DECK_APPROVED",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return approved

    def bind_deck_to_expression_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        interview_deck_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
    ) -> DeckSessionBinding:
        deck = self._deck_for_brand(organization_id, brand_id, interview_deck_id)
        if deck.status != InterviewContractStatus.approved:
            raise InterviewContractServiceError("INTERVIEW_DECK_APPROVAL_REQUIRED", "Approved deck is required before session binding.")
        binding = DeckSessionBinding(
            schema_version="cmf.deck_session_binding.v1",
            deck_session_binding_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            interview_deck_id=interview_deck_id,
            expression_session_id=expression_session_id,
            contract_ids=deck.contract_ids,
            read_only_contracts=True,
            bound_at=utc_now(),
        )
        self.repository.put_binding(binding)
        bound = deck.model_copy(update={"status": InterviewContractStatus.bound_to_session, "updated_at": utc_now()})
        self.repository.put_deck(bound)
        for contract_id in deck.contract_ids:
            contract = self.repository.contracts[contract_id]
            self.repository.put_contract(contract.model_copy(update={"status": InterviewContractStatus.bound_to_session, "updated_at": utc_now()}))
        self.repository.put_receipt(
            new_contract_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                interview_deck_id=interview_deck_id,
                contract_ids=deck.contract_ids,
                input_artifact_ids={"expression_session_id": expression_session_id},
                registry_versions=self._registry_versions(),
                route_targets=[self.repository.contracts[item].route_target for item in deck.contract_ids],
                evaluation_scores=self._latest_scores(interview_deck_id),
                failure_reasons=[],
                approval_state="bound_to_session",
                decision_code="INTERVIEW_DECK_BOUND_TO_SESSION",
                reviewer_actor_id=actor_id,
            )
        )
        return binding

    def induction_context_for_extraction(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        contract_id: UUID,
    ) -> ContractInductionContext:
        contract = self.repository.contracts.get(contract_id)
        if contract is None:
            raise InterviewContractServiceError("INTERVIEW_CONTRACT_REQUIRED", "Interview Asset Contract is required.")
        if contract.organization_id != organization_id or contract.brand_id != brand_id:
            raise InterviewContractServiceError("BRAND_SCOPE_VIOLATION", "Contract is outside active brand scope.")
        return ContractInductionContext(
            schema_version="cmf.contract_induction_context.v1",
            contract_id=contract.contract_id,
            pre_induction_plan_id=contract.pre_induction_plan_id,
            matrix_brief_id=contract.matrix_brief_id,
            edge_product_id=contract.edge_product_id,
            target_expression_states=contract.target_expression_states,
            route_target=contract.route_target,
            evidence_ids=contract.evidence_ids,
            induction_rationale_ids=contract.induction_rationale_ids,
        )

    def _deck_for_brand(self, organization_id: UUID, brand_id: UUID, interview_deck_id: UUID) -> InterviewDeck:
        deck = self.repository.decks.get(interview_deck_id)
        if deck is None:
            raise InterviewContractServiceError("INTERVIEW_DECK_REQUIRED", "Interview deck is required.")
        if deck.organization_id != organization_id or deck.brand_id != brand_id:
            raise InterviewContractServiceError("BRAND_SCOPE_VIOLATION", "Interview deck is outside active brand scope.")
        return deck

    def _latest_scores(self, interview_deck_id: UUID):
        receipts = [receipt for receipt in self.repository.receipts.values() if receipt.interview_deck_id == interview_deck_id]
        for receipt in reversed(receipts):
            if receipt.evaluation_scores is not None:
                return receipt.evaluation_scores
        return None

    @staticmethod
    def _registry_versions() -> dict[str, str]:
        return {
            "core_archetype_registry": "migrated-v1",
            "asset_derivative_registry": "migrated-v1",
            "meme_mechanism_registry": "migrated-v1",
            "reaction_archetype_registry": "migrated-v1",
            "cmf_render_mode_registry": "migrated-v1",
        }


@dataclass
class InterviewContractCommandHandler:
    command_type: str
    service: InterviewContractService
    aggregate_type: str = "interview_contract"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {"CompileInterviewDeckCommand", "CompileInterviewAssetContractCommand"}:
            return self.service.compile_interview_deck(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                force_confusion=payload.get("force_confusion", False),
                force_generic=payload.get("force_generic", False),
                compiled_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "EvaluateInterviewPlanCommand":
            return self.service.evaluate_interview_plan(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                interview_deck_id=UUID(payload["interview_deck_id"]),
                evaluator_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RejectExpressionArchetypeConfusionCommand":
            return self.service.reject_expression_archetype_confusion(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                interview_deck_id=UUID(payload["interview_deck_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                correction_note=payload["correction_note"],
            ).model_dump(mode="json")
        if self.command_type == "ApproveInterviewDeckCommand":
            return self.service.approve_interview_deck(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                interview_deck_id=UUID(payload["interview_deck_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "BindDeckToExpressionSessionCommand":
            return self.service.bind_deck_to_expression_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                interview_deck_id=UUID(payload["interview_deck_id"]),
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise InterviewContractServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("interview_deck_id") or payload.get("pre_induction_plan_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_interview_contract_command_handlers(bus: CommandBus, service: InterviewContractService) -> None:
    for command_type in [
        "CompileInterviewAssetContractCommand",
        "CompileInterviewDeckCommand",
        "EvaluateInterviewPlanCommand",
        "RejectExpressionArchetypeConfusionCommand",
        "ApproveInterviewDeckCommand",
        "BindDeckToExpressionSessionCommand",
    ]:
        bus.register_handler(InterviewContractCommandHandler(command_type=command_type, service=service))
