from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.approval_gate import ApprovalGateDecision, ApprovalGateInput  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.review_decisions import ReviewResultState  # noqa: E402
from ccp_studio.contracts.review_state import (  # noqa: E402
    ConsentCompatibilitySnapshot,
    EvidenceCompleteness,
    EvidencePanel,
    EvidencePanelType,
    ReviewEvidenceState,
    TelegramComplexity,
)
from ccp_studio.repositories.review_state import InMemoryReviewStateRepository  # noqa: E402
from ccp_studio.services.approval_gate_service import ApprovalGateService, register_approval_gate_command_handlers  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.review_decision_service import ReviewDecisionService  # noqa: E402
from ccp_studio.workflows.review_workflow import ReviewWorkflow  # noqa: E402


def _gate_input(**overrides):
    values = {
        "schema_version": "cmf.approval_gate_input.v1",
        "approval_request_id": uuid4(),
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "review_state_id": uuid4(),
        "object_type": "render_output",
        "object_id": uuid4(),
        "object_version_hash": "sha256-version",
        "lineage_refs": {
            "complete_editing_session_id": str(uuid4()),
            "scene_spec_id": str(uuid4()),
            "provider_receipt_id": str(uuid4()),
            "render_output_ref": "render:sha256-output",
            "archetype_route_receipt_id": str(uuid4()),
        },
        "consent_compatible": True,
        "source_truth_passed": True,
        "identity_passed": True,
        "evaluation_passed": True,
        "evaluation_receipt_ids": [uuid4()],
        "platform_format_passed": True,
        "platform_variant_id": "instagram_reel_9x16",
        "content_format_key": "guest_asset_pack.clip.reel",
        "content_format_registry_version_id": "content-format-registry.v1",
        "valid_content_formats": ["guest_asset_pack.clip.reel", "quote_card.carousel"],
        "evidence_refs": ["review_state:evidence", "evaluation:receipt"],
    }
    values.update(overrides)
    return ApprovalGateInput.model_validate(values)


def _panel(panel_type: EvidencePanelType, refs: list[str]):
    return EvidencePanel(
        panel_type=panel_type,
        object_refs=refs,
        summary=f"{panel_type.value} evidence",
        completeness=EvidenceCompleteness.complete,
        blocker_codes=[],
    )


def _clean_state(gate_input: ApprovalGateInput) -> ReviewEvidenceState:
    evaluation_receipt_id = gate_input.evaluation_receipt_ids[0]
    return ReviewEvidenceState(
        schema_version="cmf.review_evidence_state.v1",
        review_state_id=gate_input.review_state_id,
        organization_id=gate_input.organization_id,
        brand_id=gate_input.brand_id,
        object_type=gate_input.object_type,
        object_id=gate_input.object_id,
        approval_evidence_view_id=uuid4(),
        panels=[
            _panel(EvidencePanelType.preview, ["preview:render-output"]),
            _panel(EvidencePanelType.source_quote, ["source-ref:claim:truth:001"]),
            _panel(EvidencePanelType.transcript, ["transcript:v1:hash"]),
            _panel(EvidencePanelType.archetype_route, ["route:public-idea-asset"]),
            _panel(EvidencePanelType.brand_context, [str(uuid4())]),
            _panel(EvidencePanelType.selected_assets, ["asset:selected:plate"]),
            _panel(EvidencePanelType.render_output, ["render:sha256-output"]),
            _panel(EvidencePanelType.evaluation, [str(evaluation_receipt_id)]),
            _panel(EvidencePanelType.revision_history, ["revision_history:none"]),
            _panel(EvidencePanelType.consent_state, [str(uuid4())]),
        ],
        evaluation_failures=[],
        revision_history=[],
        consent_snapshot=ConsentCompatibilitySnapshot(
            schema_version="cmf.consent_compatibility_snapshot.v1",
            consent_record_version_id=uuid4(),
            status="active",
            compatible=True,
            changed_after_render=False,
            blocker_codes=[],
        ),
        pwa_route=f"/brands/{gate_input.brand_id}/review/render_output/{gate_input.object_id}",
        telegram_complexity=TelegramComplexity.quick_allowed,
        generated_at=utc_now(),
    )


def _decision_service(gate_service: ApprovalGateService, gate_input: ApprovalGateInput) -> ReviewDecisionService:
    state_repo = InMemoryReviewStateRepository()
    state_repo.put_state(_clean_state(gate_input))
    return ReviewDecisionService(
        state_repo,
        approval_gate_repository=gate_service.repository,
    )


def test_incomplete_lineage_blocks_approval_and_names_missing_lineage():
    service = ApprovalGateService()
    gate_input = _gate_input(lineage_refs={"scene_spec_id": str(uuid4())})

    report = service.evaluate_approval_gate(gate_input)
    receipt = next(iter(service.repository.receipts.values()))

    assert report.decision == ApprovalGateDecision.blocked
    assert "LINEAGE_INCOMPLETE" in [blocker.code for blocker in report.blockers]
    assert any("provider_receipt_id" in blocker.message for blocker in report.blockers)
    assert "LINEAGE_INCOMPLETE" in receipt.blocker_codes


