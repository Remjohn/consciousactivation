import pytest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.genesis_decision_commands import GenesisDecisionCommandRejected
from tests.stories.st_03_02 import build_context, record_command, reopen_command


def test_reopen_invalidates_active_memory_and_preserves_historical_bytes():
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    memory = repository.get_genesis_decision_memory(receipt.memory_id)
    before = memory.canonical_bytes()
    invalidation = service.reopen(reopen_command(repository, run_id, memory.memory_id))
    assert repository.active_genesis_decision_memory(run_id) is None
    assert repository.get_genesis_decision_memory(memory.memory_id).canonical_bytes() == before
    assert invalidation.affected_amendment_ids == memory.amendment_refs
    assert set(invalidation.affected_descendant_decision_ids) == {"runtime_hypotheses", "evaluation_hypotheses"}


@pytest.mark.parametrize("actor", ["code-1", "agent-1", "other-human"])
def test_only_exact_human_authority_may_reopen(actor):
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    with pytest.raises((AuthorityDenied, GenesisDecisionCommandRejected)):
        service.reopen(reopen_command(repository, run_id, receipt.memory_id, actor_id=actor))


def test_reopen_command_replay_is_idempotent():
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    command = reopen_command(repository, run_id, receipt.memory_id)
    first = service.reopen(command)
    assert service.reopen(command) == first
