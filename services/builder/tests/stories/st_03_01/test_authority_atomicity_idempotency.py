from dataclasses import replace

import pytest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.genesis_question_commands import GenesisQuestionCommandRejected
from tests.stories.st_03_01 import build_context, open_command


def test_duplicate_command_returns_original_receipt_without_duplicate_state():
    service, repository, _, run_id = build_context()
    command = open_command(repository, run_id)
    first = service.open(command)
    second = service.open(command)
    assert second == first
    assert repository.genesis_question_count == 1
    assert repository.genesis_question_receipt_count == 1


def test_conflicting_duplicate_payload_fails_closed():
    service, repository, _, run_id = build_context()
    command = open_command(repository, run_id)
    service.open(command)
    with pytest.raises(IdempotencyPayloadMismatch):
        service.open(replace(command, facts=(*command.facts, "changed")))


@pytest.mark.parametrize("actor_id", ["architect-1", "agent-1", "unknown"])
def test_only_registered_code_authority_may_open_question(actor_id):
    service, repository, _, run_id = build_context()
    with pytest.raises((AuthorityDenied, GenesisQuestionCommandRejected)):
        service.open(open_command(repository, run_id, actor_id=actor_id))


def test_atomic_failure_leaves_no_partial_governed_state():
    service, repository, _, run_id = build_context()
    before_events = repository.event_count(run_id)
    repository.inject_next_atomic_commit_failure()
    with pytest.raises(AtomicCommitFailed):
        service.open(open_command(repository, run_id))
    assert repository.event_count(run_id) == before_events
    assert repository.genesis_question_count == 0
    assert repository.genesis_question_receipt_count == 0
    assert repository.get_command_record("genesis-question-command-1") is None
