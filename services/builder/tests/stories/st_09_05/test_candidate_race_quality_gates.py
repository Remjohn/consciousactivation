import pytest

from cmf_builder.workflow.candidate_routing import (
    CandidateAction,
    CandidateAuthority,
    CandidateCommand,
    CandidateDeclaration,
    CandidateEvaluation,
    CandidateRacePlan,
    CandidateRoutingError,
    GateStatus,
    compute_selection_payload_sha256,
    select_candidate,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def authority():
    return CandidateAuthority("authority", "1.0", digest("auth"), tuple(CandidateAction), ("*",))


def candidate(cid, sandbox=None):
    return CandidateDeclaration(cid, digest(f"out:{cid}"), digest("input-contract"), digest("output-contract"), digest(f"lineage:{cid}"), sandbox or f"sandbox:{cid}")


def plan(*candidates):
    auth = authority()
    return CandidateRacePlan(
        "race:1",
        "1.0",
        "profile:workflow",
        "node:1",
        digest("input-contract"),
        digest("output-contract"),
        candidates or (candidate("a"), candidate("b")),
        digest("evaluator-policy"),
        digest("minimum-view"),
        "quality>=80",
        "cost<=budget",
        "latency<=budget",
        "budget:offline",
        4,
        "score_then_candidate_id",
        auth.authority_identity,
    )


def evaluation(cid, score=90, status=GateStatus.PASS):
    return CandidateEvaluation(cid, digest("evaluator-policy"), digest("rubric"), (digest(f"evidence:{cid}"),), status, GateStatus.PASS, GateStatus.PASS, GateStatus.PASS, score, digest("authority"))


def test_candidate_selection_waits_for_all_evaluations_and_quality_gates():
    race = plan()
    auth = authority()
    evaluations = (evaluation("a", 90), evaluation("b", 95))
    command = CandidateCommand("select", CandidateAction.SELECT, race.race_identity, compute_selection_payload_sha256(race, evaluations), auth.authority_identity)

    receipt = select_candidate(race, evaluations, command, auth)

    assert receipt.winner_candidate_id == "b"
    assert receipt.no_first_completion_shortcut is True


def test_missing_evaluation_or_gate_failure_produces_no_winner():
    race = plan()
    auth = authority()
    one_eval = (evaluation("a"),)
    command = CandidateCommand("select", CandidateAction.SELECT, race.race_identity, compute_selection_payload_sha256(race, one_eval), auth.authority_identity)
    with pytest.raises(CandidateRoutingError) as missing:
        select_candidate(race, one_eval, command, auth)
    assert missing.value.code == "MISSING_REQUIRED_EVALUATION"

    failed = (evaluation("a"), evaluation("b", status=GateStatus.FAIL))
    command = CandidateCommand("select", CandidateAction.SELECT, race.race_identity, compute_selection_payload_sha256(race, failed), auth.authority_identity)
    with pytest.raises(CandidateRoutingError) as failed_gate:
        select_candidate(race, failed, command, auth)
    assert failed_gate.value.code == "CANDIDATE_GATE_FAILED"


def test_candidate_contract_or_sandbox_independence_mismatch_fails_closed():
    bad_contract = CandidateDeclaration("bad", digest("out"), digest("other-input"), digest("output-contract"), digest("lineage"), "sandbox:bad")
    with pytest.raises(CandidateRoutingError) as contract:
        plan(candidate("a"), bad_contract)
    assert contract.value.code == "CANDIDATE_CONTRACT_MISMATCH"

    with pytest.raises(CandidateRoutingError) as sandbox:
        plan(candidate("a", "same-sandbox"), candidate("b", "same-sandbox"))
    assert sandbox.value.code == "CANDIDATE_SANDBOX_NOT_INDEPENDENT"
