"""Complete Expression Session service for TS-CMF-029."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import ConsentVersionStatus
from ccp_studio.contracts.expression_session import (
    CompleteExpressionSession,
    ExpressionSessionStatus,
    SessionQualityGateRef,
    SessionStartReceipt,
    new_session_start_receipt,
    new_session_status_event,
    recording_ref_from_configuration,
)
from ccp_studio.contracts.interview_contracts import InterviewContractStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.expression_sessions import InMemoryExpressionSessionRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.consent_service import ConsentService
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.source_ingestion import SourceIngestionService


class CompleteExpressionSessionServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CompleteExpressionSessionService:
    consent_service: ConsentService
    source_service: SourceIngestionService
    interview_contract_service: InterviewContractService
    repository: InMemoryExpressionSessionRepository = field(default_factory=InMemoryExpressionSessionRepository)

    def create_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_id: UUID,
        operator_id: UUID,
        interview_deck_id: UUID,
        consent_record_version_id: UUID,
        conversation_language: str,
        created_by_actor_id: UUID,
        expected_master_source: str,
        backup_route: str,
        platform_source: str | None,
        upload_method: str,
        file_safety_expectations: list[str],
        quality_requirements: list[str],
        session_mode: str = "guided_interview",
        orientation: str = "vertical",
        quality_gate_passed: bool = True,
        system_label_language: str = "en",
        command_id: UUID | None = None,
    ) -> CompleteExpressionSession:
        deck = self._approved_deck(organization_id, brand_id, interview_deck_id)
        consent = self._current_consent(organization_id, brand_id, guest_id, consent_record_version_id)
        session_id = uuid4()
        configuration = self.source_service.submit_recording_configuration(
            organization_id=organization_id,
            brand_id=brand_id,
            session_id=session_id,
            expected_master_source=expected_master_source,
            backup_route=backup_route,
            platform_source=platform_source,
            upload_method=upload_method,
            file_safety_expectations=file_safety_expectations,
            quality_requirements=quality_requirements,
        )
        now = utc_now()
        status = ExpressionSessionStatus.ready_for_recording if quality_gate_passed else ExpressionSessionStatus.draft
        session = CompleteExpressionSession(
            schema_version="cmf.complete_expression_session.v1",
            expression_session_id=session_id,
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            operator_id=operator_id,
            conversation_language=conversation_language,
            system_label_language=system_label_language,
            interview_deck_id=interview_deck_id,
            interview_asset_contract_ids=deck.contract_ids,
            consent_record_version_id=consent.consent_record_version_id,
            recording_configuration=recording_ref_from_configuration(
                configuration,
                session_mode=session_mode,
                orientation=orientation,
            ),
            pre_session_quality_gate=SessionQualityGateRef(
                schema_version="cmf.session_quality_gate_ref.v1",
                pre_session_quality_gate_id=uuid4(),
                gate_version="pre-session-quality-gate-v1",
                required_checks=[
                    "approved_interview_deck",
                    "active_consent_record",
                    "recording_configuration",
                    "source_truth_protocol",
                ],
                passed=quality_gate_passed,
            ),
            status=status,
            created_at=now,
            updated_at=now,
        )
        self.repository.put_session(session)
        self.repository.put_status_event(
            new_session_status_event(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=session_id,
                from_status=None,
                to_status=status,
                reason="Complete Expression Session created from approved interview contracts and setup.",
                actor_id=created_by_actor_id,
                command_id=command_id,
            )
        )
        self.repository.put_receipt(
            new_session_start_receipt(
                session=session,
                decision_code="COMPLETE_EXPRESSION_SESSION_CREATED",
                command_id=command_id,
                reviewer_actor_id=created_by_actor_id,
            )
        )
        return session

    def validate_readiness(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> SessionStartReceipt:
        session = self._session_for_brand(organization_id, brand_id, expression_session_id)
        missing = self._missing_readiness(session)
        decision = "SESSION_READINESS_VALIDATED" if not missing else "SESSION_READINESS_BLOCKED"
        receipt = new_session_start_receipt(
            session=session,
            decision_code=decision,
            missing_requirements=missing,
            command_id=command_id,
            reviewer_actor_id=actor_id,
        )
        return self.repository.put_receipt(receipt)

    def start_session(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> CompleteExpressionSession:
        session = self._session_for_brand(organization_id, brand_id, expression_session_id)
        if session.status not in {ExpressionSessionStatus.ready_for_recording, ExpressionSessionStatus.paused}:
            self._blocked_receipt(
                session,
                ["SESSION_NOT_READY_FOR_RECORDING", *self._missing_readiness(session)],
                actor_id,
                command_id,
            )
            raise CompleteExpressionSessionServiceError("SESSION_NOT_READY_FOR_RECORDING", "Session must be ready or paused before start.")
        readiness = self.validate_readiness(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
            command_id=command_id,
        )
        if readiness.missing_requirements:
            raise CompleteExpressionSessionServiceError(readiness.decision_code, ", ".join(readiness.missing_requirements))
        deck = self.interview_contract_service.repository.decks[session.interview_deck_id]
        if deck.status == InterviewContractStatus.approved:
            self.interview_contract_service.bind_deck_to_expression_session(
                organization_id=organization_id,
                brand_id=brand_id,
                interview_deck_id=session.interview_deck_id,
                expression_session_id=session.expression_session_id,
                actor_id=actor_id,
            )
        started = session.model_copy(
            update={
                "status": ExpressionSessionStatus.in_progress,
                "started_at": session.started_at or utc_now(),
                "updated_at": utc_now(),
            }
        )
        self.repository.put_session(started)
        self.repository.put_status_event(
            new_session_status_event(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                from_status=session.status,
                to_status=ExpressionSessionStatus.in_progress,
                reason="Complete Expression Session started after consent and recording readiness.",
                actor_id=actor_id,
                command_id=command_id,
            )
        )
        self.repository.put_receipt(
            new_session_start_receipt(
                session=started,
                decision_code="COMPLETE_EXPRESSION_SESSION_STARTED",
                command_id=command_id,
                reviewer_actor_id=actor_id,
            )
        )
        return started

    def pause_session(self, *, organization_id: UUID, brand_id: UUID, expression_session_id: UUID, actor_id: UUID, reason: str, command_id: UUID | None = None) -> CompleteExpressionSession:
        return self._transition(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
            to_status=ExpressionSessionStatus.paused,
            allowed_from={ExpressionSessionStatus.in_progress},
            reason=reason,
            decision_code="COMPLETE_EXPRESSION_SESSION_PAUSED",
            command_id=command_id,
        )

    def resume_session(self, *, organization_id: UUID, brand_id: UUID, expression_session_id: UUID, actor_id: UUID, reason: str = "Resume governed capture.", command_id: UUID | None = None) -> CompleteExpressionSession:
        return self._transition(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
            to_status=ExpressionSessionStatus.in_progress,
            allowed_from={ExpressionSessionStatus.paused},
            reason=reason,
            decision_code="COMPLETE_EXPRESSION_SESSION_RESUMED",
            command_id=command_id,
        )

    def fail_session(self, *, organization_id: UUID, brand_id: UUID, expression_session_id: UUID, actor_id: UUID, reason: str, command_id: UUID | None = None) -> CompleteExpressionSession:
        return self._transition(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
            to_status=ExpressionSessionStatus.failed,
            allowed_from={
                ExpressionSessionStatus.draft,
                ExpressionSessionStatus.ready_for_recording,
                ExpressionSessionStatus.in_progress,
                ExpressionSessionStatus.paused,
            },
            reason=reason,
            decision_code="COMPLETE_EXPRESSION_SESSION_FAILED",
            command_id=command_id,
        )

    def close_session(self, *, organization_id: UUID, brand_id: UUID, expression_session_id: UUID, actor_id: UUID, reason: str = "Capture complete.", command_id: UUID | None = None) -> CompleteExpressionSession:
        return self._transition(
            organization_id=organization_id,
            brand_id=brand_id,
            expression_session_id=expression_session_id,
            actor_id=actor_id,
            to_status=ExpressionSessionStatus.closed,
            allowed_from={ExpressionSessionStatus.in_progress, ExpressionSessionStatus.paused},
            reason=reason,
            decision_code="COMPLETE_EXPRESSION_SESSION_CLOSED",
            command_id=command_id,
        )

    def list_sessions_for_brand(self, *, organization_id: UUID, brand_id: UUID) -> list[CompleteExpressionSession]:
        return self.repository.sessions_for_brand(organization_id, brand_id)

    def get_session(self, *, organization_id: UUID, brand_id: UUID, expression_session_id: UUID) -> CompleteExpressionSession:
        return self._session_for_brand(organization_id, brand_id, expression_session_id)

    def _approved_deck(self, organization_id: UUID, brand_id: UUID, interview_deck_id: UUID):
        deck = self.interview_contract_service.repository.decks.get(interview_deck_id)
        if deck is None:
            raise CompleteExpressionSessionServiceError("INTERVIEW_DECK_REQUIRED", "Approved Interview Deck is required.")
        if deck.organization_id != organization_id or deck.brand_id != brand_id:
            raise CompleteExpressionSessionServiceError("BRAND_SCOPE_VIOLATION", "Interview Deck is outside active brand scope.")
        if deck.status != InterviewContractStatus.approved:
            raise CompleteExpressionSessionServiceError("INTERVIEW_DECK_APPROVAL_REQUIRED", "Interview Deck must be approved before session creation.")
        contracts = [self.interview_contract_service.repository.contracts[item] for item in deck.contract_ids]
        if not contracts or any(contract.status != InterviewContractStatus.approved for contract in contracts):
            raise CompleteExpressionSessionServiceError("INTERVIEW_CONTRACT_APPROVAL_REQUIRED", "All Interview Asset Contracts must be approved.")
        return deck

    def _current_consent(self, organization_id: UUID, brand_id: UUID, guest_id: UUID, consent_record_version_id: UUID):
        consent = self.consent_service.repository.current_version(organization_id, brand_id, guest_id)
        if consent is None:
            raise CompleteExpressionSessionServiceError("CONSENT_RECORD_REQUIRED", "Current consent is required.")
        if consent.consent_record_version_id != consent_record_version_id:
            raise CompleteExpressionSessionServiceError("CONSENT_VERSION_MISMATCH", "Session must use the current consent version.")
        if consent.status != ConsentVersionStatus.active:
            raise CompleteExpressionSessionServiceError("ACTIVE_CONSENT_REQUIRED", "Consent must be active.")
        return consent

    def _session_for_brand(self, organization_id: UUID, brand_id: UUID, expression_session_id: UUID) -> CompleteExpressionSession:
        session = self.repository.sessions.get(expression_session_id)
        if session is None:
            raise CompleteExpressionSessionServiceError("EXPRESSION_SESSION_REQUIRED", "Complete Expression Session is required.")
        if session.organization_id != organization_id or session.brand_id != brand_id:
            raise CompleteExpressionSessionServiceError("BRAND_SCOPE_VIOLATION", "Expression session is outside active brand scope.")
        return session

    def _missing_readiness(self, session: CompleteExpressionSession) -> list[str]:
        missing: list[str] = []
        consent = self.consent_service.repository.current_version(session.organization_id, session.brand_id, session.guest_id)
        if consent is None or consent.consent_record_version_id != session.consent_record_version_id:
            missing.append("CONSENT_RECORD_REQUIRED")
        elif consent.status != ConsentVersionStatus.active:
            missing.append("ACTIVE_CONSENT_REQUIRED")
        else:
            if not consent.scope.recording_allowed:
                missing.append("CONSENT_RECORDING_SCOPE_REQUIRED")
            if not consent.scope.source_storage_allowed:
                missing.append("CONSENT_SOURCE_STORAGE_SCOPE_REQUIRED")
        deck = self.interview_contract_service.repository.decks.get(session.interview_deck_id)
        if deck is None:
            missing.append("INTERVIEW_DECK_REQUIRED")
        elif deck.organization_id != session.organization_id or deck.brand_id != session.brand_id:
            missing.append("BRAND_SCOPE_VIOLATION")
        elif deck.status not in {InterviewContractStatus.approved, InterviewContractStatus.bound_to_session}:
            missing.append("INTERVIEW_DECK_APPROVAL_REQUIRED")
        for contract_id in session.interview_asset_contract_ids:
            contract = self.interview_contract_service.repository.contracts.get(contract_id)
            if contract is None:
                missing.append("INTERVIEW_CONTRACT_REQUIRED")
            elif contract.status not in {InterviewContractStatus.approved, InterviewContractStatus.bound_to_session}:
                missing.append("INTERVIEW_CONTRACT_APPROVAL_REQUIRED")
        if self.source_service.repository.get_configuration(session.expression_session_id) is None:
            missing.append("RECORDING_CONFIGURATION_REQUIRED")
        if session.recording_configuration.quality_gate_required and not session.pre_session_quality_gate.passed:
            missing.append("PRE_SESSION_QUALITY_GATE_REQUIRED")
        return list(dict.fromkeys(missing))

    def _blocked_receipt(self, session: CompleteExpressionSession, missing: list[str], actor_id: UUID, command_id: UUID | None) -> None:
        self.repository.put_receipt(
            new_session_start_receipt(
                session=session,
                decision_code="SESSION_READINESS_BLOCKED",
                missing_requirements=missing,
                command_id=command_id,
                reviewer_actor_id=actor_id,
            )
        )

    def _transition(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        expression_session_id: UUID,
        actor_id: UUID,
        to_status: ExpressionSessionStatus,
        allowed_from: set[ExpressionSessionStatus],
        reason: str,
        decision_code: str,
        command_id: UUID | None,
    ) -> CompleteExpressionSession:
        session = self._session_for_brand(organization_id, brand_id, expression_session_id)
        if session.status not in allowed_from:
            raise CompleteExpressionSessionServiceError("INVALID_SESSION_STATUS_TRANSITION", f"Cannot move from {session.status.value} to {to_status.value}.")
        updated = session.model_copy(update={"status": to_status, "updated_at": utc_now()})
        self.repository.put_session(updated)
        self.repository.put_status_event(
            new_session_status_event(
                organization_id=organization_id,
                brand_id=brand_id,
                expression_session_id=expression_session_id,
                from_status=session.status,
                to_status=to_status,
                reason=reason,
                actor_id=actor_id,
                command_id=command_id,
            )
        )
        self.repository.put_receipt(
            new_session_start_receipt(
                session=updated,
                decision_code=decision_code,
                command_id=command_id,
                reviewer_actor_id=actor_id,
            )
        )
        return updated


@dataclass
class CompleteExpressionSessionCommandHandler:
    command_type: str
    service: CompleteExpressionSessionService
    aggregate_type: str = "complete_expression_session"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateCompleteExpressionSessionCommand":
            return self.service.create_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_id=UUID(payload["guest_or_client_id"]),
                operator_id=UUID(payload["operator_id"]),
                interview_deck_id=UUID(payload["interview_deck_id"]),
                consent_record_version_id=UUID(payload["consent_record_version_id"]),
                conversation_language=payload.get("conversation_language", "en"),
                system_label_language=payload.get("system_label_language", "en"),
                expected_master_source=payload["expected_master_source"],
                backup_route=payload["backup_route"],
                platform_source=payload.get("platform_source"),
                upload_method=payload.get("upload_method", "operator_upload"),
                file_safety_expectations=payload.get("file_safety_expectations", []),
                quality_requirements=payload["quality_requirements"],
                session_mode=payload.get("session_mode", "guided_interview"),
                orientation=payload.get("orientation", "vertical"),
                quality_gate_passed=payload.get("quality_gate_passed", True),
                created_by_actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateExpressionSessionReadinessCommand":
            return self.service.validate_readiness(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "StartCompleteExpressionSessionCommand":
            return self.service.start_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "PauseCompleteExpressionSessionCommand":
            return self.service.pause_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload.get("reason", "Operator paused capture."),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ResumeCompleteExpressionSessionCommand":
            return self.service.resume_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload.get("reason", "Operator resumed capture."),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "FailCompleteExpressionSessionCommand":
            return self.service.fail_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "CloseCompleteExpressionSessionCommand":
            return self.service.close_session(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                expression_session_id=UUID(payload["expression_session_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload.get("reason", "Capture complete."),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise CompleteExpressionSessionServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("expression_session_id") or payload.get("interview_deck_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_complete_expression_session_command_handlers(bus: CommandBus, service: CompleteExpressionSessionService) -> None:
    for command_type in [
        "CreateCompleteExpressionSessionCommand",
        "ValidateExpressionSessionReadinessCommand",
        "StartCompleteExpressionSessionCommand",
        "PauseCompleteExpressionSessionCommand",
        "ResumeCompleteExpressionSessionCommand",
        "FailCompleteExpressionSessionCommand",
        "CloseCompleteExpressionSessionCommand",
    ]:
        bus.register_handler(CompleteExpressionSessionCommandHandler(command_type=command_type, service=service))
