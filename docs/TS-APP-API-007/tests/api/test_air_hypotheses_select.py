from __future__ import annotations

from fastapi.testclient import TestClient

from cmf_activative_intelligence.production_domain import EVALUATION_DIMENSIONS, HYPOTHESIS_GATES
from tests.api.fixtures.air_portfolio_fixture import AUTHORITY, build_portfolio_fixture


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def _judgment(hid: str, producer: str, all_pass: bool, score: int) -> dict:
    return {
        "hypothesis_id": hid,
        "producer_actor_id": producer,
        "gate_outcomes": {gate: all_pass for gate in HYPOTHESIS_GATES},
        "dimension_scores_micros": {dim: score for dim in EVALUATION_DIMENSIONS},
    }


def _select_body(fx: dict, *, selected: str, judgments: list[dict], idempotency_key: str) -> dict:
    return {
        "idempotency_key": idempotency_key,
        "authority": AUTHORITY,
        "selected_hypothesis_id": selected,
        "evaluator_actor_id": "dev:evaluator",
        "candidate_judgments": judgments,
        "gate_profile_ref": fx["gate_profile_ref"],
        "evaluation_profile_ref": fx["evaluation_profile_ref"],
        "evidence_refs": fx["evidence_refs"],
        "matrix_of_edging_ref": fx["matrix_of_edging_ref"],
        "role_tension_ref": fx["role_tension_ref"],
        "source_refs": fx["source_refs"],
        "authority_decision_ref": fx["authority_decision_ref"],
        "decisive_margin_micros": 100_000,
        "diversity_exhausted": False,
    }


def test_ac003_decisive_winner_promotes_portfolio(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac003")
        h1, h2, h3 = fx["hypothesis_ids"]
        judgments = [
            _judgment(h1, "p1", True, 900_000),
            _judgment(h2, "p2", False, 500_000),
            _judgment(h3, "p3", False, 500_000),
        ]
        body = _select_body(fx, selected=h1, judgments=judgments, idempotency_key="ac003-select")

        response = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=body)
        assert response.status_code == 200
        payload = response.json()
        assert payload["decision"] == "DECISIVE_WINNER"
        assert payload["stop_reason"] == "DECISIVE_ELIGIBLE_WINNER"
        assert payload["portfolio"]["portfolio_state"] == "PROMOTED"


def test_ac004_replay_with_identical_idempotency_key_is_idempotent(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac004")
        h1, h2, h3 = fx["hypothesis_ids"]
        judgments = [
            _judgment(h1, "p1", True, 900_000),
            _judgment(h2, "p2", False, 500_000),
            _judgment(h3, "p3", False, 500_000),
        ]
        body = _select_body(fx, selected=h1, judgments=judgments, idempotency_key="ac004-select")

        first = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=body)
        assert first.status_code == 200
        before = len(air.repository.list_current(object_type="hypothesis_gate_result"))
        before_comparisons = len(air.repository.list_current(object_type="comparative_evaluation_receipt"))

        second = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=body)
        assert second.status_code == 200
        after = len(air.repository.list_current(object_type="hypothesis_gate_result"))
        after_comparisons = len(air.repository.list_current(object_type="comparative_evaluation_receipt"))

        assert after == before == 3
        assert after_comparisons == before_comparisons == 1
        assert second.json()["promotion_ref"] == first.json()["promotion_ref"]
        assert second.json() == first.json()


def test_ac005_incomplete_judgments_rejected_with_no_writes(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac005")
        h1, h2, h3 = fx["hypothesis_ids"]
        judgments = [_judgment(h1, "p1", True, 900_000), _judgment(h2, "p2", False, 500_000)]  # h3 missing
        body = _select_body(fx, selected=h1, judgments=judgments, idempotency_key="ac005-select")

        revision_before = air.repository.get_object(fx["portfolio_id"]).revision
        response = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=body)
        assert response.status_code == 422
        assert response.json()["detail"]["error_code"] == "CANDIDATE_JUDGMENTS_INCOMPLETE"
        revision_after = air.repository.get_object(fx["portfolio_id"]).revision
        assert revision_after == revision_before


