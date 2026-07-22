from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.review_decisions import ReviewDecisionType, ReviewResultState  # noqa: E402
from ccp_studio.contracts.review_state import (  # noqa: E402
    ConsentCompatibilitySnapshot,
    EvidenceCompleteness,
    EvidencePanel,
    EvidencePanelType,
    EvaluationFailureView,
    ReviewEvidenceState,
    TelegramComplexity,
)
from ccp_studio.contracts.voice import (  # noqa: E402
    VoiceBridgeClaimCategory,
    new_repair_hierarchy_proof,
)
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.consent_guard import ConsentGuardService  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.review_decision_service import (  # noqa: E402
    ReviewDecisionError,
    ReviewDecisionService,
    register_review_decision_command_handlers,
)
from ccp_studio.services.voice_boost_eligibility import VoiceBoostEligibilityService  # noqa: E402
from ccp_studio.workflows.review_workflow import ReviewWorkflow  # noqa: E402


def _scope(**overrides):
    values = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": True,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": True,
    }
    values.update(overrides)
    return ConsentScope(**values)


def _panel(panel_type: EvidencePanelType, refs: list[str], completeness: EvidenceCompleteness = EvidenceCompleteness.complete):
    return EvidencePanel(
        panel_type=panel_type,
        object_refs=refs,
        summary=f"{panel_type.value} evidence",
        completeness=completeness,
        blocker_codes=[] if completeness == EvidenceCompleteness.complete else [f"{panel_type.value}_blocked"],
    )


def _review_state(*, failing: bool = False, consent_compatible: bool = True, object_id=None, evaluation_receipt_id=None):
    org_id = uuid4()
    brand_id = uuid4()
    object_id = object_id or uuid4()
    evaluation_receipt_id = evaluation_receipt_id or uuid4()
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
        _panel(EvidencePanelType.preview, ["preview:render-output"]),
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
        telegram_complexity=TelegramComplexity.pwa_required if failing else TelegramComplexity.quick_allowed,
        generated_at=utc_now(),
    )


def _service(state: ReviewEvidenceState, voice_service: VoiceBoostEligibilityService | None = None):
    repo = InMemoryReviewStateRepository()
    repo.put_state(state)
    return ReviewDecisionService(repo, voice_service=voice_service)


def _voice_service(org_id, brand_id, guest_id, actor_id):
    consent = ConsentService()
    guard = ConsentGuardService(consent)
    consent.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(),
        actor_id=actor_id,
        evidence_refs=["consent:voice-boost"],
    )
    return VoiceBoostEligibilityService(guard)


def _repair_proof():
    return new_repair_hierarchy_proof(
        recut_checked=True,
        verbatim_fragment_search_checked=True,
        prior_approved_quote_checked=True,
        human_pickup_request_checked=True,
        evidence_refs=["hierarchy:recut", "hierarchy:fragment", "hierarchy:quote", "hierarchy:pickup"],
    )


def _voice_report(voice_service, state, guest_id, *, blocked=False):
    return voice_service.evaluate(
        organization_id=state.organization_id,
        brand_id=state.brand_id,
        guest_or_client_id=guest_id,
        render_output_id=state.object_id,
        final_video_duration_seconds=60.0,
        requested_duration_seconds=4.0,
        repair_hierarchy=_repair_proof(),
        visual_covering_provided=True,
        visual_covering_ref="broll:paper-cut:bridge-cover",
        claim_categories=[VoiceBridgeClaimCategory.primary_claim if blocked else VoiceBridgeClaimCategory.bridge_context],
        evaluation_receipt_ids=[uuid4()],
        source_evidence_refs=["source:quote:001"],
    )


def test_approval_event_includes_actor_evidence_source_refs_and_evaluation_ids():
    state = _review_state()
    service = _service(state)
    actor_id = uuid4()

    receipt = service.approve_asset(
        review_state_id=state.review_state_id,
        actor_id=actor_id,
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        idempotency_key="approve:one",
    )
    approval = next(iter(service.repository.approval_events.values()))

    assert receipt.result_state == ReviewResultState.approved
    assert approval.reviewer_user_id == actor_id
    assert approval.evidence_state_id == state.review_state_id
    assert approval.evaluation_receipt_ids
    assert any(ref.startswith("source-ref") for ref in approval.source_refs)
    assert service.events[-2].event_type == "AssetApproved"


def test_reject_revision_escalation_and_voice_boost_write_typed_receipts():
    state = _review_state()
    guest_id = uuid4()
    actor_id = uuid4()
    voice_service = _voice_service(state.organization_id, state.brand_id, guest_id, actor_id)
    report = _voice_report(voice_service, state, guest_id)
    service = _service(state, voice_service)

    reject = service.reject_asset(
        review_state_id=state.review_state_id,
        actor_id=actor_id,
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        reason="source truth does not survive review",
        evidence_refs=["source-ref:claim:truth:001"],
        idempotency_key="reject:one",
    )
    revision = service.request_revision(
        review_state_id=state.review_state_id,
        actor_id=actor_id,
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        failure_category="source_truth",
        evidence_refs=["transcript_segment:source-artifact-001"],
        expected_repair="replace unsupported claim with the exact transcript-backed wording",
        idempotency_key="revision:one",
    )
    escalation = service.escalate_manual_review(
        review_state_id=state.review_state_id,
        actor_id=actor_id,
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        reason="needs a second human look before approval",
        idempotency_key="escalate:one",
    )
    voice = service.request_voice_dna_boost(
        review_state_id=state.review_state_id,
        actor_id=actor_id,
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        source_gap_ref="source-gap:bridge:001",
        eligibility_report_id=report.voice_boost_eligibility_report_id,
        structural_repair_reason="small connective bridge after all non-synthetic repair routes failed",
        evidence_refs=["source-gap:bridge:001", "hierarchy:recut"],
        idempotency_key="voice:one",
    )

    assert reject.decision_type == ReviewDecisionType.reject
    assert revision.revision_request_id in service.repository.revision_requests
    assert escalation.result_state == ReviewResultState.ready_for_review
    assert voice.voice_dna_boost_request_id in service.repository.voice_dna_boost_requests
    assert len(service.repository.receipts) == 4


