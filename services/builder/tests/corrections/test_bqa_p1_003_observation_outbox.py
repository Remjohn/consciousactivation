from __future__ import annotations

from cmf_builder.adapters.in_memory_run_repository import RecordingObservationSink
from tests.stories.st_07_04 import build_context, validation_command


class FailBeforeAcceptanceSink:
    def __init__(self) -> None:
        self.attempts = 0

    def emit(self, observation) -> None:
        self.attempts += 1
        raise RuntimeError("observation_sink_unavailable_before_acceptance")


class AcceptThenFailBeforeNextSink:
    def __init__(self, accepted: int) -> None:
        self.accepted_limit = accepted
        self.accepted = []

    def emit(self, observation) -> None:
        if len(self.accepted) >= self.accepted_limit:
            raise RuntimeError("observation_sink_unavailable_before_acceptance")
        self.accepted.append(observation)


def test_post_commit_sink_failure_returns_receipt_and_leaves_queryable_outbox() -> None:
    service, _, _, repository, _, run_id, _, _ = build_context(
        seed="BQA-P1-003"
    )
    failing = FailBeforeAcceptanceSink()
    service._observations = failing
    command = validation_command(run_id)

    receipt = service.validate(command)

    assert receipt.outcome == "SYNTHETIC_ATOMIC_CONTENT_HARNESS_VALIDATED"
    assert repository.load_run(run_id).atomic_content_harness_validation_ref
    assert repository.get_command_record(command.command_id).result == receipt
    pending = repository.pending_observations(command.command_id)
    delivered = repository.delivered_observations(command.command_id)
    assert len(pending) == 10
    assert delivered == ()
    assert failing.attempts == 1
    assert all(item.outcome == "PASS" for item in pending)
    assert all(
        item.atomic_content_harness_replay_status == "NEW_COMMIT"
        for item in pending
    )


def test_duplicate_retries_only_pending_observations_and_returns_original_receipt() -> None:
    service, _, _, repository, _, run_id, _, _ = build_context(
        seed="BQA-P1-003-retry"
    )
    failing = FailBeforeAcceptanceSink()
    service._observations = failing
    command = validation_command(run_id)
    first = service.validate(command)

    healthy = RecordingObservationSink()
    service._observations = healthy
    second = service.validate(command)
    third = service.validate(command)

    assert second == first == third
    assert repository.pending_observations(command.command_id) == ()
    assert len(repository.delivered_observations(command.command_id)) == 10
    delivered_new_commit = [
        item
        for item in healthy.observations
        if item.atomic_content_harness_replay_status == "NEW_COMMIT"
    ]
    replay = [
        item
        for item in healthy.observations
        if item.event_name == "atomic_content_harness_validation_replayed"
    ]
    assert len(delivered_new_commit) == 10
    assert len(replay) == 2


def test_partial_delivery_retries_only_unacknowledged_intents() -> None:
    service, _, _, repository, _, run_id, _, _ = build_context(
        seed="BQA-P1-003-partial"
    )
    partial = AcceptThenFailBeforeNextSink(accepted=3)
    service._observations = partial
    command = validation_command(run_id)
    receipt = service.validate(command)

    assert len(repository.delivered_observations(command.command_id)) == 3
    assert len(repository.pending_observations(command.command_id)) == 7

    healthy = RecordingObservationSink()
    service._observations = healthy
    assert service.validate(command) == receipt
    assert len(healthy.observations) == 8  # seven pending plus one replay notice
    assert repository.pending_observations(command.command_id) == ()
    assert len(repository.delivered_observations(command.command_id)) == 10
