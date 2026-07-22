from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.consent import ConsentScope, ConsentVersionStatus
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.consent_service import ConsentService, register_consent_command_handlers


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


def _consent_fixture():
    service = ConsentService()
    bus = create_in_memory_command_bus()
    register_consent_command_handlers(bus, service)
    org_id = uuid4()
    brand_id = uuid4()
    subject_id = uuid4()
    actor = _actor()
    bus.brands.add_scope(org_id, brand_id)
    return service, bus, org_id, brand_id, subject_id, actor


def _grant(service, org_id, brand_id, subject_id, actor, scope=None):
    return service.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        scope=scope or _scope(),
        actor_id=actor.actor_id,
        evidence_refs=["consent:recording:1"],
    )


def test_grant_consent_command_creates_immutable_version_and_receipt_path():
    service, bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    envelope = new_command_envelope(
        command_type="GrantConsentCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "guest_or_client_id": str(subject_id),
            "scope": _scope().model_dump(),
            "evidence_refs": ["consent:recording:1"],
        },
    )

    result = bus.submit(envelope)
    current = service.repository.current_version(org_id, brand_id, subject_id)
    receipt = next(iter(service.repository.receipts.values()))

    assert result.status == CommandStatus.succeeded
    assert current.version_number == 1
    assert current.scope.publication_allowed is True
    assert receipt.storage_path.startswith(f"brands/{brand_id}/receipts/consent/")


def test_narrowing_creates_new_active_version_and_preserves_old_version():
    service, _bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    first = _grant(service, org_id, brand_id, subject_id, actor)

    narrowed = service.narrow_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        scope=_scope(publication_allowed=False),
        actor_id=actor.actor_id,
        evidence_refs=["consent:narrowed:1"],
    )
    versions = service.repository.versions_for_subject(org_id, brand_id, subject_id)

    assert len(versions) == 2
    assert versions[0].consent_record_version_id == first.consent_record_version_id
    assert versions[0].scope.publication_allowed is True
    assert narrowed.version_number == 2
    assert narrowed.replaces_version_id == first.consent_record_version_id
    assert service.repository.current_version(org_id, brand_id, subject_id).scope.publication_allowed is False


def test_expired_consent_blocks_render_command_with_named_scope():
    service, bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    _grant(service, org_id, brand_id, subject_id, actor)
    service.expire_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        actor_id=actor.actor_id,
    )
    render = new_command_envelope(
        command_type="QueueRenderCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"guest_or_client_id": str(subject_id)},
    )

    result = bus.submit(render)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "CONSENT_EXPIRED" for item in result.validation_results)
    assert any(item.evidence.get("blocked_scope") == "active_consent" for item in result.validation_results)


def test_revocation_quarantines_pending_provider_work():
    service, _bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    _grant(service, org_id, brand_id, subject_id, actor)
    pending = service.add_pending_work(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        work_type="provider_job",
        source_ref="provider:job:queued",
    )

    revoked = service.revoke_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        actor_id=actor.actor_id,
    )
    impact = next(iter(service.repository.impacts.values()))

    assert revoked.status == ConsentVersionStatus.revoked
    assert service.repository.pending_work[pending.pending_work_id].status == "quarantined"
    assert impact.quarantine_required is True
    assert pending.pending_work_id in impact.affected_pending_work_ids


def test_review_view_shows_active_version_compatibility_evidence_and_risk():
    service, _bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    _grant(service, org_id, brand_id, subject_id, actor, _scope(publication_allowed=False))

    view = service.review_view(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=subject_id,
        command_type="PublishIntentCommand",
    )

    assert view.active_version.version_number == 1
    assert view.compatibility.allowed is False
    assert view.compatibility.blocked_scope == "publication_allowed"
    assert view.source_evidence_refs == ["consent:recording:1"]
    assert view.revocation_risk == "none"


def test_scope_mismatch_blocks_publish_intent_in_command_bus():
    service, bus, org_id, brand_id, subject_id, actor = _consent_fixture()
    _grant(service, org_id, brand_id, subject_id, actor, _scope(publication_allowed=False))
    publish = new_command_envelope(
        command_type="PublishIntentCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"guest_or_client_id": str(subject_id)},
    )

    result = bus.submit(publish)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "CONSENT_SCOPE_BLOCKED" for item in result.validation_results)
    assert any(item.evidence.get("blocked_scope") == "publication_allowed" for item in result.validation_results)
