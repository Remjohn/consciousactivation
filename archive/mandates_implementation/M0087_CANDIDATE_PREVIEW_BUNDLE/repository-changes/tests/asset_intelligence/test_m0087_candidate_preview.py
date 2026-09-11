from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "asset-intelligence" / "src"))

from cae_asset_intelligence.candidate_preview import (  # noqa: E402
    AcceptancePolicyRegistry,
    AutoAcceptanceBlockedError,
    CandidateDecision,
    CandidatePreviewCard,
    CandidatePreviewSession,
    CandidateSelectionError,
    CandidateSourceRef,
    CandidateStaleVersionError,
    NavigationDirection,
    build_portfolio,
    decide_session,
    navigate_session,
)


def _candidate(cid: str, *, confidence=9300, fit=9300, quality=8500, rights="CLEARED", eligible=True, scene="SCN-1"):
    return CandidatePreviewCard(
        candidate_id=cid,
        media_type="VIDEO_CLIP",
        preview_uri=f"https://media.test/{cid}.mp4",
        transcript_context="The source clip shows the operational turning point in context.",
        source_ref=CandidateSourceRef(object_id=cid, version="v7", sha256="a" * 64),
        source_range_ms=(1000, 5000),
        duration_ms=4000,
        rights_state=rights,
        confidence_bps=confidence,
        semantic_fit_bps=fit,
        quality_bps=quality,
        ranking=1 if cid.endswith("1") else 2,
        eligible=eligible,
        provenance={"candidate_id": cid, "scene_id": scene, "source_version": "v7", "source_sha256": "a" * 64},
        source_quality_state="HIGH",
    )


def _session(portfolio):
    return CandidatePreviewSession(
        session_id="CVS-1",
        campaign_id="camp-1",
        workspace_id="ws-1",
        target_ref={"object_id": "element-1", "version": "1", "sha256": "b" * 64},
        target_node_id="clip-1",
        request_ref={"object_id": "request-1", "version": "1", "sha256": "c" * 64},
        active_portfolio_ref={"object_id": portfolio.portfolio_id, "version": "1", "sha256": portfolio.portfolio_sha256},
        seen_candidate_ids=(portfolio.candidates[0].candidate_id,),
    )


def test_happy_path_navigation_accept_and_rejection_lineage():
    p = build_portfolio(session_id="CVS-1", request_ref={"request_id": "r1"}, candidates=[_candidate("AST-1"), _candidate("AST-2")])
    s = _session(p)
    s2 = navigate_session(s, p, direction=NavigationDirection.NEXT, expected_version=1)
    assert s2.current_index == 1
    s3, receipt, policy = decide_session(s2, p, candidate_id="AST-2", decision=CandidateDecision.ACCEPT, expected_version=2, operator_ref={"actor_type": "human", "workflow_role": "operator", "actor_id": "op-1"})
    assert s3.selected_candidate_id == "AST-2"
    assert receipt.decision == CandidateDecision.ACCEPT
    assert policy["decision"] == "PASS"


def test_good_looking_but_wrong_candidate_is_blocked_by_deterministic_policy():
    candidate = _candidate("AST-WRONG", fit=6500)
    report = AcceptancePolicyRegistry.evaluate(candidate)
    assert report["semantic_fit"] == "FAIL"
    p = build_portfolio(session_id="CVS-2", request_ref={"request_id": "r2"}, candidates=[candidate])
    with pytest.raises(AutoAcceptanceBlockedError, match="semantic_fit"):
        decide_session(_session(p), p, candidate_id="AST-WRONG", decision=CandidateDecision.AUTO_ACCEPT, expected_version=1)


def test_auto_accept_requires_rights_provenance_and_quality_gates():
    candidate = _candidate("AST-3", rights="RESTRICTED", quality=9500)
    report = AcceptancePolicyRegistry.evaluate(candidate)
    assert report["rights"] == "FAIL"
    assert report["decision"] == "BLOCKED"


def test_manual_reject_requires_human_actor_and_rationale_and_preserves_lineage():
    p = build_portfolio(session_id="CVS-3", request_ref={"request_id": "r3"}, candidates=[_candidate("AST-1"), _candidate("AST-2")])
    s = _session(p)
    with pytest.raises(CandidateSelectionError):
        decide_session(s, p, candidate_id="AST-1", decision=CandidateDecision.REJECT, expected_version=1, operator_ref={"actor_type": "model"}, rationale="wrong")
    s2, receipt, _ = decide_session(s, p, candidate_id="AST-1", decision=CandidateDecision.REJECT, expected_version=1, operator_ref={"actor_type": "human", "workflow_role": "operator", "actor_id": "op-1"}, rationale="Wrong reading despite visual quality.")
    assert "AST-1" in s2.rejected_candidate_ids
    assert any(item["candidate_id"] == "AST-1" for item in receipt.rejected_candidates)


def test_stale_and_malformed_cases_fail_closed():
    p = build_portfolio(session_id="CVS-4", request_ref={"request_id": "r4"}, candidates=[_candidate("AST-1")])
    s = _session(p)
    with pytest.raises(CandidateStaleVersionError):
        navigate_session(s, p, direction=NavigationDirection.NEXT, expected_version=99)
    with pytest.raises(CandidateSelectionError):
        decide_session(s, p, candidate_id="MISSING", decision=CandidateDecision.ACCEPT, expected_version=1, operator_ref={"actor_type": "human", "workflow_role": "operator", "actor_id": "op"})


def test_receipt_is_stable_for_same_inputs():
    p = build_portfolio(session_id="CVS-5", request_ref={"request_id": "r5"}, candidates=[_candidate("AST-1")])
    s = _session(p)
    _, first, _ = decide_session(s, p, candidate_id="AST-1", decision=CandidateDecision.AUTO_ACCEPT, expected_version=1)
    _, second, _ = decide_session(s, p, candidate_id="AST-1", decision=CandidateDecision.AUTO_ACCEPT, expected_version=1)
    assert first.receipt_sha256 == second.receipt_sha256
    assert first.receipt_id == second.receipt_id


def test_rejected_candidate_cannot_be_reaccepted_without_search_again():
    p = build_portfolio(session_id="CVS-7", request_ref={"request_id": "r7"}, candidates=[_candidate("AST-1")])
    s = _session(p)
    rejected, _, _ = decide_session(
        s, p, candidate_id="AST-1", decision=CandidateDecision.REJECT, expected_version=1,
        operator_ref={"actor_type": "human", "workflow_role": "operator", "actor_id": "op-1"},
        rationale="Wrong semantic reading.",
    )
    with pytest.raises(CandidateSelectionError, match="already rejected"):
        decide_session(
            rejected, p, candidate_id="AST-1", decision=CandidateDecision.ACCEPT, expected_version=2,
            operator_ref={"actor_type": "human", "workflow_role": "operator", "actor_id": "op-1"},
        )


def test_candidate_snapshot_is_canonical_json_safe():
    p = build_portfolio(session_id="CVS-6", request_ref={"request_id": "r6"}, candidates=[_candidate("AST-1")])
    json.dumps(p.model_dump(mode="json"), allow_nan=False)
    assert len(p.portfolio_sha256) == 64
