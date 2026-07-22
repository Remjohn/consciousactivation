from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope, ConsentVersionStatus, new_consent_version  # noqa: E402
from ccp_studio.contracts.memory_admission import MemoryClaimScope, MemoryEventType, MemoryEvidenceRef, MemoryScope  # noqa: E402
from ccp_studio.contracts.memory_governance import MemoryGovernanceActionType, MemoryGovernanceStatus, MemoryUsagePolicy  # noqa: E402
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.memory_admission_service import MemoryAdmissionService  # noqa: E402
from ccp_studio.services.memory_governance_service import MemoryGovernanceService, register_memory_governance_command_handlers  # noqa: E402
from ccp_studio.workflows.memory_admission import MemoryAdmissionWorkflow  # noqa: E402


def _scope():
    return ConsentScope(
        recording_allowed=True,
        source_storage_allowed=True,
        likeness_use_allowed=True,
        derivative_generation_allowed=True,
        provider_processing_allowed=True,
        synthetic_voice_eligible=True,
        reuse_allowed=True,
        retention_allowed=True,
        publication_allowed=True,
    )


def _evidence(source_id: str = "approval:001"):
    return MemoryEvidenceRef(
        source_type="approval_event",
        source_id=source_id,
        evidence_uri=f"object://evidence/{source_id}",
        transcript_segment_id="segment:memory:001",
        receipt_id=f"receipt:{source_id}",
        claim_scope=MemoryClaimScope.supports,
    )


def _fixture():
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    consent_repository = InMemoryConsentRepository()
    consent = consent_repository.put_version(
        new_consent_version(
            organization_id=org_id,
            brand_id=brand_id,
            guest_or_client_id=uuid4(),
            version_number=1,
            status=ConsentVersionStatus.active,
            scope=_scope(),
            created_by_actor_id=actor_id,
            evidence_refs=["consent:memory-governance"],
        )
    )
    admission = MemoryAdmissionService(consent_repository)
    candidate = admission.propose_memory_admission(
        organization_id=org_id,
        brand_id=brand_id,
        memory_type=MemoryEventType.route,
        proposed_from_event_id="approval_event:asset:001",
        proposed_statement="When Claude names the reconciliation contrast at 12:04, retain route memory because the approved asset used exact transcript phrasing.",
        evidence_refs=[_evidence()],
        confidence=0.91,
        scope=MemoryScope.route,
        consent_record_version_id=consent.consent_record_version_id,
        consent_compatible=True,
        originating_route_ref="route:source-truth-first",
        provenance_summary="Approved asset, route receipt, and transcript segment support this memory.",
        proposed_by_actor_id=actor_id,
    )
    receipt = admission.approve_memory_admission(
        candidate_id=candidate.candidate_id,
        reviewer_id=actor_id,
        role_ids=["reviewer"],
        idempotency_key="memory:approve:governance",
    )
    governance = MemoryGovernanceService(admission.repository)
    return admission, governance, org_id, brand_id, actor_id, candidate, receipt


def test_memory_review_state_shows_evidence_source_route_confidence_consent_event_and_usage():
    admission, governance, _org_id, _brand_id, _actor_id, candidate, receipt = _fixture()
    admission.record_memory_usage_citation(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="JITSkillCompiler",
        citing_object_ref="skill_invocation:route:001",
        evidence_refs=[candidate.evidence_refs[0]],
        idempotency_key="memory:citation:review-state",
    )

    state = governance.build_memory_review_state(receipt.memory_event_id)

    assert state.governance_status == MemoryGovernanceStatus.active
    assert state.evidence_refs
    assert any(ref.startswith("approval_event") for ref in state.source_refs)
    assert state.route_refs == ["route:source-truth-first"]
    assert state.confidence == 0.91
    assert state.consent_compatible is True
    assert state.created_event_id == receipt.memory_event_id
    assert state.downstream_usage_refs


def test_correction_writes_superseding_memory_event_without_mutating_original():
    admission, governance, _org_id, _brand_id, actor_id, _candidate, receipt = _fixture()
    original = admission.repository.memory_events[receipt.memory_event_id]
    original_statement = original.proposed_statement

    correction = governance.correct_memory(
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["reviewer"],
        reason="Tighten memory to the exact route condition.",
        evidence_refs=["review:correction:001"],
        corrected_statement="When Claude names the reconciliation contrast at 12:04, use route memory only for source-truth-first clips with the same transcript-backed wording.",
        idempotency_key="memory:correct:one",
    )
    original_after = admission.repository.memory_events[receipt.memory_event_id]
    superseding = admission.repository.memory_events[correction.superseding_memory_event_id]
    original_usage = governance.validate_memory_usage(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="RouteCompiler",
        usage_purpose="active route selection",
    )
    superseding_usage = governance.validate_memory_usage(
        memory_event_id=superseding.memory_event_id,
        compiler_or_agent="RouteCompiler",
        usage_purpose="active route selection",
    )

    assert original_after.proposed_statement == original_statement
    assert superseding.proposed_statement.startswith("When Claude names")
    assert correction.resulting_status == MemoryGovernanceStatus.corrected
    assert original_usage.policy == MemoryUsagePolicy.blocked
    assert original_usage.active_memory_event_id == superseding.memory_event_id
    assert superseding_usage.policy == MemoryUsagePolicy.allowed


