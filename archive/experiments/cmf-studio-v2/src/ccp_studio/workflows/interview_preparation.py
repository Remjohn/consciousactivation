"""Interview preparation workflow adapters for TS-CMF-023 through TS-CMF-028."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ccp_studio.contracts.context import ContextCompilationReceipt
from ccp_studio.contracts.induction import InductionRationaleReceipt
from ccp_studio.contracts.interview_contracts import InterviewDeck
from ccp_studio.contracts.matrix import MatrixOfEdgingBrief
from ccp_studio.contracts.pre_induction import PreInductionPlan
from ccp_studio.contracts.research import ResearchSnapshot
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.induction_rationale_service import InductionRationaleService
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService
from ccp_studio.services.research_service import ResearchService


@dataclass
class InterviewPreparationWorkflow:
    research_service: ResearchService
    context_service: ContextCompilationService | None = None
    matrix_service: MatrixService | None = None
    pre_induction_service: PreInductionService | None = None
    interview_contract_service: InterviewContractService | None = None
    induction_rationale_service: InductionRationaleService | None = None

    def __post_init__(self) -> None:
        if self.context_service is None:
            self.context_service = ContextCompilationService(research_service=self.research_service)
        if self.matrix_service is None:
            self.matrix_service = MatrixService(context_service=self.context_service)
        if self.pre_induction_service is None:
            self.pre_induction_service = PreInductionService(
                context_service=self.context_service,
                matrix_service=self.matrix_service,
            )
        if self.interview_contract_service is None:
            self.interview_contract_service = InterviewContractService(
                pre_induction_service=self.pre_induction_service,
                matrix_service=self.matrix_service,
            )
        if self.induction_rationale_service is None:
            self.induction_rationale_service = InductionRationaleService(
                context_service=self.context_service,
                matrix_service=self.matrix_service,
                pre_induction_service=self.pre_induction_service,
                interview_contract_service=self.interview_contract_service,
            )

    def stage3_collect_research_evidence(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence_ids: list[UUID],
        actor_id: UUID,
    ) -> ResearchSnapshot:
        return self.research_service.freeze_research_snapshot(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            evidence_ids=evidence_ids,
            frozen_by_actor_id=actor_id,
        )

    def stage3_compile_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence_ids: list[UUID],
        operator_id: UUID,
        audience_scope: str,
        actor_id: UUID,
        guest_id: UUID | None = None,
        operator_notes: list[str] | None = None,
    ) -> ContextCompilationReceipt:
        assert self.context_service is not None
        return self.context_service.compile_context_artifacts(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            evidence_ids=evidence_ids,
            operator_id=operator_id,
            audience_scope=audience_scope,
            compiler_actor_id=actor_id,
            guest_id=guest_id,
            operator_notes=operator_notes or [],
        )

    def stage3_4_compile_matrix(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_dossier_id: UUID,
        audience_reality_brief_id: UUID,
        context_premise_id: UUID,
        actor_id: UUID,
        trigger_map_id: UUID | None = None,
    ) -> MatrixOfEdgingBrief:
        assert self.matrix_service is not None
        return self.matrix_service.compile_matrix_brief(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_dossier_id=guest_dossier_id,
            audience_reality_brief_id=audience_reality_brief_id,
            context_premise_id=context_premise_id,
            trigger_map_id=trigger_map_id,
            compiled_by_actor_id=actor_id,
        )

    def stage4_pre_induction(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_id: UUID | None,
        operator_id: UUID,
        context_premise_id: UUID,
        matrix_brief_id: UUID,
        resonance_context_id: UUID | None,
        actor_id: UUID,
    ) -> PreInductionPlan:
        assert self.pre_induction_service is not None
        return self.pre_induction_service.compile_pre_induction_plan(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            operator_id=operator_id,
            context_premise_id=context_premise_id,
            matrix_brief_id=matrix_brief_id,
            resonance_context_id=resonance_context_id,
            compiled_by_actor_id=actor_id,
        )

    def stage4_compile_asset_contracts(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        matrix_brief_id: UUID,
        actor_id: UUID,
    ) -> InterviewDeck:
        assert self.interview_contract_service is not None
        return self.interview_contract_service.compile_interview_deck(
            organization_id=organization_id,
            brand_id=brand_id,
            pre_induction_plan_id=pre_induction_plan_id,
            matrix_brief_id=matrix_brief_id,
            compiled_by_actor_id=actor_id,
        )

    def stage3_4_compile_induction_rationale(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        pre_induction_plan_id: UUID,
        matrix_brief_id: UUID,
        actor_id: UUID,
        interview_deck_id: UUID | None = None,
        include_emotional_dna: bool = True,
        include_voice_dna: bool = True,
    ) -> InductionRationaleReceipt:
        assert self.induction_rationale_service is not None
        return self.induction_rationale_service.compile_induction_rationales(
            organization_id=organization_id,
            brand_id=brand_id,
            pre_induction_plan_id=pre_induction_plan_id,
            matrix_brief_id=matrix_brief_id,
            interview_deck_id=interview_deck_id,
            include_emotional_dna=include_emotional_dna,
            include_voice_dna=include_voice_dna,
            actor_id=actor_id,
        )
