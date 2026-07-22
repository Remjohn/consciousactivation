from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope, ConsentVersionStatus, new_consent_version  # noqa: E402
from ccp_studio.contracts.memory_admission import (  # noqa: E402
    MemoryAdmissionPolicyResult,
    MemoryClaimScope,
    MemoryEventStatus,
    MemoryEventType,
    MemoryEvidenceRef,
    MemoryScope,
)
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.memory_admission_service import (  # noqa: E402
    MemoryAdmissionError,
    MemoryAdmissionService,
    register_memory_admission_command_handlers,
)
from ccp_studio.workflows.memory_admission import MemoryAdmissionWorkflow  # noqa: E402


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


def _consent(repository: InMemoryConsentRepository, org_id, brand_id, actor_id, *, active=True, reuse=True):
    return repository.put_version(
        new_consent_version(
            organization_id=org_id,
            brand_id=brand_id,
            guest_or_client_id=uuid4(),
            version_number=1,
            status=ConsentVersionStatus.active if active else ConsentVersionStatus.revoked,
            scope=_scope(reuse_allowed=reuse, retention_allowed=reuse, source_storage_allowed=reuse),
            created_by_actor_id=actor_id,
            evidence_refs=["consent:memory"],
        )
    )


def _evidence(source_type: str = "approval_event", source_id: str = "approval:001", receipt_id: str = "receipt:001"):
    return MemoryEvidenceRef(
        source_type=source_type,
        source_id=source_id,
        evidence_uri=f"object://evidence/{source_id}",
        transcript_segment_id="segment:truth:001" if source_type != "publishing_outcome" else None,
        receipt_id=receipt_id,
        claim_scope=MemoryClaimScope.supports,
    )


def _service():
    consent_repository = InMemoryConsentRepository()
    return MemoryAdmissionService(consent_repository), consent_repository


def _candidate(service: MemoryAdmissionService, consent_id, org_id, brand_id, actor_id, **overrides):
    values = {
        "organization_id": org_id,
        "brand_id": brand_id,
        "memory_type": MemoryEventType.route,
        "proposed_from_event_id": "approval_event:asset:001",
        "proposed_statement": "When Claude names a reconciliation claim at 12:04, route through source-truth-first public idea assets because the approved clip kept authority without exaggeration.",
        "evidence_refs": [_evidence()],
        "confidence": 0.91,
        "scope": MemoryScope.route,
        "consent_record_version_id": consent_id,
        "consent_compatible": True,
        "originating_route_ref": "route:public-idea-asset",
        "provenance_summary": "Approved review event, transcript segment, and route receipt all agree.",
        "proposed_by_actor_id": actor_id,
    }
    values.update(overrides)
    return service.propose_memory_admission(**values)


def test_approved_asset_route_rejection_and_publishing_outcomes_can_propose_evidence_memory():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)

    approved = _candidate(service, consent.consent_record_version_id, org_id, brand_id, actor_id)
    rejected = _candidate(
        service,
        consent.consent_record_version_id,
        org_id,
        brand_id,
        actor_id,
        memory_type=MemoryEventType.rejected_pattern,
        proposed_from_event_id="rejection_receipt:route:001",
        evidence_refs=[_evidence("rejection_receipt", "rejection:001", "rejection-receipt:001")],
        proposed_statement="When a route repeats unsupported certainty at 09:10, store it as rejected-pattern memory because the reviewer receipt marked it source_unsupported.",
    )
    publishing = _candidate(
        service,
        consent.consent_record_version_id,
        org_id,
        brand_id,
        actor_id,
        memory_type=MemoryEventType.publishing_performance,
        proposed_from_event_id="publishing_outcome:001",
        evidence_refs=[_evidence("publishing_outcome", "publer:outcome:001", "publishing-receipt:001")],
        proposed_statement="When the quiet-authority clip published at 08:30, retain route performance memory because the outcome receipt beat the benchmark engagement threshold.",
    )

    assert approved.evidence_refs[0].receipt_id == "receipt:001"
    assert rejected.memory_type == MemoryEventType.rejected_pattern
    assert publishing.memory_type == MemoryEventType.publishing_performance
    assert len(service.repository.candidates) == 3


def test_candidate_without_evidence_or_specificity_is_rejected_not_admitted_as_lore():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)
    candidate = _candidate(
        service,
        consent.consent_record_version_id,
        org_id,
        brand_id,
        actor_id,
        proposed_statement="this brand likes bold claims",
        evidence_refs=[],
        confidence=0.95,
    )

    receipt = service.approve_memory_admission(
        candidate_id=candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["reviewer"],
        idempotency_key="memory:approve:lore",
    )
    event = service.repository.memory_events[receipt.memory_event_id]

    assert receipt.policy_result == MemoryAdmissionPolicyResult.rejected
    assert event.status == MemoryEventStatus.rejected
    assert "MEMORY_EVIDENCE_REQUIRED" in receipt.blocker_codes
    assert "MEMORY_STATEMENT_TOO_GENERIC" in receipt.blocker_codes


def test_consent_incompatible_candidate_is_quarantined_with_receipt():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id, reuse=False)
    candidate = _candidate(
        service,
        consent.consent_record_version_id,
        org_id,
        brand_id,
        actor_id,
        consent_compatible=True,
    )

    receipt = service.approve_memory_admission(
        candidate_id=candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["production_steward"],
        idempotency_key="memory:approve:quarantine",
    )

    assert receipt.policy_result == MemoryAdmissionPolicyResult.quarantined
    assert receipt.consent_compatible is True
    assert "MEMORY_CONSENT_INCOMPATIBLE" in receipt.blocker_codes
    assert service.repository.memory_events[receipt.memory_event_id].status == MemoryEventStatus.quarantined


