"""Matrix of Edging service for TS-CMF-025."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.context import ContextArtifactKind
from ccp_studio.contracts.matrix import (
    MatrixBriefStatus,
    MatrixOfEdgingBrief,
    MatrixPass,
    MatrixReceipt,
    MatrixSaturationPacket,
    PrimitiveCandidateStatus,
    new_matrix_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.dspy_programs.matrix_compiler import MatrixOfEdgingCompiler, MatrixRSCSEvaluator
from ccp_studio.repositories.matrix import InMemoryMatrixRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.context_compilation_service import ContextCompilationService


class MatrixServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class MatrixService:
    context_service: ContextCompilationService
    repository: InMemoryMatrixRepository = field(default_factory=InMemoryMatrixRepository)
    compiler: MatrixOfEdgingCompiler = field(default_factory=MatrixOfEdgingCompiler)
    evaluator: MatrixRSCSEvaluator = field(default_factory=MatrixRSCSEvaluator)

    def compile_matrix_brief(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_dossier_id: UUID,
        audience_reality_brief_id: UUID,
        context_premise_id: UUID,
        compiled_by_actor_id: UUID,
        trigger_map_id: UUID | None = None,
        primitive_refs: list[str] | None = None,
        speculative_tension_statement: str | None = None,
        force_generic: bool = False,
    ) -> MatrixOfEdgingBrief:
        self.context_service.prepare_downstream_context_inputs(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_dossier_id=guest_dossier_id,
            audience_reality_brief_id=audience_reality_brief_id,
            context_premise_id=context_premise_id,
            trigger_map_id=trigger_map_id,
        )
        dossier = self.context_service.repository.guest_dossiers[guest_dossier_id]
        audience = self.context_service.repository.audience_reality_briefs[audience_reality_brief_id]
        premise = self.context_service.repository.context_premises[context_premise_id]
        brief = self.compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            guest_dossier=dossier,
            audience_reality_brief=audience,
            context_premise=premise,
            trigger_map_id=trigger_map_id,
            created_by_actor_id=compiled_by_actor_id,
            primitive_refs=primitive_refs,
            speculative_tension_statement=speculative_tension_statement,
            force_generic=force_generic,
        )
        self.repository.put_brief(brief)
        self.repository.put_receipt(
            new_matrix_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                matrix_brief_id=brief.matrix_brief_id,
                input_context_ids=self._input_context_ids(brief),
                pass_names=[item.pass_name for item in brief.pass_outputs],
                evaluator_scores=None,
                failure_points=[item.statement for item in brief.likely_failure_points],
                reviewer_state="pending_evaluation",
                decision_code="MATRIX_BRIEF_COMPILED",
                reviewer_actor_id=compiled_by_actor_id,
            )
        )
        return brief

    def evaluate_matrix_collision(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        matrix_brief_id: UUID,
        evaluator_actor_id: UUID,
    ) -> MatrixReceipt:
        brief = self._brief_for_brand(organization_id, brand_id, matrix_brief_id)
        scores, failures, passed = self.evaluator.evaluate(brief)
        status = MatrixBriefStatus.evaluated if passed else MatrixBriefStatus.evaluation_failed
        updated = brief.model_copy(update={"status": status, "updated_at": utc_now()})
        self.repository.put_brief(updated)
        receipt = new_matrix_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            matrix_brief_id=matrix_brief_id,
            input_context_ids=self._input_context_ids(updated),
            pass_names=[item.pass_name for item in updated.pass_outputs],
            evaluator_scores=scores,
            failure_points=failures or [item.statement for item in updated.likely_failure_points],
            reviewer_state="evaluated" if passed else "revision_required",
            decision_code="MATRIX_EVALUATION_PASSED" if passed else "MATRIX_EVALUATION_FAILED",
            reviewer_actor_id=evaluator_actor_id,
        )
        return self.repository.put_receipt(receipt)

    def approve_matrix_brief(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        matrix_brief_id: UUID,
        reviewer_actor_id: UUID,
    ) -> MatrixOfEdgingBrief:
        brief = self._brief_for_brand(organization_id, brand_id, matrix_brief_id)
        if brief.status == MatrixBriefStatus.approved:
            return brief
        if brief.status != MatrixBriefStatus.evaluated:
            raise MatrixServiceError("MATRIX_EVALUATION_REQUIRED", "Matrix brief must pass evaluation before approval.")
        blockers = self._approval_blockers(brief)
        if blockers:
            raise MatrixServiceError(blockers[0], "Matrix brief has approval blockers.")
        approved = brief.model_copy(
            update={
                "status": MatrixBriefStatus.approved,
                "approved_by_actor_id": reviewer_actor_id,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_brief(approved)
        self.repository.put_receipt(
            new_matrix_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                matrix_brief_id=matrix_brief_id,
                input_context_ids=self._input_context_ids(approved),
                pass_names=[item.pass_name for item in approved.pass_outputs],
                evaluator_scores=self._latest_scores(matrix_brief_id),
                failure_points=[item.statement for item in approved.likely_failure_points],
                reviewer_state="approved",
                decision_code="MATRIX_BRIEF_APPROVED",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return approved

    def reject_generic_matrix_brief(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        matrix_brief_id: UUID,
        reviewer_actor_id: UUID,
        reason: str,
    ) -> MatrixOfEdgingBrief:
        brief = self._brief_for_brand(organization_id, brand_id, matrix_brief_id)
        rejected = brief.model_copy(update={"status": MatrixBriefStatus.rejected, "updated_at": utc_now()})
        self.repository.put_brief(rejected)
        self.repository.put_receipt(
            new_matrix_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                matrix_brief_id=matrix_brief_id,
                input_context_ids=self._input_context_ids(rejected),
                pass_names=[item.pass_name for item in rejected.pass_outputs],
                evaluator_scores=self._latest_scores(matrix_brief_id),
                failure_points=[reason],
                reviewer_state="rejected",
                decision_code="MATRIX_BRIEF_REJECTED",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return rejected

    def record_matrix_benchmark(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        matrix_brief_id: UUID,
        actor_id: UUID,
        benchmark_note: str,
    ) -> MatrixReceipt:
        brief = self._brief_for_brand(organization_id, brand_id, matrix_brief_id)
        return self.repository.put_receipt(
            new_matrix_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                matrix_brief_id=matrix_brief_id,
                input_context_ids=self._input_context_ids(brief),
                pass_names=[item.pass_name for item in brief.pass_outputs],
                evaluator_scores=self._latest_scores(matrix_brief_id),
                failure_points=[benchmark_note],
                reviewer_state="benchmark_recorded",
                decision_code="MATRIX_BENCHMARK_RECORDED",
                reviewer_actor_id=actor_id,
            )
        )

    def prepare_downstream_matrix_inputs(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        matrix_brief_id: UUID,
    ) -> MatrixSaturationPacket:
        brief = self._brief_for_brand(organization_id, brand_id, matrix_brief_id)
        if brief.status != MatrixBriefStatus.approved:
            raise MatrixServiceError("MATRIX_BRIEF_NOT_APPROVED", "Only approved Matrix briefs can feed asset contracts.")
        return MatrixSaturationPacket(
            schema_version="cmf.matrix_saturation_packet.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            matrix_brief_id=matrix_brief_id,
            primitive_candidate_ids=[item.primitive_candidate_id for item in brief.primitive_candidates],
            coalition_signature_ids=[item.coalition_signature_id for item in brief.coalition_signatures],
            edge_product_ids=[item.edge_product_id for item in brief.edge_products],
            route_implications=brief.route_implications,
        )

    def _brief_for_brand(self, organization_id: UUID, brand_id: UUID, matrix_brief_id: UUID) -> MatrixOfEdgingBrief:
        brief = self.repository.briefs.get(matrix_brief_id)
        if brief is None:
            raise MatrixServiceError("MATRIX_BRIEF_REQUIRED", "Matrix brief is required.")
        if brief.organization_id != organization_id or brief.brand_id != brand_id:
            raise MatrixServiceError("BRAND_SCOPE_VIOLATION", "Matrix brief is outside active brand scope.")
        return brief

    @staticmethod
    def _input_context_ids(brief: MatrixOfEdgingBrief) -> dict[str, UUID]:
        values = {
            "guest_dossier_id": brief.guest_dossier_id,
            "audience_reality_brief_id": brief.audience_reality_brief_id,
            "context_premise_id": brief.context_premise_id,
        }
        if brief.trigger_map_id is not None:
            values["trigger_map_id"] = brief.trigger_map_id
        return values

    def _latest_scores(self, matrix_brief_id: UUID):
        for receipt in reversed(self.repository.receipts_for_brief(matrix_brief_id)):
            if receipt.evaluator_scores is not None:
                return receipt.evaluator_scores
        return None

    @staticmethod
    def _approval_blockers(brief: MatrixOfEdgingBrief) -> list[str]:
        blockers: list[str] = []
        if any(site.speculative and site.can_anchor_question for site in brief.tension_sites):
            blockers.append("SPECULATIVE_TENSION_CANNOT_ANCHOR")
        if any(
            candidate.status in {PrimitiveCandidateStatus.unsupported, PrimitiveCandidateStatus.unresolved_registry_ref}
            for candidate in brief.primitive_candidates
        ):
            blockers.append("PRIMITIVE_REGISTRY_VALIDATION_REQUIRED")
        return blockers


@dataclass
class MatrixCommandHandler:
    command_type: str
    service: MatrixService
    aggregate_type: str = "matrix"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompileMatrixOfEdgingBriefCommand":
            brief = self.service.compile_matrix_brief(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_dossier_id=UUID(payload["guest_dossier_id"]),
                audience_reality_brief_id=UUID(payload["audience_reality_brief_id"]),
                context_premise_id=UUID(payload["context_premise_id"]),
                trigger_map_id=UUID(payload["trigger_map_id"]) if payload.get("trigger_map_id") else None,
                primitive_refs=payload.get("primitive_refs"),
                speculative_tension_statement=payload.get("speculative_tension_statement"),
                force_generic=payload.get("force_generic", False),
                compiled_by_actor_id=envelope.actor.actor_id,
            )
            return brief.model_dump(mode="json")
        if self.command_type == "EvaluateMatrixCollisionCommand":
            return self.service.evaluate_matrix_collision(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                evaluator_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ApproveMatrixBriefCommand":
            return self.service.approve_matrix_brief(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "RejectGenericMatrixBriefCommand":
            return self.service.reject_generic_matrix_brief(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
            ).model_dump(mode="json")
        if self.command_type == "RecordMatrixBenchmarkCommand":
            return self.service.record_matrix_benchmark(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                actor_id=envelope.actor.actor_id,
                benchmark_note=payload["benchmark_note"],
            ).model_dump(mode="json")
        raise MatrixServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("matrix_brief_id") or payload.get("context_premise_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_matrix_command_handlers(bus: CommandBus, service: MatrixService) -> None:
    for command_type in [
        "CompileMatrixOfEdgingBriefCommand",
        "EvaluateMatrixCollisionCommand",
        "RejectGenericMatrixBriefCommand",
        "ApproveMatrixBriefCommand",
        "RecordMatrixBenchmarkCommand",
    ]:
        bus.register_handler(MatrixCommandHandler(command_type=command_type, service=service))
