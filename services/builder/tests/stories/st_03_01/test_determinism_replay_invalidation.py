from tests.stories.st_03_01 import build_context, invalidation_command, open_command


def test_fresh_contexts_produce_byte_identical_package_receipt_and_graph():
    left, left_repo, _, left_run = build_context(seed="fresh")
    right, right_repo, _, right_run = build_context(seed="fresh")
    left_receipt = left.open(open_command(left_repo, left_run))
    right_receipt = right.open(open_command(right_repo, right_run))
    left_package = left_repo.get_genesis_question_package(left_receipt.package_id)
    right_package = right_repo.get_genesis_question_package(right_receipt.package_id)
    assert left_package.canonical_bytes() == right_package.canonical_bytes()
    assert left_receipt == right_receipt
    assert left_repo.get_decision_graph(left_receipt.graph_id) == right_repo.get_decision_graph(right_receipt.graph_id)


def test_invalidation_clears_active_state_and_preserves_history():
    service, repository, _, run_id = build_context()
    receipt = service.open(open_command(repository, run_id))
    package = repository.get_genesis_question_package(receipt.package_id)
    canonical = package.canonical_bytes()
    invalidation = service.invalidate(invalidation_command(repository, run_id, package.package_id))
    assert repository.active_genesis_question(run_id) is None
    assert repository.get_genesis_question_invalidation(invalidation.invalidation_id) == invalidation
    assert repository.get_genesis_question_package(package.package_id).canonical_bytes() == canonical
    assert repository.load_run(run_id).genesis_question_invalidation_ref == invalidation.invalidation_id


def test_invalidation_replay_is_payload_safe():
    service, repository, _, run_id = build_context()
    receipt = service.open(open_command(repository, run_id))
    command = invalidation_command(repository, run_id, receipt.package_id)
    first = service.invalidate(command)
    second = service.invalidate(command)
    assert first == second
