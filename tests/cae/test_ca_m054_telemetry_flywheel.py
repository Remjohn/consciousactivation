"""CA-M054 / INV-TELEM-001 proof suite.

The tests exercise the canonical runtime boundary rather than a pipeline-local
telemetry helper: genuine operator approval/rejection calls feed the flywheel,
while exports remain redacted, immutable derivatives.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ca_runtime.factory_observability import (
    HumanResolutionEpisode,
    TelemetryEventClass,
    TelemetryFlywheel,
    TelemetryIntegrityError,
    TelemetryRedactionError,
)
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    UniversalProgramStateRuntime,
    get_canonical_interview_state_machine,
)


@pytest.fixture
def flywheel() -> TelemetryFlywheel:
    return TelemetryFlywheel()


def test_six_class_taxonomy_is_explicit_and_stable(flywheel: TelemetryFlywheel) -> None:
    assert tuple(item.value for item in flywheel.event_classes) == (
        "EXECUTION",
        "TRANSITION",
        "OPERATOR_GATE",
        "RESOURCE",
        "FAILURE",
        "SYSTEM",
    )


def test_event_payload_is_redacted_and_content_addressed(flywheel: TelemetryFlywheel) -> None:
    event = flywheel.emit(
        TelemetryEventClass.FAILURE,
        workspace_id="workspace-a",
        aggregate_id="aggregate-1",
        actor_id="alice@example.com",
        payload={
            "error_code": "PROVIDER_TIMEOUT",
            "email": "alice@example.com",
            "api_token": "secret-token",
            "operator_id": "alice@example.com",
        },
        timestamp="2026-09-08T20:00:00+00:00",
    )
    event.verify()
    encoded = str(event.canonical_dict())
    assert "alice@example.com" not in encoded
    assert "secret-token" not in encoded
    assert event.event_sha256 and len(event.event_sha256) == 64


def test_unknown_event_class_fails_closed(flywheel: TelemetryFlywheel) -> None:
    with pytest.raises(TelemetryIntegrityError):
        flywheel.emit("MODEL_INVENTED_CLASS", workspace_id="workspace-a")


def test_authentic_resolution_yields_redacted_preference_pair_and_export(flywheel: TelemetryFlywheel) -> None:
    episode = flywheel.capture_operator_resolution(
        aggregate_id="aggregate-1",
        workspace_id="workspace-a",
        gate_id="GATE-7",
        decision="APPROVE",
        operator_id="alice@example.com",
        source_state="AWAITING_APPROVAL",
        target_state="RUNNING",
        receipt_id="receipt-1",
        chosen={"candidate_id": "candidate-good", "email": "alice@example.com"},
        rejected=[{"candidate_id": "candidate-bad", "raw_text": "private transcript"}],
        rationale="Selected the evidence-backed candidate.",
        timestamp="2026-09-08T20:00:01+00:00",
    )
    assert episode.preference_eligible
    pair = flywheel.preference_pairs()[0]
    pair.verify()
    manifest = flywheel.export_manifest()
    flywheel.verify_export(manifest)
    encoded = str(manifest)
    assert "alice@example.com" not in encoded
    assert "private transcript" not in encoded
    assert manifest["read_only_derivation"] is True
    assert manifest["redaction_verified"] is True


def test_missing_alternatives_are_recorded_but_never_promoted(flywheel: TelemetryFlywheel) -> None:
    episode = flywheel.capture_operator_resolution(
        aggregate_id="aggregate-2",
        workspace_id="workspace-a",
        gate_id="GATE-8",
        decision="REJECT",
        operator_id="operator-1",
        source_state="AWAITING_APPROVAL",
        target_state="REQUIREMENTS_EXTRACTED",
        receipt_id="receipt-2",
        rejected=[{"candidate_id": "candidate-only"}],
    )
    assert not episode.preference_eligible
    assert flywheel.preference_pairs() == ()


def test_tampered_event_and_export_fail_closed(flywheel: TelemetryFlywheel) -> None:
    event = flywheel.emit(
        TelemetryEventClass.SYSTEM,
        workspace_id="workspace-a",
        payload={"component": "runtime"},
        timestamp="2026-09-08T20:00:00+00:00",
    )
    tampered = type(event)(
        event_id=event.event_id,
        event_class=event.event_class,
        workspace_id=event.workspace_id,
        aggregate_id=event.aggregate_id,
        actor_ref=event.actor_ref,
        timestamp=event.timestamp,
        payload={"component": "tampered"},
        event_sha256=event.event_sha256,
    )
    with pytest.raises(TelemetryIntegrityError):
        tampered.verify()

    manifest = flywheel.export_manifest()
    manifest["events"][0]["payload"]["component"] = "tampered"
    with pytest.raises(TelemetryIntegrityError):
        flywheel.verify_export(manifest)


def test_raw_protected_content_cannot_be_smuggled_in_rationale(flywheel: TelemetryFlywheel) -> None:
    episode = flywheel.capture_operator_resolution(
        aggregate_id="aggregate-3",
        workspace_id="workspace-a",
        gate_id="GATE-9",
        decision="APPROVE",
        operator_id="operator-1",
        source_state="AWAITING_APPROVAL",
        target_state="RUNNING",
        receipt_id="receipt-3",
        chosen={"candidate_id": "candidate-good"},
        rejected=[{"candidate_id": "candidate-bad"}],
        rationale="Contact me at alice@example.com",
    )
    episode.verify()
    assert "alice@example.com" not in str(episode.canonical_dict())


def test_program_operator_approval_captures_only_after_canonical_commit() -> None:
    runtime = UniversalProgramStateRuntime(store=InMemoryProgramStateStore())
    runtime.register_state_machine(get_canonical_interview_state_machine())
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    service = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)

    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="workspace-a",
        actor_id="operator-1",
        initial_data={"candidate": "candidate-good"},
    )
    service.approve_program(
        aggregate_id=aggregate.aggregate_id,
        actor_id="operator-1",
        gate_id="GATE-10",
        payload={
            "chosen": {"candidate_id": "candidate-good"},
            "rejected": [{"candidate_id": "candidate-bad"}],
            "rationale": "Operator selected the evidence-backed candidate.",
        },
    )
    episodes = service._get_telemetry_flywheel().episodes
    assert len(episodes) == 1
    assert episodes[0].receipt_id == service.runtime.get_aggregate(aggregate.aggregate_id).last_receipt_id
    assert episodes[0].preference_eligible


def test_runtime_rejection_captures_operator_gate_without_fabricating_choice() -> None:
    runtime = UniversalProgramStateRuntime(store=InMemoryProgramStateStore())
    runtime.register_state_machine(get_canonical_interview_state_machine())
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    service = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)
    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="workspace-a",
        actor_id="operator-1",
    )

    service.reject_program(
        aggregate_id=aggregate.aggregate_id,
        actor_id="operator-1",
        rejection_reason="Insufficient evidence",
    )
    episode = service._get_telemetry_flywheel().episodes[0]
    assert episode.decision == "REJECT"
    assert not episode.preference_eligible


def test_export_rejects_unredacted_manifest(flywheel: TelemetryFlywheel) -> None:
    manifest = flywheel.export_manifest()
    manifest["redaction_verified"] = False
    with pytest.raises(TelemetryIntegrityError):
        flywheel.verify_export(manifest)
