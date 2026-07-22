from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.review_decisions import ReviewResultState  # noqa: E402
from ccp_studio.contracts.review_state import (  # noqa: E402
    ConsentCompatibilitySnapshot,
    EvidenceCompleteness,
    EvidencePanel,
    EvidencePanelType,
    EvaluationFailureView,
    ReviewEvidenceState,
    TelegramComplexity,
)
from ccp_studio.contracts.telegram_review import TelegramQuickActionType, TelegramQuickReviewResultCode  # noqa: E402
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.review_decision_service import ReviewDecisionService, register_review_decision_command_handlers  # noqa: E402
from ccp_studio.services.telegram_review_service import TelegramReviewService, register_telegram_review_command_handlers  # noqa: E402
from ccp_studio.workflows.publishing_workflow import PublishingWorkflow  # noqa: E402
from ccp_studio.workflows.review_workflow import ReviewWorkflow  # noqa: E402


def _panel(panel_type: EvidencePanelType, refs: list[str], completeness: EvidenceCompleteness = EvidenceCompleteness.complete):
    return EvidencePanel(
        panel_type=panel_type,
        object_refs=refs,
        summary=f"{panel_type.value} evidence",
        completeness=completeness,
        blocker_codes=[] if completeness == EvidenceCompleteness.complete else [f"{panel_type.value}_blocked"],
    )


def _review_state(*, failing: bool = False, consent_compatible: bool = True):
    org_id = uuid4()
    brand_id = uuid4()
    object_id = uuid4()
    evaluation_receipt_id = uuid4()
    failures = [
        EvaluationFailureView(
            evaluation_receipt_id=evaluation_receipt_id,
            category="source_truth",
            failure_code="SOURCE_TRUTH_CONTRADICTION",
            evidence_refs=["transcript_segment:source-artifact-001:segment:truth:001:9000-14000ms"],
            repair_recommendation="repair_source_truth",
        )
    ] if failing else []
    panels = [
        _panel(EvidencePanelType.preview, ["preview://render-output.jpg"]),
        _panel(EvidencePanelType.source_quote, ["source-ref:claim:truth:001"]),
        _panel(EvidencePanelType.transcript, ["transcript:v1:hash"]),
        _panel(EvidencePanelType.archetype_route, ["route:public-idea-asset"]),
        _panel(EvidencePanelType.brand_context, [str(uuid4())]),
        _panel(EvidencePanelType.selected_assets, ["asset:selected:plate"]),
        _panel(EvidencePanelType.render_output, ["render:sha256-output"]),
        _panel(
            EvidencePanelType.evaluation,
            [str(evaluation_receipt_id)],
            EvidenceCompleteness.conflicting if failing else EvidenceCompleteness.complete,
        ),
        _panel(EvidencePanelType.revision_history, ["revision_history:none"]),
        _panel(
            EvidencePanelType.consent_state,
            [str(uuid4())],
            EvidenceCompleteness.complete if consent_compatible else EvidenceCompleteness.conflicting,
        ),
    ]
    snapshot = ConsentCompatibilitySnapshot(
        schema_version="cmf.consent_compatibility_snapshot.v1",
        consent_record_version_id=uuid4(),
        status="active" if consent_compatible else "revoked",
        compatible=consent_compatible,
        changed_after_render=not consent_compatible,
        blocker_codes=[] if consent_compatible else ["consent_changed_after_render"],
    )
    return ReviewEvidenceState(
        schema_version="cmf.review_evidence_state.v1",
        review_state_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        object_type="render_output",
        object_id=object_id,
        approval_evidence_view_id=uuid4(),
        panels=panels,
        evaluation_failures=failures,
        revision_history=[],
        consent_snapshot=snapshot,
        brand_context_version_id=uuid4(),
        selected_asset_refs=["asset:selected:plate"],
        render_output_refs=["render:sha256-output"],
        pwa_route=f"/brands/{brand_id}/review/render_output/{object_id}",
        telegram_complexity=TelegramComplexity.pwa_required if failing or not consent_compatible else TelegramComplexity.quick_allowed,
        generated_at=utc_now(),
    )


def _service(state: ReviewEvidenceState):
    repo = InMemoryReviewStateRepository()
    repo.put_state(state)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(state.organization_id, state.brand_id)
    review_decisions = ReviewDecisionService(repo)
    register_review_decision_command_handlers(bus, review_decisions)
    telegram = TelegramReviewService(repo, bus)
    return telegram, review_decisions, bus


def test_notification_includes_preview_route_source_consent_evaluation_and_required_action():
    state = _review_state()
    service, _, _ = _service(state)
    reviewer_id = uuid4()

    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    assert notification.preview_uri == "preview://render-output.jpg"
    assert notification.route_summary == "archetype_route evidence"
    assert notification.source_snippet == "source-ref:claim:truth:001"
    assert notification.consent_status == "active:compatible"
    assert notification.evaluation_summary == "evaluation_passed"
    assert notification.required_action == "quick_review_available"
    assert TelegramQuickActionType.approve in notification.quick_actions
    assert service.repository.tokens[notification.quick_action_token_id].object_version_hash == "sha256-render-v1"


