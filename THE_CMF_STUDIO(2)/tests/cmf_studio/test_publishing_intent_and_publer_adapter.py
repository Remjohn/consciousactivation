from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.publishing import (  # noqa: E402
    PublerJobStatus,
    PublerWebhookEnvelope,
    PublishingIntentStatus,
    PublishingPlatformVariant,
    PublishingSchedule,
)
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.publishing_service import PublishingError, PublishingService, register_publishing_command_handlers  # noqa: E402
from ccp_studio.workflows.publishing_workflow import PublishingWorkflow  # noqa: E402


def _variant(**overrides):
    values = {
        "platform_variant_id": "instagram-reel-9x16",
        "platform": "instagram",
        "asset_uri": "object://render/final.mp4",
        "caption_manifest_id": uuid4(),
        "platform_format_key": "guest_asset_pack.clip.reel",
        "account_mapping_id": "publer:account:brand-instagram",
    }
    values.update(overrides)
    return PublishingPlatformVariant(**values)


def _schedule():
    return PublishingSchedule(schedule_at=utc_now(), time_zone="Europe/Brussels")


def _draft(service: PublishingService, **overrides):
    values = {
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "approved_asset_id": uuid4(),
        "approval_event_id": uuid4(),
        "consent_record_version_id": uuid4(),
        "approver_user_id": uuid4(),
        "platform_variants": [_variant()],
        "schedule": _schedule(),
        "idempotency_key": "publishing:intent:draft",
        "compliance_notes": ["approval gate passed", "caption manifest locked"],
    }
    values.update(overrides)
    return service.draft_publishing_intent(**values)


def _confirmed(service: PublishingService):
    intent = _draft(service)
    intent = service.validate_publishing_intent(intent.publishing_intent_id)
    return service.confirm_publishing_intent(
        intent.publishing_intent_id,
        confirmed_by_user_id=uuid4(),
        human_confirmation=True,
    )


def test_draft_intent_references_approved_asset_platform_caption_consent_schedule_and_approver():
    service = PublishingService()

    intent = _draft(service)
    receipt = next(iter(service.repository.receipts.values()))

    assert intent.status == PublishingIntentStatus.draft
    assert intent.approved_asset_id is not None
    assert intent.approval_event_id is not None
    assert intent.consent_record_version_id is not None
    assert intent.platform_variants[0].caption_manifest_id is not None
    assert intent.schedule.time_zone == "Europe/Brussels"
    assert intent.approver_user_id is not None
    assert receipt.decision_code == "PUBLISHING_INTENT_DRAFTED"


def test_missing_approval_or_consent_blocks_draft_with_receipt():
    service = PublishingService()

    with pytest.raises(PublishingError) as exc:
        _draft(service, approval_event_id=None, consent_record_version_id=None)
    receipt = next(iter(service.repository.receipts.values()))

    assert exc.value.code == "APPROVAL_EVENT_REQUIRED"
    assert "APPROVAL_EVENT_REQUIRED" in receipt.blocker_codes
    assert "CONSENT_RECORD_VERSION_REQUIRED" in receipt.blocker_codes
    assert receipt.decision_code == "PUBLISHING_INTENT_DRAFT_BLOCKED"


def test_confirmed_intent_submits_to_publer_and_stores_job_and_request_receipt():
    service = PublishingService()
    intent = _confirmed(service)

    job = service.submit_publishing_intent_to_publer(
        intent.publishing_intent_id,
        idempotency_key="publer:submit:one",
    )

    assert job.external_job_id is not None
    assert job.request_receipt_id is not None
    assert job.status == PublerJobStatus.scheduled
    assert service.repository.intents[intent.publishing_intent_id].status == PublishingIntentStatus.submitted
    assert any(receipt.publer_job_id == job.publer_job_id for receipt in service.repository.receipts.values())