def test_ac006_ambiguous_scores_rejected_with_no_writes_past_comparison(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac006")
        h1, h2, h3 = fx["hypothesis_ids"]
        judgments = [
            _judgment(h1, "p1", True, 700_000),
            _judgment(h2, "p2", True, 690_000),  # within decisive_margin_micros of h1 -> AMBIGUOUS
            _judgment(h3, "p3", False, 100_000),
        ]
        body = _select_body(fx, selected=h1, judgments=judgments, idempotency_key="ac006-select")

        response = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=body)
        assert response.status_code == 409
        assert response.json()["detail"]["error_code"] == "SELECTION_NOT_SUPPORTED_BY_SCORES"

        assert list(air.repository.list_current(object_type="hypothesis_stopping_receipt")) == []
        assert list(air.repository.list_current(object_type="planned_activative_intelligence_pack")) == []
        assert list(air.repository.list_current(object_type="hypothesis_promotion_receipt")) == []
        assert air.repository.get_object(fx["portfolio_id"]).payload["portfolio_state"] == "OPEN"


def test_ac007_select_against_already_promoted_portfolio_returns_409(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="ac007")
        h1, h2, h3 = fx["hypothesis_ids"]
        judgments = [
            _judgment(h1, "p1", True, 900_000),
            _judgment(h2, "p2", False, 500_000),
            _judgment(h3, "p3", False, 500_000),
        ]
        first_body = _select_body(fx, selected=h1, judgments=judgments, idempotency_key="ac007-select-1")
        first = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=first_body)
        assert first.status_code == 200

        # A genuinely different attempt (different idempotency_key AND a
        # different authority_decision_ref) against the now-PROMOTED
        # portfolio -- must be rejected, not silently treated as a replay.
        second_body = _select_body(fx, selected=h2, judgments=judgments, idempotency_key="ac007-select-2")
        second_body["authority_decision_ref"] = {**fx["authority_decision_ref"], "sha256": "c" * 64}
        second = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=second_body)
        assert second.status_code == 409
        assert second.json()["detail"]["error_code"] == "PORTFOLIO_NOT_OPEN"


def test_replay_match_checks_judgment_content_not_just_selected_id(tmp_path, monkeypatch):
    """Regression test for a gap found during review of the AC-004 replay
    fix: a request with a different idempotency_key that happens to name the
    same selected_hypothesis_id and reuse (or collide on) the same
    authority_decision_ref, but carries genuinely different
    candidate_judgments, must NOT be silently served the stale cached
    result -- it must be rejected like any other non-matching attempt
    against an already-promoted portfolio.
    """
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_portfolio_fixture(air, prefix="replaycheck")
        h1, h2, h3 = fx["hypothesis_ids"]

        first_judgments = [
            _judgment(h1, "p1", True, 900_000),
            _judgment(h2, "p2", False, 500_000),
            _judgment(h3, "p3", False, 500_000),
        ]
        first_body = _select_body(fx, selected=h1, judgments=first_judgments, idempotency_key="replaycheck-1")
        first = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=first_body)
        assert first.status_code == 200

        # Same selected_hypothesis_id and same authority_decision_ref as the
        # first call, but a different idempotency_key AND different
        # candidate_judgments (h1's own gates now fail). This must not be
        # treated as a replay of the first call.
        different_judgments = [
            _judgment(h1, "p1", False, 100_000),
            _judgment(h2, "p2", True, 900_000),
            _judgment(h3, "p3", False, 500_000),
        ]
        second_body = _select_body(fx, selected=h1, judgments=different_judgments, idempotency_key="replaycheck-2-different")
        second = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=second_body)
        assert second.status_code == 409
        assert second.json()["detail"]["error_code"] == "PORTFOLIO_NOT_OPEN"

        # Sanity check: a genuinely identical-content replay under a
        # *different* idempotency_key still succeeds (content-addressed
        # replay is intentionally broader than strict idempotency-key
        # equality -- see _matches_existing_promotion's docstring).
        identical_content_body = _select_body(fx, selected=h1, judgments=first_judgments, idempotency_key="replaycheck-3-same-content")
        third = client.post(f"/api/air/hypotheses/{fx['portfolio_id']}/select", json=identical_content_body)
        assert third.status_code == 200
        assert third.json()["promotion_ref"] == first.json()["promotion_ref"]
