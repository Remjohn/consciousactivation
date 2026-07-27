"""Telegram quick review service for TS-CMF-055."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.approval_gate import ApprovalGateDecision
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandEnvelope, CommandResult, CommandStatus, new_command_envelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.review_state import EvidenceCompleteness, EvidencePanelType, ReviewEvidenceState, TelegramComplexity
from ccp_studio.contracts.surfaces import DeepLinkTarget
from ccp_studio.contracts.telegram_review import (
    EvidenceSufficiencyDecision,
    QuickActionToken,
    QuickReviewReceipt,
    TelegramQuickActionType,
    TelegramQuickReviewResultCode,
    TelegramReviewDomainEvent,
    TelegramReviewNotification,
    new_quick_review_receipt,
)
from ccp_studio.repositories.approval_gate import InMemoryApprovalGateRepository
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository
from ccp_studio.repositories.telegram_review import InMemoryTelegramReviewRepository
from ccp_studio.services.command_bus import CommandBus


TELEGRAM_REVIEW_ROLES = {"owner", "admin", "reviewer", "production_steward"}


class TelegramReviewError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class TelegramReviewService:
    review_state_repository: InMemoryReviewStateRepository
    command_bus: CommandBus
    approval_gate_repository: InMemoryApprovalGateRepository | None = None
    repository: InMemoryTelegramReviewRepository = field(default_factory=InMemoryTelegramReviewRepository)
    token_ttl_minutes: int = 30

    def evaluate_evidence_sufficiency(
        self,
        *,
        review_state_id: UUID,
        approval_policy_report_id: UUID | None = None,
    ) -> EvidenceSufficiencyDecision:
        state = self._state(review_state_id)
        reasons: list[str] = []
        if state.telegram_complexity != TelegramComplexity.quick_allowed:
            reasons.append("telegram_complexity_pwa_required")
        if not state.consent_snapshot.compatible:
            reasons.extend(state.consent_snapshot.blocker_codes or ["consent_incompatible"])
        reasons.extend(failure.failure_code for failure in state.evaluation_failures)
        for panel in state.panels:
            if panel.completeness != EvidenceCompleteness.complete:
                reasons.extend(panel.blocker_codes or [f"{panel.panel_type.value}_{panel.completeness.value}"])
        reasons.extend(self._approval_gate_reasons(state, approval_policy_report_id))
        quick_allowed = not reasons
        decision = EvidenceSufficiencyDecision(
            schema_version="cmf.telegram_evidence_sufficiency_decision.v1",
            decision_id=uuid4(),
            object_id=state.object_id,
            quick_actions_allowed=quick_allowed,
            required_pwa_review=not quick_allowed,
            reasons=sorted(set(reasons)) if reasons else ["evidence_sufficient_for_quick_review"],
            review_state_id=state.review_state_id,
            approval_policy_report_id=approval_policy_report_id,
            created_at=utc_now(),
        )
        self.repository.put_decision(decision)
        self._event("TelegramEvidenceSufficiencyEvaluated", state, decision.model_dump(mode="json"))
        return decision

    def send_review_notification(
        self,
        *,
        review_state_id: UUID,
        user_id: UUID,
        object_version_hash: str,
        approval_policy_report_id: UUID | None = None,
    ) -> TelegramReviewNotification:
        state = self._state(review_state_id)
        decision = self.evaluate_evidence_sufficiency(
            review_state_id=review_state_id,
            approval_policy_report_id=approval_policy_report_id,
        )
        allowed_actions = [TelegramQuickActionType.open_pwa_review]
        if decision.quick_actions_allowed:
            allowed_actions = [
                TelegramQuickActionType.approve,
                TelegramQuickActionType.reject,
                TelegramQuickActionType.request_revision,
                TelegramQuickActionType.open_pwa_review,
            ]
        token = self.repository.put_token(
            QuickActionToken(
                schema_version="cmf.quick_action_token.v1",
                token_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                user_id=user_id,
                object_type=state.object_type,
                object_id=state.object_id,
                object_version_hash=object_version_hash,
                allowed_actions=allowed_actions,
                evidence_sufficiency_decision_id=decision.decision_id,
                approval_policy_report_id=approval_policy_report_id,
                expires_at=utc_now() + timedelta(minutes=self.token_ttl_minutes),
                idempotency_key=f"telegram-review:{state.review_state_id}:{object_version_hash}:{uuid4()}",
                issued_at=utc_now(),
            )
        )
        notification = self.repository.put_notification(
            TelegramReviewNotification(
                schema_version="cmf.telegram_review_notification.v1",
                notification_id=uuid4(),
                organization_id=state.organization_id,
                brand_id=state.brand_id,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                preview_uri=self._first_panel_ref(state, EvidencePanelType.preview, "preview:unavailable"),
                route_summary=self._panel_summary(state, EvidencePanelType.archetype_route, "Route evidence required."),
                source_snippet=self._first_panel_ref(state, EvidencePanelType.source_quote, "source:missing"),
                consent_status=self._consent_summary(state),
                evaluation_summary=self._evaluation_summary(state),
                required_action="quick_review_available" if decision.quick_actions_allowed else "open_pwa_review_required",
                pwa_review_url=self._pwa_link(state).route,
                quick_action_token_id=token.token_id,
                quick_actions=allowed_actions,
                evidence_sufficiency_decision_id=decision.decision_id,
                sent_at=utc_now(),
            )
        )
        self._event(
            "TelegramReviewNotificationSent",
            state,
            {
                "notification_id": str(notification.notification_id),
                "token_id": str(token.token_id),
                "quick_actions": [action.value for action in allowed_actions],
            },
        )
        return notification

    def submit_quick_action(
        self,
        *,
        token_id: UUID,
        user_id: UUID,
        action_type: TelegramQuickActionType | str,
        object_version_hash: str,
        role_ids: list[str],
        payload: dict[str, Any] | None = None,
        action_idempotency_key: str | None = None,
    ) -> QuickReviewReceipt:
        token_id = UUID(str(token_id))
        action = TelegramQuickActionType(action_type)
        token = self._token(token_id)
        idempotency_key = action_idempotency_key or f"{token.idempotency_key}:{action.value}:{user_id}:{object_version_hash}"
        prior = self.repository.receipt_for_idempotency(
            token_id=token_id,
            action_type=action,
            idempotency_key=idempotency_key,
        )
        if prior:
            return prior
        state = self._state(token.review_state_id)
        decision = self.repository.decisions.get(token.evidence_sufficiency_decision_id)
        if decision is None:
            decision = self.evaluate_evidence_sufficiency(
                review_state_id=token.review_state_id,
                approval_policy_report_id=token.approval_policy_report_id,
            )
        invalid_receipt = self._invalid_action_receipt(
            token=token,
            state=state,
            actor_id=user_id,
            action=action,
            object_version_hash=object_version_hash,
            role_ids=role_ids,
            decision=decision,
        )
        if invalid_receipt is not None:
            return self.repository.put_receipt(invalid_receipt, idempotency_key=idempotency_key)
        if action == TelegramQuickActionType.open_pwa_review or not decision.quick_actions_allowed:
            receipt = self._receipt(
                token=token,
                state=state,
                actor_id=user_id,
                action=action,
                object_version_hash=object_version_hash,
                decision=decision,
                result_code=TelegramQuickReviewResultCode.pwa_handoff_required,
                pwa_handoff_required=True,
                blocker_codes=decision.reasons if not decision.quick_actions_allowed else [],
            )
            self._event("PwaReviewDeepLinkIssued", state, {"receipt_id": str(receipt.quick_review_receipt_id)})
            return self.repository.put_receipt(receipt, idempotency_key=idempotency_key)
        command = self._command_for_action(
            token=token,
            actor_id=user_id,
            role_ids=role_ids,
            action=action,
            object_version_hash=object_version_hash,
            payload=payload or {},
            idempotency_key=idempotency_key,
        )
        result = self.command_bus.submit(command)
        result_code = self._result_code(result)
        review_receipt_id = self._uuid_or_none(result.result_payload.get("receipt_id"))
        receipt = self._receipt(
            token=token,
            state=state,
            actor_id=user_id,
            action=action,
            object_version_hash=object_version_hash,
            decision=decision,
            result_code=result_code,
            command_id=result.command_id,
            command_status=result.status.value,
            command_receipt_id=result.audit_receipt_id,
            review_decision_receipt_id=review_receipt_id,
            blocker_codes=self._result_blockers(result),
        )
        self._event(
            "TelegramQuickActionSubmitted",
            state,
            {
                "action_type": action.value,
                "command_id": str(result.command_id),
                "command_status": result.status.value,
                "quick_review_receipt_id": str(receipt.quick_review_receipt_id),
            },
        )
        if action == TelegramQuickActionType.request_revision and result.status in {CommandStatus.succeeded, CommandStatus.replayed}:
            self._event("TelegramRevisionRequested", state, {"receipt_id": str(receipt.quick_review_receipt_id)})
        return self.repository.put_receipt(receipt, idempotency_key=idempotency_key)

    def reject_stale_action(
        self,
        *,
        token_id: UUID,
        user_id: UUID,
        action_type: TelegramQuickActionType | str,
        submitted_object_version_hash: str,
    ) -> QuickReviewReceipt:
        token = self._token(token_id)
        state = self._state(token.review_state_id)
        decision = self.repository.decisions.get(token.evidence_sufficiency_decision_id)
        receipt = self._receipt(
            token=token,
            state=state,
            actor_id=user_id,
            action=TelegramQuickActionType(action_type),
            object_version_hash=submitted_object_version_hash,
            decision=decision,
            result_code=TelegramQuickReviewResultCode.stale_action_rejected,
            pwa_handoff_required=True,
            blocker_codes=["object_version_hash_mismatch"],
        )
        self._event("StaleTelegramActionRejected", state, {"receipt_id": str(receipt.quick_review_receipt_id)})
        return self.repository.put_receipt(receipt)

    def stage13_telegram_quick_review(self, **kwargs: Any) -> TelegramReviewNotification | QuickReviewReceipt:
        if "token_id" in kwargs:
            return self.submit_quick_action(**kwargs)
        return self.send_review_notification(**kwargs)

    def stage14_telegram_confirmation_handoff(self, **kwargs: Any) -> QuickReviewReceipt:
        return self.submit_quick_action(action_type=TelegramQuickActionType.open_pwa_review, **kwargs)

    def _command_for_action(
        self,
        *,
        token: QuickActionToken,
        actor_id: UUID,
        role_ids: list[str],
        action: TelegramQuickActionType,
        object_version_hash: str,
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> CommandEnvelope:
        command_type = {
            TelegramQuickActionType.approve: "ApproveAssetCommand",
            TelegramQuickActionType.reject: "RejectAssetCommand",
            TelegramQuickActionType.request_revision: "RequestRevisionCommand",
        }[action]
        command_payload: dict[str, Any] = {
            "review_state_id": str(token.review_state_id),
            "object_version_hash": object_version_hash,
            "review_idempotency_key": idempotency_key,
        }
        if token.approval_policy_report_id:
            command_payload["approval_policy_report_id"] = str(token.approval_policy_report_id)
        if action == TelegramQuickActionType.reject:
            command_payload["reason"] = payload.get("reason", "Rejected from Telegram quick review with evidence.")
            command_payload["evidence_refs"] = payload.get("evidence_refs") or self._evidence_refs(self._state(token.review_state_id))
        if action == TelegramQuickActionType.request_revision:
            state = self._state(token.review_state_id)
            first_failure = state.evaluation_failures[0] if state.evaluation_failures else None
            command_payload["failure_category"] = payload.get("failure_category") or (first_failure.category if first_failure else "telegram_quick_review")
            command_payload["evidence_refs"] = payload.get("evidence_refs") or (first_failure.evidence_refs if first_failure else self._evidence_refs(state))
            command_payload["expected_repair"] = payload.get("expected_repair") or "regenerate through revision workflow using the cited review evidence"
        return new_command_envelope(
            command_type=command_type,
            organization_id=token.organization_id,
            brand_id=token.brand_id,
            actor=ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=role_ids),
            payload=command_payload,
            source_surface="telegram_bot",
            idempotency_key=idempotency_key,
        )

    def _invalid_action_receipt(
        self,
        *,
        token: QuickActionToken,
        state: ReviewEvidenceState,
        actor_id: UUID,
        action: TelegramQuickActionType,
        object_version_hash: str,
        role_ids: list[str],
        decision: EvidenceSufficiencyDecision,
    ) -> QuickReviewReceipt | None:
        result_code: TelegramQuickReviewResultCode | None = None
        blockers: list[str] = []
        if token.revoked_at is not None:
            result_code = TelegramQuickReviewResultCode.tamper_rejected
            blockers.append("quick_action_token_revoked")
        elif token.expires_at <= utc_now():
            result_code = TelegramQuickReviewResultCode.token_expired
            blockers.append("quick_action_token_expired")
        elif token.user_id != actor_id:
            result_code = TelegramQuickReviewResultCode.tamper_rejected
            blockers.append("quick_action_actor_mismatch")
        elif not set(role_ids).intersection(TELEGRAM_REVIEW_ROLES):
            result_code = TelegramQuickReviewResultCode.tamper_rejected
            blockers.append("ROLE_PERMISSION_DENIED")
        elif action not in token.allowed_actions:
            result_code = TelegramQuickReviewResultCode.action_not_allowed
            blockers.append("quick_action_not_allowed")
        elif token.object_version_hash != object_version_hash:
            result_code = TelegramQuickReviewResultCode.stale_action_rejected
            blockers.append("object_version_hash_mismatch")
        if result_code is None:
            return None
        receipt = self._receipt(
            token=token,
            state=state,
            actor_id=actor_id,
            action=action,
            object_version_hash=object_version_hash,
            decision=decision,
            result_code=result_code,
            pwa_handoff_required=True,
            blocker_codes=blockers,
        )
        self._event("StaleTelegramActionRejected" if result_code == TelegramQuickReviewResultCode.stale_action_rejected else "TelegramQuickActionRejected", state, {"result_code": result_code.value, "blocker_codes": blockers})
        return receipt

    def _receipt(
        self,
        *,
        token: QuickActionToken,
        state: ReviewEvidenceState,
        actor_id: UUID,
        action: TelegramQuickActionType,
        object_version_hash: str,
        decision: EvidenceSufficiencyDecision | None,
        result_code: TelegramQuickReviewResultCode,
        command_id: UUID | None = None,
        command_status: str | None = None,
        command_receipt_id: UUID | None = None,
        review_decision_receipt_id: UUID | None = None,
        pwa_handoff_required: bool = False,
        blocker_codes: list[str] | None = None,
    ) -> QuickReviewReceipt:
        notification_id = self.repository.token_notification_index.get(token.token_id)
        return new_quick_review_receipt(
            notification_id=notification_id,
            token_id=token.token_id,
            actor_id=actor_id,
            organization_id=state.organization_id,
            brand_id=state.brand_id,
            review_state_id=state.review_state_id,
            object_type=state.object_type,
            object_id=state.object_id,
            object_version_hash=object_version_hash,
            action_type=action,
            evidence_sufficiency_decision_id=decision.decision_id if decision else None,
            quick_actions_allowed=decision.quick_actions_allowed if decision else False,
            result_code=result_code,
            command_id=command_id,
            command_status=command_status,
            command_receipt_id=command_receipt_id,
            review_decision_receipt_id=review_decision_receipt_id,
            pwa_handoff_required=pwa_handoff_required,
            pwa_deep_link=self._pwa_link(state) if pwa_handoff_required else None,
            blocker_codes=blocker_codes or [],
            evidence_refs=self._evidence_refs(state),
        )

    def _approval_gate_reasons(self, state: ReviewEvidenceState, approval_policy_report_id: UUID | None) -> list[str]:
        if approval_policy_report_id is None:
            return []
        if self.approval_gate_repository is None:
            return ["approval_gate_repository_required"]
        report = self.approval_gate_repository.reports.get(approval_policy_report_id)
        if report is None:
            return ["approval_policy_report_required"]
        if report.organization_id != state.organization_id or report.brand_id != state.brand_id or report.object_id != state.object_id:
            return ["approval_policy_report_scope_mismatch"]
        if report.decision == ApprovalGateDecision.approved_allowed:
            return []
        return [blocker.code for blocker in report.blockers] or [report.decision.value]

    @staticmethod
    def _result_code(result: CommandResult) -> TelegramQuickReviewResultCode:
        if result.status in {CommandStatus.succeeded, CommandStatus.replayed}:
            return TelegramQuickReviewResultCode.quick_action_succeeded
        if result.status == CommandStatus.rejected:
            return TelegramQuickReviewResultCode.command_rejected
        return TelegramQuickReviewResultCode.command_failed

    @staticmethod
    def _result_blockers(result: CommandResult) -> list[str]:
        blockers = [item.code for item in result.validation_results if not item.passed]
        payload_blockers = result.result_payload.get("blocker_codes")
        if isinstance(payload_blockers, list):
            blockers.extend(str(item) for item in payload_blockers)
        return sorted(set(blockers))

    @staticmethod
    def _uuid_or_none(value: Any) -> UUID | None:
        if value is None:
            return None
        try:
            return UUID(str(value))
        except ValueError:
            return None

    @staticmethod
    def _panel_summary(state: ReviewEvidenceState, panel_type: EvidencePanelType, fallback: str) -> str:
        panel = next((item for item in state.panels if item.panel_type == panel_type), None)
        return panel.summary if panel else fallback

    @staticmethod
    def _first_panel_ref(state: ReviewEvidenceState, panel_type: EvidencePanelType, fallback: str) -> str:
        panel = next((item for item in state.panels if item.panel_type == panel_type), None)
        if panel and panel.object_refs:
            return panel.object_refs[0]
        return fallback

    @staticmethod
    def _consent_summary(state: ReviewEvidenceState) -> str:
        compatible = "compatible" if state.consent_snapshot.compatible else "blocked"
        return f"{state.consent_snapshot.status}:{compatible}"

    @staticmethod
    def _evaluation_summary(state: ReviewEvidenceState) -> str:
        if not state.evaluation_failures:
            return "evaluation_passed"
        codes = ", ".join(failure.failure_code for failure in state.evaluation_failures)
        return f"evaluation_hard_failures:{codes}"

    @staticmethod
    def _evidence_refs(state: ReviewEvidenceState) -> list[str]:
        refs = [str(state.review_state_id), str(state.approval_evidence_view_id)]
        for panel in state.panels:
            refs.extend(panel.object_refs)
        refs.extend(ref for failure in state.evaluation_failures for ref in failure.evidence_refs)
        return refs

    def _pwa_link(self, state: ReviewEvidenceState) -> DeepLinkTarget:
        if state.pwa_deep_link is not None:
            return state.pwa_deep_link
        return DeepLinkTarget(
            schema_version="cmf.deep_link_target.v1",
            target_surface="pwa",
            route=state.pwa_route,
            object_type=state.object_type,
            object_id=state.object_id,
            brand_id=state.brand_id,
            required_reason="PWA_REVIEW_REQUIRED",
        )

    def _state(self, review_state_id: UUID) -> ReviewEvidenceState:
        state = self.review_state_repository.states.get(review_state_id)
        if state is None:
            raise TelegramReviewError("REVIEW_STATE_REQUIRED", "Review evidence state is required.")
        return state

    def _token(self, token_id: UUID) -> QuickActionToken:
        token = self.repository.tokens.get(token_id)
        if token is None:
            raise TelegramReviewError("QUICK_ACTION_TOKEN_REQUIRED", "Quick action token is required.")
        return token

    def _event(self, event_type: str, state: ReviewEvidenceState, payload: dict[str, Any]) -> TelegramReviewDomainEvent:
        return self.repository.append_event(
            TelegramReviewDomainEvent(
                schema_version="cmf.telegram_review_domain_event.v1",
                telegram_review_event_id=uuid4(),
                event_type=event_type,
                review_state_id=state.review_state_id,
                object_type=state.object_type,
                object_id=state.object_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class TelegramReviewCommandHandler:
    command_type: str
    service: TelegramReviewService
    aggregate_type: str = "telegram_review"
    allowed_roles: set[str] = field(default_factory=lambda: TELEGRAM_REVIEW_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "SendTelegramReviewNotificationCommand":
            return self.service.send_review_notification(
                review_state_id=UUID(payload["review_state_id"]),
                user_id=envelope.actor.actor_id,
                object_version_hash=payload["object_version_hash"],
                approval_policy_report_id=UUID(payload["approval_policy_report_id"]) if payload.get("approval_policy_report_id") else None,
            ).model_dump(mode="json")
        if self.command_type == "EvaluateTelegramEvidenceSufficiencyCommand":
            return self.service.evaluate_evidence_sufficiency(
                review_state_id=UUID(payload["review_state_id"]),
                approval_policy_report_id=UUID(payload["approval_policy_report_id"]) if payload.get("approval_policy_report_id") else None,
            ).model_dump(mode="json")
        if self.command_type in {"SubmitTelegramQuickActionCommand", "DeepLinkToPwaReviewCommand", "CreateRevisionFromTelegramRegenerateCommand"}:
            action = payload.get("action_type")
            if self.command_type == "DeepLinkToPwaReviewCommand":
                action = TelegramQuickActionType.open_pwa_review.value
            if self.command_type == "CreateRevisionFromTelegramRegenerateCommand":
                action = TelegramQuickActionType.request_revision.value
            return self.service.submit_quick_action(
                token_id=UUID(payload["token_id"]),
                user_id=envelope.actor.actor_id,
                action_type=action,
                object_version_hash=payload["object_version_hash"],
                role_ids=envelope.actor.role_ids,
                payload=payload.get("payload", {}),
                action_idempotency_key=payload.get("action_idempotency_key", envelope.idempotency_key),
            ).model_dump(mode="json")
        if self.command_type == "RejectStaleTelegramActionCommand":
            return self.service.reject_stale_action(
                token_id=UUID(payload["token_id"]),
                user_id=envelope.actor.actor_id,
                action_type=payload["action_type"],
                submitted_object_version_hash=payload["object_version_hash"],
            ).model_dump(mode="json")
        raise TelegramReviewError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("token_id") or payload.get("review_state_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_telegram_review_command_handlers(bus: CommandBus, service: TelegramReviewService) -> None:
    for command_type in [
        "SendTelegramReviewNotificationCommand",
        "EvaluateTelegramEvidenceSufficiencyCommand",
        "SubmitTelegramQuickActionCommand",
        "DeepLinkToPwaReviewCommand",
        "RejectStaleTelegramActionCommand",
        "CreateRevisionFromTelegramRegenerateCommand",
    ]:
        bus.register_handler(TelegramReviewCommandHandler(command_type=command_type, service=service))
