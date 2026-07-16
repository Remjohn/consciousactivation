from __future__ import annotations

from datetime import timedelta

import pytest

from cmf_builder.application.ports import AtomicCommitFailed
from cmf_builder.application.run_commands import (
    CreateCheckpointCommand,
    GrantWaiverCommand,
    ResumeRunCommand,
    TransitionRunCommand,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_01_01 import NOW, build_service, create_command


BOUNDARIES = ("events", "checkpoint", "command_record")


def _operation(name: str):
    service, repository, _, _, _ = build_service()
    if name == "create":
        command = create_command(command_id="atomic-create")
        return service, repository, command, service.create_run, None

    created = service.create_run(create_command())
    if name == "transition":
        command = TransitionRunCommand(
            command_id="atomic-transition",
            run_id=created.run_id,
            to_state=LifecycleState.SOURCE_DIAGNOSTIC,
            prerequisites=frozenset({"target_profile_selected"}),
            actor_id="architect-1",
            expected_version=2,
            correlation_id="BQA-P1-005",
            causation_id=created.receipt_id,
        )
        invoke = service.transition_run
    elif name == "waiver":
        command = GrantWaiverCommand(
            command_id="atomic-waiver",
            run_id=created.run_id,
            skipped_obligation="optional_synthetic_review",
            rationale="Deterministic correction evidence.",
            risk="low",
            affected_gates=("HG-004",),
            scope="BQA-P0-P1-TRUST-CORRECTION",
            expires_at=NOW + timedelta(hours=1),
            actor_id="architect-1",
            expected_version=2,
            correlation_id="BQA-P1-005",
            causation_id=created.receipt_id,
        )
        invoke = service.grant_waiver
    elif name == "checkpoint":
        command = CreateCheckpointCommand(
            command_id="atomic-checkpoint",
            run_id=created.run_id,
            input_hash="input:synthetic",
            policy_hash="policy:synthetic",
            actor_id="architect-1",
            expected_version=2,
            correlation_id="BQA-P1-005",
            causation_id=created.receipt_id,
        )
        invoke = service.create_checkpoint
    elif name == "resume":
        checkpoint = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="resume-setup-checkpoint",
                run_id=created.run_id,
                input_hash="input:synthetic",
                policy_hash="policy:synthetic",
                actor_id="architect-1",
                expected_version=2,
                correlation_id="BQA-P1-005",
                causation_id=created.receipt_id,
            )
        )
        command = ResumeRunCommand(
            command_id="atomic-resume",
            run_id=created.run_id,
            input_hash="input:synthetic",
            policy_hash="policy:synthetic",
            actor_id="architect-1",
            expected_version=3,
            correlation_id="BQA-P1-005",
            causation_id=checkpoint.receipt_id,
        )
        invoke = service.resume_run
    else:  # pragma: no cover - protected by test parameter values
        raise AssertionError(name)
    return service, repository, command, invoke, created.run_id


@pytest.mark.parametrize("operation", ("create", "transition", "waiver", "checkpoint", "resume"))
@pytest.mark.parametrize("boundary", BOUNDARIES)
def test_every_run_command_boundary_rolls_back_atomically(
    operation: str, boundary: str
) -> None:
    _, repository, command, invoke, known_run_id = _operation(operation)
    before_streams = {
        known_run_id: repository.events(known_run_id)
    } if known_run_id else {}
    before_checkpoints = {
        known_run_id: repository.list_checkpoints(known_run_id)
    } if known_run_id else {}
    repository.inject_next_run_command_commit_failure(boundary)

    with pytest.raises(AtomicCommitFailed):
        invoke(command)

    assert repository.get_command_record(command.command_id) is None
    if known_run_id is None:
        assert repository.stream_count == 0
    else:
        assert repository.events(known_run_id) == before_streams[known_run_id]
        assert repository.list_checkpoints(known_run_id) == before_checkpoints[known_run_id]

    receipt = invoke(command)
    assert receipt.command_id == command.command_id
    assert repository.get_command_record(command.command_id).result == receipt
