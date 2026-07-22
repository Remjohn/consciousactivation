"""Context compilation service for TS-CMF-024."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.context import (
    AudienceDeepTriggerMap,
    AudienceRealityBrief,
    ContextArtifactKind,
    ContextArtifactSaturationPacket,
    ContextCompilationReceipt,
    ContextCompilerInputPacket,
    ContextOutputStatus,
    ContextPremise,
    GuestDossier,
    InterviewerResonanceContext,
    new_context_compilation_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.research import ResearchEvidence, citation_hash
from ccp_studio.dspy_programs.context_compilers import (
    AudienceDeepTriggerMapCompiler,
    AudienceRealityBriefCompiler,
    ContextPremiseCompiler,
    GuestDossierCompiler,
    InterviewerResonanceCompiler,
)
from ccp_studio.repositories.context import InMemoryContextRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.research_service import ResearchService


class ContextCompilationServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ContextCompilationService:
    research_service: ResearchService
    repository: InMemoryContextRepository = field(default_factory=InMemoryContextRepository)
    guest_dossier_compiler: GuestDossierCompiler = field(default_factory=GuestDossierCompiler)
    audience_reality_compiler: AudienceRealityBriefCompiler = field(default_factory=AudienceRealityBriefCompiler)
    trigger_map_compiler: AudienceDeepTriggerMapCompiler = field(default_factory=AudienceDeepTriggerMapCompiler)
    context_premise_compiler: ContextPremiseCompiler = field(default_factory=ContextPremiseCompiler)
    resonance_compiler: InterviewerResonanceCompiler = field(default_factory=InterviewerResonanceCompiler)

    def compile_context_artifacts(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence_ids: list[UUID],
        operator_id: UUID,
        audience_scope: str,
        compiler_actor_id: UUID,
        research_snapshot_id: UUID | None = None,
        guest_id: UUID | None = None,
        guest_profile_hints: list[str] | None = None,
        operator_notes: list[str] | None = None,
        brand_context_version_id: UUID | None = None,
        premise_statement: str | None = None,
        reviewer_state: str = "pending_review",
    ) -> ContextCompilationReceipt:
        evidence = self._approved_evidence(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_ids=evidence_ids,
        )
        self._research_field_for_brand(organization_id, brand_id, research_field_id)
        packet = ContextCompilerInputPacket(
            schema_version="cmf.context_compiler_input_packet.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            approved_evidence_ids=evidence_ids,
            research_snapshot_id=research_snapshot_id,
            guest_id=guest_id,
            audience_scope=audience_scope,
            operator_id=operator_id,
            guest_profile_hints=guest_profile_hints or [],
            operator_notes=operator_notes or [],
            brand_context_version_id=brand_context_version_id,
        )
        dossier = self.repository.put_guest_dossier(self.guest_dossier_compiler.predict(packet, evidence))
        audience_brief = self.repository.put_audience_reality_brief(
            self.audience_reality_compiler.predict(packet, evidence)
        )
        trigger_map = self.repository.put_trigger_map(
            self.trigger_map_compiler.predict(packet, evidence, dossier, audience_brief)
        )
        premise = self.repository.put_context_premise(
            self.context_premise_compiler.predict(
                packet,
                evidence,
                dossier,
                audience_brief,
                trigger_map,
                statement_override=premise_statement,
            )
        )
        resonance = self.repository.put_resonance_context(self.resonance_compiler.predict(packet, evidence))
        evaluator_results = self._evaluator_results(
            dossier=dossier,
            audience_brief=audience_brief,
            trigger_map=trigger_map,
            premise=premise,
            resonance=resonance,
        )
        receipt = new_context_compilation_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            compiler_version=";".join(
                [
                    self.guest_dossier_compiler.compiler_version,
                    self.audience_reality_compiler.compiler_version,
                    self.trigger_map_compiler.compiler_version,
                    self.context_premise_compiler.compiler_version,
                    self.resonance_compiler.compiler_version,
                ]
            ),
            input_evidence_ids=evidence_ids,
            input_packet_hash=packet.stable_hash(),
            source_hashes=self._source_hashes(evidence),
            output_ids={
                ContextArtifactKind.guest_dossier: dossier.guest_dossier_id,
                ContextArtifactKind.audience_reality_brief: audience_brief.audience_reality_brief_id,
                ContextArtifactKind.audience_deep_trigger_map: trigger_map.trigger_map_id,
                ContextArtifactKind.context_premise: premise.context_premise_id,
                ContextArtifactKind.interviewer_resonance_context: resonance.resonance_context_id,
            },
            evaluator_results=evaluator_results,
            reviewer_state=reviewer_state,
            decision_code="CONTEXT_ARTIFACTS_COMPILED",
            reviewer_actor_id=compiler_actor_id,
        )
        return self.repository.put_receipt(receipt)

    def approve_context_artifact(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        artifact_kind: ContextArtifactKind,
        artifact_id: UUID,
        reviewer_actor_id: UUID,
    ):
        artifact = self._artifact_for_brand(organization_id, brand_id, artifact_kind, artifact_id)
        if getattr(artifact, "status") == ContextOutputStatus.rejected:
            raise ContextCompilationServiceError("CONTEXT_ARTIFACT_REJECTED", "Rejected context artifact cannot be approved.")
        if isinstance(artifact, ContextPremise) and artifact.unsupported_inference_flags:
            raise ContextCompilationServiceError(
                "CONTEXT_INFERENCE_UNSUPPORTED",
                "Context Premise has unsupported inference flags.",
            )
        evidence_ids = self._artifact_evidence_ids(artifact)
        self._approved_evidence(organization_id=organization_id, brand_id=brand_id, evidence_ids=evidence_ids)
        approved = artifact.model_copy(update={"status": ContextOutputStatus.approved, "updated_at": utc_now()})
        self.repository.put_artifact(artifact_kind, approved)
        self.repository.put_receipt(
            new_context_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                research_field_id=approved.research_field_id,
                compiler_version="reviewer-approval-v1",
                input_evidence_ids=evidence_ids,
                input_packet_hash=f"artifact:{artifact_id}",
                source_hashes=[],
                output_ids={artifact_kind: artifact_id},
                evaluator_results=["approved context artifact has evidence-backed inference refs"],
                reviewer_state="approved",
                decision_code=f"CONTEXT_ARTIFACT_APPROVED:{artifact_kind.value}",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return approved

    def reject_unsupported_context_inference(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        context_premise_id: UUID,
        reviewer_actor_id: UUID,
        reason: str,
    ) -> ContextPremise:
        premise = self._artifact_for_brand(
            organization_id,
            brand_id,
            ContextArtifactKind.context_premise,
            context_premise_id,
        )
        flags = list(dict.fromkeys([*premise.unsupported_inference_flags, reason]))
        revised = premise.model_copy(
            update={
                "unsupported_inference_flags": flags,
                "status": ContextOutputStatus.evidence_review_required,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_context_premise(revised)
        self.repository.put_receipt(
            new_context_compilation_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                research_field_id=premise.research_field_id,
                compiler_version="reviewer-rejection-v1",
                input_evidence_ids=premise.evidence_ids,
                input_packet_hash=f"premise:{context_premise_id}",
                source_hashes=[],
                output_ids={ContextArtifactKind.context_premise: context_premise_id},
                evaluator_results=flags,
                reviewer_state="revision_required",
                decision_code="CONTEXT_INFERENCE_REJECTED",
                reviewer_actor_id=reviewer_actor_id,
            )
        )
        return revised

    def prepare_downstream_context_inputs(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_dossier_id: UUID,
        audience_reality_brief_id: UUID,
        context_premise_id: UUID,
        trigger_map_id: UUID | None = None,
        interviewer_resonance_context_id: UUID | None = None,
    ) -> ContextArtifactSaturationPacket:
        dossier = self._approved_artifact(
            organization_id,
            brand_id,
            ContextArtifactKind.guest_dossier,
            guest_dossier_id,
        )
        audience = self._approved_artifact(
            organization_id,
            brand_id,
            ContextArtifactKind.audience_reality_brief,
            audience_reality_brief_id,
        )
        premise = self._approved_artifact(
            organization_id,
            brand_id,
            ContextArtifactKind.context_premise,
            context_premise_id,
        )
        if trigger_map_id is not None:
            self._approved_artifact(
                organization_id,
                brand_id,
                ContextArtifactKind.audience_deep_trigger_map,
                trigger_map_id,
            )
        if interviewer_resonance_context_id is not None:
            self._approved_artifact(
                organization_id,
                brand_id,
                ContextArtifactKind.interviewer_resonance_context,
                interviewer_resonance_context_id,
            )
        evidence_ids = list(dict.fromkeys([*self._artifact_evidence_ids(dossier), *self._artifact_evidence_ids(audience), *premise.evidence_ids]))
        receipt_ids = [
            receipt.context_compilation_receipt_id
            for receipt in self.repository.receipts.values()
            if any(output_id in receipt.output_ids.values() for output_id in [guest_dossier_id, audience_reality_brief_id, context_premise_id])
        ]
        return ContextArtifactSaturationPacket(
            schema_version="cmf.context_artifact_saturation_packet.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            guest_dossier_id=guest_dossier_id,
            audience_reality_brief_id=audience_reality_brief_id,
            context_premise_id=context_premise_id,
            trigger_map_id=trigger_map_id,
            interviewer_resonance_context_id=interviewer_resonance_context_id,
            evidence_ids=evidence_ids,
            context_compilation_receipt_ids=receipt_ids,
        )

    def _approved_evidence(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        evidence_ids: list[UUID],
    ) -> list[ResearchEvidence]:
        if not evidence_ids:
            raise ContextCompilationServiceError("CONTEXT_EVIDENCE_REQUIRED", "Context compilation requires approved evidence.")
        try:
            return self.research_service.prepare_downstream_evidence_inputs(
                organization_id=organization_id,
                brand_id=brand_id,
                evidence_ids=evidence_ids,
            )
        except Exception as exc:
            code = getattr(exc, "code", "CONTEXT_EVIDENCE_INVALID")
            raise ContextCompilationServiceError(code, str(exc)) from exc

    def _research_field_for_brand(self, organization_id: UUID, brand_id: UUID, research_field_id: UUID) -> None:
        field_record = self.research_service.repository.fields.get(research_field_id)
        if field_record is None:
            raise ContextCompilationServiceError("RESEARCH_FIELD_REQUIRED", "Research field is required.")
        if field_record.organization_id != organization_id or field_record.brand_id != brand_id:
            raise ContextCompilationServiceError("BRAND_SCOPE_VIOLATION", "Research field is outside active brand scope.")

    def _artifact_for_brand(
        self,
        organization_id: UUID,
        brand_id: UUID,
        artifact_kind: ContextArtifactKind,
        artifact_id: UUID,
    ):
        artifact = self.repository.get_artifact(artifact_kind, artifact_id)
        if artifact is None:
            raise ContextCompilationServiceError("CONTEXT_ARTIFACT_REQUIRED", "Context artifact is required.")
        if artifact.organization_id != organization_id or artifact.brand_id != brand_id:
            raise ContextCompilationServiceError("BRAND_SCOPE_VIOLATION", "Context artifact is outside active brand scope.")
        return artifact

    def _approved_artifact(
        self,
        organization_id: UUID,
        brand_id: UUID,
        artifact_kind: ContextArtifactKind,
        artifact_id: UUID,
    ):
        artifact = self._artifact_for_brand(organization_id, brand_id, artifact_kind, artifact_id)
        if artifact.status != ContextOutputStatus.approved:
            raise ContextCompilationServiceError("CONTEXT_ARTIFACT_NOT_APPROVED", "Only approved context artifacts can feed downstream contracts.")
        return artifact

    @staticmethod
    def _artifact_evidence_ids(artifact) -> list[UUID]:
        if isinstance(artifact, ContextPremise):
            return artifact.evidence_ids
        if isinstance(artifact, InterviewerResonanceContext):
            return artifact.evidence_ids
        evidence_ids: list[UUID] = []
        for value in artifact.model_dump().values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "evidence_ids" in item:
                        evidence_ids.extend(UUID(evidence_id) if isinstance(evidence_id, str) else evidence_id for evidence_id in item["evidence_ids"])
        return list(dict.fromkeys(evidence_ids))

    @staticmethod
    def _source_hashes(evidence: list[ResearchEvidence]) -> list[str]:
        hashes: list[str] = []
        for item in evidence:
            for citation in item.citations:
                hashes.append(citation_hash(citation))
        return hashes

    @staticmethod
    def _evaluator_results(
        *,
        dossier: GuestDossier,
        audience_brief: AudienceRealityBrief,
        trigger_map: AudienceDeepTriggerMap,
        premise: ContextPremise,
        resonance: InterviewerResonanceContext,
    ) -> list[str]:
        results = [
            "guest dossier preserves sourced guest truth",
            "audience reality brief preserves audience pressure fields",
            f"trigger depth mode:{trigger_map.depth_mode.value}",
            "context premise stored as temporary working hypothesis",
            "interviewer resonance preserves authentic curiosity and avoid-list",
        ]
        if not dossier.identity_facts:
            results.append("guest dossier missing identity facts")
        if not audience_brief.current_anxieties:
            results.append("audience brief missing current anxieties")
        results.extend(premise.unsupported_inference_flags)
        if not resonance.questions_to_avoid:
            results.append("resonance avoid-list missing")
        return results


@dataclass
class ContextCompilationCommandHandler:
    command_type: str
    service: ContextCompilationService
    aggregate_type: str = "context"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {
            "CompileGuestDossierCommand",
            "CompileAudienceRealityBriefCommand",
            "CompileContextPremiseCommand",
            "CompileInterviewerResonanceCommand",
            "CompileContextArtifactsCommand",
        }:
            receipt = self.service.compile_context_artifacts(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                research_field_id=UUID(payload["research_field_id"]),
                evidence_ids=[UUID(item) for item in payload["evidence_ids"]],
                operator_id=UUID(payload["operator_id"]),
                audience_scope=payload["audience_scope"],
                compiler_actor_id=envelope.actor.actor_id,
                research_snapshot_id=UUID(payload["research_snapshot_id"]) if payload.get("research_snapshot_id") else None,
                guest_id=UUID(payload["guest_id"]) if payload.get("guest_id") else None,
                guest_profile_hints=payload.get("guest_profile_hints", []),
                operator_notes=payload.get("operator_notes", []),
                brand_context_version_id=UUID(payload["brand_context_version_id"]) if payload.get("brand_context_version_id") else None,
                premise_statement=payload.get("premise_statement"),
                reviewer_state=payload.get("reviewer_state", "pending_review"),
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "ApproveContextArtifactCommand":
            artifact = self.service.approve_context_artifact(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                artifact_kind=ContextArtifactKind(payload["artifact_kind"]),
                artifact_id=UUID(payload["artifact_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
            )
            return artifact.model_dump(mode="json")
        if self.command_type == "RejectUnsupportedContextInferenceCommand":
            premise = self.service.reject_unsupported_context_inference(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                context_premise_id=UUID(payload["context_premise_id"]),
                reviewer_actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
            )
            return premise.model_dump(mode="json")
        raise ContextCompilationServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("research_field_id") or payload.get("artifact_id") or payload.get("context_premise_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_context_compilation_command_handlers(bus: CommandBus, service: ContextCompilationService) -> None:
    for command_type in [
        "CompileGuestDossierCommand",
        "CompileAudienceRealityBriefCommand",
        "CompileContextPremiseCommand",
        "CompileInterviewerResonanceCommand",
        "CompileContextArtifactsCommand",
        "ApproveContextArtifactCommand",
        "RejectUnsupportedContextInferenceCommand",
    ]:
        bus.register_handler(ContextCompilationCommandHandler(command_type=command_type, service=service))
