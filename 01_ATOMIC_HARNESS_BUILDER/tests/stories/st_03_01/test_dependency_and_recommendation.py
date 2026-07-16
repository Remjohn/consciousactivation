from dataclasses import replace

import pytest

from cmf_builder.domain.genesis_questions import DecisionDefinitionInvalid, RecommendationInvalid
from tests.stories.st_03_01 import build_context, definitions, open_command


def test_unsupported_affected_path_is_rejected_under_hg_001():
    service, repository, _, run_id = build_context()
    defs = definitions(repository, run_id)
    bad = replace(defs[0], affected_ir_paths=("fields.inputs",))
    with pytest.raises(DecisionDefinitionInvalid):
        service.open(open_command(repository, run_id, definitions=(bad, defs[1])))


def test_missing_required_evidence_locks_all_nodes_and_fails_closed():
    service, repository, _, run_id = build_context()
    with pytest.raises(DecisionDefinitionInvalid, match="No dependency-ready"):
        service.open(open_command(repository, run_id, available_evidence_refs=()))


def test_recommendation_drift_and_incomplete_alternatives_are_rejected():
    service, repository, _, run_id = build_context()
    command = open_command(repository, run_id)
    incomplete = command.alternatives[:1]
    with pytest.raises(RecommendationInvalid):
        service.open(replace(command, alternatives=incomplete))


def test_non_human_decision_authority_is_rejected():
    service, repository, _, run_id = build_context()
    defs = definitions(repository, run_id)
    bad = replace(defs[0], authority_owner="CODE")
    with pytest.raises(DecisionDefinitionInvalid):
        service.open(open_command(repository, run_id, definitions=(bad, defs[1])))