def test_publer_webhook_records_outcome_without_making_publer_canonical():
    service = PublishingService()
    intent = _confirmed(service)
    job = service.submit_publishing_intent_to_publer(
        intent.publishing_intent_id,
        idempotency_key="publer:submit:webhook",
    )
    original_approval_event_id = intent.approval_event_id
    original_caption_id = intent.platform_variants[0].caption_manifest_id
    envelope = PublerWebhookEnvelope(
        schema_version="cmf.publer_webhook_envelope.v1",
        publer_webhook_id=uuid4(),
        publishing_intent_id=intent.publishing_intent_id,
        external_job_id=job.external_job_id,
        external_status=PublerJobStatus.published,
        external_url="https://publer.example/post/123",
        idempotency_key="publer:webhook:published",
        received_at=utc_now(),
    )

    outcome = service.reconcile_publer_status(envelope)
    replay = service.reconcile_publer_status(envelope)
    updated = service.repository.intents[intent.publishing_intent_id]

    assert outcome.external_status == PublerJobStatus.published
    assert replay.publishing_outcome_id == outcome.publishing_outcome_id
    assert updated.status == PublishingIntentStatus.succeeded
    assert updated.approval_event_id == original_approval_event_id
    assert updated.platform_variants[0].caption_manifest_id == original_caption_id
    assert outcome.publishing_outcome_id in service.repository.memory_admission_proposals


def test_duplicate_scheduling_attempt_is_blocked():
    service = PublishingService()
    approved_asset_id = uuid4()
    variant = _variant()
    schedule = _schedule()
    _draft(service, approved_asset_id=approved_asset_id, platform_variants=[variant], schedule=schedule, idempotency_key="intent:one")

    with pytest.raises(PublishingError) as exc:
        _draft(service, approved_asset_id=approved_asset_id, platform_variants=[variant], schedule=schedule, idempotency_key="intent:duplicate")

    assert exc.value.code == "DUPLICATE_PUBLISHING_INTENT"
    assert any("DUPLICATE_PUBLISHING_INTENT" in receipt.blocker_codes for receipt in service.repository.receipts.values())


def test_publer_adapter_rejects_unconfirmed_intent():
    service = PublishingService()
    intent = _draft(service)

    with pytest.raises(PublishingError) as exc:
        service.submit_publishing_intent_to_publer(
            intent.publishing_intent_id,
            idempotency_key="publer:submit:unconfirmed",
        )

    assert exc.value.code == "PUBLISHING_INTENT_CONFIRMATION_REQUIRED"
    assert service.repository.publer_jobs == {}


def test_publishing_workflow_and_command_bus_emit_publishing_receipt():
    service = PublishingService()
    intent = _confirmed(service)
    workflow = PublishingWorkflow(service)
    workflow_job = workflow.stage14_publish_intent(
        intent.publishing_intent_id,
        idempotency_key="publer:workflow",
    )
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(intent.organization_id, intent.brand_id)
    register_publishing_command_handlers(bus, service)
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["publishing_approver"])
    envelope = new_command_envelope(
        command_type="ReconcilePublerStatusCommand",
        organization_id=intent.organization_id,
        brand_id=intent.brand_id,
        actor=actor,
        payload={
            "webhook": {
                "schema_version": "cmf.publer_webhook_envelope.v1",
                "publer_webhook_id": str(uuid4()),
                "publishing_intent_id": str(intent.publishing_intent_id),
                "external_job_id": workflow_job.external_job_id,
                "external_status": "published",
                "external_url": "https://publer.example/post/456",
                "idempotency_key": "publer:webhook:command",
                "received_at": utc_now().isoformat(),
            }
        },
    )

    result = bus.submit(envelope)

    assert workflow_job.publer_job_id in service.repository.publer_jobs
    assert result.status == CommandStatus.succeeded
    assert result.result_payload["external_status"] == PublerJobStatus.published.value
    assert any(event.event_type == "PublerStatusReconciled" for event in service.repository.events)

