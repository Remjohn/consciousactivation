from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except ModuleNotFoundError:
    FastAPI = None
    TestClient = None

from ccp_studio.contracts.commands import (
    ActorContext,
    ActorType,
    CommandStatus,
    new_command_envelope,
)
from ccp_studio.services.command_bus import VALIDATION_ORDER, create_in_memory_command_bus
from ccp_studio.services.static_guards import scan_for_legacy_runtime_coupling


def _bus_with_scope():
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    return bus, org_id, brand_id


def _actor():
    return ActorContext(
        actor_id=uuid4(),
        actor_type=ActorType.human,
        role_ids=["owner"],
    )


def test_command_envelope_requires_brand_scope_fields():
    bus, org_id, brand_id = _bus_with_scope()
    envelope = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
        payload={"aggregate_id": str(brand_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.domain_event_id is not None
    assert result.audit_receipt_id is not None
    assert len(bus.command_log.records) == 1
    assert len(bus.event_outbox.events) == 1
    assert len(bus.audit_receipts.receipts) == 1


def test_validation_order_before_handler_execution():
    bus, org_id, brand_id = _bus_with_scope()
    envelope = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
    )

    result = bus.submit(envelope)
    observed = [item.code for item in result.validation_results if item.passed]

    assert observed == VALIDATION_ORDER


def test_idempotency_replay_does_not_duplicate_side_effects():
    bus, org_id, brand_id = _bus_with_scope()
    key = "same-key"
    first = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
        idempotency_key=key,
    )
    second = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
        idempotency_key=key,
    )

    first_result = bus.submit(first)
    second_result = bus.submit(second)

    assert first_result.status == CommandStatus.succeeded
    assert second_result.status == CommandStatus.replayed
    assert second_result.domain_event_id == first_result.domain_event_id
    assert len(bus.event_outbox.events) == 1
    assert len(bus.audit_receipts.receipts) == 1


def test_cross_brand_command_fails_with_scope_violation_receipt():
    bus, org_id, _brand_id = _bus_with_scope()
    unknown_brand = uuid4()
    envelope = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=unknown_brand,
        actor=_actor(),
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "BRAND_SCOPE_VIOLATION" for item in result.validation_results)
    assert result.audit_receipt_id is not None
    assert len(bus.event_outbox.events) == 0


def test_receipt_writer_unavailable_blocks_handler_without_side_effects():
    bus, org_id, brand_id = _bus_with_scope()
    bus.audit_receipts.writable = False
    envelope = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "RECEIPT_WRITER_UNAVAILABLE" for item in result.validation_results)
    assert result.audit_receipt_id is None
    assert len(bus.event_outbox.events) == 0
    assert len(bus.command_log.records) == 1


def test_fastapi_route_wraps_submission_in_command_bus():
    if FastAPI is None or TestClient is None:
        pytest.skip("FastAPI adapter dependency set is incomplete in this local environment.")

    from ccp_studio.api.v1.commands import router, set_command_bus

    bus, org_id, brand_id = _bus_with_scope()
    set_command_bus(bus)
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    envelope = new_command_envelope(
        command_type="SubmitCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(),
    )

    response = client.post("/api/v1/commands", json=envelope.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.json()["status"] == "succeeded"
    assert len(bus.command_log.records) == 1


def test_legacy_runtime_coupling_guard_detects_forbidden_marker(tmp_path):
    unsafe = tmp_path / "unsafe.py"
    unsafe.write_text("import legacy_runtime.commands\n", encoding="utf-8")
    safe = tmp_path / "safe.py"
    safe.write_text("from ccp_studio.services.command_bus import CommandBus\n", encoding="utf-8")

    assert scan_for_legacy_runtime_coupling([unsafe, safe]) == [str(unsafe)]
