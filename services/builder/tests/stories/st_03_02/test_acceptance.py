def test_human_answer_decision_amendment_and_memory_commit_separately():
    from tests.stories.st_03_02 import build_context, record_command
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    memory = repository.get_genesis_decision_memory(receipt.memory_id)
    assert receipt.answer_id != receipt.final_decision_id
    assert receipt.final_decision_id != receipt.amendment_id
    assert memory.resolved_decision_ids == ("phase_hypotheses",)
    assert memory.ready_decision_ids == ("runtime_hypotheses",)
    assert memory.locked_decision_ids == ()
    assert memory.cascade_status.value == "PARTIALLY_RATIFIED"
    assert repository.load_run(run_id).genesis_decision_memory_ref == memory.memory_id


def test_provisional_draft_does_not_replace_human_ratification():
    from tests.stories.st_03_02 import build_context, record_command
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    assert receipt.authority_identity == "architect-1"
    assert receipt.final_decision_hash.startswith("sha256:")
    assert receipt.amendment_hash.startswith("sha256:")


def test_resume_returns_memory_without_replaying_answer():
    from tests.stories.st_03_02 import build_context, record_command
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    before = repository.event_count(run_id)
    memory = service.resume(run_id=run_id, actor_id="architect-1", correlation_id="resume", causation_id=receipt.receipt_id)
    assert memory.memory_id == receipt.memory_id
    assert repository.event_count(run_id) == before
