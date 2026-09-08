"""CA-M041 focused tests for reactive gate resumption and approval receipts.

Per execution-agent instruction, this bundle does not execute these tests.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable

import pytest

from ca_runtime.gate_resumption import (
    AuthorizationDecisionReceipt,
    GateAuthorityError,
    GateConflictError,
    GateAlreadyResolvedError,
    GateLifecycle,
    GateResumptionCoordinator,
    GateStaleRevisionError,
    GateResolutionSource,
    InMemoryGateRegistry,
    InMemoryReceiptStore,
    JsonlReceiptStore,
    PolicyOverride,
    ReceiptIntegrityError,
    ResumeEventType,
    SuspendedPipelineGate,
)
from ca_runtime.pi_adapter import AuthorityLane


SIGNING_KEY = "ca-m041-test-key"
GATE_ID = "gate-ca-m041"
PIPELINE_ID = "pipeline-ca-m041"
REVISION = 17
SNAPSHOT_HASH = "snapshot-sha256-001"
POLICY_HASH = "policy-sha256-001"
LOCK_TOKEN = "lock-ca-m041"


def _gate(**overrides: object) -> SuspendedPipelineGate:
    values = {
        "gate_id": GATE_ID,
        "pipeline_id": PIPELINE_ID,
        "suspension_revision": REVISION,
        "snapshot_hash": SNAPSHOT_HASH,
        "policy_revision_hash": POLICY_HASH,
        "suspended_at": "2026-09-08T04:00:00Z",
        "lock_token": LOCK_TOKEN,
        "next_node_id": "node-after-gate",
        "metadata": {"invariant": "INV-GATE-002"},
    }
    values.update(overrides)
    return SuspendedPipelineGate(**values)


def _coordinator(
    *,
    receipt_store=None,
    gate_registry=None,
    resume_handlers=None,
) -> GateResumptionCoordinator:
    coordinator = GateResumptionCoordinator(
        signing_key=SIGNING_KEY,
        receipt_store=receipt_store,
        gate_registry=gate_registry,
        resume_handlers=resume_handlers,
    )
    coordinator.register_suspended_gate(_gate())
    return coordinator


def test_ca_m041_operator_approval_is_immutable_and_receipt_precedes_lock_release() -> None:
    ordering: list[tuple[str, bool]] = []

    receipt_store = InMemoryReceiptStore()

    class RecordingReceiptStore(InMemoryReceiptStore):
        def persist(self, receipt: AuthorizationDecisionReceipt) -> None:
            ordering.append(("receipt_persist", coordinator.is_gate_locked(GATE_ID)))
            super().persist(receipt)

    receipt_store = RecordingReceiptStore()

    def after_release(_gate_id: str, _receipt: AuthorizationDecisionReceipt) -> None:
        ordering.append(("lock_release", coordinator.is_gate_locked(GATE_ID)))

    registry = InMemoryGateRegistry(after_lock_release=after_release)
    coordinator = _coordinator(receipt_store=receipt_store, gate_registry=registry)

    result = asyncio.run(
        coordinator.submit_approval(
            gate_id=GATE_ID,
            actor_id="commander-1",
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
            notes="Approve controlled resumption.",
            decision_at="2026-09-08T04:01:00Z",
        )
    )

    assert ordering == [
        ("receipt_persist", True),
        ("lock_release", False),
    ]
    assert result.lifecycle == GateLifecycle.RESUMED
    assert not coordinator.is_gate_locked(GATE_ID)
    assert result.resume_event.event_type == ResumeEventType.RESUME.value
    assert result.resume_event.next_node_id == "node-after-gate"
    assert result.receipt.source == GateResolutionSource.OPERATOR_APPROVAL.value
    assert result.receipt.verify(SIGNING_KEY)
    assert result.receipt.actor_fingerprint
    assert result.receipt.receipt_id.startswith("rcpt_appr_")
    assert coordinator.get_receipt(result.receipt.receipt_id) == result.receipt
    assert coordinator.pending_resume_events() == (result.resume_event,)


def test_ca_m041_non_commander_cannot_resume_and_lock_remains_held() -> None:
    coordinator = _coordinator()

    with pytest.raises(GateAuthorityError) as exc:
        asyncio.run(
            coordinator.submit_approval(
                gate_id=GATE_ID,
                actor_id="analyst-1",
                actor_lane=AuthorityLane.ANALYST,
                expected_suspension_revision=REVISION,
                expected_snapshot_hash=SNAPSHOT_HASH,
            )
        )

    assert exc.value.reason_code == "COMMANDER_AUTHORITY_REQUIRED"
    assert coordinator.get_gate(GATE_ID) == GateLifecycle.SUSPENDED
    assert coordinator.is_gate_locked(GATE_ID)
    assert coordinator.list_receipts(GATE_ID) == ()


def test_ca_m041_policy_override_is_commander_bound_and_resumes_reactively() -> None:
    events: list[tuple[str, bool, str]] = []

    async def resume_handler(event) -> None:
        events.append((event.event_type, coordinator.is_gate_locked(GATE_ID), event.receipt_id))

    coordinator = _coordinator(resume_handlers=[resume_handler])

    override = PolicyOverride(
        override_id="override-001",
        policy_revision_hash="policy-override-sha256-009",
        actor_id="commander-policy",
        reason="Escalated policy exception approved for this gate.",
        issued_at="2026-09-08T04:02:00Z",
    )

    result = asyncio.run(
        coordinator.submit_policy_override(
            gate_id=GATE_ID,
            override=override,
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
        )
    )

    assert result.receipt.source == GateResolutionSource.POLICY_OVERRIDE.value
    assert result.receipt.override_id == "override-001"
    assert result.receipt.override_policy_revision_hash == "policy-override-sha256-009"
    assert result.receipt.policy_revision_hash == POLICY_HASH
    assert result.receipt.verify(SIGNING_KEY)
    assert events == [(
        ResumeEventType.RESUME.value,
        False,
        result.receipt.receipt_id,
    )]
    assert coordinator.pending_resume_events() == ()


def test_ca_m041_stale_revision_fails_closed_without_receipt_or_unlock() -> None:
    coordinator = _coordinator()

    with pytest.raises(GateStaleRevisionError) as exc:
        asyncio.run(
            coordinator.submit_approval(
                gate_id=GATE_ID,
                actor_id="commander-1",
                actor_lane=AuthorityLane.COMMANDER,
                expected_suspension_revision=REVISION - 1,
                expected_snapshot_hash=SNAPSHOT_HASH,
            )
        )

    assert exc.value.reason_code == "GATE_STALE_REVISION"
    assert coordinator.get_gate(GATE_ID) == GateLifecycle.SUSPENDED
    assert coordinator.is_gate_locked(GATE_ID)
    assert coordinator.list_receipts(GATE_ID) == ()


def test_ca_m041_stale_snapshot_hash_fails_closed() -> None:
    coordinator = _coordinator()

    with pytest.raises(GateStaleRevisionError):
        asyncio.run(
            coordinator.submit_approval(
                gate_id=GATE_ID,
                actor_id="commander-1",
                actor_lane=AuthorityLane.COMMANDER,
                expected_suspension_revision=REVISION,
                expected_snapshot_hash="tampered-snapshot",
            )
        )

    assert coordinator.get_gate(GATE_ID) == GateLifecycle.SUSPENDED
    assert coordinator.is_gate_locked(GATE_ID)


def test_ca_m041_duplicate_identical_approval_is_idempotent_and_conflicting_approval_is_blocked() -> None:
    coordinator = _coordinator()

    kwargs = dict(
        gate_id=GATE_ID,
        actor_id="commander-1",
        actor_lane=AuthorityLane.COMMANDER,
        expected_suspension_revision=REVISION,
        expected_snapshot_hash=SNAPSHOT_HASH,
        decision_at="2026-09-08T04:03:00Z",
        notes="same approval",
    )

    first = asyncio.run(coordinator.submit_approval(**kwargs))
    second = asyncio.run(coordinator.submit_approval(**kwargs))

    assert second.receipt == first.receipt
    assert second.resume_event == first.resume_event
    assert len(coordinator.list_receipts(GATE_ID)) == 1

    with pytest.raises(GateAlreadyResolvedError):
        asyncio.run(
            coordinator.submit_approval(
                gate_id=GATE_ID,
                actor_id="commander-2",
                actor_lane=AuthorityLane.COMMANDER,
                expected_suspension_revision=REVISION,
                expected_snapshot_hash=SNAPSHOT_HASH,
                decision_at="2026-09-08T04:04:00Z",
                notes="conflicting actor",
            )
        )

    assert len(coordinator.list_receipts(GATE_ID)) == 1


def test_ca_m041_receipt_tampering_is_detectable() -> None:
    coordinator = _coordinator()
    result = asyncio.run(
        coordinator.submit_approval(
            gate_id=GATE_ID,
            actor_id="commander-1",
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
        )
    )

    receipt = result.receipt
    tampered = AuthorizationDecisionReceipt(
        receipt_id=receipt.receipt_id,
        gate_id=receipt.gate_id,
        pipeline_id=receipt.pipeline_id,
        actor_id="attacker",
        actor_fingerprint=receipt.actor_fingerprint,
        authority_lane=receipt.authority_lane,
        decision=receipt.decision,
        source=receipt.source,
        decision_at=receipt.decision_at,
        suspension_revision=receipt.suspension_revision,
        snapshot_hash=receipt.snapshot_hash,
        policy_revision_hash=receipt.policy_revision_hash,
        override_policy_revision_hash=receipt.override_policy_revision_hash,
        override_id=receipt.override_id,
        lock_token_hash=receipt.lock_token_hash,
        actor_signature_sha256=receipt.actor_signature_sha256,
        receipt_sha256=receipt.receipt_sha256,
        notes=receipt.notes,
        previous_receipt_sha256=receipt.previous_receipt_sha256,
    )

    with pytest.raises(ReceiptIntegrityError):
        tampered.assert_valid(SIGNING_KEY)


def test_ca_m041_receipt_store_is_restart_durable_and_append_only(tmp_path: Path) -> None:
    path = tmp_path / "ca_m041_receipts.jsonl"
    first_store = JsonlReceiptStore(path, signing_key=SIGNING_KEY)
    coordinator = _coordinator(receipt_store=first_store)

    result = asyncio.run(
        coordinator.submit_approval(
            gate_id=GATE_ID,
            actor_id="commander-durable",
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
            decision_at="2026-09-08T04:05:00Z",
        )
    )

    reopened = JsonlReceiptStore(path, signing_key=SIGNING_KEY)
    persisted = reopened.get(result.receipt.receipt_id)

    assert persisted == result.receipt
    assert persisted is not None
    assert persisted.verify(SIGNING_KEY)


def test_ca_m041_async_waiter_observes_reactive_resolution() -> None:
    async def scenario() -> tuple[bool, str]:
        coordinator = _coordinator()
        waiter = asyncio.create_task(coordinator.wait_for_resolution(GATE_ID, timeout=2.0))
        await asyncio.sleep(0)

        result = await coordinator.submit_approval(
            gate_id=GATE_ID,
            actor_id="commander-waiter",
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
        )
        observed = await waiter
        return observed.receipt.receipt_id == result.receipt.receipt_id, observed.resume_event.event_type

    observed_same_receipt, event_type = asyncio.run(scenario())

    assert observed_same_receipt
    assert event_type == ResumeEventType.RESUME.value


def test_ca_m041_resume_handler_failure_keeps_event_queued_for_retry() -> None:
    calls: list[int] = []

    def failing_handler(_event) -> None:
        calls.append(1)
        raise RuntimeError("downstream resume worker unavailable")

    coordinator = _coordinator(resume_handlers=[failing_handler])

    with pytest.raises(RuntimeError, match="downstream resume worker unavailable"):
        asyncio.run(
            coordinator.submit_approval(
                gate_id=GATE_ID,
                actor_id="commander-retry",
                actor_lane=AuthorityLane.COMMANDER,
                expected_suspension_revision=REVISION,
                expected_snapshot_hash=SNAPSHOT_HASH,
            )
        )

    assert calls == [1]
    assert not coordinator.is_gate_locked(GATE_ID)
    assert len(coordinator.pending_resume_events()) == 1


def test_ca_m041_rejects_non_resumption_policy_scope() -> None:
    coordinator = _coordinator()
    override = PolicyOverride(
        override_id="override-out-of-scope",
        policy_revision_hash="policy-sha256-010",
        actor_id="commander-policy",
        reason="Unrelated policy update",
        issued_at="2026-09-08T04:06:00Z",
        scope="RELEASE",
    )

    with pytest.raises(GateConflictError) as exc:
        asyncio.run(
            coordinator.submit_policy_override(
                gate_id=GATE_ID,
                override=override,
                actor_lane=AuthorityLane.COMMANDER,
                expected_suspension_revision=REVISION,
                expected_snapshot_hash=SNAPSHOT_HASH,
            )
        )

    assert getattr(exc.value, "reason_code", None) == "GATE_DEFINITION_CONFLICT"
    assert coordinator.is_gate_locked(GATE_ID)
    assert coordinator.list_receipts(GATE_ID) == ()


def test_ca_m041_jsonl_store_rejects_tampered_persisted_receipt(tmp_path: Path) -> None:
    path = tmp_path / "ca_m041_receipts_tampered.jsonl"
    store = JsonlReceiptStore(path, signing_key=SIGNING_KEY)
    coordinator = _coordinator(receipt_store=store)

    result = asyncio.run(
        coordinator.submit_approval(
            gate_id=GATE_ID,
            actor_id="commander-tamper",
            actor_lane=AuthorityLane.COMMANDER,
            expected_suspension_revision=REVISION,
            expected_snapshot_hash=SNAPSHOT_HASH,
            decision_at="2026-09-08T04:07:00Z",
        )
    )

    text = path.read_text(encoding="utf-8")
    text = text.replace(result.receipt.actor_id, "attacker", 1)
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ReceiptIntegrityError):
        JsonlReceiptStore(path, signing_key=SIGNING_KEY)