def test_incompatible_consent_blocks_with_consent_scope_blocked():
    service = ApprovalGateService()
    gate_input = _gate_input(consent_compatible=False, consent_blocker_codes=["CONSENT_SCOPE_BLOCKED"])

    report = service.evaluate_approval_gate(gate_input)

    assert report.decision == ApprovalGateDecision.blocked
    assert "CONSENT_SCOPE_BLOCKED" in [blocker.code for blocker in report.blockers]
    assert report.consent_compatible is False


def test_source_truth_and_identity_failures_block_with_repair_hints():
    service = ApprovalGateService()
    gate_input = _gate_input(
        source_truth_passed=False,
        disputed_source_refs=["claim:unsupported:001"],
        identity_passed=False,
        identity_failure_refs=["identity:likeness:failed"],
    )

    report = service.evaluate_approval_gate(gate_input)
    codes = {blocker.code: blocker for blocker in report.blockers}

    assert "SOURCE_TRUTH_BLOCKED" in codes
    assert codes["SOURCE_TRUTH_BLOCKED"].repair_hint == "revise_or_remove_unsupported_claim"
    assert "IDENTITY_OR_LIKENESS_FAILED" in codes
    assert codes["IDENTITY_OR_LIKENESS_FAILED"].repair_hint == "request_revision_or_reject_asset"


def test_platform_or_content_format_failure_blocks_approval():
    service = ApprovalGateService()
    gate_input = _gate_input(
        platform_format_passed=False,
        platform_blocker_codes=["CAPTION_SAFE_AREA_FAILED"],
        content_format_key="newsletter.thread",
    )

    report = service.evaluate_approval_gate(gate_input)
    codes = [blocker.code for blocker in report.blockers]

    assert "CAPTION_SAFE_AREA_FAILED" in codes
    assert "CONTENT_FORMAT_UNSUPPORTED" in codes
    assert report.content_format_validation.blocker_code == "CONTENT_FORMAT_UNSUPPORTED"
    assert report.content_format_passed is False


def test_approved_policy_report_allows_review_approval_event():
    gate_service = ApprovalGateService()
    gate_input = _gate_input()
    report = gate_service.evaluate_approval_gate(gate_input)
    decision_service = _decision_service(gate_service, gate_input)

    receipt = decision_service.approve_asset(
        review_state_id=gate_input.review_state_id,
        actor_id=uuid4(),
        role_ids=["reviewer"],
        object_version_hash=gate_input.object_version_hash,
        approval_policy_report_id=report.approval_policy_report_id,
        idempotency_key="approve:gate:allowed",
    )

    assert report.decision == ApprovalGateDecision.approved_allowed
    assert receipt.result_state == ReviewResultState.approved
    assert decision_service.repository.approval_events


def test_blocked_policy_report_prevents_approval_event_creation():
    gate_service = ApprovalGateService()
    gate_input = _gate_input(evaluation_passed=False, evaluation_hard_failure_codes=["SOURCE_TRUTH_CONTRADICTION"])
    report = gate_service.evaluate_approval_gate(gate_input)
    decision_service = _decision_service(gate_service, gate_input)

    receipt = decision_service.approve_asset(
        review_state_id=gate_input.review_state_id,
        actor_id=uuid4(),
        role_ids=["reviewer"],
        object_version_hash=gate_input.object_version_hash,
        approval_policy_report_id=report.approval_policy_report_id,
        idempotency_key="approve:gate:blocked",
    )

    assert receipt.result_state == ReviewResultState.blocked
    assert "SOURCE_TRUTH_CONTRADICTION" in receipt.blocker_codes
    assert decision_service.repository.approval_events == {}


def test_approval_gate_workflow_and_command_bus_emit_receipt():
    service = ApprovalGateService()
    gate_input = _gate_input()
    workflow = ReviewWorkflow(revision_service=None, approval_gate_service=service)
    workflow_report = workflow.stage13_approval_gate(gate_input)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(gate_input.organization_id, gate_input.brand_id)
    register_approval_gate_command_handlers(bus, service)
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="EvaluateApprovalGateCommand",
        organization_id=gate_input.organization_id,
        brand_id=gate_input.brand_id,
        actor=actor,
        payload={"gate_input": gate_input.model_dump(mode="json")},
    )

    result = bus.submit(envelope)

    assert workflow_report.decision == ApprovalGateDecision.approved_allowed
    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision"] == ApprovalGateDecision.approved_allowed.value
    assert any(event.event_type == "ApprovalBlockerReceiptRecorded" for event in service.repository.events)

