from __future__ import annotations

import hashlib
import hmac
import sys
from pathlib import Path
from time import time
from urllib.parse import urlencode
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.surfaces import ObjectStateSnapshot, SurfaceKey, new_surface_action
from ccp_studio.services.command_bus import ReferenceCommandHandler, create_in_memory_command_bus
from ccp_studio.services.surface_action_service import NotificationIntentService, SurfaceActionService
from ccp_studio.services.telegram_auth_service import TelegramAuthError, TelegramAuthService


def _signed_init_data(bot_token: str, auth_date: int | None = None) -> str:
    fields = {
        "auth_date": str(auth_date or int(time())),
        "query_id": "surface-query",
        "user": '{"id":123,"first_name":"Operator"}',
    }
    data_check_string = "\n".join(f"{key}={fields[key]}" for key in sorted(fields))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    fields["hash"] = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return urlencode(fields)


def _surface_fixture(evidence=True):
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    object_id = uuid4()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    bus.register_handler(ReferenceCommandHandler("ApproveSurfaceCommand", "surface_object"))
    service = SurfaceActionService(
        command_bus=bus,
        actor_roles_provider=lambda _actor, _org, _brand: ["owner"],
    )
    snapshot = ObjectStateSnapshot(
        schema_version="cmf.object_state_snapshot.v1",
        object_type="render_output",
        object_id=object_id,
        organization_id=org_id,
        brand_id=brand_id,
        state="pending_review",
        state_version="v1",
        evidence_sufficient_for_surface=evidence,
        evidence_refs=["render:preview", "eval:receipt"],
    )
    service.object_states.put(snapshot)
    return service, bus, org_id, brand_id, actor_id, snapshot


def test_telegram_deep_link_references_same_object_brand_state_and_command():
    service, _bus, org_id, brand_id, actor_id, snapshot = _surface_fixture(evidence=False)
    action = new_surface_action(
        source_surface=SurfaceKey.telegram_bot,
        actor_id=actor_id,
        organization_id=org_id,
        brand_id=brand_id,
        command_type="ApproveSurfaceCommand",
        idempotency_key="approve-link",
        object_snapshot=snapshot,
    )

    result = service.submit(action)

    assert result.result_code == "PWA_REVIEW_REQUIRED"
    assert result.deep_link.object_id == snapshot.object_id
    assert result.deep_link.brand_id == brand_id
    assert "render_output" in result.deep_link.route


def test_telegram_init_data_verification_accepts_signed_payload_and_rejects_invalid():
    auth = TelegramAuthService(bot_token="test-token", max_age_seconds=300)
    signed = _signed_init_data("test-token", auth_date=1000)

    fields = auth.verify_init_data(signed, now_seconds=1100)

    assert fields["query_id"] == "surface-query"
    try:
        auth.verify_init_data(signed + "tampered=true", now_seconds=1100)
    except TelegramAuthError as exc:
        assert exc.code == "TELEGRAM_AUTH_INVALID"
    else:
        raise AssertionError("tampered Telegram initData must fail")


def test_telegram_quick_action_uses_command_bus_and_writes_receipt():
    service, bus, org_id, brand_id, actor_id, snapshot = _surface_fixture()
    action = new_surface_action(
        source_surface=SurfaceKey.telegram_bot,
        actor_id=actor_id,
        organization_id=org_id,
        brand_id=brand_id,
        command_type="ApproveSurfaceCommand",
        idempotency_key="telegram-approve",
        object_snapshot=snapshot,
        payload={"next_state": "approved", "next_state_version": "v2"},
    )

    result = service.submit(action)

    assert result.accepted is True
    assert result.receipt_id is not None
    assert len(bus.command_log.records) == 1
    assert len(bus.audit_receipts.receipts) == 1
    assert result.latest_state.state == "approved"


def test_pwa_first_action_prevents_stale_telegram_overwrite():
    service, _bus, org_id, brand_id, actor_id, snapshot = _surface_fixture()
    pwa = new_surface_action(
        source_surface=SurfaceKey.pwa,
        actor_id=actor_id,
        organization_id=org_id,
        brand_id=brand_id,
        command_type="ApproveSurfaceCommand",
        idempotency_key="pwa-first",
        object_snapshot=snapshot,
        payload={"next_state": "rejected", "next_state_version": "v2"},
    )
    telegram_stale = new_surface_action(
        source_surface=SurfaceKey.telegram_bot,
        actor_id=actor_id,
        organization_id=org_id,
        brand_id=brand_id,
        command_type="ApproveSurfaceCommand",
        idempotency_key="telegram-stale",
        object_snapshot=snapshot,
        payload={"next_state": "approved", "next_state_version": "v3"},
    )

    first = service.submit(pwa)
    stale = service.submit(telegram_stale)

    assert first.accepted is True
    assert stale.accepted is False
    assert stale.result_code == "STALE_OBJECT_STATE"
    assert stale.latest_state.state == "rejected"
    assert stale.latest_state.state_version == "v2"


def test_notification_intent_uses_latest_canonical_state_after_pwa_change():
    service, _bus, org_id, brand_id, actor_id, snapshot = _surface_fixture()
    pwa = new_surface_action(
        source_surface=SurfaceKey.pwa,
        actor_id=actor_id,
        organization_id=org_id,
        brand_id=brand_id,
        command_type="ApproveSurfaceCommand",
        idempotency_key="pwa-notify",
        object_snapshot=snapshot,
        payload={"next_state": "rejected", "next_state_version": "v2"},
    )
    service.submit(pwa)
    notifications = NotificationIntentService(service.object_states)

    intent = notifications.create_from_latest_state(
        object_type=snapshot.object_type,
        object_id=snapshot.object_id,
        target_surface=SurfaceKey.telegram_bot,
        message_key="render_status_changed",
    )

    assert intent.object_snapshot.state == "rejected"
    assert intent.object_snapshot.state_version == "v2"
    assert intent.brand_id == brand_id


def test_generated_typescript_surface_contract_contains_consumer_interfaces():
    path = Path("src/ccp_studio/generated/typescript/surface_contracts.ts")
    text = path.read_text(encoding="utf-8")

    assert "export interface SurfaceActionEnvelope" in text
    assert "telegram_mini_app" in text
