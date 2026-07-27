from __future__ import annotations

from cmf_builder.domain.evidence_saturation import (
    DownstreamConsequence,
    SaturationOutcome,
)
from tests.stories.st_01_04 import build_context, evaluation_command


def test_complete_category_neutral_evidence_issues_pass_and_proceed() -> None:
    service, repository, _, run_id, source_receipt, index_receipt, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    evaluation = repository.get_saturation_evaluation(receipt.evaluation_id)
    run = repository.load_run(run_id)

    assert evaluation is not None
    assert evaluation.outcome is SaturationOutcome.PASS
    assert evaluation.downstream_consequence is DownstreamConsequence.PROCEED
    assert evaluation.gaps == ()
    assert evaluation.authority_conflicts == ()
    assert evaluation.source_lock_ref == source_receipt.source_lock_ref
    assert evaluation.evidence_index_ref == index_receipt.index_id
    assert run.saturation_evaluation_ref == evaluation.evaluation_id
    assert run.saturation_evaluation_hash == evaluation.evaluation_hash
    assert not evaluation.production_eligible and not evaluation.certified


def test_coverage_matrix_binds_required_role_and_exact_specimen() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    evaluation = repository.get_saturation_evaluation(receipt.evaluation_id)
    assert evaluation is not None
    coverage = evaluation.role_coverage
    assert len(coverage) == 1
    assert coverage[0].role == "governed_task_definition"
    assert coverage[0].status == "COMPLETE"
    assert coverage[0].required_count == coverage[0].observed_count == 1
    assert len(coverage[0].specimen_ids) == len(coverage[0].source_ids) == 1


def test_receipt_event_and_contract_bind_exact_outcome() -> None:
    service, repository, _, run_id, _, _, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    evaluation = repository.get_saturation_evaluation(receipt.evaluation_id)
    assert evaluation is not None
    receipt.validate(evaluation)
    assert repository.get_saturation_receipt(receipt.receipt_id) == receipt
    event = repository.load_run(run_id).events[-1]
    assert event.event_type == "SaturationEvaluationAttached"
    assert event.value("evaluation_ref") == evaluation.evaluation_id
    assert event.value("contract_hash") == contract.contract_hash
    assert event.value("outcome") == "PASS"
    assert event.value("downstream_consequence") == "PROCEED"