def test_quick_approve_routes_through_command_bus_and_records_same_review_decision_receipt():
    state = _review_state()
    service, review_decisions, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    receipt = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.approve,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
    )

    assert receipt.result_code == TelegramQuickReviewResultCode.quick_action_succeeded
    assert receipt.command_id is not None
    assert receipt.command_receipt_id is not None
    assert receipt.review_decision_receipt_id in review_decisions.repository.receipts
    decision_receipt = review_decisions.repository.receipts[receipt.review_decision_receipt_id]
    assert decision_receipt.result_state == ReviewResultState.approved
    assert next(iter(review_decisions.repository.approval_events.values())).evidence_state_id == state.review_state_id


def test_insufficient_or_conflicting_evidence_removes_approval_and_deep_links_to_pwa():
    state = _review_state(failing=True)
    service, review_decisions, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    receipt = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.approve,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
    )

    assert notification.quick_actions == [TelegramQuickActionType.open_pwa_review]
    assert receipt.result_code == TelegramQuickReviewResultCode.action_not_allowed
    assert receipt.pwa_handoff_required is True
    assert receipt.pwa_deep_link.route == state.pwa_route
    assert "quick_action_not_allowed" in receipt.blocker_codes
    assert review_decisions.repository.approval_events == {}


def test_stale_or_tampered_quick_action_is_rejected_by_object_version_and_actor():
    state = _review_state()
    service, _, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    stale = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.reject,
        object_version_hash="sha256-render-v2",
        role_ids=["reviewer"],
        payload={"reason": "old review message"},
    )
    tampered = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=uuid4(),
        action_type=TelegramQuickActionType.reject,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
        payload={"reason": "wrong actor"},
    )

    assert stale.result_code == TelegramQuickReviewResultCode.stale_action_rejected
    assert "object_version_hash_mismatch" in stale.blocker_codes
    assert tampered.result_code == TelegramQuickReviewResultCode.tamper_rejected
    assert "quick_action_actor_mismatch" in tampered.blocker_codes


def test_quick_regenerate_creates_revision_request_and_does_not_mutate_provider_output():
    state = _review_state()
    service, review_decisions, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    receipt = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.request_revision,
        object_version_hash="sha256-render-v1",
        role_ids=["production_steward"],
        payload={
            "failure_category": "caption_timing",
            "evidence_refs": ["caption:cues:0"],
            "expected_repair": "regenerate caption timing through revision workflow only",
        },
    )

    assert receipt.result_code == TelegramQuickReviewResultCode.quick_action_succeeded
    assert len(review_decisions.repository.revision_requests) == 1
    revision = next(iter(review_decisions.repository.revision_requests.values()))
    assert revision.failure_category == "caption_timing"
    assert revision.evidence_refs == ["caption:cues:0"]
    assert review_decisions.repository.approval_events == {}


def test_quick_action_idempotency_replays_same_quick_review_receipt():
    state = _review_state()
    service, _, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )

    first = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.reject,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
        payload={"reason": "source truth issue"},
        action_idempotency_key="telegram:reject:once",
    )
    second = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.reject,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
        payload={"reason": "source truth issue"},
        action_idempotency_key="telegram:reject:once",
    )

    assert first.quick_review_receipt_id == second.quick_review_receipt_id
    assert len(service.repository.receipts) == 1


def test_telegram_command_handler_and_workflow_hooks_route_to_service():
    state = _review_state()
    service, _, bus = _service(state)
    register_telegram_review_command_handlers(bus, service)
    reviewer_id = uuid4()
    actor = ActorContext(actor_id=reviewer_id, actor_type=ActorType.human, role_ids=["reviewer"])
    notification_result = bus.submit(
        new_command_envelope(
            command_type="SendTelegramReviewNotificationCommand",
            organization_id=state.organization_id,
            brand_id=state.brand_id,
            actor=actor,
            idempotency_key="telegram:notify:one",
            source_surface="telegram_bot",
            payload={"review_state_id": str(state.review_state_id), "object_version_hash": "sha256-render-v1"},
        )
    )
    workflow = ReviewWorkflow(revision_service=None, telegram_review_service=service)
    handoff_workflow = PublishingWorkflow(publishing_service=None, telegram_review_service=service)

    assert notification_result.status == CommandStatus.succeeded
    token_id = notification_result.result_payload["quick_action_token_id"]
    receipt = workflow.stage13_telegram_quick_review(
        token_id=token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.open_pwa_review,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
    )
    publishing_handoff = handoff_workflow.stage14_telegram_confirmation_handoff(
        token_id=token_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
    )

    assert receipt.result_code == TelegramQuickReviewResultCode.pwa_handoff_required
    assert publishing_handoff.pwa_deep_link.route == state.pwa_route


def test_expired_token_blocks_quick_action_and_routes_to_pwa():
    state = _review_state()
    service, _, _ = _service(state)
    reviewer_id = uuid4()
    notification = service.send_review_notification(
        review_state_id=state.review_state_id,
        user_id=reviewer_id,
        object_version_hash="sha256-render-v1",
    )
    token = service.repository.tokens[notification.quick_action_token_id]
    service.repository.tokens[token.token_id] = token.model_copy(update={"expires_at": utc_now() - timedelta(minutes=1)})

    receipt = service.submit_quick_action(
        token_id=notification.quick_action_token_id,
        user_id=reviewer_id,
        action_type=TelegramQuickActionType.reject,
        object_version_hash="sha256-render-v1",
        role_ids=["reviewer"],
        payload={"reason": "expired message"},
    )

    assert receipt.result_code == TelegramQuickReviewResultCode.token_expired
    assert receipt.pwa_handoff_required is True
    assert "quick_action_token_expired" in receipt.blocker_codes
