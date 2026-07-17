from tests.stories.st_03_02 import build_context, record_command


def test_fresh_contexts_produce_identical_receipts_and_memory_bytes():
    left, left_repo, _, left_run, left_question = build_context(seed="fresh")
    right, right_repo, _, right_run, right_question = build_context(seed="fresh")
    left_receipt = left.record(record_command(left_repo, left_run, left_question.package_id))
    right_receipt = right.record(record_command(right_repo, right_run, right_question.package_id))
    assert left_receipt == right_receipt
    assert left_repo.get_genesis_decision_memory(left_receipt.memory_id).canonical_bytes() == right_repo.get_genesis_decision_memory(right_receipt.memory_id).canonical_bytes()


def test_receipt_and_memory_are_hash_bound_and_run_attributable():
    service, repository, _, run_id, question = build_context()
    receipt = service.record(record_command(repository, run_id, question.package_id))
    memory = repository.get_genesis_decision_memory(receipt.memory_id)
    assert receipt.run_id == run_id
    assert receipt.memory_hash == memory.memory_hash
    assert receipt.authority_identity == memory.authority_identity == "architect-1"
    assert memory.graph_ref == question.graph_id
