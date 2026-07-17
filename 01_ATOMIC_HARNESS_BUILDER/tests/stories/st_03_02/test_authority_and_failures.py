from dataclasses import replace
import pytest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.genesis_decision_commands import GenesisDecisionCommandRejected
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.genesis_decisions import GenesisDecisionInvalid
from tests.stories.st_03_02 import build_context, record_command


@pytest.mark.parametrize("actor", ["code-1", "agent-1", "other-human", "expired-human", "unknown"])
def test_non_authorized_or_non_human_actor_cannot_ratify(actor):
    service, repository, _, run_id, question = build_context()
    with pytest.raises((AuthorityDenied, GenesisDecisionCommandRejected)):
        service.record(record_command(repository, run_id, question.package_id, actor_id=actor))


def test_option_outside_governed_question_fails_closed():
    service, repository, _, run_id, question = build_context()
    with pytest.raises(GenesisDecisionInvalid):
        service.record(record_command(repository, run_id, question.package_id, selected_option="invented"))


def test_atomic_failure_leaves_zero_partial_state():
    service, repository, _, run_id, question = build_context()
    before = repository.event_count(run_id)
    repository.inject_next_atomic_commit_failure()
    with pytest.raises(AtomicCommitFailed):
        service.record(record_command(repository, run_id, question.package_id))
    assert repository.event_count(run_id) == before
    assert repository.genesis_decision_memory_count == 0
    assert repository.get_command_record("genesis-decision-command-1") is None


def test_duplicate_retry_is_safe_but_new_replayed_approval_is_rejected():
    service, repository, _, run_id, question = build_context()
    command = record_command(repository, run_id, question.package_id)
    first = service.record(command)
    assert service.record(command) == first
    with pytest.raises(GenesisDecisionCommandRejected):
        service.record(replace(command, command_id="another-approval", expected_version=13))


def test_conflicting_duplicate_payload_fails_closed():
    service, repository, _, run_id, question = build_context()
    command = record_command(repository, run_id, question.package_id)
    service.record(command)
    with pytest.raises(IdempotencyPayloadMismatch):
        service.record(replace(command, rationale="changed"))