def test_expired_memory_is_historical_only_and_blocks_compiler_use():
    _admission, governance, _org_id, _brand_id, actor_id, _candidate, receipt = _fixture()

    expired = governance.expire_memory(
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Performance evidence is stale after benchmark update.",
        evidence_refs=["benchmark:update:2026-06"],
        idempotency_key="memory:expire:one",
    )
    decision = governance.validate_memory_usage(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="InterviewPrepCompiler",
        usage_purpose="active interview preparation",
    )

    assert expired.resulting_status == MemoryGovernanceStatus.expired
    assert expired.downstream_usage_effect == "active_memory_usage_blocked_historical_only"
    assert decision.policy == MemoryUsagePolicy.blocked
    assert decision.reason == "memory_expired_blocks_active_use"


def test_quarantine_blocks_downstream_use_until_release():
    _admission, governance, _org_id, _brand_id, actor_id, _candidate, receipt = _fixture()

    quarantined = governance.quarantine_memory(
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["production_steward"],
        reason="Potentially sensitive material requires review.",
        evidence_refs=["consent:change:001"],
        idempotency_key="memory:quarantine:one",
    )
    blocked = governance.validate_memory_usage(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="RouteCompiler",
        usage_purpose="active route selection",
    )
    released = governance.release_memory_from_quarantine(
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["production_steward"],
        reason="Consent review cleared active use.",
        evidence_refs=["consent:clearance:001"],
        idempotency_key="memory:release:one",
    )
    allowed = governance.validate_memory_usage(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="RouteCompiler",
        usage_purpose="active route selection",
    )

    assert quarantined.resulting_status == MemoryGovernanceStatus.quarantined
    assert blocked.policy == MemoryUsagePolicy.blocked
    assert released.resulting_status == MemoryGovernanceStatus.active
    assert allowed.policy == MemoryUsagePolicy.allowed


def test_reversal_is_respected_by_future_route_compilation():
    _admission, governance, _org_id, _brand_id, actor_id, _candidate, receipt = _fixture()

    reversed_receipt = governance.reverse_memory(
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["reviewer"],
        reason="Later review showed the route memory promoted the wrong route.",
        evidence_refs=["route:review:reversal"],
        idempotency_key="memory:reverse:one",
    )
    decision = governance.validate_memory_usage(
        memory_event_id=receipt.memory_event_id,
        compiler_or_agent="RouteCompiler",
        usage_purpose="boost same route",
    )

    assert reversed_receipt.resulting_status == MemoryGovernanceStatus.reversed
    assert decision.policy == MemoryUsagePolicy.blocked
    assert decision.reason == "memory_reversed_blocks_active_use"
    assert governance.repository.events[-1].event_type == "MemoryUsageBlocked"


def test_memory_governance_workflow_routes_stage14_action():
    _admission, governance, _org_id, _brand_id, actor_id, _candidate, receipt = _fixture()
    workflow = MemoryAdmissionWorkflow(memory_admission_service=_admission, memory_governance_service=governance)

    expired = workflow.stage14_govern_memory(
        action_type=MemoryGovernanceActionType.expire,
        memory_event_id=receipt.memory_event_id,
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Operator expired stale memory.",
        evidence_refs=["operator:expiry:001"],
        idempotency_key="memory:workflow:expire",
    )

    assert expired.resulting_status == MemoryGovernanceStatus.expired
    assert expired.projection_event_id in governance.repository.projection_events


def test_memory_governance_command_bus_is_idempotent_and_records_receipt():
    _admission, governance, org_id, brand_id, actor_id, _candidate, receipt = _fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_memory_governance_command_handlers(bus, governance)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="QuarantineMemoryCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="memory:command:quarantine",
        payload={
            "memory_event_id": str(receipt.memory_event_id),
            "reason": "Command quarantine for sensitive memory.",
            "evidence_refs": ["command:evidence:001"],
        },
    )

    first = bus.submit(envelope)
    second = bus.submit(envelope)

    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["resulting_status"] == MemoryGovernanceStatus.quarantined.value
    assert len(governance.repository.receipts) == 1
    assert any(event.event_type == "MemoryQuarantined" for event in governance.repository.events)
