"""CRAL, Context Premise, Emotional DNA, Voice DNA, and rationale service for TS-CMF-028."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.context import AudienceDeepTriggerMap, ContextOutputStatus
from ccp_studio.contracts.induction import (
    InductionArtifactStatus,
    InductionRationaleInspection,
    InductionRationaleReceipt,
    RationaleMode,
    SupportedPsychologyClaim,
    new_induction_rationale_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.pre_induction import PreInductionPlanStatus
from ccp_studio.contracts.research import ResearchEvidence
from ccp_studio.dspy_programs.induction_compilers import (
    CRALResearchCompiler,
    EmotionalDNAExtractor,
    InductionRationaleCompiler,
    UnsupportedPsychologyValidator,
    VoiceDNAProfileCompiler,
)
from ccp_studio.repositories.induction import InMemoryInductionRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService


class InductionRationaleServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class InductionRationaleService:
    context_service: ContextCompilationService
    matrix_service: MatrixService
    pre_induction_service: PreInductionService
    interview_contract_service: InterviewContractService | None = None
    repository: InMemoryInductionRepository = field(default_factory=InMemoryInductionRepository)
    cral_compiler: CRALResearchCompiler = field(default_factory=CRALResearchCompiler)
    emotional_dna_extractor: EmotionalDNAExtractor = field(default_factory=EmotionalDNAExtractor)
    voice_dna_compiler: VoiceDNAProfileCompiler = field(default_factory=VoiceDNAProfileCompiler)
    rationale_compiler: InductionRationaleCompiler = field(default_factory=InductionRationaleCompiler)
    psychology_validator: UnsupportedPsychologyValidator = field(default_factory=UnsupportedPsychologyValidator)

    def compile_cral_findings(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence_ids: list[UUID],
        actor_id: UUID,
    ) -> InductionRationaleReceipt:
        evidence = self._approved_evidence(organization_id, brand_id, evidence_ids)
        findings = self.cral_compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            evidence=evidence,
        )
        for finding in findings:
            self.repository.put_cral_finding(finding)
        receipt = new_induction_rationale_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            rationale_mode=RationaleMode.partial,
            cral_finding_ids=[finding.cral_finding_id for finding in findings],
            evidence_ids=evidence_ids,
            compiler_versions=self._compiler_versions(),
            decision_code="CRAL_FINDINGS_COMPILED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def compile_audience_deep_trigger_map(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        trigger_map_id: UUID,
        actor_id: UUID,
    ) -> AudienceDeepTriggerMap:
        trigger_map = self.context_service.repository.trigger_maps.get(trigger_map_id)
        if trigger_map is None:
            raise InductionRationaleServiceError("TRIGGER_MAP_REQUIRED", "Audience Deep Trigger Map is required.")
        if trigger_map.organization_id != organization_id or trigger_map.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Trigger map is outside active brand scope.")
        self.repository.put_receipt(
            new_induction_rationale_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                rationale_mode=RationaleMode.full_depth
                if trigger_map.depth_mode.value == "saturated"
                else RationaleMode.shallow_supported,
                evidence_ids=self._trigger_map_evidence_ids(trigger_map),
                compiler_versions=self._compiler_versions(),
                downstream_bindings={"trigger_map_ids": [trigger_map.trigger_map_id]},
                decision_code="AUDIENCE_DEEP_TRIGGER_MAP_READY",
                reviewer_actor_id=actor_id,
            )
        )
        return trigger_map

    def extract_emotional_dna(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        context_premise_id: UUID,
        trigger_map_id: UUID,
        actor_id: UUID,
        include_profile: bool = True,
    ) -> InductionRationaleReceipt:
        premise = self._context_premise(organization_id, brand_id, context_premise_id)
        trigger_map = self._trigger_map(organization_id, brand_id, trigger_map_id)
        dossier = self.context_service.repository.guest_dossiers[premise.guest_dossier_id]
        evidence = self._approved_evidence(organization_id, brand_id, premise.evidence_ids)
        profile = self.emotional_dna_extractor.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            guest_id=dossier.guest_id,
            dossier=dossier,
            trigger_map=trigger_map,
            premise=premise,
            evidence=evidence,
            include_profile=include_profile,
        )
        self.repository.put_emotional_dna_profile(profile)
        receipt = new_induction_rationale_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            rationale_mode=RationaleMode.full_depth if profile.status == InductionArtifactStatus.compiled else RationaleMode.partial,
            emotional_dna_profile_id=profile.emotional_dna_profile_id,
            evidence_ids=profile.evidence_ids,
            compiler_versions=self._compiler_versions(),
            blocked_claims=self.psychology_validator.evaluate_claims(self._profile_claims(profile)),
            decision_code="EMOTIONAL_DNA_EXTRACTED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def compile_voice_dna_profile(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        context_premise_id: UUID,
        emotional_dna_profile_id: UUID,
        actor_id: UUID,
        include_profile: bool = True,
    ) -> InductionRationaleReceipt:
        premise = self._context_premise(organization_id, brand_id, context_premise_id)
        dossier = self.context_service.repository.guest_dossiers[premise.guest_dossier_id]
        resonance = next(
            (
                item
                for item in self.context_service.repository.resonance_contexts.values()
                if item.research_field_id == premise.research_field_id
                and item.organization_id == organization_id
                and item.brand_id == brand_id
            ),
            None,
        )
        emotional_profile = self.repository.emotional_dna_profiles.get(emotional_dna_profile_id)
        if emotional_profile is None:
            raise InductionRationaleServiceError("EMOTIONAL_DNA_PROFILE_REQUIRED", "Emotional DNA profile is required.")
        evidence_ids = list(dict.fromkeys([*premise.evidence_ids, *emotional_profile.evidence_ids]))
        evidence = self._approved_evidence(organization_id, brand_id, evidence_ids or premise.evidence_ids)
        profile = self.voice_dna_compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            guest_id=dossier.guest_id,
            dossier=dossier,
            resonance=resonance,
            premise=premise,
            emotional_profile=emotional_profile,
            evidence=evidence,
            include_profile=include_profile,
        )
        self.repository.put_voice_dna_profile(profile)
        receipt = new_induction_rationale_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            rationale_mode=RationaleMode.full_depth if profile.status == InductionArtifactStatus.compiled else RationaleMode.partial,
            emotional_dna_profile_id=emotional_profile.emotional_dna_profile_id,
            voice_dna_profile_id=profile.voice_dna_profile_id,
            evidence_ids=profile.evidence_ids,
            compiler_versions=self._compiler_versions(),
            blocked_claims=self.psychology_validator.evaluate_claims(self._profile_claims(profile)),
            decision_code="VOICE_DNA_PROFILE_COMPILED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def compile_induction_rationales(
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
        plan = self.pre_induction_service.repository.plans.get(pre_induction_plan_id)
        if plan is None:
            raise InductionRationaleServiceError("PRE_INDUCTION_PLAN_REQUIRED", "Pre-induction plan is required.")
        if plan.organization_id != organization_id or plan.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Pre-induction plan is outside active brand scope.")
        matrix = self.matrix_service.repository.briefs.get(matrix_brief_id)
        if matrix is None:
            raise InductionRationaleServiceError("MATRIX_BRIEF_REQUIRED", "Matrix brief is required.")
        if matrix.organization_id != organization_id or matrix.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Matrix brief is outside active brand scope.")
        premise = self._context_premise(organization_id, brand_id, plan.context_premise_id)
        trigger_map = self._trigger_map(organization_id, brand_id, matrix.trigger_map_id or premise.trigger_map_id)
        dossier = self.context_service.repository.guest_dossiers[premise.guest_dossier_id]
        evidence_ids = self._rationale_evidence_ids(plan=plan, premise=premise, trigger_map=trigger_map)
        evidence = self._approved_evidence(organization_id, brand_id, evidence_ids)
        cral_findings = self.cral_compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            evidence=evidence,
        )
        for finding in cral_findings:
            self.repository.put_cral_finding(finding)
        emotional_profile = self.emotional_dna_extractor.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            guest_id=dossier.guest_id,
            dossier=dossier,
            trigger_map=trigger_map,
            premise=premise,
            evidence=evidence,
            include_profile=include_emotional_dna,
        )
        self.repository.put_emotional_dna_profile(emotional_profile)
        resonance = self.context_service.repository.resonance_contexts.get(plan.resonance_context_id) if plan.resonance_context_id else None
        voice_profile = self.voice_dna_compiler.predict(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=premise.research_field_id,
            guest_id=dossier.guest_id,
            dossier=dossier,
            resonance=resonance,
            premise=premise,
            emotional_profile=emotional_profile,
            evidence=evidence,
            include_profile=include_voice_dna,
        )
        self.repository.put_voice_dna_profile(voice_profile)
        rationales = self.rationale_compiler.predict(
            plan=plan,
            matrix=matrix,
            premise=premise,
            trigger_map=trigger_map,
            cral_findings=cral_findings,
            emotional_profile=emotional_profile,
            voice_profile=voice_profile,
            evidence=evidence,
        )
        blocked = []
        for rationale in rationales:
            blocked.extend(self.psychology_validator.evaluate_claims(rationale.supported_claims))
        if blocked:
            rationales = [
                item.model_copy(update={"rationale_mode": RationaleMode.blocked_unsupported, "status": InductionArtifactStatus.blocked})
                for item in rationales
            ]
        for rationale in rationales:
            self.repository.put_rationale(rationale)
        self._attach_to_plan(plan, rationales)
        contract_ids = self._attach_to_contracts(
            organization_id=organization_id,
            brand_id=brand_id,
            interview_deck_id=interview_deck_id,
            rationales=rationales,
        )
        mode = RationaleMode.blocked_unsupported if blocked else self._aggregate_mode([item.rationale_mode for item in rationales])
        receipt = new_induction_rationale_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            pre_induction_plan_id=pre_induction_plan_id,
            matrix_brief_id=matrix_brief_id,
            rationale_ids=[item.rationale_id for item in rationales],
            cral_finding_ids=[item.cral_finding_id for item in cral_findings],
            emotional_dna_profile_id=emotional_profile.emotional_dna_profile_id,
            voice_dna_profile_id=voice_profile.voice_dna_profile_id,
            rationale_mode=mode,
            evidence_ids=evidence_ids,
            compiler_versions=self._compiler_versions(),
            blocked_claims=blocked,
            downstream_bindings={
                "pre_induction_question_ids": [item.planned_move_id for item in rationales],
                "interview_contract_ids": contract_ids,
            },
            decision_code="INDUCTION_RATIONALE_BLOCKED_UNSUPPORTED"
            if blocked
            else "INDUCTION_RATIONALE_COMPILED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def block_unsupported_psychology(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        claims: list[SupportedPsychologyClaim],
        actor_id: UUID,
    ) -> InductionRationaleReceipt:
        blocked = self.psychology_validator.evaluate_claims(claims)
        receipt = new_induction_rationale_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            rationale_mode=RationaleMode.blocked_unsupported if blocked else RationaleMode.partial,
            evidence_ids=list(dict.fromkeys([evidence_id for claim in claims for evidence_id in claim.evidence_ids])),
            compiler_versions=self._compiler_versions(),
            blocked_claims=blocked,
            decision_code="UNSUPPORTED_PSYCHOLOGY_BLOCKED" if blocked else "PSYCHOLOGY_CLAIMS_SUPPORTED",
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def inspect_rationale_for_move(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        planned_move_id: UUID,
    ) -> InductionRationaleInspection:
        rationale = next(
            (
                item
                for item in self.repository.rationales.values()
                if item.planned_move_id == planned_move_id
                and item.organization_id == organization_id
                and item.brand_id == brand_id
            ),
            None,
        )
        if rationale is None:
            raise InductionRationaleServiceError("INDUCTION_RATIONALE_REQUIRED", "Induction rationale is required.")
        findings = [self.repository.cral_findings[item] for item in rationale.cral_finding_ids if item in self.repository.cral_findings]
        return InductionRationaleInspection(
            schema_version="cmf.induction_rationale_inspection.v1",
            rationale_id=rationale.rationale_id,
            planned_move_id=rationale.planned_move_id,
            cral_signals=[finding.signal for finding in findings],
            context_premise_id=rationale.context_premise_id,
            trigger_map_id=rationale.trigger_map_id,
            emotional_dna_profile_id=rationale.emotional_dna_profile_id,
            voice_dna_profile_id=rationale.voice_dna_profile_id,
            matrix_edge_product_id=rationale.matrix_edge_product_id,
            target_expression_state=rationale.target_expression_state,
            intended_extraction_outcome=rationale.intended_extraction_outcome,
            rationale_mode=rationale.rationale_mode,
            support_limitations=rationale.support_limitations,
        )

    def _context_premise(self, organization_id: UUID, brand_id: UUID, context_premise_id: UUID):
        premise = self.context_service.repository.context_premises.get(context_premise_id)
        if premise is None:
            raise InductionRationaleServiceError("CONTEXT_PREMISE_REQUIRED", "Context Premise is required.")
        if premise.organization_id != organization_id or premise.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Context Premise is outside active brand scope.")
        return premise

    def _trigger_map(self, organization_id: UUID, brand_id: UUID, trigger_map_id: UUID):
        trigger_map = self.context_service.repository.trigger_maps.get(trigger_map_id)
        if trigger_map is None:
            raise InductionRationaleServiceError("TRIGGER_MAP_REQUIRED", "Audience Deep Trigger Map is required.")
        if trigger_map.organization_id != organization_id or trigger_map.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Trigger map is outside active brand scope.")
        return trigger_map

    def _approved_evidence(self, organization_id: UUID, brand_id: UUID, evidence_ids: list[UUID]) -> list[ResearchEvidence]:
        try:
            return self.context_service.research_service.prepare_downstream_evidence_inputs(
                organization_id=organization_id,
                brand_id=brand_id,
                evidence_ids=list(dict.fromkeys(evidence_ids)),
            )
        except Exception as exc:
            code = getattr(exc, "code", "INDUCTION_EVIDENCE_INVALID")
            raise InductionRationaleServiceError(code, str(exc)) from exc

    @staticmethod
    def _trigger_map_evidence_ids(trigger_map: AudienceDeepTriggerMap) -> list[UUID]:
        ids: list[UUID] = []
        for collection in [
            trigger_map.hermeneutical_gaps,
            trigger_map.moral_emotional_vectors,
            trigger_map.coping_trajectory,
            trigger_map.audience_guest_matches,
            trigger_map.audience_coach_matches,
        ]:
            ids.extend(evidence_id for item in collection for evidence_id in item.evidence_ids)
        return list(dict.fromkeys(ids))

    def _rationale_evidence_ids(self, *, plan, premise, trigger_map) -> list[UUID]:
        ids = [
            *premise.evidence_ids,
            *self._trigger_map_evidence_ids(trigger_map),
            *[item for question in plan.planned_questions for item in question.evidence_ids],
        ]
        return list(dict.fromkeys(ids))

    @staticmethod
    def _profile_claims(profile) -> list[SupportedPsychologyClaim]:
        claims: list[SupportedPsychologyClaim] = []
        for attr in [
            "belief_content",
            "emotional_path",
            "suppression_markers",
            "escalation_triggers",
            "construction_mechanics",
            "negative_space",
            "normative_expression_targets",
        ]:
            claims.extend(getattr(profile, attr, []))
        return claims

    def _attach_to_plan(self, plan, rationales) -> None:
        by_move = {item.planned_move_id: item.rationale_id for item in rationales}
        questions = [
            question.model_copy(update={"rationale_id": by_move.get(question.question_id)})
            if question.question_id in by_move
            else question
            for question in plan.planned_questions
        ]
        status = plan.status
        if plan.status == PreInductionPlanStatus.superseded:
            status = PreInductionPlanStatus.superseded
        self.pre_induction_service.repository.put_plan(plan.model_copy(update={"planned_questions": questions, "status": status, "updated_at": utc_now()}))

    def _attach_to_contracts(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        interview_deck_id: UUID | None,
        rationales,
    ) -> list[UUID]:
        if self.interview_contract_service is None or interview_deck_id is None:
            return []
        deck = self.interview_contract_service.repository.decks.get(interview_deck_id)
        if deck is None:
            raise InductionRationaleServiceError("INTERVIEW_DECK_REQUIRED", "Interview deck is required.")
        if deck.organization_id != organization_id or deck.brand_id != brand_id:
            raise InductionRationaleServiceError("BRAND_SCOPE_VIOLATION", "Interview deck is outside active brand scope.")
        rationale_by_move = {item.planned_move_id: item for item in rationales}
        bound_contract_ids: list[UUID] = []
        for contract_id in deck.contract_ids:
            contract = self.interview_contract_service.repository.contracts[contract_id]
            rationale = rationale_by_move.get(contract.question_id)
            if rationale is None:
                continue
            updated_rationale = rationale.model_copy(update={"interview_contract_id": contract.contract_id, "updated_at": utc_now()})
            self.repository.put_rationale(updated_rationale)
            ids = list(dict.fromkeys([*contract.induction_rationale_ids, rationale.rationale_id]))
            self.interview_contract_service.repository.put_contract(
                contract.model_copy(update={"induction_rationale_ids": ids, "updated_at": utc_now()})
            )
            bound_contract_ids.append(contract.contract_id)
        return bound_contract_ids

    @staticmethod
    def _aggregate_mode(modes: list[RationaleMode]) -> RationaleMode:
        if any(mode == RationaleMode.blocked_unsupported for mode in modes):
            return RationaleMode.blocked_unsupported
        if any(mode == RationaleMode.partial for mode in modes):
            return RationaleMode.partial
        if any(mode == RationaleMode.shallow_supported for mode in modes):
            return RationaleMode.shallow_supported
        return RationaleMode.full_depth

    def _compiler_versions(self) -> dict[str, str]:
        return {
            "cral": self.cral_compiler.compiler_version,
            "emotional_dna": self.emotional_dna_extractor.compiler_version,
            "voice_dna": self.voice_dna_compiler.compiler_version,
            "induction_rationale": self.rationale_compiler.compiler_version,
            "supported_psychology": self.psychology_validator.compiler_version,
            "source_doctrine": "ccp-v9-narrative-state-induction;legacy-cral-voice-dna-root-down",
        }


@dataclass
class InductionRationaleCommandHandler:
    command_type: str
    service: InductionRationaleService
    aggregate_type: str = "induction_rationale"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CompileCRALFindingsCommand":
            return self.service.compile_cral_findings(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                research_field_id=UUID(payload["research_field_id"]),
                evidence_ids=[UUID(item) for item in payload["evidence_ids"]],
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "CompileAudienceDeepTriggerMapCommand":
            return self.service.compile_audience_deep_trigger_map(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                trigger_map_id=UUID(payload["trigger_map_id"]),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ExtractEmotionalDNACommand":
            return self.service.extract_emotional_dna(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                context_premise_id=UUID(payload["context_premise_id"]),
                trigger_map_id=UUID(payload["trigger_map_id"]),
                include_profile=payload.get("include_profile", True),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "CompileVoiceDNAProfileCommand":
            return self.service.compile_voice_dna_profile(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                context_premise_id=UUID(payload["context_premise_id"]),
                emotional_dna_profile_id=UUID(payload["emotional_dna_profile_id"]),
                include_profile=payload.get("include_profile", True),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "CompileInductionRationaleCommand":
            return self.service.compile_induction_rationales(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                pre_induction_plan_id=UUID(payload["pre_induction_plan_id"]),
                matrix_brief_id=UUID(payload["matrix_brief_id"]),
                interview_deck_id=UUID(payload["interview_deck_id"]) if payload.get("interview_deck_id") else None,
                include_emotional_dna=payload.get("include_emotional_dna", True),
                include_voice_dna=payload.get("include_voice_dna", True),
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockUnsupportedPsychologyCommand":
            claims = [SupportedPsychologyClaim.model_validate(item) for item in payload["claims"]]
            return self.service.block_unsupported_psychology(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                claims=claims,
                actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise InductionRationaleServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("pre_induction_plan_id") or payload.get("research_field_id") or payload.get("context_premise_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_induction_rationale_command_handlers(bus: CommandBus, service: InductionRationaleService) -> None:
    for command_type in [
        "CompileCRALFindingsCommand",
        "CompileAudienceDeepTriggerMapCommand",
        "ExtractEmotionalDNACommand",
        "CompileVoiceDNAProfileCommand",
        "CompileInductionRationaleCommand",
        "BlockUnsupportedPsychologyCommand",
    ]:
        bus.register_handler(InductionRationaleCommandHandler(command_type=command_type, service=service))
