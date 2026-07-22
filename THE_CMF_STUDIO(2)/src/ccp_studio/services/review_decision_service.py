"""Governed review decision service for TS-CMF-052."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.approval_gate import ApprovalGateDecision
from ccp_studio.contracts.review_decisions import (
    ManualEscalation,
    ReviewApprovalEvent,
    ReviewDecision,
    ReviewDecisionDomainEvent,
    ReviewDecisionReceipt,
    ReviewDecisionType,
    ReviewResultState,
    ReviewRevisionRequest,
    VoiceDnaBoostRequest,
    new_review_decision_receipt,
)
from ccp_studio.contracts.review_state import EvidenceCompleteness, ReviewEvidenceState
from ccp_studio.contracts.voice import VoiceEligibilityStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.approval_gate import InMemoryApprovalGateRepository
from ccp_studio.repositories.review_decisions import InMemoryReviewDecisionRepository
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.voice_boost_eligibility import VoiceBoostEligibilityService


ALLOWED_REVIEW_ROLES = {"owner", "admin", "reviewer", "production_steward"}


class ReviewDecisionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ReviewDecisionService:
    review_state_repository: InMemoryReviewStateRepository
    voice_service: VoiceBoostEligibilityService | None = None
    approval_gate_repository: InMemoryApprovalGateRepository | None = None
    repository: InMemoryReviewDecisionRepository = field(default_factory=InMemoryReviewDecisionRepository)
    events: list[ReviewDecisionDomainEvent] = field(default_factory=list)

    def approve_asset(
        self,
        *,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        idempotency_key: str,
        approval_policy_report_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        prior = self._prior(review_state_id, ReviewDecisionType.approve, idempotency_key)
        if prior:
            return prior
        state = self._state(review_state_id)
        self._assert_reviewer_role(role_ids)
        blockers = [*self._approval_blockers(state), *self._approval_gate_blockers(approval_policy_report_id)]
        if blockers:
            return self._blocked_receipt(
                state=state,
                decision_type=ReviewDecisionType.approve,
                object_version_hash=object_version_hash,
                blocker_codes=blockers,
                evidence_refs=self._evidence_refs(state),
                idempotency_key=idempotency_key,
                command_id=command_id,
            )
        approval = self.repository.put_approval_event(
            ReviewApprovalEvent(
                schema_version="cmf.approval_event.v1",
                approval_event_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                object_type=state.object_type,
                object_id=state.object_id,
                reviewer_user_id=actor_id,
                evidence_state_id=state.review_state_id,
                evaluation_receipt_ids=self._evaluation_receipt_ids(state),
                source_refs=self._source_refs(state),
                object_version_hash=object_version_hash,
                created_at=utc_now(),
            )
        )
        decision = self._decision(
            state=state,
            actor_id=actor_id,
            decision_type=ReviewDecisionType.approve,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.approved,
            blocker_codes=[],
        )
        receipt = self.repository.put_receipt(
            new_review_decision_receipt(
                decision_type=ReviewDecisionType.approve,
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                object_version_hash=object_version_hash,
                result_state=ReviewResultState.approved,
                evidence_refs=self._evidence_refs(state),
                command_id=command_id,
                review_decision_id=decision.review_decision_id,
                approval_event_id=approval.approval_event_id,
            ),
            idempotency_key=idempotency_key,
        )
        self._event("AssetApproved", state, {"approval_event_id": str(approval.approval_event_id), "receipt_id": str(receipt.receipt_id)})
        return receipt

    def reject_asset(
        self,
        *,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        reason: str,
        evidence_refs: list[str],
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        prior = self._prior(review_state_id, ReviewDecisionType.reject, idempotency_key)
        if prior:
            return prior
        state = self._state(review_state_id)
        self._assert_reviewer_role(role_ids)
        decision = self._decision(
            state=state,
            actor_id=actor_id,
            decision_type=ReviewDecisionType.reject,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.rejected,
            blocker_codes=[],
            evidence_refs=evidence_refs,
        )
        receipt = self._receipt(
            state=state,
            decision_type=ReviewDecisionType.reject,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.rejected,
            evidence_refs=evidence_refs,
            idempotency_key=idempotency_key,
            command_id=command_id,
            review_decision_id=decision.review_decision_id,
        )
        self._event("AssetRejected", state, {"reason": reason, "receipt_id": str(receipt.receipt_id)})
        return receipt

    def request_revision(
        self,
        *,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        failure_category: str,
        evidence_refs: list[str],
        expected_repair: str,
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        prior = self._prior(review_state_id, ReviewDecisionType.request_revision, idempotency_key)
        if prior:
            return prior
        state = self._state(review_state_id)
        self._assert_reviewer_role(role_ids)
        revision = self.repository.put_revision_request(
            ReviewRevisionRequest(
                schema_version="cmf.review_revision_request.v1",
                revision_request_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                failure_category=failure_category,
                evidence_refs=evidence_refs,
                expected_repair=expected_repair,
                requested_by_user_id=actor_id,
                created_at=utc_now(),
            )
        )
        decision = self._decision(
            state=state,
            actor_id=actor_id,
            decision_type=ReviewDecisionType.request_revision,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.revision_requested,
            blocker_codes=[],
            evidence_refs=evidence_refs,
        )
        receipt = self._receipt(
            state=state,
            decision_type=ReviewDecisionType.request_revision,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.revision_requested,
            evidence_refs=evidence_refs,
            idempotency_key=idempotency_key,
            command_id=command_id,
            review_decision_id=decision.review_decision_id,
            revision_request_id=revision.revision_request_id,
        )
        self._event(
            "RevisionRequested",
            state,
            {"failure_category": failure_category, "expected_repair": expected_repair, "receipt_id": str(receipt.receipt_id)},
        )
        return receipt

    def escalate_manual_review(
        self,
        *,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        reason: str,
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        prior = self._prior(review_state_id, ReviewDecisionType.escalate, idempotency_key)
        if prior:
            return prior
        state = self._state(review_state_id)
        self._assert_reviewer_role(role_ids)
        blockers = self._approval_blockers(state)
        result_state = ReviewResultState.blocked if blockers else ReviewResultState.ready_for_review
        escalation = self.repository.put_manual_escalation(
            ManualEscalation(
                schema_version="cmf.manual_escalation.v1",
                manual_escalation_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                reason=reason,
                result_state=result_state.value,  # type: ignore[arg-type]
                blocker_codes=blockers,
                escalated_by_user_id=actor_id,
                created_at=utc_now(),
            )
        )
        decision = self._decision(
            state=state,
            actor_id=actor_id,
            decision_type=ReviewDecisionType.escalate,
            object_version_hash=object_version_hash,
            result_state=result_state,
            blocker_codes=blockers,
        )
        receipt = self._receipt(
            state=state,
            decision_type=ReviewDecisionType.escalate,
            object_version_hash=object_version_hash,
            result_state=result_state,
            blocker_codes=blockers,
            evidence_refs=self._evidence_refs(state),
            idempotency_key=idempotency_key,
            command_id=command_id,
            review_decision_id=decision.review_decision_id,
            manual_escalation_id=escalation.manual_escalation_id,
        )
        self._event("ManualReviewEscalated", state, {"result_state": result_state.value, "receipt_id": str(receipt.receipt_id)})
        return receipt

    def request_voice_dna_boost(
        self,
        *,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        source_gap_ref: str,
        eligibility_report_id: UUID,
        structural_repair_reason: str,
        evidence_refs: list[str],
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        prior = self._prior(review_state_id, ReviewDecisionType.request_voice_dna_boost, idempotency_key)
        if prior:
            return prior
        state = self._state(review_state_id)
        self._assert_reviewer_role(role_ids)
        report = self._voice_report(eligibility_report_id)
        if report.organization_id != state.organization_id or report.brand_id != state.brand_id or report.render_output_id != state.object_id:
            raise ReviewDecisionError("VOICE_ELIGIBILITY_SCOPE_MISMATCH", "Voice eligibility report must match the review state.")
        if report.status != VoiceEligibilityStatus.eligible:
            violated = report.blocker_codes[0] if report.blocker_codes else "VOICE_BOOST_NOT_ELIGIBLE"
            raise ReviewDecisionError(violated, "Voice-DNA Boost request failed eligibility.")
        request = self.repository.put_voice_dna_boost_request(
            VoiceDnaBoostRequest(
                schema_version="cmf.voice_dna_boost_request.v1",
                request_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_id=state.object_id,
                source_gap_ref=source_gap_ref,
                eligibility_report_id=eligibility_report_id,
                requested_by_user_id=actor_id,
                evidence_refs=evidence_refs,
                structural_repair_reason=structural_repair_reason,
                created_at=utc_now(),
            )
        )
        decision = self._decision(
            state=state,
            actor_id=actor_id,
            decision_type=ReviewDecisionType.request_voice_dna_boost,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.voice_dna_boost_requested,
            blocker_codes=[],
            evidence_refs=evidence_refs,
        )
        receipt = self._receipt(
            state=state,
            decision_type=ReviewDecisionType.request_voice_dna_boost,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.voice_dna_boost_requested,
            evidence_refs=evidence_refs,
            idempotency_key=idempotency_key,
            command_id=command_id,
            review_decision_id=decision.review_decision_id,
            voice_dna_boost_request_id=request.request_id,
        )
        self._event("VoiceDnaBoostRequested", state, {"eligibility_report_id": str(eligibility_report_id), "receipt_id": str(receipt.receipt_id)})
        return receipt

    def stage13_apply_review_decision(
        self,
        *,
        decision_type: ReviewDecisionType | str,
        review_state_id: UUID,
        actor_id: UUID,
        role_ids: list[str],
        object_version_hash: str,
        idempotency_key: str,
        **kwargs: Any,
    ) -> ReviewDecisionReceipt:
        decision = ReviewDecisionType(decision_type)
        if decision == ReviewDecisionType.approve:
            return self.approve_asset(
                review_state_id=review_state_id,
                actor_id=actor_id,
                role_ids=role_ids,
                object_version_hash=object_version_hash,
                idempotency_key=idempotency_key,
                approval_policy_report_id=kwargs.get("approval_policy_report_id"),
            )
        if decision == ReviewDecisionType.reject:
            return self.reject_asset(
                review_state_id=review_state_id,
                actor_id=actor_id,
                role_ids=role_ids,
                object_version_hash=object_version_hash,
                reason=kwargs["reason"],
                evidence_refs=kwargs["evidence_refs"],
                idempotency_key=idempotency_key,
            )
        if decision == ReviewDecisionType.request_revision:
            return self.request_revision(
                review_state_id=review_state_id,
                actor_id=actor_id,
                role_ids=role_ids,
                object_version_hash=object_version_hash,
                failure_category=kwargs["failure_category"],
                evidence_refs=kwargs["evidence_refs"],
                expected_repair=kwargs["expected_repair"],
                idempotency_key=idempotency_key,
            )
        if decision == ReviewDecisionType.escalate:
            return self.escalate_manual_review(
                review_state_id=review_state_id,
                actor_id=actor_id,
                role_ids=role_ids,
                object_version_hash=object_version_hash,
                reason=kwargs["reason"],
                idempotency_key=idempotency_key,
            )
        return self.request_voice_dna_boost(
            review_state_id=review_state_id,
            actor_id=actor_id,
            role_ids=role_ids,
            object_version_hash=object_version_hash,
            source_gap_ref=kwargs["source_gap_ref"],
            eligibility_report_id=kwargs["eligibility_report_id"],
            structural_repair_reason=kwargs["structural_repair_reason"],
            evidence_refs=kwargs["evidence_refs"],
            idempotency_key=idempotency_key,
        )

    def _decision(
        self,
        *,
        state: ReviewEvidenceState,
        actor_id: UUID,
        decision_type: ReviewDecisionType,
        object_version_hash: str,
        result_state: ReviewResultState,
        blocker_codes: list[str],
        evidence_refs: list[str] | None = None,
    ) -> ReviewDecision:
        decision = ReviewDecision(
            schema_version="cmf.review_decision.v1",
            review_decision_id=uuid4(),
            organization_id=state.organization_id,
            brand_id=state.brand_id,
            review_state_id=state.review_state_id,
            object_type=state.object_type,
            object_id=state.object_id,
            reviewer_user_id=actor_id,
            decision_type=decision_type,
            object_version_hash=object_version_hash,
            evidence_refs=evidence_refs or self._evidence_refs(state),
            evaluation_receipt_ids=self._evaluation_receipt_ids(state),
            source_refs=self._source_refs(state),
            result_state=result_state,
            blocker_codes=blocker_codes,
            created_at=utc_now(),
        )
        return self.repository.put_decision(decision)

    def _receipt(
        self,
        *,
        state: ReviewEvidenceState,
        decision_type: ReviewDecisionType,
        object_version_hash: str,
        result_state: ReviewResultState,
        evidence_refs: list[str],
        idempotency_key: str,
        command_id: UUID | None = None,
        blocker_codes: list[str] | None = None,
        review_decision_id: UUID | None = None,
        approval_event_id: UUID | None = None,
        revision_request_id: UUID | None = None,
        manual_escalation_id: UUID | None = None,
        voice_dna_boost_request_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        return self.repository.put_receipt(
            new_review_decision_receipt(
                decision_type=decision_type,
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                object_version_hash=object_version_hash,
                result_state=result_state,
                evidence_refs=evidence_refs,
                blocker_codes=blocker_codes,
                command_id=command_id,
                review_decision_id=review_decision_id,
                approval_event_id=approval_event_id,
                revision_request_id=revision_request_id,
                manual_escalation_id=manual_escalation_id,
                voice_dna_boost_request_id=voice_dna_boost_request_id,
            ),
            idempotency_key=idempotency_key,
        )

    def _blocked_receipt(
        self,
        *,
        state: ReviewEvidenceState,
        decision_type: ReviewDecisionType,
        object_version_hash: str,
        blocker_codes: list[str],
        evidence_refs: list[str],
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> ReviewDecisionReceipt:
        return self._receipt(
            state=state,
            decision_type=decision_type,
            object_version_hash=object_version_hash,
            result_state=ReviewResultState.blocked,
            blocker_codes=blocker_codes,
            evidence_refs=evidence_refs,
            idempotency_key=idempotency_key,
            command_id=command_id,
        )

    def _approval_blockers(self, state: ReviewEvidenceState) -> list[str]:
        blockers: list[str] = []
        if not state.consent_snapshot.compatible:
            blockers.extend(state.consent_snapshot.blocker_codes or ["consent_incompatible"])
        blockers.extend(failure.failure_code for failure in state.evaluation_failures)
        for panel in state.panels:
            if panel.completeness != EvidenceCompleteness.complete:
                blockers.extend(panel.blocker_codes or [f"{panel.panel_type.value}_{panel.completeness.value}"])
        return sorted(set(blockers))

    def _approval_gate_blockers(self, approval_policy_report_id: UUID | None) -> list[str]:
        if approval_policy_report_id is None:
            return []
        if self.approval_gate_repository is None:
            raise ReviewDecisionError("APPROVAL_GATE_REPOSITORY_REQUIRED", "Approval gate repository is required.")
        report = self.approval_gate_repository.reports.get(approval_policy_report_id)
        if report is None:
            raise ReviewDecisionError("APPROVAL_POLICY_REPORT_REQUIRED", "Approval policy report is required.")
        if report.decision == ApprovalGateDecision.approved_allowed:
            return []
        return [blocker.code for blocker in report.blockers] or [report.decision.value]

    @staticmethod
    def _evaluation_receipt_ids(state: ReviewEvidenceState) -> list[UUID]:
        ids: list[UUID] = []
        for panel in state.panels:
            if panel.panel_type.value == "evaluation":
                for ref in panel.object_refs:
                    try:
                        ids.append(UUID(ref))
                    except ValueError:
                        continue
        return ids

    @staticmethod
    def _source_refs(state: ReviewEvidenceState) -> list[str]:
        refs: list[str] = []
        for panel in state.panels:
            if panel.panel_type.value in {"source_quote", "transcript"}:
                refs.extend(panel.object_refs)
        return refs

    @staticmethod
    def _evidence_refs(state: ReviewEvidenceState) -> list[str]:
        refs = [str(state.review_state_id), str(state.approval_evidence_view_id)]
        for panel in state.panels:
            refs.extend(panel.object_refs)
        refs.extend(ref for failure in state.evaluation_failures for ref in failure.evidence_refs)
        return refs

    def _voice_report(self, eligibility_report_id: UUID):
        if self.voice_service is None:
            raise ReviewDecisionError("VOICE_SERVICE_REQUIRED", "Voice eligibility service is required.")
        report = self.voice_service.repository.eligibility_reports.get(eligibility_report_id)
        if report is None:
            raise ReviewDecisionError("VOICE_ELIGIBILITY_REPORT_REQUIRED", "Voice eligibility report is required.")
        return report

    def _state(self, review_state_id: UUID) -> ReviewEvidenceState:
        state = self.review_state_repository.states.get(review_state_id)
        if state is None:
            raise ReviewDecisionError("REVIEW_STATE_REQUIRED", "Review evidence state is required.")
        return state

    @staticmethod
    def _assert_reviewer_role(role_ids: list[str]) -> None:
        if not set(role_ids).intersection(ALLOWED_REVIEW_ROLES):
            raise ReviewDecisionError("ROLE_PERMISSION_DENIED", "Actor lacks a review role.")

    def _prior(
        self,
        review_state_id: UUID,
        decision_type: ReviewDecisionType,
        idempotency_key: str,
    ) -> ReviewDecisionReceipt | None:
        return self.repository.receipt_for_idempotency(review_state_id, decision_type, idempotency_key)

    def _event(self, event_type: str, state: ReviewEvidenceState, payload: dict[str, Any]) -> ReviewDecisionDomainEvent:
        event = ReviewDecisionDomainEvent(
            schema_version="cmf.review_decision_domain_event.v1",
            review_decision_event_id=uuid4(),
            event_type=event_type,
            review_state_id=state.review_state_id,
            object_type=state.object_type,
            object_id=state.object_id,
            payload=payload,
            created_at=utc_now(),
        )
        self.events.append(event)
        self.events.append(
            ReviewDecisionDomainEvent(
                schema_version="cmf.review_decision_domain_event.v1",
                review_decision_event_id=uuid4(),
                event_type="ReviewDecisionReceiptRecorded",
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                payload=payload,
                created_at=utc_now(),
            )
        )
        return event


@dataclass
class ReviewDecisionCommandHandler:
    command_type: str
    service: ReviewDecisionService
    aggregate_type: str = "review_decision"
    allowed_roles: set[str] = field(default_factory=lambda: ALLOWED_REVIEW_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        common = {
            "review_state_id": UUID(payload["review_state_id"]),
            "actor_id": envelope.actor.actor_id,
            "role_ids": envelope.actor.role_ids,
            "object_version_hash": payload["object_version_hash"],
            "idempotency_key": payload.get("review_idempotency_key", envelope.idempotency_key),
            "command_id": envelope.command_id,
        }
        if self.command_type == "ApproveAssetCommand":
            return self.service.approve_asset(
                **common,
                approval_policy_report_id=UUID(payload["approval_policy_report_id"]) if payload.get("approval_policy_report_id") else None,
            ).model_dump(mode="json")
        if self.command_type == "RejectAssetCommand":
            return self.service.reject_asset(
                **common,
                reason=payload["reason"],
                evidence_refs=payload["evidence_refs"],
            ).model_dump(mode="json")
        if self.command_type == "RequestRevisionCommand":
            return self.service.request_revision(
                **common,
                failure_category=payload["failure_category"],
                evidence_refs=payload["evidence_refs"],
                expected_repair=payload["expected_repair"],
            ).model_dump(mode="json")
        if self.command_type == "EscalateManualReviewCommand":
            return self.service.escalate_manual_review(
                **common,
                reason=payload["reason"],
            ).model_dump(mode="json")
        if self.command_type == "RequestVoiceDnaBoostCommand":
            return self.service.request_voice_dna_boost(
                **common,
                source_gap_ref=payload["source_gap_ref"],
                eligibility_report_id=UUID(payload["eligibility_report_id"]),
                structural_repair_reason=payload["structural_repair_reason"],
                evidence_refs=payload["evidence_refs"],
            ).model_dump(mode="json")
        if self.command_type == "RecordReviewDecisionReceiptCommand":
            receipt = self.service.repository.receipts.get(UUID(payload["receipt_id"]))
            if receipt is None:
                raise ReviewDecisionError("REVIEW_DECISION_RECEIPT_REQUIRED", "Review decision receipt is required.")
            return receipt.model_dump(mode="json")
        raise ReviewDecisionError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("receipt_id") or payload.get("review_state_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_review_decision_command_handlers(bus: CommandBus, service: ReviewDecisionService) -> None:
    for command_type in [
        "ApproveAssetCommand",
        "RejectAssetCommand",
        "RequestRevisionCommand",
        "EscalateManualReviewCommand",
        "RequestVoiceDnaBoostCommand",
        "RecordReviewDecisionReceiptCommand",
    ]:
        bus.register_handler(ReviewDecisionCommandHandler(command_type=command_type, service=service))
