from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_archetype_and_asset_derivative_routing import _routing_fixture  # noqa: E402
from test_expression_moment_review_and_boundary_control import _candidate  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope, ConsentVersionStatus, new_consent_version  # noqa: E402
from ccp_studio.contracts.rejection_memory import (  # noqa: E402
    MemoryAdmissionCandidateStatus,
    NegativeEvidenceKind,
    RejectionCategory,
)
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.rejection_memory_service import (  # noqa: E402
    RejectionMemoryService,
    RejectionMemoryServiceError,
    register_rejection_memory_command_handlers,
)
from ccp_studio.workflows.complete_expression_session import CompleteExpressionSessionWorkflow  # noqa: E402


def _service_fixture():
    routing, review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, moment_id = _routing_fixture()
    candidate = _candidate((review, extraction, source_service, session_service, org_id, brand_id, actor_id, session, next(iter(extraction.repository.receipts.values()))))
    rejected_route_receipt = routing.reject_source_route(
        organization_id=org_id,
        brand_id=brand_id,
        expression_moment_id=moment_id,
        actor_id=actor_id,
        requested_format=None,
        reason="Source support is insufficient for this route.",
    )
    consent_repository = InMemoryConsentRepository()
    service = RejectionMemoryService(extraction, routing, consent_repository)
    return service, routing, review, extraction, source_service, session_service, consent_repository, org_id, brand_id, actor_id, session, candidate, rejected_route_receipt


def _narrow_consent(consent_repository, org_id, brand_id, actor_id):
    version = new_consent_version(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=uuid4(),
        version_number=1,
        status=ConsentVersionStatus.active,
        scope=ConsentScope(
            recording_allowed=True,
            source_storage_allowed=True,
            likeness_use_allowed=False,
            derivative_generation_allowed=False,
            provider_processing_allowed=False,
            synthetic_voice_eligible=False,
            reuse_allowed=False,
            retention_allowed=False,
            publication_allowed=False,
        ),
        created_by_actor_id=actor_id,
        evidence_refs=["consent:narrowed"],
    )
    return consent_repository.put_version(version)


def test_rejection_stores_reason_evidence_reviewer_route_attempt_and_category():
    service, _routing, _review, _extraction, _source, _session_service, _consent, org_id, brand_id, actor_id, _session, candidate, route_receipt = _service_fixture()

    receipt = service.record_rejected_expression_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        category=RejectionCategory.boundary_bad,
        reason="Boundary starts before the actual guest pressure.",
        reviewer_id=actor_id,
        route_attempt_receipt_id=route_receipt.asset_route_receipt_id,
    )
    record = service.repository.rejected_candidates[receipt.rejected_candidate_id]

    assert receipt.decision_code == "REJECTED_CANDIDATE_RECORDED"
    assert record.reason.startswith("Boundary starts")
    assert record.route_attempt_receipt_id == route_receipt.asset_route_receipt_id
    assert record.reviewer_id == actor_id
    assert record.category == RejectionCategory.boundary_bad
    assert record.source_reference_ids


def test_source_insufficient_route_becomes_negative_evidence():
    service, _routing, _review, _extraction, _source, _session_service, _consent, org_id, brand_id, actor_id, _session, _candidate_obj, route_receipt = _service_fixture()

    receipt = service.record_rejected_route_attempt(
        organization_id=org_id,
        brand_id=brand_id,
        asset_route_receipt_id=route_receipt.asset_route_receipt_id,
        category=RejectionCategory.source_unsupported,
        reviewer_id=actor_id,
    )
    ref = service.reference_negative_evidence(
        rejection_receipt_id=receipt.rejection_receipt_id,
        compiler_or_evaluator="RouteSelectionProgram",
        usage_purpose="avoid repeating unsupported route",
    )

    assert receipt.negative_evidence_eligible is True
    assert ref.evidence_kind == NegativeEvidenceKind.rejected_route
    assert ref.truth_admission_blocked is True