def test_voice_dna_boost_request_fails_with_violated_rule_when_ineligible():
    state = _review_state()
    guest_id = uuid4()
    actor_id = uuid4()
    voice_service = _voice_service(state.organization_id, state.brand_id, guest_id, actor_id)
    report = _voice_report(voice_service, state, guest_id, blocked=True)
    service = _service(state, voice_service)

    with pytest.raises(ReviewDecisionError) as exc:
        service.request_voice_dna_boost(
            review_state_id=state.review_state_id,
            actor_id=actor_id,
            role_ids=["reviewer"],
            object_version_hash="sha256-version",
            source_gap_ref="source-gap:bridge:001",
            eligibility_report_id=report.voice_boost_eligibility_report_id,
            structural_repair_reason="small connective bridge after all non-synthetic repair routes failed",
            evidence_refs=["source-gap:bridge:001"],
            idempotency_key="voice:blocked",
        )

    assert exc.value.code == "VOICE_BRIDGE_CLAIM_RESTRICTED"
    assert service.repository.voice_dna_boost_requests == {}


def test_revision_request_includes_exact_evidence_failure_category_and_repair_target():
    state = _review_state(failing=True)
    service = _service(state)

    receipt = service.request_revision(
        review_state_id=state.review_state_id,
        actor_id=uuid4(),
        role_ids=["production_steward"],
        object_version_hash="sha256-version",
        failure_category="source_truth",
        evidence_refs=state.evaluation_failures[0].evidence_refs,
        expected_repair="replace contradicted caption with transcript-backed source quote",
        idempotency_key="revision:exact",
    )
    request = service.repository.revision_requests[receipt.revision_request_id]

    assert request.failure_category == "source_truth"
    assert request.evidence_refs == state.evaluation_failures[0].evidence_refs
    assert request.expected_repair.startswith("replace contradicted")
    assert receipt.result_state == ReviewResultState.revision_requested


def test_escalation_state_policy_records_blocked_or_ready_state():
    clean = _review_state()
    failing = _review_state(failing=True, consent_compatible=False)
    clean_service = _service(clean)
    failing_service = _service(failing)

    ready = clean_service.escalate_manual_review(
        review_state_id=clean.review_state_id,
        actor_id=uuid4(),
        role_ids=["reviewer"],
        object_version_hash="sha256-clean",
        reason="second reviewer requested",
        idempotency_key="escalate:ready",
    )
    blocked = failing_service.escalate_manual_review(
        review_state_id=failing.review_state_id,
        actor_id=uuid4(),
        role_ids=["reviewer"],
        object_version_hash="sha256-failing",
        reason="conflicting evidence must block approval",
        idempotency_key="escalate:blocked",
    )

    assert ready.result_state == ReviewResultState.ready_for_review
    assert blocked.result_state == ReviewResultState.blocked
    assert "SOURCE_TRUTH_CONTRADICTION" in blocked.blocker_codes
    assert "consent_changed_after_render" in blocked.blocker_codes


def test_review_decision_command_bus_is_idempotent_and_records_receipt_event():
    state = _review_state()
    service = _service(state)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(state.organization_id, state.brand_id)
    register_review_decision_command_handlers(bus, service)
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="ApproveAssetCommand",
        organization_id=state.organization_id,
        brand_id=state.brand_id,
        actor=actor,
        idempotency_key="review-command:approve",
        payload={
            "review_state_id": str(state.review_state_id),
            "object_version_hash": "sha256-version",
            "review_idempotency_key": "approve:command",
        },
    )

    first = bus.submit(envelope)
    second = bus.submit(envelope)

    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["receipt_id"] == second.result_payload["receipt_id"]
    assert any(event.event_type == "ReviewDecisionReceiptRecorded" for event in service.events)


def test_review_workflow_stage13_apply_review_decision_routes_to_service():
    state = _review_state()
    service = _service(state)
    workflow = ReviewWorkflow(revision_service=None, review_decision_service=service)

    receipt = workflow.stage13_apply_review_decision(
        decision_type=ReviewDecisionType.approve,
        review_state_id=state.review_state_id,
        actor_id=uuid4(),
        role_ids=["reviewer"],
        object_version_hash="sha256-version",
        idempotency_key="workflow:approve",
    )

    assert receipt.result_state == ReviewResultState.approved
    assert receipt.receipt_id in service.repository.receipts

