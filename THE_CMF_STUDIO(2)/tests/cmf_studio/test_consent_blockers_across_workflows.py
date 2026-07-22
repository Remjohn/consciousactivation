from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.consent import ConsentScope
from ccp_studio.contracts.consent_blockers import ConsentRepairAction
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.consent_guard import ConsentGuardService, register_consent_guard
from ccp_studio.services.consent_service import ConsentService


def _scope(**overrides):
    values = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": False,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": True,
    }
    values.update(overrides)
    return ConsentScope(**values)


def _actor():
    return ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["owner"])


def _fixture(scope=None):
    consent = ConsentService()
    guard = ConsentGuardService(consent)
    bus = create_in_memory_command_bus()
    register_consent_guard(bus, guard)
    org_id = uuid4()
    brand_id = uuid4()
    guest_id = uuid4()
    actor = _actor()
    bus.brands.add_scope(org_id, brand_id)
    consent.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=scope or _scope(),
        actor_id=actor.actor_id,
        evidence_refs=["consent:current"],
    )
    return consent, guard, bus, org_id, brand_id, guest_id, actor


def test_registry_covers_provider_render_memory_review_publishing_future_reuse_and_voice_repair():
    _consent, guard, _bus, _org_id, _brand_id, _guest_id, _actor = _fixture()

    assert guard.repository.get_sensitive_command("SubmitProviderJobCommand").external_side_effect is True
    assert guard.repository.get_sensitive_command("QueueRenderCommand").required_scopes == [
        "likeness_use_allowed",
        "derivative_generation_allowed",
    ]
    assert "review" in guard.repository.get_sensitive_command("ApproveReviewCommand").applies_to_stages
    assert "publishing" in guard.repository.get_sensitive_command("PublishIntentCommand").applies_to_stages
    assert "future_reuse" in guard.repository.get_sensitive_command("RequestFutureReuseCommand").applies_to_stages
    assert "synthetic_voice_eligible" in guard.repository.get_sensitive_command("RequestVoiceRepairCommand").required_scopes


def test_provider_job_blocks_when_provider_processing_scope_is_false_and_writes_receipt():
    _consent, guard, bus, org_id, brand_id, guest_id, actor = _fixture(
        _scope(provider_processing_allowed=False)
    )
    envelope = new_command_envelope(
        command_type="SubmitProviderJobCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"guest_or_client_id": str(guest_id), "object_type": "provider_job", "object_id": str(uuid4())},
    )

    result = bus.submit(envelope)
    receipt = next(iter(guard.repository.blocker_receipts.values()))

    assert result.status == CommandStatus.rejected
    assert any(item.code == "CONSENT_SCOPE_BLOCKED" for item in result.validation_results)
    assert receipt.decision_code == "CONSENT_SCOPE_BLOCKED"
    assert receipt.blocked_scope == "provider_processing_allowed"


def test_likeness_revocation_blocks_rerender_and_flags_pending_jobs():
    consent, guard, bus, org_id, brand_id, guest_id, actor = _fixture(
        _scope(likeness_use_allowed=False)
    )
    pending = consent.add_pending_work(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        work_type="render",
        source_ref="render:queued",
    )
    scene_id = uuid4()
    envelope = new_command_envelope(
        command_type="RerenderSceneCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"guest_or_client_id": str(guest_id), "object_type": "scene", "object_id": str(scene_id)},
    )

    result = bus.submit(envelope)
    affected = next(iter(guard.repository.affected_pending_work.values()))

    assert result.status == CommandStatus.rejected
    assert any(item.code == "LIKENESS_REUSE_BLOCKED" for item in result.validation_results)
    assert consent.repository.pending_work[pending.pending_work_id].status == "quarantined"
    assert pending.pending_work_id in affected.pending_work_ids
    assert affected.object_id == scene_id


def test_missing_publication_consent_blocks_publishing_intent_before_scheduling():
    _consent, guard, bus, org_id, brand_id, guest_id, actor = _fixture(
        _scope(publication_allowed=False)
    )
    envelope = new_command_envelope(
        command_type="PublishIntentCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"guest_or_client_id": str(guest_id), "object_type": "publishing_intent", "object_id": str(uuid4())},
    )

    result = bus.submit(envelope)
    receipt = next(iter(guard.repository.blocker_receipts.values()))

    assert result.status == CommandStatus.rejected
    assert any(item.code == "PUBLICATION_CONSENT_REQUIRED" for item in result.validation_results)
    assert receipt.blocked_scope == "publication_allowed"
    assert ConsentRepairAction.request_updated_consent in receipt.repair_actions


def test_memory_admission_without_reuse_or_retention_consent_offers_quarantine():
    _consent, guard, _bus, org_id, brand_id, guest_id, _actor = _fixture(
        _scope(reuse_allowed=False, retention_allowed=False)
    )

    decision = guard.evaluate_workflow_boundary(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        command_type="MemoryAdmissionCommand",
        object_type="memory_candidate",
        object_id=uuid4(),
    )

    assert decision.allowed is False
    assert decision.decision_code == "MEMORY_ADMISSION_CONSENT_BLOCKED"
    assert ConsentRepairAction.quarantine in decision.repair_actions
    assert decision.blocker_receipt_id in guard.repository.blocker_receipts


def test_future_reuse_reevaluates_current_consent_instead_of_historical_approval():
    consent, guard, _bus, org_id, brand_id, guest_id, actor = _fixture()
    old_version = consent.repository.current_version(org_id, brand_id, guest_id)
    consent.narrow_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(reuse_allowed=False),
        actor_id=actor.actor_id,
        evidence_refs=["consent:narrowed"],
    )

    decision = guard.evaluate_workflow_boundary(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        command_type="RequestFutureReuseCommand",
        object_type="approved_asset",
        object_id=uuid4(),
    )

    assert old_version.scope.reuse_allowed is True
    assert decision.allowed is False
    assert decision.decision_code == "CONSENT_SCOPE_BLOCKED"
    assert decision.consent_record_version_id != old_version.consent_record_version_id


def test_consent_sensitive_workflow_with_missing_mapping_defaults_to_blocked():
    _consent, guard, bus, org_id, brand_id, guest_id, actor = _fixture()
    envelope = new_command_envelope(
        command_type="UnmappedConsentSensitiveCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "guest_or_client_id": str(guest_id),
            "requires_consent_policy": True,
            "object_type": "provider_job",
            "object_id": str(uuid4()),
        },
    )

    result = bus.submit(envelope)
    receipt = next(iter(guard.repository.blocker_receipts.values()))

    assert result.status == CommandStatus.rejected
    assert any(item.code == "CONSENT_SCOPE_MAPPING_REQUIRED" for item in result.validation_results)
    assert receipt.blocked_scope == "scope_mapping"


def test_durable_workflow_rechecks_consent_before_external_side_effect():
    consent, guard, _bus, org_id, brand_id, guest_id, actor = _fixture()
    consent.narrow_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(provider_processing_allowed=False),
        actor_id=actor.actor_id,
        evidence_refs=["consent:narrowed:provider"],
    )

    decision = guard.evaluate_workflow_boundary(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        command_type="SubmitProviderJobCommand",
        object_type="provider_job",
        object_id=uuid4(),
    )

    assert decision.allowed is False
    assert decision.decision_code == "CONSENT_SCOPE_BLOCKED"
    assert decision.blocker_receipt_id in guard.repository.blocker_receipts
