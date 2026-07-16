from __future__ import annotations

from cmf_builder.domain.evidence_saturation import SaturationContract
from tests.stories.st_01_04 import (
    build_context,
    evaluation_command,
    invalidation_command,
)


def test_fresh_context_produces_byte_identical_evaluation_and_receipt() -> None:
    first_service, first_repo, _, first_run, _, _, first_contract = build_context(seed="same")
    second_service, second_repo, _, second_run, _, _, second_contract = build_context(seed="same")
    first_receipt = first_service.evaluate(evaluation_command(first_run, first_contract))
    second_receipt = second_service.evaluate(evaluation_command(second_run, second_contract))
    first = first_repo.get_saturation_evaluation(first_receipt.evaluation_id)
    second = second_repo.get_saturation_evaluation(second_receipt.evaluation_id)
    assert first is not None and second is not None
    assert first.canonical_bytes() == second.canonical_bytes()
    assert first_receipt.canonical_bytes() == second_receipt.canonical_bytes()


def test_changed_contract_produces_new_immutable_identity() -> None:
    _, repository, _, run_id, source_receipt, index_receipt, contract = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    index = repository.get_evidence_index(index_receipt.index_id)
    assert lock is not None and index is not None
    changed = SaturationContract.create(
        contract_id="changed-contract-v2",
        source_profile_ref=lock.source_profile_ref,
        required_roles=("governed_task_definition",),
        minimum_distinct_source_ids=2,
    )
    from cmf_builder.domain.evidence_saturation import SaturationEvaluation
    first = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract, authority_identity="code-1"
    )
    second = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=changed, authority_identity="code-1"
    )
    assert first.evaluation_id != second.evaluation_id
    assert first.evaluation_hash != second.evaluation_hash


def test_invalidation_preserves_historical_reproduction_and_clears_active_state() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    evaluation = repository.get_saturation_evaluation(receipt.evaluation_id)
    assert evaluation is not None
    before = evaluation.canonical_bytes()
    invalidation = service.invalidate(invalidation_command(run_id, evaluation.evaluation_id))
    run = repository.load_run(run_id)
    assert run.saturation_evaluation_ref == evaluation.evaluation_id
    assert run.saturation_evaluation_invalidation_ref == invalidation.invalidation_id
    assert repository.is_saturation_evaluation_invalidated(evaluation.evaluation_id)
    assert repository.active_saturation_evaluation(run_id) is None
    historical = repository.get_saturation_evaluation(evaluation.evaluation_id)
    assert historical is not None and historical.canonical_bytes() == before
    assert repository.get_saturation_invalidation(invalidation.invalidation_id) == invalidation


def test_run_replay_preserves_saturation_identity_and_state_hash() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    service.evaluate(evaluation_command(run_id, contract))
    loaded = repository.load_run(run_id)
    from cmf_builder.domain.run import Run
    replayed = Run.replay(repository.events(run_id))
    assert replayed == loaded
    assert replayed.state_hash() == loaded.state_hash()
    assert replayed.state_hash_at(replayed.stream_version) == loaded.state_hash()
