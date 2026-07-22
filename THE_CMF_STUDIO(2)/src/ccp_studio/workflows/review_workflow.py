"""Review workflow adapters for TS-CMF-040."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.approval_gate import ApprovalGateInput, ApprovalPolicyReport
from ccp_studio.contracts.review_state import ReviewEvidenceState
from ccp_studio.contracts.revision import RevisionRequest
from ccp_studio.contracts.review_decisions import ReviewDecisionReceipt, ReviewDecisionType
from ccp_studio.contracts.telegram_review import QuickReviewReceipt, TelegramReviewNotification
from ccp_studio.services.approval_gate_service import ApprovalGateService
from ccp_studio.services.review_decision_service import ReviewDecisionService
from ccp_studio.services.review_state_service import ReviewStateService
from ccp_studio.services.revision_service import RevisionService
from ccp_studio.services.telegram_review_service import TelegramReviewService


@dataclass
class ReviewWorkflow:
    revision_service: RevisionService
    review_state_service: ReviewStateService | None = None
    review_decision_service: ReviewDecisionService | None = None
    approval_gate_service: ApprovalGateService | None = None
    telegram_review_service: TelegramReviewService | None = None

    def stage13_revision_and_reconstruction(
        self,
        *,
        complete_editing_session_id: UUID,
        actor_id: UUID,
        reason: str,
        target_object_type: str,
        target_object_id: UUID,
        deltas: list[dict[str, Any]],
        prior_version_id: UUID,
    ) -> RevisionRequest:
        return self.revision_service.request_scene_revision(
            complete_editing_session_id=complete_editing_session_id,
            requested_by_user_id=actor_id,
            reason=reason,
            target_object_type=target_object_type,
            target_object_id=target_object_id,
            deltas=deltas,
            prior_version_id=prior_version_id,
        )

    def stage13_build_evidence_state(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        approval_evidence_view_id: UUID,
        actor_id: UUID,
        preview_ref: str | None = None,
        source_quote_ref: str | None = None,
        archetype_route_ref: str | None = None,
        brand_context_version_id: UUID | None = None,
        selected_asset_refs: list[str] | None = None,
        render_output_refs: list[str] | None = None,
        rendered_with_consent_record_version_id: UUID | None = None,
        telegram_complexity_score: int = 0,
        surface_route: str | None = None,
    ) -> ReviewEvidenceState:
        if self.review_state_service is None:
            raise RuntimeError("ReviewStateService is required for evidence-rich review state.")
        return self.review_state_service.stage13_build_evidence_state(
            organization_id=organization_id,
            brand_id=brand_id,
            approval_evidence_view_id=approval_evidence_view_id,
            actor_id=actor_id,
            preview_ref=preview_ref,
            source_quote_ref=source_quote_ref,
            archetype_route_ref=archetype_route_ref,
            brand_context_version_id=brand_context_version_id,
            selected_asset_refs=selected_asset_refs,
            render_output_refs=render_output_refs,
            rendered_with_consent_record_version_id=rendered_with_consent_record_version_id,
            telegram_complexity_score=telegram_complexity_score,
            surface_route=surface_route,
        )

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
        if self.review_decision_service is None:
            raise RuntimeError("ReviewDecisionService is required for review decisions.")
        return self.review_decision_service.stage13_apply_review_decision(
            decision_type=decision_type,
            review_state_id=review_state_id,
            actor_id=actor_id,
            role_ids=role_ids,
            object_version_hash=object_version_hash,
            idempotency_key=idempotency_key,
            **kwargs,
        )

    def stage13_approval_gate(self, gate_input: ApprovalGateInput | dict[str, Any]) -> ApprovalPolicyReport:
        if self.approval_gate_service is None:
            raise RuntimeError("ApprovalGateService is required for approval blockers.")
        return self.approval_gate_service.stage13_approval_gate(gate_input)

    def stage13_telegram_quick_review(self, **kwargs: Any) -> TelegramReviewNotification | QuickReviewReceipt:
        if self.telegram_review_service is None:
            raise RuntimeError("TelegramReviewService is required for Telegram quick review.")
        return self.telegram_review_service.stage13_telegram_quick_review(**kwargs)
