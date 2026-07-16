from __future__ import annotations

import pytest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.evidence_saturation_commands import SaturationCommandRejected
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from tests.stories.st_01_04 import build_context, evaluation_command


class FailOnceSink:
    def __init__(self) -> None:
        self.calls = 0
        self.delivered = []

    def emit(self, observation) -> None:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("injected observation delivery failure")
        self.delivered.append(observation)


@pytest.mark.parametrize("actor_id", ["architect-1", "agent-1", "external-1", "expired-code", "unknown"])
def test_non_code_or_unauthorized_actor_fails_before_commit(actor_id: str) -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    with pytest.raises((AuthorityDenied, SaturationCommandRejected)):
        service.evaluate(evaluation_command(run_id, contract, actor_id=actor_id))
    assert repository.saturation_evaluation_count == 0
    assert repository.event_count(run_id) == 6


def test_stale_version_and_altered_index_fail_closed() -> None:
    service, repository, _, run_id, _, index_receipt, contract = build_context()
    with pytest.raises(SaturationCommandRejected):
        service.evaluate(evaluation_command(run_id, contract, expected_version=5))
    repository._evidence_indexes[index_receipt.index_id] = None  # type: ignore[index,assignment]
    with pytest.raises(SaturationCommandRejected):
        service.evaluate(evaluation_command(run_id, contract, command_id="altered-index"))
    assert repository.saturation_evaluation_count == 0


def test_atomic_failure_leaves_zero_partial_state() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    repository.inject_next_atomic_commit_failure()
    with pytest.raises(AtomicCommitFailed):
        service.evaluate(evaluation_command(run_id, contract))
    assert repository.event_count(run_id) == 6
    assert repository.saturation_evaluation_count == 0
    assert repository.saturation_receipt_count == 0
    assert repository.get_command_record("saturation-command-1") is None


def test_post_commit_observation_failure_returns_committed_receipt_and_retries() -> None:
    sink = FailOnceSink()
    service, repository, _, run_id, _, _, contract = build_context(observations=sink)
    receipt = service.evaluate(evaluation_command(run_id, contract))
    assert repository.get_saturation_evaluation(receipt.evaluation_id) is not None
    assert repository.pending_observations(receipt.command_id)
    replay = service.evaluate(evaluation_command(run_id, contract))
    assert replay == receipt
    assert repository.pending_observations(receipt.command_id) == ()
    assert repository.delivered_observations(receipt.command_id)


def test_duplicate_command_is_payload_safe_and_code_cannot_apply_waiver() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    assert service.evaluate(evaluation_command(run_id, contract)) == receipt
    assert repository.saturation_evaluation_count == 1
    with pytest.raises(IdempotencyPayloadMismatch):
        service.evaluate(evaluation_command(run_id, contract, actor_id="architect-1"))

    service2, _, _, run_id2, _, _, contract2 = build_context(seed="waiver")
    with pytest.raises(SaturationCommandRejected):
        service2.evaluate(
            evaluation_command(run_id2, contract2, human_waiver_ref="invented-waiver")
        )
