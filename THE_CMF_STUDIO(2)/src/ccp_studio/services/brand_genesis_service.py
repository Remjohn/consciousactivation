"""Brand Genesis intake and workflow service for TS-CMF-018."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.brand_genesis import (
    BrandGenesisMissingEvidenceReport,
    BrandGenesisSession,
    BrandGenesisSessionStatus,
    BrandGenesisWorkflowRun,
    BrandSourceInput,
    CreateBrandGenesisSessionCommand,
    NegativeSpaceInput,
    VisualConstitutionInput,
    VoiceDnaReference,
    VoiceDnaReferenceKind,
    new_brand_genesis_session,
    new_genesis_start_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import ConsentVersionStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.source import SourceQualityStatus
from ccp_studio.domain.policies.consent_policy import ConsentPolicy
from ccp_studio.repositories.brand_genesis_sessions import InMemoryBrandGenesisRepository
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.source_artifacts import InMemorySourceArtifactRepository
from ccp_studio.services.command_bus import CommandBus


class BrandGenesisServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class BrandGenesisService:
    consent_repository: InMemoryConsentRepository
    source_repository: InMemorySourceArtifactRepository
    repository: InMemoryBrandGenesisRepository = field(default_factory=InMemoryBrandGenesisRepository)
    consent_policy: ConsentPolicy = field(default_factory=ConsentPolicy)

    def create_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_notes: str,
        audience_summary: str,
        offer_summary: str,
        forbidden_tone: list[str],
        visual_preferences: list[str],
        voice_dna_references: list[VoiceDnaReference],
        source_inputs: list[BrandSourceInput],
        visual_constitution_input: VisualConstitutionInput | None,
        negative_space_input: NegativeSpaceInput | None,
        created_by_actor_id: UUID,
    ) -> BrandGenesisSession:
        session = new_brand_genesis_session(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_notes=brand_notes,
            audience_summary=audience_summary,
            offer_summary=offer_summary,
            forbidden_tone=forbidden_tone,
            visual_preferences=visual_preferences,
            voice_dna_references=voice_dna_references,
            source_inputs=source_inputs,
            visual_constitution_input=visual_constitution_input,
            negative_space_input=negative_space_input,
            created_by_actor_id=created_by_actor_id,
        )
        self.repository.put_session(session)
        report = self.validate_intake(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=session.brand_genesis_session_id,
        )
        if not report.complete:
            blocked = session.model_copy(
                update={
                    "status": BrandGenesisSessionStatus.blocked,
                    "last_missing_evidence_report_id": report.brand_genesis_session_id,
                    "updated_at": utc_now(),
                }
            )
            return self.repository.put_session(blocked)
        ready = session.model_copy(update={"status": BrandGenesisSessionStatus.ready, "updated_at": utc_now()})
        return self.repository.put_session(ready)

    def validate_intake(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
    ) -> BrandGenesisMissingEvidenceReport:
        session = self._session_for_brand(organization_id, brand_id, brand_genesis_session_id)
        missing_fields: list[str] = []
        blocker_codes: list[str] = []

        self._require_text(session.brand_notes, "brand_notes", missing_fields)
        self._require_text(session.audience_summary, "audience_summary", missing_fields)
        self._require_text(session.offer_summary, "offer_summary", missing_fields)
        self._require_list(session.forbidden_tone, "forbidden_tone", missing_fields)
        self._require_list(session.visual_preferences, "visual_preferences", missing_fields)
        self._require_list(session.voice_dna_references, "voice_dna_references", missing_fields)
        self._require_list(session.source_inputs, "source_inputs", missing_fields)
        if session.visual_constitution_input is None:
            missing_fields.append("visual_constitution_input")
        if session.negative_space_input is None:
            missing_fields.append("negative_space_input")

        if not missing_fields:
            blocker_codes.extend(self._validate_voice_dna_references(session.voice_dna_references))
            blocker_codes.extend(self._validate_source_inputs(session, require_accepted_source=False))

        report = BrandGenesisMissingEvidenceReport(
            schema_version="cmf.brand_genesis_missing_evidence_report.v1",
            brand_genesis_session_id=session.brand_genesis_session_id,
            organization_id=session.organization_id,
            brand_id=session.brand_id,
            missing_fields=missing_fields,
            blocker_codes=blocker_codes,
            fabricated_defaults_used=False,
            created_at=utc_now(),
        )
        self.repository.put_missing_evidence_report(report)
        return report

    def start_workflow(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        actor_id: UUID,
    ) -> BrandGenesisWorkflowRun:
        session = self._session_for_brand(organization_id, brand_id, brand_genesis_session_id)
        report = self.validate_intake(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
        )
        if report.missing_fields:
            self._block_session(session)
            raise BrandGenesisServiceError(
                "BRAND_GENESIS_INTAKE_INCOMPLETE",
                "Brand Genesis intake is incomplete; inspect missing evidence report.",
            )
        if report.blocker_codes:
            self._block_session(session)
            code = "CONSENT_SCOPE_BLOCKED" if "CONSENT_SCOPE_BLOCKED" in report.blocker_codes else report.blocker_codes[0]
            raise BrandGenesisServiceError(code, "Brand Genesis intake has unresolved blockers.")
        blocker_codes = self._validate_source_inputs(session, require_accepted_source=True)
        if blocker_codes:
            self._block_session(session)
            code = "CONSENT_SCOPE_BLOCKED" if "CONSENT_SCOPE_BLOCKED" in blocker_codes else blocker_codes[0]
            raise BrandGenesisServiceError(code, "Brand Genesis cannot start until source and consent are complete.")

        receipt = new_genesis_start_receipt(
            session=session,
            actor_id=actor_id,
            decision_code="BRAND_GENESIS_WORKFLOW_STARTED",
            evidence_refs=[
                session.storage_prefix,
                *[str(source_id) for source in session.source_inputs for source_id in source.source_artifact_ids],
                *[str(reference.voice_dna_reference_id) for reference in session.voice_dna_references],
            ],
        )
        self.repository.put_start_receipt(receipt)
        running = session.model_copy(update={"status": BrandGenesisSessionStatus.running, "updated_at": utc_now()})
        self.repository.put_session(running)
        run = BrandGenesisWorkflowRun(
            schema_version="cmf.brand_genesis_workflow_run.v1",
            workflow_run_id=uuid4(),
            brand_genesis_session_id=session.brand_genesis_session_id,
            organization_id=session.organization_id,
            brand_id=session.brand_id,
            start_receipt_id=receipt.genesis_start_receipt_id,
            status="started",
            started_at=utc_now(),
        )
        return self.repository.put_workflow_run(run)

    def get_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
    ) -> BrandGenesisSession:
        return self._session_for_brand(organization_id, brand_id, brand_genesis_session_id)

    def list_sessions_for_brand(self, *, organization_id: UUID, brand_id: UUID) -> list[BrandGenesisSession]:
        return self.repository.list_sessions_for_brand(organization_id=organization_id, brand_id=brand_id)

    def _validate_voice_dna_references(self, references: list[VoiceDnaReference]) -> list[str]:
        blockers: list[str] = []
        for reference in references:
            if not reference.approved:
                blockers.append("VOICE_DNA_REFERENCE_NOT_APPROVED")
            if reference.reference_kind == VoiceDnaReferenceKind.raw_legacy_reference:
                blockers.append("VOICE_DNA_REFERENCE_NOT_MIGRATED")
            if reference.reference_kind == VoiceDnaReferenceKind.migrated_registry_entry and reference.registry_entry_id is None:
                blockers.append("VOICE_DNA_REGISTRY_ENTRY_REQUIRED")
        return blockers

    def _validate_source_inputs(self, session: BrandGenesisSession, *, require_accepted_source: bool) -> list[str]:
        blockers: list[str] = []
        for source_input in session.source_inputs:
            consent_version = self.consent_repository.versions.get(source_input.consent_record_version_id)
            if consent_version is None:
                blockers.append("CONSENT_RECORD_REQUIRED")
            elif consent_version.organization_id != session.organization_id or consent_version.brand_id != session.brand_id:
                blockers.append("BRAND_SCOPE_VIOLATION")
            elif consent_version.status != ConsentVersionStatus.active:
                decision = self.consent_policy.evaluate(
                    command_type="StartBrandGenesisWorkflowCommand",
                    version=consent_version,
                )
                blockers.append(decision.decision_code)
            else:
                required_scopes = [
                    "source_storage_allowed",
                    "likeness_use_allowed",
                    "derivative_generation_allowed",
                    "provider_processing_allowed",
                    "reuse_allowed",
                    "retention_allowed",
                ]
                for scope_name in required_scopes:
                    if not getattr(consent_version.scope, scope_name):
                        blockers.append("CONSENT_SCOPE_BLOCKED")
                        break

            for artifact_id in source_input.source_artifact_ids:
                artifact = self.source_repository.artifacts.get(artifact_id)
                if artifact is None:
                    blockers.append("BRAND_SOURCE_REQUIRED")
                    continue
                if artifact.organization_id != session.organization_id or artifact.brand_id != session.brand_id:
                    blockers.append("BRAND_SCOPE_VIOLATION")
                if require_accepted_source and artifact.accepted_at is None:
                    blockers.append("BRAND_SOURCE_REQUIRED")

            if require_accepted_source and source_input.source_quality_receipt_ids:
                for report_id in source_input.source_quality_receipt_ids:
                    report = self.source_repository.reports.get(report_id)
                    if report is None or report.status != SourceQualityStatus.accepted:
                        blockers.append("BRAND_SOURCE_REQUIRED")
            elif require_accepted_source:
                blockers.append("BRAND_SOURCE_REQUIRED")

        return list(dict.fromkeys(blockers))

    def _session_for_brand(
        self,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
    ) -> BrandGenesisSession:
        session = self.repository.get_session_for_brand(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=brand_genesis_session_id,
        )
        if session is None:
            existing = self.repository.get_session(brand_genesis_session_id)
            if existing is not None:
                raise BrandGenesisServiceError("BRAND_SCOPE_VIOLATION", "Brand Genesis session is outside the active brand scope.")
            raise BrandGenesisServiceError("BRAND_GENESIS_SESSION_REQUIRED", "Brand Genesis session is required.")
        return session

    def _block_session(self, session: BrandGenesisSession) -> BrandGenesisSession:
        blocked = session.model_copy(update={"status": BrandGenesisSessionStatus.blocked, "updated_at": utc_now()})
        return self.repository.put_session(blocked)

    @staticmethod
    def _require_text(value: str, field_name: str, missing_fields: list[str]) -> None:
        if not value or not value.strip():
            missing_fields.append(field_name)

    @staticmethod
    def _require_list(value: list[Any], field_name: str, missing_fields: list[str]) -> None:
        if not value:
            missing_fields.append(field_name)


@dataclass
class BrandGenesisCommandHandler:
    command_type: str
    service: BrandGenesisService
    aggregate_type: str = "brand_genesis"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        if self.command_type == "CreateBrandGenesisSessionCommand":
            command = CreateBrandGenesisSessionCommand(**envelope.payload)
            session = self.service.create_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_notes=command.brand_notes,
                audience_summary=command.audience_summary,
                offer_summary=command.offer_summary,
                forbidden_tone=command.forbidden_tone,
                visual_preferences=command.visual_preferences,
                voice_dna_references=command.voice_dna_references,
                source_inputs=command.source_inputs,
                visual_constitution_input=command.visual_constitution_input,
                negative_space_input=command.negative_space_input,
                created_by_actor_id=envelope.actor.actor_id,
            )
            return session.model_dump(mode="json")
        if self.command_type == "StartBrandGenesisWorkflowCommand":
            run = self.service.start_workflow(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_genesis_session_id=UUID(envelope.payload["brand_genesis_session_id"]),
                actor_id=envelope.actor.actor_id,
            )
            return run.model_dump(mode="json")
        raise BrandGenesisServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("brand_genesis_session_id") or envelope.payload.get("brand_genesis_session_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_brand_genesis_command_handlers(bus: CommandBus, service: BrandGenesisService) -> None:
    for command_type in ["CreateBrandGenesisSessionCommand", "StartBrandGenesisWorkflowCommand"]:
        bus.register_handler(BrandGenesisCommandHandler(command_type=command_type, service=service))
