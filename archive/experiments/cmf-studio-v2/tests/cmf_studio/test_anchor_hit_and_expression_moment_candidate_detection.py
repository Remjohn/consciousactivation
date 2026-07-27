from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_source_ingestion_transcript_alignment_and_provenance import _artifact, _segments, _started_source_service  # noqa: E402
from test_jit_skill_compiler_saturation_contrast import _service as _jit_service  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.extraction import CandidateStatus  # noqa: E402
from ccp_studio.contracts.source_provenance import TranscriptSource  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.extraction_service import ExtractionService, register_extraction_command_handlers  # noqa: E402
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _extraction_fixture(with_jit=True):
    source_service, session_service, org_id, brand_id, actor_id, session = _started_source_service()
    artifact = _artifact(source_service, org_id, brand_id, actor_id, session)
    revision = source_service.generate_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        source_artifact_ids=[artifact.recording_artifact_id],
        segments=_segments(artifact.recording_artifact_id),
        transcript_source=TranscriptSource.provider_generated,
        actor_id=actor_id,
    )
    source_service.align_transcript_to_source(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision.transcript_revision_id,
        actor_id=actor_id,
    )
    source_service.select_transcript_revision(
        organization_id=org_id,
        brand_id=brand_id,
        transcript_revision_id=revision.transcript_revision_id,
        actor_id=actor_id,
    )
    contract_service = session_service.interview_contract_service
    binding = next(iter(contract_service.repository.bindings.values()))
    deck = contract_service.repository.decks[binding.interview_deck_id]
    contract = contract_service.repository.contracts[deck.contract_ids[0]]
    contract_service.repository.put_contract(
        contract.model_copy(update={"induction_rationale_ids": [uuid4()]})
    )
    jit_service = _jit_service()[0] if with_jit else None
    extraction = ExtractionService(
        source_provenance_service=source_service,
        interview_contract_service=contract_service,
        jit_skill_service=jit_service,
    )
    return extraction, source_service, session_service, org_id, brand_id, actor_id, session


def test_candidate_includes_timestamp_transcript_source_induction_anchor_route_and_confidence():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()

    receipt = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    candidate = extraction.repository.candidates[receipt.candidate_ids[0]]

    assert candidate.timestamp_start_ms == 0
    assert candidate.timestamp_end_ms > candidate.timestamp_start_ms
    assert candidate.transcript_segment_ids
    assert candidate.source_artifact_id
    assert candidate.induction_context_ids
    assert candidate.anchor_hit_ids
    assert candidate.route_rationale
    assert candidate.confidence > 0
    assert candidate.status == CandidateStatus.ready_for_review


def test_emotional_shift_cites_transcript_source_evidence():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()

    receipt = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    candidate = extraction.repository.candidates[receipt.candidate_ids[0]]

    assert candidate.emotional_shift_evidence
    assert "transcript text" in candidate.emotional_shift_evidence[0]
    assert "exposure" in candidate.source_quote.lower()


def test_unsupported_candidate_is_rejected_or_review_only_not_approved():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()

    receipt = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    candidate = extraction.repository.candidates[receipt.candidate_ids[0]]
    rejected = extraction.reject_unsupported_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        reason="Reviewer found route evidence insufficient.",
        actor_id=actor_id,
    )

    assert candidate.status in {CandidateStatus.ready_for_review, CandidateStatus.needs_review}
    assert rejected.status == CandidateStatus.rejected_unsupported


def test_jit_compiler_returns_saturation_contrast_anti_draft_and_receipt():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()

    contribution = extraction.invoke_jit_extraction_skill(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        skill_key="expression_extraction_jit",
        actor_id=actor_id,
    )

    assert contribution.saturation_context_hash
    assert contribution.contrast_output
    assert contribution.anti_draft_passed is True
    assert contribution.skill_invocation_receipt_id in extraction.repository.skill_contributions


def test_retry_preserves_prior_candidates_and_receipts():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()
    first = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )
    second = extraction.run_extraction(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        retry_of_run_id=first.extraction_run_id,
        actor_id=actor_id,
    )

    assert first.candidate_ids[0] in extraction.repository.candidates
    assert second.candidate_ids[0] in extraction.repository.candidates
    assert len(extraction.repository.receipts) == 2


def test_workflow_stage6_extract_candidates_returns_extraction_receipt():
    extraction, source_service, session_service, org_id, brand_id, actor_id, session = _extraction_fixture()
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=source_service,
        extraction_service=extraction,
    )

    receipt = workflow.stage6_extract_candidates(
        organization_id=org_id,
        brand_id=brand_id,
        expression_session_id=session.expression_session_id,
        actor_id=actor_id,
    )

    assert receipt.candidate_ids
    assert receipt.decision_code == "EXPRESSION_MOMENT_CANDIDATES_CREATED"


def test_extraction_command_bus_emits_receipt_event():
    extraction, _source, _session_service, org_id, brand_id, actor_id, session = _extraction_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_extraction_command_handlers(bus, extraction)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="RunExpressionExtractionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"expression_session_id": str(session.expression_session_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "EXPRESSION_MOMENT_CANDIDATES_CREATED"
    assert bus.event_outbox.events[-1].event_type == "RunExpressionExtractionCommand.succeeded"
