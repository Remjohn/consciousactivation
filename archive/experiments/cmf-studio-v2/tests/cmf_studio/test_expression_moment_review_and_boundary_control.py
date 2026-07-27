from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_anchor_hit_and_expression_moment_candidate_detection import _extraction_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.extraction import CandidateStatus  # noqa: E402
from ccp_studio.contracts.expression_review import (  # noqa: E402
    ExpressionMomentStatus,
    ReviewDecisionType,
    ReviewRejectionCode,
    boundary_from_candidate,
)
from ccp_studio.repositories.expression_review import ImmutableApprovedMomentError  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.expression_review_service import (  # noqa: E402
    ExpressionReviewService,
    ExpressionReviewServiceError,
    register_expression_review_command_handlers,
)
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _review_fixture():
    extraction, source_service, session_service, org_id, brand_id, actor_id, session = _extraction_fixture()
    extraction_receipt = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    review = ExpressionReviewService(extraction)
    return review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, extraction_receipt


def _candidate(review_fixture):
    review, extraction, _source, _session_service, _org, _brand, _actor, _session, receipt = review_fixture
    return extraction.repository.candidates[receipt.candidate_ids[0]]


def test_review_surface_shows_source_transcript_timestamp_context_route_and_sensitivity():
    fixture = _review_fixture()
    review, _extraction, _source, _session_service, org_id, brand_id, _actor_id, _session, receipt = fixture

    surface = review.review_surface_for_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=receipt.candidate_ids[0],
    )

    assert surface.source_playback_ref.startswith("brands/")
    assert "#t=" in surface.source_playback_ref
    assert surface.transcript_excerpt
    assert surface.timestamp_end_ms > surface.timestamp_start_ms
    assert surface.induction_context_ids
    assert surface.route_rationale
    assert "dignity_or_sensitivity_review" in surface.sensitivity_flags


def test_boundary_fix_preserves_original_candidate_and_writes_review_receipt():
    fixture = _review_fixture()
    review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, _receipt = fixture
    candidate = _candidate(fixture)
    original_start = candidate.timestamp_start_ms
    boundary = boundary_from_candidate(
        source_artifact_id=candidate.source_artifact_id,
        transcript_revision_id=candidate.transcript_revision_id,
        start_ms=150,
        end_ms=candidate.timestamp_end_ms,
        transcript_segment_ids=candidate.transcript_segment_ids,
    )

    receipt = review.adjust_expression_moment_boundary(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        reviewer_actor_id=actor_id,
        boundary=boundary,
        rationale="Tighten the start to the first usable source phrase.",
    )

    assert _candidate(fixture).timestamp_start_ms == original_start
    adjusted = review.repository.moments[receipt.new_expression_moment_ids[0]]
    assert adjusted.boundary.start_ms == 150
    assert receipt.decision_type == ReviewDecisionType.adjust_boundary
    assert receipt.source_candidate_ids == [candidate.candidate_id]


def test_merge_records_both_source_ranges():
    fixture = _review_fixture()
    review, extraction, _source, _session_service, org_id, brand_id, actor_id, _session, _receipt = fixture
    candidate = _candidate(fixture)
    second = candidate.model_copy(
        update={
            "candidate_id": uuid4(),
            "timestamp_start_ms": candidate.timestamp_end_ms + 100,
            "timestamp_end_ms": candidate.timestamp_end_ms + 900,
            "source_quote": "The second usable beat lands after the first moment.",
            "status": CandidateStatus.ready_for_review,
        }
    )
    extraction.repository.put_candidate(second)

    receipt = review.merge_expression_moment_candidates(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_ids=[candidate.candidate_id, second.candidate_id],
        reviewer_actor_id=actor_id,
        rationale="The two beats are one expression moment when reviewed together.",
    )
    moment = review.repository.moments[receipt.new_expression_moment_ids[0]]

    assert moment.status == ExpressionMomentStatus.approved
    assert len(moment.boundary.source_ranges) == 2
    assert len(receipt.source_ranges) == 2


def test_sensitivity_hold_blocks_routing_until_released():
    fixture = _review_fixture()
    review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, _receipt = fixture
    candidate = _candidate(fixture)
    approval = review.approve_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        reviewer_actor_id=actor_id,
        rationale="Source truth and boundary are sufficient.",
    )
    moment_id = approval.new_expression_moment_ids[0]

    hold = review.place_sensitivity_hold(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        reviewer_actor_id=actor_id,
        reason="Guest dignity review before routing.",
    )

    assert hold.decision_code == "EXPRESSION_MOMENT_SENSITIVITY_HELD"
    assert review.can_route_expression_moment(moment_id) is False
    with pytest.raises(ExpressionReviewServiceError, match="SENSITIVITY_HOLD_BLOCKS_ROUTING"):
        review.assert_can_route_expression_moment(moment_id)

    review.release_sensitivity_hold(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        reviewer_actor_id=actor_id,
        rationale="Sensitivity resolved by reviewer.",
    )
    assert review.can_route_expression_moment(moment_id) is True


def test_approved_moment_immutable_except_supersession():
    fixture = _review_fixture()
    review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, _receipt = fixture
    candidate = _candidate(fixture)
    approval = review.approve_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        reviewer_actor_id=actor_id,
        rationale="Approve before supersession test.",
    )
    moment = review.repository.moments[approval.new_expression_moment_ids[0]]

    with pytest.raises(ImmutableApprovedMomentError):
        review.repository.put_moment(moment.model_copy(update={"source_quote": "edited in place"}))

    replacement_boundary = boundary_from_candidate(
        source_artifact_id=moment.boundary.source_artifact_id,
        transcript_revision_id=moment.boundary.transcript_revision_id,
        start_ms=moment.boundary.start_ms,
        end_ms=moment.boundary.end_ms + 250,
        transcript_segment_ids=moment.boundary.transcript_segment_ids,
    )
    receipt = review.supersede_expression_moment(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment.expression_moment_id,
        reviewer_actor_id=actor_id,
        boundary=replacement_boundary,
        source_quote=moment.source_quote + " Corrected boundary tail.",
        rationale="Supersede rather than mutate the approved moment.",
    )

    old = review.repository.moments[moment.expression_moment_id]
    new = review.repository.moments[receipt.new_expression_moment_ids[0]]
    assert old.status == ExpressionMomentStatus.superseded
    assert old.source_quote == moment.source_quote
    assert new.supersedes_expression_moment_ids == [old.expression_moment_id]


def test_workflow_stage6_review_expression_moments_returns_review_receipt():
    fixture = _review_fixture()
    review, extraction, source_service, session_service, org_id, brand_id, actor_id, _session, receipt = fixture
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=source_service,
        extraction_service=extraction,
        expression_review_service=review,
    )

    receipts = workflow.stage6_review_expression_moments(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_ids=receipt.candidate_ids,
        actor_id=actor_id,
        rationale="Approve reviewable candidates for routing.",
    )

    assert receipts[0].decision_code == "EXPRESSION_MOMENT_APPROVED"


def test_expression_review_command_bus_emits_receipt_event():
    fixture = _review_fixture()
    review, _extraction, _source, _session_service, org_id, brand_id, actor_id, _session, receipt = fixture
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_expression_review_command_handlers(bus, review)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="ApproveExpressionMomentCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "candidate_id": str(receipt.candidate_ids[0]),
            "rationale": "Human reviewer approves source-truth and boundary.",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "EXPRESSION_MOMENT_APPROVED"
    assert bus.event_outbox.events[-1].event_type == "ApproveExpressionMomentCommand.succeeded"