def test_sensitive_or_consent_incompatible_material_is_quarantined():
    service, _routing, _review, _extraction, _source, _session_service, consent_repository, org_id, brand_id, actor_id, _session, candidate, _route_receipt = _service_fixture()
    consent = _narrow_consent(consent_repository, org_id, brand_id, actor_id)

    receipt = service.record_rejected_expression_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        category=RejectionCategory.sensitivity_or_consent,
        reason="Sensitive rejected material cannot become a fixture.",
        reviewer_id=actor_id,
        consent_record_version_id=consent.consent_record_version_id,
        sensitive_material=True,
    )
    record = service.repository.rejected_candidates[receipt.rejected_candidate_id]

    assert receipt.quarantined is True
    assert receipt.negative_evidence_eligible is False
    assert record.quarantined is True
    with pytest.raises(RejectionMemoryServiceError, match="NEGATIVE_EVIDENCE_NOT_ELIGIBLE"):
        service.reference_negative_evidence(
            rejection_receipt_id=receipt.rejection_receipt_id,
            compiler_or_evaluator="JITSkillCompiler",
            usage_purpose="fixture export",
        )


def test_future_compiler_cites_rejection_without_treating_it_as_truth():
    service, _routing, _review, _extraction, _source, _session_service, _consent, org_id, brand_id, actor_id, _session, candidate, _route_receipt = _service_fixture()
    receipt = service.record_rejected_expression_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        category=RejectionCategory.generic_or_centroid,
        reason="Candidate collapsed into generic phrasing.",
        reviewer_id=actor_id,
    )

    ref = service.reference_negative_evidence(
        rejection_receipt_id=receipt.rejection_receipt_id,
        compiler_or_evaluator="JITSkillCompiler",
        usage_purpose="anti-centroid calibration",
    )

    assert ref.rejection_receipt_id == receipt.rejection_receipt_id
    assert ref.truth_admission_blocked is True
    assert service.repository.rejected_candidates[receipt.rejected_candidate_id].admitted_as_truth is False


def test_memory_proposal_requires_explicit_gate_and_does_not_auto_admit():
    service, _routing, _review, _extraction, _source, _session_service, _consent, org_id, brand_id, actor_id, _session, candidate, _route_receipt = _service_fixture()
    receipt = service.record_rejected_expression_candidate(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        category=RejectionCategory.route_fit_failed,
        reason="Useful pattern for future route rejection.",
        reviewer_id=actor_id,
    )

    proposal = service.propose_memory_admission_from_rejection(
        rejection_receipt_id=receipt.rejection_receipt_id,
        proposed_memory_scope="route_failure_memory",
        reason="Store as negative pattern only after Epic 10 gate.",
    )

    assert proposal.status == MemoryAdmissionCandidateStatus.proposed_requires_memory_gate
    assert proposal.explicit_memory_gate_required is True
    assert proposal.auto_admitted_to_memory is False


def test_workflow_stage6_7_records_rejection_receipt():
    service, routing, review, extraction, source_service, session_service, _consent, org_id, brand_id, actor_id, _session, candidate, _route_receipt = _service_fixture()
    workflow = CompleteExpressionSessionWorkflow(
        service=session_service,
        source_provenance_service=source_service,
        extraction_service=extraction,
        expression_review_service=review,
        routing_service=routing,
        rejection_memory_service=service,
    )

    receipt = workflow.stage6_7_record_rejections(
        organization_id=org_id,
        brand_id=brand_id,
        candidate_id=candidate.candidate_id,
        actor_id=actor_id,
        category=RejectionCategory.source_unsupported,
        reason="Rejected in workflow.",
    )

    assert receipt.decision_code == "REJECTED_CANDIDATE_RECORDED"


def test_rejection_memory_command_bus_emits_rejection_receipt_event():
    service, _routing, _review, _extraction, _source, _session_service, _consent, org_id, brand_id, actor_id, _session, candidate, _route_receipt = _service_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_rejection_memory_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="RecordRejectedExpressionCandidateCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "candidate_id": str(candidate.candidate_id),
            "category": "source_unsupported",
            "reason": "Command bus rejection record.",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "REJECTED_CANDIDATE_RECORDED"
    assert bus.event_outbox.events[-1].event_type == "RecordRejectedExpressionCandidateCommand.succeeded"