def test_approved_candidate_writes_memory_event_receipt_and_usage_citation_guard():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)
    candidate = _candidate(service, consent.consent_record_version_id, org_id, brand_id, actor_id)

    receipt = service.approve_memory_admission(
        candidate_id=candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["reviewer"],
        idempotency_key="memory:approve:one",
    )
    citation = service.record_memory_usage_citation(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="JITSkillCompiler",
        citing_object_ref="skill_invocation:route-compiler:001",
        evidence_refs=[candidate.evidence_refs[0]],
        idempotency_key="memory:citation:one",
    )

    assert receipt.policy_result == MemoryAdmissionPolicyResult.approved
    assert receipt.downstream_citation_required is True
    assert service.repository.memory_events[receipt.memory_event_id].status == MemoryEventStatus.approved
    assert citation.memory_event_id == receipt.memory_event_id
    assert service.repository.events[-1].event_type == "MemoryUsageCited"


def test_compiler_citation_requires_approved_memory_event_and_matching_evidence():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)
    candidate = _candidate(service, consent.consent_record_version_id, org_id, brand_id, actor_id)
    rejected = service.reject_memory_admission(
        candidate_id=candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["reviewer"],
        reason="not stable enough",
        idempotency_key="memory:reject:one",
    )

    with pytest.raises(MemoryAdmissionError, match="MEMORY_EVENT_NOT_APPROVED"):
        service.record_memory_usage_citation(
            memory_event_id=rejected.memory_event_id,
            compiler_or_agent="JITSkillCompiler",
            citing_object_ref="skill_invocation:bad",
            evidence_refs=[candidate.evidence_refs[0]],
            idempotency_key="memory:citation:bad",
        )

    approved_candidate = _candidate(
        service,
        consent.consent_record_version_id,
        org_id,
        brand_id,
        actor_id,
        idempotency_key="memory:proposal:approved",
    )
    approved = service.approve_memory_admission(
        candidate_id=approved_candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["reviewer"],
        idempotency_key="memory:approve:approved",
    )
    with pytest.raises(MemoryAdmissionError, match="MEMORY_CITATION_EVIDENCE_MISMATCH"):
        service.record_memory_usage_citation(
            memory_event_id=approved.memory_event_id,
            compiler_or_agent="JITSkillCompiler",
            citing_object_ref="skill_invocation:mismatch",
            evidence_refs=[_evidence("approval_event", "different", "different-receipt")],
            idempotency_key="memory:citation:mismatch",
        )


def test_memory_admission_workflow_stage14_admits_evidence_memory():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)
    workflow = MemoryAdmissionWorkflow(service)

    receipt = workflow.stage14_admit_evidence_memory(
        organization_id=org_id,
        brand_id=brand_id,
        memory_type=MemoryEventType.brand,
        proposed_from_event_id="approval_event:asset:workflow",
        proposed_statement="When the guest uses the phrase 'quiet courage' at 15:22, retain brand memory because the approved asset used it as the central emotional anchor.",
        evidence_refs=[_evidence("approval_event", "approval:workflow", "receipt:workflow")],
        confidence=0.88,
        scope=MemoryScope.brand,
        consent_record_version_id=consent.consent_record_version_id,
        consent_compatible=True,
        provenance_summary="Approved asset and transcript evidence support the memory.",
        proposed_by_actor_id=actor_id,
        role_ids=["operator"],
        approval_idempotency_key="memory:workflow:approve",
    )

    assert receipt.policy_result == MemoryAdmissionPolicyResult.approved
    assert receipt.memory_event_id in service.repository.memory_events


def test_memory_admission_command_bus_is_idempotent_and_writes_receipt_event():
    service, consent_repository = _service()
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent = _consent(consent_repository, org_id, brand_id, actor_id)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_memory_admission_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["reviewer"])
    propose = new_command_envelope(
        command_type="ProposeMemoryAdmissionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="memory:propose:command",
        payload={
            "memory_type": "route",
            "proposed_from_event_id": "approval_event:asset:command",
            "proposed_statement": "When the route preserves the guest's exact 18:40 contrast, admit route memory because the approved review receipt links it to better source truth.",
            "evidence_refs": [_evidence().model_dump(mode="json")],
            "confidence": 0.9,
            "scope": "route",
            "consent_record_version_id": str(consent.consent_record_version_id),
            "consent_compatible": True,
            "provenance_summary": "Command bus proposal from approved event and evidence refs.",
            "originating_route_ref": "route:contrast-proof",
        },
    )
    first_propose = bus.submit(propose)
    second_propose = bus.submit(propose)
    candidate_id = first_propose.result_payload["candidate_id"]
    approve = new_command_envelope(
        command_type="ApproveMemoryAdmissionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="memory:approve:command",
        payload={"candidate_id": candidate_id},
    )

    first_approve = bus.submit(approve)
    second_approve = bus.submit(approve)

    assert first_propose.status == CommandStatus.succeeded
    assert second_propose.status == CommandStatus.replayed
    assert first_approve.status == CommandStatus.succeeded
    assert second_approve.status == CommandStatus.replayed
    assert first_approve.result_payload["policy_result"] == MemoryAdmissionPolicyResult.approved.value
    assert any(event.event_type == "MemoryAdmissionApproved" for event in service.repository.events)
