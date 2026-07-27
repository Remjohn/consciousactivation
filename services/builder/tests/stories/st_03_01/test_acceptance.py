from dataclasses import asdict

import pytest

from cmf_builder.application.genesis_question_commands import GenesisQuestionCommandRejected
from cmf_builder.domain.genesis_questions import DecisionNodeStatus
from tests.stories.st_03_01 import build_context, open_command


def test_opens_exactly_one_dependency_ready_question_with_complete_recommendation():
    service, repository, _, run_id = build_context()
    receipt = service.open(open_command(repository, run_id))
    package = repository.get_genesis_question_package(receipt.package_id)
    graph = repository.get_decision_graph(receipt.graph_id)
    assert receipt.outcome == "PASS"
    assert package.selected_decision_id == "phase_hypotheses"
    assert sum(node.status is DecisionNodeStatus.SELECTED for node in graph.nodes) == 1
    assert graph.nodes[1].status is DecisionNodeStatus.LOCKED
    assert graph.nodes[1].missing_dependencies == ("phase_hypotheses",)
    assert package.recommendation.authority_statement == "ADVISORY_NOT_HUMAN_RATIFICATION"
    assert {item.option_id for item in package.recommendation.alternatives} == {"minimal_linear_phases", "defer_phase_design"}


def test_package_cannot_contain_human_answer_ratification_or_ir_mutation():
    service, repository, _, run_id = build_context()
    receipt = service.open(open_command(repository, run_id))
    payload = asdict(repository.get_genesis_question_package(receipt.package_id))
    forbidden = {"human_answer", "final_value", "ratified", "signed_at", "harness_ir_mutation"}
    assert forbidden.isdisjoint(key.lower() for key in payload)


def test_second_active_question_fails_closed():
    service, repository, _, run_id = build_context()
    service.open(open_command(repository, run_id))
    with pytest.raises(GenesisQuestionCommandRejected):
        service.open(open_command(repository, run_id, command_id="genesis-question-command-2", expected_version=12))
