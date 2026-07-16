from __future__ import annotations

import pytest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.evidence_index_commands import EvidenceIndexCommandRejected
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from tests.stories.st_01_03 import build_context, index_command


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
    service, repository, _, run_id, _ = build_context()
    with pytest.raises((AuthorityDenied, EvidenceIndexCommandRejected)):
        service.index(index_command(run_id, actor_id=actor_id))
    assert repository.evidence_index_count == 0
    assert repository.event_count(run_id) == 5


def test_stale_version_and_altered_source_lock_fail_closed() -> None:
    service, repository, _, run_id, _ = build_context()
    with pytest.raises(EvidenceIndexCommandRejected):
        service.index(index_command(run_id, expected_version=4))
    repository._source_locks[repository.load_run(run_id).source_lock_ref] = None  # type: ignore[index,assignment]
    with pytest.raises(EvidenceIndexCommandRejected):
        service.index(index_command(run_id, command_id="altered-lock"))
    assert repository.evidence_index_count == 0


def test_atomic_failure_leaves_zero_partial_state() -> None:
    service, repository, _, run_id, _ = build_context()
    repository.inject_next_atomic_commit_failure()
    with pytest.raises(AtomicCommitFailed):
        service.index(index_command(run_id))
    assert repository.event_count(run_id) == 5
    assert repository.evidence_index_count == 0
    assert repository.evidence_index_receipt_count == 0
    assert repository.get_command_record("evidence-index-command-1") is None


def test_post_commit_observation_failure_returns_committed_receipt_and_retries() -> None:
    sink = FailOnceSink()
    service, repository, _, run_id, _ = build_context(observations=sink)
    receipt = service.index(index_command(run_id))
    assert repository.get_evidence_index(receipt.index_id) is not None
    assert repository.pending_observations(receipt.command_id)
    replay = service.index(index_command(run_id))
    assert replay == receipt
    assert repository.pending_observations(receipt.command_id) == ()
    assert repository.delivered_observations(receipt.command_id)


def test_duplicate_command_is_payload_safe() -> None:
    service, repository, _, run_id, _ = build_context()
    receipt = service.index(index_command(run_id))
    assert service.index(index_command(run_id)) == receipt
    assert repository.evidence_index_count == 1
    assert repository.event_count(run_id) == 6
    with pytest.raises(IdempotencyPayloadMismatch):
        service.index(index_command(run_id, actor_id="architect-1"))
